#!/usr/bin/env python3
"""Local POSIX JSON task store. Standard library only; all callers must cooperate."""
import argparse
import copy
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager, ExitStack

MAIN = 'team-tasks.json'
ARCHIVE = re.compile(r'team-tasks-archive-\d{4}-(?:0[1-9]|1[0-2])\.json\Z')
SNAPSHOT = re.compile(r'\d{8}T\d{6}\.\d{6}Z-[0-9a-f]{32}\Z')
EDITABLE = {'title', 'description', 'priority', 'isBlocking', 'tags', 'assignee',
            'assigneeId', 'dueDate', 'dueTime', 'notifyTargetId', 'snoozedUntil',
            'lastProgressAt'}
CREATE = EDITABLE | {'creator', 'creatorId', 'sourceType', 'sourceId'}


class StoreError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def require(condition, message, code='validation_failed'):
    if not condition:
        raise StoreError(code, message)


def now():
    return dt.datetime.now().astimezone().isoformat()


def digest(raw):
    return hashlib.sha256(raw).hexdigest() if raw is not None else None


def status_history_fingerprint(task):
    """CAS token for status changes; unrelated comments and edits leave it stable."""
    history = [entry for entry in task['history']
               if entry['action'] in ('create', 'status', 'reopen')]
    canonical = json.dumps(history, sort_keys=True, ensure_ascii=False,
                           separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(canonical).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()


def decode(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            require(k not in out, 'Duplicate JSON key: ' + k)
            out[k] = v
        return out
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
    except (ValueError, UnicodeError) as exc:
        raise StoreError('validation_failed', 'Invalid JSON: ' + str(exc)) from exc


def validate(doc):
    require(isinstance(doc, dict), 'Top level must be an object, not a task array')
    require(doc.get('version') == '1.0', 'Expected version 1.0; migrate explicitly')
    require(isinstance(doc.get('updatedAt'), str), 'updatedAt must be a string')
    require(isinstance(doc.get('tasks'), list), 'tasks must be an array')
    ids = set()
    for task in doc['tasks']:
        require(isinstance(task, dict), 'Each task must be an object')
        tid = task.get('id')
        require(isinstance(tid, str) and re.fullmatch(r'T-\d{6}-\d{3,}', tid), 'Invalid task ID')
        require(tid not in ids, 'Duplicate task ID: ' + tid)
        ids.add(tid)
        require(task.get('status') in ('pending', 'done', 'cancelled'), 'Invalid task status')
        for field, keys in [('comments', ('at', 'from', 'content')),
                            ('history', ('at', 'action', 'by', 'detail'))]:
            require(isinstance(task.get(field), list), field + ' must be an array')
            for item in task[field]:
                require(isinstance(item, dict) and all(k in item for k in keys),
                        'Invalid ' + field + ' entry')
                require(all(isinstance(item[k], str) for k in keys if k != 'detail'),
                        'Invalid ' + field + ' entry types')
                if field == 'comments' and 'meaningfulProgress' in item:
                    require(type(item['meaningfulProgress']) is bool,
                            'Invalid meaningfulProgress')
        if 'reminderCount' in task:
            require(type(task['reminderCount']) is int and task['reminderCount'] >= 0,
                    'Invalid reminderCount')
    receipts = doc.get('_reminderReceipts', {})
    require(isinstance(receipts, dict), 'Invalid reminder receipts')
    for tid, slots in receipts.items():
        require(isinstance(tid, str) and isinstance(slots, list) and
                all(isinstance(s, str) for s in slots), 'Invalid reminder receipts')
    events = doc.get('_reminderSyncEvents', [])
    require(isinstance(events, list), 'Invalid reminder sync events')
    seen_events = set()
    for event in events:
        require(isinstance(event, dict), 'Invalid reminder sync event')
        event_id = event.get('id')
        require(isinstance(event_id, str) and event_id and event_id not in seen_events,
                'Invalid or duplicate reminder sync event')
        seen_events.add(event_id)
        require(isinstance(event.get('taskId'), str) and event['taskId'], 'Invalid reminder sync task ID')
        require(event.get('action') in ('create', 'update', 'status', 'reopen', 'comment'),
                'Invalid reminder sync action')
        require(isinstance(event.get('changedFields'), list) and
                all(isinstance(field, str) for field in event['changedFields']),
                'Invalid reminder sync changed fields')
        require(isinstance(event.get('at'), str), 'Invalid reminder sync timestamp')
        lease = event.get('lease')
        if lease is not None:
            require(isinstance(lease, dict) and isinstance(lease.get('owner'), str) and lease['owner'] and
                    isinstance(lease.get('until'), str), 'Invalid reminder sync lease')
    return doc


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write(path, raw):
    """Never truncate the destination. Temp is retained on failure for diagnosis."""
    fd, temp = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.tmp', dir=path.parent)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    require(Path(temp).read_bytes() == raw, 'Temporary file verification failed')
    decode(Path(temp).read_bytes())
    os.replace(temp, path)
    sync_dir(path.parent)


class TaskStore:
    def __init__(self, directory, timeout=30):
        self.root = Path(directory).resolve()
        self.timeout = timeout
        self.journal = self.root / '.task-store-transaction.json'
        self.backups = self.root / 'backups'

    @contextmanager
    def locked(self):
        require(self.root.is_dir(), 'Data directory missing; create it explicitly')
        # This inode is permanent: never unlink the lock file, even after a crash.
        with (self.root / '.task-store.lock').open('a+b') as lock:
            deadline = time.monotonic() + self.timeout
            while True:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise StoreError('lock_timeout', 'Lock timed out; do not delete the lock file')
                    time.sleep(min(.05, max(0, deadline - time.monotonic())))
            try:
                yield
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def filename(self, name):
        require(isinstance(name, str) and (name == MAIN or ARCHIVE.fullmatch(name)),
                'Invalid ledger filename')
        path = self.root / name
        require(not path.is_symlink(), 'Ledger symlinks are not supported')
        return path

    def raw(self, name):
        path = self.filename(name)
        return path.read_bytes() if path.exists() else None

    def load_all(self):
        require(self.raw(MAIN) is not None, 'Main ledger missing; use init or explicit restore',
                'recovery_required')
        docs = {}
        for name in [MAIN] + sorted(p.name for p in self.root.glob('team-tasks-archive-*.json')):
            docs[name] = validate(decode(self.raw(name)))
        self.unique(docs)
        return docs

    def inspect(self):
        """Read a stable snapshot without creating locks or recovering transactions."""
        require(self.root.is_dir(), 'Data directory missing', 'inspect_unavailable')
        self.check_owned(self.root.stat(), directory=True)
        path = self.root / '.task-store.lock'
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        except OSError as exc:
            raise StoreError('inspect_unavailable', 'Existing safe store lock unavailable') from exc
        with os.fdopen(fd, 'rb') as lock:
            self.check_owned(os.fstat(fd))
            def check_lock():
                current, held = path.lstat(), os.fstat(fd)
                require((current.st_dev, current.st_ino) == (held.st_dev, held.st_ino),
                        'Store lock changed during inspection', 'conflict')
            deadline = time.monotonic() + max(0, min(self.timeout, 1))
            while True:
                try:
                    fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise StoreError('lock_timeout', 'Local status is busy; no native query was started')
                    time.sleep(min(.05, max(0, deadline - time.monotonic())))
            try:
                check_lock()
                require(not self.journal.exists() and not self.journal.is_symlink() and
                        not any(self.root.glob('team-tasks*.json.bak')),
                        'Pending recovery; inspection leaves all files unchanged', 'recovery_required')
                docs = self.load_all()
                check_lock()
                return {'ok': True, 'code': 'ok', 'recoveredTransaction': False, 'ledgers': docs}
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    @staticmethod
    def unique(docs):
        seen = set()
        for doc in docs.values():
            validate(doc)
            for task in doc['tasks']:
                require(task['id'] not in seen, 'ID appears in multiple ledgers: ' + task['id'])
                seen.add(task['id'])

    def legacy(self):
        for bak in sorted(self.root.glob('team-tasks*.json.bak')):
            name = bak.name[:-4]
            raw = self.raw(name)
            try:
                require(raw is not None, 'Missing main copy')
                current = validate(decode(raw))
                previous = validate(decode(bak.read_bytes()))
                require(current == previous, 'Different legacy backup')
            except StoreError as exc:
                raise StoreError('recovery_required',
                                 f'Preserved {bak.name}; inspect both copies and use explicit restore: {exc}')
            bak.unlink()
            sync_dir(self.root)

    def recover(self):
        if not self.journal.exists():
            return False
        try:
            txn = decode(self.journal.read_bytes())
            require(isinstance(txn, dict) and txn.get('format') == 1 and
                    isinstance(txn.get('files'), list) and txn['files'], 'Invalid transaction')
            names = set()
            pending = []
            # Validate EVERY participant before replacing any file.
            for entry in txn['files']:
                name = entry['name']
                require(name not in names, 'Duplicate transaction participant')
                names.add(name)
                path = self.filename(name)
                after = encode(validate(entry['after']))
                require(digest(after) == entry['afterHash'], 'Transaction checksum mismatch')
                actual = digest(self.raw(name))
                require(actual in (entry['beforeHash'], entry['afterHash']),
                        'File diverged from transaction: ' + name)
                if actual != entry['afterHash']:
                    pending.append((path, after))
            for path, after in pending:
                atomic_write(path, after)
            self.journal.unlink()
            sync_dir(self.root)
            return True
        except (StoreError, KeyError, TypeError) as exc:
            raise StoreError('recovery_required', 'Transaction retained; manual inspection required: ' + str(exc))

    @staticmethod
    def check_entry(parent, name, fd):
        current = os.stat(name, dir_fd=parent, follow_symlinks=False)
        held = os.fstat(fd)
        require((current.st_dev, current.st_ino) == (held.st_dev, held.st_ino),
                'Backup entry changed during operation', 'conflict')

    @staticmethod
    def check_owned(info, directory=False):
        require((stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode))
                and info.st_uid == os.geteuid() and not info.st_mode & 0o022
                and (directory or info.st_nlink == 1),
                'Backup entry must be owned by the runtime user, not writable by others, '
                'and a real directory or regular file without hard links')

    @contextmanager
    def backup_directory(self, create=False):
        # Walk the canonical root without following any replaceable component.
        with ExitStack() as stack:
            fd = os.open(self.root.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            stack.callback(os.close, fd)
            entries = []
            for name in self.root.parts[1:]:
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=fd)
                stack.callback(os.close, child)
                entries.append((fd, name, child))
                fd = child
            self.check_owned(os.fstat(fd), directory=True)
            def check():
                for entry in entries:
                    self.check_entry(*entry)
            check()
            if create:
                try:
                    os.mkdir('backups', mode=0o700, dir_fd=fd)
                except FileExistsError:
                    pass
                os.fsync(fd)
            child = os.open('backups', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=fd)
            stack.callback(os.close, child)
            entries.append((fd, 'backups', child))
            self.check_owned(os.fstat(child), directory=True)
            check()
            # Owner-only backups; tighten older owner-controlled 0755 directories.
            if create and stat.S_IMODE(os.fstat(child).st_mode) != 0o700:
                os.fchmod(child, 0o700)
                os.fsync(child)
            yield child, check

    def backup(self, originals):
        for name in originals:
            require(isinstance(name, str) and (name == MAIN or ARCHIVE.fullmatch(name)),
                    'Invalid backup ledger filename')
        with self.backup_directory(create=True) as (backups, check):
            name = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ-') + uuid.uuid4().hex
            check()
            os.mkdir(name, mode=0o700, dir_fd=backups)
            os.fsync(backups)
            folder = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                             dir_fd=backups)
            try:
                self.check_owned(os.fstat(folder), directory=True)
                for ledger, raw in originals.items():
                    if raw is None:
                        continue
                    check()
                    self.check_entry(backups, name, folder)
                    fd = os.open(ledger, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o600, dir_fd=folder)
                    with os.fdopen(fd, 'w+b') as stream:
                        self.check_owned(os.fstat(stream.fileno()))
                        self.check_entry(folder, ledger, stream.fileno())
                        stream.write(raw)
                        stream.flush()
                        os.fsync(stream.fileno())
                        stream.seek(0)
                        require(stream.read() == raw, 'Backup verification failed')
                        self.check_entry(folder, ledger, stream.fileno())
                os.fsync(folder)
                check()
                self.check_entry(backups, name, folder)
            finally:
                os.close(folder)
        return self.backups / name

    def prune(self):
        with self.backup_directory() as (backups, check):
            folders = sorted((n for n in os.listdir(backups) if SNAPSHOT.fullmatch(n)),
                             reverse=True)
            cutoff = time.time() - 30 * 86400
            for index, name in enumerate(folders):
                check()
                folder = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                 dir_fd=backups)
                try:
                    info = os.fstat(folder)
                    self.check_owned(info, directory=True)
                    self.check_entry(backups, name, folder)
                    if index < 100 or info.st_mtime >= cutoff:
                        continue
                    children = os.listdir(folder)
                    if any(not (n == MAIN or ARCHIVE.fullmatch(n)) for n in children):
                        continue
                    # Validate all children before deleting any from this snapshot.
                    with ExitStack() as stack:
                        files = []
                        for child in children:
                            fd = os.open(child, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                         dir_fd=folder)
                            stack.callback(os.close, fd)
                            self.check_owned(os.fstat(fd))
                            self.check_entry(folder, child, fd)
                            files.append((child, fd))
                        for child, fd in files:
                            check()
                            self.check_entry(backups, name, folder)
                            self.check_entry(folder, child, fd)
                            os.unlink(child, dir_fd=folder)
                    os.fsync(folder)
                    check()
                    self.check_entry(backups, name, folder)
                    os.rmdir(name, dir_fd=backups)
                    os.fsync(backups)
                finally:
                    os.close(folder)
            os.fsync(backups)

    def commit(self, changes, originals=None):
        for doc in changes.values():
            validate(doc)
        originals = originals if originals is not None else {n: self.raw(n) for n in changes}
        folder = self.backup(originals)
        txn = {'format': 1, 'id': folder.name, 'files': [
            {'name': n, 'beforeHash': digest(originals[n]), 'afterHash': digest(encode(d)), 'after': d}
            for n, d in changes.items()]}
        # Journal durability precedes every ledger replacement (including single-file writes).
        atomic_write(self.journal, encode(txn))
        self.recover()
        warnings = []
        try:
            self.prune()
        except (OSError, StoreError) as exc:
            warnings.append('Committed, but backup cleanup failed: ' + str(exc))
        return {'backup': str(folder), 'warnings': warnings}

    def read_restore_backup(self, source, target):
        require(isinstance(source, str) and source and '\x00' not in source,
                'Backup path required')
        path = Path(source)
        require('..' not in path.parts, 'Backup traversal is not supported')
        if path.is_absolute():
            try:
                path = path.relative_to(self.root)
            except ValueError:
                raise StoreError('validation_failed', 'Backup must be inside this store')
        require(len(path.parts) == 3 and path.parts[0] == 'backups' and
                SNAPSHOT.fullmatch(path.parts[1]) and path.parts[2] == target,
                'Expected backups/<snapshot-id>/<target-ledger>')
        # Anchor every open to a held directory, never resolving caller symlinks.
        fds, entries = [], []
        try:
            parent = os.open(self.root.anchor, os.O_RDONLY | os.O_DIRECTORY)
            fds.append(parent)
            parts = self.root.parts[1:] + path.parts
            for index, part in enumerate(parts):
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                if index < len(parts) - 1:
                    flags |= os.O_DIRECTORY
                fd = os.open(part, flags, dir_fd=parent)
                fds.append(fd)
                entries.append((parent, part, fd))
                if index >= len(self.root.parts) - 2:
                    self.check_owned(os.fstat(fd), directory=index < len(parts) - 1)
                parent = fd
            before = os.fstat(parent)

            def check_entries():
                for directory, name, opened in entries:
                    current = os.stat(name, dir_fd=directory, follow_symlinks=False)
                    held = os.fstat(opened)
                    require((current.st_dev, current.st_ino) == (held.st_dev, held.st_ino),
                            'Backup path changed during restore', 'conflict')

            check_entries()
            with os.fdopen(os.dup(parent), 'rb') as stream:
                raw = stream.read()
            check_entries()
            after = os.fstat(parent)
            require((before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
                    (after.st_size, after.st_mtime_ns, after.st_ctime_ns),
                    'Backup changed during restore', 'conflict')
            return raw
        except OSError as exc:
            raise StoreError('validation_failed', 'Backup path is unavailable or unsafe') from exc
        finally:
            for fd in reversed(fds):
                os.close(fd)

    def restore(self, request):
        name = request.get('target', MAIN)
        old = self.raw(name)
        require('expectedHash' in request and request['expectedHash'] == digest(old),
                'Restore target changed; inspect and provide current SHA-256 (null if missing)', 'conflict')
        doc = validate(decode(self.read_restore_backup(request.get('backup'), name)))
        docs = {}
        for path in self.root.glob('team-tasks*.json'):
            if path.name != name:
                docs[path.name] = validate(decode(self.raw(path.name)))
        docs[name] = doc
        require(MAIN in docs, 'Restore the main ledger first')
        self.unique(docs)
        legacy = self.root / (name + '.bak')
        if legacy.exists():
            # Preserve ambiguous legacy evidence before removing its blocking marker.
            evidence = self.root / ('legacy-evidence-' + uuid.uuid4().hex)
            evidence.mkdir(mode=0o700)
            with (evidence / legacy.name).open('xb') as stream:
                stream.write(legacy.read_bytes())
                stream.flush()
                os.fsync(stream.fileno())
            sync_dir(evidence)
            sync_dir(self.root)
        result = self.commit({name: doc}, {name: old})
        if legacy.exists():
            legacy.unlink()
            sync_dir(self.root)
        return result

    def execute(self, request):
        require(isinstance(request, dict), 'Request must be an operation object')
        op = request.get('op')
        shapes = {
            'init': {'op'}, 'read': {'op'}, 'inspect': {'op'}, 'validate': {'op'},
            'create': {'op', 'actor', 'fields'},
            'update': {'op', 'actor', 'id', 'changes', 'expected'},
            'status': {'op', 'actor', 'id', 'status', 'expected'},
            'complete_external': {'op', 'actor', 'id', 'expected', 'source'},
            'comment': {'op', 'actor', 'id', 'content', 'meaningfulProgress'},
            'remind': {'op', 'id', 'slot'},
            'archive': {'op', 'month'},
            'reopen': {'op', 'actor', 'id', 'expected'},
            'restore': {'op', 'backup', 'target', 'expectedHash'},
            'sync_claim': {'op', 'actor', 'limit', 'leaseSeconds'},
            'sync_ack': {'op', 'actor', 'eventIds'},
        }
        require(isinstance(op, str) and op in shapes, 'Unknown operation')
        require(set(request) <= shapes[op], 'Unexpected request fields; whole-ledger replacement forbidden')
        if op == 'inspect':
            return self.inspect()
        with self.locked():
            recovered = self.recover()
            if op == 'restore':
                result = self.restore(request)
            else:
                self.legacy()
                if op == 'init':
                    require(not any(self.root.glob('team-tasks*.json')), 'Ledger already exists', 'conflict')
                    result = self.commit({MAIN: {'version': '1.0', 'updatedAt': now(), 'tasks': []}})
                else:
                    docs = self.load_all()
                    if op in ('read', 'validate'):
                        result = {'ledgers': docs} if op == 'read' else {'counts': {n: len(d['tasks']) for n, d in docs.items()}}
                    else:
                        before = copy.deepcopy(docs)
                        result = self.mutate(docs, request)
                        if op not in ('sync_claim', 'sync_ack'):
                            self.check_transition(before, docs, op, result.get('id'))
                        changes = {n: d for n, d in docs.items() if d != before.get(n)}
                        if changes:
                            for d in changes.values():
                                d['updatedAt'] = now()
                            result.update(self.commit(changes))
                        else:
                            result['changed'] = False
            return {'ok': True, 'code': 'ok', 'recoveredTransaction': recovered, **result}

    @staticmethod
    def check_transition(before, after, op, tid):
        TaskStore.unique(after)
        old = {t['id']: t for d in before.values() for t in d['tasks']}
        new = {t['id']: t for d in after.values() for t in d['tasks']}
        require(set(new) == (set(old) | {tid} if op == 'create' else set(old)),
                'Unexpected task set change')
        for key, task in old.items():
            if op == 'archive' or key != tid:
                require(new[key] == task, 'Unrelated task modified')
            for field in ('comments', 'history'):
                require(new[key][field][:len(task[field])] == task[field], 'Append-only data changed')

    @staticmethod
    def expected(task, changes, expected):
        require(isinstance(expected, dict) and set(expected) == set(changes),
                'expected must contain exactly the fields being changed')
        for k, value in expected.items():
            require(task.get(k) == value, 'Stale value for ' + k, 'conflict')

    @staticmethod
    def fields(fields, allowed):
        require(isinstance(fields, dict) and fields and set(fields) <= allowed, 'Unsupported or empty fields')
        for k, value in fields.items():
            if k == 'isBlocking':
                require(type(value) is bool, 'isBlocking must be boolean')
            elif k == 'tags':
                require(isinstance(value, list) and all(isinstance(x, str) for x in value), 'Invalid tags')
            elif k == 'priority':
                require(value in ('critical', 'high', 'medium', 'low'), 'Invalid priority')
            else:
                require(value is None or isinstance(value, str), 'Invalid field type: ' + k)
            if k == 'title':
                require(isinstance(value, str) and value.strip(), 'Title required')

    @staticmethod
    def external_source(source):
        require(isinstance(source, dict) and set(source) ==
                {'kind', 'namespace', 'reminderId', 'completionDate', 'receiptId'},
                'Invalid external completion source fields')
        require(source['kind'] == 'macos-reminders', 'Unsupported external completion source')
        for key in ('namespace', 'receiptId'):
            require(isinstance(source[key], str) and
                    re.fullmatch(r'[0-9a-f]{64}', source[key]),
                    'Invalid external completion ' + key)
        require(isinstance(source['reminderId'], str) and source['reminderId'].strip() and
                '\x00' not in source['reminderId'], 'External reminder ID required')
        value = source['completionDate']
        require(isinstance(value, str), 'External completion date required')
        try:
            parsed = dt.datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
            require(parsed.tzinfo is not None and parsed.utcoffset() is not None,
                    'External completion date must include a timezone')
        except (TypeError, ValueError):
            raise StoreError('validation_failed', 'Invalid external completion date')
        return source

    def complete_external(self, docs, task, name, r, stamp):
        source = self.external_source(r.get('source'))
        expected = r.get('expected')
        require(isinstance(expected, dict) and set(expected) == {'status', 'historyFingerprint'} and
                expected['status'] == 'pending' and
                isinstance(expected['historyFingerprint'], str) and
                re.fullmatch(r'[0-9a-f]{64}', expected['historyFingerprint']),
                'External completion requires pending status and history fingerprint')
        # Receipt history travels with the task during archive/reopen and is append-only.
        # Check it before the current status/CAS so retrying a committed write is safe.
        for entry in task['history']:
            detail = entry.get('detail')
            receipt = detail.get('externalCompletion') if isinstance(detail, dict) else None
            if isinstance(receipt, dict) and receipt.get('receiptId') == source['receiptId']:
                require(receipt == source, 'External completion receipt source changed', 'conflict')
                return {'id': task['id'], 'duplicate': True, 'changed': False}
        require(name == MAIN and task['status'] == 'pending',
                'External completion requires an active pending task', 'conflict')
        require(status_history_fingerprint(task) == expected['historyFingerprint'],
                'Task status history changed before external completion', 'conflict')
        content = ('由 macOS 提醒事项同步完成，原生完成时间：' + source['completionDate'] +
                   '；提醒事项 ID：' + source['reminderId'])
        task.update(status='done', completedAt=stamp, cancelledAt=None)
        task['comments'].append({'at': stamp, 'from': r['actor'], 'content': content})
        task['history'].extend([
            {'at': stamp, 'action': 'status', 'by': r['actor'],
             'detail': {'status': 'done', 'externalCompletion': copy.deepcopy(source)}},
            {'at': stamp, 'action': 'comment', 'by': r['actor'], 'detail': {'content': content}},
        ])
        events = docs[MAIN].setdefault('_reminderSyncEvents', [])
        for action, fields in [('status', ['status']), ('comment', ['comments'])]:
            events.append({'id': uuid.uuid4().hex, 'taskId': task['id'], 'action': action,
                           'changedFields': fields, 'at': stamp})
        return {'id': task['id'], 'duplicate': False, 'changed': True}

    def mutate(self, docs, r):
        op = r['op']
        stamp = now()
        if op == 'sync_claim':
            require(isinstance(r.get('actor'), str) and r['actor'].strip(), 'actor required')
            limit = r.get('limit', 20)
            lease_seconds = r.get('leaseSeconds', 300)
            require(type(limit) is int and 1 <= limit <= 100, 'limit must be 1..100')
            require(type(lease_seconds) is int and 1 <= lease_seconds <= 3600,
                    'leaseSeconds must be 1..3600')
            current = dt.datetime.fromisoformat(stamp)
            events = docs[MAIN].setdefault('_reminderSyncEvents', [])
            claimed = []
            for event in events:
                lease = event.get('lease')
                expired = lease is None
                if lease is not None:
                    try:
                        expired = dt.datetime.fromisoformat(lease['until']) <= current
                    except (TypeError, ValueError):
                        raise StoreError('validation_failed', 'Invalid reminder sync lease timestamp')
                if expired and len(claimed) < limit:
                    event['lease'] = {'owner': r['actor'],
                                      'until': (current + dt.timedelta(seconds=lease_seconds)).isoformat()}
                    claimed.append(copy.deepcopy(event))
            return {'events': claimed}
        if op == 'sync_ack':
            require(isinstance(r.get('actor'), str) and r['actor'].strip(), 'actor required')
            event_ids = r.get('eventIds')
            require(isinstance(event_ids, list) and event_ids and
                    all(isinstance(event_id, str) and event_id for event_id in event_ids) and
                    len(set(event_ids)) == len(event_ids), 'eventIds must be a unique non-empty string list')
            events = docs[MAIN].setdefault('_reminderSyncEvents', [])
            wanted = set(event_ids)
            acknowledged = [event['id'] for event in events if event['id'] in wanted and
                            event.get('lease', {}).get('owner') == r['actor']]
            docs[MAIN]['_reminderSyncEvents'] = [event for event in events if event['id'] not in acknowledged]
            return {'acknowledged': acknowledged}
        if op == 'archive':
            month = r.get('month')
            require(isinstance(month, str) and re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', month), 'Invalid month')
            require(month < stamp[:7], 'Archive month must be before current month')
            moved = []
            for task in docs[MAIN]['tasks']:
                if task['status'] not in ('done', 'cancelled'):
                    continue
                completed = task.get('completedAt' if task['status'] == 'done' else 'cancelledAt')
                try:
                    parsed = dt.datetime.fromisoformat(completed)
                except (TypeError, ValueError):
                    raise StoreError('validation_failed', 'Invalid status timestamp for ' + task['id'])
                if parsed.strftime('%Y-%m') <= month:
                    moved.append(task)
            if moved:
                name = f'team-tasks-archive-{month}.json'
                docs.setdefault(name, {'version': '1.0', 'updatedAt': stamp, 'tasks': []})['tasks'].extend(moved)
                ids = {t['id'] for t in moved}
                docs[MAIN]['tasks'] = [t for t in docs[MAIN]['tasks'] if t['id'] not in ids]
            return {'moved': [t['id'] for t in moved]}
        if op != 'remind':
            require(isinstance(r.get('actor'), str) and r['actor'].strip(), 'actor required')
        if op == 'create':
            fields = r.get('fields')
            self.fields(fields, CREATE)
            require('title' in fields, 'title required')
            prefix = 'T-' + dt.datetime.now().astimezone().strftime('%y%m%d') + '-'
            seq = max((int(t['id'].split('-')[-1]) for d in docs.values() for t in d['tasks']
                       if t['id'].startswith(prefix)), default=0) + 1
            tid = prefix + f'{seq:03d}'
            task = dict(id=tid, title='', description='', priority='medium', isBlocking=False,
                        tags=[], status='pending', assignee=None, assigneeId=None, creator=r['actor'],
                        creatorId=None, createdAt=stamp, dueDate=None, dueTime=None, completedAt=None,
                        cancelledAt=None, sourceType='direct', sourceId=None, notifyTargetId=None,
                        lastReminded=None, lastRemindedSlot=None, reminderCount=0, snoozedUntil=None,
                        lastProgressAt=None, comments=[], history=[])
            task.update(fields)
            docs[MAIN]['tasks'].append(task)
        else:
            tid = r.get('id')
            matches = [(name, task) for name, d in docs.items() for task in d['tasks'] if task['id'] == tid]
            require(len(matches) == 1, 'Task not found', 'not_found')
            name, task = matches[0]
            if op == 'complete_external':
                return self.complete_external(docs, task, name, r, stamp)
            require(name == MAIN or op == 'reopen', 'Archived task must be reopened first')
        if op == 'update':
            changes = r.get('changes')
            self.fields(changes, EDITABLE)
            self.expected(task, changes, r.get('expected'))
            task.update(changes)
        elif op in ('status', 'reopen'):
            status = 'pending' if op == 'reopen' else r.get('status')
            require(status in ('pending', 'done', 'cancelled'), 'Invalid status')
            self.expected(task, {'status': status}, r.get('expected'))
            if op == 'reopen' and name != MAIN:
                docs[name]['tasks'].remove(task)
                docs[MAIN]['tasks'].append(task)
            task.update(status=status, completedAt=stamp if status == 'done' else None,
                        cancelledAt=stamp if status == 'cancelled' else None)
        elif op == 'comment':
            require(isinstance(r.get('content'), str) and r['content'].strip(), 'Comment content required')
            meaningful = r.get('meaningfulProgress', False)
            require(type(meaningful) is bool, 'meaningfulProgress must be boolean')
            comment = {'at': stamp, 'from': r['actor'], 'content': r['content']}
            if meaningful:
                comment['meaningfulProgress'] = True
                task['lastProgressAt'] = stamp
            task['comments'].append(comment)
        elif op == 'remind':
            slot = r.get('slot')
            require(isinstance(slot, str) and slot.strip(), 'slot required (include date and timezone)')
            receipts = docs[MAIN].get('_reminderReceipts', {}).get(tid, [])
            if slot in receipts or task.get('lastRemindedSlot') == slot:
                return {'id': tid, 'duplicate': True}
            require(task['status'] == 'pending', 'Cannot remind inactive task', 'conflict')
            receipts = docs[MAIN].setdefault('_reminderReceipts', {}).setdefault(tid, [])
            if task.get('lastRemindedSlot') and task['lastRemindedSlot'] not in receipts:
                receipts.append(task['lastRemindedSlot'])
            receipts.append(slot)
            task.update(lastReminded=stamp, lastRemindedSlot=slot, reminderCount=task.get('reminderCount', 0) + 1)
            return {'id': tid, 'duplicate': False}
        task['history'].append({'at': stamp, 'action': op, 'by': r['actor'],
                                'detail': {k: v for k, v in r.items() if k not in ('actor', 'op', 'id', 'expected')}})
        if op == 'create':
            changed = sorted(r['fields'])
        elif op == 'update':
            changed = sorted(r['changes'])
        elif op in ('status', 'reopen'):
            changed = ['status']
        elif op == 'comment':
            changed = ['comments', 'lastProgressAt'] if r.get('meaningfulProgress') else ['comments']
        else:
            changed = None
        if changed is not None:
            docs[MAIN].setdefault('_reminderSyncEvents', []).append({
                'id': uuid.uuid4().hex,
                'taskId': tid,
                'action': op,
                'changedFields': changed,
                'at': stamp,
            })
        return {'id': tid}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True, help='Existing local data directory')
    parser.add_argument('--request', default='-', help='UTF-8 JSON request file; default stdin')
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read() if args.request == '-' else Path(args.request).read_bytes()
        result = TaskStore(args.data_dir).execute(decode(raw))
    except StoreError as exc:
        result = {'ok': False, 'code': exc.code, 'message': str(exc)}
    except (OSError, KeyError, TypeError, ValueError) as exc:
        result = {'ok': False, 'code': 'io_error' if isinstance(exc, OSError) else 'validation_failed',
                  'message': str(exc),
                  'recoveryAdvice': 'Preserve backups, temporary files and transaction journal. Retry read to recover; do not replay non-idempotent writes until inspected.'}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
