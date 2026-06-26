#!/usr/bin/env python3
"""
team-weekly 周报/月报汇总生成模块

从工作日志数据中汇总生成结构化的周报和月报。
"""

import calendar
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from utils import (
    build_markdown_table,
    check_feature,
    check_subscription,
    create_base_parser,
    format_hours,
    format_percentage,
    month_range_str,
    now_str,
    output_error,
    output_success,
    read_input_data,
    week_range_str,
)
from worklog_manager import _load_worklogs
from team_store import _load_team


# ============================================================
# 数据聚合
# ============================================================

def _filter_logs_by_range(
    logs: List[Dict[str, Any]],
    date_from: str,
    date_to: str,
) -> List[Dict[str, Any]]:
    """按日期范围过滤日志。"""
    return [l for l in logs if date_from <= l["date"] <= date_to]


def _aggregate_by_member(logs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """按成员聚合日志数据。"""
    result: Dict[str, Dict[str, Any]] = {}
    for log in logs:
        name = log["member_name"]
        if name not in result:
            result[name] = {
                "member_name": name,
                "total_hours": 0,
                "task_count": 0,
                "tasks": [],
                "projects": set(),
                "categories": defaultdict(float),
            }
        result[name]["total_hours"] += log.get("hours", 0)
        result[name]["task_count"] += 1
        result[name]["tasks"].append(log)
        if log.get("project"):
            result[name]["projects"].add(log["project"])
        result[name]["categories"][log.get("category", "其他")] += log.get("hours", 0)

    # 将 set 转为 list 以便序列化
    for v in result.values():
        v["projects"] = list(v["projects"])
        v["categories"] = dict(v["categories"])

    return result


def _aggregate_by_project(logs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """按项目聚合日志数据。"""
    result: Dict[str, Dict[str, Any]] = {}
    for log in logs:
        proj = log.get("project", "未分类") or "未分类"
        if proj not in result:
            result[proj] = {
                "project": proj,
                "total_hours": 0,
                "task_count": 0,
                "members": set(),
            }
        result[proj]["total_hours"] += log.get("hours", 0)
        result[proj]["task_count"] += 1
        result[proj]["members"].add(log["member_name"])

    for v in result.values():
        v["members"] = list(v["members"])

    return result


# ============================================================
# 周报生成
# ============================================================

def generate_weekly_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """生成周报。

    Args:
        data: 包含以下字段的字典：
            - week (str, optional): 周标识，如 "this"、"last"、"2024-W03"
            - template (str, optional): 模板类型

    Returns:
        包含 Markdown 周报和结构化数据的字典。
    """
    now = datetime.now()
    week = data.get("week", "this")

    # 解析周范围
    if week == "this":
        target_date = now
    elif week == "last":
        target_date = now - timedelta(days=7)
    else:
        try:
            parts = week.split("-W")
            year = int(parts[0])
            week_num = int(parts[1])
            jan1 = datetime(year, 1, 1)
            start = jan1 - timedelta(days=jan1.isoweekday() - 1)
            target_date = start + timedelta(weeks=week_num - 1)
        except (ValueError, IndexError):
            raise ValueError(f"无效的周标识: {week!r}")

    date_from, date_to = week_range_str(target_date)

    # 获取日志
    logs = _load_worklogs()
    week_logs = _filter_logs_by_range(logs, date_from, date_to)

    # 获取团队信息
    team = _load_team()
    team_name = team["name"] if team else "团队"

    # 聚合数据
    by_member = _aggregate_by_member(week_logs)
    by_project = _aggregate_by_project(week_logs)
    total_hours = sum(l.get("hours", 0) for l in week_logs)
    total_tasks = len(week_logs)

    sub = check_subscription()
    is_paid = sub["tier"] == "paid"

    # 生成 Markdown 报告
    md_lines = []
    md_lines.append(f"# {team_name} 周报")
    md_lines.append(f"")
    md_lines.append(f"**报告周期**: {date_from} ~ {date_to}")
    md_lines.append(f"**生成时间**: {now_str()}")
    md_lines.append("")

    # 概览
    md_lines.append("## 概览")
    md_lines.append("")
    overview_headers = ["指标", "数值"]
    overview_rows = [
        ["参与人数", str(len(by_member))],
        ["任务总数", str(total_tasks)],
        ["总工时", format_hours(total_hours)],
        ["涉及项目", str(len(by_project))],
    ]
    md_lines.append(build_markdown_table(overview_headers, overview_rows))
    md_lines.append("")

    # 按成员统计
    md_lines.append("## 成员工作汇总")
    md_lines.append("")
    member_headers = ["成员", "任务数", "工时", "涉及项目"]
    member_rows = []
    for name, info in sorted(by_member.items()):
        member_rows.append([
            name,
            str(info["task_count"]),
            format_hours(info["total_hours"]),
            ", ".join(info["projects"]) if info["projects"] else "-",
        ])
    md_lines.append(build_markdown_table(member_headers, member_rows))
    md_lines.append("")

    # 按项目统计
    md_lines.append("## 项目进展")
    md_lines.append("")
    project_headers = ["项目", "任务数", "工时", "参与成员"]
    project_rows = []
    for proj, info in sorted(by_project.items()):
        project_rows.append([
            proj,
            str(info["task_count"]),
            format_hours(info["total_hours"]),
            ", ".join(info["members"]),
        ])
    md_lines.append(build_markdown_table(project_headers, project_rows))
    md_lines.append("")

    # 详细工作记录
    md_lines.append("## 详细工作记录")
    md_lines.append("")
    for name, info in sorted(by_member.items()):
        md_lines.append(f"### {name}")
        md_lines.append("")
        detail_headers = ["日期", "任务", "项目", "分类", "工时"]
        detail_rows = []
        for task in sorted(info["tasks"], key=lambda t: t["date"]):
            detail_rows.append([
                task["date"],
                task["task_description"],
                task.get("project", "-"),
                task.get("category", "其他"),
                format_hours(task.get("hours", 0)),
            ])
        md_lines.append(build_markdown_table(detail_headers, detail_rows))
        md_lines.append("")

    # 付费版：图表与洞察
    if is_paid:
        md_lines.append("## 工时分布图")
        md_lines.append("")

        # 项目工时饼图
        if by_project:
            md_lines.append("### 项目工时分布")
            md_lines.append("")
            md_lines.append("```mermaid")
            md_lines.append("pie title 项目工时分布")
            for proj, info in sorted(by_project.items(), key=lambda x: x[1]["total_hours"], reverse=True):
                md_lines.append(f'    "{proj}" : {info["total_hours"]:.1f}')
            md_lines.append("```")
            md_lines.append("")

        # 成员工时柱状图
        if by_member:
            md_lines.append("### 成员工时对比")
            md_lines.append("")
            md_lines.append("```mermaid")
            md_lines.append("xychart-beta")
            md_lines.append(f'    title "成员工时对比（{date_from} ~ {date_to}）"')
            md_lines.append('    x-axis [' + ", ".join(f'"{n}"' for n in sorted(by_member.keys())) + ']')
            md_lines.append('    y-axis "工时（小时）"')
            bar_data = [str(by_member[n]["total_hours"]) for n in sorted(by_member.keys())]
            md_lines.append('    bar [' + ", ".join(bar_data) + ']')
            md_lines.append("```")
            md_lines.append("")

        # 洞察分析
        md_lines.append("## 洞察与建议")
        md_lines.append("")
        insights = _generate_weekly_insights(by_member, by_project, total_hours)
        for insight in insights:
            md_lines.append(f"- {insight}")
        md_lines.append("")

    report_md = "\n".join(md_lines)

    return {
        "report_type": "weekly",
        "period": f"{date_from} ~ {date_to}",
        "summary": {
            "member_count": len(by_member),
            "task_count": total_tasks,
            "total_hours": total_hours,
            "project_count": len(by_project),
        },
        "by_member": {k: {kk: vv for kk, vv in v.items() if kk != "tasks"} for k, v in by_member.items()},
        "by_project": by_project,
        "report_markdown": report_md,
    }


def _generate_weekly_insights(
    by_member: Dict,
    by_project: Dict,
    total_hours: float,
) -> List[str]:
    """生成周报洞察建议。"""
    insights = []

    if not by_member:
        insights.append("本周暂无工作记录，请确认团队成员已录入日志。")
        return insights

    # 找出工时最多和最少的成员
    sorted_members = sorted(by_member.items(), key=lambda x: x[1]["total_hours"], reverse=True)
    top_member = sorted_members[0]
    insights.append(
        f"本周工时最多的成员是 **{top_member[0]}**，"
        f"共 {format_hours(top_member[1]['total_hours'])}，"
        f"完成 {top_member[1]['task_count']} 项任务。"
    )

    if len(sorted_members) > 1:
        bottom_member = sorted_members[-1]
        if top_member[1]["total_hours"] > 0:
            ratio = bottom_member[1]["total_hours"] / top_member[1]["total_hours"]
            if ratio < 0.3:
                insights.append(
                    f"**{bottom_member[0]}** 工时偏低（{format_hours(bottom_member[1]['total_hours'])}），"
                    f"建议关注工作分配均衡性。"
                )

    # 项目分布
    if len(by_project) > 3:
        insights.append(
            f"本周涉及 {len(by_project)} 个项目，注意避免精力过于分散。"
        )

    # 人均工时
    if by_member:
        avg_hours = total_hours / len(by_member)
        if avg_hours > 45:
            insights.append(f"人均工时 {format_hours(avg_hours)}，偏高，注意团队工作强度。")
        elif avg_hours < 20:
            insights.append(f"人均工时 {format_hours(avg_hours)}，偏低，请确认日志录入是否完整。")

    return insights


# ============================================================
# 月报生成
# ============================================================

def generate_monthly_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """生成月报（仅付费版）。

    Args:
        data: 包含以下字段的字典：
            - month (str, optional): 月标识，如 "this"、"last"、"2024-01"

    Returns:
        包含 Markdown 月报和结构化数据的字典。
    """
    sub = check_subscription()
    if sub["tier"] != "paid":
        raise PermissionError(
            "月报汇总为付费版功能。当前为免费版，如需使用请升级至付费版（¥69/月）。"
        )

    now = datetime.now()
    month = data.get("month", "this")

    if month == "this":
        year, mon = now.year, now.month
    elif month == "last":
        if now.month == 1:
            year, mon = now.year - 1, 12
        else:
            year, mon = now.year, now.month - 1
    else:
        try:
            parts = month.split("-")
            year, mon = int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            raise ValueError(f"无效的月标识: {month!r}，请使用 YYYY-MM 格式")

    date_from, date_to = month_range_str(year, mon)

    # 获取日志
    logs = _load_worklogs()
    month_logs = _filter_logs_by_range(logs, date_from, date_to)

    team = _load_team()
    team_name = team["name"] if team else "团队"

    by_member = _aggregate_by_member(month_logs)
    by_project = _aggregate_by_project(month_logs)
    total_hours = sum(l.get("hours", 0) for l in month_logs)
    total_tasks = len(month_logs)

    # 按周聚合
    weekly_data: Dict[str, Dict[str, Any]] = {}
    for log in month_logs:
        log_date = datetime.strptime(log["date"], "%Y-%m-%d")
        iso_year, iso_week, _ = log_date.isocalendar()
        week_key = f"{iso_year}-W{iso_week:02d}"
        if week_key not in weekly_data:
            weekly_data[week_key] = {"hours": 0, "tasks": 0}
        weekly_data[week_key]["hours"] += log.get("hours", 0)
        weekly_data[week_key]["tasks"] += 1

    # 生成 Markdown
    md_lines = []
    md_lines.append(f"# {team_name} 月报")
    md_lines.append("")
    md_lines.append(f"**报告月份**: {year}年{mon}月")
    md_lines.append(f"**报告周期**: {date_from} ~ {date_to}")
    md_lines.append(f"**生成时间**: {now_str()}")
    md_lines.append("")

    # 执行摘要
    md_lines.append("## 执行摘要")
    md_lines.append("")
    md_lines.append(f"本月团队共 **{len(by_member)}** 人参与工作，"
                     f"完成 **{total_tasks}** 项任务，"
                     f"累计工时 **{format_hours(total_hours)}**，"
                     f"涉及 **{len(by_project)}** 个项目。")
    md_lines.append("")

    # 核心指标
    md_lines.append("## 核心指标")
    md_lines.append("")
    overview_headers = ["指标", "数值"]
    avg_hours = total_hours / len(by_member) if by_member else 0
    overview_rows = [
        ["参与人数", str(len(by_member))],
        ["任务总数", str(total_tasks)],
        ["总工时", format_hours(total_hours)],
        ["人均工时", format_hours(avg_hours)],
        ["涉及项目", str(len(by_project))],
        ["覆盖周数", str(len(weekly_data))],
    ]
    md_lines.append(build_markdown_table(overview_headers, overview_rows))
    md_lines.append("")

    # 周度趋势
    md_lines.append("## 周度趋势")
    md_lines.append("")
    if weekly_data:
        week_headers = ["周", "任务数", "工时"]
        week_rows = []
        for wk in sorted(weekly_data.keys()):
            wd = weekly_data[wk]
            week_rows.append([wk, str(wd["tasks"]), format_hours(wd["hours"])])
        md_lines.append(build_markdown_table(week_headers, week_rows))
        md_lines.append("")

        # 周度趋势图
        md_lines.append("```mermaid")
        md_lines.append("xychart-beta")
        md_lines.append(f'    title "月度周工时趋势（{year}年{mon}月）"')
        sorted_weeks = sorted(weekly_data.keys())
        md_lines.append('    x-axis [' + ", ".join(f'"{w}"' for w in sorted_weeks) + ']')
        md_lines.append('    y-axis "工时（小时）"')
        md_lines.append('    bar [' + ", ".join(str(weekly_data[w]["hours"]) for w in sorted_weeks) + ']')
        md_lines.append("```")
        md_lines.append("")

    # 成员统计
    md_lines.append("## 成员工作汇总")
    md_lines.append("")
    member_headers = ["成员", "任务数", "工时", "占比", "涉及项目"]
    member_rows = []
    for name, info in sorted(by_member.items(), key=lambda x: x[1]["total_hours"], reverse=True):
        pct = info["total_hours"] / total_hours if total_hours > 0 else 0
        member_rows.append([
            name,
            str(info["task_count"]),
            format_hours(info["total_hours"]),
            format_percentage(pct),
            ", ".join(info["projects"]) if info["projects"] else "-",
        ])
    md_lines.append(build_markdown_table(member_headers, member_rows))
    md_lines.append("")

    # 项目统计
    md_lines.append("## 项目工时分布")
    md_lines.append("")
    project_headers = ["项目", "任务数", "工时", "占比", "参与成员"]
    project_rows = []
    for proj, info in sorted(by_project.items(), key=lambda x: x[1]["total_hours"], reverse=True):
        pct = info["total_hours"] / total_hours if total_hours > 0 else 0
        project_rows.append([
            proj,
            str(info["task_count"]),
            format_hours(info["total_hours"]),
            format_percentage(pct),
            ", ".join(info["members"]),
        ])
    md_lines.append(build_markdown_table(project_headers, project_rows))
    md_lines.append("")

    # 项目工时饼图
    if by_project:
        md_lines.append("```mermaid")
        md_lines.append("pie title 项目工时分布")
        for proj, info in sorted(by_project.items(), key=lambda x: x[1]["total_hours"], reverse=True):
            md_lines.append(f'    "{proj}" : {info["total_hours"]:.1f}')
        md_lines.append("```")
        md_lines.append("")

    # 洞察
    md_lines.append("## 洞察与建议")
    md_lines.append("")
    insights = _generate_monthly_insights(by_member, by_project, weekly_data, total_hours)
    for insight in insights:
        md_lines.append(f"- {insight}")
    md_lines.append("")

    report_md = "\n".join(md_lines)

    return {
        "report_type": "monthly",
        "period": f"{date_from} ~ {date_to}",
        "summary": {
            "member_count": len(by_member),
            "task_count": total_tasks,
            "total_hours": total_hours,
            "project_count": len(by_project),
        },
        "report_markdown": report_md,
    }


def _generate_monthly_insights(
    by_member: Dict,
    by_project: Dict,
    weekly_data: Dict,
    total_hours: float,
) -> List[str]:
    """生成月报洞察建议。"""
    insights = []

    if not by_member:
        insights.append("本月暂无工作记录。")
        return insights

    # 工时趋势
    if weekly_data:
        weeks = sorted(weekly_data.keys())
        hours_trend = [weekly_data[w]["hours"] for w in weeks]
        if len(hours_trend) >= 2:
            if hours_trend[-1] > hours_trend[0] * 1.2:
                insights.append("本月工时呈上升趋势，团队工作量在增加。")
            elif hours_trend[-1] < hours_trend[0] * 0.8:
                insights.append("本月工时呈下降趋势，请关注团队产出。")
            else:
                insights.append("本月工时保持稳定。")

    # 工时分布
    member_hours = [v["total_hours"] for v in by_member.values()]
    if member_hours:
        max_h = max(member_hours)
        min_h = min(member_hours)
        if max_h > 0 and min_h / max_h < 0.3 and len(member_hours) > 1:
            insights.append("成员工时差异较大，建议优化任务分配。")

    # 项目集中度
    if by_project and total_hours > 0:
        sorted_projects = sorted(by_project.values(), key=lambda x: x["total_hours"], reverse=True)
        top_pct = sorted_projects[0]["total_hours"] / total_hours
        if top_pct > 0.6:
            insights.append(
                f"项目 **{sorted_projects[0]['project']}** 占据 "
                f"{format_percentage(top_pct)} 工时，为本月核心项目。"
            )

    return insights


# ============================================================
# 自定义范围报告
# ============================================================

def generate_custom_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """生成自定义日期范围的报告。

    Args:
        data: 包含以下字段的字典：
            - date_from (str): 起始日期（必填）
            - date_to (str): 结束日期（必填）

    Returns:
        包含 Markdown 报告和结构化数据的字典。
    """
    date_from = data.get("date_from")
    date_to = data.get("date_to")

    if not date_from or not date_to:
        raise ValueError("请提供起止日期（date_from 和 date_to 字段）")

    logs = _load_worklogs()
    range_logs = _filter_logs_by_range(logs, date_from, date_to)

    team = _load_team()
    team_name = team["name"] if team else "团队"

    by_member = _aggregate_by_member(range_logs)
    by_project = _aggregate_by_project(range_logs)
    total_hours = sum(l.get("hours", 0) for l in range_logs)

    md_lines = []
    md_lines.append(f"# {team_name} 工作报告")
    md_lines.append("")
    md_lines.append(f"**报告周期**: {date_from} ~ {date_to}")
    md_lines.append(f"**生成时间**: {now_str()}")
    md_lines.append("")

    md_lines.append("## 概览")
    md_lines.append("")
    overview_headers = ["指标", "数值"]
    overview_rows = [
        ["参与人数", str(len(by_member))],
        ["任务总数", str(len(range_logs))],
        ["总工时", format_hours(total_hours)],
        ["涉及项目", str(len(by_project))],
    ]
    md_lines.append(build_markdown_table(overview_headers, overview_rows))
    md_lines.append("")

    # 成员汇总
    md_lines.append("## 成员工作汇总")
    md_lines.append("")
    member_headers = ["成员", "任务数", "工时", "涉及项目"]
    member_rows = []
    for name, info in sorted(by_member.items()):
        member_rows.append([
            name,
            str(info["task_count"]),
            format_hours(info["total_hours"]),
            ", ".join(info["projects"]) if info["projects"] else "-",
        ])
    md_lines.append(build_markdown_table(member_headers, member_rows))
    md_lines.append("")

    report_md = "\n".join(md_lines)

    return {
        "report_type": "custom",
        "period": f"{date_from} ~ {date_to}",
        "summary": {
            "member_count": len(by_member),
            "task_count": len(range_logs),
            "total_hours": total_hours,
            "project_count": len(by_project),
        },
        "report_markdown": report_md,
    }


# ============================================================
# 命令行入口
# ============================================================

def main() -> None:
    """命令行入口函数。"""
    parser = create_base_parser("周报/月报生成工具")
    parser.add_argument(
        "--week",
        default=None,
        help="周标识（如 this, last, 2024-W03）",
    )
    parser.add_argument(
        "--month",
        default=None,
        help="月标识（如 this, last, 2024-01）",
    )
    args, _ = parser.parse_known_args()

    try:
        action = args.action

        if action == "weekly":
            data = {}
            try:
                data = read_input_data(args)
            except ValueError:
                pass
            if args.week:
                data["week"] = args.week
            if "week" not in data:
                data["week"] = "this"
            result = generate_weekly_report(data)
            output_success(result)

        elif action == "monthly":
            data = {}
            try:
                data = read_input_data(args)
            except ValueError:
                pass
            if args.month:
                data["month"] = args.month
            if "month" not in data:
                data["month"] = "this"
            result = generate_monthly_report(data)
            output_success(result)

        elif action == "custom":
            data = read_input_data(args)
            result = generate_custom_report(data)
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
