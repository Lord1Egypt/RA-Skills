#!/usr/bin/env python3
"""Skill context_level 自动标注模块

- 增量扫描：只处理没有 meta 文件的 skill
- 手动可改：source="user" 的记录 rescan 时绝不覆盖
- 纯 stdlib，无额外依赖
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("skill-to-http.context_meta")

from _paths import SKILL_META_DIR

# 命中任一信号 → full context（依赖运行时个人记忆/用户信息）
# 规则：只检测通用的文件名/语义信号，不写死任何用户名或邮箱
FULL_CONTEXT_SIGNALS = [
    # 明确引用记忆文件
    "MEMORY.md", "memory/", "USER.md", "TOOLS.md", "AGENTS.md",
    # 语义上依赖历史/上下文
    "今日日记", "每日记录", "历史记录", "上次对话", "记忆文件",
    "daily note", "memory file", "user profile", "personal context",
]


def detect_context_level(skill_md: str) -> tuple[str, str]:
    """扫描 SKILL.md 内容，返回 (level, reason)。
    level: 'full' | 'light'
    """
    md_lower = skill_md.lower()
    for signal in FULL_CONTEXT_SIGNALS:
        if signal.lower() in md_lower:
            return ("full", f"自动检测：命中信号「{signal}」")
    return ("light", "自动检测：SKILL.md 无记忆/用户信息依赖信号")


def load_context_meta(skill_name: str) -> dict | None:
    """读取 skill_meta/{name}.json，不存在返回 None。"""
    meta_path = SKILL_META_DIR / f"{skill_name}.json"
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        logger.warning(f"Failed to parse context meta for '{skill_name}', treating as missing")
        return None


def save_context_meta(skill_name: str, level: str, reason: str, source: str = "auto") -> None:
    """写入 skill_meta/{name}.json。"""
    SKILL_META_DIR.mkdir(parents=True, exist_ok=True)
    meta = {
        "context_level": level,
        "context_level_reason": reason,
        "context_level_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "context_level_source": source,
    }
    meta_path = SKILL_META_DIR / f"{skill_name}.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def scan_missing(skill_names: list[str], skill_md_map: dict[str, str]) -> int:
    """增量扫描：只处理没有 meta 文件的 skill，返回本次扫描数量。

    规则：
    - meta 文件不存在 → 自动检测并写入 (source="auto")
    - meta 文件存在且 source="user" → 跳过，绝不覆盖
    - meta 文件存在且 source="auto" → 跳过（不重复扫描）
    """
    scanned = 0
    for name in skill_names:
        existing = load_context_meta(name)
        if existing is not None:
            # 已有 meta，跳过（无论 source 是什么）
            continue

        skill_md = skill_md_map.get(name, "")
        if not skill_md:
            logger.debug(f"Skip context scan for '{name}': no SKILL.md content")
            continue

        level, reason = detect_context_level(skill_md)
        save_context_meta(name, level, reason, source="auto")
        logger.info(f"Context level auto-detected for '{name}': {level} — {reason}")
        scanned += 1

    return scanned


def update_context_level(skill_name: str, level: str) -> None:
    """用户手动修改 context_level，source 标为 'user'。
    此函数的 source 固定为 "user"，不可通过参数覆盖。
    """
    if level not in ("light", "full"):
        raise ValueError(f"Invalid context_level: {level!r}, must be 'light' or 'full'")
    reason = "手动设置" if level == "full" else "用户标记为 light"
    save_context_meta(skill_name, level, reason, source="user")
    logger.info(f"Context level manually set for '{skill_name}': {level}")