import config
import telebot
from telebot import types



bot = telebot.TeleBot(config.token)

user_num1 = ''
user_num2 = ''
user_proc = ''
user_result = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id, f'Привет  {message.from_user.first_name}, я бот-калькулятор рациональных чисел\nВведите число: ', reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)


def process_num1_step(message, user_result=None):
    try:
        global user_num1

        if user_result == None:
            user_num1 = float(message.text)
        else:
            user_num1 = str(user_result)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembt1 = types.KeyboardButton('+')
        itembt2 = types.KeyboardButton('-')
        itembt3 = types.KeyboardButton('*')
        itembt4 = types.KeyboardButton('/')
        markup.add(itembt1, itembt2, itembt3, itembt4)

        msg = bot.send_message(message.chat.id, 'Выберите операцию', reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc_step)
    except Exception as e:
        bot.reply_to(message, 'Возможно вы ввели не число')


def process_proc_step(message):
    try:
        global user_proc

        user_proc = message.text
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(message.chat.id, 'Введите второе число: ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так...')


def process_num2_step(message):
    try:
        global user_num2

        user_num2 = float(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembt1 = types.KeyboardButton('Результат')
        itembt2 = types.KeyboardButton('Продолжить вычисление')
        markup.add(itembt1, itembt2)

        msg = bot.send_message(message.chat.id, 'Показать результат или продолжить операцию?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
        bot.reply_to(message, 'Ошибка')


def process_alternative_step(message):
    try:
        calc()

        markup = types.ReplyKeyboardRemove(selective=False)
        if message.text.lower() == 'результат':
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text.lower() == 'Продолжить вычисление':
            process_num1_step(message, user_result)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')


def calcResultPrint():
    global user_num1, user_num2, user_proc, user_result
    return f'Результат: {str(user_num1)} {user_proc} {str(user_num2)} = {str(user_result)}'


def calc():
    global user_num1, user_num2, user_proc, user_result

    user_result = eval(str(user_num1) + user_proc + str(user_num2))

    return user_result


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)

