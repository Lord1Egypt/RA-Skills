"""Behavioral coverage for the offline annual calendar reminder contract."""

import contextlib
import datetime as dt
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
CALENDARS = SCRIPTS.parent / 'references' / 'calendars' / 'CN'
sys.path.insert(0, str(SCRIPTS))
import calendar_data
import reminder_engine as engine
import task_store


def timestamp(value):
    return dt.datetime.fromisoformat(value)


def sample_task(**changes):
    value = {
        'id': 'sample', 'title': 'sample', 'status': 'pending',
        'priority': 'medium', 'isBlocking': False, 'dueDate': None,
        'dueTime': None, 'createdAt': '2026-09-18T09:00:00+08:00',
        'comments': [], 'history': [],
    }
    value.update(changes)
    return value


class BuiltinCalendarTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.data = self.root / 'data'
        self.data.mkdir(mode=0o700)
        self.store = task_store.TaskStore(self.data)
        self.store.execute({'op': 'init'})
        self.identifier = self.create_task()

    def create_task(self, created='2026-09-18T09:00:00+08:00', **fields):
        fields = {'title': 'calendar fixture', 'priority': 'critical',
                  'dueDate': '2026-09-18', 'dueTime': '18:00', **fields}
        with patch.object(task_store, 'now', return_value=created):
            result = self.store.execute({'op': 'create', 'actor': 'test', 'fields': fields})
        return result['id']

    def cli(self, now, *, slot='10:00', task_id=None, holiday_file=None,
            expected_status=0, cwd=None):
        command = [sys.executable, str(SCRIPTS / 'reminder_engine.py'),
                   '--data-dir', str(self.data), '--slot', slot, '--now', now,
                   '--reserve', '--delay-minutes', '0']
        if task_id is not None:
            command.extend(['--task-id', task_id])
        if holiday_file is not None:
            command.extend(['--holiday-file', str(holiday_file)])
        completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        self.assertEqual(completed.returncode, expected_status,
                         completed.stdout + completed.stderr)
        return json.loads(completed.stdout)

    def in_process_cli(self, now, calendar_directory, *, slot='10:00', task_id=None):
        arguments = ['--data-dir', str(self.data), '--slot', slot, '--now', now,
                     '--reserve', '--delay-minutes', '0']
        if task_id is not None:
            arguments.extend(['--task-id', task_id])
        output = io.StringIO()
        with patch.object(engine, 'load_builtin_calendar',
                          side_effect=lambda: calendar_data.load_builtin_calendar(calendar_directory)):
            with contextlib.redirect_stdout(output):
                status = engine.main(arguments)
        return status, json.loads(output.getvalue())

    def saved(self):
        return self.store.execute({'op': 'read'})['ledgers'][task_store.MAIN]

    def assert_no_receipts(self):
        document = self.saved()
        self.assertEqual(document.get('_reminderReceipts', {}), {})
        for value in document['tasks']:
            self.assertEqual(value['reminderCount'], 0)
            self.assertIsNone(value['lastRemindedSlot'])
            self.assertIsNone(value['lastReminded'])

    def calendar_file(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value), encoding='utf-8')
        return path

    def calendar_directory(self):
        directory = self.root / 'calendars'
        directory.mkdir()
        for year in (2025, 2026):
            shutil.copyfile(CALENDARS / '{}.json'.format(year), directory / '{}.json'.format(year))
        return directory

    def edit_calendar(self, directory, year, transform):
        path = directory / '{}.json'.format(year)
        value = json.loads(path.read_text(encoding='utf-8'))
        transform(value)
        path.write_text(json.dumps(value), encoding='utf-8')

    def test_default_cli_silences_national_holiday_without_receipts(self):
        result = self.cli('2026-10-01T09:00:00+08:00')
        self.assertTrue(result['ok'])
        self.assertTrue(result['silent'])
        self.assertEqual(result['selected'], [])
        self.assert_no_receipts()

    def test_default_cli_delivers_both_weekend_makeup_workdays(self):
        for day in ('2026-09-20', '2026-10-10'):
            with self.subTest(day=day):
                result = self.cli(day + 'T09:00:00+08:00')
                self.assertFalse(result['silent'])
                self.assertEqual(result['reserved'], [self.identifier])
                self.assertEqual(result['receiptSlot'], day + 'T10:00+08:00')
        self.assertEqual(self.saved()['tasks'][0]['reminderCount'], 2)

    def test_ordinary_weekend_is_silent_and_weekday_delivers(self):
        weekend = self.cli('2026-09-19T09:00:00+08:00')
        self.assertTrue(weekend['silent'])
        self.assert_no_receipts()
        weekday = self.cli('2026-09-21T09:00:00+08:00')
        self.assertFalse(weekday['silent'])
        self.assertEqual(weekday['reserved'], [self.identifier])

    def test_cli_finds_packaged_calendar_from_unrelated_working_directory(self):
        unrelated = self.root / 'unrelated'
        unrelated.mkdir()
        result = self.cli('2026-10-01T09:00:00+08:00', cwd=unrelated)
        self.assertTrue(result['silent'])
        self.assert_no_receipts()

    def test_legacy_array_completely_overrides_builtin_calendar(self):
        external = self.calendar_file('legacy.json', [])
        result = self.cli('2026-10-01T09:00:00+08:00', holiday_file=external)
        self.assertFalse(result['silent'])
        self.assertEqual(result['reserved'], [self.identifier])
        weekend = self.cli('2026-09-20T09:00:00+08:00', holiday_file=external)
        self.assertTrue(weekend['silent'])
        self.assertEqual(self.saved()['tasks'][0]['reminderCount'], 1)

    def test_structured_override_controls_holidays_and_makeup_workdays(self):
        external = self.calendar_file('external.json', {
            'holidays': ['2026-10-10'], 'makeupWorkdays': ['2026-10-03'],
        })
        holiday = self.cli('2026-10-10T09:00:00+08:00', holiday_file=external)
        self.assertTrue(holiday['silent'])
        self.assert_no_receipts()
        makeup = self.cli('2026-10-03T09:00:00+08:00', holiday_file=external)
        self.assertFalse(makeup['silent'])
        self.assertEqual(makeup['reserved'], [self.identifier])

    def test_external_override_preserves_callers_timezone_and_needs_no_year_file(self):
        external = self.calendar_file('legacy.json', [])
        result = self.cli('2024-09-20T17:00:00+00:00', holiday_file=external)
        self.assertFalse(result['silent'])
        self.assertEqual(result['receiptSlot'], '2024-09-20T10:00+00:00')
        self.assertEqual(result['scheduledFor'], '2024-09-20T17:00+00:00')

    def test_utc_now_is_converted_before_day_deadline_and_receipt_checks(self):
        self.store.execute({'op': 'update', 'actor': 'test', 'id': self.identifier,
                            'changes': {'dueDate': '2026-09-20', 'dueTime': '06:00'},
                            'expected': {'dueDate': '2026-09-18', 'dueTime': '18:00'}})
        result = self.cli('2026-09-19T23:00:00+00:00')
        self.assertFalse(result['silent'])
        self.assertEqual(result['receiptSlot'], '2026-09-20T10:00+08:00')
        self.assertEqual(result['scheduledFor'], '2026-09-20T07:00+08:00')
        self.assertIn('紧急度：overdue', result['text'])
        self.assertIn('2026-09-20T06:00+08:00', result['text'])

    def test_utc_now_entering_china_weekend_does_not_reserve(self):
        result = self.cli('2026-09-18T17:00:00+00:00')
        self.assertTrue(result['silent'])
        self.assert_no_receipts()

    def test_specialized_slot_uses_china_day_and_keeps_original_idempotency_key(self):
        # UTC Saturday becomes Sunday's official makeup workday in China.
        slot = '2026-09-19T23:00:00+00:00'
        result = self.cli('2026-09-18T09:00:00+08:00', slot=slot,
                          task_id=self.identifier)
        self.assertEqual(result['action'], 'deliver')
        self.assertEqual(result['slot'], slot)
        self.assertEqual(self.saved()['tasks'][0]['lastRemindedSlot'], slot)

    def test_specialized_slot_entering_china_holiday_does_not_reserve(self):
        result = self.cli('2026-09-30T09:00:00+08:00',
                          slot='2026-09-30T17:00:00+00:00', task_id=self.identifier)
        self.assertEqual((result['action'], result['reason']), ('silent', 'non_working_day'))
        self.assert_no_receipts()

    def test_progress_timestamps_are_converted_before_stale_day_counting(self):
        calendar = engine.load_holidays(None)
        now = timestamp('2026-09-22T01:00:00+00:00')
        reset = '2026-09-19T20:00:00+00:00'  # September 20 in China.
        variants = [
            sample_task(createdAt=reset),
            sample_task(lastProgressAt=reset),
            sample_task(comments=[{'at': reset, 'content': 'progress',
                                  'meaningfulProgress': True}]),
        ]
        for value in variants:
            with self.subTest(source=value):
                self.assertEqual(engine.stale_workdays_for(value, now, calendar), 1)

    def test_snooze_history_is_converted_before_stale_day_counting(self):
        calendar = engine.load_holidays(None)
        now = timestamp('2026-09-21T01:00:00+00:00')
        value = sample_task(history=[{
            'at': '2026-09-20T20:00:00+00:00', 'action': 'update',
            'detail': {'changes': {'snoozedUntil': '2026-09-20T23:00:00+00:00'}},
        }])
        # The snooze lies on September 21 in China; September 20 still counts.
        self.assertEqual(engine.stale_workdays_for(value, now, calendar), 1)

    def test_history_counting_crosses_years_with_official_holidays(self):
        calendar = engine.load_holidays(None)
        value = sample_task(createdAt='2025-12-30T09:00:00+08:00')
        now = timestamp('2026-01-05T09:00:00+08:00')
        # December 31 and Sunday January 4 count; January 1–3 are holidays.
        self.assertEqual(engine.stale_workdays_for(value, now, calendar), 2)

    def test_actual_counted_interval_does_not_require_progress_timestamp_year(self):
        calendar = engine.load_holidays(None)
        value = sample_task(createdAt='2024-12-31T18:00:00+00:00')
        now = timestamp('2025-01-03T01:00:00+00:00')
        self.assertEqual(engine.stale_workdays_for(value, now, calendar), 1)
        value['createdAt'] = '2024-12-31T09:00:00+08:00'
        self.assertEqual(engine.stale_workdays_for(
            value, timestamp('2025-01-01T09:00:00+08:00'), calendar), 0)

    def test_missing_current_year_returns_structured_error_without_receipts(self):
        result = self.cli('2024-09-20T09:00:00+08:00', expected_status=1)
        self.assertFalse(result['ok'])
        self.assertEqual(result['code'], 'calendar_missing_year')
        self.assertEqual(result['missingYears'], [2024])
        self.assert_no_receipts()

    def test_current_year_is_required_after_utc_to_china_conversion(self):
        result = self.cli('2026-12-31T17:00:00+00:00', expected_status=1)
        self.assertEqual(result['code'], 'calendar_missing_year')
        self.assertEqual(result['missingYears'], [2027])
        self.assert_no_receipts()

    def test_specialized_missing_planned_year_is_checked_after_timezone_conversion(self):
        result = self.cli('2026-12-31T09:00:00+08:00',
                          slot='2026-12-31T17:00:00+00:00', task_id=self.identifier,
                          expected_status=1)
        self.assertEqual(result['code'], 'calendar_missing_year')
        self.assertEqual(result['missingYears'], [2027])
        self.assert_no_receipts()

    def test_missing_history_year_prevents_all_batch_reservations(self):
        # The first candidate is valid; a later candidate must fail the entire batch.
        self.create_task(created='2024-12-30T09:00:00+08:00', title='missing history')
        before = (self.data / task_store.MAIN).read_bytes()
        result = self.cli('2026-09-18T09:00:00+08:00', expected_status=1)
        self.assertEqual(result['code'], 'calendar_missing_year')
        self.assertEqual(result['missingYears'], [2024])
        self.assertEqual((self.data / task_store.MAIN).read_bytes(), before)
        self.assert_no_receipts()

    def test_missing_history_year_prevents_specialized_reservation(self):
        identifier = self.create_task(created='2024-12-30T09:00:00+08:00')
        result = self.cli('2026-09-18T09:00:00+08:00',
                          slot='2026-09-18T14:00+08:00', task_id=identifier,
                          expected_status=1)
        self.assertEqual(result['code'], 'calendar_missing_year')
        self.assertEqual(result['missingYears'], [2024])
        self.assert_no_receipts()

    def test_all_missing_history_years_are_reported_in_sorted_order(self):
        self.create_task(created='2023-12-30T09:00:00+08:00', title='older history')
        result = self.cli('2026-09-18T09:00:00+08:00', expected_status=1)
        self.assertEqual(result['code'], 'calendar_missing_year')
        self.assertEqual(result['missingYears'], [2023, 2024])
        self.assert_no_receipts()

    def test_cross_year_dates_merge_and_deduplicate_without_granting_year_coverage(self):
        directory = self.calendar_directory()
        self.edit_calendar(directory, 2025, lambda value: value['holidays'].extend(
            ['2024-12-31', '2025-12-31']))
        self.edit_calendar(directory, 2026,
                           lambda value: value['holidays'].append('2025-12-31'))
        calendar = calendar_data.load_builtin_calendar(directory)
        self.assertEqual(calendar['coveredYears'], {2025, 2026})
        self.assertEqual(calendar['timezone'], 'Asia/Shanghai')
        self.assertIn(dt.date(2024, 12, 31), calendar['holidays'])
        self.assertEqual(sum(day == dt.date(2025, 12, 31) for day in calendar['holidays']), 1)
        with self.assertRaises(calendar_data.CalendarError) as error:
            calendar_data.require_years(calendar, {2024})
        self.assertEqual(error.exception.code, 'calendar_missing_year')
        self.assertEqual(error.exception.missing_years, [2024])

    def test_cross_year_conflict_stops_cli_before_reservation(self):
        directory = self.calendar_directory()
        self.edit_calendar(directory, 2025,
                           lambda value: value['makeupWorkdays'].append('2025-12-31'))
        self.edit_calendar(directory, 2026,
                           lambda value: value['holidays'].append('2025-12-31'))
        before = (self.data / task_store.MAIN).read_bytes()
        status, result = self.in_process_cli('2026-09-18T09:00:00+08:00', directory)
        self.assertEqual(status, 1)
        self.assertEqual(result['code'], 'calendar_conflict')
        self.assertEqual(result['conflicts'], ['2025-12-31'])
        self.assertEqual((self.data / task_store.MAIN).read_bytes(), before)
        self.assert_no_receipts()

    def test_missing_year_from_partial_calendar_stops_before_reservation(self):
        directory = self.calendar_directory()
        (directory / '2026.json').unlink()
        status, result = self.in_process_cli('2026-09-18T09:00:00+08:00', directory)
        self.assertEqual(status, 1)
        self.assertEqual(result['code'], 'calendar_missing_year')
        self.assertEqual(result['missingYears'], [2026])
        self.assert_no_receipts()

    def test_external_conflict_has_structured_error_and_no_receipts(self):
        external = self.calendar_file('conflicting.json', {
            'holidays': ['2026-09-18'], 'makeupWorkdays': ['2026-09-18'],
        })
        result = self.cli('2026-09-18T09:00:00+08:00', holiday_file=external,
                          expected_status=1)
        self.assertEqual(result['code'], 'calendar_conflict')
        self.assertEqual(result['conflicts'], ['2026-09-18'])
        self.assert_no_receipts()


if __name__ == '__main__':
    unittest.main()
