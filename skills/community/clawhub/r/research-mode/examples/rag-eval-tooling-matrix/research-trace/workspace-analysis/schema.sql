-- Research Mode SQLite bootstrap schema (optional structured-analysis layer)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS _rm_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS _rm_sources (
    source_id TEXT PRIMARY KEY,
    source_ref TEXT,
    source_title TEXT,
    source_url TEXT,
    imported_at TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS _rm_artifacts (
    artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    path TEXT NOT NULL,
    note TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT INTO _rm_meta (key, value) VALUES
    ('schema_version', '1'),
    ('task_scoped', 'true')
ON CONFLICT(key) DO NOTHING;
