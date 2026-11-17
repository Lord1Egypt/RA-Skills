import copy
from contextlib import closing
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'scripts/restore_local_projects.py'
spec = importlib.util.spec_from_file_location('recovery', MODULE)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.root = self.home / '.codex'
        self.root.mkdir()
        self.identity = 'local:' + str(self.root)
        self.folder = self.home / 'project'
        self.folder.mkdir()
        self.body = self.root / 'sessions/body.jsonl'
        self.body.parent.mkdir()
        self.body.write_text('original conversation body')
        self.project = dict(id='legacy-p', name='Project', rootPaths=[str(self.folder)], createdAt=1, updatedAt=2)
        self.old = {'local-projects': {'legacy-p': self.project}, 'project-order': ['legacy-p'],
                    r.MAP: {self.identity: {'legacy-p': 'server-p'}},
                    'thread-project-assignments': {
                        't1': {'projectKind': 'local', 'projectId': 'legacy-p'},
                        't2': {'projectKind': 'local', 'projectId': 'legacy-p'}},
                    'thread-writable-roots': {'t1': ['/never/import/permissions']},
                    'queued-follow-ups': {'t1': 'never run this'}}
        self.data = {r.ACCOUNT: {'owner': 'current-account', 'inactive': {'old': {'globals': self.old,
                     'atoms': {'account-sensitive': 'do-not-copy'}}}},
                     'projectless-thread-ids': ['t1', 'current-chat'],
                     'untouched': {'private': 'preserve'}, 'electron-persisted-atom-state': {'theme': 'light'}}
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db, db:
            db.executescript('''
              CREATE TABLE projects(id TEXT PRIMARY KEY);
              CREATE TABLE project_roots(project_id TEXT, position INTEGER, path TEXT);
              CREATE TABLE threads(id TEXT PRIMARY KEY, project_id TEXT, rollout_path TEXT, archived INTEGER, model_provider TEXT);
              INSERT INTO projects VALUES ('server-p');
            ''')
            db.execute('INSERT INTO project_roots VALUES (?,0,?)', ('server-p', str(self.folder)))
            db.executemany('INSERT INTO threads VALUES (?,NULL,?,?,?)', [
                ('t1', str(self.body), 0, 'custom'),
                ('t2', str(self.root / 'missing.jsonl'), 1, 'custom')])
        (self.root / 'sqlite').mkdir()
        with closing(sqlite3.connect(self.root / 'sqlite/codex-dev.db')) as db, db:
            db.executescript('''
              CREATE TABLE local_thread_catalog(host_id TEXT,thread_id TEXT,project_id TEXT);
              CREATE TABLE local_thread_catalog_metadata(id INTEGER,catalog_revision INTEGER);
              INSERT INTO local_thread_catalog VALUES ('local','t1',NULL),('remote','t1',NULL);
              INSERT INTO local_thread_catalog_metadata VALUES (1,0);
            ''')
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        (self.root / r.STATE).write_bytes(r.encode(self.data))

    def plan(self):
        raw = (self.root / r.STATE).read_bytes()
        db = r.db_snapshot(self.root / 'state_5.sqlite')
        try:
            return raw, r.make_plan(self.root, raw, db)
        finally:
            db.close()

    def apply(self, raw, result):
        target, updates, checked, summary = result
        with patch.object(r, 'stopped_guard'), patch.object(r.Path, 'home', return_value=self.home):
            return r.apply_plan(self.root, raw, target, updates, checked, summary, self.home / 'backups')

    def test_roundtrip_preserves_account_archive_provider_and_bodies(self):
        raw, result = self.plan()
        target, updates, checked, summary = result
        self.assertEqual(summary['projects_added'], 1)
        self.assertEqual(summary['associations_added'], 2)
        self.assertEqual(summary['missing_body_files'], 1)
        self.assertNotIn('thread-writable-roots', target)
        self.assertNotIn('queued-follow-ups', target)
        self.assertEqual(target[r.ACCOUNT], self.data[r.ACCOUNT])
        self.assertEqual(target['electron-persisted-atom-state'], self.data['electron-persisted-atom-state'])
        self.assertEqual(target['projectless-thread-ids'], ['current-chat'])
        report = self.apply(raw, result)
        self.assertFalse(report['ui_verified'])
        self.assertEqual((Path(report['backup']) / 'codex-home' / r.STATE).read_bytes(), raw)
        self.assertEqual(self.body.read_text(), 'original conversation body')
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db, db:
            self.assertEqual(db.execute('SELECT project_id,archived,model_provider FROM threads ORDER BY id').fetchall(),
                             [('server-p', 0, 'custom'), ('server-p', 1, 'custom')])
        with closing(sqlite3.connect(self.root / 'sqlite/codex-dev.db')) as db, db:
            self.assertEqual(db.execute('SELECT project_id FROM local_thread_catalog ORDER BY host_id').fetchall(), [('server-p',), (None,)])

    def test_second_run_has_no_changes(self):
        raw, result = self.plan()
        self.apply(raw, result)
        raw2, result2 = self.plan()
        self.assertEqual(result2[0], json.loads(raw2))
        self.assertEqual(result2[1], {})

    def test_current_membership_wins(self):
        other = dict(self.project, id='current-p')
        self.data['local-projects'] = {'current-p': other}
        self.data['thread-project-assignments'] = {'t1': {'projectKind': 'local', 'projectId': 'current-p'}}
        self.data[r.MAP] = {self.identity: {'current-p': 'server-p'}}
        self.save()
        _, (target, _, _, _) = self.plan()
        self.assertEqual(target['thread-project-assignments']['t1']['projectId'], 'current-p')

    def test_conflicting_project_roots_fail_closed(self):
        self.data['local-projects'] = {'legacy-p': dict(self.project, rootPaths=['/different'])}
        self.save()
        with self.assertRaises(r.RecoveryError):
            self.plan()

    def test_database_conflict_fails_closed(self):
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db, db:
            db.execute("UPDATE threads SET project_id='different-project' WHERE id='t1'")
        with self.assertRaises(r.RecoveryError):
            self.plan()

    def test_project_without_threads_still_requires_matching_roots(self):
        self.old['local-projects']['empty-project'] = dict(self.project, id='empty-project', rootPaths=['/different-root'])
        self.old[r.MAP][self.identity]['empty-project'] = 'server-p'
        self.save()
        with self.assertRaises(r.RecoveryError):
            self.plan()

    def test_unknown_threads_are_skipped_not_created(self):
        self.old['thread-project-assignments']['missing-id'] = {'projectKind': 'local', 'projectId': 'legacy-p'}
        self.save()
        _, (target, _, _, summary) = self.plan()
        self.assertEqual(summary['unmatched_associations_skipped'], 1)
        self.assertNotIn('missing-id', target['thread-project-assignments'])

    def test_write_failure_rolls_back_both_databases(self):
        raw, result = self.plan()
        real_write = r.atomic_write
        attempted = False

        def fail_once(path, value):
            nonlocal attempted
            if path == self.root / r.STATE and not attempted:
                attempted = True
                raise OSError('simulated write failure')
            return real_write(path, value)

        with patch.object(r, 'atomic_write', side_effect=fail_once):
            with self.assertRaises(OSError):
                self.apply(raw, result)
        self.assertEqual((self.root / r.STATE).read_bytes(), raw)
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db, db:
            self.assertEqual(db.execute('SELECT DISTINCT project_id FROM threads').fetchall(), [(None,)])
        with closing(sqlite3.connect(self.root / 'sqlite/codex-dev.db')) as db, db:
            self.assertEqual(db.execute('SELECT DISTINCT project_id FROM local_thread_catalog').fetchall(), [(None,)])

    def test_running_or_unobservable_app_is_refused(self):
        response = subprocess.CompletedProcess([], 0, '123 /Applications/ChatGPT.app/Contents/MacOS/ChatGPT\n', '')
        with patch.object(r.subprocess, 'run', return_value=response):
            with self.assertRaises(r.RecoveryError):
                r.stopped_guard()
        with patch.object(r.subprocess, 'run', side_effect=PermissionError):
            with self.assertRaises(r.RecoveryError):
                r.stopped_guard()

    def test_changed_state_before_apply_is_refused(self):
        raw, result = self.plan()
        self.data['new-value'] = True
        self.save()
        with self.assertRaises(r.RecoveryError):
            self.apply(raw, result)
        self.assertFalse((self.home / 'backups').exists())

    def sidebar_fixture(self):
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db, db:
            db.execute('CREATE TABLE thread_sections(id TEXT,name TEXT)')
            db.execute("INSERT INTO thread_sections VALUES ('local-section','Skills')")
        self.data['electron-persisted-atom-state'][r.SECTIONS] = {'active': {'sections': [
            {'id': 'current-section', 'name': 'Skills', 'hostSectionIds': {'local': 'local-section'}, 'itemKeys': []}]}}
        self.data[r.ACCOUNT]['inactive']['old']['atoms'][r.SECTIONS] = {'old-account': {'sections': [
            {'id': 'old-section', 'name': 'Skills', 'hostSectionIds': {'local': 'local-section'}, 'itemKeys': [
                'codex:project:legacy-p', 'codex:thread:local:t1', 'codex:thread:local:t2',
                'chatgpt:conversation:private-cloud', 'codex:project:nonexistent']}]}}
        self.save()

    def test_sidebar_restores_local_memberships_and_skips_cloud_archived_unknown(self):
        self.sidebar_fixture()
        raw, result = self.plan()
        target, _, _, summary = result
        section = target['electron-persisted-atom-state'][r.SECTIONS]['active']['sections'][0]
        self.assertEqual(section['id'], 'current-section')
        self.assertEqual(section['itemKeys'], ['codex:project:legacy-p', 'codex:thread:local:t1'])
        self.assertEqual(summary['sidebar_items_added'], 2)
        self.assertEqual(summary['sidebar_items_skipped'], 3)
        self.assertEqual(target[r.ACCOUNT], self.data[r.ACCOUNT])
        self.apply(raw, result)
        raw2, result2 = self.plan()
        self.assertEqual(result2[0], json.loads(raw2))
        self.assertEqual(result2[3]['sidebar_items_added'], 0)

    def test_sidebar_preserves_existing_membership(self):
        self.sidebar_fixture()
        self.data['electron-persisted-atom-state'][r.SECTIONS]['active']['sections'].append(
            {'id': 'another', 'name': 'Custom', 'itemKeys': ['codex:project:legacy-p']})
        self.save()
        _, (target, _, _, summary) = self.plan()
        sections = target['electron-persisted-atom-state'][r.SECTIONS]['active']['sections']
        self.assertNotIn('codex:project:legacy-p', sections[0]['itemKeys'])
        self.assertEqual(summary['sidebar_items_added'], 1)

    def test_sidebar_ambiguous_account_refuses(self):
        self.sidebar_fixture()
        self.data['electron-persisted-atom-state'][r.SECTIONS]['another-account'] = {'sections': []}
        self.save()
        with self.assertRaises(r.RecoveryError):
            self.plan()

    def test_missing_local_section_cannot_report_complete(self):
        self.sidebar_fixture()
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db, db:
            db.execute('DELETE FROM thread_sections')
        with self.assertRaisesRegex(r.RecoveryError, '仍有本地条目未恢复'):
            self.plan()

    def test_renamed_local_section_cannot_silently_discard_missing_members(self):
        self.sidebar_fixture()
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db, db:
            db.execute("UPDATE thread_sections SET name='Renamed'")
        with self.assertRaisesRegex(r.RecoveryError, '仍有本地条目未恢复'):
            self.plan()

    def test_sidebar_creates_missing_local_section_with_new_identity(self):
        self.sidebar_fixture()
        self.data['electron-persisted-atom-state'][r.SECTIONS]['active']['sections'] = []
        self.save()
        _, (target, _, _, summary) = self.plan()
        section = target['electron-persisted-atom-state'][r.SECTIONS]['active']['sections'][0]
        self.assertNotEqual(section['id'], 'old-section')
        self.assertEqual(section['hostSectionIds'], {'local': 'local-section'})
        self.assertEqual(summary['sidebar_sections_added'], 1)

    def test_report_cannot_overwrite_source_state_even_in_preview(self):
        raw = (self.root / r.STATE).read_bytes()
        with patch.dict(r.os.environ, {'CODEX_HOME': str(self.root)}), patch.object(
                r.sys, 'argv', ['restore_local_projects.py', '--report', str(self.root / r.STATE)]):
            with self.assertRaises(r.RecoveryError):
                r.main()
        self.assertEqual((self.root / r.STATE).read_bytes(), raw)

    def test_skill_directory_cannot_hold_runtime_outputs(self):
        with self.assertRaises(r.RecoveryError):
            r.validate_output(MODULE.parent.parent / 'runtime.json', self.root)
        with self.assertRaises(r.RecoveryError):
            r.validate_output(self.root / 'backups', self.root)

    def test_backup_failure_does_not_mutate_sources(self):
        raw, result = self.plan()
        with patch.object(r, 'copy_tree', side_effect=OSError('backup disk unavailable')):
            with self.assertRaises(OSError):
                self.apply(raw, result)
        self.assertEqual((self.root / r.STATE).read_bytes(), raw)
        with closing(sqlite3.connect(self.root / 'state_5.sqlite')) as db:
            self.assertEqual(db.execute('SELECT DISTINCT project_id FROM threads').fetchall(), [(None,)])

    def test_restart_during_partial_write_stops_automatic_rollback(self):
        raw, result = self.plan()
        calls = 0

        def restart():
            nonlocal calls
            calls += 1
            if calls >= 5:
                raise r.RecoveryError('application restarted')

        with patch.object(r, 'stopped_guard', side_effect=restart), patch.object(r.Path, 'home', return_value=self.home):
            with self.assertRaisesRegex(r.RecoveryError, '停止自动回滚'):
                r.apply_plan(self.root, raw, *result, self.home / 'backups')
        self.assertEqual((self.root / r.STATE).read_bytes(), raw)
        self.assertTrue(list((self.home / 'backups').glob('*/codex-home/' + r.STATE)))

    def test_report_failure_is_reported_as_written_not_rolled_back(self):
        raw, result = self.plan()
        real_write = r.atomic_write

        def fail_report(path, value):
            if path.name == 'result.json':
                raise OSError('report disk unavailable')
            return real_write(path, value)

        with patch.object(r, 'atomic_write', side_effect=fail_report):
            with self.assertRaisesRegex(r.RecoveryError, '本地恢复已写入'):
                self.apply(raw, result)
        self.assertEqual(json.loads((self.root / r.STATE).read_bytes()), result[0])

    def test_nonstandard_app_location_is_also_refused(self):
        result = subprocess.CompletedProcess([], 0, '123 /Users/example/Apps/ChatGPT.app/Contents/MacOS/ChatGPT\n', '')
        with patch.object(r.subprocess, 'run', return_value=result):
            with self.assertRaises(r.RecoveryError):
                r.stopped_guard()

    def test_shared_source_lock_blocks_other_recovery_even_with_different_backup(self):
        with patch.object(r.Path, 'home', return_value=self.home):
            with r.recovery_lock(self.root) as path:
                self.assertFalse(path.is_relative_to(self.root))
                with self.assertRaises(r.RecoveryError):
                    r.acquire_recovery_lock(self.root / '..' / '.codex')
            self.assertFalse(path.exists())

    def test_shared_lock_releases_after_handled_failure(self):
        with patch.object(r.Path, 'home', return_value=self.home):
            with self.assertRaises(OSError):
                with r.recovery_lock(self.root):
                    raise OSError('simulated failure')
            with r.recovery_lock(self.root) as path:
                self.assertTrue(path.is_dir())


if __name__ == '__main__':
    unittest.main(verbosity=2)
