#!/usr/bin/env python3
"""
Save stock strategy to the scheme tracking file.

The file path is determined by:
  1. --path argument
  2. STOCK_SCHEME_PATH environment variable
  3. Default: ~/Documents/stock/scheme.md

Reads JSON from stdin, formats it, and appends/updates the scheme file.

Usage:
    echo '{"stock_code":"688111","stock_name":"金山办公",...}' | python3 save_scheme.py [--path /path/to/scheme.md]
"""

import sys
import json
import os
import re
import argparse
from datetime import datetime
from pathlib import Path


def get_scheme_path():
    """Resolve scheme file path from arg, env var, or default."""
    env_path = os.environ.get("STOCK_SCHEME_PATH", "")
    if env_path:
        return Path(env_path).expanduser()
    return Path.home() / "Documents" / "stock" / "scheme.md"


def ensure_file(scheme_path):
    """Ensure scheme.md exists with proper header."""
    scheme_path.parent.mkdir(parents=True, exist_ok=True)
    if not scheme_path.exists():
        header = f"""# 股票策略跟踪

> 最后更新：{datetime.now().strftime('%Y-%m-%d')}

"""
        scheme_path.write_text(header, encoding="utf-8")


def parse_entry_conditions(conditions):
    """Convert entry_conditions list to markdown table rows."""
    rows = []
    for cond in conditions:
        name = cond.get("name", "")
        target = cond.get("target", "")
        current = cond.get("current", "")
        triggered = cond.get("triggered", "❌ 未触发")
        note = cond.get("note", "")
        rows.append(f"| {name} | {target} | {current} | {triggered} | {note} |")
    return "\n".join(rows)


def format_strategy(data):
    """Format a single strategy entry as markdown."""
    stock_code = data.get("stock_code", "")
    stock_name = data.get("stock_name", "")
    analysis_date = data.get("analysis_date", datetime.now().strftime("%Y-%m-%d"))
    status = data.get("status", "观察中")
    conclusion = data.get("conclusion", "")
    current_price = data.get("current_price", "")
    current_pe = data.get("current_pe", "")
    market_cap = data.get("market_cap", "")

    # Entry conditions table
    entry_conditions = data.get("entry_conditions", [])
    if entry_conditions:
        entry_table = parse_entry_conditions(entry_conditions)
    else:
        entry_table = "| 条件 | 目标值 | 当前值 | 是否触发 | 备注 |\n|------|--------|--------|----------|------|"

    # Optional fields
    stop_loss = data.get("stop_loss", "")
    target_price = data.get("target_price", "")
    exit_signals = data.get("exit_signals", [])
    key_assumptions = data.get("key_assumptions", [])
    open_questions = data.get("open_questions", [])
    position_size = data.get("position_size", "")
    time_horizon = data.get("time_horizon", "")

    # Build markdown
    lines = [
        f"## {stock_name} ({stock_code})",
        "",
        f"- **分析日期**: {analysis_date}",
        f"- **当前状态**: {status}",
        f"- **分析结论**: {conclusion}",
    ]

    if current_price:
        lines.append(f"- **分析时股价**: {current_price}")
    if current_pe:
        lines.append(f"- **分析时PE**: {current_pe}")
    if market_cap:
        lines.append(f"- **分析时市值**: {market_cap}")
    if position_size:
        lines.append(f"- **建议仓位**: {position_size}")
    if time_horizon:
        lines.append(f"- **持有周期**: {time_horizon}")

    lines.extend([
        "",
        "### 建仓条件",
        "",
        "| 条件 | 目标值 | 当前值 | 是否触发 | 备注 |",
        "|------|--------|--------|----------|------|",
    ])

    if entry_conditions:
        lines.append(entry_table)
    else:
        lines.append("| 未明确 | - | - | - | - |")

    if stop_loss:
        lines.extend(["", "### 止损线", "", f"- {stop_loss}"])

    if target_price:
        lines.extend(["", "### 目标价", "", f"- {target_price}"])

    if exit_signals:
        lines.extend(["", "### 退出信号", ""])
        for i, sig in enumerate(exit_signals, 1):
            lines.append(f"{i}. {sig}")

    if key_assumptions:
        lines.extend(["", "### 核心假设", ""])
        for i, assumption in enumerate(key_assumptions, 1):
            lines.append(f"{i}. {assumption}")

    if open_questions:
        lines.extend(["", "### 未解问题", ""])
        for i, q in enumerate(open_questions, 1):
            lines.append(f"{i}. {q}")

    # History tracking
    lines.extend([
        "",
        "### 历史跟踪",
        "",
        f"- {analysis_date}: 分析完成，建议{status}",
    ])

    return "\n".join(lines) + "\n\n"


def extract_existing_section(content, stock_code):
    """Extract existing section for a stock if it exists."""
    pattern = rf"(## [^\n]*\s*\({re.escape(stock_code)}\).*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1), match.start(), match.end()
    return None, -1, -1


def update_history(content, start, end, new_entry):
    """Replace old section with updated entry, preserving history."""
    old_section = content[start:end]

    # Extract existing history
    history_match = re.search(r"### 历史跟踪\n\n(.*?)(?=\n### |\Z)", old_section, re.DOTALL)
    existing_history = []
    if history_match:
        existing_history = [line.strip("- ").strip() for line in history_match.group(1).strip().split("\n") if line.strip()]

    # Add new history line
    today = datetime.now().strftime("%Y-%m-%d")
    new_history_line = f"- {today}: 策略更新"

    # Prepend new history to existing
    all_history = [new_history_line] + existing_history
    history_block = "### 历史跟踪\n\n" + "\n".join(all_history)

    # Replace history section in new_entry
    new_entry_with_history = re.sub(
        r"### 历史跟踪\n\n.*?\n\n",
        history_block + "\n\n",
        new_entry,
        flags=re.DOTALL
    )

    return content[:start] + new_entry_with_history + content[end:]


def main():
    parser = argparse.ArgumentParser(description="Save stock strategy to scheme file")
    parser.add_argument("--path", type=str, default=None, help="Path to scheme.md (overrides STOCK_SCHEME_PATH env var)")
    args = parser.parse_args()

    scheme_path = Path(args.path) if args.path else get_scheme_path()

    # Read JSON from stdin
    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: No JSON input provided", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    ensure_file(scheme_path)
    content = scheme_path.read_text(encoding="utf-8")

    stock_code = data.get("stock_code", "")
    if not stock_code:
        print("Error: stock_code is required", file=sys.stderr)
        sys.exit(1)

    new_entry = format_strategy(data)

    existing, start, end = extract_existing_section(content, stock_code)
    if existing:
        # Update existing section
        content = update_history(content, start, end, new_entry)
        action = "updated"
    else:
        # Append new section
        content = content.rstrip() + "\n\n" + new_entry
        action = "added"

    # Update last_updated timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r"> 最后更新：\d{4}-\d{2}-\d{2}",
        f"> 最后更新：{today}",
        content
    )

    scheme_path.write_text(content, encoding="utf-8")
    print(f"Successfully {action} strategy for {data.get('stock_name', stock_code)} ({stock_code})")


if __name__ == "__main__":
    main()
