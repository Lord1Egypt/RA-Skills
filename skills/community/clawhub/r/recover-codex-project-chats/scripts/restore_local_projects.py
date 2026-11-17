#!/usr/bin/env python3
"""Restore local project metadata across signed-in identities. Never copy auth or cloud state."""
from __future__ import annotations

import argparse
import copy
from contextlib import closing, contextmanager, ExitStack
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
import uuid

STATE = '.codex-global-state.json'
ACCOUNT = 'electron-account-renderer-state-v1'
MAP = 'app-server-project-id-by-legacy-project-id-by-host'
MIGRATION = 'app-server-projects-migration-by-host'
SECTIONS = 'sidebar-custom-sections-v3'


class RecoveryError(Exception):
    pass


def atomic_write(path, data):
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def db_snapshot(path):
    source = sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)
    target = sqlite3.connect(':memory:')
    try:
        source.backup(target)
        if target.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise RecoveryError('数据库完整性检查未通过，已停止。')
    except BaseException:
        target.close()
        raise
    finally:
        source.close()
    return target


def stopped_guard():
    try:
        result = subprocess.run(['/bin/ps', '-axo', 'pid=,comm='],
                                text=True, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RecoveryError('无法确认应用已退出，未写入。请在系统终端中运行此工具。') from exc
    found = []
    for line in result.stdout.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) != 2:
            continue
        pid, command = parts
        if (('/ChatGPT.app/Contents/' in command or
             '/Codex.app/Contents/' in command or
             Path(command).name.lower() in ('chatgpt', 'codex', 'codex.exe')) and
                int(pid) != os.getpid()):
            found.append(pid)
    if found:
        raise RecoveryError('ChatGPT/Codex 或后台进程仍在运行。请用 ⌘Q 完全退出，再双击恢复入口。')


def acquire_recovery_lock(root):
    """A shared directory lock used by both account and legacy repairs."""
    digest = hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:32]
    path = Path.home() / '.local/state/recover-codex-project-chats/locks' / (digest + '.lock')
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise RecoveryError('另一恢复任务正在运行，或异常终止后留下运行锁。确认没有恢复任务后，用 rmdir 删除此空目录再重试：' + str(path)) from exc
    return path


@contextmanager
def recovery_lock(root):
    path = acquire_recovery_lock(root)
    try:
        yield path
    finally:
        path.rmdir()


def local_project(project):
    # Deliberately omit cloud backing/ownership, permissions, and arbitrary metadata.
    required = ('id', 'name', 'rootPaths', 'createdAt', 'updatedAt')
    if not isinstance(project, dict) or any(k not in project for k in required):
        raise RecoveryError('项目配置格式与此工具不兼容，未写入。')
    if not isinstance(project['id'], str) or not isinstance(project['name'], str):
        raise RecoveryError('项目名称或编号格式不正确。')
    roots = project['rootPaths']
    if not isinstance(roots, list) or not roots or not all(isinstance(x, str) and Path(x).is_absolute() for x in roots):
        raise RecoveryError('项目目录格式不正确。')
    return {k: copy.deepcopy(project[k]) for k in required}


def restore_sidebar(data, current, projects, rows, database):
    """Merge only local sidebar memberships; never copy a whole account's atoms."""
    source_sections = []
    for snapshot in data[ACCOUNT].get('inactive', {}).values():
        for account in snapshot.get('atoms', {}).get(SECTIONS, {}).values():
            source_sections.extend(account.get('sections', []))
    stats = {'sidebar_sections_added': 0, 'sidebar_items_added': 0, 'sidebar_items_skipped': 0}
    if not source_sections:
        return stats
    atoms = current.setdefault('electron-persisted-atom-state', {})
    account_ids = set(atoms.get(SECTIONS, {}))
    if not account_ids:
        account_ids = set(atoms.get('chatgpt-sidebar-state-v2', {}))
    if len(account_ids) != 1:
        raise RecoveryError('无法唯一确认当前账号的空间配置。请在应用中加载侧栏后重试，未写入。')
    account_id = next(iter(account_ids))
    payload = atoms.setdefault(SECTIONS, {}).setdefault(account_id, {'sections': []})
    destinations = payload.setdefault('sections', [])
    # Validate section identity against this machine's local database.
    section_rows = dict(database.execute('SELECT id,name FROM thread_sections'))
    placed = {key for s in destinations for key in s.get('itemKeys', [])}
    placed.update(atoms.get('unified-sidebar-pinned-order-v1', []))
    skipped = set()
    for old in source_sections:
        local_id = old.get('hostSectionIds', {}).get('local')
        name = old.get('name')
        if not local_id or section_rows.get(local_id) != name:
            for key in old.get('itemKeys', []):
                valid = (key.startswith('codex:project:') and key.removeprefix('codex:project:') in projects)
                if key.startswith('codex:thread:local:'):
                    tid = key.removeprefix('codex:thread:local:')
                    valid = tid in rows and rows[tid][2] == 0
                if valid and key not in placed:
                    raise RecoveryError('旧空间的本机编号不存在或名称不一致，仍有本地条目未恢复。请核对空间配置，未写入。')
                skipped.add(key)
            continue
        matches = [s for s in destinations if s.get('hostSectionIds', {}).get('local') == local_id]
        if not matches:
            matches = [s for s in destinations if s.get('name') == name and not s.get('hostSectionIds', {}).get('local')]
        if len(matches) > 1:
            raise RecoveryError('当前账号存在重复的空间，需人工核对，未写入。')
        eligible = []
        for key in old.get('itemKeys', []):
            if key.startswith('codex:project:'):
                valid = key.removeprefix('codex:project:') in projects
            elif key.startswith('codex:thread:local:'):
                tid = key.removeprefix('codex:thread:local:')
                valid = tid in rows and rows[tid][2] == 0
            else:
                valid = False
            if not valid:
                skipped.add(key)
            elif key not in placed:
                eligible.append(key)
                placed.add(key)
        if not eligible:
            continue
        if matches:
            destination = matches[0]
        else:
            destination = {'id': str(uuid.uuid4()), 'name': name,
                           'hostSectionIds': {'local': local_id}, 'itemKeys': [], 'appearance': None}
            destinations.append(destination)
            stats['sidebar_sections_added'] += 1
        destination.setdefault('itemKeys', []).extend(eligible)
        stats['sidebar_items_added'] += len(eligible)
    stats['sidebar_items_skipped'] = len(skipped)
    return stats


def make_plan(root, raw, database):
    data = json.loads(raw)
    scoped = data.get(ACCOUNT)
    if not isinstance(scoped, dict) or not scoped.get('owner'):
        raise RecoveryError('请先登录要使用的 GPT 账号，退出应用后再运行。')
    if not isinstance(scoped.get('inactive', {}), dict):
        raise RecoveryError('账号配置格式不兼容，未写入。')
    current = copy.deepcopy(data)
    projects = copy.deepcopy(data.get('local-projects', {}))
    assignments = copy.deepcopy(data.get('thread-project-assignments', {}))
    order = list(data.get('project-order', []))
    identity = 'local:' + str(root.resolve())
    mappings = copy.deepcopy(data.get(MAP, {}))
    local_map = mappings.setdefault(identity, {})
    source_count = 0
    for _, snapshot in sorted(scoped.get('inactive', {}).items()):
        g = snapshot.get('globals', {})
        old_projects = g.get('local-projects', {})
        if not old_projects:
            continue
        source_count += 1
        for pid, value in old_projects.items():
            clean = local_project(value)
            if clean['id'] != pid:
                raise RecoveryError('项目编号不一致，未写入。')
            if pid in projects and projects[pid]['rootPaths'] != clean['rootPaths']:
                raise RecoveryError('同一项目对应了不同目录，需人工核对，未写入。')
            projects.setdefault(pid, clean)
        for pid in g.get('project-order', []):
            if pid in projects and pid not in order:
                order.append(pid)
        for tid, membership in g.get('thread-project-assignments', {}).items():
            if membership.get('projectKind') != 'local' or membership.get('projectId') not in old_projects:
                continue
            wanted = {'projectKind': 'local', 'projectId': membership['projectId']}
            if tid in assignments:
                # The active account's explicit membership always wins.
                if tid in data.get('thread-project-assignments', {}):
                    continue
                if assignments[tid] != wanted:
                    raise RecoveryError('旧账号之间存在不同的会话归属，需人工核对，未写入。')
            assignments[tid] = wanted
        for pid, sid in g.get(MAP, {}).get(identity, {}).items():
            if pid in old_projects:
                if pid in local_map and local_map[pid] != sid:
                    raise RecoveryError('项目索引映射冲突，未写入。')
                local_map[pid] = sid
    if not projects:
        raise RecoveryError('没有找到可恢复的本地项目。')
    for pid in projects:
        if pid not in order:
            order.append(pid)

    schema = {row[1] for row in database.execute('PRAGMA table_info(threads)')}
    if not {'id', 'project_id', 'rollout_path', 'archived'}.issubset(schema):
        raise RecoveryError('此版本的会话数据库结构不兼容，未写入。')
    server_projects = {row[0] for row in database.execute('SELECT id FROM projects')}
    server_roots = {}
    for pid, path in database.execute('SELECT project_id,path FROM project_roots ORDER BY position'):
        server_roots.setdefault(pid, []).append(path)
    for pid, project in projects.items():
        sid = local_map.get(pid)
        if sid is None and pid in server_projects:
            sid = pid
        if sid is None:
            matches = [k for k, roots in server_roots.items() if roots == project['rootPaths']]
            if len(matches) == 1:
                sid = matches[0]
        if sid not in server_projects or server_roots.get(sid) != project['rootPaths']:
            raise RecoveryError('项目目录与数据库索引不一致，未写入。')
        local_map[pid] = sid
    rows = {row[0]: row[1:] for row in database.execute('SELECT id,project_id,rollout_path,archived FROM threads')}
    updates, checked, missing_bodies, unknown = {}, {}, 0, 0
    for tid, membership in assignments.items():
        if membership.get('projectKind') != 'local' or membership.get('projectId') not in projects:
            continue
        if tid not in rows:
            unknown += 1
            continue
        pid = membership['projectId']
        sid = local_map[pid]
        existing, rollout, archived = rows[tid]
        if existing not in (None, sid):
            raise RecoveryError('会话已有不同的数据库归属，需人工核对，未写入。')
        checked[tid] = sid
        if existing != sid:
            updates[tid] = sid
        if not Path(rollout).is_file():
            missing_bodies += 1
    # Keep stale references out of the active account, while retaining the original stash.
    assignments = {tid: value for tid, value in assignments.items()
                   if tid in rows or tid in data.get('thread-project-assignments', {})}
    current['local-projects'] = projects
    current['project-order'] = order
    current['thread-project-assignments'] = assignments
    current[MAP] = mappings
    assigned = set(checked)
    current['projectless-thread-ids'] = [tid for tid in current.get('projectless-thread-ids', []) if tid not in assigned]
    sidebar_stats = restore_sidebar(data, current, projects, rows, database)
    if (projects != data.get('local-projects', {}) or
            assignments != data.get('thread-project-assignments', {}) or updates):
        migration = current.setdefault(MIGRATION, {}).setdefault(identity, {})
        migration.update(version=1, projectsMigrated=True, threadAssignmentsMigrated=False,
                         threadAssignmentsReadMigrated=False)
        migration['pendingThreadAssignmentIds'] = sorted(set(migration.get('pendingThreadAssignmentIds', [])) | assigned)
    assert current[ACCOUNT] == data[ACCOUNT]
    summary = {
        'source_accounts': source_count,
        'projects_total': len(projects),
        'projects_added': len(set(projects) - set(data.get('local-projects', {}))),
        'associations_total': len(checked),
        'associations_added': len(set(assignments) - set(data.get('thread-project-assignments', {}))),
        'database_updates': len(updates),
        'missing_body_files': missing_bodies,
        'unmatched_associations_skipped': unknown,
        'project_names': [projects[pid]['name'] for pid in order if pid in projects],
        **sidebar_stats,
    }
    return current, updates, checked, summary


def clone_or_copy(source, target):
    if sys.platform == 'darwin':
        lib = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True)
        fn = lib.clonefile
        fn.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        fn.restype = ctypes.c_int
        if fn(os.fsencode(source), os.fsencode(target), 0) == 0:
            return str(target)
    return shutil.copy2(source, target)


def copy_tree(source, target):
    def sockets_only(directory, names):
        return [n for n in names if stat.S_ISSOCK(os.lstat(Path(directory) / n).st_mode)]
    shutil.copytree(source, target, symlinks=True, copy_function=clone_or_copy, ignore=sockets_only)


def encode(data):
    return (json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n').encode()


def support_directories():
    base = Path.home() / 'Library/Application Support'
    return [base / name for name in ('Codex', 'ChatGPT', 'com.openai.codex', 'com.openai.chat')
            if (base / name).is_dir()]


def validate_output(path, root):
    """Reports/backups must not overwrite or recurse into the recovery sources."""
    resolved = path.resolve()
    protected = [root.resolve(), *(p.resolve() for p in support_directories()), Path(__file__).parent.parent.resolve()]
    if any(resolved == p or resolved.is_relative_to(p) for p in protected):
        raise RecoveryError('报告和备份必须放在应用数据及 Skill 目录之外。')


def create_backup(root, backup_root):
    """Back up the full stopped recovery set, excluding only Unix sockets."""
    stopped_guard()
    validate_output(backup_root, root)
    stamp = dt.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup = backup_root / ('local-projects-' + stamp)
    backup.mkdir(parents=True, mode=0o700)
    sources = [root, *support_directories()]
    try:
        for i, path in enumerate(sources):
            if backup.resolve().is_relative_to(path.resolve()):
                raise RecoveryError('备份目录不能放在被备份的目录内。')
            print(f'备份 {i + 1}/{len(sources)}：{path.name}', flush=True)
            copy_tree(path, backup / ('codex-home' if i == 0 else 'ApplicationSupport-' + path.name))
        stopped_guard()
        # Check only copies. No direct integrity checks or writes against a running app.
        for filename in ('state_5.sqlite', 'sqlite/codex-dev.db'):
            saved = backup / 'codex-home' / filename
            if saved.exists():
                db = db_snapshot(saved)
                db.close()
        return backup
    except BaseException:
        print(f'备份未完成，保留目录：{backup}', file=sys.stderr)
        raise


def apply_plan(root, state_bytes, target, updates, checked, summary, backup_root):
    stopped_guard()
    if (root / STATE).read_bytes() != state_bytes:
        raise RecoveryError('配置刚发生变化，请重新运行。')
    backup = create_backup(root, backup_root)
    try:
        if (root / STATE).read_bytes() != state_bytes:
            raise RecoveryError('备份期间配置发生变化，未写入，请完全退出应用后重试。')
        before = {}
        paths = [root / 'state_5.sqlite']
        cache_path = root / 'sqlite/codex-dev.db'
        if cache_path.exists():
            paths.append(cache_path)
        try:
            for path in paths:
                before[path] = db_snapshot(path)
        except BaseException:
            for saved in before.values():
                saved.close()
            raise
        target_bytes = encode(target)
        mutation_started = False
        try:
            for path in paths:
                stopped_guard()
                with closing(sqlite3.connect(path)) as conn, conn:
                    mutation_started = True
                    if path.name == 'state_5.sqlite':
                        conn.executemany('UPDATE threads SET project_id=? WHERE id=? AND project_id IS NULL',
                                         [(sid, tid) for tid, sid in updates.items()])
                        actual = dict(conn.execute('SELECT id,project_id FROM threads'))
                        if any(actual.get(tid) != sid for tid, sid in checked.items()):
                            raise RecoveryError('数据库关联回读不一致。')
                    else:
                        columns = {r[1] for r in conn.execute('PRAGMA table_info(local_thread_catalog)')}
                        if {'project_id', 'thread_id', 'host_id'}.issubset(columns):
                            conn.executemany("UPDATE local_thread_catalog SET project_id=? WHERE host_id='local' AND thread_id=?",
                                             [(sid, tid) for tid, sid in checked.items()])
                            tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                            if 'local_thread_catalog_metadata' in tables:
                                conn.execute('UPDATE local_thread_catalog_metadata SET catalog_revision=catalog_revision+1 WHERE id=1')
            stopped_guard()
            atomic_write(root / STATE, target_bytes)
            if json.loads((root / STATE).read_bytes()) != target:
                raise RecoveryError('配置回读不一致。')
            for path in paths:
                check = db_snapshot(path)
                check.close()
        except BaseException as original:
            if mutation_started:
                try:
                    stopped_guard()
                except RecoveryError as stopped:
                    raise RecoveryError('写入中断且应用可能已重启，停止自动回滚。请退出应用并使用保留的备份排查。') from stopped
                rollback_errors = []
                for path, saved in before.items():
                    try:
                        with closing(sqlite3.connect(path)) as conn:
                            saved.backup(conn)
                    except (OSError, sqlite3.Error) as exc:
                        rollback_errors.append(str(exc))
                try:
                    atomic_write(root / STATE, state_bytes)
                except OSError as exc:
                    rollback_errors.append(str(exc))
                if rollback_errors:
                    raise RecoveryError('自动回滚未完成，请退出应用并使用保留的备份排查：' + '; '.join(rollback_errors)) from original
            raise
        finally:
            for saved in before.values():
                saved.close()
        report = dict(summary, status='local_metadata_restored', ui_verified=False,
                      backup=str(backup), state_sha256=hashlib.sha256(target_bytes).hexdigest(),
                      database_body_files_modified=0)
        try:
            atomic_write(backup / 'result.json', encode(report))
        except OSError as exc:
            raise RecoveryError('本地恢复已写入，但结果报告保存失败。请保留备份并检查侧栏：' + str(backup)) from exc
        return report
    except BaseException:
        print(f'备份目录：{backup}', file=sys.stderr)
        raise


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='应用已退出后执行恢复；默认仅预览')
    parser.add_argument('--report', type=Path, help='保存不含账号标识的预览报告')
    parser.add_argument('--backup-dir', type=Path, default=Path.home() / 'Documents/Codex/codex-recovery-backups',
                        help='备份的持久目录；必须在应用数据和 Skill 目录外')
    args = parser.parse_args()
    root = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).expanduser().resolve()
    if not (root / STATE).is_file() or not (root / 'state_5.sqlite').is_file():
        raise RecoveryError('未找到本地配置或会话数据库。')
    if args.report:
        validate_output(args.report, root)
    validate_output(args.backup_dir, root)
    with ExitStack() as stack:
        if args.apply:
            stopped_guard()
            stack.enter_context(recovery_lock(root))
        raw = (root / STATE).read_bytes()
        db = db_snapshot(root / 'state_5.sqlite')
        try:
            target, updates, checked, summary = make_plan(root, raw, db)
        finally:
            db.close()
        print(f"项目：{summary['projects_total']} 个（新增 {summary['projects_added']} 个）")
        print(f"会话关联：{summary['associations_total']} 条（新增 {summary['associations_added']} 条）")
        print(f"需要更新数据库关联：{summary['database_updates']} 条")
        print(f"空间归属：补回 {summary['sidebar_items_added']} 项，新增 {summary['sidebar_sections_added']} 个空间")
        print(f"正文文件当前找不到：{summary['missing_body_files']} 条；此工具只恢复关联。")
        if args.report:
            atomic_write(args.report.resolve(), encode(summary))
        if not args.apply:
            print('当前仅预览，未修改应用数据。')
            return 0
        if target == json.loads(raw) and not updates:
            print('当前账号的本地项目、会话关联和空间归属已齐全，无需恢复。')
            return 0
        report = apply_plan(root, raw, target, updates, checked, summary, args.backup_dir)
        print('本地项目、会话关联和空间归属已恢复。请重新打开 ChatGPT/Codex 检查侧栏。')
        print('尚未完成界面验收；归档状态保持原样。')
        print('备份：' + report['backup'])
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RecoveryError, OSError, sqlite3.Error, ValueError, KeyError, TypeError) as error:
        print('未完成恢复：' + str(error), file=sys.stderr)
        sys.exit(1)
