#!/usr/bin/env bash
# swarmArena installer / preflight check.
#
#   bash install.sh [path/to/config.json]
#
# Verifies: Python >= 3.10; all scripts present and py_compile-clean; the config
# parses and validates; credentials visible via env (warn-only in paper mode);
# lighter-sdk importable (hard requirement only for live/autonomous_live modes).
# Paper mode runs stdlib-only — missing SDK is a warning, never a failure.

set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$SKILL_ROOT/scripts"
CONFIG_ARG="${1:-$SKILL_ROOT/config.json}"

pass() { printf '  [ok]   %s\n' "$1"; }
warn() { printf '  [warn] %s\n' "$1"; }
fail() { printf '  [FAIL] %s\n' "$1"; exit 1; }

echo "swarmArena install check"
echo "skill root: $SKILL_ROOT"

# --- 1. Python >= 3.10 -------------------------------------------------------
command -v python3 >/dev/null 2>&1 || fail "python3 not found"
PY_VER="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
    || fail "Python >= 3.10 required (found $PY_VER)"
pass "python3 $PY_VER"

# --- 2. all scripts present + py_compile -------------------------------------
REQUIRED_SCRIPTS="
autonomous_runner.py trade_loop.py market_scan_from_lighter.py
compute_features.py compute_signal.py compute_confluence.py
recommend_leverage.py size_position.py risk_checks.py prepare_order.py
live_execution_adapter.py lighter_rest_client.py lighter_signer.py
position_monitor.py trailing_stop.py fetch_trade_outcomes.py
review_trades.py update_metrics.py journal_trade.py
onboarding.py validate_config.py reconcile_state.py halt.py resume.py
status.py register_crons.py approval_runner.py
filelock.py decision_parser.py prompt_builder.py llm_client.py
model_runner.py arena_runner.py bot.py
"
for s in $REQUIRED_SCRIPTS; do
    [ -f "$SCRIPTS_DIR/$s" ] || fail "missing script: scripts/$s"
done
pass "all 34 scripts present"

if python3 - "$SCRIPTS_DIR" <<'PYEOF'
import os, py_compile, sys, tempfile
d = sys.argv[1]
files = sorted(f for f in os.listdir(d) if f.endswith(".py"))
with tempfile.TemporaryDirectory() as td:
    for f in files:
        py_compile.compile(os.path.join(d, f), cfile=os.path.join(td, f + ".pyc"), doraise=True)
PYEOF
then
    pass "py_compile clean for every script"
else
    fail "py_compile errors"
fi

# --- 3. config valid ---------------------------------------------------------
CONFIG="$CONFIG_ARG"
if [ ! -f "$CONFIG" ]; then
    if [ -f "$SKILL_ROOT/config.example.json" ]; then
        warn "config not found at $CONFIG — validating config.example.json instead"
        CONFIG="$SKILL_ROOT/config.example.json"
    else
        fail "no config found"
    fi
fi
python3 -m json.tool "$CONFIG" >/dev/null || fail "config is not valid JSON: $CONFIG"
pass "config parses as JSON"

VERDICT="$(python3 "$SCRIPTS_DIR/validate_config.py" "$CONFIG" || true)"
OK="$(printf '%s' "$VERDICT" | python3 -c 'import sys, json; print(json.load(sys.stdin)["ok"])')"
[ "$OK" = "True" ] || fail "config validation failed: $VERDICT"
pass "config validates ($CONFIG)"
printf '%s' "$VERDICT" | python3 -c '
import sys, json
v = json.load(sys.stdin)
for w in v.get("warnings", []):
    print("  [warn] config:", w)
'

MODE="$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["mode"])' "$CONFIG")"
pass "mode: $MODE"

# --- 4. credentials (env only; warn-only in paper mode) ----------------------
MISSING_CREDS=""
for var in LIGHTER_API_PRIVATE_KEY LIGHTER_API_KEY_INDEX LIGHTER_ACCOUNT_INDEX; do
    if [ -z "${!var:-}" ]; then MISSING_CREDS="$MISSING_CREDS $var"; fi
done
if [ -n "$MISSING_CREDS" ]; then
    if [ "$MODE" = "paper" ] || [ "$MODE" = "approval" ]; then
        warn "credentials not set (env:$MISSING_CREDS ) — fine for $MODE mode"
    else
        fail "mode=$MODE requires env credentials:$MISSING_CREDS"
    fi
else
    pass "credentials present in env (values masked: ****${LIGHTER_API_PRIVATE_KEY: -4})"
fi

# --- 5. lighter-sdk (required for live modes only) ---------------------------
if python3 -c 'import lighter' >/dev/null 2>&1; then
    pass "lighter-sdk installed"
else
    if [ "$MODE" = "live" ] || [ "$MODE" = "autonomous_live" ]; then
        fail "lighter-sdk required for $MODE — run: pip install -r $SKILL_ROOT/requirements.txt"
    else
        warn "lighter-sdk not installed — only needed for live/autonomous_live (paper is stdlib-only)"
    fi
fi

# --- 6. example data files parse ---------------------------------------------
for j in config.example.json state.example.json trades.example.json cron-templates.json; do
    python3 -m json.tool "$SKILL_ROOT/$j" >/dev/null || fail "$j is not valid JSON"
done
pass "all JSON examples parse"

mkdir -p "$SKILL_ROOT/logs"
pass "logs/ directory ready"

echo
echo "install check passed (mode=$MODE)."
echo "next: python3 $SCRIPTS_DIR/onboarding.py   # or copy config.example.json -> config.json"
echo "      python3 $SCRIPTS_DIR/register_crons.py --mode $MODE"
