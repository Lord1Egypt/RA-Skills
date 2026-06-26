#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

PERSISTENT_CANDIDATES = [
    Path('/data/disk'),
    Path('/mnt/data'),
    Path('/data'),
    Path('/srv/data'),
    Path('/Volumes/Data'),
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value).strip('-')
    return value or 'change'


def is_writable_dir(path: Path) -> bool:
    return path.exists() and path.is_dir() and os.access(path, os.W_OK)


def resolve_archive_root(explicit: str | None, workspace: Path):
    warnings = []
    if explicit:
        p = Path(explicit).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p, True, warnings, 'explicit'

    env_root = os.environ.get('SYSTEM_CHANGE_ARCHIVE_ROOT')
    if env_root:
        p = Path(env_root).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p, True, warnings, 'env'

    for candidate in PERSISTENT_CANDIDATES:
        if is_writable_dir(candidate):
            return candidate, True, warnings, 'candidate'

    fallback = (workspace / '.system-change-archive-fallback').resolve()
    fallback.mkdir(parents=True, exist_ok=True)
    warnings.append('Using workspace fallback archive root; this is not a persistent hard-guarantee layer.')
    return fallback, False, warnings, 'fallback'


def rel_dest(base: Path, src: Path) -> Path:
    cleaned = str(src).lstrip('/')
    return base / cleaned


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def append_daily_index(index_path: Path, time_label: str, change_name: str, archive_dir: Path, summary: str, status: str):
    index_path.parent.mkdir(parents=True, exist_ok=True)
    line = f'- {time_label} | `{change_name}` | `{archive_dir}` | {summary} | {status}\n'
    if index_path.exists():
        existing = index_path.read_text(encoding='utf-8')
    else:
        existing = '# Daily System Change Index\n\n'
    if line not in existing:
        index_path.write_text(existing + line, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description='Initialize a system change archive scaffold.')
    ap.add_argument('--change-name', required=True)
    ap.add_argument('--summary', required=True)
    ap.add_argument('--archive-root')
    ap.add_argument('--timestamp')
    ap.add_argument('--workspace', default=os.getcwd())
    ap.add_argument('--restart-required', action='store_true')
    ap.add_argument('--context', default='')
    ap.add_argument('--agent', default='')
    ap.add_argument('--operator', default='')
    ap.add_argument('--file', action='append', dest='files', default=[])
    ap.add_argument('--copy-before', action='store_true')
    ap.add_argument('--init-index', action='store_true')
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    ts = datetime.now().astimezone() if not args.timestamp else datetime.fromisoformat(args.timestamp)
    date_part = ts.strftime('%Y-%m-%d')
    time_part = ts.strftime('%H%M')
    slug = slugify(args.change_name)

    archive_root, persistent, warnings, source = resolve_archive_root(args.archive_root, workspace)
    change_dir = archive_root / 'backups' / 'system-changes' / date_part / f'{time_part}-{slug}'

    pre = change_dir / 'PRE-RESTART'
    post = change_dir / 'POST-RESTART'
    for d in [pre / 'backup', pre / 'after', pre / 'diff', post / 'logs']:
        d.mkdir(parents=True, exist_ok=True)

    readme = f'''# {args.change_name}\n\n## Summary\n{args.summary}\n\n## Why this matters\n- Document the intended system-level change before restart/reload.\n\n## Restart/Reload Expected\n- {'Yes' if args.restart_required else 'Not specified'}\n\n## Risks\n- Restart/reload may fail or produce degraded behavior.\n\n## Rollback Summary\n- Restore files from PRE-RESTART/backup and re-apply previous known-good state.\n'''

    meta = {
        'timestamp': ts.isoformat(),
        'timezone': str(ts.tzinfo),
        'change_name': args.change_name,
        'summary': args.summary,
        'archive_root': str(archive_root),
        'persistent_storage': persistent,
        'archive_root_source': source,
        'archive_dir': str(change_dir),
        'restart_required': args.restart_required,
        'context': args.context,
        'agent': args.agent,
        'operator': args.operator,
        'files': args.files,
        'warnings': warnings,
    }

    plan = f'''# Execution Plan\n\n## Target files\n'''
    if args.files:
        plan += ''.join(f'- `{f}`\n' for f in args.files)
    else:
        plan += '- (add target files)\n'
    plan += '''\n## Intended edits\n- Fill in exact before/after changes.\n\n## Restart/Reload Command\n- Fill in command(s) if applicable.\n\n## Verification Points\n- Fill in expected checks after change.\n\n## Rollback Steps\n- Restore backups from PRE-RESTART/backup/.\n'''

    restart_result = '# Restart Result\n\n- Fill in what happened during restart/reload.\n'
    verify = '# Verification\n\n- Fill in post-restart checks and outcomes.\n'

    write_text(pre / 'README.md', readme)
    write_text(pre / 'meta.json', json.dumps(meta, indent=2, ensure_ascii=False) + '\n')
    write_text(pre / 'plan.md', plan)
    write_text(post / 'restart-result.md', restart_result)
    write_text(post / 'verify.md', verify)

    copied = []
    missing = []
    if args.copy_before:
        for f in args.files:
            src = Path(f).expanduser()
            if src.exists() and src.is_file():
                dest = rel_dest(pre / 'backup', src.resolve())
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
                copied.append({'src': str(src.resolve()), 'dest': str(dest)})
            else:
                missing.append(str(src))

    if args.init_index:
        index_path = archive_root / 'backups' / 'system-changes' / date_part / 'index.md'
        append_daily_index(index_path, time_part, slug, change_dir, args.summary, 'initialized')

    result = {
        'archive_root': str(archive_root),
        'persistent_storage': persistent,
        'archive_root_source': source,
        'archive_dir': str(change_dir),
        'warnings': warnings,
        'copied_before_files': copied,
        'missing_before_files': missing,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
