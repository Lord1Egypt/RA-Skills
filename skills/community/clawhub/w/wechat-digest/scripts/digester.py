#!/usr/bin/env python3
"""WeChat Digest — extract, summarize, and synthesize WeChat articles."""
import re
import json
import sys
from pathlib import Path
from typing import Optional
from html.parser import HTMLParser

# ── Noise patterns for WeChat articles ──────────────────────────────
NOISE_PATTERNS = {
    "follow_us": re.compile(r'(点击.*关注|关注.*公众号|长按.*二维码|follow\s+us|scan\s+QR)', re.I),
    "bottom_ad": re.compile(r'(阅读原文|在看|点赞|分享|转发|好看|喜欢作者)', re.I),
    "related": re.compile(r'(推荐阅读|往期|相关文章|延伸阅读)', re.I),
    "menu": re.compile(r'(设为星标|置顶|进入公众号|底部菜单)', re.I),
    "footer": re.compile(r'(版权声明|本文.*转载|未经.*许可|不得转载)', re.I),
}


class SimpleHTMLParser(HTMLParser):
    """Minimal HTML extractor."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False
        if tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
            self.text_parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.text_parts.append(data)

    def get_text(self):
        return "".join(self.text_parts)


def extract_text(html: str) -> str:
    """Extract clean text from HTML."""
    parser = SimpleHTMLParser()
    parser.feed(html)
    return parser.get_text()


def denoise(text: str) -> str:
    """Remove noise patterns from WeChat article text."""
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            clean_lines.append(line)
            continue

        # Check noise patterns
        skip = False
        for label, pat in NOISE_PATTERNS.items():
            if pat.search(stripped):
                skip = True
                break

        if not skip:
            clean_lines.append(stripped)

    return "\n".join(clean_lines)


def extract_structure(text: str) -> dict:
    """Extract structured information from article text."""
    structure = {
        "title": "",
        "paragraphs": [],
        "key_data": [],
        "quotes": [],
        "outline": [],
    }
    lines = text.splitlines()

    # Title: first non-empty line (likely H1 or header)
    for line in lines:
        line = line.strip()
        if line and len(line) < 200:
            structure["title"] = line
            break

    # Extract quotes (lines in quotation marks or with 「」)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Quotes
        if (line.startswith('"') and line.endswith('"')) or \
           (line.startswith('「') and line.endswith('」')) or \
           re.match(r'^[—–-]\s', line):
            structure["quotes"].append(line)

        # Key data (numbers with units or percentages)
        if re.search(r'\d+[%％]|\d+\.\d+\s*(万|亿|元|美元|人|个|家)', line):
            structure["key_data"].append(line)

        # Outline (short lines that could be section headers)
        outline_pattern = re.compile(r'^[一二三四五六七八九十\d]+[、.．]\s*\S+')
        if outline_pattern.match(line) or (len(line) < 30 and not line.endswith(('。', '？', '！', '，')) and not line.startswith(('"', '「', '—'))):
            structure["outline"].append(line)

    return structure


def one_liner(article: dict) -> str:
    """Generate extreme brevity summary."""
    title = article.get("title", "Untitled")
    paragraphs = article.get("paragraphs", [])
    key_data = article.get("key_data", [])

    parts = [title]
    if key_data:
        parts.append(f"Key: {'; '.join(kd[:60] for kd in key_data[:2])}")
    return " | ".join(parts)


def three_paragraph_summary(article: dict) -> str:
    """Generate 3-paragraph summary."""
    title = article.get("title", "Untitled")
    data = article.get("key_data", [])
    quotes = article.get("quotes", [])

    para1 = f"**{title}** — "
    para1 += f"Presents {len(data)} key data points and {len(quotes)} notable quotes."
    para2 = "Key findings include: "
    para2 += "; ".join(d[:80] for d in data[:3]) if data else "No specific data found."
    para3 = "Quotes: " + "; ".join(q[:80] for q in quotes[:2]) if quotes else "No notable quotes extracted."

    return f"{para1}\n\n{para2}\n\n{para3}"


def knowledge_card(article: dict) -> dict:
    """Generate structured knowledge card."""
    return {
        "title": article.get("title", ""),
        "type": "knowledge_card",
        "key_data": article.get("key_data", [])[:5],
        "quotes": article.get("quotes", [])[:3],
        "outline": article.get("outline", []),
        "paragraph_count": len(article.get("paragraphs", [])),
    }


def synthesize(articles: list) -> dict:
    """Cross-article synthesis."""
    all_data = []
    all_quotes = []
    for a in articles:
        all_data.extend(a.get("key_data", []))
        all_quotes.extend(a.get("quotes", []))

    return {
        "source_count": len(articles),
        "common_themes": list(set(d[:40] for d in all_data)),
        "key_quotes": list(set(q[:60] for q in all_quotes))[:5],
        "synthesis": f"Synthesized {len(articles)} articles: {len(all_data)} data points, {len(all_quotes)} quotes."
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="WeChat Digest — article extraction and summarization")
    parser.add_argument("--url", "-u", help="WeChat article URL")
    parser.add_argument("--urls", "-U", nargs="+", help="Multiple URLs for synthesis")
    parser.add_argument("--file", "-f", help="File with URLs (one per line)")
    parser.add_argument("--format", choices=["one-line", "3-paragraph", "knowledge-card", "markdown"], default="3-paragraph")
    parser.add_argument("--synthesize", action="store_true", help="Cross-article synthesis")
    parser.add_argument("--outdir", "-o", help="Output directory")
    args = parser.parse_args()

    if args.file:
        urls = Path(args.file).read_text().splitlines()
    elif args.urls:
        urls = args.urls
    elif args.url:
        urls = [args.url]
    else:
        # Self-test mode
        sample_text = """# AI 时代的写作革命

这是一个关于 AI 写作工具的深度分析文章。文章指出，2024 年中国 AI 写作市场规模达到 50 亿元。

「AI 不会取代作家，但会取代不会用 AI 的作家。」

目前已有超过 1000 万用户在使用各类 AI 写作工具。行业预测显示，2025 年市场规模将突破 80 亿元。

## 核心观点

AI 写作工具正在改变内容生产方式。从辅助到主导，技术演进速度超出预期。
"""
        urls = []
        test_articles = []
        for text in [sample_text]:
            clean = denoise(text)
            articles = extract_structure(clean)
            test_articles.append(articles)

        if test_articles:
            print(f"[wechat-digest] Self-test: {len(test_articles)} article(s)\n")
            for article in test_articles:
                if args.format == "one-line":
                    print(one_liner(article))
                elif args.format == "knowledge-card":
                    print(json.dumps(knowledge_card(article), ensure_ascii=False, indent=2))
                else:
                    print(three_paragraph_summary(article))
                    print("---")
        return 0

    # Process URLs (placeholder — in production would use web_fetch)
    print("[wechat-digest] URL processing requires network access.")
    print(f"Will process {len(urls)} URL(s).")
    print(f"Format: {args.format}")
    if args.synthesize:
        print("Cross-article synthesis requested.")

    return 0


if __name__ == "__main__":
    main()
