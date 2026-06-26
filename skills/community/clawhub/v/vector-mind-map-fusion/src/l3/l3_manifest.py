#!/usr/bin/env python3
"""
L3 Run Manifest — 跨层汇总报告
L3 每次运行后生成 manifest，记录本轮 + L1/L2 最近 cost tracker 数据。
写入 memory/_state/last_run_manifest.json
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from utils.cost_tracker import get_recent_records


STATE_DIR = Path(__file__).parent.parent.parent / "memory" / "_state"
MANIFEST_FILE = STATE_DIR / "last_run_manifest.json"

STATE_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_manifest(
    l3_stats: dict,
    infinitydb_nodes_before: int,
    infinitydb_nodes_after: int,
    l2_files_cleared: list[str],
    errors: Optional[list] = None,
) -> dict:
    """
    生成并写入 manifest。

    Args:
        l3_stats: L3 run() 返回的 stats dict
        infinitydb_nodes_before: InfinityDB 运行前的节点数
        infinitydb_nodes_after: InfinityDB 运行后的节点数
        l2_files_cleared: 本次清理的 L2 文件列表
        errors: 错误列表

    Returns:
        manifest dict
    """
    # 读取最近 L1/L2 cost tracker 记录
    l1_records = get_recent_records(layer="l1", limit=1)
    l2_records = get_recent_records(layer="l2", limit=1)

    manifest = {
        "version": 1,
        "run_at": now_iso(),
        "l3": {
            "chunks_in": l3_stats.get("chunks_in", 0),
            "neurons_written": l3_stats.get("neurons_written", 0),
            "schemas_written": l3_stats.get("schemas_written", 0),
            "relations_written": l3_stats.get("relations_written", 0),
            "ollama_calls": l3_stats.get("ollama_calls", 0),
            "tokens_approx": l3_stats.get("tokens_approx", 0),
            "duration_ms": l3_stats.get("duration_ms", 0),
            "infinitydb_nodes_before": infinitydb_nodes_before,
            "infinitydb_nodes_after": infinitydb_nodes_after,
            "infinitydb_nodes_delta": infinitydb_nodes_after - infinitydb_nodes_before,
            "l2_files_cleared": l2_files_cleared,
            "errors": errors or [],
        },
        "l1_cost": l1_records[0] if l1_records else None,
        "l2_cost": l2_records[0] if l2_records else None,
    }

    tmp_file = MANIFEST_FILE.with_suffix(".tmp.json")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    tmp_file.rename(MANIFEST_FILE)

    return manifest


def read_manifest() -> Optional[dict]:
    """读取上一次运行的 manifest"""
    if not MANIFEST_FILE.exists():
        return None
    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None
