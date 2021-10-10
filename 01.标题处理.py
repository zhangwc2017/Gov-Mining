# -*- coding:utf-8 -*-
from pyhanlp import *
import pandas as pd
import codecs
import re

CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
CustomDictionary.add("应急预案","健康码")
segment = HanLP.newSegment().enableOrganizationRecognize(True)#调用机构识别模块

inputfile='title.xlsx'
outputfile='data/tile-标题分析-nto.xlsx'
f1 = open('data/标题 实体词表-nto.txt', 'w', encoding='utf-8')
f2 = open('data/标题 关键词表.txt', 'w', encoding='utf-8')
f3 = open('data/标题 动词词表.txt', 'w', encoding='utf-8')

data=pd.read_excel(inputfile,sheetname= 'Sheet1')

#抽取标题中的实体词
print('开始抽取实体......')
bb = []
data['标题实体'] = data['标题']#复制列
for i in data['标题实体']:
    kk = []
    ww = segment.seg(i.strip())  # 分词 #strip()方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    for term in ww:  # 对每个词而言
        zz = '{}\t{}'.format(term.word, term.nature)  # 标注词和词性
        if 'nto' in zz:  # 抽取实体的词性规则
            if term.word not in bb:
                bb.append(zz) # bb为词性为nt的词表，即机构词表
            if term.word not in kk:
                kk.append(zz)#打印全部词性标注结果
    y='；'.join(kk)
    data['标题实体']=data['标题实体'].replace(i,y)
print(bb, file=f1)#打印机构词表

#抽取标题中的关键词
print('开始抽取关键词......')
from textrank4zh import TextRank4Keyword, TextRank4Sentence
tr4w = TextRank4Keyword()
ww=[]
data['标题关键词'] = data['标题']#复制列
for i in data['标题关键词']:
    text=''.join(i)
    tr4w.analyze(text=text, lower=True, window=2)
    a = []
    for item in tr4w.get_keywords(8, word_min_len=3):
        # print(item.word, item.weight)
        a.append(item.word)
    y = "；".join(a)  # 转化为字符串格式
    y_pos = segment.seg(y)
    kk = []
    for term in y_pos:  # 对每个词而言
        zz = '{}\t{}'.format(term.word, term.nature)  # 标注词和词性
        # print(zz)
        # print(term.word,term.nature)
        #抽取主题词的词性规则
        if 'nb' in zz or 'nf' in zz or 'nh' in zz or 'nm' in zz or 'nn' in zz or 'nz' in zz or 'g' in zz:
            if zz not in kk:
                kk.append(term.word)
            if zz not in ww:
                ww.append(zz)
    yy = "；".join(kk)
    data['标题关键词'] = data['标题关键词'].replace(i, yy)
print(ww, file=f2)#打印关键词表

#抽取标题中的公文类型
print('开始抽取公文类型......')
# with codecs.open('data/list_gov_type.txt', 'r', 'utf-8') as f:
#     line = f.read().strip()
#     theory_list = line.split("\n")  # 以换行符分隔
#     pattern = '|'.join(theory_list)
data['公文类型'] = data['标题']#复制列
for i in data['公文类型']:
    text = ''.join(i)
    # list = re.findall(pattern, text)
    # list_merge = set(list)
    kk=''
    if '决议' in text:
        kk='决议'
    elif '决定' in text:
        kk='决定'
    elif '令' in text:
        kk='命令'
    elif '公报' in text:
        kk='公报'
    elif '公告' in text or '举报' in text:
        kk='公告'
    elif '通告' in text or '告知书' in text or '提示' in text:
        kk='通告'
    elif '意见' in text:
        kk='意见'
    elif '通知' in text:
        kk='通知'
    elif '通报' in text:
        kk='通报'
    elif '报告' in text:
        kk='报告'
    elif '请示' in text:
        kk='请示'
    elif '批复' in text:
        kk='批复'
    elif '议案' in text:
        kk='议案'
    elif '函' in text:
        kk='函'
    elif '纪要' in text:
        kk='纪要'
    elif '倡议书' in text:
        kk = '倡议书'
    elif '慰问信' in text or '一封信' in text or '指南' in text:
        kk='公开信'
    else:
        kk='None'
    # b = ",".join(list)  # 列表格式转为字符串格式
    data['公文类型'] = data['公文类型'].replace(i, kk)

#抽取标题中的动词（作为主体与主体间、主体与主题间的关联关系）
print('开始抽取动词......')
data['标题动词'] = data['标题']  # 复制列
vv=[]
for i in data['标题动词']:
    text = ''.join(i)
    y = segment.seg(text)
    kk = []
    for term in y:  # 对每个词而言
        zz = '{}\t{}'.format(term.word, term.nature)  # 标注词和词性
        # print(zz)
        # print(term.word,term.nature)
        if 'v' in zz:
            kk.append(zz)
            if term.word not in vv:
                vv.append(zz)
    b = ",".join(kk)  # 列表格式转为字符串格式
    data['标题动词'] = data['标题动词'].replace(i, b)
print(vv, file=f3)#打印动词词表

data.to_excel(outputfile)