#!/usr/bin/env python3
"""
L2 Cron Entry Point
被 OpenClaw cron 触发，执行完整的 L2 pipeline。
触发时间：每天 00:30（Asia/Shanghai）

路径基于项目根目录（不依赖 /workspace/fusion）
"""

import sys
import os
import time as time_module
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT / "src" / "l2"))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
os.chdir(str(PROJECT_ROOT / "src" / "l2"))

from l2_daily import run
from utils.cost_tracker import track_layer


def main():
    t0 = time_module.time()
    print(f"[L2 Cron] 开始执行: {datetime.now().isoformat()}")

    stats = run()
    duration_ms = int((time_module.time() - t0) * 1000)

    if stats:
        track_layer(
            layer="l2",
            ollama_calls=stats.get("ollama_calls", 0),
            tokens_approx=stats.get("tokens_approx", 0),
            chunks_in=stats.get("chunks_in", 0),
            chunks_out=stats.get("chunks_out", 0),
            duration_ms=duration_ms,
            dedup_level1=stats.get("dedup_level1", 0),
            dedup_level2=stats.get("dedup_level2", 0),
            dedup_level3=stats.get("dedup_level3", 0),
            dedup_level4=stats.get("dedup_level4", 0),
        )
    else:
        # 无 chunks 也记录一条
        track_layer(
            layer="l2",
            chunks_in=0,
            chunks_out=0,
            duration_ms=duration_ms,
        )

    print(f"[L2 Cron] 结束: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
