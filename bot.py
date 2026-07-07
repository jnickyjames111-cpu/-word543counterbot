import os
import logging
import re

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Core counting logic
# ---------------------------------------------------------
def analyze_text(text: str) -> str:
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    sentence_count = len(re.findall(r"[.!?]+", text)) or (1 if text.strip() else 0)
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()]) or (1 if text.strip() else 0)

    # crude reading time estimate: 200 words per minute
    reading_time_min = max(1, round(word_count / 200)) if word_count else 0

    return (
        "📊 *Text Analysis*\n\n"
        f"📝 Words: `{word_count}`\n"
        f"🔤 Characters (with spaces): `{char_count}`\n"
        f"🔡 Characters (no spaces): `{char_count_no_spaces}`\n"
        f"📄 Sentences: `{sentence_count}`\n"
        f"📃 Paragraphs: `{paragraph_count}`\n"
        f"⏱ Estimated reading time: `{reading_time_min} min`"
    )


# ---------------------------------------------------------
# Handlers
# ---------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm *Word Counter Bot*.\n\n"
        "Just send me any text and I'll count words, characters, "
        "sentences, and paragraphs for you.\n\n"
        "Commands:\n"
        "/start – show this message\n"
        "/help – how to use the bot",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me any block of text (as a normal message) and I'll reply "
        "with word count, character count, sentence count, paragraph count, "
        "and estimated reading time."
    )


async def count_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text or not text.strip():
        await update.message.reply_text("Please send some text to analyze.")
        return
    result = analyze_text(text)
    await update.message.reply_text(result, parse_mode="Markdown")


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. "
            "Set it in Railway's Variables tab."
        )

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_text))

    logger.info("Bot starting (polling mode)...")
    app.run_polling()


if __name__ == "__main__":
    main()
