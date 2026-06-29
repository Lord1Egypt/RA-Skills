from __future__ import annotations

import argparse
import json
from pathlib import Path

import chat_context
import file_classifier as fc
import gitea_api as g
import permissions
import source_registry
import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_id", required=True)
    parser.add_argument("--open_id", default="system")
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--message_sid", default="", help="OpenClaw MessageSid for audit.")
    parser.add_argument("--update_state", action="store_true", help="无变化时也更新 last_scan_time")
    parser.add_argument("--save_to", default="", help="optional path to write the JSON scan result")
    args = parser.parse_args()

    source = source_registry.get_source(args.source_id)
    if not source:
        out(json_fail("source_not_found", "找不到资料源。"))
        return

    actor = chat_context.actor_id(args.open_id, args.sender_id)
    chat_type = chat_context.normalize_chat_type(args.chat_type)
    binding = None
    if chat_type == "group":
        if actor in {"", "system"}:
            out(json_fail("missing_sender_id", "群聊手动扫描必须传入 SenderId。"))
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
    if source.get("source_type") not in {"gitea_repo", "obsidian_git_repo"}:
        out(json_fail("unsupported_source", "当前增量扫描只支持 Gitea/Obsidian Git 资料源。"))
        return
    try:
        ref = source.get("source_ref") or g.default_branch(source["source_owner"], source["source_repo"])
        current_commit = g.branch_commit_sha(source["source_owner"], source["source_repo"], ref)
        tree = g.list_tree(source["source_owner"], source["source_repo"], ref, recursive=True)
    except Exception as exc:
        out(json_fail("cannot_read_source", str(exc)))
        return

    current, details = classify_tree(tree)

    old = source.get("file_fingerprints", {})
    added = [details[p] for p in sorted(current) if p not in old]
    modified = [details[p] for p in sorted(current) if p in old and old[p] != current[p]]
    deleted = [{"path": p, "old_sha": old[p]} for p in sorted(old) if p not in current]
    has_updates = bool(added or modified or deleted)

    if args.update_state and not has_updates:
        source["last_scan_time"] = now_str()
        sc.update_json("sources.json", lambda current: {**current, args.source_id: source}, default={})

    result = {
        "success": True,
        "source_id": args.source_id,
        "has_updates": has_updates,
        "changes": {"added": added, "modified": modified, "deleted": deleted},
        "change_count": len(added) + len(modified) + len(deleted),
        "current_fingerprints": current,
        "current_commit": current_commit,
        "ref": ref,
        "chat_type": chat_type or "direct",
        "chat_id": args.chat_id if chat_type == "group" else "",
        "message_sid": args.message_sid,
        "binding": binding,
    }
    if args.save_to:
        target = Path(args.save_to)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["saved_to"] = str(target)
    out(result)


if __name__ == "__main__":
    main()
