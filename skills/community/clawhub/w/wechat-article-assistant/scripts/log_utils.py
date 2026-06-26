#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging helpers for the WeChat Article Assistant skill."""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler

from config import get_paths
from utils import ensure_dir


LOGGER_NAMESPACE = "wechat_article_assistant"
_CONFIGURED = False


def _env_first(*names: str) -> str:
    for name in names:
        value = os.environ.get(name, "")
        if value:
            return value
    return ""


def _env_bool(default: bool, *names: str) -> bool:
    value = _env_first(*names)
    if not value:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def configure_logging(
    level: str | None = None,
    console: bool | None = None,
    file_logging: bool | None = None,
    *,
    force: bool = False,
) -> logging.Logger:
    global _CONFIGURED

    if _CONFIGURED and not force:
        return logging.getLogger(LOGGER_NAMESPACE)

    logger = logging.getLogger(LOGGER_NAMESPACE)
    logger.handlers.clear()
    logger.propagate = False

    resolved_level = (
        level
        or _env_first("WECHAT_ARTICLE_ASSISTANT_LOG_LEVEL", "WECHAT_ARTICLE_OPENCLAW_LOG_LEVEL")
        or "WARNING"
    ).upper()
    resolved_console = (
        _env_bool(False, "WECHAT_ARTICLE_ASSISTANT_LOG_CONSOLE", "WECHAT_ARTICLE_OPENCLAW_LOG_CONSOLE")
        if console is None
        else console
    )
    resolved_file = (
        _env_bool(False, "WECHAT_ARTICLE_ASSISTANT_LOG_TO_FILE", "WECHAT_ARTICLE_OPENCLAW_LOG_TO_FILE")
        if file_logging is None
        else file_logging
    )

    numeric_level = getattr(logging, resolved_level, logging.WARNING)
    logger.setLevel(numeric_level)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if resolved_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if resolved_file:
        paths = get_paths()
        ensure_dir(paths.logs_dir)
        file_handler = RotatingFileHandler(
            paths.logs_dir / "wechat_article_assistant.log",
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    _CONFIGURED = True
    logger.debug(
        "logging configured level=%s console=%s file=%s",
        resolved_level,
        resolved_console,
        resolved_file,
    )
    return logger


def get_logger(name: str) -> logging.Logger:
    if not _CONFIGURED:
        configure_logging()
    suffix = name.rsplit(".", 1)[-1]
    return logging.getLogger(f"{LOGGER_NAMESPACE}.{suffix}")
