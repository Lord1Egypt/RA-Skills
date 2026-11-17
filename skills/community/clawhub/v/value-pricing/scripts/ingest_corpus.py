"""Ingest knowledge bases (an Obsidian vault, docs, decks, past artifacts) into corpus/index.jsonl.

One record per heading-delimited chunk: source, path, title, heading trail, front matter, tags,
[[wikilinks]], text. The vault's own structure survives, so "every note tagged #customer" or "the Pricing
folder" stays queryable. Reads .md .markdown .txt .html .htm, and .pdf with the Python pypdf library.
Skips .obsidian/, .git/, node_modules/ and files over --max-mb. Read-only on the sources.

  ingest_corpus.py --study S --path ~/Vault --path ./decks [--grep "pric|customer"]

Also writes corpus/index_stats.json (files, chunks, top folders, top tags): read it first to see the
shape of the material, then grep the index.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
import yaml
from bs4 import BeautifulSoup

from common import Study, study_arg

EXT = {".md", ".markdown", ".txt", ".html", ".htm", ".pdf"}
SKIP_DIRS = {".obsidian", ".git", "node_modules", ".trash", "__pycache__", ".venv"}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
TAG = re.compile(r"(?:^|\s)#([A-Za-z][\w/-]+)")


def read(p: Path) -> str:
    if p.suffix.lower() == ".pdf":
        if PdfReader is None:
            raise RuntimeError("PDF ingestion requires pypdf; install scripts/requirements.txt")
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(p)).pages)
    raw = p.read_text(errors="replace")
    if p.suffix.lower() in (".html", ".htm"):
        soup = BeautifulSoup(raw, "lxml")
        for t in soup(["script", "style"]):
            t.decompose()
        return "\n".join(l.strip() for l in soup.get_text("\n").splitlines() if l.strip())
    return raw


def front_matter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            try:
                fm = yaml.safe_load(text[3:end]) or {}
                return (fm if isinstance(fm, dict) else {}), text[end + 4:]
            except yaml.YAMLError:
                pass
    return {}, text


def chunks(body: str, max_chars: int):
    trail, buf = [], []
    for line in body.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if "".join(buf).strip():
                yield list(trail), "\n".join(buf).strip()
            buf = []
            trail = trail[: len(m.group(1)) - 1] + [m.group(2).strip()]
        else:
            buf.append(line)
            if sum(len(b) for b in buf) > max_chars:
                yield list(trail), "\n".join(buf).strip()
                buf = []
    if "".join(buf).strip():
        yield list(trail), "\n".join(buf).strip()


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--path", action="append", required=True)
    ap.add_argument("--grep", help="keep only files whose path or text matches this regex")
    ap.add_argument("--max-mb", type=float, default=5)
    ap.add_argument("--max-chars", type=int, default=4000)
    a = ap.parse_args()
    st = Study(a.study)
    rx = re.compile(a.grep, re.I) if a.grep else None
    files, n, folders, tags = 0, 0, Counter(), Counter()
    with st.path("corpus", "index.jsonl").open("w") as fh:
        for root in a.path:
            root = Path(root).expanduser().resolve()
            for p in sorted(root.rglob("*")):
                if p.is_symlink() or p.suffix.lower() not in EXT or any(part in SKIP_DIRS for part in p.parts) or not p.is_file():
                    continue
                if p.stat().st_size > a.max_mb * 1e6:
                    continue
                text = read(p)
                if not text.strip() or (rx and not (rx.search(str(p)) or rx.search(text))):
                    continue
                fm, body = front_matter(text)
                fmt = fm.get("tags") or []
                fmt = [fmt] if isinstance(fmt, str) else fmt
                ftags = set(TAG.findall(body)) | {str(t) for t in fmt}
                links = sorted(set(WIKILINK.findall(body)))
                rel = str(p.relative_to(root))
                files += 1
                folders[str(Path(rel).parent)] += 1
                tags.update(ftags)
                for i, (trail, txt) in enumerate(chunks(body, a.max_chars)):
                    fh.write(json.dumps({"source": str(root), "path": rel, "chunk": i, "title": str(fm.get("title") or p.stem),
                                         "headings": trail, "front_matter": {k: str(v) for k, v in fm.items()},
                                         "tags": sorted(ftags), "wikilinks": links, "text": txt}, ensure_ascii=False) + "\n")
                    n += 1
    stats = {"files": files, "chunks": n, "top_folders": folders.most_common(25), "top_tags": tags.most_common(40)}
    st.path("corpus", "index_stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
