#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuration and path management."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/133.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class Paths:
    root: Path
    data_dir: Path
    db_path: Path
    downloads_dir: Path
    images_dir: Path
    articles_dir: Path
    reports_dir: Path
    qrcodes_dir: Path
    logs_dir: Path


def _default_root() -> Path:
    env = os.environ.get("WECHAT_ARTICLE_ASSISTANT_HOME") or os.environ.get("WECHAT_ARTICLE_OPENCLAW_HOME")
    if env:
        return Path(env).expanduser().resolve()
    # 默认使用 OpenClaw 媒体目录，方便统一管理二维码、下载内容和登录数据
    return Path.home().joinpath(".openclaw", "media", "wechat-article-assistant").resolve()


@lru_cache(maxsize=1)
def get_paths() -> Paths:
    root = _default_root()
    # 数据库直接放在 root 目录下，不额外创建 data 子目录
    data_dir = root
    downloads_dir = root / "downloads"
    return Paths(
        root=root,
        data_dir=data_dir,
        db_path=data_dir / "app.db",
        downloads_dir=downloads_dir,
        images_dir=downloads_dir / "images",
        articles_dir=downloads_dir / "articles",
        reports_dir=downloads_dir / "reports",
        qrcodes_dir=root / "qrcodes",
        logs_dir=root / "logs",
    )
