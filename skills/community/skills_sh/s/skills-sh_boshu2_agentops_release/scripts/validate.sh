#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0

check() { if bash -c "$2"; then echo "PASS: $1"; PASS=$((PASS + 1)); else echo "FAIL: $1"; FAIL=$((FAIL + 1)); fi; }

check "SKILL.md exists" "[ -f '$SKILL_DIR/SKILL.md' ]"
check "SKILL.md has YAML frontmatter" "head -1 '$SKILL_DIR/SKILL.md' | grep -q '^---$'"
check "SKILL.md has name: release" "grep -q '^name: release' '$SKILL_DIR/SKILL.md'"
check "SKILL.md mentions changelog" "grep -qi 'changelog' '$SKILL_DIR/SKILL.md'"
check "SKILL.md mentions tag" "grep -q 'tag' '$SKILL_DIR/SKILL.md'"
check "SKILL.md mentions pre-flight" "grep -qi 'pre-flight' '$SKILL_DIR/SKILL.md'"
check "SKILL.md mentions version bump" "grep -qi 'version bump' '$SKILL_DIR/SKILL.md'"

echo ""; echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
