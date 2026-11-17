"""多语种分词增强的零依赖回归单测（common.tokenize）。

验证：中文词边界、中英混排、日文假名 n-gram、韩文/阿拉伯文按词、与旧 bigram 兼容。
"""

import common


def test_chinese_word_boundary():
    t = common.tokenize("人工智能 大模型 语义检索")
    assert "人工智能" in t
    assert "大模型" in t
    assert "语义检索" in t or ("语义" in t and "检索" in t)


def test_cjk_latin_mixed():
    t = common.tokenize("苹果 iPhone 芯片性能")
    assert "苹果" in t
    assert "iphone" in t
    assert "芯片" in t


def test_japanese_kana_ngram():
    t = common.tokenize("日本語のテスト")
    assert any("日本" in x for x in t)


def test_korean_by_word():
    t = common.tokenize("한국어 테스트")
    assert "한국어" in t
    assert "테스트" in t


def test_arabic_by_word():
    t = common.tokenize("مرحبا بالعالم")
    assert "مرحبا" in t


def test_backward_compat_bigram():
    # 旧 bigram 行为仍保留：未登录词至少产出相邻 2-gram
    t = common.tokenize("人工智能够聪明")
    assert "人工" in t
    assert "智能" in t


def test_overlap_preserved():
    # 两近似中文摘要仍有非空词重叠（不破坏打分/去重语义）
    a = common.tokenize("苹果产业链 立讯精密 代工")
    b = common.tokenize("苹果产业链 歌尔股份 代工")
    assert a & b  # 交集非空
