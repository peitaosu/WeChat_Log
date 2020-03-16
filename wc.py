import jieba
from os import path
from PIL import Image
import numpy as  np
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.font_manager as fm

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
