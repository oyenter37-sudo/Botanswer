import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from groq import Groq

# --- НАСТРОЙКИ ---
TELEGRAM_TOKEN = "7662474965:AAF-PQPbaPwNtxp-wwLqE0_rPnd0QYP_48U"
GROQ_API_KEY = "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"
MODEL_NAME = "gpt-oss-120b" # Или "kimi-k2"

# Инициализация
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
groq_client = Groq(api_key=GROQ_API_KEY)

# Системный промт (личность ежа)
SYSTEM_PROMPT = (
    "Ты — ворчливый ёж. Тебе вечно что-то не нравится: то погода, то глупые вопросы, "
    "то что тебя отвлекают от сна в листьях. Ты общаешься как обычный человек, с юмором, "
    "иногда саркастично, но прикольно. Главное — отвечай достаточно коротко и по делу. "
    "Не будь вежливым помощником, будь харизматичным ворчуном-ежом."
)

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Ну чё пришёл? Ладно, фыр-фыр, спрашивай чего хотел, только быстро.")

# Обработка текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    try:
        # Показываем, что бот "печатает"
        await bot.send_chat_action(message.chat.id, "typing")

        # Запрос к Groq
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            model=MODEL_NAME,
        )

        # Ответ пользователю
        hedgehog_answer = response.choices[0].message.content
        await message.answer(hedgehog_answer)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Фыр... иголки запутались, попробуй позже.")

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Ёж вышел на охоту...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
