#!/usr/bin/env python3
"""
team-weekly 工时统计与效能分析模块（付费版功能）

提供工时统计、趋势分析、效率评估和甘特图生成。
"""

import calendar
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    build_markdown_table,
    check_subscription,
    create_base_parser,
    format_hours,
    format_percentage,
    now_str,
    output_error,
    output_success,
    read_input_data,
    require_paid,
    week_range_str,
)
from worklog_manager import _load_worklogs
from team_store import _load_team


# ============================================================
# 工时统计
# ============================================================

def analyze_workload(data: Dict[str, Any]) -> Dict[str, Any]:
    """工时统计分析。

    Args:
        data: 包含以下字段的字典：
            - date_from (str, optional): 起始日期
            - date_to (str, optional): 结束日期
            - member (str, optional): 指定成员
            - project (str, optional): 指定项目

    Returns:
        工时统计结果和 Markdown 报告。
    """
    require_paid("工时统计")

    logs = _load_worklogs()
    date_from = data.get("date_from")
    date_to = data.get("date_to")
    member = data.get("member")
    project = data.get("project")

    if date_from:
        logs = [l for l in logs if l["date"] >= date_from]
    if date_to:
        logs = [l for l in logs if l["date"] <= date_to]
    if member:
        logs = [l for l in logs if l["member_name"] == member]
    if project:
        logs = [l for l in logs if l.get("project") == project]

    total_hours = sum(l.get("hours", 0) for l in logs)

    # 按成员统计
    by_member: Dict[str, float] = defaultdict(float)
    for log in logs:
        by_member[log["member_name"]] += log.get("hours", 0)

    # 按项目统计
    by_project: Dict[str, float] = defaultdict(float)
    for log in logs:
        proj = log.get("project", "未分类") or "未分类"
        by_project[proj] += log.get("hours", 0)

    # 按分类统计
    by_category: Dict[str, float] = defaultdict(float)
    for log in logs:
        cat = log.get("category", "其他")
        by_category[cat] += log.get("hours", 0)

    # 按日统计
    by_date: Dict[str, float] = defaultdict(float)
    for log in logs:
        by_date[log["date"]] += log.get("hours", 0)

    # 生成 Markdown
    period_str = ""
    if date_from and date_to:
        period_str = f"{date_from} ~ {date_to}"
    elif date_from:
        period_str = f"{date_from} 至今"
    elif date_to:
        period_str = f"截至 {date_to}"
    else:
        period_str = "全部"

    md_lines = []
    md_lines.append("# 工时统计分析报告")
    md_lines.append("")
    md_lines.append(f"**统计范围**: {period_str}")
    if member:
        md_lines.append(f"**指定成员**: {member}")
    if project:
        md_lines.append(f"**指定项目**: {project}")
    md_lines.append(f"**生成时间**: {now_str()}")
    md_lines.append("")

    # 总览
    md_lines.append("## 总览")
    md_lines.append("")
    md_lines.append(f"- 总工时: **{format_hours(total_hours)}**")
    md_lines.append(f"- 涉及成员: **{len(by_member)}** 人")
    md_lines.append(f"- 涉及项目: **{len(by_project)}** 个")
    md_lines.append(f"- 工作天数: **{len(by_date)}** 天")
    md_lines.append("")

    # 成员工时
    if not member:
        md_lines.append("## 成员工时分布")
        md_lines.append("")
        headers = ["成员", "工时", "占比"]
        rows = []
        for name, hours in sorted(by_member.items(), key=lambda x: x[1], reverse=True):
            pct = hours / total_hours if total_hours > 0 else 0
            rows.append([name, format_hours(hours), format_percentage(pct)])
        md_lines.append(build_markdown_table(headers, rows))
        md_lines.append("")

        # 饼图
        md_lines.append("```mermaid")
        md_lines.append("pie title 成员工时分布")
        for name, hours in sorted(by_member.items(), key=lambda x: x[1], reverse=True):
            md_lines.append(f'    "{name}" : {hours:.1f}')
        md_lines.append("```")
        md_lines.append("")

    # 项目工时
    if not project:
        md_lines.append("## 项目工时分布")
        md_lines.append("")
        headers = ["项目", "工时", "占比"]
        rows = []
        for proj, hours in sorted(by_project.items(), key=lambda x: x[1], reverse=True):
            pct = hours / total_hours if total_hours > 0 else 0
            rows.append([proj, format_hours(hours), format_percentage(pct)])
        md_lines.append(build_markdown_table(headers, rows))
        md_lines.append("")

    # 分类工时
    md_lines.append("## 工作分类分布")
    md_lines.append("")
    cat_headers = ["分类", "工时", "占比"]
    cat_rows = []
    for cat, hours in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        pct = hours / total_hours if total_hours > 0 else 0
        cat_rows.append([cat, format_hours(hours), format_percentage(pct)])
    md_lines.append(build_markdown_table(cat_headers, cat_rows))
    md_lines.append("")

    md_lines.append("```mermaid")
    md_lines.append("pie title 工作分类分布")
    for cat, hours in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        md_lines.append(f'    "{cat}" : {hours:.1f}')
    md_lines.append("```")
    md_lines.append("")

    report_md = "\n".join(md_lines)

    return {
        "total_hours": total_hours,
        "by_member": dict(by_member),
        "by_project": dict(by_project),
        "by_category": dict(by_category),
        "report_markdown": report_md,
    }


# ============================================================
# 趋势分析
# ============================================================

def analyze_trend(data: Dict[str, Any]) -> Dict[str, Any]:
    """工时趋势分析。

    Args:
        data: 包含以下字段的字典：
            - member (str, optional): 指定成员
            - project (str, optional): 指定项目
            - period (str, optional): 分析周期 (week/month)，默认 week
            - weeks (int, optional): 回溯周数，默认 4

    Returns:
        趋势分析结果和 Markdown 报告。
    """
    require_paid("趋势分析")

    logs = _load_worklogs()
    member = data.get("member")
    project = data.get("project")
    weeks_back = int(data.get("weeks", 4))

    if member:
        logs = [l for l in logs if l["member_name"] == member]
    if project:
        logs = [l for l in logs if l.get("project") == project]

    now = datetime.now()

    # 按周聚合
    weekly_stats: Dict[str, Dict[str, Any]] = {}
    for i in range(weeks_back):
        target = now - timedelta(weeks=i)
        w_start, w_end = week_range_str(target)
        week_key = f"W{weeks_back - i}"
        week_label = f"{w_start}~{w_end}"
        week_logs = [l for l in logs if w_start <= l["date"] <= w_end]
        weekly_stats[week_key] = {
            "label": week_label,
            "hours": sum(l.get("hours", 0) for l in week_logs),
            "tasks": len(week_logs),
        }

    # 生成 Markdown
    md_lines = []
    title = "工时趋势分析"
    if member:
        title = f"{member} 工时趋势分析"
    if project:
        title += f"（项目: {project}）"
    md_lines.append(f"# {title}")
    md_lines.append("")
    md_lines.append(f"**分析周期**: 近 {weeks_back} 周")
    md_lines.append(f"**生成时间**: {now_str()}")
    md_lines.append("")

    # 数据表格
    md_lines.append("## 周度数据")
    md_lines.append("")
    headers = ["周", "日期范围", "任务数", "工时"]
    rows = []
    for key in sorted(weekly_stats.keys()):
        ws = weekly_stats[key]
        rows.append([key, ws["label"], str(ws["tasks"]), format_hours(ws["hours"])])
    md_lines.append(build_markdown_table(headers, rows))
    md_lines.append("")

    # 趋势图
    sorted_keys = sorted(weekly_stats.keys())
    md_lines.append("## 趋势图")
    md_lines.append("")
    md_lines.append("```mermaid")
    md_lines.append("xychart-beta")
    md_lines.append(f'    title "工时趋势（近{weeks_back}周）"')
    md_lines.append('    x-axis [' + ", ".join(f'"{k}"' for k in sorted_keys) + ']')
    md_lines.append('    y-axis "工时（小时）"')
    md_lines.append('    bar [' + ", ".join(str(weekly_stats[k]["hours"]) for k in sorted_keys) + ']')
    md_lines.append('    line [' + ", ".join(str(weekly_stats[k]["hours"]) for k in sorted_keys) + ']')
    md_lines.append("```")
    md_lines.append("")

    # 趋势判断
    hours_list = [weekly_stats[k]["hours"] for k in sorted_keys]
    md_lines.append("## 趋势判断")
    md_lines.append("")
    if len(hours_list) >= 2 and hours_list[0] > 0:
        change_pct = (hours_list[-1] - hours_list[0]) / hours_list[0]
        if change_pct > 0.2:
            md_lines.append(f"- 工时呈**上升**趋势，增幅 {format_percentage(change_pct)}。")
        elif change_pct < -0.2:
            md_lines.append(f"- 工时呈**下降**趋势，降幅 {format_percentage(abs(change_pct))}。")
        else:
            md_lines.append("- 工时保持**稳定**。")

    avg_hours = sum(hours_list) / len(hours_list) if hours_list else 0
    md_lines.append(f"- 周均工时: **{format_hours(avg_hours)}**")
    md_lines.append("")

    report_md = "\n".join(md_lines)

    return {
        "weekly_stats": weekly_stats,
        "trend": "up" if hours_list and len(hours_list) >= 2 and hours_list[-1] > hours_list[0] * 1.2
                 else ("down" if hours_list and len(hours_list) >= 2 and hours_list[-1] < hours_list[0] * 0.8
                       else "stable"),
        "report_markdown": report_md,
    }


# ============================================================
# 效率分析
# ============================================================

def analyze_efficiency(data: Dict[str, Any]) -> Dict[str, Any]:
    """成员效率分析。

    Args:
        data: 包含以下字段的字典：
            - member (str, optional): 指定成员（不指定则分析所有成员）
            - weeks (int, optional): 回溯周数，默认 4

    Returns:
        效率分析结果和 Markdown 报告。
    """
    require_paid("效率分析")

    logs = _load_worklogs()
    member = data.get("member")
    weeks_back = int(data.get("weeks", 4))

    now = datetime.now()
    cutoff = now - timedelta(weeks=weeks_back)
    cutoff_str = cutoff.strftime("%Y-%m-%d")
    logs = [l for l in logs if l["date"] >= cutoff_str]

    if member:
        logs = [l for l in logs if l["member_name"] == member]

    # 按成员聚合
    member_stats: Dict[str, Dict[str, Any]] = {}
    for log in logs:
        name = log["member_name"]
        if name not in member_stats:
            member_stats[name] = {
                "total_hours": 0,
                "task_count": 0,
                "projects": set(),
                "categories": defaultdict(float),
                "daily_hours": defaultdict(float),
            }
        ms = member_stats[name]
        hours = log.get("hours", 0)
        ms["total_hours"] += hours
        ms["task_count"] += 1
        if log.get("project"):
            ms["projects"].add(log["project"])
        ms["categories"][log.get("category", "其他")] += hours
        ms["daily_hours"][log["date"]] += hours

    # 生成 Markdown
    md_lines = []
    title = "团队效率分析" if not member else f"{member} 效率分析"
    md_lines.append(f"# {title}")
    md_lines.append("")
    md_lines.append(f"**分析周期**: 近 {weeks_back} 周")
    md_lines.append(f"**生成时间**: {now_str()}")
    md_lines.append("")

    if not member_stats:
        md_lines.append("暂无工作记录。")
        return {"member_stats": {}, "report_markdown": "\n".join(md_lines)}

    # 效率对比表
    md_lines.append("## 成员效率对比")
    md_lines.append("")
    headers = ["成员", "总工时", "任务数", "日均工时", "工作天数", "项目数"]
    rows = []

    for name, ms in sorted(member_stats.items(), key=lambda x: x[1]["total_hours"], reverse=True):
        work_days = len(ms["daily_hours"])
        avg_daily = ms["total_hours"] / work_days if work_days > 0 else 0
        rows.append([
            name,
            format_hours(ms["total_hours"]),
            str(ms["task_count"]),
            format_hours(avg_daily),
            str(work_days),
            str(len(ms["projects"])),
        ])
    md_lines.append(build_markdown_table(headers, rows))
    md_lines.append("")

    # 工时对比柱状图
    if len(member_stats) > 1:
        md_lines.append("```mermaid")
        md_lines.append("xychart-beta")
        md_lines.append(f'    title "成员工时对比（近{weeks_back}周）"')
        sorted_names = sorted(member_stats.keys())
        md_lines.append('    x-axis [' + ", ".join(f'"{n}"' for n in sorted_names) + ']')
        md_lines.append('    y-axis "工时（小时）"')
        md_lines.append('    bar [' + ", ".join(
            str(member_stats[n]["total_hours"]) for n in sorted_names
        ) + ']')
        md_lines.append("```")
        md_lines.append("")

    # 个人详细分析
    for name, ms in sorted(member_stats.items()):
        md_lines.append(f"### {name} 详细分析")
        md_lines.append("")
        work_days = len(ms["daily_hours"])
        avg_daily = ms["total_hours"] / work_days if work_days > 0 else 0
        md_lines.append(f"- 总工时: {format_hours(ms['total_hours'])}")
        md_lines.append(f"- 任务数: {ms['task_count']}")
        md_lines.append(f"- 工作天数: {work_days}")
        md_lines.append(f"- 日均工时: {format_hours(avg_daily)}")
        md_lines.append(f"- 涉及项目: {', '.join(ms['projects']) if ms['projects'] else '-'}")
        md_lines.append("")

        # 分类占比
        if ms["categories"]:
            md_lines.append("工作分类分布:")
            md_lines.append("")
            for cat, hours in sorted(ms["categories"].items(), key=lambda x: x[1], reverse=True):
                pct = hours / ms["total_hours"] if ms["total_hours"] > 0 else 0
                md_lines.append(f"  - {cat}: {format_hours(hours)} ({format_percentage(pct)})")
            md_lines.append("")

    report_md = "\n".join(md_lines)

    # 序列化 set 和 defaultdict
    serializable_stats = {}
    for name, ms in member_stats.items():
        serializable_stats[name] = {
            "total_hours": ms["total_hours"],
            "task_count": ms["task_count"],
            "projects": list(ms["projects"]),
            "categories": dict(ms["categories"]),
            "work_days": len(ms["daily_hours"]),
        }

    return {
        "member_stats": serializable_stats,
        "report_markdown": report_md,
    }


# ============================================================
# 甘特图生成
# ============================================================

def generate_gantt(data: Dict[str, Any]) -> Dict[str, Any]:
    """生成项目甘特图。

    Args:
        data: 包含以下字段的字典：
            - project (str, optional): 指定项目
            - weeks (int, optional): 回溯周数，默认 4

    Returns:
        甘特图 Mermaid 代码和结构化数据。
    """
    require_paid("甘特图")

    logs = _load_worklogs()
    project = data.get("project")
    weeks_back = int(data.get("weeks", 4))

    now = datetime.now()
    cutoff = now - timedelta(weeks=weeks_back)
    cutoff_str = cutoff.strftime("%Y-%m-%d")
    logs = [l for l in logs if l["date"] >= cutoff_str]

    if project:
        logs = [l for l in logs if l.get("project") == project]

    # 按项目-成员-日期聚合
    project_tasks: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for log in logs:
        proj = log.get("project", "未分类") or "未分类"
        member = log["member_name"]
        key = f"{proj}_{member}"

        if proj not in project_tasks:
            project_tasks[proj] = {}

        if member not in project_tasks[proj]:
            project_tasks[proj][member] = {
                "start": log["date"],
                "end": log["date"],
                "hours": 0,
                "tasks": 0,
            }

        pt = project_tasks[proj][member]
        pt["start"] = min(pt["start"], log["date"])
        pt["end"] = max(pt["end"], log["date"])
        pt["hours"] += log.get("hours", 0)
        pt["tasks"] += 1

    # 生成 Mermaid 甘特图
    md_lines = []
    md_lines.append("# 项目进度甘特图")
    md_lines.append("")
    md_lines.append(f"**统计范围**: 近 {weeks_back} 周")
    if project:
        md_lines.append(f"**指定项目**: {project}")
    md_lines.append(f"**生成时间**: {now_str()}")
    md_lines.append("")

    md_lines.append("```mermaid")
    md_lines.append("gantt")
    md_lines.append("    title 项目进度甘特图")
    md_lines.append("    dateFormat YYYY-MM-DD")
    md_lines.append("")

    for proj, members in sorted(project_tasks.items()):
        md_lines.append(f"    section {proj}")
        for member, info in sorted(members.items()):
            task_name = f"{member}({format_hours(info['hours'])})"
            md_lines.append(f"    {task_name} : {info['start']}, {info['end']}")

    md_lines.append("```")
    md_lines.append("")

    # 项目统计表
    md_lines.append("## 项目汇总")
    md_lines.append("")
    headers = ["项目", "参与成员", "总工时", "起止日期"]
    rows = []
    for proj, members in sorted(project_tasks.items()):
        total_h = sum(m["hours"] for m in members.values())
        all_starts = [m["start"] for m in members.values()]
        all_ends = [m["end"] for m in members.values()]
        rows.append([
            proj,
            str(len(members)),
            format_hours(total_h),
            f"{min(all_starts)} ~ {max(all_ends)}",
        ])
    md_lines.append(build_markdown_table(headers, rows))
    md_lines.append("")

    report_md = "\n".join(md_lines)

    return {
        "project_tasks": {
            proj: {member: info for member, info in members.items()}
            for proj, members in project_tasks.items()
        },
        "report_markdown": report_md,
    }


# ============================================================
# 命令行入口
# ============================================================

def main() -> None:
    """命令行入口函数。"""
    parser = create_base_parser("工时统计与效能分析工具")
    parser.add_argument("--member", default=None, help="指定成员")
    parser.add_argument("--project", default=None, help="指定项目")
    args, _ = parser.parse_known_args()

    try:
        action = args.action
        data = {}
        try:
            data = read_input_data(args)
        except ValueError:
            pass

        if args.member:
            data["member"] = args.member
        if args.project:
            data["project"] = args.project

        if action == "workload":
            result = analyze_workload(data)
            output_success(result)

        elif action == "trend":
            result = analyze_trend(data)
            output_success(result)

        elif action == "efficiency":
            result = analyze_efficiency(data)
            output_success(result)

        elif action == "gantt":
            result = generate_gantt(data)
            output_success(result)

        else:
            output_error(f"未知操作: {action}", "UNKNOWN_ACTION")

    except (ValueError, PermissionError) as e:
        output_error(str(e), type(e).__name__.upper())
    except Exception as e:
        output_error(f"内部错误: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
