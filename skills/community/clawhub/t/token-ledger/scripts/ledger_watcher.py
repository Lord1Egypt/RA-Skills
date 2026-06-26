#!/usr/bin/env python3
"""
OpenClaw Token Ledger Watcher
Watches ~/.openclaw/agents/main/sessions/*.jsonl for new lines,
parses usage, writes into SQLite ledger.db.

Usage:
  python3 ledger_watcher.py           # runs forever (daemon mode)
  python3 ledger_watcher.py --once    # one-shot scan (for cron/backfill)
"""

import json, glob, os, sys, sqlite3, time, hashlib
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
SESSION_DIR   = Path.home() / ".openclaw/agents/main/sessions"
LEDGER_DB     = Path.home() / ".openclaw/ledger.db"
CHECKPOINT    = Path.home() / ".openclaw/ledger-checkpoint.json"
POLL_INTERVAL = 2      # seconds between scans (daemon mode)
PRICE_VERSION = "2026-03-07"

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
}

MODEL_ALIASES = {
    "claude-haiku-4-5-20251001": "claude-haiku-4-5",
    "claude-3-5-haiku-20241022": "claude-haiku-4-5",
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
    """Returns (cost_breakdown, cost_source)."""
    inp = u.get("input", 0) or 0
    out = u.get("output", 0) or 0
    cr  = u.get("cacheRead", 0) or 0
    cw  = u.get("cacheWrite", 0) or 0

    # Try provider-reported cost first
    prov_cost = u.get("cost") or {}
    prov_total = prov_cost.get("total", 0) or 0
    if prov_total > 0:
        return {
            "input":       prov_cost.get("input", 0) or 0,
            "output":      prov_cost.get("output", 0) or 0,
            "cacheRead":   prov_cost.get("cacheRead", 0) or 0,
            "cacheWrite":  prov_cost.get("cacheWrite", 0) or 0,
            "total":       prov_total,
        }, "provider"

    # Local models: cost = 0
    if provider in LOCAL_PROVIDERS:
        return {"input":0,"output":0,"cacheRead":0,"cacheWrite":0,"total":0}, "local"

    # Calculate from PRICING table
    p = PRICING.get(model)
    if p:
        cost_in  = inp / 1e6 * p["input"]
        cost_out = out / 1e6 * p["output"]
        cost_cr  = cr  / 1e6 * p["cacheRead"]
        cost_cw  = cw  / 1e6 * p["cacheWrite"]
        return {
            "input": cost_in, "output": cost_out,
            "cacheRead": cost_cr, "cacheWrite": cost_cw,
            "total": cost_in + cost_out + cost_cr + cost_cw,
        }, "calculated"

    return {"input":0,"output":0,"cacheRead":0,"cacheWrite":0,"total":0}, "unknown"

def session_key_from_path(path: str) -> str:
    """Derive a session key from the JSONL filename."""
    name = os.path.basename(path)
    # strip extensions
    name = name.split(".jsonl")[0]
    return f"agent:main:{name}"

# ── DB ───────────────────────────────────────────────────────────────
def get_db() -> sqlite3.Connection:
    db = sqlite3.connect(str(LEDGER_DB))
    db.execute("PRAGMA journal_mode=WAL")
    schema = Path(__file__).parent / "ledger_schema.sql"
    db.executescript(schema.read_text())
    db.commit()
    return db

def insert_call(db: sqlite3.Connection, row: dict):
    db.execute("""
        INSERT OR IGNORE INTO calls
        (call_id, session_key, turn_hint, ts, provider, model, model_raw,
         call_reason, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens,
         cost_input, cost_output, cost_cache_read, cost_cache_write, cost_total, cost_source,
         channel, message_id, price_version, usage_raw)
        VALUES
        (:call_id,:session_key,:turn_hint,:ts,:provider,:model,:model_raw,
         :call_reason,:input_tokens,:output_tokens,:cache_read_tokens,:cache_write_tokens,
         :cost_input,:cost_output,:cost_cache_read,:cost_cache_write,:cost_total,:cost_source,
         :channel,:message_id,:price_version,:usage_raw)
    """, row)
    db.commit()

def upsert_turn(db: sqlite3.Connection, call: dict):
    """Aggregate calls within 60s window into a turn."""
    key = call["session_key"]
    ts  = call["ts"]

    # find latest existing turn for this session within 60s
    row = db.execute("""
        SELECT turn_id FROM turns
        WHERE session_key=? AND ended_at >= datetime(?, '-60 seconds')
        ORDER BY ended_at DESC LIMIT 1
    """, (key, ts)).fetchone()

    if row:
        turn_id = row[0]
        db.execute("""
            UPDATE turns SET
              ended_at       = MAX(ended_at, ?),
              total_input    = total_input    + ?,
              total_output   = total_output   + ?,
              total_cache_read  = total_cache_read  + ?,
              total_cache_write = total_cache_write + ?,
              total_cost     = total_cost     + ?,
              call_count     = call_count     + 1,
              model          = ?,
              provider       = ?
            WHERE turn_id=?
        """, (ts,
              call["input_tokens"], call["output_tokens"],
              call["cache_read_tokens"], call["cache_write_tokens"],
              call["cost_total"], call["model"], call["provider"],
              turn_id))
    else:
        turn_id = call["call_id"]
        db.execute("""
            INSERT OR IGNORE INTO turns
            (turn_id, session_key, started_at, ended_at, channel, source_kind,
             total_input, total_output, total_cache_read, total_cache_write, total_cost,
             call_count, provider, model, price_version)
            VALUES (?,?,?,?,?,?, ?,?,?,?,?, ?,?,?,?)
        """, (
            turn_id, key, ts, ts,
            call.get("channel"), call.get("source_kind"),
            call["input_tokens"], call["output_tokens"],
            call["cache_read_tokens"], call["cache_write_tokens"],
            call["cost_total"], 1,
            call["provider"], call["model"], call["price_version"]
        ))
    db.commit()

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
    session_key = session_key_from_path(path)

    # Detect channel from session key
    channel = "unknown"
    source_kind = "interactive"
    if "discord:channel" in session_key: channel = "discord"
    elif "whatsapp" in session_key: channel = "whatsapp"
    elif "telegram" in session_key: channel = "telegram"
    if ":cron:" in session_key: source_kind = "cron"; channel = "cron"
    elif ":subagent:" in session_key: source_kind = "subagent"

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
                # skip zero-usage entries (delivery-mirror etc)
                if not any(usage.get(k, 0) for k in ["input","output","cacheRead","cacheWrite"]): continue

                model_raw = msg.get("model") or ""
                model     = normalize_model(model_raw)
                provider  = detect_provider(model_raw)

                inp = usage.get("input", 0) or 0
                out = usage.get("output", 0) or 0
                cr  = usage.get("cacheRead", 0) or 0
                cw  = usage.get("cacheWrite", 0) or 0

                cost_breakdown, cost_source = calc_cost(model, provider, usage)

                call_id = entry.get("id") or hashlib.md5(
                    f"{session_key}:{entry.get('timestamp','')}:{line_num}".encode()
                ).hexdigest()[:16]

                call_row = {
                    "call_id":           call_id,
                    "session_key":       session_key,
                    "turn_hint":         entry.get("parentId"),
                    "ts":                entry.get("timestamp", ""),
                    "provider":          provider,
                    "model":             model,
                    "model_raw":         model_raw,
                    "call_reason":       "primary",
                    "input_tokens":      inp,
                    "output_tokens":     out,
                    "cache_read_tokens": cr,
                    "cache_write_tokens":cw,
                    "cost_input":        cost_breakdown["input"],
                    "cost_output":       cost_breakdown["output"],
                    "cost_cache_read":   cost_breakdown["cacheRead"],
                    "cost_cache_write":  cost_breakdown["cacheWrite"],
                    "cost_total":        cost_breakdown["total"],
                    "cost_source":       cost_source,
                    "channel":           channel,
                    "message_id":        None,
                    "price_version":     PRICE_VERSION,
                    "usage_raw":         json.dumps(usage),
                    "source_kind":       source_kind,
                }
                insert_call(db, call_row)
                upsert_turn(db, call_row)
                new_calls += 1

    except Exception as e:
        print(f"[watcher] error scanning {path}: {e}", file=sys.stderr)

    return line_num  # return last processed line number

def scan_all(db: sqlite3.Connection, cp: dict) -> int:
    patterns = [
        str(SESSION_DIR / "*.jsonl"),
        str(SESSION_DIR / "*.jsonl.deleted*"),
        str(SESSION_DIR / "*.jsonl.reset*"),
    ]
    total = 0
    for pattern in patterns:
        for path in glob.glob(pattern):
            key = os.path.basename(path)
            start = cp.get(key, 0)
            last_line = scan_file(path, start, db, cp)
            if last_line > start:
                cp[key] = last_line
                total += last_line - start
    return total

# ── Main ─────────────────────────────────────────────────────────────
def main():
    one_shot = "--once" in sys.argv
    print(f"[ledger_watcher] starting, db={LEDGER_DB}, mode={'once' if one_shot else 'daemon'}")

    db = get_db()
    seed_price_versions(db)
    cp = load_checkpoint()

    if one_shot:
        n = scan_all(db, cp)
        save_checkpoint(cp)
        print(f"[ledger_watcher] one-shot: processed {n} new lines")
        return

    # Daemon loop
    try:
        while True:
            n = scan_all(db, cp)
            if n > 0:
                save_checkpoint(cp)
                print(f"[ledger_watcher] +{n} lines written to ledger at {datetime.now().isoformat()}")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("[ledger_watcher] stopped")
        save_checkpoint(cp)

def seed_price_versions(db: sqlite3.Connection):
    """Seed price_versions table from PRICING dict if empty."""
    count = db.execute("SELECT COUNT(*) FROM price_versions WHERE version=?", (PRICE_VERSION,)).fetchone()[0]
    if count > 0: return
    provider_map = {
        "claude": "anthropic", "gpt": "openai", "o1":"openai","o3":"openai","o4":"openai",
        "gemini": "google",
    }
    now = datetime.now(timezone.utc).isoformat()
    rows = []
    for model, p in PRICING.items():
        prov = "unknown"
        for prefix, name in provider_map.items():
            if model.startswith(prefix): prov = name; break
        rows.append((PRICE_VERSION, prov, model,
                     p["input"], p["output"], p["cacheRead"], p["cacheWrite"], now, None))
    db.executemany("""
        INSERT OR IGNORE INTO price_versions
        (version,provider,model,input_per_m,output_per_m,cache_read_per_m,cache_write_per_m,fetched_at,source_url)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, rows)
    db.commit()
    print(f"[ledger_watcher] seeded {len(rows)} price entries for version {PRICE_VERSION}")

if __name__ == "__main__":
    main()
