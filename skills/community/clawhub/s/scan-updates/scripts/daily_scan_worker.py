from __future__ import annotations

import argparse
import json

import cards
import file_classifier as fc
import gitea_api as g
import permissions
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def delivery_for_source(source: dict) -> dict:
    targets = []
    if source.get("target_scope") == "personal":
        owner = source.get("created_by", "")
        if owner and owner != "system":
            targets.append(owner)
    elif source.get("target_scope") == "team":
        team = sc.teams().get(source.get("target_team_id", ""), {})
        targets.extend([item for item in team.get("admins", []) if item])
    return {
        "channel": "feishu",
        "target": targets[0] if targets else "",
        "targets": targets,
        "chat_type": "direct",
        "thread_id": "",
        "account_id": "default",
    }


def classify_tree(tree: list[dict]) -> tuple[dict, dict]:
    current = {}
    details = {}
    raw_files = []
    has_code = False
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item.get("path", "")
        size = item.get("size") or 0
        cls = fc.classify(path, size)
        if cls["kind"] == "code":
            has_code = True
        raw_files.append((item, cls))
    for item, cls in raw_files:
        path = item.get("path", "")
        sha = item.get("sha", "")
        size = item.get("size") or 0
        if not has_code and path.rsplit("/", 1)[-1].lower().startswith("readme"):
            cls = {"kind": "markdown", "action": "document", "reason": "README in document-only repository"}
        current[path] = sha
        details[path] = {"path": path, "sha": sha, "size": size, **cls}
    return current, details


def scan_source(source_id: str, source: dict) -> dict:
    ref = source.get("source_ref") or g.default_branch(source["source_owner"], source["source_repo"])
    current_commit = g.branch_commit_sha(source["source_owner"], source["source_repo"], ref)
    tree = g.list_tree(source["source_owner"], source["source_repo"], ref, recursive=True)
    current, details = classify_tree(tree)

    old = source.get("file_fingerprints", {})
    added = [details[p] for p in sorted(current) if p not in old]
    modified = [details[p] for p in sorted(current) if p in old and old[p] != current[p]]
    deleted = [{"path": p, "old_sha": old[p]} for p in sorted(old) if p not in current]
    return {
        "source_id": source_id,
        "has_updates": bool(added or modified or deleted),
        "changes": {"added": added, "modified": modified, "deleted": deleted},
        "change_count": len(added) + len(modified) + len(deleted),
        "current_fingerprints": current,
        "current_commit": current_commit,
        "ref": ref,
    }


def create_task(source_id: str, source: dict, scan: dict, created_by: str) -> str:
    task_id = sc.new_record_id("task")
    task_record = {
        "type": "incremental_update_confirm",
        "source_id": source_id,
        "created_by": created_by,
        "deliver_to": delivery_for_source(source),
        "change_count": scan["change_count"],
        "changes": scan["changes"],
        "current_fingerprints": scan["current_fingerprints"],
        "current_commit": scan.get("current_commit", ""),
        "target_kb_owner": source.get("target_kb_owner"),
        "target_kb_repo": source.get("target_kb_repo"),
        "created_at": now_str(),
    }
    sc.update_json("active_tasks.json", lambda current: {**current, task_id: task_record}, default={})
    return task_id


def create_job(source_id: str, source: dict, scan: dict, created_by: str) -> str:
    job_id = sc.new_record_id("job")
    deliver_to = delivery_for_source(source)
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
        "created_by": created_by,
        "deliver_to": deliver_to,
        "target_scope": source.get("target_scope"),
        "target_team_id": source.get("target_team_id", ""),
        "target_project_id": source.get("target_project_id", ""),
        "target_kb_owner": source.get("target_kb_owner"),
        "target_kb_repo": source.get("target_kb_repo"),
        "changes": scan["changes"],
        "change_count": scan["change_count"],
        "current_fingerprints": scan["current_fingerprints"],
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
    sc.update_json("jobs.json", lambda current: {**current, job_id: job_record}, default={})
    return job_id


def touch_source(source_id: str, source: dict, status: str = "no_updates") -> None:
    source["last_scan_time"] = now_str()
    source["last_status"] = status
    sc.update_json("sources.json", lambda current: {**current, source_id: source}, default={})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=100)
    parser.add_argument("--created_by", default="system")
    parser.add_argument("--source_id", default="", help="optional single source for manual scan")
    args = parser.parse_args()

    sources = sc.sources()
    selected = {args.source_id: sources.get(args.source_id)} if args.source_id else sources
    results = []
    for source_id, source in selected.items():
        try:
            if not source:
                results.append({"source_id": source_id, "success": False, "error": "source_not_found"})
                continue
            if not source.get("enabled", True) or not source.get("auto_update", True):
                results.append({"source_id": source_id, "success": True, "skipped": "disabled_or_manual_source"})
                continue
            if source.get("source_type") not in {"gitea_repo", "obsidian_git_repo"}:
                results.append({"source_id": source_id, "success": True, "skipped": "unsupported_source_type"})
                continue
            allowed, reason = permissions.can_scan_source(args.created_by, source)
            if not allowed:
                results.append({"source_id": source_id, "success": False, "error": "permission_denied", "reason": reason})
                continue
            scan = scan_source(source_id, source)
            if not scan["has_updates"]:
                touch_source(source_id, source)
                results.append({"source_id": source_id, "success": True, "has_updates": False})
                continue
            if scan["change_count"] > args.threshold:
                task_id = create_task(source_id, source, scan, args.created_by)
                deliver_to = delivery_for_source(source)
                results.append({
                    "source_id": source_id,
                    "success": True,
                    "needs_confirm": True,
                    "task_id": task_id,
                    "change_count": scan["change_count"],
                    "deliver_to": deliver_to,
                    "interactive_card": cards.incremental_confirm(task_id, source.get("source_label", source_id), scan["change_count"]),
                })
            else:
                job_id = create_job(source_id, source, scan, args.created_by)
                results.append({"source_id": source_id, "success": True, "needs_confirm": False, "job_id": job_id, "change_count": scan["change_count"]})
        except Exception as exc:
            results.append({"source_id": source_id, "success": False, "error": str(exc)})
    out({"success": True, "results": results})


if __name__ == "__main__":
    main()
