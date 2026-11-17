"""Deterministic semantic and failure-boundary tests; no external requests."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("collect", ROOT / "scripts/collect.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
PROXY = "http://fixture-user:fixture-password@127.0.0.1:9"


def args(mode, *extra):
    return c.parser().parse_args(["--mode", mode, *extra])


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()
        c.REDACTOR = c.Redactor()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def error(self, code, action, status=None):
        with self.assertRaises(c.CollectionError) as caught:
            action()
        self.assertEqual(caught.exception.code, code)
        if status:
            self.assertEqual(caught.exception.status, status)


class SharedTests(Base):
    def test_proxy_missing_invalid_supported_and_private_file(self):
        a = args("price")
        self.error("proxy_required", lambda: c.proxy_input(a), "missing_input")
        self.assertIsNone(c.proxy_input(a, required=False))
        for value in ["socks5://localhost:9", "http://localhost", "http://localhost:9/path", "http://localhost:9?q=x"]:
            with self.subTest(value=value), patch.dict(os.environ, {"PROXYLANE_PROXY_URL": value}):
                self.error("unsupported_proxy", lambda: c.proxy_input(a), "input_error")
        connection = self.directory / "connection.private"
        connection.write_text(PROXY)
        a.proxy_file = str(connection)
        self.assertEqual(c.proxy_input(a), PROXY)
        serialized = json.dumps(c.REDACTOR.value({"exception": PROXY, "password": "secret", "user": "fixture-user"}))
        self.assertNotIn("fixture-password", serialized)
        self.assertNotIn("fixture-user", serialized)

    def test_redaction_tokens_url_userinfo_and_known_secret(self):
        redactor = c.Redactor()
        redactor.add("fixture-bearer-secret")
        cleaned = redactor.value({"token": "fixture-token", "xsecToken": "fixture-xsec", "Authorization": "Bearer fixture-bearer-secret", "url": "https://fixture-user:fixture-password@example.invalid/p?sign=private&plain=kept", "error": "Bearer fixture-bearer-secret"})
        rendered = json.dumps(cleaned)
        for secret in ["fixture-token", "fixture-xsec", "fixture-bearer-secret", "fixture-user:fixture-password", "private"]:
            self.assertNotIn(secret, rendered)
        self.assertIn("plain=kept", rendered)

    def test_short_secret_does_not_destroy_unrelated_words(self):
        redactor = c.Redactor()
        redactor.add("u")
        self.assertEqual(redactor.text("user u has output"), "user [REDACTED] has output")

    def test_persist_hash_and_private_file_permissions(self):
        a = args("price", "--fixture", "--out", str(self.directory))
        first = c.persist(a, "record", {"token": "secret", "text": "fixture"})
        second = c.persist(a, "record", {"text": "fixture", "token": "other-secret"})
        self.assertEqual(first["sha256"], second["sha256"])
        stored = self.directory / first["path"]
        self.assertEqual(stat.S_IMODE(stored.stat().st_mode), 0o600)
        self.assertNotIn("other-secret", stored.read_text())

    def test_normalization_deduplicates_identity_preserving_source_order(self):
        self.assertEqual(c.normalize([{"id": "b", "text": "one"}, {"id": "a", "text": "two"}, {"id": "b", "text": "duplicate"}], "id"), [{"id": "b", "text": "one"}, {"id": "a", "text": "two"}])

    def test_youtube_identity_url_forms_and_invalid_host(self):
        expected = "aircAruvnKk"
        for target in [expected, "https://youtu.be/" + expected, "https://www.youtube.com/watch?v=" + expected, "https://www.youtube.com/shorts/" + expected]:
            self.assertEqual(c.video_id(target), expected)
        self.error("video_id_required", lambda: c.video_id("https://evil.example/watch?v=" + expected), "input_error")

    def test_http_retries_only_transient_status_and_no_retry_auth(self):
        def response(status):
            return SimpleNamespace(status_code=status, raise_for_status=lambda: None)
        session = SimpleNamespace(get=lambda *a, **k: None)
        with patch.object(session, "get", side_effect=[response(503), response(200)]) as call, patch.object(c.time, "sleep"):
            self.assertEqual(c.bounded_get(session, "https://example.org").status_code, 200)
            self.assertEqual(call.call_count, 2)
        for status in [401, 403, 407, 429]:
            with patch.object(session, "get", return_value=response(status)) as call, patch.object(c.time, "sleep"):
                self.error("http_" + str(status), lambda: c.bounded_get(session, "https://example.org"), "blocked")
                self.assertEqual(call.call_count, 2 if status == 429 else 1)


class TranscriptTests(Base):
    def test_fixture_language_timing_and_limit(self):
        a = args("youtube-transcript", "--fixture", "--limit", "1")
        result = c.transcript(a)
        self.assertEqual(result["proof_mode"], "fixture")
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["observations"][0]["language"], "en")
        self.assertEqual(result["observations"][0]["start_seconds"], 0.0)
        self.assertFalse(result["coverage"]["complete_track"])

    def test_same_second_captions_are_distinct_and_negative_time_fails(self):
        raw = c.fixture("youtube-transcript")
        raw["segments"] = [{"text": "one", "start": 0.1, "duration": 1}, {"text": "two", "start": 0.9, "duration": 1}]
        with patch.object(c, "fixture", return_value=raw):
            self.assertEqual(len(c.transcript(args("youtube-transcript", "--fixture"))["observations"]), 2)
        raw["segments"][0]["start"] = -1
        with patch.object(c, "fixture", return_value=raw):
            self.error("invalid_timing", lambda: c.transcript(args("youtube-transcript", "--fixture")), "error")

    def test_missing_captions_and_proxy_auth_are_distinct(self):
        a = args("youtube-transcript", "--target", "aircAruvnKk")
        os.environ["PROXYLANE_PROXY_URL"] = PROXY
        for name, message, expected_code, status in [("NoTranscriptFound", "missing", "NoTranscriptFound", "no_data"), ("ProxyError", "Tunnel connection failed: 407 Proxy Authentication Required", "proxy_auth_required", "blocked")]:
            error = type(name, (Exception,), {})(message)
            api = SimpleNamespace(fetch=lambda *a, **k: None)
            with patch("youtube_transcript_api.YouTubeTranscriptApi", return_value=api), patch.object(api, "fetch", side_effect=error):
                self.error(expected_code, lambda: c.transcript(a), status)

    def test_identity_mismatch_and_bounded_block_retry(self):
        a = args("youtube-transcript", "--target", "aircAruvnKk", "--attempts", "2")
        os.environ["PROXYLANE_PROXY_URL"] = PROXY
        fetched = SimpleNamespace(video_id="wrong", language="English", language_code="en", is_generated=False, to_raw_data=lambda: [])
        api = SimpleNamespace(fetch=lambda *a, **k: fetched)
        with patch("youtube_transcript_api.YouTubeTranscriptApi", return_value=api):
            self.error("caption_target_mismatch", lambda: c.transcript(a), "error")
        error = type("RequestBlocked", (Exception,), {})("blocked")
        with patch("youtube_transcript_api.YouTubeTranscriptApi", return_value=api), patch.object(api, "fetch", side_effect=error) as call, patch.object(c.time, "sleep"):
            self.error("RequestBlocked", lambda: c.transcript(a), "blocked")
            self.assertEqual(call.call_count, 2)


class CommentsTests(Base):
    def setup_live(self):
        os.environ["PROXYLANE_PROXY_URL"] = PROXY
        a = args("youtube-comments", "--target", "aircAruvnKk", "--limit", "2")
        a._scratch = str(self.directory)
        raw = c.fixture("youtube-comments")
        raw["id"] = "aircAruvnKk"
        return a, raw

    def test_private_proxy_config_not_argv_and_cleanup(self):
        a, raw = self.setup_live()
        def execute(command, **kwargs):
            self.assertNotIn(PROXY, " ".join(command))
            config = Path(command[command.index("--config-locations") + 1])
            self.assertEqual(stat.S_IMODE(config.stat().st_mode), 0o600)
            self.assertIn("--proxy", config.read_text())
            self.assertIn(PROXY, config.read_text())
            return SimpleNamespace(returncode=0, stdout=json.dumps(raw), stderr="")
        with patch.object(c.subprocess, "run", side_effect=execute):
            result = c.comments(a)
        self.assertEqual(len(result["observations"]), 2)
        self.assertEqual(list(self.directory.glob("*.conf")), [])

    def test_empty_comments_target_mismatch_and_407(self):
        a, raw = self.setup_live()
        raw["comments"] = []
        with patch.object(c.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout=json.dumps(raw), stderr="")):
            self.assertEqual(c.comments(a)["status"], "no_data")
        raw["id"] = "wrong"
        with patch.object(c.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout=json.dumps(raw), stderr="")):
            self.error("target_mismatch", lambda: c.comments(a), "error")
        with patch.object(c.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout="", stderr="Tunnel 407 Proxy Authentication Required")):
            self.error("proxy_auth_required", lambda: c.comments(a), "blocked")
        self.assertEqual(list(self.directory.glob("*.conf")), [])


class Locator:
    def __init__(self, text="", count=1, visible=True, anchors=None):
        self.text, self.number, self.visible, self.anchors = text, count, visible, anchors or []
        self.children = {}
    def count(self): return self.number
    def is_visible(self): return self.visible
    def inner_text(self): return self.text
    def locator(self, selector): return self.children[selector]
    def all(self): return self.anchors
    def get_attribute(self, key): return getattr(self, key, None)


class GoogleTests(Base):
    def setup_google(self):
        os.environ["PROXYLANE_PROXY_URL"] = PROXY
        contract = {"reviewed": True, "surface": "ai-mode", "observed_on": "2026-10-07", "surface_selector": "#ai-root", "answer_selector": "#answer", "citation_selector": "a.citation", "surface_marker": "Fixture AI"}
        path = self.directory / "contract.json"
        path.write_text(json.dumps(contract))
        a = args("google-citations", "--query", "fixture query", "--surface", "ai-mode", "--dom-contract", str(path))
        root, answer = Locator("Fixture AI visible answer"), Locator("Fixture answer text")
        source = Locator("Fixture source"); source.href = "https://example.org/source"
        hidden = Locator("Hidden non-source", visible=False); hidden.href = "https://example.org/not-a-source"
        legal = Locator("Privacy"); legal.href = "https://policies.google.com/privacy"
        answer.children["a.citation"] = Locator(anchors=[source, source, hidden, legal])
        root.children["#answer"] = answer
        # If citations were selected from the enclosing root, this unit would
        # fail rather than accidentally include another unrelated sibling.
        page = SimpleNamespace(url="https://www.google.com/search?q=fixture+query&udm=50", content=lambda: "<html>fixture</html>", locator=lambda selector: root)
        closable = SimpleNamespace(close=lambda: None, stop=lambda: None)
        browser = (closable, closable, closable, page, SimpleNamespace(status=200))
        return a, contract, path, root, answer, page, browser

    def test_visible_answer_scoped_source_citations_and_region_unverified(self):
        a, _, _, _, _, _, browser = self.setup_google()
        with patch.object(c, "browser_page", return_value=browser):
            result = c.google(a)
        row = result["observations"][0]
        self.assertEqual(row["citations"], [{"url": "https://example.org/source", "title": "Fixture source"}])
        self.assertEqual(row["regional_validation"], "unverified")
        self.assertEqual(result["status"], "partial")

    def test_unreviewed_contract_fails_before_navigation(self):
        a, contract, path, _, _, _, _ = self.setup_google()
        contract["reviewed"] = False; path.write_text(json.dumps(contract))
        with patch.object(c, "browser_page") as navigate:
            self.error("unreviewed_dom_contract", lambda: c.google(a), "unsupported_surface")
            navigate.assert_not_called()

    def test_missing_ambiguous_root_and_missing_marker(self):
        for count, text, code in [(0, "Fixture AI", "surface_missing_or_ambiguous"), (2, "Fixture AI", "surface_missing_or_ambiguous"), (1, "not AI", "surface_marker_missing")]:
            with self.subTest(code=code, count=count):
                a, _, _, root, _, _, browser = self.setup_google()
                root.number, root.text = count, text
                with patch.object(c, "browser_page", return_value=browser):
                    self.error(code, lambda: c.google(a), "unsupported_surface")

    def test_challenge_and_target_mismatch(self):
        a, _, _, _, _, page, browser = self.setup_google()
        page.content = lambda: "unusual traffic from your computer"
        with patch.object(c, "browser_page", return_value=browser):
            self.error("google_challenge", lambda: c.google(a), "blocked")
        page.content = lambda: "fixture"
        page.url = "https://www.google.com/search?q=unrelated"
        with patch.object(c, "browser_page", return_value=browser):
            self.error("target_mismatch", lambda: c.google(a), "error")

    def test_empty_citations_and_google_redirect_decode(self):
        raw = c.fixture("google-citations")
        with patch.object(c, "fixture", return_value=raw):
            result = c.google(args("google-citations", "--fixture"))
        self.assertIn("https://example.org/fixture-source-b", [i["url"] for i in result["observations"][0]["citations"]])
        raw["citations"] = []
        with patch.object(c, "fixture", return_value=raw):
            self.assertEqual(c.google(args("google-citations", "--fixture"))["status"], "no_data")


class PriceTests(Base):
    def test_amazon_identity_variant_required_fields_and_currency_boundary(self):
        raw = c.fixture("price")
        row, _, _ = c.parse_price(raw["html"], raw["url"], raw["expected_id"], "amazon", "Blue")
        self.assertIsNone(row["currency"])
        self.assertIsNone(row["price"])
        self.assertEqual(row["price_text"], "$19.99")
        self.error("product_target_mismatch", lambda: c.parse_price(raw["html"], raw["url"], "WRONG", "amazon"), "error")
        self.error("variant_mismatch", lambda: c.parse_price(raw["html"], raw["url"], raw["expected_id"], "amazon", "Green"), "error")
        self.error("offer_fields_missing", lambda: c.parse_price(raw["html"].replace("id='availability'", "id='other'"), raw["url"], raw["expected_id"], "amazon"), "no_data")

    def product(self):
        return {"@type": "Product", "sku": "EXACT-SKU", "name": "Fixture blue item", "offers": {"@type": "Offer", "price": "12.50", "priceCurrency": "USD", "availability": "https://schema.org/InStock"}}

    def html(self, product):
        return '<script type="application/ld+json">' + json.dumps({"@graph": [product]}) + '</script>'

    def test_jsonld_exact_offer_in_graph(self):
        row, _, _ = c.parse_price(self.html(self.product()), "https://example.org/product", "EXACT-SKU", "jsonld", "blue")
        self.assertEqual((row["price"], row["currency"]), ("12.50", "USD"))
        self.error("product_target_mismatch", lambda: c.parse_price(self.html(self.product()), "https://example.org", "OTHER", "jsonld"))

    def test_jsonld_invalid_price_currency_availability_aggregate_and_multiple(self):
        for key, value, code in [("price", "NaN", "invalid_price"), ("price", "-1", "invalid_price"), ("priceCurrency", "$", "offer_fields_missing"), ("availability", "https://schema.org/Product", "offer_fields_missing"), ("@type", "AggregateOffer", "offer_ambiguous")]:
            with self.subTest(key=key, value=value):
                product = self.product(); product["offers"][key] = value
                self.error(code, lambda: c.parse_price(self.html(product), "https://example.org", "EXACT-SKU", "jsonld"), "no_data")
        product = self.product(); product["offers"] = [product["offers"], copy.deepcopy(product["offers"])]
        self.error("offer_ambiguous", lambda: c.parse_price(self.html(product), "https://example.org", "EXACT-SKU", "jsonld"))
        self.error("variant_unverified", lambda: c.parse_price(self.html(self.product()), "https://example.org", "EXACT-SKU", "jsonld", "red"))


class MCPShapeTests(Base):
    def test_structured_json_text_and_rejection(self):
        self.assertEqual(c.mcp_data({"structuredContent": {"ok": True}}), {"ok": True})
        self.assertEqual(c.mcp_data({"content": [{"type": "text", "text": '{"ok":true}'}]}), {"ok": True})
        self.error("mcp_shape_unsupported", lambda: c.mcp_data({"content": [{"type": "text", "text": "not JSON"}]}))

    def test_xhs_missing_inputs_no_session_mutation(self):
        self.error("mcp_required", lambda: c.xiaohongshu(args("xiaohongshu")), "missing_input")
        self.error("xhs_proxy_required", lambda: c.xiaohongshu(args("xiaohongshu", "--mcp-url", "http://localhost:18060/mcp")), "missing_input")
        raw = c.fixture("xiaohongshu"); raw["data"]["note"]["noteId"] = "wrong"
        with patch.object(c, "fixture", return_value=raw):
            self.error("note_target_mismatch", lambda: c.xiaohongshu(args("xiaohongshu", "--fixture")), "error")


if __name__ == "__main__":
    unittest.main()
