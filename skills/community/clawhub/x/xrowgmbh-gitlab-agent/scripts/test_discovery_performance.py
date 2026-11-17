"""Concurrency, fail-closed and full-discovery equivalence regressions."""

from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import threading
import unittest
from unittest.mock import patch


DIRECTORY = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("benchmark_discovery", DIRECTORY / "benchmark-discovery.py")
bench = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bench)


class DiscoveryPerformanceTests(unittest.TestCase):
    def setUp(self):
        self.active = bench.load_script(DIRECTORY / "list-active-items.py")

    def test_independent_reads_overlap_but_are_bounded_and_keep_input_order(self):
        barrier = threading.Barrier(4, timeout=5)
        lock = threading.Lock()
        counts = {"active": 0, "peak": 0}

        def read(value):
            with lock:
                counts["active"] += 1
                counts["peak"] = max(counts["peak"], counts["active"])
            barrier.wait()
            with lock:
                counts["active"] -= 1
            return value * 2

        self.assertEqual(self.active.parallel_reads(read, range(12)), list(range(0, 24, 2)))
        self.assertEqual(counts["peak"], 4)

    def test_read_failure_propagates_instead_of_becoming_an_empty_success(self):
        def read(value):
            if value == 1:
                raise subprocess.CalledProcessError(1, ["glab", "api"])
            return value
        with self.assertRaises(subprocess.CalledProcessError):
            self.active.parallel_reads(read, range(8))

    def test_label_reads_overlap_after_membership_and_writes_stay_on_caller(self):
        fixture = bench.GitLabFixture(projects=2, items=16, latency_ms=0)
        records = [(row, "issue") for row in fixture.items if row["project_id"] == 1]
        barrier = threading.Barrier(4, timeout=5)
        caller = threading.get_ident()
        reads = Counter()
        lock = threading.Lock()

        def read(endpoint):
            if "/members/all/" in endpoint:
                return fixture.response(endpoint)
            with lock:
                reads[endpoint] += 1
                first = reads[endpoint] == 1
            if first:
                self.assertNotEqual(threading.get_ident(), caller)
                barrier.wait()
            else:
                self.assertEqual(threading.get_ident(), caller)
            return {"labels": ["workflow::forbidden", "keep"]}

        writes = []
        def write(command, **_kwargs):
            self.assertEqual(threading.get_ident(), caller)
            self.assertIn("remove_labels=workflow::forbidden", command)
            writes.append(command)

        with patch.object(self.active, "api_json", side_effect=read), \
                patch.object(self.active.subprocess, "run", side_effect=write):
            result = self.active.permitted_items(records, 99, "robot", "owner")
        self.assertEqual([row["iid"] for row in result], [row["iid"] for row, _ in records])
        self.assertEqual(len(writes), len(records))
        self.assertTrue(all(row["labels"] == ["keep"] for row in result))
        self.assertTrue(all(count == 2 for count in reads.values()))

    def test_changed_labels_are_rechecked_before_serial_mutation(self):
        row = bench.GitLabFixture(projects=2, items=1, latency_ms=0).items[0]
        with patch.object(self.active, "owner_created_membership", return_value=True), \
                patch.object(self.active, "api_json", side_effect=[
                    {"labels": ["workflow::forbidden"]},
                    {"labels": ["workflow::review", "new-human-label"]},
                ]), patch.object(self.active.subprocess, "run") as write:
            result = self.active.permitted_items([(row, "issue")], 99, "robot", "owner")
        write.assert_not_called()
        self.assertEqual(result[0]["labels"], ["new-human-label", "workflow::review"])

    def test_unreadable_object_is_omitted_without_suppressing_its_peer(self):
        fixture = bench.GitLabFixture(projects=3, items=2, latency_ms=0)
        def read(endpoint):
            if endpoint.endswith("/issues/1"):
                raise subprocess.CalledProcessError(1, ["glab", "api"])
            return fixture.response(endpoint)
        records = [(row, "issue" if row["iid"] == 1 else "merge_request") for row in fixture.items]
        with patch.object(self.active, "api_json", side_effect=read), \
                patch.object(self.active.subprocess, "run") as write:
            result = self.active.permitted_items(records, 99, "robot", "owner")
        write.assert_not_called()
        self.assertEqual([row["iid"] for row in result], [2])

    def test_membership_failure_denies_work_and_never_reads_dependency_links(self):
        fixture = bench.GitLabFixture(projects=3, items=12, latency_ms=0)
        original = fixture.response
        def response(endpoint):
            if "/members/all/" in endpoint and "project-1" in endpoint:
                raise subprocess.CalledProcessError(1, ["glab", "api"])
            payload = original(endpoint)
            if "project-1/" in endpoint and "/members/" not in endpoint:
                return {**payload, "labels": ["workflow::forbidden"]}
            return payload
        fixture.response = response
        output, _seconds = bench.run_once(self.active, fixture)
        self.assertTrue(output)
        self.assertTrue(all(row["project_id"] == 2 for row in output))
        self.assertFalse(any(endpoint.startswith("projects/1/issues/") for endpoint in fixture.logical_calls))

    def test_failed_project_metadata_prevents_incident_reads(self):
        with patch.object(self.active, "paginated", return_value=[{"id": 1}, {"id": 2}]) as pages, \
                patch.object(self.active, "api_json", side_effect=lambda ep: {"id": int(ep.split("/")[1])}):
            with self.assertRaises(ValueError):
                self.active.unassigned_incidents({})
        pages.assert_called_once_with("projects?membership=true&simple=true")

    def test_graphql_failure_makes_main_fail_without_emitting_partial_queue(self):
        fixture = bench.GitLabFixture(projects=3, items=12, latency_ms=0)
        output = io.StringIO()
        with patch.object(self.active, "api_json", side_effect=fixture.api_json), \
                patch.object(self.active, "graphql_json", side_effect=ValueError("Unavailable")), \
                patch.object(self.active, "configured_owner", return_value="owner"), \
                patch.object(self.active, "configured_accept_entries", return_value=[]), \
                patch.object(self.active.shutil, "which", return_value="glab"), \
                redirect_stdout(output), redirect_stderr(io.StringIO()):
            self.assertEqual(self.active.main(), 69)
        self.assertEqual(output.getvalue(), "")

    def test_full_main_matches_serial_requests_and_output_across_pages(self):
        serial = bench.load_script(DIRECTORY / "list-active-items.py")
        serial.READ_WORKERS = 1
        result = bench.benchmark(serial, self.active, projects=12, items=240, latency_ms=1, runs=2)
        self.assertTrue(result["output_equivalent"])
        self.assertTrue(result["logical_read_coverage_equivalent"])
        self.assertEqual(result["returned_items"], 220)
        self.assertEqual(result["measurements"]["baseline"]["peak_concurrent_reads"], [1, 1])
        self.assertTrue(all(peak <= 4 for peak in result["measurements"]["candidate"]["peak_concurrent_reads"]))
        print("\nDISCOVERY_BENCHMARK " + json.dumps(result, sort_keys=True))

    def test_benchmark_rejects_output_drift(self):
        serial = bench.load_script(DIRECTORY / "list-active-items.py")
        original = self.active.normalized
        with patch.object(self.active, "normalized", side_effect=lambda *args: {**original(*args), "drift": True}):
            with self.assertRaisesRegex(AssertionError, "differs from baseline"):
                bench.benchmark(serial, self.active, projects=3, items=12, latency_ms=0, runs=1)

    def test_benchmark_rejects_missing_dependency_reads(self):
        serial = bench.load_script(DIRECTORY / "list-active-items.py")
        with patch.object(self.active, "root_cause_flags", side_effect=lambda rows: [False] * len(rows)):
            with self.assertRaisesRegex(AssertionError, "differs from baseline"):
                bench.benchmark(serial, self.active, projects=3, items=12, latency_ms=0, runs=1)

    def test_profile_and_packaged_plugin_use_identical_discovery_code(self):
        root = DIRECTORY.parents[4]
        packaged = root / "container/openclaw/src/extensions/gitlab-agent/scripts/list-active-items.py"
        self.assertEqual((DIRECTORY / "list-active-items.py").read_bytes(), packaged.read_bytes())


if __name__ == "__main__":
    unittest.main()
