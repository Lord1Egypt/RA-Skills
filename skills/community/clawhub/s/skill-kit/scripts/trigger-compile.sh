#!/bin/bash
# trigger-compile.sh — Reads triggers declarations from SKILL.md, generates dispatcher hook scripts, and registers them in settings.json
# Usage: bash trigger-compile.sh [--dry-run] [--list]
set -euo pipefail

HOOKS_DIR="$HOME/.claude/hooks"
SETTINGS="$HOME/.claude/settings.json"
SKILLS_DIRS=("$HOME/.claude/skills")
DRY_RUN=false
LIST_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --list) LIST_ONLY=true ;;
  esac
done

# --- 1. Collect triggers fields from all SKILL.md files ---
declare -A TRIGGERS_BY_EVENT  # event -> trigger entries

scan_skills() {
  for skills_dir in "${SKILLS_DIRS[@]}"; do
    [[ -d "$skills_dir" ]] || continue
    for skill_dir in "$skills_dir"/*/; do
      local skill_file="$skill_dir/SKILL.md"
      [[ -f "$skill_file" ]] || continue

      local skill_name
      skill_name=$(basename "$skill_dir")

      # Extract triggers block from frontmatter
      local in_frontmatter=false
      local in_triggers=false
      local current_event="" current_action="" current_matcher="" current_pattern="" current_message="" current_exit_code=""

      while IFS= read -r line; do
        # frontmatter boundary
        if [[ "$line" == "---" ]]; then
          if $in_frontmatter; then
            # end of frontmatter — save last trigger
            if [[ -n "$current_event" ]]; then
              save_trigger "$skill_name" "$current_event" "$current_action" "$current_matcher" "$current_pattern" "$current_message" "$current_exit_code"
            fi
            break
          fi
          in_frontmatter=true
          continue
        fi

        $in_frontmatter || continue

        # start of triggers: block
        if [[ "$line" =~ ^triggers: ]]; then
          in_triggers=true
          continue
        fi

        $in_triggers || continue

        # new entry start (- event:)
        if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*event:[[:space:]]*(.*) ]]; then
          # save previous trigger
          if [[ -n "$current_event" ]]; then
            save_trigger "$skill_name" "$current_event" "$current_action" "$current_matcher" "$current_pattern" "$current_message" "$current_exit_code"
          fi
          current_event="${BASH_REMATCH[1]}"
          current_action="" current_matcher="" current_pattern="" current_message="" current_exit_code=""
          continue
        fi

        # other top-level key that is not triggers (unindented key: or top-level keyword)
        if [[ "$line" =~ ^[a-zA-Z_-]+: ]] && ! [[ "$line" =~ ^[[:space:]] ]]; then
          # save last trigger
          if [[ -n "$current_event" ]]; then
            save_trigger "$skill_name" "$current_event" "$current_action" "$current_matcher" "$current_pattern" "$current_message" "$current_exit_code"
          fi
          in_triggers=false
          continue
        fi

        # parse attributes
        if [[ "$line" =~ ^[[:space:]]+action:[[:space:]]*(.*) ]]; then
          current_action="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+matcher:[[:space:]]*(.*) ]]; then
          current_matcher="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+pattern:[[:space:]]*\"(.*)\" ]]; then
          current_pattern="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+pattern:[[:space:]]*(.*) ]]; then
          current_pattern="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+message:[[:space:]]*\"(.*)\" ]]; then
          current_message="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+message:[[:space:]]*(.*) ]]; then
          current_message="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]+exit_code_filter:[[:space:]]*(.*) ]]; then
          current_exit_code="${BASH_REMATCH[1]}"
        fi

      done < "$skill_file"
    done
  done
}

save_trigger() {
  local skill="$1" event="$2" action="$3" matcher="$4" pattern="$5" message="$6" exit_code="$7"
  local entry="$skill|$action|$matcher|$pattern|$message|$exit_code"
  # prevent duplicates
  local existing="${TRIGGERS_BY_EVENT[$event]:-}"
  if [[ "$existing" == *"$entry"* ]]; then
    return
  fi
  TRIGGERS_BY_EVENT[$event]="${existing}${existing:+$'\n'}$entry"
}

# --- 2. Print trigger list ---
list_triggers() {
  echo "=== Registered Triggers ==="
  echo ""
  for event in "${!TRIGGERS_BY_EVENT[@]}"; do
    echo "[$event]"
    while IFS='|' read -r skill action matcher pattern message exit_code; do
      [[ -z "$skill" ]] && continue
      printf "  %-20s action=%-8s" "$skill" "$action"
      [[ -n "$matcher" ]] && printf " matcher=%s" "$matcher"
      [[ -n "$pattern" ]] && printf " pattern=\"%s\"" "$pattern"
      echo ""
    done <<< "${TRIGGERS_BY_EVENT[$event]}"
    echo ""
  done
}

# --- 3. Generate dispatcher scripts ---
generate_dispatcher() {
  local event="$1"
  local entries="${TRIGGERS_BY_EVENT[$event]}"
  local output_file="$HOOKS_DIR/trigger-${event}.sh"
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  local script="#!/bin/bash
# AUTO-GENERATED by skill-toolkit trigger compiler
# DO NOT EDIT — regenerate with: /skill-toolkit trigger compile
# Generated: $timestamp

INPUT=\$(cat)
TOOL_NAME=\$(echo \"\$INPUT\" | jq -r '.tool_name // empty' 2>/dev/null)
COMMAND=\$(echo \"\$INPUT\" | jq -r '.tool_input.command // empty' 2>/dev/null)
EXIT_CODE=\"\${EXIT_CODE:-0}\"
"

  while IFS='|' read -r skill action matcher pattern message exit_code_filter; do
    [[ -z "$skill" ]] && continue

    local condition_start="" condition_end=""

    # build matcher/pattern condition
    if [[ -n "$matcher" ]] || [[ -n "$pattern" ]] || [[ -n "$exit_code_filter" ]]; then
      local conditions=()
      [[ -n "$matcher" ]] && conditions+=("[[ \"\$TOOL_NAME\" == \"$matcher\" ]]")
      [[ -n "$pattern" ]] && conditions+=("echo \"\$COMMAND\" | grep -qE \"$pattern\"")
      [[ -n "$exit_code_filter" ]] && conditions+=("[[ \"\$EXIT_CODE\" == \"$exit_code_filter\" ]]")

      condition_start="if ${conditions[0]}"
      for ((i=1; i<${#conditions[@]}; i++)); do
        condition_start="$condition_start && ${conditions[$i]}"
      done
      condition_start="$condition_start; then"
      condition_end="fi"
    fi

    script+="
### $skill ($event, action=$action) ###
"
    [[ -n "$condition_start" ]] && script+="$condition_start
"

    case "$action" in
      suggest)
        script+="echo '<skill-trigger name=\"$skill\">'
echo '$message'
echo 'Call the Skill(\"$skill\") tool.'
echo '</skill-trigger>'
"
        ;;
      block)
        script+="echo '$message'
exit 1
"
        ;;
      inject)
        script+="# prevent infinite loop: block only once per session
FIRE_FLAG=\"\$HOME/.claude/data/trigger-stop-${skill}\"
if [[ -f \"\$FIRE_FLAG\" ]]; then
  exit 0
fi
mkdir -p \"\$HOME/.claude/data\"
touch \"\$FIRE_FLAG\"
jq -n '{
  \"decision\": \"block\",
  \"reason\": \"$skill trigger\",
  \"systemMessage\": \"$message\"
}'
"
        ;;
    esac

    [[ -n "$condition_end" ]] && script+="$condition_end
"
  done <<< "$entries"

  if $DRY_RUN; then
    echo "=== Would generate: $output_file ==="
    echo "$script"
    echo ""
  else
    echo "$script" > "$output_file"
    chmod +x "$output_file"
    echo "Generated: $output_file"
  fi
}

# --- 4. Register hooks in settings.json ---
register_hooks() {
  if $DRY_RUN; then
    echo "=== Would register in settings.json ==="
  fi

  local tmp_settings
  tmp_settings=$(mktemp)
  cp "$SETTINGS" "$tmp_settings"

  for event in "${!TRIGGERS_BY_EVENT[@]}"; do
    local hook_cmd="bash ~/.claude/hooks/trigger-${event}.sh"
    local matcher=""

    # collect matchers for PostToolUse/PreToolUse
    if [[ "$event" == "PostToolUse" ]] || [[ "$event" == "PreToolUse" ]]; then
      local matchers=()
      while IFS='|' read -r skill action m pattern message exit_code; do
        [[ -n "$m" ]] && matchers+=("$m")
      done <<< "${TRIGGERS_BY_EVENT[$event]}"

      # unique matchers
      if [[ ${#matchers[@]} -gt 0 ]]; then
        matcher=$(printf '%s\n' "${matchers[@]}" | sort -u | paste -sd '|')
      fi
    fi

    if $DRY_RUN; then
      echo "  Event: $event"
      echo "  Command: $hook_cmd"
      [[ -n "$matcher" ]] && echo "  Matcher: $matcher"
      echo ""
    else
      # remove existing trigger- prefixed hooks, then re-add
      local hook_entry
      if [[ -n "$matcher" ]]; then
        hook_entry=$(jq -n --arg cmd "$hook_cmd" --arg m "$matcher" '{
          matcher: $m,
          hooks: [{ type: "command", command: $cmd, timeout: 10 }]
        }')
      else
        hook_entry=$(jq -n --arg cmd "$hook_cmd" '{
          hooks: [{ type: "command", command: $cmd, timeout: 10 }]
        }')
      fi

      # remove existing trigger- hooks + add new entry
      jq --arg event "$event" --arg cmd "$hook_cmd" --argjson entry "$hook_entry" '
        .hooks[$event] = (
          (.hooks[$event] // [])
          | map(select(.hooks[0].command | test("trigger-") | not))
          | . + [$entry]
        )
      ' "$tmp_settings" > "${tmp_settings}.new"
      mv "${tmp_settings}.new" "$tmp_settings"

      echo "Registered: $event → $hook_cmd"
    fi
  done

  if ! $DRY_RUN; then
    cp "$tmp_settings" "$SETTINGS"
    echo ""
    echo "settings.json updated."
  fi
  rm -f "$tmp_settings"
}

# --- Main ---
mkdir -p "$HOOKS_DIR"
scan_skills

if [[ ${#TRIGGERS_BY_EVENT[@]} -eq 0 ]]; then
  echo "No triggers found in any SKILL.md."
  exit 0
fi

if $LIST_ONLY; then
  list_triggers
  exit 0
fi

echo "Found triggers in ${#TRIGGERS_BY_EVENT[@]} event(s):"
list_triggers

for event in "${!TRIGGERS_BY_EVENT[@]}"; do
  generate_dispatcher "$event"
done

register_hooks

# --- 5. Verify generated scripts ---
echo ""
echo "=== Verification ==="
errors=0
for event in "${!TRIGGERS_BY_EVENT[@]}"; do
  script_file="$HOOKS_DIR/trigger-${event}.sh"
  if bash -n "$script_file" 2>/dev/null; then
    echo "  ✓ trigger-${event}.sh syntax OK"
  else
    echo "  ✗ trigger-${event}.sh syntax ERROR:"
    bash -n "$script_file" 2>&1 | head -5
    errors=$((errors + 1))
  fi
done

if jq . "$SETTINGS" > /dev/null 2>&1; then
  echo "  ✓ settings.json valid JSON"
else
  echo "  ✗ settings.json invalid JSON!"
  errors=$((errors + 1))
fi

if [[ $errors -gt 0 ]]; then
  echo ""
  echo "ERROR: $errors verification failure(s). Fix before restarting Claude Code."
  exit 1
fi

echo ""
echo "Done. Restart Claude Code to apply."
