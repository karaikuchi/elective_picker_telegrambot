import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from gpt import gpt
import config

TOKEN = config.TOKEN
dp = Dispatcher()


class Form(StatesGroup):
    list_courses = State()
    interest = State()


builder = InlineKeyboardBuilder()
builder.button(text="Yes, thank you!", callback_data="like")
builder.button(text="No, it does not help me", callback_data="dislike")
builder.adjust(1, 1)


@dp.message(CommandStart())
async def welcome(message: types.Message, state: FSMContext):
    await state.set_state(Form.list_courses)
    await message.answer(f"Welcome {hbold(message.from_user.full_name)}! ")
    await message.answer(f"I am chat bot that will help you to choose elective course")
    await message.answer(f"Firstly, provide me with a list of courses")


@dp.message(Form.list_courses)
async def process_courses(message: types.Message, state: FSMContext):
    await state.update_data(list_courses=message.text)
    await state.set_state(Form.interest)
    await message.answer(f"Now, please write about your interests")


@dp.message(Form.interest)
async def process_interest(message: types.Message, state: FSMContext):
    await state.update_data(interest=message.text)
    data = await state.get_data()
    await state.clear()
    final_request = f"{data['list_courses']}.\n{data['interest']}.\nWhat should I choose?"
    await message.answer(f"Got it, give me seconds to think...")
    result = await gpt(final_request)
    await message.answer(result)
    await message.answer("Was this advice helpful?", reply_markup=builder.as_markup())


@dp.callback_query()
async def process_feedback(callback: types.CallbackQuery):
    if callback.data == "like":
        await callback.message.answer("I am glad to could help you!")
    elif callback.data == "dislike":
        await callback.message.answer("I apologize, next time I will try me best!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
