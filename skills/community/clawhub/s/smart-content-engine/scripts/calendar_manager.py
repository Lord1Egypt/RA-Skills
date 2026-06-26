#!/usr/bin/env python3
"""
content-engine 内容日历管理模块

提供内容发布日历的规划、查看、建议和导出功能。
"""

import csv
import io
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    format_platform_name,
    generate_id,
    get_data_file,
    get_month_range,
    get_week_range,
    load_input_data,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    truncate_text,
    validate_platform,
    write_json_file,
    PLATFORMS,
)


# ============================================================
# 数据文件路径
# ============================================================

CALENDAR_FILE = "calendar.json"
CONTENTS_FILE = "contents.json"


def _get_calendar() -> List[Dict[str, Any]]:
    """读取日历数据。"""
    return read_json_file(get_data_file(CALENDAR_FILE))


def _save_calendar(calendar: List[Dict[str, Any]]) -> None:
    """保存日历数据。"""
    write_json_file(get_data_file(CALENDAR_FILE), calendar)


def _get_contents() -> List[Dict[str, Any]]:
    """读取所有内容数据。"""
    return read_json_file(get_data_file(CONTENTS_FILE))


def _find_content(contents: List[Dict], content_id: str) -> Optional[Dict]:
    """根据 ID 查找内容。"""
    for c in contents:
        if c.get("id") == content_id:
            return c
    return None


# ============================================================
# 最佳发布时间建议
# ============================================================

# 各平台推荐发布时间（基于行业经验数据）
OPTIMAL_POSTING_TIMES = {
    "twitter": {
        "weekday": ["09:00", "12:00", "17:00", "20:00"],
        "weekend": ["10:00", "14:00", "19:00"],
        "best": "周二至周四 09:00-12:00",
        "avoid": "凌晨 00:00-06:00",
    },
    "linkedin": {
        "weekday": ["08:00", "10:00", "12:00", "17:00"],
        "weekend": ["10:00"],
        "best": "周二至周四 08:00-10:00",
        "avoid": "周末和晚间",
    },
    "wechat": {
        "weekday": ["07:30", "12:00", "18:00", "21:00"],
        "weekend": ["09:00", "12:00", "20:00"],
        "best": "工作日 18:00-21:00（通勤和休闲时段）",
        "avoid": "凌晨 01:00-06:00",
    },
    "blog": {
        "weekday": ["10:00", "14:00"],
        "weekend": ["10:00"],
        "best": "周一至周三 10:00",
        "avoid": "无特别限制",
    },
    "medium": {
        "weekday": ["08:00", "11:00", "14:00"],
        "weekend": ["10:00", "14:00"],
        "best": "周二至周四 08:00-11:00",
        "avoid": "周五下午和周末晚间",
    },
}

# 星期映射
WEEKDAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


# ============================================================
# 日历操作
# ============================================================

def plan_calendar(data: Dict[str, Any]) -> None:
    """添加内容发布计划到日历。

    必填字段: content_id, platform, date
    可选字段: time（发布时间，默认使用推荐时间）, note

    Args:
        data: 日历计划数据字典。
    """
    if not require_paid_feature("calendar", "内容日历"):
        return

    content_id = data.get("content_id") or data.get("id")
    platform = data.get("platform", "")
    date = data.get("date", "")

    if not content_id:
        output_error("内容ID（content_id）为必填字段", code="VALIDATION_ERROR")
        return

    if not platform:
        output_error("目标平台（platform）为必填字段", code="VALIDATION_ERROR")
        return

    if not date:
        output_error("发布日期（date）为必填字段，格式: YYYY-MM-DD", code="VALIDATION_ERROR")
        return

    try:
        platform = validate_platform(platform)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    # 校验日期格式
    try:
        plan_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        output_error("日期格式无效，请使用 YYYY-MM-DD 格式", code="VALIDATION_ERROR")
        return

    # 检查内容是否存在
    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    # 确定发布时间
    time = data.get("time", "")
    if not time:
        # 使用推荐时间
        weekday = plan_date.weekday()
        times = OPTIMAL_POSTING_TIMES.get(platform, {})
        if weekday < 5:
            suggested_times = times.get("weekday", ["10:00"])
        else:
            suggested_times = times.get("weekend", ["10:00"])
        time = suggested_times[0] if suggested_times else "10:00"

    # 创建日历条目
    calendar = _get_calendar()
    entry = {
        "id": generate_id("CL"),
        "content_id": content_id,
        "content_title": truncate_text(content.get("title", ""), 50),
        "platform": platform,
        "platform_name": format_platform_name(platform),
        "date": date,
        "time": time,
        "weekday": WEEKDAY_NAMES[plan_date.weekday()],
        "note": data.get("note", ""),
        "status": "planned",
        "created_at": now_iso(),
    }

    calendar.append(entry)
    _save_calendar(calendar)

    output_success({
        "message": f"已添加日历计划: {date} {time} 发布到 {format_platform_name(platform)}",
        "entry": entry,
    })


def view_calendar(data: Optional[Dict[str, Any]] = None) -> None:
    """查看内容日历。

    可选字段: view（week/month，默认 week）, date（起始日期，默认今天）

    Args:
        data: 可选的查看参数字典。
    """
    if not require_paid_feature("calendar", "内容日历"):
        return

    view_type = data.get("view", "week") if data else "week"
    base_date = data.get("date", today_str()) if data else today_str()

    calendar = _get_calendar()

    # 确定日期范围
    if view_type == "month":
        date_range = get_month_range(base_date)
    else:
        date_range = get_week_range(base_date)

    start = date_range["start"]
    end = date_range["end"]

    # 过滤日期范围内的条目
    filtered = [
        e for e in calendar
        if start <= e.get("date", "") <= end
    ]

    # 按日期和时间排序
    filtered.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))

    # 按日期分组
    grouped = {}
    current = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")

    while current <= end_dt:
        date_str = current.strftime("%Y-%m-%d")
        weekday = WEEKDAY_NAMES[current.weekday()]
        day_entries = [e for e in filtered if e.get("date") == date_str]
        grouped[date_str] = {
            "weekday": weekday,
            "entries": day_entries,
            "count": len(day_entries),
        }
        current += timedelta(days=1)

    # 生成 Markdown 视图
    view_title = "月度日历" if view_type == "month" else "周日历"
    report_lines = [f"# 内容{view_title}（{start} ~ {end}）", ""]

    for date_str, day_data in grouped.items():
        weekday = day_data["weekday"]
        entries = day_data["entries"]

        if entries:
            report_lines.append(f"## {date_str}（{weekday}）")
            report_lines.append("")
            for e in entries:
                status_icon = "✅" if e.get("status") == "published" else "📅"
                report_lines.append(
                    f"- {status_icon} **{e.get('time', '')}** "
                    f"[{e.get('platform_name', '')}] "
                    f"{e.get('content_title', '')}"
                )
                if e.get("note"):
                    report_lines.append(f"  > {e['note']}")
            report_lines.append("")
        else:
            report_lines.append(f"## {date_str}（{weekday}）— 无计划")
            report_lines.append("")

    # 统计
    total_planned = len(filtered)
    platform_dist = {}
    for e in filtered:
        pname = e.get("platform_name", "")
        platform_dist[pname] = platform_dist.get(pname, 0) + 1

    report = "\n".join(report_lines)

    output_success({
        "view_type": view_type,
        "date_range": date_range,
        "total_planned": total_planned,
        "platform_distribution": platform_dist,
        "calendar_view": report,
        "entries": filtered,
    })


def suggest_times(data: Dict[str, Any]) -> None:
    """建议最佳发布时间。

    可选字段: platform（不指定则返回所有平台的建议）, date

    Args:
        data: 可选的参数字典。
    """
    platform_filter = data.get("platform") if data else None
    target_date = data.get("date", today_str()) if data else today_str()

    try:
        dt = datetime.strptime(target_date, "%Y-%m-%d")
        weekday = dt.weekday()
        weekday_name = WEEKDAY_NAMES[weekday]
        is_weekend = weekday >= 5
    except ValueError:
        dt = datetime.now()
        weekday = dt.weekday()
        weekday_name = WEEKDAY_NAMES[weekday]
        is_weekend = weekday >= 5

    suggestions = []
    platforms = [platform_filter] if platform_filter else PLATFORMS

    for platform in platforms:
        try:
            platform = validate_platform(platform)
        except ValueError:
            continue

        times_config = OPTIMAL_POSTING_TIMES.get(platform, {})
        time_key = "weekend" if is_weekend else "weekday"
        recommended_times = times_config.get(time_key, ["10:00"])

        suggestions.append({
            "platform": platform,
            "platform_name": format_platform_name(platform),
            "date": target_date,
            "weekday": weekday_name,
            "recommended_times": recommended_times,
            "best_time": times_config.get("best", ""),
            "avoid": times_config.get("avoid", ""),
        })

    output_success({
        "message": f"{target_date}（{weekday_name}）发布时间建议",
        "suggestions": suggestions,
    })


def export_calendar(data: Optional[Dict[str, Any]] = None) -> None:
    """导出内容日历。

    可选字段: format（markdown/csv，默认 markdown）, file_path, view（week/month）, date

    Args:
        data: 可选的导出参数字典。
    """
    if not require_paid_feature("calendar", "内容日历"):
        return

    export_format = data.get("format", "markdown") if data else "markdown"
    file_path = data.get("file_path") if data else None
    view_type = data.get("view", "month") if data else "month"
    base_date = data.get("date", today_str()) if data else today_str()

    calendar = _get_calendar()

    # 确定日期范围
    if view_type == "month":
        date_range = get_month_range(base_date)
    else:
        date_range = get_week_range(base_date)

    start = date_range["start"]
    end = date_range["end"]

    filtered = [
        e for e in calendar
        if start <= e.get("date", "") <= end
    ]
    filtered.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))

    if export_format == "csv":
        output_content = _export_csv(filtered)
    else:
        output_content = _export_markdown(filtered, start, end)

    if file_path:
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(output_content)
            output_success({
                "message": f"日历已导出到 {file_path}",
                "format": export_format,
                "entries_count": len(filtered),
            })
        except IOError as e:
            output_error(f"导出失败: {e}", code="EXPORT_ERROR")
    else:
        output_success({
            "content": output_content,
            "format": export_format,
            "entries_count": len(filtered),
        })


def _export_markdown(entries: List[Dict[str, Any]], start: str, end: str) -> str:
    """导出为 Markdown 格式。

    Args:
        entries: 日历条目列表。
        start: 起始日期。
        end: 结束日期。

    Returns:
        Markdown 格式的日历内容。
    """
    lines = [f"# 内容发布日历（{start} ~ {end}）", ""]
    lines.append("| 日期 | 星期 | 时间 | 平台 | 内容 | 状态 | 备注 |")
    lines.append("|------|------|------|------|------|------|------|")

    for e in entries:
        status = "已发布" if e.get("status") == "published" else "已计划"
        lines.append(
            f"| {e.get('date', '')} "
            f"| {e.get('weekday', '')} "
            f"| {e.get('time', '')} "
            f"| {e.get('platform_name', '')} "
            f"| {e.get('content_title', '')} "
            f"| {status} "
            f"| {e.get('note', '')} |"
        )

    # 付费版: 添加 Mermaid Gantt 图
    sub = check_subscription()
    if sub["tier"] == "paid" and entries:
        lines.append("")
        lines.append("## 时间线视图")
        lines.append("")
        lines.append(_generate_gantt_chart(entries))

    return "\n".join(lines)


def _generate_gantt_chart(entries: List[Dict[str, Any]]) -> str:
    """生成 Mermaid Gantt 时间线图。

    Args:
        entries: 日历条目列表。

    Returns:
        Mermaid Gantt 图代码块。
    """
    lines = ["```mermaid", "gantt", "    title 内容发布时间线", "    dateFormat YYYY-MM-DD"]

    # 按平台分组
    platforms_seen = {}
    for e in entries:
        platform = e.get("platform_name", "其他")
        if platform not in platforms_seen:
            platforms_seen[platform] = []
        platforms_seen[platform].append(e)

    for platform, platform_entries in platforms_seen.items():
        lines.append(f"    section {platform}")
        for e in platform_entries:
            title = e.get("content_title", "内容")[:20]
            date = e.get("date", today_str())
            status = "done," if e.get("status") == "published" else ""
            # Gantt 条目格式: 任务名 :状态, 开始日期, 持续时间
            lines.append(f"    {title} :{status} {date}, 1d")

    lines.append("```")
    return "\n".join(lines)


def _export_csv(entries: List[Dict[str, Any]]) -> str:
    """导出为 CSV 格式。

    Args:
        entries: 日历条目列表。

    Returns:
        CSV 格式的日历内容。
    """
    output = io.StringIO()
    fieldnames = ["date", "weekday", "time", "platform_name", "content_title", "status", "note", "content_id"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for e in entries:
        row = {k: e.get(k, "") for k in fieldnames}
        writer.writerow(row)

    return output.getvalue()


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine 内容日历管理")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "plan": lambda: plan_calendar(data or {}),
        "view": lambda: view_calendar(data),
        "suggest": lambda: suggest_times(data),
        "export": lambda: export_calendar(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
