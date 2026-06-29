#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""make_anki.py — export a study-notes HTML page to an Anki-importable TSV deck.

The notes stay a single self-contained HTML file; the flashcard deck rides inside it,
invisibly, as a hidden block the skill writes while generating the notes. It uses plain
HTML elements (NOT JSON) on purpose: backslashes are literal in HTML, so LaTeX like
`$\tfrac{3}{2}R$` needs no escaping — whereas in JSON `\t`/`\n` would silently corrupt
`\tfrac`/`\nabla`.

    <div id="anki-deck" hidden>
      <div class="anki-card" data-tags="热学 第一定律">
        <div class="anki-front">等温过程理想气体内能如何变化？</div>
        <div class="anki-back">$\Delta U = 0$（内能只是温度的函数，$T$ 不变）</div>
      </div>
    </div>

This tool extracts that deck (and, as a bonus, any self-test `.quiz` questions) and
writes a TSV: `front <TAB> back <TAB> tags`, one card per line. Math is converted to
Anki's MathJax delimiters (`$…$` → `\(…\)`, `$$…$$` → `\[…\]`) so cards render in Anki
out of the box. Import: Anki → File → Import → Fields separated by Tab, map col 3 → Tags.

Usage:  python scripts/make_anki.py <notes.html> [deck.tsv] [--no-quiz]
"""
import html as htmllib
import os
import re
import sys

CARD_RE = re.compile(
    r'<div class="anki-card"([^>]*)>\s*'
    r'<div class="anki-front">(.*?)</div>\s*'
    r'<div class="anki-back">(.*?)</div>', re.S)
TAGS_RE = re.compile(r'data-tags="([^"]*)"')
ANSWER_RE = re.compile(r'^[^>]*data-answer="(\d+)"')
STEM_RE = re.compile(r'<div class="quiz-stem">(.*?)</div>', re.S)
OPT_RE = re.compile(r'<button class="quiz-opt">(.*?)</button>', re.S)
EXPLAIN_RE = re.compile(r'<div class="quiz-explain">(.*?)</div>', re.S)


def to_mathjax(s):
    s = re.sub(r'\$\$(.+?)\$\$', lambda m: r'\[' + m.group(1) + r'\]', s, flags=re.S)
    s = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', lambda m: r'\(' + m.group(1) + r'\)', s, flags=re.S)
    return s


def clean(s):
    """Strip tags, unescape entities, collapse whitespace, neutralise TSV delimiters."""
    s = re.sub(r'<span class="qn">.*?</span>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = htmllib.unescape(s)
    s = s.replace('\t', ' ').replace('\r', ' ')
    s = re.sub(r'\s*\n\s*', ' ', s).strip()
    return to_mathjax(s)


def cards_from_deck(html):
    out = []
    for attrs, front, back in CARD_RE.findall(html):
        tm = TAGS_RE.search(attrs)
        f, b = clean(front), clean(back)
        if f and b:
            out.append((f, b, tm.group(1).strip() if tm else ""))
    return out


def cards_from_quiz(html):
    out = []
    # split on each quiz-q; a chunk runs to the next quiz-q (or end), so the
    # stem/option/explain closing tags are always inside it. Non-greedy regexes
    # then pick that question's own content.
    for chunk in re.split(r'<div class="quiz-q"', html)[1:]:
        am = ANSWER_RE.match(chunk)
        stem = STEM_RE.search(chunk)
        opts = OPT_RE.findall(chunk)
        if not am or not stem or not opts:
            continue
        ai = int(am.group(1))
        if ai >= len(opts):
            continue
        front = clean(stem.group(1))
        back = "正确答案：" + clean(opts[ai])
        expl = EXPLAIN_RE.search(chunk)
        if expl:
            back += "  —  " + clean(expl.group(1))
        out.append((front, back, "自测"))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    no_quiz = '--no-quiz' in sys.argv
    if not args:
        sys.exit("usage: make_anki.py <notes.html> [deck.tsv] [--no-quiz]")
    src = args[0]
    out = args[1] if len(args) > 1 else os.path.splitext(src)[0] + ".tsv"
    html = open(src, encoding="utf-8", errors="replace").read()

    cards = cards_from_deck(html)
    n_deck = len(cards)
    if not no_quiz:
        cards += cards_from_quiz(html)
    if not cards:
        sys.exit("no cards found: add an <script id=\"anki-deck\"> JSON block or a .quiz widget.")

    with open(out, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n#html:true\n#tags column:3\n")
        for front, back, tags in cards:
            f.write(f"{front}\t{back}\t{tags}\n")
    print(f"wrote {out}: {len(cards)} cards ({n_deck} from anki-deck"
          + ("" if no_quiz else f", {len(cards) - n_deck} from quiz") + ")")


if __name__ == "__main__":
    main()
