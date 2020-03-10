import os, sys, sqlite3
from datetime import datetime

def get_messages_from_table(db_file, table_name):
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM " + table_name + " ORDER BY CreateTime")
    for row in c.fetchall():
        when_str = datetime.fromtimestamp(int(row[0])).strftime('%Y-%m-%d %H:%M:%S')
        who_str = row[1]
        what_str = row[4]
        print("{} {} : {}".format(when_str, who_str, what_str))
    conn.close()

