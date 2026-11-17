"""Required GraphQL batching and complete dependency-pagination regressions."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("list-active-items.py")


def issue(iid):
    return {"iid": iid, "project_id": 7, "kind": "issue",
            "web_url": f"https://gitlab.example/team/project/-/issues/{iid}"}


def page(iid, states=(), *, more=False, cursor=None):
    return {"fullPath": "team/project", "item": {"iid": str(iid), "linkedWorkItems": {
        "nodes": [{"linkType": "blocks", "workItemState": state} for state in states],
        "pageInfo": {"hasNextPage": more, "endCursor": cursor},
    }}}


class DiscoveryGraphQLTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("graphql_discovery", SCRIPT)
        self.active = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.active)

    def test_uses_variables_and_validates_graphql_errors_even_with_partial_data(self):
        result = subprocess.CompletedProcess([], 0, json.dumps({"data": {"p0": page(1)}}))
        with patch.object(self.active.subprocess, "run", return_value=result) as run:
            self.assertEqual(self.active.graphql_json("query($path: ID!){project(fullPath:$path){id}}",
                                                    {"path": "team/project"}), {"p0": page(1)})
        self.assertIn("path=team/project", run.call_args.args[0])
        self.assertEqual(run.call_args.kwargs["timeout"], 25)
        for payload in ({}, {"data": None}, {"data": {"p0": page(1)}, "errors": [{"message": "partial"}]}):
            with self.subTest(payload=payload), patch.object(
                self.active.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(payload))
            ):
                with self.assertRaises(ValueError):
                    self.active.graphql_json("query{project{id}}", {})

    def test_reads_later_pages_even_after_a_blocking_open_item_was_found(self):
        responses = [
            {"p0": page(1, ["OPEN"], more=True, cursor="next"), "p1": page(2, ["CLOSED"])},
            {"p0": page(1, ["CLOSED"])},
        ]
        with patch.object(self.active, "graphql_json", side_effect=responses) as query, \
                patch.object(self.active, "api_json") as rest:
            self.assertEqual(self.active.root_cause_flags([issue(1), issue(2)]), [True, False])
        rest.assert_not_called()
        self.assertEqual(query.call_count, 2)
        second_query, second_variables = query.call_args.args
        self.assertEqual(second_variables, {"p0": "team/project", "i0": "1", "c0": "next"})
        self.assertNotIn("p1:", second_query)

    def test_open_dependency_on_a_later_page_is_not_missed(self):
        with patch.object(self.active, "graphql_json", side_effect=[
            {"p0": page(1, ["CLOSED"], more=True, cursor="next")}, {"p0": page(1, ["OPEN"])},
        ]):
            self.assertEqual(self.active.root_cause_flags([issue(1)]), [True])

    def test_invalid_or_partial_pages_fail_without_rest_fallback(self):
        bad_pages = [None, {}, page(99), {**page(1), "fullPath": "other/project"},
                     page(1, ["UNKNOWN"]), page(1, more=True), page(1, more=True, cursor="")]
        for field, value in (("nodes", None), ("nodes", {}), ("pageInfo", {}),
                             ("pageInfo", {"hasNextPage": "false"}),
                             ("nodes", [{"linkType": "relates_to", "workItemState": "OPEN"}])):
            broken = deepcopy(page(1))
            broken["item"]["linkedWorkItems"][field] = value
            bad_pages.append(broken)
        for broken in bad_pages:
            with self.subTest(page=broken), patch.object(self.active, "graphql_json", return_value={"p0": broken}), \
                    patch.object(self.active, "api_json") as rest:
                with self.assertRaises(ValueError):
                    self.active.root_cause_flags([issue(1)])
                rest.assert_not_called()

    def test_repeated_cursor_fails_instead_of_looping_or_returning_partial_success(self):
        with patch.object(self.active, "graphql_json", return_value={"p0": page(1, more=True, cursor="same")}) as query:
            with self.assertRaisesRegex(ValueError, "cursor did not advance"):
                self.active.root_cause_flags([issue(1)])
        self.assertEqual(query.call_count, 2)

    def test_batches_at_most_ten_issues_and_keeps_result_order(self):
        sizes = []
        def read(_query, variables):
            keys = [key for key in variables if key.startswith("p")]
            sizes.append(len(keys))
            return {key: page(int(variables["i" + key[1:]]),
                              ["OPEN"] if int(variables["i" + key[1:]]) % 3 == 0 else []) for key in keys}
        with patch.object(self.active, "graphql_json", side_effect=read):
            result = self.active.root_cause_flags([issue(value) for value in range(1, 26)])
        self.assertEqual(sorted(sizes), [5, 10, 10])
        self.assertEqual(result, [value % 3 == 0 for value in range(1, 26)])

    def test_empty_queue_does_not_issue_a_graphql_query(self):
        with patch.object(self.active, "graphql_json") as query:
            self.assertEqual(self.active.root_cause_flags([]), [])
        query.assert_not_called()

    def test_graphql_transport_failure_propagates_without_rest_fallback(self):
        with patch.object(self.active, "graphql_json", side_effect=subprocess.TimeoutExpired("glab", 25)), \
                patch.object(self.active, "api_json") as rest:
            with self.assertRaises(subprocess.TimeoutExpired):
                self.active.root_cause_flags([issue(1)])
        rest.assert_not_called()


if __name__ == "__main__":
    unittest.main()
