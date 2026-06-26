#!/usr/bin/env bash
# extract-deps.sh — extract skill dependency edges (frontmatter depends-on + topic body Skill() calls)
# Usage: extract-deps.sh <slug...> [--scope topic|skill|both]
# Output: JSON {"nodes":[...], "edges":[...]} to stdout

set -euo pipefail

SKILLS_DIR_PRIMARY="${SKILLS_DIR:-$HOME/.claude/skills}"
SKILLS_DIR_FALLBACK="$HOME/.agents/skills"
SCOPE="both"

# Parse args
declare -a slugs=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope) SCOPE="${2:?--scope requires a value}"; shift 2 ;;
    --scope=*) SCOPE="${1#--scope=}"; shift ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) slugs+=("$1"); shift ;;
  esac
done

if [[ ${#slugs[@]} -eq 0 ]]; then
  echo "Usage: $0 <slug...> [--scope topic|skill|both]" >&2
  exit 1
fi

case "$SCOPE" in
  topic|skill|both) ;;
  *) echo "Invalid --scope: $SCOPE (expected topic|skill|both)" >&2; exit 1 ;;
esac

# Resolve each slug to a path
declare -a paths=()
declare -a resolved=()
for slug in "${slugs[@]}"; do
  if [[ -d "$SKILLS_DIR_PRIMARY/$slug" ]]; then
    paths+=("$SKILLS_DIR_PRIMARY/$slug")
    resolved+=("$slug")
  elif [[ -d "$SKILLS_DIR_FALLBACK/$slug" ]]; then
    paths+=("$SKILLS_DIR_FALLBACK/$slug")
    resolved+=("$slug")
  elif [[ -d "$slug" ]]; then
    paths+=("$slug")
    resolved+=("$(basename "$slug")")
  else
    echo "WARN: skill '$slug' not found" >&2
  fi
done

if [[ ${#resolved[@]} -eq 0 ]]; then
  echo "ERROR: none of the requested skills resolved" >&2
  exit 1
fi

# Membership helper
is_in_set() {
  local needle="$1"
  for s in "${resolved[@]}"; do
    [[ "$s" == "$needle" ]] && return 0
  done
  return 1
}

# Parse depends-on from frontmatter (both inline [a, b] and YAML block - name forms)
parse_depends_on() {
  local skill_md="$1"
  [[ ! -f "$skill_md" ]] && return
  awk '
    BEGIN { in_fm = 0; in_deps_block = 0 }
    /^---[[:space:]]*$/ {
      if (in_fm == 0) { in_fm = 1; next }
      else { in_fm = 0; exit }
    }
    !in_fm { next }
    /^depends-on:[[:space:]]*\[/ {
      gsub(/^depends-on:[[:space:]]*\[/, "")
      gsub(/\].*$/, "")
      n = split($0, arr, /,/)
      for (i = 1; i <= n; i++) {
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", arr[i])
        gsub(/^"|"$|^'\''|'\''$/, "", arr[i])
        if (arr[i] != "") print arr[i]
      }
      in_deps_block = 0
      next
    }
    /^depends-on:[[:space:]]*$/ { in_deps_block = 1; next }
    in_deps_block == 1 && /^[[:space:]]*-[[:space:]]/ {
      sub(/^[[:space:]]*-[[:space:]]*/, "")
      gsub(/^"|"$|^'\''|'\''$/, "")
      sub(/[[:space:]]*#.*$/, "")
      gsub(/^[[:space:]]+|[[:space:]]+$/, "")
      if ($0 != "") print
      next
    }
    in_deps_block == 1 && /^[^[:space:]-]/ { in_deps_block = 0 }
  ' "$skill_md"
}

# Strip YAML frontmatter (between the first two "---" delimiters) so body
# extractors don't pick up depends-on entries as body refs.
md_body() {
  local f="$1"
  awk '
    BEGIN { fm_count = 0 }
    /^---[[:space:]]*$/ { fm_count++; next }
    fm_count >= 2 { print }
    fm_count == 0 { print }
  ' "$f"
}

# Parse body Skill("name", ...) calls — captures the slug regardless of topic suffix
parse_skill_calls() {
  local md="$1"
  [[ ! -f "$md" ]] && return
  md_body "$md" \
    | grep -oE 'Skill\(["'"'"'][a-z][a-z0-9_-]*' 2>/dev/null \
    | sed -E 's/^Skill\(["'"'"']//' \
    | sort -u
}

# Parse body /name slash references (e.g., `/skill-kit upgrade`, `/consolidate pr-review`).
# Requires a word boundary before the slash so paths like `org/repo` and shell
# arguments like `--dir ~/work/repo` don't match. Then strips the leading slash.
parse_slash_calls() {
  local md="$1"
  [[ ! -f "$md" ]] && return
  md_body "$md" \
    | grep -oE '(^|[[:space:]`(])/[a-z][a-z0-9_-]+' 2>/dev/null \
    | sed -E 's|.*/||' \
    | sort -u
}

# Combined body references — both Skill() and slash forms, deduplicated.
parse_body_refs() {
  {
    parse_skill_calls "$1"
    parse_slash_calls "$1"
  } | sort -u
}

# JSON-safe quote
json_quote() {
  printf '"%s"' "${1//\"/\\\"}"
}

# Build output
{
  echo "{"
  echo "  \"nodes\": ["
  first=1
  # Skill nodes
  for slug in "${resolved[@]}"; do
    if [[ $first -eq 0 ]]; then echo ","; fi
    printf '    {"id": %s, "type": "skill", "owner": null}' "$(json_quote "$slug")"
    first=0
  done
  # Topic nodes
  if [[ "$SCOPE" != "skill" ]]; then
    for i in "${!paths[@]}"; do
      p="${paths[$i]}"
      slug="${resolved[$i]}"
      for topic_md in "$p"/*.md; do
        [[ ! -f "$topic_md" ]] && continue
        base=$(basename "$topic_md" .md)
        [[ "$base" == "SKILL" || "$base" == "CHANGELOG" || "$base" == "README" ]] && continue
        echo ","
        printf '    {"id": %s, "type": "topic", "owner": %s}' \
          "$(json_quote "$slug/$base")" "$(json_quote "$slug")"
      done
    done
  fi
  echo ""
  echo "  ],"
  echo "  \"edges\": ["
  first=1
  for i in "${!paths[@]}"; do
    p="${paths[$i]}"
    slug="${resolved[$i]}"
    # Single dedup ledger covers both frontmatter and body edges so a target
    # referenced in both (e.g., consolidate → superpowers) emits once.
    emitted_keys="|"
    # depends-on edges (skill-level)
    while IFS= read -r dep; do
      [[ -z "$dep" ]] && continue
      dedup_key="$slug>$dep"
      case "$emitted_keys" in
        *"|$dedup_key|"*) continue ;;
      esac
      emitted_keys="${emitted_keys}${dedup_key}|"
      if [[ $first -eq 0 ]]; then echo ","; fi
      kind="depends-on"
      if ! is_in_set "$dep"; then kind="outside"; fi
      printf '    {"source": %s, "target": %s, "kind": %s, "source_file": %s}' \
        "$(json_quote "$slug")" "$(json_quote "$dep")" "$(json_quote "$kind")" \
        "$(json_quote "$slug/SKILL.md")"
      first=0
    done < <(parse_depends_on "$p/SKILL.md")
    # Body refs (both Skill() and slash forms) — emit at topic granularity
    # when --scope=both, aggregated at skill level when --scope=skill.
    # SKILL.md body (after frontmatter) is searched too — high-value refs
    # often live in the Topics table and Workflow sections, not just topics.
    # `emitted_keys` is inherited from the depends-on loop so duplicates across
    # frontmatter + body (e.g. consolidate → superpowers) emit only once.
    for topic_md in "$p"/*.md; do
      [[ ! -f "$topic_md" ]] && continue
      base=$(basename "$topic_md" .md)
      [[ "$base" == "CHANGELOG" || "$base" == "README" ]] && continue
      while IFS= read -r called; do
        [[ -z "$called" ]] && continue
        [[ "$called" == "$slug" ]] && continue  # self-reference
        # Filter common false positives:
        # - generic frontmatter / shell words
        # - GitHub API URL path segments matched by the `/name` slash regex
        #   (e.g., `repos/{owner}/{repo}/issues` produces a `/issues` match)
        case "$called" in
          name|description|version|metadata|user|admin|root|usr|tmp|bin|etc|opt|dev|var|home|mnt) continue ;;
          api|repos|pulls|issues|orgs|users|runs|workflows|actions|releases|comments|hooks|events|commits|branches|tags|teams|reviews) continue ;;
          bak|tmp|cache|claude|agents|ralph|omc|node_modules) continue ;;
        esac
        if [[ "$SCOPE" == "skill" ]]; then
          src_id="$slug"
        elif [[ "$base" == "SKILL" ]]; then
          src_id="$slug"
        else
          src_id="$slug/$base"
        fi
        dedup_key="$src_id>$called"
        case "$emitted_keys" in
          *"|$dedup_key|"*) continue ;;
        esac
        emitted_keys="${emitted_keys}${dedup_key}|"
        if [[ $first -eq 0 ]]; then echo ","; fi
        kind="solid"
        if ! is_in_set "$called"; then kind="outside"; fi
        printf '    {"source": %s, "target": %s, "kind": %s, "source_file": %s}' \
          "$(json_quote "$src_id")" "$(json_quote "$called")" "$(json_quote "$kind")" \
          "$(json_quote "$slug/$base.md")"
        first=0
      done < <(parse_body_refs "$topic_md")
    done
  done
  echo ""
  echo "  ]"
  echo "}"
}
