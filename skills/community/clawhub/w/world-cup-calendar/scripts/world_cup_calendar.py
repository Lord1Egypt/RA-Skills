#!/usr/bin/env python3
"""把 2026 世界杯赛程预览或同步到飞书日历。"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "references" / "fwc2026-schedule.json"
LARK_CLI_PACKAGE = "@larksuite/cli"


def load_matches(include_past: bool) -> list[dict]:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    matches = data["matches"]
    if include_past:
        return matches

    now_ts = datetime.now(timezone.utc).timestamp()
    return [m for m in matches if iso_to_timestamp(m["end_bj"]) >= now_ts]


def iso_to_timestamp(value: str) -> int:
    return int(datetime.fromisoformat(value).timestamp())


def normalize_teams(value: str) -> set[str]:
    return {item.strip().upper() for item in value.split(",") if item.strip()}


def match_has_focus_team(match: dict, focus_teams: set[str]) -> bool:
    return match["home"].upper() in focus_teams or match["away"].upper() in focus_teams


def event_summary(match: dict) -> str:
    return match["title_zh"]


def event_description(match: dict) -> str:
    group_line = f"小组：{match['group']}\n" if match.get("group") else ""
    return (
        f"比赛编号：{match['id']}\n"
        f"阶段：{match['stage']}\n"
        f"{group_line}"
        f"北京时间：{match['start_bj']} - {match['end_bj']}\n"
        f"原始时间：{match['date_et']} {match['time_et']} Eastern Time\n"
        f"比赛地：{match['city_zh']}（{match['city']}）\n"
        f"数据来源：FIFA 官方赛程 PDF\n"
        f"{match['source_url']}\n\n"
        "隐私设置：日程详情仅自己可见，忙闲状态为空闲，不占用同事约会时间。"
    )


def build_event_payload(
    match: dict,
    focus_teams: set[str],
    reminder_minutes: int,
    visibility: str,
    busy_status: str,
) -> dict:
    reminders = []
    if match_has_focus_team(match, focus_teams):
        reminders.append({"minutes": reminder_minutes})

    payload = {
        "summary": event_summary(match),
        "description": event_description(match),
        "start_time": {
            "timestamp": str(iso_to_timestamp(match["start_bj"])),
            "timezone": "Asia/Shanghai",
        },
        "end_time": {
            "timestamp": str(iso_to_timestamp(match["end_bj"])),
            "timezone": "Asia/Shanghai",
        },
        "location": {
            "name": match["city_zh"],
            "address": match["city"],
        },
        "visibility": visibility,
        "free_busy_status": busy_status,
        "need_notification": False,
        "source": "world-cup-calendar",
    }
    if reminders:
        payload["reminders"] = reminders
    return payload


def run_lark(args: list[str]) -> dict:
    cmd = ["lark-cli", *args]
    completed = subprocess.run(cmd, text=True, capture_output=True)
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(message)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"raw": completed.stdout}


def command_version(command: str, version_arg: str = "--version") -> str | None:
    if not shutil.which(command):
        return None
    completed = subprocess.run([command, version_arg], text=True, capture_output=True)
    if completed.returncode != 0:
        return "已安装，但读取版本失败"
    return (completed.stdout or completed.stderr).strip()


def install_lark_cli() -> None:
    if not shutil.which("npm"):
        print("没有找到 npm，暂时不能自动安装 lark-cli。")
        print("请先安装 Node.js LTS：https://nodejs.org/")
        return

    print(f"开始安装飞书 CLI：npm install -g {LARK_CLI_PACKAGE}")
    completed = subprocess.run(["npm", "install", "-g", LARK_CLI_PACKAGE], text=True)
    if completed.returncode != 0:
        print("安装失败。可以手动执行：")
        print(f"npm install -g {LARK_CLI_PACKAGE}")
        raise SystemExit(completed.returncode)
    print("飞书 CLI 安装完成。")


def doctor(args) -> None:
    print("环境检查：")

    python_version = ".".join(str(part) for part in sys.version_info[:3])
    print(f"- Python：{python_version}")

    node_version = command_version("node")
    print(f"- Node.js：{node_version or '未安装'}")

    npm_version = command_version("npm")
    print(f"- npm：{npm_version or '未安装'}")

    lark_path = shutil.which("lark-cli")
    lark_version = command_version("lark-cli")
    print(f"- lark-cli：{lark_version or '未安装'}")
    if lark_path:
        print(f"  路径：{lark_path}")

    if not lark_path:
        print("\n没有检测到 lark-cli。")
        print(f"推荐安装命令：npm install -g {LARK_CLI_PACKAGE}")
        if args.install_cli:
            install_lark_cli()
            lark_version_after = command_version("lark-cli")
            print(f"重新检查 lark-cli：{lark_version_after or '仍未检测到，请确认 npm 全局 bin 在 PATH 中'}")
        else:
            print("如果希望脚本帮你安装，请执行：")
            print("python3 scripts/world_cup_calendar.py doctor --install-cli")
    else:
        print("\n基础命令已就绪。首次同步前还需要按提示完成飞书日历授权。")


def find_key(obj, key: str):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for value in obj.values():
            found = find_key(value, key)
            if found is not None:
                return found
    if isinstance(obj, list):
        for item in obj:
            found = find_key(item, key)
            if found is not None:
                return found
    return None


def collect_key_lists(obj, key: str) -> list:
    found = []
    if isinstance(obj, dict):
        if isinstance(obj.get(key), list):
            found.extend(obj[key])
        for value in obj.values():
            found.extend(collect_key_lists(value, key))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(collect_key_lists(item, key))
    return found


def get_or_create_calendar(calendar_name: str, execute: bool) -> str | None:
    if not execute:
        print(f"预览：将使用或创建私密日历：{calendar_name}")
        return None

    try:
        result = run_lark(
            ["calendar", "calendars", "list", "--as", "user", "--format", "json", "--page-all"]
        )
    except RuntimeError as exc:
        print_lark_error("查询日历列表失败", exc)
        raise SystemExit(1)

    calendars = find_key(result, "calendar_list") or []
    for calendar in calendars:
        if calendar.get("summary") == calendar_name or calendar.get("summary_alias") == calendar_name:
            print(f"已找到日历：{calendar_name}")
            return calendar["calendar_id"]

    data = {
        "summary": calendar_name,
        "summary_alias": calendar_name,
        "description": "2026 世界杯赛程，北京时间。由 world-cup-calendar 创建。",
        "permissions": "private",
    }
    try:
        created = run_lark(
            [
                "calendar",
                "calendars",
                "create",
                "--as",
                "user",
                "--format",
                "json",
                "--data",
                json.dumps(data, ensure_ascii=False),
            ]
        )
    except RuntimeError as exc:
        print_lark_error("创建私密日历失败", exc)
        raise SystemExit(1)

    calendar_id = find_key(created, "calendar_id")
    if not calendar_id:
        print("创建日历后没有拿到 calendar_id，请检查 lark-cli 输出。")
        raise SystemExit(1)
    print(f"已创建私密日历：{calendar_name}")
    return calendar_id


def find_calendar_id(calendar_name: str) -> str | None:
    try:
        result = run_lark(
            ["calendar", "calendars", "list", "--as", "user", "--format", "json", "--page-all"]
        )
    except RuntimeError as exc:
        print_lark_error("查询日历列表失败", exc)
        raise SystemExit(1)

    calendars = find_key(result, "calendar_list") or []
    for calendar in calendars:
        if calendar.get("summary") == calendar_name or calendar.get("summary_alias") == calendar_name:
            return calendar["calendar_id"]
    return None


def parse_match_numbers(value: str) -> set[int]:
    numbers: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start > end:
                start, end = end, start
            numbers.update(range(start, end + 1))
        else:
            numbers.add(int(part))

    invalid = [n for n in sorted(numbers) if n < 1 or n > 104]
    if invalid:
        raise ValueError(f"比赛编号必须在 1 到 104 之间，发现：{invalid}")
    return numbers


def wanted_match_ids(args) -> set[str]:
    if args.all:
        return {m["id"] for m in load_matches(include_past=True)}
    if not args.match_numbers:
        raise SystemExit("请指定 --match-numbers，例如 19,43,70；或者使用 --all 删除整套世界杯日程。")
    return {f"FWC2026-{n:03d}" for n in parse_match_numbers(args.match_numbers)}


def search_world_cup_events(calendar_id: str) -> list[dict]:
    data = {
        "query": "世界杯",
        "filter": {
            "start_time": {"timestamp": str(iso_to_timestamp("2026-06-01T00:00:00+08:00"))},
            "end_time": {"timestamp": str(iso_to_timestamp("2026-07-31T23:59:59+08:00"))},
        },
    }
    params = {"calendar_id": calendar_id, "page_size": 100}
    try:
        result = run_lark(
            [
                "calendar",
                "events",
                "search",
                "--as",
                "user",
                "--format",
                "json",
                "--page-all",
                "--page-limit",
                "20",
                "--params",
                json.dumps(params, ensure_ascii=False),
                "--data",
                json.dumps(data, ensure_ascii=False),
            ]
        )
    except RuntimeError as exc:
        print_lark_error("搜索世界杯日程失败", exc)
        raise SystemExit(1)
    return collect_key_lists(result, "items")


def event_match_id(event: dict) -> str | None:
    text = f"{event.get('summary', '')}\n{event.get('description', '')}"
    import re

    match = re.search(r"FWC2026-\d{3}", text)
    return match.group(0) if match else None


def delete_events(args) -> None:
    calendar_id = find_calendar_id(args.calendar_name)
    if not calendar_id:
        print(f"没有找到日历：{args.calendar_name}，无需删除。")
        return

    if args.delete_calendar:
        print(f"将删除整个飞书日历：{args.calendar_name}")
        if not args.execute:
            print("这是预览，没有删除。确认无误后加 --execute 才会真正删除日历。")
            return
        try:
            run_lark(
                [
                    "calendar",
                    "calendars",
                    "delete",
                    "--as",
                    "user",
                    "--format",
                    "json",
                    "--params",
                    json.dumps({"calendar_id": calendar_id}, ensure_ascii=False),
                ]
            )
        except RuntimeError as exc:
            print_lark_error("删除日历失败", exc)
            raise SystemExit(1)
        print(f"已删除日历：{args.calendar_name}")
        return

    targets = wanted_match_ids(args)
    events = search_world_cup_events(calendar_id)
    matched = []
    for event in events:
        match_id = event_match_id(event)
        if match_id in targets:
            matched.append((match_id, event))

    if not matched:
        print("没有找到符合条件的世界杯日程，无需删除。")
        return

    print(f"找到 {len(matched)} 个将删除的日程：")
    for match_id, event in sorted(matched, key=lambda item: item[0]):
        print(f"{match_id}｜{event.get('summary', '无标题')}｜event_id={event.get('event_id')}")

    if not args.execute:
        print("\n这是预览，没有删除。确认无误后加 --execute 才会真正删除。")
        return

    for index, (match_id, event) in enumerate(sorted(matched, key=lambda item: item[0]), start=1):
        event_id = event.get("event_id")
        if not event_id:
            print(f"跳过 {match_id}：没有 event_id。")
            continue
        try:
            run_lark(
                [
                    "calendar",
                    "events",
                    "delete",
                    "--as",
                    "user",
                    "--format",
                    "json",
                    "--params",
                    json.dumps(
                        {
                            "calendar_id": calendar_id,
                            "event_id": event_id,
                            "need_notification": "false",
                        },
                        ensure_ascii=False,
                    ),
                ]
            )
        except RuntimeError as exc:
            print_lark_error(f"删除失败：{match_id}", exc)
            raise SystemExit(1)
        print(f"已删除 {index}/{len(matched)}：{match_id}")


def print_lark_error(prefix: str, exc: RuntimeError) -> None:
    raw = str(exc)
    print(prefix)
    try:
        data = json.loads(raw)
        hint = find_key(data, "hint")
        scope = find_key(data, "message")
        if scope:
            print(f"原因：{scope}")
        if hint:
            print(f"建议：{hint}")
        else:
            print(raw)
    except json.JSONDecodeError:
        print(raw)


def preview(matches: list[dict], focus_teams: set[str], limit: int) -> None:
    shown = matches[:limit] if limit else matches
    print(f"共 {len(matches)} 场比赛。下面显示 {len(shown)} 场：")
    for match in shown:
        reminder = "，提前一天提醒" if match_has_focus_team(match, focus_teams) else "，不提醒"
        print(
            f"{match['id']}｜{match['start_bj'][:16].replace('T', ' ')}｜"
            f"{match['stage']}｜{match['title_zh']}｜{match['city_zh']}{reminder}"
        )


def sync(args) -> None:
    matches = load_matches(include_past=not args.no_past)
    focus_teams = normalize_teams(args.focus_team)
    if args.only_focus:
        matches = [m for m in matches if match_has_focus_team(m, focus_teams)]

    calendar_id = get_or_create_calendar(args.calendar_name, args.execute)
    print(
        f"准备同步 {len(matches)} 场；关注球队：{', '.join(sorted(focus_teams)) or '无'}；"
        f"日程可见性：{args.visibility}；忙闲状态：{args.busy_status}"
    )

    for index, match in enumerate(matches, start=1):
        payload = build_event_payload(
            match,
            focus_teams=focus_teams,
            reminder_minutes=args.reminder_minutes,
            visibility=args.visibility,
            busy_status=args.busy_status,
        )
        params = {"idempotency_key": f"world-cup-calendar-2026-{match['id']}"}
        if not args.execute:
            if index <= args.limit:
                print(f"\n预览 {index}/{len(matches)}：{match['id']} {payload['summary']}")
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            continue

        try:
            run_lark(
                [
                    "calendar",
                    "events",
                    "create",
                    "--as",
                    "user",
                    "--format",
                    "json",
                    "--params",
                    json.dumps({"calendar_id": calendar_id, **params}, ensure_ascii=False),
                    "--data",
                    json.dumps(payload, ensure_ascii=False),
                ]
            )
        except RuntimeError as exc:
            print_lark_error(f"创建失败：{match['id']} {payload['summary']}", exc)
            raise SystemExit(1)
        print(f"已创建 {index}/{len(matches)}：{payload['summary']}")

    if not args.execute:
        print("\n这是预览，没有写入飞书。确认无误后加 --execute 才会真正创建日程。")


def main() -> None:
    parser = argparse.ArgumentParser(description="把 2026 世界杯赛程同步到飞书日历。")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview_parser = subparsers.add_parser("preview", help="只查看赛程，不访问飞书。")
    preview_parser.add_argument("--focus-team", default="ARG", help="关注球队代码，多个用逗号分隔，默认 ARG。")
    preview_parser.add_argument("--limit", type=int, default=12, help="预览条数，0 表示全部。")
    preview_parser.add_argument("--no-past", action="store_true", help="跳过已经结束的比赛。")

    sync_parser = subparsers.add_parser("sync", help="预览或同步到飞书。")
    sync_parser.add_argument("--execute", action="store_true", help="真正写入飞书；不加就是安全预览。")
    sync_parser.add_argument("--calendar-name", default="world-cup-calendar", help="飞书日历名称。")
    sync_parser.add_argument("--focus-team", default="ARG", help="关注球队代码，多个用逗号分隔，默认 ARG。")
    sync_parser.add_argument("--reminder-minutes", type=int, default=1440, help="关注球队提前提醒分钟数，默认 1440。")
    sync_parser.add_argument("--visibility", choices=["private", "default", "public"], default="private")
    sync_parser.add_argument("--busy-status", choices=["free", "busy"], default="free")
    sync_parser.add_argument("--only-focus", action="store_true", help="只同步关注球队比赛。")
    sync_parser.add_argument("--no-past", action="store_true", help="跳过已经结束的比赛。")
    sync_parser.add_argument("--limit", type=int, default=3, help="安全预览时展示 payload 的条数。")

    delete_parser = subparsers.add_parser("delete", help="按比赛编号删除，或删除整套世界杯日程。")
    delete_parser.add_argument("--execute", action="store_true", help="真正删除；不加就是安全预览。")
    delete_parser.add_argument("--calendar-name", default="world-cup-calendar", help="飞书日历名称。")
    delete_parser.add_argument("--match-numbers", help="要删除的比赛编号，例如 19,43,70 或 19-21。")
    delete_parser.add_argument("--all", action="store_true", help="删除 104 场世界杯日程。")
    delete_parser.add_argument("--delete-calendar", action="store_true", help="删除整个 world-cup-calendar 日历。")

    doctor_parser = subparsers.add_parser("doctor", help="检查 Python、Node.js、npm 和 lark-cli。")
    doctor_parser.add_argument("--install-cli", action="store_true", help="如果缺少 lark-cli，则尝试用 npm 自动安装。")

    args = parser.parse_args()
    matches = load_matches(include_past=not getattr(args, "no_past", False))
    focus_teams = normalize_teams(getattr(args, "focus_team", "ARG"))

    if args.command == "preview":
        preview(matches, focus_teams, args.limit)
    elif args.command == "sync":
        sync(args)
    elif args.command == "delete":
        delete_events(args)
    elif args.command == "doctor":
        doctor(args)


if __name__ == "__main__":
    main()
