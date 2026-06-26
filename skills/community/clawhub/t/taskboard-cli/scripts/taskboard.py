#!/usr/bin/env python3
"""TaskBoard CLI — lightweight SQLite task coordination for multi-agent workflows.

No network calls, no environment variables, no external dependencies.
Hooks print instructions to stdout for the agent to execute.
"""

import argparse
import sqlite3
import sys
import os
import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = SCRIPT_DIR / "schema.sql"
DEFAULT_DB = SCRIPT_DIR / "taskboard.db"

PRIORITY_EMOJI = {"urgent": "🔴", "high": "🟠", "normal": "🔵", "low": "⚪"}
STATUS_EMOJI = {"todo": "📋", "in_progress": "🔨", "done": "✅", "blocked": "🚫", "rejected": "❌"}
VALID_STATUSES = ("todo", "in_progress", "done", "blocked", "rejected")


def get_db(db_path=None):
    path = db_path or str(DEFAULT_DB)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    with open(SCHEMA_PATH) as f:
        db.executescript(f.read())
    # Migrate: add on_ack/on_done if missing (upgrade from v1)
    cols = [r[1] for r in db.execute("PRAGMA table_info(tasks)").fetchall()]
    if "on_ack" not in cols:
        db.execute("ALTER TABLE tasks ADD COLUMN on_ack TEXT DEFAULT NULL")
    if "on_done" not in cols:
        db.execute("ALTER TABLE tasks ADD COLUMN on_done TEXT DEFAULT NULL")
    return db


# ─── Commands ───────────────────────────────────────────────


def cmd_create(args):
    db = get_db(args.db)
    thread_id = args.thread_id
    if not thread_id and args.parent:
        parent = db.execute(
            "SELECT thread_id FROM tasks WHERE id = ?", (args.parent,)
        ).fetchone()
        if parent and parent["thread_id"]:
            thread_id = parent["thread_id"]

    on_ack = getattr(args, "on_ack", None)
    on_done = getattr(args, "on_done", None)

    cur = db.execute(
        """INSERT INTO tasks
           (title, description, acceptance_criteria, assigned_to, created_by,
            parent_id, priority, thread_id, on_ack, on_done)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            args.title,
            args.desc or "",
            args.criteria or "",
            args.assign,
            args.author,
            args.parent,
            args.priority or "normal",
            thread_id,
            on_ack,
            on_done,
        ),
    )
    task_id = cur.lastrowid
    db.commit()

    print(f"✅ Task #{task_id} created: {args.title}")
    if args.assign:
        print(f"   Assigned to: {args.assign}")
    if args.parent:
        print(f"   Parent: #{args.parent}")
    if thread_id:
        print(f"   Thread: {thread_id}")
    if on_ack:
        print(f"   on_ack: {on_ack}")
    if on_done:
        print(f"   on_done: {on_done}")


def cmd_list(args):
    db = get_db(args.db)
    conditions = []
    params = []

    if args.assigned_to:
        conditions.append("assigned_to = ?")
        params.append(args.assigned_to)
    if args.status:
        conditions.append("status = ?")
        params.append(args.status)
    if args.created_by:
        conditions.append("created_by = ?")
        params.append(args.created_by)
    if args.parent is not None:
        if args.parent == -1:
            conditions.append("parent_id IS NULL")
        else:
            conditions.append("parent_id = ?")
            params.append(args.parent)

    where = " WHERE " + " AND ".join(conditions) if conditions else ""

    if args.json:
        rows = db.execute(
            f"SELECT * FROM tasks{where} ORDER BY priority DESC, created_at DESC",
            params,
        ).fetchall()
        print(json.dumps([dict(r) for r in rows], indent=2))
        return

    rows = db.execute(
        f"""SELECT id, title, status, priority, assigned_to, parent_id
            FROM tasks{where}
            ORDER BY priority DESC, created_at DESC""",
        params,
    ).fetchall()

    if not rows:
        print("No tasks found.")
        return

    for r in rows:
        p = PRIORITY_EMOJI.get(r["priority"], "·")
        s = STATUS_EMOJI.get(r["status"], "·")
        parent = f" (sub of #{r['parent_id']})" if r["parent_id"] else ""
        assign = f" → {r['assigned_to']}" if r["assigned_to"] else " (unassigned)"
        print(
            f"  {p} #{r['id']:>3} {s} [{r['status']:<11}] {r['title']}{assign}{parent}"
        )


def cmd_show(args):
    db = get_db(args.db)
    task = db.execute("SELECT * FROM tasks WHERE id = ?", (args.id,)).fetchone()
    if not task:
        print(f"❌ Task #{args.id} not found")
        sys.exit(1)

    if args.json:
        t = dict(task)
        t["comments"] = [
            dict(c)
            for c in db.execute(
                "SELECT * FROM task_comments WHERE task_id = ? ORDER BY created_at",
                (args.id,),
            ).fetchall()
        ]
        t["subtasks"] = [
            dict(s)
            for s in db.execute(
                "SELECT id, title, status, assigned_to FROM tasks WHERE parent_id = ?",
                (args.id,),
            ).fetchall()
        ]
        print(json.dumps(t, indent=2))
        return

    print(f"\n{'='*50}")
    print(f"  Task #{task['id']}: {task['title']}")
    print(f"{'='*50}")
    print(
        f"  Status:    {STATUS_EMOJI.get(task['status'],'')} {task['status']}"
    )
    print(
        f"  Priority:  {PRIORITY_EMOJI.get(task['priority'],'')} {task['priority']}"
    )
    print(f"  Assigned:  {task['assigned_to'] or '(unassigned)'}")
    print(f"  Created by: {task['created_by']}")
    if task["parent_id"]:
        print(f"  Parent:    #{task['parent_id']}")
    print(f"  Created:   {task['created_at']}")
    print(f"  Updated:   {task['updated_at']}")
    if task["thread_id"]:
        print(f"  Thread:    {task['thread_id']}")
    if task["description"]:
        print(f"\n  📝 Description:\n  {task['description']}")
    if task["acceptance_criteria"]:
        print(f"\n  ✅ Acceptance Criteria:\n  {task['acceptance_criteria']}")

    on_ack = task["on_ack"] if "on_ack" in task.keys() else None
    on_done = task["on_done"] if "on_done" in task.keys() else None
    if on_ack:
        print(f"\n  🔔 On Ack: {on_ack}")
    if on_done:
        print(f"\n  🔔 On Done: {on_done}")

    subtasks = db.execute(
        "SELECT id, title, status, assigned_to FROM tasks WHERE parent_id = ?",
        (args.id,),
    ).fetchall()
    if subtasks:
        print(f"\n  📦 Subtasks:")
        for s in subtasks:
            se = STATUS_EMOJI.get(s["status"], "·")
            print(
                f"    {se} #{s['id']} [{s['status']}] {s['title']} → {s['assigned_to'] or '?'}"
            )

    comments = db.execute(
        "SELECT * FROM task_comments WHERE task_id = ? ORDER BY created_at",
        (args.id,),
    ).fetchall()
    if comments:
        print(f"\n  💬 Comments:")
        for c in comments:
            print(f"    [{c['created_at']}] {c['author']}: {c['content']}")
    print()


def cmd_update(args):
    db = get_db(args.db)
    task = db.execute("SELECT * FROM tasks WHERE id = ?", (args.id,)).fetchone()
    if not task:
        print(f"❌ Task #{args.id} not found")
        sys.exit(1)

    updates = []
    params = []
    changes = []

    if args.status:
        changes.append(("status", task["status"], args.status))
        updates.append("status = ?")
        params.append(args.status)
    if args.assign is not None:
        new_assign = args.assign if args.assign != "none" else None
        changes.append(("assigned_to", task["assigned_to"], new_assign))
        updates.append("assigned_to = ?")
        params.append(new_assign)
    if args.priority:
        changes.append(("priority", task["priority"], args.priority))
        updates.append("priority = ?")
        params.append(args.priority)
    if args.title:
        changes.append(("title", task["title"], args.title))
        updates.append("title = ?")
        params.append(args.title)
    if args.desc is not None:
        changes.append(("description", task["description"], args.desc))
        updates.append("description = ?")
        params.append(args.desc)
    if args.criteria is not None:
        changes.append(
            ("acceptance_criteria", task["acceptance_criteria"], args.criteria)
        )
        updates.append("acceptance_criteria = ?")
        params.append(args.criteria)
    if getattr(args, "on_ack", None) is not None:
        old = task["on_ack"] if "on_ack" in task.keys() else None
        changes.append(("on_ack", old, args.on_ack))
        updates.append("on_ack = ?")
        params.append(args.on_ack)
    if getattr(args, "on_done", None) is not None:
        old = task["on_done"] if "on_done" in task.keys() else None
        changes.append(("on_done", old, args.on_done))
        updates.append("on_done = ?")
        params.append(args.on_done)

    if not updates:
        print("Nothing to update.")
        return

    updates.append("updated_at = datetime('now')")
    params.append(args.id)

    db.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", params)

    author = args.author or "unknown"
    for field, old, new in changes:
        db.execute(
            "INSERT INTO task_updates (task_id, field, old_value, new_value, changed_by) VALUES (?, ?, ?, ?, ?)",
            (args.id, field, str(old), str(new), author),
        )

    db.commit()
    print(f"✅ Task #{args.id} updated:")
    for field, old, new in changes:
        print(f"   {field}: {old} → {new}")

    if args.note:
        db.execute(
            "INSERT INTO task_comments (task_id, author, content) VALUES (?, ?, ?)",
            (args.id, author, args.note),
        )
        db.commit()
        print(f"   📝 Note added")

    # Refresh and emit hooks
    task = db.execute("SELECT * FROM tasks WHERE id = ?", (args.id,)).fetchone()
    if args.status == "in_progress" and task["on_ack"]:
        print(f"\n🔔 ON_ACK: {task['on_ack']}")
    if args.status == "done" and task["on_done"]:
        print(f"\n🔔 ON_DONE: {task['on_done']}")


def cmd_comment(args):
    db = get_db(args.db)
    task = db.execute("SELECT id FROM tasks WHERE id = ?", (args.id,)).fetchone()
    if not task:
        print(f"❌ Task #{args.id} not found")
        sys.exit(1)

    db.execute(
        "INSERT INTO task_comments (task_id, author, content) VALUES (?, ?, ?)",
        (args.id, args.author, args.content),
    )
    db.commit()
    print(f"💬 Comment added to task #{args.id}")


def cmd_summary(args):
    db = get_db(args.db)
    rows = db.execute(
        "SELECT status, COUNT(*) as cnt FROM tasks GROUP BY status"
    ).fetchall()

    if not rows:
        print("No tasks yet.")
        return

    total = sum(r["cnt"] for r in rows)
    print(f"\n📊 TaskBoard Summary ({total} total)")
    print("─" * 30)
    for r in rows:
        e = STATUS_EMOJI.get(r["status"], "·")
        print(f"  {e} {r['status']:<12} {r['cnt']}")

    agents = db.execute(
        """SELECT assigned_to, COUNT(*) as cnt,
                  SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as done_cnt
           FROM tasks WHERE assigned_to IS NOT NULL
           GROUP BY assigned_to"""
    ).fetchall()
    if agents:
        print(f"\n👥 By Agent:")
        for a in agents:
            print(f"  {a['assigned_to']}: {a['done_cnt']}/{a['cnt']} done")
    print()


def cmd_history(args):
    db = get_db(args.db)
    rows = db.execute(
        "SELECT * FROM task_updates WHERE task_id = ? ORDER BY created_at",
        (args.id,),
    ).fetchall()
    if not rows:
        print(f"No history for task #{args.id}")
        return
    print(f"\n📜 History for task #{args.id}:")
    for r in rows:
        print(
            f"  [{r['created_at']}] {r['changed_by']}: {r['field']} {r['old_value']} → {r['new_value']}"
        )


def cmd_set_thread(args):
    db = get_db(args.db)
    task = db.execute("SELECT id FROM tasks WHERE id = ?", (args.id,)).fetchone()
    if not task:
        print(f"❌ Task #{args.id} not found")
        sys.exit(1)
    db.execute(
        "UPDATE tasks SET thread_id = ?, updated_at = datetime('now') WHERE id = ?",
        (args.thread_id, args.id),
    )
    db.commit()
    print(f"🔗 Task #{args.id} linked to thread {args.thread_id}")


def cmd_get_thread(args):
    db = get_db(args.db)
    task = db.execute(
        "SELECT thread_id FROM tasks WHERE id = ?", (args.id,)
    ).fetchone()
    if not task:
        print(f"❌ Task #{args.id} not found")
        sys.exit(1)
    if task["thread_id"]:
        print(task["thread_id"])
    else:
        print(f"No thread linked to task #{args.id}")
        sys.exit(1)


# ─── Main ───────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="TaskBoard — SQLite task coordination for multi-agent workflows"
    )
    parser.add_argument(
        "--db", help="Path to SQLite database (default: scripts/taskboard.db)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # create
    p = sub.add_parser("create", help="Create a new task")
    p.add_argument("title", help="Task title")
    p.add_argument("--desc", "-d", help="Description")
    p.add_argument("--criteria", "-c", help="Acceptance criteria")
    p.add_argument("--assign", "-a", help="Assign to agent")
    p.add_argument("--author", default="paimon", help="Created by")
    p.add_argument("--parent", "-p", type=int, help="Parent task ID")
    p.add_argument(
        "--priority",
        choices=["low", "normal", "high", "urgent"],
        default="normal",
    )
    p.add_argument("--thread-id", "-t", help="Discord thread ID")
    p.add_argument("--on-ack", help="Hook: action when task is acknowledged/started")
    p.add_argument("--on-done", help="Hook: action when task is completed")

    # list
    p = sub.add_parser("list", help="List tasks")
    p.add_argument("--assigned-to", "--mine", help="Filter by assignee")
    p.add_argument("--status", "-s", help="Filter by status")
    p.add_argument("--created-by", help="Filter by creator")
    p.add_argument("--parent", type=int, help="Filter by parent (-1 for top-level)")
    p.add_argument("--json", action="store_true", help="JSON output")

    # show
    p = sub.add_parser("show", help="Show task details")
    p.add_argument("id", type=int, help="Task ID")
    p.add_argument("--json", action="store_true", help="JSON output")

    # update
    p = sub.add_parser("update", help="Update a task")
    p.add_argument("id", type=int, help="Task ID")
    p.add_argument(
        "--status", "-s", choices=list(VALID_STATUSES)
    )
    p.add_argument("--assign", "-a", help='Reassign (use "none" to unassign)')
    p.add_argument("--priority", choices=["low", "normal", "high", "urgent"])
    p.add_argument("--title", help="New title")
    p.add_argument("--desc", "-d", help="New description")
    p.add_argument("--criteria", "-c", help="New acceptance criteria")
    p.add_argument("--note", "-n", help="Add a note/comment with the update")
    p.add_argument("--author", default="paimon", help="Updated by")
    p.add_argument("--on-ack", help="Hook: action on ack")
    p.add_argument("--on-done", help="Hook: action on done")

    # comment
    p = sub.add_parser("comment", help="Add a comment")
    p.add_argument("id", type=int, help="Task ID")
    p.add_argument("content", help="Comment text")
    p.add_argument("--author", default="paimon", help="Comment author")

    # summary
    sub.add_parser("summary", help="Show board summary")

    # history
    p = sub.add_parser("history", help="Show task change history")
    p.add_argument("id", type=int, help="Task ID")

    # set-thread
    p = sub.add_parser("set-thread", help="Link task to a Discord thread")
    p.add_argument("id", type=int, help="Task ID")
    p.add_argument("thread_id", help="Discord thread ID")

    # get-thread
    p = sub.add_parser("get-thread", help="Get linked thread ID")
    p.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    commands = {
        "create": cmd_create,
        "list": cmd_list,
        "show": cmd_show,
        "update": cmd_update,
        "comment": cmd_comment,
        "summary": cmd_summary,
        "history": cmd_history,
        "set-thread": cmd_set_thread,
        "get-thread": cmd_get_thread,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
