#!/usr/bin/env python3
"""
Task Manager - SQLite-powered task management system

Usage:
    task add "title" [options]
    task list [options]
    task show <id>
    task update <id> [options]
    task start <id>
    task complete <id>
    task archive <id>
    task delete <id>
    task stats
"""

import sqlite3
import json
import uuid
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import argparse
import sys

# Database path - stored in skill's data/ directory for natural workspace isolation
# Each agent has their own skill directory copy, so data is naturally isolated
def get_db_path() -> Path:
    """Get database path in skill's data/ directory"""
    script_dir = Path(__file__).parent
    return script_dir / "data" / "tasks.db"

DB_PATH = get_db_path()


def get_connection():
    """Get database connection"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_db_initialized():
    """Ensure database is initialized, auto-init if not"""
    if not DB_PATH.exists():
        init_db(silent=True)
        return True
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    if not cursor.fetchone():
        conn.close()
        init_db(silent=True)
        return True
    conn.close()
    return False


def init_db(silent: bool = False):
    """Initialize database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'P2',
            status TEXT DEFAULT 'pending',
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            due_date TEXT,
            reminder_count INTEGER DEFAULT 0,
            max_reminders INTEGER DEFAULT 3,
            source TEXT,
            parent_id TEXT,
            metadata TEXT
        )
    """)
    
    # Create task_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            action TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON tasks(created_at)")
    
    conn.commit()
    conn.close()
    
    if not silent:
        print(f"✅ Database initialized: {DB_PATH}")


def add_task(title: str, priority: str = "P2", tags: List[str] = None, 
             desc: str = None, due: str = None, source: str = "manual") -> Optional[str]:
    """Create a task"""
    # Validate title
    if not title or not title.strip():
        print("❌ Task title cannot be empty")
        return None
    
    conn = get_connection()
    cursor = conn.cursor()
    
    task_id = str(uuid.uuid4())[:8]
    now = datetime.now().isoformat()
    tags_json = json.dumps(tags or [], ensure_ascii=False)
    
    cursor.execute("""
        INSERT INTO tasks (id, title, description, priority, status, tags, 
                          created_at, updated_at, due_date, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (task_id, title.strip(), desc, priority, "pending", tags_json, now, now, due, source))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Task created: {task_id}")
    print(f"   Title: {title}")
    print(f"   Priority: {priority}")
    if tags:
        print(f"   Tags: {', '.join(tags)}")
    return task_id


def list_tasks(status: str = None, priority: str = None, tags: str = None, 
               sort: str = "created", limit: int = 50):
    """List tasks"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if priority:
        query += f" AND priority IN ({','.join(['?']*len(priority.split(',')))})"
        params.extend(priority.split(','))
    
    if tags:
        query += " AND tags LIKE ?"
        params.append(f"%{tags}%")
    
    # Sorting
    if sort == "priority":
        query += " ORDER BY CASE priority WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 WHEN 'P3' THEN 3 END"
    elif sort == "due":
        query += " ORDER BY due_date IS NULL, due_date"
    else:
        query += " ORDER BY created_at DESC"
    
    query += f" LIMIT {limit}"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("No tasks found")
        return
    
    print(f"\n📋 Task list ({len(rows)} tasks)")
    print("-" * 80)
    
    status_icons = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "archived": "📁"}
    priority_icons = {"P0": "🔴", "P1": "🟠", "P2": "🟡", "P3": "🟢"}
    
    for row in rows:
        status_icon = status_icons.get(row["status"], "❓")
        priority_icon = priority_icons.get(row["priority"], "⚪")
        
        print(f"{status_icon} {priority_icon} [{row['id']}] {row['title']}")
        if row["tags"]:
            tags_list = json.loads(row["tags"])
            if tags_list:
                print(f"   Tags: {', '.join(tags_list)}")
        if row["due_date"]:
            print(f"   Due: {row['due_date']}")
    
    print("-" * 80)


def show_task(task_id: str):
    """Show task details"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print(f"❌ Task not found: {task_id}")
        return
    
    print(f"\n📋 Task details")
    print("-" * 60)
    print(f"ID: {row['id']}")
    print(f"Title: {row['title']}")
    print(f"Status: {row['status']}")
    print(f"Priority: {row['priority']}")
    
    if row['description']:
        print(f"Description: {row['description']}")
    
    if row['tags']:
        tags_list = json.loads(row['tags'])
        if tags_list:
            print(f"Tags: {', '.join(tags_list)}")
    
    print(f"Created: {row['created_at']}")
    print(f"Updated: {row['updated_at']}")
    
    if row['due_date']:
        print(f"Due date: {row['due_date']}")
    
    print(f"Reminders: {row['reminder_count']}/{row['max_reminders']}")
    
    if row['source']:
        print(f"Source: {row['source']}")
    
    print("-" * 60)


def update_task(task_id: str, silent: bool = False, **kwargs) -> bool:
    """Update task, returns success status"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if task exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        if not silent:
            print(f"❌ Task not found: {task_id}")
        conn.close()
        return False
    
    # Build update statement
    updates = []
    params = []
    
    for key, value in kwargs.items():
        if key == "tags" and isinstance(value, list):
            value = json.dumps(value, ensure_ascii=False)
        updates.append(f"{key} = ?")
        params.append(value)
    
    if not updates:
        if not silent:
            print("⚠️  No fields to update")
        conn.close()
        return False
    
    updates.append("updated_at = ?")
    params.append(datetime.now().isoformat())
    params.append(task_id)
    
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    
    # Record history
    cursor.execute("""
        INSERT INTO task_history (task_id, action, old_value, new_value, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (task_id, "update", json.dumps(dict(row), ensure_ascii=False), 
          json.dumps(kwargs, ensure_ascii=False), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    if not silent:
        print(f"✅ Task updated: {task_id}")
    return True


def complete_task(task_id: str):
    """Mark task as completed"""
    if update_task(task_id, silent=True, status="completed"):
        print(f"🎉 Task completed: {task_id}")
    else:
        print(f"❌ Task not found: {task_id}")


def start_task(task_id: str):
    """Mark task as in progress"""
    if update_task(task_id, silent=True, status="in_progress"):
        print(f"🔄 Task in progress: {task_id}")
    else:
        print(f"❌ Task not found: {task_id}")


def delete_task(task_id: str):
    """Delete task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        print(f"❌ Task not found: {task_id}")
        conn.close()
        return
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    print(f"✅ Task deleted: {task_id}")


def archive_task(task_id: str):
    """Archive task"""
    if update_task(task_id, silent=True, status="archived"):
        print(f"📁 Task archived: {task_id}")
    else:
        print(f"❌ Task not found: {task_id}")


def show_stats():
    """Show statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total tasks
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    # By status
    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    status_stats = dict(cursor.fetchall())
    
    # By priority
    cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
    priority_stats = dict(cursor.fetchall())
    
    # Completion rate
    completed = status_stats.get("completed", 0)
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    conn.close()
    
    print("\n📊 Task Statistics")
    print("=" * 60)
    print(f"Total: {total}")
    print(f"Pending: {status_stats.get('pending', 0)} | "
          f"In Progress: {status_stats.get('in_progress', 0)} | "
          f"Completed: {completed} | "
          f"Archived: {status_stats.get('archived', 0)}")
    print(f"P0: {priority_stats.get('P0', 0)} | "
          f"P1: {priority_stats.get('P1', 0)} | "
          f"P2: {priority_stats.get('P2', 0)} | "
          f"P3: {priority_stats.get('P3', 0)}")
    print(f"Completion rate: {completion_rate:.1f}%")
    print(f"Database: {DB_PATH}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Task Management System")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # init command
    subparsers.add_parser("init", help="Initialize database")
    
    # add command
    add_parser = subparsers.add_parser("add", help="Create task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--priority", "-p", default="P2", help="Priority (P0/P1/P2/P3)")
    add_parser.add_argument("--tags", "-t", help="Tags (comma-separated)")
    add_parser.add_argument("--desc", "-d", help="Description")
    add_parser.add_argument("--due", help="Due date")
    add_parser.add_argument("--source", "-s", default="manual", help="Source")
    
    # list command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--priority", help="Filter by priority (comma-separated)")
    list_parser.add_argument("--tags", help="Filter by tags")
    list_parser.add_argument("--sort", choices=["priority", "due", "created"], default="created", help="Sort order")
    list_parser.add_argument("--limit", "-l", type=int, default=50, help="Limit results")
    
    # show command
    show_parser = subparsers.add_parser("show", help="Show task details")
    show_parser.add_argument("task_id", help="Task ID")
    
    # update command
    update_parser = subparsers.add_parser("update", help="Update task")
    update_parser.add_argument("task_id", help="Task ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--desc", help="New description")
    update_parser.add_argument("--priority", help="New priority")
    update_parser.add_argument("--status", help="New status")
    update_parser.add_argument("--tags", help="New tags (comma-separated)")
    update_parser.add_argument("--due", help="New due date")
    update_parser.add_argument("--reminder-count", type=int, help="Reminder count")
    
    # complete command
    complete_parser = subparsers.add_parser("complete", help="Mark as completed")
    complete_parser.add_argument("task_id", help="Task ID")
    
    # start command
    start_parser = subparsers.add_parser("start", help="Mark as in progress")
    start_parser.add_argument("task_id", help="Task ID")
    
    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete task")
    delete_parser.add_argument("task_id", help="Task ID")
    
    # archive command
    archive_parser = subparsers.add_parser("archive", help="Archive task")
    archive_parser.add_argument("task_id", help="Task ID")
    
    # stats command
    subparsers.add_parser("stats", help="Show statistics")
    
    args = parser.parse_args()
    
    # Auto-init for non-init commands
    if args.command and args.command != "init":
        ensure_db_initialized()
    
    if args.command == "init":
        init_db()
    elif args.command == "add":
        tags = args.tags.split(",") if args.tags else None
        add_task(args.title, args.priority, tags, args.desc, args.due, args.source)
    elif args.command == "list":
        list_tasks(args.status, args.priority, args.tags, args.sort, args.limit)
    elif args.command == "show":
        show_task(args.task_id)
    elif args.command == "update":
        kwargs = {}
        if args.title:
            kwargs["title"] = args.title
        if args.desc:
            kwargs["description"] = args.desc
        if args.priority:
            kwargs["priority"] = args.priority
        if args.status:
            kwargs["status"] = args.status
        if args.tags:
            kwargs["tags"] = args.tags.split(",")
        if args.due:
            kwargs["due_date"] = args.due
        if args.reminder_count is not None:
            kwargs["reminder_count"] = args.reminder_count
        update_task(args.task_id, **kwargs)
    elif args.command == "complete":
        complete_task(args.task_id)
    elif args.command == "start":
        start_task(args.task_id)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "archive":
        archive_task(args.task_id)
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()