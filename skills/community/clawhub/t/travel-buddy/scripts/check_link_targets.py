#!/usr/bin/env python3
"""Follow every outbound link on a rendered Travel Buddy page and report where it lands.

Usage: python check_link_targets.py <final.html> [--timeout 20] [--workers 8] [--json report.json]

WHY THIS IS A SEPARATE SCRIPT, AND NOT PART OF THE DELIVERY GATE
---------------------------------------------------------------
`render_final_trip_html.py`, `check_plan_consistency.py` and `validate_trip_html.py` are offline
and deterministic: the same input always gives the same verdict, so `save_trip_deliverables.py`
can import them and refuse to save. This check cannot join them, because it needs the network.
Wiring it into the save path would make saving fail on a plane, in CI, or behind a captive
portal — and a gate that fails for reasons unrelated to the work is a gate people learn to skip.
So it runs on demand, and SKILL.md names it in the pre-delivery checklist instead.

WHAT IT CATCHES
---------------
A button can name the right provider, use HTTPS, carry every required attribute, and still show
the traveller nothing — a dead host, a link that redirects onto a different company's site, a
provider that answers 404 for a path someone hand-built. Those are decidable from one request.

THE VERDICT DEPENDS ON THE USER AGENT, WHICH IS WHY `broken` IS NARROW
---------------------------------------------------------------------
This was measured, and it nearly shipped as a false accusation. The same Google Flights URL:

    User-Agent: Chrome/124      →  HTTP 200, no redirect, no "unsupported" anywhere
    User-Agent: Python-urllib   →  HTTP 200, redirected to /travel/flights/unsupported

An earlier check ran those two requests with different agents, compared the results, and
concluded the link was broken. It was not; the agent string was doing the talking. A checker
that reports `broken` on a landing path therefore reports something about itself, not about the
traveller's browser.

So `broken` is reserved for what survives any plausible agent: a hard 4xx/5xx that is not a
known challenge code, or a redirect onto a different host. Everything else that looks wrong —
an "unsupported"-shaped landing path, dropped query parameters, a refused connection, a 202/403
challenge — is `unverified`: a finding the author must read and resolve by opening it in a real
browser, never a silent pass and never an accusation.

On one real page klm.nl refused the connection outright, transavia.com returned 403, and every
booking.com URL answered 202 with its query string stripped. All five open normally in a
browser. A checker that failed them would cry wolf on most real travel links and be switched
off within a week, taking any genuine defect with it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Statuses that mean "a machine asked, so the site said no" rather than "this link is broken".
BOT_STATUSES = {202, 403, 405, 429}
# Statuses that mean "ask again, more slowly". A host that rate-limits a burst answers these to
# the 5th request and 200 to the 1st, so a single reading of one is a statement about the burst.
RETRY_STATUSES = {429, 500, 502, 503, 504}
RETRY_BACKOFF = (1.5, 4.0)          # seconds before retry 1 and retry 2
MIN_HOST_INTERVAL = 1.1             # seconds between two requests to the SAME host

# One lock and one "last request" clock per host, so requests to a host are spaced while requests
# to DIFFERENT hosts stay fully concurrent. This is the whole fix: the pool's speed was never the
# problem, hammering one host with it was.
#
# Measured on a real delivered page, 2026-09-12: eight dining cards pointed at one aggregator.
# Requests 1-4 returned 200 and 5-8 returned HTTP 503, so the page reported EIGHT broken links
# that a browser opens fine -- and two runs of the same file disagreed (`42 ok, 0 broken` then
# `34 ok, 8 broken`), which is worse than either verdict alone: the author believes whichever run
# they saw. The author then rewrote fourteen URLs away from a source that works.
_HOST_LOCKS: dict[str, threading.Lock] = {}
_HOST_LAST: dict[str, float] = {}
_HOST_SLOW: set[str] = set()
_HOST_TABLE_LOCK = threading.Lock()


def _host_pushed_back(host: str) -> None:
    """Remember that this host answered a burst with a retry status."""
    with _HOST_TABLE_LOCK:
        _HOST_SLOW.add(host)


def _host_gate(host: str) -> None:
    """Space requests to a host that has pushed back; leave every other host at full speed.

    Throttling every host unconditionally was the first version of this fix and it was too
    expensive to keep: measured on the delivered page below, 31 of 37 links point at one map
    provider that never rate-limits, and serialising them took the run from a few seconds to
    **34.2 s**. This repository already knows what a slow gate becomes -- `check_link_targets.py`
    is deliberately outside `save_trip_deliverables.py` because "a gate that fails on a plane or
    in CI is a gate people learn to skip", and a gate people skip catches nothing.

    So the interval is applied only to hosts that have actually answered with a retry status in
    this run. Normal pages pay nothing; the one host that throttles gets asked politely.
    """
    with _HOST_TABLE_LOCK:
        if host not in _HOST_SLOW:
            return
        lock = _HOST_LOCKS.setdefault(host, threading.Lock())
    lock.acquire()
    try:
        wait = MIN_HOST_INTERVAL - (time.monotonic() - _HOST_LAST.get(host, 0.0))
        if wait > 0:
            time.sleep(wait)
    finally:
        _HOST_LAST[host] = time.monotonic()
        lock.release()
# Path fragments a provider uses to say it could not honour the request it was handed.
DEAD_END_MARKERS = ("unsupported", "/error", "not-found", "notfound", "/404", "page-not-found")
LINK_CLASSES = ("booking-link", "dining-link", "map-link")


def extract_links(html: str) -> list[tuple[str, str]]:
    """Return (kind, url) for every outbound button, de-duplicated, in document order."""
    found: dict[str, str] = {}
    for match in re.finditer(r'<a\s+class="([^"]*)"([^>]*?)href="([^"]+)"', html):
        class_attr, attrs, href = match.group(1), match.group(2), unescape(match.group(3))
        if not any(name in class_attr for name in LINK_CLASSES):
            continue
        if not href.lower().startswith("https://"):
            continue
        booking_type = re.search(r'data-booking-type="([^"]*)"', attrs)
        if booking_type:
            kind = booking_type.group(1)
        elif "dining-link" in class_attr:
            kind = "dining"
        else:
            kind = "map"
        found.setdefault(href, kind)
    return [(kind, url) for url, kind in found.items()]


def probe(url: str, timeout: float) -> dict:
    """Ask once, then up to twice more with backoff if the answer says 'too fast'.

    Retries are per-URL and spaced by _host_gate, so a host that throttles a burst gets the chance
    to give its real answer instead of its rate limiter's. `attempts` rides out in the result so
    classify() can say how hard the checker tried rather than asserting a verdict it cannot support.
    """
    host = urlparse(url).hostname or ""
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    result: dict = {}
    for attempt in range(len(RETRY_BACKOFF) + 1):
        if attempt:
            time.sleep(RETRY_BACKOFF[attempt - 1])
        _host_gate(host)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return {"status": response.status, "final_url": response.geturl(),
                        "attempts": attempt + 1}
        except urllib.error.HTTPError as exc:
            result = {"status": exc.code, "final_url": exc.url or url, "attempts": attempt + 1}
        except Exception as exc:  # timeouts, TLS refusals, DNS -- indistinguishable from blocking
            result = {"status": None, "final_url": None, "attempts": attempt + 1,
                      "transport_error": type(exc).__name__}
        if result.get("status") not in RETRY_STATUSES:
            return result
        _host_pushed_back(host)   # from here on, this host alone is asked one at a time
    return result


def classify(url: str, result: dict) -> tuple[str, str]:
    """Return (verdict, explanation). Verdicts: ok, unverified, broken."""
    status = result.get("status")
    final = result.get("final_url")

    if status is None:
        return ("unverified",
                f"no response ({result.get('transport_error', 'unknown')}) — usually bot "
                f"mitigation or TLS fingerprinting; open it in a browser to confirm")
    tries = result.get("attempts", 1)
    if status in BOT_STATUSES:
        return ("unverified", f"HTTP {status} — bot challenge, not evidence the link is broken")
    # A 5xx that survives two backed-off retries is still not `broken`, and the rule above says
    # why: `broken` is reserved for what survives any plausible agent, and a browser never sends
    # the burst that produces one. It may be a real outage -- so it is a finding the author must
    # resolve by opening it, which is exactly what `unverified` means here.
    if status >= 500:
        return ("unverified",
                f"HTTP {status} after {tries} attempt(s) — a host rate-limiting this run and a "
                f"genuine outage look identical from here; open it in a browser to tell them apart")
    if status >= 400:
        return ("broken", f"HTTP {status}")

    requested, landed = urlparse(url), urlparse(final or url)
    if landed.hostname and requested.hostname and \
            landed.hostname.replace("www.", "") != requested.hostname.replace("www.", ""):
        return ("broken", f"redirected off-domain to {landed.hostname}")
    if any(marker in (landed.path or "").casefold() for marker in DEAD_END_MARKERS):
        # Deliberately NOT broken: the same URL returns 200 with no redirect under a browser
        # agent and lands here under a scripted one. Reporting it as broken would be a claim
        # about our user agent, not about the traveller's browser.
        return ("unverified",
                f"HTTP {status} but landed on {landed.path} — providers serve this to unfamiliar "
                f"clients, so it may be agent-dependent; open it in a browser and confirm the "
                f"page really shows what the button's label promises")

    lost = {k for k, _ in parse_qsl(requested.query)} - {k for k, _ in parse_qsl(landed.query)}
    if lost:
        # Only meaningful when the site actually served us; a challenge page drops params too.
        return ("unverified",
                f"HTTP {status} but dropped query parameter(s) {sorted(lost)} — prefill may not "
                f"survive; confirm in a browser before trusting the button's label")
    return ("ok", f"HTTP {status}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("html")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--json", help="Write the full report to this path")
    args = parser.parse_args()

    try:
        content = Path(args.html).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: could not read HTML: {exc}", file=sys.stderr)
        return 2

    links = extract_links(content)
    if not links:
        print("ERROR: no outbound booking/dining/map links found — is this a rendered trip page?",
              file=sys.stderr)
        return 2

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        results = list(pool.map(lambda item: probe(item[1], args.timeout), links))

    rows = []
    for (kind, url), result in zip(links, results):
        verdict, explanation = classify(url, result)
        rows.append({"kind": kind, "url": url, "verdict": verdict, "detail": explanation,
                     "final_url": result.get("final_url")})

    broken = [r for r in rows if r["verdict"] == "broken"]
    unverified = [r for r in rows if r["verdict"] == "unverified"]

    for row in sorted(rows, key=lambda r: (r["verdict"] != "broken", r["kind"])):
        print(f"{row['verdict'].upper():<10} {row['kind']:<7} {row['url']}")
        if row["verdict"] != "ok":
            print(f"           └─ {row['detail']}")

    print(f"\n{len(rows)} link(s): {len(rows) - len(broken) - len(unverified)} ok, "
          f"{len(unverified)} unverified, {len(broken)} broken.")
    if args.json:
        Path(args.json).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"report: {args.json}")

    if broken:
        print("\nFix or remove every BROKEN link before delivery. UNVERIFIED links are not "
              "failures, but the page must not claim more about them than was confirmed.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
