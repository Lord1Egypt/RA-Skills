import copy
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import calendar_data as data
import calendar_manager as manager


def annual(year=2027):
    """Synthetic future request, based on the schema of an official seed."""
    document = json.loads((data.DEFAULT_CALENDAR_DIR / '2026.json').read_text(encoding='utf-8'))
    document['year'] = year
    document['holidays'] = ['{:04d}-01-01'.format(year), '{:04d}-01-02'.format(year)]
    document['makeupWorkdays'] = ['{:04d}-01-03'.format(year)]
    return document


class CalendarManagerTests(unittest.TestCase):
    def write(self, path, document):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document), encoding='utf-8')

    def run_cli(self, arguments, cwd=None):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'calendar_manager.py'), *arguments],
                                cwd=cwd, capture_output=True, text=True)
        return result, json.loads(result.stdout)

    def test_official_seed_counts_and_dates(self):
        calendar = data.load_builtin_calendar()
        self.assertEqual(calendar['coveredYears'], {2025, 2026})
        first = data.read_document(data.DEFAULT_CALENDAR_DIR / '2025.json')
        second = data.read_document(data.DEFAULT_CALENDAR_DIR / '2026.json')
        self.assertEqual((len(first['holidays']), len(first['makeupWorkdays'])), (28, 5))
        self.assertEqual((len(second['holidays']), len(second['makeupWorkdays'])), (33, 6))
        self.assertIn('2025-06-02', first['holidays'])
        self.assertIn('2026-02-23', second['holidays'])
        self.assertIn('2026-09-20', second['makeupWorkdays'])

    def test_missing_year_and_default_path_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            result, value = self.run_cli(['validate', '--year', '2026'], cwd=temporary)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(value['coveredYears'], [2025, 2026])
            result, value = self.run_cli(['validate', '--year', '2024',
                                          '--calendar-dir', str(Path(temporary) / 'missing')])
            self.assertEqual(result.returncode, 1)
            self.assertEqual(value['code'], 'calendar_missing_year')
            self.assertEqual(value['missingYears'], [2024])
            self.assertFalse((Path(temporary) / 'missing').exists())

    def test_install_is_durable_and_idempotent_without_rewriting(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / 'calendars'
            document = annual()
            result = manager.install_calendar(document, directory)
            self.assertEqual((result['code'], result['changed']), ('calendar_installed', True))
            target = directory / '2027.json'
            before, modified = target.read_bytes(), target.stat().st_mtime_ns
            retry = copy.deepcopy(document)
            retry['updatedAt'] = '2026-12-08T09:00:00+08:00'
            retry['holidays'] = list(reversed(retry['holidays'])) + retry['holidays'][:1]
            result = manager.install_calendar(retry, directory)
            self.assertEqual((result['code'], result['changed']), ('calendar_unchanged', False))
            self.assertEqual(target.read_bytes(), before)
            self.assertEqual(target.stat().st_mtime_ns, modified)
            self.assertTrue((directory / manager.LOCK_FILE).is_file())
            self.assertEqual(manager.validate_calendar(2027, directory)['code'], 'calendar_valid')
            self.assertEqual([path.name for path in directory.iterdir() if path.suffix == '.tmp'], [])

    def test_different_content_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            document = annual()
            manager.install_calendar(document, directory)
            before = (directory / '2027.json').read_bytes()
            document['holidays'].append('2027-05-01')
            with self.assertRaises(data.CalendarError) as error:
                manager.install_calendar(document, directory)
            self.assertEqual(error.exception.code, 'calendar_exists_different')
            self.assertEqual((directory / '2027.json').read_bytes(), before)

    def test_dry_run_creates_nothing_and_reports_existing_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / 'never-created'
            result = manager.install_calendar(annual(), directory, dry_run=True)
            self.assertEqual((result['code'], result['changed'], result['dryRun']),
                             ('calendar_install_ready', True, True))
            self.assertFalse(directory.exists())
            directory.mkdir()
            self.write(directory / '2027.json', annual())
            before = {path.name: path.read_bytes() for path in directory.iterdir()}
            result = manager.install_calendar(annual(), directory, dry_run=True)
            self.assertFalse(result['changed'])
            self.assertEqual({path.name: path.read_bytes() for path in directory.iterdir()}, before)
            self.assertFalse((directory / manager.LOCK_FILE).exists())

    def test_invalid_request_does_not_create_directory_or_placeholder(self):
        invalid = [
            {'schemaVersion': True}, {'year': True}, {'timezone': 'UTC'},
            {'source': {'url': 'https://gov.cn.example.com/notice', 'publishedAt': '2026-11-04'}},
            {'source': {'url': 'http://www.gov.cn/notice', 'publishedAt': '2026-11-04'}},
            {'source': {'url': 'https://www.gov.cn/notice', 'publishedAt': '2026-02-30'}},
            {'updatedAt': '2026-12-07T09:00:00'}, {'holidays': []},
            {'holidays': ['20270101']}, {'holidays': ['2027-02-30']},
            {'holidays': ['2028-01-01']}, {'holidays': ['2026-11-30']},
            {'makeupWorkdays': ['2027-01-01']},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            for index, changes in enumerate(invalid):
                with self.subTest(changes=changes):
                    document = annual()
                    document.update(changes)
                    directory = Path(temporary) / str(index)
                    with self.assertRaises(data.CalendarError):
                        manager.install_calendar(document, directory)
                    self.assertFalse(directory.exists())

    def test_duplicate_json_keys_and_malformed_file_names_fail(self):
        with self.assertRaises(data.CalendarError) as error:
            data.decode_document('{"year": 2027, "year": 2026}')
        self.assertEqual(error.exception.code, 'calendar_invalid')
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write(directory / '2028.json', annual(2027))
            with self.assertRaises(data.CalendarError):
                data.load_builtin_calendar(directory)

    def test_cross_year_dates_are_preserved_deduplicated_and_checked_for_conflict(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            previous, current = annual(2026), annual(2027)
            previous['holidays'].append('2026-12-31')
            current['holidays'].extend(['2026-12-31', '2026-12-31'])
            manager.install_calendar(previous, directory)
            manager.install_calendar(current, directory)
            merged = data.load_builtin_calendar(directory)
            self.assertEqual(len(merged['holidays']), 5)
            self.assertIn('2026-12-31', data.read_document(directory / '2027.json')['holidays'])
            current['holidays'] = ['2027-01-01']
            current['makeupWorkdays'].append('2026-12-31')
            self.write(directory / '2027.json', current)
            with self.assertRaises(data.CalendarError) as error:
                manager.validate_calendar(2026, directory)
            self.assertEqual(error.exception.code, 'calendar_conflict')
            self.assertEqual(error.exception.conflicts, ['2026-12-31'])

    def test_cross_file_conflict_prevents_new_install_and_dry_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            previous, current = annual(2026), annual(2027)
            previous['holidays'].append('2026-12-31')
            current['makeupWorkdays'].append('2026-12-31')
            self.write(directory / '2026.json', previous)
            for dry_run in (True, False):
                with self.subTest(dry_run=dry_run):
                    with self.assertRaises(data.CalendarError) as error:
                        manager.install_calendar(current, directory, dry_run=dry_run)
                    self.assertEqual(error.exception.code, 'calendar_conflict')
                    self.assertFalse((directory / '2027.json').exists())

    def test_write_failure_keeps_existing_files_and_can_be_retried(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            manager.install_calendar(annual(2026), directory)
            before = (directory / '2026.json').read_bytes()
            with mock.patch.object(manager.os, 'link', side_effect=OSError('disk unavailable')):
                with self.assertRaises(data.CalendarError) as error:
                    manager.install_calendar(annual(2027), directory)
            self.assertEqual(error.exception.code, 'calendar_io_error')
            self.assertFalse((directory / '2027.json').exists())
            self.assertEqual((directory / '2026.json').read_bytes(), before)
            self.assertFalse(any(path.suffix == '.tmp' for path in directory.iterdir()))
            self.assertTrue(manager.install_calendar(annual(2027), directory)['changed'])

    def test_durability_failure_after_atomic_add_has_safe_idempotent_retry(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            with mock.patch.object(manager, 'sync_directory', side_effect=OSError('fsync failed')):
                with self.assertRaises(data.CalendarError) as error:
                    manager.install_calendar(annual(), directory)
            self.assertEqual(error.exception.code, 'calendar_io_error')
            self.assertEqual(data.read_document(directory / '2027.json')['year'], 2027)
            self.assertFalse(manager.install_calendar(annual(), directory)['changed'])

    def test_fixed_lock_timeout_is_retryable(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            with open(directory / manager.LOCK_FILE, 'w') as handle:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self.assertRaises(data.CalendarError) as error:
                    manager.install_calendar(annual(), directory, lock_timeout=0.05)
                self.assertEqual(error.exception.code, 'calendar_lock_timeout')
                self.assertFalse((directory / '2027.json').exists())
            self.assertTrue(manager.install_calendar(annual(), directory)['changed'])

    def test_concurrent_installers_add_exactly_once_or_refuse_different_content(self):
        for different in (False, True):
            with self.subTest(different=different), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                directory = root / 'calendars'
                first, second = annual(), annual()
                if different:
                    second['holidays'].append('2027-05-01')
                requests = [root / 'request-a.json', root / 'request-b.json']
                for path, document in zip(requests, (first, second)):
                    self.write(path, document)
                processes = [subprocess.Popen(
                    [sys.executable, str(SCRIPTS / 'calendar_manager.py'), 'install',
                     '--request', str(path), '--calendar-dir', str(directory)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for path in requests]
                values = []
                for process in processes:
                    stdout, stderr = process.communicate(timeout=10)
                    self.assertFalse(stderr, stderr)
                    values.append(json.loads(stdout))
                self.assertEqual(sum(value.get('changed', False) for value in values), 1)
                if different:
                    self.assertEqual(sum(value['ok'] for value in values), 1)
                    self.assertIn('calendar_exists_different', [value['code'] for value in values])
                else:
                    self.assertTrue(all(value['ok'] for value in values))
                saved = data.read_document(directory / '2027.json')
                self.assertIn(manager.semantic_content(saved),
                              [manager.semantic_content(first), manager.semantic_content(second)])

    def test_symbolic_links_do_not_redirect_calendar_writes_or_reads(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real = root / 'real'
            real.mkdir()
            linked = root / 'linked'
            linked.symlink_to(real, target_is_directory=True)
            with self.assertRaises(data.CalendarError):
                manager.install_calendar(annual(), linked)
            self.assertEqual(list(real.iterdir()), [])
            external = root / 'outside.json'
            self.write(external, annual())
            (real / '2027.json').symlink_to(external)
            with self.assertRaises(data.CalendarError):
                data.load_builtin_calendar(real)
            self.assertEqual(json.loads(external.read_text())['year'], 2027)

    def test_non_regular_calendar_files_fail_without_hanging_or_leaking_descriptors(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            fifo = directory / '2027.json'
            os.mkfifo(fifo)
            completed = subprocess.run(
                [sys.executable, str(SCRIPTS / 'calendar_manager.py'), 'validate', '--year',
                 '2027', '--calendar-dir', str(directory)], capture_output=True, text=True,
                timeout=2)
            self.assertEqual(completed.returncode, 1)
            self.assertEqual(json.loads(completed.stdout)['code'], 'calendar_io_error')
            real_open, opened = os.open, []
            def track_open(*args, **kwargs):
                descriptor = real_open(*args, **kwargs)
                opened.append(descriptor)
                return descriptor
            with mock.patch.object(data.os, 'open', side_effect=track_open):
                with self.assertRaises(data.CalendarError):
                    data.read_document(directory)
            self.assertEqual(len(opened), 1)
            with self.assertRaises(OSError):
                os.fstat(opened[0])

    def test_cli_invalid_input_returns_json_and_leaves_retry_possible(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = root / 'request.json'
            request.write_text('{ broken', encoding='utf-8')
            directory = root / 'calendars'
            result, value = self.run_cli(['install', '--request', str(request),
                                          '--calendar-dir', str(directory)])
            self.assertEqual(result.returncode, 1)
            self.assertEqual(value['code'], 'calendar_invalid')
            self.assertFalse(directory.exists())
            self.write(request, annual())
            result, value = self.run_cli(['install', '--request', str(request),
                                          '--calendar-dir', str(directory), '--dry-run'])
            self.assertEqual(result.returncode, 0)
            self.assertTrue(value['dryRun'])
            self.assertFalse(directory.exists())
            result, value = self.run_cli(['install', '--request', str(request),
                                          '--calendar-dir', str(directory)])
            self.assertEqual(result.returncode, 0)
            self.assertTrue(value['changed'])

    def test_cli_unencodable_metadata_fails_before_creating_calendar_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for location in ('extra', 'source'):
                with self.subTest(location=location):
                    document = annual()
                    if location == 'source':
                        document['source']['url'] += chr(0xD800)
                    else:
                        document['extra'] = chr(0xD800)
                    request = root / (location + '.json')
                    request.write_text(json.dumps(document), encoding='utf-8')
                    directory = root / (location + '-calendars')
                    for dry_run in (True, False):
                        arguments = ['install', '--request', str(request),
                                     '--calendar-dir', str(directory)]
                        if dry_run:
                            arguments.append('--dry-run')
                        result, value = self.run_cli(arguments)
                        self.assertEqual(result.returncode, 1)
                        self.assertEqual(result.stderr, '')
                        self.assertEqual(value['code'], 'calendar_invalid')
                        self.assertFalse(directory.exists())


if __name__ == '__main__':
    unittest.main()
