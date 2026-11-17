#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2epub.py — Convert Full.md into an EPUB with one XHTML document per
translated chapter.

Chapter documents are named chapter_XXX.html using transIdx from
_vartemp.json when available. The EPUB NCX/Nav TOC uses the same translated
chapter order and titles, so EReaders receive a stable chapter index.

Usage:
  uv run --with ebooklib --with markdown python md2epub.py \
      --input Full.md --output Full.epub --title "Book Title"

Optional:
  --state _vartemp.json
  --cover assets/cover.png
"""
from __future__ import annotations

import argparse
import datetime
import html
import json
import mimetypes
import re
import sys
from pathlib import Path

try:
    import markdown
    from ebooklib import epub
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e.name}", file=sys.stderr)
    print("       Use: uv run --with ebooklib --with markdown python md2epub.py",
          file=sys.stderr)
    raise SystemExit(1)

CH_HEADING_RE = re.compile(r"^#\s+(Chương\s+(\d+))(?:\s*[:—–-]\s*(.*))?\s*$",
                           re.IGNORECASE)
DIGITS_RE = re.compile(r"\d+")
TRAILING_SEP = re.compile(
    r"^(---|<div style=\"page-break-after: always;\"></div>)$"
)
IMG_SRC_RE = re.compile(r'src="(assets/[^"]+)"')
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

CSS = """\
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.65;
       margin: 5% 6%; color: #1a1a1a; }
h1 { font-size: 1.5em; text-align: center; page-break-before: always; margin-top: 0; }
h2 { font-size: 1.2em; margin-top: 1.4em; }
p { text-align: justify; margin: 0.7em 0; }
blockquote { font-style: italic; color: #555; border-left: 3px solid #bbb;
             margin: 1em 0; padding: 0.1em 0 0.1em 1em; }
hr { border: 0; border-top: 1px solid #aaa; margin: 1.5em 0; }
img { max-width: 100%; height: auto; display: block; margin: 1em auto; }
.cover { text-align: center; padding-top: 25%; }
.cover h1 { page-break-before: avoid; font-size: 2em; margin-bottom: 0.5em; }
.sub { color: #666; font-style: italic; }
"""


def load_state(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def chapter_index(state: dict) -> dict[int, dict]:
    """Map translated chapter index (transIdx) to its metadata."""
    result = {}
    for chapter in state.get("chapters", []):
        if not isinstance(chapter, dict):
            continue
        try:
            trans_idx = int(chapter["transIdx"])
        except (KeyError, TypeError, ValueError):
            continue
        result[trans_idx] = chapter
    return result


def split_chapters(text: str) -> list[tuple[int, str | None, list[str]]]:
    """
    Split Full.md into translated chapters.

    Returns (fallback_index, chapter_number, lines). Non-chapter material is
    ignored when chapter headings exist, preserving the previous behavior.
    """
    chunks = []
    cur = []
    cur_num = None
    fallback = 0
    for line in text.splitlines():
        m = CH_HEADING_RE.match(line)
        if m:
            if cur and cur_num is not None:
                fallback += 1
                chunks.append((fallback, cur_num, cur))
            cur = [line]
            cur_num = m.group(2)
        else:
            cur.append(line)
    if cur and cur_num is not None:
        fallback += 1
        chunks.append((fallback, cur_num, cur))
    return chunks


def clean_lines(lines: list[str]) -> list[str]:
    lines = list(lines)
    while lines and (not lines[-1].strip()
                     or TRAILING_SEP.match(lines[-1].strip())):
        lines.pop()
    return lines


def md_to_html(md_text: str) -> str:
    md_text = WIKILINK_RE.sub(lambda m: m.group(2) or m.group(1), md_text)
    return markdown.markdown(md_text, extensions=["extra", "sane_lists"])


def collect_images(chapters_html: list[str]) -> set[str]:
    return {src for body in chapters_html for src in IMG_SRC_RE.findall(body)}


def build_epub(md_path: Path, out_path: Path, title: str,
               cover_img: Path | None, state_path: Path | None) -> tuple[int, list[str]]:
    text = md_path.read_text(encoding="utf-8-sig")
    raw_chunks = split_chapters(text)
    if not raw_chunks:
        print(f"[ERROR] No '# Chương N' headings found in {md_path.name}")
        return 1, []

    state = load_state(state_path)
    by_trans_idx = chapter_index(state)
    warnings: list[str] = []

    chapters = []
    for fallback_idx, number, lines in raw_chunks:
        lines = clean_lines(lines)
        meta = by_trans_idx.get(fallback_idx, {})
        # Prefer the explicit translated chapter title from state. Otherwise
        # preserve the title from the Markdown heading.
        heading_match = CH_HEADING_RE.match(lines[0]) if lines else None
        source_heading_title = (
            heading_match.group(3).strip()
            if heading_match and heading_match.group(3)
            else f"Chương {number}"
        )
        heading = meta.get("title") or source_heading_title
        trans_idx = int(meta.get("transIdx", fallback_idx))
        chapters.append((trans_idx, number, heading, lines))

    # EPUB navigation must have unique, stable order.
    seen = set()
    for trans_idx, _, _, _ in chapters:
        if trans_idx in seen:
            warnings.append(
                f"Duplicate transIdx={trans_idx}; falling back to source order."
            )
        seen.add(trans_idx)
    chapters.sort(key=lambda item: item[0])

    bodies = [md_to_html("\n".join(lines)) for _, _, _, lines in chapters]
    needed = collect_images(bodies)
    base = md_path.parent
    missing = sorted(s for s in needed if not (base / s).exists())
    for src in missing:
        warnings.append(f"Missing image; image tag will be removed: {src}")
    if missing:
        for i, body in enumerate(bodies):
            for src in missing:
                bodies[i] = re.sub(
                    r'<img[^>]+src="' + re.escape(src) + r'"[^>]*/?>',
                    "", bodies[i], flags=re.IGNORECASE
                )

    book = epub.EpubBook()
    book.set_identifier(
        "md2epub-" + re.sub(r"[^a-z0-9]+", "-", md_path.stem.lower()).strip("-")
    )
    book.set_title(title)
    book.set_language("vi")

    style = epub.EpubItem(
        uid="style",
        file_name="style/style.css",
        media_type="text/css",
        content=CSS.encode("utf-8"),
    )
    book.add_item(style)

    cover = epub.EpubHtml(title="Bìa", file_name="title.xhtml", lang="vi")
    if cover_img and cover_img.exists():
        mime = mimetypes.guess_type(cover_img.name)[0] or "image/png"
        ext = cover_img.suffix.lstrip(".").lower()
        img = epub.EpubImage(
            uid="cover-img",
            file_name=f"assets/cover.{ext}",
            media_type=mime,
            content=cover_img.read_bytes(),
        )
        book.add_item(img)
        cover_body = (
            f'<div class="cover"><img src="assets/cover.{ext}" alt="Bìa"/>'
            f'<h1>{html.escape(title)}</h1>'
        )
    else:
        cover_body = f'<div class="cover"><h1>{html.escape(title)}</h1>'
    cover_body += (
        f'<p class="sub">Bản tổng hợp {len(chapters)} chương — '
        f'{datetime.date.today().strftime("%d/%m/%Y")}</p></div>'
    )
    cover.content = cover_body
    cover.add_link(href="style/style.css", rel="stylesheet", type="text/css")
    book.add_item(cover)

    for i, src in enumerate(sorted(needed - set(missing))):
        p = base / src
        mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        book.add_item(epub.EpubImage(
            uid=f"img{i:03d}", file_name=src, media_type=mime,
            content=p.read_bytes()
        ))

    toc = []
    # One EPUB content document per translated chapter. The transIdx is the
    # stable filename/TOC identity, independent of rawIdx.
    for trans_idx, number, heading, lines, in chapters:
        fname = f"chapter_{trans_idx:03d}.html"
        ch = epub.EpubHtml(
            title=heading,
            file_name=fname,
            lang="vi",
            uid=f"chapter-{trans_idx:03d}",
        )
        body = md_to_html("\n".join(lines))
        for src in missing:
            body = re.sub(
                r'<img[^>]+src="' + re.escape(src) + r'"[^>]*/?>',
                "", body, flags=re.IGNORECASE
            )
        ch.content = body
        ch.add_link(href="style/style.css", rel="stylesheet", type="text/css")
        book.add_item(ch)
        toc.append(ch)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", cover, *toc]

    epub.write_epub(str(out_path), book)
    return 0, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Full.md -> Full.epub")
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--cover", type=Path, default=None)
    parser.add_argument("--state", type=Path, default=None,
                        help="Path to _vartemp.json for rawIdx/transIdx/title metadata")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    md_path = (args.input or base / "Full.md").resolve()
    out_path = (args.output or base / "Full.epub").resolve()
    title = args.title or base.name
    cover_img = args.cover.resolve() if args.cover else None
    state_path = args.state.resolve() if args.state else (md_path.parent / "_vartemp.json")

    if not md_path.exists():
        print(f"[ERROR] Input not found: {md_path}", file=sys.stderr)
        return 1

    rc, warnings = build_epub(md_path, out_path, title, cover_img, state_path)
    if rc:
        return rc

    print(f"[OK] Created {out_path}")
    print(f"     Size: {out_path.stat().st_size / 1024:.0f} KB")
    for w in warnings:
        print(f"     [WARNING] {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
