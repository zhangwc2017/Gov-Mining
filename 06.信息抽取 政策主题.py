# -*- coding: utf-8 -*-
from pyhanlp import *
import codecs
import collections # 词频统计库
from textrank4zh import TextRank4Keyword, TextRank4Sentence
tr4w = TextRank4Keyword()
CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
segment = HanLP.newSegment().enableOrganizationRecognize(True)#调用机构识别模块

path_src = 'txt/'
fm='data/06.政策主题抽取结果(15, word_min_len=3).txt'
f1=open('data/06.政策主题词表(15, word_min_len=3).txt', 'w', encoding='utf-8')
ww=[]
all_text=''
for filename in os.listdir(path_src):
    fn = path_src + filename
    text = codecs.open(fn, 'r', encoding='ANSI').read()
    tr4w.analyze(text=text, lower=True, window=2)
    a = []
    for item in tr4w.get_keywords(15, word_min_len=3):#每篇公文提取关键词的数量需要测试，过多会有不关键的冗余词出现，过少提取不出来。
        # print(item.word, item.weight)
        a.append(item.word)
    y = "；".join(a)  # 转化为字符串格式
    y_pos = segment.seg(y)
    kk = []
    for term in y_pos:  # 对每个词而言
        zz = '{}\t{}'.format(term.word, term.nature)  # 标注词和词性
        if 'nb' in zz or 'nf' in zz or 'nh' in zz or 'nm' in zz or 'nz' in zz or 'g' in zz:
            if zz not in kk:
                kk.append(zz)
            ww.append(zz)
    list = "；".join(kk)
    text=filename+":"+list+"\n" #注意：字符串连接用+，list连接用append
    text=text.replace('.txt','')
    all_text=all_text+text
fb = open(fm, "w", encoding="utf-8")
fb.writelines(all_text)
fb.close()
# 词频统计
word_counts = collections.Counter(ww)  # 对分词做词频统计
word_counts_top50000 = word_counts.most_common(50000)  # 获取前10最高频的词
print(word_counts_top50000, file=f1)