#!/usr/bin/env python3

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, time, timedelta, timezone
from pathlib import Path

import watch_meeting_conflicts as watcher


def meeting(meeting_id, code, subject, start, end):
    result = watcher.normalize_meeting(
        {
            "meeting_id": meeting_id,
            "meeting_code": code,
            "subject": subject,
            "start_time": start,
            "end_time": end,
            "status": "MEETING_STATE_NOT_START",
        }
    )
    assert result is not None
    return result


class ConflictWatcherTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.state = Path(self.temporary.name) / "state.json"
        self.query_start = datetime(2026, 8, 13, tzinfo=timezone.utc)
        self.query_end = datetime(2026, 8, 27, tzinfo=timezone.utc)

    def tearDown(self):
        self.temporary.cleanup()

    def process(self, meetings, alert_existing=False):
        return watcher.process_snapshot(
            meetings,
            self.state,
            15,
            alert_existing,
            self.query_start,
            self.query_end,
        )

    def test_wrapped_cli_response(self):
        items, token = watcher.response_page(
            {"data": {"meeting_info_list": [{"meeting_code": "123"}], "next_page_token": "next"}}
        )
        self.assertEqual(items[0]["meeting_code"], "123")
        self.assertEqual(token, "next")

    def test_baseline_is_silent_then_new_conflict_alerts_once(self):
        original = meeting("m1", "111", "项目周会", "2026-08-14T10:00:00+08:00", "2026-08-14T11:00:00+08:00")
        invited = meeting("m2", "222", "客户评审", "2026-08-14T10:30:00+08:00", "2026-08-14T11:30:00+08:00")

        self.assertIsNone(self.process([original]))
        event = self.process([original, invited])
        self.assertIsNotNone(event)
        self.assertEqual(event["event"], "meeting.conflict.detected")
        self.assertEqual(event["source"], "tmeet-conflict-check")
        self.assertTrue(any(conflict["kind"] == "hard" for conflict in event["conflicts"]))
        self.assertNotIn("meeting_id", json.dumps(event, ensure_ascii=False))
        self.assertIsNone(self.process([original, invited]))

    def test_non_conflicting_addition_is_silent(self):
        first = meeting("m1", "111", "A", "2026-08-14T10:00:00+08:00", "2026-08-14T11:00:00+08:00")
        later = meeting("m2", "222", "B", "2026-08-14T12:00:00+08:00", "2026-08-14T13:00:00+08:00")
        self.assertIsNone(self.process([first]))
        self.assertIsNone(self.process([first, later]))

    def test_soft_and_multi_conflicts(self):
        first = meeting("m1", "111", "A", "2026-08-14T10:00:00+08:00", "2026-08-14T11:00:00+08:00")
        soft = meeting("m2", "222", "B", "2026-08-14T11:10:00+08:00", "2026-08-14T12:00:00+08:00")
        second = meeting("m3", "333", "C", "2026-08-14T10:15:00+08:00", "2026-08-14T10:45:00+08:00")
        third = meeting("m4", "444", "D", "2026-08-14T10:30:00+08:00", "2026-08-14T10:50:00+08:00")
        conflicts = watcher.detect_conflicts([first, soft, second, third], 15)
        self.assertTrue(any(conflict["kind"] == "soft" for conflict in conflicts))
        self.assertTrue(any(conflict["kind"] == "multi" for conflict in conflicts))

    def test_default_schedule_is_weekday_whole_and_half_hours(self):
        timezone_value = timezone(timedelta(hours=8))
        slots = watcher.schedule_times(time(9, 0), time(18, 0), (0, 30), "")

        self.assertEqual(slots[0], time(9, 0))
        self.assertIn(time(9, 30), slots)
        self.assertEqual(slots[-1], time(18, 0))
        self.assertNotIn(time(18, 30), slots)

        friday = datetime(2026, 8, 14, 9, 0, 30, tzinfo=timezone_value)
        weekend = datetime(2026, 8, 15, 9, 0, 30, tzinfo=timezone_value)
        self.assertIsNotNone(watcher.matching_schedule_slot(friday, timezone_value, (1, 2, 3, 4, 5), slots, 120))
        self.assertIsNone(watcher.matching_schedule_slot(weekend, timezone_value, (1, 2, 3, 4, 5), slots, 120))

        next_slot = watcher.next_schedule_slot(
            datetime(2026, 8, 14, 18, 1, tzinfo=timezone_value),
            timezone_value,
            (1, 2, 3, 4, 5),
            slots,
        )
        self.assertEqual(next_slot, datetime(2026, 8, 17, 9, 0, tzinfo=timezone_value))

    def test_custom_schedule_times_override_default_minutes(self):
        slots = watcher.schedule_times(time(8, 30), time(19, 0), (0, 30), "09:15,17:45")
        self.assertEqual(slots, (time(9, 15), time(17, 45)))

    def test_cross_platform_process_probe_and_command_resolution(self):
        self.assertTrue(watcher.process_is_running(os.getpid()))
        self.assertEqual(
            os.path.normcase(watcher.resolve_executable(sys.executable)),
            os.path.normcase(sys.executable),
        )
        self.assertTrue(watcher.needs_windows_batch_shell(r"C:\Tools\tmeet.cmd", "nt"))
        self.assertFalse(watcher.needs_windows_batch_shell(r"C:\Tools\tmeet.exe", "nt"))
        self.assertFalse(watcher.needs_windows_batch_shell("/usr/local/bin/tmeet", "posix"))

    def test_stale_lock_is_recovered_without_signalling_current_process(self):
        lock_path = self.state.with_name(self.state.name + ".lock")
        lock_path.write_text("2147483647", encoding="utf-8")
        with watcher.StateLock(self.state):
            self.assertEqual(lock_path.read_text(encoding="utf-8"), str(os.getpid()))
        self.assertFalse(lock_path.exists())

    @unittest.skipUnless(os.name == "nt", "Windows-only process handle test")
    def test_windows_process_probe_does_not_signal_process(self):
        self.assertTrue(watcher._windows_process_is_running(os.getpid()))

    @unittest.skipUnless(os.name == "nt", "Windows-only npm .cmd shim test")
    def test_windows_cmd_shim_can_be_invoked_by_run_cli(self):
        shim = Path(self.temporary.name) / "tmeet.cmd"
        shim.write_text(
            '@echo off\r\n@echo {"data":{"meeting_info_list":[]}}\r\n',
            encoding="ascii",
        )
        payload = watcher.run_cli((str(shim),), 5)
        self.assertEqual(payload, {"data": {"meeting_info_list": []}})

    def test_command_entrypoint_stays_silent_until_fixture_changes(self):
        fixture = Path(self.temporary.name) / "meetings.json"
        first = {
            "meeting_id": "m1",
            "meeting_code": "111",
            "subject": "A",
            "start_time": "2026-08-14T10:00:00+08:00",
            "end_time": "2026-08-14T11:00:00+08:00",
        }
        second = {
            "meeting_id": "m2",
            "meeting_code": "222",
            "subject": "B",
            "start_time": "2026-08-14T10:30:00+08:00",
            "end_time": "2026-08-14T11:30:00+08:00",
        }
        fixture.write_text(json.dumps({"data": {"meeting_info_list": [first]}}), encoding="utf-8")

        output = io.StringIO()
        with redirect_stdout(output):
            result = watcher.main(
                (
                    "--trigger",
                    "manual",
                    "--office-start",
                    "00:00",
                    "--office-end",
                    "00:00",
                    "--schedule-times",
                    "00:00",
                    "--state-file",
                    str(self.state),
                    "--fixture",
                    str(fixture),
                )
            )
        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "")

        fixture.write_text(json.dumps({"data": {"meeting_info_list": [first, second]}}), encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            result = watcher.main(
                (
                    "--trigger",
                    "manual",
                    "--office-start",
                    "00:00",
                    "--office-end",
                    "00:00",
                    "--schedule-times",
                    "00:00",
                    "--state-file",
                    str(self.state),
                    "--fixture",
                    str(fixture),
                )
            )
        self.assertEqual(result, 0)
        event = json.loads(output.getvalue())
        self.assertEqual(event["event"], "meeting.conflict.detected")

    def test_scheduled_launch_outside_slot_does_not_touch_cli_or_state(self):
        nonexistent_fixture = Path(self.temporary.name) / "must-not-be-read.json"
        future_slot = (datetime.now().astimezone() + timedelta(minutes=5)).strftime("%H:%M")

        output = io.StringIO()
        with redirect_stdout(output):
            result = watcher.main(
                (
                    "--trigger",
                    "scheduled",
                    "--timezone",
                    "local",
                    "--office-start",
                    "00:00",
                    "--office-end",
                    "23:59",
                    "--schedule-times",
                    future_slot,
                    "--slot-grace-seconds",
                    "1",
                    "--state-file",
                    str(self.state),
                    "--fixture",
                    str(nonexistent_fixture),
                )
            )
        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "")
        self.assertFalse(self.state.exists())


if __name__ == "__main__":
    unittest.main()
