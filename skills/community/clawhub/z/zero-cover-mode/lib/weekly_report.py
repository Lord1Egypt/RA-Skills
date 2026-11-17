"""零稀泥模式 — 周报生成 weekly_report.py

从 FIX_CLOSURE_LOG.ndjson 聚合生成周报。

Usage:
    python weekly_report.py generate <ndjson_path> <week_str> [output_path]
    python weekly_report.py list-weeks <ndjson_path>
"""

import json, os, sys, logging
from datetime import datetime, timezone, timedelta

from .config import TZ

log = logging.getLogger("weekly")


def get_iso_week(ts_str):
    """从 ISO8601 时间戳提取 ISO 周号

    P1-v11.2-3: 用 datetime.fromisoformat 直接解析，
    不再用手动字符串索引截断。兼容带/不带时区、带/不带微秒的格式。
    """
    if not ts_str:
        return None
    try:
        # Python 3.11+ fromisoformat 原生支持 Z 后缀
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        iso = dt.isocalendar()
        return f"{iso[0]}-W{iso[1]:02d}"
    except (ValueError, TypeError):
        try:
            date_part = ts_str[:10]
            dt = datetime.strptime(date_part, "%Y-%m-%d")
            iso = dt.isocalendar()
            return f"{iso[0]}-W{iso[1]:02d}"
        except (ValueError, TypeError):
            return None


def generate_weekly_report(ndjson_path, week_str):
    """从 ndjson 聚合周报数据（流式加载）"""
    if not os.path.exists(ndjson_path):
        return None

    weekly_records = []
    total_ndjson_lines = 0
    with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            total_ndjson_lines += 1
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if get_iso_week(row.get("timestamp", "")) == week_str:
                weekly_records.append(row)

    total = len(weekly_records)
    if total == 0:
        return {"week": week_str, "total_fixes": 0, "empty": True,
                "total_ndjson_lines": total_ndjson_lines}

    # P1-2: 'blocking' 在 ndjson 中始终为 false（失败的修复不写入 ndjson），
    # 所以 passed 总是等于 total_fixes。改用 blocking_count 表示 fixed_blocking 记录数。
    passed = sum(1 for r in weekly_records if r.get("blocking") is False)
    blocking_record_count = sum(1 for r in weekly_records if r.get("was_blocking_issue") is True)
    test_total = sum(r.get("test_count", 0) for r in weekly_records)
    regr_pass_total = sum(r.get("regression_pass", 0) for r in weekly_records)
    regr_fail_total = sum(r.get("regression_fail", 0) for r in weekly_records)
    regr_all = regr_pass_total + regr_fail_total
    regr_pass_rate = (f"{regr_pass_total}/{regr_all} "
                      f"({regr_pass_total/regr_all*100:.0f}%)"
                     ) if regr_all > 0 else "N/A"

    bug_type_count = {}
    for r in weekly_records:
        bt = r.get("bug_type")
        if bt:
            bug_type_count[bt] = bug_type_count.get(bt, 0) + 1

    alerts = {bt: cnt for bt, cnt in bug_type_count.items() if cnt >= 2 and bt != "multiple"}

    return {
        "week": week_str,
        "total_fixes": total,
        "passed_fixes": passed,
        # P5: blocked_fixes removed — duplicate of blocking_count
        "blocking_count": blocking_record_count,    # P1-2: 仅当失败修复也写入 ndjson 时才有意义
        "test_count": test_total,
        "regr_pass_count": regr_pass_total,
        "regr_fail_count": regr_fail_total,
        "regr_pass_rate": regr_pass_rate,
        "new_test_count": test_total,
        "alerts": alerts,
        "total_ndjson_lines": total_ndjson_lines,
        "fixes": [
            {
                "bug_id": r.get("bug_id", ""),
                "module": r.get("module", ""),
                "bug_type": r.get("bug_type", ""),
                "root_cause": (r.get("root_cause", "") or "")[:60],
                "fix_type": r.get("fix_type", ""),
                "regression_pass": r.get("regression_pass", 0),
                "timestamp": (r.get("timestamp", "") or "")[:10],
            }
            for r in weekly_records
        ],
    }


def write_report_md(ndjson_path, week_str, output_path):
    """生成 markdown 格式周报"""
    data = generate_weekly_report(ndjson_path, week_str)
    if data is None:
        log.error("ndjson not found: %s", ndjson_path)
        return False

    if data.get("empty"):
        content = (f"# 修复闭环周报 — {week_str}\n\n"
                   f"**数据源**: {ndjson_path}\n"
                   f"**本周记录**: 0 条\n\n"
               f"> 注意: ndjson 仅存储成功的修复（blocking 始终为 False），\n"
               f"> 被 Phase 1/2 阻断的修复不纳入计数。\n\n"
               f"本周无修复记录。\n")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M CST")

    alerts_md = ""
    if data["alerts"]:
        alerts_md = ("## \u26a0\ufe0f 重构警报\n\n"
                     "| Bug 类型 | 出现次数 |\n"
                     "|----------|---------|\n")
        for bt, cnt in sorted(data["alerts"].items(), key=lambda x: -x[1]):
            alerts_md += f"| {bt} | {cnt} 次 |\n"
        alerts_md += "\n"

    fixes_md = ("## 修复明细\n\n"
                "| # | Bug ID | 模块 | bug_type | 根因摘要 | 修复类型 | 测试通过 | 日期 |\n"
                "|---|--------|------|----------|---------|---------|---------|------|\n")
    for i, fix in enumerate(data["fixes"], 1):
        fixes_md += (f"| {i} | {fix['bug_id']} | {fix['module']} "
                     f"| {fix['bug_type']} | {fix['root_cause']} "
                     f"| {fix['fix_type']} | {fix['regression_pass']} "
                     f"| {fix['timestamp']} |\n")

    total_lines = data.get('total_ndjson_lines', 0)
    # P2-D: N/A 显示优化
    pass_rate_display = data['regr_pass_rate']
    if pass_rate_display == "N/A":
        pass_rate_display = "N/A（无回归测试执行）"
    content = (f"# 修复闭环周报 — {data['week']}\n\n"
               f"**生成时间**: {now}\n"
               f"**数据源**: {ndjson_path}（{total_lines} 条记录）\n\n"
               f"---\n\n"
               f"## 概览\n\n"
               f"| 指标 | 数值 |\n"
               f"|------|------|\n"
               f"| 本周修复 | {data['total_fixes']} 个 bug |\n"
               f"| 新增测试 | {data['new_test_count']} 个 |\n"
               f"| 回归通过率 | {data['regr_pass_rate']} |\n"
               f"| 阻塞记录 | {data['blocking_count']} 个 |\n"
               f"| 活跃重构警报 | {len(data['alerts'])} 个 |\n\n"
               f"{fixes_md}\n"
               f"{alerts_md}\n"
               f"## 趋势\n\n"
               f"> 本周修复数: {data['total_fixes']} | "
               f"回归通过率: {data['regr_pass_rate']} | "
               f"阻塞记录: {data['blocking_count']}\n\n"
               f"---\n\n"
               f"*本报告由零稀泥模式 weekly_report.py 自动聚合生成*\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="周报生成器")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("generate", help="生成周报")
    p.add_argument("ndjson_path", nargs="?",
                   default="FIX_CLOSURE_LOG.ndjson")
    p.add_argument("week_str", nargs="?")
    p.add_argument("output_path", nargs="?")

    p = sub.add_parser("list-weeks", help="列出可用周")
    p.add_argument("ndjson_path", nargs="?",
                   default="FIX_CLOSURE_LOG.ndjson")

    args = parser.parse_args()

    try:
        if args.command == "generate":
            now = datetime.now(TZ)
            iso = now.isocalendar()
            week_str = args.week_str or f"{iso[0]}-W{iso[1]:02d}"
            output = (args.output_path
                      or f"reports/fix_closure_weekly_{week_str}.md")
            os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
            if write_report_md(args.ndjson_path, week_str, output):
                print(f"OK: 周报已生成 -> {output}")
            else:
                sys.exit(1)
        elif args.command == "list-weeks":
            if not os.path.exists(args.ndjson_path):
                print("ndjson not found")
                sys.exit(1)
            weeks = set()
            with open(args.ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                        w = get_iso_week(row.get("timestamp", ""))
                        if w:
                            weeks.add(w)
                    except json.JSONDecodeError:
                        continue
            for w in sorted(weeks):
                print(w)
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
