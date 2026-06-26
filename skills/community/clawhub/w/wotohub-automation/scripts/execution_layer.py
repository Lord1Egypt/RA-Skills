#!/usr/bin/env python3
"""Execution helpers for WotoHub skill.

Policy:
- Host model handles semantic understanding/generation.
- This module handles deterministic execution helpers and rule-based fallbacks.
- Do not pretend to call an internal model from inside the skill.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Optional


# ============================================================================
# 1. API 重试机制
# ============================================================================

def retry_api_call(func: Callable, max_retries: int = 3, base_delay: float = 1.0) -> Any:
    """Retry API call with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)


# ============================================================================
# 2. 宿主 drafts / fallback helpers
# ============================================================================

def prepare_emails_from_host_drafts(host_drafts: Optional[list[dict]]= None) -> list[dict]:
    """Return host-provided drafts as-is for downstream normalization.

    The skill does not generate host drafts itself.
    """
    return [dict(x) for x in (host_drafts or []) if isinstance(x, dict)]


def analyze_reply_rule_based(
    reply: dict,
    brief: Optional[dict]= None,
    reply_model_analysis: Optional[dict]= None,
    allow_fallback: bool = True,
) -> dict:
    """Reply analysis helper.

    Host model output should be preferred by the caller when available.
    Rule-based heuristics remain available as explicit fallback only.
    """
    from reply_pipeline import ReplyPipeline
    return ReplyPipeline.analyze(
        reply,
        brief=brief,
        reply_model_analysis=reply_model_analysis,
        allow_fallback=allow_fallback,
    )


def generate_search_strategy_rule_based(product_summary: dict) -> dict:
    """Rule-based fallback for search strategy generation.

    Host model output should be preferred by the caller when available.
    """
    from search_strategy import generate_search_strategy
    return generate_search_strategy(product_summary)


# ============================================================================
# 5. URL 抓取超时
# ============================================================================

def fetch_url_with_timeout(url: str, timeout: int = 15) -> Optional[str]:
    """Fetch URL with timeout."""
    from url_fetcher import fetch_url_text

    try:
        import requests
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}")
        return None


# ============================================================================
# 6. 邮件规范化统一点
# ============================================================================

def normalize_email_once(email: dict) -> dict:
    """Normalize email once (single point)."""
    from html_email_utils import plain_text_to_html, normalize_html_body

    # 确保邮件已规范化
    if not email.get("htmlBody"):
        email["htmlBody"] = normalize_html_body(
            plain_text_to_html(email.get("body", ""))
        )
    if not email.get("plainTextBody"):
        email["plainTextBody"] = email.get("body", "")

    return email
