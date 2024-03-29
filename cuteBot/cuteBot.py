import telebot
import urllib.request
import os
import praw 
import threading
from flask import Flask, request

bot_token = 'your_bot_token'
bot = telebot.TeleBot(token=bot_token)
reddit = praw.Reddit(client_id= 'CYJNh3ecbQhxzQ', client_secret= 'du58jAIgpE9lbfXoLoJlkEUnl4Y', username= 'tgdankbot', password= 'Kutaluta@3crest', user_agent= 't5' )
subreddit = reddit.subreddit('aww')
hot_aww = subreddit.hot(limit=30)
url_arr = []
app = Flask(__name__)

def update_urls():
    url_arr[:] = []
    for i in range(0,20):
        for submission in hot_aww:
            if 'jpg' in submission.url:
                url_arr.append(submission.url)
                print(url_arr[i])


def dl(url):
    f = open('pic.jpg', 'wb')
    if 'jpg' in url:
        f.write(urllib.request.urlopen(url).read())
    f.close


def send_photo(): 
    threading.Timer(21600,send_photo).start()
    update_urls()
    count = len(url_arr)
    for i in range(0,count-1):
        if(url_arr[i] is not None):
            dl(url_arr[i])
            img = open('pic.jpg','rb')
            if os.stat('pic.jpg').st_size != 0:
                bot.send_photo('channel/chat_id',photo = img)
            img.close
    keep_up()


def keep_up():
    threading.Timer(500,keep_up).start()
    urllib.request.urlopen('https://cuteheaven-bot.herokuapp.com/')
    print('requested')

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome, press /help for more information')

@bot.message_handler(commands = ['help'])
def send_welcome(message):
    bot.reply_to(message, 'Hit /send')

@bot.message_handler(func=lambda message: 'send 384252204' in message.text)
def every24(message):
        send_photo()
        keep_up()
        
        
@app.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://cuteheaven-bot.herokuapp.com/' + bot_token)
    return "!", 200

if __name__ == "__name__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

