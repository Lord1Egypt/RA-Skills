"""Deterministic fault tests; generated test squares are not model-made samples."""
import copy
import json
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

from PIL import Image
import newspaper_project as n


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "project"
        self.root.mkdir()
        self.source = self.base / "source.png"
        self.output = self.base / "result.png"
        Image.new("RGB", (640, 400), "orange").save(self.source)
        Image.new("RGB", (640, 400), "blue").save(self.output)
        n.init(self.root, "Fictional test", orientation="landscape", pages=2,
               delegated_approval="Explicitly authorized offline fixture evaluation")
        project = n.load(self.root)
        n.copy_asset(self.root, project, "source", self.source, "content", "synthetic")
        n.save(self.root, project)
        self.spec = {"stage": "extraction", "model": "test-only", "promptVersion": "v1",
                     "inputs": ["source"], "instruction": "Separate the subject"}

    def page_spec(self, page_id):
        return {**self.spec, "stage": "page", "pageId": page_id, "instruction": "Fictional layout"}

    def approved_issue(self):
        n.approve(self.root, "plan", "delegated", "Fixture plan checked")
        front = n.begin(self.root, self.page_spec("page-01"))
        n.complete(self.root, front["taskId"], self.source)
        n.approve(self.root, "front", "delegated", "Fixture front checked")
        inner = n.begin(self.root, self.page_spec("page-02"))
        n.complete(self.root, inner["taskId"], self.output)
        n.approve(self.root, "issue", "delegated", "Fixture issue checked")
        return front, inner

    def test_cached_result_and_missing_usage(self):
        first = n.begin(self.root, self.spec)
        n.complete(self.root, first["taskId"], self.output)
        reused = n.begin(self.root, {**self.spec, "caption": "Management name", "rationale": "Explanation"})
        self.assertEqual(reused["action"], "cached")
        self.assertEqual(reused["taskId"], first["taskId"])
        measured = n.status(self.root)
        self.assertEqual(measured["taskAttempts"], 1)
        self.assertEqual(measured["cacheHits"], 1)
        self.assertIsNone(measured["recordedTokens"])
        self.assertIsNone(measured["recordedDurationMs"])

    def test_corrupt_cache_is_never_returned(self):
        first = n.begin(self.root, self.spec)
        result = n.complete(self.root, first["taskId"], self.output)
        (self.root / result["asset"]["path"]).write_bytes(b"broken")
        self.assertEqual(n.begin(self.root, self.spec)["action"], "blocked")

    def test_changed_input_bytes_rejected_and_instruction_changes_key(self):
        first = n.begin(self.root, self.spec)
        n.complete(self.root, first["taskId"], self.output)
        changed = n.begin(self.root, {**self.spec, "instruction": "Change only the subject pose"})
        self.assertNotEqual(first["taskId"], changed["taskId"])
        asset = n.load(self.root)["assets"]["source"]
        (self.root / asset["path"]).write_bytes(b"tampered")
        with self.assertRaises(ValueError):
            n.begin(self.root, self.spec)

    def test_auto_retry_once_only_affirmative_not_started(self):
        first = n.begin(self.root, self.spec)
        n.fail(self.root, first["taskId"], "not-started", True, "Rate limit rejected request before execution")
        retry = n.begin(self.root, self.spec)
        self.assertEqual((retry["action"], retry["attempt"]), ("run", 2))
        n.fail(self.root, retry["taskId"], "not-started", True, "Rate limited again")
        self.assertEqual(n.begin(self.root, self.spec)["action"], "blocked")

    def test_unknown_timeout_and_in_progress_do_not_retry(self):
        first = n.begin(self.root, self.spec)
        self.assertEqual(n.begin(self.root, self.spec)["action"], "blocked")
        n.fail(self.root, first["taskId"], "unknown", True, "Connection lost")
        self.assertEqual(n.begin(self.root, self.spec)["action"], "blocked")
        retry = n.begin(self.root, self.spec, retry_manual=True)
        self.assertEqual(retry["taskId"], first["taskId"])
        n.fail(self.root, first["taskId"], "not-started", True, "Timeout")
        self.assertEqual(n.begin(self.root, self.spec)["action"], "blocked")

    def test_late_valid_output_recovered_without_second_attempt(self):
        first = n.begin(self.root, self.spec)
        n.fail(self.root, first["taskId"], "unknown", False, "Response missing")
        n.complete(self.root, first["taskId"], self.output)
        self.assertEqual(n.begin(self.root, self.spec)["action"], "cached")
        self.assertEqual(n.status(self.root)["taskAttempts"], 1)

    def test_explicit_new_generation_then_same_intent_failure_recovery(self):
        self.approved_issue()
        old = n.begin(self.root, self.page_spec("page-02"))
        new = n.begin(self.root, self.page_spec("page-02"), new_intent=True)
        self.assertNotEqual(old["taskId"], new["taskId"])
        n.fail(self.root, new["taskId"], "not-started", True, "Rejected before start")
        recovered = n.begin(self.root, self.page_spec("page-02"))
        self.assertEqual(new["taskId"], recovered["taskId"])
        self.assertEqual(new["spec"]["generationKey"], recovered["spec"]["generationKey"])
        n.complete(self.root, recovered["taskId"], self.source)
        project = n.load(self.root)
        self.assertEqual(len(project["pages"]["page-02"]["history"]), 1)
        n.restore_page(self.root, "page-02", old["taskId"])
        restored = n.begin(self.root, self.page_spec("page-02"))
        self.assertEqual(restored["taskId"], old["taskId"])
        again = n.begin(self.root, self.page_spec("page-02"), new_intent=True)
        self.assertNotIn(again["taskId"], [old["taskId"], new["taskId"]])

    def test_unknown_new_intent_keeps_nonce_and_does_not_reapply_old_cache(self):
        self.approved_issue()
        original_asset = n.load(self.root)["pages"]["page-02"]["assetId"]
        new = n.begin(self.root, self.page_spec("page-02"), new_intent=True)
        n.fail(self.root, new["taskId"], "unknown", True, "Lost response")
        blocked = n.begin(self.root, self.page_spec("page-02"))
        self.assertEqual((blocked["action"], blocked["taskId"]), ("blocked", new["taskId"]))
        self.assertEqual(n.load(self.root)["pages"]["page-02"]["assetId"], original_asset)
        resumed = n.begin(self.root, self.page_spec("page-02"), retry_manual=True)
        self.assertEqual(resumed["taskId"], new["taskId"])

    def test_older_intent_late_result_cannot_replace_newer_page(self):
        self.approved_issue()
        old = n.begin(self.root, self.page_spec("page-02"), new_intent=True)
        latest = n.begin(self.root, self.page_spec("page-02"), new_intent=True)
        n.complete(self.root, latest["taskId"], self.source)
        late = n.complete(self.root, old["taskId"], self.output)
        self.assertFalse(late["appliedToPage"])
        self.assertEqual(n.load(self.root)["pages"]["page-02"]["taskId"], latest["taskId"])

    def test_pending_front_revision_revokes_previous_issue_approval(self):
        self.approved_issue()
        n.begin(self.root, self.page_spec("page-01"), new_intent=True)
        project = n.load(self.root)
        self.assertNotIn("issue", project["approvals"])
        self.assertNotIn("front", project["approvals"])
        self.assertTrue(project["pages"]["page-01"]["needsRender"])
        with self.assertRaises(ValueError):
            n.begin(self.root, self.page_spec("page-02"), new_intent=True)

    def test_plan_local_change_preserves_front_and_untouched_assets(self):
        self.approved_issue()
        before = n.load(self.root)
        plan = copy.deepcopy(before["plan"])
        plan["pages"][1]["articles"] = [{"heading": "New copy", "body": "Printed text"}]
        result = n.set_plan(self.root, plan)
        self.assertEqual(result["invalidatedPages"], ["page-02"])
        after = n.load(self.root)
        self.assertEqual(after["pages"]["page-01"], before["pages"]["page-01"])
        self.assertEqual(after["assets"], before["assets"])
        self.assertTrue(after["pages"]["page-02"]["needsRender"])
        self.assertIn("front", after["approvals"])

    def test_front_copy_edit_keeps_finished_inner_page_and_can_export(self):
        self.approved_issue()
        before = n.load(self.root)
        inner_asset = before["pages"]["page-02"]["assetId"]
        changed = copy.deepcopy(before["plan"])
        changed["pages"][0]["articles"] = [{"heading": "Corrected headline", "body": "One local copy edit"}]
        self.assertEqual(n.set_plan(self.root, changed)["invalidatedPages"], ["page-01"])
        n.approve(self.root, "plan", "delegated", "Approved local headline correction")
        revised = n.begin(self.root, self.page_spec("page-01"), new_intent=True)
        n.complete(self.root, revised["taskId"], self.output)
        n.approve(self.root, "front", "delegated", "Corrected front page checked")
        after = n.load(self.root)
        self.assertEqual(after["pages"]["page-02"]["assetId"], inner_asset)
        self.assertFalse(after["pages"]["page-02"]["needsRender"])
        n.approve(self.root, "issue", "delegated", "Existing inner page still matches this issue")
        result = n.export_pdf(self.root, self.base / "local-copy-edit.pdf")
        self.assertEqual(len(result["pages"]), 2)
        self.assertEqual(n.status(self.root)["taskAttempts"], 3)

    def test_shared_visual_direction_change_invalidates_every_page(self):
        self.approved_issue()
        changed = n.load(self.root)["plan"]
        changed["style"] = "Replace the issue-wide palette and typography"
        self.assertEqual(n.set_plan(self.root, changed)["invalidatedPages"], ["page-01", "page-02"])
        project = n.load(self.root)
        self.assertTrue(all(page["needsRender"] for page in project["pages"].values()))
        self.assertNotIn("front", project["approvals"])
        self.assertNotIn("issue", project["approvals"])

    def test_plan_edit_during_generation_does_not_apply_stale_result(self):
        n.approve(self.root, "plan", "delegated", "Plan checked")
        started = n.begin(self.root, self.page_spec("page-01"))
        changed = n.load(self.root)["plan"]
        changed["pages"][0]["summary"] = "Changed after request"
        n.set_plan(self.root, changed)
        result = n.complete(self.root, started["taskId"], self.output)
        self.assertFalse(result["appliedToPage"])
        self.assertEqual(n.load(self.root)["tasks"][started["taskId"]]["status"], "completed")
        self.assertNotIn("page-01", n.load(self.root)["pages"])

    def test_confirmations_cannot_be_faked_by_empty_feedback_or_delegation(self):
        with self.assertRaises(ValueError):
            n.begin(self.root, self.page_spec("page-01"))
        n.approve(self.root, "plan", "delegated", "Satisfied; no changes requested")
        with self.assertRaises(ValueError):
            n.begin(self.root, self.page_spec("page-02"))
        project = n.load(self.root)
        project["delegatedApproval"] = None
        n.save(self.root, project)
        with self.assertRaises(ValueError):
            n.approve(self.root, "plan", "delegated", "Unapproved delegation")

    def test_duplex_is_print_mode_not_page_limit(self):
        other = self.base / "duplex"
        other.mkdir()
        n.init(other, "Four pages", paper="A3", orientation="landscape", sides="double", pages=4)
        project = n.load(other)
        self.assertEqual(len(project["plan"]["pages"]), 4)
        self.assertEqual((project["paper"]["widthMm"], project["paper"]["heightMm"]), (420, 297))

    def test_archive_roundtrip_preserves_hashes_plans_history_and_records(self):
        self.approved_issue()
        package = self.base / "roundtrip.newspaper.zip"
        n.archive(self.root, package)
        restored = self.base / "restored"
        n.restore(package, restored)
        self.assertEqual(n.load(self.root), n.load(restored))
        for asset in n.load(restored)["assets"].values():
            self.assertEqual(n.check_asset(self.root, asset).read_bytes(), n.check_asset(restored, asset).read_bytes())

    def test_archive_rejects_traversal_duplicates_and_symlinks(self):
        for name, entries in (("traversal", ["../outside.txt"]), ("absolute", ["C:/outside.txt"]),
                              ("backslash", ["..\\outside.txt"]), ("duplicate", ["project.json", "PROJECT.JSON"])):
            package = self.base / (name + ".zip")
            with zipfile.ZipFile(package, "w") as zipped:
                for item in entries:
                    zipped.writestr(item, "{}")
            with self.assertRaises((ValueError, KeyError)):
                n.restore(package, self.base / ("restore-" + name))
        package = self.base / "symlink.zip"
        with zipfile.ZipFile(package, "w") as zipped:
            info = zipfile.ZipInfo("project.json")
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            zipped.writestr(info, "../outside.txt")
        with self.assertRaises(ValueError):
            n.restore(package, self.base / "restore-symlink")

    def test_pdf_actual_dimensions_native_pixels_and_no_project(self):
        from pypdf import PdfReader
        self.approved_issue()
        output = self.base / "print.pdf"
        result = n.export_pdf(self.root, output)
        document = PdfReader(output)
        self.assertEqual(len(document.pages), 2)
        for page in document.pages:
            self.assertAlmostEqual(float(page.mediabox.width), 297 / 25.4 * 72, places=3)
            self.assertAlmostEqual(float(page.mediabox.height), 210 / 25.4 * 72, places=3)
            images = list(page["/Resources"]["/XObject"].values())
            self.assertEqual((images[0].get_object()["/Width"], images[0].get_object()["/Height"]), (640, 400))
        self.assertNotIn(b"/EmbeddedFiles", output.read_bytes())
        self.assertFalse(result["containsProject"])
        self.assertLess(result["pages"][0]["effectiveDpi"], 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
