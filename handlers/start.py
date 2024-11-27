from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"Ваш chat_id: {chat_id}")
    name = message.from_user.first_name
    msg = f"Привет {name}, хочешь отправить домашнее задание?"
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Отправить дз",
                callback_data="homework"
            )
            ]
        ]
    )

    await message.answer(msg, reply_markup=kb)