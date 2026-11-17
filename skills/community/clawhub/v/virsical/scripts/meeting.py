"""
Virsical 会议室管理模块。

提供会议室查询（双接口合并）、预订、会议列表等功能。
查询时同时调用 /rooms（详情：容量/区域/设备）和 /rooms/occupied（占用状态）接口，
合并后展示完整的会议室信息及今日空闲时段。
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional

from .config import get_config
from .auth_manager import TokenManager
from .virsical_client import VirsicalClient

CST = timezone(timedelta(hours=8))

# 工作时间范围（分钟）
WORK_START_MIN = 8 * 60   # 08:00
WORK_END_MIN = 22 * 60    # 22:00


def _now_iso() -> str:
    """返回当前 CST 时间的 ISO 8601 格式。"""
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _to_iso(dt: datetime) -> str:
    """转换 datetime 为 ISO 8601 格式。"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CST)
    return dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _min_to_hhmm(m: int) -> str:
    """分钟数转 HH:MM 格式。"""
    return f"{m // 60:02d}:{m % 60:02d}"


def _parse_device_name(device_str: str) -> str:
    """解析设备列表字符串，逗号分隔转为顿号分隔。"""
    if not device_str:
        return ""
    devices = [d.strip() for d in device_str.split(",") if d.strip()]
    return "、".join(devices) if devices else ""


def _parse_occupied_slots(occupied_list: list) -> list:
    """解析占用时间段字符串列表为 (start_min, end_min) 列表。

    Args:
        occupied_list: 如 ["2026-06-02 09:00~10:00", "2026-06-02 14:00~15:30"]

    Returns:
        [(540, 600), (840, 930), ...] 分钟数元组
    """
    busy = []
    for seg in (occupied_list or []):
        try:
            parts = str(seg).strip().split("~")
            if len(parts) != 2:
                continue
            start_str = parts[0].strip()
            end_str = parts[1].strip()

            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            s_min = start_dt.hour * 60 + start_dt.minute

            if len(end_str) <= 5:
                e_dt = datetime.strptime(end_str, "%H:%M")
                e_min = e_dt.hour * 60 + e_dt.minute
            else:
                e_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
                e_min = e_dt.hour * 60 + e_dt.minute

            busy.append((s_min, e_min))
        except Exception:
            continue
    return busy


def _get_free_slots(occupied_list: list, now_min: int) -> list:
    """计算今日剩余空闲时段。

    Args:
        occupied_list: 占用时间段字符串列表
        now_min: 当前时间（分钟）

    Returns:
        [(start_min, end_min), ...] 空闲时段列表（至少 15 分钟）
    """
    busy = _parse_occupied_slots(occupied_list)
    busy.sort()
    free = []
    cursor = max(WORK_START_MIN, now_min)

    for bs, be in busy:
        if be <= cursor:
            continue
        if bs > cursor:
            free.append((cursor, bs))
        cursor = max(cursor, be)

    if cursor < WORK_END_MIN:
        free.append((cursor, WORK_END_MIN))

    return [(s, e) for s, e in free if e - s >= 15]


def _format_free_slots(free_slots: list) -> str:
    """格式化空闲时段为可读字符串。"""
    if not free_slots:
        return "今日已无空闲"
    return "、".join([
        f"{_min_to_hhmm(s)}-{_min_to_hhmm(e)}" for s, e in free_slots
    ])


def _get_tenant_id() -> int:
    """获取当前用户的 tenant_id（复用全局配置和 TokenManager 单例）。"""
    from .auth_manager import TOKEN_FILE
    try:
        if TOKEN_FILE.exists():
            data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
            token = data.get("virsical:default", {})
            return token.get("tenantId", 0)
    except Exception:
        pass
    return 0


# ── 核心查询函数 ──────────────────────────────────────────────────


def get_room_list(
    capacity: int = -1,
    exclude_capacities: str = "1;8",
    tenant_id: Optional[int] = None,
    meeting_id: int = 0,
) -> dict:
    """获取会议室详细列表（含容量、区域、设备信息）。

    调用 /vsk/smt-meeting/ai/rooms 接口。

    Args:
        capacity: 会议室类型，-1 表示不限制
        exclude_capacities: 排除的会议室类型，分号分隔如 "1;8"
        tenant_id: 租户 ID，默认自动获取
        meeting_id: 会议 ID，固定 0

    Returns:
        API 原始响应
    """
    client = VirsicalClient()
    if tenant_id is None:
        tenant_id = _get_tenant_id()

    body = {
        "tenantId": tenant_id,
        "capacity": capacity,
        "excludeCapacities": exclude_capacities,
        "meetingId": meeting_id,
    }

    return client.post("/vsk/smt-meeting/ai/rooms", body=body)


def check_room_occupancy(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    exclude_capacities: str = "1;8",
    capacity: int = -1,
    room_name: Optional[str] = None,
    tenant_id: Optional[int] = None,
) -> dict:
    """查询会议室（双接口合并：详情 + 占用状态）。

    同时调用 /vsk/smt-meeting/ai/rooms 和 /vsk/smt-meeting/ai/rooms/occupied，
    合并返回包含容量、区域、设备及占用状态的完整会议室数据。

    Args:
        start_time: 开始时间（ISO 8601），默认当前时间
        end_time: 结束时间（ISO 8601），默认当前时间+1小时
        exclude_capacities: 排除的会议室类型，分号分隔如 "1;8"
        capacity: 会议室类型，-1 不限制
        room_name: 会议室名称（模糊搜索）
        tenant_id: 租户 ID

    Returns:
        合并后的会议室数据 {"code": 0, "data": [...], "total": N}
    """
    client = VirsicalClient()
    if tenant_id is None:
        tenant_id = _get_tenant_id()

    if not start_time:
        start_time = _now_iso()
    if not end_time:
        end_dt = datetime.now(CST) + timedelta(hours=1)
        end_time = _to_iso(end_dt)

    # 详情查询 payload
    rooms_payload = {
        "tenantId": tenant_id,
        "capacity": capacity,
        "excludeCapacities": exclude_capacities,
        "meetingId": 0,
    }

    # 占用查询 payload
    occupied_payload = {
        "tenantId": tenant_id,
        "capacity": capacity,
        "excludeCapacities": exclude_capacities,
        "meetingId": 0,
        "startTime": start_time,
        "endTime": end_time,
    }

    # 可选筛选参数
    if room_name:
        rooms_payload["roomName"] = room_name
        occupied_payload["roomName"] = room_name

    # 查询两个接口
    rooms_result = client.post("/vsk/smt-meeting/ai/rooms", body=rooms_payload)
    occupied_result = client.post("/vsk/smt-meeting/ai/rooms/occupied", body=occupied_payload)

    # 提取房间详情
    room_list = rooms_result.get("data", [])
    if isinstance(room_list, dict):
        room_list = room_list.get("records", room_list.get("list", []))
    
    # 检查 /rooms 接口是否返回空数据
    rooms_empty = len(room_list) == 0

    # 提取占用数据
    occupied_list = (
        occupied_result.get("data", [])
        if occupied_result.get("code") == 0
        else []
    )
    if isinstance(occupied_list, dict):
        occupied_list = occupied_list.get("records", occupied_list.get("list", []))

    # 构建占用映射
    occupied_map = {r["roomId"]: r.get("occupiedTime", []) for r in occupied_list}

    # 合并数据
    merged = []
    for room in room_list:
        rid = room.get("roomId")
        room["occupiedTime"] = occupied_map.get(rid, [])
        merged.append(room)

    result = {
        "code": rooms_result.get("code", 0),
        "data": merged,
        "total": len(merged),
    }
    
    # 如果 /rooms 接口本身就返回空数据，提示配置会议室
    if rooms_empty:
        result["rooms_empty"] = True
        result["message"] = "暂无可用会议室，请在 Virsical 系统中配置会议室"

    return result


def check_room_occupancy_simple(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    exclude_capacities: Optional[list] = None,
    room_name: Optional[str] = None,
) -> dict:
    """查询会议室占用状态（仅占用接口，向后兼容旧调用）。

    Args:
        start_time: 开始时间（ISO 8601）
        end_time: 结束时间（ISO 8601）
        exclude_capacities: 需要排除的会议室类型列表
        room_name: 会议室名称

    Returns:
        占用状态原始响应
    """
    client = VirsicalClient()

    if not start_time:
        start_time = _now_iso()
    if not end_time:
        end_dt = datetime.now(CST) + timedelta(hours=1)
        end_time = _to_iso(end_dt)

    tenant_id = _get_tenant_id()

    body = {
        "tenantId": tenant_id,
        "capacity": -1,
        "excludeCapacities": "1;8",
        "meetingId": 0,
        "startTime": start_time,
        "endTime": end_time,
    }

    if exclude_capacities:
        body["excludeCapacities"] = exclude_capacities
    if room_name:
        body["roomName"] = room_name

    return client.post("/vsk/smt-meeting/ai/rooms/occupied", body=body)


# ── 预订相关 ──────────────────────────────────────────────────────


# ─── 会议预订错误码映射 ───
MEETING_ERROR_CODES = {
    "200999": "该时间段会议室有冲突或者是收费会议室，请更换时间段或选择其他会议室",
    "200998": "富士胶片定制",
    "200000": "操作成功",
    "200001": "操作失败",
    "200002": "任务执行失败",
    "200003": "租户不存在",
    "200004": "登录失败，用户名或密码不正确",
    "200005": "租户已过期",
    "200006": "用户预订已被限制",
    "200007": "用户预订已被限制",
    "200008": "登录失败，email不正确",
    "200009": "登录失败，工号不正确",
    "200010": "登录失败，卡片不正确",
    "102055": "部门管理员未设置",
    "201000": "已签到用户重复签到",
    "201001": "会议参会人中未找到签到用户",
    "201002": "当前用户没有管理会议的权限",
    "201003": "会议室维护，邮箱不能重复",
    "201004": "当前会议室存在预订的会议，不允许删除",
    "201005": "会议室不存在",
    "20100501": "会议室已被删除",
    "201006": "删除CMMA会议室失败",
    "201009": "已签到用户重复签到",
    "202001": "会议开始时间为空",
    "202002": "会议结束时间为空",
    "202003": "会议结束时间早于开始时间",
    "202004": "会议当前状态不允许编辑",
    "202066": "会议进入签到时间，不允许编辑",
    "202067": "特殊预订没有预订循环会议权限",
    "202068": "特殊预订没有预订跨天会议权限",
    "202069": "特殊预订提前预订天数限制",
    "202005": "循环会议不允许跨天",
    "202006": "长期会议不能小于最小天数",
    "202064": "长期会议不能大于最大天数",
    "202007": "当前用户不允许编辑会议",
    "202008": "非代订人必须参与会议",
    "202009": "开始时间不能早于当前时间",
    "202010": "会议时间处于会议室维护期间",
    "202011": "周期会议参数校验",
    "202012": "周期会议无法生成",
    "202013": "周期会议最长天数校验",
    "202014": "周期会议不允许预订",
    "202015": "会议开始时间早于工作时间",
    "202016": "会议结束时间晚于工作时间",
    "202017": "webex会议没有可用的线路资源",
    "207012": "会议时长小于会议室设置最大分钟数",
    "207013": "会议时长大于会议室设置跨天最大分钟数",
    "202128": "参会人数超过最大方数",
    "202126": "当前时间段没有会议资源",
    "202127": "参数配置缺失",
    "202148": "YMS预订时间距会议开始时间不可小于5分钟",
    "202147": "会议室未绑定设备终端，请重新选择会议室",
    "202106": "系统没有该会议室，请更换其他会议室",
    "20250223": "暂不支持预约多会议室",
    "202105": "预约人不存在",
    "202025": "没有选择会议室",
}


def _get_default_title(tm: TokenManager) -> str:
    """根据用户信息生成默认会议标题。

    格式："{realname}的会议"，使用 realname 字段。

    Args:
        tm: Token 管理器

    Returns:
        默认会议标题，如 "lp的会议"
    """
    token = tm.load_token() if tm else None
    if not token:
        return "我的会议"

    # 使用 realname（来自 getAgentToken 接口）
    realname = token.get("realname", "")
    if realname:
        return f"{realname}的会议"

    return "我的会议"


def book_meeting(
    room_id: str,
    title: Optional[str] = None,
    start_time: str = "",
    end_time: str = "",
    attendees: Optional[list] = None,
    description: Optional[str] = None,
    is_secret: bool = False,
) -> dict:
    """预订会议室。

    流程：
    1. 查询会议室占用状态
    2. 检查目标会议室是否空闲
    3. 空闲则预订，占用则返回替代建议

    Args:
        room_id: 会议室名称或 ID
        title: 会议标题。为空时自动使用 "{用户名}的会议" 格式
        start_time: 开始时间（ISO 8601 如 2026-06-03T10:00:00+08:00）
        end_time: 结束时间（ISO 8601）
        attendees: 参会人员 ID 列表
        description: 会议描述
        is_secret: 是否私密会议

    Returns:
        预订结果 {"success": bool, "message": str, ...}
    """
    client = VirsicalClient()
    cfg = get_config()
    tm = TokenManager(cfg)

    # 获取用户信息
    token = tm.load_token()
    creator_id = int(token.get("userId", 0)) if token else 0
    tenant_id = int(token.get("tenantId", 0)) if token else 0

    # 默认标题：未提供或为占位值时，使用 "{用户名}的会议"
    if not title or not title.strip() or title.strip() == "会议":
        title = _get_default_title(tm)

    # Step 1: 查询会议室（用 check_room_occupancy 获取完整信息）
    result = check_room_occupancy(
        start_time=start_time,
        end_time=end_time,
        tenant_id=tenant_id
    )
    
    # 检查是否系统级空（/rooms 接口本身返回空）
    if result.get("rooms_empty"):
        return {
            "success": False,
            "message": result.get("message", "暂无可用会议室，请在 Virsical 系统中配置会议室")
        }
    
    rooms = result.get("data", [])
    if isinstance(rooms, dict):
        rooms = rooms.get("records", rooms.get("list", []))
    if not isinstance(rooms, list):
        rooms = []
    
    # 如果没有任何会议室（但不是系统级空，可能是时间段问题）
    if not rooms:
        return {
            "success": False,
            "message": "该时间段暂无可用会议室，请尝试其他时间"
        }

    def _slots_conflict(req_start: datetime, req_end: datetime, occupied_slots: list) -> bool:
        """检查占用时段是否与请求时间冲突。"""
        for slot in occupied_slots:
            try:
                parts = str(slot).split("~")
                if len(parts) != 2:
                    continue
                s_dt = datetime.strptime(parts[0].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=CST)
                e_str = parts[1].strip()
                if len(e_str) <= 5:
                    e_dt = datetime.strptime(e_str, "%H:%M").replace(
                        year=s_dt.year, month=s_dt.month, day=s_dt.day, tzinfo=CST
                    )
                else:
                    e_dt = datetime.strptime(e_str, "%Y-%m-%d %H:%M").replace(tzinfo=CST)
                if s_dt < req_end and e_dt > req_start:
                    return True
            except Exception:
                continue
        return False

    # 解析请求时间
    req_start = datetime.fromisoformat(start_time)
    req_end = datetime.fromisoformat(end_time)

    # Step 2: 查找目标会议室
    target_room = None
    free_rooms = []

    for room in rooms:
        room_name_val = room.get("roomName", room.get("name", ""))
        room_id_val = str(room.get("roomId", room.get("id", "")))
        occupied_slots = room.get("occupiedTime", [])
        is_conflict = _slots_conflict(req_start, req_end, occupied_slots)

        if not is_conflict:
            free_rooms.append({
                "roomName": room_name_val,
                "roomId": room_id_val,
                "capacity": room.get("capacity", 0),
            })

        if room_id in (room_name_val, room_id_val, str(room.get("id", ""))):
            target_room = room

    # Step 3: 检查并预订
    if not target_room:
        return {
            "success": False,
            "message": f"未找到会议室: {room_id}",
            "available_rooms": free_rooms[:5],
        }

    if _slots_conflict(req_start, req_end, target_room.get("occupiedTime", [])):
        return {
            "success": False,
            "message": f"会议室 {target_room.get('roomName', room_id)} 在此时段已被占用",
            "suggested_rooms": free_rooms[:5],
        }

    # Step 4: 执行预订（正确参数格式）
    # 时间转为毫秒时间戳
    start_ts = int(datetime.fromisoformat(start_time).timestamp() * 1000)
    end_ts = int(datetime.fromisoformat(end_time).timestamp() * 1000)

    # 解析 room ID
    try:
        room_id_num = int(room_id)
    except (ValueError, TypeError):
        room_id_num = int(target_room.get("roomId", target_room.get("id", 0)))

    book_body = {
        "bookType": 0,
        "name": title,
        "startTime": start_ts,
        "endTime": end_ts,
        "roomIds": [room_id_num],
        "creatorId": creator_id,
        "tenantId": tenant_id,
    }

    result = client.post("/vsk/smt-meeting/ai/meeting/reserve", body=book_body)

    code = result.get("code", result.get("status", -1))
    if code == 0 or code == "0":
        # 预订成功后，尝试缓存 realname 到 token（用于生成默认标题）
        resp_data = result.get("data", result)
        realname = resp_data.get("hostName", resp_data.get("hostNameEn", ""))
        if realname and token:
            token["realname"] = realname
            tm.save_token(token)

        return {
            "success": True,
            "message": "会议室预订成功",
            "room": target_room.get("roomName", room_id),
            "time": f"{start_time} ~ {end_time}",
            "data": resp_data,
        }
    else:
        err_code = str(code)
        err_msg = result.get("msg", result.get("message", ""))
        err_detail = MEETING_ERROR_CODES.get(err_code, MEETING_ERROR_CODES.get(err_msg, ""))
        full_msg = err_msg
        if err_detail:
            full_msg = f"{err_msg}（{err_detail}）"
        return {"success": False, "message": full_msg, "code": code}


def list_meetings(
    page_size: int = 30,
) -> dict:
    """查询会议列表。

    Args:
        page_size: 每页条数，默认 30

    Returns:
        会议列表及分页信息
    """
    client = VirsicalClient()
    tenant_id = _get_tenant_id()

    body = {
        "size": page_size,
        "tenantId": tenant_id,
    }

    return client.post("/vsk/smt-meeting/ai/meeting/page", body=body)


# ── 格式化函数 ────────────────────────────────────────────────────


def format_room_list(rooms: list, show_free_slots: bool = True) -> str:
    """格式化会议室列表（增强版：区域分组 + 容量 + 设备 + 空闲时段）。

    Args:
        rooms: 会议室列表（已通过 check_room_occupancy 合并数据）
        show_free_slots: 是否显示今日空闲时段

    Returns:
        格式化的 Markdown 文本
    """
    if not rooms:
        return "暂无可用会议室，请在 Virsical 系统中配置会议室"

    now_bj = datetime.now(CST)
    now_min = now_bj.hour * 60 + now_bj.minute

    # 按区域分组
    zone_map = {}
    for room in rooms:
        zone_raw = room.get("zoneName") or ""
        parts = zone_raw.split("/")
        group = (
            "/".join(parts[1:]) if len(parts) > 1
            else (parts[0] if parts else "其他")
        )
        zone_map.setdefault(group, []).append(room)

    # 容量分布统计
    cap_count = {}
    for room in rooms:
        cap = room.get("capacity", 0) or 0
        cap_count[cap] = cap_count.get(cap, 0) + 1
    cap_summary = "、".join(
        f"{c}人×{n}间" if c > 0 else f"容量未知×{n}间"
        for c, n in sorted(cap_count.items())
    )

    lines = [f"共 {len(rooms)} 间 | 容量分布：{cap_summary}\n"]

    # 表格
    lines.append("| 区域 | 会议室 | 容量 |")
    lines.append("|------|--------|------|")

    for group, group_rooms in zone_map.items():
        # 按容量分组合并会议室名称
        cap_rooms = {}
        for room in group_rooms:
            name = room.get("roomName", "未知")
            capacity = room.get("capacity", 0)
            cap_label = f"{capacity}人" if capacity and capacity > 0 else "?"
            cap_rooms.setdefault(cap_label, []).append(name)

        for cap_label, room_names in cap_rooms.items():
            names_str = "、".join(room_names)
            lines.append(f"| 📍 {group} | {names_str} | {cap_label} |")

    lines.append("")

    # 设备与空闲补充（仅当有设备信息或存在已占用房间时展示）
    has_device = any(room.get("deviceName") for room in rooms)
    has_occupied = any(room.get("occupiedTime") for room in rooms)
    if has_device or has_occupied or show_free_slots:
        for group, group_rooms in zone_map.items():
            for room in group_rooms:
                name = room.get("roomName", "未知")
                device = _parse_device_name(room.get("deviceName") or "")
                occupied_time = room.get("occupiedTime", [])
                free_info = ""
                if show_free_slots:
                    free_slots = _get_free_slots(occupied_time, now_min)
                    free_info = _format_free_slots(free_slots)
                if device or occupied_time:
                    parts = [f"**{name}**"]
                    if device:
                        parts.append(f"🖥️ {device}")
                    if occupied_time:
                        parts.append("🔴 已占用")
                    elif free_info:
                        parts.append(f"🟢 {free_info}")
                    lines.append("　• " + " | ".join(parts))

    return "\n".join(lines)


def query_available_rooms(
    capacity_min: int = 0,
    capacity_max: int = 0,
    exclude_capacities: str = "1;8",
    tenant_id: Optional[int] = None,
) -> str:
    """一站式查询可用会议室（供 WorkBuddy 直接调用）。

    Args:
        capacity_min: 最小容量筛选，0 不限制
        capacity_max: 最大容量筛选，0 不限制
        exclude_capacities: 排除的容量，分号分隔
        tenant_id: 租户 ID

    Returns:
        格式化后的会议室信息文本
    """
    # 先不带容量筛选查询所有会议室，判断是否是系统级空
    result_all = check_room_occupancy(
        exclude_capacities=exclude_capacities,
        tenant_id=tenant_id,
    )

    # 检查是否是 /rooms 接口本身返回空
    if result_all.get("rooms_empty"):
        return result_all.get("message", "暂无可用会议室，请在 Virsical 系统中配置会议室")

    rooms_all = result_all.get("data", result_all.get("result", []))
    if isinstance(rooms_all, dict):
        rooms_all = rooms_all.get("records", rooms_all.get("list", []))

    # 如果没有容量筛选，直接返回所有
    if capacity_min <= 0 and capacity_max <= 0:
        return format_room_list(rooms_all)

    # 有容量筛选，先筛选
    filtered = []
    for r in rooms_all:
        cap = r.get("capacity", 0)
        if cap <= 0:
            continue
        if capacity_min > 0 and cap < capacity_min:
            continue
        if capacity_max > 0 and cap > capacity_max:
            continue
        filtered.append(r)
    
    # 如果筛选后有结果，直接返回
    if filtered:
        return format_room_list(filtered)
    
    # 如果筛选后没有结果，推荐容量相似的会议室
    # 计算目标容量范围的中点
    target_cap = capacity_min if capacity_min > 0 else capacity_max
    if capacity_min > 0 and capacity_max > 0:
        target_cap = (capacity_min + capacity_max) // 2
    
    # 按容量与目标的距离排序
    def cap_distance(room):
        cap = room.get("capacity", 0)
        return abs(cap - target_cap) if cap > 0 else 9999
    
    recommended = sorted(rooms_all, key=cap_distance)[:5]
    
    lines = [f"暂无 {capacity_min}-{capacity_max} 人容量的会议室"]
    lines.append("")
    lines.append("为您推荐以下容量相近的会议室：")
    lines.append("")
    
    if recommended:
        lines.append(format_room_list(recommended, show_free_slots=False))
    else:
        lines.append("暂无可用会议室")
    
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python meeting.py rooms                   # 查询所有会议室（详情+空闲）")
        print("  python meeting.py filter <min> <max>      # 按容量筛选")
        print("  python meeting.py check [start] [end]     # 仅占用查询")
        print("  python meeting.py book <rid> <title> <start> <end>")
        print("  python meeting.py list")
        sys.exit(1)

    action = sys.argv[1]

    if action == "rooms":
        print(query_available_rooms())

    elif action == "filter":
        lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        hi = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        print(query_available_rooms(capacity_min=lo, capacity_max=hi))

    elif action == "check":
        start = sys.argv[2] if len(sys.argv) > 2 else None
        end = sys.argv[3] if len(sys.argv) > 3 else None
        result = check_room_occupancy(start_time=start, end_time=end)
        print(format_room_list(result.get("data", [])))

    elif action == "book":
        if len(sys.argv) < 6:
            print("Error: book requires room_id, title, start_time, end_time")
            sys.exit(1)
        result = book_meeting(
            room_id=sys.argv[2],
            title=sys.argv[3],
            start_time=sys.argv[4],
            end_time=sys.argv[5],
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == "list":
        result = list_meetings()
        print(json.dumps(result, ensure_ascii=False, indent=2))
