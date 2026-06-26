#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
check() { if bash -c "$2"; then echo "PASS: $1"; PASS=$((PASS + 1)); else echo "FAIL: $1"; FAIL=$((FAIL + 1)); fi; }

check "SKILL.md exists" "[ -f '$SKILL_DIR/SKILL.md' ]"
check "SKILL.md has YAML frontmatter" "head -1 '$SKILL_DIR/SKILL.md' | grep -q '^---$'"
check "name is flywheel" "grep -q '^name: flywheel' '$SKILL_DIR/SKILL.md'"
check "mentions health or velocity" "grep -qiE 'health|velocity' '$SKILL_DIR/SKILL.md'"
check "mentions pool" "grep -qi 'pool' '$SKILL_DIR/SKILL.md'"
check "artifact-consistency script exists" "[ -x '$SKILL_DIR/scripts/artifact-consistency.sh' ]"
check "artifact-consistency allowlist exists" "[ -f '$SKILL_DIR/references/artifact-consistency-allowlist.txt' ]"

echo ""; echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
