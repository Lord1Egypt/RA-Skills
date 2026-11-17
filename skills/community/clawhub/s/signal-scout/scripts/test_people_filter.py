#!/usr/bin/env python3
"""No-people mode: prove no person data leaks into filtered output.

Every leak test is a pair. The fixture is first checked to CONTAIN every
planted person string (negative control), then the filtered output is checked
to contain NONE of them. Covers people_filter directly, finalize.py end to end
(JSON, handoff, HTML, CSV), verification-before-redaction ordering, and the
MCP server's _finish_run with stubbed anthropic/mcp modules. No network.
"""

from __future__ import annotations

import contextlib
import csv
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import finalize
import verify_sources
from people_filter import (
    NAME_PLACEHOLDER,
    collect_person_names,
    drop_people,
    is_personal_url,
    redact_people,
    redact_text,
    strip_people,
)
from signal_scout_core import TIER_VERIFIED

SCRIPTS = Path(__file__).resolve().parent
MCP_SERVER = SCRIPTS.parents[2] / "mcp-server"
REAL_RUN = subprocess.run

THREAD_URL = "https://www.reddit.com/r/devops/comments/abc123/flaky_ci_again/"
ISSUE_URL = "https://github.com/acme/ci-runner/issues/42"
COMPANY_URL = "https://acme.com/partners"

# Every string here identifies a person and must never reach filtered output.
PLANTED = (
    "Jane Doe",
    "janedoe",
    "devguy42",
    "linkedin.com/in/",
    "jane.doe@gmail.com",
    "x.com/janedoe",
    "x.com/someone",
    "bobbuilder",
    "linkedin.com/posts/",
    "mobile.twitter.com",
    "m.facebook.com",
)

SEGMENT_EVIDENCE = (
    "Flaky CI again, third time this week. @janedoe said the same thing and u/devguy42 "
    "had to rerun every pipeline by hand."
)


def individual() -> dict:
    dims = {"pain_strength": 4, "product_fit": 4, "timing": 4, "reachability": 3, "evidence_quality": 3}
    return {
        "name": "Jane Doe (@janedoe)", "stage": "High intent", "score": 74,
        "pain_signal": "CI keeps failing", "evidence": "my CI is broken again",
        "why_fit": "w", "why_now": "n", "source_title": "post",
        "source_url": "https://x.com/janedoe/status/123", "source_type": "Social post",
        "signal_date": "2026-09-01", "suggested_channel": "Reply on X",
        "opener": "Hi Jane, saw your CI post", "caution": "c", "dimensions": dims,
    }


def segment(name: str, url: str, evidence: str) -> dict:
    return {
        "name": name, "stage": "Problem aware", "score": 75,
        "pain_signal": "flaky CI", "evidence": evidence,
        "why_fit": "Same pain Jane Doe described", "why_now": "n",
        "source_title": "thread", "source_url": url, "source_type": "Forum",
        "signal_date": "2026-09-02", "content_angle": "Write about flaky CI",
        "proof_points": ["@bobbuilder's benchmark, quoted by Sam Lee", "see https://www.linkedin.com/in/janedoe"],
        "caution": "c",
        "dimensions": {"pain_strength": 4, "product_fit": 4, "timing": 3, "evidence_quality": 4},
    }


def company() -> dict:
    return {
        "name": "Acme", "domain": "acme.com", "role": "Integration/distribution partner",
        "stage": "Trigger present", "score": 70, "pain_signal": "p",
        "evidence": "Acme launched a partner program", "why_fit": "w", "why_now": "n",
        "source_title": "Partners", "source_url": COMPANY_URL, "source_type": "Company page",
        "signal_date": "2026-09-03", "execution_path": "Self-serve program",
        "contact_path": "partners@acme.com or ask jane.doe@gmail.com",
        "bd_angle": "b", "what_to_propose": "w", "caution": "c",
        "dimensions": {"strategic_fit": 4, "timing": 3, "execution_ease": 3, "evidence_quality": 4},
    }


def fixture() -> dict:
    return {
        "title": "CI Tool", "product": "P", "product_url": "https://ci.example",
        "target_customer": "devops leads", "search_scope": "s", "generated_at": "2026-10-06",
        "verdict": "Strong signal from Jane Doe and others",
        "search_queries_used": ["flaky ci", "from:janedoe ci"],
        "sources_consulted": [
            THREAD_URL, "https://www.linkedin.com/in/janedoe", "https://x.com/janedoe",
            "https://www.linkedin.com/posts/janedoe_ci-activity-7100",
            "https://mobile.twitter.com/janedoe/status/5", "https://m.facebook.com/janedoe",
        ],
        "individuals": [individual()],
        "segments": [
            segment("Teams with flaky CI", THREAD_URL, SEGMENT_EVIDENCE),
            segment("Runner users", "https://x.com/someone/status/9", "runner pain"),
        ],
        "companies": [company()],
        "patterns": [{"title": "Flaky CI", "count": 2, "insight": "Jane Doe and @janedoe-style posts"}],
        "outreach_plan": {"angle": "a", "first_step": "Reply to Jane Doe", "personalization_notes": "DM @janedoe"},
        "executive_summary": {"overview": "o", "key_findings": ["Jane Doe is the hottest lead"]},
        "competitive_context": {"battlecard": [
            {"competitor": "OldCI", "claim": "slow", "evidence": "per @janedoe it is slow",
             "source_url": ISSUE_URL, "counter_angle": "fast"},
            {"competitor": "OtherCI", "claim": "c", "evidence": "e",
             "source_url": "https://www.linkedin.com/in/bob", "counter_angle": "x"},
        ]},
        "limits": ["Classified Jane Doe as Individual, not Company"],
    }


def assert_no_leak(test: unittest.TestCase, text: str, where: str) -> None:
    lowered = text.lower()
    for needle in PLANTED:
        test.assertNotIn(needle.lower(), lowered, f"{needle!r} leaked into {where}")


class NegativeControl(unittest.TestCase):
    def test_fixture_contains_every_planted_string(self):
        raw = json.dumps(fixture()).lower()
        for needle in PLANTED:
            self.assertIn(needle.lower(), raw, f"fixture is missing {needle!r}; the leak tests would prove nothing")


class PersonalUrlTests(unittest.TestCase):
    def test_classification(self):
        personal = [
            "https://www.linkedin.com/in/janedoe", "https://x.com/janedoe/status/1", "https://twitter.com/janedoe",
            "https://www.reddit.com/user/devguy42", "https://reddit.com/u/devguy42",
            "https://news.ycombinator.com/user?id=pg", "https://github.com/janedoe",
            "https://bsky.app/profile/jane.bsky.social", "https://medium.com/@jane/post",
            "https://mastodon.social/@jane",
            "https://www.linkedin.com/posts/janedoe_ci-activity-7100",
            "https://mobile.twitter.com/janedoe/status/5", "https://m.facebook.com/janedoe",
            "https://old.reddit.com/user/devguy42",
        ]
        public = [
            THREAD_URL, ISSUE_URL, COMPANY_URL, "https://github.com/acme/repo",
            "https://www.linkedin.com/company/acme", "https://news.ycombinator.com/item?id=1",
            "https://x.com/search?q=ci", "https://notreddit.com/user/x", "https://notx.com/janedoe",
            "https://notlinkedin.com/in/janedoe",
        ]
        for url in personal:
            self.assertTrue(is_personal_url(url), url)
        for url in public:
            self.assertFalse(is_personal_url(url), url)


class StripPeopleTests(unittest.TestCase):
    def test_no_person_data_leaks(self):
        out, stats = strip_people(fixture())
        assert_no_leak(self, json.dumps(out), "strip_people output")
        self.assertNotIn("individuals", out)
        self.assertIs(out["people"], False)
        self.assertEqual(stats["individuals_removed"], 1)
        # Segment on x.com/someone and battlecard on a LinkedIn profile are dropped whole.
        self.assertEqual(stats["dropped_for_personal_source"], 2)

    def test_keeps_non_person_content(self):
        out, _ = strip_people(fixture())
        self.assertEqual([s["name"] for s in out["segments"]], ["Teams with flaky CI"])
        self.assertEqual(out["segments"][0]["source_url"], THREAD_URL)
        self.assertIn(THREAD_URL, out["sources_consulted"])
        self.assertEqual(len(out["sources_consulted"]), 1)
        self.assertIn("partners@acme.com", out["companies"][0]["contact_path"])
        self.assertEqual(out["companies"][0]["domain"], "acme.com")
        self.assertEqual(out["competitive_context"]["battlecard"][0]["source_url"], ISSUE_URL)
        self.assertIn(NAME_PLACEHOLDER, out["segments"][0]["evidence"])
        self.assertTrue(any(str(x).startswith("No-people mode:") for x in out["limits"]))

    def test_idempotent_keeps_original_note(self):
        once, _ = strip_people(fixture())
        twice, stats = strip_people(once)
        self.assertEqual(once, twice)
        self.assertEqual(stats["redactions"], 0)

    def test_input_not_mutated(self):
        data = fixture()
        strip_people(data)
        self.assertEqual(data, fixture())


class VerifyThenRedactOrdering(unittest.TestCase):
    """A segment quote containing a handle must still verify: drop first,
    verify the unredacted quote, redact afterwards."""

    def test_handle_in_quote_verifies_then_is_redacted(self):
        public, stats = drop_people(fixture())
        filler = " Unrelated discussion about build caches, runners, and deploy queues." * 12
        pages = {
            THREAD_URL: "Some header." + filler + " " + SEGMENT_EVIDENCE + filler,
            COMPANY_URL: "Acme launched a partner program for integrations." + filler,
            ISSUE_URL: "per @janedoe it is slow, and other users agree." + filler,
        }

        def fetch_text(url, timeout):
            return (200, pages[url]) if url in pages else (None, "")

        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "analysis.json"
            handoff = Path(tmp) / "handoff.json"
            src.write_text(json.dumps(public), encoding="utf-8")
            argv = ["verify_sources.py", str(src), "--annotate-out", str(src), "--handoff-out", str(handoff)]
            with mock.patch.object(verify_sources, "fetch_text", fetch_text), \
                    mock.patch.object(verify_sources, "fetch_wayback", lambda u, t: ("", "", "")), \
                    mock.patch.object(verify_sources, "fetch_archive_ph", lambda u, t: ("", "")), \
                    mock.patch.object(sys, "argv", argv), \
                    contextlib.redirect_stdout(io.StringIO()):
                try:
                    verify_sources.main()
                except SystemExit as exc:
                    self.assertIn(exc.code, (0, None))
            annotated = json.loads(src.read_text(encoding="utf-8"))
            self.assertEqual(annotated["segments"][0]["verification_tier"], TIER_VERIFIED)

            final = finalize.finish_people_filter(src, annotated, stats, handoff)
            self.assertEqual(final["segments"][0]["verification_tier"], TIER_VERIFIED)
            assert_no_leak(self, src.read_text(encoding="utf-8"), "annotated JSON")
            assert_no_leak(self, handoff.read_text(encoding="utf-8"), "handoff.json")


class FinalizeEndToEnd(unittest.TestCase):
    def run_finalize(self, tmp: Path, *flags: str, data: dict | None = None) -> tuple[Path, str]:
        src = tmp / "analysis-2026-10-06.json"
        src.write_text(json.dumps(data or fixture()), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "finalize.py"), str(src), "--skip-verify", *flags],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return src, result.stdout

    def test_no_people_flag_outputs_are_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src, stdout = self.run_finalize(tmp_path, "--no-people")
            public = tmp_path / "public"
            outputs = {
                "public JSON": public / src.name,
                "HTML report": public / "signal-scout-report.html",
                "CSV": public / "prospects.csv",
            }
            for where, path in outputs.items():
                self.assertTrue(path.exists(), where)
                assert_no_leak(self, path.read_text(encoding="utf-8"), where)
            assert_no_leak(self, stdout, "finalize stdout")
            # Private draft untouched; nothing written beside it.
            self.assertEqual(json.loads(src.read_text(encoding="utf-8")), fixture())
            self.assertFalse((tmp_path / "prospects.csv").exists())
            with (public / "prospects.csv").open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual({r["type"] for r in rows}, {"segment", "company"})
            self.assertEqual([r["domain"] for r in rows if r["type"] == "company"], ["acme.com"])

    def test_people_false_in_json_enables_filter(self):
        data = fixture()
        data["people"] = False
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src, _ = self.run_finalize(tmp_path, data=data)
            assert_no_leak(self, (tmp_path / "public" / "signal-scout-report.html").read_text(encoding="utf-8"), "HTML")

    def test_default_mode_keeps_individuals(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.run_finalize(tmp_path)
            self.assertIn("Jane Doe", (tmp_path / "signal-scout-report.html").read_text(encoding="utf-8"))
            self.assertFalse((tmp_path / "public").exists())

    def test_only_people_fails_clearly(self):
        data = fixture()
        for key in ("segments", "companies"):
            data.pop(key)
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "analysis.json"
            src.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "finalize.py"), str(src), "--no-people", "--validate-only"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("no Segments or Companies left", result.stdout)


class FinalizeWithVerification(unittest.TestCase):
    """finalize.py end to end with verification ON, against a local HTTP server."""

    def test_verified_public_outputs_do_not_leak(self):
        import http.server
        import threading

        filler = " Unrelated discussion about build caches, runners, and deploy queues." * 12
        pages = {
            "/thread": "Some header." + filler + " " + SEGMENT_EVIDENCE + filler,
            "/partners": "Acme launched a partner program for integrations." + filler,
            "/issue": "per @janedoe it is slow, and other users agree." + filler,
        }

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                body = pages.get(self.path.split("?")[0])
                if body is None:
                    self.send_response(404)
                    self.end_headers()
                    return
                payload = f"<html><body><p>{body}</p></body></html>".encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args):
                pass

        httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{httpd.server_address[1]}"
        try:
            data = fixture()
            data["segments"][0]["source_url"] = base + "/thread"
            data["companies"][0]["source_url"] = base + "/partners"
            data["competitive_context"]["battlecard"][0]["source_url"] = base + "/issue"
            data["sources_consulted"][0] = base + "/thread"
            with tempfile.TemporaryDirectory() as tmp:
                src = Path(tmp) / "analysis-2026-10-06.json"
                src.write_text(json.dumps(data), encoding="utf-8")
                env = dict(os.environ, NO_PROXY="127.0.0.1", no_proxy="127.0.0.1")
                for key in ("http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"):
                    env.pop(key, None)
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / "finalize.py"), str(src), "--no-people", "--timeout", "5", "--allow-private-addresses"],
                    capture_output=True, text=True, env=env, timeout=120,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                assert_no_leak(self, result.stdout, "finalize stdout")
                public = Path(tmp) / "public"
                for name in (src.name, "handoff.json", "signal-scout-report.html", "prospects.csv"):
                    assert_no_leak(self, (public / name).read_text(encoding="utf-8"), name)
                verified = json.loads((public / src.name).read_text(encoding="utf-8"))
                self.assertEqual(verified["segments"][0]["verification_tier"], TIER_VERIFIED)
        finally:
            httpd.shutdown()


class GenerateReportDirect(unittest.TestCase):
    def test_people_false_never_renders_a_person(self):
        data = fixture()
        data["people"] = False
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "in.json", Path(tmp) / "out.html"
            src.write_text(json.dumps(data), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPTS / "generate_report.py"), str(src), str(out), "--no-history"],
                           check=True, capture_output=True)
            assert_no_leak(self, out.read_text(encoding="utf-8"), "generate_report HTML")


def load_server():
    """Import mcp-server/server.py with anthropic and mcp stubbed (CI installs neither)."""
    stubs = {}
    if "anthropic" not in sys.modules:
        anthropic = types.ModuleType("anthropic")
        anthropic.Anthropic = object
        stubs["anthropic"] = anthropic
    fastmcp = types.ModuleType("mcp.server.fastmcp")

    class FastMCP:
        def __init__(self, *args, **kwargs):
            pass

        def tool(self):
            return lambda fn: fn

        def run(self, **kwargs):
            pass

    fastmcp.FastMCP = FastMCP
    stubs.update({
        "mcp": types.ModuleType("mcp"),
        "mcp.server": types.ModuleType("mcp.server"),
        "mcp.server.fastmcp": fastmcp,
    })
    sys.path.insert(0, str(MCP_SERVER))
    try:
        with mock.patch.dict(sys.modules, stubs):
            sys.modules.pop("server", None)
            import server  # noqa: PLC0415
            return server
    finally:
        sys.path.remove(str(MCP_SERVER))


class McpServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = load_server()

    def fake_run(self, cmd, **kwargs):
        """verify_sources is replaced (no network): it annotates and writes a
        handoff from the unredacted text, and prints names, as the real one does.
        generate_report runs for real."""
        if cmd[1].endswith("verify_sources.py"):
            src = Path(cmd[2])
            data = json.loads(src.read_text(encoding="utf-8"))
            for kind in ("individuals", "segments", "companies"):
                for item in data.get(kind) or []:
                    item["verification_tier"] = TIER_VERIFIED
            Path(cmd[cmd.index("--annotate-out") + 1]).write_text(json.dumps(data), encoding="utf-8")
            Path(cmd[cmd.index("--handoff-out") + 1]).write_text(json.dumps(data), encoding="utf-8")
            names = [i["name"] for k in ("individuals", "segments") for i in data.get(k) or []]
            stdout = "Verified: " + ", ".join(names) + " | evidence: " + data["segments"][0]["evidence"]
            return subprocess.CompletedProcess(cmd, 0, stdout=stdout, stderr="")
        return REAL_RUN(cmd, **kwargs)

    def finish(self, tmp: str, people: bool) -> tuple[dict, str]:
        with mock.patch.object(self.server, "OUTPUT_DIR", Path(tmp)), \
                mock.patch.object(self.server.subprocess, "run", self.fake_run), \
                mock.patch.object(self.server, "record_call", lambda **kw: 0.0):
            result = self.server._finish_run(
                fixture(), None, product_url="https://ci.example", depth="standard", focus="all", people=people,
            )
        written = "".join(p.read_text(encoding="utf-8") for p in Path(tmp).rglob("*") if p.is_file())
        return result, written

    def test_default_is_no_people(self):
        import inspect
        for tool in (self.server.classify_and_score, self.server.find_first_customers):
            self.assertIs(inspect.signature(tool).parameters["people"].default, False)

    def test_no_people_leaks_nowhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, written = self.finish(tmp, people=False)
        self.assertEqual(result["individuals"], 0)
        self.assertIs(result["people"], False)
        assert_no_leak(self, json.dumps(result), "tool result")
        assert_no_leak(self, written, "files the server wrote")

    def test_people_true_keeps_individuals(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, written = self.finish(tmp, people=True)
        self.assertEqual(result["individuals"], 1)
        self.assertIn("Jane Doe", written)

    def test_verify_timeout_is_metered_and_flagged(self):
        metered = []

        def timeout_run(cmd, **kwargs):
            if cmd[1].endswith("verify_sources.py"):
                raise subprocess.TimeoutExpired(cmd, kwargs.get("timeout"))
            return REAL_RUN(cmd, **kwargs)

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(self.server, "OUTPUT_DIR", Path(tmp)), \
                mock.patch.object(self.server.subprocess, "run", timeout_run), \
                mock.patch.object(self.server, "record_call", lambda **kw: metered.append(kw) or 0.0):
            result = self.server._finish_run(
                fixture(), None, product_url="https://ci.example", depth="deep", focus="all", people=False,
            )
            written = "".join(p.read_text(encoding="utf-8") for p in Path(tmp).rglob("*") if p.is_file())
        self.assertEqual(len(metered), 1)
        self.assertIs(result["verification_timed_out"], True)
        assert_no_leak(self, json.dumps(result), "timeout result")
        assert_no_leak(self, written, "timeout files")

    def test_verify_crash_leaves_no_unredacted_file(self):
        def crash_run(cmd, **kwargs):
            if cmd[1].endswith("verify_sources.py"):
                raise OSError("fork failed")
            return REAL_RUN(cmd, **kwargs)

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(self.server, "OUTPUT_DIR", Path(tmp)), \
                mock.patch.object(self.server.subprocess, "run", crash_run), \
                mock.patch.object(self.server, "record_call", lambda **kw: 0.0):
            with self.assertRaises(OSError):
                self.server._finish_run(
                    fixture(), None, product_url="https://ci.example", depth="quick", focus="all", people=False,
                )
            written = "".join(p.read_text(encoding="utf-8") for p in Path(tmp).rglob("*") if p.is_file())
        assert_no_leak(self, written, "files left after a verification crash")

    def failing_verify(self, keep_segment: bool, write_handoff: bool = True):
        """verify_sources exiting 1: the company's claim is Not on page; the
        segment is Verified (or also Not on page). The handoff drops what failed."""
        def run(cmd, **kwargs):
            if not cmd[1].endswith("verify_sources.py"):
                return REAL_RUN(cmd, **kwargs)
            data = json.loads(Path(cmd[2]).read_text(encoding="utf-8"))
            for item in data.get("segments") or []:
                item["verification_tier"] = TIER_VERIFIED if keep_segment else "unsupported"
            for item in data.get("companies") or []:
                item["verification_tier"] = "unsupported"
            Path(cmd[cmd.index("--annotate-out") + 1]).write_text(json.dumps(data), encoding="utf-8")
            if write_handoff:
                handoff = {k: v for k, v in data.items() if k != "companies"}
                if not keep_segment:
                    handoff.pop("segments")
                Path(cmd[cmd.index("--handoff-out") + 1]).write_text(json.dumps(handoff), encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 1, stdout="1 claim(s) are NOT ON THE PAGE they cite.", stderr="boom")
        return run

    def finish_with(self, tmp: str, run) -> dict:
        with mock.patch.object(self.server, "OUTPUT_DIR", Path(tmp)), \
                mock.patch.object(self.server.subprocess, "run", run), \
                mock.patch.object(self.server, "record_call", lambda **kw: 0.0):
            return self.server._finish_run(
                fixture(), None, product_url="https://ci.example", depth="standard", focus="all", people=False,
            )

    def test_not_on_page_prospect_is_left_out_of_the_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.finish_with(tmp, self.failing_verify(keep_segment=True))
            report = Path(result["report_path"]).read_text(encoding="utf-8")
        self.assertEqual((result["segments"], result["companies"]), (1, 0))
        self.assertEqual(result["disqualified_by_verification"], 1)
        self.assertNotIn(">Not on page<", report)
        self.assertIn("Teams with flaky CI", report)

    def test_no_report_when_every_prospect_fails_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "every prospect"):
                self.finish_with(tmp, self.failing_verify(keep_segment=False))
            self.assertEqual(list(Path(tmp).rglob("report-*.html")), [])

    def test_no_report_when_the_verifier_fails_without_a_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "did not complete"):
                self.finish_with(tmp, self.failing_verify(keep_segment=True, write_handoff=False))
            self.assertEqual(list(Path(tmp).rglob("report-*.html")), [])

    def test_verify_timeout_sized_to_depth(self):
        timeouts = self.server.VERIFY_TIMEOUTS
        self.assertLess(timeouts["quick"], timeouts["standard"])
        self.assertLess(timeouts["standard"], timeouts["deep"])

    def test_domain_normalized_in_mcp_path(self):
        data = fixture()
        data["companies"].append(dict(company(), name="Beta", domain="https://www.Beta.io/partners"))
        data["companies"].append(dict(company(), name="Gamma", domain="not a domain"))
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(self.server, "OUTPUT_DIR", Path(tmp)), \
                    mock.patch.object(self.server.subprocess, "run", self.fake_run), \
                    mock.patch.object(self.server, "record_call", lambda **kw: 0.0):
                result = self.server._finish_run(
                    data, None, product_url="https://ci.example", depth="standard", focus="all", people=False,
                )
            saved = json.loads(Path(result["analysis_path"]).read_text(encoding="utf-8"))
        self.assertEqual([c.get("domain") for c in saved["companies"]], ["acme.com", "beta.io", None])

    def test_focus_individuals_requires_people(self):
        with self.assertRaises(ValueError):
            self.server._validate_depth_focus("standard", "individuals", people=False)

    def test_prompt_tells_model_to_skip_people(self):
        captured = {}

        def fake_complete(system, prompt, tools):
            captured["prompt"] = prompt
            return {}, None

        with mock.patch.object(self.server, "_complete", fake_complete):
            self.server._run_classification("u", "", [{"source_url": "s", "evidence": "e"}], "quick", "all")
        self.assertIn(self.server.NO_PEOPLE_INSTRUCTION, captured["prompt"])


class NameMatchingTests(unittest.TestCase):
    def names_for(self, name: str) -> list[str]:
        return collect_person_names({"individuals": [{"name": name}]})

    def test_base_name_split_on_dashes_and_at(self):
        for raw in ("Jane Doe \u2014 CTO, Acme", "Jane Doe \u2013 CTO", "Jane Doe - CTO", "Jane Doe at Acme"):
            out, _ = redact_text("Thanks to Jane Doe for the thread.", self.names_for(raw))
            self.assertNotIn("Jane Doe", out, raw)

    def test_common_word_single_name_not_redacted(self):
        out, n = redact_text("Acme will launch a program. Will we join?", self.names_for("Will"))
        self.assertEqual(out, "Acme will launch a program. Will we join?")
        self.assertEqual(n, 0)

    def test_full_name_whole_word_any_case(self):
        names = self.names_for("Will Smith")
        out, _ = redact_text("Will Smith posted; a willsmithy will not match.", names)
        self.assertEqual(out, "[person removed] posted; a willsmithy will not match.")

    def test_distinctive_handle_token_redacted(self):
        out, _ = redact_text("search from:janedoe ci", self.names_for("janedoe"))
        self.assertNotIn("janedoe", out)

    def test_npm_scope_and_path_handles_survive(self):
        text = "Uses @vercel/og and @types/node; ping @janedoe."
        out, _ = redact_text(text, [])
        self.assertIn("@vercel/og", out)
        self.assertIn("@types/node", out)
        self.assertNotIn("@janedoe", out)
        self.assertTrue(out.endswith("."))


class UrlIdentifierTests(unittest.TestCase):
    """CodeRabbit: a non-personal URL can still carry a recorded name or handle."""

    NAMES = collect_person_names({"individuals": [{"name": "Jane Doe (@janedoe)"}]})

    def test_text_url_with_recorded_handle_is_removed(self):
        for url in ("https://forum.example.com/t/janedoe-ci-woes/9",
                    "https://blog.example.com/posts?author=JaneDoe",
                    "https://news.example.com/2026/jane-doe-on-flaky-ci"):
            out, n = redact_text(f"See {url} for details.", self.NAMES)
            self.assertNotIn(url, out, url)
            self.assertGreater(n, 0)

    def test_unicode_name_in_url_is_removed(self):
        names = collect_person_names({"individuals": [{"name": "Jos\u00e9 \u00c1lvarez"}]})
        for url in ("https://forum.example.com/t/jos\u00e9-\u00e1lvarez/3",
                    "https://forum.example.com/t/jos%C3%A9-%C3%A1lvarez/3"):
            out, _ = redact_text(f"See {url} now.", names)
            self.assertNotIn(url, out, url)

    def test_unrecorded_email_or_handle_in_url_is_removed(self):
        for url in ("https://acme.com/?contact=alice@example.com",
                    "https://acme.com/?contact=alice%40example.com",
                    "https://acme.com/share?via=@someperson"):
            out, _ = redact_text(f"See {url} now.", [])
            self.assertNotIn(url, out, url)
            self.assertNotIn("alice", out)
            self.assertNotIn("someperson", out)

    def test_role_inbox_and_npm_scope_urls_kept(self):
        for url in ("https://acme.com/?contact=partners@acme.com", "https://www.npmjs.com/package/@vercel/og"):
            out, _ = redact_text(f"See {url} now.", [])
            self.assertIn(url, out, url)

    def test_unrelated_url_kept(self):
        out, _ = redact_text(f"See {THREAD_URL}.", self.NAMES)
        self.assertIn(THREAD_URL, out)

    def test_prospect_sourced_from_url_naming_a_person_is_dropped(self):
        data = fixture()
        data["segments"].append(segment("Named thread", "https://forum.example.com/t/janedoe-ci-woes/9", "e"))
        out, stats = strip_people(data)
        self.assertNotIn("Named thread", [s["name"] for s in out.get("segments", [])])
        self.assertNotIn("janedoe", json.dumps(out).lower())

    def test_single_token_handle_case_insensitive(self):
        out, _ = redact_text("Thanks JaneDoe and JANEDOE.", self.NAMES)
        self.assertNotIn("janedoe", out.lower())

    def test_full_name_matches_in_lower_case(self):
        names = collect_person_names({"individuals": [{"name": "Will Smith"}]})
        out, _ = redact_text("thanks will smith", names)
        self.assertEqual(out, "thanks [person removed]")


class FinalizeInterruptedVerification(unittest.TestCase):
    """CodeRabbit: if verification is interrupted, public/ must hold nothing unredacted."""

    def test_public_folder_clean_when_verify_interrupted(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "analysis-2026-10-06.json"
            src.write_text(json.dumps(fixture()), encoding="utf-8")

            def interrupted(label, cmd):
                raise KeyboardInterrupt

            with mock.patch.object(finalize, "run_step", interrupted), \
                    mock.patch.object(sys, "argv", ["finalize.py", str(src), "--no-people"]), \
                    contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(KeyboardInterrupt):
                    finalize.main()
            public = Path(tmp) / "public"
            leftovers = [p for p in public.rglob("*") if p.is_file()] if public.exists() else []
            for path in leftovers:
                self.assertNotIn("janedoe", path.read_text(encoding="utf-8").lower(), path.name)
                self.assertNotIn("Jane Doe", path.read_text(encoding="utf-8"), path.name)


class RedactPeopleUnit(unittest.TestCase):
    def test_known_limit_bare_name_never_recorded_as_individual(self):
        """Documented boundary (COMPLIANCE.md): pattern matching, not NER. A bare
        name that was never an Individual and has no handle or URL stays."""
        out, _ = strip_people(fixture())
        self.assertIn("Sam Lee", json.dumps(out))

    def test_non_personal_urls_untouched(self):
        text = f"See {THREAD_URL} and {ISSUE_URL}, also https://www.linkedin.com/in/janedoe."
        out, n = redact_people(text, [])
        self.assertIn(THREAD_URL, out)
        self.assertIn(ISSUE_URL, out)
        self.assertNotIn("linkedin.com/in", out)
        self.assertEqual(n, 1)


class RecordedNameVariants(unittest.TestCase):
    """A name the analysis recorded as an Individual must not survive in any
    spelling the filter can reasonably derive from it."""

    def names_for(self, name: str) -> list[str]:
        return collect_person_names({"individuals": [{"name": name}]})

    def check(self, recorded: str, text: str, *leaks: str):
        out, n = redact_text(text, self.names_for(recorded))
        for leak in leaks:
            self.assertNotIn(leak.lower(), out.lower(), f"{recorded!r} in {text!r} -> {out!r}")
        self.assertGreater(n, 0, text)

    def test_short_single_token_names(self):
        self.check("Lena", "Lena said it is slow", "Lena")
        self.check("\u674e\u96f7", "\u674e\u96f7 said so", "\u674e\u96f7")

    def test_cjk_name_inside_running_text(self):
        self.check("\u738b\u5c0f\u660e", "\u738b\u5c0f\u660e\u8bf4\u592a\u6162\u4e86", "\u738b\u5c0f\u660e")

    def test_hebrew_name_with_prefix_letter(self):
        name = "\u05d3\u05e0\u05d4 \u05dc\u05d5\u05d9"
        self.check(name, "\u05d5" + name + " \u05db\u05ea\u05d1\u05d4", name)

    def test_case_variants(self):
        self.check("Jane Doe", "jane doe said it", "jane doe")
        self.check("Jane Doe", "JANE DOE said it", "jane doe")

    def test_single_tokens_of_a_full_name(self):
        self.check("Jane Doe", "Ms. Doe said it", "Doe")
        self.check("Jane Doe", "Jane said it", "Jane")
        self.check("Jane Doe", "Doe, Jane", "Doe", "Jane")

    def test_whitespace_and_joiner_variants(self):
        self.check("Jane Doe", "Jane\u00a0Doe said it", "Jane", "Doe")
        self.check("Jane Doe", "Jane  Doe said it", "Jane", "Doe")
        self.check("Jane Doe", "Jane-Doe and JaneDoe agree", "Jane", "Doe")

    def test_title_is_not_part_of_the_name(self):
        self.check("Dr. Jane Doe", "Jane Doe said it", "Jane Doe")
        self.check("Prof. Jane Doe", "Doe said it", "Doe")

    def test_decomposed_and_unaccented_spellings(self):
        recorded = "Jos\u00e9 \u00c1lvarez"
        self.check(recorded, "Jose\u0301 A\u0301lvarez said", "lvarez")
        self.check(recorded, "Jose Alvarez said", "Alvarez", "Jose")

    def test_everyday_word_tokens_are_still_left_alone(self):
        out, _ = redact_text("Smith posted; we will ship it.", self.names_for("Will Smith"))
        self.assertEqual(out, "[person removed] posted; we will ship it.")

    def test_name_as_dict_key(self):
        data = {"individuals": [{"name": "Jane Doe"}], "segments": [segment("Teams", THREAD_URL, "e")],
                "notes": {"Jane Doe": "x", "by_person": {"jane.doe@acme.com": "y"}}}
        out, stats = strip_people(data)
        dumped = json.dumps(out)
        self.assertNotIn("Jane Doe", dumped)
        self.assertNotIn("jane.doe@acme.com", dumped)
        self.assertGreater(stats["redactions"], 0)


class ContactPatternVariants(unittest.TestCase):
    def clean(self, text: str, *leaks: str, names: list[str] | None = None):
        out, n = redact_text(text, names or [])
        for leak in leaks:
            self.assertNotIn(leak, out, f"{text!r} -> {out!r}")
        self.assertGreater(n, 0, text)

    def test_scheme_less_profile_url(self):
        self.clean("profile: linkedin.com/in/jane-doe-123 (no scheme)", "jane-doe")
        self.clean("see www.x.com/janedoe.", "janedoe")

    def test_scheme_less_public_url_is_kept(self):
        text = "docs at github.com/acme/ci-runner/issues/42 and acme.com/partners"
        out, n = redact_text(text, [])
        self.assertEqual((out, n), (text, 0))

    def test_linkedin_article_and_youtube_channel_urls_are_personal(self):
        for url in ("https://www.linkedin.com/pulse/why-ci-hurts-jane-doe-xyz", "https://www.youtube.com/c/JaneDoe",
                    "https://www.youtube.com/user/JaneDoe", "https://www.youtube.com/channel/UCabc"):
            self.assertTrue(is_personal_url(url), url)
        self.assertFalse(is_personal_url("https://www.youtube.com/watch?v=abc"))

    def test_non_ascii_email(self):
        self.clean("mail jos\u00e9@acme.com", "acme.com", "jos")

    def test_fullwidth_at_sign(self):
        self.clean("ping \uff20janedoe or jane\uff20acme.com", "janedoe", "acme.com")

    def test_obfuscated_email(self):
        self.clean("jane [at] acme [dot] com", "jane", "acme")
        self.clean("jane(at)acme.com", "jane", "acme")

    def test_non_ascii_handle_is_removed_whole(self):
        out, _ = redact_text("@jos\u00e9_garc\u00eda wrote this", [])
        self.assertEqual(out, "[person removed] wrote this")

    def test_handle_followed_by_status_path(self):
        self.clean("see @janedoe/status/123", "janedoe")

    def test_role_inbox_on_a_recorded_persons_domain(self):
        names = collect_person_names({"individuals": [{"name": "Jane Doe"}]})
        self.clean("contact hello@janedoe.com", "janedoe", names=names)
        out, _ = redact_text("contact hello@acme.com", names)
        self.assertIn("hello@acme.com", out)


class LimitsNoteWording(unittest.TestCase):
    def test_note_does_not_claim_the_report_names_no_people(self):
        out, _ = strip_people(fixture())
        note = [x for x in out["limits"] if str(x).startswith("No-people mode:")][0]
        self.assertNotIn("names no people", note)
        self.assertIn("review before publishing", note)


if __name__ == "__main__":
    unittest.main()
