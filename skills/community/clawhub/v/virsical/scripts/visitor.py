"""
Virsical 访客管理模块。

提供访客邀请列表查询功能。
"""

import json
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

from .virsical_client import VirsicalClient

CST = timezone(timedelta(hours=8))

# 访客状态映射（字符串键）
VISITOR_STATUS_MAP = {
    "12": "审批中",
    "6": "已拒绝",
    "8": "处理中",
    "0": "未开始",
    "7": "已过期",
    "1": "未到访",
    "2": "已签到",
    "3": "已签出",
    "4": "已取消",
    "10": "失败",
    "9": "系统签出",
}


def _to_ms_timestamp(dt: datetime) -> int:
    """转换 datetime 为毫秒时间戳。"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CST)
    return int(dt.timestamp() * 1000)


def _format_timestamp(ts) -> str:
    """格式化毫秒时间戳为可读时间。"""
    try:
        ts_int = int(ts)
        dt = datetime.fromtimestamp(ts_int / 1000, CST)
        return f"{dt.month}月{dt.day}日 {dt.hour:02d}:{dt.minute:02d}"
    except Exception:
        return str(ts)


def _get_tenant_id() -> int:
    """获取当前用户的 tenant_id。"""
    from .auth_manager import TOKEN_FILE
    try:
        if TOKEN_FILE.exists():
            data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
            token = data.get("virsical:default", {})
            return token.get("tenantId", 0)
    except Exception:
        pass
    return 0


def list_visitors(
    visitor_name: Optional[str] = None,
    start_date: Optional[int] = None,
    end_date: Optional[int] = None,
    page: int = 1,
    rows: int = 30,
) -> dict:
    """查询访客邀请列表。

    Args:
        visitor_name: 访客姓名（模糊搜索）
        start_date: 开始日期（毫秒时间戳），默认当前时间 -30 天
        end_date: 结束日期（毫秒时间戳），默认当前时间 +30 天
        page: 页码
        rows: 每页条数，默认 30

    Returns:
        访客列表
    """
    client = VirsicalClient()
    tenant_id = _get_tenant_id()

    now_ms = int(time.time() * 1000)
    if start_date is None:
        start_date = now_ms - 30 * 24 * 3600 * 1000  # 默认查过去30天
    if end_date is None:
        end_date = now_ms + 30 * 24 * 3600 * 1000  # 到未来30天

    query = {
        "rows": rows,
        "from": 1,
        "locationId": 0,
        "companyId": tenant_id,
    }

    if visitor_name:
        query["visitorName"] = visitor_name
    if start_date:
        query["prdStartDate"] = start_date
    if end_date:
        query["prdEndDate"] = end_date
    if page != 1:
        query["page"] = page

    result = client.get("/vsk/vst-visitor/api/invitations", query=query)
    return _simplify_visitors(result)


def _simplify_visitors(result: dict) -> dict:
    """简化访客响应数据，只保留关键字段。

    Args:
        result: API 原始响应

    Returns:
        简化后的访客数据
    """
    data = result.get("data", result)
    if isinstance(data, dict):
        records = data.get("rows", data.get("records", data.get("list", [])))
        total = data.get("total", len(records))
        current = data.get("page", 1)
    elif isinstance(data, list):
        records = data
        total = len(records)
        current = 1
    else:
        records = []
        total = 0
        current = 1

    # 如果没有记录，直接返回空
    if not records:
        return {
            "total": 0,
            "page": current,
            "records": [],
        }

    simplified = []
    for item in records:
        # 访客姓名
        visitor_name = item.get("visitorName", "未知")
        # 到访时间
        visit_ts = item.get("preVisitorTime", 0)
        visit_time = _format_timestamp(visit_ts) if visit_ts else "未知"
        # 邀请人
        invitee = item.get("employeeName", "")
        # 状态
        status_code = str(item.get("visitorStatus", ""))
        status_label = VISITOR_STATUS_MAP.get(status_code, f"未知({status_code})")
        # 邀请码
        invitation_code = item.get("invitationCode", "")
        # 电话
        phone = item.get("visitorNumber", "")

        simplified.append({
            "visitorName": visitor_name,
            "visitTime": visit_time,
            "invitee": invitee,
            "status": status_label,
            "invitationCode": invitation_code,
            "phone": phone,
        })

    return {
        "total": total,
        "page": current,
        "records": simplified,
    }


def get_visitor_status(status_code) -> str:
    """获取访客状态的中文描述。

    Args:
        status_code: 状态码（字符串）

    Returns:
        中文状态描述
    """
    return VISITOR_STATUS_MAP.get(str(status_code), f"未知({status_code})")


def format_visitor_list(visitors: list) -> str:
    """格式化访客列表为可读文本。

    Args:
        visitors: 访客记录列表

    Returns:
        格式化的文本
    """
    if not visitors:
        return "暂无访客记录"

    lines = []
    for v in visitors:
        name = v.get("visitorName", "未知")
        visit_time = v.get("visitTime", "")
        invitee = v.get("invitee", "")
        status = v.get("status", "")
        phone = v.get("phone", "")

        line = f"- **{name}** | {visit_time} | {status}"
        if phone:
            line += f" | 📞 {phone}"
        if invitee:
            line += f" | 邀请人: {invitee}"
        lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else None
    result = list_visitors(visitor_name=name)
    print(format_visitor_list(result.get("records", [])))
