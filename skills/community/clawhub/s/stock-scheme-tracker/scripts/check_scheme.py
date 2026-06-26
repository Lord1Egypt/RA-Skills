#!/usr/bin/env python3
"""
Check stock strategies in the scheme tracking file.

The file path is determined by:
  1. --path argument
  2. STOCK_SCHEME_PATH environment variable
  3. Default: ~/Documents/stock/scheme.md

Two modes:
1. Parse mode: Extract all tracked stocks and their conditions as JSON
   Usage: python3 check_scheme.py --parse [--path /path/to/scheme.md]

2. Report mode: Generate markdown report from JSON with latest market data
   Usage: echo '{"stocks":[...]}' | python3 check_scheme.py --report

The JSON format for report mode:
{
  "stocks": [
    {
      "code": "688111",
      "name": "金山办公",
      "status": "观察中",
      "conditions": [
        {"name": "PE(TTM)", "target": "≤45-50", "current": "62.46", "triggered": "❌ 未触发", "note": "3年分位点7.33%"}
      ],
      "stop_loss": "跌破前期低点",
      "target_price": "机构目标价400元",
      "exit_signals": ["月活环比下滑"],
      "recommendation": "继续观察，等待PE回落至50以下"
    }
  ]
}
"""

import sys
import json
import re
import os
import argparse
from pathlib import Path
from datetime import datetime


def get_scheme_path():
    """Resolve scheme file path from arg, env var, or default."""
    env_path = os.environ.get("STOCK_SCHEME_PATH", "")
    if env_path:
        return Path(env_path).expanduser()
    return Path.home() / "Documents" / "stock" / "scheme.md"


def parse_scheme(scheme_path):
    """Parse scheme.md and return list of stock strategies."""
    if not scheme_path.exists():
        return []

    content = scheme_path.read_text(encoding="utf-8")

    # Split by stock sections (## Stock Name (CODE))
    pattern = r"##\s+(.+?)\s*\(([A-Z0-9]+)\)\n"
    matches = list(re.finditer(pattern, content))

    stocks = []
    for i, match in enumerate(matches):
        name = match.group(1).strip()
        code = match.group(2).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section = content[start:end]

        # Parse status
        status_match = re.search(r"\*\*当前状态\*\*:\s*(.+)", section)
        status = status_match.group(1).strip() if status_match else "未知"

        # Parse entry conditions table
        conditions = []
        table_match = re.search(
            r"###\s+建仓条件\n\n\|[^\n]+\|\n\|[-\s|]+\|\n(.*?)(?=\n###|\n\n##|\Z)",
            section,
            re.DOTALL
        )
        if table_match:
            table_body = table_match.group(1).strip()
            for line in table_body.split("\n"):
                line = line.strip()
                if not line or line.startswith("|") is False:
                    continue
                cols = [c.strip() for c in line.strip("|").split("|")]
                if len(cols) >= 4:
                    conditions.append({
                        "name": cols[0],
                        "target": cols[1],
                        "current": cols[2],
                        "triggered": cols[3] if len(cols) > 3 else "",
                        "note": cols[4] if len(cols) > 4 else ""
                    })

        # Parse stop loss
        stop_loss = ""
        sl_match = re.search(r"###\s+止损线\n\n-?\s*(.+?)(?=\n###|\n\n##|\Z)", section, re.DOTALL)
        if sl_match:
            stop_loss = sl_match.group(1).strip()

        # Parse target price
        target_price = ""
        tp_match = re.search(r"###\s+目标价\n\n-?\s*(.+?)(?=\n###|\n\n##|\Z)", section, re.DOTALL)
        if tp_match:
            target_price = tp_match.group(1).strip()

        # Parse exit signals
        exit_signals = []
        es_match = re.search(r"###\s+退出信号\n\n(.*?)(?=\n###|\n\n##|\Z)", section, re.DOTALL)
        if es_match:
            for line in es_match.group(1).strip().split("\n"):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith("-")):
                    exit_signals.append(re.sub(r"^\d+\.\s*", "", line).strip("- "))

        stocks.append({
            "code": code,
            "name": name,
            "status": status,
            "conditions": conditions,
            "stop_loss": stop_loss,
            "target_price": target_price,
            "exit_signals": exit_signals
        })

    return stocks


def generate_report(data):
    """Generate markdown report from JSON with latest market data."""
    stocks = data.get("stocks", [])
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# 策略核对报告 — {today}",
        "",
        f"> 共跟踪 {len(stocks)} 只股票",
        "",
    ]

    triggered_count = 0
    for stock in stocks:
        code = stock.get("code", "")
        name = stock.get("name", "")
        status = stock.get("status", "")
        conditions = stock.get("conditions", [])
        recommendation = stock.get("recommendation", "")
        stop_loss = stock.get("stop_loss", "")
        target_price = stock.get("target_price", "")
        exit_signals = stock.get("exit_signals", [])

        lines.extend([
            f"## {name} ({code})",
            "",
            f"- **当前状态**: {status}",
        ])

        if conditions:
            lines.extend([
                "",
                "| 条件 | 目标 | 当前 | 状态 | 备注 |",
                "|------|------|------|------|------|",
            ])
            for cond in conditions:
                cname = cond.get("name", "")
                target = cond.get("target", "")
                current = cond.get("current", "")
                triggered = cond.get("triggered", "")
                note = cond.get("note", "")
                lines.append(f"| {cname} | {target} | {current} | {triggered} | {note} |")
                if "✅" in triggered or "已触发" in triggered:
                    triggered_count += 1

        if stop_loss:
            lines.extend(["", f"**止损线**: {stop_loss}"])
        if target_price:
            lines.extend(["", f"**目标价**: {target_price}"])
        if exit_signals:
            lines.extend(["", "**退出信号**:", ""])
            for sig in exit_signals:
                lines.append(f"- {sig}")

        if recommendation:
            lines.extend(["", f"**建议**: {recommendation}"])

        lines.append("")

    # Summary
    lines.insert(4, f"> 其中 {triggered_count} 个条件已触发")
    lines.insert(5, "")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check stock strategies")
    parser.add_argument("--parse", action="store_true", help="Parse scheme.md and output JSON")
    parser.add_argument("--report", action="store_true", help="Generate report from JSON input")
    parser.add_argument("--path", type=str, default=None, help="Path to scheme.md (overrides STOCK_SCHEME_PATH env var)")
    args = parser.parse_args()

    scheme_path = Path(args.path) if args.path else get_scheme_path()

    if args.parse:
        stocks = parse_scheme(scheme_path)
        print(json.dumps({"stocks": stocks}, ensure_ascii=False, indent=2))
        return

    if args.report:
        raw = sys.stdin.read().strip()
        if not raw:
            print("Error: No JSON input for report mode", file=sys.stderr)
            sys.exit(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
        report = generate_report(data)
        print(report)
        return

    # Default: just parse and print summary
    stocks = parse_scheme(scheme_path)
    if not stocks:
        print("没有找到任何股票策略。请先使用 save 模式保存策略。")
        return

    print(f"共跟踪 {len(stocks)} 只股票:")
    for s in stocks:
        print(f"  - {s['name']} ({s['code']}): {s['status']}, {len(s['conditions'])} 个条件")


if __name__ == "__main__":
    main()
