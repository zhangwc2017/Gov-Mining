# -*- coding: utf-8 -*-
from pyhanlp import *
import codecs
import collections # 词频统计库
# from textrank4zh import TextRank4Keyword, TextRank4Sentence
# tr4w = TextRank4Keyword()
CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
StandardTokenizer = JClass("com.hankcs.hanlp.seg.Segment").enableCustomDictionaryForcing
segment = HanLP.newSegment().enableOrganizationRecognize(True)#调用机构识别模块

path_src = 'txt/'
fm='data/04.政策主体抽取结果.txt'
f1=open('data/04.政策主体词表.txt', 'w', encoding='utf-8')

ww=[]
all_text=''
for filename in os.listdir(path_src):
    fn = path_src + filename
    text = codecs.open(fn, 'r', encoding='ANSI').read()
    y_pos = segment.seg(text)
    kk = []
    for term in y_pos:  # 对每个词而言
        zz = '{}\t{}'.format(term.word, term.nature)  # 标注词和词性
        if 'nto' in zz:#政策主体识别的词性规则。nt需要再核查
            if zz not in kk:
                kk.append(zz)
            if zz not in ww:
                ww.append(zz)
    list = "；".join(kk)
    text=filename+":"+list+"\n" #注意：字符串连接用+，list连接用append
    text=text.replace('.txt','')
    all_text=all_text+text
fb = open(fm, "w", encoding="utf-8")
fb.writelines(all_text)
fb.close()

word_counts = collections.Counter(ww)  # 对分词做词频统计
word_counts_top50000 = word_counts.most_common(50000)  # 获取前10最高频的词
# word_list = "；".join(word_counts_top1000)
print(word_counts_top50000, file=f1)