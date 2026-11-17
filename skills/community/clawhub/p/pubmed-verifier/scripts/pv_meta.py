"""pv_meta - shared constants and tiny cross-module helpers (v6.4.0).

Split out of verify_pmids.py: the single file had grown past the 120 KB
static-reader ceiling that evaluation platforms and agent hosts apply,
which made the tail of the file invisible to any static pass. Every
module here is stdlib-only; import verify_pmids for the full public API
(the main module re-exports everything these modules define)."""

import re
import json
import os
import time
import sys
import urllib.parse
import urllib.request
import urllib.error
import http.client
import sqlite3
import csv
import zipfile
import html
import random
import io
import itertools
from collections import defaultdict
from html.parser import HTMLParser
from difflib import SequenceMatcher
from pathlib import Path
import xml.etree.ElementTree as ET

_TOOL_VERSION = "7.0.0"

_UA_TOOL = "pubmed-verifier/7.0 (+citation verifier; stdlib-only)"

_GITHUB_URL = "https://github.com/docsor1212/pubmed-verifier"

_SH_URL = "https://skillhub.cn/skills/indiv-sorsor/pubmed-verifier"

_UA_BROWSER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def _clean_doi(doi: str) -> str:
    """Normalize a DOI for identity comparison: strip url/doi: prefixes
    (repeatedly -- composite prefixes happen), bare-host forms and trailing
    punctuation (including CJK sentence marks and closing brackets/quotes —
    scanned text routinely ends a DOI with them), lowercase."""
    s = str(doi or "").strip().lower()
    changed = True
    while changed:
        changed = False
        for pref in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/",
                     "http://dx.doi.org/", "dx.doi.org/", "doi.org/", "doi:"):
            if s.startswith(pref):
                s = s[len(pref):].strip()
                changed = True
        if s.endswith((".", ",", ";", ":", "。", "，", "；", "）", "」", "】",
                      ")", "]", "}", "!", "?", "!", "?", '"', "”", "’", "'")):
            s = s[:-1].rstrip()
            changed = True
        if "?" in s:
            s = s.split("?", 1)[0].strip()   # tracking params on doi.org links
            changed = True
    return s

def dois_match(claimed: str, registered: str) -> bool:
    """Exact match after normalization -- DOI identity, never similarity."""
    a, b = _clean_doi(claimed), _clean_doi(registered)
    return bool(a) and bool(b) and a == b

NEG_CACHE_TTL_DAYS = 3    # negatives expire faster: an ahead-of-print PMID

_HAS_CJK = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]')


ARXIV_OLD_RE = re.compile(r'^[a-z-]+(?:\.[A-Z]{2})?/\d{7}(v\d+)?$', re.IGNORECASE)


def _extract_author_surnames(author_str: str) -> list[str]:
    """Extract surname list from author string like 'Ravelli A, Martini A, et al'"""
    surnames = []
    # Split on comma
    parts = author_str.split(",")
    for part in parts:
        part = part.strip()
        # v4.0.0: a leading reference number ("[3] Zhang S") must not block
        # the surname pattern — numbered lists are the common scan shape
        part = re.sub(r'^\[?\d+\]?[.．、)]?\s*', '', part)
        if part.lower() in ("et al", "et al.", "et"):
            continue
        # Match "Surname Initials" or just "Surname"
        m = re.match(r'^([A-ZÀ-ÿ][a-zÀ-ÿ]+)', part)
        if m:
            surnames.append(m.group(1))
    return surnames


_LINT_KNOWN_KEYS = {"pmid", "title", "authors", "journal", "year",
                    "doi", "arxiv_id"}


_TEXT_NUM_RE = re.compile(r'^\s*(?:\[(\d{1,3})\]|(\d{1,3})[.、)．])\s*')


def _arxiv_id_valid_shape(arxiv_id: str) -> bool:
    """Shape check first: malformed months (13xx) made the official API hang
    in the past (cite-holmes lesson), and garbage IDs waste calls."""
    s = arxiv_id.strip()
    m = ARXIV_NEW_RE.match(s.upper().replace("ARXIV:", ""))
    if m and 1 <= int(m.group(2)) <= 12:
        return True
    return bool(ARXIV_OLD_RE.match(s))


ARXIV_NEW_RE = re.compile(r'^(\d{2})(0[1-9]|1[0-2])\.(\d{4,5})(v\d+)?$', re.IGNORECASE)


_LINT_KNOWN_COLS = {"pmid", "title", "authors", "journal", "year",
                    "doi", "arxiv_id", "arxiv"}


_OPENALEX_BASE = "https://api.openalex.org"


# __all__ recalculated at the true end of the module so every
# late-appended name is exported to `import *` consumers
_NAMES = [n for n in dir() if not n.startswith('__')]
__all__ = _NAMES
del _NAMES


_META_LINE_RE = re.compile(r"^[-\u2022*]?\s*(?:DOI|PMID|arXiv|[A-Za-z\u4e00-\u9fff]{1,12}ID|url)\s*[:\uff1a]", re.I)


_TABLE_ROW_RE = re.compile(r"^(?:19|20)\d{2}\s*\|")


_HEADING_MARK_RE = re.compile(r"^#{1,6}\s+")


_QUOTE_MARK_RE = re.compile(r"^>\s?")


CT_KEY = "claimed_title"


CT_SEP = " "


CT_NL = chr(10)
