"""A guess at the language of a customer's message: Portuguese, English, or neither.

The helper normally learns a customer's language from the model, which reports it with each
answer. When the model's answer is refused twice, the helper writes the hand-off itself and, for a
customer who is new, nothing has recorded a language yet. This counts common words of each language
in what the customer wrote. Words that both languages use are left out of the lists, a tie or no
hit means "no guess", and the caller then keeps the language it already had.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Literal, Optional

Guess = Literal["pt", "en"]

_PT = frozenset(
    """
    o os um uma uns umas de do da dos das em na nas nos pelo pela por para pra pro com sem que eu
    voce voces vc vcs tem temos tenho quero queria gostaria qual quais quanto quanta quantos
    quantas quando onde como nao sim obrigado obrigada oi ola bom boa dia tarde noite favor esta
    estao sao foi mais muito tambem aqui meu minha seu sua isso esse essa pode posso podem vai
    entrega frete preco troca devolucao pagamento cartao horario abre abrem loja
    """.split()
)
_EN = frozenset(
    """
    the of to in is are was were be been am i you your yours we our it its this that these those
    does did have has had what which who when where how can could would should will shall may
    might please thanks thank hello hi hey good morning afternoon evening not yes my with without
    from at on by and or but if just also here there much many open opens closed delivery
    shipping price cost return exchange refund pay payment card hours store shop they them their
    he she her his him
    """.split()
)

_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def _fold(word: str) -> str:
    base = unicodedata.normalize("NFKD", word.lower())
    return "".join(ch for ch in base if not unicodedata.combining(ch))


def guess_language(text: str) -> Optional[Guess]:
    """``pt`` or ``en`` when one language has more of its common words in ``text``, else None."""
    words = [_fold(w) for w in _WORD.findall(text)]
    portuguese = sum(1 for w in words if w in _PT)
    english = sum(1 for w in words if w in _EN)
    if portuguese > english:
        return "pt"
    if english > portuguese:
        return "en"
    return None
