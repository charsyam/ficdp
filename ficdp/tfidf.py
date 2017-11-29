import math
import sys
import os
from konlpy.tag import Kkma
import string
import re

THRESHOLD=0.01
SIZE_THRESHOLD=2
TFIDF_SIZE = 30
STEMMING_WORD_LIST = ['한다', '있다', '되고', '하고', '하여', '에게', '을', '를', '이', '가', '고', '게', '의', '과', '는', '에', '은', '와', '된', '로', 'ed', 'es', 's']
NO_USE_WORD = {
    '얼마나': 1,
    '어떻': 1,
    '있다': 1,
    '모두': 1,
    '또한': 1,
    'the': 1,
    'why': 1,
    'what': 1,
    'how': 1,
    'of': 1,
    'as': 1,
    '필요함': 1,
    '수정함': 1,
    '가능함': 1,
    '신속한': 1,
    '신속하고': 1,
    '서술하시오': 1,
    '각각': 1,
    '까지': 1,
    '있습니다': 1,
    '유연한' : 1,
    '있는지' : 1,
    'and' : 1,
    'big' : 1,
    'to' : 1,
    'none' : 1,
    '않음' : 1,
    '처럼' : 1,
    '따른' : 1
}

class TFIDF(object):
    def __init__(self):
        self.word_map = {}
        self.doc_map = {}
        self.kkma = Kkma()

    def parse_path(self, dir_path): 
        for dirname, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                if filename.endswith(".txt") == False:
                    continue

                fname = dirname + "/" + filename
                words = self.get_word_dict(self.get_data(fname))
                for word in words:
                    if word in self.word_map:
                        m = self.word_map[word]
                        if fname in m:
                            m[fname] += 1
                        else:
                            m[fname] = 1
                    else:
                        self.word_map[word] = { fname: 1 }

                    self.doc_map[fname] = words

    def get_tf(self, fname, word):
        try:
            return self.doc_map[fname][word]/len(self.doc_map[fname])
        except:
            return 0

    def get_df(self, fname, word):
        try:
            return len(self.word_map[word])
        except:
            return 1

    def get_idf(self, df, alldf):
        k =  alldf / (df)
        return math.log(alldf / df)

    def get_tfidfs(self):
        ret = []
        for fname in self.doc_map.keys():
            ret.append((fname, self.get_tfidf(fname)))

        return ret
            
    def get_tfidf(self, fname):
        ret = []
        for word in self.doc_map[fname]:
            tf = self.get_tf(fname, word)
            df = self.get_df(fname, word)
            alldf = len(self.doc_map)
            idf = self.get_idf(df, alldf)
            tfidf = tf * idf
            ret.append((word, tfidf, tf, df, idf, alldf))

        return sorted(ret, key=lambda x: x[1], reverse=True)

    def get_word_dict2(self, data):
        data = data.strip()
        m = {}

        words = self.kkma.nouns(data)
        for word in words:
            if len(word) < SIZE_THRESHOLD:
                continue

            word = word.lower()
            if word in m:
                m[word] += 1
            else:
                m[word] = 1

        return m


    def get_word_dict(self, data):
        data = data.strip()
        m = {}
        chars = re.escape(string.punctuation)
        data = re.sub(r'['+chars+']', ' ',data)

        for line in data.split('\n'):
            for word in line.split():
                for sword in STEMMING_WORD_LIST:
                    if word.endswith(sword) == True:
                        word = word[:-len(sword)]
                        break

                if len(word) < 2:
                    continue

                word = word.lower()
                if word in NO_USE_WORD:
                    continue

                if word in m:
                    m[word] += 1
                else:
                    m[word] = 1

        return m

    def get_data(self, filename):
        f = open(filename)
        return f.read()

        
if __name__ == '__main__':
    tfidf = TFIDF()
    tfidf.parse_path(sys.argv[1])

    m = {}
    for word in tfidf.get_tfidfs():
        print("")
        print(word[0])
        sl = sorted(word[1], key=lambda x: x[1], reverse=True)
        for wi in sl[0:20]:
            print(wi[0], wi[1])

        for t in word[1]:
            if t[1] < THRESHOLD:
                continue

            w = t[0]
            if w in m:
                m[w] += 1  
            else:
                m[w] = 1

    sl = sorted(m.items(), key=lambda x: x[1], reverse=True)
#    for word in sl:
#        print(word)
