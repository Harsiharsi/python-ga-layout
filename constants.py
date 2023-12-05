from copy import deepcopy

LEFT_KEYS = list('12345qwertasdfgzxcvb')
RIGHT_KEYS = list('7890-yuiophjkl;nm,./')
KEYS = LEFT_KEYS + RIGHT_KEYS
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
SMALL_KANAS = VOWEL_KANAS + Y_KANAS
SMALLED_KANAS = SMALL_VOWEL + SMALL_Y_KANAS
SPECIAL_LETTERS = DAKUTEN + HANDAKUTEN + SHIFT + SMALL_KANAS
VOICE_KANAS = list('なにぬねのまみむめもらりるれろわを')
LEFT_LETTERS = VOICELESS_KANAS
RIGHT_LETTERS = SMALL_KANAS + VOICE_KANAS + DAKUTEN + HANDAKUTEN
SPECIAL_MORAS = list('っんー')
ALL_CHARACTERS = LEFT_LETTERS + RIGHT_LETTERS + SPECIAL_MORAS

CHARACTER_PLACE = [
    [SHIFT, LEFT_KEYS],
    [VOICELESS_KANAS, LEFT_KEYS],
    [SMALL_KANAS + DAKUTEN + HANDAKUTEN, RIGHT_KEYS],
    [VOICE_KANAS, RIGHT_KEYS],
    [SPECIAL_MORAS, KEYS],
    [[None], KEYS],
]

FRONT = 0
BACK = 1
LAYER = [FRONT, BACK]
LAYERS = [None] * len(LAYER)

FIXED_CHARACTERS = TEN + MARU
FIXED_PLACE = list(',.')
FIXED = {',': [None, TEN[0]], '.': [None, MARU[0]]}

LAYOUT = {k: deepcopy(LAYERS) for k in KEYS}

CHARACTERS = list('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもゃゅょらりるれろわをんっー、。゛゜')
VOWELS = list('あいうえお')
SMALL_VOWELS = list('ぁぃぅぇぉ')
Y_ROW = list('ゃゅょ') #Y_ROW = list('やゆよ')
SMALL_Y = list('やゆよ') #SMALL_Y = list('ゃゅょ')
SMALL_DICT = {e1: e2 for e1, e2 in zip(VOWELS + Y_ROW, SMALL_VOWELS + SMALL_Y)}
VOICELESS_KANAS = list('かきくけこさしすせそたちつてとはひふへほ')
VOICE_KANAS = list('がぎぐげござじずぜぞだぢづでどばびぶべぼ')
H_ROW = list('はひふへほ')
P_ROW = list('ぱぴぷぺぽ')
VOICING_DICT = {e1: e2 for e1, e2 in zip(VOICELESS_KANAS, VOICE_KANAS)}
P_DICT = {e1: e2 for e1, e2 in zip(H_ROW, P_ROW)}
FRONT_KEYS = list('123457890-qwrtyuiopasdfghjkl;zxcvbnm,./')
SHIFTED_KEYS = list('!@#$%&*()_QWRTYUIOPASDFGHJKL:ZXCVBNM<>?')
KEYS = FRONT_KEYS + SHIFTED_KEYS
CHARACTERS += [None] * (len(KEYS) - len(CHARACTERS))
SHIFT_DICT = {e2: e1 for e1, e2 in zip(FRONT_KEYS, SHIFTED_KEYS)}
