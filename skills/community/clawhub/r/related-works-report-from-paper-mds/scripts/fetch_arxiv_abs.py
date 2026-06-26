#!/usr/bin/env python3
"""Fetch title/authors/abstract from an arXiv abs/html/pdf URL."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen


USER_AGENT = "Mozilla/5.0 (compatible; related-works-report skill)"


def normalize_abs_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.netloc not in {"arxiv.org", "www.arxiv.org"}:
        raise ValueError(f"unsupported host: {parsed.netloc}")

    path = parsed.path.rstrip("/")
    if path.startswith("/abs/"):
        paper_id = path[len("/abs/") :]
    elif path.startswith("/html/"):
        paper_id = path[len("/html/") :]
    elif path.startswith("/pdf/"):
        paper_id = path[len("/pdf/") :].removesuffix(".pdf")
    else:
        raise ValueError(f"unsupported arXiv path: {parsed.path}")

    paper_id = re.sub(r"v\d+$", "", paper_id)
    return f"https://arxiv.org/abs/{paper_id}"


def fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def extract_meta_list(name: str, text: str) -> list[str]:
    pattern = rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"'
    return [html.unescape(v).strip() for v in re.findall(pattern, text)]


def extract_meta_one(name: str, text: str) -> str:
    values = extract_meta_list(name, text)
    return values[0] if values else ""


def extract_abstract(text: str) -> str:
    abstract = extract_meta_one("citation_abstract", text)
    if abstract:
        return re.sub(r"\s+", " ", abstract).strip()

    match = re.search(
        r'<blockquote class="abstract mathjax">\s*<span class="descriptor">Abstract:</span>(.*?)</blockquote>',
        text,
        flags=re.S,
    )
    if not match:
        return ""

    raw = re.sub(r"<[^>]+>", " ", match.group(1))
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def fetch_metadata(url: str) -> dict[str, object]:
    abs_url = normalize_abs_url(url)
    text = fetch_html(abs_url)
    return {
        "input_url": url,
        "canonical_abs_url": abs_url,
        "arxiv_id": extract_meta_one("citation_arxiv_id", text),
        "title": extract_meta_one("citation_title", text),
        "authors": extract_meta_list("citation_author", text),
        "abstract": extract_abstract(text),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args(argv)

    try:
        result = fetch_metadata(args.url)
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
