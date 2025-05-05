import random
import os
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from fastapi import FastAPI
import uvicorn

# ======================
# FastAPI Health Check
# ======================
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "IELTS Bot is online", "telegram": "active"}

# ======================
# Telegram Bot Core
# ======================
BOT_TOKEN = os.getenv("7799617257:AAG6mp9kM2GRiT8O5HYlB_J0cG2zrBEx_x4")  # Set in Render environment variables

def load_questions():
    """Load questions from text files"""
    questions = {}
    try:
        question_files = {
            'part1': 'part1_questions.txt',
            'part2': 'part2_questions.txt', 
            'part3': 'part3_questions.txt'
        }
        
        for part, filename in question_files.items():
            with open(filename, 'r', encoding='utf-8') as f:
                questions[part] = [line.strip() for line in f if line.strip()]
        return questions
        
    except Exception as e:
        print(f"⚠️ Error loading questions: {e}")
        return None

questions = load_questions()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not questions:
        await update.message.reply_text("❌ Question database not loaded")
        return
    
    keyboard = [
        [InlineKeyboardButton("🎤 Part 1", callback_data='part1'),
         InlineKeyboardButton("🗣️ Part 2", callback_data='part2')],
        [InlineKeyboardButton("💬 Part 3", callback_data='part3'),
         InlineKeyboardButton("📝 Full Test", callback_data='full')]
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
        if query.data == 'part1':
            response = f"🎤 Part 1 Question:\n\n{random.choice(questions['part1'])}"
        elif query.data == 'part2':
            response = f"🗣️ Part 2 Question:\n\n{random.choice(questions['part2'])}"
        elif query.data == 'part3':
            response = f"💬 Part 3 Question:\n\n{random.choice(questions['part3'])}"
        elif query.data == 'full':
            response = (
                "📚 Full IELTS Test\n\n"
                f"🎤 Part 1:\n{random.choice(questions['part1'])}\n\n"
                f"🗣️ Part 2:\n{random.choice(questions['part2'])}\n\n"
                f"💬 Part 3:\n{random.choice(questions['part3'])}"
            )
        
        keyboard = [
            [InlineKeyboardButton("🔄 New Question", callback_data=query.data),
             InlineKeyboardButton("🏠 Menu", callback_data='menu')]
        ]
        
        await query.edit_message_text(
            response,
            reply_markup=InlineKeyboardMarkup(keyboard))
            
    except Exception as e:
        await query.edit_message_text(f"⚠️ Error: {str(e)}")

# ======================
# Server Management
# ======================
def run_fastapi():
    """Run the health check server"""
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_bot():
    """Run the Telegram bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_query, pattern='^(part1|part2|part3|full|menu)$'))
    application.run_polling()

# ======================
# Main Execution
# ======================
if __name__ == '__main__':
    print("🚀 Starting IELTS Speaking Bot...")
    
    # Start health check in background thread
    threading.Thread(target=run_fastapi, daemon=True).start()
    
    # Start Telegram bot in main thread
    run_bot()
