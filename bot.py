# All Exam Hack Bot 13.0 – Ultra Addictive & Gamified
# Author: Tany's Project
# Fully Working, Python 3.11 Compatible

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler
)

# 🔹 Telegram API token
API_TOKEN = "8499727045:AAF4P2qAHoXotwh1pGNbV1NUBBywLqGh784"

# Conversation states
LANGUAGE, EXAM, SUBJECT, RESOURCE, MINI_GAME = range(5)

# Languages
LANGUAGES = {"en": "English", "hi": "हिंदी", "mr": "मराठी"}

# Exams
EXAMS = [
    "Class 8th", "Class 9th", "Class 10th", "Class 11th", "Class 12th",
    "SSC CGL", "SSC CHSL", "SSC MTS", "Railway NTPC", "Railway ALP", "Railway Group D",
    "Banking IBPS PO", "Banking IBPS Clerk", "Banking SBI PO", "Banking SBI Clerk",
    "LIC AAO", "LIC ADO", "Insurance NICL", "Insurance GIC",
    "UPSC", "NDA", "CDS", "GATE", "CAT", "CLAT", "NEET", "JEE",
    "CTET", "State Teacher Exams",
    "State Police Constable", "State Police SI",
    "Group C/D Exams"
]

# Subjects
SUBJECTS = ["Maths", "Science", "Reasoning", "GK", "Current Affairs"]

# Resources
RESOURCES = ["Previous Year Papers", "Notes", "Solutions", "Hacks & Shortcuts"]

# Motivation Quotes
MOTIVATION_QUOTES = [
    "Success doesn’t come to you, you go to it!",
    "Believe in yourself, you are halfway there!",
    "Push yourself, because no one else is going to do it for you.",
    "Dream big, work hard, stay focused.",
    "Little progress each day adds up to big results.",
    "Your future is created by what you do today, not tomorrow.",
    "Motivation gets you started. Habit keeps you going.",
    "Great things never come from comfort zones.",
    "Wake up with determination, go to bed with satisfaction.",
    "The key to success is to focus on goals, not obstacles.",
]

# Quiz Questions
QUIZ_QUESTIONS = [
    {"q": "Who is the Father of the Indian Constitution?", "options": ["Gandhi", "Ambedkar", "Nehru"], "a": "Ambedkar"},
    {"q": "Speed = ?", "options": ["Distance/Time", "Time/Distance", "Force/Mass"], "a": "Distance/Time"},
    {"q": "Who discovered Gravity?", "options": ["Newton", "Einstein", "Galileo"], "a": "Newton"},
    {"q": "Capital of India?", "options": ["Mumbai", "New Delhi", "Kolkata"], "a": "New Delhi"},
    {"q": "H2O is chemical formula of?", "options": ["Water", "Oxygen", "Hydrogen"], "a": "Water"},
    {"q": "Largest planet in Solar System?", "options": ["Earth", "Jupiter", "Mars"], "a": "Jupiter"},
]

# Track user data
user_data_store = {}
last_quiz = {}

# --- Bot Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(v, callback_data=k)] for k, v in LANGUAGES.items()]
    await update.message.reply_text(
        "👋 Welcome to All Exam Hack Bot 13.0!\nSelect your language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return LANGUAGE

async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    context.user_data["lang"] = lang
    keyboard = [[InlineKeyboardButton(exam, callback_data=exam)] for exam in EXAMS]
    await query.edit_message_text("📚 Select your exam:", reply_markup=InlineKeyboardMarkup(keyboard))
    return EXAM

async def choose_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    exam = query.data
    context.user_data["exam"] = exam
    keyboard = [[InlineKeyboardButton(subject, callback_data=subject)] for subject in SUBJECTS]
    await query.edit_message_text(
        f"📖 Exam: {exam}\nSelect your subject:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SUBJECT

async def choose_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data
    context.user_data["subject"] = subject

    # resources + mini game button
    keyboard = [[InlineKeyboardButton(res, callback_data=res)] for res in RESOURCES]
    keyboard.append([InlineKeyboardButton("🎮 Play Mini Game", callback_data="mini_game")])

    await query.edit_message_text(
        f"📘 Subject: {subject}\nChoose resource type:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return RESOURCE

async def choose_resource(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "mini_game":
        return await mini_game_start(update, context)

    exam = context.user_data.get("exam")
    subject = context.user_data.get("subject")
    await query.edit_message_text(f"✅ Here is your {choice} for {exam} - {subject}.\n(Placeholder content)")
    return ConversationHandler.END

# --- Mini Game ---
async def mini_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    question = random.choice(QUIZ_QUESTIONS)
    context.user_data["mini_game_question"] = question
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"game_{opt}")] for opt in question["options"]]
    await query.edit_message_text(f"🎯 Mini Quiz: {question['q']}", reply_markup=InlineKeyboardMarkup(keyboard))
    return MINI_GAME

async def mini_game_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.replace("game_", "")
    question = context.user_data.get("mini_game_question")
    if question and choice == question["a"]:
        await query.edit_message_text(f"✅ Correct! {choice} is right. 🏆 Points +10")
    else:
        await query.edit_message_text(f"❌ Wrong! Correct answer: {question['a']}. 😢 Try again tomorrow!")
    return ConversationHandler.END

# Premium
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔒 Premium coming soon! Unlimited downloads, AI Tutor, Secret Hacks 🚀")

# Referral
async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📢 Invite friends: https://t.me/AllExamHackBot")

# --- Main ---
def main():
    app = Application.builder().token(API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(choose_language)],
            EXAM: [CallbackQueryHandler(choose_exam)],
            SUBJECT: [CallbackQueryHandler(choose_subject)],
            RESOURCE: [CallbackQueryHandler(choose_resource)],
            MINI_GAME: [CallbackQueryHandler(mini_game_answer, pattern="^game_")]
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("refer", refer))

    print("✅ All Exam Hack Bot 13.0 is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
