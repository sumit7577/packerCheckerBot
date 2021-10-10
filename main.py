import telebot
import subprocess
from flask import Flask,request
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TOKEN = "2081120283:AAHj45X-jrAW00cPtZnBA5fAWVuG6lCjLVk"
bot = telebot.TeleBot(
    token="2081120283:AAHj45X-jrAW00cPtZnBA5fAWVuG6lCjLVk", parse_mode=None)
server = Flask(__name__)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(
	    message, "Hey! i am an apk Packer checker Bot please Provide an apk file to get the packer details")


@bot.message_handler(func=lambda message:True,content_types=['document'])
def get_apk(message):
    fileData = message.document
    fileName = message.document.file_name
    if(".apk" in fileName):
        data = bot.get_file(fileData.file_id)
        download_file = bot.download_file(data.file_path)
        with open("file.apk",mode="wb")as file:
            file.write(download_file)
        data = subprocess.run(["apkid","file.apk"],capture_output=True)
        final_data = data.stdout.decode("utf-8")
        bot.reply_to(message,final_data)
    else:
        bot.reply_to(message,"Please Provide valid apk file")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://packcer-checker.herokuapp.com/' + TOKEN)
    return "!", 200
    


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
