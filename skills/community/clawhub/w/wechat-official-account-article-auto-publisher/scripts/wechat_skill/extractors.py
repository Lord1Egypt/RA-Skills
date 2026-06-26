from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .markdown_tools import (
    extract_title_from_markdown,
    first_markdown_image,
    html_to_markdown_text,
    html_to_text,
    markdown_to_html,
    parse_frontmatter,
    trim_digest,
)
from .models import Article
from .utils import decode_escaped_unicode, normalize_whitespace


def is_url(value: str) -> bool:
    return bool(re.match(r"^https?://", (value or "").strip(), re.I))


def _load_markdown_file(path: Path) -> Article:
    md_text = decode_escaped_unicode(path.read_text(encoding="utf-8")).lstrip("\ufeff")
    frontmatter, body = parse_frontmatter(md_text)
    title = normalize_whitespace((frontmatter.get("title") or extract_title_from_markdown(body)).strip())[:64]
    source_url = normalize_whitespace(frontmatter.get("source_url") or "")
    html = markdown_to_html(body)
    digest = trim_digest(html_to_text(html))
    return Article(
        title=title or "未命名文章",
        markdown=body.strip(),
        html=html,
        digest=digest,
        source_url=source_url,
        author=normalize_whitespace(frontmatter.get("author") or ""),
        cover_hint=first_markdown_image(body),
    )


def _clean_article_html(node: BeautifulSoup, source_url: str) -> str:
    for tag in node.select("script,style,iframe,.ad,.ads,.advertisement,.comment,.qr_code_pc_outer,.rich_media_tool"):
        tag.decompose()

    for img in node.find_all("img"):
        source = (img.get("data-src") or img.get("src") or "").strip()
        if source:
            img["src"] = urljoin(source_url, source)

    for anchor in node.find_all("a"):
        href = (anchor.get("href") or "").strip()
        if href:
            anchor["href"] = urljoin(source_url, href)

    return str(node)


def _extract_weixin_article(soup: BeautifulSoup, url: str) -> Article:
    title_node = soup.select_one("#activity-name") or soup.find("h1") or soup.find("title")
    content_node = soup.select_one("#js_content") or soup.select_one(".rich_media_content")
    author_node = soup.select_one("#js_name") or soup.select_one(".rich_media_meta_nickname")

    if not content_node:
        raise RuntimeError("无法从 mp.weixin.qq.com 页面提取正文")

    html = _clean_article_html(content_node, url)
    markdown_body = html_to_markdown_text(html)
    title = normalize_whitespace(title_node.get_text(" ", strip=True) if title_node else "未命名文章")[:64]
    author = normalize_whitespace(author_node.get_text(" ", strip=True) if author_node else "")
    cover_hint = ""
    first_img = content_node.find("img")
    if first_img:
        cover_hint = (first_img.get("data-src") or first_img.get("src") or "").strip()

    return Article(
        title=title or "未命名文章",
        markdown=markdown_body,
        html=markdown_to_html(markdown_body),
        digest=trim_digest(html_to_text(html)),
        source_url=url,
        author=author,
        cover_hint=cover_hint,
    )


def _extract_generic_article(soup: BeautifulSoup, url: str) -> Article:
    title_node = soup.find("h1") or soup.find("title")
    body_node = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", class_=re.compile(r"content|article|post|entry", re.I))
        or soup.body
    )
    if not body_node:
        raise RuntimeError("无法从网页提取正文")

    html = _clean_article_html(body_node, url)
    markdown_body = html_to_markdown_text(html)
    title = normalize_whitespace(title_node.get_text(" ", strip=True) if title_node else "未命名文章")[:64]
    cover_hint = ""
    first_img = body_node.find("img")
    if first_img:
        cover_hint = (first_img.get("data-src") or first_img.get("src") or "").strip()

    return Article(
        title=title or "未命名文章",
        markdown=markdown_body,
        html=markdown_to_html(markdown_body),
        digest=trim_digest(html_to_text(html)),
        source_url=url,
        cover_hint=cover_hint,
    )


def extract_from_url(url: str, timeout: int = 30) -> Article:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    if "mp.weixin.qq.com" in url:
        return _extract_weixin_article(soup, url)
    return _extract_generic_article(soup, url)


def load_article(input_value: str, timeout: int = 30) -> Article:
    if is_url(input_value):
        return extract_from_url(input_value, timeout=timeout)

    path = Path(input_value).resolve()
    if not path.exists():
        raise RuntimeError(f"文件不存在: {path}")
    return _load_markdown_file(path)
