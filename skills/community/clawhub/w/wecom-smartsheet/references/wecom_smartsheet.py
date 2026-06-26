#!/usr/bin/env python3
"""
企微智能表格 推送+提醒 一体化脚本
功能：
  1. 向3个智能表格推送数据（Webhook方式）
  2. 向3个企微群发送提醒通知（群机器人Webhook）
  3. 支持按角色场景发送不同提醒
  4. 可作为定时巡检的基础

用法：
  python3 wecom_smartsheet.py --table expense --action push --data '{"报销描述":"测试","金额":"100"}'
  python3 wecom_smartsheet.py --table task --action push --data '{"任务详细描述":"测试任务"}'
  python3 wecom_smartsheet.py --table video --action push --data '{"AI 生成的视频标题":"测试视频"}'
  python3 wecom_smartsheet.py --action notify --notify-type expense --message "费用审批提醒：xxx"
  python3 wecom_smartsheet.py --action push-and-notify --table expense --data '...' --message '...'
"""

import json
import argparse
import requests
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# 配置区 — 首次使用请替换为你自己的 Webhook Key
# ═══════════════════════════════════════════════════════════

# 表格 Webhook URL（接收数据）
TABLE_WEBHOOKS = {
    "expense": "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={EXPENSE_WEBHOOK_KEY}",
    "task": "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={TASK_WEBHOOK_KEY}",
    "video": "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={VIDEO_WEBHOOK_KEY}",
}

# 群机器人 Webhook URL（发送通知）
BOT_WEBHOOKS = {
    "expense": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={EXPENSE_BOT_KEY}",
    "task": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={TASK_BOT_KEY}",
    "video": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={VIDEO_BOT_KEY}",
}

# 字段映射：字段标题 → 字段ID
FIELD_MAPS = {
    "expense": {
        "报销描述": "f95bql",
        "报销费用类型": "fSIkwz",
        "费用类型": "fV2Vy0",
        "费用内容": "ftQMc5",
        "金额": "ftk5Tx",
        "实发工资金额": "fv0Ji4",
        "单据图片": "ffC9Tb",
        "收款户名": "fQgUks",
        "收款人开户银行": "fFh8FX",
        "收款人银行账号": "fpe6NV",
        "财务初审人": "fMAfWQ",
        "财务初审意见": "f2hMiW",
        "终审人员": "fn8TJd",
        "终审人员意见": "ff1LL6",
        "终审结果": "fMRZPT",
        "终审审批时间": "fs4s7u",
        "支付账户": "fBOypp",
        "银行制单日期": "fgbqSn",
        "支付人": "fbA3YP",
        "付款截止日期": "fgeUSZ",
        "支付人意见": "f4JIH4",
        "支付日期": "fafRRt",
        "支付凭据": "fowtyf",
        "流程结果": "fG5K0s",
        "终审日期": "fy8sMG",
        "审批进度": "fZPqRZ",
    },
    "task": {
        "任务详细描述": "ftQMc5",
        "填写任务最新进展": "fAUNqS",
        "填写时间": "fJtBHe",
        "完全责任人": "fMAfWQ",
        "任务结果交付给谁": "fvMIN1",
        "任务重要紧急分类": "fLjDXp",
        "任务类型": "ftk5Tx",
        "任务优先级": "f8lJy9",
        "图片": "far6pU",
        "协同任务完成的人": "fn8TJd",
        "不参与任务但需要知会的人": "fsaQFC",
        "计划开始时间": "fSP1Xe",
        "计划结束时间": "fIH343",
        "实际开始时间": "fnmp0N",
        "实际结束时间": "fNxWUG",
        "任务工作小时数": "f5mcXr",
        "任务状态": "fp6iMs",
        "进度": "f9ftBb",
        "每周回顾任务": "fOinuX",
        "每月回顾任务": "furcM5",
        "任务完成总结": "f2CRNT",
        "备注": "fCpF71",
    },
    "video": {
        "视频类别": "fIxg8J",
        "逐字稿文档": "flj0f9",
        "AI 生成的视频标题": "fRZCUc",
        "逐字稿负责人": "ftQMc5",
        "文字稿提供日期": "ftk5Tx",
        "视频营销完全责任人": "fExzxn",
        "视频生成完全责任人": "f0WI70",
        "音频负责人": "ffFwIh",
        "音频制作计划完成日期": "fGP81d",
        "音频制作实际完成日期": "fgbWRh",
        "视频生成负责人": "fn8TJd",
        "视频制作计划完成日期": "faGcmb",
        "视频制作实际完成日期": "f8SU87",
        "后期合成负责人": "fsPk4D",
        "后期计划完成日期": "fRGWEC",
        "后期实际完成日期": "fdRqlx",
        "计划上传发布日期": "fa4rBU",
        "发布负责人": "fQg3so",
        "实际上传发布日期和时间": "fh0mD5",
        "备注和总结": "fJSKId",
    },
}

# 选择类型字段的可选值（用于校验）
SELECT_OPTIONS = {
    "expense": {
        "报销费用类型": ["房租税金", "办公用品", "差旅费", "餐饮费", "其他"],
        "终审结果": ["同意", "驳回", "待审批"],
        "支付人意见": ["已支付", "待支付"],
        "流程结果": ["已完成", "进行中", "已取消"],
        "审批进度": ["待初审", "初审通过", "待终审", "终审通过", "终审驳回"],
    },
    "task": {
        "任务重要紧急分类": ["重要紧急", "重要不紧急", "紧急不重要", "不紧急不重要"],
        "任务类型": ["财务类", "市场与销售类", "人力资源类", "技术类", "行政类"],
        "任务优先级": ["星标任务（极其重要紧急）", "高", "中", "低"],
        "任务状态": ["未开始", "进行中", "已完成", "已取消"],
    },
    "video": {
        "视频类别": ["短视频", "长视频", "直播"],
    },
}


# ═══════════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════════

def date_to_timestamp(date_str: str) -> str:
    """日期字符串 → 毫秒时间戳字符串（用于Webhook）
    
    支持格式：
      - "2026-04-28" → 当天 00:00:00
      - "2026-04-28 09:00:00" → 精确时间
    """
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return str(int(dt.timestamp() * 1000))
        except ValueError:
            continue
    raise ValueError(f"无法解析日期: {date_str}")


def convert_field_value(table: str, field_title: str, value):
    """将用户友好的字段值转换为 Webhook 要求的格式
    
    规则：
      - 选择类型字段 → [{"text": "值"}]
      - 人员类型字段 → [{"user_id": "值"}]（空字符串=不指定）
      - 日期类型字段 → 毫秒时间戳字符串
      - 数值类型字段 → 数字
      - 文本类型字段 → 字符串
    """
    # 选择类型字段
    if table in SELECT_OPTIONS and field_title in SELECT_OPTIONS[table]:
        if isinstance(value, list):
            return [{"text": v} for v in value]
        return [{"text": str(value)}]

    # 人员类型字段（包含"人"的字段）
    person_keywords = ["人", "负责人", "审批人"]
    if any(kw in field_title for kw in person_keywords):
        if isinstance(value, list):
            return [{"user_id": v} for v in value]
        if value == "" or value is None:
            return [{"user_id": ""}]
        return [{"user_id": str(value)}]

    # 日期类型字段（包含"日期"/"时间"的字段）
    date_keywords = ["日期", "时间"]
    if any(kw in field_title for kw in date_keywords):
        if isinstance(value, (int, float)):
            return str(int(value))
        if isinstance(value, str) and value.isdigit():
            return value
        try:
            return date_to_timestamp(str(value))
        except ValueError:
            return str(value)

    # 进度字段（小数）
    if field_title == "进度":
        try:
            return float(value)
        except (ValueError, TypeError):
            return value

    # 工作小时数字段（整数）
    if field_title == "任务工作小时数":
        try:
            return int(value)
        except (ValueError, TypeError):
            return value

    # 图片/附件字段
    if field_title in ["单据图片", "图片", "支付凭据"]:
        return []  # Webhook 不支持直接上传附件

    # 默认文本
    return str(value)


def build_webhook_payload(table: str, data: dict) -> dict:
    """构建 Webhook 请求体
    
    Args:
        table: 表格标识 (expense/task/video)
        data: 字段标题→值 的字典
    
    Returns:
        Webhook 请求体 JSON
    """
    field_map = FIELD_MAPS[table]
    values = {}

    for field_title, value in data.items():
        if field_title not in field_map:
            print(f"  ⚠️ 字段 '{field_title}' 不在映射表中，跳过")
            continue
        field_id = field_map[field_title]
        values[field_id] = convert_field_value(table, field_title, value)

    return {"add_records": [{"values": values}]}


def push_to_table(table: str, data: dict) -> dict:
    """向智能表格推送数据（不含追踪）
    
    Args:
        table: 表格标识 (expense/task/video)
        data: 字段标题→值 的字典
    
    Returns:
        API 响应
    """
    url = TABLE_WEBHOOKS[table]
    payload = build_webhook_payload(table, data)
    
    print(f"📤 推送到 [{table}] 表格...")
    print(f"   数据: {json.dumps(data, ensure_ascii=False)}")
    
    resp = requests.post(url, json=payload, timeout=10)
    result = resp.json()
    
    if result.get("errcode") == 0:
        record_id = result.get("add_records", [{}])[0].get("record_id", "")
        print(f"   ✅ 成功! record_id={record_id}")
    else:
        print(f"   ❌ 失败: errcode={result.get('errcode')}, errmsg={result.get('errmsg')}")
    
    return result


def send_notification(notify_type: str, title: str, fields: list, mention_list: list = None) -> dict:
    """向企微群发送 Markdown 格式提醒通知
    
    Args:
        notify_type: 通知类型 (expense/task/video)
        title: 通知标题
        fields: [(label, value, color), ...] 格式的字段列表
                color: "info"/"warning"/"comment" 或 None
        mention_list: @指定成员的userid列表
    
    Returns:
        API 响应
    """
    url = BOT_WEBHOOKS[notify_type]
    
    # 构建 Markdown 内容
    content = f"**{title}**\n"
    for label, value, color in fields:
        if color:
            content += f"> {label}：<font color=\"{color}\">{value}</font>\n"
        else:
            content += f"> {label}：{value}\n"
    
    payload = {
        "msgtype": "markdown",
        "markdown": {"content": content.strip()}
    }
    if mention_list:
        payload["mentioned_list"] = mention_list
    
    print(f"🔔 发送 [{notify_type}] 群通知...")
    resp = requests.post(url, json=payload, timeout=10)
    result = resp.json()
    
    if result.get("errcode") == 0:
        print(f"   ✅ 通知发送成功!")
    else:
        print(f"   ❌ 通知失败: {result}")
    
    return result


# ═══════════════════════════════════════════════════════════
# 场景化提醒模板
# ═══════════════════════════════════════════════════════════

def notify_expense_pending(description: str, amount: str, deadline: str, 
                           applicant: str = "", reviewer: str = "") -> dict:
    """费用审批提醒 - 发给审批人/责任人"""
    fields = [
        ("报销描述", description, "info"),
        ("费用申请人", applicant, None),
        ("金额", f"¥{amount}", "warning"),
        ("付款截止", deadline, "warning"),
        ("审批进度", "待审批", "comment"),
    ]
    if reviewer:
        fields.append(("审批人", reviewer, None))
    return send_notification("expense", "【费用审批提醒】", fields)


def notify_task_deadline(task_name: str, responsible: str, deadline: str,
                         priority: str = "", progress: str = "") -> dict:
    """工作任务截止提醒 - 发给责任人"""
    fields = [
        ("任务", task_name, "info"),
        ("责任人", responsible, None),
        ("截止日期", deadline, "warning"),
    ]
    if priority:
        fields.append(("优先级", priority, "warning"))
    if progress:
        fields.append(("当前进度", progress, "comment"))
    return send_notification("task", "【工作任务提醒】", fields)


def notify_video_milestone(video_title: str, stage: str, deadline: str,
                           responsible: str = "") -> dict:
    """视频制作里程碑提醒 - 发给对应阶段负责人"""
    fields = [
        ("视频标题", video_title, "info"),
        ("当前阶段", stage, "info"),
        ("截止日期", deadline, "warning"),
    ]
    if responsible:
        fields.append(("负责人", responsible, None))
    return send_notification("video", "【视频制作提醒】", fields)


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="企微智能表格 推送+提醒 一体化工具")
    parser.add_argument("--action", choices=["push", "notify", "push-and-notify"], 
                        required=True, help="操作类型")
    parser.add_argument("--table", choices=["expense", "task", "video"],
                        help="目标表格")
    parser.add_argument("--data", type=str, help="推送数据 (JSON字符串，用字段标题作key)")
    parser.add_argument("--notify-type", choices=["expense", "task", "video"],
                        help="通知类型（notify时使用）")
    parser.add_argument("--message", type=str, help="通知内容")
    
    args = parser.parse_args()
    
    if args.action in ["push", "push-and-notify"]:
        if not args.table or not args.data:
            print("❌ push 操作需要 --table 和 --data 参数")
            return
        
        data = json.loads(args.data)
        result = push_to_table(args.table, data)
        
        if args.action == "push-and-notify" and result.get("errcode") == 0:
            # 推送成功后自动发送通知
            if args.message:
                send_notification(args.table, args.message, [])
            else:
                # 根据表格类型自动生成通知
                auto_notify_map = {
                    "expense": lambda d: notify_expense_pending(
                        d.get("报销描述", "新费用申请"),
                        d.get("金额", "0"),
                        d.get("付款截止日期", "待定"),
                        d.get("费用申请人", ""),
                    ),
                    "task": lambda d: notify_task_deadline(
                        d.get("任务详细描述", "新任务"),
                        d.get("完全责任人", ""),
                        d.get("计划结束时间", "待定"),
                        d.get("任务优先级", ""),
                    ),
                    "video": lambda d: notify_video_milestone(
                        d.get("AI 生成的视频标题", "新视频"),
                        "制作中",
                        d.get("视频制作计划完成日期", "待定"),
                        d.get("视频生成完全责任人", ""),
                    ),
                }
                auto_notify_map[args.table](data)
    
    elif args.action == "notify":
        if not args.notify_type or not args.message:
            print("❌ notify 操作需要 --notify-type 和 --message 参数")
            return
        send_notification(args.notify_type, args.message, [])


# ═══════════════════════════════════════════════════════════
# 本地到期追踪（推送数据时同步记录）
# ═══════════════════════════════════════════════════════════

import os

TRACK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wecom_deadline_tracker.json")


def load_tracker() -> list:
    """加载本地到期追踪记录"""
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tracker(records: list):
    """保存本地到期追踪记录"""
    with open(TRACK_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def track_record(table: str, data: dict, record_id: str = ""):
    """推送成功后，记录到期信息到本地"""
    tracker = load_tracker()
    
    # 日期字段名映射
    deadline_fields = {
        "expense": "付款截止日期",
        "task": "计划结束时间",
        "video": "视频制作计划完成日期",
    }
    
    deadline_key = deadline_fields.get(table, "")
    deadline_val = data.get(deadline_key, "")
    
    # 名称字段映射
    name_fields = {
        "expense": "报销描述",
        "task": "任务详细描述",
        "video": "AI 生成的视频标题",
    }
    name_key = name_fields.get(table, "")
    name_val = data.get(name_key, "")
    
    # 责任人字段映射
    responsible_fields = {
        "expense": "财务初审人",
        "task": "完全责任人",
        "video": "视频生成完全责任人",
    }
    resp_key = responsible_fields.get(table, "")
    resp_val = data.get(resp_key, "")
    
    entry = {
        "table": table,
        "record_id": record_id,
        "name": name_val,
        "deadline": deadline_val,
        "responsible": resp_val,
        "data": data,
        "tracked_at": datetime.now().isoformat(),
        "notified": False,
    }
    
    tracker.append(entry)
    save_tracker(tracker)
    print(f"   📌 已记录到期追踪: {name_val} → 截止 {deadline_val}")


def push_to_table(table: str, data: dict, track: bool = True) -> dict:
    """向智能表格推送数据
    
    Args:
        table: 表格标识 (expense/task/video)
        data: 字段标题→值 的字典
        track: 是否同步记录到期信息到本地
    
    Returns:
        API 响应
    """
    url = TABLE_WEBHOOKS[table]
    payload = build_webhook_payload(table, data)
    
    print(f"📤 推送到 [{table}] 表格...")
    print(f"   数据: {json.dumps(data, ensure_ascii=False)}")
    
    resp = requests.post(url, json=payload, timeout=10)
    result = resp.json()
    
    if result.get("errcode") == 0:
        record_id = result.get("add_records", [{}])[0].get("record_id", "")
        print(f"   ✅ 成功! record_id={record_id}")
        if track:
            track_record(table, data, record_id)
    else:
        print(f"   ❌ 失败: errcode={result.get('errcode')}, errmsg={result.get('errmsg')}")
    
    return result


def get_upcoming_deadlines(days: int = 3) -> list:
    """获取未来N天内即将到期的记录"""
    tracker = load_tracker()
    now = datetime.now()
    upcoming = []
    
    for entry in tracker:
        deadline = entry.get("deadline", "")
        if not deadline:
            continue
        try:
            # 支持多种日期格式
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    dl = datetime.strptime(deadline, fmt)
                    break
                except ValueError:
                    continue
            else:
                continue
            
            delta = (dl - now).days
            if 0 <= delta <= days and not entry.get("notified", False):
                entry["days_remaining"] = delta
                upcoming.append(entry)
        except Exception:
            continue
    
    return upcoming


if __name__ == "__main__":
    main()
