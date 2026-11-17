#!/usr/bin/env python3
"""Regression tests for verify_sources.py's HTTP-status handling.

Run: python3 test_verify_sources.py    (stdlib only; mocks the network)

These exist because the rate-limit special case shipped Reddit-only: the
branch that treats a throttled fetch as "unverified, not dead" checked
`is_reddit(url)` before checking the status code. Real dogfooding hit this
directly — heavy Hacker News fetching in one run got a later run's IP
rate-limited (HTTP 429), and every one of those live, real threads was
recorded as TIER_BROKEN ("unreachable or invalid") instead of TIER_SNIPPET_ONLY.

The invariant this defends: HTTP 429 means "you are being throttled," on any
domain, full stop. It is never evidence a source is dead, so it must never
be indistinguishable from a 404 or a DNS failure in the output.
"""

from __future__ import annotations

import http.server
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import safe_fetch
import verify_sources
from signal_scout_core import TIER_BROKEN, TIER_SNIPPET_ONLY, TIER_UNSUPPORTED, TIER_VERIFIED, tier_for_evidence

DATE_RE = r"^\d{4}-\d{2}-\d{2}$"

REAL_PAGE = (
    "Navigation Home About. " * 50
    + "We've been tracking inventory in a giant Google Sheet for two years "
    "and it takes about six hours every single week to reconcile."
    + " Related discussions. " * 50
)
EVIDENCE = (
    "We've been tracking inventory in a giant Google Sheet for two years "
    "and it takes about six hours every single week to reconcile."
)


NO_ARCHIVE = ("", "", "")


def run_verify(prospects: dict, wayback: tuple[str, str, str] = NO_ARCHIVE) -> dict:
    """Write `prospects` to a temp file, run main() with --annotate-out, return the annotated JSON.

    Always mocks fetch_wayback (default: no archived copy) so failure-path tests
    never hit archive.org for real."""
    with tempfile.TemporaryDirectory() as tmp:
        input_path = Path(tmp) / "in.json"
        output_path = Path(tmp) / "out.json"
        input_path.write_text(json.dumps(prospects), encoding="utf-8")
        argv = ["verify_sources.py", str(input_path), "--annotate-out", str(output_path)]
        with mock.patch.object(verify_sources, "fetch_wayback", return_value=wayback):
            with mock.patch.object(sys, "argv", argv):
                try:
                    verify_sources.main()
                except SystemExit:
                    pass
        return json.loads(output_path.read_text(encoding="utf-8"))


class TestRateLimitHandling(unittest.TestCase):
    def _one_prospect(self, url: str = "https://news.ycombinator.com/item?id=1") -> dict:
        return {"individuals": [{"name": "test", "source_url": url, "evidence": EVIDENCE}]}

    def test_429_on_non_reddit_domain_is_snippet_only_not_broken(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(429, "")):
            result = run_verify(self._one_prospect("https://news.ycombinator.com/item?id=1"))
        tier = result["individuals"][0]["verification_tier"]
        self.assertEqual(tier, TIER_SNIPPET_ONLY, "a 429 must never be reported as TIER_BROKEN")

    def test_429_on_reddit_is_also_snippet_only(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(429, "")):
            result = run_verify(self._one_prospect("https://www.reddit.com/r/test/comments/1"))
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_SNIPPET_ONLY)

    def test_403_on_reddit_is_snippet_only(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(403, "")):
            result = run_verify(self._one_prospect("https://www.reddit.com/r/test/comments/1"))
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_SNIPPET_ONLY)

    def test_403_on_non_reddit_domain_is_broken(self):
        """403 elsewhere is left as a genuine failure — it may mean truly
        forbidden/gated content, not just an anti-bot wall like Reddit's."""
        with mock.patch.object(verify_sources, "fetch_text", return_value=(403, "")):
            result = run_verify(self._one_prospect("https://example.com/some-page"))
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_BROKEN)

    def test_404_is_still_broken(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(404, "")):
            result = run_verify(self._one_prospect("https://news.ycombinator.com/item?id=1"))
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_BROKEN)

    def test_200_with_matching_evidence_still_verifies(self):
        """Guard against the fix accidentally swallowing the normal success path."""
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify(self._one_prospect("https://news.ycombinator.com/item?id=1"))
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_VERIFIED)


class TestVerifiedAtStamp(unittest.TestCase):
    def test_stamped_on_success(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify({"individuals": [{
                "name": "test", "source_url": "https://news.ycombinator.com/item?id=1", "evidence": EVIDENCE,
            }]})
        self.assertRegex(result["individuals"][0]["verified_at"], DATE_RE)

    def test_stamped_even_on_broken_source(self):
        """verified_at records when the check ran, not whether it passed —
        a broken source was still checked at a point in time."""
        with mock.patch.object(verify_sources, "fetch_text", return_value=(404, "")):
            result = run_verify({"individuals": [{
                "name": "test", "source_url": "https://example.com/dead", "evidence": EVIDENCE,
            }]})
        self.assertRegex(result["individuals"][0]["verified_at"], DATE_RE)


class TestOpenerGrounding(unittest.TestCase):
    def _prospect(self, opener: str) -> dict:
        return {"individuals": [{
            "name": "test",
            "source_url": "https://news.ycombinator.com/item?id=1",
            "evidence": EVIDENCE,
            "opener": opener,
        }]}

    def test_opener_grounded_in_evidence_is_not_flagged(self):
        grounded = "Saw you mentioned reconciling inventory in a Google Sheet every week — sounds brutal."
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify(self._prospect(grounded))
        self.assertNotIn("opener_grounding_note", result["individuals"][0])

    def test_opener_inventing_unrelated_specifics_is_flagged(self):
        invented = "Congrats on raising a Series B and hiring 10 engineers next quarter."
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify(self._prospect(invented))
        self.assertIn("opener_grounding_note", result["individuals"][0])

    def test_empty_opener_is_not_flagged(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify(self._prospect(""))
        self.assertNotIn("opener_grounding_note", result["individuals"][0])

    def test_flagged_opener_does_not_fail_the_run(self):
        """This is a softer signal than verification_tier — it must not trip
        the same exit(1) that broken/unsupported sources do."""
        invented = "Congrats on raising a Series B and hiring 10 engineers next quarter."
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            with tempfile.TemporaryDirectory() as tmp:
                input_path = Path(tmp) / "in.json"
                input_path.write_text(json.dumps(self._prospect(invented)), encoding="utf-8")
                argv = ["verify_sources.py", str(input_path)]
                with mock.patch.object(sys, "argv", argv):
                    try:
                        verify_sources.main()
                        exited_with = 0
                    except SystemExit as exc:
                        exited_with = exc.code
        self.assertEqual(exited_with, 0)


class TestWaybackFallback(unittest.TestCase):
    def _one_prospect(self, url: str = "https://example.com/gone") -> dict:
        return {"individuals": [{"name": "test", "source_url": url, "evidence": EVIDENCE}]}

    def test_dead_link_rescued_by_archive(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(404, "")):
            result = run_verify(
                self._one_prospect(),
                wayback=("https://web.archive.org/web/2026/https://example.com/gone", "20260101", REAL_PAGE),
            )
        prospect = result["individuals"][0]
        self.assertEqual(prospect["verification_tier"], TIER_VERIFIED)
        self.assertIn("Wayback", prospect["verification_note"])

    def test_dead_link_with_no_archive_stays_broken(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(404, "")):
            result = run_verify(self._one_prospect())
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_BROKEN)

    def test_thin_page_rescued_by_archive(self):
        """A JS-rendered page (too little text) should try the archive before
        settling for Unverified."""
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, "tiny spa shell")):
            result = run_verify(
                self._one_prospect("https://example.com/spa"),
                wayback=("https://web.archive.org/web/2026/https://example.com/spa", "20260201", REAL_PAGE),
            )
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_VERIFIED)

    def test_reddit_403_rescued_by_archive(self):
        """Reddit's bot wall is exactly what the archive route recovers from —
        an archived thread upgrades snippet-only to a real containment check."""
        with mock.patch.object(verify_sources, "fetch_text", return_value=(403, "")):
            result = run_verify(
                self._one_prospect("https://www.reddit.com/r/test/comments/1"),
                wayback=("https://web.archive.org/web/2026/reddit", "20260301", REAL_PAGE),
            )
        self.assertEqual(result["individuals"][0]["verification_tier"], TIER_VERIFIED)


class TestBattlecardVerification(unittest.TestCase):
    def _data(self, competitor_mentioned: str = "") -> dict:
        individual = {"name": "test", "source_url": "https://news.ycombinator.com/item?id=1", "evidence": EVIDENCE}
        if competitor_mentioned:
            individual["competitor_mentioned"] = competitor_mentioned
        return {
            "individuals": [individual],
            "competitive_context": {
                "top_competitors": ["SheetTracker"],
                "battlecard": [{
                    "competitor": "SheetTracker",
                    "claim": "Users complain reconciliation takes hours",
                    "evidence": EVIDENCE,
                    "source_url": "https://news.ycombinator.com/item?id=2",
                }],
            },
        }

    def test_battlecard_entry_gets_verified(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify(self._data())
        entry = result["competitive_context"]["battlecard"][0]
        self.assertEqual(entry["verification_tier"], TIER_VERIFIED)
        self.assertRegex(entry["verified_at"], DATE_RE)

    def test_corroborated_entry_counts_mentions(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify(self._data(competitor_mentioned="SheetTracker"))
        entry = result["competitive_context"]["battlecard"][0]
        self.assertEqual(entry["corroboration_count"], 1)
        self.assertNotIn("corroboration_note", entry)

    def test_single_source_entry_flagged(self):
        with mock.patch.object(verify_sources, "fetch_text", return_value=(200, REAL_PAGE)):
            result = run_verify(self._data())
        entry = result["competitive_context"]["battlecard"][0]
        self.assertEqual(entry["corroboration_count"], 0)
        self.assertIn("single-source", entry["corroboration_note"])

    def test_disqualified_battlecard_entry_does_not_fail_run(self):
        """A fabricated battlecard claim is dropped, not run-fatal — prospects
        alone decide the exit code."""
        data = self._data()
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "in.json"
            handoff_path = Path(tmp) / "handoff.json"
            input_path.write_text(json.dumps(data), encoding="utf-8")

            def fetch(url, timeout):
                if "item?id=2" in url:
                    return 200, "Completely unrelated page about gardening tips and tomato varieties. " * 20
                return 200, REAL_PAGE

            argv = ["verify_sources.py", str(input_path), "--handoff-out", str(handoff_path)]
            with mock.patch.object(verify_sources, "fetch_text", side_effect=fetch):
                with mock.patch.object(verify_sources, "fetch_wayback", return_value=NO_ARCHIVE):
                    with mock.patch.object(sys, "argv", argv):
                        try:
                            verify_sources.main()
                            exited_with = 0
                        except SystemExit as exc:
                            exited_with = exc.code
            handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
        self.assertEqual(exited_with, 0)
        self.assertNotIn("battlecard", handoff.get("competitive_context", {}))


class TestTextExtractor(unittest.TestCase):
    def test_meta_and_ldjson_harvested_from_spa_shell(self):
        html = (
            '<html><head>'
            f'<meta property="og:description" content="{EVIDENCE}">'
            '<script type="application/ld+json">{"@type":"Article","headline":"Inventory pain"}</script>'
            '<script>var app = "should not appear";</script>'
            '</head><body><div id="root"></div></body></html>'
        )
        parser = verify_sources._TextExtractor()
        parser.feed(html)
        text = parser.text()
        self.assertIn("giant Google Sheet", text)
        self.assertIn("Inventory pain", text)
        self.assertNotIn("should not appear", text)


SECRET_PAGE = "<p>INTERNAL-SECRET metadata token " + "filler words " * 40 + "</p>"
SECRET_EVIDENCE = "INTERNAL-SECRET metadata token"


class TestFetchGuard(unittest.TestCase):
    """source_url comes from an agent and can point anywhere, so the tier must
    not work as an oracle for what an internal address serves. Each "never
    contacted" check reads the server's hit counter: a refused fetch and one
    that reached a service and then failed look the same from the result."""

    def setUp(self):
        self.hits: Counter[str] = Counter()
        hits = self.hits

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.split("?")[0]
                hits[path] += 1
                if path.startswith("/redirect-to/"):
                    self.send_response(302)
                    self.send_header("Location", "http://" + path[len("/redirect-to/"):])
                    self.end_headers()
                    return
                if path == "/wayback":
                    body = json.dumps({"archived_snapshots": {"closest": {
                        "available": True, "timestamp": "20260801000000",
                        "url": f"http://archive.test:{self.server.server_port}/snapshot",
                    }}}).encode()
                else:
                    body = SECRET_PAGE.encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.addCleanup(self.httpd.server_close)
        self.addCleanup(self.httpd.shutdown)
        patcher = mock.patch.object(verify_sources, "POLICY", safe_fetch.FetchPolicy())
        patcher.start()
        self.addCleanup(patcher.stop)

    def fake_dns(self, mapping: dict[str, str | list[str]]):
        real = socket.getaddrinfo

        def resolver(host, port, *args, **kwargs):
            key = host.decode() if isinstance(host, bytes) else host
            if key in mapping:
                ips = mapping[key]
                ips = [ips] if isinstance(ips, str) else ips
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port)) for ip in ips]
            return real(host, port, *args, **kwargs)

        return mock.patch.object(socket, "getaddrinfo", resolver)

    def assert_refused(self, url: str):
        with mock.patch.object(verify_sources, "fetch_wayback") as wayback, \
                mock.patch.object(verify_sources, "fetch_archive_ph") as archive_ph:
            tier, note, quoted, topical = verify_sources.check_source(url, SECRET_EVIDENCE, 3)
        self.assertEqual(tier, TIER_BROKEN, url)
        self.assertEqual((quoted, topical), (0.0, 0.0), url)
        self.assertIn("Refused", note, url)
        wayback.assert_not_called()  # an internal URL is not sent to a third party
        archive_ph.assert_not_called()
        self.assertEqual(sum(self.hits.values()), 0, f"{url} reached the server")

    def test_control_the_fixture_is_reachable_when_allowed(self):
        policy = safe_fetch.FetchPolicy(allow_private=True)
        with mock.patch.object(verify_sources, "POLICY", policy):
            tier, _, _, _ = verify_sources.check_source(f"http://127.0.0.1:{self.port}/", SECRET_EVIDENCE, 3)
        self.assertEqual(tier, TIER_VERIFIED)

    def test_local_address_spellings_are_never_contacted(self):
        for host in (
            "127.0.0.1", "localhost", "localhost.", "LOCALHOST", "127.0.0.1.",
            "2130706433", "0x7f.1", "0x7f000001", "0177.0.0.1", "127.1",
            "[::1]", "[::ffff:127.0.0.1]", "[::ffff:7f00:1]", "[64:ff9b::7f00:1]",
            "[0:0:0:0:0:ffff:127.0.0.1]", "①②⑦.⓪.⓪.①", "１２７.０.０.１", "127.0.0.1%2f",
            "user@127.0.0.1", "example.com@127.0.0.1", "169.254.169.254", "metadata.google.internal",
        ):
            with self.subTest(host=host):
                self.assert_refused(f"http://{host}:{self.port}/latest/meta-data")

    def test_non_http_schemes_are_refused(self):
        for url in ("file:///etc/passwd", "ftp://example.com/x", "data:text/plain,hello"):
            with self.subTest(url=url), self.assertRaises(safe_fetch.BlockedURL):
                verify_sources.fetch_text(url, 3)

    def test_hostname_resolving_to_loopback_is_never_contacted(self):
        with self.fake_dns({"evil.test": "127.0.0.1"}):
            self.assert_refused(f"http://evil.test:{self.port}/")

    def test_hostname_with_any_private_record_is_refused(self):
        with self.fake_dns({"mixed.test": ["93.184.215.14", "127.0.0.1"]}):
            self.assert_refused(f"http://mixed.test:{self.port}/")

    def test_connection_goes_to_the_address_that_was_checked(self):
        # Rebinding: public for the check, loopback for a later lookup. There
        # must be no later lookup; the socket connects to the checked answer.
        answers = iter(["93.184.215.14", "127.0.0.1"])
        real = socket.getaddrinfo

        def rebinding(host, port, *args, **kwargs):
            if host == "rebind.test":
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (next(answers), port))]
            return real(host, port, *args, **kwargs)

        connected = []

        def connect(_sock, sockaddr):
            connected.append(sockaddr[0])
            raise OSError("no network in tests")

        with mock.patch.object(socket, "getaddrinfo", rebinding), mock.patch.object(socket.socket, "connect", connect):
            status, text = verify_sources.fetch_text(f"http://rebind.test:{self.port}/", 3)
        self.assertEqual((status, text), (None, ""))
        self.assertEqual(connected, ["93.184.215.14"])

    def test_redirect_to_a_local_address_is_not_followed(self):
        policy = safe_fetch.FetchPolicy(allow_hosts=frozenset({"public.test"}))
        url = f"http://public.test:{self.port}/redirect-to/127.0.0.1:{self.port}/secret"
        with self.fake_dns({"public.test": "127.0.0.1"}), mock.patch.object(verify_sources, "POLICY", policy), \
                mock.patch.object(verify_sources, "fetch_wayback") as wayback:
            tier, note, _, _ = verify_sources.check_source(url, SECRET_EVIDENCE, 3)
        self.assertEqual(tier, TIER_BROKEN)
        self.assertIn("Refused", note)
        wayback.assert_not_called()
        self.assertEqual(self.hits["/secret"], 0)

    def test_proxy_mode_still_refuses_local_targets(self):
        policy = safe_fetch.FetchPolicy(use_env_proxy=True)
        with mock.patch.object(verify_sources, "POLICY", policy):
            self.assert_refused(f"http://127.0.0.1:{self.port}/")
            with self.fake_dns({"evil.test": "127.0.0.1"}):
                self.assert_refused(f"http://evil.test:{self.port}/")

    def test_wayback_fallback_still_works_through_the_guard(self):
        policy = safe_fetch.FetchPolicy(allow_hosts=frozenset({"archive.test"}))
        api = f"http://archive.test:{self.port}/wayback?url="
        with self.fake_dns({"archive.test": "127.0.0.1"}), mock.patch.object(verify_sources, "POLICY", policy), \
                mock.patch.object(verify_sources, "WAYBACK_API", api):
            snapshot_url, date_found, text = verify_sources.fetch_wayback("https://example.com/gone", 3)
        self.assertEqual(snapshot_url, f"http://archive.test:{self.port}/snapshot")
        self.assertEqual(date_found, "20260801")
        self.assertIn(SECRET_EVIDENCE, text)

    def test_wayback_answer_cannot_steer_the_fetcher_off_the_archive(self):
        # elsewhere.test is exempt from the address check, so without a host
        # check on the answer this snapshot URL would be fetched.
        policy = safe_fetch.FetchPolicy(allow_hosts=frozenset({"archive.test", "elsewhere.test"}))
        api = f"http://archive.test:{self.port}/wayback?url="
        answer = {"archived_snapshots": {"closest": {
            "available": True, "timestamp": "20260801000000", "url": f"http://elsewhere.test:{self.port}/internal"}}}
        with self.fake_dns({"archive.test": "127.0.0.1", "elsewhere.test": "127.0.0.1"}), \
                mock.patch.object(verify_sources, "POLICY", policy), mock.patch.object(verify_sources, "WAYBACK_API", api), \
                mock.patch.object(verify_sources.json, "load", return_value=answer):
            result = verify_sources.fetch_wayback("https://example.com/gone", 3)
        self.assertEqual(result, ("", "", ""))
        self.assertEqual(self.hits["/internal"], 0)

    def test_allow_private_addresses_flag_reaches_a_local_source(self):
        data = {"individuals": [{"name": "t", "source_url": f"http://127.0.0.1:{self.port}/", "evidence": SECRET_EVIDENCE}]}
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "in.json", Path(tmp) / "out.json"
            src.write_text(json.dumps(data), encoding="utf-8")
            argv = ["verify_sources.py", str(src), "--annotate-out", str(out), "--allow-private-addresses"]
            with mock.patch.object(sys, "argv", argv):
                verify_sources.main()
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["individuals"][0]["verification_tier"], TIER_VERIFIED)


class TestProxyIsOptIn(unittest.TestCase):
    def test_a_proxy_in_the_environment_keeps_the_connect_time_check(self):
        # TestFetchGuard replaces POLICY, so read the import-time default in a fresh process.
        env = dict(os.environ, HTTP_PROXY="http://127.0.0.1:9", HTTPS_PROXY="http://127.0.0.1:9")
        out = subprocess.run(
            [sys.executable, "-c", "import verify_sources; print(verify_sources.POLICY.use_env_proxy)"],
            cwd=Path(__file__).parent, env=env, capture_output=True, text=True, check=True,
        ).stdout
        self.assertEqual(out.strip(), "False")


class TestVerbatimQuotesAreNotAccused(unittest.TestCase):
    """A quote copied from the page must never tier as Not on page because of
    markup, typography or script."""

    PAD = "<p>" + "Bruno is an open source API client that stores collections as plain files on disk. " * 4 + "</p>"

    def tier(self, evidence: str, html: str) -> str:
        parser = verify_sources._TextExtractor()
        parser.feed(html)
        return tier_for_evidence(evidence, parser.text())[0]

    def test_adjacent_blocks_without_whitespace(self):
        html = "<h1>Pricing</h1><p>Teams pay per seat</p><ul><li>Offline first</li><li>Git sync</li></ul>" + self.PAD
        self.assertEqual(self.tier("Offline first", html), TIER_VERIFIED)
        self.assertEqual(self.tier("Teams pay per seat", html), TIER_VERIFIED)

    def test_inline_markup_does_not_split_a_word(self):
        parser = verify_sources._TextExtractor()
        parser.feed("<p>un<b>believ</b>able <a href='#'>link</a>s</p>")
        self.assertEqual(parser.text(), "unbelievable links")

    def test_curly_apostrophe_on_page_straight_in_evidence(self):
        html = ("<p>We switched because Bruno\u2019s offline mode works and Postman\u2019s cloud sync kept "
                "failing for our team every single week.</p>" + self.PAD)
        evidence = "We switched because Bruno's offline mode works and Postman's cloud sync kept failing"
        self.assertEqual(self.tier(evidence, html), TIER_VERIFIED)

    def test_non_latin_verbatim_quotes(self):
        hebrew = ("\u05d4\u05db\u05dc\u05d9 \u05d4\u05d6\u05d4 \u05d0\u05d9\u05d8\u05d9 \u05de\u05d3\u05d9 "
                  "\u05d5\u05d0\u05e0\u05d7\u05e0\u05d5 \u05de\u05d7\u05e4\u05e9\u05d9\u05dd \u05d7\u05dc\u05d5\u05e4\u05d4")
        japanese = "\u3053\u306e\u30c4\u30fc\u30eb\u306f\u9045\u3059\u304e\u308b\u306e\u3067\u4ee3\u308f\u308a\u3092\u63a2\u3057\u3066\u3044\u307e\u3059"
        for quote in (hebrew, japanese):
            page = "<p>" + ("\u524d\u7f6e " + quote + "\u3002 ") * 12 + "</p>"
            self.assertEqual(self.tier(quote, page), TIER_VERIFIED, quote)

    def test_non_latin_claim_absent_from_page_is_still_caught(self):
        japanese = "\u3053\u306e\u30c4\u30fc\u30eb\u306f\u9045\u3059\u304e\u308b\u306e\u3067\u4ee3\u308f\u308a\u3092\u63a2\u3057\u3066\u3044\u307e\u3059"
        self.assertEqual(self.tier(japanese, self.PAD), TIER_UNSUPPORTED)

    def test_accented_capitalized_word_on_page(self):
        html = "<p>Our team at Caf\u00e9 Roma moved every collection to Bruno last spring.</p>" + self.PAD
        self.assertEqual(self.tier("Our team at Caf\u00e9 Roma moved every collection to Bruno", html), TIER_VERIFIED)


if __name__ == "__main__":
    unittest.main(verbosity=2)
