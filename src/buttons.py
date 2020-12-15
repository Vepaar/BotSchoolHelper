from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add("Add Question")
main_markup.add("Print")
main_markup.add("Clean")


def button_question(questions):
    main_markup = InlineKeyboardMarkup()
    for i in questions:
        main_markup.add(
            InlineKeyboardButton(i[0], callback_data=i[1]))
    return main_markup
