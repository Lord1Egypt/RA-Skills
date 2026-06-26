#!/usr/bin/env python3
"""
L1 Cron Entry Point
被 OpenClaw cron 触发，执行完整的 L1 pipeline。
触发时间：每天 00:30（Asia/Shanghai）

路径基于项目根目录（不依赖 /workspace/fusion）
"""

import os
import sys
import time as time_module
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT / "src" / "l1"))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
os.chdir(str(PROJECT_ROOT / "src" / "l1"))

from scan_sessions_incremental import ByteOffsetScanner
from l1_classifier import L1Classifier, save_to_l2a
from utils.cost_tracker import track_layer

RAW_CHUNKS_TMP_FILE = str(PROJECT_ROOT / "memory" / "_state" / "l1_raw_chunks_tmp.jsonl")


def main():
    t0 = time_module.time()

    print(f"[L1 Cron] 开始执行: {datetime.now().isoformat()}")

    scanner = ByteOffsetScanner()
    raw_chunks = scanner.scan()
    chunks_in = len(raw_chunks) if raw_chunks else 0

    stats = {
        "ollama_calls": 0,
        "tokens_approx": 0,
        "dedup_level1": 0,
        "dedup_level2": 0,
        "dedup_level3": 0,
    }
    chunks_out = 0

    if raw_chunks:
        classifier = L1Classifier()
        processed = classifier.process(raw_chunks)

        # 收集 cost tracker stats
        c_stats = classifier.get_stats()
        stats.update(c_stats)

        if processed:
            drop_count = sum(1 for c in processed if c.get("_dropped"))
            new_count = sum(1 for c in processed if c.get("dedup_level") == 0)
            chunks_out = new_count
            print(f"[L1 Cron] 处理完成: {new_count} 新增, {drop_count} 过滤")
            date_str = datetime.now().strftime("%Y-%m-%d")
            save_to_l2a(processed, date_str)
        else:
            print("[L1 Cron] 无有效 chunks")
    else:
        if os.path.exists(RAW_CHUNKS_TMP_FILE):
            print(f"[L1 Cron] 发现 stale tmp，尝试恢复...")
            classifier = L1Classifier()
            processed = classifier.process_from_tmp()

            c_stats = classifier.get_stats()
            stats.update(c_stats)

            if processed:
                drop_count = sum(1 for c in processed if c.get("_dropped"))
                new_count = sum(1 for c in processed if c.get("dedup_level") == 0)
                chunks_out = new_count
                print(f"[L1 Cron] 恢复完成: {new_count} 新增, {drop_count} 过滤")
                date_str = datetime.now().strftime("%Y-%m-%d")
                save_to_l2a(processed, date_str)
                if os.path.exists(RAW_CHUNKS_TMP_FILE):
                    os.remove(RAW_CHUNKS_TMP_FILE)
                    print(f"[L1 Cron] 清理 stale tmp")
            else:
                print(f"[L1 Cron] 恢复完成: 0 新增")
        else:
            print("[L1 Cron] 无新 chunks")

    duration_ms = int((time_module.time() - t0) * 1000)

    # 写 cost tracker
    track_layer(
        layer="l1",
        ollama_calls=stats["ollama_calls"],
        tokens_approx=stats["tokens_approx"],
        chunks_in=chunks_in,
        chunks_out=chunks_out,
        duration_ms=duration_ms,
        dedup_level1=stats["dedup_level1"],
        dedup_level2=stats["dedup_level2"],
        dedup_level3=stats["dedup_level3"],
    )

    print(f"[L1 Cron] 结束: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
