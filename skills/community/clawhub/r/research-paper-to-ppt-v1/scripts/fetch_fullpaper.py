#!/usr/bin/env python3
"""Fetch full paper content from InfoX-Med full-paper API with token normalization and figure extraction.

Purpose:
- Work around environment tokens that may contain non-hex prefixes or wrong lengths.
- Try a small set of token candidates derived from INFOX_MED_TOKEN.
- Return normalized paper meta, full text, and a best-effort figure inventory.

This script is intentionally conservative:
- It does not fabricate figures.
- It only emits figure refs/URLs found in API payload fields or text.
- If the API cannot be read with a valid token, it exits non-zero.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Tuple
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_BASE = os.environ.get("INFOX_MED_API_BASE", "http://60.205.166.229:9306").rstrip("/")
FAIL = "检索失败，无法生成"
TOKEN_RE = re.compile(r"^[0-9a-f]{32}\|\d{7}$")
URL_RE = re.compile(r"https?://[^\s\]\)>'\"]+")
FIG_RE = re.compile(r"\b(?:Figure|Fig\.?|Table)\s*([0-9]+[A-Za-z]?(?:\s*[A-Za-z]\s*[–\-]\s*[A-Za-z])?)", re.I)
IMG_EXT_RE = re.compile(r"\.(?:png|jpg|jpeg|webp|gif|tif|tiff|svg)(?:\?|$)", re.I)
PDF_RE = re.compile(r"\.pdf(?:\?|$)", re.I)


def normalize_token_candidates(raw: str) -> List[str]:
    raw = (raw or "").strip()
    if not raw:
        return []
    candidates: List[str] = []
    seen = set()

    def add(tok: str) -> None:
        tok = tok.strip()
        if tok and tok not in seen:
            seen.add(tok)
            candidates.append(tok)

    add(raw)
    if "|" in raw:
        left, right = raw.rsplit("|", 1)
        digits = re.sub(r"\D", "", right)
        hex32s = re.findall(r"[0-9a-f]{32}", left.lower())
        for hx in hex32s:
            if len(digits) >= 7:
                add(f"{hx}|{digits[:7]}")
        # Also try taking the last 32 hex chars from a mixed prefix.
        compact_hex = "".join(re.findall(r"[0-9a-f]", left.lower()))
        if len(compact_hex) >= 32 and len(digits) >= 7:
            add(f"{compact_hex[-32:]}|{digits[:7]}")
    return [t for t in candidates if TOKEN_RE.match(t)]


def http_get_json(url: str, token: str) -> Dict[str, Any]:
    req = Request(url, headers={"X-Token": token, "Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def fetch_by_doc_id(doc_id: str, tokens: Iterable[str]) -> Tuple[Dict[str, Any], str]:
    url = f"{API_BASE}/api/v1/paper/doc-id/{doc_id}?raw=true"
    last_err = None
    for token in tokens:
        try:
            payload = http_get_json(url, token)
            return payload, token
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if hasattr(e, 'read') else str(e)
            last_err = f"HTTP {e.code}: {body}"
            continue
        except URLError as e:
            last_err = f"URL error: {e}"
            continue
        except Exception as e:
            last_err = str(e)
            continue
    raise SystemExit(last_err or FAIL)


def first_nonempty(d: Dict[str, Any], keys: List[str]) -> Any:
    for k in keys:
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return None


def collect_urls(obj: Any, out: List[str]) -> None:
    if isinstance(obj, dict):
        for v in obj.values():
            collect_urls(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_urls(v, out)
    elif isinstance(obj, str):
        out.extend(URL_RE.findall(obj))


def infer_figure_ref(text: str, idx: int) -> str:
    m = FIG_RE.search(text or "")
    if m:
        return f"Figure {m.group(1).replace(' ', '')}"
    return f"Figure {idx}"


def extract_figures(rec: Dict[str, Any]) -> List[Dict[str, str]]:
    urls: List[str] = []
    collect_urls(rec, urls)
    figures: List[Dict[str, str]] = []
    seen = set()

    # First pass: structured figure/image-like fields if present
    for key, value in rec.items():
        lk = str(key).lower()
        if any(x in lk for x in ["figure", "fig", "image", "img", "graphic", "table"]):
            bucket: List[str] = []
            collect_urls(value, bucket)
            for u in bucket:
                if IMG_EXT_RE.search(u) and u not in seen:
                    seen.add(u)
                    figures.append({"figure_ref": infer_figure_ref(str(value), len(figures)+1), "url": u})

    # Second pass: any image-like URLs anywhere in payload
    for u in urls:
        if IMG_EXT_RE.search(u) and u not in seen:
            seen.add(u)
            figures.append({"figure_ref": f"Figure {len(figures)+1}", "url": u})

    # Deduplicate obvious PDF URLs away from figures.
    figures = [f for f in figures if not PDF_RE.search(f.get("url", ""))]
    return figures


def derive_title_from_markdown(md: str) -> str:
    for line in (md or "").splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            return s.lstrip("#").strip()
    return ""


def build_meta(rec: Dict[str, Any]) -> Dict[str, Any]:
    md = str(first_nonempty(rec, ["md_content", "full_text", "fulltext", "content_md", "content"]) or "")
    authors_raw = first_nonempty(rec, ["authors", "author", "author_list"]) or ""
    authors = authors_raw if isinstance(authors_raw, list) else [a.strip() for a in str(authors_raw).split(",") if a.strip()]
    return {
        "title_en": first_nonempty(rec, ["title", "title_en"]) or derive_title_from_markdown(md),
        "title_zh": first_nonempty(rec, ["title_zh", "title_cn", "chinese_title"]) or "",
        "authors": authors,
        "first_author": authors[0] if authors else "",
        "corresponding_author": first_nonempty(rec, ["corresponding_author", "corr_author"]) or "",
        "journal": first_nonempty(rec, ["journal", "journal_name"]) or "",
        "year": str(first_nonempty(rec, ["year", "publish_year"]) or "")[:4],
        "doi": first_nonempty(rec, ["doi"]) or "",
        "pmid": str(first_nonempty(rec, ["pmid"]) or ""),
        "source_id": str(first_nonempty(rec, ["doc_id", "id", "_id"]) or ""),
        "pdf_url": first_nonempty(rec, ["pdf_url", "pdf", "pdf_link", "qiniu_url"]) or "",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc-id", required=True)
    ap.add_argument("--meta-out", required=True)
    ap.add_argument("--fulltext-out", required=True)
    ap.add_argument("--figures-out", required=True)
    ap.add_argument("--debug-out")
    args = ap.parse_args()

    raw = os.environ.get("INFOX_MED_TOKEN", "")
    tokens = normalize_token_candidates(raw)
    if not tokens:
        raise SystemExit("No valid token candidate derived from INFOX_MED_TOKEN")

    payload, used_token = fetch_by_doc_id(args.doc_id, tokens)
    data = payload.get("data") or []
    if not data:
        raise SystemExit(FAIL)
    rec = data[0]
    meta = build_meta(rec)
    fulltext = first_nonempty(rec, ["full_text", "fulltext", "body_markdown", "content_md", "content", "md_content"]) or ""
    fulltext_zh = first_nonempty(rec, ["full_text_zh", "fulltext_zh"]) or ""
    merged_fulltext = fulltext if len(fulltext) >= len(fulltext_zh) else fulltext_zh
    figures = extract_figures(rec)

    with open(args.meta_out, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    with open(args.fulltext_out, "w", encoding="utf-8") as f:
        f.write(merged_fulltext)
    with open(args.figures_out, "w", encoding="utf-8") as f:
        json.dump(figures, f, ensure_ascii=False, indent=2)
    if args.debug_out:
        with open(args.debug_out, "w", encoding="utf-8") as f:
            json.dump({
                "used_token": used_token,
                "token_candidates": tokens,
                "payload_keys": list(rec.keys()),
                "figure_count": len(figures),
            }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
