from sqlalchemy.exc import NoResultFound
import csv

from models import User, Message
from models import session as db


def create_csv_file(user_id, filename):
    messages = db.query(Message).filter_by(user_id=user_id).all()
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['id', 'date', 'text', 'sticker', 'photo', 'video', 'voice']
        )
        for message in messages:
            writer.writerow(
                [
                    message.id,
                    message.date,
                    message.text,
                    message.sticker,
                    message.photo,
                    message.video,
                    message.voice
                ]
            )


async def collect_user_data(message):
    """Собирает информацию о пользователе и возвращает объект его модели."""
    _user = message.from_user
    user = User(
        user_id=_user.id,
        url=_user.url,
        username=_user.username,
        first_name=_user.first_name,
        last_name=_user.last_name,
        is_premium=_user.is_premium,
        language_code=_user.language_code
    )
    return user


async def collect_message_data(
        message, user,
        sticker=None, photo=None, video=None, voice=None
):
    """Собирает информацию о сообщении и возвращает объект его модели."""
    if message.sticker:
        sticker = message.sticker.file_unique_id
    if message.photo:
        photo = message.photo[0].file_unique_id
    if message.video:
        video = message.video.file_unique_id
    if message.voice:
        voice = message.voice.file_unique_id
    message = Message(
        user=user,
        id=message.message_id,
        date=message.date,
        text=message.text,
        sticker=sticker,
        photo=photo,
        video=video,
        voice=voice
    )
    return message


async def collect_check_and_commit_user_and_message(message):
    """
    Собирает информацию о пользователе и отправленном им сообщении.
    Если пользователя еще нет в БД, добавляет туда его и его сообщение,
    иначе добавляет только сообщение.
    """
    user = await collect_user_data(message)
    db_user = db.query(User).filter_by(user_id=user.user_id).one()
    if not db_user:
        db.add(user)
        db.commit()
        db_user = user
    message = await collect_message_data(message, db_user)
    db.add(message)
    db.commit()


async def update_user(message):
    """
    Проверят, есть ли изменения в информации о пользователе и если
    есть, то обновляет запись о нем в БД.
    Обрабатывает ситуацию, когда записи о пользователе нет в БД из-за
    того, что он не отправлял боту /start.
    """
    user = await collect_user_data(message)
    try:
        db_user = db.query(User).filter_by(user_id=message.from_user.id).one()
        if str(user) != str(db_user):
            db_user.url = user.url,
            db_user.username = user.username,
            db_user.first_name = user.first_name,
            db_user.last_name = user.last_name,
            db_user.is_premium = user.is_premium,
            db_user.language_code = user.language_code
    except NoResultFound:
        db.add(user)
    db.commit()


async def collect_and_commit_message(message):
    """Собирает информацию о сообщении пользователя и сохраняет в БД."""
    db_user = db.query(User).filter_by(user_id=message.from_user.id).one()
    message = await collect_message_data(message, db_user)
    db.add(message)
    db.commit()
