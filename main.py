import telebot
import subprocess

bot = telebot.TeleBot(
    token="2081120283:AAHj45X-jrAW00cPtZnBA5fAWVuG6lCjLVk", parse_mode=None)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(
	    message, "Hey! i am an apk Packer checker Bot please Provide an apk file to get the packer details")


@bot.message_handler(func=lambda message: True,content_types=['document'])
def get_apk(message):
    fileData = message.document
    if(fileData[:3:-1] == "kpa."):
        data = bot.get_file(fileData.file_id)
        download_file = bot.download_file(data.file_path)
        with open("file.apk",mode="wb")as file:
            file.write(download_file)
        data = subprocess.run(["apkid","file.apk"],capture_output=True)
        final_data = data.stdout.decode("utf-8")
        bot.reply_to(message,final_data)
    else:
        bot.reply_to(message,"Please Provide Valid apk file")
    

bot.infinity_polling()
