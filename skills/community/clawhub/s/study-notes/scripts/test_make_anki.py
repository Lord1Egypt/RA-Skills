#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Self-contained tests for make_anki.py. Run: python scripts/test_make_anki.py"""
import make_anki as mk

DECK = (
    '<div id="anki-deck" hidden>'
    '<div class="anki-card" data-tags="热学 热容">'
    '<div class="anki-front">单原子 $C_{V,m}$？</div>'
    r'<div class="anki-back">$$C_{V,m}=\tfrac{3}{2}R$$</div>'
    '</div></div>'
)
QUIZ = (
    '<div class="quiz-q" data-answer="0">'
    '<div class="quiz-stem"><span class="qn">1</span>卡诺温标？</div>'
    '<button class="quiz-opt">开尔文 $K$</button>'
    '<button class="quiz-opt">摄氏</button>'
    '<div class="quiz-explain">绝对温度。</div></div>'
)


def run():
    # 1. deck card extracted; LaTeX backslash survives (no JSON corruption of \tfrac)
    cards = mk.cards_from_deck(DECK)
    assert len(cards) == 1, cards
    front, back, tags = cards[0]
    assert r"\tfrac{3}{2}R" in back, back          # \t NOT eaten
    assert back.startswith(r"\[") and back.endswith(r"\]"), back  # display math → \[..\]
    assert r"\(C_{V,m}\)" in front, front          # inline math → \(..\)
    assert tags == "热学 热容"

    # 2. quiz question → card, front=stem, back=correct option + explanation
    q = mk.cards_from_quiz(QUIZ)
    assert len(q) == 1 and "卡诺温标" in q[0][0], q
    assert "开尔文" in q[0][1] and "绝对温度" in q[0][1], q
    assert q[0][2] == "自测"

    # 3. no math delimiters leak (every $ converted)
    for f, b, _ in cards + q:
        assert "$" not in f and "$" not in b, (f, b)

    print("OK  make_anki regression tests passed (3/3)")


if __name__ == "__main__":
    run()
