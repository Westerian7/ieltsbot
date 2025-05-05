import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Bot Token (replace if needed)
BOT_TOKEN = "7799617257:AAG6mp9kM2GRiT8O5HYlB_J0cG2zrBEx_x4"

# Load questions from text files
def load_questions():
    """Load questions from part1_questions.txt, part2_questions.txt, part3_questions.txt"""
    questions = {}
    try:
        with open("part1_questions.txt", "r", encoding="utf-8") as f:
            questions['part1'] = [line.strip() for line in f if line.strip()]
        
        with open("part2_questions.txt", "r", encoding="utf-8") as f:
            questions['part2'] = [line.strip() for line in f if line.strip()]
        
        with open("part3_questions.txt", "r", encoding="utf-8") as f:
            questions['part3'] = [line.strip() for line in f if line.strip()]
            
        return questions
    except FileNotFoundError as e:
        print(f"❌ Error loading question files: {e}")
        return None

# Load questions at startup
questions = load_questions()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not questions:
        await update.message.reply_text("❌ Failed to load questions. Check if files exist!")
        return
    
    keyboard = [
        [InlineKeyboardButton("🎤 Part 1", callback_data='part1')],
        [InlineKeyboardButton("🗣️ Part 2", callback_data='part2')],
        [InlineKeyboardButton("💬 Part 3", callback_data='part3')],
        [InlineKeyboardButton("📝 Full Test", callback_data='full')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📚 IELTS Speaking Bot\nChoose a question type:",
        reply_markup=reply_markup
    )

# Handle button clicks
async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not questions:
        await query.edit_message_text("❌ Questions not loaded. Check server logs.")
        return
    
    try:
        if query.data == 'part1':
            response = "🎤 **Part 1 Question:**\n\n" + random.choice(questions['part1'])
        elif query.data == 'part2':
            response = "🗣️ **Part 2 Question:**\n\n" + random.choice(questions['part2'])
        elif query.data == 'part3':
            response = "💬 **Part 3 Question:**\n\n" + random.choice(questions['part3'])
        elif query.data == 'full':
            response = (
                "📚 **Full IELTS Speaking Test**\n\n"
                "🎤 **Part 1:**\n" + random.choice(questions['part1']) + "\n\n"
                "🗣️ **Part 2:**\n" + random.choice(questions['part2']) + "\n\n"
                "💬 **Part 3:**\n" + random.choice(questions['part3'])
            )
        
        # Add action buttons
        keyboard = [
            [InlineKeyboardButton("🔄 New Question", callback_data=query.data)],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup)
    
    except Exception as e:
        await query.edit_message_text(f"⚠️ Error: {str(e)}")

# Main function
def main():
    print("🤖 IELTS Speaking Bot is starting...")
    
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_query, pattern='^(part1|part2|part3|full)$'))
    application.add_handler(CallbackQueryHandler(start, pattern='^menu$'))
    
    # Start polling
    print("✅ Bot is now running! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()