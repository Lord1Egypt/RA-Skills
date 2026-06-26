#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

INDEPENDENT_NEWS = {
    'bbc.co.uk', 'bbc.com', 'news.bbc.co.uk', 'reuters.com', 'apnews.com', 'nytimes.com', 'wsj.com',
    'theguardian.com', 'abcnews.go.com', 'abcnews.com', 'cnn.com', 'bloomberg.com', 'ft.com',
    'thenationalnews.com', 'forbes.com', 'businessinsider.com', 'washingtonpost.com',
    'latimes.com', 'npr.org', 'aljazeera.com', 'economist.com'
}
PRESSWIRE_HINTS = {
    'prnewswire.com', 'businesswire.com', 'globenewswire.com', 'einnews.com', 'accesswire.com'
}
DIRECTORY_HINTS = {
    'crunchbase.com', 'pitchbook.com', 'zoominfo.com', 'companieshouse.gov.uk', 'opencorporates.com'
}
PRIMARY_TEXT_HINTS = {
    'about', 'contact', 'official website', 'company website', 'press release',
    'linkedin', 'instagram', 'facebook', 'youtube', 'x.com', 'twitter.com'
}
URL_PAT = re.compile(r'https?://[^\s|}>]+')
TEMPLATE_URL_PAT = re.compile(r'\|\s*url\s*=\s*([^|\n]+)', re.I)
TITLE_PAT = re.compile(r'\|\s*title\s*=\s*([^|\n]+)', re.I)
WORK_PAT = re.compile(r'\|\s*(?:work|website|publisher)\s*=\s*([^|\n]+)', re.I)
DATE_PAT = re.compile(r'\|\s*date\s*=\s*([^|\n]+)', re.I)
AUTHOR_PAT = re.compile(r'\|\s*author\s*=\s*([^|\n]+)', re.I)
ARCHIVE_URL_PAT = re.compile(r'\|\s*archive-url\s*=\s*([^|\n]+)', re.I)
REF_BLOCK_PAT = re.compile(r'<ref[^>]*>(.*?)</ref>|\{\{cite [^}]+\}\}', re.I | re.S)
RAW_REF_PAT = re.compile(r'<ref[^>]*>(.*?)</ref>', re.I | re.S)


def load_text(path: str | None) -> str:
    if not path or path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def normalize_host(url: str) -> str:
    return urlparse(url.strip()).netloc.lower().replace('www.', '')


def classify_url(url: str) -> tuple[str, str]:
    u = url.strip()
    if not u:
        return 'unknown', 'empty-url'
    lower = u.lower()
    host = normalize_host(u)
    if any(h in lower for h in DIRECTORY_HINTS):
        return 'directory/database', host
    if host in PRESSWIRE_HINTS:
        return 'press-release-wire', host
    if host in INDEPENDENT_NEWS:
        return 'independent-secondary', host
    if any(hint in lower for hint in PRIMARY_TEXT_HINTS):
        return 'primary-or-affiliated', host
    if host.endswith('.gov') or host.endswith('.gov.ae') or host.endswith('.edu'):
        return 'institutional-primary', host
    if host:
        return 'needs-review', host
    return 'unknown', 'unparsed'


def extract_refs(text: str) -> list[dict]:
    refs = []
    for idx, m in enumerate(REF_BLOCK_PAT.finditer(text), start=1):
        block = m.group(0)
        urls = URL_PAT.findall(block)
        urls += [u.strip() for u in TEMPLATE_URL_PAT.findall(block)]
        urls = list(dict.fromkeys(urls))
        title_m = TITLE_PAT.search(block)
        work_m = WORK_PAT.search(block)
        date_m = DATE_PAT.search(block)
        author_m = AUTHOR_PAT.search(block)
        archive_m = ARCHIVE_URL_PAT.search(block)
        title = title_m.group(1).strip() if title_m else ''
        work = work_m.group(1).strip() if work_m else ''
        date = date_m.group(1).strip() if date_m else ''
        author = author_m.group(1).strip() if author_m else ''
        archive = archive_m.group(1).strip() if archive_m else ''
        cls, detail = classify_url(urls[0]) if urls else ('no-url-found', 'manual-check')
        refs.append({
            'index': idx,
            'raw': block,
            'preview': block[:220].replace('\n', ' '),
            'title': title,
            'work': work,
            'date': date,
            'author': author,
            'archive_url': archive,
            'urls': urls,
            'classification': cls,
            'detail': detail,
        })
    return refs


def count_independent(refs: list[dict]) -> int:
    return sum(1 for r in refs if r['classification'] == 'independent-secondary')


def count_weak(refs: list[dict]) -> int:
    weak_classes = {'primary-or-affiliated', 'press-release-wire', 'directory/database'}
    return sum(1 for r in refs if r['classification'] in weak_classes)
