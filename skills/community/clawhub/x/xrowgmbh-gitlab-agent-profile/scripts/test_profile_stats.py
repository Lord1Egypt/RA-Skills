#!/usr/bin/env python3
"""Offline regression coverage for group discovery and profile publication."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
from datetime import date
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

spec = importlib.util.spec_from_file_location("profile_stats", Path(__file__).with_name("update-profile-stats.py"))
stats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stats)


def project(pid=1, name="group/public", visibility="public", branch="main", **extra):
    return {"id": pid, "path_with_namespace": name, "visibility": visibility,
            "default_branch": branch, "empty_repo": False, **extra}


def mr(author="agent", merged="2026-08-15T12:00:00Z", **extra):
    return {"merged_at": merged, "title": "feat: example", "labels": ["size::medium"],
            "author": {"username": author}, "merge_user": {"username": "owner"},
            "reviewers": [], "web_url": "https://gitlab.example/group/public/-/merge_requests/1", **extra}


def commit(sha="direct", when="2026-08-16T12:00:00Z", **extra):
    return {"id": sha, "committed_date": when, "title": "fix: example",
            "author_name": "Owner", "committer_name": "Owner", **extra}


class CompletedMonthsTests(unittest.TestCase):
    def test_last_twelve_completed_months(self):
        months = stats.month_keys(12, date(2026, 9, 8))
        self.assertEqual(months, [
            "2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02",
            "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08",
        ])

    def test_first_and_last_day_both_exclude_current_month(self):
        for today in [date(2026, 9, 1), date(2026, 9, 30)]:
            self.assertEqual(stats.month_keys(1, today), ["2026-08"])

    def test_year_rollover(self):
        self.assertEqual(stats.month_keys(3, date(2026, 1, 1)), ["2025-10", "2025-11", "2025-12"])

    def test_leap_year(self):
        self.assertEqual(stats.month_keys(2, date(2024, 3, 1)), ["2024-01", "2024-02"])
        self.assertEqual(stats.month_keys(1, date(2024, 2, 29)), ["2024-01"])

    def test_invalid_month_count(self):
        for value in [0, -1]:
            with self.assertRaises(ValueError):
                stats.month_keys(value, date(2026, 9, 8))


class DiscoveryTests(unittest.TestCase):
    def test_group_pagination_includes_subgroups_archived_and_private_projects(self):
        first = [project(pid, f"group/project-{pid}") for pid in range(1, 101)]
        last = project(101, "group/subgroup/archive", "private", "master", archived=True)
        with patch.object(stats, "glab_json", side_effect=[first, [first[0], last], []]) as api:
            found = stats.resolve_projects(None, "group")
        self.assertEqual(len(found), 101)
        self.assertIn(last, found)
        paths = [call.args[0] for call in api.call_args_list]
        self.assertEqual(len(paths), 3)
        self.assertTrue(all("include_subgroups=true&with_shared=false" in path for path in paths))
        self.assertIn("per_page=100&page=2", paths[1])
        self.assertIn("order_by=id&sort=asc", paths[0])

    def test_nested_group_is_url_encoded_and_blank_override_uses_discovery(self):
        with patch.object(stats, "paginated", return_value=[project(name="parent/group/repo")]) as pages:
            stats.resolve_projects("  ", "parent/group")
        self.assertTrue(pages.call_args.args[0].startswith("/groups/parent%2Fgroup/projects?"))

    def test_explicit_projects_override_discovery_and_are_deduplicated(self):
        with patch.object(stats, "paginated", side_effect=AssertionError("unexpected group query")), patch.object(
            stats, "glab_json", side_effect=[project(name="group/a"), project(2, "other/b")]
        ) as api:
            result = stats.resolve_projects("a,group/a\nother/b", "group")
        self.assertEqual(len(result), 2)
        self.assertEqual([call.args[0] for call in api.call_args_list], ["/projects/group%2Fa", "/projects/other%2Fb"])

    def test_shared_outside_project_is_rejected(self):
        with patch.object(stats, "paginated", return_value=[project(name="outside/repo")]):
            with self.assertRaisesRegex(ValueError, "namespace"):
                stats.resolve_projects(None, "group")

    def test_missing_visibility_or_default_branch_fails_closed(self):
        for value in [project(visibility=None), project(branch=None), {"id": 1}]:
            with patch.object(stats, "glab_json", return_value=value):
                with self.assertRaises(ValueError):
                    stats.resolve_projects("public", "group")

    def test_empty_and_disabled_repositories_can_have_no_default_branch(self):
        for value in [project(branch=None, empty_repo=True), project(branch=None, repository_access_level="disabled")]:
            with patch.object(stats, "glab_json", return_value=value):
                self.assertEqual(stats.resolve_projects("public", "group"), [value])

    def test_api_errors_and_non_list_pages_do_not_become_empty_statistics(self):
        with patch.object(stats, "glab_json", return_value={"message": "error"}):
            with self.assertRaisesRegex(ValueError, "paginated"):
                stats.paginated("/groups/group/projects")
        with patch.object(stats.subprocess, "run", side_effect=subprocess.CalledProcessError(
            1, ["glab"], stderr="private project details"
        )):
            with self.assertRaisesRegex(RuntimeError, "collection is incomplete") as raised:
                stats.glab_json("/private/path")
        self.assertNotIn("private", str(raised.exception))


class CollectionTests(unittest.TestCase):
    def collect(self, projects, pages):
        with patch.object(stats, "username_display_name", return_value="Owner"), patch.object(
            stats, "paginated", side_effect=pages
        ) as api, contextlib.redirect_stderr(io.StringIO()):
            result = stats.collect_stats(projects, "owner", "agent", ["2026-08"])
        return result, api

    def test_default_branch_and_complete_month_filtering_preserve_mr_classification(self):
        public = project(branch="release/1")
        private = project(2, "group/confidential", "private", "master")
        public_mrs = [
            mr(labels=["type::feature", "size::large"], merge_commit_sha="merged"),
            mr("owner", squash_commit_sha="squashed"),
            mr(title="chore: ignore", labels=["type::feature"], merge_commit_sha="ignored-merge"),
            mr(merged="2026-09-01T00:00:00Z"),
            mr(merged="2026-07-31T23:59:59Z"),
        ]
        public_commits = [
            commit(), commit("merged"), commit("squashed"), commit("ignored-merge"),
            commit("partial", "2026-09-01T00:00:00Z"), commit("old", "2026-07-31T23:59:59Z"),
            commit("skip", title="docs: ignore"),
        ]
        private_mrs = [mr(merge_user={"username": "agent"}, labels=[])]
        (monthly, records), api = self.collect([public, private], [public_mrs, public_commits, private_mrs, [commit("private-direct")]])
        month = monthly[0]
        self.assertEqual((month.owner_mrs, month.agent_with_owner, month.agent_autonomous, month.direct_owner_main), (1, 1, 1, 2))
        self.assertAlmostEqual(month.contribution_score, 6.4)
        self.assertEqual(len(records), 5)
        self.assertEqual(records, sorted(records, key=lambda row: row["date"], reverse=True))
        queries = [parse_qs(urlsplit(call.args[0]).query) for call in api.call_args_list if "repository/commits" in call.args[0]]
        self.assertEqual([query["ref_name"] for query in queries], [["release/1"], ["master"]])
        self.assertEqual(queries[0]["until"], ["2026-09-01T00:00:00Z"])
        self.assertEqual(queries[0]["since"], ["2026-08-01T00:00:00Z"])

    def test_known_merge_commit_exclusion_is_scoped_to_its_project(self):
        (monthly, _), _ = self.collect(
            [project(), project(2, "group/second")],
            [[mr(merge_commit_sha="same-sha")], [], [], [commit("same-sha")]],
        )
        self.assertEqual(monthly[0].direct_owner_main, 1)

    def test_empty_and_disabled_features_do_not_call_unavailable_apis(self):
        projects = [
            project(empty_repo=True, branch=None),
            project(2, "group/disabled", branch=None, repository_access_level="disabled", merge_requests_enabled=False),
        ]
        (monthly, records), api = self.collect(projects, AssertionError("unexpected API request"))
        api.assert_not_called()
        self.assertEqual(monthly[0].contribution_score, 0)
        self.assertEqual(records, [])


class PublicationTests(unittest.TestCase):
    def test_private_records_are_anonymized_and_still_reconcile_with_totals(self):
        projects = [project(), project(2, "group/confidential-name", "private"), project(3, "group/internal-name", "internal")]
        records = [
            {"date": "2026-08-20T00:00:00Z", "month": "2026-08", "visibility": "public", "kind": "merge_request",
             "category": "owner", "points": 1, "project": "group/public", "title": "feat: public"},
            {"date": "2026-08-19T00:00:00Z", "month": "2026-08", "visibility": "private", "kind": "merge_request",
             "category": "agent_autonomous", "points": 2, "project": "group/confidential-name", "title": "private-title",
             "url": "https://private.example/hidden", "reference": "private-sha", "reviewers": ["private-reviewer"]},
            {"date": "2026-08-18T00:00:00Z", "month": "2026-08", "visibility": "internal", "kind": "merge_request",
             "category": "agent_autonomous", "points": 1, "project": "group/internal-name", "title": "internal-title"},
        ]
        monthly = [stats.MonthStats("2026-08", 1, 0, 2, 0, 1, 0, 3)]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "proof.json"
            stats.write_records(output, records, monthly, projects)
            text = output.read_text()
            data = json.loads(text)
        for private_value in ["confidential-name", "internal-name", "private-title", "internal-title", "private.example", "private-sha", "private-reviewer"]:
            self.assertNotIn(private_value, text)
        self.assertEqual(data["records"], records[:1])
        self.assertEqual(data["private_monthly_totals"], [
            {"month": "2026-08", "kind": "merge_request", "category": "agent_autonomous", "count": 2, "points": 3.0},
        ])
        self.assertEqual(data["coverage"]["project_count"], 3)
        self.assertEqual(data["coverage"]["private_project_count"], 2)
        self.assertEqual(data["coverage"]["public_projects"], ["group/public"])
        self.assertEqual(data["period"], {"first_month": "2026-08", "last_month": "2026-08", "completed_months_only": True})
        self.assertEqual(sum(row["points"] for row in data["records"]) + sum(row["points"] for row in data["private_monthly_totals"]),
                         data["months"][0]["contribution_score"])

    def test_collection_failure_preserves_previous_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            assets = Path(directory) / "assets"
            assets.mkdir()
            for name in ["gitlab-agent-profile.svg", "gitlab-agent-profile.webp", "gitlab-agent-profile-records.json"]:
                (assets / name).write_bytes(b"previous snapshot")
            with patch.dict(os.environ, {"GITLAB_AGENT_PROFILE_WORKSPACE": directory, "GITLAB_AGENT_PROFILE_AGENT_USERNAME": "agent"}, clear=True), patch.object(
                stats, "resolve_projects", return_value=[project()]
            ), patch.object(stats, "collect_stats", side_effect=RuntimeError("API unavailable")):
                with self.assertRaisesRegex(RuntimeError, "API unavailable"):
                    stats.main()
            self.assertTrue(all(path.read_bytes() == b"previous snapshot" for path in assets.iterdir()))


if __name__ == "__main__":
    unittest.main()
