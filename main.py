from pyexpat.errors import messages

from bot_config import dp, bot, database
import asyncio

from handlers.start import start_router
from handlers.home_work import homework_router

async def on_startup(bot):
    database.create_tables()

async def main():
    dp.include_router(start_router)
    dp.include_router(homework_router)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())