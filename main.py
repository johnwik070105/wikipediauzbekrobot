import json
import requests
import wikipedia
import logging
from aiogram import Bot, Dispatcher, executor, types
#from background import keep_alive

wikipedia.set_lang('uz')

logging.basicConfig(level=logging.DEBUG)

API_TOKEN = '6411697239:AAELdYOJPQU2ZIl15wieFc-glN4N7g49NVk'

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot)



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
  kb.add(types.KeyboardButton(text="✅ Ro'yxatdan o'tish", request_contact=True))
  await message.answer(text=f"Xush kelibsiz, {message.from_user.full_name}. Botdan to'liq foydalanish uchun ro'yxatdan o'tish tugmasini bosing...", reply_markup=kb)

@dp.message_handler(commands='info')
async def info(message: types.Message):
  with open('users.json', 'r') as f:
    info_bot = json.load(f)
  await message.answer(text=f"Botning foydalanuvchilari soni: {len(list(info_bot.keys()))}")


@dp.message_handler(content_types="contact")
async def register(message: types.Message):
  await message.answer(text="Tabriklaymiz, siz ro'yxatdan o'tdingiz. Endi qanday mavzu haqida ma'lumot kerak bo'lsa, menga mavzuni yozib yuboring...", reply_markup=types.ReplyKeyboardRemove())
  with open('users.json', 'r') as file:
    users_data = json.load(file)
    file.close()
  if str(message.from_user.id) not in list(users_data.keys()):
    await bot.send_message(
      chat_id='-1001893377121',
      text=f"""Full name: {message.from_user.full_name}
  Username: @{message.from_user.username}
  Phone number: <code>{message.contact.phone_number}</code>
  User ID: <code>{message.from_user.id}</code>"""
    )
  users_data[f"{message.from_user.id}"] = {'full_name': message.from_user.full_name, 'username': message.from_user.username, 'phone_number': message.contact.phone_number}
  with open('users.json', 'w') as file:
    json.dump(users_data, file, indent=4)
    file.close()


@dp.message_handler(content_types=['text'])
async def wiki(message: types.Message):
  with open('users.json', 'r') as file:
    users_datas_for_if = json.load(file)
  if str(message.from_user.id) in list(users_datas_for_if.keys()):
    try:
      other_posts = wikipedia.search(message.text)
      result = wikipedia.summary(message.text)
  
      kb = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
      for button in other_posts[1:]:
        kb.insert(types.InlineKeyboardButton(text=button, callback_data=button))
  
      await message.answer(text=result, reply_markup=kb)
    except:
      await message.answer(text="Faqat mavzuni o'zini xatosiz va ortiqcha matn kiritmasdan yozing...")
  else:
    await message.answer(text="Botdan foydalanish uchun ro'yxatdan o'tish tugmasini bosing...")
  
@dp.callback_query_handler()
async def inline_query_text(callback_query: types.CallbackQuery):
  other_posts = wikipedia.search(callback_query.data)
  result = wikipedia.summary(callback_query.data)

  kb = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
  for button in other_posts[1:]:
    kb.insert(types.InlineKeyboardButton(text=button, callback_data=button))

  await callback_query.answer()
  await callback_query.message.answer(text=result, reply_markup=kb)



if __name__ == '__main__':
  executor.start_polling(dispatcher=dp)
