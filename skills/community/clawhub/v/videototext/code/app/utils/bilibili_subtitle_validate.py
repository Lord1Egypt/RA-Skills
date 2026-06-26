"""B 站字幕与视频元数据一致性校验（启发式）。"""

from __future__ import annotations

import re
from typing import Any


def normalize_title_for_match(title: str) -> str:
    """保留汉字与数字，去掉空格与常见装饰，便于与字幕正文比对。"""
    t = (title or "").strip()
    t = re.sub(r"[\s\u3000]+", "", t)
    return re.sub(r"[^\u4e00-\u9fff0-9]", "", t)


def should_enforce_title_match(title: str, min_chars: int) -> bool:
    return len(normalize_title_for_match(title)) >= min_chars


def title_match_score(video_title: str, subtitle_plain_text: str) -> float:
    """用标题中相邻汉字二元组在字幕中的命中率衡量相关性，范围 [0,1]。
    标题过短（有效汉字少于阈值）时返回 1.0，表示不做此项过滤。
    """
    cjk = normalize_title_for_match(video_title)
    if len(cjk) < 6:
        return 1.0
    bigrams = [cjk[i : i + 2] for i in range(len(cjk) - 1)]
    if not bigrams:
        return 1.0
    text = subtitle_plain_text or ""
    hits = sum(1 for b in bigrams if b in text)
    return hits / len(bigrams)


def passes_duration_coverage(
    body: list[dict[str, Any]],
    duration_sec: float,
    min_duration_check: float,
    min_coverage_ratio: float,
    long_min_duration: float,
    min_body_lines_long: int,
) -> bool:
    """时长与条数启发式：防止半截、极短错轨。"""
    if not body:
        return False
    duration_sec = float(duration_sec or 0)
    last_to = float(body[-1].get("to") or 0)
    if duration_sec >= min_duration_check:
        if last_to < duration_sec * min_coverage_ratio:
            return False
    if duration_sec >= long_min_duration and len(body) < min_body_lines_long:
        return False
    return True
