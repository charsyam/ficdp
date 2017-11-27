import math
import sys
import itertools
import os

class Similarity(object):
    def check_similarity(self, dir_path):
        return self.parse_path(dir_path)

    def parse_path(self, dir_path):
        files = []
        for dirname, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                if filename.endswith(".txt") == False:
                    continue

                files.append(dirname + "/" + filename)

        ret = []
        for i in range(len(files)-1):
            file1 = files[i]
            for file2 in files[i+1:]:
                name = file1 + ":" + file2
                value = self.cosine_similarity_from_file(file1, file2)
        
                ret.append((name, value))

        return ret

    def jacard_similarity_from_file(self, file1, file2):
        doc1 = self.get_word_dict(self.get_data(file1))    
        doc2 = self.get_word_dict(self.get_data(file2))    

        return self.jacard_similarity(doc1, doc2)

    def cosine_similarity_from_file(self, file1, file2):
        doc1 = self.get_word_dict(self.get_data(file1))    
        doc2 = self.get_word_dict(self.get_data(file2))    

        return self.cosine_similarity(doc1, doc2)

    def jacard_similarity(self, doc1, doc2):
        union = self.union(doc1, doc2)
        union_len = len(union)

        intersection = self.intersection(doc1, doc2)
        return len(intersection) / len(union)

    def union(self, *dicts):
        return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))

    def intersection(self, dic1, dic2):
        return set(dic1.keys()) & set(dic2.keys())
        
    def cosine_similarity(self, doc1, doc2):
        doc1_vector_magnitude = sum([math.pow(x, 2) for x in doc1.values()])
        doc2_vector_magnitude = sum([math.pow(x, 2) for x in doc2.values()])

        dot_product = sum([v * doc2[k] for k, v in doc1.items() if k in doc2])
        magnitude = math.sqrt(doc1_vector_magnitude) * math.sqrt(doc2_vector_magnitude)
        if magnitude == 0:
            magnitude = 1
        return dot_product / magnitude

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
    sim = Similarity()
#    print(sim.cosine_similarity_from_file(sys.argv[1], sys.argv[2]))
#    print(sim.jacard_similarity_from_file(sys.argv[1], sys.argv[2]))
    for i in sim.check_similarity(sys.argv[1]):
        print(i)
