"""#144 requirements: ordered read-only work, metadata, scripts and to-dos."""

import importlib.util
import io
import json
import subprocess
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("queue_report", Path(__file__).with_name("work-queue-report.py"))
queue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue)


def item(iid, *, kind="issue", labels=None):
    return {
        "project_id": 42, "iid": iid, "title": f"Item {iid}", "state": "opened",
        "issue_type": "incident" if kind == "incident" else "issue",
        "web_url": f"https://gitlab.com/team/project/-/{'merge_requests' if kind == 'merge_request' else 'issues'}/{iid}",
        "assignees": [{"username": "robot"}], "labels": labels or [],
        "updated_at": "2026-10-01T12:00:00Z", "user_notes_count": 0,
        "created_at": "2026-09-01T12:00:00Z", "time_stats": {"total_time_spent": 5400},
    }


class QueueReportTests(unittest.TestCase):
    def test_failure_categories_preserve_cause_without_authenticated_details(self):
        cases = [
            (subprocess.CalledProcessError(1, ["private-command"], stderr="private-token (HTTP 401)"), "gitlab-authentication"),
            (subprocess.CalledProcessError(1, [], stderr=b"private-token (HTTP 403)"), "gitlab-permission"),
            (subprocess.CalledProcessError(1, [], stderr="private-token (HTTP 429)"), "gitlab-rate-limit"),
            (subprocess.CalledProcessError(1, [], stderr="private-token (HTTP 503)"), "gitlab-unavailable"),
            (subprocess.CalledProcessError(1, [], stderr="HTTP 401 HTTP 403 private-token"), "gitlab-api"),
            (subprocess.TimeoutExpired("private-command", 25, stderr="private-token"), "gitlab-timeout"),
            (FileNotFoundError("private-path"), "helper-unavailable"),
            (ValueError("private-token"), "report-invalid"),
        ]
        for error, expected in cases:
            stdout, stderr = io.StringIO(), io.StringIO()
            with self.subTest(code=expected), patch.object(queue, "report", side_effect=error), \
                    redirect_stdout(stdout), redirect_stderr(stderr):
                self.assertEqual(queue.main(), 1)
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "WORK_QUEUE_ERROR=" + json.dumps({"error_code": expected}) + "\n")
            self.assertNotIn("private", stderr.getvalue())

    def setUp(self):
        dependencies = patch.object(queue.active, "root_cause_flags", side_effect=lambda rows: [False] * len(rows))
        dependencies.start()
        self.addCleanup(dependencies.stop)

    def run_report(self, issues=(), mrs=(), todos=(), current=None, member=True, related=None):
        candidates = [*issues, *mrs]

        def api(endpoint):
            if endpoint == "user":
                return {"id": 7, "username": "robot", "name": "Robot"}
            for row in candidates:
                if endpoint == queue.active.object_endpoint(row, "merge_request" if row in mrs else "issue")[1]:
                    return current if current is not None else row
            raise AssertionError(endpoint)

        def pages(endpoint):
            if endpoint.startswith("issues?state"):
                return list(issues)
            if endpoint.startswith("merge_requests?state"):
                return list(mrs)
            if endpoint == "todos?state=pending":
                return list(todos)
            if endpoint.endswith("/related_merge_requests"):
                return list((related or {}).get(int(endpoint.split("/")[-2]), []))
            return []

        with patch.object(queue, "read_api", side_effect=api), \
                patch.object(queue.active, "paginated", side_effect=pages), \
                patch.object(queue.active, "configured_owner", return_value="owner"), \
                patch.object(queue.active, "project_is_active", return_value=True), \
                patch.object(queue.active, "owner_created_membership", return_value=member), \
                patch.object(queue.active, "synchronize_forbidden") as labels, \
                patch.object(queue.active, "assign_unassigned_items") as assign, \
                patch.object(queue.active, "adopt_incident") as adopt:
            result = queue.report()
            # Opening a report must not perform scheduled agent mutations.
            labels.assert_not_called()
            assign.assert_not_called()
            adopt.assert_not_called()
            return result

    def test_related_mr_states_are_metadata_not_discovery_filtering(self):
        result = self.run_report([item(i) for i in range(1, 5)], [item(9, kind="merge_request")], related={
            1: [{"state": "opened"}], 2: [{"state": "closed"}, {"state": "merged"}],
            4: [{"state": "merged"}, {"state": "opened"}],
        })
        self.assertEqual(len(result["items"]), 5)
        self.assertEqual({r["iid"]: r.get("has_open_merge_request") for r in result["items"]},
                         {1: True, 2: False, 3: False, 4: True, 9: None})

    def test_incomplete_related_mr_state_fails_instead_of_inventing_visibility(self):
        for related in [[{}], [{"state": "unknown"}], [None]]:
            with self.subTest(related=related), self.assertRaises(ValueError):
                self.run_report([item(1)], related={1: related})

    def test_created_kind_labels_and_total_time_are_visible(self):
        incident = item(1, kind="incident", labels=["priority::high", "size::small", "type::support"])
        mr = item(2, kind="merge_request")
        result = self.run_report([incident], [mr])
        self.assertEqual(result["items"][0]["kind"], "incident")
        self.assertEqual(result["items"][0]["created_at"], incident["created_at"])
        self.assertEqual(result["items"][0]["updated_at"], incident["updated_at"])
        self.assertEqual(result["items"][0]["project_path"], "team/project")
        self.assertEqual(result["items"][0]["labels"], incident["labels"])
        self.assertEqual(result["items"][0]["time_spent"], 5400)
        self.assertEqual(result["items"][1]["kind"], "merge_request")

    def test_reuses_discovery_priority_and_blocking_order(self):
        low, high, blocker, root = [item(i, labels=[priority]) for i, priority in (
            (1, "priority::low"), (2, "priority::high"), (3, "priority::blocker"), (4, "priority::high"))]
        with patch.object(queue.active, "root_cause_flags", side_effect=lambda rows: [row["iid"] == 4 for row in rows]):
            result = self.run_report([low, high, blocker, root])
        self.assertEqual([row["iid"] for row in result["items"]], [3, 4, 2, 1])

    def test_denied_unassigned_closed_and_unreadable_labels_are_omitted(self):
        row = item(1)
        self.assertEqual(self.run_report([row], member=False)["items"], [])
        for change in ({"assignees": []}, {"state": "closed"}, {"labels": None}):
            with self.subTest(change=change):
                self.assertEqual(self.run_report([row], current={**row, **change})["items"], [])

    def test_least_recent_activity_first_within_each_priority(self):
        for priority in ("blocker", "high", "medium", "low", None):
            with self.subTest(priority=priority):
                labels = [f"priority::{priority}"] if priority else []
                unattended = {**item(1, kind="merge_request", labels=labels),
                              "created_at": "2026-10-01T12:00:00Z"}
                recently_worked = {**item(9, labels=labels),
                                   "created_at": "2026-09-01T12:00:00Z",
                                   "updated_at": "2026-10-20T12:00:00Z"}
                result = self.run_report([recently_worked], [unattended])
                self.assertEqual([row["iid"] for row in result["items"]], [1, 9])

    def test_read_only_report_retains_maintainer_holds_and_shared_activity_order(self):
        unattended = {**item(9, labels=["workflow::paused"]),
                      "project_id": 99,
                      "web_url": "https://gitlab.com/other/project/-/issues/9",
                      "created_at": "2026-08-01T12:00:00Z",
                      "updated_at": "2026-09-01T12:00:00Z"}
        new = {**item(1, kind="merge_request"), "created_at": "2026-10-01T12:00:00Z"}
        result = self.run_report([unattended], [new])
        self.assertEqual([row["iid"] for row in result["items"]], [9, 1])
        self.assertEqual(result["items"][0]["labels"], ["workflow::paused"])
        unattended["updated_at"] = "2026-10-20T12:00:00Z"
        result = self.run_report([unattended], [new])
        self.assertEqual([row["iid"] for row in result["items"]], [1, 9])

    def test_priority_precedes_age_and_timezone_offsets_are_respected(self):
        old = {**item(1), "updated_at": "2026-09-01T12:00:00Z"}
        urgent = {**item(2, labels=["priority::blocker"]),
                  "updated_at": "2026-11-01T12:00:00Z"}
        self.assertEqual([row["iid"] for row in self.run_report([old, urgent])["items"]], [2, 1])
        old["updated_at"] = "2026-10-01T13:00:00+02:00"
        self.assertEqual([row["iid"] for row in self.run_report([item(3), old])["items"]], [1, 3])

    def test_discovery_and_report_share_activity_order_without_mutating_input(self):
        first, second = item(9), item(1, kind="merge_request")
        first["updated_at"] = "2026-09-01T12:00:00Z"
        normalized = [queue.active.normalized(first, "issue"),
                      queue.active.normalized(second, "merge_request")]
        before = json.dumps(normalized)
        direct = queue.active.order_items(normalized)
        report = self.run_report([first], [second])["items"]
        self.assertEqual([row["web_url"] for row in direct], [row["web_url"] for row in report])
        self.assertEqual(json.dumps(normalized), before)
        # Older normalized callers expose activity only through the cursor.
        for row in normalized:
            row.pop("updated_at")
        self.assertEqual([row["iid"] for row in queue.active.order_items(normalized)], [9, 1])

    def test_pending_todos_include_other_actions_and_preserve_api_order(self):
        todos = [{"id": n, "state": "pending", "target": {"title": str(n), "labels": [],
                  "updated_at": "2026-10-01T12:00:00Z"},
                  "project": {"path_with_namespace": "team/project"},
                  "author": {"username": "owner"}, "action_name": action,
                  "target_url": "https://gitlab.com/team/project/-/issues/1#note_2"}
                 for n, action in [(9, "directly_addressed"), (3, "assigned")]]
        result = self.run_report(todos=todos + [{"state": "done"}])
        self.assertEqual([todo["id"] for todo in result["todos"]], [9, 3])
        self.assertEqual(result["todos"][0]["updated_at"], "2026-10-01T12:00:00Z")
        self.assertEqual(result["todos"][0]["project_path"], "team/project")
        self.assertEqual([todo["owner_addressed"] for todo in result["todos"]], [True, False])

    def test_shows_actual_existing_script_sources(self):
        sources = self.run_report()["scripts"]
        by_name = {entry["name"]: entry for entry in sources}
        for name in ("list-active-items.py", "list-directly-addressed-todos.py"):
            self.assertEqual(by_name[name]["source"], (queue.SCRIPT_DIR / name).read_text())

    def test_api_uses_only_bounded_read_command(self):
        with patch.object(queue.subprocess, "run") as run:
            run.return_value.stdout = "[]"
            self.assertEqual(queue.read_api("todos?state=pending"), [])
        self.assertEqual(run.call_args.args[0], ["glab", "api", "todos?state=pending"])
        self.assertEqual(run.call_args.kwargs["timeout"], 25)
        self.assertNotIn("shell", run.call_args.kwargs)


if __name__ == "__main__":
    unittest.main()
