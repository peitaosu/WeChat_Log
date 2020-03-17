# -*- coding: utf-8 -*-

import os, sys, sqlite3
from datetime import datetime

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