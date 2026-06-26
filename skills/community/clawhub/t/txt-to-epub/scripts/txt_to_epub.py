#!/usr/bin/env python3
import argparse
import html
import os
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import chardet
from ebooklib import epub


DEFAULT_CSS = """
body {
  margin: 0 auto;
  max-width: 44em;
  padding: 1.2em;
  line-height: 1.72;
  font-family: "Noto Serif CJK SC", "Songti SC", serif;
}
h1 {
  margin: 0.8em 0 1em;
  line-height: 1.3;
  font-size: 1.45em;
}
p {
  text-indent: 2em;
  margin: 0.45em 0;
}
""".strip()


RE_CN_NOVEL = re.compile(
    r"^第[零〇一二两三四五六七八九十百千万\d]+[章节卷部篇回集](?:\s*|[：:、\.．\-—]\s*)(?:\S.*)?$"
)
RE_EN_CHAPTER = re.compile(
    r"^(?:chapter|part|section)\s+\d+[a-z]?(?:\s*[：:\.\-—]\s*.*)?$", re.IGNORECASE
)
RE_NUM_HEADING = re.compile(r"^\d+(?:\.\d+){0,3}\s+\S.*$")
RE_CN_LIST = re.compile(r"^[一二三四五六七八九十百千万]+、\S.*$")
RE_MD_HEADING = re.compile(r"^#{1,4}\s+\S.*$")


@dataclass
class Chapter:
    title: str
    content: str


def detect_encoding(raw: bytes) -> str:
    detected = chardet.detect(raw) or {}
    encoding = (detected.get("encoding") or "").strip()
    if encoding:
        return encoding
    return "utf-8"


def read_text(path: Path) -> Tuple[str, str]:
    raw = path.read_bytes()
    guess = detect_encoding(raw)
    candidates = [guess, "utf-8", "gb18030", "big5", "utf-16"]
    tried = set()
    for enc in candidates:
        if not enc or enc.lower() in tried:
            continue
        tried.add(enc.lower())
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8(replace)"


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u3000", " ")
    text = re.sub(r"\t+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def compact_spaces(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def is_blank(line: str) -> bool:
    return compact_spaces(line) == ""


def punctuation_ratio(text: str) -> float:
    if not text:
        return 0.0
    punct = re.findall(r"[\.,;:!?，。！？；：、()（）\[\]{}'\"《》<>]", text)
    return len(punct) / max(1, len(text))


def detect_pattern(title: str, split_mode: str) -> Optional[str]:
    checks: Sequence[Tuple[str, re.Pattern]] = [
        ("cn_novel", RE_CN_NOVEL),
        ("en_chapter", RE_EN_CHAPTER),
        ("num_heading", RE_NUM_HEADING),
        ("cn_list", RE_CN_LIST),
        ("md_heading", RE_MD_HEADING),
    ]
    allowed = {
        "auto": {"cn_novel", "en_chapter", "num_heading", "cn_list", "md_heading"},
        "novel": {"cn_novel", "en_chapter"},
        "tutorial": {"num_heading", "en_chapter", "cn_list", "md_heading"},
        "length": set(),
    }[split_mode]
    for name, pattern in checks:
        if name in allowed and pattern.match(title):
            return name
    return None


def heading_score(title: str, prev_blank: bool, next_blank: bool, split_mode: str) -> int:
    pattern_name = detect_pattern(title, split_mode)
    if not pattern_name:
        return -1

    base = {
        "cn_novel": 5,
        "en_chapter": 5,
        "num_heading": 4,
        "cn_list": 3,
        "md_heading": 4,
    }[pattern_name]

    if len(title) <= 30:
        base += 1
    if prev_blank:
        base += 1
    if next_blank:
        base += 1
    if re.search(r"[。！？；;!?]$", title):
        base -= 2
    if punctuation_ratio(title) > 0.35:
        base -= 2
    return base


def choose_preface_title(language: str) -> str:
    if language.lower().startswith("zh"):
        return "前言"
    return "Preface"


def clean_heading_title(title: str) -> str:
    t = title.strip()
    t = re.sub(r"^#{1,4}\s+", "", t)
    t = re.sub(r"^第[零〇一二两三四五六七八九十百千万\d]+[章节卷部篇回集]\s*[：:、\.．\-—]?\s*", "", t)
    t = re.sub(r"^(?:chapter|part|section)\s+\d+[a-z]?\s*[：:\.\-—]?\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\d+(?:\.\d+){0,3}\s+", "", t)
    t = re.sub(r"^[一二三四五六七八九十百千万]+、\s*", "", t)
    t = compact_spaces(t)
    return t or title.strip()


def find_headings(lines: List[str], split_mode: str) -> List[Tuple[int, str, int]]:
    headings: List[Tuple[int, str, int]] = []
    threshold = 5
    for idx, raw in enumerate(lines):
        title = compact_spaces(raw)
        if not title:
            continue
        prev_blank = idx == 0 or is_blank(lines[idx - 1])
        next_blank = idx == len(lines) - 1 or is_blank(lines[idx + 1])
        score = heading_score(title, prev_blank, next_blank, split_mode)
        if score >= threshold:
            if headings:
                prev_idx, prev_title, _ = headings[-1]
                between = "".join(lines[prev_idx + 1 : idx]).strip()
                if prev_title == title and len(between) < 20:
                    continue
            headings.append((idx, title, score))
    return headings


def text_to_paragraphs(text: str) -> List[str]:
    blocks = re.split(r"\n\s*\n", text)
    return [compact_spaces(block) for block in blocks if compact_spaces(block)]


def fallback_chunk_chapters(text: str, chunk_chars: int) -> List[Chapter]:
    paragraphs = text_to_paragraphs(text)
    if not paragraphs:
        return [Chapter(title="Part 1", content="")]
    chapters: List[Chapter] = []
    buf: List[str] = []
    length = 0
    part = 1
    for para in paragraphs:
        addition = len(para) + (2 if buf else 0)
        if buf and length + addition > chunk_chars:
            chapters.append(Chapter(title=f"Part {part}", content="\n\n".join(buf)))
            part += 1
            buf = [para]
            length = len(para)
        else:
            buf.append(para)
            length += addition
    if buf:
        chapters.append(Chapter(title=f"Part {part}", content="\n\n".join(buf)))
    return chapters


def merge_short_chapters(chapters: List[Chapter], min_chars: int) -> List[Chapter]:
    if len(chapters) <= 1 or min_chars <= 0:
        return chapters
    merged: List[Chapter] = []
    for chapter in chapters:
        content_len = len(re.sub(r"\s+", "", chapter.content))
        if merged and content_len < min_chars:
            merged[-1].content = (
                merged[-1].content
                + "\n\n"
                + chapter.title
                + "\n\n"
                + chapter.content
            ).strip()
        else:
            merged.append(chapter)
    return merged


def split_into_chapters(
    text: str,
    split_mode: str,
    title_style: str,
    language: str,
    min_chapter_chars: int,
    chunk_chars: int,
) -> Tuple[List[Chapter], str]:
    if split_mode == "length":
        return fallback_chunk_chapters(text, chunk_chars), "length"

    lines = text.split("\n")
    headings = find_headings(lines, split_mode)
    if not headings:
        return fallback_chunk_chapters(text, chunk_chars), "length_fallback"

    chapters: List[Chapter] = []
    first_idx = headings[0][0]
    preface_text = "\n".join(lines[:first_idx]).strip()
    if preface_text:
        chapters.append(Chapter(title=choose_preface_title(language), content=preface_text))

    for i, (start_idx, raw_title, _) in enumerate(headings):
        end_idx = headings[i + 1][0] if i + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start_idx + 1 : end_idx]).strip()
        final_title = raw_title if title_style == "full" else clean_heading_title(raw_title)
        chapters.append(Chapter(title=final_title, content=body))

    chapters = merge_short_chapters(chapters, min_chapter_chars)
    return chapters, "rule"


def chapter_to_xhtml(chapter: Chapter) -> str:
    paragraphs = text_to_paragraphs(chapter.content)
    escaped_title = html.escape(chapter.title)
    if not paragraphs:
        body = "<p></p>"
    else:
        body = "\n".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)
    return (
        "<html xmlns=\"http://www.w3.org/1999/xhtml\">"
        "<head><meta charset=\"utf-8\"/></head>"
        f"<body><h1>{escaped_title}</h1>{body}</body></html>"
    )


def build_epub(
    chapters: List[Chapter],
    output_path: Path,
    title: str,
    author: str,
    language: str,
) -> None:
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language(language)
    if author:
        book.add_author(author)

    css_item = epub.EpubItem(
        uid="style_main",
        file_name="style/main.css",
        media_type="text/css",
        content=DEFAULT_CSS,
    )
    book.add_item(css_item)

    chapter_items: List[epub.EpubHtml] = []
    for idx, chapter in enumerate(chapters, start=1):
        file_name = f"chap_{idx:04d}.xhtml"
        item = epub.EpubHtml(title=chapter.title, file_name=file_name, lang=language)
        item.content = chapter_to_xhtml(chapter)
        item.add_item(css_item)
        book.add_item(item)
        chapter_items.append(item)

    book.toc = tuple(chapter_items)
    book.spine = ["nav", *chapter_items]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(output_path), book, {})


def infer_default_title(input_path: Path) -> str:
    return input_path.stem or "Untitled"


def resolve_output_path(input_path: Path, output: Optional[str]) -> Path:
    if output:
        return Path(output).expanduser().resolve()
    return input_path.with_suffix(".epub")


def print_preview(chapters: List[Chapter], max_items: int = 8) -> None:
    for idx, chapter in enumerate(chapters[:max_items], start=1):
        print(f"  {idx:>2}. {chapter.title}")
    if len(chapters) > max_items:
        print(f"  ... ({len(chapters) - max_items} more chapters)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert TXT files to EPUB with rule-based chapter splitting.")
    parser.add_argument("--input", required=True, help="Path to input TXT file")
    parser.add_argument("--output", help="Path to output EPUB file")
    parser.add_argument("--title", help="Book title")
    parser.add_argument("--author", default="", help="Book author")
    parser.add_argument("--language", default="zh-CN", help="Book language, e.g. zh-CN/en")
    parser.add_argument(
        "--split-mode",
        default="auto",
        choices=["auto", "novel", "tutorial", "length"],
        help="Chapter splitting mode",
    )
    parser.add_argument(
        "--title-style",
        default="full",
        choices=["full", "clean"],
        help="Use full title or strip numbering prefix",
    )
    parser.add_argument("--min-chapter-chars", type=int, default=300, help="Merge chapter if body is shorter than this")
    parser.add_argument("--chunk-chars", type=int, default=8000, help="Fallback chunk size for length split")
    parser.add_argument("--verbose", action="store_true", help="Print split details")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = resolve_output_path(input_path, args.output)
    raw_text, detected_encoding = read_text(input_path)
    text = normalize_text(raw_text)
    if not text:
        raise ValueError("Input text is empty after normalization")

    final_title = args.title or infer_default_title(input_path)
    chapters, split_method = split_into_chapters(
        text=text,
        split_mode=args.split_mode,
        title_style=args.title_style,
        language=args.language,
        min_chapter_chars=max(0, args.min_chapter_chars),
        chunk_chars=max(1000, args.chunk_chars),
    )

    build_epub(
        chapters=chapters,
        output_path=output_path,
        title=final_title,
        author=args.author,
        language=args.language,
    )

    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Title: {final_title}")
    print(f"Author: {args.author or '-'}")
    print(f"Language: {args.language}")
    print(f"Detected Encoding: {detected_encoding}")
    print(f"Split Mode: {args.split_mode}")
    print(f"Split Method Used: {split_method}")
    print(f"Title Style: {args.title_style}")
    print(f"Chapter Count: {len(chapters)}")
    print("Chapter Preview:")
    print_preview(chapters)

    if args.verbose:
        size = os.path.getsize(output_path)
        print(f"Output Size: {size} bytes")


if __name__ == "__main__":
    main()
