import telebot
bot = telebot.TeleBot('6493165557:AAHpqhuRWEB4sBO-0Arp3yEoyQttSokIB28')
from telebot import types

questions = ["В каком году была основана компания Apple?",
             "Какое имя у мыши в мультфильме Том и Джерри?",
             "Какой город является столицей Франции?"]

answers = [["1976", "1978", "1980", "1982"],
           ["Джерри", "Том", "Спайк", "Ниблер"],
           ["Марсель", "Штутгарт", "Париж", "Мюнхен"]]

correct_answers = ["1976", "Джерри", "Париж"]

scores = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Quiz бот. Давай поиграем в викторину!")

@bot.message_handler(commands=['quiz'])
def quiz_questions(message):
    chat_id = message.chat.id
    user_scores = scores.get(chat_id, 0)
    score_message = f"Текущий счёт: {user_scores}"
    bot.send_message(chat_id, score_message)

    for num, question in enumerate(questions):
        options = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        ans_options = answers[num]

        options.add(telebot.types.KeyboardButton(ans_options[0]))
        options.add(telebot.types.KeyboardButton(ans_options[1]))
        options.add(telebot.types.KeyboardButton(ans_options[2]))
        options.add(telebot.types.KeyboardButton(ans_options[3]))

        question_message = f"{num+1}. {question}"
        bot.send_message(chat_id, question_message, reply_markup=options)
        bot.register_next_step_handler(message, check_answer, num)

def check_answer(message, question_num):
    chat_id = message.chat.id
    user_answer = message.text
    correct_answer = correct_answers[question_num]

    if user_answer == correct_answer:
        user_scores = scores.get(chat_id, 0)
        user_scores += 1
        scores[chat_id] = user_scores
        reply_message = "Правильно!"
    else:
        reply_message = "Неправильно."

    bot.send_message(chat_id, reply_message)

bot.polling()
