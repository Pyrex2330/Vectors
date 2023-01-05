from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import asyncio
from vectors import draw_vectors_bot

from vectors import draw_vectors_bot

bot = Bot(token=getenv('API_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# создаём форму и указываем поля
class Form(StatesGroup):
    diagrams_chart = State()
    voltages_check = State()
    angles_1 = State()
    angles_2 = State()
    angles_3 = State()


start_buttons = ['Начать', 'Отмена']
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*start_buttons)


# Начинаем наш диалог
@dp.message_handler(Text(equals='Начать'))
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.diagrams_chart.set()
    await message.reply("Введите количество диаграмм (1-3)", reply_markup=keyboard)


# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


# Сюда приходит ответ с количеством
@dp.message_handler(lambda message: not message.text.isdigit() or not int(message.text) in range(1, 4),
                    state=Form.diagrams_chart)
async def charts_invalid(message: types.Message):
    return await message.reply('Некорректный ввод. Введите цифру от 1 до 3')


@dp.message_handler(state=Form.diagrams_chart)
async def charts_valid(message: types.Message, state: FSMContext):
    await state.update_data(counter=int(message.text))
    await Form.voltages_check.set()
    await message.reply('Введите напряжения сторон (кВ) через пробел')


@dp.message_handler(state=Form.voltages_check)
async def voltages_check(message: types.Message, state: FSMContext):
    voltages = message.text.split()
    counter = await state.get_data()
    counter = counter.get('counter')
    if not all(voltage.isdigit() for voltage in voltages) or not len(voltages) == counter:
        await message.reply(
            'Некорректный ввод. Число сторон и количество напряжений должно быть одинаково. '
            'Напряжения должны быть цифрами')
    else:
        angles = {voltage: [] for voltage in voltages}
        await state.update_data(voltages=voltages, angles=angles)
        await Form.angles_1.set()
        await message.answer('Направление C принимается за положительное, направление L за отрицательное')
        await message.reply(f'Введите углы стороны {voltages[0]}кВ через пробел')


@dp.message_handler(state=Form.angles_1)
async def get_voltages(message: types.Message, state: FSMContext):
    data = await state.get_data()
    voltages = data.get('voltages')
    counter = data.get('counter')
    angles = data.get('angles')
    angles_side = message.text.split()

    try:
        if len(angles_side) != 3 or not all(angle not in range(-180, 181) for angle in angles_side):
            await message.reply('Некорректный ввод. Повторите')
        else:
            angles_side = [int(i) for i in angles_side]
            curr_voltage = voltages[0]
            try:
                voltages.pop(0)
            except IndexError:
                print(IndexError)
            angles[curr_voltage] = angles_side
            counter -= 1
            await state.update_data(angles=angles, counter=counter, voltages=voltages)
            if counter != 0:
                await message.reply(f'Введите углы стороны {voltages[0]}кВ через пробел')
            else:
                await state.update_data(angles=angles)
                # await Form.angles_2.set()
                # await finish(message, state)
                async with state.proxy() as data:
                    data['diagram'] = asyncio.run(draw_vectors_bot(data.get('angles')))
                    await bot.send_photo(message.chat.id, data.get('diagram'))
                    # data['diagram'].seek(0)
                    # await bot.send_photo(message.chat.id, data.get('diagram'))
                    # await bot.send_message(message.chat.id, data)
    except Exception as ex:
        pass
    finally:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
