import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import start_keyboards
from config import API_TOKEN

import sqlite3

# Connect to database
conn = sqlite3.connect('users.db')

# Create a cursor
cursor = conn.cursor()  # cursor - bu yerda ma'lumotlarni baza bilan aloqada bo'lish uchun ishlatiladi

# Create a table | Create table jadval_nomi(ustun_nomi tipi, ustun_nomi tipi)
sql_query = '''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    status TEXT,
    Ism_familiya TEXT,
    Yosh TEXT,
    Texnologiya TEXT,
    Username TEXT,
    phone TEXT,
    Hudud TEXT,
    Narx TEXT,
    Murojat TEXT,
    Maqsad TEXT,
    user_id TEXT
)'''

# Save (commit) the changes
conn.commit()

cursor.execute(sql_query)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

class Register(StatesGroup):
    status = State()
    Ism_familiya = State()
    Yosh = State()
    Texnologiya = State()
    Username = State()
    phone = State()
    Hudud = State()
    Narx = State()
    Murojat = State()
    Maqsad = State()



@dp.message_handler(commands=['start'])
async def salom_ber(message: types.Message):    
    await message.answer(text=f"Assalomu aleykum, xush kelibsiz-{message.from_user.full_name}" , reply_markup=start_keyboards)


@dp.message_handler(lambda message: message.text == 'Ish Joyi kere')
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(status='Ish Joyi Kerak')
    await Register.status.set()
    await message.answer(text="Ism familiya otchestva kiriting")
    await Register.next()


@dp.message_handler(state=Register.Ism_familiya)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(Ism_familiya =message.text)
    await message.answer(text="Yoshingizni Kiriting")
    await Register.next()

@dp.message_handler(state=Register.Yosh)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data( Yosh =message.text)
    await message.answer(text="Texnologiyani kiriting:")
    await Register.next()
    


@dp.message_handler(state=Register.Texnologiya)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(Texnologiya =message.text)
    await state.update_data(Username=message.from_user.username)
    await Register.next()
    contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)
    

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(contact)
    await message.answer(text="Telefon raqamingizni yuboring", reply_markup=keyboard)
    await Register.next()



@dp.message_handler(content_types=types.ContentType.CONTACT, state=Register.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(text="Hududingizni kiriting")
    await Register.next()

@dp.message_handler(state=Register.Hudud)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(Hudud =message.text)
    await message.answer(text="Narx: ")
    await Register.next()

@dp.message_handler(state=Register.Narx)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(Narx =message.text)
    await message.answer(text="Qachon murojat qilsa boladi: ")
    await Register.next()

@dp.message_handler(state=Register.Murojat)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(Murojat =message.text)
    await message.answer(text="Maqsad: ")
    await Register.next()


@dp.message_handler(state=Register.Maqsad)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(Maqsad=message.text)
    data = await state.get_data()
    print(data)
    await state.finish()
    await message.answer(f"{data['status']}:\n👨‍💼 Xodim: {data['Ism_familiya']}\n🕑 Yosh: {data['Yosh']}\n📚 Texnologiya: {data['Texnologiya']}\n🇺🇿 Telegram: {data['Username']}\n📞 Aloqa: {data['phone']}\n🌐 Hudud: {data['Hudud']}\n💰 Narxi: {data['Narx']}\n🕰 Murojaat qilish vaqti: {data['Murojat']}\n🔎 Maqsad: {data['Maqsad']} \nshu ma'lumotlar adminga yuborildi")
    cursor.execute(
        'INSERT INTO users(status,Ism_familiya,Yosh,Texnologiya,Username,phone,Hudud,Narx,Murojat,user_id) VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?)',
        (data['status'], data['Ism_familiya'], data['Yosh'], data['Texnologiya'], data['Username'],data['phone'],data['Hudud'],data['Narx'],data['Murojat'] ,str(message.from_user.id))
    )
    conn.commit()
    user_info = f"{data['status']}:\n👨‍💼 Xodim: {data['Ism_familiya']}\n🕑 Yosh: {data['Yosh']}\n📚 Texnologiya: {data['Texnologiya']}\n🇺🇿 Telegram: {data['Username']}\n📞 Aloqa: {data['phone']}\n🌐 Hudud: {data['Hudud']}\n💰 Narxi: {data['Narx']}\n🕰 Murojaat qilish vaqti: {data['Murojat']}\n🔎 Maqsad: {data['Maqsad']}"
    await bot.send_message(chat_id='6313238207', text=f'Yangi Zapros:\n{user_info}')




if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)