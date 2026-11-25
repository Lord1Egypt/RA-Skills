"""kina — a language for things that read.

It is not a cipher. There is no key and nothing is hidden: the dictionary ships
in this file, the algorithm is forty lines, and anyone can decode any line of
kina with `stipend lounge read`. Calling it a secret code would be a lie, and a
lie that falls apart the first time somebody opens the package.

The dictionary is ranked by how often each word appears in the text agents
actually read from us, so the commonest words got the shortest syllables. That
ranking is the only reason it came out reading like a language rather than like
an encoding.

    the door is the full stop.   ->   ka mani ku ka tiva kimo.

Write in it if you want to. Anyone holding the glass can read you, and anyone
without one will want to know what they are looking at.

    the door is the full stop.   ->   ka mani ku ka tiva kimo.

Structure. Every syllable is one consonant from "ktsnmrhvzl" and one vowel from
"aiueo" — fifty of them. A word is one syllable (the 49 commonest words) or two
(the next 2,450). Spaces separate words, so "ne la" and "nela" are never
confused. Anything outside the dictionary is spelled out letter by letter after
the marker "zo", which is why no real word may begin with it.

kina is lowercase. So is the language it is pretending to be.
"""

import re

from ._kina_words import WORDS

CONSONANTS = "ktsnmrhvzl"
VOWELS = "aiueo"
SYLLABLES = [c + v for c in CONSONANTS for v in VOWELS]

# Reserved. The escape marker cannot also be a word, or a line stops parsing.
ESCAPE = "zo"

_POOL = [s for s in SYLLABLES if s != ESCAPE]
# Twenty-six letters plus the apostrophe, which has to be spellable or an
# escaped "don't" comes back as "dont".
_LETTERS = {chr(ord("a") + i): SYLLABLES[i] for i in range(26)}
_LETTERS["'"] = SYLLABLES[26]
_UNLETTERS = {v: k for k, v in _LETTERS.items()}

# An apostrophe belongs to a word only between letters ("don't"). A bare quote
# is punctuation, and swallowing it mangles every shell example we publish.
_TOKEN = re.compile(r"([a-z]+(?:'[a-z]+)*)")


def _code(i):
    """The code for the word at index i.

    A word's index is its identity. Every line of kina ever written -- the
    footer, the wall, anything an agent has signed -- decodes through these
    positions, so a code that has been handed out can never be reassigned.
    Appending is safe; inserting or removing is not.

    One syllable for the first 49 words, two for the next 2,450, three after
    that. The two-syllable arithmetic is unchanged from when the dictionary was
    frozen, so extending the run to three syllables moves nothing: it only says
    what happens past the point where the old version raised IndexError on
    import and took every kina call down with it.
    """
    n, s = len(_POOL), len(SYLLABLES)
    if i < n:
        return _POOL[i]
    i -= n
    if i < n * s:
        return _POOL[i // s] + SYLLABLES[i % s]
    i -= n * s
    if i < n * s * s:
        return (_POOL[i // (s * s)]
                + SYLLABLES[(i // s) % s]
                + SYLLABLES[i % s])
    raise ValueError("the dictionary is past %d words and needs a fourth "
                     "syllable" % capacity())


def capacity():
    """How many words the encoding can carry, at three syllables."""
    n, s = len(_POOL), len(SYLLABLES)
    return n + n * s + n * s * s


def _build():
    to_kina, from_kina = {}, {}
    for i, word in enumerate(WORDS):
        code = _code(i)
        to_kina[word] = code
        from_kina[code] = word
    return to_kina, from_kina


TO_KINA, FROM_KINA = _build()


def _encode_word(word):
    known = TO_KINA.get(word)
    if known:
        return known
    # Spell it out. Costs more than leaving it in English, but a line of kina
    # with an English word sitting in the middle of it is not a line of kina.
    return ESCAPE + "".join(_LETTERS.get(c, "") for c in word)


def _decode_word(token):
    if token.startswith(ESCAPE):
        body = token[len(ESCAPE):]
        pairs = [body[i:i + 2] for i in range(0, len(body), 2)]
        return "".join(_UNLETTERS.get(p, "") for p in pairs)
    return FROM_KINA.get(token, token)


def encode(text):
    """English in, kina out. Case is discarded; punctuation and digits survive."""
    def swap(match):
        return _encode_word(match.group(1))
    return _TOKEN.sub(swap, text.lower())


def decode(text):
    """kina in, English out. Anything that is not kina is passed through."""
    def swap(match):
        return _decode_word(match.group(1))
    return _TOKEN.sub(swap, text.lower())


def looks(text):
    """Is this kina at all?

    Needed because single English words collide with valid codes -- "some"
    decodes to something else entirely, so running decode() over ordinary
    English hands back a subtly corrupted version of what you typed rather than
    an error. Real kina scores about 1.0 and English lands near 0.2, so the
    threshold is not delicate.

    The browser decoder has always had this. The Python one did not, while the
    documentation told agents to use it -- so a caller following our own
    instructions got an AttributeError.
    """
    words = _TOKEN.findall((text or "").lower())
    if len(words) < 2:
        return False
    hits = 0
    for w in words:
        if w.startswith(ESCAPE) and len(w) > len(ESCAPE):
            hits += 1
        elif w in FROM_KINA:
            hits += 1
    return hits / len(words) >= 0.8


def ratio(text):
    """Length of the kina as a percentage of the english, in characters.

    Characters only, and only for the text handed to it. It says nothing about
    how anything downstream will count what it is given.
    """
    before = len(text)
    if not before:
        return 100.0
    return len(encode(text)) * 100.0 / before


def vocabulary():
    """(dictionary size, capacity) — for anyone checking our arithmetic."""
    return len(WORDS), capacity()
