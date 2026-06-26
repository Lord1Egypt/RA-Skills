from pathlib import Path

import pytest

from bin.parse_email import ParsedEmail, parse_eml

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> ParsedEmail:
    return parse_eml((FIXTURES / name).read_bytes())


def test_benign_basics():
    e = load("benign.eml")
    assert e.from_address == "noreply@github.com"
    assert e.from_display == "GitHub"
    assert e.from_domain == "github.com"
    assert e.subject == "[NickVanzo/royal-hackathon-itu] PR merged"
    assert e.message_id == "<abc123@github.com>"
    assert "pull request #1" in e.body_plain


def test_benign_auth_header_preserved():
    e = load("benign.eml")
    # parse_eml keeps the raw Authentication-Results string for check_auth.py
    assert e.authentication_results is not None
    assert "dkim=pass" in e.authentication_results


def test_benign_extracts_urls():
    e = load("benign.eml")
    assert "https://github.com/NickVanzo/royal-hackathon-itu/pull/1" in e.urls


def test_phish_html_body_stripped_to_plain():
    e = load("phish_spoof.eml")
    # html tags stripped
    assert "<b>" not in e.body_plain
    assert "<p>" not in e.body_plain
    # meaningful text preserved
    assert "limited" in e.body_plain.lower()
    assert "urgent action required" in e.body_plain.lower()


def test_phish_extracts_all_urls():
    e = load("phish_spoof.eml")
    assert "http://bit.ly/xyz7A9" in e.urls
    assert "http://192.168.1.50:8080/login" in e.urls
    assert "https://paypal.com/verify" in e.urls
    assert "https://paypa1-secure.ru/login" in e.urls


def test_phish_from_domain_extraction():
    e = load("phish_spoof.eml")
    assert e.from_address == "support@paypa1-secure.ru"
    assert e.from_domain == "paypa1-secure.ru"
    assert e.from_display == "PayPal Support"


def test_phish_auth_failure_preserved():
    e = load("phish_spoof.eml")
    assert "dkim=fail" in e.authentication_results
    assert "spf=fail" in e.authentication_results
    assert "dmarc=fail" in e.authentication_results


def test_bec_quanta_extracts_domain():
    e = load("bec_quanta.eml")
    assert e.from_domain == "quanta-computer-inc.xyz"
    assert "Mark Anderson" in e.from_display


def test_bec_quanta_body_contains_key_tokens():
    e = load("bec_quanta.eml")
    lower = e.body_plain.lower()
    # all BEC signal tokens present
    for token in ("urgent", "wire", "invoice", "swift", "cfo"):
        assert token in lower, f"missing token: {token}"


def test_missing_from_header_raises():
    raw = b"Subject: no from\r\n\r\nbody"
    with pytest.raises(ValueError, match="missing From"):
        parse_eml(raw)


def test_bytes_and_str_both_accepted():
    raw = (FIXTURES / "benign.eml").read_text()
    e = parse_eml(raw)
    assert e.from_domain == "github.com"
