from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler
from credentials import Keys
from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu, default_callback_handler)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓'
        'help_with_resume': 'Помощь с резюме',
        # Добавить команду в меню можно так:
        # 'command': 'button text'

    })


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def help_with_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "resume_profile"
    text = load_message("resume_profile")
    await send_photo(update, context, "resume_profile")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Введите название желаемой вакансии")


async def help_with_resume_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["vacancy"] = text
        await send_text(update, context, "Введите ваши ФИО")
    elif dialog.count == 2:
        dialog.user["fio"] = text
        await send_text(update, context, "Опыт работы: названия компаний, должности, обязанности")
    elif dialog.count == 3:
        dialog.user["experience"] = text
        await send_text(update, context, "Какими навыками обладаете?")
    elif dialog.count == 4:
        dialog.user["skills"] = text
        await send_text(update, context, "Добавьте информацию об образовании и квалификации")
    elif dialog.count == 5:
        dialog.user["qualification"] = text
        prompt = load_prompt("resume_profile")
        user_info = dialog_user_info_to_str(dialog.user)
        my_message = await send_text(update, context,
                                     "ChatGPT занимается генерацией вашего резюме. Подождите пару секунд...")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)

async def mode_handler(update, context):
    if dialog.mode == "resume_profile":
        await help_with_resume_dialog(update, context)


ob_keys = Keys()
dialog = Dialog()

chat_gpt = ChatGptService(ob_keys.gpt_token)
app = ApplicationBuilder().token(ob_keys.bot_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("talk", talk))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("help_with_resume", help_with_resume))
# Зарегистрировать обработчик команды можно так:
# app.add_handler(CommandHandler('command', handler_func))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mode_handler))
# Зарегистрировать обработчик коллбэка можно так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))

app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
