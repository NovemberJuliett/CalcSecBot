import os

from dotenv import load_dotenv

import ptbot

from pytimeparse import parse


def reply(chat_id, text):
    message_id = bot.send_message(TG_CHAT_ID, "Запускаю таймер")
    msg = parse(text)
    bot.create_countdown(msg, notify_progress, chat_id=chat_id, message_id=message_id, total_sec=msg)
    bot.create_timer(msg, notify, chat_id=chat_id)


def notify(chat_id):
    bot.send_message(chat_id, "Время вышло")


def notify_progress(secs_left, chat_id, message_id, total_sec):
    secs_passed = total_sec - secs_left
    prog = render_progressbar(total_sec, secs_passed)
    count = "Осталось {} секунд".format(secs_left)
    result = count + "\n" + prog
    bot.update_message(chat_id, message_id, result)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


if __name__ == '__main__':
    load_dotenv()

    TG_TOKEN = os.environ['TG_TOKEN']
    TG_CHAT_ID = os.environ['TG_CHAT_ID']

    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(reply)
    bot.run_bot()
