from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram import Router
import time
from os import remove

from assistants import (
    collect_check_and_commit_user_and_message,
    collect_and_commit_message,
    update_user,
    create_csv_file
)
from keyboards import (
    markup_example, markup_another_button, markup_unload
)
import texts
from settings import admins_list
from models import session as db
from models import User


class StateMachine(StatesGroup):
    user_id = State()


router = Router()


@router.callback_query()
async def answering_callbacks(call, state: FSMContext):
    if call.data == 'button example':
        await call.message.answer(text='тупик')
    elif call.data == 'prepared text':
        await call.message.answer(text=texts.spoonfulofdust)
    elif call.data == 'unload user mesages':
        await call.message.answer(text='отправь id нужного пользователя')
        await state.set_state(StateMachine.user_id)


@router.message(Command("a"))
async def admin_command(msg: Message):
    await collect_and_commit_message(msg)
    if msg.from_user.id in admins_list:
        await msg.answer(text='админ меню', reply_markup=markup_unload)


@router.message(Command("start"))
async def command_start(msg: Message):
    await collect_check_and_commit_user_and_message(msg)
    await msg.answer(text='text', reply_markup=markup_example)
    await msg.answer_photo(
        photo=FSInputFile('files/photo/photo.jpg'),
        caption='photo w/ caption and button',
        reply_markup=markup_another_button
    )


@router.message(StateMachine.user_id)
async def create_and_send_csv(msg: Message, state: FSMContext):
    await collect_and_commit_message(msg)
    await state.clear()

    if msg.text.isdigit():
        user = msg.text
    else:
        if 'https://t.me/' in msg.text:
            user = msg.text.replace('https://t.me/', '')
            user = db.query(User).filter_by(username=user).one().user_id
        else:
            user = msg.text.replace('@', '')
            user = db.query(User).filter_by(username=user).one().user_id

    try:
        add = time.time()
        filename = f'{user} -- {add}.csv'
        create_csv_file(user_id=user, filename=filename)
        await msg.answer_document(FSInputFile(filename))
        remove(filename)
    except Exception as ex:
        ex_text = f'Возникла ошибка: {ex}'
        print(ex_text)
        await msg.answer(text=ex_text)


@router.message()
async def any_message(msg: Message):
    await update_user(msg)
    await collect_and_commit_message(msg)
    await msg.answer(text='answer to any message except start')
