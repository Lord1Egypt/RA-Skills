"""A small JavaScript tokenizer for the widget checks.

It is not a parser. It splits a script into identifiers, punctuators, numbers,
strings (with their escapes decoded), template literals and regex literals, so
the rules can look at what a name really is and at what a string really says
(``'\\u0068ttps:'`` is ``https:``). Comments are dropped.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

KEYWORDS_BEFORE_EXPRESSION = {
    "return", "typeof", "instanceof", "in", "of", "new", "delete", "void",
    "throw", "case", "do", "else", "yield", "await",
}

PUNCTUATORS = sorted(
    """>>>= ... === !== **= <<= >>= >>> &&= ||= ??= => == != <= >= && || ?? ?. ++ --
    += -= *= /= %= &= |= ^= ** << >> { } ( ) [ ] ; , < > + - * / % & | ^ ! ~ ? : = . @ #""".split(),
    key=len,
    reverse=True,
)

_IDENT_START = re.compile(r"[A-Za-z_$\u0080-￿]")
_IDENT = re.compile(r"[A-Za-z0-9_$\u0080-￿]*")
_NUMBER = re.compile(
    r"0[xX][0-9a-fA-F_]+n?|0[oO][0-7_]+n?|0[bB][01_]+n?|"
    r"(?:\d[\d_]*\.?[\d_]*|\.\d[\d_]*)(?:[eE][+-]?\d[\d_]*)?n?"
)


@dataclass
class Token:
    kind: str  # ident | punct | num | str | template | regex
    value: str  # decoded value for str; raw text otherwise
    line: int
    # template literals: the decoded static parts and whether ${...} appears
    parts: List[str] = field(default_factory=list)
    has_subst: bool = False

    def is_punct(self, *values: str) -> bool:
        return self.kind == "punct" and self.value in values

    def is_ident(self, *values: str) -> bool:
        return self.kind == "ident" and (not values or self.value in values)


class LexError(Exception):
    def __init__(self, message: str, line: int):
        super().__init__(message)
        self.line = line


_SIMPLE_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


def _read_escape(src: str, i: int, line: int):
    """src[i] is the character after a backslash. Returns (text, new_index, lines_consumed)."""
    if i >= len(src):
        raise LexError("unterminated escape", line)
    c = src[i]
    if c in "\r\n\u2028\u2029":  # line continuation
        if c == "\r" and src[i + 1:i + 2] == "\n":
            return "", i + 2, 1
        return "", i + 1, 1
    if c == "x":
        h = src[i + 1:i + 3]
        if not re.fullmatch(r"[0-9a-fA-F]{2}", h):
            raise LexError("bad \\x escape", line)
        return chr(int(h, 16)), i + 3, 0
    if c == "u":
        if src[i + 1:i + 2] == "{":
            end = src.find("}", i + 2)
            h = src[i + 2:end] if end != -1 else ""
            if not re.fullmatch(r"[0-9a-fA-F]{1,6}", h):
                raise LexError("bad \\u{} escape", line)
            return chr(min(int(h, 16), 0x10FFFF)), end + 1, 0
        h = src[i + 1:i + 5]
        if not re.fullmatch(r"[0-9a-fA-F]{4}", h):
            raise LexError("bad \\u escape", line)
        return chr(int(h, 16)), i + 5, 0
    if c == "0" and src[i + 1:i + 2].isdigit():
        # legacy octal: decode loosely, it only matters that we see the text
        m = re.match(r"[0-7]{1,3}", src[i:])
        return chr(int(m.group(0), 8)), i + len(m.group(0)), 0
    return _SIMPLE_ESCAPES.get(c, c), i + 1, 0


def tokenize(src: str, first_line: int = 1) -> List[Token]:
    tokens: List[Token] = []
    i, n, line = 0, len(src), first_line
    # stack of open braces: "{" for blocks/objects, "${" for template substitutions
    brace_stack: List[str] = []

    def prev_allows_regex() -> bool:
        if not tokens:
            return True
        t = tokens[-1]
        if t.kind in ("num", "str", "template", "regex"):
            return False
        if t.kind == "ident":
            return t.value in KEYWORDS_BEFORE_EXPRESSION
        return t.value not in (")", "]", "}")

    def read_template(start: int, start_line: int, tok: Optional[Token]):
        """Scan template text from `start` (just after ` or }) to the closing ` or ${."""
        nonlocal line
        j = start
        buf = []
        while True:
            if j >= n:
                raise LexError("unterminated template literal", start_line)
            c = src[j]
            if c == "`":
                tok.parts.append("".join(buf))
                return j + 1, False
            if c == "$" and src[j + 1:j + 2] == "{":
                tok.parts.append("".join(buf))
                tok.has_subst = True
                return j + 2, True
            if c == "\\":
                text, j, nl = _read_escape(src, j + 1, line)
                line += nl
                buf.append(text)
                continue
            if c == "\n":
                line += 1
            buf.append(c)
            j += 1

    open_templates: List[Token] = []

    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            i += 1
            continue
        if c in " \t\r\f\v\u00a0\ufeff\u2028\u2029":
            i += 1
            continue
        # comments (and the HTML-like <!-- --> that scripts tolerate)
        if src.startswith("//", i) or src.startswith("<!--", i):
            end = src.find("\n", i)
            i = n if end == -1 else end
            continue
        if src.startswith("/*", i):
            end = src.find("*/", i + 2)
            if end == -1:
                raise LexError("unterminated comment", line)
            line += src.count("\n", i, end)
            i = end + 2
            continue
        if src.startswith("-->", i) and (not tokens or tokens[-1].line < line):
            end = src.find("\n", i)
            i = n if end == -1 else end
            continue
        if c in "'\"":
            start_line = line
            j = i + 1
            buf = []
            while True:
                if j >= n or src[j] in "\r\n":
                    raise LexError("unterminated string", start_line)
                ch = src[j]
                if ch == c:
                    break
                if ch == "\\":
                    text, j, nl = _read_escape(src, j + 1, line)
                    line += nl
                    buf.append(text)
                    continue
                buf.append(ch)
                j += 1
            tokens.append(Token("str", "".join(buf), start_line))
            i = j + 1
            continue
        if c == "`":
            tok = Token("template", "", line)
            i, in_subst = read_template(i + 1, line, tok)
            tokens.append(tok)
            if in_subst:
                brace_stack.append("${")
                open_templates.append(tok)
            continue
        if c == "}" and brace_stack and brace_stack[-1] == "${":
            brace_stack.pop()
            tok = open_templates.pop()
            i, in_subst = read_template(i + 1, line, tok)
            # emit a marker so rules see the template continues; the template
            # token itself already carries all static parts
            if in_subst:
                brace_stack.append("${")
                open_templates.append(tok)
            continue
        if c == "/" and prev_allows_regex():
            start_line = line
            j = i + 1
            in_class = False
            while True:
                if j >= n or src[j] in "\r\n":
                    raise LexError("unterminated regular expression", start_line)
                ch = src[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == "[":
                    in_class = True
                elif ch == "]":
                    in_class = False
                elif ch == "/" and not in_class:
                    break
                j += 1
            m = re.match(r"[A-Za-z]*", src[j + 1:])
            end = j + 1 + len(m.group(0))
            tokens.append(Token("regex", src[i:end], start_line))
            i = end
            continue
        if c.isdigit() or (c == "." and src[i + 1:i + 2].isdigit()):
            m = _NUMBER.match(src, i)
            tokens.append(Token("num", m.group(0), line))
            i = m.end()
            continue
        if c == "\\":
            # eval is `eval`: identifiers with escapes hide names from every check
            raise LexError("unicode escape in an identifier", line)
        if _IDENT_START.match(c):
            m = _IDENT.match(src, i + 1)
            end = m.end()
            if src[end:end + 1] == "\\":
                raise LexError("unicode escape in an identifier", line)
            tokens.append(Token("ident", src[i:end], line))
            i = end
            continue
        for p in PUNCTUATORS:
            if src.startswith(p, i):
                if p == "?." and src[i + 2:i + 3].isdigit():
                    p = "?"
                if p == "{":
                    brace_stack.append("{")
                elif p == "}" and brace_stack:
                    brace_stack.pop()
                tokens.append(Token("punct", p, line))
                i += len(p)
                break
        else:
            raise LexError("unexpected character %r" % c, line)
    if open_templates:
        raise LexError("unterminated template literal", open_templates[-1].line)
    return tokens


def check_brackets(tokens: List[Token]) -> Optional[LexError]:
    """A cheap structural check used when no JavaScript engine is available."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: List[Token] = []
    for t in tokens:
        if t.kind != "punct":
            continue
        if t.value in "([{":
            stack.append(t)
        elif t.value in pairs:
            if not stack or stack[-1].value != pairs[t.value]:
                return LexError("unbalanced %r" % t.value, t.line)
            stack.pop()
    if stack:
        return LexError("unclosed %r" % stack[-1].value, stack[-1].line)
    return None
