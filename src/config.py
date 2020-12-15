import os
from flask import Flask, request
import telebot
from flask_sqlalchemy import SQLAlchemy


token = "1426858587:AAHohoG7dxdPVIPrpEkqVngLvdmz3I78Pzc"
DATABASE_URL = 'postgres+psycopg2://vepar:031003@localhost:5432/h1nter_bot'

server = Flask(__name__)
bot = telebot.TeleBot(token)
server.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
server.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(server)