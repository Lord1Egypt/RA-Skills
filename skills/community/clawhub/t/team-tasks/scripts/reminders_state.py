"""Private, durable adapter state; separate from the task-store transaction."""

import hashlib
from contextlib import contextmanager
import json
import os
import re
from pathlib import Path
import stat
import tempfile
import time
import uuid


class StateError(Exception):
    def __init__(self, code, message, details=None):
        self.code, self.details = code, details or {}
        super().__init__(message)


def namespace_for(directory):
    return hashlib.sha256(str(Path(directory).resolve()).encode('utf-8')).hexdigest()


def state_root_path(value=None):
    return Path(value).expanduser().resolve() if value else Path.home() / 'Library' / 'Application Support' / 'team-tasks'


def validate_list_name(value):
    if (not isinstance(value, str) or not value.strip() or
            any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value)):
        raise StateError('invalid_list_name', '列表名称必须是非空文本，且不能包含换行或控制字符')
    return value


def validate_binding(value, list_name):
    """Validate the durable identity independently of its storage location."""
    if not isinstance(value, dict) or value.get('version') != 1 or value.get('listName') != list_name:
        raise StateError('state_recovery_required', '初始化绑定格式无效，保留原文件核查')
    validate_list_name(list_name)
    origin = value.get('namespaceDir', value.get('dataDir'))
    if (not isinstance(value.get('dataDir'), str) or not Path(value['dataDir']).is_absolute() or
            not isinstance(origin, str) or not Path(origin).is_absolute() or
            value.get('namespace') != hashlib.sha256(origin.encode('utf-8')).hexdigest()):
        raise StateError('state_recovery_required', '绑定目录或命名空间无效，保留原文件核查')
    if value.get('phase') not in ('prepared', 'deleting_old', 'rebuilding', 'verifying', 'complete'):
        raise StateError('state_recovery_required', '未知初始化阶段')
    if not isinstance(value.get('listId'), str) or not value['listId']:
        raise StateError('state_recovery_required', '初始化绑定缺少原生列表 ID')
    if (not isinstance(value.get('oldIds'), list) or
            not all(isinstance(item, str) and item for item in value['oldIds']) or
            len(set(value['oldIds'])) != len(value['oldIds']) or
            not isinstance(value.get('backup'), str) or not re.fullmatch(r'[a-f0-9]{32}\.json', value['backup']) or
            not isinstance(value.get('backupHash'), str) or not re.fullmatch(r'[a-f0-9]{64}', value['backupHash'])):
        raise StateError('state_recovery_required', '初始化记录中的旧 ID 集合或快照校验无效')
    imports = value.get('legacyImports', {})
    if not isinstance(imports, dict):
        raise StateError('state_recovery_required', '旧绑定归档记录无效')
    for source, evidence in imports.items():
        if (not isinstance(source, str) or not Path(source).is_absolute() or
                not isinstance(evidence, dict) or
                not re.fullmatch(r'[a-f0-9]{64}', str(evidence.get('sha256', ''))) or
                not isinstance(evidence.get('archive'), str) or not Path(evidence['archive']).is_absolute()):
            raise StateError('state_recovery_required', '旧绑定归档记录无效')
    return value


def binding_records(state_root=None):
    """Read the shared registry plus this caller's legacy registry, without writes.

    Imported originals remain as evidence. Their exact hashes let all new callers
    detect an old installation still writing them, even with another state root.
    """
    shared = state_root_path() / 'mirror-bindings'
    legacy = state_root_path(state_root) / 'mirror-bindings'
    records = {}
    for directory in dict.fromkeys((shared, legacy)):
        if not directory.exists() and not directory.is_symlink():
            continue
        check_directory(directory)
        for path in sorted(directory.glob('*.json')):
            value, raw = read_json(path, with_bytes=True)
            name = value.get('listName') if isinstance(value, dict) else None
            validate_binding(value, name)
            if path.name != hashlib.sha256(name.encode('utf-8')).hexdigest() + '.json':
                raise StateError('state_recovery_required', '绑定文件名与列表名称不一致')
            for source, evidence in value.get('legacyImports', {}).items():
                original = read_json(Path(source), with_bytes=True)
                if original is not None and hashlib.sha256(original[1]).hexdigest() != evidence['sha256']:
                    raise StateError('binding_conflict', '已迁入的旧绑定仍在变化；停用旧版同步后核查',
                                     {'listName': name, 'legacyBindingPath': source})
            if name in records:
                current = records[name][0]
                imported = current.get('legacyImports', {}).get(str(path))
                if current != value and (not imported or imported['sha256'] != hashlib.sha256(raw).hexdigest()):
                    raise StateError('binding_conflict', '公共绑定与旧状态根中的绑定冲突，保留双方核查',
                                     {'listName': name, 'bindingPath': str(records[name][1]),
                                      'legacyBindingPath': str(path)})
                continue
            records[name] = (value, path)
    directories = {}
    native_ids = {}
    for name, (value, _) in records.items():
        if value['dataDir'] in directories or value['listId'] in native_ids:
            raise StateError('binding_conflict', '同一台账或原生列表存在多个绑定，保留状态核查')
        directories[value['dataDir']] = name
        native_ids[value['listId']] = name
    return records


def check_directory(path):
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o022:
        raise StateError('state_recovery_required', '状态目录必须属于当前用户且不能被其他用户写入：' + str(path))


def private_directory(path):
    path = Path(path)
    if not path.exists():
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
    check_directory(path)
    return path


@contextmanager
def registry_lock(directory):
    """Serialize short identity commits across differently named list locks."""
    import fcntl
    private_directory(directory)
    fd = os.open(directory / '.registry.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a+b') as lock:
        info = os.fstat(lock.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_nlink != 1 or info.st_mode & 0o077:
            raise StateError('state_recovery_required', '公共绑定锁必须是当前用户的私有普通文件')
        deadline = time.monotonic() + 30
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise StateError('macos_sync_lock_timeout', '公共绑定正在更新')
                time.sleep(.05)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def read_json(path, missing=None, *, with_bytes=False):
    path = Path(path)
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except FileNotFoundError:
        return missing
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_nlink != 1 or info.st_mode & 0o077:
            raise StateError('state_recovery_required', '状态文件必须是当前用户的私有普通文件：' + str(path))
        try:
            raw = stream.read()
            def unique_pairs(pairs):
                out = {}
                for key, item in pairs:
                    if key in out:
                        raise ValueError('Duplicate JSON key')
                    out[key] = item
                return out
            value = json.loads(raw, object_pairs_hook=unique_pairs,
                               parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
        except (ValueError, UnicodeError) as exc:
            raise StateError('state_recovery_required', '状态文件损坏；不能重新初始化覆盖：' + str(path)) from exc
        current = path.lstat()
        if (info.st_dev, info.st_ino) != (current.st_dev, current.st_ino):
            raise StateError('state_recovery_required', '读取期间状态文件被替换')
        return (value, raw) if with_bytes else value


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def write_json(path, value, exclusive=False):
    write_private_bytes(path, json_bytes(value), exclusive=exclusive)


def write_private_bytes(path, raw, exclusive=False):
    path = Path(path)
    private_directory(path.parent)
    if path.exists():
        read_json(path)  # Reject symlinks, hard links and unsafe replacement targets.
        if exclusive:
            raise StateError('state_conflict', '备份快照已存在，不能覆盖')
    elif path.is_symlink():
        raise StateError('state_recovery_required', '状态文件不能是符号链接')
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if Path(name).read_bytes() != raw:
            raise StateError('state_recovery_required', '状态临时文件回读不一致')
        os.replace(name, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class MirrorState:
    def __init__(self, directory, list_name=None, state_root=None):
        self.root = Path(directory).resolve()
        self.namespace = namespace_for(self.root)
        self.state_root = state_root_path(state_root)
        self.map_path = self.root / 'reminders-map.json'
        records = binding_records(self.state_root)
        if list_name is None:
            matches = [name for name, (value, _) in records.items() if value['dataDir'] == str(self.root)]
            # A full directory relocation brings its map; retain the original name
            # and namespace and let binding() require explicit --rebind.
            if not matches:
                mapping = read_json(self.map_path)
                if mapping is not None:
                    if not isinstance(mapping, dict):
                        raise StateError('state_recovery_required', '映射格式无效')
                    matches = [name for name, (value, _) in records.items()
                               if value['listId'] == mapping.get('listId') and value['namespace'] == mapping.get('namespace')]
                    if not matches:
                        raise StateError('state_recovery_required', '映射没有对应绑定；保留状态核查')
            if len(matches) != 1:
                raise StateError('list_name_required', '此台账尚未配置镜像；首次启用请指定 --list-name，台账功能可继续使用')
            list_name = matches[0]
        self.list_name = validate_list_name(list_name)
        key = hashlib.sha256(self.list_name.encode('utf-8')).hexdigest()
        self.binding_dir = state_root_path() / 'mirror-bindings'
        self.binding_path = self.binding_dir / (key + '.json')
        self.binding_lock = self.binding_dir / (key + '.lock')
        self.legacy_binding_path = self.state_root / 'mirror-bindings' / (key + '.json')
        self.check_ledger_binding(records)

    def check_ledger_binding(self, records=None):
        records = binding_records(self.state_root) if records is None else records
        for name, (value, _) in records.items():
            if value['dataDir'] == str(self.root) and name != self.list_name:
                raise StateError('binding_conflict', '此台账已绑定其他列表，不能自动建立第二镜像',
                                 {**self.binding_details(value), 'requestedListName': self.list_name})

    def binding_details(self, value):
        return {'listName': value['listName'], 'expectedDataDir': str(self.root), 'boundDataDir': value['dataDir'],
                'expectedNamespace': namespace_for(self.root), 'boundNamespace': value['namespace'],
                'bindingPath': str(self.binding_dir / (hashlib.sha256(value['listName'].encode('utf-8')).hexdigest() + '.json')),
                'listId': value['listId'],
                'initializationPhase': value['phase']}

    def check_native_target(self, list_id, records=None):
        records = binding_records(self.state_root) if records is None else records
        for name, (value, _) in records.items():
            if value['listId'] == list_id and name != self.list_name:
                raise StateError('binding_conflict', '此原生列表已被其他名称的绑定占用；改名不会解除占用',
                                 {**self.binding_details(value), 'requestedListName': self.list_name})

    def binding(self):
        self.check_ledger_binding()
        value = self.read_binding()
        if value is None:
            return None
        if value['dataDir'] != str(self.root):
            raise StateError('binding_conflict',
                             '目标列表已绑定 {}，当前台账为 {}；独立台账请指定其他 --list-name，同一台账搬迁才使用 --rebind'.format(value['dataDir'], self.root),
                             self.binding_details(value))
        self.namespace = value['namespace']
        return value

    def read_binding(self):
        """Validate identity without enforcing location, for explicit relocation only."""
        record = binding_records(self.state_root).get(self.list_name)
        return record[0] if record else None

    def migrate_legacy_binding(self):
        """Called only inside the shared list lock and ledger lock, before writes.

        Archive exact bytes, then atomically publish the canonical record last.
        The original is retained; hashes distinguish it from later stale writes.
        """
        self.check_ledger_binding()
        if self.legacy_binding_path == self.binding_path:
            return
        original = read_json(self.legacy_binding_path, with_bytes=True)
        if original is None:
            return
        value, raw = original
        validate_binding(value, self.list_name)
        self.mapping(value, required=value['phase'] in ('complete', 'verifying'))
        canonical = read_json(self.binding_path)
        source = str(self.legacy_binding_path)
        checksum = hashlib.sha256(raw).hexdigest()
        if canonical and source in canonical.get('legacyImports', {}):
            return  # binding_records already verified the retained original.
        if canonical is not None and canonical != value:
            raise StateError('binding_conflict', '公共绑定与旧绑定冲突，不能迁入')
        archive_root = private_directory(state_root_path() / 'binding-migration-backups')
        archive = archive_root / uuid.uuid4().hex
        write_private_bytes(archive / 'binding.json', raw, exclusive=True)
        if read_json(archive / 'binding.json', with_bytes=True)[1] != raw:
            raise StateError('state_recovery_required', '旧绑定归档回读不一致')
        write_json(archive / 'manifest.json', {'version': 1, 'source': source, 'sha256': checksum}, exclusive=True)
        for parent in (archive_root, archive_root.parent):
            fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        updated = {**value, 'legacyImports': {**value.get('legacyImports', {}),
                   source: {'sha256': checksum, 'archive': str(archive)}}}
        if read_json(self.legacy_binding_path, with_bytes=True) != original:
            raise StateError('binding_conflict', '归档期间旧绑定发生变化，保留原绑定核查')
        self.save_binding(updated)

    def mapping(self, binding, required=True):
        value = read_json(self.map_path)
        if value is None:
            if required:
                raise StateError('state_recovery_required', '映射丢失；恢复状态文件，不能重新清空列表')
            return None
        if not isinstance(value, dict) or value.get('version') != 1 or value.get('namespace') != binding['namespace'] or value.get('listId') != binding['listId'] or not isinstance(value.get('tasks'), dict):
            raise StateError('state_recovery_required', '映射与初始化绑定不一致')
        seen = set()
        for tid, entry in value['tasks'].items():
            if not isinstance(entry, dict) or entry.get('state') not in ('mirrored', 'terminal', 'detached') or type(entry.get('missing', 0)) is not int or entry.get('missing', 0) < 0:
                raise StateError('state_recovery_required', '任务映射记录无效：' + str(tid))
            native_id = entry.get('reminderId')
            if not isinstance(native_id, str) or not native_id or native_id in seen:
                raise StateError('state_recovery_required', '原生事项 ID 映射无效或重复')
            seen.add(native_id)
            if not re.fullmatch(r'T-\d{6}-\d{3,}', tid):
                raise StateError('state_recovery_required', '任务映射 ID 无效')
            for field in ('observedFingerprint', 'pendingFingerprint'):
                fingerprint = entry.get(field)
                if fingerprint is not None and (not isinstance(fingerprint, str) or not re.fullmatch(r'[a-f0-9]{64}', fingerprint)):
                    raise StateError('state_recovery_required', '状态历史基线无效：' + tid)
            if entry['state'] in ('mirrored', 'terminal') and not entry.get('observedFingerprint'):
                raise StateError('state_recovery_required', '任务状态历史基线丢失：' + tid)
            if entry['state'] == 'mirrored' and not entry.get('pendingFingerprint'):
                raise StateError('state_recovery_required', '待处理任务同步基线丢失：' + tid)
        return value

    def save_binding(self, value):
        validate_binding(value, self.list_name)
        with registry_lock(self.binding_dir):
            records = binding_records(self.state_root)
            self.check_ledger_binding(records)
            self.check_native_target(value['listId'], records)
            write_json(self.binding_path, value)

    def save_map(self, value):
        write_json(self.map_path, value)

    def empty_map(self, list_id):
        return {'version': 1, 'namespace': self.namespace, 'listId': list_id, 'tasks': {}}
