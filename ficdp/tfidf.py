import math
import sys
import os

class TFIDF(object):
    def __init__(self):
        self.word_map = {}
        self.doc_map = {}

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
            

    def get_word_dict(self, data):
        data = data.strip()
        m = {}
        for line in data.split('\n'):
            for word in line.split():
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
    for word in tfidf.get_tfidfs():
        print(word[0])
        for i in range(10):
            print(word[1][i])
