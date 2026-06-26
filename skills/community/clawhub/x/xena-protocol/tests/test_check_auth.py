from pathlib import Path

import pytest

from bin.check_auth import AuthVerdict, parse_authentication_results
from bin.parse_email import parse_eml

FIXTURES = Path(__file__).parent / "fixtures"


def _auth_from(fname: str) -> AuthVerdict:
    e = parse_eml((FIXTURES / fname).read_bytes())
    return parse_authentication_results(e.authentication_results)


def test_benign_all_pass():
    v = _auth_from("benign.eml")
    assert v.spf == "pass"
    assert v.dkim == "pass"
    assert v.dmarc == "pass"
    assert v.all_fail is False
    assert v.any_fail is False


def test_phish_all_fail():
    v = _auth_from("phish_spoof.eml")
    assert v.spf == "fail"
    assert v.dkim == "fail"
    assert v.dmarc == "fail"
    assert v.all_fail is True
    assert v.any_fail is True


def test_bec_all_pass():
    # bec_quanta is interesting: pure social engineering with legit auth pass
    # (attacker-owned domain they actually published SPF/DKIM/DMARC for)
    v = _auth_from("bec_quanta.eml")
    assert v.spf == "pass"
    assert v.dkim == "pass"
    assert v.dmarc == "pass"
    assert v.all_fail is False


def test_missing_header_returns_neutral():
    v = parse_authentication_results(None)
    assert v.spf is None
    assert v.dkim is None
    assert v.dmarc is None
    assert v.all_fail is False
    assert v.any_fail is False


def test_empty_header_returns_neutral():
    v = parse_authentication_results("")
    assert v.spf is None
    assert v.all_fail is False


def test_softfail_not_treated_as_fail():
    # softfail = advisory, not a hard fail; don't trigger the stage-1 gate
    raw = "mx.example.com; spf=softfail; dkim=pass; dmarc=pass"
    v = parse_authentication_results(raw)
    assert v.spf == "softfail"
    assert v.all_fail is False
    assert v.any_fail is False  # softfail doesn't count as a fail


def test_temperror_not_treated_as_fail():
    raw = "mx.example.com; spf=temperror; dkim=pass; dmarc=pass"
    v = parse_authentication_results(raw)
    assert v.spf == "temperror"
    assert v.all_fail is False
    assert v.any_fail is False


def test_partial_fail_is_any_fail_not_all_fail():
    raw = "mx.example.com; spf=pass; dkim=fail; dmarc=pass"
    v = parse_authentication_results(raw)
    assert v.dkim == "fail"
    assert v.any_fail is True
    assert v.all_fail is False


def test_multiline_header_parsed():
    raw = """mx.google.com;
       dkim=fail header.d=paypal.com;
       spf=fail smtp.mailfrom=sender.ru;
       dmarc=fail header.from=paypal.com"""
    v = parse_authentication_results(raw)
    assert v.spf == "fail"
    assert v.dkim == "fail"
    assert v.dmarc == "fail"
    assert v.all_fail is True


def test_case_insensitive_keys():
    raw = "mx.example.com; SPF=Pass; DKIM=PASS; DMARC=pass"
    v = parse_authentication_results(raw)
    assert v.spf == "pass"
    assert v.dkim == "pass"
    assert v.dmarc == "pass"


def test_extra_methods_ignored():
    # real headers often include other auth methods (arc, dkim-atps, ...)
    raw = "mx.example.com; spf=pass; dkim=pass; dmarc=pass; arc=pass; bimi=pass"
    v = parse_authentication_results(raw)
    assert v.spf == "pass"
    assert v.dkim == "pass"
    assert v.dmarc == "pass"


def test_reason_reported_for_fail():
    raw = "mx.example.com; spf=fail (sender ip not authorized); dkim=fail; dmarc=fail"
    v = parse_authentication_results(raw)
    # parenthetical reasons are stripped — we just want the verdict keyword
    assert v.spf == "fail"
