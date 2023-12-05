import csv
import itertools
from functools import reduce


figure = [
    '1qaz0p;/\'[',
    '2wsx9ol.',
    '3edc8ik,',
    '4rfv5tgb7ujm6yhn',
]

d = {}
with open('combinations.csv', 'r', encoding='utf-8') as f:
    cr = csv.reader(f, delimiter=' ')
    for e in cr:
        if e == []:
            continue

        s = e[0]
        n = float(e[1])
        d[''.join(sorted(s))] = n
        d[''.join(sorted(s, reverse=True))] = n

with open('combinations_made.csv', 'w', encoding='utf-8') as f:
    cs = '12345qwertasdfgzxcvb67890yuiophjkl;nm,./[\''

    for k in cs:
        hand = 'l' if k[0] in '12345qwertasdfgzxcvb' else 'r'
        f.write(k + ' ' + '0' + ' ' + hand + '\n')

    for k in d:
        hand = 'l' if k[0] in '12345qwertasdfgzxcvb' else 'r'
        f.write(k + ' ' + str(d[k]) + ' ' + hand + '\n')

    for i in [3, 4]:
        p = list(itertools.permutations(cs, i))
        combos = [''.join(e) for e in p]
        for co in combos:
            not_combo = False
            two_combos = list(itertools.combinations(co, 2))
            two_combos = [''.join(e) for e in two_combos]
            chuncks = [tco for tco in two_combos if d.get(tco) and d[tco] < 110]
            if set(chuncks) != set(two_combos):
                continue

            is_orderd = True
            for s in [co, co[::-1]]:
                l = []
                for c in s:
                    for i, e in enumerate(figure):
                        if c in e:
                            l.append(i)

                if l not in [sorted(l), sorted(l, reverse=True)]:
                    is_orderd = False
            if not is_orderd:
                continue

            worsts = sorted([d[ch] for ch in chuncks], reverse=True)[0:i-1]
            score = reduce(lambda x, y: x + y, worsts)
            hand = 'l' if co[0] in '12345qwertasdfgzxcvb' else 'r'
            f.write(co + ' ' + str(score * 0.7) + ' ' + hand + '\n')
