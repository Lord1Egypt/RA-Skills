#!/usr/bin/env python3
"""Generate a color-coded HTML snapshot of OpenClaw sessions for Canvas/browser display."""

from __future__ import annotations

import argparse
import html
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

DEFAULT_OUTPUT = "assets/agents_canvas.html"
DEFAULT_ACTIVE_MINUTES = 720
DEFAULT_REFRESH = 5
ACTIVE_THRESHOLD_MS = 75_000
IDLE_THRESHOLD_MS = 240_000

STATUS_CLASSES = {
    "RUN": "status-run",
    "IDLE": "status-idle",
    "STALE": "status-stale",
    "EXITED": "status-exited",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an HTML dashboard of OpenClaw sessions")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Output HTML path (default: %(default)s relative to this skill)")
    parser.add_argument("--active-minutes", type=int, default=DEFAULT_ACTIVE_MINUTES,
                        help="Lookback window for `openclaw sessions --active`")
    parser.add_argument("--agent", type=str, default=None,
                        help="Limit to a specific agent id")
    parser.add_argument("--all-agents", action="store_true",
                        help="Aggregate sessions across all agents")
    parser.add_argument("--refresh", type=int, default=DEFAULT_REFRESH,
                        help="Meta refresh interval in seconds (0 disables auto-refresh)")
    parser.add_argument("--cost-per-1k", type=float, default=float(os.getenv("AGENT_MONITOR_COST_PER_1K", 0)),
                        help="USD cost per 1K tokens for the cost column (default: env or 0)")
    parser.add_argument("--loop", type=int, default=0,
                        help="Keep regenerating forever, every N seconds (0 runs once and exits)")
    return parser.parse_args()


def fetch_sessions(args: argparse.Namespace) -> List[dict]:
    cmd = ["openclaw", "sessions", "--json", "--active", str(args.active_minutes)]
    if args.agent:
        cmd += ["--agent", args.agent]
    if args.all_agents:
        cmd.append("--all-agents")
    out = subprocess.check_output(cmd, text=True)
    payload = json.loads(out)
    return payload.get("sessions", [])


def human_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def classify_status(age_ms: Optional[int]) -> str:
    if age_ms is None:
        return "RUN"
    if age_ms <= ACTIVE_THRESHOLD_MS:
        return "RUN"
    if age_ms <= IDLE_THRESHOLD_MS:
        return "IDLE"
    return "STALE"


def format_tokens(total_tokens: Optional[int]) -> str:
    if total_tokens is None:
        return "-"
    if total_tokens >= 1000:
        return f"{total_tokens / 1000:.1f}k"
    return str(total_tokens)


def format_cost(total_tokens: Optional[int], rate: float) -> str:
    if not total_tokens or rate <= 0:
        return "-"
    usd = (total_tokens / 1000.0) * rate
    return f"${usd:,.2f}"


def render_html(sessions: List[dict], args: argparse.Namespace) -> str:
    now_dt = datetime.now()
    now_epoch = now_dt.timestamp()
    refresh_tag = ""
    if args.refresh > 0:
        refresh_tag = f'<meta http-equiv="refresh" content="{args.refresh}">'

    status_counts = {key: 0 for key in STATUS_CLASSES}
    tokens_total = 0
    lag_total = 0.0
    lag_count = 0
    longest_runtime = 0.0

    rows_html = []
    for session in sessions:
        key = html.escape(session.get("key", session.get("sessionId", "unknown")))
        age_ms = session.get("ageMs")
        status = session.get("status") or classify_status(age_ms)
        status_counts.setdefault(status, 0)
        status_counts[status] += 1

        updated_ms = session.get("updatedAt")
        lag_seconds = None
        last_update_local = "-"
        last_update_ago = "-"
        if updated_ms:
            lag_seconds = max(0.0, now_epoch - (updated_ms / 1000.0))
            last_update_local = datetime.fromtimestamp(updated_ms / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
            last_update_ago = f"{human_duration(lag_seconds)} ago"
            lag_total += lag_seconds
            lag_count += 1

        created_ms = session.get("createdAt")
        runtime_display = "-"
        if created_ms:
            runtime_seconds = max(0.0, now_epoch - (created_ms / 1000.0))
            runtime_display = human_duration(runtime_seconds)
            longest_runtime = max(longest_runtime, runtime_seconds)

        tokens = session.get("totalTokens")
        tokens_total += tokens or 0
        tokens_display = format_tokens(tokens)
        cost_display = format_cost(tokens, args.cost_per_1k)
        model = html.escape(session.get("model", "-"))
        kind = html.escape(session.get("kind", "-"))

        status_badge = f"<span class='status {STATUS_CLASSES.get(status, 'status-run')}'>{status}</span>"
        cost_cell = f"<td>{html.escape(cost_display)}</td>" if args.cost_per_1k > 0 else ""

        rows_html.append(
            "<tr>"
            f"<td>{key}</td>"
            f"<td>{status_badge}</td>"
            f"<td>{runtime_display}</td>"
            f"<td>{last_update_ago}</td>"
            f"<td>{last_update_local}</td>"
            f"<td>{tokens_display}</td>"
            f"{cost_cell}"
            f"<td>{model}</td>"
            f"<td>{kind}</td>"
            "</tr>"
        )

    cost_total = (tokens_total / 1000.0) * args.cost_per_1k if args.cost_per_1k > 0 else None
    avg_lag = human_duration(lag_total / lag_count) if lag_count else "-"
    longest_run_display = human_duration(longest_runtime) if longest_runtime else "-"
    cost_header = "<th>Cost</th>" if args.cost_per_1k > 0 else ""
    summary_cost = f"${cost_total:,.2f}" if cost_total is not None else "-"
    colspan = 9 if args.cost_per_1k > 0 else 8

    cards_html = f"""
    <div class=\"cards\">
      <div class=\"card accent-run\"><p class=\"label\">RUN</p><p class=\"value\">{status_counts.get('RUN', 0)}</p></div>
      <div class=\"card accent-idle\"><p class=\"label\">IDLE</p><p class=\"value\">{status_counts.get('IDLE', 0)}</p></div>
      <div class=\"card accent-stale\"><p class=\"label\">STALE</p><p class=\"value\">{status_counts.get('STALE', 0)}</p></div>
      <div class=\"card\"><p class=\"label\">Σ Tokens (window)</p><p class=\"value\">{format_tokens(tokens_total)}</p></div>
      <div class=\"card\"><p class=\"label\">Σ Cost</p><p class=\"value\">{summary_cost}</p></div>
      <div class=\"card\"><p class=\"label\">Longest run</p><p class=\"value\">{longest_run_display}</p></div>
      <div class=\"card\"><p class=\"label\">Avg lag</p><p class=\"value\">{avg_lag}</p></div>
    </div>
    """

    html_body = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  {refresh_tag}
  <title>OpenClaw Agent Sessions</title>
  <style>
    :root {{
      --bg: #05060a;
      --panel: #0f1118;
      --panel-alt: #151823;
      --border: #1f2333;
      --text: #e8eaed;
      --muted: #9ba3b4;
      --run: #1dd1a1;
      --idle: #feca57;
      --stale: #ff6b6b;
      --exited: #576574;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: 'SFMono-Regular', Consolas, Menlo, ui-monospace, monospace;
      background: radial-gradient(circle at top, rgba(29,78,216,0.15), transparent 45%), var(--bg);
      color: var(--text);
      padding: 32px;
    }}
    h2 {{ margin: 0 0 8px; font-weight: 600; }}
    p.meta {{ color: var(--muted); margin: 4px 0 24px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 24px; }}
    .card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 12px 16px; }}
    .card .label {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin: 0; }}
    .card .value {{ font-size: 1.5rem; margin: 4px 0 0; }}
    .accent-run {{ border-color: rgba(29,209,161,0.5); box-shadow: 0 0 12px rgba(29,209,161,0.2); }}
    .accent-idle {{ border-color: rgba(254,202,87,0.5); box-shadow: 0 0 12px rgba(254,202,87,0.2); }}
    .accent-stale {{ border-color: rgba(255,107,107,0.5); box-shadow: 0 0 12px rgba(255,107,107,0.2); }}
    table {{ width: 100%; border-collapse: collapse; background: var(--panel); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
    thead th {{ background: #0b0d13; position: sticky; top: 0; z-index: 1; }}
    th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); }}
    tr:nth-child(even) {{ background: var(--panel-alt); }}
    .status {{ padding: 2px 10px; border-radius: 999px; font-weight: 600; font-size: 0.85rem; }}
    .status-run {{ background: rgba(29,209,161,0.12); color: var(--run); }}
    .status-idle {{ background: rgba(254,202,87,0.12); color: var(--idle); }}
    .status-stale {{ background: rgba(255,107,107,0.12); color: var(--stale); }}
    .status-exited {{ background: rgba(87,101,116,0.12); color: var(--exited); }}
    @media (max-width: 900px) {{
      body {{ padding: 16px; }}
      table {{ font-size: 0.85rem; }}
      th, td {{ padding: 8px; }}
    }}
  </style>
</head>
<body>
  <h2>OpenClaw Agent Sessions</h2>
  <p class=\"meta\">Last generated: {now_dt:%Y-%m-%d %H:%M:%S} &nbsp;|&nbsp; Window: {args.active_minutes} min &nbsp;|&nbsp; Sessions: {len(sessions)}</p>
  {cards_html}
  <table>
    <thead>
      <tr>
        <th>Session</th>
        <th>Status</th>
        <th>Runtime</th>
        <th>Last Update (ago)</th>
        <th>Last Update (local)</th>
        <th>Tokens</th>
        {cost_header}
        <th>Model</th>
        <th>Kind</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows_html) if rows_html else f'<tr><td colspan="{colspan}">No sessions in window</td></tr>'}
    </tbody>
  </table>
</body>
</html>
"""
    return html_body


def write_snapshot(args: argparse.Namespace) -> bool:
    try:
        sessions = fetch_sessions(args)
    except subprocess.CalledProcessError as exc:
        print(f"[agents-canvas] Failed to fetch sessions: {exc}", file=sys.stderr)
        return False

    output_path = Path(args.output)
    if not output_path.is_absolute():
        base = Path(__file__).resolve().parent.parent
        output_path = base / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(sessions, args), encoding="utf-8")
    print(f"[{datetime.now():%H:%M:%S}] Updated {output_path} (sessions: {len(sessions)})")
    return True


def main() -> None:
    args = parse_args()
    interval = max(0, args.loop)
    if interval == 0:
        write_snapshot(args)
        return

    print(f"[agents-canvas] Looping every {interval}s. Press Ctrl+C to stop.")
    try:
        while True:
            write_snapshot(args)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped loop.")


if __name__ == "__main__":
    main()
