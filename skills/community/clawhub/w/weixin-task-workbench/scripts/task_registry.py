#!/usr/bin/env python3
import argparse
import json
import shutil
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import sys

STATUS_CHOICES = [
    "todo",
    "in_progress",
    "waiting_input",
    "blocked",
    "completed",
    "archived",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_registry() -> dict:
    return {
        "version": 1,
        "currentTaskId": None,
        "nextTaskId": 1,
        "tasks": [],
    }


def alias_registry_paths(path: Path) -> list[Path]:
    name = path.name
    aliases = {path}
    if "@" in name:
        aliases.add(path.with_name(name.replace("@", "_")))
    if "_im.wechat" in name:
        aliases.add(path.with_name(name.replace("_im.wechat", "@im.wechat")))
    return sorted(aliases)


def choose_registry_path(path: Path) -> Path:
    aliases = alias_registry_paths(path)
    existing = [p for p in aliases if p.exists()]
    if not existing:
        return path
    populated = []
    for p in existing:
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            tasks = data.get("tasks", [])
            populated.append((len(tasks), data.get("currentTaskId") is not None, p))
        except Exception:
            populated.append((0, False, p))
    populated.sort(key=lambda item: (item[0], item[1], str(item[2]) == str(path)), reverse=True)
    return populated[0][2]


def load_json_file(path: Path) -> Optional[dict]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        data.setdefault("version", 1)
        data.setdefault("currentTaskId", None)
        data.setdefault("nextTaskId", 1)
        data.setdefault("tasks", [])
        return data
    except Exception:
        return None


def merge_registries(base: dict, incoming: dict) -> dict:
    def status_rank(status: str) -> int:
        return {
            "todo": 0,
            "in_progress": 1,
            "waiting_input": 2,
            "blocked": 3,
            "completed": 4,
            "archived": 5,
        }.get(status or "todo", 0)

    def task_score(task: dict) -> tuple:
        return (
            1 if task.get("summary") else 0,
            status_rank(task.get("status", "todo")),
            task.get("updatedAt", ""),
        )

    merged = {}
    order = []
    for source in (base, incoming):
        for task in source.get("tasks", []):
            key = (task.get("title"), task.get("sessionKey"))
            if key not in merged:
                merged[key] = deepcopy(task)
                order.append(key)
            elif task_score(task) > task_score(merged[key]):
                merged[key] = deepcopy(task)

    tasks = [merged[key] for key in order]
    tasks.sort(key=lambda t: (t.get("createdAt", ""), t.get("id", 0), t.get("title", "")))
    title_to_new_id = {}
    for i, task in enumerate(tasks, start=1):
        task["id"] = i
        title_to_new_id[task.get("title")] = i

    current_title = None
    for candidate in (incoming, base):
        current_id = candidate.get("currentTaskId")
        if current_id is None:
            continue
        for task in candidate.get("tasks", []):
            if task.get("id") == current_id:
                current_title = task.get("title")
                break
        if current_title:
            break

    current_task_id = title_to_new_id.get(current_title)
    return {
        "version": 1,
        "currentTaskId": current_task_id,
        "nextTaskId": len(tasks) + 1,
        "tasks": tasks,
    }


def find_cross_account_candidates(path: Path) -> list[Path]:
    try:
        account_dir = path.parent
        root = account_dir.parent
        peer_name = path.name
    except Exception:
        return []
    if not root.exists():
        return []
    candidates = []
    peer_aliases = {p.name for p in alias_registry_paths(path)}
    for other_account_dir in root.iterdir():
        if not other_account_dir.is_dir() or other_account_dir == account_dir:
            continue
        for peer_alias in peer_aliases:
            candidate = other_account_dir / peer_alias
            if candidate.exists():
                candidates.append(candidate)
    return sorted(set(candidates))


def restore_cross_account_registry(path: Path, data: dict) -> tuple[dict, list[str]]:
    restored_from = []
    merged = data
    for candidate in find_cross_account_candidates(path):
        other = load_json_file(candidate)
        if not other or not other.get("tasks"):
            continue
        if not merged.get("tasks") or len(other.get("tasks", [])) > len(merged.get("tasks", [])):
            merged = merge_registries(other, merged)
            restored_from.append(str(candidate))
    return merged, restored_from


def sync_registry_aliases(primary: Path) -> None:
    for alias in alias_registry_paths(primary):
        if alias == primary:
            continue
        alias.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(primary, alias)


def load_registry(path: Path) -> dict:
    resolved = choose_registry_path(path)
    if not resolved.exists():
        data = default_registry()
        data, restored_from = restore_cross_account_registry(path, data)
        save_registry(path, data)
        if restored_from:
            data["_restoredFrom"] = restored_from
        return data
    data = load_json_file(resolved) or default_registry()
    restored_from = []
    if not data.get("tasks"):
        data, restored_from = restore_cross_account_registry(path, data)
    if resolved != path or restored_from:
        save_registry(path, data)
    else:
        sync_registry_aliases(path)
    if restored_from:
        data["_restoredFrom"] = restored_from
    return data


def save_registry(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    sync_registry_aliases(path)


def find_task(data: dict, task_id: int) -> dict:
    for task in data["tasks"]:
        if task["id"] == task_id:
            return task
    raise SystemExit(f"Task #{task_id} not found")


def emit(payload: dict) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_init(args):
    path = Path(args.registry)
    data = load_registry(path)
    payload = {"ok": True, "registry": str(path), "data": data}
    if data.get("_restoredFrom"):
        payload["restoredFrom"] = data["_restoredFrom"]
    save_registry(path, {k: v for k, v in data.items() if not k.startswith("_")})
    emit(payload)


def cmd_add(args):
    path = Path(args.registry)
    data = load_registry(path)
    task_id = data["nextTaskId"]
    task = {
        "id": task_id,
        "title": args.title,
        "status": args.status,
        "sessionKey": args.session_key,
        "summary": args.summary or "",
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
        "tags": args.tags or [],
    }
    data["tasks"].append(task)
    data["nextTaskId"] = task_id + 1
    if args.make_current or data["currentTaskId"] is None:
        data["currentTaskId"] = task_id
    save_registry(path, data)
    emit({"ok": True, "action": "add", "task": task, "currentTaskId": data["currentTaskId"]})


def cmd_list(args):
    path = Path(args.registry)
    data = load_registry(path)
    tasks = data["tasks"]
    if not args.include_archived:
        tasks = [t for t in tasks if t.get("status") != "archived"]
    emit({"ok": True, "action": "list", "currentTaskId": data["currentTaskId"], "tasks": tasks})


def cmd_switch(args):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    data["currentTaskId"] = task["id"]
    task["updatedAt"] = now_iso()
    save_registry(path, data)
    emit({"ok": True, "action": "switch", "currentTaskId": data["currentTaskId"], "task": task})


def cmd_show(args):
    path = Path(args.registry)
    data = load_registry(path)
    task_id = args.task_id if args.task_id is not None else data.get("currentTaskId")
    if task_id is None:
        emit({"ok": True, "action": "show", "task": None, "currentTaskId": None})
        return
    task = find_task(data, task_id)
    emit({"ok": True, "action": "show", "task": task, "currentTaskId": data["currentTaskId"]})


def cmd_update(args):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    changed = {}
    if args.title is not None:
        task["title"] = args.title
        changed["title"] = args.title
    if args.status is not None:
        task["status"] = args.status
        changed["status"] = args.status
    if args.session_key is not None:
        task["sessionKey"] = args.session_key
        changed["sessionKey"] = args.session_key
    if args.summary is not None:
        task["summary"] = args.summary
        changed["summary"] = args.summary
    if args.tags is not None:
        task["tags"] = args.tags
        changed["tags"] = args.tags
    task["updatedAt"] = now_iso()
    save_registry(path, data)
    emit({"ok": True, "action": "update", "changed": changed, "task": task})


def cmd_close_like(args, status: str, action: str):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    task["status"] = status
    if args.summary is not None:
        task["summary"] = args.summary
    task["updatedAt"] = now_iso()
    if data.get("currentTaskId") == task["id"] and status in {"completed", "archived"}:
        active = [t for t in data["tasks"] if t["id"] != task["id"] and t.get("status") not in {"completed", "archived"}]
        data["currentTaskId"] = active[-1]["id"] if active else None
    save_registry(path, data)
    emit({"ok": True, "action": action, "task": task, "currentTaskId": data["currentTaskId"]})


def cmd_summarize(args):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    emit({
        "ok": True,
        "action": "summarize",
        "task": {
            "id": task["id"],
            "title": task["title"],
            "status": task["status"],
            "summary": task.get("summary", ""),
            "updatedAt": task["updatedAt"],
            "sessionKey": task.get("sessionKey"),
        },
        "currentTaskId": data["currentTaskId"],
    })


def build_parser():
    parser = argparse.ArgumentParser(description="Manage Weixin Task Workbench JSON registry")
    parser.add_argument("--registry", required=True, help="Path to registry JSON file")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add")
    p.add_argument("title")
    p.add_argument("--status", choices=STATUS_CHOICES, default="todo")
    p.add_argument("--session-key", required=True)
    p.add_argument("--summary")
    p.add_argument("--make-current", action="store_true")
    p.add_argument("--tags", nargs="*")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list")
    p.add_argument("--include-archived", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("switch")
    p.add_argument("task_id", type=int)
    p.set_defaults(func=cmd_switch)

    p = sub.add_parser("show")
    p.add_argument("task_id", type=int, nargs="?")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("update")
    p.add_argument("task_id", type=int)
    p.add_argument("--title")
    p.add_argument("--status", choices=STATUS_CHOICES)
    p.add_argument("--session-key")
    p.add_argument("--summary")
    p.add_argument("--tags", nargs="*")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("close")
    p.add_argument("task_id", type=int)
    p.add_argument("--summary")
    p.set_defaults(func=lambda a: cmd_close_like(a, "completed", "close"))

    p = sub.add_parser("archive")
    p.add_argument("task_id", type=int)
    p.add_argument("--summary")
    p.set_defaults(func=lambda a: cmd_close_like(a, "archived", "archive"))

    p = sub.add_parser("summarize")
    p.add_argument("task_id", type=int)
    p.set_defaults(func=cmd_summarize)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
