#!/usr/bin/env python3
"""Live terminal dashboard for OpenClaw agent sessions (now with log subscription + Canvas export helpers)."""

from __future__ import annotations

import argparse
import atexit
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

DEFAULT_INTERVAL = 3.0
DEFAULT_ACTIVE_MINUTES = 720
DEFAULT_RETENTION = 120.0
ACTIVE_THRESHOLD = 75.0
IDLE_THRESHOLD = 240.0
SESSION_ID_RE = re.compile(r"sessionId=([0-9a-fA-F-]{36})")


RESET = "\033[0m"
COLORS = {
    "RUN": "\033[32m",
    "IDLE": "\033[33m",
    "STALE": "\033[35m",
    "EXITED": "\033[90m",
    "HEADER": "\033[36m",
}


def supports_color() -> bool:
    return sys.stdout.isatty() and os.getenv("NO_COLOR") is None


USE_COLOR = supports_color()


def colorize(text: str, color: str) -> str:
    if not USE_COLOR:
        return text
    return f"{color}{text}{RESET}"


@dataclass
class SessionState:
    first_seen: float
    last_present: float
    live: bool = True
    data: dict = field(default_factory=dict)


class SessionMonitor:
    def __init__(self, retention: float) -> None:
        self.retention = retention
        self.state: Dict[str, SessionState] = {}
        self.id_to_key: Dict[str, str] = {}
        self.lock = threading.Lock()

    def update_from_snapshot(self, sessions: List[dict], now: float) -> None:
        with self.lock:
            for entry in self.state.values():
                entry.live = False

            for session in sessions:
                key = session.get("key")
                if not key:
                    key = session.get("sessionId") or "unknown"
                session_id = session.get("sessionId")

                entry: Optional[SessionState] = None
                if session_id:
                    old_key = self.id_to_key.get(session_id)
                    if old_key and old_key != key:
                        entry = self.state.pop(old_key, None)
                    else:
                        entry = self.state.get(key)
                else:
                    entry = self.state.get(key)

                if not entry:
                    entry = SessionState(first_seen=now, last_present=now)

                entry.data = session
                entry.last_present = now
                entry.live = True
                self.state[key] = entry
                if session_id:
                    self.id_to_key[session_id] = key

    def touch_session(self, session_id: str) -> None:
        now = time.time()
        with self.lock:
            key = self.id_to_key.get(session_id)
            if not key:
                key = f"session:{session_id}"
            entry = self.state.get(key)
            if not entry:
                entry = SessionState(first_seen=now, last_present=now)
            entry.last_present = now
            entry.live = True
            data = entry.data or {}
            data.setdefault("key", key)
            data["sessionId"] = session_id
            data["updatedAt"] = int(now * 1000)
            entry.data = data
            self.state[key] = entry
            self.id_to_key[session_id] = key

    def prune(self, now: float) -> None:
        with self.lock:
            expired = [
                key
                for key, entry in self.state.items()
                if not entry.live and (now - entry.last_present) > self.retention
            ]
            for key in expired:
                self.state.pop(key, None)
                # also remove from id_to_key
                for sid, mapped_key in list(self.id_to_key.items()):
                    if mapped_key == key:
                        self.id_to_key.pop(sid, None)

    def snapshot_rows(self) -> List[tuple[str, SessionState]]:
        with self.lock:
            return list(self.state.items())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Live OpenClaw session monitor")
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                        help="Refresh interval in seconds (default: %(default)s)")
    parser.add_argument("--active-minutes", type=int, default=DEFAULT_ACTIVE_MINUTES,
                        help="Lookback window passed to `openclaw sessions --active`")
    parser.add_argument("--agent", type=str, default=None,
                        help="Limit to a specific agent id")
    parser.add_argument("--all-agents", action="store_true",
                        help="Aggregate sessions across all configured agents")
    parser.add_argument("--retention", type=float, default=DEFAULT_RETENTION,
                        help="Seconds to keep EXITED sessions visible (default: %(default)s)")
    parser.add_argument("--cost-per-1k", type=float, default=float(os.getenv("AGENT_MONITOR_COST_PER_1K", 0)),
                        help="USD cost per 1K tokens. Set to 0 to hide the cost column.")
    parser.add_argument("--once", action="store_true",
                        help="Render a single snapshot and exit")
    parser.add_argument("--no-subscribe", action="store_true",
                        help="Disable log subscription (poll-only mode)")
    return parser.parse_args()


def run_openclaw_sessions(args: argparse.Namespace) -> List[dict]:
    cmd = ["openclaw", "sessions", "--json", "--active", str(args.active_minutes)]
    if args.agent:
        cmd += ["--agent", args.agent]
    if args.all_agents:
        cmd.append("--all-agents")
    out = subprocess.check_output(cmd, text=True)
    payload = json.loads(out)
    return payload.get("sessions", [])


def extract_session_id(payload: dict) -> Optional[str]:
    text = payload.get("message") or ""
    match = SESSION_ID_RE.search(text)
    if match:
        return match.group(1)
    raw = payload.get("raw")
    if raw:
        match = SESSION_ID_RE.search(raw)
        if match:
            return match.group(1)
    return None


def tail_logs(monitor: SessionMonitor, stop_event: threading.Event) -> None:
    cmd = ["openclaw", "logs", "--json", "--follow", "--plain", "--interval", "1000"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)

    def _cleanup() -> None:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                proc.kill()

    atexit.register(_cleanup)

    try:
        while not stop_event.is_set():
            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    break
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            session_id = extract_session_id(payload)
            if session_id:
                monitor.touch_session(session_id)
    finally:
        _cleanup()


def human_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_tokens(total_tokens: Optional[int]) -> str:
    if total_tokens is None:
        return "-"
    if total_tokens >= 1000:
        return f"{total_tokens / 1000:.1f}k"
    return str(total_tokens)


def format_cost(total_tokens: Optional[int], cost_per_1k: float) -> str:
    if not total_tokens or cost_per_1k <= 0:
        return "-"
    usd = (total_tokens / 1000.0) * cost_per_1k
    return f"${usd:,.2f}"


def classify_status(entry: SessionState, now: float) -> str:
    if not entry.live:
        return "EXITED"
    data = entry.data or {}
    updated_ms = data.get("updatedAt")
    if not updated_ms:
        return "RUN"
    age_seconds = max(0.0, (now * 1000 - updated_ms) / 1000.0)
    if age_seconds <= ACTIVE_THRESHOLD:
        return "RUN"
    if age_seconds <= IDLE_THRESHOLD:
        return "IDLE"
    return "STALE"


def ellipsize(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."


def render_dashboard(monitor: SessionMonitor, args: argparse.Namespace) -> None:
    os.write(sys.stdout.fileno(), b"\033[2J\033[H")
    now = time.time()
    local_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    items = monitor.snapshot_rows()

    rows = []
    for key, entry in items:
        data = entry.data or {}
        status = classify_status(entry, now)
        updated_ms = data.get("updatedAt")
        lag_seconds = None
        updated_display = "-"
        if updated_ms:
            lag_seconds = max(0.0, (now * 1000 - updated_ms) / 1000.0)
            updated_display = f"{human_duration(lag_seconds)} ago"
        runtime_seconds = max(0.0, now - entry.first_seen)
        runtime = human_duration(runtime_seconds)
        start_time = datetime.fromtimestamp(entry.first_seen).strftime("%H:%M:%S")
        total_tokens = data.get("totalTokens")
        raw_tokens = total_tokens if isinstance(total_tokens, int) else 0
        rows.append({
            "key": data.get("key", key),
            "status": status,
            "runtime": runtime,
            "runtime_seconds": runtime_seconds,
            "start": start_time,
            "updated": updated_display,
            "lag_seconds": lag_seconds or 0.0,
            "tokens": format_tokens(total_tokens),
            "raw_tokens": raw_tokens,
            "cost": format_cost(total_tokens, args.cost_per_1k),
            "model": data.get("model", "-"),
            "kind": data.get("kind", "-"),
        })

    rows.sort(key=lambda r: (r["status"] != "RUN", r["start"]))
    state_counts = Counter(row["status"] for row in rows)
    run_count = state_counts.get("RUN", 0)
    idle_count = state_counts.get("IDLE", 0)
    stale_count = state_counts.get("STALE", 0)
    exited_count = state_counts.get("EXITED", 0)
    token_sum = sum(row["raw_tokens"] for row in rows)
    longest_run = max((row["runtime_seconds"] for row in rows), default=0.0)
    avg_lag = (sum(row["lag_seconds"] for row in rows) / len(rows)) if rows else 0.0
    cost_sum = (token_sum / 1000.0) * args.cost_per_1k if args.cost_per_1k > 0 else None

    title = colorize("Agents CLI Monitor", COLORS["HEADER"])
    header = f"{title}  |  Now: {local_now}  |  Sessions: {len(rows)}"
    print(header)

    summary_parts = [
        colorize(f"RUN {run_count}", COLORS["RUN"]),
        colorize(f"IDLE {idle_count}", COLORS["IDLE"]),
        colorize(f"STALE {stale_count}", COLORS["STALE"]),
        colorize(f"EXIT {exited_count}", COLORS["EXITED"]),
        f"Σ tokens: {format_tokens(token_sum)}",
    ]
    if cost_sum is not None:
        summary_parts.append(f"Σ cost: ${cost_sum:,.2f}")
    summary_parts.append(f"Longest run: {human_duration(longest_run)}")
    summary_parts.append(f"Avg lag: {human_duration(avg_lag)}")

    print(" | \n".join(summary_parts))
    print()

    term_width = shutil.get_terminal_size((120, 40)).columns
    col_widths = {
        "key": max(24, min(40, term_width // 5)),
        "status": 8,
        "runtime": 8,
        "start": 6,
        "updated": 14,
        "tokens": 8,
        "cost": 10 if args.cost_per_1k > 0 else 0,
        "model": 14,
    }
    headers = [
        ("Session", col_widths["key"]),
        ("State", col_widths["status"]),
        ("Run", col_widths["runtime"]),
        ("Start", col_widths["start"]),
        ("Last Update (ago)", col_widths["updated"]),
        ("Tokens", col_widths["tokens"]),
    ]
    if args.cost_per_1k > 0:
        headers.append(("Cost", col_widths["cost"]))
    headers.extend([
        ("Model", col_widths["model"]),
        ("Kind", 10),
    ])

    header_line = "  ".join(f"{name:<{width}}" for name, width in headers)
    print(header_line)
    print("-" * min(term_width, len(header_line)))

    if not rows:
        print("No sessions in the selected window.")
        return

    for row in rows:
        status_field = f"{row['status']:<{col_widths['status']}}"
        parts = [
            f"{ellipsize(row['key'], col_widths['key']):<{col_widths['key']}}",
            colorize(status_field, COLORS.get(row['status'], '')),
            f"{row['runtime']:<{col_widths['runtime']}}",
            f"{row['start']:<{col_widths['start']}}",
            f"{row['updated']:<{col_widths['updated']}}",
            f"{row['tokens']:<{col_widths['tokens']}}",
        ]
        if args.cost_per_1k > 0:
            parts.append(f"{row['cost']:<{col_widths['cost']}}")
        parts.extend([
            f"{ellipsize(row['model'], col_widths['model']):<{col_widths['model']}}",
            f"{ellipsize(row['kind'], 10):<10}",
        ])
        print("  ".join(parts))


def monitor_loop(args: argparse.Namespace) -> None:
    monitor = SessionMonitor(args.retention)
    stop_event = threading.Event()
    log_thread: Optional[threading.Thread] = None

    if not args.no_subscribe:
        log_thread = threading.Thread(target=tail_logs, args=(monitor, stop_event), daemon=True)
        log_thread.start()

    interval = max(0.5, args.interval)

    try:
        while True:
            try:
                sessions = run_openclaw_sessions(args)
            except subprocess.CalledProcessError as exc:
                sys.stderr.write(f"[agents-cli-monitor] Failed to fetch sessions: {exc}\n")
                time.sleep(interval)
                continue

            now = time.time()
            monitor.update_from_snapshot(sessions, now)
            monitor.prune(now)
            render_dashboard(monitor, args)

            if args.once:
                break

            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\nExiting monitor.")
                break
    finally:
        stop_event.set()
        if log_thread and log_thread.is_alive():
            log_thread.join(timeout=1.0)


def main() -> None:
    args = parse_args()
    try:
        monitor_loop(args)
    except KeyboardInterrupt:
        print("\nExiting monitor.")


if __name__ == "__main__":
    main()
