import os
import random
import telebot
import psycopg2
from flask import request
from telebot.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
)
from buttons import main_markup, button_question
import config
from models import User, Question
from sqlalchemy import tuple_
from message import hello_message
from message import adder



server = config.server
bot = config.bot
db = config.db


bot = telebot.TeleBot(config.token)


@server.route("/", methods=["POST"])
def receive_update():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return {"ok": True}


def create_user(id, username):
    users_ids = [i.id for i in User.query.all()]
    if id not in users_ids:
        user = User(id=id, username=username)
        db.session.add(user)
        db.session.commit()

def delete_history(message):
    Question.query.filter_by(user=message.from_user.id).delete()
    db.session.commit()
    bot.send_message(message.chat.id,"Очищено")


def create_id():
    id = random.choice(range(10000000))
    if id not in [i.id for i in Question.query.all()]:
        return id
    return create_id


def create_question(que, answ, id, user_id):
    a = Question(
        id=create_id(), 
        question=que,
        answer=answ,
        user=user_id
        )
    db.session.add(a)
    db.session.commit()
    bot.send_message(id, "Ваш запрос добавлен!\U0001f604")


def gen_message(id):
    button = [i.answer for i in Question.query.filter_by(id = id)]
    return button[0]

def get_message(user_id):
    questions = [(i.question,i.id)for i in Question.query.filter_by(user = user_id)]
    buttons = button_question(questions)
    return buttons
        
    
@bot.message_handler(commands=['help', 'start'])
def answer(message):
    create_user(
        message.from_user.id,
        message.from_user.username)
    print(message.from_user.username)
    bot.send_message(message.chat.id, hello_message(message.chat.username), reply_markup = main_markup)


@bot.message_handler(commands=['help', 'start'])
def answer(message):
    bot.send_message(
        message.chat.id, 
        hello_message(message.chat.username), 
        reply_markup=main_markup)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == "Add Question":
        bot.send_message(message.chat.id, adder)
    elif message.text.split(':')[0] == "ADD":
        que = (message.text.split(':')[1])
        answ = (message.text.split(':')[2])
        user_id = (message.from_user.id)
        create_question(que, answ, message.chat.id, user_id)
    elif message.text == 'Print':
        buttons = get_message(message.from_user.id)
        bot.send_message(message.chat.id, "Выберите вопрос", reply_markup = buttons)
    elif message.text == 'Clean':
        delete_history(message)
    else:
        bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    answ = gen_message(query.data)
    bot.send_message(
        query.message.chat.id,
        answ)
    bot.delete_message(query.message.chat.id, query.message.json['message_id'])


@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(
            request.stream.read().decode("ut-f-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    s = bot.set_webhook(
        url='https://313bad311b8d.ngrok.io' + config.token)
    if s:
        return print("webhook setup ok")
    else:
        return print("webhook setup failed")



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))