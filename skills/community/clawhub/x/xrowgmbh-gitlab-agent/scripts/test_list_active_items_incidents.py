"""Regression tests for incident adoption during active-work discovery."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("list-active-items.py")
SPEC = importlib.util.spec_from_file_location("list_active_items", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class IncidentDiscoveryTests(unittest.TestCase):
    def test_lists_unassigned_incidents_across_member_projects(self):
        incident = {"iid": 2, "issue_type": "incident", "assignees": []}

        def pages(endpoint):
            if endpoint == "projects?membership=true&simple=true":
                return [{"id": 7}, {"id": 8}]
            if endpoint.startswith("projects/7/"):
                return [incident]
            return []
        def project(endpoint):
            project_id = int(endpoint.split("/")[1])
            return {"id": project_id, "archived": False}
        with patch.object(module, "paginated", side_effect=pages) as paginated, patch.object(
            module, "api_json", side_effect=project
        ):
            self.assertEqual(module.unassigned_incidents({}), [incident])
        self.assertEqual(paginated.call_count, 3)

    def test_skips_inactive_projects_before_reading_incidents(self):
        projects = [
            {"id": 7, "archived": True},
            {"id": 8, "archived": False, "marked_for_deletion_at": "2026-10-01"},
            {"id": 9, "archived": False, "forked_from_project": {"id": 1}},
            {"id": 10, "archived": False},
        ]
        def pages(endpoint):
            if endpoint == "projects?membership=true&simple=true":
                return [{"id": project["id"]} for project in projects]
            self.assertEqual(endpoint, "projects/10/issues?state=opened&issue_type=incident&assignee_id=None")
            return []
        with patch.object(module, "paginated", side_effect=pages) as paginated, patch.object(
            module, "api_json", side_effect=lambda endpoint: projects[int(endpoint.split("/")[1]) - 7]
        ) as api:
            self.assertEqual(module.unassigned_incidents({}), [])
        self.assertEqual(paginated.call_count, 2)
        self.assertEqual(api.call_count, 4)

    def test_project_metadata_is_cached_and_incomplete_metadata_fails_closed(self):
        cache = {}
        with patch.object(module, "api_json", return_value={"id": 7, "archived": False}) as api:
            self.assertTrue(module.project_is_active(7, cache))
            self.assertTrue(module.project_is_active(7, cache))
        api.assert_called_once_with("projects/7")
        with patch.object(module, "api_json", return_value={"id": 8}):
            with self.assertRaises(ValueError):
                module.project_is_active(8, cache)

    def test_maintainer_hold_prevents_even_critical_incident_adoption(self):
        item = {"iid": 2, "web_url": "https://gitlab.com/team/project/-/issues/2"}
        current = {"issue_type": "incident", "state": "opened", "assignees": [],
                   "labels": ["workflow::paused"], "severity": "CRITICAL"}
        with patch.object(module, "owner_created_membership", return_value=True), patch.object(
            module, "api_json", return_value=current
        ), patch.object(module.subprocess, "run") as write:
            self.assertIsNone(module.adopt_incident(item, "agent", 12, "owner"))
            write.assert_not_called()

    def test_adopts_critical_incident_after_membership_gate(self):
        item = {"project_id": 7, "iid": 2, "web_url": "https://gitlab.com/team/project/-/issues/2"}
        current = {
            "issue_type": "incident", "state": "opened", "assignees": [],
            "labels": ["priority::low", "workflow::backlog", "keep"], "severity": "CRITICAL",
        }
        adopted = {**current, "assignees": [{"username": "agent"}]}
        with patch.object(module, "owner_created_membership", return_value=True) as member, patch.object(
            module, "api_json", side_effect=[current, current]
        ) as api, patch.object(
            module.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(adopted))
        ) as run:
            self.assertEqual(module.adopt_incident(item, "agent", 12, "owner"), adopted)
        member.assert_called_once_with("team/project", 12, "agent", "owner")
        self.assertEqual(api.call_count, 2)
        command = run.call_args.args[0]
        self.assertIn("assignee_ids=12", command)
        self.assertIn("add_labels=priority::blocker,type::support,workflow::in-progress", command)
        self.assertIn("remove_labels=priority::low,workflow::backlog", command)

    def test_denied_gate_only_replaces_workflow_label(self):
        item = {"project_id": 7, "iid": 2, "web_url": "https://gitlab.com/team/project/-/issues/2"}
        with patch.object(module, "owner_created_membership", return_value=False), patch.object(
            module, "api_json", return_value={"labels": ["workflow::backlog", "keep"]}
        ) as api, patch.object(module.subprocess, "run") as run:
            self.assertIsNone(module.adopt_incident(item, "agent", 12, "owner"))
        api.assert_called_once_with("projects/team%2Fproject/issues/2")
        command = run.call_args.args[0]
        self.assertIn("add_labels=workflow::forbidden", command)
        self.assertIn("remove_labels=workflow::backlog", command)
        self.assertFalse(any(arg.startswith("assignee_ids=") for arg in command))

    def test_assigned_incident_is_not_overwritten(self):
        item = {"project_id": 7, "iid": 2, "web_url": "https://gitlab.com/team/project/-/issues/2"}
        current = {
            "issue_type": "incident", "state": "opened",
            "assignees": [{"username": "human"}], "labels": [],
        }
        with patch.object(module, "owner_created_membership", return_value=True), patch.object(
            module, "api_json", return_value=current
        ), patch.object(module.subprocess, "run") as run:
            self.assertIsNone(module.adopt_incident(item, "agent", 12, "owner"))
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
