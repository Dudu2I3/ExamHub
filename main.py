import telebot

bot = telebot.TeleBot('6345291697:AAEboN8wJsc-kwO-V_DVQ9ZHMwc8VDiHw8o')

from telebot import types


@bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\nХочешь использовать нашего бота?"
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    markup.add(button_yes)
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def response(function_call):
    if function_call.message:
        if function_call.data == "yes":
            second_mess = "Ура,тогда давай пройдем регистрацию! /reg"
            markup = types.InlineKeyboardMarkup()

            bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            bot.answer_callback_query(function_call.id)


name = '';
surname = '';
age = 0;
type_person = '';


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name);  # следующий шаг – функция get_name
    # else:
    # bot.send_message(message.from_user.id, 'Напиши /reg');


def get_name(message):  # получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);


def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);


def get_age(message):
    global age;
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
    bot.send_message(message.from_user.id, 'Спасибо за регистрацию. Продолжим?');
    bot.register_next_step_handler(message, get_type_person);


def get_type_person(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Школьник")
    button2 = types.KeyboardButton("Студент")
    markup.add(button1, button2)
    msg = bot.send_message(message.chat.id, "Привет! Кто ты?", reply_markup=markup)
    bot.register_next_step_handler(msg, process_callback)


def process_callback(message):
    if message.text == "Школьник":
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("Назад", callback_data="back")
        button2 = types.InlineKeyboardButton("Далее", callback_data="next")
        markup.add(button1, button2)


bot.infinity_polling()
