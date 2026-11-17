# -*- coding: utf-8 -*-
"""
路径与全局配置。

所有运行时数据都落在用户目录下的 WorkBuddy 记忆区：
  ~/.workbuddy/memory/            -> 原有的「每日日志」（YYYY-MM-DD.md）+ MEMORY.md
  ~/.workbuddy/memory/zwjh_store/ -> 本技能新增的索引库（知识图谱 + 向量索引 + 配置）

设计原则：
  - 纯标准库，零外部依赖，冷启动快、不拖累电脑。
  - 不创建任何可执行/脚本类文件（.ps1/.sh/.bat 等），全部用 Python 驱动。
  - 不要求任何 API Key；联网功能（如百度网盘）均为可插拔的「可选适配器」。
"""

from __future__ import annotations

import json
import os
from pathlib import Path

# ── 核心路径 ──────────────────────────────────────────────────────────────
WORKBUDDY_DIR = Path(os.path.expanduser("~")) / ".workbuddy"
MEMORY_DIR = WORKBUDDY_DIR / "memory"
ZWJH_DIR = MEMORY_DIR / "zwjh_store"          # 本技能专属索引目录
DB_PATH = ZWJH_DIR / "zwjh.db"                 # SQLite：记忆/图谱/向量索引
CONFIG_PATH = ZWJH_DIR / "config.json"         # 用户配置（硬件档位、备份目标等）
INSTALLED_VERSION_PATH = ZWJH_DIR / "installed_version.json"  # 更新校验缓存

# 其他 skill 可共享的「记忆底座」公共接口目录（可插拔基础设施）
SHARED_INDEX_DIR = ZWJH_DIR / "shared"

# 实体类型白名单（可插拔：其他 skill 也能注册新类型）
ENTITY_TYPES = ["person", "project", "task", "event", "document", "concept", "org", "custom"]

# 去重 / 冲突判定阈值
NEAR_DUP_JACCARD = 0.82     # token 集合重合度高于此值视为近似重复
STALE_DAYS = 90             # 超过该天数无访问的记忆视为「陈旧」

# 默认备份保留份数
BACKUP_KEEP = 7


def ensure_dirs() -> None:
    """确保运行时目录存在（首次运行时调用）。"""
    for d in (MEMORY_DIR, ZWJH_DIR, SHARED_INDEX_DIR):
        try:
            d.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass


def load_config() -> dict:
    ensure_dirs()
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_config(cfg: dict) -> None:
    ensure_dirs()
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def today_str() -> str:
    from datetime import date
    return date.today().strftime("%Y-%m-%d")


def daily_log_path(day: str | None = None) -> Path:
    """返回某天的每日日志路径；默认今天。"""
    if day is None:
        day = today_str()
    return MEMORY_DIR / f"{day}.md"
