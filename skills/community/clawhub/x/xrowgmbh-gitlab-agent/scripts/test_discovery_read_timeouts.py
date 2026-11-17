"""Bounded timeout recovery without stale responses, partial queues or write retries."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch


DIRECTORY = Path(__file__).resolve().parent


def load():
    spec = importlib.util.spec_from_file_location("read_timeouts", DIRECTORY / "list-active-items.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def response(payload):
    return subprocess.CompletedProcess([], 0, stdout=json.dumps(payload))


class DiscoveryReadTimeoutTests(unittest.TestCase):
    def setUp(self):
        self.active = load()
        sleep_patch = patch("time.sleep")
        self.sleep = sleep_patch.start()
        self.addCleanup(sleep_patch.stop)
        self.stderr = io.StringIO()
        self.redirect = redirect_stderr(self.stderr)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)

    def timeout(self):
        return subprocess.TimeoutExpired(["glab", "api", "incident-query"], 25)

    def test_incident_get_retries_once_then_returns_live_response(self):
        endpoint = "projects/1/issues?state=opened&issue_type=incident&assignee_id=None"
        with patch.object(self.active.subprocess, "run", side_effect=[self.timeout(), response([])]) as run:
            self.assertEqual(self.active.api_json(endpoint), [])
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[0], run.call_args_list[1])
        self.assertEqual(run.call_args.kwargs["timeout"], 25)
        self.sleep.assert_called_once_with(1)
        self.assertIn("retrying once", self.stderr.getvalue())

    def test_pagination_retries_same_page_without_skipping_or_duplicating(self):
        self.active.PER_PAGE = 2
        first = [{"id": 1}, {"id": 2}]
        with patch.object(self.active.subprocess, "run", side_effect=[response(first), self.timeout(), response([])]) as run:
            self.assertEqual(self.active.paginated("issues?scope=assigned_to_me"), first)
        self.assertEqual(run.call_count, 3)
        self.assertEqual(run.call_args_list[1], run.call_args_list[2])
        self.assertIn("page=2", run.call_args.args[0][-1])

    def test_collaborator_scan_keeps_candidates_after_transient_timeout(self):
        item = {"id": 100, "iid": 7, "project_id": 1, "issue_type": "issue", "assignees": [],
                "web_url": "https://gitlab.example/team/app/-/issues/7"}
        with patch.object(self.active, "active_member_projects", return_value=[{"id": 1, "path_with_namespace": "team/app"}]), \
                patch.object(self.active.subprocess, "run", side_effect=[self.timeout(), response([item])]) as run:
            self.assertEqual(self.active.assignment_candidates(99, "owner", "owner", {}), [item])
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[0], run.call_args_list[1])

    def test_repeated_timeouts_are_bounded_and_propagate(self):
        with patch.object(self.active.subprocess, "run", side_effect=self.timeout()) as run:
            with self.assertRaises(subprocess.TimeoutExpired):
                self.active.api_json("user")
        self.assertEqual(run.call_count, 2)
        self.sleep.assert_called_once_with(1)

    def test_http_errors_are_not_retried(self):
        for status in (401, 403, 404, 429, 500):
            with self.subTest(status=status), patch.object(
                self.active.subprocess, "run",
                side_effect=subprocess.CalledProcessError(1, ["glab", "api"], stderr=f"HTTP {status}"),
            ) as run:
                with self.assertRaises(subprocess.CalledProcessError):
                    self.active.api_json("user")
                run.assert_called_once()
        self.sleep.assert_not_called()

    def test_malformed_json_is_not_retried(self):
        with patch.object(self.active.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout="broken")) as run:
            with self.assertRaises(json.JSONDecodeError):
                self.active.api_json("user")
        run.assert_called_once()
        self.sleep.assert_not_called()

    def test_graphql_timeout_retries_identical_query_without_rest_fallback(self):
        with patch.object(self.active.subprocess, "run", side_effect=[self.timeout(), response({"data": {"p0": {}}})]) as run:
            self.assertEqual(self.active.graphql_json("query($p: ID!){project(fullPath:$p){id}}", {"p": "team/app"}), {"p0": {}})
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[0], run.call_args_list[1])
        self.assertTrue(all(call.args[0][2] == "graphql" for call in run.call_args_list))
        self.assertNotIn("team/app", self.stderr.getvalue())

    def test_graphql_errors_or_partial_data_are_not_retried(self):
        for payload in ({"errors": [{"message": "denied"}], "data": {}}, {"data": None}):
            with self.subTest(payload=payload), patch.object(self.active.subprocess, "run", return_value=response(payload)) as run:
                with self.assertRaises(ValueError):
                    self.active.graphql_json("query{currentUser{id}}", {})
                run.assert_called_once()
        self.sleep.assert_not_called()

    def test_label_mutation_timeout_is_never_retried(self):
        with patch.object(self.active, "api_json", return_value={"labels": ["workflow::forbidden"]}), \
                patch.object(self.active.subprocess, "run", side_effect=self.timeout()) as run:
            with self.assertRaises(subprocess.TimeoutExpired):
                self.active.synchronize_forbidden("projects/team%2Fapp/issues/1", allowed=True)
        run.assert_called_once()
        self.assertEqual(run.call_args.args[0][2:4], ["-X", "PUT"])
        self.sleep.assert_not_called()

    def test_exhausted_incident_read_makes_main_fail_without_partial_queue(self):
        output = io.StringIO()
        def incidents(_cache):
            self.active.api_json("projects/1/issues?issue_type=incident")
            return []
        with patch.object(self.active.shutil, "which", return_value="glab"), \
                patch.object(self.active, "configured_owner", return_value="owner"), \
                patch.object(self.active, "unassigned_incidents", side_effect=incidents), \
                patch.object(self.active.subprocess, "run", side_effect=[response({"id": 99, "username": "robot"}), self.timeout(), self.timeout()]) as run, \
                redirect_stdout(output):
            self.assertEqual(self.active.main(), 69)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(run.call_count, 3)


if __name__ == "__main__":
    unittest.main()
