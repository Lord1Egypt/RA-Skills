from __future__ import annotations

import argparse
import json
from pathlib import Path

import chat_context
import permissions
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def delivery(task: dict, chat_type: str, chat_id: str, actor: str, thread_id: str, account_id: str) -> dict:
    existing = task.get("deliver_to") or {}
    if existing.get("target") or existing.get("targets"):
        return existing
    target = chat_id if chat_type == "group" else actor
    return {
        "channel": "feishu",
        "target": target,
        "targets": [target] if target else [],
        "chat_type": chat_type or "direct",
        "thread_id": thread_id,
        "account_id": account_id or "default",
    }


def load_scan(task: dict) -> dict:
    updates_file = task.get("updates_file", "")
    if updates_file and Path(updates_file).exists():
        return json.loads(Path(updates_file).read_text(encoding="utf-8"))
    return {
        "changes": task.get("changes", {}),
        "change_count": task.get("change_count", 0),
        "current_fingerprints": task.get("current_fingerprints", {}),
        "current_commit": task.get("current_commit", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", required=True)
    parser.add_argument("--confirmed_by", required=True)
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--message_sid", default="", help="OpenClaw MessageSid for audit.")
    parser.add_argument("--message_thread_id", default="", help="OpenClaw MessageThreadId, if any.")
    parser.add_argument("--account_id", default="default", help="OpenClaw AccountId.")
    args = parser.parse_args()

    tasks = sc.active_tasks()
    task = tasks.get(args.task_id)
    if not task:
        out(json_fail("task_not_found", "找不到待确认的增量更新任务。"))
        return
    if task.get("type") != "incremental_update_confirm":
        out(json_fail("bad_task_type", "该任务不是增量更新确认任务。"))
        return

    source_id = task.get("source_id", "")
    source = sc.sources().get(source_id)
    if not source:
        out(json_fail("source_not_found", "找不到该任务对应的资料源。"))
        return

    actor = chat_context.actor_id(args.confirmed_by, args.sender_id)
    chat_type = chat_context.normalize_chat_type(args.chat_type)
    task_chat_type = task.get("chat_type", "")
    task_chat_id = task.get("chat_id", "")
    binding = None
    if task_chat_type == "group" and chat_type != "group":
        out(json_fail("confirm_context_mismatch", "该任务是在群聊中创建的，请回到原群确认。"))
        return
    if chat_type == "group":
        if task_chat_id and args.chat_id != task_chat_id:
            out(json_fail("chat_id_mismatch", "请在创建该任务的同一个群里确认。"))
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

    if task.get("created_by") == "system":
        allowed, reason = permissions.can_config_source(actor, source)
    else:
        allowed, reason = permissions.can_scan_source(actor, source)
    if not allowed:
        out(json_fail("permission_denied", reason))
        return
    scan = load_scan(task)
    final_chat_type = chat_type or task_chat_type or "direct"
    final_chat_id = args.chat_id if chat_type == "group" else task_chat_id
    job_id = sc.new_record_id("job")
    job_record = {
        "type": "incremental_compile",
        "status": "pending",
        "source_id": source_id,
        "source_type": source.get("source_type", ""),
        "source_label": source.get("source_label", ""),
        "source_url": source.get("source_url", ""),
        "source_ref": source.get("source_ref", ""),
        "source_owner": source.get("source_owner", ""),
        "source_repo": source.get("source_repo", ""),
        "created_by": task.get("created_by", actor),
        "confirmed_by": actor,
        "chat_type": final_chat_type,
        "chat_id": final_chat_id,
        "message_sid": args.message_sid,
        "message_thread_id": args.message_thread_id or task.get("message_thread_id", ""),
        "account_id": args.account_id or task.get("account_id", "default"),
        "deliver_to": delivery(
            task,
            final_chat_type,
            final_chat_id,
            task.get("created_by", actor),
            args.message_thread_id or task.get("message_thread_id", ""),
            args.account_id or task.get("account_id", "default"),
        ),
        "binding": binding,
        "target_scope": source.get("target_scope"),
        "target_team_id": source.get("target_team_id", ""),
        "target_project_id": source.get("target_project_id", ""),
        "target_kb_owner": source.get("target_kb_owner"),
        "target_kb_repo": source.get("target_kb_repo"),
        "changes": scan.get("changes", {}),
        "change_count": scan.get("change_count", task.get("change_count", 0)),
        "current_fingerprints": scan.get("current_fingerprints", {}),
        "current_commit": scan.get("current_commit", ""),
        "batch_size": 100,
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

    def mutate_jobs(current: dict) -> dict:
        current[job_id] = job_record
        return current

    def mutate_tasks(current: dict) -> dict:
        current.pop(args.task_id, None)
        return current

    try:
        sc.update_json("jobs.json", mutate_jobs, default={})
        sc.update_json("active_tasks.json", mutate_tasks, default={})
    except Exception as exc:
        out(json_fail("confirm_incremental_failed", str(exc)))
        return
    out({"success": True, "job_id": job_id, "change_count": job_record["change_count"]})


if __name__ == "__main__":
    main()
