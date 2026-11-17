#!/opt/homebrew/bin/python3
"""
OpenClaw Token Ledger Watcher (Unified v2026-03-17)
Watches ~/.openclaw/agents/main/sessions/*.jsonl for new lines,
parses usage, writes into SQLite ledger.db.

Usage:
  python3 ledger_watcher.py           # runs forever (daemon mode)
  python3 ledger_watcher.py --once    # one-shot scan (for cron/backfill)
  python3 ledger_watcher.py --sync-spark  # one-shot Spark token sync
"""

from __future__ import annotations

import json, glob, os, sys, sqlite3, time, hashlib, urllib.request, urllib.parse
from typing import Optional
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
SESSION_DIR   = Path.home() / ".openclaw/agents/main/sessions"
SESSIONS_JSON = SESSION_DIR / "sessions.json"
CRON_RUNS_DIR = Path.home() / ".openclaw/cron/runs"
LEDGER_DB     = Path.home() / ".openclaw/ledger.db"
CHECKPOINT    = Path.home() / ".openclaw/ledger-checkpoint.json"
SPARK_CHECKPOINT = Path.home() / ".openclaw/ledger-spark-checkpoint.json"
API_HUB_URL   = os.environ.get("LOCAL_API_HUB_URL", "http://127.0.0.1:3456")
SPARK_NFS_LOG = Path.home() / "spark-nfs/.spark/token-ledger.jsonl"
SPARK_LOCAL_LOG = Path.home() / ".openclaw/spark-token-ledger-segments/token-ledger.jsonl"
SPARK_ROTATIONS = 7

POLL_INTERVAL = max(1, int(os.environ.get("TOKEN_LEDGER_POLL_INTERVAL", "30")))
SPARK_SYNC_INTERVAL = 3600
PRICE_VERSION = "2026-03-17-unified"
PRICE_VERSION_FETCHED_AT = "2026-03-17T00:00:00Z"
PRICING_SOURCE_URLS = {
    "anthropic": "https://platform.claude.com/docs/en/about-claude/pricing",
    "openai": "https://developers.openai.com/api/docs/models",
    "google": "https://ai.google.dev/gemini-api/docs/pricing",
}

# Avoid re-opening every historical session file on every polling cycle.  The
# checkpoint remains the durable source of progress; this in-memory signature
# cache only suppresses work for files that have not changed since the last
# scan in the current process.
_file_signatures: dict[str, tuple[int, int]] = {}

# ── Pricing table (per 1M tokens) ───────────────────────────────────
PRICING = {
    "claude-opus-4-6":              {"input":5.00,  "output":25.00, "cacheRead":0.50,  "cacheWrite":6.25},
    "claude-sonnet-4-6":            {"input":3.00,  "output":15.00, "cacheRead":0.30,  "cacheWrite":3.75},
    "claude-haiku-4-5":             {"input":1.00,  "output":5.00,  "cacheRead":0.10,  "cacheWrite":1.25},
    "claude-haiku-3-5":             {"input":0.80,  "output":4.00,  "cacheRead":0.08,  "cacheWrite":1.00},
    "gpt-5.2":                      {"input":1.75,  "output":14.00, "cacheRead":0.175, "cacheWrite":0},
    "gpt-5.1":                      {"input":1.25,  "output":10.00, "cacheRead":0.125, "cacheWrite":0},
    "gpt-5":                        {"input":1.25,  "output":10.00, "cacheRead":0.125, "cacheWrite":0},
    "gpt-5-mini":                   {"input":0.25,  "output":2.00,  "cacheRead":0.025, "cacheWrite":0},
    "gpt-5-nano":                   {"input":0.05,  "output":0.40,  "cacheRead":0.005, "cacheWrite":0},
    "gpt-5.3-codex":                {"input":1.75,  "output":14.00, "cacheRead":0.175, "cacheWrite":0},
    "gpt-5.2-codex":                {"input":1.75,  "output":14.00, "cacheRead":0.175, "cacheWrite":0},
    "gpt-5.3-chat-latest":          {"input":1.75,  "output":14.00, "cacheRead":0.175, "cacheWrite":0},
    "gpt-5.2-chat-latest":          {"input":1.75,  "output":14.00, "cacheRead":0.175, "cacheWrite":0},
    "gemini-3-pro-preview":         {"input":2.00,  "output":12.00, "cacheRead":0.20,  "cacheWrite":0},
    "gemini-3-flash-preview":       {"input":0.50,  "output":3.00,  "cacheRead":0.05,  "cacheWrite":0},
    "gemini-3.1-pro-preview":       {"input":2.00,  "output":12.00, "cacheRead":0.20,  "cacheWrite":0},
    "gemini-3.1-flash-lite-preview":{"input":0.10,  "output":0.40,  "cacheRead":0.01,  "cacheWrite":0},
    "gemini-2.5-pro":               {"input":1.25,  "output":10.00, "cacheRead":0.125, "cacheWrite":0},
    "gemini-2.5-flash":             {"input":0.30,  "output":2.50,  "cacheRead":0.03,  "cacheWrite":0},
    "qwen-spark-35b":               {"input":0,     "output":0,     "cacheRead":0,     "cacheWrite":0},
    "qwen-spark-27b":               {"input":0,     "output":0,     "cacheRead":0,     "cacheWrite":0},
}

MODEL_ALIASES = {
    "claude-haiku-4-5-20251001": "claude-haiku-4-5",
    "claude-3-5-haiku-20241022": "claude-haiku-4-5",
    "qwen-spark": "qwen-spark-35b",
    "Qwen3.5-35B-A3B": "qwen-spark-35b",
    "Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf": "qwen-spark-35b",
    "qwen3.5:35b-a3b": "qwen-spark-35b",
}

LOCAL_PROVIDERS = {"local-dgx-spark", "local-macbook-pro", "llamacpp"}

# ── Helpers ──────────────────────────────────────────────────────────
def normalize_model(raw: str) -> str:
    if not raw: return "unknown"
    if "/" in raw: raw = raw.split("/", 1)[1]
    return MODEL_ALIASES.get(raw, raw)

def detect_provider(model_raw: str) -> str:
    if not model_raw: return "unknown"
    if model_raw.startswith("anthropic/"): return "anthropic"
    if model_raw.startswith("openai/"): return "openai"
    if model_raw.startswith("google/"): return "google"
    if "local-dgx-spark" in model_raw: return "local-dgx-spark"
    if "local-macbook-pro" in model_raw: return "local-macbook-pro"
    m = normalize_model(model_raw)
    if m.startswith("claude"): return "anthropic"
    if m.startswith("gpt") or m.startswith("o1") or m.startswith("o3") or m.startswith("o4"): return "openai"
    if m.startswith("gemini"): return "google"
    if "qwen" in m.lower() or "gguf" in m.lower(): return "local-dgx-spark"
    return "unknown"

def calc_cost(model: str, provider: str, u: dict) -> tuple[dict, str]:
    inp = u.get("input", 0) or 0
    out = u.get("output", 0) or 0
    cr  = u.get("cacheRead", 0) or 0
    cw  = u.get("cacheWrite", 0) or 0

    prov_cost = u.get("cost") or {}
    prov_total = prov_cost.get("total", 0) or 0
    if prov_total > 0:
        return {
            "input": prov_cost.get("input", 0) or 0,
            "output": prov_cost.get("output", 0) or 0,
            "cacheRead": prov_cost.get("cacheRead", 0) or 0,
            "cacheWrite": prov_cost.get("cacheWrite", 0) or 0,
            "total": prov_total,
        }, "provider"

    if provider in LOCAL_PROVIDERS:
        return {"input":0,"output":0,"cacheRead":0,"cacheWrite":0,"total":0}, "local"

    p = PRICING.get(model)
    if p:
        cost_in  = inp / 1e6 * p["input"]
        cost_out = out / 1e6 * p["output"]
        cost_cr  = cr  / 1e6 * p["cacheRead"]
        cost_cw  = cw  / 1e6 * p["cacheWrite"]
        return {"input": cost_in, "output": cost_out, "cacheRead": cost_cr, "cacheWrite": cost_cw, "total": cost_in + cost_out + cost_cr + cost_cw}, "calculated"

    return {"input":0,"output":0,"cacheRead":0,"cacheWrite":0,"total":0}, "unknown"

def session_key_from_path(path: str) -> str:
    name = os.path.basename(path)
    name = name.split(".jsonl")[0]
    return f"agent:main:{name}"

# ── Session Metadata Resolver ────────────────────────────────────────
import re as _re
_session_meta_cache: dict = {}
_session_meta_mtime: float = 0.0

def _detect_source_kind(session_key: str) -> str:
    if ":cron:" in session_key:
        return "cron"
    if ":subagent:" in session_key or ":run:" in session_key:
        return "subagent"
    return "interactive"

def load_session_meta() -> dict:
    global _session_meta_cache, _session_meta_mtime
    try:
        st = os.stat(SESSIONS_JSON)
        if st.st_mtime == _session_meta_mtime and _session_meta_cache:
            return _session_meta_cache
        _session_meta_mtime = st.st_mtime
    except OSError:
        return _session_meta_cache

    try:
        with open(SESSIONS_JSON, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[watcher] failed to load sessions.json: {e}", file=sys.stderr)
        return _session_meta_cache

    meta = {}
    for sk, entry in data.items():
        sid = entry.get("sessionId")
        if not sid: continue
        source_kind = _detect_source_kind(sk)
        # Detect channel and chat_id from session key
        channel = "unknown"
        chat_id = None
        thread_id_meta = None
        if "discord:" in sk: channel = "discord"
        elif "whatsapp" in sk: channel = "whatsapp"
        elif "telegram" in sk: channel = "telegram"

        # Extract chat_id from session key like "agent:main:discord:channel:1476967290254655508"
        m_chat = _re.search(r'discord:channel:(\d+)', sk)
        if m_chat: chat_id = m_chat.group(1)

        # Extract thread_id from session key like "...:topic:1479712989392273498"
        m_thread = _re.search(r':topic:(\d+)', sk)
        if m_thread: thread_id_meta = m_thread.group(1)

        # For cron sessions, extract delivery channel
        if source_kind == "cron":
            dc = entry.get("deliveryContext") or {}
            dc_to = dc.get("to", "") or ""
            m_dc = _re.search(r'(\d{17,20})', dc_to)
            if m_dc:
                chat_id = m_dc.group(1)
                channel = dc.get("channel", "") or "discord"

        meta[sid] = {
            "session_key": sk,
            "source_kind": source_kind,
            "channel": channel,
            "chat_id": chat_id,
            "thread_id": thread_id_meta,
        }
    _session_meta_cache = meta
    return meta

def resolve_session_meta(jsonl_path: str) -> dict:
    basename = os.path.basename(jsonl_path)
    # Strip .jsonl and any .deleted* / .reset* suffix
    full_stem = basename.split(".jsonl")[0]

    # Extract thread_id from -topic- suffix
    # e.g. "a2c6e616-...-topic-1477936395443245127"
    topic_match = _re.search(r'-topic-(\d{17,20})$', full_stem)
    if topic_match:
        base_uuid = full_stem[:topic_match.start()]
        thread_id = topic_match.group(1)
    else:
        base_uuid = full_stem
        thread_id = None

    meta_map = load_session_meta()

    # Try exact sessionId match (base UUID without -topic-)
    meta = meta_map.get(base_uuid)
    if meta:
        result = dict(meta)
        if thread_id and not result.get("thread_id"):
            result["thread_id"] = thread_id
        return result

    # Try full stem match
    meta = meta_map.get(full_stem)
    if meta:
        return meta

    session_key = session_key_from_path(jsonl_path)
    source_kind = "interactive"

    # Detect source kind from path and session key
    if CRON_RUNS_DIR in Path(jsonl_path).parents:
        source_kind = "cron"
    elif ":cron:" in session_key:
        source_kind = "cron"
    elif ":subagent:" in session_key:
        source_kind = "subagent"

    # Detect channel from session key
    channel = "unknown"
    if "discord:channel" in session_key: channel = "discord"
    elif "whatsapp" in session_key: channel = "whatsapp"
    elif source_kind == "cron": channel = "cron"
    if thread_id and channel == "unknown": channel = "discord"

    return {
        "session_key": session_key,
        "source_kind": source_kind,
        "channel": channel,
        "thread_id": thread_id,
    }

# ── Spark Token Sync ─────────────────────────────────────────────────
def load_spark_checkpoint() -> dict:
    if SPARK_CHECKPOINT.exists():
        try: return json.loads(SPARK_CHECKPOINT.read_text())
        except: pass
    return {"processed_ids": []}

def save_spark_checkpoint(cp: dict):
    cp_copy = dict(cp)
    cp_copy.pop("processed_ids", None)
    temp_path = SPARK_CHECKPOINT.with_name(f".{SPARK_CHECKPOINT.name}.{os.getpid()}.tmp")
    try:
        temp_path.write_text(json.dumps(cp_copy, indent=2, sort_keys=True) + "\n")
        temp_path.chmod(0o600)
        temp_path.replace(SPARK_CHECKPOINT)
    finally:
        temp_path.unlink(missing_ok=True)

def spark_segment_paths(base_path: Path = SPARK_LOCAL_LOG) -> list[Path]:
    paths = [Path(f"{base_path}.{index}") for index in range(SPARK_ROTATIONS, 0, -1)]
    paths.append(base_path)
    return [path for path in paths if path.is_file()]

def spark_segment_identity(path: Path) -> str:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            job_id = entry.get("job_id") or entry.get("id")
            timestamp = entry.get("timestamp") or entry.get("ts")
            if job_id or timestamp:
                raw = f"{timestamp or ''}\0{job_id or ''}".encode()
                return hashlib.sha256(raw).hexdigest()
    return hashlib.sha256(f"empty\0{path.name}".encode()).hexdigest()

def spark_entry_row(entry: dict) -> dict | None:
    job_id = entry.get("job_id") or entry.get("id")
    if not job_id:
        return None

    model = entry.get("model", "qwen-spark")
    if model in ("qwen-spark", "Qwen3.5-35B-A3B", "Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf", "qwen3.5:35b-a3b"):
        model = "qwen-spark-35b"
    elif "27b" in model.lower():
        model = "qwen-spark-27b"

    job_type = entry.get("job_type", "cron")
    task_name = entry.get("metadata", {}).get("task_id", job_type)
    return {
        "call_id": f"spark-{job_id}",
        "session_key": f"spark:{task_name}:{job_id}",
        "turn_hint": None,
        "ts": entry.get("timestamp") or entry.get("ts", ""),
        "provider": entry.get("provider", "local-dgx-spark"),
        "model": model,
        "model_raw": entry.get("model", "qwen-spark"),
        "call_reason": "primary",
        "input_tokens": entry.get("input_tokens", 0) or entry.get("input", 0),
        "output_tokens": entry.get("output_tokens", 0) or entry.get("output", 0),
        "cache_read_tokens": entry.get("cache_read_tokens", 0) or entry.get("cacheRead", 0),
        "cache_write_tokens": entry.get("cache_write_tokens", 0) or entry.get("cacheWrite", 0),
        "cost_input": 0, "cost_output": 0, "cost_cache_read": 0, "cost_cache_write": 0,
        "cost_total": 0, "cost_source": "local",
        "channel": "spark",
        "chat_id": None, "thread_id": None, "message_id": None,
        "source_kind": "cron" if job_type == "cron" else "spark",
        "cron_job_id": job_id if job_type == "cron" else None,
        "price_version": PRICE_VERSION,
        "usage_raw": json.dumps(entry),
    }

def scan_spark_segment(
    db: sqlite3.Connection,
    path: Path,
    start_line: int = 0,
    start_offset: int | None = None,
) -> tuple[int, int, int, str | None]:
    new_count = 0
    line_count = start_line if start_offset is not None else 0
    last_timestamp = None
    with path.open("rb") as handle:
        if start_offset is not None:
            handle.seek(start_offset)
        for raw_line in handle:
            line_count += 1
            if start_offset is None and line_count <= start_line:
                continue
            try:
                entry = json.loads(raw_line.decode("utf-8", errors="replace"))
            except (json.JSONDecodeError, UnicodeError):
                continue
            row = spark_entry_row(entry)
            if row is None:
                continue
            if insert_call(db, row, commit=False):
                new_count += 1
            last_timestamp = row["ts"] or last_timestamp
        next_offset = handle.tell()
    return new_count, line_count, next_offset, last_timestamp

def sync_spark_segment_files(db: sqlite3.Connection, cp: dict, paths: list[Path]) -> int:
    progress = cp.get("segments", {})
    next_progress = {}
    active_ids = []
    new_count = 0

    try:
        for path in paths:
            segment_id = spark_segment_identity(path)
            active_ids.append(segment_id)
            state = progress.get(segment_id, {})
            start_line = max(0, int(state.get("next_line", 0)))
            raw_offset = state.get("next_offset")
            start_offset = max(0, int(raw_offset)) if raw_offset is not None else None
            if start_offset is not None and start_offset > path.stat().st_size:
                start_line = 0
                start_offset = 0

            added, line_count, next_offset, last_timestamp = scan_spark_segment(
                db, path, start_line, start_offset
            )
            new_count += added

            if start_offset is None and start_line > line_count:
                # A legacy line-only checkpoint points past a truncated file.
                # Re-read from byte zero; INSERT OR IGNORE stays idempotent.
                added, line_count, next_offset, last_timestamp = scan_spark_segment(
                    db, path, 0, 0
                )
                new_count += added

            next_progress[segment_id] = {
                "next_line": line_count,
                "next_offset": next_offset,
                "last_timestamp": last_timestamp or state.get("last_timestamp"),
                "last_path": path.name,
            }
        db.commit()
    except Exception:
        db.rollback()
        raise

    cp["segments"] = {segment_id: next_progress[segment_id] for segment_id in active_ids}
    return new_count

def fetch_spark_entries_fallback() -> list[dict]:
    entries = []
    try:
        url = f"{API_HUB_URL}/spark/token-log?limit=1000"
        req = urllib.request.Request(url, method="GET")
        req.add_header("Accept", "application/json")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            if data.get("ok"):
                entries = data.get("entries", [])
    except Exception as exc:
        print(f"[spark_sync] API failed, trying NFS: {exc}", file=sys.stderr)
        try:
            if SPARK_NFS_LOG.exists():
                with SPARK_NFS_LOG.open("r") as handle:
                    for line in handle:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except Exception as nfs_exc:
            print(f"[spark_sync] NFS also failed: {nfs_exc}", file=sys.stderr)
    return entries

def sync_spark_tokens(db: sqlite3.Connection) -> int:
    cp = load_spark_checkpoint()
    paths = spark_segment_paths()
    if paths:
        new_count = sync_spark_segment_files(db, cp, paths)
        save_spark_checkpoint(cp)
        return new_count

    entries = fetch_spark_entries_fallback()
    new_count = 0
    for entry in entries:
        row = spark_entry_row(entry)
        if row is None:
            continue
        try:
            if insert_call(db, row, commit=False):
                new_count += 1
        except Exception as exc:
            print(f"[spark_sync] error inserting {row['call_id']}: {exc}", file=sys.stderr)
    db.commit()
    save_spark_checkpoint(cp)
    return new_count

# ── DB ───────────────────────────────────────────────────────────────
def persist_price_version(db: sqlite3.Connection) -> int:
    """Persist the exact bundled price table used by calculated ledger rows."""
    inserted = 0
    for model, price in PRICING.items():
        provider = detect_provider(model)
        cursor = db.execute(
            """
            INSERT OR IGNORE INTO price_versions
            (version, provider, model, input_per_m, output_per_m,
             cache_read_per_m, cache_write_per_m, fetched_at, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                PRICE_VERSION,
                provider,
                model,
                price["input"],
                price["output"],
                price["cacheRead"],
                price["cacheWrite"],
                PRICE_VERSION_FETCHED_AT,
                PRICING_SOURCE_URLS.get(provider),
            ),
        )
        inserted += max(cursor.rowcount, 0)
    return inserted


def get_db() -> sqlite3.Connection:
    LEDGER_DB.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(LEDGER_DB))
    db.execute("PRAGMA journal_mode=WAL")

    has_calls = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='calls'").fetchone()
    if has_calls:
        existing_cols = {r[1] for r in db.execute("PRAGMA table_info(calls)").fetchall()}
        for col in ["chat_id", "thread_id", "source_kind", "cron_job_id"]:
            if col not in existing_cols:
                default = "'interactive'" if col == "source_kind" else "NULL"
                db.execute(f"ALTER TABLE calls ADD COLUMN {col} TEXT DEFAULT {default}")
                print(f"[watcher] migrated: added calls.{col}")

    db.commit()
    schema = Path(__file__).parent / "ledger_schema.sql"
    if schema.exists():
        db.executescript(schema.read_text())
    persist_price_version(db)
    db.commit()
    return db

def insert_call(db: sqlite3.Connection, row: dict, commit: bool = True) -> bool:
    cursor = db.execute("""
        INSERT OR IGNORE INTO calls
        (call_id, session_key, turn_hint, ts, provider, model, model_raw,
         call_reason, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens,
         cost_input, cost_output, cost_cache_read, cost_cache_write, cost_total, cost_source,
         channel, chat_id, thread_id, message_id, source_kind, cron_job_id, price_version, usage_raw)
        VALUES
        (:call_id,:session_key,:turn_hint,:ts,:provider,:model,:model_raw,
         :call_reason,:input_tokens,:output_tokens,:cache_read_tokens,:cache_write_tokens,
         :cost_input,:cost_output,:cost_cache_read,:cost_cache_write,:cost_total,:cost_source,
         :channel,:chat_id,:thread_id,:message_id,:source_kind,:cron_job_id,:price_version,:usage_raw)
    """, row)
    if commit:
        db.commit()
    return cursor.rowcount > 0

# ── Checkpoint ───────────────────────────────────────────────────────
def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        try: return json.loads(CHECKPOINT.read_text())
        except: pass
    return {}

def save_checkpoint(cp: dict):
    CHECKPOINT.write_text(json.dumps(cp, indent=2))

# ── Core scan ────────────────────────────────────────────────────────
def scan_file(path: str, start_line: int, db: sqlite3.Connection, cp: dict) -> int:
    path_obj = Path(path)
    is_cron_runs = CRON_RUNS_DIR in path_obj.parents

    cron_job_id = None
    channel = "unknown"
    chat_id = None
    thread_id = None

    if is_cron_runs:
        basename = os.path.basename(path)
        name_part = basename.replace('.jsonl', '')
        cron_job_id = name_part.split('_')[0] if '_' in name_part else name_part
        session_key = f"agent:main:cron:{cron_job_id}"
        source_kind = "cron"
        channel = "cron"
    else:
        meta = resolve_session_meta(path)
        session_key = meta["session_key"]
        source_kind = meta["source_kind"]
        channel = meta.get("channel", "unknown")
        chat_id = meta.get("chat_id")
        thread_id = meta.get("thread_id")

    line_num = 0
    new_calls = 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line_num += 1
                if line_num <= start_line:
                    continue
                line = line.strip()
                if not line: continue
                try:
                    entry = json.loads(line)
                except: continue

                msg = entry.get("message")
                if not isinstance(msg, dict): continue
                if msg.get("role") != "assistant": continue
                usage = msg.get("usage")
                if not usage: continue
                if not any(usage.get(k, 0) for k in ["input","output","cacheRead","cacheWrite"]):
                    continue

                model_raw = msg.get("model") or ""
                model = normalize_model(model_raw)
                provider = detect_provider(model_raw)

                cost_breakdown, cost_source = calc_cost(model, provider, usage)

                call_id = entry.get("id") or hashlib.md5(f"{session_key}:{entry.get('timestamp','')}:{line_num}".encode()).hexdigest()[:16]

                call_row = {
                    "call_id": call_id, "session_key": session_key, "turn_hint": entry.get("parentId"),
                    "ts": entry.get("timestamp", ""), "provider": provider, "model": model, "model_raw": model_raw,
                    "call_reason": "primary",
                    "input_tokens": usage.get("input", 0) or 0,
                    "output_tokens": usage.get("output", 0) or 0,
                    "cache_read_tokens": usage.get("cacheRead", 0) or 0,
                    "cache_write_tokens": usage.get("cacheWrite", 0) or 0,
                    "cost_input": cost_breakdown["input"], "cost_output": cost_breakdown["output"],
                    "cost_cache_read": cost_breakdown["cacheRead"], "cost_cache_write": cost_breakdown["cacheWrite"],
                    "cost_total": cost_breakdown["total"], "cost_source": cost_source,
                    "channel": "cron" if is_cron_runs else channel,
                    "chat_id": chat_id if not is_cron_runs else None,
                    "thread_id": thread_id if not is_cron_runs else None,
                    "message_id": None,
                    "source_kind": source_kind,
                    "cron_job_id": cron_job_id if is_cron_runs else None,
                    "price_version": PRICE_VERSION,
                    "usage_raw": json.dumps(usage),
                }
                insert_call(db, call_row)
                new_calls += 1
    except Exception as e:
        print(f"[watcher] error scanning {path}: {e}", file=sys.stderr)

    return line_num

def scan_all(db: sqlite3.Connection, cp: dict) -> int:
    patterns = [
        str(SESSION_DIR / "*.jsonl"),           # Active sessions (incl. -topic- threads)
        str(SESSION_DIR / "*.jsonl.deleted*"),   # Deleted threads/sessions
        str(SESSION_DIR / "*.jsonl.reset*"),     # Reset sessions
        str(CRON_RUNS_DIR / "**/*.jsonl"),       # Cron runs
    ]
    total = 0
    for pattern in patterns:
        for path in glob.glob(pattern, recursive=True):
            try:
                stat = os.stat(path)
            except FileNotFoundError:
                # Session rotation can remove a file between glob() and stat().
                continue

            signature = (stat.st_mtime_ns, stat.st_size)
            if _file_signatures.get(path) == signature:
                continue

            # Absolute paths prevent basename collisions between active
            # sessions and cron runs.  Fall back to the legacy basename key so
            # existing checkpoints migrate without reprocessing old files.
            key = os.path.abspath(path)
            start = cp.get(key, cp.get(os.path.basename(path), 0))
            last_line = scan_file(path, start, db, cp)
            if last_line > start:
                cp[key] = last_line
                total += last_line - start
            _file_signatures[path] = signature
    return total

# ── Backfill ─────────────────────────────────────────────────────────
def backfill_source_kind(db: sqlite3.Connection) -> int:
    rows = db.execute("""
        SELECT call_id, session_key FROM calls
        WHERE (session_key LIKE '%:cron:%' OR session_key LIKE 'agent:main:cron:%')
        AND source_kind != 'cron'
    """).fetchall()

    updated = 0
    for call_id, session_key in rows:
        cron_job_id = None
        if ":cron:" in session_key:
            parts = session_key.split(":cron:")
            if len(parts) > 1:
                cron_job_id = parts[1].split(":")[0]
        db.execute("UPDATE calls SET source_kind = 'cron', cron_job_id = ? WHERE call_id = ?", (cron_job_id, call_id))
        updated += 1
    db.commit()
    return updated

# ── Main ─────────────────────────────────────────────────────────────
def main():
    one_shot = "--once" in sys.argv
    sync_spark = "--sync-spark" in sys.argv
    backfill = "--backfill" in sys.argv

    print(f"[ledger_watcher] starting, mode={'sync-spark' if sync_spark else 'backfill' if backfill else 'once' if one_shot else 'daemon'}")

    db = get_db()

    if backfill:
        n = backfill_source_kind(db)
        print(f"[ledger_watcher] backfill: {n} records updated")
        return

    if sync_spark:
        n = sync_spark_tokens(db)
        print(f"[ledger_watcher] Spark sync: {n} entries")
        return

    cp = load_checkpoint()

    if one_shot:
        n = scan_all(db, cp)
        save_checkpoint(cp)
        # Also sync Spark tokens in one-shot
        spark_n = sync_spark_tokens(db)
        print(f"[ledger_watcher] one-shot: {n} session lines, {spark_n} Spark entries")
        return

    # Daemon loop
    last_spark_sync = 0
    try:
        while True:
            n = scan_all(db, cp)
            if n > 0:
                save_checkpoint(cp)
                print(f"[ledger_watcher] +{n} lines at {datetime.now().isoformat()}")

            # Periodic Spark sync
            if time.time() - last_spark_sync > SPARK_SYNC_INTERVAL:
                spark_n = sync_spark_tokens(db)
                if spark_n > 0:
                    print(f"[ledger_watcher] Spark +{spark_n} entries")
                last_spark_sync = time.time()

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("[ledger_watcher] stopped")
        save_checkpoint(cp)

if __name__ == "__main__":
    main()
