from __future__ import annotations

import argparse
import json
from pathlib import Path

import cards
import chat_context
import permissions
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def delivery(chat_type: str, chat_id: str, actor: str, thread_id: str, account_id: str) -> dict:
    target = chat_id if chat_type == "group" else actor
    return {
        "channel": "feishu",
        "target": target,
        "targets": [target] if target else [],
        "chat_type": chat_type or "direct",
        "thread_id": thread_id,
        "account_id": account_id or "default",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_id", required=True)
    parser.add_argument("--updates_file", required=True, help="scan_updates.py 输出 JSON 文件")
    parser.add_argument("--threshold", type=int, default=100)
    parser.add_argument("--created_by", default="system")
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--message_sid", default="", help="OpenClaw MessageSid for audit.")
    parser.add_argument("--message_thread_id", default="", help="OpenClaw MessageThreadId, if any.")
    parser.add_argument("--account_id", default="default", help="OpenClaw AccountId.")
    args = parser.parse_args()

    path = Path(args.updates_file)
    if not path.exists():
        out(json_fail("updates_file_not_found", "找不到更新扫描结果。"))
        return
    updates = json.loads(path.read_text(encoding="utf-8"))
    if not updates.get("success"):
        out(json_fail("bad_updates_file", "更新扫描结果不是成功状态。"))
        return

    sources = sc.sources()
    source = sources.get(args.source_id)
    if not source:
        out(json_fail("source_not_found", "找不到资料源。"))
        return

    actor = chat_context.actor_id(args.created_by, args.sender_id)
    chat_type = chat_context.normalize_chat_type(args.chat_type)
    binding = None
    if chat_type == "group":
        if actor in {"", "system"}:
            out(json_fail("missing_sender_id", "群聊增量扫描必须传入 SenderId。"))
            return
        group, error = chat_context.resolve_group_context(actor, args.chat_id)
        if error:
            out(error)
            return
        ok, error = chat_context.ensure_source_matches_group(source, group["team_id"])
        if not ok:
            out(error)
            return
        binding = group["binding"]

    allowed, reason = permissions.can_scan_source(actor, source)
    if not allowed:
        out(json_fail("permission_denied", reason))
        return

    if not updates.get("has_updates"):
        source_label = source.get("source_label", args.source_id)
        out({
            "success": True,
            "has_updates": False,
            "message": "没有发现更新。",
            "interactive_card": cards.no_updates(source_label),
        })
        return

    change_count = updates.get("change_count", 0)
    deliver_to = delivery(chat_type or "direct", args.chat_id if chat_type == "group" else "", actor, args.message_thread_id, args.account_id)
    if change_count > args.threshold:
        task_id = sc.new_record_id("task")
        task_record = {
            "type": "incremental_update_confirm",
            "source_id": args.source_id,
            "created_by": actor,
            "chat_type": chat_type or "direct",
            "chat_id": args.chat_id if chat_type == "group" else "",
            "message_sid": args.message_sid,
            "message_thread_id": args.message_thread_id,
            "account_id": args.account_id or "default",
            "deliver_to": deliver_to,
            "updates_file": str(path),
            "change_count": change_count,
            "created_at": now_str(),
        }
        sc.update_json("active_tasks.json", lambda current: {**current, task_id: task_record}, default={})
        out({
            "success": True,
            "needs_confirm": True,
            "task_id": task_id,
            "change_count": change_count,
            "interactive_card": cards.incremental_confirm(task_id, source.get("source_label", args.source_id), change_count),
        })
        return

    job_id = sc.new_record_id("job")
    job_record = {
        "type": "incremental_compile",
        "status": "pending",
        "source_id": args.source_id,
        "source_type": source.get("source_type", ""),
        "source_label": source.get("source_label", ""),
        "source_url": source.get("source_url", ""),
        "source_ref": source.get("source_ref", ""),
        "source_owner": source.get("source_owner", ""),
        "source_repo": source.get("source_repo", ""),
        "created_by": actor,
        "chat_type": chat_type or "direct",
        "chat_id": args.chat_id if chat_type == "group" else "",
        "message_sid": args.message_sid,
        "message_thread_id": args.message_thread_id,
        "account_id": args.account_id or "default",
        "deliver_to": deliver_to,
        "binding": binding,
        "target_scope": source.get("target_scope"),
        "target_team_id": source.get("target_team_id", ""),
        "target_project_id": source.get("target_project_id", ""),
        "target_kb_owner": source.get("target_kb_owner"),
        "target_kb_repo": source.get("target_kb_repo"),
        "changes": updates.get("changes", {}),
        "change_count": change_count,
        "current_fingerprints": updates.get("current_fingerprints", {}),
        "current_commit": updates.get("current_commit", ""),
        "updates_file": str(path),
        "batch_size": args.threshold,
        "next_cursor": 0,
        "auto_continue": True,
        "execution_mode": "background_worker",
        "worker_required": True,
        "worker_spawn": {},
        "notified": False,
        "notify_status": "not_ready",
        "notify_attempts": 0,
        "notify_last_error": "",
        "created_at": now_str(),
        "updated_at": now_str(),
    }
    sc.update_json("jobs.json", lambda current: {**current, job_id: job_record}, default={})
    out({"success": True, "needs_confirm": False, "job_id": job_id, "change_count": change_count})


if __name__ == "__main__":
    main()
