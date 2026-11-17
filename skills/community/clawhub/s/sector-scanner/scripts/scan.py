#!/usr/bin/env python3
"""
A股板块资金流向扫描器 — Skill 入口脚本

Usage:
    python scan.py --all                          # 扫描全部板块, 输出 JSON
    python scan.py --sectors semiconductor,ai_compute  # 扫描指定板块
    python scan.py --all --output csv --file result.csv  # 输出 CSV 文件
    python scan.py --self-test                    # 快速自检
    python scan.py --list-sectors                 # 列出可用板块

Output:
    JSON: 扫描结果以 JSON 格式输出到 stdout, 进度信息输出到 stderr
    CSV:  板块排名 CSV + 个股明细 CSV (若指定 --file 则写文件, 否则 stdout)
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

# Resolve config directory relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"


def progress_msg(current: int, total: int, message: str) -> None:
    """Print progress to stderr so it doesn't mix with JSON output on stdout."""
    pct = f"{current/total*100:.0f}%" if total else "0%"
    print(f"[{pct}] {message}", file=sys.stderr, flush=True)


def list_sectors(engine) -> None:
    """Print all available sector IDs and names."""
    for sector in engine.sectors:
        print(f"{sector.id}\t{sector.name}\t{len(sector.stocks)} stocks")


def output_json(results: list) -> None:
    """Output scan results as JSON to stdout."""
    data = {
        "scan_time": results[0].scanned_at.isoformat() if results else None,
        "source": results[0].source if results else "unknown",
        "total_sectors": len(results),
        "total_stocks": sum(r.total_count for r in results),
        "sectors": [r.to_dict() for r in results],
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


def output_csv(results: list, filepath: str | None = None) -> None:
    """Output scan results as CSV. If filepath given, writes ranking + detail files."""
    if filepath:
        ranking_path = Path(filepath)
        detail_path = ranking_path.with_suffix(".detail.csv")
    else:
        ranking_path = None
        detail_path = None

    # Ranking CSV
    ranking_buf = io.StringIO()
    writer = csv.writer(ranking_buf)
    writer.writerow(["排名", "板块", "均分", "热度", "红盘", "均涨跌", "资金流向"])
    for rank, r in enumerate(results, 1):
        writer.writerow([
            rank,
            r.name,
            f"{r.average_score:.1f}",
            r.heat_label,
            f"{r.red_count}/{r.total_count}",
            f"{r.avg_pct_chg:+.2f}%",
            r.flow_label,
        ])

    # Detail CSV
    detail_buf = io.StringIO()
    writer = csv.writer(detail_buf)
    writer.writerow(["板块", "排名", "代码", "名称", "价格", "涨跌幅", "评分", "资金流向", "量比", "评分明细"])
    for r in results:
        for rank, s in enumerate(r.stocks, 1):
            writer.writerow([
                r.name,
                rank,
                s.code,
                s.name,
                s.price,
                f"{s.pct_chg:+.2f}%",
                s.score,
                s.flow_label,
                s.volume_ratio,
                " | ".join(s.details),
            ])

    if ranking_path:
        ranking_path.write_text(ranking_buf.getvalue(), encoding="utf-8-sig")
        detail_path.write_text(detail_buf.getvalue(), encoding="utf-8-sig")
        print(f"Ranking CSV: {ranking_path}", file=sys.stderr)
        print(f"Detail CSV: {detail_path}", file=sys.stderr)
    else:
        print("=== Ranking ===")
        print(ranking_buf.getvalue(), end="")
        print("\n=== Detail ===")
        print(detail_buf.getvalue(), end="")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A股板块资金流向扫描器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="扫描全部板块 (默认)")
    group.add_argument("--sectors", type=str, help="指定板块ID, 逗号分隔 (如 semiconductor,ai_compute)")
    group.add_argument("--self-test", action="store_true", help="快速自检")
    group.add_argument("--list-sectors", action="store_true", help="列出可用板块")

    parser.add_argument("--output", choices=["json", "csv"], default="json", help="输出格式 (默认 json)")
    parser.add_argument("--file", type=str, help="CSV 输出文件路径 (仅 --output csv 时有效)")

    args = parser.parse_args()

    # Add scripts dir to sys.path so sibling modules can be imported
    sys.path.insert(0, str(SCRIPT_DIR))

    from scanner import ScanEngine

    engine = ScanEngine(SCRIPT_DIR.parent)

    if args.list_sectors:
        list_sectors(engine)
        return 0

    if args.self_test:
        print("Running self-test...", file=sys.stderr)
        results = engine.scan(progress_callback=progress_msg)
        stock_count = sum(len(r.stocks) for r in results)
        sources = ", ".join(sorted({r.source for r in results}))
        print(f"self-test ok: {len(results)} sectors, {stock_count} stocks, source={sources}", file=sys.stderr)
        if results:
            print("\nTop 5 sectors:", file=sys.stderr)
            for i, r in enumerate(results[:5], 1):
                print(f"  {i}. {r.name}  score={r.average_score:.1f}  flow={r.flow_label}  red={r.red_count}/{r.total_count}", file=sys.stderr)
        return 0

    # Determine which sectors to scan
    sector_ids = None
    if args.sectors:
        sector_ids = [s.strip() for s in args.sectors.split(",") if s.strip()]

    results = engine.scan(sector_ids=sector_ids, progress_callback=progress_msg)

    if not results:
        print("No results. Check sector IDs or TDX connectivity.", file=sys.stderr)
        return 1

    if args.output == "json":
        output_json(results)
    else:
        output_csv(results, args.file)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
