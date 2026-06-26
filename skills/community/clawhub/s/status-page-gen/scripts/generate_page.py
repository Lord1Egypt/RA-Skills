#!/usr/bin/env python3
"""
generate_page.py — Generate a self-contained dark-theme HTML status page.

Takes service check JSON and cert check JSON, produces a single HTML file
with all CSS inline. No external dependencies, no CDN links, no JS frameworks.

Usage:
    python3 generate_page.py \
        --services /tmp/status_check.json \
        --certs /tmp/cert_check.json \
        --history assets/history.json \
        --output ~/status.html

    # Minimal (services only)
    python3 generate_page.py --services /tmp/status_check.json --output ~/status.html
"""

import argparse
import html
import json
import os
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# CSS — dark theme, no external dependencies
# ---------------------------------------------------------------------------
CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:         #0f1117;
  --bg-card:    #1a1d27;
  --bg-card2:   #222636;
  --border:     #2e3147;
  --text:       #e2e8f0;
  --text-muted: #7c85a2;
  --up:         #22c55e;
  --up-bg:      #14532d30;
  --degraded:   #f59e0b;
  --degraded-bg:#451a0330;
  --down:       #ef4444;
  --down-bg:    #450a0a30;
  --warn:       #f59e0b;
  --warn-bg:    #451a0340;
  --accent:     #6366f1;
  --radius:     10px;
  --font:       -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --mono:       ui-monospace, "SF Mono", "Cascadia Code", monospace;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-size: 15px;
  line-height: 1.6;
  min-height: 100vh;
  padding: 0 0 60px;
}

header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 28px 0;
  margin-bottom: 36px;
}

.header-inner {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.header-title h1 {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.header-title p {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 2px;
}

.overall-badge {
  font-size: 13px;
  font-weight: 600;
  padding: 6px 16px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  white-space: nowrap;
}

.overall-badge.all-up   { background: var(--up-bg);       color: var(--up);       border: 1px solid var(--up); }
.overall-badge.has-down { background: var(--down-bg);     color: var(--down);     border: 1px solid var(--down); }
.overall-badge.has-deg  { background: var(--degraded-bg); color: var(--degraded); border: 1px solid var(--degraded); }

.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.dot.up       { background: var(--up);       box-shadow: 0 0 6px var(--up); }
.dot.degraded { background: var(--degraded); box-shadow: 0 0 6px var(--degraded); }
.dot.down     { background: var(--down);     box-shadow: 0 0 6px var(--down); }

main {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Summary row */
.summary-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 14px;
  margin-bottom: 32px;
}

.summary-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 16px;
  text-align: center;
}

.summary-card .num {
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
}

.summary-card .label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 5px;
}

.num.up       { color: var(--up); }
.num.degraded { color: var(--degraded); }
.num.down     { color: var(--down); }

/* Section heading */
.section-heading {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 10px;
  margin-top: 28px;
  padding-left: 2px;
}

/* Service cards */
.service-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.service-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 20px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px 20px;
  align-items: start;
  transition: border-color 0.15s;
}

.service-card:hover { border-color: #3d4265; }

.service-card.up       { border-left: 3px solid var(--up); }
.service-card.degraded { border-left: 3px solid var(--degraded); }
.service-card.down     { border-left: 3px solid var(--down); }

.service-name {
  font-weight: 600;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 9px;
}

.service-meta {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.service-meta span { display: flex; align-items: center; gap: 4px; }

.badge {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.badge.up       { background: var(--up-bg);       color: var(--up); }
.badge.degraded { background: var(--degraded-bg); color: var(--degraded); }
.badge.down     { background: var(--down-bg);     color: var(--down); }

.service-right {
  text-align: right;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

/* Uptime bars */
.uptime-row {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.uptime-item {
  text-align: center;
}

.uptime-pct {
  font-size: 14px;
  font-weight: 600;
  font-family: var(--mono);
}

.uptime-label {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
}

.uptime-pct.high   { color: var(--up); }
.uptime-pct.medium { color: var(--degraded); }
.uptime-pct.low    { color: var(--down); }

/* Cert warning banner */
.cert-warning {
  background: var(--warn-bg);
  border: 1px solid var(--warn);
  border-radius: 6px;
  color: var(--warn);
  font-size: 12px;
  padding: 4px 10px;
  margin-top: 6px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

/* Tags */
.tag {
  background: var(--bg-card2);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 11px;
  color: var(--text-muted);
  padding: 1px 7px;
}

/* HTTP error detail */
.error-detail {
  font-size: 11px;
  font-family: var(--mono);
  color: var(--down);
  margin-top: 4px;
}

/* Footer */
footer {
  max-width: 860px;
  margin: 48px auto 0;
  padding: 0 24px;
  border-top: 1px solid var(--border);
  padding-top: 20px;
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

/* Responsive */
@media (max-width: 600px) {
  .service-card { grid-template-columns: 1fr; }
  .service-right { text-align: left; align-items: flex-start; }
  .header-inner  { flex-direction: column; align-items: flex-start; }
}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    """HTML-escape a string."""
    return html.escape(str(s), quote=True)


def fmt_rtt(ms) -> str:
    if ms is None:
        return "—"
    return f"{ms:.0f}ms"


def uptime_class(pct) -> str:
    if pct is None:
        return ""
    if pct >= 99:
        return "high"
    if pct >= 95:
        return "medium"
    return "low"


def fmt_uptime(pct) -> str:
    if pct is None:
        return "—"
    return f"{pct:.1f}%"


def load_json(path: str, label: str) -> dict | None:
    if not path:
        return None
    if not os.path.exists(path):
        print(f"WARNING: {label} file not found: {path}", file=sys.stderr)
        return None
    with open(path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"WARNING: Invalid JSON in {label} file: {e}", file=sys.stderr)
            return None


def build_cert_map(cert_data: dict | None) -> dict:
    """Build a map of service_name → cert info."""
    if not cert_data:
        return {}
    return {c["service_name"]: c for c in cert_data.get("certs", [])}


def build_history_map(history_data: dict | None) -> dict:
    """Build a map of service_name → {uptime_24h, uptime_7d, uptime_30d}."""
    if not history_data:
        return {}
    return history_data.get("services", {})


def overall_status(services: list) -> str:
    statuses = [s.get("status") for s in services]
    if "down" in statuses:
        return "down"
    if "degraded" in statuses:
        return "degraded"
    return "up"


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def render_service_card(svc: dict, cert_map: dict, history_map: dict) -> str:
    name = svc.get("name", "Unknown")
    status = svc.get("status", "unknown")
    url = svc.get("url", "")
    http_info = svc.get("http", {})
    ping_info = svc.get("ping", {})
    tags = svc.get("tags", [])
    last_checked = svc.get("last_checked", "")

    rtt = http_info.get("response_time_ms")
    status_code = http_info.get("status_code")
    http_error = http_info.get("error")
    ping_ok = ping_info.get("ok", False)

    cert = cert_map.get(name, {})
    uptime = history_map.get(name, {})

    # Cert warning
    cert_html = ""
    if cert:
        if cert.get("expired"):
            cert_html = f'<div class="cert-warning">⚠ SSL EXPIRED ({abs(cert.get("days_remaining", 0))}d ago)</div>'
        elif cert.get("expiring_soon"):
            cert_html = f'<div class="cert-warning">⚠ SSL expires in {cert.get("days_remaining")}d</div>'
        elif cert.get("error"):
            cert_html = f'<div class="cert-warning">⚠ SSL check failed: {esc(cert["error"])}</div>'

    # Tags
    tags_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)

    # Meta row
    meta_parts = []
    if url:
        meta_parts.append(f'<span>🔗 {esc(url)}</span>')
    if rtt is not None:
        meta_parts.append(f'<span>⚡ {fmt_rtt(rtt)}</span>')
    if status_code is not None:
        meta_parts.append(f'<span>HTTP {status_code}</span>')
    if ping_ok:
        meta_parts.append('<span>📡 ping ok</span>')
    if tags:
        meta_parts.append(f'<span style="display:flex;gap:4px;flex-wrap:wrap">{tags_html}</span>')

    meta_html = "".join(f'<span>{p}</span>' if not p.startswith("<span") else p for p in meta_parts)

    # Error detail
    error_html = ""
    if http_error and status != "up":
        error_html = f'<div class="error-detail">{esc(http_error)}</div>'

    # Uptime bars
    uptime_html = ""
    if uptime:
        u24 = uptime.get("uptime_24h")
        u7d = uptime.get("uptime_7d")
        u30d = uptime.get("uptime_30d")
        uptime_html = f"""
        <div class="uptime-row">
          <div class="uptime-item">
            <span class="uptime-pct {uptime_class(u24)}">{fmt_uptime(u24)}</span>
            <span class="uptime-label">24h</span>
          </div>
          <div class="uptime-item">
            <span class="uptime-pct {uptime_class(u7d)}">{fmt_uptime(u7d)}</span>
            <span class="uptime-label">7d</span>
          </div>
          <div class="uptime-item">
            <span class="uptime-pct {uptime_class(u30d)}">{fmt_uptime(u30d)}</span>
            <span class="uptime-label">30d</span>
          </div>
        </div>"""

    return f"""
    <div class="service-card {esc(status)}">
      <div class="service-left">
        <div class="service-name">
          <span class="dot {esc(status)}"></span>
          {esc(name)}
        </div>
        <div class="service-meta">{meta_html}</div>
        {error_html}
        {cert_html}
      </div>
      <div class="service-right">
        <span class="badge {esc(status)}">{esc(status)}</span>
        {uptime_html}
      </div>
    </div>"""


def render_page(
    services_data: dict,
    cert_data: dict | None,
    history_data: dict | None,
    title: str = "Service Status",
) -> str:
    """Render a complete self-contained HTML status page."""

    services = services_data.get("services", [])
    checked_at_raw = services_data.get("checked_at", "")
    cert_map = build_cert_map(cert_data)
    history_map = build_history_map(history_data)

    # Parse checked_at for display
    try:
        checked_dt = datetime.fromisoformat(checked_at_raw.replace("Z", "+00:00"))
        checked_str = checked_dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        checked_str = checked_at_raw or "Unknown"

    # Counts
    total = len(services)
    up_count = sum(1 for s in services if s.get("status") == "up")
    degraded_count = sum(1 for s in services if s.get("status") == "degraded")
    down_count = sum(1 for s in services if s.get("status") == "down")

    # Overall status
    ov = overall_status(services)
    if ov == "up":
        badge_class = "all-up"
        badge_text = "All Systems Operational"
        badge_dot = "up"
    elif ov == "down":
        badge_class = "has-down"
        badge_text = f"{down_count} Service{'s' if down_count != 1 else ''} Down"
        badge_dot = "down"
    else:
        badge_class = "has-deg"
        badge_text = f"{degraded_count} Service{'s' if degraded_count != 1 else ''} Degraded"
        badge_dot = "degraded"

    # Sort: down first, then degraded, then up
    order = {"down": 0, "degraded": 1, "up": 2}
    sorted_services = sorted(services, key=lambda s: order.get(s.get("status", "up"), 9))

    # Cert warnings
    cert_warnings = []
    if cert_data:
        for c in cert_data.get("certs", []):
            if c.get("expired") or c.get("expiring_soon") or c.get("error"):
                cert_warnings.append(c)

    # Build service cards
    cards_html = "\n".join(
        render_service_card(svc, cert_map, history_map) for svc in sorted_services
    )

    # Cert summary section (top-level warnings)
    cert_banner = ""
    if cert_warnings:
        items = []
        for c in cert_warnings:
            sname = esc(c.get("service_name", c.get("host", "?")))
            if c.get("expired"):
                items.append(f'<li>⚠ <strong>{sname}</strong> — SSL certificate EXPIRED</li>')
            elif c.get("expiring_soon"):
                items.append(f'<li>⚠ <strong>{sname}</strong> — SSL expires in {c["days_remaining"]} days</li>')
            elif c.get("error"):
                items.append(f'<li>⚠ <strong>{sname}</strong> — SSL check failed: {esc(c["error"])}</li>')

        cert_banner = f"""
    <div class="section-heading">SSL Certificate Warnings</div>
    <div class="service-card" style="border-left:3px solid var(--warn)">
      <ul style="list-style:none;display:flex;flex-direction:column;gap:6px;color:var(--warn);font-size:13px;">
        {"".join(items)}
      </ul>
    </div>"""

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="300">
  <title>{esc(title)}</title>
  <style>
{CSS}
  </style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="header-title">
      <h1>{esc(title)}</h1>
      <p>Last checked: {esc(checked_str)}</p>
    </div>
    <div class="overall-badge {badge_class}">
      <span class="dot {badge_dot}"></span>
      {esc(badge_text)}
    </div>
  </div>
</header>

<main>

  <div class="summary-row">
    <div class="summary-card">
      <div class="num">{total}</div>
      <div class="label">Total</div>
    </div>
    <div class="summary-card">
      <div class="num up">{up_count}</div>
      <div class="label">Operational</div>
    </div>
    <div class="summary-card">
      <div class="num degraded">{degraded_count}</div>
      <div class="label">Degraded</div>
    </div>
    <div class="summary-card">
      <div class="num down">{down_count}</div>
      <div class="label">Down</div>
    </div>
  </div>

  {cert_banner}

  <div class="section-heading">Services</div>
  <div class="service-list">
    {cards_html}
  </div>

</main>

<footer>
  <span>status-page-gen · Generated {esc(generated_at)}</span>
  <span>{up_count}/{total} services operational</span>
</footer>

</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate a self-contained HTML status page."
    )
    parser.add_argument(
        "--services",
        required=True,
        help="Path to check_services.py JSON output",
    )
    parser.add_argument(
        "--certs",
        default=None,
        help="Path to check_certs.py JSON output (optional)",
    )
    parser.add_argument(
        "--history",
        default=None,
        help="Path to history database (assets/history.json)",
    )
    parser.add_argument(
        "--output",
        default="status.html",
        help="Output HTML file path (default: status.html)",
    )
    parser.add_argument(
        "--title",
        default="Service Status",
        help='Page title (default: "Service Status")',
    )
    args = parser.parse_args()

    # Load inputs
    services_data = load_json(args.services, "services check")
    if not services_data:
        print("ERROR: Cannot load services check data.", file=sys.stderr)
        sys.exit(1)

    cert_data = load_json(args.certs, "cert check") if args.certs else None
    history_data = None

    if args.history:
        raw = load_json(args.history, "history")
        if raw:
            if "services" in raw and "entries" not in raw:
                # Already pre-computed stats format (e.g. from get_stats output)
                history_data = raw
            elif "entries" in raw:
                # Raw history log — compute stats on the fly via history.py
                import importlib.util, os as _os

                skill_dir = _os.path.dirname(_os.path.abspath(__file__))
                history_script = _os.path.join(skill_dir, "history.py")

                if _os.path.exists(history_script):
                    spec = importlib.util.spec_from_file_location("history_mod", history_script)
                    history_mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(history_mod)
                    history_data = history_mod.get_stats(args.history)
                else:
                    print("WARNING: history.py not found; skipping uptime stats.", file=sys.stderr)

    # Render
    page = render_page(services_data, cert_data, history_data, args.title)

    # Write output
    output_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(output_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"Status page written to: {args.output}", file=sys.stderr)
    print(f"  Services: {services_data.get('total', '?')} total, "
          f"{services_data.get('up', '?')} up, "
          f"{services_data.get('down', '?')} down", file=sys.stderr)


if __name__ == "__main__":
    main()
