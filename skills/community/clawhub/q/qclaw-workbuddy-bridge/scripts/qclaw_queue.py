#!/usr/bin/env python3
"""
QClaw ↔ WorkBuddy 任务队列管理器
用法:
  python3 qclaw_queue.py add "任务描述" [--intent "用户意图"] [--ctx '{"key": "value"}']
  python3 qclaw_queue.py list [--status pending|done|all]
  python3 qclaw_queue.py poll [--wait]        # 阻塞式等待新任务
  python3 qclaw_queue.py poll --once          # 单次检查
  python3 qclaw_queue.py result <task_id>      # 获取任务结果
  python3 qclaw_queue.py done <task_id> <result_file>  # 标记完成并写入结果
  python3 qclaw_queue.py status <task_id> <status>
"""

import json
import os
import sys
import uuid
import time
import argparse
from datetime import datetime, timezone, timedelta

QUEUE_DIR = os.path.expanduser("~/.workbuddy/queue")
QUEUE_FILE = os.path.join(QUEUE_DIR, "qclaw_tasks.json")
QUEUE_FILE_LOCK = os.path.join(QUEUE_DIR, "qclaw_tasks.lock")

TZ_OFFSET = 8  # 北京时间

TRIGGER_FILE = os.path.join(QUEUE_DIR, ".trigger")

def beijing_now():
    return datetime.now(timezone(timedelta(hours=TZ_OFFSET)))

def _write_trigger():
    """写触发文件，唤醒 WorkBuddy"""
    os.makedirs(QUEUE_DIR, exist_ok=True)
    with open(TRIGGER_FILE, "w", encoding="utf-8") as f:
        json.dump({"fired_at": beijing_now().isoformat()}, f, ensure_ascii=False)

def ensure_queue():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    if not os.path.exists(QUEUE_FILE):
        data = {"tasks": [], "version": "1.0"}
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def read_queue():
    ensure_queue()
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_queue(data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── add ──────────────────────────────────────────────────────────────────────

def cmd_add(args):
    task = {
        "id": str(uuid.uuid4())[:8],
        "created_at": beijing_now().isoformat(),
        "status": "pending",
        "input": {
            "description": args.description,
            "intent": args.intent or args.description,
            "context": json.loads(args.ctx) if args.ctx else {},
        },
        "result": None,
        "error": None,
    }
    data = read_queue()
    data["tasks"].insert(0, task)  # 新任务放最前
    write_queue(data)
    # 写触发文件，唤醒 WorkBuddy
    _write_trigger()
    print(f"✅ 任务已入队 [{task['id']}]: {args.description}")
    print(f"   队列位置: {QUEUE_FILE}")
    return task["id"]

# ── list ─────────────────────────────────────────────────────────────────────

def cmd_list(args):
    data = read_queue()
    tasks = data.get("tasks", [])

    if args.status and args.status != "all":
        tasks = [t for t in tasks if t.get("status") == args.status]

    if not tasks:
        print("📭 队列为空")
        return

    print(f"📋 队列任务 (共 {len(tasks)} 条)\n")
    for t in tasks:
        icon = {"pending": "⏳", "processing": "🔄", "done": "✅", "error": "❌"}.get(t["status"], "?")
        created = t.get("created_at", "")[:19]
        print(f"  {icon} [{t['id']}] [{t['status']}] {created}")
        print(f"     {t['input']['description'][:60]}")
        if t.get("result"):
            res = t["result"]
            summary = res.get("summary", "")
            print(f"     → {summary[:80]}")
        if t.get("error"):
            print(f"     → ❌ {t['error'][:60]}")
        print()

# ── poll ─────────────────────────────────────────────────────────────────────

def cmd_poll(args):
    """阻塞/非阻塞地等待下一个 pending 任务"""
    seen = set()
    while True:
        data = read_queue()
        for t in data.get("tasks", []):
            if t["status"] == "pending" and t["id"] not in seen:
                seen.add(t["id"])
                print(json.dumps(t, ensure_ascii=False))
                if args.wait:
                    # 继续等待，不退出
                    continue
                else:
                    return
        if not args.wait:
            print("[]")
            return
        time.sleep(5)

# ── result ────────────────────────────────────────────────────────────────────

def cmd_result(args):
    data = read_queue()
    for t in data.get("tasks", []):
        if t["id"] == args.task_id:
            if t.get("result"):
                print(json.dumps(t["result"], ensure_ascii=False, indent=2))
            elif t.get("error"):
                print(f"❌ 任务执行失败: {t['error']}", file=sys.stderr)
                sys.exit(1)
            else:
                print("⏳ 任务尚未执行完成")
            return
    print(f"❌ 未找到任务: {args.task_id}", file=sys.stderr)
    sys.exit(1)

# ── mark done / error ─────────────────────────────────────────────────────────

def cmd_done(args):
    data = read_queue()
    result_data = None
    if args.result_file:
        if args.result_file == "-":
            result_data = json.loads(sys.stdin.read())
        else:
            with open(args.result_file, "r", encoding="utf-8") as f:
                result_data = json.load(f)
    else:
        result_data = {}

    for t in data.get("tasks", []):
        if t["id"] == args.task_id:
            t["status"] = "done"
            t["done_at"] = beijing_now().isoformat()
            t["result"] = result_data
            write_queue(data)
            print(f"✅ 任务 [{args.task_id}] 已标记完成")
            return
    print(f"❌ 未找到任务: {args.task_id}", file=sys.stderr)
    sys.exit(1)

def cmd_error(args):
    data = read_queue()
    for t in data.get("tasks", []):
        if t["id"] == args.task_id:
            t["status"] = "error"
            t["done_at"] = beijing_now().isoformat()
            t["error"] = args.message
            write_queue(data)
            print(f"❌ 任务 [{args.task_id}] 已标记失败: {args.message}")
            return
    print(f"❌ 未找到任务: {args.task_id}", file=sys.stderr)
    sys.exit(1)

def cmd_status(args):
    data = read_queue()
    for t in data.get("tasks", []):
        if t["id"] == args.task_id:
            t["status"] = args.new_status
            write_queue(data)
            print(f"📝 任务 [{args.task_id}] 状态 → {args.new_status}")
            return
    print(f"❌ 未找到任务: {args.task_id}", file=sys.stderr)
    sys.exit(1)

def cmd_trigger(args):
    """发送触发信号给 WorkBuddy（主动唤醒，不等待轮询）"""
    _write_trigger()
    print(f"🔔 触发信号已发送，WorkBuddy 将在下次调度时立即处理任务")

def cmd_watch(args):
    """阻塞式监听：等待触发信号到达后处理 pending 任务"""
    seen = set()
    once = getattr(args, "once", False)

    if once:
        # launchd / 完全无轮询模式：检查一次，有信号处理，无信号直接退出
        if not os.path.exists(TRIGGER_FILE):
            return  # 无信号，直接退出，不浪费任何资源
        print(f"🔔 收到触发信号（launchd），处理 pending 任务...")
    else:
        print(f"👁  监听触发信号文件: {TRIGGER_FILE}（按 Ctrl+C 退出）")
        while True:
            if os.path.exists(TRIGGER_FILE):
                print(f"\n🔔 收到触发信号，开始处理 pending 任务...")
                break
            time.sleep(5)
        seen = set()  # 重置 seen，确保每次手动启动都处理所有 pending

    os.remove(TRIGGER_FILE)
    data = read_queue()
    pending = [t for t in data.get("tasks", [])
               if t["status"] == "pending" and t["id"] not in seen]
    if not pending:
        print("   队列为空，跳过")
        return
    for t in pending:
        seen.add(t["id"])
        print(json.dumps(t, ensure_ascii=False))
    print("✅ 本轮处理完成，等待下一次触发信号...")

# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QClaw ↔ WorkBuddy 任务队列")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="添加新任务到队列")
    p_add.add_argument("description", help="任务描述")
    p_add.add_argument("--intent", help="原始用户意图")
    p_add.add_argument("--ctx", help="JSON 格式额外上下文")

    p_list = sub.add_parser("list", help="列出队列中的任务")
    p_list.add_argument("--status", choices=["pending", "done", "error", "all"], default="all")

    p_poll = sub.add_parser("poll", help="等待下一个 pending 任务（阻塞或非阻塞）")
    p_poll.add_argument("--wait", action="store_true", help="持续等待（不退出）")
    p_poll.add_argument("--once", action="store_true", help="单次检查后退出")

    p_result = sub.add_parser("result", help="获取任务结果")
    p_result.add_argument("task_id", help="任务 ID")

    p_done = sub.add_parser("done", help="标记任务完成并写入结果")
    p_done.add_argument("task_id", help="任务 ID")
    p_done.add_argument("result_file", nargs="?", default=None, help="结果 JSON 文件路径，- 表示 stdin")

    p_err = sub.add_parser("error", help="标记任务失败")
    p_err.add_argument("task_id", help="任务 ID")
    p_err.add_argument("message", help="错误信息")

    p_st = sub.add_parser("status", help="修改任务状态")
    p_st.add_argument("task_id", help="任务 ID")
    p_st.add_argument("new_status", choices=["pending", "processing", "done", "error"])

    sub.add_parser("trigger", help="发送触发信号给 WorkBuddy（主动唤醒）")
    p_watch = sub.add_parser("watch", help="阻塞监听触发信号，收到后处理 pending 任务")
    p_watch.add_argument("--once", action="store_true",
                         help="单次检查后退出（用于 launchd 等事件驱动场景，完全不轮询）")

    args = parser.parse_args()

    if args.cmd == "add":
        cmd_add(args)
    elif args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "poll":
        cmd_poll(args)
    elif args.cmd == "result":
        cmd_result(args)
    elif args.cmd == "done":
        cmd_done(args)
    elif args.cmd == "error":
        cmd_error(args)
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "trigger":
        cmd_trigger(args)
    elif args.cmd == "watch":
        cmd_watch(args)
    else:
        parser.print_help()
