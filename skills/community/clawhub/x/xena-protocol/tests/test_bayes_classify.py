import json
from pathlib import Path

import pytest

from bin.bayes_classify import (
    classify,
    load_model,
    tokenize,
)

FIXTURES = Path(__file__).parent / "fixtures"
MODEL = load_model(FIXTURES / "bayes_model_tiny.json")


# Tokenizer invariants
def test_tokenize_lowercases():
    assert "urgent" in tokenize("URGENT please")


def test_tokenize_strips_punctuation_and_numbers():
    # numbers and punctuation dropped by the [a-z]+ regex
    toks = tokenize("Wire $10,000 by Friday!")
    assert "wire" in toks
    assert "friday" in toks
    assert "by" not in toks  # stopword
    assert not any(c.isdigit() for t in toks for c in t)


def test_tokenize_drops_stopwords():
    toks = tokenize("the quick brown fox and the lazy dog")
    for sw in ("the", "and"):
        assert sw not in toks


def test_tokenize_drops_short_tokens():
    toks = tokenize("I am a bot")
    # all <= 2 chars after stopword removal are dropped
    assert not any(len(t) <= 2 for t in toks)


def test_tokenize_strips_html():
    toks = tokenize("<p>Hello <b>urgent</b> matter</p>")
    assert "hello" in toks
    assert "urgent" in toks
    assert "matter" in toks
    # no tag names leaked
    assert "html" not in toks


# Classifier behavior
def test_classify_phishy_text_scores_high():
    text = "Urgent wire inheritance bitcoin please verify"
    score, top = classify(text, MODEL)
    assert score > 0.8
    # top contributors come back with (token, p_phish)
    toks = [t for t, _ in top]
    for expected in ("urgent", "wire", "inheritance", "bitcoin", "verify"):
        assert expected in toks


def test_classify_benign_text_scores_low():
    text = "Meeting invitation for the project. Please accept."
    score, _ = classify(text, MODEL)
    assert score < 0.3


def test_classify_unknown_tokens_neutral():
    # all unknown → neutral 0.5
    score, top = classify("zzzzz yyyyy xxxxx", MODEL)
    assert score == 0.5
    assert top == []


def test_classify_returns_top_n():
    text = " ".join(MODEL["tokens"].keys())  # every token
    score, top = classify(text, MODEL, top_n=3)
    assert len(top) == 3
    # most discriminating = furthest from 0.5 → inheritance (0.95), quanta (0.88), bitcoin (0.85)
    tokens = [t for t, _ in top]
    assert "inheritance" in tokens


def test_classify_bec_quanta_scenario():
    # simulates BEC body tokens
    text = "Invoice urgent wire transfer Quanta"
    score, _ = classify(text, MODEL)
    assert score > 0.75


def test_classify_empty_text_neutral():
    score, top = classify("", MODEL)
    assert score == 0.5
    assert top == []


def test_load_model_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_model(tmp_path / "nope.json")


def test_load_model_reads_valid(tmp_path):
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"tokens": {"x": {"p_phish": 0.5}}}))
    m = load_model(p)
    assert m["tokens"]["x"]["p_phish"] == 0.5
