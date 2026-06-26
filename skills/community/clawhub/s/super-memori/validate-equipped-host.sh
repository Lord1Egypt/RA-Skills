#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

STEP1_JSON_FILE=/tmp/super-memori-equipped-step1.json
STEP1_RC=0
if ! ./index-memory.sh --incremental --json > "$STEP1_JSON_FILE"; then
  STEP1_RC=$?
fi
cat "$STEP1_JSON_FILE"
python3 - "$STEP1_JSON_FILE" "$STEP1_RC" <<'PY'
import json, pathlib, sys
path = pathlib.Path(sys.argv[1])
step1_rc = int(sys.argv[2])
payload = json.loads(path.read_text())
if step1_rc == 0:
    raise SystemExit(0)
if step1_rc != 2:
    raise SystemExit(step1_rc)
warns = payload.get('warnings', [])
post_audit = next((item.get('post_audit') for item in payload.get('actions', []) if 'post_audit' in item), {}) or {}
if warns != ['integrity audit reported drift or orphans after maintenance']:
    raise SystemExit('equipped-host validation failed: unexpected step1 warning payload')
if post_audit.get('status') != 'warn' or post_audit.get('vector_state') != 'stale-vectors':
    raise SystemExit('equipped-host validation failed: step1 warning was not the expected transient stale-vectors state')
if post_audit.get('orphan_chunks') or post_audit.get('orphan_fts_chunks') or post_audit.get('orphan_vectors') or post_audit.get('broken_relations'):
    raise SystemExit('equipped-host validation failed: step1 reported real integrity drift, not transient stale-vectors')
if not post_audit.get('missing_vectors'):
    raise SystemExit('equipped-host validation failed: step1 stale-vectors state had no missing_vectors evidence')
print('Step 1 acknowledged expected transient stale-vectors state; continuing to vector rebuild.')
PY

./index-memory.sh --rebuild-vectors --json
./query-memory.sh "agent memory" --mode hybrid --json --limit 3 | tee /tmp/super-memori-equipped-query.json
./validate-release.sh --strict
./scripts/release-prep.sh
./health-check.sh --json | tee /tmp/super-memori-equipped-health.json
python3 audit-memory.sh --json | tee /tmp/super-memori-equipped-audit.json

python3 - <<'PY'
import json, pathlib
query = json.loads(pathlib.Path('/tmp/super-memori-equipped-query.json').read_text())
health = json.loads(pathlib.Path('/tmp/super-memori-equipped-health.json').read_text())
audit = json.loads(pathlib.Path('/tmp/super-memori-equipped-audit.json').read_text())
checks = {item.get('name'): item for item in health.get('checks', [])}
if query.get('mode_used') != 'hybrid':
    raise SystemExit(f"equipped-host validation failed: mode_used={query.get('mode_used')}")
if not query.get('semantic_ready'):
    raise SystemExit('equipped-host validation failed: semantic_ready=false')
if query.get('degraded'):
    raise SystemExit('equipped-host validation failed: degraded=true')
if health.get('status') != 'OK':
    raise SystemExit(f"equipped-host validation failed: health status={health.get('status')}")
semantic_fresh_check = checks.get('semantic_freshness') or {}
if not semantic_fresh_check.get('ok', False):
    raise SystemExit('equipped-host validation failed: semantic_fresh=false after rebuild')
skill_mem = checks.get('skill_operational_memory', {}).get('detail', {})
agent_change = checks.get('agent_change_memory', {}).get('detail', {})
if skill_mem.get('validation_state') != 'current' or not skill_mem.get('fresh', False):
    raise SystemExit(f"equipped-host validation failed: skill_operational_memory not current/fresh ({skill_mem})")
if agent_change.get('status') != 'ok':
    raise SystemExit(f"equipped-host validation failed: agent_change_memory.status={agent_change.get('status')}")
if audit.get('status') != 'ok' or audit.get('vector_state') != 'ok' or not audit.get('semantic_fresh'):
    raise SystemExit(f"equipped-host validation failed: audit status={audit.get('status')} vector_state={audit.get('vector_state')} semantic_fresh={audit.get('semantic_fresh')}")
print('Host is fully equipped and super-memori hybrid mode is operational for the current active line.')
print('Semantic retrieval: ACTIVE')
print('Vector state: HEALTHY')
print('Release health/audit/change-memory state: CLEAN')
PY
