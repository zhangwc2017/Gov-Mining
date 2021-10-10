# -*- coding:utf-8 -*-
from pyhanlp import *
import pandas as pd
import codecs
import re

inputfile='data/政策依据.xlsx'
outputfile='data/政策依据 处理结果.xlsx'
f1 = open('data/政策依据 词表.txt', 'w', encoding='utf-8')
data=pd.read_excel(inputfile,sheetname= 'Sheet1')

#抽取标题中的实体词
print('开始抽取......')
bb = []
data['政策依据文件'] = data['政策依据']#复制列
for i in data['政策依据文件']:
    text=''.join(i)
    p1 = re.compile(r"[《](.*?)[》]", re.S)#re.S是为了让.表示除了换行符的任一字符, 加了？是最小匹配，不加是贪婪匹配
    ss=re.findall(p1, text)
    s = set(ss)
    bb.append(s)
    y='；'.join(s)
    data['政策依据文件'] = data['政策依据文件'].replace(i, y)
print(bb, file=f1)#打印机构词表
data.to_excel(outputfile)