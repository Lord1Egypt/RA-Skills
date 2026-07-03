-- todos/schema/init_todos.sql
-- v1.0 初始化 schema (2026-06-10)
-- 业界参考：anthropics/skills todo 状态机 / GTD 方法论 / SOUL.md 规则15

CREATE TABLE IF NOT EXISTS todos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    content         TEXT    NOT NULL,                               -- 命令式："检查515070止损"
    active_form     TEXT    NOT NULL,                               -- 进行时："正在检查止损"
    status          TEXT    NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','in_progress','completed','cancelled','overdue')),
    priority        TEXT    NOT NULL DEFAULT 'medium'
                    CHECK (priority IN ('high','medium','low')),
    due_at          TEXT,                                           -- ISO8601，可空
    tags            TEXT    NOT NULL DEFAULT '[]',                 -- JSON 数组
    created_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    completed_at    TEXT,
    source          TEXT    NOT NULL DEFAULT 'chat',             -- chat/cron/import
    raw_input       TEXT                                        -- 用户原始输入，便于复盘
);

CREATE INDEX IF NOT EXISTS idx_todos_status   ON todos(status);
CREATE INDEX IF NOT EXISTS idx_todos_due       ON todos(due_at);
CREATE INDEX IF NOT EXISTS idx_todos_priority ON todos(priority);
CREATE INDEX IF NOT EXISTS idx_todos_tags      ON todos(tags);

-- 归档表（已完成/取消的不删除，30 天后清理）
CREATE TABLE IF NOT EXISTS todos_archive (
    id              INTEGER PRIMARY KEY,
    content         TEXT    NOT NULL,
    active_form     TEXT    NOT NULL,
    status          TEXT    NOT NULL,
    priority        TEXT    NOT NULL,
    due_at          TEXT,
    tags            TEXT    NOT NULL,
    created_at      TEXT    NOT NULL,
    updated_at      TEXT    NOT NULL,
    completed_at    TEXT,
    archived_at     TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    source          TEXT    NOT NULL DEFAULT 'chat',
    raw_input       TEXT
);

CREATE INDEX IF NOT EXISTS idx_archive_status ON todos_archive(status);
CREATE INDEX IF NOT EXISTS idx_archive_archived ON todos_archive(archived_at);

-- 审计日志（所有写操作）
CREATE TABLE IF NOT EXISTS audit_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    action      TEXT    NOT NULL,                                 -- add/list/done/del/update/archive
    todo_id     INTEGER,
    actor       TEXT    NOT NULL DEFAULT 'agent',                 -- user/agent/cron
    details     TEXT                                           -- JSON
);