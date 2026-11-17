#!/usr/bin/env python3
"""Install a zero-model macOS command schedule for the team-tasks mirror.

Nothing is installed on import or by --plan. Native enable/disable are explicit.
The same stable helper application executes both the launchd authorization probe
and recurring calls; an interactive Terminal invocation is never permission proof.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import plistlib
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from reminders_state import StateError, MirrorState

BEIJING = dt.timezone(dt.timedelta(hours=8))
TIMEZONE = 'Asia/Shanghai'
SYNC_SCRIPT = Path(__file__).with_name('macos_reminders_sync.py').resolve()
HELPER_SCRIPT = Path(__file__).with_name('macos_sync_helper.js').resolve()
DEFAULT_STATE_ROOT = Path.home() / 'Library' / 'Application Support' / 'team-tasks'
PLAN_TIMES = ['07:00'] + ['{:02d}:{:02d}'.format(hour, minute)
                         for hour in range(9, 22) for minute in range(0, 60, 10)] + ['22:00']
OWNER = 'team-tasks.macos-sync.v1'
HELPER_VERSION = '1.6.4'


class ScheduleError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def schedule_slot(now=None):
    """Return the Beijing minute's slot, or None; never catch up missed slots."""
    stamp = now if now is not None else dt.datetime.now(dt.timezone.utc)
    if not isinstance(stamp, dt.datetime) or stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError('schedule_slot requires a timezone-aware datetime')
    local = stamp.astimezone(BEIJING)
    if local.strftime('%H:%M') not in PLAN_TIMES:
        return None
    return local.replace(second=0, microsecond=0).isoformat(timespec='minutes')


def _local_path(value, *, directory=False, executable=False):
    path = Path(value).expanduser().resolve()
    if not path.is_absolute() or (directory and not path.is_dir()) or (not directory and not path.is_file()):
        raise ScheduleError('invalid_local_path', 'Local path is missing: ' + str(path))
    if executable and not os.access(path, os.X_OK):
        raise ScheduleError('invalid_interpreter', 'Python interpreter is not executable: ' + str(path))
    return path


def schedule_spec(directory=None, interpreter=None, state_root=None, *, list_name=None):
    """Portable command-job specification; callers register it using their own APIs."""
    command = None
    if directory is not None:
        data = _local_path(directory, directory=True)
        python = _local_path(interpreter or sys.executable, executable=True)
        script = _local_path(SYNC_SCRIPT)
        list_name = MirrorState(data, list_name, state_root).list_name
        command = [str(python), str(script), '--data-dir', str(data), '--scheduled', '--list-name=' + list_name]
        if state_root is not None:
            command.extend(['--state-root', str(Path(state_root).expanduser().resolve())])
    return {'version': 1, 'timezone': TIMEZONE, 'listName': list_name, 'dailyTimes': list(PLAN_TIMES),
            'dailySlotCount': len(PLAN_TIMES), 'weekdays': 'all', 'command': command,
            'callsModel': False, 'missedSlots': 'skip', 'maxConcurrentRuns': 1,
            'duplicateSlots': 'skip_after_success',
            'registration': 'Use a direct command job; an assistant/model job is not equivalent.'}


def _atomic_json(path, value):
    _private_directory(path.parent)
    if path.is_symlink():
        raise ScheduleError('unsafe_state_path', 'Refusing symlink state file: ' + str(path))
    fd, temp = tempfile.mkstemp(prefix='.' + path.name + '.', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            os.chmod(temp, 0o600)
            json.dump(value, stream, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def _private_directory(path):
    if path.is_symlink():
        raise ScheduleError('unsafe_state_path', 'Refusing symlink state directory: ' + str(path))
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.stat().st_uid != os.getuid():
        raise ScheduleError('unsafe_state_owner', 'State directory belongs to another user: ' + str(path))
    os.chmod(path, 0o700)


def _read_json(path):
    if path.is_symlink():
        raise ScheduleError('unsafe_state_path', 'Refusing symlink state file: ' + str(path))
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return None
    except (ValueError, OSError) as exc:
        raise ScheduleError('invalid_schedule_state', 'Cannot read schedule state: ' + str(path)) from exc
    if not isinstance(value, dict):
        raise ScheduleError('invalid_schedule_state', 'Expected a JSON object: ' + str(path))
    return value


def _run(command, timeout=30):
    try:
        return subprocess.run(command, capture_output=True, text=True, check=False, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ScheduleError('native_command_failed', str(exc)) from exc


def _require_success(result, operation):
    if result.returncode:
        raise ScheduleError('native_command_failed', operation + ': ' + (result.stderr.strip() or result.stdout.strip()))


class NativeSchedule:
    def __init__(self, directory, state_root=None, interpreter=None, *, home=None, uid=None, list_name=None):
        self.directory = _local_path(directory, directory=True)
        self.requested_list_name = list_name
        self.interpreter = _local_path(interpreter or sys.executable, executable=True)
        self.script = _local_path(SYNC_SCRIPT)
        self.state_root = Path(state_root or DEFAULT_STATE_ROOT).expanduser().resolve()
        self.home = Path(home or Path.home()).expanduser().resolve()
        self.uid = os.getuid() if uid is None else uid
        self.namespace = hashlib.sha256(str(self.directory).encode('utf-8')).hexdigest()
        self.label = 'com.team-tasks.reminders-sync.' + self.namespace[:20]
        self.domain = 'gui/' + str(self.uid)
        self.install_dir = self.state_root / 'schedules' / self.namespace
        self.app = self.install_dir / 'TeamTasksReminders.app'
        self.bundle_id = self.label
        self.config = self.install_dir / 'scheduled-config.json'
        self.probe_config = self.install_dir / 'probe-config.json'
        self.probe_result = self.install_dir / 'probe-result.json'
        self.probe_helper_result = self.install_dir / 'probe-helper-result.json'
        self.last_result = self.install_dir / 'last-result.json'
        self.helper_result = self.install_dir / 'helper-result.json'
        self.manifest = self.install_dir / 'registration.json'
        self.plist = self.home / 'Library' / 'LaunchAgents' / (self.label + '.plist')
        self.probe_plist = self.install_dir / 'probe.plist'
        self.probe_label = self.label + '.probe'

    def _require_macos(self):
        if platform.system() != 'Darwin':
            raise ScheduleError('native_schedule_requires_macos', 'macOS LaunchAgent installation requires a Mac execution host')

    @contextmanager
    def _control_lock(self):
        import fcntl
        _private_directory(self.state_root)
        _private_directory(self.state_root / 'schedules')
        _private_directory(self.install_dir)
        path = self.install_dir / '.schedule-control.lock'
        fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'a+b') as stream:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ScheduleError('schedule_control_busy', 'Another enable, disable or diagnostic is running') from exc
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def plan(self):
        return {'ok': True, 'code': 'schedule_plan',
                'spec': schedule_spec(self.directory, self.interpreter, self.state_root, list_name=self._target_name()),
                'macFallback': {'type': 'LaunchAgent', 'label': self.label,
                                'plist': str(self.plist), 'helperApp': str(self.app),
                                'stateRoot': str(self.state_root), 'checkerIntervalSeconds': 60,
                                'proof': 'One-shot --diagnose through the same GUI launchd/helper chain.',
                                'requiresInitializedMirror': True, 'installsAnything': False}}

    def _app_command(self, config):
        # open -n starts a new helper process with its own NSProcessInfo.arguments;
        # -W keeps launchd's process alive until its child app exits.
        return ['/usr/bin/open', '-n', '-W', str(self.app), '--args', '--config', str(config)]

    def _plist_data(self, probe=False):
        config = self.probe_config if probe else self.config
        label = self.probe_label if probe else self.label
        result = {'Label': label, 'ProgramArguments': self._app_command(config),
                  'RunAtLoad': bool(probe), 'ProcessType': 'Background',
                  'LimitLoadToSessionType': 'Aqua',
                  'StandardOutPath': str(self.install_dir / 'launcher.stdout.log'),
                  'StandardErrorPath': str(self.install_dir / 'launcher.stderr.log'),
                  'EnvironmentVariables': {'TEAM_TASKS_SCHEDULE_OWNER': OWNER}}
        if not probe:
            result['StartInterval'] = 60
        return result

    def _assert_owned_plist(self, path, probe=False, *, allow_absent=True):
        if path.is_symlink():
            raise ScheduleError('schedule_ownership_conflict', 'Refusing symlink LaunchAgent: ' + str(path))
        if not path.exists():
            if allow_absent:
                return False
            raise ScheduleError('schedule_ownership_conflict', 'Missing owned LaunchAgent: ' + str(path))
        try:
            with path.open('rb') as stream:
                actual = plistlib.load(stream)
        except (OSError, ValueError, plistlib.InvalidFileException) as exc:
            raise ScheduleError('schedule_ownership_conflict', 'Unreadable LaunchAgent: ' + str(path)) from exc
        expected = self._plist_data(probe)
        if actual != expected or path.stat().st_uid != os.getuid():
            raise ScheduleError('schedule_ownership_conflict', 'LaunchAgent does not match this installer: ' + str(path))
        return True

    def _write_plist(self, path, probe=False):
        self._assert_owned_plist(path, probe)
        if path.parent.is_symlink():
            raise ScheduleError('unsafe_state_path', 'Refusing symlink LaunchAgents directory')
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd, temp = tempfile.mkstemp(prefix='.' + path.name + '.', dir=str(path.parent))
        try:
            with os.fdopen(fd, 'wb') as stream:
                os.chmod(temp, 0o600)
                plistlib.dump(self._plist_data(probe), stream, sort_keys=True)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)

    def _loaded(self, probe=False, *, timeout=30):
        label = self.probe_label if probe else self.label
        return _run(['/bin/launchctl', 'print', self.domain + '/' + label], timeout=timeout).returncode == 0

    def _bootout(self, probe=False):
        path = self.probe_plist if probe else self.plist
        self._assert_owned_plist(path, probe, allow_absent=False)
        if self._loaded(probe):
            _require_success(_run(['/bin/launchctl', 'bootout', self.domain + '/' +
                                  (self.probe_label if probe else self.label)]), 'Stopping owned LaunchAgent')

    def _target_name(self):
        # Resolve lazily: a damaged mirror must never prevent --status/--disable.
        return MirrorState(self.directory, self.requested_list_name, self.state_root).list_name

    def _bootstrap_status(self):
        from macos_reminders_sync import bootstrap_status
        return bootstrap_status(self.directory, self.state_root, list_name=self._target_name())

    def _config(self, *, probe=False, token=None):
        target_name = self._target_name()
        argv = [str(self.script), '--data-dir', str(self.directory), '--state-root', str(self.state_root),
                '--list-name=' + target_name]
        if probe:
            argv.extend(['--diagnose', '--native-check', '--result-file', str(self.probe_result), '--probe-token', token])
        else:
            argv.extend(['--scheduled', '--result-file', str(self.last_result)])
        return {'version': 1, 'owner': OWNER, 'python': str(self.interpreter), 'argv': argv, 'listName': target_name,
                'mode': 'diagnose' if probe else 'scheduled',
                'helperResultFile': str(self.probe_helper_result if probe else self.helper_result),
                'logFile': str(self.install_dir / ('probe.log' if probe else 'sync.log')),
                'probeToken': token if probe else None}

    def _build_helper(self):
        source = _local_path(HELPER_SCRIPT)
        fingerprint = hashlib.sha256(source.read_bytes()).hexdigest()
        record = _read_json(self.manifest)
        if record and (record.get('owner') != OWNER or record.get('namespace') != self.namespace):
            raise ScheduleError('schedule_ownership_conflict', 'Unexpected schedule registration record')
        if self.app.is_symlink():
            raise ScheduleError('schedule_ownership_conflict', 'Refusing symlink helper app')
        if self.app.exists():
            if not record:
                raise ScheduleError('schedule_ownership_conflict', 'An unregistered helper app already exists')
            if record.get('helperFingerprint') == fingerprint:
                with (self.app / 'Contents' / 'Info.plist').open('rb') as stream:
                    info = plistlib.load(stream)
                if info.get('CFBundleIdentifier') != self.bundle_id:
                    raise ScheduleError('schedule_ownership_conflict', 'Helper bundle identity was changed')
                if info.get('CFBundleVersion') == HELPER_VERSION and info.get('CFBundleShortVersionString') == HELPER_VERSION:
                    _require_success(_run(['/usr/bin/codesign', '--verify', str(self.app)]),
                                     'Verifying installed fixed helper')
                    return fingerprint
        with tempfile.TemporaryDirectory(prefix='.helper-build-', dir=str(self.install_dir)) as staging:
            built = Path(staging) / self.app.name
            _require_success(_run(['/usr/bin/osacompile', '-l', 'JavaScript', '-o', str(built), str(source)], timeout=60),
                             'Compiling fixed Reminders helper')
            info_path = built / 'Contents' / 'Info.plist'
            with info_path.open('rb') as stream:
                info = plistlib.load(stream)
            info.update({'CFBundleIdentifier': self.bundle_id, 'CFBundleName': '团队待办同步',
                         'CFBundleVersion': HELPER_VERSION, 'CFBundleShortVersionString': HELPER_VERSION,
                         'LSUIElement': True,
                         'NSAppleEventsUsageDescription': '团队待办同步需要访问提醒事项，读取完成状态并更新团队待办列表。'})
            with info_path.open('wb') as stream:
                plistlib.dump(info, stream)
            _require_success(_run(['/usr/bin/codesign', '--force', '--sign', '-', '--identifier', self.bundle_id, str(built)], timeout=60),
                             'Signing fixed helper identity')
            old = self.install_dir / ('.helper-old-' + uuid.uuid4().hex)
            if self.app.exists():
                os.replace(self.app, old)
            try:
                os.replace(built, self.app)
            except OSError:
                if old.exists():
                    os.replace(old, self.app)
                raise
            if old.exists():
                shutil.rmtree(old)
        return fingerprint

    def _probe(self, timeout=150):
        # All tokens and user paths are private JSON data, never executable source.
        token = uuid.uuid4().hex
        config = self._config(probe=True, token=token)
        target_name = config['listName']
        _atomic_json(self.probe_config, config)
        self._write_plist(self.probe_plist, probe=True)
        self._bootout(probe=True)
        try:
            _require_success(_run(['/bin/launchctl', 'bootstrap', self.domain, str(self.probe_plist)]),
                             'Starting background authorization probe')
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                response = _read_json(self.probe_result)
                helper = _read_json(self.probe_helper_result)
                if response and response.get('probeToken') == token:
                    if response.get('ok') is not True:
                        raise ScheduleError(response.get('code', 'background_probe_failed'), response.get('message', 'Background access failed'))
                    if (response.get('requestMode') != 'diagnose' or not response.get('initialized') or
                            response.get('nativeProbeVerified') is not True or
                            response.get('listName') != target_name):
                        raise ScheduleError('invalid_background_proof', 'Background diagnostic did not prove initialized mirror access')
                    return response
                if helper and helper.get('probeToken') == token and helper.get('ok') is False:
                    raise ScheduleError('background_probe_failed', helper.get('message', 'Fixed helper could not run diagnostic'))
                time.sleep(.1)
            raise ScheduleError('background_probe_timeout',
                                '后台权限验证超时；请在系统设置 → 隐私与安全性 → 自动化中检查「团队待办同步」。周期任务未启用。')
        finally:
            self._bootout(probe=True)

    def _record(self, fingerprint, phase, **fields):
        target_name = fields.get('initialized', {}).get('listName')
        if target_name is None:
            target_name = self._target_name()
        result = {'version': 1, 'owner': OWNER, 'namespace': self.namespace,
                  'directory': str(self.directory), 'listName': target_name, 'interpreter': str(self.interpreter),
                  'script': str(self.script), 'label': self.label, 'helperFingerprint': fingerprint,
                  'phase': phase, 'updatedAt': dt.datetime.now(dt.timezone.utc).isoformat()}
        result.update(fields)
        _atomic_json(self.manifest, result)
        return result

    def enable(self):
        self._require_macos()
        with self._control_lock():
            return self._enable()

    def _enable(self):
        initialized = self._bootstrap_status()
        if not initialized.get('initialized'):
            raise ScheduleError('mirror_not_initialized',
                                '先显式运行 --initialize-mirror，在新建或空列表完成初始化和验证，再启用定时同步。')
        _private_directory(self.install_dir)
        self._assert_owned_plist(self.plist)
        # Never replace a loaded job sharing our label when its owned plist is absent.
        if self._loaded() and not self.plist.exists():
            raise ScheduleError('schedule_ownership_conflict', 'A loaded job uses this label without the owned LaunchAgent file')
        if self.plist.exists():
            self._bootout()
        fingerprint = self._build_helper()
        self._record(fingerprint, 'probing', initialized=initialized)
        try:
            proof = self._probe()
        except (ScheduleError, StateError, OSError) as exc:
            self._record(fingerprint, 'disabled', initialized=initialized,
                         lastError={'code': getattr(exc, 'code', 'schedule_error'), 'message': str(exc)})
            raise
        try:
            spec = schedule_spec(self.directory, self.interpreter, self.state_root, list_name=self._target_name())
            _atomic_json(self.config, self._config())
            self._write_plist(self.plist)
            _require_success(_run(['/bin/launchctl', 'bootstrap', self.domain, str(self.plist)]),
                             'Enabling periodic command sync')
            self._record(fingerprint, 'enabled', initialized=initialized,
                         backgroundProof={'probeToken': proof['probeToken'], 'provedAt': dt.datetime.now(dt.timezone.utc).isoformat()})
        except (ScheduleError, StateError, OSError) as exc:
            if self.plist.exists():
                self._bootout()
            self._record(fingerprint, 'disabled', initialized=initialized,
                         lastError={'code': getattr(exc, 'code', 'schedule_error'), 'message': str(exc)})
            raise
        return {'ok': True, 'code': 'schedule_enabled', 'label': self.label,
                'spec': spec,
                'backgroundProof': True, 'callsModel': False}

    def disable(self):
        self._require_macos()
        with self._control_lock():
            return self._disable()

    def _disable(self):
        record = _read_json(self.manifest)
        if record and (record.get('owner') != OWNER or record.get('namespace') != self.namespace):
            raise ScheduleError('schedule_ownership_conflict', 'Unexpected schedule registration record')
        owned = self._assert_owned_plist(self.plist)
        if not owned:
            if self._loaded():
                raise ScheduleError('schedule_ownership_conflict', 'Loaded job has no matching owned plist; refusing to stop it')
            return {'ok': True, 'code': 'schedule_already_disabled', 'label': self.label}
        self._bootout()
        self.plist.unlink()
        if record:
            record.update(phase='disabled', updatedAt=dt.datetime.now(dt.timezone.utc).isoformat())
            _atomic_json(self.manifest, record)
        return {'ok': True, 'code': 'schedule_disabled', 'label': self.label,
                'retained': ['helper identity', 'mirror data', 'background proof', 'logs']}

    def status(self):
        record = _read_json(self.manifest)
        if record and (record.get('owner') != OWNER or record.get('namespace') != self.namespace):
            raise ScheduleError('schedule_ownership_conflict', 'Unexpected schedule registration record')
        owned = self._assert_owned_plist(self.plist)
        loaded = self._loaded(timeout=1) if platform.system() == 'Darwin' else False
        if loaded and not owned:
            raise ScheduleError('schedule_ownership_conflict', 'Loaded job has no matching owned plist')
        last = _read_json(self.last_result)
        helper = _read_json(self.helper_result)
        target = {'listName': record.get('listName') if record else None}
        if target['listName'] is None:
            try:
                target['listName'] = self._target_name()
            except StateError as exc:
                target['mirrorState'] = {'code': exc.code, 'message': str(exc)}
        return {'ok': True, 'code': 'schedule_status', 'label': self.label, 'enabled': loaded and owned,
                **target,
                'platform': platform.system(), 'registration': record,
                'lastSync': last, 'lastHelper': helper, 'callsModel': False,
                'logFile': str(self.install_dir / 'sync.log'),
                'permissionAdvice': '系统设置 → 隐私与安全性 → 自动化 → 团队待办同步 → 提醒事项；拒绝授权后不会更换身份重试。'}

    def diagnose(self):
        self._require_macos()
        with self._control_lock():
            return self._diagnose()

    def _diagnose(self):
        record = _read_json(self.manifest)
        if not record or record.get('owner') != OWNER or record.get('namespace') != self.namespace:
            raise ScheduleError('schedule_not_installed', 'Run --enable after explicit mirror initialization to install the fixed helper')
        self._assert_owned_plist(self.probe_plist, probe=True, allow_absent=False)
        return {'ok': True, 'code': 'schedule_diagnosed', 'backgroundProof': self._probe(), 'callsModel': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True)
    parser.add_argument('--state-root', help='Stable private app-data root; defaults to ~/Library/Application Support/team-tasks')
    parser.add_argument('--list-name', help='Explicit mirror list name; reuse the existing binding when omitted')
    parser.add_argument('--interpreter', help='Fixed executable Python path; defaults to this process interpreter')
    action = parser.add_mutually_exclusive_group(required=True)
    for name in ['plan', 'enable', 'disable', 'status', 'diagnose']:
        action.add_argument('--' + name, action='store_true')
    args = parser.parse_args(argv)
    try:
        scheduler = NativeSchedule(args.data_dir, args.state_root, args.interpreter, list_name=args.list_name)
        operation = next(name for name in ['plan', 'enable', 'disable', 'status', 'diagnose'] if getattr(args, name))
        result = getattr(scheduler, operation)()
    except (ScheduleError, StateError) as exc:
        result = {'ok': False, 'code': exc.code, 'message': str(exc)}
    except (OSError, TypeError, KeyError, ValueError) as exc:
        result = {'ok': False, 'code': 'schedule_error', 'message': str(exc)}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
