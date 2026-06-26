#!/usr/bin/env python3
"""性能基准测试 - 测量各脚本的执行时间和内存占用

用法:
    benchmark <正文目录>
"""

import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def benchmark_script(name: str, args: list) -> dict:
    """测量单个脚本的执行时间"""
    script = SCRIPTS_DIR / f"{name}.py"
    if not script.exists():
        return None

    start = time.perf_counter()
    result = subprocess.run(
        [sys.executable, str(script)] + args,
        capture_output=True, text=True, timeout=120
    )
    elapsed = time.perf_counter() - start

    return {
        "script": name,
        "time_ms": round(elapsed * 1000, 1),
        "exit_code": result.returncode,
        "output_lines": len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0,
    }


def list_chapters(directory: str):
    return list(Path(directory).glob("*.md"))


def main():
    if len(sys.argv) < 2:
        print("📖 性能基准测试")
        print("用法: benchmark <正文目录>")
        sys.exit(0)

    novel_dir = sys.argv[1]
    if not Path(novel_dir).is_dir():
        print(f"❌ 目录不存在: {novel_dir}")
        sys.exit(1)

    # 统计章节数和字数
    chapters = list(Path(novel_dir).glob("*.md"))
    total_chars = 0
    for c in chapters:
        total_chars += len(c.read_text(encoding="utf-8"))

    print(f"📊 基准测试: {len(chapters)} 章, {total_chars:,} 字\n")

    scripts = [
        ("consistency_check", [novel_dir]),
        ("repetition_check", [novel_dir]),
        ("dialogue_tag_check", [novel_dir]),
        ("chapter_hook_check", [novel_dir]),
        ("chapter_title_check", [novel_dir]),
        ("opening_score", [novel_dir]),
        ("paragraph_check", [novel_dir]),
        ("rhythm_check", [novel_dir]),
        ("foreshadow_scan", [novel_dir]),
        ("tension_forecast", [novel_dir]),
    ]

    results = []
    for name, args in scripts:
        print(f"  ⏳ {name}...", end=" ", flush=True)
        r = benchmark_script(name, args)
        if r:
            results.append(r)
            status = f"{r['time_ms']}ms"
            if r["exit_code"] != 0:
                status += " ❌"
            print(status)
        else:
            print("跳过")

    # 结果表格
    print(f"\n{'='*60}")
    print(f"{'脚本':<25} {'时间':>10} {'输出行':>8}")
    print(f"{'-'*60}")

    total_time = 0
    for r in sorted(results, key=lambda x: x["time_ms"], reverse=True):
        print(f"{r['script']:<25} {r['time_ms']:>8}ms {r['output_lines']:>8}")
        total_time += r["time_ms"]

    print(f"{'-'*60}")
    print(f"{'总计':<25} {total_time:>8}ms")
    print(f"\n💡 首次运行会触发 jieba 分词加载，后续会快很多")

    # 并行模式对比
    print(f"\n{'='*60}")
    print("🔄 并行模式测试...")
    parallel_script = SCRIPTS_DIR / "run_parallel.py"
    if parallel_script.exists():
        start = time.perf_counter()
        result = subprocess.run(
            [sys.executable, str(parallel_script), novel_dir, "--workers", "4"],
            capture_output=True, text=True, timeout=120
        )
        parallel_time = round((time.perf_counter() - start) * 1000)
        speedup = round(total_time / max(parallel_time, 1), 1)
        print(f"  串行: {total_time}ms")
        print(f"  并行(4线程): {parallel_time}ms")
        print(f"  加速比: {speedup}x")


if __name__ == "__main__":
    main()
