import csv

COMBOS = {}
class Combo():
    def __init__(self, pattern, score, hand):
        self.pattern = pattern
        self.score = score
        self.hand = hand

    def __str__(self):
        return self.pattern

with open('combinations_data/combinations_made.csv', 'r', encoding='utf-8') as f:
    for e in f:
        line = e.strip().split(' ')
        if line[0] == '':
            continue

        COMBOS[line[0]] = Combo(line[0], float(line[1]), line[2])

ngrams = {}
with open('corpus/4gram.csv', 'r') as f:
    cr = csv.reader(f, delimiter='\t')
    for line in cr:
        ngrams[line[0]] = float(line[1])

monograms = {}
with open('corpus/1gram.csv', 'r') as f:
    cr = csv.reader(f, delimiter='\t')
    for line in cr:
        monograms[line[0]] = float(line[1])

for k in monograms:
    s = 'あいうえおかきくけこさしすせそたちつてとはひふへほゃゅょ'
    s2 = 'ぁぃぅぇぉがぎぐげござじずぜぞだぢづでどばびぶべぼやゆよ'
    h = 'はひふへほ'
    p = 'ぱぴぷぺぽ'
    if k in s2:
        index = s2.index(k)
        monograms[s[index]] += monograms[k]
    elif k in p:
        index = p.index(k)
        monograms[h[index]] += monograms[k]

    if k == 'ヴ':
        monograms['う'] += monograms[k]
monograms['゛'] = 0
monograms['゜'] = 0
monograms['S'] = 0
monograms['、'] = 2
monograms['。'] = 1
monograms[None] = 0

bigrams = {}
with open('corpus/2gram.csv', 'r') as f:
    cr = csv.reader(f, delimiter='\t')
    for line in cr:
        bigrams[line[0]] = float(line[1])

if __name__ == '__main__':
    pass
