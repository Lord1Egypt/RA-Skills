#!/usr/bin/env bash
# Validation environment requirement: this script must run from within the
# OpenClaw workspace where ../skill-creator-canonical/ is available.
# It is not designed for isolated package-directory execution.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

python3 ../skill-creator-canonical/scripts/quick_validate.py "$ROOT"
python3 ../skill-creator-canonical/scripts/validate_weak_models.py "$ROOT"
python3 tests/test_temporal_retrieval.py
python3 tests/test_relation_target_validation.py
python3 tests/test_repair_plan.py
python3 tests/test_semantic_unbuilt_state.py
python3 tests/test_promotion_candidates.py
python3 tests/test_hot_change_buffer.py
python3 tests/test_result_authority_surface.py
python3 tests/test_evals_surface.py
python3 tests/test_semantic_daemon_surface.py

for f in SKILL.md _meta.json .clawhubignore CHANGELOG.md PACKAGING_CHECKLIST.md \
         query-memory.sh memorize.sh index-memory.sh health-check.sh startup-self-check.sh \
         audit-memory.sh repair-memory.sh list-promotion-candidates.sh validate-release.sh \
         hooks/super-memori-session-start/HOOK.md hooks/super-memori-session-start/handler.js \
         references/release-status.md references/verification-evidence.md references/reference-test-log.md; do
  [[ -f "$ROOT/$f" ]] || { echo "release gate blocked: missing package-root file $f"; exit 1; }
done
[[ -d "$ROOT/scripts" ]] || { echo 'release gate blocked: missing scripts/ directory'; exit 1; }
[[ -d "$ROOT/references" ]] || { echo 'release gate blocked: missing references/ directory'; exit 1; }
[[ -f "$ROOT/tests/regression/run-all.sh" ]] || { echo 'release gate blocked: tests/regression/run-all.sh missing'; exit 1; }
bash "$ROOT/tests/regression/run-all.sh"

python3 repair-memory.sh --classify --json >/tmp/super-memori-repair-classify.json
python3 audit-memory.sh --json >/tmp/super-memori-audit.json
./health-check.sh --json >/tmp/super-memori-health.json || true

python3 - <<'PY'
import json, pathlib, re
root = pathlib.Path('/tmp')
audit = json.loads((root / 'super-memori-audit.json').read_text())
health = json.loads((root / 'super-memori-health.json').read_text())
checks = {item.get('name'): item for item in health.get('checks', [])}
if audit.get('broken_relations'):
    raise SystemExit('release gate blocked: broken_relations present')
if audit.get('vector_state') not in {'ok', 'semantic-unbuilt', 'stale-vectors'}:
    raise SystemExit(f"release gate blocked: unexpected vector_state {audit.get('vector_state')}")
if health.get('status') == 'FAIL':
    raise SystemExit('release gate blocked: health FAIL')
for forbidden_name in ('canonical_files', 'lexical_fts'):
    item = checks.get(forbidden_name)
    if item and not item.get('ok', False):
        raise SystemExit(f'release gate blocked: critical WARN surface {forbidden_name} is not ok')

skill_root = pathlib.Path.cwd()
meta = json.loads((skill_root / '_meta.json').read_text())
version = meta.get('version')
if not isinstance(version, str) or not version.strip():
    raise SystemExit('release gate blocked: _meta.json version missing or invalid')
published_at = meta.get('publishedAt')
if published_at is not None and (not isinstance(published_at, int) or published_at <= 0):
    raise SystemExit('release gate blocked: _meta.json publishedAt must be null (unpublished) or a positive integer (published)')
is_published = published_at is not None

skill_text = (skill_root / 'SKILL.md').read_text()
expected_release_line = (
    f'**Release line:** `v{version}` current published line'
    if is_published else
    f'**Release line:** `v{version}` unpublished current candidate line'
)
if expected_release_line not in skill_text:
    state = 'published' if is_published else 'unpublished'
    raise SystemExit(f'release gate blocked: SKILL.md release line is not synced to {state} version {version}')
changelog_text = (skill_root / 'CHANGELOG.md').read_text()
release_status_text = (skill_root / 'references/release-status.md').read_text()
verification_text = (skill_root / 'references/verification-evidence.md').read_text()
reference_log_text = (skill_root / 'references/reference-test-log.md').read_text()

if f'# Super Memori — v{version} Project Skill' not in skill_text:
    raise SystemExit(f'release gate blocked: SKILL.md heading is not synced to version {version}')
if f'**Release line:** `v{version}`' not in skill_text:
    raise SystemExit(f'release gate blocked: SKILL.md release line is not synced to version {version}')
header_versions = re.findall(r'^##.*\(v(\d+\.\d+\.\d+)\)', skill_text, re.MULTILINE)
for hv in header_versions:
    if hv != version:
        raise SystemExit(f'release gate blocked: section header contains stale version v{hv}, expected v{version}')
if not re.search(rf'^##\s+{re.escape(version)}\s+-\s+', changelog_text, re.MULTILINE):
    raise SystemExit(f'release gate blocked: CHANGELOG.md latest entry missing version {version}')
if f'## {version} meaning' not in release_status_text:
    raise SystemExit(f'release gate blocked: release-status.md missing active version heading {version}')
if f'The current active release line is `{version}`.' not in release_status_text:
    raise SystemExit(f'release gate blocked: release-status.md current active line not synced to {version}')
if f'# Verification Evidence — super-memori {version}' not in verification_text:
    raise SystemExit(f'release gate blocked: verification-evidence.md heading not synced to {version}')
if f'- line: `{version}`' not in verification_text:
    raise SystemExit(f'release gate blocked: verification-evidence.md line marker not synced to {version}')
if f'# Reference Test Log — super-memori {version}' not in reference_log_text:
    raise SystemExit(f'release gate blocked: reference-test-log.md heading not synced to {version}')

print('[OK] release gate baseline checks passed')
print(f'[OK] release surface sync checks passed for version {version}')
PY

if [[ "$STRICT" == "1" ]]; then
  python3 - <<'PY'
import json, pathlib
root = pathlib.Path('/tmp')
health = json.loads((root / 'super-memori-health.json').read_text())
audit = json.loads((root / 'super-memori-audit.json').read_text())
if health.get('status') not in {'OK', 'WARN'}:
    raise SystemExit('strict gate blocked: invalid health state')
if audit.get('vector_state') == 'orphan-vectors':
    raise SystemExit('strict gate blocked: orphan-vectors drift present')
print('[OK] strict release gate checks passed')
PY
fi
