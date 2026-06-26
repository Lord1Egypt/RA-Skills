import os
import json
import sqlite3
import asyncio
import chromadb
import requests
import filelock


def configure_global_environment(db_path: str = "./chroma_db"):
    """
    Sets process-wide environment variables for ChromaDB/HuggingFace caching.
    Must be run synchronously at startup to prevent async race conditions.
    """
    cache_dir = os.path.join(db_path, ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    os.environ["CHROMA_CACHE_DIR"] = cache_dir
    os.environ["HF_HOME"] = cache_dir


def get_db_connection(db_path: str = "openclaw.db") -> sqlite3.Connection:
    # ADDED: check_same_thread=False to prevent async threading crashes
    conn = sqlite3.connect(db_path, timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.commit()
    return conn


def get_chroma_lock(db_path: str = "./chroma_db") -> filelock.FileLock:
    """
    FIX (concurrency): Returns a cross-process file lock for serializing ChromaDB
    write operations.

    ChromaDB's embedded PersistentClient (SQLite metadata store + HNSW index) is NOT
    safe for concurrent writers across processes. If two daily_worker.py cron jobs
    overlap, simultaneous writes corrupt the HNSW segment and SQLite WAL.

    Callers MUST acquire this lock (as a context manager) before any ChromaDB
    .add() or .upsert() call:

        chroma_lock = get_chroma_lock(config["CHROMA_DB_PATH"])
        with chroma_lock:
            collection.add(...)

    Read-only operations (.count(), .query()) do not need the lock.
    Lock timeout is 120 seconds — long enough to cover a full embedding + write
    cycle, short enough to surface deadlocks quickly.
    """
    os.makedirs(db_path, exist_ok=True)
    lock_path = os.path.join(db_path, ".chromadb.lock")
    return filelock.FileLock(lock_path, timeout=120)


def get_vector_collection(db_path: str = "./chroma_db"):
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(
        name="published_posts",
        metadata={"hnsw:space": "cosine"}
    )


def validate_llm_provider(config: dict):
    provider = config.get("LLM_PROVIDER", "gemini").lower()

    if provider == "gemini":
        if not config.get("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY is required for the Gemini provider.")
        import google.generativeai as genai
        genai.configure(api_key=config["GEMINI_API_KEY"])
        models = [m.name for m in genai.list_models()]
        if not any("gemini" in m for m in models):
            raise ValueError("Gemini API key is invalid or lacks model access.")

    elif provider == "openai":
        if not config.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is required for the OpenAI provider.")
        from openai import OpenAI
        client = OpenAI(api_key=config["OPENAI_API_KEY"])
        client.models.list()

    elif provider == "anthropic":
        if not config.get("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY is required for the Anthropic provider.")
        from anthropic import Anthropic, AuthenticationError
        try:
            client = Anthropic(api_key=config["ANTHROPIC_API_KEY"])
            # Lightweight 1-token ping to verify the key is live
            client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}]
            )
        except AuthenticationError:
            raise ValueError("Anthropic API key is invalid or lacks access.")
        except Exception as e:
            raise ValueError(f"Anthropic API connectivity check failed: {e}")

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: '{provider}'")


def validate_wp_credentials(config: dict):
    # FIX (security): Enforce HTTPS before transmitting credentials.
    # Basic Auth (WP Application Passwords) sends credentials in the Authorization
    # header, which is plaintext over HTTP. An http:// URL would broadcast the
    # WordPress admin password across the network in cleartext.
    wp_url = config.get("WP_URL", "")
    if not wp_url.lower().startswith("https://"):
        raise ValueError(
            f"WP_URL must use HTTPS to protect credentials in transit. "
            f"Received: '{wp_url[:40]}'. "
            "Update your .env to use https:// and ensure your server has a valid TLS certificate."
        )

    auth     = (config["WP_USERNAME"], config["WP_APP_PASSWORD"])
    base_url = wp_url.rstrip("/")

    # 1. Read check — verify authentication
    read_resp = requests.get(f"{base_url}/wp-json/wp/v2/users/me", auth=auth)
    if read_resp.status_code != 200:
        raise ValueError(f"WP authentication failed: {read_resp.text}")

    # 2. Write lifecycle check — create a draft, then immediately delete it
    post_resp = requests.post(
        f"{base_url}/wp-json/wp/v2/posts",
        auth=auth,
        json={"title": "OpenClaw API Test", "status": "draft"}
    )
    if post_resp.status_code != 201:
        raise ValueError(
            f"WP REST API write blocked (HTTP {post_resp.status_code}). "
            "Check security plugins (Wordfence, iThemes, Cloudflare) and allow POST/PUT requests."
        )

    post_id = post_resp.json()["id"]
    requests.delete(f"{base_url}/wp-json/wp/v2/posts/{post_id}?force=true", auth=auth)


def initialize_databases():
    # Make sure env config is set before any database/vector logic starts
    configure_global_environment()
    db_conn = get_db_connection()

    db_conn.executescript("""
        CREATE TABLE IF NOT EXISTS posts (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            query                TEXT NOT NULL UNIQUE,
            wp_post_id           INTEGER,
            wp_url               TEXT,
            wp_status            TEXT DEFAULT 'draft',
            meta_description     TEXT,
            embedding_text       TEXT,
            word_count           INTEGER,
            schema_types         TEXT,
            inbound_link_count   INTEGER DEFAULT 0,
            published_at         DATETIME,
            content_updated_at   DATETIME,
            wp_modified_date     DATETIME,
            last_modified_at     DATETIME,
            last_link_injected_at DATETIME,
            run_id               TEXT,
            created_at           DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS run_log (
            run_id               TEXT PRIMARY KEY,
            status               TEXT,
            query                TEXT,
            step_reached         INTEGER,
            error_message        TEXT,
            llm_calls            INTEGER DEFAULT 0,
            scrape_quality_score REAL,
            estimated_cost_usd   REAL,
            duration_seconds     REAL,
            created_at           DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS internal_links (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            source_post_id  INTEGER,
            target_post_id  INTEGER,
            anchor_text     TEXT,
            injected_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(source_post_id) REFERENCES posts(id),
            FOREIGN KEY(target_post_id) REFERENCES posts(id)
        );

        CREATE TABLE IF NOT EXISTS ctr_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            wp_post_id  INTEGER,
            gsc_query   TEXT,
            position    REAL,
            clicks      INTEGER,
            impressions INTEGER,
            ctr         REAL,
            recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db_conn.commit()
    db_conn.close()


if __name__ == "__main__":
    print("Validating credentials and initialising databases...")
    configure_global_environment()
    initialize_databases()
    # Add interactive prompt logic here if running manually