#!/usr/bin/env python3
"""
L2 Checkpoint — 断点恢复
防止 L2 处理大量 chunks 时 crash，从 checkpoint 恢复而非从头重跑。
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


STATE_DIR = Path(__file__).parent.parent.parent / "memory" / "_state"
CHECKPOINT_FILE = STATE_DIR / "l2_checkpoint.json"
CHECKPOINT_INTERVAL = 500  # 每处理 N 条写一次 checkpoint


STATE_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_checkpoint() -> Optional[dict]:
    """加载 checkpoint（返回 None 如果不存在或版本不匹配）"""
    if not CHECKPOINT_FILE.exists():
        return None
    try:
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            cp = json.load(f)
        if cp.get("version") != 1:
            return None
        return cp
    except (json.JSONDecodeError, IOError):
        return None


def save_checkpoint(
    date_str: str,
    processed_ids: set[str],
    last_checkpoint_line: int = 0,
):
    """写入 checkpoint"""
    cp = {
        "version": 1,
        "last_run": now_iso(),
        "date_str": date_str,
        "processed_ids": sorted(processed_ids),  # sorted 便于调试
        "checkpoint_interval": CHECKPOINT_INTERVAL,
        "last_checkpoint_line": last_checkpoint_line,
    }
    tmp_file = CHECKPOINT_FILE.with_suffix(".tmp.json")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(cp, f, ensure_ascii=False)
    tmp_file.rename(CHECKPOINT_FILE)


def clear_checkpoint():
    """L2 成功完成后清除 checkpoint"""
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()
