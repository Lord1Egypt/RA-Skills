#!/usr/bin/env bash
# run-e2e.sh — E2E tests for openclaw-uninstall (install → schedule → uninstall → verify).
# Uses mocks: clawhub stub, --dry-run for schedule, temp dirs for uninstall/verify.
# Usage: ./tests/run-e2e.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HELPERS="$SCRIPT_DIR/helpers"
PASSED=0
FAILED=0

run_test() {
  local name="$1"
  if eval "$2"; then
    echo "  ✅ $name"
    ((PASSED++)) || true
    return 0
  else
    echo "  ❌ $name"
    ((FAILED++)) || true
    return 1
  fi
}

echo "=== openclaw-uninstall E2E tests ==="
echo ""

# --- Test 1: install.sh with clawhub stub ---
run_test "install.sh installs skill to workdir" '
  WORKDIR=$(mktemp -d)
  BINDIR=$(mktemp -d)
  trap "rm -rf \"$WORKDIR\" \"$BINDIR\"" RETURN
  ln -sf "$HELPERS/clawhub-stub.sh" "$BINDIR/clawhub"
  export PATH="$BINDIR:$PATH"
  export OPENCLAW_UNINSTALL_REPO_ROOT="$REPO_ROOT"
  cd "$REPO_ROOT" && ./scripts/install.sh "$WORKDIR"
  [[ -f "$WORKDIR/skills/uninstaller/SKILL.md" ]]
  [[ -d "$WORKDIR/skills/uninstaller/scripts" ]]
'

# --- Test 2: schedule-uninstall --dry-run ---
run_test "schedule-uninstall --dry-run prints CMD with args" '
  OUT=$(cd "$REPO_ROOT" && ./scripts/schedule-uninstall.sh --dry-run --notify-im "discord:user:123" --no-backup --preserve-state 2>&1)
  echo "$OUT" | grep -q "DRY_RUN_CMD:"
  echo "$OUT" | grep -q "notify-im"
  echo "$OUT" | grep -q "no-backup"
  echo "$OUT" | grep -q "preserve-state"
'

# --- Test 3: uninstall-oneshot --dry-run validates and exits without destructive ops ---
run_test "uninstall-oneshot --dry-run validates STATE_DIR" '
  FAKE_ROOT="$HOME/.openclaw-e2e-test-$$"
  mkdir -p "$FAKE_ROOT"
  STATE_DIR="$FAKE_ROOT/.openclaw"
  mkdir -p "$STATE_DIR"
  touch "$STATE_DIR/openclaw.json"
  export OPENCLAW_STATE_DIR="$STATE_DIR"
  cd "$REPO_ROOT" && ./scripts/uninstall-oneshot.sh --dry-run --no-backup
  [[ -d "$STATE_DIR" ]]
  rm -rf "$FAKE_ROOT"
'

# --- Test 3b: uninstall-oneshot --dry-run --preserve-state ---
run_test "uninstall-oneshot --dry-run --preserve-state prints Would preserve" '
  FAKE_ROOT="$HOME/.openclaw-e2e-test-$$"
  mkdir -p "$FAKE_ROOT"
  STATE_DIR="$FAKE_ROOT/.openclaw"
  mkdir -p "$STATE_DIR"
  touch "$STATE_DIR/openclaw.json"
  export OPENCLAW_STATE_DIR="$STATE_DIR"
  OUT=$(cd "$REPO_ROOT" && ./scripts/uninstall-oneshot.sh --dry-run --preserve-state 2>&1)
  echo "$OUT" | grep -q "Would preserve"
  [[ -d "$STATE_DIR" ]]
  rm -rf "$FAKE_ROOT"
'

# --- Test 4: verify-clean in clean env ---
run_test "verify-clean reports Fully cleaned when no residue" '
  FAKE_HOME=$(mktemp -d)
  export HOME="$FAKE_HOME"
  export OPENCLAW_STATE_DIR="$FAKE_HOME/.openclaw"
  OUT=$(cd "$REPO_ROOT" && ./scripts/verify-clean.sh 2>&1)
  echo "$OUT" | grep -q "Result: Fully cleaned"
  rm -rf "$FAKE_HOME"
'

# --- Test 5: verify-clean reports residue when state dir exists ---
run_test "verify-clean reports residue when state dir exists" '
  FAKE_HOME=$(mktemp -d)
  mkdir -p "$FAKE_HOME/.openclaw"
  export HOME="$FAKE_HOME"
  export OPENCLAW_STATE_DIR="$FAKE_HOME/.openclaw"
  OUT=$(cd "$REPO_ROOT" && ./scripts/verify-clean.sh 2>&1)
  echo "$OUT" | grep -q "Result: Residue found"
  rm -rf "$FAKE_HOME"
'

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
if [[ $FAILED -eq 0 ]]; then
  exit 0
else
  exit 1
fi
</think>

<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
StrReplace