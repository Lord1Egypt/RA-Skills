from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def can_cancel(task: dict, sender_id: str) -> tuple[bool, str]:
    if task.get("created_by") == sender_id:
        return True, ""
    if task.get("created_by") != "system":
        return False, "只有触发该扫描的人可以取消。"
    source = sc.sources().get(task.get("source_id", ""), {})
    if source.get("target_scope") == "personal":
        return (source.get("created_by") == sender_id), "只有资料源 owner 可以取消。"
    if source.get("target_scope") == "team":
        team = sc.teams().get(source.get("target_team_id", ""), {})
        return (sender_id in team.get("admins", [])), "只有团队管理员可以取消定时扫描创建的确认任务。"
    return False, "不能确认操作者是否有取消权限。"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", required=True)
    parser.add_argument("--sender_id", required=True)
    args = parser.parse_args()

    tasks = sc.active_tasks()
    task = tasks.get(args.task_id)
    if not task:
        out(json_fail("task_not_found", "找不到待取消的增量确认任务。"))
        return
    if task.get("type") != "incremental_update_confirm":
        out(json_fail("bad_task_type", "该任务不是增量更新确认任务。"))
        return
    allowed, reason = can_cancel(task, args.sender_id)
    if not allowed:
        out(json_fail("permission_denied", reason))
        return

    def mutate(current: dict) -> dict:
        current.pop(args.task_id, None)
        return current

    sc.update_json("active_tasks.json", mutate, default={})
    out({"success": True, "cancelled": True, "task_id": args.task_id, "cancelled_at": now_str()})


if __name__ == "__main__":
    main()
