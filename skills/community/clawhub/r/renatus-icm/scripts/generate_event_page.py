#!/usr/bin/env python3
"""
generate_event_page.py

Paste a Renatus event URL → generates a complete event landing page.

Usage:
  python3 scripts/generate_event_page.py \
    --event-url "https://backoffice.myrenatus.com/Events/EventDetails?eventId=abc123..." \
    --output site/wholesale-masters/index.html

  # Dry run (print extracted data without writing file)
  python3 scripts/generate_event_page.py --event-url "..." --dry-run

Requirements:
  - Chrome/Brave with --remote-debugging-port=9222
  - Active Renatus session in browser
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

try:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import load_config
    _cfg = load_config()
except Exception:
    _cfg = {}

from playwright.sync_api import sync_playwright

DEFAULT_CDP_URL = "http://127.0.0.1:9222"
RENATUS_HOST = "https://backoffice.myrenatus.com"

# ---------------------------------------------------------------------------
# Event page HTML template (drop-in replacement for the commercial one)
# ---------------------------------------------------------------------------
EVENT_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{event_name}} | {{company_name}}</title>
  <meta name="description" content="{{meta_description}}" />
  <style>
    :root {{
      --bg: #0f172a;
      --card: #111827;
      --card-2: #1f2937;
      --text: #e5e7eb;
      --muted: #94a3b8;
      --accent: {accent_color};
      --accent-dark: {accent_color_dark};
      --border: rgba(255,255,255,.10);
      --danger: #ef4444;
      --info: #38bdf8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
      color: var(--text);
      min-height: 100vh;
    }}
    .wrap {{ max-width: 960px; margin: 0 auto; padding: 40px 20px 64px; }}
    .hero {{ text-align: center; margin-bottom: 28px; }}
    .eyebrow {{
      display: inline-block; font-size: 12px; letter-spacing: .12em;
      text-transform: uppercase; color: var(--info); margin-bottom: 12px; font-weight: 700;
    }}
    h1 {{ margin: 0 0 12px; font-size: clamp(2rem, 4vw, 3.3rem); line-height: 1.05; }}
    .sub {{ max-width: 740px; margin: 0 auto; color: var(--muted); font-size: 1.05rem; line-height: 1.6; }}
    .grid {{ display: grid; grid-template-columns: 1.1fr .9fr; gap: 24px; margin-top: 28px; }}
    .card {{
      background: rgba(17,24,39,.92); border: 1px solid var(--border);
      border-radius: 20px; padding: 24px;
      box-shadow: 0 12px 40px rgba(0,0,0,.25); backdrop-filter: blur(8px);
    }}
    .meta {{ display: grid; gap: 14px; }}
    .meta-item {{
      background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.07);
      border-radius: 14px; padding: 14px 16px;
    }}
    .meta-label {{ color: var(--muted); font-size: 12px; letter-spacing: .08em;
      text-transform: uppercase; margin-bottom: 6px; font-weight: 700; }}
    .meta-value {{ font-size: 1rem; line-height: 1.5; font-weight: 600; }}
    .note {{
      margin-top: 18px; padding: 14px 16px; border-radius: 14px;
      background: rgba(56, 189, 248, .08); border: 1px solid rgba(56, 189, 248, .22);
      color: #dbeafe; font-size: .96rem; line-height: 1.55;
    }}
    form {{ display: grid; gap: 14px; }}
    .row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    label {{ display: block; font-size: .92rem; font-weight: 600; margin-bottom: 8px; }}
    input {{
      width: 100%; padding: 14px 15px; border-radius: 12px;
      border: 1px solid rgba(255,255,255,.14);
      background: rgba(255,255,255,.04); color: var(--text); font-size: 1rem; outline: none;
    }}
    input:focus {{ border-color: rgba(56, 189, 248, .7); box-shadow: 0 0 0 3px rgba(56, 189, 248, .14); }}
    .btn {{
      appearance: none; border: none; cursor: pointer;
      background: var(--accent); color: #052e16; font-weight: 800;
      font-size: 1rem; padding: 15px 18px; border-radius: 12px;
      transition: transform .04s ease, background .2s ease;
    }}
    .btn:hover {{ background: var(--accent-dark); color: white; }}
    .btn:disabled {{ opacity: .7; cursor: wait; }}
    .small {{ color: var(--muted); font-size: .88rem; line-height: 1.5; }}
    .status {{ display: none; border-radius: 12px; padding: 14px 16px; font-size: .95rem; line-height: 1.55; }}
    .status.ok {{ background: rgba(34,197,94,.12); border: 1px solid rgba(34,197,94,.28); color: #dcfce7; }}
    .status.err {{ background: rgba(239,68,68,.10); border: 1px solid rgba(239,68,68,.25); color: #fee2e2; }}
    .footer {{ margin-top: 22px; text-align: center; color: var(--muted); font-size: .88rem; }}
    @media (max-width: 840px) {{ .grid, .row {{ grid-template-columns: 1fr; }} .wrap {{ padding-top: 28px; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div class="eyebrow">Renatus Live Event</div>
      <h1>{{event_name}}</h1>
      <p class="sub">{{event_tagline}}</p>
    </div>

    <div class="grid">
      <div class="card">
        <div class="meta">
          <div class="meta-item">
            <div class="meta-label">Date{{s_plural}}</div>
            <div class="meta-value">{date_display}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Location</div>
            <div class="meta-value">{location_display}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Speakers</div>
            <div class="meta-value">{speakers_display}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">What you'll learn</div>
            <div class="meta-value">{{event_description}}</div>
          </div>
        </div>

        <div class="note">
          Public registrations are submitted automatically to Renatus. Based on the event rules currently exposed by Renatus, this form registers eligible attendees for the public-eligible session(s) available through Back Office.
        </div>
      </div>

      <div class="card">
        <form id="event-form">
          <input type="hidden" name="eventId" value="{{event_id}}" />
          <div class="row">
            <div>
              <label for="firstName">First name</label>
              <input id="firstName" name="firstName" autocomplete="given-name" required placeholder="Jane" />
            </div>
            <div>
              <label for="lastName">Last name</label>
              <input id="lastName" name="lastName" autocomplete="family-name" required placeholder="Smith" />
            </div>
          </div>

          <div>
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required placeholder="jane@example.com" />
          </div>

          <div>
            <label for="phone">Phone</label>
            <input id="phone" name="phone" type="tel" autocomplete="tel" required placeholder="(555) 555-5555" />
          </div>

          <input type="text" name="website" tabindex="-1" autocomplete="off" style="display:none" />

          <button id="submitBtn" class="btn" type="submit">Register now</button>

          <div id="ok" class="status ok"></div>
          <div id="err" class="status err"></div>

          <div class="small">You'll get immediate confirmation on this page once Renatus accepts the registration.</div>
        </form>
      </div>
    </div>

    <div class="footer">{{company_name}} registration page for the {{event_name}} campaign.</div>
  </div>

  <script>
    const EDGE_URL = '{{edge_url}}';
    // Event config (injected at generation time)
    const __EVENT_CONFIG__ = __EVENT_CONFIG_JSON__;
    const __CONFIRMATION_URL__ = '{{confirmation_url}}';
    // Convenience vars for confirmation redirect
    const __EVENT_NAME__ = __EVENT_CONFIG__.event_name || '{{event_name}}';
    const __EVENT_DATE__ = __EVENT_CONFIG__.event_date || '';
    const __EVENT_TIME__ = __EVENT_CONFIG__.event_time || '';
    const __EVENT_LOCATION__ = __EVENT_CONFIG__.event_location || '';
    const __EVENT_INSTRUCTORS__ = __EVENT_CONFIG__.instructors || '';
    const form = document.getElementById('event-form');
    const ok = document.getElementById('ok');
    const err = document.getElementById('err');
    const submitBtn = document.getElementById('submitBtn');

    function showOk(message) {{ ok.style.display = 'block'; err.style.display = 'none'; ok.textContent = message; }}
    function showErr(message) {{ err.style.display = 'block'; ok.style.display = 'none'; err.textContent = message; }}

    form.addEventListener('submit', async (e) => {{
      e.preventDefault();
      submitBtn.disabled = true;
      ok.style.display = 'none';
      err.style.display = 'none';

      const fd = new FormData(form);
      const payload = {{
        eventId: fd.get('eventId') || '{{event_id}}',
        firstName: String(fd.get('firstName') || '').trim(),
        lastName: String(fd.get('lastName') || '').trim(),
        email: String(fd.get('email') || '').trim(),
        phone: String(fd.get('phone') || '').trim(),
        website: String(fd.get('website') || ''),
        source_page: window.location.href
      }};

      try {{
        const resp = await fetch(EDGE_URL, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload)
        }});
        const data = await resp.json().catch(() => ({{}}));
        if (!resp.ok || data.error) {{
          throw new Error(data.details || data.error || `HTTP ${{resp.status}}`);
        }}
        form.reset();
        // Build confirmation URL with event details as query params
        const sessions = Array.isArray(data.registeredSessions) && data.registeredSessions.length
          ? data.registeredSessions.join(', ')
          : 'the available session';
        const firstName = String(fd.get('firstName') || '').trim();
        const confirmParams = new URLSearchParams({
          event_id: payload.eventId,
          event_name: window.__EVENT_NAME__ || '{{event_name}}',
          event_date: window.__EVENT_DATE__ || '',
          event_time: window.__EVENT_TIME__ || '',
          event_location: window.__EVENT_LOCATION__ || '',
          instructors: window.__EVENT_INSTRUCTORS__ || '',
          name: firstName,
        });
        const confirmUrl = (window.__CONFIRMATION_URL__ || './confirmation.html') + '?' + confirmParams.toString();
        form.reset();
        showOk(`Registration submitted for ${{sessions}}. ` +
          `<a href="$\{confirmUrl}" style="color:#22c55e;font-weight:700;">View confirmation &rarr;</a>`);
      }} catch (e) {{
        showErr(`Registration could not be completed right now. ${{e.message || 'Please try again later.'}}`);
      }} finally {{
        submitBtn.disabled = false;
      }}
    }});
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# JS: Extract event data from backoffice.myrenatus.com
# ---------------------------------------------------------------------------
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
      const k = decodeURIComponent(idx >= 0 ? part.slice(0, idx) : part);
      const v = decodeURIComponent(idx >= 0 ? part.slice(idx + 1) : '');
      out[k] = v;
    }
    return out;
  }

  function storageAuth() {
    try {
      return JSON.parse(localStorage.getItem('auth') || '{}') || {};
    } catch (_) {
      return {};
    }
  }

  let currentAuth = storageAuth();

  function xsrfToken() {
    const ls = localStorage.getItem('__RequestVerificationToken');
    if (ls) return ls;
    const c = cookies();
    for (const [k, v] of Object.entries(c)) {
      if (k.toLowerCase().includes('requestverificationtoken') || k.toLowerCase().includes('xsrf')) return v;
    }
    return null;
  }

  function accessToken() {
    return currentAuth?.access_token || '';
  }

  async function api(method, url, body = null, contentType = 'application/json; charset=UTF-8') {
    const headers = { 'x-requested-with': 'XMLHttpRequest' };
    const xsrf = xsrfToken();
    const bearer = accessToken();
    if (xsrf) headers['x-xsrf-token'] = xsrf;
    if (bearer) headers['Authorization'] = `Bearer ${bearer}`;
    if (contentType) headers['content-type'] = contentType;

    const res = await fetch(url, {
      method,
      credentials: 'include',
      headers,
      body: body == null ? undefined : (typeof body === 'string' ? body : JSON.stringify(body)),
    });

    const text = await res.text();
    let parsed = null;
    try { parsed = JSON.parse(text); } catch (_) {}

    return { ok: res.ok, status: res.status, text, json: parsed };
  }

  // Extract event ID from URL
  const urlParams = new URLSearchParams(location.search);
  let eventId = urlParams.get('eventId') || '';

  // If no eventId in URL, try from page content / React state
  if (!eventId) {
    // Try React __STATE__ or similar
    const scripts = document.querySelectorAll('script');
    for (const script of scripts) {
      const text = script.textContent || '';
      const match = text.match(/eventId["\s:]+([^"',\s]+)/i);
      if (match) { eventId = match[1]; break; }
    }
  }

  if (!eventId) {
    return { ok: false, stage: 'event_id', message: 'Could not find eventId in URL or page. Paste a URL like: backoffice.myrenatus.com/Events/EventDetails?eventId=...' };
  }

  // Fetch event
  let eventResp = await api('GET',
    `${location.origin}/api/queryproxy/execute?url=/api/event/getsavedevent?&Value=${encodeURIComponent(eventId)}`,
    null, null
  );

  // Auth refresh retry
  if (eventResp.status === 401) {
    await sleep(1500);
    eventResp = await api('GET',
      `${location.origin}/api/queryproxy/execute?url=/api/event/getsavedevent?&Value=${encodeURIComponent(eventId)}`,
      null, null
    );
  }

  if (eventResp.status === 401 || !eventResp.ok || !eventResp.json) {
    return {
      ok: false, stage: 'auth',
      message: 'Cannot access Renatus API from this browser session. Make sure you are logged into backoffice.myrenatus.com.',
      status: eventResp.status,
      hasXsrf: !!xsrfToken(), hasAccessToken: !!accessToken(),
    };
  }

  const ev = eventResp.json;

  const sessions = (ev.Sessions || []).map((s) => ({
    guid: s.SessionGuid,
    name: s.Name || 'Session',
    startDate: s.StartDate || '',
    endDate: s.EndDate || '',
    locationName: s.LocationName || 'Online',
    fee: s.Fee,
    inPersonFee: s.InPersonAttendingFee,
    mediumId: s.MediumId,
    requirements: {
      requireActiveIMA: !!s.RequireActiveIMA,
      requireXtreamEducation: !!s.RequireXtreamEducation,
      requireNoEducation: !!s.RequireNoEducation,
      isPublicEligible: !s.RequireActiveIMA && !s.RequireXtreamEducation && !s.RequireNoEducation &&
        !s.RequireOneStarQualify && !s.RequireThreeStarQualify && !s.RequireFiveStarQualify &&
        !s.RequireEssentialEducation && !s.RequireProfitEducation && !s.RequireAdvancedEducation &&
        !s.RequireGeniusIn21DaysEducation && !s.IsLeadOnly && !s.IsNonLeadOnly,
    },
  }));

  const publicSessions = sessions.filter((s) => s.requireXtreamEducation === false &&
    !s.requireActiveIMA && !s.requireNoEducation);

  return {
    ok: true,
    eventId,
    eventName: ev.Name || 'Renatus Event',
    eventTagline: ev.Tagline || ev.Description || 'Register for this exclusive Renatus event.',
    eventDescription: ev.Description || 'Learn from expert instructors in this hands-on event.',
    locationName: ev.LocationName || publicSessions[0]?.locationName || 'Online',
    sessions,
    publicSessionCount: publicSessions.length,
    publicSessions,
    rawEvent: {
      name: ev.Name,
      description: ev.Description,
      tagline: ev.Tagline,
      startDate: ev.EventStartDate,
      endDate: ev.EventEndDate,
      locationName: ev.LocationName,
    },
  };
}
"""


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Generate a Renatus event landing page from a backoffice event URL."
    )
    ap.add_argument(
        "--event-url", required=True,
        help="Renatus event URL, e.g. https://backoffice.myrenatus.com/Events/EventDetails?eventId=..."
    )
    ap.add_argument(
        "--output", required=True,
        help="Output HTML path, e.g. site/my-event/index.html"
    )
    ap.add_argument(
        "--edge-url",
        default="https://YOUR_PROJECT_REF.functions.supabase.co/submit-renatus-registration",
        help="Supabase edge function URL for form submission"
    )
    ap.add_argument(
        "--company-name", default="Autonomous Ops Studio",
        help="Company name shown in the page"
    )
    ap.add_argument(
        "--event-id",
        help="Override event ID (auto-detected from URL if omitted)"
    )
    ap.add_argument(
        "--cdp-url", default=DEFAULT_CDP_URL,
        help="Chrome CDP URL"
    )
    ap.add_argument(
        "--dry-run", action="store_true",
        help="Print extracted data without writing the HTML file"
    )
    ap.add_argument(
        "--timeout-seconds", type=int, default=60
    )
    return ap.parse_args()


def extract_event_id(url: str) -> str:
    try:
        from urllib.parse import parse_qs, urlparse
        parsed = urlparse(url)
        if parsed.query:
            params = dict(p.split("=", 1) for p in parsed.query.split("&") if "=" in p)
            return params.get("eventId", "")
        return ""
    except Exception:
        return ""


def find_authenticated_page(browser, args: argparse.Namespace):
    """Find first browser context with active Renatus auth."""
    diagnostics = []
    for idx, context in enumerate(browser.contexts):
        page = context.new_page()
        try:
            page.goto(RENATUS_HOST, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        time.sleep(1)

        check = page.evaluate("""
            () => {
                const auth = localStorage.getItem('auth');
                const xsrf = localStorage.getItem('__RequestVerificationToken');
                return { hasAuth: !!auth, hasXsrf: !!xsrf, url: location.href };
            }
        """)
        diagnostics.append({"context": idx, **check})

        if check.get("hasAuth") and check.get("hasXsrf"):
            return page, diagnostics

        try:
            page.close()
        except Exception:
            pass

    return None, diagnostics


def render_page(event_data: dict, args: argparse.Namespace) -> str:
    ev = event_data
    sessions = ev.get("sessions", [])
    public_sessions = ev.get("publicSessions", [])

    # Format dates
    date_parts = set()
    location_parts = set()
    speaker_parts = []

    for s in sessions:
        start = s.get("startDate", "")
        if start:
            # e.g. 2026-04-16T09:00:00 → Apr 16, 2026
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                date_parts.add(dt.strftime("%B %d, %Y"))
            except Exception:
                date_parts.add(start[:10])
        loc = s.get("locationName", "")
        if loc:
            location_parts.add(loc)

    date_display = "; ".join(sorted(date_parts)) if date_parts else ev.get("rawEvent", {}).get("startDate", "TBD")
    if len(date_parts) > 1:
        date_display = "See session details"

    location_display = " / ".join(sorted(location_parts)) if location_parts else ev.get("locationName", "Online")

    # Speakers (session names often contain instructor names)
    session_names = [s.get("name", "") for s in sessions]
    # De-duplicate and filter short names
    seen = set()
    for n in session_names:
        if n and len(n) > 2:
            speaker_key = n.lower()
            if speaker_key not in seen:
                seen.add(speaker_key)
                speaker_parts.append(n)
    speakers_display = ", ".join(speaker_parts[:4]) if speaker_parts else "Renatus Instructors"

    event_id = args.event_id or ev.get("eventId", "")
    event_name = ev.get("eventName", "Renatus Event")
    event_tagline = ev.get("eventTagline") or ev.get("rawEvent", {}).get("tagline") or f"Register for {event_name}"
    event_description = ev.get("eventDescription") or ev.get("rawEvent", {}).get("description") or "Learn from expert instructors in this hands-on event."

    # Truncate description if too long
    if len(event_description) > 300:
        event_description = event_description[:297] + "..."

    meta_description = f"Register for {event_name}. {event_description[:150]}"

    html = EVENT_PAGE_TEMPLATE.format(
        event_id=event_id,
        confirmation_url=args.confirmation_url or 'confirmation.html',
        event_name=event_name,
        event_tagline=event_tagline,
        event_description=event_description,
        meta_description=meta_description,
        date_display=date_display,
        location_display=location_display,
        speakers_display=speakers_display,
        edge_url=args.edge_url,
        company_name=args.company_name,
        s_plural="" if len(date_parts) == 1 else "s",
        accent_color="#22c55e",
        accent_color_dark="#16a34a",
    )
    # Inject event config JSON separately to avoid format() parsing JSON braces
    event_config_json = json.dumps({
        'event_name': event_name,
        'event_date': event_date,
        'event_time': event_time,
        'event_location': location_display,
        'instructors': speakers_display,
    }, default='')
    html = html.replace('__EVENT_CONFIG_JSON__', event_config_json)
    return html



def resolve_event_url(args) -> str:
    """Resolve the Renatus event URL: from --event-url, --event-id (config lookup), or prompt."""
    if args.event_url:
        return args.event_url
    # Try config lookup by event-id
    if args.event_id:
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from config_loader import get_event_by_id
            ev = get_event_by_id(args.event_id)
            if ev and ev.get("renatus_url"):
                print(f"Found event {args.event_id} in config: {ev.get('name', '?')}")
                return ev["renatus_url"]
            if ev:
                # Construct URL from event ID
                return f"https://backoffice.myrenatus.com/Events/EventDetails?eventId={args.event_id}"
            print(f"Warning: event {args.event_id} not found in config.json", file=sys.stderr)
        except Exception:
            pass
        return f"https://backoffice.myrenatus.com/Events/EventDetails?eventId={args.event_id}"
    # Prompt-free: construct from common pattern
    raise SystemExit("Error: --event-url or --event-id required. Run with --help for usage.")


def main() -> int:
    args = parse_args()

    event_id_from_url = extract_event_id(args.event_url)
    if not args.event_id:
        args.event_id = event_id_from_url

    print(f"Event URL: {args.event_url}")
    print(f"Output: {args.output}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url, timeout=args.timeout_seconds * 1000)

        page, diagnostics = find_authenticated_page(browser, args)
        if page is None:
            print("ERROR: No authenticated Renatus session found.", file=sys.stderr)
            print("Make sure Chrome/Brave is open to backoffice.myrenatus.com and you are logged in.", file=sys.stderr)
            print("Diagnostics:", json.dumps(diagnostics, indent=2), file=sys.stderr)
            return 1

        # Navigate to the event URL
        print(f"Navigating to: {args.event_url}")
        page.goto(args.event_url, wait_until="domcontentloaded", timeout=args.timeout_seconds * 1000)
        page.wait_for_load_state("networkidle", timeout=10000)
        time.sleep(2)

        # Extract event data
        print("Extracting event data from Renatus...")
        result = page.evaluate(EXTRACT_JS)

        if not result.get("ok"):
            print(f"FAILED: {result.get('stage')} — {result.get('message')}", file=sys.stderr)
            if result.get("diagnostics"):
                print("Diagnostics:", json.dumps(result["diagnostics"], indent=2), file=sys.stderr)
            return 1

        print(f"Event name: {result.get('eventName')}")
        print(f"Event ID:   {result.get('eventId')}")
        sessions = result.get("sessions", [])
        print(f"Sessions:   {len(sessions)} total / {result.get('publicSessionCount')} public-eligible")
        for s in sessions:
            reqs = [k for k, v in s.get("requirements", {}).items() if v]
            req_str = f"  [{', '.join(reqs)}]" if reqs else "  [PUBLIC]"
            print(f"  - {s['name']} | {s['startDate'][:10] if s.get('startDate') else 'TBD'} | {s['locationName']}{req_str}")

        if args.dry_run:
            print("\nDry run — not writing file.")
            page.close()
            return 0

        # Render HTML
        html = render_page(result, args)

        # Write output
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)

        print(f"\nGenerated: {out_path.absolute()}")
        print(f"Edge URL:  {args.edge_url}")
        print(f"Event ID:  {result.get('eventId')}")
        print()
        print("Next steps:")
        print(f"  1. Review the file: open {out_path}")
        print(f"  2. Update SUPABASE secrets: RENATUS_EVENT_ID={result.get('eventId')}")
        print(f"  3. Deploy: python3 scripts/deploy_hostinger.py (or FTP upload)")

        page.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
