import telebot

bot = telebot.TeleBot('6655848781:AAH5PwaU9X57MIVLc4rEsETRPBUb439lb3s')

from telebot import types


@bot.message_handler(commands=['start'])
def startBot(message):      # начало работы бота
    first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\nХочешь использовать нашего бота?"
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    markup.add(button_yes)
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)         # начало регистрации
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


@bot.message_handler(content_types=['text'])        # регистрация
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name);  # следующий шаг – функция get_name
    # else:
    # bot.send_message(message.from_user.id, 'Напиши /reg');


def get_name(message):          # получаем имя
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);


def get_surname(message):       # получаем фамилию
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);


def get_age(message):       # получаем возраст
    global age;
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
    bot.send_message(message.from_user.id, 'Спасибо за регистрацию.Выбери к какому предмету ты хочешь подготовиться\n1 - /sport\n2 - /itam\n3 - /bioengineers\n4 - /ai_knowledge')
    bot.register_next_step_handler(message, links)


def links(message):         #ссылки на чаты
    if message.text == '/sport':
        bot.send_message(message.from_user.id, "@sport_misis");
    elif message.text == '/itam':
        bot.send_message(message.from_user.id, "@itatmisis");
    elif message.text == '/bio':
        bot.send_message(message.from_user.id, "@bioengineers_MISIS");
    elif message.text == '/ai_knowledge':
        bot.send_message(message.from_user.id, "https://t.me/aiknowledgeclub");


bot.infinity_polling()
