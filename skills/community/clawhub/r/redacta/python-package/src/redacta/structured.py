#!/usr/bin/env python3
"""
Redacta - structured-pattern redaction layer (Layer 1).

Deterministically detects fixed-format patient identifiers in clinical text and
replaces each distinct value with a numbered, labelled token. Contextual
identifiers that need judgement (patient names, postal addresses, identifying
ages) are handled separately by the agent - see SKILL.md.

Usage:
    python3 redact_structured.py input.txt        # read a file
    python3 redact_structured.py < input.txt      # read stdin
    python3 redact_structured.py input.txt --text-only

Default output is JSON on stdout with three keys:
    redacted_text  - the text with structured identifiers tokenised
    report         - {token_type: number_of_distinct_values}
    token_map      - {token: original_value}  (for review / re-identification)

Standard library only. No network access; all processing is local.
"""

import argparse
import json
import re
import sys


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def is_valid_nhs(digits):
    """Validate a 10-digit NHS number using the Modulus-11 check digit.

    Weight digits 1-9 by 10..2, sum, take mod 11; the check digit is
    11 - remainder (11 -> 0). A computed check of 10 means the number is
    invalid. This is what stops 10-digit phone numbers being read as NHS
    numbers.
    """
    if len(digits) != 10 or not digits.isdigit():
        return False
    if digits == digits[0] * 10:                 # all-same-digit is invalid
        return False
    weights = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(d) * w for d, w in zip(digits[:9], weights))
    check = 11 - (total % 11)
    if check == 11:
        check = 0
    if check == 10:
        return False
    return check == int(digits[9])


# UK National Insurance number prefix rules (HMRC).
_NI_INVALID_PREFIX = {"BG", "GB", "NK", "KN", "TN", "NT", "ZZ"}
_NI_PREFIX1_BAD = set("DFIQUV")     # first letter may not be one of these
_NI_PREFIX2_BAD = set("DFIOQUV")    # second letter may not be one of these


def is_valid_ni(prefix):
    """Validate the two-letter prefix of a UK National Insurance number."""
    prefix = prefix.upper()
    if len(prefix) != 2 or prefix in _NI_INVALID_PREFIX:
        return False
    return prefix[0] not in _NI_PREFIX1_BAD and prefix[1] not in _NI_PREFIX2_BAD


# ---------------------------------------------------------------------------
# Token allocation: same value -> same token, distinct values -> new numbers
# ---------------------------------------------------------------------------

class Tokeniser:
    def __init__(self):
        self._by_key = {}     # (type, key) -> token
        self._counters = {}   # type -> int
        self.token_map = {}   # token -> first-seen original spelling

    def token_for(self, type_name, original, key=None):
        k = (type_name, key if key is not None else original)
        if k in self._by_key:
            return self._by_key[k]
        self._counters[type_name] = self._counters.get(type_name, 0) + 1
        token = "[%s_%d]" % (type_name, self._counters[type_name])
        self._by_key[k] = token
        self.token_map[token] = original
        return token


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_MONTHS = ("January|February|March|April|May|June|July|August|September|"
           "October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept?|"
           "Oct|Nov|Dec")

_DATE = "(?:%s)" % "|".join([
    r"\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}",                      # 14/03/1952
    r"\d{4}-\d{2}-\d{2}",                                       # 1952-03-14
    r"\d{1,2}(?:st|nd|rd|th)?\s+(?:%s)\s+\d{4}" % _MONTHS,      # 14th March 1952
    r"(?:%s)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}" % _MONTHS,    # March 14, 1952
])

# Date of birth: a date only counts when it sits next to a DOB keyword, so that
# clinical/appointment dates are left intact.
_DOB_RE = re.compile(
    r"(?P<kw>\b(?:date\s+of\s+birth|d\.?o\.?b\.?|born(?:\s+on)?)[\s:.]*)"
    r"(?P<date>%s)" % _DATE, re.IGNORECASE)

_NHS_RE = re.compile(r"\b(\d{3}[\s\-]?\d{3}[\s\-]?\d{4})\b")

_NI_RE = re.compile(
    r"\b([A-Za-z]{2})\s?(\d{2})\s?(\d{2})\s?(\d{2})\s?([A-Da-d])\b")

_SSN_FMT_RE = re.compile(
    r"(?<!\d)(?!000|666|9\d\d)(\d{3})([\-\s])(\d{2})\2(\d{4})(?!\d)")
_SSN_KW_RE = re.compile(
    r"(?P<kw>(?:SSN|Social\s*Security(?:\s*(?:Number|No\.?|#))?)[\s:]*)"
    r"(?P<num>(?!000|666|9\d\d)\d{9})(?!\d)", re.IGNORECASE)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

_MRN_RE = re.compile(
    r"(?P<kw>(?:MRN|Hospital\s*(?:No\.?|Number)|Hosp\.?\s*(?:No\.?|Number)|"
    r"Patient\s*ID|Unit\s*(?:No\.?|Number))[\s:]*)(?P<id>[A-Z0-9\-]{4,15})",
    re.IGNORECASE)

_POSTCODE_RE = re.compile(
    r"\b(GIR\s?0AA|[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b", re.IGNORECASE)

_US_STATES = ("AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|"
              "MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|"
              "TX|UT|VT|VA|WA|WV|WI|WY|DC")
_ZIP_KW_RE = re.compile(
    r"(?P<kw>(?:ZIP|Zip\s*Code|Postal\s*Code)[\s:]*)"
    r"(?P<zip>\d{5}(?:-\d{4})?)(?!\d)", re.IGNORECASE)
_ZIP_STATE_RE = re.compile(
    r"(?P<pre>(?:,?\s)(?:%s)\s+)(?P<zip>\d{5}(?:-\d{4})?)(?!\d)" % _US_STATES)


# ---------------------------------------------------------------------------
# Redaction passes
# ---------------------------------------------------------------------------

def _digits(s):
    return re.sub(r"\D", "", s)


def redact_mrn(text, tok):
    return _MRN_RE.sub(
        lambda m: m.group("kw") + tok.token_for(
            "MRN", m.group("id"), key=m.group("id").upper()), text)


def redact_nhs(text, tok):
    def repl(m):
        raw = m.group(1)
        d = _digits(raw)
        if len(d) == 10 and is_valid_nhs(d):
            return tok.token_for("NHS_NUMBER", raw, key=d)
        return raw
    return _NHS_RE.sub(repl, text)


def redact_ni(text, tok):
    def repl(m):
        if not is_valid_ni(m.group(1)):
            return m.group(0)
        key = (m.group(1) + m.group(2) + m.group(3) + m.group(4)
               + m.group(5)).upper()
        return tok.token_for("NI_NUMBER", m.group(0).strip(), key=key)
    return _NI_RE.sub(repl, text)


def redact_ssn(text, tok):
    def fmt(m):
        if m.group(3) == "00" or m.group(4) == "0000":
            return m.group(0)
        key = m.group(1) + m.group(3) + m.group(4)
        return tok.token_for("SSN", m.group(0), key=key)
    text = _SSN_FMT_RE.sub(fmt, text)

    def kw(m):
        d = m.group("num")
        if d[3:5] == "00" or d[5:9] == "0000":
            return m.group(0)
        return m.group("kw") + tok.token_for("SSN", d, key=d)
    return _SSN_KW_RE.sub(kw, text)


def redact_email(text, tok):
    return _EMAIL_RE.sub(
        lambda m: tok.token_for("EMAIL", m.group(0), key=m.group(0).lower()),
        text)


def redact_phone(text, tok):
    def mk(m):
        return tok.token_for("PHONE", m.group(0).strip(), key=_digits(m.group(0)))

    # +44 (UK international)
    text = re.sub(
        r"(?<!\d)\+44[\s\-]?(?:\(0\))?[\s\-]?\d{2,5}[\s\-]?\d{3,4}[\s\-]?\d{3,4}(?!\d)",
        mk, text)
    # +1 (US/Canada international)
    text = re.sub(
        r"(?<!\d)\+1[\s\-.]?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}(?!\d)",
        mk, text)

    # UK landline/mobile: 0-prefixed, 10-11 digits total
    def uk(m):
        if 10 <= len(_digits(m.group(0))) <= 11:
            return mk(m)
        return m.group(0)
    text = re.sub(
        r"(?<!\d)\(?0\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}(?!\d)", uk, text)

    # US: (415) 555-1212, 415-555-1212, 415.555.1212 (area/exchange start 2-9)
    text = re.sub(
        r"(?<!\d)\(?[2-9]\d{2}\)?[\s\-.][2-9]\d{2}[\s\-.]\d{4}(?!\d)", mk, text)
    return text


def redact_postcode(text, tok):
    def repl(m):
        clean = re.sub(r"\s", "", m.group(0))
        if 5 <= len(clean) <= 7:
            return tok.token_for("POSTCODE", m.group(0), key=clean.upper())
        return m.group(0)
    return _POSTCODE_RE.sub(repl, text)


def redact_zip(text, tok):
    text = _ZIP_KW_RE.sub(
        lambda m: m.group("kw") + tok.token_for("ZIP", m.group("zip")), text)
    text = _ZIP_STATE_RE.sub(
        lambda m: m.group("pre") + tok.token_for("ZIP", m.group("zip")), text)
    return text


def redact_dob(text, tok):
    return _DOB_RE.sub(
        lambda m: m.group("kw") + tok.token_for(
            "DATE_OF_BIRTH", m.group("date")), text)


def redact_structured(text):
    """Run every pass in order and return (redacted_text, report, token_map)."""
    # Normalise non-breaking spaces so spaced identifiers still match.
    for ch in (" ", " ", " "):
        text = text.replace(ch, " ")

    tok = Tokeniser()
    # Order matters: keyword-anchored and checksum-validated patterns first,
    # weaker heuristics last, so high-confidence matches win any overlap.
    for fn in (redact_mrn, redact_nhs, redact_ni, redact_ssn, redact_email,
               redact_phone, redact_postcode, redact_zip, redact_dob):
        text = fn(text, tok)

    report = {}
    for token in tok.token_map:
        type_name = token.strip("[]").rsplit("_", 1)[0]
        report[type_name] = report.get(type_name, 0) + 1
    return text, report, tok.token_map


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Redacta structured-pattern redaction layer (Layer 1).")
    ap.add_argument("file", nargs="?",
                    help="input file; reads stdin if omitted")
    ap.add_argument("--text-only", action="store_true",
                    help="print only the redacted text (no JSON)")
    args = ap.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            raw = fh.read()
    else:
        raw = sys.stdin.read()

    redacted, report, token_map = redact_structured(raw)

    if args.text_only:
        sys.stdout.write(redacted)
        if not redacted.endswith("\n"):
            sys.stdout.write("\n")
        return

    json.dump({"redacted_text": redacted, "report": report,
               "token_map": token_map},
              sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
