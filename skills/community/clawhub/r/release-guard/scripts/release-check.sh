#!/usr/bin/env bash
set -u

skill_dir="${1:-}"
status=0

say() { printf '%s\n' "$*"; }
pass() { say "PASS: $*"; }
warn() { say "WARN: $*"; }
fail() { say "FAIL: $*"; status=1; }

if [ -z "$skill_dir" ]; then
  say "Usage: bash scripts/release-check.sh /path/to/skill-folder"
  exit 2
fi

if [ ! -d "$skill_dir" ]; then
  fail "Skill folder does not exist: $skill_dir"
  exit "$status"
fi

if [ -f "$skill_dir/SKILL.md" ]; then
  pass "SKILL.md exists."
else
  fail "SKILL.md is missing."
fi

file_count=$(find "$skill_dir" -type f \
  ! -path '*/.git/*' \
  ! -path '*/node_modules/*' \
  ! -path '*/.clawhub/*' \
  | wc -l | tr -d ' ')

if [ "$file_count" -le 10 ]; then
  pass "Package file count is reviewable: $file_count files."
else
  warn "Package has $file_count files; review for accidental bundled workspace content."
fi

for unwanted in agents memory node_modules .git workspace skills-archive; do
  if find "$skill_dir" -type d -name "$unwanted" -print -quit | grep -q .; then
    warn "Found directory named '$unwanted'; confirm it belongs to this skill."
  fi
done

if grep -RInE '(^|[;[:space:]])e[v]al([[:space:]]|$)' "$skill_dir" \
  --exclude-dir=.git --exclude-dir=node_modules --exclude='release-check.sh' >/tmp/release-guard-shell-eval.$$ 2>/dev/null; then
  warn "Potential dynamic shell evaluation found; review these lines:"
  sed -n '1,20p' /tmp/release-guard-shell-eval.$$
else
  pass "No dynamic shell evaluation found outside release-check.sh."
fi
rm -f /tmp/release-guard-shell-eval.$$

if grep -RInE '(api[_-]?key|secret|token|password)[[:space:]]*[:=]' "$skill_dir" \
  --exclude-dir=.git --exclude-dir=node_modules >/tmp/release-guard-secret.$$ 2>/dev/null; then
  warn "Secret-like assignment text found; manually verify it is not a real credential:"
  sed -n '1,20p' /tmp/release-guard-secret.$$
else
  pass "No simple secret-like assignments found."
fi
rm -f /tmp/release-guard-secret.$$

if [ "$status" -eq 0 ]; then
  say "FINAL: PASS with any WARN items requiring manual review."
else
  say "FINAL: FAIL. Fix the FAIL items before publishing."
fi
exit "$status"
