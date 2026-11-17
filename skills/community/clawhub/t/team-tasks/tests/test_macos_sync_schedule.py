import datetime as dt
import io
import json
import os
from pathlib import Path
import platform
import plistlib
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import macos_sync_schedule as mod


class ScheduleSlotTests(unittest.TestCase):
    def test_exactly_80_slots_each_day_including_weekend(self):
        for date in [dt.date(2026, 10, 13), dt.date(2026, 10, 17), dt.date(2026, 10, 18)]:
            slots = [mod.schedule_slot(dt.datetime.combine(date, dt.time(hour, minute), mod.BEIJING))
                     for hour in range(24) for minute in range(60)]
            planned = [value for value in slots if value is not None]
            self.assertEqual(len(planned), 80)
            self.assertEqual(planned[0], date.isoformat() + 'T07:00+08:00')
            self.assertEqual(planned[1], date.isoformat() + 'T09:00+08:00')
            self.assertEqual(planned[-1], date.isoformat() + 'T22:00+08:00')

    def test_seconds_stay_in_slot_and_2201_is_outside(self):
        self.assertEqual(mod.schedule_slot(dt.datetime(2026, 10, 13, 22, 0, 59, 999999, mod.BEIJING)),
                         '2026-10-13T22:00+08:00')
        for hour, minute in [(6, 59), (7, 1), (8, 0), (9, 1), (21, 51), (22, 1)]:
            self.assertIsNone(mod.schedule_slot(dt.datetime(2026, 10, 13, hour, minute, tzinfo=mod.BEIJING)))

    def test_utc_and_foreign_timezone_resolve_same_slot(self):
        stamp = dt.datetime(2026, 10, 13, 1, 0, 42, tzinfo=dt.timezone.utc)
        self.assertEqual(mod.schedule_slot(stamp), '2026-10-13T09:00+08:00')
        self.assertEqual(mod.schedule_slot(stamp.astimezone(dt.timezone(dt.timedelta(hours=-7)))),
                         '2026-10-13T09:00+08:00')
        # A missed 09:00 isn't caught up at 09:01.
        self.assertIsNone(mod.schedule_slot(stamp + dt.timedelta(minutes=1)))

    def test_naive_time_is_rejected(self):
        with self.assertRaises(ValueError):
            mod.schedule_slot(dt.datetime(2026, 10, 13, 9))

    def test_portable_spec_has_no_provider_or_model(self):
        spec = mod.schedule_spec()
        self.assertEqual(spec['dailySlotCount'], 80)
        self.assertEqual(spec['timezone'], 'Asia/Shanghai')
        self.assertFalse(spec['callsModel'])
        self.assertEqual(spec['missedSlots'], 'skip')
        self.assertEqual(spec['weekdays'], 'all')
        self.assertIsNone(spec['command'])


class NativeScheduleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='team-tasks-schedule-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.directory = self.base / "台账 $x 'quote' ; data"
        self.directory.mkdir()
        self.home = self.base / 'home'
        self.home.mkdir()
        self.home_patch = patch.object(Path, 'home', return_value=self.home)
        self.home_patch.start()
        self.addCleanup(self.home_patch.stop)
        self.list_name = '团队待办 · 项目甲'
        self.schedule = mod.NativeSchedule(self.directory, self.base / 'state', home=self.home, list_name=self.list_name)
        self.commands = []
        self.loaded = set()
        self.probe_response = {'ok': True, 'nativeProbeVerified': True, 'initialized': True, 'requestMode': 'diagnose', 'listName': self.list_name}
        self.initialized = {'initialized': True, 'namespace': self.schedule.namespace, 'listId': 'native-list-id',
                            'listName': self.list_name}

    def native_run(self, argv, timeout=30):
        self.commands.append(argv)
        if argv[0] != '/bin/launchctl':
            raise AssertionError('No actual native command may execute in mocked installer tests: ' + repr(argv))
        action = argv[1]
        if action == 'print':
            return SimpleNamespace(returncode=0 if argv[2].split('/')[-1] in self.loaded else 113, stdout='', stderr='')
        if action == 'bootout':
            self.loaded.discard(argv[2].split('/')[-1])
        elif action == 'bootstrap':
            with Path(argv[3]).open('rb') as stream:
                plist = plistlib.load(stream)
            label = plist['Label']
            self.loaded.add(label)
            if label == self.schedule.probe_label:
                config = json.loads(self.schedule.probe_config.read_text(encoding='utf-8'))
                result = dict(self.probe_response, probeToken=config['probeToken'])
                mod._atomic_json(self.schedule.probe_result, result)
        else:
            raise AssertionError(argv)
        return SimpleNamespace(returncode=0, stdout='', stderr='')

    def enable_mocked(self):
        with patch.object(mod.platform, 'system', return_value='Darwin'), \
                patch.object(self.schedule, '_bootstrap_status', return_value=self.initialized), \
                patch.object(self.schedule, '_build_helper', return_value='source-fingerprint'), \
                patch.object(mod, '_run', side_effect=self.native_run):
            return self.schedule.enable()

    def test_plan_is_read_only_and_command_arguments_preserve_paths(self):
        with patch.object(mod, '_run') as run:
            plan = self.schedule.plan()
        self.assertEqual(plan['spec']['command'][3], str(self.directory))
        self.assertEqual(plan['spec']['command'][-2:], ['--state-root', str(self.schedule.state_root)])
        self.assertFalse(self.schedule.state_root.exists())
        run.assert_not_called()
        self.assertFalse(plan['macFallback']['installsAnything'])

    def test_enable_requires_completed_initialization_before_compile_or_native_access(self):
        with patch.object(mod.platform, 'system', return_value='Darwin'), \
                patch.object(self.schedule, '_bootstrap_status', return_value={'initialized': False}), \
                patch.object(self.schedule, '_build_helper') as build, patch.object(mod, '_run') as run:
            with self.assertRaises(mod.ScheduleError) as caught:
                self.schedule.enable()
        self.assertEqual(caught.exception.code, 'mirror_not_initialized')
        build.assert_not_called()
        run.assert_not_called()
        self.assertFalse(self.schedule.plist.exists())

    def test_real_launchd_chain_proof_precedes_periodic_bootstrap(self):
        result = self.enable_mocked()
        self.assertEqual(result['code'], 'schedule_enabled')
        self.assertTrue(result['backgroundProof'])
        self.assertFalse(result['callsModel'])
        bootstraps = [argv for argv in self.commands if argv[1] == 'bootstrap']
        self.assertEqual([argv[3] for argv in bootstraps],
                         [str(self.schedule.probe_plist), str(self.schedule.plist)])
        self.assertIn(self.schedule.label, self.loaded)
        self.assertNotIn(self.schedule.probe_label, self.loaded)
        with self.schedule.plist.open('rb') as stream:
            periodic = plistlib.load(stream)
        with self.schedule.probe_plist.open('rb') as stream:
            probe = plistlib.load(stream)
        self.assertEqual(periodic['StartInterval'], 60)
        self.assertFalse(periodic['RunAtLoad'])
        self.assertTrue(probe['RunAtLoad'])
        self.assertNotIn('StartInterval', probe)
        # Same launcher, app and fixed bundle identity; only JSON config differs.
        self.assertEqual(periodic['ProgramArguments'][:-1], probe['ProgramArguments'][:-1])
        self.assertIn(str(self.schedule.app), periodic['ProgramArguments'])
        config = json.loads(self.schedule.config.read_text(encoding='utf-8'))
        self.assertEqual(config['argv'], [str(mod.SYNC_SCRIPT), '--data-dir', str(self.directory),
                                         '--state-root', str(self.schedule.state_root), '--list-name=' + self.list_name, '--scheduled',
                                         '--result-file', str(self.schedule.last_result)])
        self.assertEqual(json.loads(self.schedule.manifest.read_text())['phase'], 'enabled')
        self.assertEqual(self.schedule.config.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.schedule.install_dir.stat().st_mode & 0o777, 0o700)

    def test_denied_permission_never_registers_periodic_job_or_changes_identity(self):
        self.probe_response = {'ok': False, 'initialized': True, 'requestMode': 'diagnose',
                               'code': 'macos_permission_denied', 'message': 'denied -1743'}
        original_bundle = self.schedule.bundle_id
        with self.assertRaises(mod.ScheduleError) as caught:
            self.enable_mocked()
        self.assertEqual(caught.exception.code, 'macos_permission_denied')
        self.assertEqual(self.schedule.bundle_id, original_bundle)
        self.assertFalse(self.schedule.plist.exists())
        self.assertEqual(self.loaded, set())
        self.assertEqual(json.loads(self.schedule.manifest.read_text())['phase'], 'disabled')
        self.assertEqual(len([argv for argv in self.commands if argv[1] == 'bootstrap']), 1)

    def test_local_status_cannot_be_accepted_as_native_permission_proof(self):
        self.probe_response.pop('nativeProbeVerified')
        with self.assertRaises(mod.ScheduleError) as caught:
            self.enable_mocked()
        self.assertEqual(caught.exception.code, 'invalid_background_proof')
        self.assertFalse(self.schedule.plist.exists())

    def test_diagnostic_must_prove_initialized_mirror(self):
        self.probe_response['initialized'] = False
        with self.assertRaises(mod.ScheduleError) as caught:
            self.enable_mocked()
        self.assertEqual(caught.exception.code, 'invalid_background_proof')
        self.assertFalse(self.schedule.plist.exists())

    def test_stale_probe_token_is_not_permission_proof(self):
        mod._private_directory(self.schedule.install_dir)
        mod._atomic_json(self.schedule.probe_result, {'ok': True, 'initialized': True,
                         'requestMode': 'diagnose', 'probeToken': 'old-token'})
        def no_child_result(argv, timeout=30):
            self.commands.append(argv)
            return SimpleNamespace(returncode=113 if argv[1] == 'print' else 0, stdout='', stderr='')
        with patch.object(mod, '_run', side_effect=no_child_result):
            with self.assertRaises(mod.ScheduleError) as caught:
                self.schedule._probe(timeout=.02)
        self.assertEqual(caught.exception.code, 'background_probe_timeout')

    def test_probe_for_other_list_never_enables_job(self):
        self.probe_response['listName'] = '其他列表'
        with self.assertRaises(mod.ScheduleError) as caught:
            self.enable_mocked()
        self.assertEqual(caught.exception.code, 'invalid_background_proof')
        self.assertFalse(self.schedule.plist.exists())
        self.assertEqual(self.loaded, set())

    def test_registry_failure_after_probe_keeps_disabled_record(self):
        original_probe = self.schedule._probe
        def probe_then_corrupt():
            proof = original_probe()
            self.schedule._target_name = lambda: (_ for _ in ()).throw(
                mod.StateError('binding_conflict', 'registry changed'))
            return proof
        with patch.object(self.schedule, '_probe', side_effect=probe_then_corrupt):
            with self.assertRaises(mod.StateError) as caught:
                self.enable_mocked()
        self.assertEqual(caught.exception.code, 'binding_conflict')
        self.assertFalse(self.schedule.plist.exists())
        self.assertEqual(self.loaded, set())
        self.assertEqual(json.loads(self.schedule.manifest.read_text())['phase'], 'disabled')

    def test_disable_only_own_job_and_preserves_helper_data_and_logs(self):
        self.enable_mocked()
        other = self.schedule.plist.parent / 'com.other.application.plist'
        other.write_bytes(b'other job unchanged')
        log = self.schedule.install_dir / 'sync.log'
        log.write_text('history')
        with patch.object(mod.platform, 'system', return_value='Darwin'), \
                patch.object(mod, '_run', side_effect=self.native_run):
            result = self.schedule.disable()
        self.assertEqual(result['code'], 'schedule_disabled')
        self.assertFalse(self.schedule.plist.exists())
        self.assertEqual(other.read_bytes(), b'other job unchanged')
        self.assertEqual(log.read_text(), 'history')
        self.assertTrue(self.schedule.config.exists())
        self.assertEqual(json.loads(self.schedule.manifest.read_text())['phase'], 'disabled')
        bootouts = [argv[-1] for argv in self.commands if argv[1] == 'bootout']
        self.assertTrue(all(value.endswith(self.schedule.label) or value.endswith(self.schedule.probe_label)
                            for value in bootouts))

    def test_changed_plist_is_never_stopped_or_overwritten(self):
        self.schedule.plist.parent.mkdir(parents=True)
        with self.schedule.plist.open('wb') as stream:
            plistlib.dump({'Label': self.schedule.label, 'ProgramArguments': ['/usr/bin/true']}, stream)
        before = self.schedule.plist.read_bytes()
        with patch.object(mod.platform, 'system', return_value='Darwin'), patch.object(mod, '_run') as run:
            with self.assertRaises(mod.ScheduleError) as caught:
                self.schedule.disable()
        self.assertEqual(caught.exception.code, 'schedule_ownership_conflict')
        self.assertEqual(self.schedule.plist.read_bytes(), before)
        run.assert_not_called()

    def test_loaded_job_without_owned_file_is_not_adopted(self):
        self.loaded.add(self.schedule.label)
        with self.assertRaises(mod.ScheduleError) as caught:
            self.enable_mocked()
        self.assertEqual(caught.exception.code, 'schedule_ownership_conflict')
        self.assertFalse(self.schedule.plist.exists())
        self.assertIn(self.schedule.label, self.loaded)

    def test_status_queries_launchd_and_private_results_without_reminders(self):
        self.enable_mocked()
        mod._atomic_json(self.schedule.last_result, {'ok': True, 'code': 'synced', 'slot': '2026-10-13T09:00+08:00'})
        with patch.object(mod.platform, 'system', return_value='Darwin'), \
                patch.object(mod, '_run', side_effect=self.native_run):
            result = self.schedule.status()
        self.assertTrue(result['enabled'])
        self.assertEqual(result['lastSync']['code'], 'synced')
        self.assertEqual(self.commands[-1][1], 'print')
        self.assertFalse(result['callsModel'])

    def test_native_actions_skip_other_operating_systems(self):
        for operation in ['enable', 'disable', 'diagnose']:
            with patch.object(mod.platform, 'system', return_value='Windows'), patch.object(mod, '_run') as run:
                with self.assertRaises(mod.ScheduleError) as caught:
                    getattr(self.schedule, operation)()
                self.assertEqual(caught.exception.code, 'native_schedule_requires_macos')
                run.assert_not_called()
        self.assertFalse(self.schedule.state_root.exists())

    def test_control_operations_are_serialized(self):
        with self.schedule._control_lock():
            with self.assertRaises(mod.ScheduleError) as caught:
                with self.schedule._control_lock():
                    self.fail('nested controller must be refused')
        self.assertEqual(caught.exception.code, 'schedule_control_busy')

    def test_symlink_launchagent_and_state_are_refused(self):
        target = self.base / 'foreign.json'
        target.write_text('{}')
        self.schedule.plist.parent.mkdir(parents=True)
        self.schedule.plist.symlink_to(target)
        with self.assertRaises(mod.ScheduleError):
            self.schedule._assert_owned_plist(self.schedule.plist)
        unsafe = self.base / 'unsafe.json'
        unsafe.symlink_to(target)
        with self.assertRaises(mod.ScheduleError):
            mod._atomic_json(unsafe, {'overwrite': True})
        self.assertEqual(target.read_text(), '{}')

    def test_cli_plan_parses_and_is_read_only(self):
        output = io.StringIO()
        with patch('sys.stdout', output):
            code = mod.main(['--data-dir', str(self.directory), '--state-root', str(self.schedule.state_root), '--list-name', self.list_name, '--plan'])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())['code'], 'schedule_plan')
        self.assertFalse(self.schedule.state_root.exists())

    def test_cli_corrupt_mirror_reports_json_without_native_registration(self):
        output = io.StringIO()
        with patch.object(mod.platform, 'system', return_value='Darwin'), \
                patch.object(mod.NativeSchedule, '_bootstrap_status',
                             side_effect=mod.StateError('state_recovery_required', 'mapping corrupted')), \
                patch.object(mod, '_run') as run, patch('sys.stdout', output):
            code = mod.main(['--data-dir', str(self.directory), '--state-root',
                             str(self.schedule.state_root), '--enable'])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())['code'], 'state_recovery_required')
        run.assert_not_called()
        self.assertFalse(self.schedule.plist.exists())


    def initialize_real_mirror(self):
        import macos_reminders_sync as sync
        import task_store
        from test_macos_reminders_sync import FakeRemindersClient
        task_store.TaskStore(self.directory).execute({'op': 'init'})
        with patch.object(sync.platform, 'system', return_value='Darwin'):
            sync.execute(self.directory, state_root=self.schedule.state_root,
                         list_name=self.list_name, initialize=True, client=FakeRemindersClient())

    def test_list_name_reaches_spec_probe_periodic_bootstrap_and_registration(self):
        self.list_name = '团队待办 · 甲 "quote" $(literal)'
        self.schedule.requested_list_name = self.list_name
        self.probe_response['listName'] = self.list_name
        self.initialized['listName'] = self.list_name
        self.initialize_real_mirror()
        self.assertEqual(self.schedule._bootstrap_status()['listName'], self.list_name)
        self.assertEqual(self.schedule._bootstrap_status()['listId'], 'L-main')
        for config in [self.schedule._config(), self.schedule._config(probe=True, token='test')]:
            self.assertEqual(config['listName'], self.list_name)
            self.assertEqual(config['argv'].count('--list-name=' + self.list_name), 1)
        spec = self.schedule.plan()['spec']
        self.assertIn('--list-name=' + self.list_name, spec['command'])
        self.assertEqual(spec['listName'], self.list_name)
        self.enable_mocked()
        self.assertEqual(json.loads(self.schedule.manifest.read_text())['listName'], self.list_name)

    def test_old_commands_without_list_name_discover_binding_and_keep_helper_identity(self):
        self.initialize_real_mirror()
        old = mod.NativeSchedule(self.directory, self.schedule.state_root, home=self.home)
        self.assertEqual(old._bootstrap_status()['listName'], self.list_name)
        self.assertEqual(old.plan()['spec']['listName'], self.list_name)
        self.assertEqual(old.label, self.schedule.label)
        self.assertEqual(old.bundle_id, self.schedule.bundle_id)
        self.assertEqual(old.install_dir, self.schedule.install_dir)
        self.assertIn('--list-name=' + self.list_name, old._config()['argv'])

    def test_option_like_list_name_stays_data_in_generated_commands(self):
        import macos_reminders_sync as sync
        self.schedule.requested_list_name = '--scheduled'
        command = self.schedule.plan()['spec']['command'][1:]
        configs = [self.schedule._config(), self.schedule._config(probe=True, token='literal')]
        for argv in [command, *(config['argv'] for config in configs)]:
            with patch.object(sys, 'argv', argv), patch.object(sync, 'write_json'), \
                    patch.object(sync, 'execute', return_value={'ok': True}) as execute, patch('sys.stdout', io.StringIO()):
                self.assertEqual(sync.main(), 0)
            self.assertEqual(execute.call_args.kwargs['list_name'], '--scheduled')

    def test_new_schedule_without_name_requires_configuration_without_native_calls(self):
        fresh = mod.NativeSchedule(self.directory, self.schedule.state_root, home=self.home)
        with patch.object(mod, '_run') as native:
            with self.assertRaises(mod.StateError) as caught:
                fresh.plan()
        self.assertEqual(caught.exception.code, 'list_name_required')
        native.assert_not_called()
        self.assertFalse(self.schedule.state_root.exists())

    def test_explicit_other_name_is_rejected_before_schedule_changes(self):
        self.initialize_real_mirror()
        self.schedule.requested_list_name = '错误的另一个列表'
        with patch.object(mod, '_run') as native:
            with self.assertRaises(mod.StateError) as caught:
                self.schedule.plan()
        self.assertEqual(caught.exception.code, 'binding_conflict')
        native.assert_not_called()
        self.assertFalse(self.schedule.plist.exists())

    def test_status_and_disable_remain_available_with_damaged_mirror_registry(self):
        self.enable_mocked()
        record = json.loads(self.schedule.manifest.read_text())
        record.pop('listName')  # Old registrations did not store the name.
        mod._atomic_json(self.schedule.manifest, record)
        with patch.object(mod.platform, 'system', return_value='Darwin'), \
                patch.object(mod, '_run', side_effect=self.native_run), \
                patch.object(self.schedule, '_target_name', side_effect=mod.StateError('state_recovery_required', 'corrupt')):
            status = self.schedule.status()
            self.assertTrue(status['enabled'])
            self.assertEqual(status['mirrorState']['code'], 'state_recovery_required')
            self.assertEqual(self.schedule.disable()['code'], 'schedule_disabled')
        self.assertFalse(self.schedule.plist.exists())


@unittest.skipUnless(platform.system() == 'Darwin', 'Native compile and isolated Foundation runner require macOS')
class FixedHelperTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='team-tasks-helper-home-')
        self.addCleanup(temporary.cleanup)
        mocked_home = patch.object(Path, 'home', return_value=Path(temporary.name))
        mocked_home.start()
        self.addCleanup(mocked_home.stop)

    def test_helper_compiles_and_reuses_fixed_identity_without_launching(self):
        with tempfile.TemporaryDirectory(prefix='team-tasks-helper-build-test-') as temporary:
            base = Path(temporary)
            data = base / 'data'
            data.mkdir()
            schedule = mod.NativeSchedule(data, base / 'state', home=base / 'home', list_name='编译测试')
            mod._private_directory(schedule.install_dir)
            fingerprint = schedule._build_helper()
            with (schedule.app / 'Contents' / 'Info.plist').open('rb') as stream:
                info = plistlib.load(stream)
            self.assertEqual(info['CFBundleIdentifier'], schedule.bundle_id)
            self.assertEqual(info['CFBundleVersion'], mod.HELPER_VERSION)
            self.assertEqual(info['CFBundleShortVersionString'], mod.HELPER_VERSION)
            self.assertIn('提醒事项', info['NSAppleEventsUsageDescription'])
            self.assertTrue(info['LSUIElement'])
            schedule._record(fingerprint, 'disabled')
            with patch.object(mod, '_run', return_value=SimpleNamespace(returncode=0, stdout='', stderr='')) as run:
                self.assertEqual(schedule._build_helper(), fingerprint)
            run.assert_called_once_with(['/usr/bin/codesign', '--verify', str(schedule.app)])
            signed = subprocess.run(['/usr/bin/codesign', '--verify', str(schedule.app)],
                                    capture_output=True, text=True)
            self.assertEqual(signed.returncode, 0, signed.stderr)

    def test_helper_passes_arbitrary_text_as_argv_without_shell(self):
        with tempfile.TemporaryDirectory(prefix='team-tasks-helper-argv-test-') as temporary:
            base = Path(temporary)
            output = base / 'arguments.json'
            script = base / 'safe child.py'
            script.write_text('import json,sys\nfrom pathlib import Path\nPath(sys.argv[1]).write_text(json.dumps(sys.argv[2:],ensure_ascii=False))\n')
            malicious = '中文 $HOME `touch /tmp/never-team-tasks` ; $(echo exposed) "quote"'
            config = {'version': 1, 'owner': mod.OWNER, 'python': sys.executable,
                      'argv': [str(script), str(output), malicious], 'mode': 'scheduled',
                      'helperResultFile': str(base / 'helper.json'), 'logFile': str(base / 'log'),
                      'probeToken': None}
            path = base / 'config.json'
            mod._atomic_json(path, config)
            result = subprocess.run(['/usr/bin/osascript', '-l', 'JavaScript', str(mod.HELPER_SCRIPT),
                                     '--config', str(path)], capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text()), [malicious])
            helper = json.loads((base / 'helper.json').read_text())
            self.assertTrue(helper['ok'])
            self.assertEqual((base / 'helper.json').stat().st_mode & 0o777, 0o600)
            self.assertEqual((base / 'log').stat().st_mode & 0o777, 0o600)

    def test_helper_reports_child_failure_and_rotates_large_log(self):
        with tempfile.TemporaryDirectory(prefix='team-tasks-helper-failure-test-') as temporary:
            base = Path(temporary)
            script = base / 'failure.py'
            script.write_text('import sys\nprint("expected child failure")\nsys.exit(7)\n')
            log = base / 'sync.log'
            log.write_bytes(b'x' * (5242880 + 1))
            config = {'version': 1, 'owner': mod.OWNER, 'python': sys.executable,
                      'argv': [str(script)], 'mode': 'diagnose', 'probeToken': 'fixed-test-token',
                      'helperResultFile': str(base / 'helper.json'), 'logFile': str(log)}
            path = base / 'config.json'
            mod._atomic_json(path, config)
            result = subprocess.run(['/usr/bin/osascript', '-l', 'JavaScript', str(mod.HELPER_SCRIPT),
                                     '--config', str(path)], capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            helper = json.loads((base / 'helper.json').read_text())
            self.assertFalse(helper['ok'])
            self.assertEqual(helper['exitCode'], 7)
            self.assertEqual(helper['probeToken'], 'fixed-test-token')
            self.assertEqual((base / 'sync.log.previous').stat().st_size, 5242880 + 1)
            self.assertIn('expected child failure', log.read_text())


if __name__ == '__main__':
    unittest.main()
