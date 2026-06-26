#!/usr/bin/env python3
"""
HTML to Text Converter — stdin으로 받은 HTML을 읽기 좋은 텍스트로 변환

사용법:
    curl -sL "https://example.com" | python3 html_to_text.py
    cat page.html | python3 html_to_text.py --format markdown
    python3 html_to_text.py --file page.html --format plain
"""

import argparse
import re
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("beautifulsoup4가 필요합니다: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def html_to_markdown(html: str) -> str:
    """HTML을 Markdown 형식으로 변환한다."""
    soup = BeautifulSoup(html, "html.parser")

    # 불필요한 요소 제거
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe"]):
        tag.decompose()

    lines = []
    for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "a", "blockquote", "pre", "code"]):
        text = element.get_text(strip=True)
        if not text:
            continue

        tag = element.name

        if tag == "h1":
            lines.append(f"\n# {text}\n")
        elif tag == "h2":
            lines.append(f"\n## {text}\n")
        elif tag == "h3":
            lines.append(f"\n### {text}\n")
        elif tag in ("h4", "h5", "h6"):
            lines.append(f"\n#### {text}\n")
        elif tag == "p":
            lines.append(f"{text}\n")
        elif tag == "li":
            lines.append(f"- {text}")
        elif tag == "a":
            href = element.get("href", "")
            if href and not href.startswith("#") and element.parent.name not in ("h1", "h2", "h3", "h4", "p", "li"):
                lines.append(f"[{text}]({href})")
        elif tag == "blockquote":
            lines.append(f"> {text}\n")
        elif tag in ("pre", "code"):
            lines.append(f"```\n{text}\n```\n")

    result = "\n".join(lines)
    # 연속 빈 줄 정리
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def html_to_plain(html: str) -> str:
    """HTML을 순수 텍스트로 변환한다."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    # 연속 빈 줄 정리
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_metadata(html: str) -> dict:
    """HTML에서 메타데이터를 추출한다."""
    soup = BeautifulSoup(html, "html.parser")
    meta = {}

    title_tag = soup.find("title")
    if title_tag:
        meta["title"] = title_tag.get_text(strip=True)

    for tag in soup.find_all("meta"):
        name = tag.get("name", tag.get("property", ""))
        content = tag.get("content", "")
        if name and content:
            meta[name] = content

    return meta


def main():
    parser = argparse.ArgumentParser(description="HTML to Text Converter")
    parser.add_argument("--file", type=str, help="입력 HTML 파일 (없으면 stdin)")
    parser.add_argument("--format", type=str, default="markdown", choices=["markdown", "plain", "metadata"],
                        help="출력 형식 (기본: markdown)")
    parser.add_argument("--encoding", type=str, default="utf-8", help="입력 인코딩")

    args = parser.parse_args()

    # HTML 읽기
    if args.file:
        with open(args.file, "r", encoding=args.encoding) as f:
            html = f.read()
    else:
        html = sys.stdin.read()

    if not html.strip():
        print("입력 HTML이 비어있습니다.", file=sys.stderr)
        sys.exit(1)

    # 변환
    if args.format == "markdown":
        print(html_to_markdown(html))
    elif args.format == "plain":
        print(html_to_plain(html))
    elif args.format == "metadata":
        import json
        meta = extract_metadata(html)
        print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
