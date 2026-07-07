# @word543counterbot

A simple Telegram bot that counts words, characters, sentences, and
paragraphs in any text you send it, and estimates reading time.

## Features
- `/start` and `/help` commands
- Send any text message → get instant analysis:
  - Word count
  - Character count (with/without spaces)
  - Sentence count
  - Paragraph count
  - Estimated reading time

## 1. Create the bot on Telegram
1. Open Telegram and message **@BotFather**
2. Send `/newbot`
3. Choose a display name (e.g. "Word Counter")
4. Choose the username: `word543counterbot`
5. BotFather will give you a **token** — copy it, you'll need it below

## 2. Run locally (optional, for testing)
```bash
git clone <your-repo-url>
cd word543counterbot
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and paste your BOT_TOKEN
export $(cat .env | xargs)   # or use python-dotenv if you prefer
python bot.py
```

## 3. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: word counter bot"
git branch -M main
git remote add origin https://github.com/<your-username>/word543counterbot.git
git push -u origin main
```
**Important:** `.env` is already in `.gitignore` — never commit your real bot token.

## 4. Deploy on Railway
1. Go to [railway.app](https://railway.app) and log in with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Select your `word543counterbot` repository
4. Once the project is created, go to **Variables** and add:
   - `BOT_TOKEN` = the token you got from BotFather
5. Railway will detect the `Procfile` and run `python bot.py` automatically
   as a **worker** process (no web port needed — this bot uses polling)
6. Under **Settings → Deploy**, make sure the service is set to run the
   `worker` process (Railway usually auto-detects this from the Procfile)
7. Once deployed, open Telegram and message your bot — it should respond!

## Notes
- This bot uses **polling** (`run_polling()`), which is simplest for Railway —
  no webhook/domain setup required.
- If you later want to scale or reduce latency, you can switch to
  **webhooks**, but polling is fine for a personal/small-scale bot.
