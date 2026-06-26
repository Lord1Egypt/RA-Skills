#!/usr/bin/env python3
"""extract_pdf.py — extract text from a PDF using pypdf.

Usage:
  python scripts/extract_pdf.py --input paper.pdf --output paper.txt
  python scripts/extract_pdf.py --url https://arxiv.org/pdf/2301.12345 --output paper.txt
  python scripts/extract_pdf.py --doi 10.1038/s41586-020-2649-2 --output paper.txt
  python scripts/extract_pdf.py --input paper.pdf --pages 1-5

DOI resolution (--doi):
  1. If paper-fetch skill is installed, shells out to it (5-source OA chain).
  2. Otherwise, queries Unpaywall directly (single-source fallback).
  Discovery: PAPER_FETCH_SCRIPT env var → ~/.claude/skills/paper-fetch/scripts/fetch.py

Limitations (printed as warnings, not errors):
  - Scanned (image-only) PDFs return empty or junk text. Use OCR separately.
  - Multi-column layouts may interleave columns; this is a known pypdf limit.
  - Math/figures are dropped.

The script never crashes the pipeline — it always exits 0 with a JSON status.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from _common import (
    EXIT_RUNTIME, EXIT_UPSTREAM, EXIT_VALIDATION, err, maybe_emit_schema, ok,
)

try:
    from pypdf import PdfReader
except ImportError:
    err("missing_dependency",
        "pypdf not installed. Run: pip install pypdf",
        retryable=False, exit_code=EXIT_RUNTIME,
        dependency="pypdf")


# ---------- paper-fetch discovery ----------

_FETCH_SCRIPT = "scripts/fetch.py"

# All known skill install paths across platforms.
# Order: Claude Code → OpenCode → OpenClaw → Hermes → agents convention.
_CONVENTION_PATHS = [
    Path.home() / ".claude" / "skills" / "paper-fetch" / _FETCH_SCRIPT,
    Path.home() / ".config" / "opencode" / "skills" / "paper-fetch" / _FETCH_SCRIPT,
    Path.home() / ".opencode" / "skills" / "paper-fetch" / _FETCH_SCRIPT,
    Path.home() / ".openclaw" / "skills" / "paper-fetch" / _FETCH_SCRIPT,
    Path.home() / ".hermes" / "skills" / "research" / "paper-fetch" / _FETCH_SCRIPT,
    Path.home() / ".agents" / "skills" / "paper-fetch" / _FETCH_SCRIPT,
]


def _find_paper_fetch() -> Path | None:
    """Locate paper-fetch's fetch.py. Returns path or None.

    Discovery chain:
      1. PAPER_FETCH_SCRIPT env var (explicit override)
      2. Known skill install paths across platforms
    """
    env = os.environ.get("PAPER_FETCH_SCRIPT")
    if env:
        p = Path(env)
        if p.is_file():
            return p
        print(f"[warn] PAPER_FETCH_SCRIPT={env} not found, trying convention paths",
              file=sys.stderr)
    for path in _CONVENTION_PATHS:
        if path.is_file():
            return path
    return None


def _fetch_via_paper_fetch(doi: str, fetch_script: Path) -> tuple[Path, dict[str, Any]]:
    """Resolve DOI via paper-fetch skill. Returns (pdf_path, metadata)."""
    tmpdir = tempfile.mkdtemp(prefix="scholar_fetch_")
    result = subprocess.run(
        [sys.executable, str(fetch_script), doi,
         "--format", "json", "--out", tmpdir],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        # Try to parse structured error from paper-fetch
        detail = result.stdout.strip() or result.stderr.strip()
        err("paper_fetch_failed",
            f"paper-fetch exited {result.returncode} for {doi}: {detail}",
            retryable=result.returncode in (2, 4),
            exit_code=EXIT_UPSTREAM, doi=doi)

    try:
        envelope = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        err("paper_fetch_bad_response",
            f"paper-fetch returned non-JSON for {doi}",
            retryable=False, exit_code=EXIT_RUNTIME, doi=doi)

    if not envelope.get("ok"):
        e = envelope.get("error", {})
        err("paper_fetch_error",
            e.get("message", f"paper-fetch failed for {doi}"),
            retryable=e.get("retryable", False),
            exit_code=EXIT_UPSTREAM, doi=doi)

    data = envelope.get("data", {})
    local_path = data.get("local_path") or data.get("path")
    if not local_path or not Path(local_path).is_file():
        # Check tmpdir for any PDF
        pdfs = list(Path(tmpdir).glob("*.pdf"))
        if pdfs:
            local_path = str(pdfs[0])
        else:
            err("paper_fetch_no_pdf",
                f"paper-fetch succeeded but no PDF found for {doi}",
                retryable=False, exit_code=EXIT_RUNTIME, doi=doi)

    fetch_meta = {
        "doi": doi,
        "source": data.get("source", "paper-fetch"),
        "title": data.get("title"),
        "authors": data.get("authors"),
        "year": data.get("year"),
        "pdf_url": data.get("pdf_url") or data.get("url"),
    }
    return Path(local_path), fetch_meta


def _fetch_via_unpaywall(doi: str) -> tuple[Path, dict[str, Any]]:
    """Fallback: resolve DOI via Unpaywall API directly."""
    import httpx

    email = os.environ.get("SCHOLAR_MAILTO", "scholar-deep-research@example.com")
    api_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"

    try:
        r = httpx.get(api_url, follow_redirects=True, timeout=30.0,
                      headers={"User-Agent": "scholar-deep-research/0.1"})
        r.raise_for_status()
    except httpx.HTTPError as e:
        status = getattr(getattr(e, "response", None), "status_code", None)
        err("unpaywall_request_failed",
            f"Unpaywall API failed for {doi}: {type(e).__name__}: {e}",
            retryable=True, exit_code=EXIT_UPSTREAM,
            doi=doi, status=status)

    data = r.json()
    best_oa = data.get("best_oa_location") or {}
    pdf_url = best_oa.get("url_for_pdf") or best_oa.get("url")

    if not pdf_url:
        err("no_open_access_pdf",
            f"No open-access PDF found for DOI {doi} via Unpaywall",
            retryable=False, exit_code=EXIT_VALIDATION,
            doi=doi, is_oa=data.get("is_oa", False))

    # Download the PDF
    try:
        r2 = httpx.get(pdf_url, follow_redirects=True, timeout=60.0,
                       headers={"User-Agent": "scholar-deep-research/0.1"})
        r2.raise_for_status()
    except httpx.HTTPError as e:
        status = getattr(getattr(e, "response", None), "status_code", None)
        err("pdf_download_failed",
            f"Failed to download PDF from {pdf_url}: {type(e).__name__}: {e}",
            retryable=True, exit_code=EXIT_UPSTREAM,
            doi=doi, pdf_url=pdf_url, status=status)

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.write(r2.content)
    tmp.close()

    fetch_meta = {
        "doi": doi,
        "source": "unpaywall_fallback",
        "title": data.get("title"),
        "authors": [a.get("family", "") + ", " + a.get("given", "")
                     for a in (data.get("z_authors") or []) if a.get("family")],
        "year": data.get("year"),
        "pdf_url": pdf_url,
    }
    return Path(tmp.name), fetch_meta


# ---------- extraction ----------

def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(total))
    pages: set[int] = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a) - 1, int(b)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < total)


def extract(pdf_path: Path, pages: list[int]) -> tuple[str, dict]:
    reader = PdfReader(str(pdf_path))
    parts = []
    warnings = []
    for i in pages:
        try:
            t = reader.pages[i].extract_text() or ""
        except Exception as e:
            warnings.append(f"page {i+1}: {e}")
            t = ""
        parts.append(t)
    text = "\n\n".join(parts)
    char_count = len(text.strip())
    is_scanned = char_count < 200 * len(pages)
    meta = {
        "pages_extracted": len(pages),
        "total_pages": len(reader.pages),
        "char_count": char_count,
        "looks_scanned": is_scanned,
        "warnings": warnings,
    }
    return text, meta


def main() -> None:
    p = argparse.ArgumentParser(description="Extract text from PDF.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="Local PDF path")
    src.add_argument("--url", help="URL to download then extract")
    src.add_argument("--doi", help="DOI to resolve via paper-fetch or Unpaywall")
    p.add_argument("--output", help="Write extracted text to this path")
    p.add_argument("--pages", help="Page range, e.g. 1-5,8,10-12")
    p.add_argument("--schema", action="store_true",
                   help="Print this command's parameter schema as JSON and exit")
    maybe_emit_schema(p, "extract_pdf")
    args = p.parse_args()

    fetch_meta: dict[str, Any] | None = None

    if args.doi:
        fetch_script = _find_paper_fetch()
        if fetch_script:
            print(f"[info] Using paper-fetch: {fetch_script}", file=sys.stderr)
            pdf_path, fetch_meta = _fetch_via_paper_fetch(args.doi, fetch_script)
        else:
            print("[info] paper-fetch not found, falling back to Unpaywall",
                  file=sys.stderr)
            pdf_path, fetch_meta = _fetch_via_unpaywall(args.doi)
    elif args.url:
        import httpx
        try:
            r = httpx.get(args.url, follow_redirects=True, timeout=60.0,
                          headers={"User-Agent": "scholar-deep-research/0.1"})
            r.raise_for_status()
        except httpx.HTTPError as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            err("download_failed",
                f"Failed to download {args.url}: {type(e).__name__}: {e}",
                retryable=True, exit_code=EXIT_UPSTREAM,
                url=args.url, status=status)
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.write(r.content)
        tmp.close()
        pdf_path = Path(tmp.name)
    else:
        pdf_path = Path(args.input)
        if not pdf_path.exists():
            err("file_not_found",
                f"PDF not found: {pdf_path}",
                retryable=False, exit_code=EXIT_VALIDATION,
                path=str(pdf_path))

    try:
        reader = PdfReader(str(pdf_path))
        page_indices = parse_pages(args.pages, len(reader.pages))
        text, meta = extract(pdf_path, page_indices)
    except Exception as e:
        err("pypdf_failure",
            f"pypdf failed to read {pdf_path}: {type(e).__name__}: {e}",
            retryable=False, exit_code=EXIT_RUNTIME,
            path=str(pdf_path))

    if fetch_meta:
        meta["fetch_meta"] = fetch_meta

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        meta["output"] = str(out)
    else:
        meta["text_preview"] = text[:500]

    ok(meta)


if __name__ == "__main__":
    main()
