#!/usr/bin/env bash
# Verify workspace structure, file sizes, and required files
# Usage: bash scripts/audit-structure.sh [--verbose]
set -euo pipefail

WS="${WS:-$HOME/.openclaw/workspace}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONF="${AUDIT_CONFIG:-$SKILL_DIR/audit.conf}"

# Load custom limits if config exists
if [ -f "$CONF" ]; then
  # shellcheck source=/dev/null
  source "$CONF"
fi

# Defaults (overridden by audit.conf)
AGENTS_LIMIT="${AGENTS_LIMIT:-1000}"
SOUL_LIMIT="${SOUL_LIMIT:-200}"
USER_LIMIT="${USER_LIMIT:-200}"
IDENTITY_LIMIT="${IDENTITY_LIMIT:-50}"
TOOLS_LIMIT="${TOOLS_LIMIT:-500}"
HEARTBEAT_LIMIT="${HEARTBEAT_LIMIT:-100}"
MEMORY_LIMIT="${MEMORY_LIMIT:-150}"

echo "=== Structure & Size Audit ==="
echo ""

# Required files
echo "--- Required Files ---"
REQUIRED=("AGENTS.md" "SOUL.md" "USER.md" "IDENTITY.md" "TOOLS.md")
REQ_MISS=0
for f in "${REQUIRED[@]}"; do
  if [ -f "$WS/$f" ]; then
    echo "  ✅ $f"
  else
    echo "  ❌ MISSING: $f"
    REQ_MISS=$((REQ_MISS + 1))
  fi
done

echo ""
echo "--- Optional Files ---"
OPTIONAL=("HEARTBEAT.md" "MEMORY.md" "BOOT.md" "BOOTSTRAP.md")
for f in "${OPTIONAL[@]}"; do
  if [ -f "$WS/$f" ]; then
    echo "  ✅ $f"
  else
    echo "  ⊘ $f (not present)"
  fi
done

# Check memory/ directory
if [ -d "$WS/memory" ]; then
  DAILY_COUNT=$(find "$WS/memory" -maxdepth 1 -name "????-??-??.md" | wc -l | tr -d ' ')
  echo "  ✅ memory/ ($DAILY_COUNT daily files)"
else
  echo "  ⊘ memory/ directory (not present)"
fi

# Check skills/ directory
if [ -d "$WS/skills" ]; then
  SKILL_COUNT=$(find "$WS/skills" -maxdepth 2 -name "SKILL.md" | wc -l | tr -d ' ')
  echo "  ✅ skills/ ($SKILL_COUNT skills)"
else
  echo "  ⊘ skills/ (not present)"
fi

echo ""
echo "--- File Size Limits ---"
SIZE_WARN=0
check_size() {
  local file="$1" limit="$2" label="$3"
  if [ -f "$WS/$file" ]; then
    lines=$(wc -l < "$WS/$file" | tr -d ' ')
    if [ "$lines" -gt "$limit" ]; then
      echo "  ⚠️  $label: $lines lines (limit: $limit)"
      SIZE_WARN=$((SIZE_WARN + 1))
    else
      echo "  ✅ $label: $lines/$limit lines"
    fi
  fi
}

check_size "AGENTS.md" "$AGENTS_LIMIT" "AGENTS.md"
check_size "SOUL.md" "$SOUL_LIMIT" "SOUL.md"
check_size "USER.md" "$USER_LIMIT" "USER.md"
check_size "IDENTITY.md" "$IDENTITY_LIMIT" "IDENTITY.md"
check_size "TOOLS.md" "$TOOLS_LIMIT" "TOOLS.md"
check_size "HEARTBEAT.md" "$HEARTBEAT_LIMIT" "HEARTBEAT.md"
check_size "MEMORY.md" "$MEMORY_LIMIT" "MEMORY.md"

echo ""
echo "--- Skills Validation ---"
SKILL_ISSUES=0
if [ -d "$WS/skills" ]; then
  for skilldir in "$WS/skills"/*/; do
    [ -d "$skilldir" ] || continue
    skillname=$(basename "$skilldir")
    skillmd="$skilldir/SKILL.md"
    if [ ! -f "$skillmd" ]; then
      echo "  ❌ $skillname: missing SKILL.md"
      SKILL_ISSUES=$((SKILL_ISSUES + 1))
      continue
    fi
    # Check frontmatter has name and description
    has_name=$(head -20 "$skillmd" | grep -c "^name:" || true)
    has_desc=$(head -20 "$skillmd" | grep -c "^description:" || true)
    if [ "$has_name" -eq 0 ] || [ "$has_desc" -eq 0 ]; then
      echo "  ⚠️  $skillname: missing name or description in frontmatter"
      SKILL_ISSUES=$((SKILL_ISSUES + 1))
    else
      echo "  ✅ $skillname"
    fi
  done
else
  echo "  (no skills directory)"
fi

echo ""
echo "--- Memory Hygiene ---"
MEM_ISSUES=0
if [ -d "$WS/memory" ]; then
  # Check for secrets in memory files
  SECRET_HITS=$(grep -rl -E '(sk-[a-zA-Z0-9]{20,}|tvly-[a-zA-Z0-9]+|ghp_[a-zA-Z0-9]+|xai-[a-zA-Z0-9]+|fmu1-[a-zA-Z0-9]+|op_[a-zA-Z0-9]+)' "$WS/memory/" "$WS/MEMORY.md" 2>/dev/null | head -5)
  if [ -n "$SECRET_HITS" ]; then
    echo "  ❌ Possible secrets found in memory files:"
    echo "$SECRET_HITS" | while read -r f; do echo "    - $(basename "$f")"; done
    MEM_ISSUES=$((MEM_ISSUES + 1))
  else
    echo "  ✅ No secrets detected in memory files"
  fi
else
  echo "  ⊘ No memory directory to scan"
fi

echo ""
echo "--- Git Status ---"
if [ -d "$WS/.git" ]; then
  UNTRACKED=$(cd "$WS" && git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
  MODIFIED=$(cd "$WS" && git diff --name-only 2>/dev/null | wc -l | tr -d ' ')
  STAGED=$(cd "$WS" && git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
  HAS_REMOTE=$(cd "$WS" && git remote -v 2>/dev/null | wc -l | tr -d ' ')

  echo "  Untracked: $UNTRACKED | Modified: $MODIFIED | Staged: $STAGED"
  if [ "$HAS_REMOTE" -gt 0 ]; then
    echo "  ⚠️  Remote configured — ensure workspace is PRIVATE"
  else
    echo "  ✅ No remote configured"
  fi

  # Check .gitignore for secrets
  if [ -f "$WS/.gitignore" ]; then
    for pattern in "*.key" "*.pem" ".env" "secrets*"; do
      if grep -qF "$pattern" "$WS/.gitignore"; then
        :
      else
        echo "  ⚠️  .gitignore missing pattern: $pattern"
      fi
    done
  else
    echo "  ⚠️  No .gitignore file"
  fi
else
  echo "  ⊘ Not a git repository"
fi

echo ""
TOTAL_ISSUES=$((REQ_MISS + SIZE_WARN + SKILL_ISSUES + MEM_ISSUES))
if [ "$TOTAL_ISSUES" -gt 0 ]; then
  echo "⚠️  $TOTAL_ISSUES issue(s) found"
  exit 1
else
  echo "✅ Structure audit passed"
  exit 0
fi
