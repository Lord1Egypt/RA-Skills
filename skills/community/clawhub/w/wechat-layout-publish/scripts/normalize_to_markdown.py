#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urljoin


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


def fetch_url(url: str) -> Tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        content_type = resp.headers.get("Content-Type", "")
        return body.decode(charset, errors="replace"), content_type


def read_source(args: argparse.Namespace) -> Tuple[str, str, Optional[str]]:
    if args.url:
        text, content_type = fetch_url(args.url)
        source_type = "html" if "html" in content_type.lower() else "text"
        return text, source_type, args.url
    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
        suffix = Path(args.input).suffix.lower()
        if suffix in {".md", ".markdown"}:
            return text, "markdown", None
        if suffix in {".html", ".htm"}:
            return text, "html", None
        return text, "auto", None
    return sys.stdin.read(), "auto", None


def extract_title(raw_html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.I | re.S)
    if match:
        return clean_text(match.group(1))
    match = re.search(r"<h1[^>]*>(.*?)</h1>", raw_html, re.I | re.S)
    if match:
        return clean_text(match.group(1))
    return ""


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def looks_like_markdown(text: str) -> bool:
    if re.search(r"^\s{0,3}#{1,6}\s+\S+", text, re.M):
        return True
    if re.search(r"^\s*([-*+]|\d+\.)\s+\S+", text, re.M):
        return True
    if "```" in text:
        return True
    return False


def normalize_markdown_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    out = []
    blank = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank += 1
            if blank <= 1:
                out.append("")
            continue
        blank = 0
        out.append(line)
    return "\n".join(out).strip() + "\n"


def convert_html_to_markdown(raw_html: str, base_url: Optional[str]) -> Tuple[str, str]:
    title = extract_title(raw_html)
    html_body = raw_html
    article_match = re.search(r"<article\b[^>]*>(.*?)</article>", raw_html, re.I | re.S)
    if article_match:
        html_body = article_match.group(1)
    else:
        main_match = re.search(r"<main\b[^>]*>(.*?)</main>", raw_html, re.I | re.S)
        if main_match:
            html_body = main_match.group(1)
        else:
            body_match = re.search(r"<body\b[^>]*>(.*?)</body>", raw_html, re.I | re.S)
            if body_match:
                html_body = body_match.group(1)

    html_body = re.sub(r"<!--.*?-->", "", html_body, flags=re.S)
    html_body = re.sub(r"<(script|style|noscript|svg|canvas)[^>]*>.*?</\1>", "", html_body, flags=re.I | re.S)
    html_body = re.sub(r"<(nav|footer|header|aside|form)[^>]*>.*?</\1>", "", html_body, flags=re.I | re.S)

    code_blocks = []

    def stash_code(match: re.Match) -> str:
        lang = clean_text(match.group(1))
        code = clean_text(match.group(2))
        token = f"@@CODEBLOCK_{len(code_blocks)}@@"
        block = f"```{lang}\n{code}\n```" if lang else f"```\n{code}\n```"
        code_blocks.append(block)
        return token

    def stash_plain_pre(match: re.Match) -> str:
        code = clean_text(match.group(1))
        token = f"@@CODEBLOCK_{len(code_blocks)}@@"
        code_blocks.append(f"```\n{code}\n```")
        return token

    html_body = re.sub(
        r"<pre[^>]*>\s*<code(?:[^>]*class=[\"'][^\"']*language-([^\"']+)[^\"']*[\"'])?[^>]*>(.*?)</code>\s*</pre>",
        stash_code,
        html_body,
        flags=re.I | re.S,
    )
    html_body = re.sub(
        r"<pre[^>]*>(.*?)</pre>",
        stash_plain_pre,
        html_body,
        flags=re.I | re.S,
    )

    def replace_image(match: re.Match) -> str:
        attrs = match.group(1)
        src_match = re.search(r'src=["\']([^"\']+)["\']', attrs, re.I)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', attrs, re.I)
        if not src_match:
            return ""
        src = src_match.group(1).strip()
        if base_url:
            src = urljoin(base_url, src)
        alt = clean_text(alt_match.group(1)) if alt_match else ""
        return f"\n![{alt}]({src})\n"

    html_body = re.sub(r"<img\b([^>]*?)\/?>", replace_image, html_body, flags=re.I | re.S)

    def replace_link(match: re.Match) -> str:
        attrs = match.group(1)
        inner = clean_text(match.group(2))
        href_match = re.search(r'href=["\']([^"\']+)["\']', attrs, re.I)
        if not href_match:
            return inner
        href = href_match.group(1).strip()
        if base_url:
            href = urljoin(base_url, href)
        return f"[{inner}]({href})" if inner else href

    html_body = re.sub(r"<a\b([^>]*)>(.*?)</a>", replace_link, html_body, flags=re.I | re.S)

    for level in range(6, 0, -1):
        pattern = rf"<h{level}[^>]*>(.*?)</h{level}>"
        html_body = re.sub(
            pattern,
            lambda m, level=level: f"\n{'#' * level} {clean_text(m.group(1))}\n",
            html_body,
            flags=re.I | re.S,
        )

    html_body = re.sub(r"<blockquote[^>]*>(.*?)</blockquote>", lambda m: blockquote_to_markdown(m.group(1)), html_body, flags=re.I | re.S)
    html_body = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: f"- {clean_text(m.group(1))}\n", html_body, flags=re.I | re.S)
    html_body = re.sub(r"</?(ul|ol)[^>]*>", "\n", html_body, flags=re.I)
    html_body = re.sub(r"<hr[^>]*\/?>", "\n---\n", html_body, flags=re.I)
    html_body = re.sub(r"<br\s*\/?>", "\n", html_body, flags=re.I)
    html_body = re.sub(r"</?(p|div|section|figure|figcaption|main|article)[^>]*>", "\n\n", html_body, flags=re.I)
    html_body = re.sub(r"</?(span|strong|b|em|i|u|small|mark)[^>]*>", "", html_body, flags=re.I)
    html_body = re.sub(r"<table[^>]*>(.*?)</table>", lambda m: table_to_markdown(m.group(1)), html_body, flags=re.I | re.S)
    html_body = re.sub(r"<[^>]+>", " ", html_body)
    html_body = html.unescape(html_body)
    html_body = re.sub(r"[ \t]+\n", "\n", html_body)
    html_body = re.sub(r"\n{3,}", "\n\n", html_body)

    for idx, block in enumerate(code_blocks):
        html_body = html_body.replace(f"@@CODEBLOCK_{idx}@@", f"\n{block}\n")

    markdown = normalize_markdown_text(html_body)
    return markdown, title


def table_to_markdown(table_html: str) -> str:
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, flags=re.I | re.S)
    parsed_rows = []
    for row in rows:
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, flags=re.I | re.S)
        if cells:
            parsed_rows.append([clean_text(cell) for cell in cells])
    if len(parsed_rows) < 2:
        return "\n"
    header = parsed_rows[0]
    divider = ["---"] * len(header)
    body = parsed_rows[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(divider) + " |",
    ]
    for row in body:
        padded = row + [""] * (len(header) - len(row))
        lines.append("| " + " | ".join(padded[: len(header)]) + " |")
    return "\n" + "\n".join(lines) + "\n"


def blockquote_to_markdown(inner_html: str) -> str:
    text = clean_text(inner_html)
    if not text:
        return "\n"
    lines = [f"> {line.strip()}" for line in re.split(r"\n+", text) if line.strip()]
    return "\n" + "\n".join(lines) + "\n"


def normalize_plain_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    out = []
    paragraph = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(" ".join(line.strip() for line in paragraph if line.strip()))
            out.append("")
            paragraph = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            continue
        if re.match(r"^(\d+[\.\)]|[-*•])\s+", stripped):
            flush_paragraph()
            item = re.sub(r"^(\d+[\.\)]|[-*•])\s+", "", stripped)
            out.append(f"- {item}")
            continue
        if len(stripped) <= 30 and not re.search(r"[。！？.!?]$", stripped):
            flush_paragraph()
            out.append(f"## {stripped}")
            out.append("")
            continue
        paragraph.append(stripped)

    flush_paragraph()
    return normalize_markdown_text("\n".join(out))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize pasted text, HTML files, or article URLs into clean Markdown."
    )
    parser.add_argument("--input", help="Input file path. Reads stdin when omitted.")
    parser.add_argument("--url", help="Source article URL.")
    parser.add_argument("--output", help="Write Markdown output to this file.")
    parser.add_argument("--meta-output", help="Optional JSON metadata output path.")
    args = parser.parse_args()

    text, source_type, source_url = read_source(args)
    title = ""

    if source_type == "markdown" or (source_type == "auto" and looks_like_markdown(text)):
        markdown = normalize_markdown_text(text)
    elif source_type == "html" or (source_type == "auto" and re.search(r"<[a-zA-Z][^>]*>", text)):
        markdown, title = convert_html_to_markdown(text, source_url)
    else:
        markdown = normalize_plain_text(text)

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)

    if args.meta_output:
        Path(args.meta_output).write_text(
            json.dumps(
                {
                    "title": title,
                    "sourceUrl": source_url,
                    "detectedType": source_type,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
