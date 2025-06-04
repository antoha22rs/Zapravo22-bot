from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# Состояния для диалога
ASK_QUESTION, ASK_NAME, ASK_PHONE = range(3)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получена команда /start от пользователя:", update.message.from_user.username)  # Для отладки
    await update.message.reply_text("Здравствуйте! Какой вопрос у вас есть?")
    return ASK_QUESTION

# Получение вопроса
async def get_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['question'] = update.message.text
    await update.message.reply_text("Спасибо! Напишите ваше ФИО.")
    return ASK_NAME

# Получение ФИО
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Отлично! Теперь укажите ваш номер телефона.")
    return ASK_PHONE

# Получение номера телефона
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    user_data = (
        f"Новый запрос:\n"
        f"Вопрос: {context.user_data['question']}\n"
        f"ФИО: {context.user_data['name']}\n"
        f"Телефон: {context.user_data['phone']}\n"
    )
    # Сохранение в файл
    with open("client_data.txt", "a", encoding="utf-8") as file:
        file.write(user_data + "-" * 30 + "\n")
    await update.message.reply_text(
        "Спасибо за информацию! Юрист с вами свяжется."
    )
    # Отправка данных вам
    await context.bot.send_message(
        chat_id="1684093467",
        text=user_data
    )
    return ConversationHandler.END

# Команда /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог отменён.")
    return ConversationHandler.END

def main():
    # Токен для @Zapravo22_bot
    TOKEN = "7770900658:AAGTRwZNfo73D_q8Dw0IW_7FWdhkRWm3xv0"

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Настраиваем диалог
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_question)],
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Добавляем обработчик
    application.add_handler(conv_handler)

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()