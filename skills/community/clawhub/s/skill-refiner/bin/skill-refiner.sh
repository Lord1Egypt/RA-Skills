#!/usr/bin/env bash
# skill-refiner: Audit and fix OpenClaw skills for skill-creator compliance
# Usage: npx skill-refiner [workspace_dir]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${1:-$HOME/.openclaw/workspace}"

echo "🔍 skill-refiner — scanning: $WORKSPACE"
echo ""

# Find all skills
SKILLS=$(bash "$SCRIPT_DIR/../scripts/find_skills.sh" "$WORKSPACE")

if [ -z "$SKILLS" ]; then
  echo "No skills found in $WORKSPACE"
  exit 0
fi

TOTAL=0
COMPLIANT=0
NON_COMPLIANT=0

while IFS= read -r skill_dir; do
  TOTAL=$((TOTAL + 1))
  result=$(python3 "$SCRIPT_DIR/../scripts/audit_skill.py" "$skill_dir")
  name=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('skill_name','?'))")
  is_compliant=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('compliant',False))")
  issues=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n  '.join(d.get('issues',[])))")
  warnings=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n  '.join(d.get('warnings',[])))")

  if [ "$is_compliant" = "True" ]; then
    COMPLIANT=$((COMPLIANT + 1))
    echo "✅ $name"
    if [ -n "$warnings" ]; then
      echo "  ⚠️  $warnings"
    fi
  else
    NON_COMPLIANT=$((NON_COMPLIANT + 1))
    echo "❌ $name"
    if [ -n "$issues" ]; then
      echo "  ✗  $issues"
    fi
    if [ -n "$warnings" ]; then
      echo "  ⚠️  $warnings"
    fi
  fi
done <<< "$SKILLS"

echo ""
echo "─────────────────────────────────"
echo "Total: $TOTAL  ✅ $COMPLIANT  ❌ $NON_COMPLIANT"
