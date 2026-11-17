#!/usr/bin/env python3
"""Persistent work schedule manager for OpenClaw."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import tempfile
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DEFAULT_HOME = Path("~/.openclaw/workspace/work-schedule").expanduser()
DEFAULT_TIMEZONE = "Asia/Shanghai"
PRIORITY_ORDER = {"高": 0, "中": 1, "低": 2}
ACTIVE = {"pending", "in_progress"}


def data_home() -> Path:
    configured = os.environ.get("WORK_SCHEDULE_HOME")
    return Path(configured).expanduser().resolve() if configured else DEFAULT_HOME.resolve()


def schedule_timezone() -> ZoneInfo:
    name = os.environ.get("WORK_SCHEDULE_TZ", DEFAULT_TIMEZONE)
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise SystemExit(f"无效时区 WORK_SCHEDULE_TZ={name}") from exc


def local_now() -> datetime:
    return datetime.now(schedule_timezone())


def local_today() -> date:
    return local_now().date()


def paths() -> dict[str, Path]:
    home = data_home()
    return {
        "home": home,
        "data": home / "schedule.json",
        "view": home / "工作日程.md",
        "history": home / "history.jsonl",
        "lock": home / ".schedule.lock",
    }


@contextmanager
def locked() -> Iterator[dict[str, Path]]:
    target = paths()
    target["home"].mkdir(parents=True, exist_ok=True)
    with target["lock"].open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield target
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def now_iso() -> str:
    return local_now().isoformat(timespec="seconds")


def empty_store() -> dict[str, Any]:
    return {"version": 1, "updated_at": now_iso(), "items": []}


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_store()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"日程数据无法读取，请先备份并检查 {path}: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("items"), list):
        raise SystemExit(f"日程数据结构无效：{path}")
    return value


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def validate_date(value: str | None, field: str = "date") -> str | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise SystemExit(f"{field} 必须为 YYYY-MM-DD：{value}") from exc


def validate_time(value: str | None, field: str = "time") -> str | None:
    if not value:
        return None
    try:
        parsed = datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise SystemExit(f"{field} 必须为 HH:MM：{value}") from exc
    return parsed.strftime("%H:%M")


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def safe_filename(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", value).strip(" .")
    return cleaned or "attachment"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unique_attachment_path(directory: Path, filename: str) -> Path:
    candidate = directory / filename
    stem, suffix = candidate.stem, candidate.suffix
    index = 2
    while candidate.exists():
        candidate = directory / f"{stem}-{index}{suffix}"
        index += 1
    return candidate


def next_id(items: list[dict[str, Any]], item_date: str | None) -> str:
    prefix_date = (item_date or local_today().isoformat()).replace("-", "")
    prefix = f"WS-{prefix_date}-"
    numbers = []
    for item in items:
        identifier = str(item.get("id", ""))
        if identifier.startswith(prefix):
            try:
                numbers.append(int(identifier.rsplit("-", 1)[1]))
            except ValueError:
                pass
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
    return (
        item.get("date") or "9999-12-31",
        item.get("time") or "99:99",
        PRIORITY_ORDER.get(item.get("priority", "中"), 1),
        item.get("created_at", ""),
    )


def display_when(item: dict[str, Any]) -> str:
    day = item.get("date") or "待安排日期"
    start = item.get("time")
    end = item.get("end_time")
    if start and end:
        return f"{day} {start}-{end}"
    if start:
        return f"{day} {start}"
    return day


def render_markdown(store: dict[str, Any]) -> str:
    items = sorted(store["items"], key=sort_key)
    groups = [
        ("待办日程", [item for item in items if item.get("status") in ACTIVE and item.get("date")]),
        ("待安排日期", [item for item in items if item.get("status") in ACTIVE and not item.get("date")]),
        ("已完成", [item for item in items if item.get("status") == "completed"]),
        ("已取消", [item for item in items if item.get("status") == "cancelled"]),
    ]
    lines = [
        "# 工作日程",
        "",
        f"> 更新时间：{store.get('updated_at', '')}",
        "",
    ]
    for heading, group in groups:
        lines.extend([f"## {heading}", ""])
        if not group:
            lines.extend(["暂无。", ""])
            continue
        for item in group:
            marker = "x" if item.get("status") == "completed" else " "
            priority = item.get("priority", "中")
            category = item.get("category", "其他")
            lines.append(
                f"- [{marker}] **{display_when(item)}**｜{item['title']}｜"
                f"{priority}｜{category}｜`{item['id']}`"
            )
            if item.get("notes"):
                lines.append(f"  - 备注：{item['notes']}")
            if item.get("deadline"):
                lines.append(f"  - 截止：{item['deadline']}")
            attachments = item.get("attachments") or []
            for attachment in attachments:
                label = attachment.get("label") or "附件"
                if attachment.get("type") == "url":
                    lines.append(f"  - 附件：[{label}]({attachment['url']})")
                elif attachment.get("type") == "file":
                    lines.append(f"  - 附件：[{label}]({attachment['relative_path']})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def save_store(target: dict[str, Path], store: dict[str, Any], event: dict[str, Any]) -> None:
    store["updated_at"] = now_iso()
    atomic_write(target["data"], json.dumps(store, ensure_ascii=False, indent=2) + "\n")
    atomic_write(target["view"], render_markdown(store))
    event["at"] = now_iso()
    with target["history"].open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def find_item(store: dict[str, Any], identifier: str) -> dict[str, Any]:
    matches = [item for item in store["items"] if item.get("id") == identifier]
    if not matches:
        raise SystemExit(f"未找到事项：{identifier}")
    return matches[0]


def cmd_add(args: argparse.Namespace) -> None:
    title = normalize_text(args.title)
    if not title:
        raise SystemExit("title 不能为空")
    item_date = validate_date(args.date)
    item_time = validate_time(args.time)
    end_time = validate_time(args.end_time, "end_time")
    if args.priority not in PRIORITY_ORDER:
        raise SystemExit("priority 必须为 高、中、低")
    with locked() as target:
        store = load_store(target["data"])
        duplicate = next(
            (
                item for item in store["items"]
                if item.get("status") in ACTIVE
                and normalize_text(item.get("title", "")).lower() == title.lower()
                and item.get("date") == item_date
                and item.get("time") == item_time
            ),
            None,
        )
        if duplicate:
            print(json.dumps({"status": "duplicate", "item": duplicate}, ensure_ascii=False))
            return
        item = {
            "id": next_id(store["items"], item_date),
            "title": title,
            "date": item_date,
            "time": item_time,
            "end_time": end_time,
            "deadline": normalize_text(args.deadline) if args.deadline else None,
            "priority": args.priority,
            "category": normalize_text(args.category),
            "notes": normalize_text(args.notes) if args.notes else None,
            "source": normalize_text(args.source) if args.source else None,
            "status": "pending",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "completed_at": None,
            "attachments": [],
        }
        store["items"].append(item)
        save_store(target, store, {"action": "add", "id": item["id"], "after": item})
        print(json.dumps({"status": "created", "item": item}, ensure_ascii=False))


def cmd_update(args: argparse.Namespace) -> None:
    changes = {
        "title": normalize_text(args.title) if args.title is not None else None,
        "date": validate_date(args.date) if args.date is not None else None,
        "time": validate_time(args.time) if args.time is not None else None,
        "end_time": validate_time(args.end_time, "end_time") if args.end_time is not None else None,
        "deadline": normalize_text(args.deadline) if args.deadline is not None else None,
        "priority": args.priority,
        "category": normalize_text(args.category) if args.category is not None else None,
        "notes": normalize_text(args.notes) if args.notes is not None else None,
    }
    provided = {key: value for key, value in changes.items() if getattr(args, key) is not None}
    if not provided:
        raise SystemExit("没有提供需要修改的字段")
    if args.priority is not None and args.priority not in PRIORITY_ORDER:
        raise SystemExit("priority 必须为 高、中、低")
    with locked() as target:
        store = load_store(target["data"])
        item = find_item(store, args.id)
        before = dict(item)
        item.update(provided)
        item["updated_at"] = now_iso()
        save_store(target, store, {"action": "update", "id": args.id, "before": before, "after": item})
        print(json.dumps({"status": "updated", "item": item}, ensure_ascii=False))


def change_status(identifier: str, status: str) -> None:
    with locked() as target:
        store = load_store(target["data"])
        item = find_item(store, identifier)
        before = dict(item)
        item["status"] = status
        item["updated_at"] = now_iso()
        if status == "completed":
            item["completed_at"] = now_iso()
        save_store(
            target,
            store,
            {"action": status, "id": identifier, "before": before, "after": item},
        )
        print(json.dumps({"status": status, "item": item}, ensure_ascii=False))


def cmd_attach(args: argparse.Namespace) -> None:
    label = normalize_text(args.label) if args.label else None
    with locked() as target:
        store = load_store(target["data"])
        item = find_item(store, args.id)
        attachments = item.setdefault("attachments", [])
        if args.url:
            parsed = urlparse(args.url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise SystemExit("附件 URL 只允许有效的 HTTP/HTTPS 地址")
            normalized_url = args.url.strip()
            duplicate = next(
                (entry for entry in attachments if entry.get("type") == "url" and entry.get("url") == normalized_url),
                None,
            )
            if duplicate:
                print(json.dumps({"status": "duplicate", "attachment": duplicate}, ensure_ascii=False))
                return
            attachment = {
                "type": "url",
                "label": label or Path(parsed.path).name or parsed.netloc,
                "url": normalized_url,
                "added_at": now_iso(),
            }
        else:
            source = Path(args.file).expanduser().resolve()
            if not source.is_file():
                raise SystemExit(f"附件文件不存在或不是普通文件：{source}")
            max_mb = int(os.environ.get("WORK_SCHEDULE_ATTACHMENT_MAX_MB", "100"))
            size = source.stat().st_size
            if size > max_mb * 1024 * 1024:
                raise SystemExit(f"附件超过 {max_mb} MB 限制：{source.name}")
            checksum = file_sha256(source)
            duplicate = next(
                (entry for entry in attachments if entry.get("type") == "file" and entry.get("sha256") == checksum),
                None,
            )
            if duplicate:
                print(json.dumps({"status": "duplicate", "attachment": duplicate}, ensure_ascii=False))
                return
            attachment_dir = target["home"] / "attachments" / args.id
            attachment_dir.mkdir(parents=True, exist_ok=True)
            destination = unique_attachment_path(attachment_dir, safe_filename(source.name))
            shutil.copy2(source, destination)
            relative = destination.relative_to(target["home"]).as_posix()
            attachment = {
                "type": "file",
                "label": label or source.name,
                "relative_path": relative,
                "original_name": source.name,
                "size_bytes": size,
                "sha256": checksum,
                "added_at": now_iso(),
            }
        attachments.append(attachment)
        item["updated_at"] = now_iso()
        save_store(
            target,
            store,
            {"action": "attach", "id": args.id, "attachment": attachment},
        )
        print(json.dumps({"status": "attached", "attachment": attachment}, ensure_ascii=False))


def cmd_show(args: argparse.Namespace) -> None:
    with locked() as target:
        store = load_store(target["data"])
        item = find_item(store, args.id)
    print(json.dumps(item, ensure_ascii=False, indent=2))


def resolve_range(value: str) -> tuple[date | None, date | None]:
    today = local_today()
    if value == "today":
        return today, today
    if value == "tomorrow":
        tomorrow = today + timedelta(days=1)
        return tomorrow, tomorrow
    if value == "week":
        return today, today + timedelta(days=6)
    if value == "all":
        return None, None
    parsed = date.fromisoformat(value)
    return parsed, parsed


def selected_items(store: dict[str, Any], selector: str) -> list[dict[str, Any]]:
    start, end = resolve_range(selector)
    result = []
    for item in store["items"]:
        if item.get("status") not in ACTIVE:
            continue
        item_date = item.get("date")
        if selector == "all":
            result.append(item)
        elif item_date and start <= date.fromisoformat(item_date) <= end:
            result.append(item)
    return sorted(result, key=sort_key)


def format_items(items: list[dict[str, Any]]) -> str:
    if not items:
        return "暂无事项。"
    lines = []
    for item in items:
        attachment_count = len(item.get("attachments") or [])
        attachment_text = f"｜附件{attachment_count}个" if attachment_count else ""
        lines.append(
            f"- {display_when(item)}｜{item['title']}｜"
            f"{item.get('priority', '中')}｜{item.get('category', '其他')}｜{item['id']}"
            f"{attachment_text}"
        )
    return "\n".join(lines)


def cmd_list(args: argparse.Namespace) -> None:
    with locked() as target:
        store = load_store(target["data"])
    print(format_items(selected_items(store, args.date)))


def cmd_brief(args: argparse.Namespace) -> None:
    with locked() as target:
        store = load_store(target["data"])
    today = local_today()
    today_items = selected_items(store, args.date)
    overdue = sorted(
        [
            item for item in store["items"]
            if item.get("status") in ACTIVE
            and item.get("date")
            and date.fromisoformat(item["date"]) < today
        ],
        key=sort_key,
    )
    unscheduled = sorted(
        [
            item for item in store["items"]
            if item.get("status") in ACTIVE and not item.get("date")
        ],
        key=sort_key,
    )
    if not today_items and not overdue and not unscheduled:
        print("今日暂无已登记工作安排。")
        return
    range_start, range_end = resolve_range(args.date)
    heading_date = range_start if range_start and range_start == range_end else today
    lines = [f"【每日工作提醒｜{heading_date.isoformat()}】", ""]
    lines.extend(["一、今日工作", format_items(today_items), ""])
    if overdue:
        lines.extend(["二、逾期未完成", format_items(overdue), ""])
    if unscheduled:
        lines.extend(["三、待安排日期", format_items(unscheduled), ""])
    high = [item for item in today_items if item.get("priority") == "高"]
    if high:
        lines.extend(["重点关注", format_items(high)])
    print("\n".join(lines).rstrip())


def add_common_fields(parser: argparse.ArgumentParser, update: bool = False) -> None:
    parser.add_argument("--title", required=not update)
    parser.add_argument("--date")
    parser.add_argument("--time")
    parser.add_argument("--end-time")
    parser.add_argument("--deadline")
    parser.add_argument("--priority", choices=["高", "中", "低"], default=None if update else "中")
    parser.add_argument("--category", default=None if update else "其他")
    parser.add_argument("--notes")
    if not update:
        parser.add_argument("--source")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    add_parser = sub.add_parser("add", help="Add a schedule item")
    add_common_fields(add_parser)
    add_parser.set_defaults(func=cmd_add)

    update_parser = sub.add_parser("update", help="Update a schedule item")
    update_parser.add_argument("--id", required=True)
    add_common_fields(update_parser, update=True)
    update_parser.set_defaults(func=cmd_update)

    done_parser = sub.add_parser("done", help="Mark an item completed")
    done_parser.add_argument("--id", required=True)
    done_parser.set_defaults(func=lambda args: change_status(args.id, "completed"))

    cancel_parser = sub.add_parser("cancel", help="Mark an item cancelled")
    cancel_parser.add_argument("--id", required=True)
    cancel_parser.set_defaults(func=lambda args: change_status(args.id, "cancelled"))

    attach_parser = sub.add_parser("attach", help="Attach a local file or URL")
    attach_parser.add_argument("--id", required=True)
    source_group = attach_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--file")
    source_group.add_argument("--url")
    attach_parser.add_argument("--label")
    attach_parser.set_defaults(func=cmd_attach)

    show_parser = sub.add_parser("show", help="Show one schedule item")
    show_parser.add_argument("--id", required=True)
    show_parser.set_defaults(func=cmd_show)

    list_parser = sub.add_parser("list", help="List schedule items")
    list_parser.add_argument("--date", default="today", help="today, tomorrow, week, all, or YYYY-MM-DD")
    list_parser.set_defaults(func=cmd_list)

    brief_parser = sub.add_parser("brief", help="Generate the daily reminder")
    brief_parser.add_argument("--date", default="today")
    brief_parser.set_defaults(func=cmd_brief)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
