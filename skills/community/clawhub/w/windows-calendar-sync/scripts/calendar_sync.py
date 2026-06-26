"""
calendar_sync.py — 将提醒事件写入 Microsoft Outlook 日历
依赖: Python 标准库 (urllib, json, datetime) + authenticate.py
用法:
  python calendar_sync.py add --title "会议" --start "2026-04-15T10:00" --duration 60
  python calendar_sync.py list --days 7
  python calendar_sync.py delete <event_id>
"""
import json, os, sys, argparse, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from authenticate import get_access_token

GRAPH_API = "https://graph.microsoft.com/v1.0"


# ── 时区 ────────────────────────────────────────────────────────
def _tz() -> timezone:
    try:
        from tzlocal import get_localzone_name
        name = get_localzone_name()
        import zoneinfo
        return zoneinfo.ZoneInfo(name)
    except Exception:
        return timezone(timedelta(hours=8))  # 兜底 Asia/Shanghai


# ── HTTP 帮手 ───────────────────────────────────────────────────
def _req(path: str, token: str, method="GET", body=None) -> dict:
    url = f"{GRAPH_API}/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }
    data = json.dumps(body, ensure_ascii=False).encode() if body else None
    req  = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


# ── 日历事件 CRUD ───────────────────────────────────────────────
def add_event(title: str, start: str, end: str | None = None,
              duration: int = 30, body: str = "",
              location: str = "", reminder: int = 15,
              category: str = "", recurrence: str = "") -> dict:
    """
    添加日历事件。
    start / end 格式: ISO 8601 (如 "2026-04-15T10:00" 或 "2026-04-15T10:00:00")
    """
    # 解析结束时间
    if end:
        end_iso = end if "T" in end else f"{end}:00"
    else:
        dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        end_dt = dt + timedelta(minutes=duration)
        end_iso = end_dt.isoformat().replace("+00:00", "")

    # 拼装 body
    event = {
        "subject": title,
        "start":   {"dateTime": start, "timeZone": "Asia/Shanghai"},
        "end":     {"dateTime": end_iso, "timeZone": "Asia/Shanghai"},
        "reminderMinutesBeforeStart": reminder if reminder > 0 else 0,
        "isReminderOn": reminder > 0,
    }
    if body:
        event["body"] = {"contentType": "text", "content": body}
    if location:
        event["location"] = {"displayName": location}
    if recurrence:
        event["recurrence"] = {
            "pattern": {"type": "weekly"},
            "range":  {"type": "noEnd", "startDate": start[:10]}
        }
    if category:
        event["categories"] = [category]

    token  = get_access_token()
    result = _req("me/events", token, method="POST", body=event)

    eid    = result.get("id", "")
    wlink  = result.get("webLink", "")
    print(f"\n✅ 事件已创建!")
    print(f"   标题: {title}")
    print(f"   开始: {start}")
    print(f"   结束: {end_iso}")
    if reminder > 0:
        print(f"   提醒: 提前 {reminder} 分钟")
    if eid:
        print(f"   ID:   {eid}")
    if wlink:
        print(f"   🔗 {wlink}")
    return result


def list_events(days: int = 7) -> list:
    """列出未来 N 天内所有日历事件"""
    now = datetime.now(_tz())
    end = now + timedelta(days=days)

    query = urllib.parse.urlencode({
        "$filter":  f"start/dateTime ge '{now.isoformat()}' and "
                    f"end/dateTime le '{end.isoformat()}'",
        "$orderby": "start/dateTime",
        "$top":     "50",
    })
    token  = get_access_token()
    result = _req(f"me/calendarView?{query}", token)
    events = result.get("value", [])

    if not events:
        print(f"\n📅 未来 {days} 天内没有日程")
        return []

    print(f"\n📅 未来 {days} 天日程 (共 {len(events)} 个):\n")
    for ev in events:
        s = ev.get("start", {}).get("dateTime", "?")
        e = ev.get("end",   {}).get("dateTime", "?")
        s = s[:16] if "T" in s else s
        e = e[:16] if "T" in e else e
        print(f"  [{s} – {e}] {ev.get('subject','(无标题)')}")
        if ev.get("location"):
            print(f"    📍 {ev['location'].get('displayName','')}")
    return events


def delete_event(event_id: str) -> bool:
    """按 ID 删除日历事件"""
    token = get_access_token()
    _req(f"me/events/{event_id}", token, method="DELETE")
    print(f"\n✅ 事件已删除 (ID: {event_id})")
    return True


def search_events(query: str, days: int = 30) -> list:
    """按标题关键词搜索事件"""
    now  = datetime.now(_tz())
    end  = now + timedelta(days=days)
    q    = urllib.parse.urlencode({
        "$filter":  f"contains(subject,'{query}') and "
                    f"start/dateTime ge '{now.isoformat()}'",
        "$orderby": "start/dateTime",
        "$top":     "20",
    })
    token  = get_access_token()
    result = _req(f"me/calendarView?{q}", token)
    events = result.get("value", [])
    if events:
        print(f"\n🔍 找到 {len(events)} 个「{query}」相关事件:\n")
        for ev in events:
            s = ev.get("start",{}).get("dateTime","?")[:16]
            print(f"  [{s}] {ev.get('subject')}")
    else:
        print(f"\n🔍 没有找到「{query}」相关事件")
    return events


# ── CLI 入口 ────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Microsoft Outlook 日历同步工具"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # add
    p = sub.add_parser("add", help="添加日历事件")
    p.add_argument("--title",    "-t", required=True, help="事件标题")
    p.add_argument("--start",    "-s", required=True, help="开始时间 ISO 8601")
    p.add_argument("--end",      "-e",              help="结束时间 ISO 8601")
    p.add_argument("--duration", "-d", type=int, default=30, help="持续分钟数")
    p.add_argument("--body",     "-b",              help="事件描述")
    p.add_argument("--location", "-l",              help="地点")
    p.add_argument("--reminder", "-r", type=int, default=15, help="提前提醒分钟")
    p.add_argument("--category", "-c",              help="分类标签")
    p.add_argument("--recurrence",                 help="RRULE 重复规则")
    p.add_argument("--delete",                     dest="del_id",
                   help="删除指定 ID 的事件")

    # list
    p = sub.add_parser("list", help="列出未来事件")
    p.add_argument("--days",   type=int, default=7,  help="查看未来几天")
    p.add_argument("--search", "-q",                   help="按标题搜索")

    # delete
    p = sub.add_parser("delete", help="删除事件")
    p.add_argument("event_id", help="事件 ID")

    args = parser.parse_args()

    try:
        if args.cmd == "add":
            if args.del_id:
                delete_event(args.del_id)
            else:
                add_event(args.title, args.start, args.end,
                          args.duration, args.body or "",
                          args.location or "", args.reminder,
                          args.category or "", args.recurrence or "")

        elif args.cmd == "list":
            if args.search:
                search_events(args.search, args.days)
            else:
                list_events(args.days)

        elif args.cmd == "delete":
            delete_event(args.event_id)

    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        print(f"\n❌ API 错误 ({e.code}): {body.get('error',{}).get('code')}", file=sys.stderr)
        print(f"   {body.get('error',{}).get('message','')}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
