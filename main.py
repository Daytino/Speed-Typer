from flask import Flask, render_template, request
from random import randint
import threading
import tkinter
import requests
import datetime

app = Flask(__name__)

symbols = list("qwertyuiopasdfghjklzxcvbnm123456789")
wrds = str()
letters = str()


def generate_words():
    global wrds
    words = str()

    for i in range(5):
        words += requests.get("https://random-word-api.herokuapp.com/word").text[2:-2]
        words += " "
    wrds = str(words[:-1])


threading.Timer(0.0, generate_words).start()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home_words', methods=['POST', 'GET'])
def home_words():
    return render_template("logging_words.html")


@app.route('/words', methods=['POST', 'GET'])
def words():
    global d1
    output = request.form
    name = output["name"]
    generate_words()
    d1 = datetime.datetime.now()
    return render_template("words_process.html", words=wrds, name=name)


@app.route('/end_words', methods=['POST', 'GET'])
def end_words():
    global wrds
    output = request.form
    text = output["text"]
    root = tkinter.Tk()
    root.withdraw()
    clipboard = root.clipboard_get()
    d2 = datetime.datetime.now()
    delta = (d2 - d1).seconds

    if text == wrds:
        if clipboard in wrds or clipboard == wrds:
            return render_template("end.html", victory=3)
        else:
            if delta <= 30:
                return render_template("end.html", victory=1)
    else:
        return render_template("end.html", victory=2)


@app.route('/home_letters', methods=['POST', 'GET'])
def home_letters():
    return render_template("logging_letters.html")


@app.route('/letters', methods=['POST', 'GET'])
def letters():
    global d1, letters
    output = request.form
    name = output["name"]
    d1 = datetime.datetime.now()

    letters = str()
    for i in range(24):
        letters += symbols[randint(0, 25)]
        space_chance = randint(0, 3)
        if 0 <= space_chance <= 2 and i != 23:
            letters += " "
    return render_template("letters_process.html", letters=letters, name=name)


@app.route('/end_letters', methods=['POST', 'GET'])
def end_letters():
    output = request.form
    text = output["text"]

    root = tkinter.Tk()
    root.withdraw()
    clipboard = root.clipboard_get()

    d2 = datetime.datetime.now()
    delta = (d2 - d1).seconds

    if text == letters:
        if clipboard in letters:
            return render_template("end.html", victory=3)
        else:
            if delta <= 30:
                return render_template("end.html", victory=1)
    else:
        return render_template("end.html", victory=2)


if __name__ == "__main__":
    app.run(use_reloader=False)
