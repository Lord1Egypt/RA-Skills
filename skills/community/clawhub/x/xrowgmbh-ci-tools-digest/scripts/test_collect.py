"""Calendar coverage and fail-closed GitLab collection regressions."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from datetime import datetime, timezone
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("digest_collect", Path(__file__).with_name("collect.py"))
collect = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collect)


def at(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def release(tag, timestamp):
    return {"tag_name": tag, "released_at": timestamp}


def mr(iid, timestamp, **extra):
    return {"iid": iid, "title": f"Change {iid}", "web_url": f"https://gitlab.com/xrow-public/ci-tools/-/merge_requests/{iid}",
            "merged_at": timestamp, "updated_at": timestamp, **extra}


class CalendarTests(unittest.TestCase):
    def test_previous_complete_month_includes_first_day(self):
        start, end, through, _ = collect.month_window(now=at("2026-11-01T08:00:00Z"))
        self.assertEqual((start, end, through), (at("2026-10-01T00:00:00Z"), at("2026-11-01T00:00:00Z"), at("2026-11-01T00:00:00Z")))

    def test_january_rolls_back_to_previous_year(self):
        start, end, *_ = collect.month_window(now=at("2026-01-01T00:00:00Z"))
        self.assertEqual((start.year, start.month, end.year, end.month), (2025, 12, 2026, 1))

    def test_leap_february_has_29_days(self):
        start, end, *_ = collect.month_window("2024-02", now=at("2026-01-01T00:00:00Z"))
        self.assertEqual((end - start).days, 29)

    def test_non_leap_february_has_28_days(self):
        start, end, *_ = collect.month_window("2025-02", now=at("2026-01-01T00:00:00Z"))
        self.assertEqual((end - start).days, 28)

    def test_december_rolls_into_next_year(self):
        _, end, *_ = collect.month_window("2025-12", now=at("2026-02-01T00:00:00Z"))
        self.assertEqual(end, at("2026-01-01T00:00:00Z"))

    def test_unfinished_month_requires_explicit_preview(self):
        with self.assertRaisesRegex(ValueError, "not complete"):
            collect.month_window("2026-10", now=at("2026-10-31T23:59:59Z"))

    def test_future_month_is_rejected_even_in_preview(self):
        with self.assertRaisesRegex(ValueError, "future month"):
            collect.month_window("2026-11", now=at("2026-10-31T23:59:59Z"), allow_incomplete=True)

    def test_invalid_months_are_rejected(self):
        for value in ["2026-1", "2026-13", "2026-00", "26-10", "2026-10-01"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                collect.month_window(value)

    def test_offset_clock_is_converted_before_month_selection(self):
        start, *_ = collect.month_window(now=at("2026-11-01T00:30:00+01:00"))
        self.assertEqual(start, at("2026-09-01T00:00:00Z"))


class CollectionTests(unittest.TestCase):
    def evidence(self, releases=(), merged=(), opened=(), **kwargs):
        def records(endpoint, params):
            if endpoint == "releases":
                return list(releases)
            return list(merged if params["state"] == "merged" else opened)
        with patch.object(collect, "pages", side_effect=records) as pages:
            data = collect.collect("2026-10", now=kwargs.pop("now", at("2026-11-02T10:00:00Z")), **kwargs)
        return data, pages

    def test_release_and_merge_boundaries_use_event_dates(self):
        events = ["2026-09-30T23:59:59Z", "2026-10-01T00:00:00Z", "2026-10-31T23:59:59Z", "2026-11-01T00:00:00Z"]
        data, pages = self.evidence(
            releases=[release(str(i), stamp) for i, stamp in enumerate(events)],
            merged=[mr(i, stamp, updated_at="2026-12-01T00:00:00Z") for i, stamp in enumerate(events)],
        )
        self.assertEqual(data["counts"], {"releases": 2, "merged_merge_requests": 2})
        self.assertEqual([x["iid"] for x in data["merged_merge_requests"]], [1, 2])
        self.assertTrue(data["complete"])
        self.assertNotIn("updated_before", pages.call_args_list[1].args[1])

    def test_offset_timestamps_are_compared_as_utc_instants(self):
        data, _ = self.evidence(releases=[release("outside", "2026-10-01T00:30:00+01:00"), release("inside", "2026-11-01T00:30:00+01:00")])
        self.assertEqual([x["tag_name"] for x in data["releases"]], ["inside"])

    def test_preview_is_explicit_and_cannot_include_future_events(self):
        data, _ = self.evidence(now=at("2026-10-31T10:00:00Z"), allow_incomplete=True,
                                releases=[release("real", "2026-10-01T00:00:00Z"), release("future", "2026-10-31T11:00:00Z")])
        self.assertFalse(data["complete"])
        self.assertEqual(data["collected_through_utc"], "2026-10-31T10:00:00Z")
        self.assertEqual(data["window_end_utc"], "2026-11-01T00:00:00Z")
        self.assertEqual(data["counts"]["releases"], 1)

    def test_old_open_mrs_are_separate_from_monthly_counts(self):
        data, pages = self.evidence(opened=[mr(7, "2025-01-01T00:00:00Z")])
        self.assertEqual(data["counts"]["merged_merge_requests"], 0)
        self.assertEqual(data["open_merge_requests"][0]["iid"], 7)
        self.assertEqual(pages.call_args_list[2].args[1], {"state": "opened"})
        self.assertEqual(data["open_merge_requests_as_of_utc"], "2026-11-02T10:00:00Z")

    def test_reruns_have_one_monthly_file_and_branch_identity(self):
        first, _ = self.evidence()
        second, _ = self.evidence(now=at("2026-12-03T00:00:00Z"))
        for key in ["month", "output_path", "suggested_branch", "window_start_utc", "window_end_utc"]:
            self.assertEqual(first[key], second[key])
        self.assertEqual(first["output_path"], "docs/digest/digest-2026-10.md")

    def test_missing_or_naive_timestamp_fails_instead_of_lowering_count(self):
        for item in [{"tag_name": "bad"}, release("bad", None), release("bad", "2026-10-01T00:00:00")]:
            with self.subTest(item=item), self.assertRaises((KeyError, AttributeError, ValueError)):
                self.evidence(releases=[item])


class PaginationTests(unittest.TestCase):
    def run_pages(self, batches):
        def result(*args, **kwargs):
            batch = next(batches)
            return subprocess.CompletedProcess(args[0], 0, json.dumps(batch), "")
        return patch.object(collect.subprocess, "run", side_effect=result)

    def test_reads_all_pages_including_final_empty_page(self):
        with patch.object(collect, "PAGE_SIZE", 2), self.run_pages(iter([[{"iid": 1}, {"iid": 2}], [{"iid": 3}, {"iid": 4}], []])) as run:
            items = list(collect.pages("merge_requests", {"state": "merged"}))
        self.assertEqual([item["iid"] for item in items], [1, 2, 3, 4])
        self.assertEqual(run.call_count, 3)
        self.assertIn("page=3", run.call_args.args[0][2])
        self.assertEqual(run.call_args.kwargs["timeout"], 30)

    def test_repeated_page_fails_closed(self):
        with patch.object(collect, "PAGE_SIZE", 1), self.run_pages(iter([[{"iid": 1}], [{"iid": 1}]])), self.assertRaisesRegex(ValueError, "repeated"):
            list(collect.pages("merge_requests", {}))

    def test_error_objects_and_malformed_records_are_rejected(self):
        for batch in [{"message": "forbidden"}, [None], [{}]]:
            with self.subTest(batch=batch), self.run_pages(iter([batch])), self.assertRaises(ValueError):
                list(collect.pages("merge_requests", {}))

    def test_api_failure_does_not_return_partial_success(self):
        with patch.object(collect, "PAGE_SIZE", 1), patch.object(collect.subprocess, "run", side_effect=[subprocess.CompletedProcess([], 0, '[{"iid": 1}]'), subprocess.CalledProcessError(1, ["glab"])]), self.assertRaises(subprocess.CalledProcessError):
            list(collect.pages("merge_requests", {}))

    def test_cli_failure_has_no_success_json_on_stdout(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("sys.argv", ["collect.py"]), patch.object(collect, "collect", side_effect=ValueError("bad response")), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = collect.main()
        self.assertEqual(status, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("bad response", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
