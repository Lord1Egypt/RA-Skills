#!/usr/bin/env python3
"""Recover public/open PDFs for a MentorForge publication index.

This script is intentionally conservative: it only downloads direct PDF URLs
already present in the index, writes a recovered index, and records failures for
agent/browser fallback. It does not use paywalled sources.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

try:
    import certifi
except Exception:  # pragma: no cover
    certifi = None


def slugify(text: str, max_len: int = 90) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text or "").strip("-").lower()
    return text[:max_len].strip("-") or "paper"


def load_index(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"metadata": {}, "publications": data}, data
    publications = data.get("publications")
    if not isinstance(publications, list):
        raise ValueError("publication index must be a list or contain a `publications` list")
    return data, publications


def ssl_context(allow_insecure: bool) -> ssl.SSLContext:
    if allow_insecure:
        return ssl._create_unverified_context()  # noqa: SLF001
    if certifi is not None:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


def candidate_pdf_url(record: dict[str, Any]) -> str | None:
    for key in ["pdf_url", "pdf", "open_pdf_url"]:
        value = record.get(key)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value
    links = record.get("links")
    if isinstance(links, dict):
        for key in ["pdf", "PDF"]:
            value = links.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                return value
    return None


def download_pdf(url: str, dest: Path, timeout: int, allow_insecure: bool) -> tuple[bool, str]:
    if dest.exists() and dest.stat().st_size > 5000:
        return True, f"already exists: {dest.stat().st_size} bytes"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 MentorForge/0.2",
            "Accept": "application/pdf,*/*",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=ssl_context(allow_insecure)) as response:
            payload = response.read()
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"

    if len(payload) < 5000:
        return False, f"too small: {len(payload)} bytes"
    if not payload[:2048].lstrip().startswith(b"%PDF"):
        return False, "response is not a PDF"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(payload)
    return True, f"{len(payload)} bytes"


def main() -> int:
    parser = argparse.ArgumentParser(description="Recover public PDFs for a MentorForge publication index.")
    parser.add_argument("--publication-index", required=True, type=Path)
    parser.add_argument("--pdf-dir", type=Path, help="Directory for recovered PDFs. Defaults to sibling `papers/`.")
    parser.add_argument("--output-index", type=Path, help="Recovered index path. Defaults to recovered-publication-index.json next to the input.")
    parser.add_argument("--report", type=Path, help="Markdown report path. Defaults to pdf-recovery-report.md next to the input.")
    parser.add_argument("--max-pdfs", type=int, default=30)
    parser.add_argument("--max-attempts", type=int, default=80)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--allow-insecure-ssl", action="store_true")
    args = parser.parse_args()

    index_path = args.publication_index
    data, records = load_index(index_path)
    pdf_dir = args.pdf_dir or index_path.parent / "papers"
    output_index = args.output_index or index_path.parent / "recovered-publication-index.json"
    report_path = args.report or index_path.parent / "pdf-recovery-report.md"

    jobs: list[tuple[int, dict[str, Any], str, Path]] = []
    already = 0
    for i, record in enumerate(records):
        local_pdf = record.get("local_pdf")
        if isinstance(local_pdf, str) and Path(local_pdf).exists() and Path(local_pdf).stat().st_size > 5000:
            already += 1
            continue
        url = candidate_pdf_url(record)
        if not url:
            continue
        title = record.get("title") or f"paper-{i + 1}"
        year = record.get("year") or "unknown"
        paper_id = record.get("id") or f"paper-{i + 1}"
        dest = pdf_dir / f"{year}_{slugify(title)}_{slugify(str(paper_id), 32)}.pdf"
        jobs.append((i, record, url, dest))
        if len(jobs) >= args.max_attempts:
            break

    successes = 0
    attempts: list[tuple[dict[str, Any], str, bool, str, Path]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        future_map = {
            pool.submit(download_pdf, url, dest, args.timeout, args.allow_insecure_ssl): (record, url, dest)
            for _i, record, url, dest in jobs
        }
        for future in as_completed(future_map):
            record, url, dest = future_map[future]
            ok, status = future.result()
            if ok:
                record["local_pdf"] = str(dest)
                successes += 1
            attempts.append((record, url, ok, status, dest))
            if already + successes >= args.max_pdfs:
                # Let already submitted jobs finish; do not schedule more.
                pass

    recovered = {
        **data,
        "metadata": {
            **(data.get("metadata") if isinstance(data.get("metadata"), dict) else {}),
            "pdf_recovery": {
                "already_local": already,
                "attempted": len(attempts),
                "downloaded": successes,
                "pdf_dir": str(pdf_dir),
            },
        },
        "publications": records,
    }
    output_index.write_text(json.dumps(recovered, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# PDF Recovery Report",
        "",
        f"- Publication index: `{index_path}`",
        f"- Already local PDFs: {already}",
        f"- Download attempts: {len(attempts)}",
        f"- Successful downloads: {successes}",
        "",
        "| Status | Year | Title | URL | Local PDF / Error |",
        "|---|---:|---|---|---|",
    ]
    for record, url, ok, status, dest in sorted(attempts, key=lambda item: (not item[2], str(item[0].get("title", "")))):
        title = str(record.get("title") or "").replace("|", "\\|")
        year = record.get("year") or ""
        detail = str(dest if ok else status).replace("|", "\\|")
        lines.append(f"| {'ok' if ok else 'fail'} | {year} | {title} | {url} | {detail} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Already local PDFs: {already}")
    print(f"Attempted: {len(attempts)}")
    print(f"Downloaded: {successes}")
    print(f"Wrote recovered index: {output_index}")
    print(f"Wrote report: {report_path}")
    return 0 if successes or already else 1


if __name__ == "__main__":
    sys.exit(main())
