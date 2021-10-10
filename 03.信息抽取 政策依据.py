# -*- coding: utf-8 -*-
from pyhanlp import *
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import re

path_src = 'txt/'
fm='data/政策依据抽取结果.txt'

all_text=''
for filename in os.listdir(path_src):
    fn = path_src + filename
    text = codecs.open(fn, 'r', encoding='ANSI').read()
    docs = re.split(r'[，,：:；;。？！…\n\t]', text)
    ww = []#依据
    kk = []
    for doc in docs:
        if '按照' in doc or '据' in doc or '《' in doc:
            if '数据' not in doc:
                ww.append(doc)
    list='；'.join(ww)
    text = filename + ":" + list + "\n"
    text = text.replace('.txt', '')
    all_text = all_text + text
fb = open(fm, "w", encoding="utf-8")
fb.writelines(all_text)
fb.close()