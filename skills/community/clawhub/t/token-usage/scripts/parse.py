#!/usr/bin/env python3
"""Parse OpenClaw session JSONL files and aggregate token usage."""

import json
import gzip
import os
import subprocess
import contextlib
import sqlite3
import tempfile
import shutil
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("Asia/Calcutta")
import argparse
import re
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import glob

DEFAULT_PRICING = {
    "kimi/k2.7": {"input": 0.90, "output": 3.75, "cache_read": 0.10, "cache_write": 1.00},
    "kimi/k2.7-code": {"input": 0.90, "output": 3.75, "cache_read": 0.10, "cache_write": 1.00},
    "kimi/k3": {"input": 2.78, "output": 13.89, "cache_read": 0.28, "cache_write": 2.78},
    "kimi/k3-1m": {"input": 2.78, "output": 13.89, "cache_read": 0.28, "cache_write": 2.78},
    "anthropic/claude-sonnet-4.5": {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75},
    "openai/gpt-4o": {"input": 2.50, "output": 10.00, "cache_read": 1.25, "cache_write": 0},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache_read": 0.075, "cache_write": 0},
    "openai/gpt-5.6-luna": {"input": 0.20, "output": 1.20, "cache_read": 0.02, "cache_write": 0},
    "openai/gpt-5.6-terra": {"input": 2.00, "output": 12.00, "cache_read": 0.20, "cache_write": 0},
    "openai/gpt-5.4": {"input": 2.50, "output": 15.00, "cache_read": 0.25, "cache_write": 0},
}

def load_pricing():
    pricing_file = Path(__file__).parent / "pricing.json"
    if pricing_file.exists():
        with open(pricing_file) as f:
            return {**DEFAULT_PRICING, **json.load(f)}
    return DEFAULT_PRICING

def find_sessions(base_paths=None):
    if base_paths is None:
        base_paths = [
            Path.home() / ".openclaw" / "agents" / "main" / "sessions",
            Path.home() / ".openclaw" / "agents" / "sub" / "sessions",
            # Codex app-server rollout logs use a nested YYYY/MM/DD layout.
            Path.home() / ".openclaw" / "agents" / "main" / "agent" / "codex-home" / "sessions",
        ]
    sessions = []
    for bp in base_paths:
        if bp.exists():
            sessions.extend(glob.glob(str(bp / "**" / "*.jsonl"), recursive=True))
            sessions.extend(glob.glob(str(bp / "**" / "*.jsonl.gz"), recursive=True))
            # Ended sessions are rotated to zstd-compressed archives that the
            # live parser cannot see; include them so a full-day report is not
            # silently zero just because no session stayed open overnight.
            sessions.extend(glob.glob(str(bp / "**" / "*.jsonl.deleted.*.zst"), recursive=True))
    return sorted(set(sessions))

# ---------------------------------------------------------------------------
# SQLite transcript backend (OpenClaw 2026.9.x)
# ---------------------------------------------------------------------------
# Since the 9.x storage migration, live session transcripts live in
# `${OPENCLAW_HOME}/.openclaw/agents/<agent>/agent/openclaw-agent.sqlite` (table
# `transcript_events.event_json`), not as loose `.jsonl` files. Ended-session
# JSONL is additionally rotated to zstd archives or SQLite `archive_blob`s.
# The live DB is protected state: `exec` refuses to open it in place, so we
# snapshot it to a temp copy and read that.
_SQLITE_DB_CANDIDATES = [
    "agents/main/agent/openclaw-agent.sqlite",
    "agents/sub/agent/openclaw-agent.sqlite",
]

def _sqlite_transcript_sources(state_dir=None):
    """Yield path for each agent SQLite transcript DB."""
    root = Path(state_dir) if state_dir else Path.home() / ".openclaw"
    for rel in _SQLITE_DB_CANDIDATES:
        p = root / rel
        if p.exists():
            yield p

def _snapshot_sqlite(db_path):
    """Snapshot the live DB to a temp file so we can read it without holding the
    production lock or tripping the protected-state guard.

    Uses the SQLite online-backup API rather than a raw file copy: the live DB
    is under constant write (WAL), and a plain shutil.copyfile can catch a torn
    checkpoint, yielding a copy sqlite3 then refuses to open ("unable to open
    database file"). sqlite3.Connection.backup copies a consistent snapshot even
    while the source is being written.

    Snapshots to /tmp, NOT tempfile.gettempdir(): OpenClaw sets TMPDIR to
    ${OPENCLAW_HOME}/.openclaw/tmp, which is inside the protected state dir and sqlite3 refuses
    to open databases there. /tmp is genuinely outside the guard.

    Returns the temp path, or None on failure. Caller must unlink it."""
    fd, tmp = tempfile.mkstemp(suffix=".sqlite", prefix="oc-tok-", dir="/tmp")
    os.close(fd)
    try:
        src = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            dst = sqlite3.connect(tmp)
            try:
                src.backup(dst)
            finally:
                dst.close()
        finally:
            src.close()
        return tmp
    except (sqlite3.Error, OSError):
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return None

def parse_sqlite_transcripts(db_path, since=None, until=None):
    """Yield (timestamp, model, usage_dict) from transcript_events.event_json."""
    snap = _snapshot_sqlite(db_path)
    if not snap:
        return
    try:
        con = sqlite3.connect(snap)
        cur = con.cursor()
        try:
            rows = cur.execute(
                "SELECT event_json FROM transcript_events"
                " WHERE event_json LIKE '%\"usage\"%'"
            )
            for (event_json,) in rows:
                try:
                    d = json.loads(event_json)
                except (json.JSONDecodeError, TypeError):
                    continue
                m = d.get("message") or {}
                if m.get("role") != "assistant":
                    continue
                usage = m.get("usage")
                if not usage:
                    continue
                ts = d.get("timestamp") or d.get("ts") or ""
                model = m.get("model") or d.get("model") or d.get("api") or ""
                yield ts, model, usage
        finally:
            con.close()
    except sqlite3.Error:
        pass
    finally:
        try:
            os.unlink(snap)
        except OSError:
            pass

def aggregate_sqlite(since=None, until=None):
    """Aggregate token usage straight from the SQLite transcript backend."""
    by_day = defaultdict(lambda: defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0
    }))
    total = 0
    for db in _sqlite_transcript_sources():
        for ts, model, usage in parse_sqlite_transcripts(db, since, until):
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            day = ts[:10] if ts else "unknown"
            key = model or "unknown"
            d = by_day[day][key]
            d["input"] += usage.get("input", 0)
            d["output"] += usage.get("output", 0)
            d["cacheRead"] += usage.get("cacheRead", 0)
            d["cacheWrite"] += usage.get("cacheWrite", 0)
            d["messages"] += 1
            total += 1
    return by_day, total


def _friendly_session_name(session_key):
    """Derive a human-readable process name from a session_key.

    'agent:main:telegram:direct:849773381' -> 'telegram:direct:849773381'
    'agent:main:cron:daily-job-hunt'       -> 'cron:daily-job-hunt'
    'agent:sub:spawn:research-xyz'         -> 'subagent:research-xyz'
    """
    if not session_key:
        return "unknown"
    parts = session_key.split(":")
    # Strip leading 'agent'/<scope> prefix; keep the meaningful tail.
    if parts and parts[0] == "agent":
        parts = parts[1:]
    if parts and parts[0] in ("main", "sub"):
        scope = parts.pop(0)
        if scope == "sub" and parts and parts[0] != "cron":
            parts.insert(0, "subagent")
    return ":".join(parts) if parts else session_key


def _session_process_names():
    """Yield (session_id, process_name) from session_nodes, one per session.

    Prefers the user-set display_name/label; falls back to a derived
    session_key name. Reads through a snapshot of the same SQLite DBs
    used for transcripts.
    """
    seen = set()
    for db in _sqlite_transcript_sources():
        snap = _snapshot_sqlite(db)
        if not snap:
            continue
        try:
            con = sqlite3.connect(snap)
            cur = con.cursor()
            try:
                rows = cur.execute(
                    "SELECT current_session_id, session_key, display_name, label"
                    " FROM session_nodes"
                ).fetchall()
            finally:
                con.close()
            for sid, skey, dname, label in rows:
                if not sid or sid in seen:
                    continue
                seen.add(sid)
                name = (dname or "").strip() or (label or "").strip() \
                    or _friendly_session_name(skey)
                yield sid, name
        except sqlite3.Error:
            pass
        finally:
            try:
                os.unlink(snap)
            except OSError:
                pass


def aggregate_sqlite_by_process(since=None, until=None):
    """Aggregate token usage by friendly process name + model.

    Returns {process: {model: {input,output,cacheRead,cacheWrite,messages}}}
    plus a total message count.
    """
    names = dict(_session_process_names())
    by_process = defaultdict(lambda: defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0
    }))
    total = 0
    for db in _sqlite_transcript_sources():
        # parse_sqlite_transcripts only yields (ts, model, usage) — but the
        # session id is recoverable from event_json, so re-read it here via a
        # per-db scan that keeps session_id alongside usage.
        snap = _snapshot_sqlite(db)
        if not snap:
            continue
        try:
            con = sqlite3.connect(snap)
            cur = con.cursor()
            try:
                rows = cur.execute(
                    "SELECT session_id, event_json FROM transcript_events"
                    " WHERE event_json LIKE '%\"usage\"%'"
                ).fetchall()
            finally:
                con.close()
        except sqlite3.Error:
            try:
                os.unlink(snap)
            except OSError:
                pass
            continue
        finally:
            try:
                os.unlink(snap)
            except OSError:
                pass

        for sid, event_json in rows:
            try:
                d = json.loads(event_json)
            except (json.JSONDecodeError, TypeError):
                continue
            m = d.get("message") or {}
            if m.get("role") != "assistant":
                continue
            usage = m.get("usage")
            if not usage:
                continue
            ts = d.get("timestamp") or d.get("ts") or ""
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            model = m.get("model") or d.get("model") or d.get("api") or "unknown"
            process = names.get(sid) or _friendly_session_name(d.get("sessionKey")) or sid[:8]
            p = by_process[process][model]
            p["input"] += usage.get("input", 0)
            p["output"] += usage.get("output", 0)
            p["cacheRead"] += usage.get("cacheRead", 0)
            p["cacheWrite"] += usage.get("cacheWrite", 0)
            p["messages"] += 1
            total += 1
    return by_process, total

def parse_session_file(path):
    """Yield (timestamp, model, usage_dict) for each assistant message."""
    path = str(path)
    if ".deleted." in path or path.endswith(".zst"):
        ctx = contextlib.closing(_zstd_stream(path))
    elif path.endswith(".gz"):
        ctx = gzip.open(path, "rt", encoding="utf-8", errors="replace")
    else:
        ctx = open(path, "rt", encoding="utf-8", errors="replace")
    try:
        with ctx as f:
            codex_model = ""
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Codex rollout logs emit cumulative token_count events.  The
                # last_token_usage object is per-turn, so it is safe to sum.
                if msg.get("type") == "event_msg":
                    payload = msg.get("payload", {})
                    if payload.get("type") == "token_count":
                        info = payload.get("info") or {}
                        usage = info.get("last_token_usage") or {}
                        if usage:
                            # Codex input_tokens is total prompt input, including
                            # the cached subset. Keep billed uncached input and
                            # cache reads disjoint in the normalized report.
                            cached = usage.get("cached_input_tokens", 0) or 0
                            prompt = usage.get("input_tokens", 0) or 0
                            yield (
                                msg.get("timestamp", ""),
                                codex_model or "openai/gpt-5.6-luna",
                                {
                                    "input": max(prompt - cached, 0),
                                    "output": usage.get("output_tokens", 0),
                                    "cacheRead": usage.get("cached_input_tokens", 0),
                                    "cacheWrite": usage.get("cache_write_input_tokens", 0),
                                },
                            )
                    continue
                if msg.get("type") == "turn_context":
                    codex_model = msg.get("payload", {}).get("model", "") or codex_model
                    continue
                if msg.get("type") != "message":
                    continue
                m = msg.get("message", {})
                if m.get("role") != "assistant":
                    continue
                usage = m.get("usage") or msg.get("usage")
                if not usage:
                    continue
                ts = msg.get("timestamp", "")
                model = m.get("model", msg.get("model", msg.get("api", "")))
                yield ts, model, usage
    except (FileNotFoundError, OSError):
        pass

def _zstd_stream(path):
    """Yield decompressed text lines from a zstd-compressed session archive."""
    proc = subprocess.Popen(
        ["zstd", "-d", "-c", "--", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        for line in proc.stdout:
            yield line
    finally:
        proc.stdout.close()
        proc.wait()


def aggregate(sessions, since=None, until=None):
    by_day = defaultdict(lambda: defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0
    }))
    by_session = defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "models": set()
    })
    
    for spath in sessions:
        sid = Path(spath).stem
        for ts, model, usage in parse_session_file(spath):
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            day = ts[:10] if ts else "unknown"
            model_key = model or "unknown"
            
            inp = usage.get("input", 0)
            out = usage.get("output", 0)
            
            d = by_day[day][model_key]
            d["input"] += inp
            d["output"] += out
            d["cacheRead"] += usage.get("cacheRead", 0)
            d["cacheWrite"] += usage.get("cacheWrite", 0)
            d["messages"] += 1
            
            s = by_session[sid]
            s["input"] += inp
            s["output"] += out
            s["cacheRead"] += usage.get("cacheRead", 0)
            s["cacheWrite"] += usage.get("cacheWrite", 0)
            s["messages"] += 1
            s["models"].add(model_key)
    
    return by_day, by_session

def detect_cron_job(path):
    """Extract cron job ID and name from first user message in session."""
    open_fn = gzip.open if path.endswith(".gz") else open
    try:
        with open_fn(path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if msg.get("type") != "message":
                    continue
                m = msg.get("message", {})
                if m.get("role") != "user":
                    continue
                content = m.get("content", [])
                text = ""
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        text += c.get("text", "")
                match = re.search(r'\[cron:([a-f0-9\-]+)\s+([^\]]+)\]', text)
                if match:
                    return match.group(1), match.group(2).strip()
                match2 = re.search(r'\[cron:([a-z0-9\-]+)\s+([^\]]+)\]', text)
                if match2:
                    return match2.group(1), match2.group(2).strip()
                break
    except Exception:
        pass
    return None, None

def aggregate_by_cron(sessions, since=None, until=None):
    """Aggregate token usage by cron job and date."""
    by_day_job = defaultdict(lambda: {
        "input": 0, "output": 0, "messages": 0, "name": ""
    })
    
    for spath in sessions:
        job_id, job_name = detect_cron_job(spath)
        if not job_id:
            continue
        for ts, model, usage in parse_session_file(spath):
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            day = ts[:10] if ts else "unknown"
            key = f"{day}:{job_id}"
            
            inp = usage.get("input", 0)
            out = usage.get("output", 0)
            
            by_day_job[key]["input"] += inp
            by_day_job[key]["output"] += out
            by_day_job[key]["messages"] += 1
            if job_name and not by_day_job[key]["name"]:
                by_day_job[key]["name"] = job_name
    
    return by_day_job

def estimate_cost(usage, model, pricing):
    """Estimate cost in USD. Prices are per 1M tokens."""
    p = pricing.get(model)
    if p is None and "/" not in model:
        # Try common provider prefixes
        for prefix in ["kimi/", "openai/", "anthropic/", "google/", "deepseek/", "qwen/", "x-ai/"]:
            p = pricing.get(prefix + model)
            if p is not None:
                break
    if p is None:
        # Never silently price an unknown provider as Kimi.
        p = {}
    cost = 0.0
    cost += usage.get("input", 0) * (p.get("input") or 0) / 1e6
    cost += usage.get("output", 0) * (p.get("output") or 0) / 1e6
    cost += usage.get("cacheRead", 0) * (p.get("cache_read") or 0) / 1e6
    cost += usage.get("cacheWrite", 0) * (p.get("cache_write") or 0) / 1e6
    return cost

def format_report(by_day, by_session, pricing=None, costs=False):
    lines = []
    total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}
    
    for day in sorted(by_day.keys(), reverse=True):
        lines.append(f"\n## {day}")
        day_total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}
        for model in sorted(by_day[day].keys()):
            u = by_day[day][model]
            usage_for_cost = {"input": u["input"], "output": u["output"], "cacheRead": u["cacheRead"], "cacheWrite": u["cacheWrite"]}
            c = estimate_cost(usage_for_cost, model, pricing) if (costs and pricing) else 0.0
            lines.append(f"  {model:30s}  in={u['input']:>10,}  out={u['output']:>8,}  cache={u['cacheRead']:>8,}  msgs={u['messages']:>4}")
            if costs and pricing:
                lines.append(f"{'':34s}est. ${c:.4f}")
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                day_total[k] += u[k]
            day_total["cost"] += c
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                total[k] += u[k]
            total["cost"] += c
        lines.append(f"  {'Day total':30s}  in={day_total['input']:>10,}  out={day_total['output']:>8,}  cache={day_total['cacheRead']:>8,}  msgs={day_total['messages']:>4}")
        if costs and pricing:
            lines.append(f"  {'':34s}est. ${day_total['cost']:.4f}")
    
    lines.append(f"\n## Grand Total")
    lines.append(f"  input={total['input']:,}  output={total['output']:,}  cacheRead={total['cacheRead']:,}  messages={total['messages']:,}")
    if costs and pricing:
        lines.append(f"  est. cost=${total['cost']:.4f}")
    
    return "\n".join(lines)

def format_process_report(by_process, pricing=None, costs=False):
    lines = []
    total = {"input": 0, "output": 0, "messages": 0, "cost": 0.0}

    # Flatten process+model rows, sort by combined tokens desc.
    rows = []
    for process, models in by_process.items():
        for model, u in models.items():
            rows.append((process, model, u))
    rows.sort(key=lambda r: r[2]["input"] + r[2]["output"], reverse=True)

    lines.append(f"\n{'Process':<44} {'Model':<20} {'Msgs':>5} {'In':>11} {'Out':>9}" + ("  Cost" if costs else ""))
    lines.append("-" * (96 + (8 if costs else 0)))

    cur_process = None
    for process, model, u in rows:
        if process != cur_process:
            cur_process = process
            lines.append(f"{process}")
        usage_for_cost = {"input": u["input"], "output": u["output"], "cacheRead": u.get("cacheRead", 0), "cacheWrite": u.get("cacheWrite", 0)}
        c = estimate_cost(usage_for_cost, model, pricing) if (costs and pricing) else 0.0
        cost_str = f"  ${c:.4f}" if costs else ""
        lines.append(f"  {model:<42} {u['messages']:>5} {u['input']:>11,} {u['output']:>9,}{cost_str}")
        for k in ["input", "output", "messages"]:
            total[k] += u[k]
        total["cost"] += c

    lines.append("-" * (96 + (8 if costs else 0)))
    cost_str = f"  ${total['cost']:.4f}" if costs else ""
    lines.append(f"{'TOTAL':<44} {'':<20} {total['messages']:>5} {total['input']:>11,} {total['output']:>9,}{cost_str}")
    return "\n".join(lines)


def format_cron_report(by_day_job, pricing=None, costs=False):
    lines = []
    total = {"input": 0, "output": 0, "messages": 0, "cost": 0.0}
    
    days = defaultdict(dict)
    for key, data in by_day_job.items():
        day, job_id = key.split(":", 1)
        days[day][job_id] = data
    
    for day in sorted(days.keys(), reverse=True):
        lines.append(f"\n## {day}")
        day_total = {"input": 0, "output": 0, "messages": 0, "cost": 0.0}
        
        jobs = sorted(days[day].items(), 
                     key=lambda x: x[1]["input"] + x[1]["output"], 
                     reverse=True)
        
        for job_id, data in jobs:
            name = data.get("name", job_id[:8])
            if len(name) > 28:
                name = name[:25] + "..."
            
            usage_for_cost = {"input": data["input"], "output": data["output"], "cacheRead": 0, "cacheWrite": 0}
            c = estimate_cost(usage_for_cost, "kimi/k2.7", pricing) if (costs and pricing) else 0.0
            
            lines.append(f"  {name:<28}  calls={data['messages']:>4}  in={data['input']:>10,}  out={data['output']:>8,}")
            if costs and pricing:
                lines.append(f"{'':34s}est. ${c:.4f}")
            
            for k in ["input", "output", "messages"]:
                day_total[k] += data[k]
            day_total["cost"] += c
            for k in ["input", "output", "messages"]:
                total[k] += data[k]
            total["cost"] += c
        
        lines.append(f"  {'DAY TOTAL':<28}  calls={day_total['messages']:>4}  in={day_total['input']:>10,}  out={day_total['output']:>8,}")
        if costs and pricing:
            lines.append(f"  {'':34s}est. ${day_total['cost']:.4f}")
    
    lines.append(f"\n## Grand Total")
    lines.append(f"  input={total['input']:,}  output={total['output']:,}  messages={total['messages']:,}")
    if costs and pricing:
        lines.append(f"  est. cost=${total['cost']:.4f}")
    
    return "\n".join(lines)

def to_json(by_day, by_session, pricing=None):
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": {},
        "sessions": {}
    }
    for day, models in by_day.items():
        out["days"][day] = {}
        for model, u in models.items():
            d = dict(u)
            if pricing:
                usage_for_cost = {"input": u["input"], "output": u["output"], "cacheRead": u["cacheRead"], "cacheWrite": u["cacheWrite"]}
                d["estimated_cost_usd"] = round(estimate_cost(usage_for_cost, model, pricing), 6)
            out["days"][day][model] = d
    for sid, s in by_session.items():
        out["sessions"][sid] = {
            **{k: s[k] for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]},
            "models": list(s["models"])
        }
    return out

def to_cron_json(by_day_job, pricing=None):
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": {}
    }
    for key, data in by_day_job.items():
        day, job_id = key.split(":", 1)
        if day not in out["days"]:
            out["days"][day] = {}
        d = {
            "name": data.get("name", ""),
            "input": data["input"],
            "output": data["output"],
            "messages": data["messages"]
        }
        if pricing:
            usage_for_cost = {"input": data["input"], "output": data["output"], "cacheRead": 0, "cacheWrite": 0}
            d["estimated_cost_usd"] = round(estimate_cost(usage_for_cost, "kimi/k2.7", pricing), 6)
        out["days"][day][job_id] = d
    return out

def main():
    parser = argparse.ArgumentParser(description="Track OpenClaw token usage")
    parser.add_argument("--yesterday", action="store_true", help="Report for yesterday only")
    parser.add_argument("--today", action="store_true", help="Report for today only")
    parser.add_argument("--week", action="store_true", help="Report for last 7 days")
    parser.add_argument("--all", action="store_true", help="Report all time")
    parser.add_argument("--by-model", action="store_true", help="Group by model")
    parser.add_argument("--by-cron", action="store_true", help="Group by cron job")
    parser.add_argument("--by-process", action="store_true", help="Group by process type and name (session_nodes)")
    parser.add_argument("--last-hour", action="store_true", help="Report for the last 60 minutes")
    parser.add_argument("--since", help="ISO start time (e.g. 2026-09-22T13:00:00)")
    parser.add_argument("--until", help="ISO end time")
    parser.add_argument("--costs", action="store_true", help="Estimate costs")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--sessions", nargs="*", help="Specific session files")
    args = parser.parse_args()
    
    now = datetime.now(LOCAL_TZ)
    since = args.since or None
    until = args.until or None

    if args.last_hour:
        # Events store UTC 'Z' timestamps — cutoff must be UTC too.
        since = (now - timedelta(hours=1)).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    elif args.today:
        since = now.strftime("%Y-%m-%dT00:00:00")
    elif args.yesterday:
        yesterday = now - timedelta(days=1)
        since = yesterday.strftime("%Y-%m-%dT00:00:00")
        until = now.strftime("%Y-%m-%dT00:00:00")
    elif args.week:
        since = (now - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00")
    elif not args.all and not since:
        args.today = True
        since = now.strftime("%Y-%m-%dT00:00:00")
    
    pricing = load_pricing() if args.costs else None
    
    if args.by_process:
        by_process, total = aggregate_sqlite_by_process(since=since, until=until)
        if args.json:
            out = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "window": {"since": since, "until": until},
                "processes": {
                    proc: {
                        "models": {m: dict(u) for m, u in models.items()},
                        "input": sum(u["input"] for u in models.values()),
                        "output": sum(u["output"] for u in models.values()),
                        "messages": sum(u["messages"] for u in models.values()),
                    }
                    for proc, models in by_process.items()
                },
                "total_messages": total,
            }
            if pricing:
                for proc, pdata in out["processes"].items():
                    c = 0.0
                    for m, u in pdata["models"].items():
                        uc = estimate_cost({"input": u["input"], "output": u["output"], "cacheRead": 0, "cacheWrite": 0}, m, pricing)
                        u["estimated_cost_usd"] = round(uc, 6)
                        c += uc
                    pdata["estimated_cost_usd"] = round(c, 6)
            print(json.dumps(out, indent=2))
        else:
            print(format_process_report(by_process, pricing, args.costs))
        return
    
    sessions = args.sessions or find_sessions()
    if not sessions:
        print("No session files found.")
        return
    
    if args.by_cron:
        by_day_job = aggregate_by_cron(sessions, since=since, until=until)
        # Fold in the SQLite transcript backend (9.x storage migration) so cron
        # reports are not silently zero when every session file has rotated.
        sq_by_day, _ = aggregate_sqlite(since=since, until=until)
        for day, models in sq_by_day.items():
            for model, u in models.items():
                # by_day_job is keyed 'day:job_id'; SQLite lacks cron tags, so
                # attribute it to a synthetic 'sqlite-backend' bucket per day.
                key = f"{day}:sqlite-backend"
                tgt = by_day_job[key]
                tgt["input"] += u["input"]
                tgt["output"] += u["output"]
                tgt["messages"] += u["messages"]
                if not tgt["name"]:
                    tgt["name"] = "(sqlite backend)"
        if args.json:
            print(json.dumps(to_cron_json(by_day_job, pricing), indent=2))
        else:
            print(format_cron_report(by_day_job, pricing, args.costs))
    else:
        by_day, by_session = aggregate(sessions, since=since, until=until)
        # Merge the SQLite transcript backend (9.x storage migration): ended
        # sessions live in openclaw-agent.sqlite, not as loose .jsonl files, so
        # without this a full-day report is silently zero once sessions close.
        sq_by_day, _ = aggregate_sqlite(since=since, until=until)
        for day, models in sq_by_day.items():
            for model, u in models.items():
                d = by_day[day][model or "unknown"]
                d["input"] += u["input"]
                d["output"] += u["output"]
                d["cacheRead"] += u["cacheRead"]
                d["cacheWrite"] += u["cacheWrite"]
                d["messages"] += u["messages"]
        if args.json:
            print(json.dumps(to_json(by_day, by_session, pricing), indent=2))
        else:
            print(format_report(by_day, by_session, pricing, args.costs))

if __name__ == "__main__":
    main()
