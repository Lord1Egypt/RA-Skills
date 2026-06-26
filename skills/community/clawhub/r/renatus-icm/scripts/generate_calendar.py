#!/usr/bin/env python3
"""
generate_calendar.py

Generate an events calendar HTML page from config.json events.
Lists all active events with registration links.

Usage:
  python3 scripts/generate_calendar.py --output site/calendar.html
  python3 scripts/generate_calendar.py --dry-run
  python3 scripts/generate_calendar.py --config config.json --output site/calendar.html
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import load_config, active_events
except Exception:
    load_config = None
    active_events = None


CALENDAR_CSS = """
:root {
  --bg: #0f172a;
  --card: #111827;
  --card-2: #1f2937;
  --text: #e5e7eb;
  --muted: #94a3b8;
  --accent: #22c55e;
  --accent-dark: #16a34a;
  --border: rgba(255,255,255,.10);
  --info: #38bdf8;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
  background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
  color: var(--text);
  min-height: 100vh;
}
.wrap { max-width: 960px; margin: 0 auto; padding: 40px 20px 64px; }
.hero { text-align: center; margin-bottom: 48px; }
.eyebrow { display: inline-block; font-size: 12px; letter-spacing: .12em;
  text-transform: uppercase; color: var(--info); margin-bottom: 12px; font-weight: 700; }
h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; line-height: 1.1; }
.sub { color: var(--muted); font-size: 1.05rem; line-height: 1.6; max-width: 600px; margin: 0 auto; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.card {
  background: rgba(17,24,39,.92); border: 1px solid var(--border);
  border-radius: 16px; padding: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,.2);
  display: flex; flex-direction: column; gap: 12px;
}
.card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.badge { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  padding: 4px 10px; border-radius: 100px; }
.badge-upcoming { background: rgba(34,197,94,.15); color: #4ade80; border: 1px solid rgba(34,197,94,.3); }
.badge-past { background: rgba(239,68,68,.10); color: #f87171; border: 1px solid rgba(239,68,68,.25); }
.card h2 { font-size: 1.15rem; font-weight: 700; line-height: 1.3; color: var(--text); }
.meta { display: flex; flex-direction: column; gap: 6px; }
.meta-item { display: flex; align-items: center; gap: 8px; color: var(--muted); font-size: .9rem; }
.meta-icon { font-size: 14px; flex-shrink: 0; }
.meta-value { color: var(--text); font-weight: 500; }
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  background: var(--accent); color: #052e16; font-weight: 800; font-size: .9rem;
  padding: 12px 20px; border-radius: 10px; text-decoration: none;
  transition: background .2s ease; margin-top: auto;
}
.btn:hover { background: var(--accent-dark); color: white; }
.footer { margin-top: 48px; text-align: center; color: var(--muted); font-size: .85rem; }
.empty { text-align: center; padding: 60px 20px; color: var(--muted); }
.empty p { font-size: 1.1rem; margin-bottom: 8px; }
.empty span { font-size: .9rem; }
@media (max-width: 640px) { .grid { grid-template-columns: 1fr; } .wrap { padding-top: 28px; } }
"""

CALENDAR_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{page_title}}</title>
  <style>{css}</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div class="eyebrow">Upcoming Events</div>
      <h1>{{hero_title}}</h1>
      <p class="sub">{{hero_subtitle}}</p>
    </div>

    {{event_grid}}

    <div class="footer">
      <p>Questions? Contact us at the links below.</p>
    </div>
  </div>
</body>
</html>
"""

EVENT_CARD = """    <div class="card">
      <div class="card-header">
        <h2>{name}</h2>
        <span class="badge badge-{status}">{status_label}</span>
      </div>
      <div class="meta">
        <div class="meta-item">
          <span class="meta-icon">📅</span>
          <span class="meta-value">{dates}</span>
        </div>
        {location_html}
        {instructor_html}
      </div>
      <a href="{registration_url}" class="btn">Register Free →</a>
    </div>"""


def parse_args():
    ap = argparse.ArgumentParser(
        description="Generate an events calendar page from config.json events."
    )
    ap.add_argument("--config", default="config.json",
                    help="Path to config.json (default: config.json in current dir)")
    ap.add_argument("--output", default="site/calendar.html",
                    help="Output HTML path")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--page-title", default="Renatus Events Calendar",
                    help="Page <title> and H1")
    ap.add_argument("--hero-title", default="Free Real Estate Training Events",
                    help="Hero headline")
    ap.add_argument("--hero-subtitle",
                    default="Register for free live training from experienced real estate investors.",
                    help="Hero subtitle")
    return ap.parse_args()


def get_events(config_path: str) -> list[dict]:
    # Use config_loader from skill scripts dir; pass the caller's config path
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from config_loader import load_config
        cfg = load_config(config_path_override=config_path)
        return cfg.get("events", [])
    except Exception:
        pass
    # Fallback: load JSON directly from config_path
    p = Path(config_path)
    if p.exists():
        data = json.loads(p.read_text())
        return data.get("events", [])
    return []


def event_status(event: dict) -> tuple[str, str]:
    """Return (status_class, status_label) based on event dates."""
    # Try to parse a date from the event name or metadata
    # For now, use the "active" flag; can enhance with actual date parsing later
    if not event.get("active", True):
        return "past", "Ended"
    return "upcoming", "Upcoming"


def make_location_html(event: dict) -> str:
    loc = event.get("location", "")
    if not loc:
        return ""
    return f"""        <div class="meta-item">
          <span class="meta-icon">📍</span>
          <span class="meta-value">{loc}</span>
        </div>"""


def make_instructor_html(event: dict) -> str:
    instructor = event.get("instructors", "")
    if not instructor:
        return ""
    return f"""        <div class="meta-item">
          <span class="meta-icon">👤</span>
          <span class="meta-value">{instructor}</span>
        </div>"""


def render_event_card(event: dict) -> str:
    status_class, status_label = event_status(event)
    return EVENT_CARD.format(
        name=event.get("name", "Renatus Event"),
        status=status_class,
        status_label=status_label,
        dates=event.get("dates", event.get("date", "TBD")),
        location_html=make_location_html(event),
        instructor_html=make_instructor_html(event),
        registration_url=event.get("registration_url", "#"),
    )


def build_grid(events: list[dict]) -> str:
    if not events:
        return """<div class="empty">
      <p>No events found.</p>
      <span>Add events to config.json to display them here.</span>
    </div>"""
    cards = "\n".join(render_event_card(ev) for ev in events)
    return f'<div class="grid">\n{cards}\n    </div>'


def render(args) -> str:
    events = get_events(args.config)
    grid = build_grid(events)

    html = CALENDAR_TEMPLATE.replace("{{page_title}}", args.page_title)
    html = html.replace("{{hero_title}}", args.hero_title)
    html = html.replace("{{hero_subtitle}}", args.hero_subtitle)
    html = html.replace("{{event_grid}}", grid)
    html = html.replace("{css}", CALENDAR_CSS.strip())

    # Inject active event count into hero subtitle
    count = len(events)
    if count:
        html = html.replace(
            "{{hero_subtitle}}",
            f" {count} free event{'s' if count != 1 else ''} available. {args.hero_subtitle}"
        )
    return html


def main() -> int:
    args = parse_args()

    events = get_events(args.config)
    print(f"Config: {args.config}")
    print(f"Events found: {len(events)}")
    for ev in events:
        status = "active" if ev.get("active", True) else "inactive"
        print(f"  [{status}] {ev.get('name', '?')} — {ev.get('registration_url', 'no URL')}")

    html = render(args)

    if args.dry_run:
        print(f"\n=== Calendar HTML Preview (first 1000 chars) ===")
        print(html[:1000])
        print("...\n[truncated]")
        return 0

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"\nGenerated: {out.absolute()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
