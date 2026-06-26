from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


GREEK_COMMANDS = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ε",
    "varepsilon": "ε",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "vartheta": "ϑ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "pi": "π",
    "rho": "ρ",
    "sigma": "σ",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "φ",
    "varphi": "φ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",
    "Gamma": "Γ",
    "Delta": "Δ",
    "Theta": "Θ",
    "Lambda": "Λ",
    "Xi": "Ξ",
    "Pi": "Π",
    "Sigma": "Σ",
    "Phi": "Φ",
    "Psi": "Ψ",
    "Omega": "Ω",
    "infty": "∞",
    "sum": "∑",
    "prod": "∏",
    "partial": "∂",
        "le": "≤",
    "leq": "≤",
    "ge": "≥",
    "geq": "≥",
        "in": "∈",
        "approx": "≈",
        "pm": "±",
        "cdot": "·",
    "times": "×",
}


OPERATOR_WORDS = {"min", "max", "sin", "cos", "tan", "log", "ln", "exp"}


@dataclass
class Node:
    pass


@dataclass
class Seq(Node):
    items: list[Node]


@dataclass
class Text(Node):
    value: str


@dataclass
class Frac(Node):
    num: Node
    den: Node


@dataclass
class Script(Node):
    base: Node
    sub: Node | None = None
    sup: Node | None = None


@dataclass
class Delim(Node):
    begin: str
    body: Node
    end: str


class FormulaParser:
    """Small parser for Word-style inline formulas used in academic drafts."""

    def __init__(self, text: str) -> None:
        self.text = normalize_formula_text(text)
        self.i = 0

    def parse(self) -> Node:
        node = self._parse_expression(stop="")
        return simplify(node)

    def _parse_expression(self, stop: str) -> Node:
        items: list[Node] = []
        while self.i < len(self.text):
            ch = self.text[self.i]
            if stop and ch in stop:
                break
            if ch == "/":
                self.i += 1
                numerator = strip_outer_delim(items.pop() if items else Text(""))
                denominator = self._parse_scriptable_atom(stop)
                items.append(Frac(numerator, denominator))
                continue
            items.append(self._parse_scriptable_atom(stop))
        return seq_from_items(items)

    def _parse_scriptable_atom(self, stop: str) -> Node:
        base = self._parse_atom(stop)
        sub = None
        sup = None
        while self.i < len(self.text) and self.text[self.i] in "_^":
            marker = self.text[self.i]
            self.i += 1
            script = self._parse_group_or_single(stop)
            if marker == "_":
                sub = script
            else:
                sup = script
        if sub is not None or sup is not None:
            return Script(base=base, sub=sub, sup=sup)
        return base

    def _parse_group_or_single(self, stop: str) -> Node:
        if self.i < len(self.text) and self.text[self.i] == "{":
            self.i += 1
            node = self._parse_expression("}")
            if self.i < len(self.text) and self.text[self.i] == "}":
                self.i += 1
            return node
        return self._parse_single_script_atom(stop)

    def _parse_single_script_atom(self, stop: str) -> Node:
        if self.i >= len(self.text):
            return Text("")
        ch = self.text[self.i]
        if stop and ch in stop:
            return Text("")
        if ch == "\\":
            return Text(self._read_command())
        if ch in "([{":
            return self._parse_atom(stop)
        self.i += 1
        return Text(ch)

    def _parse_atom(self, stop: str) -> Node:
        if self.i >= len(self.text):
            return Text("")
        ch = self.text[self.i]
        if self._starts_command("frac"):
            return self._parse_latex_frac()
        if self._starts_command("left"):
            self._read_command_raw()
            return self._parse_atom(stop)
        if self._starts_command("right"):
            self._read_command_raw()
            return Text("")
        if ch in "([{":
            begin = ch
            end = {"(": ")", "[": "]", "{": "}"}[begin]
            self.i += 1
            body = self._parse_expression(end)
            if self.i < len(self.text) and self.text[self.i] == end:
                self.i += 1
            return Delim(begin, body, end)
        if ch == "\\":
            return Text(self._read_command())
        if ch.isalpha() or ch.isdigit():
            return Text(self._read_word())
        self.i += 1
        if ch in "+-=<>≤≥≈":
            return Text(f" {ch} ")
        return Text(ch)

    def _read_command(self) -> str:
        self.i += 1
        start = self.i
        while self.i < len(self.text) and self.text[self.i].isalpha():
            self.i += 1
        name = self.text[start : self.i]
        return GREEK_COMMANDS.get(name, f"\\{name}")

    def _read_command_raw(self) -> str:
        self.i += 1
        start = self.i
        while self.i < len(self.text) and self.text[self.i].isalpha():
            self.i += 1
        return self.text[start : self.i]

    def _starts_command(self, name: str) -> bool:
        token = f"\\{name}"
        if not self.text.startswith(token, self.i):
            return False
        end = self.i + len(token)
        return end >= len(self.text) or not self.text[end].isalpha()

    def _parse_latex_frac(self) -> Node:
        self._read_command_raw()
        numerator = self._parse_required_group()
        denominator = self._parse_required_group()
        return Frac(strip_outer_delim(numerator), strip_outer_delim(denominator))

    def _parse_required_group(self) -> Node:
        while self.i < len(self.text) and self.text[self.i].isspace():
            self.i += 1
        if self.i < len(self.text) and self.text[self.i] == "{":
            self.i += 1
            node = self._parse_expression("}")
            if self.i < len(self.text) and self.text[self.i] == "}":
                self.i += 1
            return node
        return self._parse_scriptable_atom("")

    def _read_word(self) -> str:
        start = self.i
        while self.i < len(self.text) and (
            self.text[self.i].isalnum() or self.text[self.i] in {"𝓡", "ℛ", "ḡ"}
        ):
            self.i += 1
        return self.text[start : self.i]


def normalize_formula_text(text: str) -> str:
    text = text.strip()
    if text.startswith("$") and text.endswith("$") and len(text) >= 2:
        text = text[1:-1].strip()
    if text.startswith("\\(") and text.endswith("\\)") and len(text) >= 4:
        text = text[2:-2].strip()
    text = text.replace("−", "-").replace("—", "-").replace("–", "-")
    text = text.replace("×", "×").replace("∙", "·")
    return text


def parse_formula(text: str) -> Node:
    return FormulaParser(text).parse()


def seq_from_items(items: Iterable[Node]) -> Node:
    flat: list[Node] = []
    for item in items:
        if isinstance(item, Seq):
            flat.extend(item.items)
        else:
            flat.append(item)
    return simplify(Seq(flat))


def simplify(node: Node) -> Node:
    if isinstance(node, Seq):
        items: list[Node] = []
        buffer = ""
        for item in node.items:
            item = simplify(item)
            if isinstance(item, Text):
                buffer += item.value
                continue
            if buffer:
                items.append(Text(_normalize_operator_spaces(buffer)))
                buffer = ""
            items.append(item)
        if buffer:
            items.append(Text(_normalize_operator_spaces(buffer)))
        if len(items) == 1:
            return items[0]
        return Seq(items)
    if isinstance(node, Frac):
        return Frac(simplify(node.num), simplify(node.den))
    if isinstance(node, Script):
        return Script(
            base=simplify(node.base),
            sub=simplify(node.sub) if node.sub is not None else None,
            sup=simplify(node.sup) if node.sup is not None else None,
        )
    if isinstance(node, Delim):
        return Delim(node.begin, simplify(node.body), node.end)
    return node


def strip_outer_delim(node: Node) -> Node:
    if isinstance(node, Delim) and (node.begin, node.end) in {("(", ")"), ("[", "]")}:
        return node.body
    return node


def _normalize_operator_spaces(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" ?([+\-=<>≤≥]) ?", r" \1 ", text)
    return text
