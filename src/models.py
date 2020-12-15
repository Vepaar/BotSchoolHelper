from config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, unique=True, nullable=False)
    answer = db.Column(db.String, unique=True, nullable=False)
    user = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False) 
