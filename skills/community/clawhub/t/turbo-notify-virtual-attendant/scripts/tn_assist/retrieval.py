"""Which knowledge files go into a customer's pack besides the core ones.

The core files (company, tone, hand-off) always go in. For the rest the helper reads the words of
the new message, of the recent conversation and of what is known about the customer, and picks the
files of the index that share the most of them. The same words always pick the same files; ties go
by path.

Four things keep a plain word match honest:

* Filler is ignored ("como", "posso", "the", "can"): it must not take a slot from a real word.
* Words match by their first four letters, so "pagar" finds "pagamento" and "trocar" finds "troca".
* A rare word counts more than one that is in every file.
* A small built-in vocabulary of shop words, in Portuguese and English, ties together what a
  customer and an owner say differently ("reembolso" and "devolução", "pay" and "pagamento"). It
  only adds weaker matches: a word the customer really wrote always counts more.

The limit counts files other than the core ones, so the core files can never use up the slots.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from collections.abc import Collection, Iterator

STEM_LETTERS = 4
MIN_LETTERS = 3
#: How much a match is worth, by where the word came from.
NEW_MESSAGE = 2.0
RECENT = 1.0
PROFILE = 0.5
#: A word added by the vocabulary is worth this share of the word that added it.
RELATED = 0.6

_WORD = re.compile(r"\w+", re.UNICODE)
_INDEX_LINE = re.compile(r"^-\s+([\w./-]+\.md):\s*(.*)$")

#: Words that say nothing about a subject. Folded: lower case, no accents.
STOPWORDS = frozenset(
    """
    que por com sem sob sobre entre ate desde uma uns umas dos das nos nas pelo pela pelos pelas
    para pra mas como quando onde qual quais quem porque pois entao assim ainda tambem nem nao sim
    ja mais menos muito muita muitos muitas pouco pouca tudo todo toda todos todas cada algum
    alguma alguns algumas nenhum nenhuma outro outra outros outras mesmo mesma eles elas ele ela
    voce voces meu minha meus minhas seu sua seus suas nosso nossa nossos nossas dele dela deles
    delas isso isto aquilo esse essa esses essas este esta estes estas aquele aquela aqui ali aca
    agora hoje amanha ontem depois antes logo sempre nunca talvez apenas somente tao bem mal sou
    foi era sao somos fui estar estou estao estamos estava tem tenho temos tinha tive havia houve
    vou vai vamos vao fazer faz fazem fazemos fiz fez dar dou dao deu dizer diz disse ver vejo veja
    viu saber sei sabe sabem poder posso pode podem podemos podia poderia puder querer quero quer
    querem queremos queria gostaria gostar precisar preciso precisa precisamos precisam precisava
    dever devo deve devem devemos ficar fica ficam ficou pedir peco pede olhar olha olhada ola oi
    opa obrigado obrigada valeu favor duvida duvidas pergunta perguntar perguntei ajuda ajudar ajudo
    possivel possiveis informacao informacoes informar informa coisa coisas pessoa pessoas gente
    vez vezes tipo whatsapp wpp zap
    the and for with from have has had will would could should can may might your you our their
    them they this that these those what which who whom whose how when where why does did done
    doing was were been being are not but its his her him she any all yes now get got let want
    need like know tell help please thanks thank hello hey okay sure just also really very
    more most some than then there here too each other such into over under again once only
    own same don doesn didn isn aren wasn weren won wouldn couldn shouldn hasn haven hadn ain
    """.split()
)

#: Shop words that mean about the same thing, in Portuguese and English. Folded.
_GROUPS = (
    # paying
    """pagar pagamento pago pagando pix cartao credito debito boleto parcelar parcelamento parcela
    juros vista pay paying payment card credit debit installment installments cash transfer""",
    # returning, exchanging and getting money back
    """reembolso reembolsar reembolsam estorno estornar devolver devolucao devolvemos troca trocar
    trocas arrependimento desistir desistencia cancelar cancelamento volta refund refunds return
    returns exchange exchanges cancel cancellation""",
    # delivery and pickup
    """entrega entregar entregue entregamos frete envio enviar remessa correio transportadora
    retirada retirar bairro cep prazo delivery deliver shipping ship shipment courier pickup
    postage district neighborhood neighbourhood""",
    # prices, discounts and offers ("how much" is a question about a price)
    """preco precos valor valores custo custa custar quanto tabela catalogo orcamento promocao
    desconto descontos cupom cupons oferta ofertas price prices cost costs quote catalog catalogue
    discount discounts coupon coupons offer offers promotion sale much""",
    # opening hours and where the shop is (not "loja" or "shop": nearly every file says it)
    """horario horarios hora abre abrir aberto aberta fecha fechar fechado funcionamento expediente
    domingo sabado feriado endereco localizacao hours hour open opening close closing closed
    address location holiday sunday saturday""",
    # warranty and defects
    """garantia garantir defeito defeituoso assistencia conserto quebrou quebrar warranty guarantee
    defect defective broken repair""",
    # products and stock
    """produto produtos item itens modelo cor tamanho estoque disponivel disponibilidade unidade
    unidades vender vendem vende product products items model color colour size stock available
    availability unit units many sell sells sold""",
)


def _fold(word: str) -> str:
    base = unicodedata.normalize("NFKD", word.lower())
    return "".join(ch for ch in base if not unicodedata.combining(ch))


def _words(text: str) -> Iterator[str]:
    for raw in _WORD.findall(text):
        word = _fold(raw)
        if len(word) >= MIN_LETTERS and word not in STOPWORDS:
            yield word


def stems(text: str) -> set[str]:
    """The subject words of a text, each cut to its first letters."""
    return {word[:STEM_LETTERS] for word in _words(text)}


def _related() -> dict[str, frozenset[str]]:
    related: dict[str, set[str]] = {}
    for group in _GROUPS:
        members = stems(group)
        for member in members:
            related.setdefault(member, set()).update(members - {member})
    return {stem: frozenset(others) for stem, others in related.items()}


_RELATED = _related()


def parse_index(index_text: str) -> list[tuple[str, str]]:
    entries = []
    for line in index_text.splitlines():
        match = _INDEX_LINE.match(line.strip())
        if match:
            entries.append((match.group(1), match.group(2)))
    return entries


def _wanted(texts: tuple[tuple[str, float], ...]) -> dict[str, float]:
    """Each subject word with the best weight it came with, and its relatives at a lower one."""
    wanted: dict[str, float] = {}
    for text, weight in texts:
        for stem in stems(text):
            wanted[stem] = max(wanted.get(stem, 0.0), weight)
            for other in _RELATED.get(stem, ()):
                wanted[other] = max(wanted.get(other, 0.0), weight * RELATED)
    return wanted


def select_knowledge(
    index_text: str,
    query: str,
    limit: int = 3,
    bodies: dict[str, str] | None = None,
    *,
    recent: str = "",
    profile: str = "",
    exclude: Collection[str] = (),
) -> list[str]:
    """Up to ``limit`` files of the index, best match first, never one of ``exclude``.

    ``query`` is the new message; ``recent`` the last lines of the conversation and ``profile`` what
    is known about the customer, both counted for less. A file is read as its path, its description
    in the index and the start of its text.
    """
    skip = set(exclude)
    docs = {
        path: stems(f"{path} {description} {(bodies or {}).get(path, '')[:2000]}")
        for path, description in parse_index(index_text)
        if path not in skip
    }
    if not docs:
        return []
    frequency = Counter(stem for found in docs.values() for stem in found)
    wanted = _wanted(((query, NEW_MESSAGE), (recent, RECENT), (profile, PROFILE)))
    scored = []
    for path, found in docs.items():
        score = sum(
            weight * math.log(1 + len(docs) / frequency[stem])
            for stem, weight in wanted.items()
            if stem in found
        )
        if score > 0:
            scored.append((-round(score, 9), path))
    scored.sort()
    return [path for _, path in scored[: max(0, limit)]]
