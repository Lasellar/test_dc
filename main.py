from asyncio import run
from logging import basicConfig, INFO

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv

from handlers import router

load_dotenv()
token = getenv('TOKEN')


async def main():
    bot = Bot(
        token=token
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.fsm.close()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        skip_updates=False
    )


if __name__ == "__main__":
    basicConfig(level=INFO)
    run(main())
