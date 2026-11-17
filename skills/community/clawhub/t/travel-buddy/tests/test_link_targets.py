#!/usr/bin/env python3
"""Regression tests for scripts/check_link_targets.py.

Offline by design. The whole lesson behind this checker is that a live probe's verdict depends
on the user agent it was sent with, so a test that made real requests would be asserting against
whatever a provider felt like serving that minute.

The case that matters most is the `unsupported` landing path. An earlier version called that
`broken`, on the strength of two curl runs that had accidentally used different agents. The same
Google Flights URL returns 200 with no redirect under a Chrome agent. Reporting it as broken
accused a working link, so the rule now returns `unverified` and the test pins that down.

Run:  python tests/test_link_targets.py
      python -m pytest tests/test_link_targets.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_link_targets import classify, extract_links  # noqa: E402


def main() -> int:
    failures: list[str] = []

    def check(label: str, got: str, want: str) -> None:
        if got != want:
            failures.append(f"{label}: expected {want!r}, got {got!r}")

    def verdict(url: str, status, final=None, error=None) -> str:
        result = {"status": status, "final_url": final if final is not None else url}
        if error:
            result["transport_error"] = error
        return classify(url, result)[0]

    # Hard failures survive any plausible user agent.
    check("404 is broken", verdict("https://a.com/x", 404), "broken")
    check("410 is broken", verdict("https://a.com/x", 410), "broken")
    # 503 USED to be asserted broken here, and that assertion was wrong in the direction this
    # whole file exists to prevent. A host that rate-limits a burst answers 200 to the first
    # request and 503 to the fifth, so a single 503 is a statement about the burst, not the link.
    # Measured on a real delivered page, 2026-09-12: eight dining cards pointed at one aggregator,
    # requests 1-4 returned 200 and 5-8 returned 503, and the page reported EIGHT broken links
    # that open fine in a browser -- with two runs of the same file disagreeing (42 ok/0 broken,
    # then 34 ok/8 broken). The author rewrote fourteen working URLs because of it.
    #
    # `broken` is reserved for what survives any plausible agent, and a browser never sends that
    # burst. So 5xx is now `unverified`: a finding the author must resolve by opening it, which is
    # the honest verdict when a rate limiter and an outage are indistinguishable from here.
    check("5xx is unverified, not broken", verdict("https://a.com/x", 503), "unverified")
    check("500 is unverified too", verdict("https://a.com/x", 500), "unverified")
    check("4xx is still broken", verdict("https://a.com/x", 404), "broken")
    check("off-domain redirect is broken",
          verdict("https://a.com/x", 200, "https://elsewhere.com/x"), "broken")

    # Challenge codes are the majority of real travel links; failing them switches the gate off.
    for code in (202, 403, 405, 429):
        check(f"HTTP {code} is unverified", verdict("https://a.com/x", code), "unverified")
    check("refused connection is unverified",
          verdict("https://a.com/x", None, None, "URLError"), "unverified")

    # THE regression: an "unsupported" landing must never be reported as broken, because the
    # same URL returns 200 unredirected under a browser agent.
    check("unsupported landing is unverified, not broken",
          verdict("https://www.google.com/travel/flights?q=x", 200,
                  "https://www.google.com/travel/flights/unsupported?q=x"), "unverified")
    check("error landing is unverified",
          verdict("https://a.com/x", 200, "https://a.com/error"), "unverified")
    check("404 landing path is unverified",
          verdict("https://a.com/x", 200, "https://a.com/404"), "unverified")

    # Dropped prefill is a real concern but not proof of breakage.
    check("dropped query params are unverified",
          verdict("https://b.com/s?checkin=1&ss=x", 200, "https://b.com/s"), "unverified")
    check("kept query params are ok",
          verdict("https://b.com/s?checkin=1", 200, "https://b.com/s?checkin=1"), "ok")

    # www is not a different host.
    check("www variance is not off-domain",
          verdict("https://a.com/x", 200, "https://www.a.com/x"), "ok")
    check("clean 200 is ok", verdict("https://a.com/x", 200), "ok")

    # Extraction: the three button classes, deduplicated, https only.
    html = (
        '<a class="booking-link" data-booking-type="flight" href="https://a.com/1">x</a>'
        '<a class="booking-link" data-booking-type="hotel" href="https://a.com/2">x</a>'
        '<a class="dining-link" href="https://a.com/3">x</a>'
        '<a class="map-link segment-map-link" href="https://a.com/4">x</a>'
        '<a class="booking-link" data-booking-type="flight" href="https://a.com/1">dup</a>'
        '<a class="page-nav-link" href="https://a.com/5">not a button</a>'
        '<a class="booking-link" data-booking-type="ticket" href="http://a.com/6">insecure</a>'
    )
    links = extract_links(html)
    kinds = sorted(kind for kind, _ in links)
    check("extracts exactly the four unique https buttons", str(len(links)), "4")
    check("kinds are read from data-booking-type or class",
          ",".join(kinds), "dining,flight,hotel,map")


    # The retry and the throttle, which are what make the verdict above trustworthy rather than
    # merely softer. Tested against a fake opener so the assertions need no network and cannot
    # flake on somebody else's rate limiter.
    import check_link_targets as CLT

    calls: list[str] = []

    class _FakeError(Exception):
        pass

    def fake_urlopen(request, timeout=None):
        url = request.full_url
        calls.append(url)
        import urllib.error
        if "always503" in url:
            raise urllib.error.HTTPError(url, 503, "Service Unavailable", None, None)
        if "flaky" in url and len([c for c in calls if "flaky" in c]) < 3:
            raise urllib.error.HTTPError(url, 503, "Service Unavailable", None, None)
        class _R:
            status = 200
            def geturl(self_inner): return url
            def __enter__(self_inner): return self_inner
            def __exit__(self_inner, *a): return False
        return _R()

    real_urlopen = CLT.urllib.request.urlopen
    real_sleep = CLT.time.sleep
    CLT.urllib.request.urlopen = fake_urlopen
    CLT.time.sleep = lambda _s: None          # the backoff is real; waiting for it in a test is not
    try:
        CLT._HOST_SLOW.clear()
        calls.clear()
        result = CLT.probe("https://always503.example/x", 5)
        check("a 5xx is retried rather than believed once",
              str(result.get("attempts")), str(len(CLT.RETRY_BACKOFF) + 1))
        check("the host that pushed back is marked for throttling",
              str("always503.example" in CLT._HOST_SLOW), "True")

        CLT._HOST_SLOW.clear()
        calls.clear()
        recovered = CLT.probe("https://flaky.example/x", 5)
        check("a host that recovers on retry is reported as it finally answered",
              str(recovered.get("status")), "200")
        check("and it took more than one attempt", str(recovered.get("attempts") > 1), "True")

        # A host that never pushed back must never be slowed: that cost 34.2 s on a real page
        # whose 31 map links were serialised for nothing, and a slow gate is a skipped gate.
        #
        # Asserted on whether a WAIT WAS REQUESTED, not on elapsed time. The first version of this
        # case measured the clock while `time.sleep` was still stubbed out two lines above, so it
        # could not tell a throttled host from an unthrottled one and survived a mutation that
        # throttled everything.
        slept: list[float] = []
        CLT.time.sleep = lambda seconds: slept.append(seconds)
        CLT._HOST_SLOW.clear()
        CLT._host_gate("never-pushed-back.example")
        CLT._host_gate("never-pushed-back.example")
        check("an unthrottled host is never made to wait", str(slept), "[]")

        slept.clear()
        CLT._host_pushed_back("pushed-back.example")
        CLT._host_gate("pushed-back.example")
        CLT._host_gate("pushed-back.example")
        check("a host that pushed back IS made to wait", str(len(slept) >= 1), "True")
    finally:
        CLT.urllib.request.urlopen = real_urlopen
        CLT.time.sleep = real_sleep
        CLT._HOST_SLOW.clear()

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("OK: link-target verdicts hold, and an agent-dependent landing is never called broken.")
    return 0


def test_link_target_verdicts() -> None:
    """Pytest surface. This file is a main()-style script, so before this function existed
    `python -m pytest tests/` collected zero tests and printed "no tests ran" -- which a
    contributor or a CI job reads as green while the suite is in fact never executed. One
    assertion per file keeps both entry points honest without restructuring the checks above."""
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
