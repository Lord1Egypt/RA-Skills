#!/usr/bin/env python3
"""
add_event.py

Paste a Renatus event URL → scrape details → add to config.json → generate landing page.

Usage:
  python3 scripts/add_event.py \\
    --event-url "https://backoffice.myrenatus.com/Events/EventDetails?eventId=..." \\
    --output site/my-event.html

  # Or with explicit config path
  python3 scripts/add_event.py \\
    --event-url "..." \\
    --config config.json \\
    --output site/my-event.html

Requirements:
  - Chrome/Brave with --remote-debugging-port=9222
  - Active Renatus session in browser
  - config.json (will be created from config.json.example if missing)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

# Re-use the extraction JS from generate_event_page.py
EXTRACT_JS = r
## SECURITY NOTE: What this script reads
## - localStorage.getItem('auth') → extracts access_token for API calls
## - localStorage.getItem('__RequestVerificationToken') → XSRF token for POST requests
## - document.cookie → session cookies for authenticated requests
## NO passwords are extracted. This only reads existing browser session tokens.
## Use a dedicated Chrome profile (not your main session) for CDP access.

"""
async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  function cookies() {
    const out = {};
    const raw = document.cookie || '';
    for (const part of raw.split(/;\s*/)) {
      if (!part) continue;
      const idx = part.indexOf('=');
      out[decodeURIComponent(idx >= 0 ? part.slice(0, idx) : part)] =
           decodeURIComponent(idx >= 0 ? part.slice(idx + 1) : '');
    }
    return out;
  }
  function storageAuth() {
    try { return JSON.parse(localStorage.getItem('auth') || '{}') || {}; } catch (_) { return {}; }
  }
  let currentAuth = storageAuth();
  function xsrfToken() {
    const ls = localStorage.getItem('__RequestVerificationToken');
    if (ls) return ls;
    for (const [k, v] of Object.entries(cookies())) {
      if (k.toLowerCase().includes('requestverificationtoken') || k.toLowerCase().includes('xsrf')) return v;
    }
    return null;
  }
  function accessToken() { return currentAuth?.access_token || ''; }
  async function api(method, url, body = null) {
    const headers = { 'x-requested-with': 'XMLHttpRequest' };
    const xsrf = xsrfToken(); const bearer = accessToken();
    if (xsrf) headers['x-xsrf-token'] = xsrf;
    if (bearer) headers['Authorization'] = `Bearer ${bearer}`;
    const ct = body == null ? null : 'application/json; charset=UTF-8';
    if (ct) headers['content-type'] = ct;
    const res = await fetch(url, { method, credentials: 'include', headers,
      body: body == null ? undefined : (typeof body === 'string' ? body : JSON.stringify(body)) });
    const text = await res.text(); let parsed = null;
    try { parsed = JSON.parse(text); } catch (_) {}
    return { ok: res.ok, status: res.status, text, json: parsed };
  }
  const urlParams = new URLSearchParams(location.search);
  let eventId = urlParams.get('eventId') || '';
  if (!eventId) {
    for (const script of document.querySelectorAll('script')) {
      const m = script.textContent?.match(/eventId["\s:]+([^"',\s]+)/i);
      if (m) { eventId = m[1]; break; }
    }
  }
  if (!eventId) {
    return { ok: false, stage: 'event_id', message: 'Could not find eventId in URL' };
  }
  let ev = await api('GET',
    `${location.origin}/api/queryproxy/execute?url=/api/event/getsavedevent?&Value=${encodeURIComponent(eventId)}`, null);
  if (ev.status === 401) { await sleep(1500);
    ev = await api('GET',
    `${location.origin}/api/queryproxy/execute?url=/api/event/getsavedevent?&Value=${encodeURIComponent(eventId)}`, null); }
  if (!ev.ok || !ev.json) {
    return { ok: false, stage: 'fetch',
      message: 'Cannot access Renatus API. Make sure you are logged in.',
      hasXsrf: !!xsrfToken(), hasAccessToken: !!accessToken() };
  }
  const d = ev.json;
  const sessions = (d.Sessions || []).map(s => ({
    name: s.Name, startDate: s.StartDate, endDate: s.EndDate,
    locationName: s.LocationName || 'Online', fee: s.Fee,
    requirements: {
      requireActiveIMA: !!s.RequireActiveIMA,
      requireXtreamEducation: !!s.RequireXtreamEducation,
      requireNoEducation: !!s.RequireNoEducation,
    }
  }));
  const dates = [...new Set(sessions
    .map(s => s.startDate
      ? new Date(s.startDate).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
      : null).filter(Boolean))];
  return {
    ok: true, eventId,
    eventName: d.Name || 'Renatus Event',
    tagline: d.Tagline || d.Description || '',
    description: d.Description || '',
    dates: dates.join(' and '),
    location: d.LocationName || sessions[0]?.locationName || 'Online',
    sessions,
    instructors: 'Renatus Instructors',
  };
}
"""

RENATUS_HOST = "https://backoffice.myrenatus.com"
DEFAULT_CDP_URL = "http://127.0.0.1:9222"


def parse_args():
    ap = argparse.ArgumentParser(
        description="Add a Renatus event to config.json and generate its landing page. "
                    "Paste the backoffice event URL — script scrapes details and registers it."
    )
    ap.add_argument("--event-url", required=True,
                    help="Renatus event URL, e.g. https://backoffice.myrenatus.com/Events/EventDetails?eventId=...")
    ap.add_argument("--config", default="config.json",
                    help="Path to config.json (default: config.json in current dir)")
    ap.add_argument("--output", required=True,
                    help="Output path for the generated landing page, e.g. site/my-event/index.html")
    ap.add_argument("--dry-run", action="store_true",
                    help="Scrape and print event data without writing files")
    ap.add_argument("--no-generate", dest="generate", action="store_false",
                    help="Add to config but skip generating the landing page")
    ap.add_argument("--cdp-url", default=DEFAULT_CDP_URL)
    ap.add_argument("--timeout-seconds", type=int, default=60)
    return ap.parse_args()


def find_authenticated_page(browser, cdp_url: str):
    for idx, context in enumerate(browser.contexts):
        page = context.new_page()
        try:
            page.goto(RENATUS_HOST, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        time.sleep(1)
        check = page.evaluate("""
            () => ({
                hasAuth: !!localStorage.getItem('auth'),
                hasXsrf: !!localStorage.getItem('__RequestVerificationToken'),
                url: location.href
            })
        """)
        if check.get("hasAuth") and check.get("hasXsrf"):
            return page
        try:
            page.close()
        except Exception:
            pass
    return None


def load_config(path: str) -> dict:
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    # Try .example
    example = p.with_name("config.json.example")
    if example.exists():
        print(f"Config not found at {path}, creating from example...")
        return json.loads(example.read_text())
    print(f"Warning: No config.json at {path} or {example}", file=sys.stderr)
    return {"events": []}


def save_config(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2))
    print(f"Saved config: {path}")


def add_event_to_config(config_data: dict, event_data: dict, output_path: str) -> dict:
    """Add or update event in config.events array."""
    events = config_data.get("events", [])
    event_id = event_data["eventId"]

    # Determine paths
    output_p = Path(output_path)
    site_url = config_data.get("domains", {}).get("site_url", "https://YOUR_DOMAIN")
    registration_url = str(site_url.rstrip("/")) + "/" + str(output_p.parent.name) + "/"

    new_event = {
        "id": event_id,
        "name": event_data.get("eventName", "Renatus Event"),
        "renatus_url": f"https://backoffice.myrenatus.com/Events/EventDetails?eventId={event_id}",
        "registration_url": registration_url,
        "landing_page_path": output_path,
        "email_template_path": f"email/{output_p.parent.name}-day1.html",
        "subject": f"Free Real Estate Training — {event_data.get('eventName', 'Event')}",
        "active": True,
    }

    # Update or append
    updated = False
    for i, ev in enumerate(events):
        if ev.get("id") == event_id:
            events[i] = {**ev, **new_event}
            updated = True
            break
    if not updated:
        events.append(new_event)

    config_data["events"] = events
    return config_data


def main() -> int:
    args = parse_args()

    print(f"Event URL: {args.event_url}")
    print("Connecting to browser...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url, timeout=args.timeout_seconds * 1000)
        page = find_authenticated_page(browser, args.cdp_url)
        if not page:
            print("ERROR: No authenticated Renatus session found.", file=sys.stderr)
            print("Make sure you are logged into backoffice.myrenatus.com in Chrome/Brave.", file=sys.stderr)
            return 1

        page.goto(args.event_url, wait_until="domcontentloaded", timeout=args.timeout_seconds * 1000)
        page.wait_for_load_state("networkidle", timeout=10000)
        time.sleep(2)

        result = page.evaluate(EXTRACT_JS)
        page.close()

        if not result.get("ok"):
            print(f"ERROR: {result.get('message')}", file=sys.stderr)
            return 1

    ev = result
    print(f"Event:    {ev.get('eventName')}")
    print(f"ID:       {ev.get('eventId')}")
    print(f"Date:     {ev.get('dates')}")
    print(f"Location: {ev.get('location')}")
    print(f"Sessions: {len(ev.get('sessions', []))}")

    if args.dry_run:
        print("\nDry run — not writing files.")
        return 0

    # Load config
    config = load_config(args.config)

    # Add to config
    config = add_event_to_config(config, ev, args.output)

    if args.generate:
        # Generate the landing page using generate_event_page logic inline
        # (avoids import issues across scripts)
        print(f"\nGenerating landing page: {args.output}")
        from generate_event_page import render_page
        try:
            html = render_page(ev, args)
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html, encoding="utf-8")
            print(f"Generated: {out_path.absolute()}")
        except Exception as e:
            print(f"Warning: Could not generate page ({e}). Event was added to config.", file=sys.stderr)
            print("  Run: python3 scripts/generate_event_page.py --event-id " + ev.get("eventId", "") + " --output " + args.output)

    # Save config
    save_config(args.config, config)

    print(f"\nAdded to config: {ev.get('eventName')} ({ev.get('eventId')})")
    print("Next: update config.json with any overrides, then deploy the landing page.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
