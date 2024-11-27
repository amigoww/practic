from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from bot_config import database

homework_router = Router()

class Homework(StatesGroup):
    name = State()
    group_number = State()
    number = State()
    link = State()

@homework_router.callback_query(F.data == "homework")
async def start_homework(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Homework.name)
    await callback_query.message.answer("Как вас зовут?")

@homework_router.message(Homework.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Вводите только буквами!")
        return

    if len(name) > 15:
        await message.answer("Вводите не больше 15 символов!")
        return

    await state.update_data(name=message.text)
    await state.set_state(Homework.group_number)
    await message.answer("какая у вас группа?")

@homework_router.message(Homework.group_number)
async def process_group(message: types.Message, state: FSMContext):
    group = message.text
    if not group.isdigit():
        await message.answer("Вводите только номер группы(цифрами)!")
        return
    await state.update_data(group_number=message.text)
    await state.set_state(Homework.number)
    await message.answer("Номер домашнего задания?")

@homework_router.message(Homework.number)
async def process_number(message: types.Message, state: FSMContext):
    number = message.text
    if not number.isdigit():
        await message.answer("Вводите только номер дз(цифрами)!")
        return
    await state.update_data(number=message.text)
    await state.set_state(Homework.link)
    await message.answer("Скиньте ссылку на git")

@homework_router.message(Homework.link)
async def process_link(message: types.Message, state: FSMContext):
    await message.answer("Домашнее задание отправлено!")
    await state.update_data(link=message.text)
    data = await state.get_data()
    print(data)

    database.execute(
        query="""
                INSERT INTO homework (name, group_number, number, link)
                VALUES (?, ?, ?, ?)
                """,
        params=(data["name"], data["group_number"],data["number"], data["link"])
    )

    await state.clear()
