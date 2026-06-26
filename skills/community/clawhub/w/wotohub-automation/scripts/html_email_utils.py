#!/usr/bin/env python3
from __future__ import annotations
from typing import Optional

import html
import re

_ALLOWED_TAGS = {"p", "br", "strong", "em", "ul", "ol", "li", "a"}


def looks_like_html(value: str) -> bool:
    value = (value or "").strip()
    if not value:
        return False
    return bool(re.search(r"<(p|br|strong|em|ul|ol|li|a)(\\s|>)", value, flags=re.I))


def contains_cjk(value: str) -> bool:
    value = value or ""
    return bool(re.search(r"[\u4e00-\u9fff]", value))


def plain_text_to_html(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return "<p></p>"
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    html_parts = []
    for p in paragraphs:
        escaped = html.escape(p).replace("\n", "<br>")
        html_parts.append(f"<p>{escaped}</p>")
    return "\n".join(html_parts)


def html_to_plain_text(value: str) -> str:
    value = value or ""
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</p>\s*<p>", "\n\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def strip_unsafe_tags(value: str) -> str:
    value = value or ""
    value = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", value, flags=re.I | re.S)
    value = re.sub(r" on\w+=\"[^\"]*\"", "", value, flags=re.I)
    value = re.sub(r" on\w+='[^']*'", "", value, flags=re.I)
    return value


def normalize_html_body(value: str) -> str:
    value = strip_unsafe_tags(value or "")
    if not value.strip():
        return "<p></p>"
    if "<p" not in value and "<br" not in value and "<ul" not in value:
        return plain_text_to_html(value)
    return value.strip()


def validate_email_html(value: str) -> bool:
    value = (value or "").strip().lower()
    if not value:
        return False
    return any(f"<{tag}" in value for tag in _ALLOWED_TAGS)


def normalize_email_content(
    html_body: Optional[str]= None,
    plain_text_body: Optional[str]= None,
    body: Optional[str]= None,
) -> dict:
    raw_html = (html_body or "").strip()
    raw_plain = (plain_text_body or "").strip()
    raw_body = (body or "").strip()
    source_text = raw_plain or raw_body

    if raw_html:
        if looks_like_html(raw_html):
            final_html = normalize_html_body(raw_html)
        else:
            final_html = normalize_html_body(plain_text_to_html(raw_html))
    elif source_text:
        final_html = normalize_html_body(plain_text_to_html(source_text))
    else:
        final_html = "<p></p>"

    final_plain = html_to_plain_text(final_html).strip()
    return {
        "htmlBody": final_html,
        "plainTextBody": final_plain,
        "isHtmlSource": bool(raw_html and looks_like_html(raw_html)),
    }
