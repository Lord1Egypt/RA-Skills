#!/bin/bash
# Soul Question skill — structure & content validation
# Run: bash skills/soul-question/test-skill.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
README="$SKILL_DIR/README.md"
CLAWHUB="$SKILL_DIR/clawhub.json"

PASS=0
FAIL=0

check() {
  local desc="$1"
  local result="$2"
  if [ "$result" = "true" ]; then
    echo "  ✅ $desc"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $desc"
    FAIL=$((FAIL + 1))
  fi
}

echo "═══════════════════════════════════════"
echo "  Soul Question — Skill Validation"
echo "═══════════════════════════════════════"
echo ""

# ─── 1. File existence ───
echo "📁 File existence"
check "SKILL.md exists" "$([ -f "$SKILL_MD" ] && echo true || echo false)"
check "README.md exists" "$([ -f "$README" ] && echo true || echo false)"
check "clawhub.json exists" "$([ -f "$CLAWHUB" ] && echo true || echo false)"
echo ""

# ─── 2. SKILL.md frontmatter ───
echo "📋 SKILL.md frontmatter"
FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$SKILL_MD")
check "Has YAML frontmatter" "$(echo "$FRONTMATTER" | grep -q 'name:' && echo true || echo false)"
check "name field = soul-question" "$(echo "$FRONTMATTER" | grep -q 'name: soul-question' && echo true || echo false)"
check "Has description field" "$(echo "$FRONTMATTER" | grep -q 'description:' && echo true || echo false)"
check "Has version field" "$(echo "$FRONTMATTER" | grep -q 'version:' && echo true || echo false)"
echo ""

# ─── 3. SKILL.md required sections ───
echo "📑 SKILL.md sections"
check "Has 'When to Activate'" "$(grep -q '## When to Activate' "$SKILL_MD" && echo true || echo false)"
check "Has 'Input'" "$(grep -q '## Input' "$SKILL_MD" && echo true || echo false)"
check "Has 'Workflow'" "$(grep -q '## Workflow' "$SKILL_MD" && echo true || echo false)"
check "Has 'Guidelines'" "$(grep -q '## Guidelines' "$SKILL_MD" && echo true || echo false)"
check "Has 'Error Handling'" "$(grep -q '## Error Handling' "$SKILL_MD" && echo true || echo false)"
check "Has quality gate" "$(grep -q 'Quality gate\|quality gate\|Quality Gate' "$SKILL_MD" && echo true || echo false)"
echo ""

# ─── 4. Signal types (core differentiation) ───
echo "🔍 Signal types defined"
check "Value-behavior gap" "$(grep -q 'Value-behavior gap\|value-behavior gap' "$SKILL_MD" && echo true || echo false)"
check "Untested.*assumption" "$(grep -q 'Untested.*assumption\|untested.*assumption' "$SKILL_MD" && echo true || echo false)"
check "Frame lock" "$(grep -q 'Frame lock\|frame lock' "$SKILL_MD" && echo true || echo false)"
check "Contradiction" "$(grep -q 'Contradiction\|contradiction' "$SKILL_MD" && echo true || echo false)"
check "Avoidance" "$(grep -q 'Avoidance\|avoidance' "$SKILL_MD" && echo true || echo false)"
check "Meta-question" "$(grep -q 'Meta-question\|meta-question' "$SKILL_MD" && echo true || echo false)"
echo ""

# ─── 5. Anti-pattern guards ───
echo "🚫 Anti-pattern guards"
check "Warns against generic questions" "$(grep -q 'generic\|Generic\|template' "$SKILL_MD" && echo true || echo false)"
check "Warns against disguised advice" "$(grep -q 'disguised advice\|advice in question' "$SKILL_MD" && echo true || echo false)"
check "Has 'less is more' / quality-over-quantity" "$(grep -q 'Less is more\|quality.*quantity\|Quality over quantity' "$SKILL_MD" && echo true || echo false)"
echo ""

# ─── 6. Output format ───
echo "📤 Output format"
check "Has output template with 🪞" "$(grep -q '🪞' "$SKILL_MD" && echo true || echo false)"
check "Has 'Based on' citation format" "$(grep -q 'Based on:' "$SKILL_MD" && echo true || echo false)"
check "Explicitly says no preamble/summary" "$(grep -q 'No preamble\|No summary' "$SKILL_MD" && echo true || echo false)"
echo ""

# ─── 7. Language check (should be English for global audience) ───
echo "🌍 Language (global-readiness)"
CJK_LINES=$(grep -cP '[\x{4e00}-\x{9fff}]' "$SKILL_MD" 2>/dev/null || echo 0)
check "SKILL.md has no CJK characters (English only)" "$([ "$CJK_LINES" -eq 0 ] && echo true || echo false)"
CJK_README=$(grep -cP '[\x{4e00}-\x{9fff}]' "$README" 2>/dev/null || echo 0)
check "README.md has no CJK characters" "$([ "$CJK_README" -eq 0 ] && echo true || echo false)"
echo ""

# ─── 8. clawhub.json validation ───
echo "📦 clawhub.json"
if command -v python3 &>/dev/null; then
  VALID_JSON=$(python3 -c "import json; json.load(open('$CLAWHUB')); print('true')" 2>/dev/null || echo "false")
  check "Valid JSON" "$VALID_JSON"
  if [ "$VALID_JSON" = "true" ]; then
    check "Has 'name' field" "$(python3 -c "import json; d=json.load(open('$CLAWHUB')); print('true' if 'name' in d else 'false')")"
    check "Has 'tagline' field" "$(python3 -c "import json; d=json.load(open('$CLAWHUB')); print('true' if 'tagline' in d else 'false')")"
    check "Has 'description' field" "$(python3 -c "import json; d=json.load(open('$CLAWHUB')); print('true' if 'description' in d else 'false')")"
    check "Has 'category' field" "$(python3 -c "import json; d=json.load(open('$CLAWHUB')); print('true' if 'category' in d else 'false')")"
    check "Has 'tags' (non-empty list)" "$(python3 -c "import json; d=json.load(open('$CLAWHUB')); print('true' if isinstance(d.get('tags'), list) and len(d['tags'])>0 else 'false')")"
    check "version matches SKILL.md" "$(python3 -c "
import json, re
ch = json.load(open('$CLAWHUB'))
with open('$SKILL_MD') as f:
    fm = re.search(r'version:\s*\"?([^\"\\n]+)', f.read())
print('true' if fm and ch.get('version') == fm.group(1).strip() else 'false')
")"
    TAGLINE_LEN=$(python3 -c "import json; print(len(json.load(open('$CLAWHUB')).get('tagline','')))")
    check "Tagline under 80 chars (${TAGLINE_LEN})" "$([ "$TAGLINE_LEN" -le 80 ] && echo true || echo false)"
  fi
else
  echo "  ⚠️  python3 not found, skipping JSON validation"
fi
echo ""

# ─── 9. README quality checks ───
echo "📖 README.md"
check "Has install command" "$(grep -q 'openclaw install' "$README" && echo true || echo false)"
check "Has usage example" "$(grep -q 'soul question\|Soul Question' "$README" && echo true || echo false)"
check "Has privacy section" "$(grep -qi 'privacy' "$README" && echo true || echo false)"
check "Has license" "$(grep -qi 'license\|MIT' "$README" && echo true || echo false)"
check "Has concrete examples with output" "$(grep -q '🪞 Soul Question' "$README" && echo true || echo false)"
echo ""

# ─── Summary ───
TOTAL=$((PASS + FAIL))
echo "═══════════════════════════════════════"
echo "  Results: $PASS/$TOTAL passed"
if [ "$FAIL" -gt 0 ]; then
  echo "  ⚠️  $FAIL check(s) failed"
  exit 1
else
  echo "  All checks passed ✓"
  exit 0
fi
