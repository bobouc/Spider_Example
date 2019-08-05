import os
import time
import requests
import random
import json
import pprint
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud


kybook_path = 'kybook.txt'
WC_MASK_IMG = 'ky.jpg'
WC_FONT_PATH = '/Library/Fonts/Songti.ttc'

def comment_spider(page = 0):
    url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2783&productId=11990777&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&rid=0&fold=1"%page
    kv = {'user-agent': 'Mozilla/5.0','Referer':'https://item.jd.com/11990777.html'}

    try:
        r = requests.get(url,headers = kv)
        r.raise_for_status()
    except:
        print("spider failed.")
    r_json_str = r.text[26:-2]
    r_json_obj = json.loads(r_json_str)
    pprint.pprint(r_json_obj['comments'])
    r_json_comments = r_json_obj['comments']
    for r_json_comment in r_json_comments:
        with open(kybook_path,'a+') as f:
            f.write(r_json_comment['content']+'\n')
        print(r_json_comment['content'])

def bunch_comment_spider():
    if os._exists(kybook_path):
        os.remove(kybook_path)
    for i in range(20):
        comment_spider(i)
        time.sleep(random.random() * 5)
    
def cut_word():
    # 打开爬取的评论数据文件
    with open(kybook_path) as file:     
        # 读取文件内容
        comment_txt = file.read()       
        #分词处理
        wordlist = jieba.cut(comment_txt, cut_all=True)  
        #json处理   
        wl = " ".join(wordlist)                             
        print(wl)
        return wl

def create_word_cloud():
    # 设置词云形状图片
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, font_path=WC_FONT_PATH)
    # 生成词云
    wc.generate(cut_word())
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()

if __name__ == '__main__':
    #comment_spider()
    bunch_comment_spider()

    create_word_cloud()
    