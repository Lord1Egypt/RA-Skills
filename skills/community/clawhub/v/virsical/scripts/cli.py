"""
Virsical 统一命令行入口。

提供所有 Virsical 功能的一站式 CLI 接口，包括：
- 会话管理（预检、登录、登出）
- 会议室（查询、预订、列表）
- 访客查询
- 工单（参数、创建）
- 配置管理

用法: python -m scripts.cli <命令> [参数...]
"""

import json
import sys
from typing import Optional


def _print_json(obj):
    """格式化输出 JSON。"""
    print(json.dumps(obj, ensure_ascii=False, indent=2))


# ═══════════════════════════════════════════════════════════════════
# 会话管理命令
# ═══════════════════════════════════════════════════════════════════

def cmd_ready(scene: str):
    """一站式预检：配置 → 认证 → License。"""
    from .session import ensure_ready
    result = ensure_ready(scene)
    _print_json(result)
    if not result["ready"]:
        print(f"\n下一步: {result['next_action']}")


def cmd_config_status():
    """查看配置状态。"""
    from .config import get_config
    cfg = get_config()
    print(f"配置完整 | Base URL: {cfg.base_url}")


def cmd_config_set():
    """查看当前配置（无需设置，已使用固定凭证）。"""
    from .config import get_config
    cfg = get_config()
    print(f"Base URL: {cfg.base_url}")
    print("OAuth 凭证已使用固定值，无需配置")


def cmd_login():
    """执行本地登录流程。"""
    from .config import get_config, reset_config
    from .auth_manager import TokenManager, check_token_before_login, local_login

    reset_config()
    cfg = get_config()

    tm = TokenManager(cfg)
    check = check_token_before_login(tm)
    if not check["should_login"]:
        print(f"已登录，用户: {check.get('username', '未知')}")
        return

    result = local_login(cfg, tm)
    _print_json(result)


def cmd_agent_login(auth_code: str):
    """使用 Agent 授权码登录并保存 token。"""
    from .config import get_config, reset_config
    from .auth_manager import TokenManager, check_token_before_login, exchange_agent_code_for_token

    reset_config()
    cfg = get_config()
    tm = TokenManager(cfg)

    check = check_token_before_login(tm)
    if not check["should_login"]:
        print(f"已登录，用户: {check.get('username', '未知')}")
        return

    result = exchange_agent_code_for_token(auth_code, cfg, tm)
    _print_json(result)
    if result.get("success"):
        print(f"\n登录成功，可以继续使用 Virsical 技能。")


def cmd_logout():
    """登出 Virsical。"""
    from .config import get_config
    from .auth_manager import TokenManager
    cfg = get_config()
    tm = TokenManager(cfg)
    tm.logout()
    print("已登出")


# ═══════════════════════════════════════════════════════════════════
# 会议室命令
# ═══════════════════════════════════════════════════════════════════

def cmd_rooms(capacity_min: int = 0, capacity_max: int = 0):
    """查询可用会议室。"""
    from .meeting import query_available_rooms
    print(query_available_rooms(capacity_min=capacity_min, capacity_max=capacity_max))


def cmd_room_check(start: Optional[str] = None, end: Optional[str] = None,
                   capacity: int = -1, exclude: str = "1;8"):
    """按时间段查询会议室占用状态。"""
    from .meeting import check_room_occupancy, format_room_list
    result = check_room_occupancy(
        start_time=start, end_time=end,
        capacity=capacity, exclude_capacities=exclude,
    )
    print(format_room_list(result.get("data", [])))


def cmd_book(room_id: str, title: str, start: str, end: str):
    """预订会议室。"""
    from .meeting import book_meeting
    result = book_meeting(room_id=room_id, title=title, start_time=start, end_time=end)
    _print_json(result)
    if result["success"]:
        print(f"\n预订成功!")
    elif "suggested_rooms" in result:
        print("\n建议替代会议室:")
        for r in result.get("suggested_rooms", []):
            print(f"  - {r.get('roomName', '?')} ({r.get('capacity', '?')}人)")
    elif "available_rooms" in result:
        print("\n可用会议室:")
        for r in result.get("available_rooms", []):
            print(f"  - {r.get('roomName', '?')} ({r.get('capacity', '?')}人)")


def cmd_meetings():
    """查询我的会议列表。"""
    from .meeting import list_meetings
    result = list_meetings()
    records = result.get("data", result.get("result", {}))
    if isinstance(records, dict):
        records = records.get("records", [])
    for m in records:
        print(f"- {m.get('name', '无标题')} | {m.get('roomNames', '')} | {m.get('startTime', '')} ~ {m.get('endTime', '')}")


# ═══════════════════════════════════════════════════════════════════
# 访客命令
# ═══════════════════════════════════════════════════════════════════

def cmd_visitors(name: Optional[str] = None):
    """查询访客记录。"""
    from .visitor import list_visitors, format_visitor_list
    result = list_visitors(visitor_name=name)
    print(format_visitor_list(result.get("records", [])))


# ═══════════════════════════════════════════════════════════════════
# 工单命令
# ═══════════════════════════════════════════════════════════════════

def cmd_req_params():
    """获取工单创建参数。"""
    from .requirement import get_requirement_params
    result = get_requirement_params()
    print(json.dumps(result, ensure_ascii=False, indent=2)[:3000])


def cmd_req_create(project_id: int, content: str, type_id: int, priority: int = 23):
    """创建工单。"""
    from .requirement import create_requirement
    result = create_requirement(
        project_id=project_id,
        content=content,
        requirement_type_id=type_id,
        priority=priority,
    )
    _print_json(result)


# ═══════════════════════════════════════════════════════════════════
# License 命令
# ═══════════════════════════════════════════════════════════════════

def cmd_license(scene: str):
    """检查 License 权限。"""
    from .license import check_license_for_scene
    result = check_license_for_scene(scene)
    _print_json(result)


def cmd_licenses():
    """列出所有 License。"""
    from .license import fetch_licenses, format_license_list
    result = fetch_licenses()
    if result["success"]:
        print(f"已获取许可列表：")
        print(format_license_list(result["licenses"]))
    else:
        print(f"获取失败: {result['message']}")


# ═══════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════

USAGE = """Virsical CLI - 威思客智慧空间管理平台

用法: python -m scripts.cli <命令> [参数...]

会话管理:
  ready <scene>         一站式预检（meeting/visitor/requirement）
  config                 查看配置状态
  login                  登录（OAuth 本地回调）
  agent-login <code>     使用 Agent 授权码登录
  logout                登出

会议室:
  rooms [min] [max]     查询可用会议室（可选容量范围）
  check [start] [end]   按时间段查询占用
  book <rid> <title> <start> <end>  预订会议室
  meetings               查询我的会议

访客:
  visitors [name]       查询访客记录

工单:
  req-params            获取工单创建参数
  req-create <pid> <content> <tid> [priority]  创建工单

License:
  license <scene>       检查场景许可
  licenses              列出所有许可
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        # 会话管理
        if cmd == "ready":
            cmd_ready(args[0] if args else "meeting")
        elif cmd == "config":
            cmd_config_status()
        elif cmd == "login":
            cmd_login()
        elif cmd == "agent-login":
            if len(args) < 1:
                print("错误: agent-login 需要授权码参数")
                sys.exit(1)
            cmd_agent_login(args[0])
        elif cmd == "logout":
            cmd_logout()

        # 会议室
        elif cmd == "rooms":
            lo = int(args[0]) if args else 0
            hi = int(args[1]) if len(args) > 1 else 0
            cmd_rooms(capacity_min=lo, capacity_max=hi)
        elif cmd == "check":
            start = args[0] if args else None
            end = args[1] if len(args) > 1 else None
            cmd_room_check(start=start, end=end)
        elif cmd == "book":
            if len(args) < 4:
                print("错误: book 需要 room_id, title, start_time, end_time")
                sys.exit(1)
            cmd_book(args[0], args[1], args[2], args[3])
        elif cmd == "meetings":
            cmd_meetings()

        # 访客
        elif cmd == "visitors":
            cmd_visitors(args[0] if args else None)

        # 工单
        elif cmd == "req-params":
            cmd_req_params()
        elif cmd == "req-create":
            if len(args) < 3:
                print("错误: req-create 需要 project_id, content, type_id")
                sys.exit(1)
            priority = int(args[3]) if len(args) > 3 else 23
            cmd_req_create(int(args[0]), args[1], int(args[2]), priority)

        # License
        elif cmd == "license":
            cmd_license(args[0] if args else "meeting")
        elif cmd == "licenses":
            cmd_licenses()

        else:
            print(f"未知命令: {cmd}")
            print(USAGE)
            sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
