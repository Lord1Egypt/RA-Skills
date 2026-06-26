import sqlite3
from pathlib import Path

from app.db.bootstrap import bootstrap_database


def _migrate_auto_feedback_column(db_path: Path) -> bool:
    """Add auto_feedback_processed column to reply_pairs if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    try:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(reply_pairs)").fetchall()]
        if "auto_feedback_processed" not in cols:
            conn.execute("ALTER TABLE reply_pairs ADD COLUMN auto_feedback_processed INTEGER DEFAULT 0")
            conn.commit()
            print("  Migrated: added auto_feedback_processed column to reply_pairs")
            return True
        return False
    finally:
        conn.close()


def _migrate_embedding_columns(db_path: Path) -> bool:
    """Add embedding BLOB columns to chunks and reply_pairs if missing."""
    conn = sqlite3.connect(db_path)
    migrated = False
    try:
        for table in ("chunks", "reply_pairs"):
            cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
            if "embedding" not in cols:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN embedding BLOB")
                conn.commit()
                print(f"  Migrated: added embedding column to {table}")
                migrated = True
        return migrated
    finally:
        conn.close()


def _migrate_sender_profiles(db_path: Path) -> bool:
    """Create sender_profiles table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    try:
        existing = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='sender_profiles'").fetchone()
        if existing:
            return False
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sender_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                display_name TEXT,
                domain TEXT,
                company TEXT,
                sender_type TEXT,
                relationship_note TEXT,
                reply_count INTEGER DEFAULT 0,
                avg_reply_words REAL,
                first_seen TEXT,
                last_seen TEXT,
                topics_json TEXT DEFAULT '[]',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_sender_profiles_email ON sender_profiles(email);
            CREATE INDEX IF NOT EXISTS idx_sender_profiles_domain ON sender_profiles(domain);
        """)
        conn.commit()
        print("  Migrated: created sender_profiles table")
        return True
    finally:
        conn.close()


def _migrate_draft_history(db_path: Path) -> bool:
    """Create draft_history table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    try:
        existing = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='draft_history'").fetchone()
        if existing:
            return False
        conn.execute("""
            CREATE TABLE IF NOT EXISTS draft_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inbound_text TEXT NOT NULL,
                sender TEXT,
                generated_draft TEXT NOT NULL,
                final_reply TEXT,
                edit_distance_pct REAL,
                confidence TEXT,
                model_used TEXT,
                retrieval_method TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("  Migrated: created draft_history table")
        return True
    finally:
        conn.close()


def main() -> None:
    db_path = bootstrap_database()
    print(f"Bootstrapped database at {db_path}")
    migrated = _migrate_auto_feedback_column(db_path)
    if not migrated:
        print("  auto_feedback_processed column already exists")
    emb_migrated = _migrate_embedding_columns(db_path)
    if not emb_migrated:
        print("  embedding columns already exist")
    sp_migrated = _migrate_sender_profiles(db_path)
    if not sp_migrated:
        print("  sender_profiles table already exists")
    dh_migrated = _migrate_draft_history(db_path)
    if not dh_migrated:
        print("  draft_history table already exists")


if __name__ == "__main__":
    main()
