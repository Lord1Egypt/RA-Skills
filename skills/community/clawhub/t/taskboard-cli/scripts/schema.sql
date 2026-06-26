-- TaskBoard Schema v2
-- SQLite backend for multi-agent task coordination

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    acceptance_criteria TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'todo' 
        CHECK(status IN ('todo','in_progress','done','blocked','rejected')),
    priority TEXT NOT NULL DEFAULT 'normal'
        CHECK(priority IN ('low','normal','high','urgent')),
    assigned_to TEXT DEFAULT NULL,
    created_by TEXT NOT NULL,
    parent_id INTEGER DEFAULT NULL REFERENCES tasks(id),
    thread_id TEXT DEFAULT NULL,
    on_ack TEXT DEFAULT NULL,
    on_done TEXT DEFAULT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS task_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS task_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    field TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_by TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_assigned ON tasks(assigned_to, status);
CREATE INDEX IF NOT EXISTS idx_tasks_parent ON tasks(parent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_comments_task ON task_comments(task_id);
CREATE INDEX IF NOT EXISTS idx_updates_task ON task_updates(task_id);
