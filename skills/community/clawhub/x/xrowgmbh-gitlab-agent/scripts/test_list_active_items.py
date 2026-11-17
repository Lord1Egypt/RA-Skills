#!/usr/bin/env python3
"""Regression tests for gated GitLab active-item discovery."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("list_active_items", SCRIPT_DIR / "list-active-items.py")
assert spec and spec.loader
active = importlib.util.module_from_spec(spec)
spec.loader.exec_module(active)

USER = {"id": 33363466, "username": "eugene-harold-krabs"}
MEMBERSHIP = {
    "username": USER["username"],
    "access_level": 30,
    "membership_state": "active",
    "created_by": {"username": "xrow"},
}


def item(iid=7, *, kind="issue", labels=None, project="xrow-public/ci-tools"):
    route = "merge_requests" if kind == "merge_request" else "work_items"
    return {
        "project_id": 11721554,
        "iid": iid,
        "title": "assigned item",
        "web_url": f"https://gitlab.com/{project}/-/{route}/{iid}",
        "labels": list(labels or []),
        "assignees": [{"username": USER["username"]}],
        "updated_at": "2026-10-08T10:00:00.000Z",
        "user_notes_count": 0,
    }


class GateTests(unittest.TestCase):
    def test_object_endpoint_validates_url_and_kind(self):
        project, endpoint = active.object_endpoint(item(), "issue")
        self.assertEqual(project, "xrow-public/ci-tools")
        self.assertEqual(endpoint, "projects/xrow-public%2Fci-tools/issues/7")
        _, endpoint = active.object_endpoint(item(kind="merge_request"), "merge_request")
        self.assertTrue(endpoint.endswith("/merge_requests/7"))
        with self.assertRaises(ValueError):
            active.object_endpoint(item(kind="merge_request"), "issue")

    def test_membership_must_be_active_owner_created_and_complete(self):
        cases = [
            (MEMBERSHIP, True),
            ({**MEMBERSHIP, "created_by": {"username": "mallory"}}, False),
            ({**MEMBERSHIP, "membership_state": "blocked"}, False),
            ({**MEMBERSHIP, "access_level": 0}, False),
            ({**MEMBERSHIP, "access_level": True}, False),
            ({key: value for key, value in MEMBERSHIP.items() if key != "created_by"}, False),
        ]
        for membership, expected in cases:
            with self.subTest(membership=membership), patch.object(active, "api_json", return_value=membership):
                self.assertEqual(active.owner_created_membership("xrow-public/ci-tools", USER["id"], USER["username"], "xrow"), expected)

    def test_maintainer_paused_issues_and_mrs_are_not_executable_or_relabelled(self):
        for kind in ("issue", "merge_request"):
            candidate = item(kind=kind)
            # Fresh labels win over the earlier unpaused list snapshot.
            with self.subTest(kind=kind), patch.object(active, "owner_created_membership", return_value=True), patch.object(
                active, "api_json", return_value={"labels": ["workflow::paused", "type::bug"]}
            ), patch.object(active.subprocess, "run") as write:
                self.assertEqual(active.permitted_items([(candidate, kind)], USER["id"], USER["username"], "xrow"), [])
                write.assert_not_called()

    def test_denied_item_is_labeled_and_silently_skipped(self):
        denied = item(labels=["workflow::review", "type::bug"])
        with patch.object(active, "owner_created_membership", return_value=False), patch.object(
            active, "api_json", return_value={"labels": denied["labels"]}
        ), patch.object(active.subprocess, "run") as write:
            self.assertEqual(active.permitted_items([(denied, "issue")], USER["id"], USER["username"], "xrow"), [])
        self.assertEqual(write.call_args.args[0][-4:], ["-f", "add_labels=workflow::forbidden", "-f", "remove_labels=workflow::review"])

    def test_allowed_item_clears_forbidden_and_preserves_other_labels(self):
        allowed = item(labels=["workflow::forbidden", "type::bug"])
        with patch.object(active, "owner_created_membership", return_value=True), patch.object(
            active, "api_json", return_value={"labels": allowed["labels"]}
        ), patch.object(active.subprocess, "run") as write:
            result = active.permitted_items([(allowed, "issue")], USER["id"], USER["username"], "xrow")
        self.assertEqual(result[0]["labels"], ["type::bug"])
        self.assertEqual(write.call_args.args[0][-2:], ["-f", "remove_labels=workflow::forbidden"])

    def test_gate_reuses_membership_per_project_but_checks_each_object_labels(self):
        records = [(item(7), "issue"), (item(8), "issue")]
        with patch.object(active, "owner_created_membership", return_value=True) as member, patch.object(
            active, "api_json", return_value={"labels": []}
        ) as api, patch.object(active.subprocess, "run") as write:
            result = active.permitted_items(records, USER["id"], USER["username"], "xrow")
        self.assertEqual(len(result), 2)
        member.assert_called_once()
        self.assertEqual(api.call_count, 2)
        write.assert_not_called()

    def test_unreadable_labels_fail_closed_without_write(self):
        with patch.object(active, "owner_created_membership", return_value=True), patch.object(
            active, "api_json", return_value={}
        ), patch.object(active.subprocess, "run") as write:
            self.assertEqual(active.permitted_items([(item(), "issue")], USER["id"], USER["username"], "xrow"), [])
        write.assert_not_called()

    def test_owner_skips_membership_check(self):
        with patch.object(active, "owner_created_membership") as member, patch.object(
            active, "api_json", return_value={"labels": []}
        ):
            self.assertEqual(len(active.permitted_items([(item(), "issue")], USER["id"], USER["username"], USER["username"])), 1)
        member.assert_not_called()


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.graphql_variables = []
        def dependencies(_query, variables):
            self.graphql_variables.append(variables)
            return {
                key: {"fullPath": value, "item": {"iid": variables["i" + key[1:]],
                    "linkedWorkItems": {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}
                for key, value in variables.items() if key.startswith("p")
            }
        graphql = patch.object(active, "graphql_json", side_effect=dependencies)
        graphql.start()
        self.addCleanup(graphql.stop)

    @patch.object(active.shutil, "which", return_value="/usr/bin/glab")
    def test_main_gates_before_root_cause_lookup_and_emits_only_allowed(self, _which):
        allowed, denied = item(7), item(8)
        calls = []

        def pages(endpoint):
            calls.append(endpoint)
            if endpoint == "issues?state=opened&scope=assigned_to_me":
                return [allowed, denied]
            if endpoint == "merge_requests?state=opened&scope=assigned_to_me":
                return []
            self.fail(f"unexpected page: {endpoint}")

        def read(endpoint):
            if endpoint == "user":
                return USER
            if endpoint == "projects/11721554":
                return {"id": 11721554, "archived": False}
            if endpoint.endswith("/members/all/33363466"):
                return MEMBERSHIP
            if endpoint.endswith("/issues/7"):
                return {"labels": []}
            if endpoint.endswith("/issues/8"):
                return {"labels": ["workflow::forbidden"]}
            self.fail(f"unexpected read: {endpoint}")

        # Deny one item based on malformed URL before any content or link lookup.
        denied["web_url"] = "https://gitlab.com/wrong/-/work_items/9"
        with patch.object(active, "unassigned_incidents", return_value=[]), patch.object(
            active, "api_json", side_effect=read
        ), patch.object(active, "paginated", side_effect=pages), patch.object(
            active, "configured_owner", return_value="xrow"
        ), patch.object(
            active, "configured_accept_entries", return_value=[]
        ):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(active.main(), 0)
        self.assertEqual([row["iid"] for row in json.loads(output.getvalue())], [7])
        self.assertNotIn("projects/11721554/issues/8/links", calls)
        self.assertEqual([variables["i0"] for variables in self.graphql_variables], ["7"])

    def test_pagination_reads_all_pages(self):
        first_page = [{"iid": value} for value in range(100)]
        with patch.object(active, "api_json", side_effect=[first_page, [{"iid": 100}]]):
            self.assertEqual(len(active.paginated("issues?state=opened")), 101)

    def test_invalid_activity_fails_closed(self):
        with self.assertRaises(ValueError):
            active.normalized({**item(), "user_notes_count": -1}, "issue")

    def test_reads_collaborator_config(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "openclaw.json"
            path.write_text(json.dumps({"skills": {"entries": {"gitlab-agent": {"config": {"collaborators": {"accept": ["xrow"]}}}}}}))
            with patch.dict(os.environ, {active.CONFIG_PATH_ENV: str(path)}):
                self.assertEqual(active.configured_accept_entries(), ["xrow"])


if __name__ == "__main__":
    unittest.main()
