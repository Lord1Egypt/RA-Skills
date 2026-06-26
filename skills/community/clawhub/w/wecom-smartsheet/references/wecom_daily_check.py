#!/usr/bin/env python3
"""
企微智能表格 定时巡检脚本
功能：检查本地追踪的到期信息，按表格类型分别推送提醒到对应企微群

使用方式：通过 WorkBuddy Automation 每天 09:00 定时触发
"""

import sys
import os
import json
import requests
from datetime import datetime

# 添加 references 目录到路径（与 wecom_smartsheet.py 同目录）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wecom_smartsheet import get_upcoming_deadlines

# 群机器人 Webhook - 每个表格对应不同群（首次使用请替换为你自己的 Bot Key）
BOT_WEBHOOKS = {
    "expense": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={EXPENSE_BOT_KEY}",
    "task": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={TASK_BOT_KEY}",
    "video": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={VIDEO_BOT_KEY}",
}

TABLE_NAMES = {
    "expense": "费用审批系统",
    "task": "工作任务系统",
    "video": "视频制作工作流",
}

# 每个群的专属标题和 emoji
TABLE_HEADERS = {
    "expense": "💰 费用审批提醒",
    "task": "📌 工作任务提醒",
    "video": "🎬 视频制作提醒",
}

# Tracker 文件路径（脚本在 references/ 子目录，tracker 在技能根目录）
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 技能文件夹根目录
TRACKER_FILE = os.path.join(SCRIPT_DIR, "wecom_deadline_tracker.json")


def load_tracker() -> list:
    """加载本地追踪记录"""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tracker(records: list):
    """保存本地追踪记录"""
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def send_to_bot(table: str, content: str) -> bool:
    """发送 markdown 消息到对应群的机器人"""
    webhook_url = BOT_WEBHOOKS.get(table)
    if not webhook_url:
        print(f"  ⚠️ 未找到 [{table}] 的群机器人配置")
        return False

    payload = {
        "msgtype": "markdown",
        "markdown": {"content": content.strip()}
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        result = resp.json()
        if result.get("errcode") == 0:
            print(f"  ✅ {TABLE_NAMES.get(table, table)} 通知已发送")
            return True
        else:
            print(f"  ❌ {TABLE_NAMES.get(table, table)} 发送失败: {result}")
            return False
    except Exception as e:
        print(f"  ❌ {TABLE_NAMES.get(table, table)} 发送异常: {e}")
        return False


def build_deadline_content(table: str, entries: list) -> str:
    """根据表格类型构建到期提醒内容"""
    header = TABLE_HEADERS.get(table, "📋 提醒")
    table_name = TABLE_NAMES.get(table, table)
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"**{header}**\n> 日期：{today}\n\n"

    if not entries:
        content += "> 暂无即将到期的项目 ✅\n\n"
    else:
        for i, entry in enumerate(entries, 1):
            days_left = entry.get("days_remaining", "?")
            name = entry.get("name", "未命名")
            deadline = entry.get("deadline", "未知")
            responsible = entry.get("responsible", "")

            urgency = "🔴" if days_left <= 1 else "🟡" if days_left <= 2 else "🟢"
            content += f"{urgency} **{name}**\n"
            content += f"   截止：<font color=\"warning\">{deadline}</font>（剩余{days_left}天）\n"
            if responsible:
                content += f"   责任人：{responsible}\n"
            content += "\n"

    content += "_WorkBuddy 定时巡检_"
    return content


def build_summary_content(table: str, total_tracked: int, upcoming_count: int) -> str:
    """构建无到期记录时的日常摘要"""
    header = TABLE_HEADERS.get(table, "📋 提醒")
    table_name = TABLE_NAMES.get(table, table)
    today = datetime.now().strftime("%Y-%m-%d %A")

    # 按表格类型定制摘要文案
    summaries = {
        "expense": f"**{header}**\n> 日期：{today}\n\n> 费用追踪记录：{total_tracked} 条\n> 即将到期：{upcoming_count} 条（3天内）\n\n> 今日暂无紧急费用审批 ✅",
        "task": f"**{header}**\n> 日期：{today}\n\n> 任务追踪记录：{total_tracked} 条\n> 即将到期：{upcoming_count} 条（3天内）\n\n> 今日暂无紧急到期任务 ✅",
        "video": f"**{header}**\n> 日期：{today}\n\n> 视频追踪记录：{total_tracked} 条\n> 即将到期：{upcoming_count} 条（3天内）\n\n> 今日暂无紧急视频制作 ✅",
    }

    content = summaries.get(table, f"**{header}**\n> 日期：{today}\n> 追踪：{total_tracked} 条")
    content += "\n\n_WorkBuddy 定时巡检_"
    return content


def send_deadline_alerts(days: int = 3):
    """检查并推送即将到期的提醒 - 按表格类型分别发送到对应群"""
    print(f"\n🔍 巡检时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    upcoming = get_upcoming_deadlines(days)
    tracker = load_tracker()
    total_tracked = len(tracker)

    # 按表格类型分组
    by_table = {}
    for entry in upcoming:
        table = entry.get("table", "unknown")
        by_table.setdefault(table, []).append(entry)

    if upcoming:
        print(f"  ⚠️ 发现 {len(upcoming)} 条即将到期的记录")
    else:
        print(f"  ✅ 没有即将到期的任务")

    # 逐表发送 - 每个表格发到自己的群
    for table in ["task", "video", "expense"]:
        entries = by_table.get(table, [])
        table_name = TABLE_NAMES.get(table, table)

        if entries:
            # 有到期记录 → 发送到期提醒
            content = build_deadline_content(table, entries)
            success = send_to_bot(table, content)

            # 标记已通知
            if success:
                for entry in tracker:
                    if entry.get("record_id") in [e.get("record_id") for e in entries]:
                        entry["notified"] = True
                save_tracker(tracker)
        else:
            # 无到期记录 → 发送日常摘要（也发到对应群）
            content = build_summary_content(table, total_tracked, len(upcoming))
            send_to_bot(table, content)


if __name__ == "__main__":
    send_deadline_alerts(3)
