from config import BOT_TOKEN, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, ADMIN_ID
from aiogram import Dispatcher, Bot, types, executor
import psycopg2
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

connection = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(KeyboardButton("Вибор")).add(KeyboardButton("Сброс"))
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Якщо ви хочете зареєструватися у конкурсі, натисніть кнопку нижче',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Зарегуватися у конкурсі', callback_data=f'add')))
@dp.callback_query_handler(lambda c: c.data == 'add')
async def process_callback_button(callback_query: types.CallbackQuery):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (str(callback_query.from_user.id),))
            if cursor.fetchone():
                await bot.send_message(callback_query.from_user.id, 'Ви вже зареєстровані!')
            else:
                cursor.execute("INSERT INTO users(id, nickname, name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",(callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.first_name))
                connection.commit()
                await bot.send_message(callback_query.from_user.id, 'Ви успішно зареєструвались!')
@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
        if message.from_user.id == 1110618366:
            await bot.send_message(message.from_user.id, 'Меню адміна', reply_markup=admin_keyboard)
@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'Вибор' and message.from_user.id == 1110618366:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM users WHERE win IS NULL ORDER BY RANDOM() LIMIT 1;""")
            for ret in cursor.fetchall():
                await message.reply(f"id: {ret[0]} nickname: {ret[2]} name: {ret[1]}")
                await bot.send_message(chat_id=ret[0], text="Ви вийграли! Невздовзі з вами з'вяжуться")
                cursor.execute("UPDATE users SET win = 1 WHERE id = %s", (ret[0],))
    elif message.text == 'Сброс' and message.from_user.id == 1110618366:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM users """)
            for ret in cursor.fetchall():
                await bot.send_message(chat_id=ret[0],text='Вам потрібно переєструватися, для цього нажміть кнопку нижче',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Зарегуватися у конкурсі', callback_data=f'add')))
            cursor.execute("""TRUNCATE users;""")
            await message.reply("Готово")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)