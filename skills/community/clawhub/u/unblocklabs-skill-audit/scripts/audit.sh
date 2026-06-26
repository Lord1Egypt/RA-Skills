#!/usr/bin/env bash
# skill-audit/scripts/audit.sh
# Scans skill locations and outputs one JSON object per skill (JSONL format).
# Usage: bash audit.sh [workspace_skills_dir]

set -euo pipefail

WORKSPACE_SKILLS="${1:-$HOME/clawd/skills}"
GLOBAL_SKILLS_BASE="$HOME/.local/share/fnm/node-versions"

# Find global skills dir
GLOBAL_SKILLS=""
if [ -d "$GLOBAL_SKILLS_BASE" ]; then
  LATEST_NODE=$(ls -1 "$GLOBAL_SKILLS_BASE" 2>/dev/null | sort -V | tail -1)
  CANDIDATE="$GLOBAL_SKILLS_BASE/$LATEST_NODE/installation/lib/node_modules/openclaw/skills"
  [ -d "$CANDIDATE" ] && GLOBAL_SKILLS="$CANDIDATE"
fi

audit_skill() {
  local skill_md="$1"
  local source_label="$2"
  local skill_dir
  skill_dir="$(dirname "$skill_md")"
  local skill_name
  skill_name="$(basename "$skill_dir")"

  # Frontmatter
  local has_frontmatter="false" fm_name="" fm_description=""
  if head -1 "$skill_md" | grep -q "^---"; then
    has_frontmatter="true"
    fm_name=$(awk '/^---/{n++;next} n==1 && /^name:/{sub(/^name:\s*/, ""); print; exit}' "$skill_md" | tr -d '"')
    fm_description=$(awk '/^---/{n++;next} n==1 && /^description:/{sub(/^description:\s*/, ""); print; exit}' "$skill_md" | tr -d '"')
  fi

  # Description trigger quality
  local desc_is_trigger="false"
  echo "$fm_description" | grep -qiE "(use when|trigger|use for|use if|invoke|run when|fires when|activate)" && desc_is_trigger="true"

  # Gotchas section
  local has_gotchas="false"
  grep -qiE "^#+\s*(gotcha|pitfall|common issue|common error|known issue|caveat|watch out|warning|trouble)" "$skill_md" && has_gotchas="true"

  # Progressive disclosure
  local subdir_count=0
  local has_scripts="false" has_references="false" has_assets="false"
  [ -d "$skill_dir/scripts" ] && has_scripts="true" && subdir_count=$((subdir_count+1))
  { [ -d "$skill_dir/references" ] || [ -d "$skill_dir/ref" ] || [ -d "$skill_dir/docs" ]; } && has_references="true" && subdir_count=$((subdir_count+1))
  { [ -d "$skill_dir/assets" ] || [ -d "$skill_dir/templates" ]; } && has_assets="true" && subdir_count=$((subdir_count+1))
  [ -d "$skill_dir/examples" ] && subdir_count=$((subdir_count+1))
  local has_progressive_disclosure="false"
  [ "$subdir_count" -gt 0 ] && has_progressive_disclosure="true"

  # Executable files
  local executable_count
  executable_count=$(find "$skill_dir" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.mjs" -o -name "*.js" -o -name "*.ts" \) -not -path "*/node_modules/*" -not -path "*/.venv/*" 2>/dev/null | wc -l | tr -d ' ')

  # Size
  local skill_md_size
  skill_md_size=$(wc -c < "$skill_md" | tr -d ' ')

  # Total files
  local total_files
  total_files=$(find "$skill_dir" -type f -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/.git/*" 2>/dev/null | wc -l | tr -d ' ')

  # Score
  local score=0
  [ "$has_frontmatter" = "true" ] && [ -n "$fm_name" ] && [ -n "$fm_description" ] && score=$((score+2))
  [ "$desc_is_trigger" = "true" ] && score=$((score+2))
  [ "$has_gotchas" = "true" ] && score=$((score+2))
  [ "$has_progressive_disclosure" = "true" ] && score=$((score+2))
  [ "$executable_count" -gt 0 ] && score=$((score+1))
  [ "$skill_md_size" -ge 200 ] && [ "$skill_md_size" -le 5000 ] && score=$((score+1))

  printf '%s|%s|%s|%d|%s|%s|%s|%s|%d|%d|%d\n' \
    "$skill_name" "$source_label" "$skill_dir" "$score" \
    "$desc_is_trigger" "$has_gotchas" "$has_progressive_disclosure" "$has_frontmatter" \
    "$executable_count" "$skill_md_size" "$total_files"
}

echo "NAME|SOURCE|PATH|SCORE|TRIGGER_DESC|HAS_GOTCHAS|PROGRESSIVE|FRONTMATTER|EXECUTABLES|SKILLMD_SIZE|TOTAL_FILES"

# Workspace
find "$WORKSPACE_SKILLS" -maxdepth 2 -name "SKILL.md" -not -path "*/node_modules/*" -not -path "*/.venv/*" 2>/dev/null | sort | while read -r f; do
  audit_skill "$f" "workspace"
done

# Global
if [ -n "$GLOBAL_SKILLS" ]; then
  find "$GLOBAL_SKILLS" -maxdepth 2 -name "SKILL.md" 2>/dev/null | sort | while read -r f; do
    audit_skill "$f" "global"
  done
fi

# Orphan .skill files
echo "---ORPHANS---"
find "$WORKSPACE_SKILLS" -name "*.skill" -type f 2>/dev/null
