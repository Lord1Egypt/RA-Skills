#!/usr/bin/env python3
"""Deterministic resume extraction layer built on pdfmuse.

Turns a PDF/DOCX resume into (a) clean reading-order Markdown and (b) a JSON
sidecar of deterministically-mined facts (emails, phones, URLs, social profiles,
column layout, parser warnings). The semantic mapping to JSON Resume is done by
Claude reading the Markdown -- this script never guesses job titles or dates, it
only extracts what is literally on the page.

Usage:
    python scripts/extract.py RESUME.pdf [MORE ...] [--out DIR]
    python scripts/extract.py ./resumes/            # a folder (recursive)
    python scripts/extract.py "resumes/*.pdf"       # a glob

For each input file <stem>.<ext> it writes into --out (default ./resume_parsed/):
    <stem>.extract.md    clean markdown body (headers/footers dropped)
    <stem>.extract.json  {source, page_count, columns, warnings, contacts, links}

A JSON manifest of every processed file is printed to stdout.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys


def _ensure_pdfmuse():
    """Import pdfmuse, installing it once on first use so users need no setup."""
    try:
        import pdfmuse  # noqa: F401
        return pdfmuse
    except ImportError:
        print("pdfmuse not found -- installing (one-time)...", file=sys.stderr)
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "pdfmuse"],
            check=True,
        )
        import pdfmuse  # noqa: F401
        return pdfmuse


# --- deterministic field mining -------------------------------------------------

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# URL: explicit scheme, www., or a bare known-network domain with a path.
URL_RE = re.compile(
    r"(?:https?://|www\.)[^\s|,;<>()]+"
    r"|(?:github\.com|linkedin\.com|gitlab\.com|behance\.net|dribbble\.com"
    r"|stackoverflow\.com|medium\.com|zhihu\.com|juejin\.cn|twitter\.com|x\.com)"
    r"/[^\s|,;<>()]+",
    re.IGNORECASE,
)

# Phone: optional +country, then digit groups separated by space/dash/dot/parens.
# Post-filtered by total digit count so we do not match dates or IDs.
PHONE_RE = re.compile(r"(?<![\w])(?:\+?\d{1,3}[\s\-.]?)?(?:\(\d{1,4}\)[\s\-.]?)?\d(?:[\d\s\-.]{5,18}\d)")

# Reject phone candidates that are really dates/year-ranges (e.g. 2012-2016,
# 2020-03-15). A leading '+' or parentheses marks a genuine phone, so keep those.
DATE_LIKE = re.compile(r"^\d{4}[-./]\d{1,4}(?:[-./]\d{1,4})?$")

# Map a host to a human profile-network label for JSON Resume `basics.profiles`.
NETWORKS = {
    "github.com": "GitHub",
    "linkedin.com": "LinkedIn",
    "gitlab.com": "GitLab",
    "twitter.com": "Twitter",
    "x.com": "Twitter",
    "stackoverflow.com": "Stack Overflow",
    "medium.com": "Medium",
    "behance.net": "Behance",
    "dribbble.com": "Dribbble",
    "zhihu.com": "知乎",
    "juejin.cn": "掘金",
}


def _clean_url(u: str) -> str:
    u = u.rstrip(").,;")
    if not u.lower().startswith(("http://", "https://")):
        u = "https://" + u
    return u


def _valid_phone(candidate: str) -> str | None:
    c = candidate.strip()
    # A '+' or '(' signals a real phone; otherwise reject date-like tokens.
    if not c.startswith("+") and "(" not in c and DATE_LIKE.match(c):
        return None
    digits = re.sub(r"\D", "", c)
    if 7 <= len(digits) <= 15:
        return c
    return None


def mine_contacts(text: str, links: list) -> dict:
    emails = _dedup(EMAIL_RE.findall(text))

    urls = _dedup(_clean_url(u) for u in URL_RE.findall(text))
    # Fold in any real hyperlink annotations pdfmuse recovered.
    for ln in links:
        uri = ln.get("uri") or ln.get("url") if isinstance(ln, dict) else None
        if uri:
            urls.append(_clean_url(uri))
    urls = _dedup(urls)

    phones = []
    for cand in PHONE_RE.findall(text):
        v = _valid_phone(cand)
        if v and not EMAIL_RE.search(v):
            phones.append(re.sub(r"\s+", " ", v))
    phones = _dedup(phones)

    profiles = []
    seen = set()
    for u in urls:
        host = re.sub(r"^https?://(www\.)?", "", u, flags=re.IGNORECASE).split("/")[0].lower()
        label = NETWORKS.get(host)
        if label and u not in seen:
            profiles.append({"network": label, "url": u})
            seen.add(u)

    return {"emails": emails, "phones": phones, "urls": urls, "profiles": profiles}


def _dedup(items) -> list:
    out, seen = [], set()
    for x in items:
        if x not in seen:
            out.append(x)
            seen.add(x)
    return out


# --- column-layout heuristic ----------------------------------------------------

def detect_columns(doc) -> int:
    """Best-effort count of text columns via x0 clustering of line boxes.

    Two-column resumes are where pdfmuse reading order is least reliable, so we
    surface a warning rather than silently trusting the order.
    """
    xs = []
    page_w = 0.0
    for pg in doc.pages:
        page_w = max(page_w, pg.width or 0.0)
        for ln in pg.lines:
            bbox = ln["bbox"] if isinstance(ln, dict) else ln.bbox
            xs.append(bbox["x0"])
    if len(xs) < 12 or page_w <= 0:
        return 1
    xs.sort()
    # A genuine column gutter is a wide empty band between two dense x0 clusters.
    mid = page_w * 0.5
    left = [x for x in xs if x < mid]
    right = [x for x in xs if x >= mid]
    if not left or not right:
        return 1
    # Require both sides to hold a real share of lines (>25%) to call it 2-col.
    share = min(len(left), len(right)) / len(xs)
    gutter = min(right) - max(left)
    if share >= 0.25 and gutter > page_w * 0.06:
        return 2
    return 1


# --- per-file extraction --------------------------------------------------------

SUPPORTED = (".pdf", ".docx")


def extract_one(pdfmuse, path: str, out_dir: str) -> dict:
    with open(path, "rb") as f:
        data = f.read()

    markdown = pdfmuse.to_markdown(data, drop_boilerplate=True)
    plain = pdfmuse.to_text(data)  # keep boilerplate: contacts can live in footers
    doc = pdfmuse.parse(data)

    links = []
    for pg in doc.pages:
        links.extend(pg.links or [])

    warnings = list(doc.warnings or [])
    columns = detect_columns(doc)
    if columns >= 2:
        warnings.append(
            "Detected a multi-column layout; reading order may interleave columns. "
            "Verify the work/education timeline against the source PDF."
        )

    contacts = mine_contacts(plain, links)

    stem = os.path.splitext(os.path.basename(path))[0]
    md_path = os.path.join(out_dir, f"{stem}.extract.md")
    json_path = os.path.join(out_dir, f"{stem}.extract.json")

    sidecar = {
        "source": os.path.abspath(path),
        "page_count": len(doc.pages),
        "columns": columns,
        "warnings": warnings,
        "contacts": contacts,
    }

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sidecar, f, ensure_ascii=False, indent=2)

    return {
        "source": path,
        "markdown": md_path,
        "sidecar": json_path,
        "page_count": len(doc.pages),
        "columns": columns,
        "n_emails": len(contacts["emails"]),
        "n_phones": len(contacts["phones"]),
        "n_profiles": len(contacts["profiles"]),
        "warnings": warnings,
    }


def gather_inputs(patterns: list[str]) -> list[str]:
    files: list[str] = []
    for pat in patterns:
        if os.path.isdir(pat):
            for root, _, names in os.walk(pat):
                for n in names:
                    if n.lower().endswith(SUPPORTED):
                        files.append(os.path.join(root, n))
        elif any(ch in pat for ch in "*?[") and not os.path.exists(pat):
            files.extend(glob.glob(pat, recursive=True))
        else:
            files.append(pat)
    # Keep only supported, de-duplicated, stable order.
    return _dedup(f for f in files if f.lower().endswith(SUPPORTED))


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract resumes with pdfmuse.")
    ap.add_argument("inputs", nargs="+", help="PDF/DOCX files, a folder, or a glob")
    ap.add_argument("--out", default="resume_parsed", help="output directory")
    args = ap.parse_args()

    files = gather_inputs(args.inputs)
    if not files:
        print("No .pdf/.docx inputs matched.", file=sys.stderr)
        return 1

    os.makedirs(args.out, exist_ok=True)
    pdfmuse = _ensure_pdfmuse()

    results, failures = [], []
    for path in files:
        try:
            results.append(extract_one(pdfmuse, path, args.out))
        except Exception as e:  # keep the batch going; report the casualty
            failures.append({"source": path, "error": f"{type(e).__name__}: {e}"})
            print(f"WARN failed on {path}: {e}", file=sys.stderr)

    manifest = {"out_dir": args.out, "count": len(results), "results": results}
    if failures:
        manifest["failures"] = failures
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
