#!/usr/bin/env python3
"""财务目标追踪工具 — 纯 Python 标准库，零外部依赖。

用法：
  python goal.py create "旅行基金" 10000 2026-12-31
  python goal.py deposit "旅行基金" 2000
  python goal.py progress "旅行基金"
  python goal.py list
  python goal.py delete "旅行基金"
"""

import argparse
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional

# ─── 路径（与 invest.py 保持一致，迁移到 workspace data/）─────────
_HOME_WS = str(Path.home() / ".openclaw" / "workspace")
_RAW_DIR = os.environ.get("LEDGER_DATA_DIR", "~/.openclaw/workspace/data/ledger")
_DATA_DIR_RAW = Path(_RAW_DIR).expanduser().resolve()
if str(_DATA_DIR_RAW).startswith(_HOME_WS):
    _DATA_DIR = _DATA_DIR_RAW
else:
    _DATA_DIR_RAW = Path.home() / ".openclaw" / "workspace" / "data" / "ledger"
    _DATA_DIR = _DATA_DIR_RAW

# 确保目录存在
_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 兼容迁移：旧路径的 goals.json 迁移到新路径
_OLD_GOALS_FILE = Path(__file__).parent.parent / "data" / "goals.json"
_GOALS_FILE = _DATA_DIR / "goals.json"
if _OLD_GOALS_FILE.exists() and not _GOALS_FILE.exists():
    import shutil
    shutil.move(str(_OLD_GOALS_FILE), str(_GOALS_FILE))

# ─── 路径安全校验 ─────────────────────────────────────────
def _safe_ledger_path(p: Path) -> bool:
    """白名单：只允许写入 _DATA_DIR"""
    try:
        r = p.resolve()
        return str(r).startswith(str(_DATA_DIR))
    except Exception:
        return False


def _load_goals() -> Dict:
    if not os.path.isfile(_GOALS_FILE):
        return {"goals": []}
    with open(_GOALS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return {"goals": data}
    return data


def _save_goals(data: Dict) -> None:
    if not _safe_ledger_path(_GOALS_FILE):
        raise ValueError(f"不允许写入 Ledger 路径: {_GOALS_FILE}")
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(_GOALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _find_goal(goals: list, name: str) -> Optional[Dict]:
    for g in goals:
        if g["name"] == name:
            return g
    return None


def _today() -> date:
    return date.today()


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


# ─── 进度条 ─────────────────────────────────────────────
def _bar(pct: float, width: int = 20) -> str:
    filled = int(round(pct / 100 * width))
    filled = max(0, min(width, filled))
    return "\u2588" * filled + "\u2591" * (width - filled)


# ─── 预测逻辑 ───────────────────────────────────────────
def _forecast(goal: Dict, today: date) -> str:
    """根据存款历史计算月均存款速度，预测能否按时达成。"""
    deposits = goal.get("deposits", [])
    if len(deposits) < 1:
        return "暂无存款记录，无法预测"

    first_date = datetime.strptime(deposits[0]["date"], "%Y-%m-%d").date()
    days_elapsed = (today - first_date).days
    if days_elapsed <= 0:
        days_elapsed = 1

    total_deposited = sum(d["amount"] for d in deposits)
    monthly_rate = total_deposited / days_elapsed * 30

    remaining = goal["target"] - total_deposited
    if remaining <= 0:
        return "\u2705 已达成！"

    deadline = _parse_date(goal["deadline"])
    days_left = max(0, (deadline - today).days)
    months_left = days_left / 30

    if monthly_rate <= 0:
        return f"\u274c 按当前速度无法达成（需每月存 \u00a5{remaining / max(months_left, 0.1):,.0f}）"

    required_monthly = remaining / max(months_left, 0.1)

    if monthly_rate >= required_monthly:
        return "\u2705 预计可达成"
    else:
        return (
            f"\u274c 按当前速度无法达成"
            f"（当前月均 \u00a5{monthly_rate:,.0f}，需每月存 \u00a5{required_monthly:,.0f}）"
        )


# ─── 格式化单个目标 ─────────────────────────────────────
def _format_goal(goal: Dict, index: int, today: date, show_details: bool = False) -> str:
    total = sum(d["amount"] for d in goal.get("deposits", []))
    pct = min(round(total / goal["target"] * 100, 1), 999)
    remaining = max(goal["target"] - total, 0)

    lines = [f"{index}. {goal['name']}"]

    if pct >= 100:
        lines.append(f"   目标金额：\u00a5{goal['target']:,.0f}")
        lines.append(f"   当前存款：\u00a5{total:,.0f}")
        lines.append(f"   进度：{_bar(100)}  {pct}%")
        lines.append(f"   状态：\u2705 \u5df2\u8fbe\u6210\uff01")
        return "\n".join(lines)

    lines.append(f"   目标金额：\u00a5{goal['target']:,.0f}")
    lines.append(f"   当前存款：\u00a5{total:,.0f}")
    lines.append(f"   距离目标：\u00a5{remaining:,.0f}")
    lines.append(f"   进度：{_bar(pct)}  {pct}%")

    deadline = _parse_date(goal["deadline"])
    days_left = (deadline - today).days
    if days_left >= 0:
        lines.append(f"   截止日期：{goal['deadline']}（\u5269\u4f59 {days_left} \u5929）")
    else:
        lines.append(f"   截止日期：{goal['deadline']}（\u5df2\u8fc7\u671f {abs(days_left)} \u5929）")

    forecast = _forecast(goal, today)
    if "已达成" not in forecast:
        lines.append(f"   预计达成：{forecast}")
    else:
        lines.append(f"   状态：{forecast}")

    if show_details and goal.get("deposits"):
        lines.append(f"   存款记录：")
        for d in goal["deposits"]:
            lines.append(f"     {d['date']}  +\u00a5{d['amount']:,.0f}  {d.get('note', '')}")

    return "\n".join(lines)


# ─── 子命令 ─────────────────────────────────────────────
def cmd_create(args):
    data = _load_goals()
    goals = data["goals"]
    if _find_goal(goals, args.name):
        print(f"❌ 目标「{args.name}」已存在")
        sys.exit(1)
    today_str = _today().isoformat()
    goal = {
        "name": args.name,
        "target": args.amount,
        "deadline": args.deadline,
        "created_at": today_str,
        "deposits": [],
    }
    goals.append(goal)
    _save_goals(data)
    print(f"✅ 目标「{args.name}」已创建")
    print(f"   目标金额：¥{args.amount:,.0f}")
    print(f"   截止日期：{args.deadline}")
    print(f"   创建时间：{today_str}")


def cmd_deposit(args):
    data = _load_goals()
    goals = data["goals"]
    goal = _find_goal(goals, args.name)
    if not goal:
        print(f"❌ 未找到目标「{args.name}」")
        print(f"   现有目标：{', '.join(g['name'] for g in goals)}" if goals else "   暂无目标")
        sys.exit(1)
    today_str = _today().isoformat()
    deposit = {
        "date": today_str,
        "amount": args.amount,
        "note": args.note or "",
    }
    goal["deposits"].append(deposit)
    total = sum(d["amount"] for d in goal["deposits"])
    pct = min(round(total / goal["target"] * 100, 1), 999)
    _save_goals(data)
    print(f"✅ 已向「{args.name}」存入 ¥{args.amount:,.0f}")
    print(f"   当前存款：¥{total:,.0f} / ¥{goal['target']:,.0f}（{pct}%）")
    if total >= goal["target"]:
        print(f"   🎉 恭喜！目标已达成！")


def cmd_progress(args):
    data = _load_goals()
    goals = data["goals"]
    goal = _find_goal(goals, args.name)
    if not goal:
        print(f"❌ 未找到目标「{args.name}」")
        print(f"   现有目标：{', '.join(g['name'] for g in goals)}" if goals else "   暂无目标")
        sys.exit(1)
    today = _today()
    print("🎯 目标进度")
    print(_format_goal(goal, 1, today, show_details=True))


def cmd_list(args):
    data = _load_goals()
    goals = data["goals"]
    if not goals:
        print("🎯 暂无财务目标")
        print('   使用 create "目标名" 金额 截止日期 创建新目标')
        return
    today = _today()
    print("🎯 财务目标追踪\n")
    active, completed = [], []
    for g in goals:
        total = sum(d["amount"] for d in g.get("deposits", []))
        if total >= g["target"]:
            completed.append(g)
        else:
            active.append(g)
    active.sort(key=lambda g: g["deadline"])
    all_sorted = active + completed
    for i, g in enumerate(all_sorted, 1):
        print(_format_goal(g, i, today))
        if i < len(all_sorted):
            print()


def cmd_delete(args):
    data = _load_goals()
    goals = data["goals"]
    goal = _find_goal(goals, args.name)
    if not goal:
        print(f"❌ 未找到目标「{args.name}」")
        sys.exit(1)
    print(f"⚠️  即将永久删除目标「{args.name}」（此操作不可恢复）：")
    print(f"   名称：{goal.get('name')}")
    print(f"   目标金额：¥{goal.get('target', 0):,.2f}")
    ans = input("   确认删除？输入「删除」确认：").strip()
    if ans != "删除":
        print("❌ 已取消删除")
        sys.exit(0)
    goals.remove(goal)
    _save_goals(data)
    print(f"✅ 已删除目标「{args.name}」")


# ─── 主入口 ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="🎯 财务目标追踪")
    sub = parser.add_subparsers(dest="command")

    p_create = sub.add_parser("create", help="创建新目标")
    p_create.add_argument("name", help="目标名称")
    p_create.add_argument("amount", type=float, help="目标金额")
    p_create.add_argument("deadline", help="截止日期 (YYYY-MM-DD)")

    p_deposit = sub.add_parser("deposit", help="存入金额")
    p_deposit.add_argument("name", help="目标名称")
    p_deposit.add_argument("amount", type=float, help="存入金额")
    p_deposit.add_argument("--note", default="", help="备注")

    p_progress = sub.add_parser("progress", help="查看单个目标进度")
    p_progress.add_argument("name", help="目标名称")

    sub.add_parser("list", help="列出所有目标")

    p_delete = sub.add_parser("delete", help="删除目标")
    p_delete.add_argument("name", help="目标名称")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "create": cmd_create,
        "deposit": cmd_deposit,
        "progress": cmd_progress,
        "list": cmd_list,
        "delete": cmd_delete,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()