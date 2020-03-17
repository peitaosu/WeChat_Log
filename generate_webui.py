# -*- coding: utf-8 -*-

import os, sys, sqlite3
from datetime import datetime
import jieba
from os import path
from PIL import Image
import numpy as  np
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.font_manager as fm

def get_messages_from_table(db_file, table_name):
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM " + table_name + " ORDER BY CreateTime")
    date_list = []
    messages = {}
    for row in c.fetchall():
        when_str = datetime.fromtimestamp(int(row[0])).strftime('%Y-%m-%d %H:%M:%S')
        date_str = when_str.split(" ")[0]
        time_str = when_str.split(" ")[1]
        who_int = row[1]
        if row[4].startswith("<msg><emoji "):
            what_str = "[表情]"
        elif "<msg><img " in row[4]:
            what_str = "[图片]"
        elif "<img " in row[4]:
            what_str = "[图片]"
        elif "<msg><videomsg " in row[4]:
            what_str = "[视频]"
        elif "<msg><voicemsg " in row[4]:
            what_str = "[语音]"
        elif "<location x=" in row[4]:
            what_str = "[定位]"
        elif "<appmsg appid=" in row[4]:
            what_str = "[小程序]"
        elif "<gameext type=" in row[4]:
            what_str = "[剪刀石头布]" 
        else:
            what_str = row[4]
        if date_str not in messages:
            messages[date_str] = []
            date_list.append(date_str)
        else:
            messages[date_str].append(
                {
                    "time": time_str,
                    "who": who_int,
                    "what": what_str
                }
            )
    conn.close()
    return [date_list, messages]

def create_wc(text, bg_file, font_file, out_file):
    bg=np.array(Image.open(bg_file))
    def jiebaclearText(text):
        mywordList=[]
        seg_list=jieba.cut(text,cut_all=False)
        return ' '.join(seg_list)
    wc_text=jiebaclearText(text)
    wc=WordCloud(
        background_color="white", 
        max_words=100,
        mask=bg,
        max_font_size=40,
        random_state=42,
        font_path=font_file,
        min_word_length=2,
        scale=2
        ).generate(wc_text)
    my_font=fm.FontProperties(fname=font_file)
    image_colors=ImageColorGenerator(bg)
    wc.recolor(color_func=image_colors)
    wc.to_file(out_file)
    img = Image.open(out_file)
    img = img.resize((480, 480),Image.ANTIALIAS)
    img.save(out_file, optimized=True, quality=100)


def generate_webui():
    prefix = """
    <!DOCTYPE html>
    <html>
    <head><title>{0} -- {1}</title><link href='css/fonts.css' rel='stylesheet' type='text/css'><link href='css/web.css' rel='stylesheet' type='text/css'><script src="js/jquery.min.js"></script><script src="js/web.js"></script></head>
    <body><div id="dashboard"><div id="navbar"><p>Navigation Bar</p><div class="nav prev"><a href="{2}.html">Previous Date</a></div><div class="nav next"><a href="{3}.html">Next Date</a></div></div><div id="wordcloud"><p>Words Cloud</p><img id="wc_img" src="img/wc/{4}.jpg"/></div></div><div id="chatbox"><div id="holder"></div><div id="entrances"><div class="entrance"><p><strong>{5}</strong></p><p><span>{6}</span></p></div></div><div id="messageview" class="p1"><div id="title"><div id="close"><div class="cy"></div><div class="cx"></div></div><p>{7}</p><span>{8}</span></div><div id="chat-messages">
    """
    suffix = """
    </div><div id="sendmessage"><input type="text" value="Send Message..." /><button id="send"></button></div></div></div>
    </body>
    </html>
    """
    # TODO: change title to your title for display
    title = "THIS IS TITLE"
    # TODO: change MM.sqlite to your message log db
    # TODO: change Chat_xxx to your message log table
    [date_list, messages] = get_messages_from_table(r"MM.sqlite", "Chat_xxx")

    if not os.path.isdir("out/img/wc"):
        os.makedirs("out/img/wc")

    for date_iter in range(len(date_list)):
        date = date_list[date_iter]
        if date_iter == len(date_list) - 1:
            next_date = date
        else:
            next_date = date_list[date_iter + 1]
        if date_iter == 0:
            prev_date = date
        else:
            prev_date = date_list[date_iter - 1]
        print("Processing {} ...".format(date))
        with open(os.path.join("out", date + ".html"), "w") as out_file:
            out_file.write(prefix.format(title, date, prev_date, next_date, date, title, date, title, date))
            out_file.write("<label>{}</label>\n".format(date))
            text = ""
            for message in messages[date]:
                if message["who"] == 0:
                    out_file.write('<div class="message">\n')
                else:
                    out_file.write('<div class="message right">\n')
                out_file.write('<img/><div class="bubble">{}<div class="corner"></div><span>{}</span></div></div>'.format(message["what"], message["time"]))
                text = text + message["what"]
            # TODO: change bg.jpg to your wordcloud background image
            # TODO: change font.ttf to your wordcloud font file
            create_wc(text, "bg.jpg", "font.ttf", "out/img/wc/{}.jpg".format(date))
            out_file.write(suffix)
