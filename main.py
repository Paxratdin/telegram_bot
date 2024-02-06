from config import TOKEN
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from deep_translator import GoogleTranslator

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("https").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


button = [
    [
         InlineKeyboardButton("1️⃣-qatar",callback_data="1"),
         InlineKeyboardButton("2️⃣-qatar",callback_data="2")
    ],
    
    [
        InlineKeyboardButton("🇺🇿Uzbek", callback_data="uz"),
        InlineKeyboardButton("🇬🇧English", callback_data="en")
    ],
    
    [
        InlineKeyboardButton("🇬🇧English", callback_data="en"),
        InlineKeyboardButton("🇺🇿Uzbek", callback_data="uz")
    ],
    
    [
         InlineKeyboardButton("🇺🇿Uzbek",callback_data='uz'),
         InlineKeyboardButton("🇷🇺Russain",callback_data='ru')
    ],
    
    [
         InlineKeyboardButton("🇷🇺Rus",callback_data='en'),
         InlineKeyboardButton("🇺🇿Uzbek",callback_data='uz')
    ]
]

reply_markup = InlineKeyboardMarkup(button)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text(f"Assalawma aleykum {user.first_name} Til sazlamari 👇 \n🔄 1-qatar arqalı qaysı tilden, 2-qatar arqalı qaysı tilge awdarma qılıwdı belgileysiz",reply_markup=reply_markup)


async def callback_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global query
    query = update.callback_query


async def translate_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    translate_text = GoogleTranslator(source="auto", target=query.data).translate(text=text)
    await update.message.reply_text(translate_text)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_query))
    app.run_polling()

if(__name__ == "__main__"):
    main()