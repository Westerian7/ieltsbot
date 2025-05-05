async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not questions:
        await update.message.reply_text("❌ Question database not loaded")  # Properly closed
        return
    
    keyboard = [
        [InlineKeyboardButton("🎤 Part 1", callback_data='part1'),
         InlineKeyboardButton("🗣️ Part 2", callback_data='part2')],
        [InlineKeyboardButton("💬 Part 3", callback_data='part3'),
         InlineKeyboardButton("📝 Full Test", callback_data='full')]
    ]
    
    # This is the critical fix - properly closed parentheses:
    await update.message.reply_text(
        "📚 IELTS Speaking Practice\nChoose a question type:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )  # <- This closing parenthesis was missing

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not questions:
        await query.edit_message_text("❌ Questions not available")  # Properly closed
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
        
        await query.edit_message_text(  # Properly closed
            response,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
            
    except Exception as e:
        await query.edit_message_text(f"⚠️ Error: {str(e)}")  # Properly closed
