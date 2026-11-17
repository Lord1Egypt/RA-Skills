"""Tests for the Social actions catalog, profiles, and lookup CLI."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPOSITORY / "references" / "actions.jsonl"
PROFILES_PATH = REPOSITORY / "references" / "profiles.json"
LOOKUP_SCRIPT = REPOSITORY / "scripts" / "lookup_actions.py"

sys.path.insert(0, str(REPOSITORY / "scripts"))
import lookup_actions  # noqa: E402
import import_actions  # noqa: E402


class ActionsCatalogAndLookupTests(unittest.TestCase):
    def test_catalog_file_is_valid_jsonl(self):
        self.assertTrue(CATALOG_PATH.exists(), f"missing {CATALOG_PATH}")
        lines = [
            line.strip()
            for line in CATALOG_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(lines), 31)
        keys = set()
        for idx, line in enumerate(lines, start=1):
            data = json.loads(line)
            for required in ("key", "name", "summary", "description"):
                self.assertIn(required, data)
                self.assertTrue(str(data[required]).strip())
            self.assertNotIn(data["key"], keys, f"duplicate key {data['key']} at line {idx}")
            keys.add(data["key"])
        self.assertIn("uploadSocialMedia", keys)
        self.assertIn("getSocialPortals", keys)

    def test_profiles_file_is_valid_and_consistent(self):
        self.assertTrue(PROFILES_PATH.exists(), f"missing {PROFILES_PATH}")
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data.get("version"), 1)
        self.assertEqual(data.get("service"), "social")
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--validate"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validation OK", result.stdout)

    def test_lookup_cli_profiles_listing(self):
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--profiles"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("social-viewer", result.stdout)
        self.assertIn("social-publisher", result.stdout)
        self.assertIn("social-admin", result.stdout)

    def test_lookup_cli_task_inspection(self):
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--task", "media-asset-management"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("uploadSocialMedia", result.stdout)
        self.assertIn("getSocialMediaLibrary", result.stdout)

    def test_lookup_cli_search_names_only(self):
        result = subprocess.run(
            [sys.executable, str(LOOKUP_SCRIPT), "--search", "draft", "--names-only"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("createSocialDraft", result.stdout)

    def test_all_profiles_fit_within_300_action_limit(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        profiles = data["profiles"]
        viewer = lookup_actions.resolve_profile_actions("social-viewer", profiles)
        creator = lookup_actions.resolve_profile_actions("social-creator", profiles)
        publisher = lookup_actions.resolve_profile_actions("social-publisher", profiles)
        admin = lookup_actions.resolve_profile_actions("social-admin", profiles)
        self.assertEqual(len(viewer), 16)
        self.assertEqual(len(creator), 23)
        self.assertEqual(len(publisher), 30)
        self.assertEqual(len(admin), 31)
        self.assertLessEqual(len(admin), 300)

    def test_viewer_is_read_only(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("social-viewer", data["profiles"])
        self.assertIn("getSocialPortals", actions)
        self.assertIn("getSocialMediaLibrary", actions)
        self.assertNotIn("uploadSocialMedia", actions)
        self.assertNotIn("publishSocialPost", actions)
        self.assertNotIn("deleteSocialSchedule", actions)
        self.assertNotIn("createSocialDraft", actions)

    def test_creator_can_draft_and_upload_but_not_publish(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("social-creator", data["profiles"])
        self.assertIn("createSocialDraft", actions)
        self.assertIn("uploadSocialMedia", actions)
        self.assertIn("validateSocialPost", actions)
        self.assertNotIn("publishSocialPost", actions)
        self.assertNotIn("createSocialSchedule", actions)
        self.assertNotIn("deleteSocialSchedule", actions)

    def test_publisher_can_publish_but_not_delete_schedules(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("social-publisher", data["profiles"])
        self.assertIn("publishSocialPost", actions)
        self.assertIn("createSocialSchedule", actions)
        self.assertIn("deleteSocialDraft", actions)
        self.assertNotIn("deleteSocialSchedule", actions)

    def test_admin_includes_schedule_delete(self):
        data = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        actions = lookup_actions.resolve_profile_actions("social-admin", data["profiles"])
        self.assertIn("deleteSocialSchedule", actions)
        self.assertEqual(len(actions), 31)

    def test_importer_parses_dump(self):
        sample = (
            "Authorize On Demand\n"
            "All Tools\n"
            "getSocialPortals Fetches social portals accessible to the authenticated user.\n"
        )
        parsed = import_actions.parse_dump(sample)
        keys = {entry["key"]: entry for entry in parsed}
        self.assertIn("getSocialPortals", keys)


if __name__ == "__main__":
    unittest.main()
