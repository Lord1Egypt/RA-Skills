#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Library module for Safebooru DAPI fetching (no external CLI).

This file is imported by other code if needed; the main CLI entry is safebooru.py.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Iterable, List, Optional
from urllib.parse import quote, urlsplit, urlunsplit

import requests

POST_DAPI = "https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1"
TAG_DAPI = "https://safebooru.org/index.php?page=dapi&s=tag&q=index"  # XML

DEFAULT_UA = "Mozilla/5.0 (OpenClaw safebooru-fetcher; +https://clawhub.ai)"

SORT_MAP = {
    "id_desc": "sort:id:desc",
    "id_asc": "sort:id:asc",
    "score_desc": "sort:score:desc",
    "score_asc": "sort:score:asc",
    "random": "sort:random",
}


@dataclass
class Post:
    id: int
    file_url: str
    preview_url: Optional[str] = None
    sample_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    rating: Optional[str] = None
    score: Optional[int] = None


def _sleep_backoff(attempt: int) -> None:
    time.sleep(0.6 * (2 ** attempt))


def http_get(url: str, *, timeout: int = 30, retries: int = 3) -> requests.Response:
    last_err: Optional[Exception] = None
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent": DEFAULT_UA})
            r.raise_for_status()
            return r
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                _sleep_backoff(attempt)
            else:
                raise
    raise last_err  # pragma: no cover


def build_tags(
    tags: str,
    *,
    sort: str = "id_desc",
    min_score: Optional[int] = None,
    exclude: Iterable[str] = (),
) -> str:
    parts: List[str] = []
    base = tags.strip()
    if base:
        parts.extend(base.split())

    for t in exclude:
        t = t.strip()
        if not t:
            continue
        parts.append(t if t.startswith("-") else "-" + t)

    if min_score is not None:
        parts.append(f"score:>={int(min_score)}")

    parts.append(SORT_MAP.get(sort, SORT_MAP["id_desc"]))
    return " ".join(parts)


def fetch_posts(tags_expr: str, *, limit: int = 10, page: int = 1) -> List[Post]:
    pid = max(0, int(page) - 1)
    url = f"{POST_DAPI}&tags={quote(tags_expr)}&limit={int(limit)}&pid={pid}"
    r = http_get(url)
    if not r.text.strip():
        return []
    data = r.json()
    out: List[Post] = []
    for item in data:
        fu = item.get("file_url")
        pid_ = item.get("id")
        if not fu or pid_ is None:
            continue
        out.append(
            Post(
                id=int(pid_),
                file_url=str(fu),
                preview_url=item.get("preview_url"),
                sample_url=item.get("sample_url"),
                rating=item.get("rating"),
                score=item.get("score"),
            )
        )
    return out


def download_file(url: str, out_path: str, *, timeout: int = 60, retries: int = 3) -> None:
    def candidates(u: str) -> List[str]:
        parts = urlsplit(u)
        p = parts.path
        alts = [u]
        if p.lower().endswith(".jpg"):
            alts.append(urlunsplit((parts.scheme, parts.netloc, p[:-4] + ".png", parts.query, parts.fragment)))
        elif p.lower().endswith(".png"):
            alts.append(urlunsplit((parts.scheme, parts.netloc, p[:-4] + ".jpg", parts.query, parts.fragment)))
        return alts

    last_err: Optional[str] = None
    for cand in candidates(url):
        for attempt in range(retries):
            try:
                r = requests.get(cand, timeout=timeout, headers={"User-Agent": DEFAULT_UA})
                if r.status_code == 404:
                    last_err = "HTTP 404"
                    break
                if r.status_code != 200:
                    last_err = f"HTTP {r.status_code}"
                    _sleep_backoff(attempt)
                    continue
                with open(out_path, "wb") as f:
                    f.write(r.content)
                return
            except Exception as e:
                last_err = str(e)
                if attempt < retries - 1:
                    _sleep_backoff(attempt)
                else:
                    break

    raise RuntimeError(last_err or "download failed")


def suggest_tags(pattern: str, *, limit: int = 50) -> List[tuple[str, int]]:
    p = pattern.strip()
    if not p:
        return []
    if "%" not in p:
        p = f"%{p}%"

    url = f"{TAG_DAPI}&name_pattern={quote(p)}&limit={int(limit)}"
    r = http_get(url)
    xml = r.text

    names = re.findall(r'name="([^"]+)"', xml)
    counts = re.findall(r'count="(\d+)"', xml)

    out: List[tuple[str, int]] = []
    for i in range(min(len(names), len(counts))):
        out.append((names[i], int(counts[i])))

    out.sort(key=lambda x: x[1], reverse=True)
    return out


def safe_slug(text: str, max_len: int = 50) -> str:
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^a-zA-Z0-9_\-]+", "_", text)
    return text[:max_len].strip("_") or "safebooru"


def download_posts(
    tags: str,
    *,
    limit: int = 5,
    page: int = 1,
    sort: str = "id_desc",
    min_score: Optional[int] = None,
    exclude: Iterable[str] = (),
    out_dir: str = "./downloads",
) -> List[str]:
    tags_expr = build_tags(tags, sort=sort, min_score=min_score, exclude=exclude)
    posts = fetch_posts(tags_expr, limit=limit, page=page)
    if not posts:
        return []

    os.makedirs(out_dir, exist_ok=True)
    slug = safe_slug(tags)

    paths: List[str] = []
    for post in posts[:limit]:
        ext = os.path.splitext(urlsplit(post.file_url).path)[1] or ".jpg"
        filename = f"{slug}_{post.id}{ext}"
        path = os.path.join(out_dir, filename)
        download_file(post.file_url, path)
        paths.append(os.path.abspath(path))
        time.sleep(0.4)

    return paths
