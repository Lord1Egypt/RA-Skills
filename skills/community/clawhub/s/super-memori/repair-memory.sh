#!/usr/bin/env python3
# Exit codes: 0=repair plan or action completed, 2=repair recommended / partial, 3=unsafe or unavailable, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'scripts'))
from super_memori_common import LEARNINGS_DIR, audit_memory_integrity, read_state, semantic_runtime_status

ROOT = Path(__file__).resolve().parent
BACKUP_DIR = ROOT / 'backups'


class RepairArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(4)


def run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def classify_state(audit: dict, semantic: dict) -> dict:
    continue_ok = []
    rebuild = []
    rollback = []
    if audit['vector_state'] == 'semantic-unbuilt':
        continue_ok.append('lexical runtime remains valid; semantic stack not built on this host yet')
    if audit['vector_state'] == 'stale-vectors':
        rebuild.append('run vector rebuild before trusting hybrid quality')
    if audit['orphan_chunks'] or audit['orphan_fts_chunks'] or audit['orphan_vectors']:
        rollback.append('storage drift/orphans detected; inspect backups before further mutation')
    if audit['broken_relations']:
        rebuild.append('migrate or remove broken relation targets in learning files')
    if not semantic['model_ready']:
        continue_ok.append('semantic rebuild cannot run until local deps/model exist')
    return {'continue': continue_ok, 'rebuild': rebuild, 'rollback': rollback}


def backup_file(path: Path) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime('%Y%m%dT%H%M%S')
    target = BACKUP_DIR / f'{path.name}.{stamp}.bak'
    shutil.copy2(path, target)
    return target


def migrate_relations() -> dict:
    changed = []
    backups = []
    for path in sorted(LEARNINGS_DIR.glob('*.md')):
        raw = path.read_text(encoding='utf-8', errors='ignore')
        new = raw
        new = new.replace('- refines: semantic-spine', '- refines: path:/home/irtual/.openclaw/workspace/skills/super_memori/scripts/super_memori_common.py')
        new = new.replace('- extends: retrieval-quality', '- extends: path:/home/irtual/.openclaw/workspace/skills/super_memori/query-memory.sh')
        if new != raw:
            backup = backup_file(path)
            path.write_text(new, encoding='utf-8')
            changed.append(str(path))
            backups.append(str(backup))
    return {'changed_files': changed, 'backups': backups}


def rebuild_safe() -> dict:
    audit = audit_memory_integrity()
    actions = []
    if audit['orphan_chunks'] or audit['orphan_fts_chunks'] or audit['orphan_vectors']:
        return {'status': 'unsafe', 'reason': 'orphan drift detected; inspect manually before rebuild'}
    code, out, err = run(['bash', '-lc', f'cd {ROOT} && ./index-memory.sh --incremental --json'])
    actions.append({'step': 'lexical_incremental', 'exit_code': code, 'stdout': out, 'stderr': err})
    if audit['vector_state'] == 'stale-vectors':
        code, out, err = run(['bash', '-lc', f'cd {ROOT} && ./index-memory.sh --rebuild-vectors --json'])
        actions.append({'step': 'vector_rebuild', 'exit_code': code, 'stdout': out, 'stderr': err})
    return {'status': 'applied', 'actions': actions}


def main() -> int:
    p = RepairArgumentParser(description='Plan or run deterministic super_memori repair actions')
    p.add_argument('--plan', action='store_true')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--classify', action='store_true')
    p.add_argument('--migrate-relations', action='store_true')
    p.add_argument('--rebuild-safe', action='store_true')
    p.add_argument('--json', action='store_true')
    args = p.parse_args()

    if not any([args.plan, args.apply, args.classify, args.migrate_relations, args.rebuild_safe]):
        args.plan = True

    state = read_state()
    semantic = semantic_runtime_status(state)
    audit = audit_memory_integrity()
    decision = classify_state(audit, semantic)
    payload = {
        'status': 'plan',
        'audit': audit,
        'semantic': semantic,
        'decision': decision,
        'actions': [],
        'warnings': [],
    }

    exit_code = 0
    if args.classify:
        payload['status'] = 'classified'
        payload['actions'] = decision
        exit_code = 2 if decision['rebuild'] or decision['rollback'] else 0
    elif args.migrate_relations:
        result = migrate_relations()
        payload['status'] = 'migrated'
        payload['actions'] = [result]
        exit_code = 0 if result['changed_files'] else 2
    elif args.rebuild_safe:
        result = rebuild_safe()
        payload['status'] = result['status']
        payload['actions'] = result.get('actions', [])
        payload['reason'] = result.get('reason')
        exit_code = 0 if result['status'] == 'applied' else 3
    elif args.apply:
        applied = []
        if audit['broken_relations']:
            applied.append({'migrate_relations': migrate_relations()})
        applied.append({'classify': decision})
        safe_result = rebuild_safe()
        applied.append({'rebuild_safe': safe_result})
        payload['status'] = 'applied'
        payload['actions'] = applied
        exit_code = 0 if safe_result.get('status') == 'applied' else 2
    else:
        payload['actions'] = decision
        payload['warnings'] = decision['continue']
        exit_code = 2 if decision['rebuild'] or decision['rollback'] or decision['continue'] else 0

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload)
    return exit_code


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f'repair-memory internal error: {exc}', file=sys.stderr)
        raise SystemExit(5)
