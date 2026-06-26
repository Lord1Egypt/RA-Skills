#!/usr/bin/env python3
"""
SQLite persistence layer for YouTube Comment Moderator.
Single DB per installation. All scripts import from here.
"""

import os
import sqlite3
from datetime import datetime, timezone

DEFAULT_DB_PATH = os.environ.get(
    "YT_MOD_DB",
    os.path.join("data", "youtube-comment-moderator", "moderator.db")
)


def get_db(db_path=None):
    """Get a connection with WAL mode and foreign keys enabled."""
    path = db_path or DEFAULT_DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn):
    """Create tables if they don't exist."""
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS comments (
        comment_id    TEXT PRIMARY KEY,
        video_id      TEXT NOT NULL,
        channel_id    TEXT NOT NULL,
        author        TEXT,
        author_channel_id TEXT,
        text          TEXT,
        like_count    INTEGER DEFAULT 0,
        reply_count   INTEGER DEFAULT 0,
        published_at  TEXT,
        fetched_at    TEXT NOT NULL,
        classification TEXT,
        confidence    INTEGER,
        action        TEXT,
        action_detail TEXT,
        reply_draft   TEXT,
        processed_at  TEXT,
        raw_json      TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_comments_video ON comments(video_id);
    CREATE INDEX IF NOT EXISTS idx_comments_channel ON comments(channel_id);
    CREATE INDEX IF NOT EXISTS idx_comments_classification ON comments(classification);
    CREATE INDEX IF NOT EXISTS idx_comments_action ON comments(action);
    CREATE INDEX IF NOT EXISTS idx_comments_processed ON comments(processed_at);

    CREATE TABLE IF NOT EXISTS videos (
        video_id     TEXT PRIMARY KEY,
        channel_id   TEXT NOT NULL,
        title        TEXT,
        published_at TEXT,
        comment_count INTEGER DEFAULT 0,
        view_count   INTEGER DEFAULT 0,
        first_scanned TEXT,
        last_scanned  TEXT,
        fully_scanned INTEGER DEFAULT 0
    );

    CREATE INDEX IF NOT EXISTS idx_videos_channel ON videos(channel_id);

    CREATE TABLE IF NOT EXISTS channels (
        channel_id   TEXT PRIMARY KEY,
        channel_name TEXT,
        config_json  TEXT,
        added_at     TEXT NOT NULL,
        last_check   TEXT
    );

    CREATE TABLE IF NOT EXISTS moderation_log (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        comment_id   TEXT NOT NULL,
        action       TEXT NOT NULL,
        detail       TEXT,
        success      INTEGER DEFAULT 1,
        error        TEXT,
        created_at   TEXT NOT NULL,
        FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
    );

    CREATE INDEX IF NOT EXISTS idx_log_comment ON moderation_log(comment_id);
    CREATE INDEX IF NOT EXISTS idx_log_created ON moderation_log(created_at);
    """)
    conn.commit()


def upsert_comment(conn, comment, channel_id):
    """Insert or update a comment. Returns True if new."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute("""
            INSERT INTO comments (comment_id, video_id, channel_id, author,
                author_channel_id, text, like_count, reply_count,
                published_at, fetched_at, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(comment_id) DO UPDATE SET
                like_count = excluded.like_count,
                reply_count = excluded.reply_count,
                fetched_at = excluded.fetched_at
        """, (
            comment["comment_id"], comment["video_id"], channel_id,
            comment.get("author"), comment.get("author_channel_id"),
            comment.get("text"), comment.get("like_count", 0),
            comment.get("reply_count", 0), comment.get("published_at"),
            now, None
        ))
        # rowcount=1 means insert, not update (SQLite quirk: both return 1)
        # Check if it was already classified
        row = conn.execute(
            "SELECT processed_at FROM comments WHERE comment_id = ?",
            (comment["comment_id"],)
        ).fetchone()
        return row["processed_at"] is None
    except sqlite3.IntegrityError:
        return False


def mark_classified(conn, comment_id, classification, confidence, action, reply_draft=None):
    """Mark a comment as classified."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        UPDATE comments SET classification = ?, confidence = ?,
            action = ?, reply_draft = ?, processed_at = ?
        WHERE comment_id = ?
    """, (classification, confidence, action, reply_draft, now, comment_id))


def log_action(conn, comment_id, action, detail=None, success=True, error=None):
    """Log a moderation action."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        INSERT INTO moderation_log (comment_id, action, detail, success, error, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (comment_id, action, detail, 1 if success else 0, error, now))


def update_action(conn, comment_id, action, detail=None):
    """Update the action on a comment."""
    conn.execute(
        "UPDATE comments SET action = ?, action_detail = ? WHERE comment_id = ?",
        (action, detail, comment_id)
    )


def get_unprocessed(conn, channel_id=None):
    """Get comments that haven't been classified yet."""
    if channel_id:
        return conn.execute(
            "SELECT * FROM comments WHERE processed_at IS NULL AND channel_id = ?",
            (channel_id,)
        ).fetchall()
    return conn.execute(
        "SELECT * FROM comments WHERE processed_at IS NULL"
    ).fetchall()


def get_pending_actions(conn, channel_id=None):
    """Get classified comments awaiting action (reply_drafted, flagged_for_review)."""
    q = "SELECT * FROM comments WHERE action IN ('reply_drafted', 'flagged_for_review')"
    params = ()
    if channel_id:
        q += " AND channel_id = ?"
        params = (channel_id,)
    return conn.execute(q, params).fetchall()


def get_stats(conn, channel_id=None):
    """Get moderation stats."""
    where = ""
    params = ()
    if channel_id:
        where = "WHERE channel_id = ?"
        params = (channel_id,)

    total = conn.execute(f"SELECT COUNT(*) FROM comments {where}", params).fetchone()[0]

    if channel_id:
        classified = conn.execute(
            "SELECT COUNT(*) FROM comments WHERE channel_id = ? AND processed_at IS NOT NULL",
            (channel_id,)
        ).fetchone()[0]
    else:
        classified = conn.execute(
            "SELECT COUNT(*) FROM comments WHERE processed_at IS NOT NULL"
        ).fetchone()[0]

    rows = conn.execute(f"""
        SELECT classification, action, COUNT(*) as cnt
        FROM comments {where}
        GROUP BY classification, action
    """, params).fetchall()

    by_class = {}
    by_action = {}
    for r in rows:
        c = r["classification"] or "unclassified"
        a = r["action"] or "pending"
        by_class[c] = by_class.get(c, 0) + r["cnt"]
        by_action[a] = by_action.get(a, 0) + r["cnt"]

    return {"total": total, "classified": classified, "by_classification": by_class, "by_action": by_action}


def upsert_video(conn, video_id, channel_id, title=None, published_at=None,
                 comment_count=None, view_count=None):
    """Insert or update a video."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        INSERT INTO videos (video_id, channel_id, title, published_at,
            comment_count, view_count, first_scanned, last_scanned)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
            title = COALESCE(excluded.title, videos.title),
            comment_count = COALESCE(excluded.comment_count, videos.comment_count),
            view_count = COALESCE(excluded.view_count, videos.view_count),
            last_scanned = excluded.last_scanned
    """, (video_id, channel_id, title, published_at,
          comment_count, view_count, now, now))


def mark_video_scanned(conn, video_id):
    """Mark a video as fully scanned."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "UPDATE videos SET fully_scanned = 1, last_scanned = ? WHERE video_id = ?",
        (now, video_id)
    )


def get_scanned_videos(conn, channel_id):
    """Get set of video IDs that have been fully scanned for a channel."""
    rows = conn.execute(
        "SELECT video_id FROM videos WHERE channel_id = ? AND fully_scanned = 1",
        (channel_id,)
    ).fetchall()
    return {r["video_id"] for r in rows}


def is_known(conn, comment_id):
    """Check if a comment has already been processed."""
    row = conn.execute(
        "SELECT processed_at FROM comments WHERE comment_id = ?",
        (comment_id,)
    ).fetchone()
    return row is not None and row["processed_at"] is not None


def save_channel(conn, channel_id, channel_name, config_json=None):
    """Upsert channel info."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        INSERT INTO channels (channel_id, channel_name, config_json, added_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(channel_id) DO UPDATE SET
            channel_name = excluded.channel_name,
            config_json = COALESCE(excluded.config_json, channels.config_json)
    """, (channel_id, channel_name, config_json, now))


def update_last_check(conn, channel_id):
    """Update the last check timestamp for a channel."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "UPDATE channels SET last_check = ? WHERE channel_id = ?",
        (now, channel_id)
    )
