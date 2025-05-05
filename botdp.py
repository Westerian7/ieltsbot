import random
import os
import threading
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ======================
# FastAPI Health Check
# ======================
app = FastAPI()
start_time = datetime.now()

@app.get("/")
def health_check():
    return {
        "status": "IELTS Bot is online",
        "uptime": str(datetime.now() - start_time),
        "telegram": "active"
    }

# ======================
# Telegram Bot Config
# ======================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual token

def load_questions():
    questions = {}
    try:
        for part in ['part1', 'part2', 'part3']:
            with open(f"{part}_questions.txt", 'r', encoding='utf-8') as f:
                questions[part] = [line.strip() for line in f if line.strip()]
        return questions
    except Exception as e:
        print(f"Error loading questions: {e}")
        return None

questions = load_questions()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not questions:
        await update.message.reply_text("❌ Question database not loaded")
        return
    
    keyboard = [
        [InlineKeyboardButton("🎤 Part 1", callback_data='part1')],
        [InlineKeyboardButton("🗣️ Part 2", callback_data='part2')],
        [InlineKeyboardButton("💬 Part 3", callback_data='part3')],
        [InlineKeyboardButton("📝 Full Test", callback_data='full')]
    ]
    
    await update.message.reply_text(
        "📚 IELTS Speaking Practice\nChoose a question type:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not questions:
        await query.edit_message_text("❌ Questions not available")
        return
    
    try:
        if query.data == 'menu':
            keyboard = [
                [InlineKeyboardButton("🎤 Part 1", callback_data='part1')],
                [InlineKeyboardButton("🗣️ Part 2", callback_data='part2')],
                [InlineKeyboardButton("💬 Part 3", callback_data='part3')],
                [InlineKeyboardButton("📝 Full Test", callback_data='full')]
            ]
            await query.edit_message_text(
                "📚 IELTS Speaking Practice\nChoose a question type:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
            
        if query.data == 'part1':
            response = f"🎤 Part 1:\n\n{random.choice(questions['part1'])}"
        elif query.data == 'part2':
            response = f"🗣️ Part 2:\n\n{random.choice(questions['part2'])}"
        elif query.data == 'part3':
            response = f"💬 Part 3:\n\n{random.choice(questions['part3'])}"
        elif query.data == 'full':
            response = (
                "📚 Full Test:\n\n"
                f"🎤 Part 1:\n{random.choice(questions['part1'])}\n\n"
                f"🗣️ Part 2:\n{random.choice(questions['part2'])}\n\n"
                f"💬 Part 3:\n{random.choice(questions['part3'])}"
            )
        
        await query.edit_message_text(
            text=response,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 New", callback_data=query.data)],
                [InlineKeyboardButton("🏠 Menu", callback_data='menu')]
            ])
        )
    except Exception as e:
        await query.edit_message_text(f"⚠️ Error: {str(e)}")

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    threading.Thread(target=run_server, daemon=True).start()
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_query, pattern='^(part1|part2|part3|full|menu)$'))
    application.run_polling()

if __name__ == '__main__':
    main()
