import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from oxfordLookup import getDefinitions
from googletrans import Translator


tranlator = Translator()

# API_TOKEN = getenv('TOKEN_BOT')
API_TOKEN =''


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Speak English botiga xush kelibsiz!")



@dp.message_handler()
async def myTranslator(message: types.Message):
    lang = tranlator.detect(message.text).lang
    
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(tranlator.translate(message.text, dest).text)

    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = tranlator.translate(message.text, dest='en').text
        
        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply(f"Audio: {lookup['audio']}")
        else:
            await message.reply("Bunday so'z topilmadi")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)