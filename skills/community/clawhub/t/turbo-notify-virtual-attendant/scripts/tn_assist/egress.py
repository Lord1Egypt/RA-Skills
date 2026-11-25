"""The egress guard: what may leave toward one customer.

Deterministic and conservative. A reply is refused when it contains another person's number or
name, text from a non-public source, a credential, or a personal-data pattern that the customer
did not supply and public knowledge does not publish. A refusal is safe by design: the caller turns
it into a hand-off, never into a retry.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from tn_assist.config import admin_numbers
from tn_assist.memory import Card, Fact, read_lines
from tn_assist.paths import ContactKey, InvalidContactKey, Workspace
from tn_assist.sources import SourceRegistry

SHINGLE = 5
_NUMBERISH = re.compile(r"\+?[0-9](?:[0-9\s().\-/,_\u00b7\u2022:]{6,}[0-9])")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_CREDENTIAL = re.compile(r"tn_(?:live|oat|oup|ort)_[A-Za-z0-9_-]{8,}", re.IGNORECASE)
_WORD = re.compile(r"\w+", re.UNICODE)
_DATE = re.compile(
    r"(?<![0-9])(?:0?[1-9]|[12][0-9]|3[01])[/.\-](?:0?[1-9]|1[0-2])[/.\-](?:[0-9]{4}|[0-9]{2})(?![0-9])"
)
_MONEY = re.compile(
    r"(?:R\$|US\$|\$|\u20ac|EUR|USD|BRL)\s?[0-9]{1,3}(?:[.,][0-9]{3})*(?:[.,][0-9]{2})?(?![0-9])",
    re.IGNORECASE,
)
MAX_MONEY_DIGITS = 9


@dataclass(frozen=True)
class EgressVerdict:
    ok: bool
    reasons: tuple[str, ...] = ()


NOTE_PREFIX = "note_"
MIN_NOTE_WORDS = 3  # a one or two word note ("pago") says too little to be a quote


def _contains(words: list[str], sequence: list[str]) -> bool:
    size = len(sequence)
    return any(words[i : i + size] == sequence for i in range(len(words) - size + 1))


def _normalize(text: str) -> str:
    """What a reader would see: compatibility forms folded, invisible characters gone, every
    Unicode dash and space turned into a plain one. Detection runs on this, never on raw text."""
    out = []
    for ch in unicodedata.normalize("NFKC", text):
        category = unicodedata.category(ch)
        if category == "Cf":
            continue
        if category == "Nd":
            out.append(str(unicodedata.digit(ch)))
        elif category == "Pd" or ch in "\u2212\u2011\u2010":
            out.append("-")
        elif category in ("Zs", "Zl", "Zp") or ch in "\t\r\n":
            out.append(" ")
        else:
            out.append(ch)
    return "".join(out)


def _fold(text: str) -> str:
    base = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in base if not unicodedata.combining(ch))


def _words(text: str) -> list[str]:
    return _WORD.findall(_fold(text))


def _shingles(text: str) -> set[tuple[str, ...]]:
    words = _words(text)
    return {tuple(words[i : i + SHINGLE]) for i in range(max(0, len(words) - SHINGLE + 1))}


def _digit_runs(text: str) -> list[str]:
    runs = []
    for match in _NUMBERISH.finditer(text):
        digits = re.sub(r"[^0-9]", "", match.group(0))
        if 8 <= len(digits) <= 19:
            runs.append(digits)
    return runs


def _mask_dates_and_money(text: str) -> str:
    """Hide what is plainly a date or a price from the "unknown number" rule. A match with too
    many digits to be a price is left in place, so a long number cannot hide inside a currency."""
    text = _DATE.sub(" ", text)

    def money(match: re.Match[str]) -> str:
        digits = re.sub(r"[^0-9]", "", match.group(0))
        return " " if len(digits) <= MAX_MONEY_DIGITS else match.group(0)

    return _MONEY.sub(money, text)


def _same_person(digits: str, number: str) -> bool:
    return digits.endswith(number) or number.endswith(digits)


def _canonical(digits: str) -> str:
    try:
        return str(ContactKey.parse(digits))
    except InvalidContactKey:
        return digits


def _read(ws: Workspace, *parts: str) -> str:
    try:
        return ws.path(*parts).read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError):
        return ""


def _knowledge_texts(ws: Workspace) -> tuple[str, str]:
    """(public text, non-public text) of the knowledge base."""
    public: list[str] = []
    internal: list[str] = []
    root = ws.path("knowledge")
    if root.is_dir():
        for path in sorted(root.rglob("*.md")):
            relative = path.relative_to(root).parts
            target = internal if relative[0] == "internal" else public
            target.append(path.read_text(encoding="utf-8"))
    return "\n".join(public), "\n".join(internal)


# Words a customer could set as their WhatsApp display name to make every reply that uses the word
# look like a leak (a hand-off for everyone else). A one-word name from WhatsApp that is one of
# these is not protected; a person-confirmed name always is.
COMMON_WORDS = frozenset(
    """obrigado obrigada valeu thanks thank hello hola ola oi ola bom boa dia tarde noite bye tchau
    sim nao yes none nome name cliente customer loja store atendente suporte support empresa company
    pedido order preco price valor total plano plan mensal anual monthly annual entrega delivery
    prazo horario hours segunda terca quarta quinta sexta sabado domingo monday tuesday wednesday
    thursday friday saturday sunday hoje amanha today tomorrow aqui here agora now ajuda help
    produto product servico service desconto discount pagamento payment""".split()
)


def _protects(fact: Fact) -> bool:
    """Whether another customer's name keeps replies from mentioning it.

    A person-confirmed name always does, and so does any full name. A one-word name only when
    WhatsApp reported it (the model's own inference from a stranger's words never counts) and it is
    not a word every reply uses.
    """
    if fact.source in ("admin", "attendant") or len(fact.value.split()) >= 2:
        return True
    return fact.source == "platform" and _fold(fact.value).strip() not in COMMON_WORDS


def _other_contacts(ws: Workspace, contact: ContactKey) -> tuple[set[str], set[str]]:
    numbers: set[str] = set(admin_numbers(ws))
    names: set[str] = set()
    contacts = ws.root / "contacts"
    if contacts.is_dir():
        for directory in contacts.iterdir():
            if not directory.is_dir() or directory.name == str(contact):
                continue
            numbers.add(directory.name)
            try:
                card = Card.load(ws, ContactKey.parse(directory.name))
            except InvalidContactKey:
                continue
            fact = card.get("name")
            if fact and len(fact.value) >= 4 and _protects(fact):
                names.add(fact.value)
    return numbers, names


def _own_text(ws: Workspace, contact: ContactKey) -> str:
    """Only what this person said, or what a human confirmed about them. Facts the model inferred
    are left out on purpose: the model could otherwise whitelist a leak by recording it first."""
    said = [ln.text for ln in read_lines(ws, contact) if ln.role == "contact"]
    confirmed = [
        f.value
        for f in Card.load(ws, contact).facts()
        if f.source != "inferred" and not f.key.startswith(NOTE_PREFIX)
    ]
    return " ".join(said + confirmed + [str(contact)])


def check_egress(ws: Workspace, text: str, *, contact: ContactKey) -> EgressVerdict:
    reasons: set[str] = set()
    text = _normalize(text)
    public_text, internal_text = _knowledge_texts(ws)
    # What the team wrote about this customer is for the team: it must not come back as a quote.
    notes = [f.value for f in Card.load(ws, contact).facts() if f.key.startswith(NOTE_PREFIX)]
    if notes:
        internal_text = f"{internal_text}\n{' '.join(notes)}"
    own_text = _normalize(_own_text(ws, contact))
    public_text = _normalize(public_text)
    allowed_digits = {_canonical(d) for d in _digit_runs(public_text + " " + own_text)}
    allowed_digits.add(str(contact))
    allowed_mail = {m.lower() for m in _EMAIL.findall(public_text + " " + own_text)}
    others, other_names = _other_contacts(ws, contact)

    # Dates and amounts of money are not phone numbers, but only for the "unknown number" rule:
    # another contact's number is looked for in the whole text, however it is dressed.
    def is_allowed(canonical: str) -> bool:
        return canonical in allowed_digits or any(
            _same_person(canonical, a) for a in allowed_digits
        )

    for digits in _digit_runs(text):
        canonical = _canonical(digits)
        if not is_allowed(canonical) and any(_same_person(canonical, n) for n in others):
            reasons.add("other_contact")
    for digits in _digit_runs(_mask_dates_and_money(text)):
        canonical = _canonical(digits)
        if not is_allowed(canonical) and not any(_same_person(canonical, n) for n in others):
            reasons.add("personal_data")
    only_digits = re.sub(r"[^0-9]", "", text)
    allowed_run = re.sub(r"[^0-9]", "", own_text + public_text)
    for number in others:
        if len(number) < 10:
            continue
        # the whole number, and the national forms people write ("11 99999-0001", or without the 9)
        national = number[2:] if number.startswith("55") and len(number) >= 12 else number
        forms = {number, national, national[:2] + national[-8:]}
        if any(
            form in only_digits and form not in allowed_run for form in forms if len(form) >= 10
        ):
            reasons.add("other_contact")
    for mail in _EMAIL.findall(text):
        if mail.lower() not in allowed_mail:
            reasons.add("personal_data")

    folded = _fold(text)
    own_names = _fold(own_text + " " + public_text)
    for name in other_names:
        pattern = r"\b" + re.escape(_fold(name)) + r"\b"
        if re.search(pattern, folded) and not re.search(pattern, own_names):
            reasons.add("other_contact")

    markers = SourceRegistry.load(ws).non_public_markers()
    squeezed = re.sub(r"\W", "", folded)  # spaced out or punctuated, a marker is still a marker
    if any(
        m.lower() in text.lower()
        or (len(squeezed_m := re.sub(r"\W", "", _fold(m))) >= 6 and squeezed_m in squeezed)
        for m in markers
    ):
        reasons.add("non_public")
    if internal_text:
        hidden = _shingles(internal_text) - _shingles(public_text) - _shingles(own_text)
        if hidden & _shingles(text):
            reasons.add("non_public")

    # A note is checked whole, so a short one (shorter than a shingle) cannot slip through.
    outgoing = _words(text)
    allowed_words = _words(public_text) + _words(own_text)
    for note in notes:
        sequence = _words(note)
        if (
            len(sequence) >= MIN_NOTE_WORDS
            and _contains(outgoing, sequence)
            and not _contains(allowed_words, sequence)
        ):
            reasons.add("non_public")

    if _CREDENTIAL.search(text):
        reasons.add("credential")
    return EgressVerdict(not reasons, tuple(sorted(reasons)))
