"""Whether a customer's messages only close the conversation, so that saying nothing is fair.

A thumbs up, an "ok" or a "thanks" at the end of a chat asks for nothing. Answering it adds noise,
and handing the customer to a person over it is worse: the assistant goes silent for that customer
until someone resumes. So the model may decide that nothing needs to be said (``no_reply_needed``),
but it cannot silence a customer on its own say-so. This is the guard that runs before the helper
honours that decision. It is a closed list, not a guess about meaning, so a question can never pass.

The rule, for every message the customer has not been answered yet:

1. it is at most ``MAX_CHARS`` characters long;
2. it has no question mark in any script, and no digit (a number is content);
3. every word in it (letters only, accents and case folded, a letter repeated three or more times
   shortened, so "obrigadooo" and "okkk" count) is in a fixed list of Portuguese and English
   thanks, acknowledgements and the small words around them, with at most ``MAX_WORDS`` words, and
   at least one of them is a thanks or an acknowledgement itself, or two of them make a closing
   phrase ("era isso", "that's all");
4. a message with no words at all passes only when it holds an emoji or a symbol (a thumbs up).

A greeting ("oi", "bom dia"), a yes or a no, an offer accepted ("pode", "sim"), a request and every
other language are not in the list, so they are answered or handed over as before. Whether an "ok"
accepts something the assistant offered is the model's judgment: the contract tells it to answer
then, and this list cannot tell the two apart.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable

MAX_CHARS = 60
MAX_WORDS = 6

#: A question in any script. Checked on the text as written and after Unicode normalization.
_QUESTION_MARKS = frozenset("?¿？؟❓❔⁇⁈‽")

#: Words that thank or acknowledge. Folded: lower case, no accents.
ANCHORS = frozenset(
    """
    ok okay okey blz beleza certo certinho combinado entendi entendido perfeito perfeita otimo
    otima show top legal bacana joia massa valeu vlw obrigado obrigada obrigadinho obrigadao obg
    obgd brigado brigada agradeco agradecido agradecida grato grata fechado tranquilo tchau flw
    falou abraco abracos
    thanks thank thx thnx ty tysm cheers great perfect awesome cool nice alright noted understood
    appreciate appreciated bye goodbye cya
    """.split()
)
#: Small words that may stand next to them. None carries a question or a request.
FILLERS = frozenset(
    """
    muito demais bom bem pela pelo pelas pelos ajuda atencao informacao informacoes tempo rapidez
    resposta retorno gentileza simpatia paciencia atendimento era so isso isto ate logo mais um
    uma ta tah e a o mil voce voces vc vcs
    you so much very a lot big thats all it got sounds good for your the help time info
    information answer reply response quick quickly again see later soon really truly just is was
    been that
    """.split()
)
#: Two words that close a conversation together, though neither does alone.
PHRASES = frozenset(
    {
        ("era", "isso"),
        ("e", "isso"),
        ("so", "isso"),
        ("tudo", "certo"),
        ("ta", "bom"),
        ("ate", "logo"),
        ("ate", "mais"),
        ("thats", "all"),
        ("thats", "it"),
        ("got", "it"),
        ("sounds", "good"),
        ("all", "good"),
        ("see", "you"),
    }
)
_ALLOWED = ANCHORS | FILLERS | {word for pair in PHRASES for word in pair}
_LETTERS = re.compile(r"[^\W\d_]+", re.UNICODE)


def _normalize(text: str) -> str:
    """Compatibility forms folded, invisible characters gone, lower case, no accents."""
    kept = [ch for ch in unicodedata.normalize("NFKC", text) if unicodedata.category(ch) != "Cf"]
    decomposed = unicodedata.normalize("NFKD", "".join(kept).lower())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def _variants(word: str) -> Iterable[str]:
    """The word, and the word with repeated letters shortened ("obrigadooo", "okkk", "coool")."""
    yield word
    yield re.sub(r"(.)\1{2,}", r"\1\1", word)
    yield re.sub(r"(.)\1{2,}", r"\1", word)
    yield re.sub(r"(.)\1+", r"\1", word)


def _known(word: str) -> str | None:
    return next((v for v in _variants(word) if v in _ALLOWED), None)


def is_closing(text: str) -> bool:
    """True when ``text`` is a thanks or an acknowledgement and nothing else."""
    raw = text.strip()
    if not raw or len(raw) > MAX_CHARS:
        return False
    folded = _normalize(raw)
    if any(ch in _QUESTION_MARKS for ch in raw + folded):
        return False
    if any(ch.isnumeric() for ch in folded):
        return False
    letters = _LETTERS.findall(folded.replace("'", "").replace("’", ""))
    if not letters:
        # no words: a thumbs up, folded hands, a heart. Punctuation alone says nothing.
        return any(unicodedata.category(ch) in ("So", "Sk") for ch in raw)
    if len(letters) > MAX_WORDS:
        return False
    words = [_known(word) for word in letters]
    if any(word is None for word in words):
        return False
    known = [word for word in words if word is not None]
    pairs = {(a, b) for a, b in zip(known, known[1:])}
    return any(word in ANCHORS for word in known) or bool(pairs & PHRASES)


def closes_conversation(texts: Iterable[str]) -> bool:
    """True when there is at least one message and every one of them is a closing."""
    messages = list(texts)
    return bool(messages) and all(is_closing(text) for text in messages)
