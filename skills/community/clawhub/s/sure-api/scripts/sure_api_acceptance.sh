#!/usr/bin/env bash
set -euo pipefail

ROOT="/root/.openclaw/workspace"
SKILL_DIR="$ROOT/skills/sure-api"
SKILL_MD="$SKILL_DIR/SKILL.md"
REF_OPENAPI="$SKILL_DIR/references/openapi.yaml"
REF_SUMMARY="$SKILL_DIR/references/api_endpoints_summary.md"
CLI_JS="$SKILL_DIR/scripts/sure_api_cli.js"
REQ_SH="$SKILL_DIR/scripts/sure_api_request.sh"
SMOKE_SH="$SKILL_DIR/scripts/sure_api_smoke.sh"
UPDATE_SH="$SKILL_DIR/scripts/sure_openapi_update.sh"
SUM_JS="$SKILL_DIR/scripts/sure_openapi_summarize.js"

fail(){ echo "[FAIL] $*" >&2; exit 1; }
ok(){ echo "[OK] $*"; }

[ -d "$SKILL_DIR" ] || fail "missing skill dir"
[ -f "$SKILL_MD" ] || fail "missing SKILL.md"
[ -f "$REF_OPENAPI" ] || fail "missing references/openapi.yaml"
[ -f "$REF_SUMMARY" ] || fail "missing references/api_endpoints_summary.md"
[ -f "$CLI_JS" ] || fail "missing sure_api_cli.js"
[ -f "$REQ_SH" ] || fail "missing sure_api_request.sh"
[ -f "$SMOKE_SH" ] || fail "missing sure_api_smoke.sh"
[ -f "$UPDATE_SH" ] || fail "missing sure_openapi_update.sh"
[ -f "$SUM_JS" ] || fail "missing sure_openapi_summarize.js"

grep -q '^---$' "$SKILL_MD" || fail "SKILL.md missing frontmatter fence"
grep -q '^name: sure-api$' "$SKILL_MD" || fail "SKILL.md name must be sure-api"
grep -q '^description:' "$SKILL_MD" || fail "SKILL.md missing description"
grep -q 'https://github.com/we-promise/sure/tree/main/docs/api' "$SKILL_MD" || fail "SKILL.md missing official docs dir URL"
grep -q 'https://github.com/we-promise/sure/blob/main/docs/api/openapi.yaml' "$SKILL_MD" || fail "SKILL.md missing official openapi URL"
grep -q 'self-update' "$SKILL_MD" || fail "SKILL.md should explain self-update"
grep -q 'ClawHub publish readiness' "$SKILL_MD" || fail "SKILL.md should include publish readiness section"

grep -q '/api/v1/accounts' "$REF_SUMMARY" || fail "endpoint summary missing accounts"
grep -q '/api/v1/transactions' "$REF_SUMMARY" || fail "endpoint summary missing transactions"
grep -q '/api/v1/trades' "$REF_SUMMARY" || fail "endpoint summary missing trades"
grep -q '/api/v1/valuations' "$REF_SUMMARY" || fail "endpoint summary missing valuations"
grep -q '/api/v1/chats' "$REF_SUMMARY" || fail "endpoint summary missing chats"

node "$SUM_JS" "$REF_OPENAPI" >/tmp/sure_api_summary.check.md
cmp -s /tmp/sure_api_summary.check.md "$REF_SUMMARY" || fail "summary out of date; run sure_openapi_update.sh"
ok "skill structure and references look good"

if [ "${1:-}" = "--with-live-api" ]; then
  "$SMOKE_SH" >/tmp/sure_api_smoke.out
  ok "live API smoke passed"
else
  echo "[SKIP] live API smoke not run (pass --with-live-api to enable)"
fi

echo "DONE: sure-api acceptance passed"
