#!/usr/bin/env python3
"""
Cost Tracker — 每层 Ollama/处理消耗追踪
数据写入 memory/_state/cost_tracker.jsonl（append-only）
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


STATE_DIR = Path(__file__).parent.parent.parent / "memory" / "_state"
TRACKER_FILE = STATE_DIR / "cost_tracker.jsonl"

STATE_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_record(record: dict):
    """追加一条记录到 JSONL 文件"""
    with open(TRACKER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def track_layer(
    layer: str,
    ollama_calls: int = 0,
    tokens_approx: int = 0,
    chunks_in: int = 0,
    chunks_out: int = 0,
    duration_ms: int = 0,
    dedup_level1: int = 0,
    dedup_level2: int = 0,
    dedup_level3: int = 0,
    dedup_level4: int = 0,
    errors: Optional[list] = None,
    extra: Optional[dict] = None,
):
    """
    记录一层的 cost metrics。

    Args:
        layer: "l1" | "l2" | "l3"
        ollama_calls: Ollama encode_batch 调用次数
        tokens_approx: 估算 token 数（按平均每条 50 token 估算）
        chunks_in: 输入 chunks 数
        chunks_out: 输出 chunks 数
        duration_ms: 处理耗时（毫秒）
        dedup_level1: 第1级（content_hash）去重数
        dedup_level2: 第2级（simhash）去重数
        dedup_level3: 第3级（cosine）去重数
        dedup_level4: 第4级（HNSW）去重数
        errors: 错误列表
        extra: 额外字段
    """
    record = {
        "layer": layer,
        "timestamp": now_iso(),
        "ollama_calls": ollama_calls,
        "tokens_approx": tokens_approx,
        "chunks_in": chunks_in,
        "chunks_out": chunks_out,
        "dedup": {
            "level1_content_hash": dedup_level1,
            "level2_simhash": dedup_level2,
            "level3_cosine": dedup_level3,
            "level4_hnsw": dedup_level4,
        },
        "duration_ms": duration_ms,
        "errors": errors or [],
    }
    if extra:
        record["extra"] = extra

    _write_record(record)


def get_recent_records(layer: str = None, limit: int = 10) -> list[dict]:
    """
    读取最近的 cost 记录。

    Args:
        layer: 可选，只读某层
        limit: 返回条数
    """
    if not TRACKER_FILE.exists():
        return []

    records = []
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                if layer is None or record.get("layer") == layer:
                    records.append(record)

    return records[-limit:]


def get_layer_stats(layer: str, last_n: int = 10) -> dict:
    """
    汇总某层最近 N 条记录的平均 metrics。

    Args:
        layer: "l1" | "l2" | "l3"
        last_n: 统计最近几条

    Returns:
        dict 含平均值字段
    """
    records = get_recent_records(layer=layer, limit=last_n * 2)  # 多读点防不足
    records = [r for r in records if r.get("layer") == layer][-last_n:]

    if not records:
        return {}

    total_duration = sum(r.get("duration_ms", 0) for r in records)
    total_ollama = sum(r.get("ollama_calls", 0) for r in records)
    total_tokens = sum(r.get("tokens_approx", 0) for r in records)
    total_chunks_in = sum(r.get("chunks_in", 0) for r in records)
    total_chunks_out = sum(r.get("chunks_out", 0) for r in records)

    return {
        "layer": layer,
        "samples": len(records),
        "avg_duration_ms": round(total_duration / len(records), 1),
        "total_duration_ms": total_duration,
        "avg_ollama_calls": round(total_ollama / len(records), 1),
        "total_ollama_calls": total_ollama,
        "avg_tokens": round(total_tokens / len(records), 1),
        "total_chunks_in": total_chunks_in,
        "total_chunks_out": total_chunks_out,
        "avg_chunks_in": round(total_chunks_in / len(records), 1),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        for layer in ["l1", "l2", "l3"]:
            stats = get_layer_stats(layer, last_n=10)
            if stats:
                print(f"\n=== {layer.upper()} Stats (最近 {stats['samples']} 条) ===")
                print(f"  平均耗时: {stats['avg_duration_ms']} ms")
                print(f"  平均 Ollama 调用: {stats['avg_ollama_calls']} 次")
                print(f"  平均 Token: {stats['avg_tokens']}")
                print(f"  平均 chunks in: {stats['avg_chunks_in']}")
                print(f"  总 chunks in: {stats['total_chunks_in']}")
                print(f"  总 chunks out: {stats['total_chunks_out']}")
    else:
        # 打印最近记录
        records = get_recent_records(limit=5)
        for r in records:
            print(json.dumps(r, indent=2, ensure_ascii=False))
