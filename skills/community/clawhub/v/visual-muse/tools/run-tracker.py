#!/usr/bin/env python3
"""创意工坊运行追踪器。记录每次生成的完整链路信息。"""

from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timezone, timedelta

RUNTIME_DIR = os.environ.get(
    "RUNTIME_DIR",
    "/home/node/.openclaw/workspace/runtime"
)

JST = timezone(timedelta(hours=8))


def new_run() -> dict:
    """创建新的运行记录。"""
    run_id = datetime.now(JST).strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
    run = {
        "run_id": run_id,
        "created_at": datetime.now(JST).isoformat(),
        "status": "started",
        "request": None,
        "prompt": None,
        "workflow_config": None,
        "render_result": None,
        "critic_result": None,
        "final_choice": None,
        "checkpoint": None,
        "lora": None,
        "template": None,
        "seeds": [],
        "errors": []
    }
    path = os.path.join(RUNTIME_DIR, f"{run_id}.json")
    os.makedirs(RUNTIME_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(run, f, ensure_ascii=False, indent=2)
    return {"run_id": run_id, "path": path}


def update_run(run_id: str, updates: dict) -> dict:
    """更新运行记录的指定字段。"""
    path = os.path.join(RUNTIME_DIR, f"{run_id}.json")
    if not os.path.exists(path):
        return {"error": f"运行记录不存在: {run_id}"}

    with open(path, "r", encoding="utf-8") as f:
        run = json.load(f)

    run.update(updates)
    run["updated_at"] = datetime.now(JST).isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(run, f, ensure_ascii=False, indent=2)

    return {"run_id": run_id, "updated_fields": list(updates.keys())}


def list_runs(limit: int = 10) -> list:
    """列出最近的运行记录。"""
    os.makedirs(RUNTIME_DIR, exist_ok=True)
    files = sorted(
        [f for f in os.listdir(RUNTIME_DIR) if f.endswith(".json")],
        reverse=True
    )[:limit]
    runs = []
    for f in files:
        path = os.path.join(RUNTIME_DIR, f)
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            runs.append({
                "run_id": data.get("run_id"),
                "created_at": data.get("created_at"),
                "status": data.get("status"),
                "checkpoint": data.get("checkpoint"),
                "template": data.get("template"),
            })
    return runs


def get_run(run_id: str) -> dict:
    """获取完整的运行记录。"""
    path = os.path.join(RUNTIME_DIR, f"{run_id}.json")
    if not os.path.exists(path):
        return {"error": f"运行记录不存在: {run_id}"}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="创意工坊运行追踪器")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("new", help="创建新运行记录")

    p_update = sub.add_parser("update", help="更新运行记录")
    p_update.add_argument("--run-id", required=True)
    p_update.add_argument("--data", required=True, help="JSON 格式的更新数据")

    p_list = sub.add_parser("list", help="列出最近的运行记录")
    p_list.add_argument("--limit", type=int, default=10)

    p_get = sub.add_parser("get", help="获取完整运行记录")
    p_get.add_argument("--run-id", required=True)

    args = parser.parse_args()

    if args.command == "new":
        result = new_run()
    elif args.command == "update":
        updates = json.loads(args.data)
        result = update_run(args.run_id, updates)
    elif args.command == "list":
        result = list_runs(args.limit)
    elif args.command == "get":
        result = get_run(args.run_id)
    else:
        result = {"error": "未知命令"}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
