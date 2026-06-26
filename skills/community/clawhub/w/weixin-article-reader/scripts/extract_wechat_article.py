#!/usr/bin/env python3
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser


BLOCK_TAGS = {
    "address",
    "article",
    "blockquote",
    "br",
    "dd",
    "div",
    "dl",
    "dt",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "td",
    "th",
    "tr",
    "ul",
}


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if "mp.weixin.qq.com" not in parsed.netloc:
        raise ValueError("not a mp.weixin.qq.com url")
    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query.setdefault("scene", ["1"])
    new_query = urllib.parse.urlencode(query, doseq=True)
    return urllib.parse.urlunparse(
        (parsed.scheme or "https", parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment)
    )


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://mp.weixin.qq.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


class WeixinHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_chunks = []
        self.author_chunks = []
        self.publish_chunks = []
        self.content_chunks = []
        self.fallback_title_chunks = []
        self.fallback_author_chunks = []
        self.fallback_content_chunks = []

        self._stack = []
        self._ignore_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        element_id = attrs_dict.get("id", "")
        classes = set(attrs_dict.get("class", "").split())
        markers = set()

        if self._is_active("content") and tag in {"script", "style", "iframe"}:
            self._ignore_depth += 1

        if element_id == "activity-name":
            markers.add("title")
        elif "rich_media_title" in classes and not self.title_chunks:
            markers.add("fallback_title")

        if element_id == "js_name":
            markers.add("author")
        elif "rich_media_meta_text" in classes and not self.author_chunks:
            markers.add("fallback_author")

        if element_id in {"publish_time", "post-date", "js_publish_time"}:
            markers.add("publish")

        if element_id == "js_content":
            markers.add("content")
        elif "rich_media_content" in classes and not self.content_chunks:
            markers.add("fallback_content")

        self._stack.append(markers)

        if self._content_target_active() and self._ignore_depth == 0 and tag in BLOCK_TAGS:
            self._active_content_chunks().append("\n")

    def handle_endtag(self, tag):
        if self._content_target_active() and self._ignore_depth == 0 and tag in BLOCK_TAGS:
            self._active_content_chunks().append("\n")

        if self._ignore_depth > 0 and tag in {"script", "style", "iframe"}:
            self._ignore_depth -= 1

        if self._stack:
            self._stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        text = html.unescape(text)
        if self._is_active("title"):
            self.title_chunks.append(text)
        elif self._is_active("fallback_title"):
            self.fallback_title_chunks.append(text)
        if self._is_active("author"):
            self.author_chunks.append(text)
        elif self._is_active("fallback_author"):
            self.fallback_author_chunks.append(text)
        if self._is_active("publish"):
            self.publish_chunks.append(text)
        if self._content_target_active() and self._ignore_depth == 0:
            self._active_content_chunks().append(text)

    def _is_active(self, marker: str) -> bool:
        return any(marker in entry for entry in self._stack)

    def _content_target_active(self) -> bool:
        return self._is_active("content") or (not self.content_chunks and self._is_active("fallback_content"))

    def _active_content_chunks(self):
        if self._is_active("content"):
            return self.content_chunks
        return self.fallback_content_chunks


def collapse_lines(text: str) -> str:
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def first_nonempty(*values: str) -> str:
    for value in values:
        value = value.strip()
        if value:
            return value
    return ""


def parse_publish_date(html_text: str, publish_text: str) -> str:
    publish_text = publish_text.strip()
    if publish_text:
        date_match = re.search(r"\d{4}-\d{1,2}-\d{1,2}", publish_text)
        if date_match:
            return date_match.group(0)
        return publish_text

    for pattern in [
        r"""createTime\s*=\s*['"](\d{4}-\d{1,2}-\d{1,2})(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?['"]""",
        r"""["']createTime["']\s*:\s*["'](\d{4}-\d{1,2}-\d{1,2})(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?["']""",
        r"""["']publish_time["']\s*:\s*["'](\d{4}-\d{1,2}-\d{1,2})["']""",
        r"""var\s+publish_time\s*=\s*['"](\d{4}-\d{1,2}-\d{1,2})['"]""",
    ]:
        match = re.search(pattern, html_text, re.I)
        if match:
            return match.group(1)

    for pattern in [
        r"""oriCreateTime\s*=\s*['"]?(\d{10})['"]?""",
        r"""createTime\s*=\s*['"]?(\d{10})['"]?""",
        r"""\bct\s*=\s*['"]?(\d{10})['"]?""",
        r"""["']publish_time["']\s*:\s*["']?(\d{10})["']?""",
        r"""var\s+publish_time\s*=\s*['"](\d{10})['"]""",
    ]:
        match = re.search(pattern, html_text, re.I)
        if match:
            timestamp = int(match.group(1))
            shanghai_tz = timezone(timedelta(hours=8))
            return datetime.fromtimestamp(timestamp, tz=shanghai_tz).strftime("%Y-%m-%d")

    return ""


def extract_article(html_text: str, source_url: str) -> dict:
    parser = WeixinHTMLParser()
    parser.feed(html_text)

    title = collapse_lines(" ".join(parser.title_chunks or parser.fallback_title_chunks))
    author = collapse_lines(" ".join(parser.author_chunks or parser.fallback_author_chunks))
    publish_date = collapse_lines(" ".join(parser.publish_chunks))
    content = collapse_lines("".join(parser.content_chunks or parser.fallback_content_chunks))

    title = first_nonempty(title)
    author = first_nonempty(author)
    publish_date = parse_publish_date(html_text, publish_date)
    content = first_nonempty(content)

    return {
        "ok": bool(content),
        "source_url": source_url,
        "title": title,
        "author": author,
        "publish_date": publish_date,
        "content": content,
    }


def main():
    if len(sys.argv) != 2:
        print(json.dumps({"ok": False, "error": "usage: extract_wechat_article.py <url>"}, ensure_ascii=False))
        sys.exit(2)

    try:
        source_url = normalize_url(sys.argv[1])
        html_text = fetch_html(source_url)
        result = extract_article(html_text, source_url)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
