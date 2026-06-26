#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从指定信息源拉取特朗普相关新闻摘要，供 AI 翻译成中文并编辑后推送。
使用 RSS 与 Federal Register 官方 API，无需 API Key。
"""
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path
from html import unescape
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# 本脚本所在目录，用于调用 fetch_truth_social.py
SCRIPT_DIR = Path(__file__).resolve().parent
FETCH_TRUTH_SOCIAL = SCRIPT_DIR / "fetch_truth_social.py"

# 中国时间当日 0 点（用于“今日”范围，可选）
CHINA_TZ = timedelta(hours=8)

# 确凿信息源：RSS 与 API（均可直接访问）
SOURCES = [
    {
        "id": "whitehouse",
        "name": "The White House (Briefing Room)",
        "type": "rss",
        "url": "https://www.whitehouse.gov/briefing-room/feed/",
        "note": "政策类权威出处",
    },
    {
        "id": "scotusblog",
        "name": "SCOTUSblog",
        "type": "rss",
        "url": "https://www.scotusblog.com/feed/",
        "note": "最高法院与特朗普相关诉讼解读",
    },
    {
        "id": "reuters",
        "name": "Reuters (路透社)",
        "type": "rss",
        "url": "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best",
        "note": "政治类，中立快速",
    },
    {
        "id": "ap",
        "name": "Associated Press (美联社)",
        "type": "rss",
        "url": "https://feeds.apnews.com/rss/ap_top_news",
        "note": "Top News，事实采集",
    },
    {
        "id": "afp",
        "name": "AFP (法新社)",
        "type": "rss",
        "url": "https://www.afp.com/en/actus/afp_communique/all/feed",
        "note": "国际视角",
    },
]

# 用于筛选“特朗普相关”的关键词（标题或摘要）
TRUMP_KEYWORDS = re.compile(
    r"\btrump\b|\bDonald\s+Trump\b|white\s+house\s+briefing|executive\s+order|scotus|supreme\s+court",
    re.I,
)


def fetch_url(url, timeout=25):
    """GET 请求，返回 UTF-8 字符串。"""
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw-TrumpNews/1.0; RSS reader)",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
    )
    with urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_rss_or_atom(raw_xml, source_name):
    """解析 RSS 2.0 或 Atom，返回 [(title, link, pub_date, summary), ...]。"""
    root = ET.fromstring(raw_xml)
    items = []
    # RSS: channel > item
    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        date_el = item.find("pubDate") or item.find("dc:date")
        desc_el = item.find("description") or item.find("content:encoded")
        title = (title_el.text or "").strip() if title_el is not None else ""
        link = (link_el.text or "").strip() if link_el is not None else ""
        pub_date = (date_el.text or "").strip() if date_el is not None else ""
        summary = (desc_el.text or "").strip() if desc_el is not None else ""
        if title or link:
            items.append((title, link, pub_date, summary))
    # Atom: feed > entry
    if not items:
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title_el = entry.find("{http://www.w3.org/2005/Atom}title")
            link_el = entry.find("{http://www.w3.org/2005/Atom}link[@href]")
            updated_el = entry.find("{http://www.w3.org/2005/Atom}updated") or entry.find("{http://www.w3.org/2005/Atom}published")
            summary_el = entry.find("{http://www.w3.org/2005/Atom}summary") or entry.find("{http://www.w3.org/2005/Atom}content")
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = (link_el.get("href") or "").strip() if link_el is not None else ""
            pub_date = (updated_el.text or "").strip() if updated_el is not None else ""
            summary = (summary_el.text or "").strip() if summary_el is not None else ""
            if title or link:
                items.append((title, link, pub_date, summary))
    return items


def fetch_federal_register(limit=15):
    """拉取 Federal Register 中特朗普相关总统文件（含行政命令）。"""
    today = (datetime.now(timezone.utc) + CHINA_TZ).date()
    start = (today - timedelta(days=14)).strftime("%m/%d/%Y")
    end = (today + timedelta(days=1)).strftime("%m/%d/%Y")
    params = [
        "conditions[president]=donald-trump",
        "conditions[type][]=PRESDOCU",
        "conditions[presidential_document_type]=executive_order",
        f"conditions[signing_date][gte]={start}",
        f"conditions[signing_date][lte]={end}",
        "per_page=" + str(limit),
        "order=newest",
    ]
    url = "https://www.federalregister.gov/api/v1/documents.json?" + "&".join(params)
    try:
        raw = fetch_url(url)
        data = json.loads(raw)
    except (URLError, HTTPError, json.JSONDecodeError):
        return []
    out = []
    for doc in data.get("results", [])[:limit]:
        title = doc.get("title", "")
        doc_num = doc.get("document_number", "")
        signing = doc.get("signing_date", "")
        pdf = doc.get("pdf_url", "")
        html = doc.get("html_url", "")
        link = pdf or html or ""
        out.append((title or "Executive Order", link, signing, f"Document {doc_num}"))
    return out


def strip_html(s, max_len=400):
    """简单去标签并截断。"""
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = unescape(s)
    s = " ".join(s.split())
    return s[:max_len] + ("..." if len(s) > max_len else "")


def _fetch_truth_social_block():
    """若已安装 truthbrush 且配置了 Truth Social 凭证，拉取 Truth Social 块并返回文本；否则返回 None。"""
    if not FETCH_TRUTH_SOCIAL.is_file():
        return None
    try:
        r = subprocess.run(
            [sys.executable, str(FETCH_TRUTH_SOCIAL)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(SCRIPT_DIR.parent),
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass
    return None


def main():
    today_str = (datetime.now(timezone.utc) + CHINA_TZ).strftime("%Y-%m-%d")
    lines = [
        f"# Trump-related news & documents (sources snapshot) · {today_str}",
        "",
        "Below are items from the listed authoritative and wire sources. Use this to translate into Chinese, edit, and push to the user.",
        "",
    ]

    # Truth Social（可选：需 pip install truthbrush 与 TRUTHSOCIAL_* 环境变量）
    truth_block = _fetch_truth_social_block()
    if truth_block:
        lines.append(truth_block)
        lines.append("")

    # Federal Register（行政命令）
    lines.append("## Federal Register (Executive Orders & Presidential Documents)")
    lines.append("")
    try:
        fr_items = fetch_federal_register()
        if fr_items:
            for title, link, date_str, note in fr_items:
                lines.append(f"- **{title}**")
                if date_str:
                    lines.append(f"  Date: {date_str}")
                if note:
                    lines.append(f"  {note}")
                if link:
                    lines.append(f"  Link: {link}")
                lines.append("")
        else:
            lines.append("(No matching documents in the last 14 days.)")
            lines.append("")
    except Exception as e:
        lines.append(f"(Federal Register fetch error: {e})")
        lines.append("")

    # RSS 源
    for src in SOURCES:
        if src["type"] != "rss":
            continue
        lines.append(f"## {src['name']}")
        if src.get("note"):
            lines.append(f"*{src['note']}*")
        lines.append("")
        try:
            raw = fetch_url(src["url"])
            items = parse_rss_or_atom(raw, src["name"])
            kept = []
            for title, link, pub_date, summary in items[:25]:
                text = f"{title} {summary}"
                if not TRUMP_KEYWORDS.search(text) and "white house" not in text.lower() and "briefing" not in text.lower():
                    if src["id"] in ("whitehouse", "scotusblog"):
                        kept.append((title, link, pub_date, summary))
                    else:
                        continue
                else:
                    kept.append((title, link, pub_date, summary))
            if not kept and src["id"] in ("whitehouse", "scotusblog"):
                kept = [(t, l, d, s) for t, l, d, s in items[:10]]
            for title, link, pub_date, summary in kept[:12]:
                lines.append(f"- **{title}**")
                if pub_date:
                    lines.append(f"  Date: {pub_date}")
                if summary:
                    lines.append(f"  Summary: {strip_html(summary)}")
                if link:
                    lines.append(f"  Link: {link}")
                lines.append("")
            if not kept:
                lines.append("(No Trump-related items in recent feed.)")
                lines.append("")
        except Exception as e:
            lines.append(f"(Fetch error: {e})")
            lines.append("")

    lines.append("---")
    sources_note = "Sources: Truth Social (if configured), White House Briefing Room, Federal Register, SCOTUSblog, Reuters, AP, AFP. "
    lines.append(sources_note + "Translate the above into Chinese, edit for clarity, and push to the user.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
