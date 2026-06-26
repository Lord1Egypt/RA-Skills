#!/usr/bin/env python3
"""
generate_email_template.py

Generate a campaign HTML email template for any Renatus event.
Feed it a Renatus event URL (CDP scrape) or pass details directly.

Usage:
  # Option A: scrape from Renatus URL (needs active browser session)
  python3 scripts/generate_email_template.py \
    --event-url "https://backoffice.myrenatus.com/Events/EventDetails?eventId=..." \
    --output email/my-event-day1.html

  # Option B: pass details directly
  python3 scripts/generate_email_template.py \
    --event-name "Commercial Core - Live Education" \
    --event-date "Thursday, April 16, 2026" \
    --event-time "9:00 AM – 5:00 PM MDT" \
    --instructors "INSTRUCTOR_NAME" \
    --event-description "Commercial real estate analysis, underwriting, cap rates..." \
    --output email/my-event-day1.html

  # Preview to stdout
  python3 scripts/generate_email_template.py --dry-run --event-name "Test Event" --instructors "Jane Smith"

Requirements:
  - Chrome/Brave with --remote-debugging-port=9222 (for --event-url mode)
  - Active Renatus session in browser
"""
from __future__ import annotations

import argparse
import base64
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
from shutil import which
from textwrap import dedent

from playwright.sync_api import sync_playwright

DEFAULT_CDP_URL = "http://127.0.0.1:9222"
RENATUS_HOST = "https://backoffice.myrenatus.com"


# ---------------------------------------------------------------------------
# HTML Email Template
# ---------------------------------------------------------------------------
EMAIL_TEMPLATE = """<!--
  Email Campaign: {event_name}
  Event: {event_date}
  Instructors: {instructors}

  SUBJECT LINE OPTIONS:
{subject_lines}
-->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{email_title}</title>
</head>
<body style="margin:0;padding:0;background-color:#f6f9fb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">

  <!-- Main Container -->
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#f6f9fb;">
    <tr>
      <td align="center" style="padding:40px 20px;">

        <!-- Email Content -->
        <table border="0" cellpadding="0" cellspacing="0" width="600" style="background-color:#ffffff;border-radius:12px;overflow:hidden;max-width:600px;width:100%;">

          <!-- Header -->
          <tr>
            <td align="center" style="background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 100%);padding:40px 30px;text-align:center;">
              <h1 style="margin:0 0 10px 0;font-size:28px;font-weight:700;color:#ffffff;line-height:1.2;">
                {header_title}
              </h1>
              <p style="margin:0;font-size:16px;color:#ffffff;opacity:0.9;">
                {header_subtitle}
              </p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:30px;">

              <!-- Urgency Banner -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#fef3c7;border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;margin-bottom:30px;">
                <tr>
                  <td style="padding:16px 20px;">
                    <p style="margin:0 0 4px 0;font-size:14px;font-weight:600;color:#92400e;">
                      {urgency_date}
                    </p>
                    <p style="margin:0;font-size:14px;color:#78350f;">
                      {urgency_location}
                    </p>
                  </td>
                </tr>
              </table>

              <!-- Intro paragraphs -->
              <p style="font-size:17px;line-height:1.6;color:#1e293b;margin:0 0 20px 0;">
                {intro_paragraph1}
              </p>

              <p style="font-size:17px;line-height:1.6;color:#1e293b;margin:0 0 30px 0;">
                {intro_paragraph2}
              </p>

              <!-- Instructors Section -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;margin:30px 0;">
                <tr>
                  <td style="padding:24px;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                      <tr>
                        <td width="120" style="padding-right:20px;vertical-align:top;">
                          <img src="{instructor_image_url}" alt="{instructors}" width="120" height="120" style="border-radius:60px;display:block;object-fit:cover;" />
                        </td>
                        <td style="vertical-align:top;">
                          <h2 style="margin:0 0 8px 0;font-size:20px;font-weight:700;color:#1e3a8a;">
                            {instructors}
                          </h2>
                          <p style="margin:0 0 10px 0;font-size:14px;color:#64748b;line-height:1.5;">
                            {instructor_bio}
                          </p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <!-- What You'll Learn -->
              <h3 style="margin:0 0 16px 0;font-size:18px;font-weight:700;color:#1e293b;">
                What you'll learn at this event:
              </h3>
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:30px;">
                <tr>
                  <td style="vertical-align:top;width:50%;padding:0 8px 8px 0;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                      <tr>
                        <td style="vertical-align:top;padding-right:10px;font-size:16px;line-height:1.4;color:#1e293b;">
                          {bullet_1}
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <!-- CTA Button -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:30px;">
                <tr>
                  <td align="center">
                    <a href="{cta_url}"
                       style="display:inline-block;background:#2563eb;color:#ffffff;font-size:16px;font-weight:700;padding:16px 32px;border-radius:8px;text-decoration:none;">
                      {cta_text}
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Footer -->
              <p style="font-size:12px;color:#94a3b8;text-align:center;margin:0;line-height:1.5;">
                You're receiving this because you signed up for updates from Renatus.
                <a href="{{unsubscribe_url}}" style="color:#94a3b8;">Unsubscribe</a>
              </p>

            </td>
          </tr>

        </table>
        <!-- End Email Content -->

      </td>
    </tr>
  </table>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# CDP extraction JS (same flow as generate_event_page.py)
# ---------------------------------------------------------------------------
EXTRACT_JS = r"""
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
    try { return JSON.parse(localStorage.getItem('auth') || '{}') || {}; } catch (_) { return {}; }
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

  function accessToken() { return currentAuth?.access_token || ''; }

  async function api(method, url, body = null, contentType = 'application/json; charset=UTF-8') {
    const headers = { 'x-requested-with': 'XMLHttpRequest' };
    const xsrf = xsrfToken();
    const bearer = accessToken();
    if (xsrf) headers['x-xsrf-token'] = xsrf;
    if (bearer) headers['Authorization'] = `Bearer ${bearer}`;
    if (contentType) headers['content-type'] = contentType;
    const res = await fetch(url, { method, credentials: 'include', headers,
      body: body == null ? undefined : (typeof body === 'string' ? body : JSON.stringify(body)) });
    const text = await res.text();
    let parsed = null;
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
    return { ok: false, stage: 'event_id', message: 'Could not find eventId in URL. Paste a URL like: backoffice.myrenatus.com/Events/EventDetails?eventId=...' };
  }

  let ev = await api('GET',
    `${location.origin}/api/queryproxy/execute?url=/api/event/getsavedevent?&Value=${encodeURIComponent(eventId)}`,
    null, null);
  if (ev.status === 401) { await sleep(1500); ev = await api('GET',
    `${location.origin}/api/queryproxy/execute?url=/api/event/getsavedevent?&Value=${encodeURIComponent(eventId)}`,
    null, null); }

  if (!ev.ok || !ev.json) {
    return { ok: false, stage: 'fetch', status: ev.status,
      message: 'Cannot access Renatus API. Make sure you are logged in to backoffice.myrenatus.com.',
      hasXsrf: !!xsrfToken(), hasAccessToken: !!accessToken() };
  }

  const data = ev.json;
  const sessions = (data.Sessions || []).map(s => ({
    name: s.Name, startDate: s.StartDate, endDate: s.EndDate,
    locationName: s.LocationName || 'Online', fee: s.Fee,
    requirements: {
      requireActiveIMA: !!s.RequireActiveIMA,
      requireXtreamEducation: !!s.RequireXtreamEducation,
      requireNoEducation: !!s.RequireNoEducation,
    }
  }));

  const dates = [...new Set(sessions
    .map(s => s.startDate ? new Date(s.startDate).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) : null)
    .filter(Boolean))];

  const times = [...new Set(sessions
    .map(s => s.startDate && s.endDate
      ? new Date(s.startDate).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZoneName: 'short' }) +
        ' – ' + new Date(s.endDate).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZoneName: 'short' })
      : null).filter(Boolean))];

  return {
    ok: true, eventId,
    eventName: data.Name || 'Renatus Event',
    tagline: data.Tagline || data.Description || '',
    description: data.Description || '',
    dates: dates.join(' and '),
    times: times.join(' | '),
    location: data.LocationName || sessions[0]?.locationName || 'Online',
    sessions,
    instructors: 'Renatus Instructors',
  };
}
"""


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Generate a campaign HTML email template for any Renatus event. "
                    "Use --event-url (CDP scrape) or pass details with flags."
    )
    ap.add_argument("--event-url", help="Renatus event URL (CDP scrape)")
    ap.add_argument("--event-name", default="", help="Event name")
    ap.add_argument("--event-date", default="", help="Event date(s)")
    ap.add_argument("--event-time", default="", help="Event time")
    ap.add_argument("--instructors", default="", help="Instructor names")
    ap.add_argument("--instructor-bio", default="", help="Instructor bio paragraph")
    ap.add_argument("--event-description", default="", help="What you'll learn / event description")
    ap.add_argument("--cta-text", default="Register Now — It's Free", help="CTA button text")
    ap.add_argument("--cta-url", default="https://YOUR_REGISTRATION_PAGE_URL/", help="CTA button URL")
    ap.add_argument("--header-title", default="", help="Email header title (default: event name)")
    ap.add_argument("--header-subtitle", default="", help="Email header subtitle")
    ap.add_argument("--instructor-image", default="https://YOUR_INSTRUCTOR_PHOTO_URL.jpg",
                    help="Instructor photo URL")
    ap.add_argument("--output", help="Output HTML file path")
    ap.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing file")
    ap.add_argument("--cdp-url", default=DEFAULT_CDP_URL)
    ap.add_argument("--timeout-seconds", type=int, default=60)
    ap.add_argument("--subject-lines", default="", help="Override subject lines (comma-separated)")
    return ap.parse_args()


def generate_subject_lines(event_name: str, event_date: str) -> str:
    date_short = ""
    if event_date:
        try:
            from datetime import datetime
            dt = datetime.strptime(event_date.split(" ")[1].rstrip(","), "%B %d")
            date_short = dt.strftime("b %d")
        except Exception:
            date_short = event_date.split(" ")[0]
    lines = [
        f"  1. Learn from operators who've done it at scale ({date_short})",
        f"  2. Free real estate training — {event_name}",
        f"  3. [Free event] {event_name} — register now",
    ]
    return "\n".join(lines)


def make_defaults(event_name: str, event_date: str, instructors: str) -> dict:
    return {
        "event_name":         event_name or "Renatus Event",
        "event_date":         event_date,
        "email_title":        f"Free Real Estate Training — {event_name}" if event_name else "Free Real Estate Training",
        "header_title":       "{{header_title}}" if not event_name else event_name,
        "header_subtitle":    "Register free — seats are limited",
        "urgency_date":       f"📅 {event_date}" if event_date else "📅 Upcoming event",
        "urgency_location":   "Online + in-person option",
        "intro_paragraph1":   "Most investors stay stuck in residential because commercial feels intimidating. The numbers are bigger. The analysis is different. One bad deal can wipe you out.",
        "intro_paragraph2":   "But what if you could learn directly from operators who've built portfolios worth $100M+?",
        "instructors":        instructors or "Renatus Expert Instructors",
        "instructor_bio":     "[INSTRUCTOR_BIO — replace with your instructor.s background]",
        "instructor_image_url": "https://YOUR_INSTRUCTOR_PHOTO_URL.jpg",
        "bullet_1":           "✔ Commercial underwriting and deal analysis",
        "cta_text":          "Register Free — Get Details",
        "cta_url":           "https://YOUR_REGISTRATION_PAGE/",
        "subject_lines":      generate_subject_lines(event_name, event_date),
    }


def render(event_name: str, event_date: str, instructors: str, args: argparse.Namespace) -> str:
    # Merge scraped/event data with CLI overrides
    defaults = make_defaults(event_name, event_date, instructors)

    # Build bullet list from description
    bullets = []
    desc = args.event_description or defaults.get("intro_paragraph1", "")
    if desc:
        # split on periods / newlines and take first 4 meaningful sentences
        sentences = [s.strip() for s in desc.replace("\n", ". ").split(".") if len(s.strip()) > 20]
        for s in sentences[:4]:
            bullets.append(f"✔ {s.strip()}.")
    bullet_text = "<br>".join(bullets) if bullets else defaults.get("bullet_1", "")

    # Resolve placeholders with actual values
    header_title = args.header_title or event_name or "Renatus Event"
    subject_lines = args.subject_lines or generate_subject_lines(header_title, event_date)

    subs = {
        "event_name":          event_name or "Renatus Event",
        "event_date":          event_date,
        "email_title":         f"Free Real Estate Training — {header_title}",
        "header_title":        header_title,
        "header_subtitle":     args.header_subtitle or defaults.get("header_subtitle", ""),
        "urgency_date":        f"📅 {event_date}" if event_date else "📅 Upcoming event",
        "urgency_location":    args.urgency_location if hasattr(args, 'urgency_location') else defaults.get("urgency_location", ""),
        "intro_paragraph1":   args.event_description or defaults.get("intro_paragraph1", ""),
        "intro_paragraph2":   args.intro_paragraph2 if hasattr(args, 'intro_paragraph2') and args.intro_paragraph2 else defaults.get("intro_paragraph2", ""),
        "instructors":        instructors or args.instructors or defaults.get("instructors", ""),
        "instructor_bio":    args.instructor_bio or defaults.get("instructor_bio", ""),
        "instructor_image_url": args.instructor_image,
        "bullet_1":           bullet_text,
        "cta_text":           args.cta_text,
        "cta_url":            args.cta_url,
        "subject_lines":      subject_lines,
    }

    html = EMAIL_TEMPLATE
    for k, v in subs.items():
        html = html.replace(f"{{{k}}}", str(v) if v else "")

    return html


def find_authenticated_page(browser, cdp_url: str, timeout: int):
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
        if check.get("hasAuth") and check.get("hasXsrf"):
            return page
        try:
            page.close()
        except Exception:
            pass
    return None


def main() -> int:
    args = parse_args()

    # If --event-url, scrape from CDP
    event_name = args.event_name
    event_date = args.event_date
    instructors = args.instructors

    if args.event_url:
        print(f"Event URL: {args.event_url}")
        print("Connecting to browser CDP...")
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(args.cdp_url, timeout=args.timeout_seconds * 1000)
            page = find_authenticated_page(browser, args.cdp_url, args.timeout_seconds)
            if not page:
                print("ERROR: No authenticated Renatus session found.", file=sys.stderr)
                print("Make sure you are logged into backoffice.myrenatus.com in Chrome/Brave.", file=sys.stderr)
                return 1

            page.goto(args.event_url, wait_until="domcontentloaded", timeout=args.timeout_seconds * 1000)
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(2)

            result = page.evaluate(EXTRACT_JS)
            if not result.get("ok"):
                print(f"ERROR: {result.get('message')}", file=sys.stderr)
                return 1

            event_name  = result.get("eventName",  args.event_name)
            event_date  = result.get("dates",        args.event_date) or result.get("times", "")
            instructors = result.get("instructors",  args.instructors)

            print(f"Event:    {event_name}")
            print(f"Date:     {event_date}")
            print(f"Location: {result.get('location', '')}")
            print(f"Instructors: {instructors}")
            sessions = result.get("sessions", [])
            print(f"Sessions: {len(sessions)}")
            for s in sessions:
                reqs = [k for k, v in s.get("requirements", {}).items() if v]
                req_str = f"  [{', '.join(reqs)}]" if reqs else "  [PUBLIC]"
                print(f"  - {s['name']} | {s['locationName']}{req_str}")

            if args.dry_run:
                print("\nDry run — not writing file.")
                return 0

    if not event_name and not args.dry_run:
        print("ERROR: --event-name required (or use --event-url to scrape)", file=sys.stderr)
        return 1

    if args.dry_run and not event_name:
        event_name = "Test Event"
        event_date = "Thursday, May 1, 2026"
        instructors = "Jane Smith"

    html = render(event_name, event_date, instructors, args)

    if args.dry_run:
        print("\n" + "=" * 60)
        print("GENERATED EMAIL TEMPLATE (first 1500 chars):")
        print("=" * 60)
        print(html[:1500])
        print("...\n[truncated]")
        return 0

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"\nGenerated: {out_path.absolute()}")
    print(f"Next: open {out_path} in a browser to preview")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
