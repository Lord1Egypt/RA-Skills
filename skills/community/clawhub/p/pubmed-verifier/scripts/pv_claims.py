"""pv_claims - claims loading, validation and skeletons (v6.4.0 split).

The structured-claims layer: JSON/CSV loaders, the offline linters and
the claims-template generator. Stdlib-only; re-exported by the main
module."""

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

# cross-module imports (explicit — underscore names are excluded
# from `import *`, so every private helper is named here)
from pv_meta import (_LINT_KNOWN_COLS, _LINT_KNOWN_KEYS, _TOOL_VERSION, _arxiv_id_valid_shape, _clean_doi)
from pv_textio import (
    parse_bibtex, parse_ris, ris_to_bib_fields, bib_entry_route,
    sniff_bibliography_format, parse_plaintext_references)

def _load_csv_claims(filepath: str) -> dict:
    """Load claimed metadata from CSV file. Returns {pmid: claimed_dict}.

    Expected columns: pmid, title, authors, journal, year; pure-arXiv rows
    (arxiv_id, no pmid) are collected into _load_csv_claims.arxiv_rows;
    pure-DOI rows (doi, no pmid/arxiv) into _load_csv_claims.doi_rows (v3.4.0).
    Authors can be semicolon-separated or pipe-separated.
    """
    if not hasattr(_load_csv_claims, "arxiv_rows"):
        _load_csv_claims.arxiv_rows = {}
    if not hasattr(_load_csv_claims, "doi_rows"):
        _load_csv_claims.doi_rows = {}
    claims = {}
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pmid = str(row.get("pmid", "") or row.get("PMID", "")).strip()
                arxiv_col = str(row.get("arxiv_id", "") or row.get("arxiv", "") or "").strip()
                doi_col = str(row.get("doi", "") or row.get("DOI", "") or "").strip()
                if not pmid and not arxiv_col:
                    # v3.4.0: pure-DOI row — collected into the DOI claims map
                    cd = _clean_doi(doi_col) if doi_col else ""
                    if cd:
                        authors_raw = row.get("authors", "") or row.get("Authors", "") or ""
                        if ";" in authors_raw:
                            doi_authors = [a.strip() for a in authors_raw.split(";") if a.strip()]
                        elif "|" in authors_raw:
                            doi_authors = [a.strip() for a in authors_raw.split("|") if a.strip()]
                        else:
                            doi_authors = [a.strip() for a in authors_raw.split(",") if a.strip()]
                        _load_csv_claims.doi_rows.setdefault(cd, {
                            "claimed_title": row.get("title", "") or row.get("Title", "") or "",
                            "claimed_authors": doi_authors,
                            "claimed_journal": row.get("journal", "") or row.get("Journal", "") or "",
                            "claimed_year": str(row.get("year", "") or row.get("Year", "") or ""),
                        })
                    continue
                if pmid and not pmid.isdigit():
                    continue
                if not pmid and arxiv_col:
                    # pure-arXiv row: collected into the arXiv claims map
                    _load_csv_claims.arxiv_rows.setdefault(arxiv_col.lower(), {
                        "claimed_title": row.get("title", "") or row.get("Title", "") or "",
                        "claimed_year": str(row.get("year", "") or row.get("Year", "") or ""),
                        "claimed_doi": str(row.get("doi", "") or row.get("DOI", "") or ""),
                    })
                    continue
                authors_raw = row.get("authors", "") or row.get("Authors", "") or ""
                # Support semicolon, pipe, or comma separation (but comma conflicts with CSV)
                if ";" in authors_raw:
                    authors = [a.strip() for a in authors_raw.split(";") if a.strip()]
                elif "|" in authors_raw:
                    authors = [a.strip() for a in authors_raw.split("|") if a.strip()]
                else:
                    authors = [a.strip() for a in authors_raw.split(",") if a.strip()]
                claims[pmid] = {
                    "claimed_title": row.get("title", "") or row.get("Title", "") or "",
                    "claimed_authors": authors,
                    "claimed_journal": row.get("journal", "") or row.get("Journal", "") or "",
                    "claimed_year": str(row.get("year", "") or row.get("Year", "") or ""),
                    "claimed_doi": str(row.get("doi", "") or row.get("DOI", "") or ""),
                    "claimed_arxiv": str(row.get("arxiv_id", "") or row.get("arxiv", "") or "").strip(),
                }
    except Exception as e:
        print(f"[ERROR] reading CSV claims file: {e}", file=sys.stderr)
    _load_csv_claims.arxiv_rows = getattr(_load_csv_claims, "arxiv_rows", {})
    return claims

def _pmid_claim_from_item(item: dict) -> dict:
    """Normalize one JSON claim object into the PMID claim dict (v3.3.0)."""
    return {
        "claimed_title": str(item.get("title", "") or ""),
        "claimed_authors": [str(a) for a in item["authors"]]
                           if isinstance(item.get("authors"), list) else [],
        "claimed_journal": str(item.get("journal", "") or ""),
        "claimed_year": str(item.get("year", "") or ""),
        "claimed_doi": str(item.get("doi", "") or ""),
    }

def _arxiv_claim_from_item(item: dict) -> dict:
    """Normalize one JSON claim object into the arXiv claim dict.
    v3.3.0 carries claimed_doi through so the preprint↔published
    cross-check can compare it with the arXiv-registered DOI."""
    return {
        "claimed_title": str(item.get("title", "") or ""),
        "claimed_year": str(item.get("year", "") or ""),
        "claimed_doi": str(item.get("doi", "") or ""),
    }

def _doi_claim_from_item(item: dict) -> dict:
    """Normalize one claim object keyed by DOI (v3.4.0): the DOI itself is
    the verification key, so there is no claimed_doi here."""
    return {
        "claimed_title": str(item.get("title", "") or ""),
        "claimed_authors": [str(a) for a in item["authors"]]
                           if isinstance(item.get("authors"), list) else [],
        "claimed_journal": str(item.get("journal", "") or ""),
        "claimed_year": str(item.get("year", "") or ""),
    }

def lint_claims_json(path: str) -> list:
    """Lint a JSON claims file offline. Returns diagnostic strings."""
    issues = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"ERROR: file unreadable as JSON: {e}"]
    if not isinstance(data, list):
        return ["ERROR: JSON claims must be an array of objects"]
    seen_keys = {}
    for i, item in enumerate(data, 1):
        tag = f"row {i}"
        if not isinstance(item, dict):
            issues.append(f"{tag}: ERROR not an object")
            continue
        unknown = sorted(set(item) - _LINT_KNOWN_KEYS)
        if unknown:
            issues.append(f"{tag}: WARN unknown key(s) {unknown} — "
                          f"known: {sorted(_LINT_KNOWN_KEYS)}")
        pmid = str(item.get("pmid", "") or "").strip()
        arx = str(item.get("arxiv_id", "") or "").strip()
        doi = str(item.get("doi", "") or "").strip()
        title = str(item.get("title", "") or "").strip()
        if not (pmid or arx or doi):
            issues.append(f"{tag}: ERROR no pmid / arxiv_id / doi — row is unusable")
            continue
        key = ("pmid", pmid) if pmid and pmid.isdigit() else \
              ("arxiv", arx.lower()) if arx else \
              ("doi", _clean_doi(doi) or doi.lower()) if doi else None
        if key and key in seen_keys:
            issues.append(f"{tag}: WARN duplicate of {tag and seen_keys[key]} "
                          f"(same {key[0]} {key[1]!r}) — the row will be merged")
        else:
            seen_keys[key] = tag
        if pmid and not pmid.isdigit():
            # JSON loader tolerates a non-digit pmid when another ID key
            # routes the row — keep the lint warning at WARN level there
            level = "WARN" if (arx or doi) else "ERROR"
            issues.append(f"{tag}: {level} pmid={pmid!r} is not all digits")
        if arx and not _arxiv_id_valid_shape(arx):
            issues.append(f"{tag}: ERROR arxiv_id={arx!r} fails the arXiv ID shape "
                          f"(new YYMM.NNNNN or old category/NNNNNNN)")
        if doi:
            cd = _clean_doi(doi)
            if not cd or not cd.startswith("10."):
                issues.append(f"{tag}: ERROR doi={doi!r} does not look like a DOI "
                              f"(10./prefix missing after cleaning)")
        if not title:
            issues.append(f"{tag}: WARN no title — verdict caps at partial "
                          f"(existence-only without it)")
        authors = item.get("authors")
        if authors is not None and not isinstance(authors, list):
            issues.append(f"{tag}: WARN authors should be a list of surname strings, "
                          f"got {type(authors).__name__}")
    return issues

def lint_claims_csv(path: str) -> list:
    """Lint a CSV claims file offline. Returns diagnostic strings."""
    issues = []
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = [fn.strip() for fn in (reader.fieldnames or [])]
            rows = [(reader.line_num, row) for row in reader]
    except Exception as e:
        return [f"ERROR: file unreadable as CSV: {e}"]
    unknown_cols = [c for c in fieldnames
                    if c.lower() not in _LINT_KNOWN_COLS]
    if unknown_cols:
        issues.append(f"columns: WARN unknown column(s) {unknown_cols} — "
                      f"known: {sorted(_LINT_KNOWN_COLS)} (typo?)")
    if "pmid" not in [c.lower() for c in fieldnames] and \
       "arxiv_id" not in [c.lower() for c in fieldnames] and \
       "arxiv" not in [c.lower() for c in fieldnames] and \
       "doi" not in [c.lower() for c in fieldnames]:
        issues.append("columns: ERROR none of pmid / arxiv_id / doi present")
    blank = 0
    seen_keys = {}
    for i, row in rows:   # i = physical line number captured at read time
        tag = f"line {i}"
        vals = {k: (v if isinstance(v, str) else "") for k, v in row.items()}
        if not any(v.strip() for v in vals.values()):
            blank += 1
            continue
        get = lambda *names: next((str(vals.get(n, "") or "").strip()
                                   for n in names if str(vals.get(n, "") or "").strip()), "")
        pmid = get("pmid", "PMID")
        arx = get("arxiv_id", "arxiv")
        doi = get("doi", "DOI")
        title = get("title", "Title")
        if not (pmid or arx or doi):
            issues.append(f"{tag}: ERROR no pmid / arxiv_id / doi — row is unusable")
            continue
        if pmid and not pmid.isdigit():
            issues.append(f"{tag}: ERROR pmid={pmid!r} is not all digits")
        if arx and not _arxiv_id_valid_shape(arx):
            issues.append(f"{tag}: ERROR arxiv_id={arx!r} fails the arXiv ID shape "
                          f"(new YYMM.NNNNN or old category/NNNNNNN)")
        if doi:
            cd = _clean_doi(doi)
            if not cd or not cd.startswith("10."):
                issues.append(f"{tag}: ERROR doi={doi!r} does not look like a DOI "
                              f"(10./prefix missing after cleaning)")
        if not title:
            issues.append(f"{tag}: WARN no title — verdict caps at partial "
                          f"(existence-only without it)")
        key = ("pmid", pmid) if pmid and pmid.isdigit() else \
              ("arxiv", arx.lower()) if arx else \
              ("doi", _clean_doi(doi) or doi.lower()) if doi else None
        if key and key in seen_keys:
            issues.append(f"{tag}: WARN duplicate of {seen_keys[key]} "
                          f"(same {key[0]} {key[1]!r}) — the row will be merged")
        else:
            seen_keys[key] = tag
    if blank:
        issues.append(f"rows: INFO {blank} blank row(s) skipped")
    return issues

def lint_claims_bib(path: str) -> list:
    """Lint a BibTeX bibliography offline (v3.6.0)."""
    entries, issues = parse_bibtex(path)
    issues = list(issues)
    if not entries and not any(i.startswith("ERROR") for i in issues):
        issues.append("ERROR: no @entries found in the file")
    seen_keys = {}
    for e in entries:
        # sanitize: the citekey is user data — a ": WARN"/": ERROR" inside it
        # must not spoof the severity counter (which reads after ": ")
        ck = " ".join(str(e["citekey"]).replace(":", "_").split())
        tag = f"@{e['entry_type']} {ck} (line {e['line']})"
        kind, ident, _ = bib_entry_route(e["fields"])
        if kind == "none":
            issues.append(f"{tag}: ERROR no pmid / doi / arXiv ID — "
                          f"entry cannot be routed")
        else:
            key = (kind, ident)
            if key in seen_keys:
                issues.append(f"{tag}: WARN duplicate of {seen_keys[key]} "
                              f"(same {kind} {ident!r}) — the row will be merged")
            else:
                seen_keys[key] = tag
        if not e["fields"].get("title"):
            note = ("stays unknown (no cross-check possible)"
                    if kind in ("doi", "none") else
                    "verdict caps at partial")
            issues.append(f"{tag}: WARN no title — {note}")
    return issues

def lint_claims_ris(path: str) -> list:
    """Lint an RIS bibliography offline (v3.7.0)."""
    entries, issues = parse_ris(path)
    issues = list(issues)
    seen_keys = {}
    for e in entries:
        # sanitize both user-controlled halves — the TY value reaches the tag
        # verbatim and a ": WARN" inside it would spoof the severity counter
        ck = " ".join(str(e["citekey"]).replace(":", "_").split())
        et = " ".join(str(e["entry_type"]).replace(":", "_").split())
        tag = f"@{et} {ck} (line {e['line']})"
        kind, ident, _ = bib_entry_route(ris_to_bib_fields(e["fields"]))
        if kind == "none":
            issues.append(f"{tag}: ERROR no pmid / doi / arXiv ID — "
                          f"record cannot be routed")
        else:
            key = (kind, ident)
            if key in seen_keys:
                issues.append(f"{tag}: WARN duplicate of {seen_keys[key]} "
                              f"(same {kind} {ident!r}) — the row will be merged")
            else:
                seen_keys[key] = tag
        if not e["fields"].get("ti"):
            note = ("stays unknown (no cross-check possible)"
                    if kind in ("doi", "none") else
                    "verdict caps at partial")
            issues.append(f"{tag}: WARN no title — {note}")
    return issues

def write_claims_template(src_path: str, out_path: str) -> tuple:
    """Claims skeleton generator (v4.6.0): read any supported input (plain-text
    reference list, .bib, .ris) and write a claims CSV with every routable
    field the parsers could extract — the user fills the gaps and runs the
    exact --claims-file path. Lowercase header row matches _load_csv_claims.
    Returns (rows_written, notes)."""
    lower = src_path.lower()
    fmt = ("bib" if lower.endswith(".bib")
           else "ris" if lower.endswith(".ris")
           else sniff_bibliography_format(src_path))
    if fmt == "bib":
        entries, issues = parse_bibtex(src_path)
        rows = []
        for e in entries:
            f = e["fields"]
            kind, ident, _ = bib_entry_route(f)
            rows.append({"pmid": f.get("pmid", ""),
                         "doi": ident if kind == "doi" else f.get("doi", ""),
                         "arxiv_id": ident if kind == "arxiv" else "",
                         "title": f.get("title", ""),
                         "authors": "; ".join(f.get("authors", []))
                         if isinstance(f.get("authors"), list) else f.get("authors", ""),
                         "journal": f.get("journal", ""), "year": f.get("year", "")})
    elif fmt == "ris":
        raw, issues = parse_ris(src_path)
        rows = []
        for e in raw:
            f = ris_to_bib_fields(e["fields"])
            kind, ident, _ = bib_entry_route(f)
            rows.append({"pmid": f.get("pmid", ""),
                         "doi": ident if kind == "doi" else f.get("doi", ""),
                         "arxiv_id": ident if kind == "arxiv" else "",
                         "title": f.get("title", ""),
                         "authors": "; ".join(f.get("authors", []))
                         if isinstance(f.get("authors"), list) else f.get("authors", ""),
                         "journal": f.get("journal", ""), "year": f.get("year", "")})
    else:
        entries, issues = parse_plaintext_references(src_path)
        rows = [{"pmid": e["pmid"], "doi": e["doi"], "arxiv_id": e["arxiv_id"],
                 "title": e["claimed_title"],
                 "authors": "; ".join(e["claimed_authors"]),
                 "journal": e["claimed_journal"], "year": e["claimed_year"]}
                for e in entries]
    notes = list(issues)
    if not rows:
        return 0, notes + ["no parseable entries — nothing written"]
    import csv as _csv
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = _csv.DictWriter(fh, fieldnames=["pmid", "doi", "arxiv_id", "title",
                                            "authors", "journal", "year"])
        w.writeheader()
        w.writerows(rows)
    notes.append(f"{len(rows)} skeleton row(s) written — fill the empty cells, "
                 "then run with --claims-file")
    return len(rows), notes

def run_claims_template(src_path: str, out_path: str) -> int:
    rows, notes = write_claims_template(src_path, out_path)
    for n in notes:
        print(f"  claims-template: {n}")
    if not rows:
        return 1
    print(f"Claims template written to {out_path}")
    return 0


# __all__ recalculated at the true end of the module so every
# late-appended name is exported to `import *` consumers
_NAMES = [n for n in dir() if not n.startswith('__')]
__all__ = _NAMES
del _NAMES
