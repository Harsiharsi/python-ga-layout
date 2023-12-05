import random
import csv
import itertools
import math
import re
from copy import deepcopy
from functools import reduce
from traceback import format_exc
from deap.tools import selRandom
from operator import attrgetter

import data
import constants

LEFT_FRONT_KEYS = list('12345qwertasdfgzxcvb')
LEFT_BACK_KEYS = list('!@#$%QWERTASDFGZXCVB')
LEFT_KEYS = LEFT_FRONT_KEYS + LEFT_BACK_KEYS
RIGHT_FRONT_KEYS = list('67890yuiophjkl;nm,./')
RIGHT_BACK_KEYS = list('^&*()YUIOPHJKL:NM<>?')
RIGHT_KEYS = RIGHT_FRONT_KEYS + RIGHT_BACK_KEYS

FRONT_KEYS = LEFT_FRONT_KEYS + RIGHT_FRONT_KEYS
BACK_KEYS = LEFT_BACK_KEYS + RIGHT_BACK_KEYS
KEYS = FRONT_KEYS + BACK_KEYS

FRONT_TO_BACK = {f:b for f, b in zip(FRONT_KEYS + BACK_KEYS, BACK_KEYS + BACK_KEYS)}
BACK_TO_FRONT = {b:f for b, f in zip(BACK_KEYS + FRONT_KEYS, FRONT_KEYS + FRONT_KEYS)}

TEN = list('、')
MARU = list('。')
DAKUTEN = list('゛')
HANDAKUTEN = list('゜')
SHIFT = list('S')
VOICELESS_KANAS = list('かきくけこさしすせそたちつてとはひふへほ')
VOICED_KANAS = list('がぎぐげござじずぜぞだぢづでどばびぶべぼ')
H_KANAS = list('はひふへほ')
P_KANAS = list('ぱぴぷぺぽ')
VOWEL_KANAS = list('あいうえお')
SMALL_VOWEL = list('ぁぃぅぇぉ')
SMALL_Y_KANAS = list('やゆよ')
Y_KANAS = list('ゃゅょ')
VOICE_KANAS = list('なにぬねのまみむめもらりるれろわを')
SPECIAL_MORAS = list('っんー')

LEFT_SPECIAL_CHARACTERS = SHIFT
RIGHT_SPECIAL_CHARACTERS = VOWEL_KANAS + Y_KANAS + HANDAKUTEN + DAKUTEN
SPECIAL_CHARACTERS = LEFT_SPECIAL_CHARACTERS + RIGHT_SPECIAL_CHARACTERS

CHARACTERS = TEN + MARU + VOICELESS_KANAS + VOICE_KANAS + SPECIAL_MORAS

KEYS_CHARS = [
    [FRONT_KEYS, SPECIAL_CHARACTERS],
    [KEYS, CHARACTERS],
]

sample = lambda l: random.sample(l, len(l))

def split_keys_to_chunks(s):
    candidates = [s[0:i] for i in range(4, 0, -1)]
    possibles = [data.COMBOS[c] for c in candidates if data.COMBOS.get(c)]
    selected = [combo for combo in possibles if not (len(combo.pattern) == 2 and combo.score >= 110)][0]

    n = len(selected.pattern)
    return [selected] + split_keys_to_chunks(s[n:]) if len(s) > n else [selected]

def classify_chunks_into_hands(l):
    left_chunks = [e for e in l if e.hand == 'l']
    right_chunks = [e for e in l if e.hand == 'r']
    return (left_chunks, right_chunks)

def chunks_to_interchunks(l):
    interchunks = [[]]

    for e in l:
        last = interchunks[-1]
        if last == []:
            last.append(e)
            continue

        key_history = reduce(lambda x, y: x + y.pattern, last, '')
        same_finger = [True
                         for k in key_history
                         for ek in e.pattern
                         if (len(k + ek) == 2 and data.COMBOS[k + ek].score >= 110)]
        if not same_finger:
            last.append(e)
        else:
            interchunks.append([e])

    return interchunks

def evaluate_chunks(l):
    score = 0
    key_history = ''

    for e in l:
        score += e.score

        if not key_history:
            key_history += e.pattern
            continue

        worst = max([data.COMBOS[k + k2].score for k in e.pattern for k2 in key_history])

        penalty = 1.1 if data.COMBOS.get(key_history + e.pattern) else 1.3
        score += worst * penalty
        key_history += e.pattern

    return score

def evaluate_interchunks(l):
    score = 0
    interchunk = []

    for e in l:
        if interchunk == []:
            interchunk = e
            continue

        last_keys = reduce(lambda x, y: x + y.pattern, interchunk, '')
        keys = reduce(lambda x, y: x + y.pattern, e, '')
        worst = max([data.COMBOS[k + k2].score for k in last_keys for k2 in keys])
        score += worst * 1.4
        interchunk = e

    return score

def evaluate(s):
    score = 0
    both_hand_chunks = classify_chunks_into_hands(split_keys_to_chunks(s))

    interchunks = []
    for ic in both_hand_chunks:
        interchunks.append(chunks_to_interchunks(ic))

    for ic in interchunks:
        for chunk in ic:
            score += evaluate_chunks(chunk)

        score += evaluate_interchunks(ic)

    return score

class Layout():
    best_ind = None
    second_best_ind = None

    def __init__(self, p1=None, p2=None):
        self.layout = {}
        self.kana_to_key = {}
        self.fitness = 0

        if p1 and p2:
            self.crossover(p1, p2)
        else:
            self.put_characters_randomly()

        self.make_kana_to_key_dictionary()

    def put_characters_randomly(self):
        layout = {k:None for k in KEYS}

        for keys, chars in KEYS_CHARS:
            cs = sample(chars)
            ks = sample([k for k in keys if layout[k] == None])
            for k, c in zip(ks, cs):
                if chars == SPECIAL_CHARACTERS:
                    layout[BACK_TO_FRONT[k]] = c
                    layout[FRONT_TO_BACK[k]] = c
                else:
                    layout[k] = c

        self.layout = layout
        self.push_to_front()

    def push_to_front(self):
        self.push_high_freq_chars_to_front()
        self.push_back_chars_to_front()

    def push_high_freq_chars_to_front(self):
        keys = sample(FRONT_KEYS)
        front_chars = [self.layout[k] for k in keys]
        back_chars = [self.layout[FRONT_TO_BACK[k]] for k in keys]
        chars = [(f, b) if data.monograms[f] > data.monograms[b] else (b, f) for f, b in zip(front_chars, back_chars)]

        for k, c in zip(keys, chars):
            self.layout[k] = c[0]
            self.layout[FRONT_TO_BACK[k]] = c[1]

    def push_back_chars_to_front(self):
        front_back_keys = [
            [FRONT_KEYS, BACK_KEYS],
        ]
        for keys in front_back_keys:
            front_keys = keys[0]
            back_keys = keys[1]
            front_none_keys = sample([k for k in front_keys if self.layout[k] == None])
            back_assinged_keys = sample([k for k in back_keys if self.layout[k] != None and self.layout[k] not in SPECIAL_CHARACTERS])
            for fk, bk in zip(front_none_keys, back_assinged_keys):
                self.layout[fk] = self.layout[bk]
                self.layout[bk] = None

    def crossover(self, p1, p2):
        layout = {k:None for k in KEYS}

        for keys, chars in KEYS_CHARS:
            ks = sample(keys)
            cs = sample(chars)
            for c in cs:
                chosen = p1 if random.random() < 0.5 else p2
                another = p2 if chosen == p1 else p1
                ck = [k for k in chosen.layout.keys() if k in ks and chosen.layout[k] == c]
                ak = [k for k in another.layout.keys() if k in ks and another.layout[k] == c]

                for k in ck + ak + keys:
                    if c in SPECIAL_CHARACTERS:
                        if layout.get(k) == None and layout.get(FRONT_TO_BACK[k]) == None:
                            layout[BACK_TO_FRONT[k]] = c
                            layout[FRONT_TO_BACK[k]] = c
                            break

                    if layout.get(k) == None:
                        layout[k] = c
                        break

        self.layout = layout
        self.push_to_front()

    def mutate(self, indpb=0.1):
        self.fitness = 0

        left_right_front_keys = [FRONT_KEYS]
        for keys in left_right_front_keys: 
            ks = sample(keys)
            frcs = [self.layout[k] for k in ks]
            bcs = [self.layout[FRONT_TO_BACK[k]] for k in ks]
            cs = [(frc, bc) for frc, bc in zip(frcs, bcs)]
            n = int(len(ks) * indpb)
            n = n if n >= 2 else 2
            mutant_keys = sample(ks[0:n]) + ks[n:]
            for k, c in zip(mutant_keys, cs):
                self.layout[k] = c[0]
                self.layout[FRONT_TO_BACK[k]] = c[1]

        left_right_keys = [KEYS]
        for keys in left_right_keys:
            ks = sample([k for k in keys if self.layout[k] not in SPECIAL_CHARACTERS])
            cs = [self.layout[k] for k in ks]
            n = int(len(ks) * indpb)
            n = n if n >= 2 else 2
            mutant_keys = sample(ks[0:n]) + ks[n:]
            for k, c in zip(mutant_keys, cs):
                self.layout[k] = c

        self.push_to_front()
        self.make_kana_to_key_dictionary()

    def make_kana_to_key_dictionary(self):
        shift = [k for k in FRONT_KEYS if self.layout[k] in SHIFT][0]
        dakuten = [k for k in FRONT_KEYS if self.layout[k] in DAKUTEN][0]
        handakuten = [k for k in FRONT_KEYS if self.layout[k] in HANDAKUTEN][0]

        for k in self.layout.keys():
            c = self.layout[k]

            shifted = ''
            if k in BACK_KEYS:
                shifted = shift
                k = BACK_TO_FRONT[k]

            self.kana_to_key[c] = k + shifted

            if c in constants.VOICELESS_KANAS:
                self.kana_to_key[constants.VOICING_DICT[c]] = k + shifted + dakuten

                if c in constants.H_ROW:
                    self.kana_to_key[constants.P_DICT[c]] = k + shifted + handakuten

            elif c in constants.SMALL_DICT.keys():
                self.kana_to_key[constants.SMALL_DICT[c]] = k + shift
                if c == 'う':
                    self.kana_to_key['ヴ'] = k + dakuten

    def evaluate(self):
        self.fitness = 0

        ngrams = data.ngrams
        for ng in ngrams:
            frequency = ngrams[ng]

            l = [self.kana_to_key.get(c) for c in ng if self.kana_to_key.get(c)]
            s = reduce(lambda x, y: x + y, l, '')
            if not s:
                continue
            self.fitness += evaluate(s) * frequency

    @classmethod
    def tournament(cls, individuals, k, tournsize, fit_attr='fitness'):
        chosen = []
        for i in range(k):
            aspirants = selRandom(individuals, tournsize)
            chosen.append(min(aspirants, key=attrgetter(fit_attr)))
        return chosen

    def __str__(self):
        s = ''
        for i, k in enumerate('1234567890qwertyuiopasdfghjkl;zxcvbnm,./!@#$%^&*()QWERTYUIOPASDFGHJKL:ZXCVBNM<>?'):
            c = self.layout[k] if self.layout.get(k) else None
            if c:
                s += c
            else:
                s += ' *'

            if (i + 1) % 10 == 0:
                s += '\n'
            elif (i + 1) % 5 == 0:
                s += '   '

            if (i + 1) % (len(constants.FRONT_KEYS) + 1) == 0 and \
                not (i + 1) == (len(constants.FRONT_KEYS) + 1) * 2:
                s += '-------------------------\n'

        return s[:-1]

if __name__ == '__main__':
    pass
