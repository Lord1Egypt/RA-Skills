#!/usr/bin/env bash
# SupStack API Helper — OpenClaw Skill
# Wraps the SupStack REST API for clean agent invocation
#
# Usage: bash scripts/supstack.sh <command> [args]

set -euo pipefail

API="https://supstack.me/api/v1"

# State directory for research monitor persistence
STATE_DIR="${SUPSTACK_STATE_DIR:-$HOME/.openclaw/workspace/supstack}"
mkdir -p "$STATE_DIR" 2>/dev/null || true

# Fetch helper — returns JSON, handles errors
fetch() {
  local url="$1"
  local response
  response=$(curl -sf --max-time 15 "$url" 2>/dev/null) || {
    echo '{"error":"API request failed or timed out. URL: '"$url"'"}'
    return 1
  }
  echo "$response"
}

# Compact JSON output (relevant fields only, not the full payload)
cmd="${1:-help}"
shift || true

case "$cmd" in

  # ──────────────────────────────────────────────
  # ONBOARDING — First run check
  # ──────────────────────────────────────────────
  welcome)
    force=false
    for arg in "$@"; do
      [ "$arg" = "--force" ] && force=true
    done

    onboarded_file="$STATE_DIR/onboarded"

    if [ "$force" = true ]; then
      # Forced intro — fetch live stats for a fresh welcome
      stats=$(fetch "$API/categories" 2>/dev/null | jq '{
        totalSupplements: .meta.totalSupplements,
        totalGoals: .meta.totalGoals,
        evidenceDistribution: .data.evidenceDistribution
      }' 2>/dev/null) || stats='{"totalSupplements": 218, "totalGoals": 15}'
      echo "$stats" | jq '. + {firstRun: false, forced: true}'
    elif [ -f "$onboarded_file" ]; then
      echo '{"firstRun": false}'
    else
      # First run — mark as onboarded and fetch stats
      touch "$onboarded_file"
      stats=$(fetch "$API/categories" 2>/dev/null | jq '{
        totalSupplements: .meta.totalSupplements,
        totalGoals: .meta.totalGoals,
        categories: [.data.categories[].name],
        types: [.data.types[].name]
      }' 2>/dev/null) || stats='{"totalSupplements": 218, "totalGoals": 15}'
      echo "$stats" | jq '. + {firstRun: true}'
    fi
    ;;

  # ──────────────────────────────────────────────
  # Full supplement info
  # ──────────────────────────────────────────────
  info)
    slug="${1:?Usage: supstack.sh info <slug>}"
    fetch "$API/supplements/$slug" | jq --arg slug "$slug" '{
      data: {
        id: .data.id,
        name: .data.name,
        fullName: .data.fullName,
        type: .data.type,
        shortDescription: .data.shortDescription,
        longDescription: .data.longDescription,
        evidence: .data.evidence,
        dosage: .data.dosage,
        safety: .data.safety,
        goals: .data.goals,
        mechanisms: .data.mechanisms,
        effects: .data.effects,
        synergies: .data.synergies,
        timing: .data.timing,
        form: .data.form,
        duration: .data.duration,
        cycling: .data.cycling,
        recentStudies: [.data.recentStudies[]? | {title, study_type, year, key_finding, sample_size}],
        pageUrl: ("https://supstack.me/supplements/" + $slug)
      }
    }'
    ;;

  # ──────────────────────────────────────────────
  # Search (full-text with additive scoring)
  # ──────────────────────────────────────────────
  search)
    query="${1:?Usage: supstack.sh search <query>}"
    fetch "$API/search?q=$(printf '%s' "$query" | jq -sRr @uri)&limit=8" | jq '.data[] | {slug, name, evidence: .evidence.score, matchType, pageUrl: ("https://supstack.me/supplements/" + .slug)}'
    ;;

  # ──────────────────────────────────────────────
  # Dosing protocol
  # ──────────────────────────────────────────────
  protocol)
    slug="${1:?Usage: supstack.sh protocol <slug>}"
    fetch "$API/supplements/$slug/protocol" | jq '.data'
    ;;

  # ──────────────────────────────────────────────
  # Goal-based matching
  # ──────────────────────────────────────────────
  match)
    goal1="${1:?Usage: supstack.sh match <goal1> [goal2] [goal3] [limit]}"
    goal2="${2:-}"
    goal3="${3:-}"
    limit="${4:-5}"
    goals="$goal1"
    [ -n "$goal2" ] && goals="$goals,$goal2"
    [ -n "$goal3" ] && goals="$goals,$goal3"
    fetch "$API/match?goals=$goals&limit=$limit" | jq '.data[] | {
      supplement: .supplement.name,
      slug: .supplement.slug,
      evidence: .supplement.evidence.score,
      safety: .supplement.safety.overallRating,
      matchScore,
      goals: [.goalBreakdown[] | {goal: .goalId, relevance: .relevanceScore, improvement: .expectedImprovement, timeline: .timeToEffect}],
      pageUrl: ("https://supstack.me/supplements/" + .supplement.slug)
    }'
    ;;

  # ──────────────────────────────────────────────
  # Smart recommendations (stack-aware)
  # ──────────────────────────────────────────────
  recommend)
    # Parse --goals=X,Y and --stack=A,B flags
    goals="" stack="" limit="5"
    for arg in "$@"; do
      case "$arg" in
        --goals=*) goals="${arg#--goals=}" ;;
        --stack=*) stack="${arg#--stack=}" ;;
        [0-9]*) limit="$arg" ;;
      esac
    done
    if [ -z "$goals" ] && [ -z "$stack" ]; then
      echo "Usage: supstack.sh recommend [--goals=g1,g2] [--stack=s1,s2] [limit]"
      echo "At least one of --goals or --stack is required."
      exit 1
    fi
    url="$API/recommend?limit=$limit"
    [ -n "$goals" ] && url="$url&goals=$goals"
    [ -n "$stack" ] && url="$url&stack=$stack"
    fetch "$url" | jq '{
      recommendations: [.data.recommendations[]? | {
        supplement: .supplement.name,
        slug: .supplement.slug,
        evidence: .supplement.evidence.score,
        safety: .supplement.safety.overallRating,
        dosage: .supplement.dosage.recommended,
        compositeScore: .scores.composite,
        scores: .scores,
        stackSynergies: .stackSynergies,
        warnings: .warnings,
        pageUrl: ("https://supstack.me/supplements/" + .supplement.slug)
      }],
      gapAnalysis: .data.gapAnalysis
    }'
    ;;

  # ──────────────────────────────────────────────
  # Safety profile
  # ──────────────────────────────────────────────
  safety)
    slug="${1:?Usage: supstack.sh safety <slug>}"
    fetch "$API/safety?supplement=$slug" | jq --arg slug "$slug" '.data + {pageUrl: ("https://supstack.me/supplements/" + $slug)}'
    ;;

  # ──────────────────────────────────────────────
  # Drug interactions (single supplement)
  # ──────────────────────────────────────────────
  interactions)
    slug="${1:?Usage: supstack.sh interactions <slug> [medication]}"
    medication="${2:-}"
    url="$API/interactions?supplement=$slug"
    [ -n "$medication" ] && url="$url&medication=$(printf '%s' "$medication" | jq -sRr @uri)"
    fetch "$url" | jq '.data'
    ;;

  # ──────────────────────────────────────────────
  # Supplement-supplement interactions
  # ──────────────────────────────────────────────
  interactions-multi)
    if [ $# -lt 2 ]; then
      echo "Usage: supstack.sh interactions-multi <slug1> <slug2> [slug3...]"
      exit 1
    fi
    slugs=$(IFS=,; echo "$*")
    fetch "$API/interactions?supplements=$slugs" | jq '.data'
    ;;

  # ──────────────────────────────────────────────
  # Synergies (single supplement)
  # ──────────────────────────────────────────────
  synergies)
    slug="${1:?Usage: supstack.sh synergies <slug>}"
    fetch "$API/synergies?supplement=$slug" | jq '.data'
    ;;

  # ──────────────────────────────────────────────
  # Synergies between specific supplements
  # ──────────────────────────────────────────────
  synergies-multi)
    if [ $# -lt 2 ]; then
      echo "Usage: supstack.sh synergies-multi <slug1> <slug2> [slug3...]"
      exit 1
    fi
    slugs=$(IFS=,; echo "$*")
    fetch "$API/synergies?supplements=$slugs" | jq '.data'
    ;;

  # ──────────────────────────────────────────────
  # Research studies
  # ──────────────────────────────────────────────
  studies)
    url="$API/studies?pageSize=5"
    for arg in "$@"; do
      case "$arg" in
        --supplement=*) url="$url&supplement=${arg#--supplement=}" ;;
        --type=*) url="$url&type=${arg#--type=}" ;;
        --q=*) url="$url&q=$(printf '%s' "${arg#--q=}" | jq -sRr @uri)" ;;
      esac
    done
    fetch "$url" | jq '.data[] | {title, supplement_name, study_type, year, key_finding, sample_size}'
    ;;

  # ──────────────────────────────────────────────
  # RESEARCH MONITOR — Setup tracking
  # ──────────────────────────────────────────────
  monitor-setup)
    if [ $# -lt 1 ]; then
      echo "Usage: supstack.sh monitor-setup <slug1,slug2,...> [--frequency=weekly|biweekly|monthly]"
      exit 1
    fi
    slugs="$1"
    frequency="weekly"
    for arg in "${@:2}"; do
      case "$arg" in
        --frequency=*) frequency="${arg#--frequency=}" ;;
      esac
    done

    # Validate each slug exists in the API
    IFS=',' read -ra SUPP_ARRAY <<< "$slugs"
    valid_slugs=()
    for slug in "${SUPP_ARRAY[@]}"; do
      slug=$(echo "$slug" | xargs) # trim whitespace
      result=$(fetch "$API/search?q=$slug&limit=1" 2>/dev/null | jq -r '.data[0].slug // empty' 2>/dev/null) || true
      if [ -n "$result" ]; then
        valid_slugs+=("$slug")
      else
        echo "WARNING: '$slug' not found in database — skipping"
      fi
    done

    if [ ${#valid_slugs[@]} -eq 0 ]; then
      echo "ERROR: No valid supplements found. Check slugs with: supstack.sh search <name>"
      exit 1
    fi

    # Build monitor state
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    valid_csv=$(IFS=,; echo "${valid_slugs[*]}")

    jq -n \
      --arg slugs "$valid_csv" \
      --arg freq "$frequency" \
      --arg now "$now" \
      '{
        supplements: ($slugs | split(",")),
        frequency: $freq,
        createdAt: $now,
        lastChecked: null,
        seenStudyIds: {}
      }' > "$STATE_DIR/monitor.json"

    echo "Research Monitor configured:"
    jq '{
      tracking: .supplements,
      frequency: .frequency,
      supplementCount: (.supplements | length)
    }' "$STATE_DIR/monitor.json"
    ;;

  # ──────────────────────────────────────────────
  # RESEARCH MONITOR — Check for new studies
  # ──────────────────────────────────────────────
  monitor-check)
    if [ ! -f "$STATE_DIR/monitor.json" ]; then
      echo '{"error": "Research Monitor not configured. Run: supstack.sh monitor-setup <slug1,slug2,...>"}'
      exit 1
    fi

    state=$(cat "$STATE_DIR/monitor.json")
    supplements=$(echo "$state" | jq -r '.supplements[]')
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    all_new_studies="[]"
    updated_seen="{}"

    # Load existing seen IDs
    existing_seen=$(echo "$state" | jq '.seenStudyIds')

    for slug in $supplements; do
      # Fetch newest studies for this supplement
      response=$(fetch "$API/studies?supplement=$slug&sort=newest&pageSize=10" 2>/dev/null) || continue

      # Get study IDs we've already seen for this supplement
      seen_ids=$(echo "$existing_seen" | jq -r --arg s "$slug" '.[$s] // [] | .[]')

      # Filter to only new studies (output as array)
      new_for_slug=$(echo "$response" | jq --arg slug "$slug" --arg seen "$seen_ids" '
        ($seen | split("\n") | map(select(. != ""))) as $seen_list |
        [.data[]? | select(.id as $id | $seen_list | index($id) | not)] |
        map({
          id,
          title,
          supplement: $slug,
          supplement_name: .supplement_name,
          study_type: .study_type,
          year,
          source,
          key_finding,
          sample_size
        })
      ' 2>/dev/null) || continue

      # Collect new studies
      if [ -n "$new_for_slug" ] && [ "$new_for_slug" != "[]" ]; then
        all_new_studies=$(echo "$all_new_studies" | jq --argjson new "$new_for_slug" '. + $new')
      fi

      # Update seen IDs (all current IDs for this supplement)
      current_ids=$(echo "$response" | jq --arg s "$slug" '[.data[]?.id]')
      prev_ids=$(echo "$existing_seen" | jq --arg s "$slug" '.[$s] // []')
      merged_ids=$(echo "[$prev_ids, $current_ids]" | jq '.[0] + .[1] | unique | .[:50]')
      updated_seen=$(echo "$updated_seen" | jq --arg s "$slug" --argjson ids "$merged_ids" '. + {($s): $ids}')
    done

    # Update state file
    echo "$state" | jq \
      --arg now "$now" \
      --argjson seen "$updated_seen" \
      '.lastChecked = $now | .seenStudyIds = $seen' \
      > "$STATE_DIR/monitor.json"

    # Count new studies
    new_count=$(echo "$all_new_studies" | jq 'length')

    # Output result
    jq -n \
      --argjson studies "$all_new_studies" \
      --argjson count "$new_count" \
      --arg checked "$now" \
      --argjson tracked "$(echo "$state" | jq '.supplements')" \
      '{
        newStudies: $studies,
        summary: {
          newStudyCount: $count,
          supplementsChecked: ($tracked | length),
          supplements: $tracked,
          checkedAt: $checked
        }
      }'
    ;;

  # ──────────────────────────────────────────────
  # RESEARCH MONITOR — Status
  # ──────────────────────────────────────────────
  monitor-status)
    if [ ! -f "$STATE_DIR/monitor.json" ]; then
      echo '{"status": "not configured", "hint": "Run: supstack.sh monitor-setup <slug1,slug2,...>"}'
      exit 0
    fi
    jq '{
      status: "active",
      tracking: .supplements,
      frequency: .frequency,
      lastChecked: .lastChecked,
      supplementCount: (.supplements | length),
      seenStudyCounts: (.seenStudyIds | to_entries | map({key, count: (.value | length)}) | from_entries)
    }' "$STATE_DIR/monitor.json"
    ;;

  # ──────────────────────────────────────────────
  # RESEARCH MONITOR — Add supplements to tracking
  # ──────────────────────────────────────────────
  monitor-add)
    slug="${1:?Usage: supstack.sh monitor-add <slug>}"
    if [ ! -f "$STATE_DIR/monitor.json" ]; then
      echo "Monitor not configured. Run monitor-setup first."
      exit 1
    fi
    jq --arg s "$slug" '.supplements = (.supplements + [$s] | unique)' \
      "$STATE_DIR/monitor.json" > "$STATE_DIR/monitor.json.tmp" \
      && mv "$STATE_DIR/monitor.json.tmp" "$STATE_DIR/monitor.json"
    echo "Added '$slug'. Now tracking:"
    jq '.supplements' "$STATE_DIR/monitor.json"
    ;;

  # ──────────────────────────────────────────────
  # RESEARCH MONITOR — Remove supplement from tracking
  # ──────────────────────────────────────────────
  monitor-remove)
    slug="${1:?Usage: supstack.sh monitor-remove <slug>}"
    if [ ! -f "$STATE_DIR/monitor.json" ]; then
      echo "Monitor not configured."
      exit 1
    fi
    jq --arg s "$slug" '.supplements = [.supplements[] | select(. != $s)]' \
      "$STATE_DIR/monitor.json" > "$STATE_DIR/monitor.json.tmp" \
      && mv "$STATE_DIR/monitor.json.tmp" "$STATE_DIR/monitor.json"
    echo "Removed '$slug'. Now tracking:"
    jq '.supplements' "$STATE_DIR/monitor.json"
    ;;

  # ──────────────────────────────────────────────
  # RESEARCH MONITOR — Stop and clear all tracking
  # ──────────────────────────────────────────────
  monitor-clear)
    rm -f "$STATE_DIR/monitor.json"
    echo '{"status": "cleared", "message": "Research Monitor stopped and all tracking data removed."}'
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Read the full profile
  # ──────────────────────────────────────────────
  profile)
    profile_file="$STATE_DIR/profile.md"
    if [ ! -f "$profile_file" ]; then
      # Initialize from template
      script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
      template="$script_dir/../templates/profile.md"
      if [ -f "$template" ]; then
        cp "$template" "$profile_file"
      else
        echo "# SupStack User Profile" > "$profile_file"
        echo "" >> "$profile_file"
        echo "No data yet." >> "$profile_file"
      fi
    fi
    cat "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Update a section
  # ──────────────────────────────────────────────
  profile-update)
    section="${1:?Usage: supstack.sh profile-update <section> <content>}"
    shift
    content="$*"
    if [ -z "$content" ]; then
      echo "Usage: supstack.sh profile-update <section> <content>"
      echo "Sections: stack, medications, goals, conditions, allergies, trials, interests, history, preferences, profile, notes"
      exit 1
    fi

    profile_file="$STATE_DIR/profile.md"

    # Initialize profile if it doesn't exist
    if [ ! -f "$profile_file" ]; then
      script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
      template="$script_dir/../templates/profile.md"
      if [ -f "$template" ]; then
        cp "$template" "$profile_file"
      else
        echo "# SupStack User Profile" > "$profile_file"
      fi
    fi

    # Map short section names to markdown headings
    case "$section" in
      stack)        heading="Current Stack" ;;
      medications|meds) heading="Medications" ;;
      goals)        heading="Health Goals" ;;
      conditions)   heading="Health Conditions" ;;
      allergies)    heading="Allergies & Intolerances" ;;
      trials)       heading="Past Trials" ;;
      interests)    heading="Interests" ;;
      history)      heading="Search History" ;;
      preferences|prefs) heading="Preferences" ;;
      profile|info) heading="Profile" ;;
      notes)        heading="Notes" ;;
      *)
        echo "Unknown section: $section"
        echo "Valid: stack, medications, goals, conditions, allergies, trials, interests, history, preferences, profile, notes"
        exit 1
        ;;
    esac

    # Use python for reliable markdown section replacement
    python3 -c "
import re, sys

heading = sys.argv[1]
new_content = sys.argv[2]
filepath = sys.argv[3]

with open(filepath, 'r') as f:
    text = f.read()

# Pattern: ## Heading\n...until next ## or EOF
pattern = r'(## ' + re.escape(heading) + r'\n)(?:(?!## ).)*'

if re.search(pattern, text, re.DOTALL):
    text = re.sub(pattern, lambda m: m.group(1) + new_content + '\n\n', text, flags=re.DOTALL)
else:
    # Section doesn't exist, append it
    text = text.rstrip() + '\n\n## ' + heading + '\n' + new_content + '\n'

with open(filepath, 'w') as f:
    f.write(text)

print('Updated: ' + heading)
" "$heading" "$content" "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Add a line to a section
  # ──────────────────────────────────────────────
  profile-add)
    section="${1:?Usage: supstack.sh profile-add <section> <line>}"
    shift
    line="$*"
    if [ -z "$line" ]; then
      echo "Usage: supstack.sh profile-add <section> <line>"
      exit 1
    fi

    profile_file="$STATE_DIR/profile.md"

    # Initialize if needed
    if [ ! -f "$profile_file" ]; then
      bash "${BASH_SOURCE[0]}" profile > /dev/null
    fi

    case "$section" in
      stack)        heading="Current Stack" ;;
      medications|meds) heading="Medications" ;;
      goals)        heading="Health Goals" ;;
      conditions)   heading="Health Conditions" ;;
      allergies)    heading="Allergies & Intolerances" ;;
      trials)       heading="Past Trials" ;;
      interests)    heading="Interests" ;;
      history)      heading="Search History" ;;
      preferences|prefs) heading="Preferences" ;;
      profile|info) heading="Profile" ;;
      notes)        heading="Notes" ;;
      *)            echo "Unknown section: $section"; exit 1 ;;
    esac

    python3 -c "
import re, sys

heading = sys.argv[1]
new_line = sys.argv[2]
filepath = sys.argv[3]

with open(filepath, 'r') as f:
    text = f.read()

# Find the section and append before the next section or EOF
pattern = r'(## ' + re.escape(heading) + r'\n(?:(?!## ).)*)'
match = re.search(pattern, text, re.DOTALL)

if match:
    section_content = match.group(1)
    # Remove HTML comments (template placeholders)
    cleaned = re.sub(r'<!--.*?-->\n?', '', section_content)
    insert_pos = match.end()
    # Add the new line at the end of the section
    text = text[:insert_pos] + '- ' + new_line + '\n' + text[insert_pos:]
else:
    text = text.rstrip() + '\n\n## ' + heading + '\n- ' + new_line + '\n'

with open(filepath, 'w') as f:
    f.write(text)

print('Added to ' + heading + ': ' + new_line)
" "$heading" "$line" "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Get a specific section
  # ──────────────────────────────────────────────
  profile-get)
    section="${1:?Usage: supstack.sh profile-get <section>}"
    profile_file="$STATE_DIR/profile.md"

    if [ ! -f "$profile_file" ]; then
      echo "No profile yet."
      exit 0
    fi

    case "$section" in
      stack)        heading="Current Stack" ;;
      medications|meds) heading="Medications" ;;
      goals)        heading="Health Goals" ;;
      conditions)   heading="Health Conditions" ;;
      allergies)    heading="Allergies & Intolerances" ;;
      trials)       heading="Past Trials" ;;
      interests)    heading="Interests" ;;
      history)      heading="Search History" ;;
      preferences|prefs) heading="Preferences" ;;
      profile|info) heading="Profile" ;;
      notes)        heading="Notes" ;;
      *)            echo "Unknown section: $section"; exit 1 ;;
    esac

    python3 -c "
import re, sys

heading = sys.argv[1]
filepath = sys.argv[2]

with open(filepath, 'r') as f:
    text = f.read()

pattern = r'## ' + re.escape(heading) + r'\n((?:(?!## ).)*)'
match = re.search(pattern, text, re.DOTALL)

if match:
    content = match.group(1).strip()
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content).strip()
    if content:
        print(content)
    else:
        print('(empty)')
else:
    print('(section not found)')
" "$heading" "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Get stack as comma-separated slugs (for API calls)
  # ──────────────────────────────────────────────
  profile-stack-slugs)
    profile_file="$STATE_DIR/profile.md"
    if [ ! -f "$profile_file" ]; then
      echo ""
      exit 0
    fi

    python3 -c "
import re, sys

filepath = sys.argv[1]

with open(filepath, 'r') as f:
    text = f.read()

pattern = r'## Current Stack\n((?:(?!## ).)*)'
match = re.search(pattern, text, re.DOTALL)

if match:
    content = match.group(1)
    content = re.sub(r'<!--.*?-->', '', content)
    # Extract slugs (first field before |)
    slugs = []
    for line in content.strip().split('\n'):
        line = line.strip().lstrip('- ')
        if '|' in line:
            slug = line.split('|')[0].strip()
            if slug:
                slugs.append(slug)
    print(','.join(slugs))
" "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Get medications as list (for interaction checks)
  # ──────────────────────────────────────────────
  profile-medications)
    profile_file="$STATE_DIR/profile.md"
    if [ ! -f "$profile_file" ]; then
      echo "[]"
      exit 0
    fi

    python3 -c "
import re, sys, json

filepath = sys.argv[1]

with open(filepath, 'r') as f:
    text = f.read()

pattern = r'## Medications\n((?:(?!## ).)*)'
match = re.search(pattern, text, re.DOTALL)

meds = []
if match:
    content = match.group(1)
    content = re.sub(r'<!--.*?-->', '', content)
    for line in content.strip().split('\n'):
        line = line.strip().lstrip('- ')
        if line and '|' in line:
            med_name = line.split('|')[0].strip()
            if med_name:
                meds.append(med_name)
        elif line:
            meds.append(line)

print(json.dumps(meds))
" "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Log interest in a supplement
  # ──────────────────────────────────────────────
  profile-log-interest)
    slug="${1:?Usage: supstack.sh profile-log-interest <slug> [context]}"
    shift
    context="${*:-}"
    profile_file="$STATE_DIR/profile.md"
    month=$(date +"%Y-%m")

    # Initialize if needed
    if [ ! -f "$profile_file" ]; then
      bash "${BASH_SOURCE[0]}" profile > /dev/null
    fi

    python3 -c "
import re, sys

slug = sys.argv[1]
context = sys.argv[2] if len(sys.argv) > 2 else ''
month = sys.argv[3]
filepath = sys.argv[4]

with open(filepath, 'r') as f:
    text = f.read()

# Find Interests section
pattern = r'(## Interests\n)((?:(?!## ).)*)'
match = re.search(pattern, text, re.DOTALL)

if match:
    section_header = match.group(1)
    section_body = match.group(2)
    # Remove comments
    clean_body = re.sub(r'<!--.*?-->\n?', '', section_body)

    # Check if this slug already exists
    lines = [l for l in clean_body.strip().split('\n') if l.strip().startswith('- ')]
    found = False
    new_lines = []
    for line in lines:
        parts = line.lstrip('- ').split(' | ')
        if len(parts) >= 3 and parts[0].strip() == slug:
            # Increment count, update date
            count = int(parts[2].strip()) + 1
            # Preserve name, update count, month, append context
            old_ctx = parts[4].strip() if len(parts) > 4 else ''
            new_ctx = (old_ctx + '; ' + context).strip('; ') if context else old_ctx
            new_lines.append(f'- {parts[0].strip()} | {parts[1].strip()} | {count} | {month} | {new_ctx}')
            found = True
            print(f'Updated interest: {slug} (query #{count})')
        else:
            new_lines.append(line)

    if not found:
        # New interest — need to look up name
        name = slug.replace('-', ' ').title()
        new_lines.append(f'- {slug} | {name} | 1 | {month} | {context}')
        print(f'New interest logged: {slug}')

    new_section = section_header + '\n'.join(new_lines) + '\n\n'
    text = text[:match.start()] + new_section + text[match.end():]
else:
    # No section yet, create it
    name = slug.replace('-', ' ').title()
    text = text.rstrip() + f'\n\n## Interests\n- {slug} | {name} | 1 | {month} | {context}\n'
    print(f'New interest logged: {slug}')

with open(filepath, 'w') as f:
    f.write(text)
" "$slug" "$context" "$month" "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Log a search/query
  # ──────────────────────────────────────────────
  profile-log-search)
    query_type="${1:?Usage: supstack.sh profile-log-search <type> <subject> [context]}"
    subject="${2:?Usage: supstack.sh profile-log-search <type> <subject> [context]}"
    shift 2
    context="${*:-}"
    profile_file="$STATE_DIR/profile.md"
    today=$(date +"%Y-%m-%d")

    # Initialize if needed
    if [ ! -f "$profile_file" ]; then
      bash "${BASH_SOURCE[0]}" profile > /dev/null
    fi

    # Append to Search History, keep only last 30 entries
    python3 -c "
import re, sys

qtype = sys.argv[1]
subject = sys.argv[2]
context = sys.argv[3] if len(sys.argv) > 3 else ''
today = sys.argv[4]
filepath = sys.argv[5]

with open(filepath, 'r') as f:
    text = f.read()

new_line = f'- {today} | {qtype} | {subject} | {context}'

pattern = r'(## Search History\n)((?:(?!## ).)*)'
match = re.search(pattern, text, re.DOTALL)

if match:
    section_header = match.group(1)
    section_body = match.group(2)
    clean_body = re.sub(r'<!--.*?-->\n?', '', section_body)
    lines = [l for l in clean_body.strip().split('\n') if l.strip().startswith('- ')]
    lines.append(new_line)
    # Keep last 30
    lines = lines[-30:]
    new_section = section_header + '\n'.join(lines) + '\n\n'
    text = text[:match.start()] + new_section + text[match.end():]
else:
    text = text.rstrip() + f'\n\n## Search History\n{new_line}\n'

with open(filepath, 'w') as f:
    f.write(text)

print(f'Logged: {qtype} | {subject}')
" "$query_type" "$subject" "$context" "$today" "$profile_file"
    ;;

  # ──────────────────────────────────────────────
  # USER PROFILE — Get interests (supplements researched but not taking)
  # ──────────────────────────────────────────────
  profile-interests)
    profile_file="$STATE_DIR/profile.md"
    if [ ! -f "$profile_file" ]; then
      echo "[]"
      exit 0
    fi

    python3 -c "
import re, sys, json

filepath = sys.argv[1]

with open(filepath, 'r') as f:
    text = f.read()

pattern = r'## Interests\n((?:(?!## ).)*)'
match = re.search(pattern, text, re.DOTALL)

interests = []
if match:
    content = match.group(1)
    content = re.sub(r'<!--.*?-->', '', content)
    for line in content.strip().split('\n'):
        line = line.strip().lstrip('- ')
        if not line:
            continue
        parts = [p.strip() for p in line.split('|')]
        entry = {'slug': parts[0] if len(parts) > 0 else ''}
        entry['name'] = parts[1] if len(parts) > 1 else ''
        entry['queryCount'] = int(parts[2]) if len(parts) > 2 else 1
        entry['lastAsked'] = parts[3] if len(parts) > 3 else ''
        entry['context'] = parts[4] if len(parts) > 4 else ''
        if entry['slug']:
            interests.append(entry)

# Sort by query count descending
interests.sort(key=lambda x: x['queryCount'], reverse=True)
print(json.dumps(interests, indent=2))
" "$profile_file"
    ;;

  # ══════════════════════════════════════════════
  # N-OF-1 EXPERIMENT TRACKER
  # ══════════════════════════════════════════════

  # ──────────────────────────────────────────────
  # EXPERIMENT — Start a new experiment
  # ──────────────────────────────────────────────
  experiment-start)
    slug="${1:?Usage: supstack.sh experiment-start <slug> <goal>}"
    goal="${2:?Usage: supstack.sh experiment-start <slug> <goal>}"

    experiments_dir="$STATE_DIR/experiments"
    mkdir -p "$experiments_dir" 2>/dev/null || true

    # Fetch tracking protocol from API
    protocol=$(fetch "$API/supplements/$slug/tracking?goal=$goal" 2>/dev/null) || true
    if [ -z "$protocol" ]; then
      echo '{"error": "Failed to fetch tracking protocol. Check slug and goal."}'
      exit 1
    fi

    # Check for error in response
    err=$(echo "$protocol" | jq -r '.error // empty' 2>/dev/null)
    if [ -n "$err" ]; then
      echo "$protocol" | jq '.'
      exit 1
    fi

    # Generate experiment ID
    exp_id="${slug}--${goal}--$(date +%Y%m%d)"
    exp_file="$experiments_dir/${exp_id}.json"

    # Check if experiment already exists
    if [ -f "$exp_file" ]; then
      echo "{\"error\": \"Experiment already exists: $exp_id\", \"hint\": \"Use experiment-status $exp_id to view it, or experiment-list to see all.\"}"
      exit 1
    fi

    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Extract schedule info
    schedule=$(echo "$protocol" | jq '.data.checkIn.schedule')
    first_checkin_days=$(echo "$schedule" | jq '.firstCheckIn.value')
    freq_days=$(echo "$schedule" | jq '.frequency.value')
    total_checkins=$(echo "$schedule" | jq '.totalCheckIns')

    # Build experiment state
    jq -n \
      --arg id "$exp_id" \
      --arg slug "$slug" \
      --arg goal "$goal" \
      --arg now "$now" \
      --argjson schedule "$schedule" \
      --argjson first "$first_checkin_days" \
      --argjson freq "$freq_days" \
      --argjson total "$total_checkins" \
      --arg supp_name "$(echo "$protocol" | jq -r '.data.supplement.name')" \
      --arg goal_name "$(echo "$protocol" | jq -r '.data.goal.name')" \
      --arg dose "$(echo "$protocol" | jq -r '.data.protocol.recommendedDose')" \
      --arg timing "$(echo "$protocol" | jq -r '.data.protocol.recommendedTiming')" \
      '{
        id: $id,
        supplement: { slug: $slug, name: $supp_name },
        goal: { id: $goal, name: $goal_name },
        protocol: { dose: $dose, timing: $timing },
        status: "awaiting-baseline",
        startedAt: $now,
        schedule: $schedule,
        nextCheckIn: null,
        checkInsDone: 0,
        totalCheckIns: $total,
        baseline: null,
        checkIns: [],
        verdict: null
      }' > "$exp_file"

    echo "$protocol" | jq --arg id "$exp_id" '{
      experimentId: $id,
      status: "awaiting-baseline",
      message: "Experiment created. Now collect baseline answers before starting the supplement.",
      supplement: .data.supplement,
      goal: .data.goal,
      protocol: .data.protocol,
      baselineQuestions: .data.baseline
    }'
    ;;

  # ──────────────────────────────────────────────
  # EXPERIMENT — Record baseline answers
  # ──────────────────────────────────────────────
  experiment-baseline)
    exp_id="${1:?Usage: supstack.sh experiment-baseline <experiment-id> <answers-json>}"
    answers="${2:?Usage: supstack.sh experiment-baseline <experiment-id> '<json-answers>'}"

    exp_file="$STATE_DIR/experiments/${exp_id}.json"
    if [ ! -f "$exp_file" ]; then
      echo "{\"error\": \"Experiment not found: $exp_id\"}"
      exit 1
    fi

    status=$(jq -r '.status' "$exp_file")
    if [ "$status" != "awaiting-baseline" ]; then
      echo "{\"error\": \"Experiment is in '$status' state, not awaiting-baseline.\"}"
      exit 1
    fi

    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    first_days=$(jq '.schedule.firstCheckIn.value' "$exp_file")
    next_checkin=$(date -u -v+"${first_days}d" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "+${first_days} days" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)

    jq \
      --argjson answers "$answers" \
      --arg now "$now" \
      --arg next "$next_checkin" \
      '.status = "active" |
       .baseline = { recordedAt: $now, answers: $answers } |
       .nextCheckIn = $next' \
      "$exp_file" > "$exp_file.tmp" && mv "$exp_file.tmp" "$exp_file"

    jq '{
      experimentId: .id,
      status: .status,
      message: "Baseline recorded! Start taking the supplement now.",
      supplement: .supplement.name,
      goal: .goal.name,
      protocol: .protocol,
      nextCheckIn: .nextCheckIn,
      totalCheckIns: .totalCheckIns
    }' "$exp_file"
    ;;

  # ──────────────────────────────────────────────
  # EXPERIMENT — Record a check-in
  # ──────────────────────────────────────────────
  experiment-checkin)
    exp_id="${1:?Usage: supstack.sh experiment-checkin <experiment-id> <answers-json>}"
    answers="${2:?Usage: supstack.sh experiment-checkin <experiment-id> '<json-answers>'}"

    exp_file="$STATE_DIR/experiments/${exp_id}.json"
    if [ ! -f "$exp_file" ]; then
      echo "{\"error\": \"Experiment not found: $exp_id\"}"
      exit 1
    fi

    status=$(jq -r '.status' "$exp_file")
    if [ "$status" != "active" ]; then
      echo "{\"error\": \"Experiment is '$status', not active.\"}"
      exit 1
    fi

    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    checkins_done=$(jq '.checkInsDone' "$exp_file")
    total_checkins=$(jq '.totalCheckIns' "$exp_file")
    new_count=$((checkins_done + 1))

    freq_days=$(jq '.schedule.frequency.value' "$exp_file")

    if [ "$new_count" -ge "$total_checkins" ]; then
      new_status="completed"
      next_checkin="null"
    else
      new_status="active"
      next_checkin="\"$(date -u -v+"${freq_days}d" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "+${freq_days} days" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)\""
    fi

    jq \
      --argjson answers "$answers" \
      --arg now "$now" \
      --argjson num "$new_count" \
      --arg new_status "$new_status" \
      --argjson next "$next_checkin" \
      '.checkIns += [{ checkInNumber: $num, recordedAt: $now, answers: $answers }] |
       .checkInsDone = $num |
       .status = $new_status |
       .nextCheckIn = $next' \
      "$exp_file" > "$exp_file.tmp" && mv "$exp_file.tmp" "$exp_file"

    result=$(jq --argjson num "$new_count" '{
      experimentId: .id,
      status: .status,
      checkInNumber: $num,
      totalCheckIns: .totalCheckIns,
      nextCheckIn: .nextCheckIn,
      message: (if .status == "completed" then "All check-ins complete! Run experiment-evaluate to get your verdict." else "Check-in \($num) recorded." end)
    }' "$exp_file")

    echo "$result"
    ;;

  # ──────────────────────────────────────────────
  # EXPERIMENT — Get experiment status
  # ──────────────────────────────────────────────
  experiment-status)
    exp_id="${1:-}"

    if [ -z "$exp_id" ]; then
      # Show all experiments if no ID given
      experiments_dir="$STATE_DIR/experiments"
      if [ ! -d "$experiments_dir" ] || [ -z "$(ls -A "$experiments_dir" 2>/dev/null)" ]; then
        echo '{"experiments": [], "message": "No experiments found."}'
        exit 0
      fi
      jq -s '[.[] | {id, supplement: .supplement.name, goal: .goal.name, status, checkInsDone, totalCheckIns, startedAt, nextCheckIn}]' "$experiments_dir"/*.json
      exit 0
    fi

    exp_file="$STATE_DIR/experiments/${exp_id}.json"
    if [ ! -f "$exp_file" ]; then
      echo "{\"error\": \"Experiment not found: $exp_id\"}"
      exit 1
    fi

    jq '{
      id,
      supplement: .supplement.name,
      goal: .goal.name,
      status,
      protocol,
      startedAt,
      checkInsDone,
      totalCheckIns,
      nextCheckIn,
      hasBaseline: (.baseline != null),
      checkInDates: [.checkIns[]?.recordedAt],
      verdict
    }' "$exp_file"
    ;;

  # ──────────────────────────────────────────────
  # EXPERIMENT — Evaluate and compute verdict
  # ──────────────────────────────────────────────
  experiment-evaluate)
    exp_id="${1:?Usage: supstack.sh experiment-evaluate <experiment-id>}"

    exp_file="$STATE_DIR/experiments/${exp_id}.json"
    if [ ! -f "$exp_file" ]; then
      echo "{\"error\": \"Experiment not found: $exp_id\"}"
      exit 1
    fi

    # Fetch the tracking protocol with success criteria
    slug=$(jq -r '.supplement.slug' "$exp_file")
    goal=$(jq -r '.goal.id' "$exp_file")
    protocol=$(fetch "$API/supplements/$slug/tracking?goal=$goal" 2>/dev/null) || true
    if [ -z "$protocol" ]; then
      echo '{"error": "Failed to fetch protocol for evaluation."}'
      exit 1
    fi

    # Use python for evaluation logic (comparing baseline to latest check-in)
    python3 -c "
import json, sys

exp = json.load(open(sys.argv[1]))
protocol = json.loads(sys.argv[2])

baseline = exp.get('baseline', {}).get('answers', {})
check_ins = exp.get('checkIns', [])

if not baseline:
    print(json.dumps({'error': 'No baseline recorded yet.'}))
    sys.exit(0)

if not check_ins:
    print(json.dumps({'error': 'No check-ins recorded yet. Complete at least one check-in.'}))
    sys.exit(0)

latest = check_ins[-1].get('answers', {})
criteria = protocol.get('data', {}).get('successCriteria', {})
primary = criteria.get('primary', [])
secondary = criteria.get('secondary', [])
verdict_map = criteria.get('verdict', {})

results = {'primary': [], 'secondary': []}

def evaluate_criterion(c, baseline, latest):
    metric = c['metric']
    condition = c['condition']
    threshold = c.get('threshold')
    b_val = baseline.get(metric)
    l_val = latest.get(metric)

    result = {
        'metric': metric,
        'condition': condition,
        'description': c.get('description', ''),
        'baseline': b_val,
        'latest': l_val,
        'met': False
    }

    if b_val is None or l_val is None:
        result['note'] = 'Missing data — cannot evaluate'
        return result

    try:
        b_num = float(b_val)
        l_num = float(l_val)

        if condition == 'increase' and threshold:
            result['change'] = round(l_num - b_num, 2)
            result['met'] = (l_num - b_num) >= threshold
        elif condition == 'decrease' and threshold:
            result['change'] = round(b_num - l_num, 2)
            result['met'] = (b_num - l_num) >= threshold
        elif condition == 'improve':
            result['met'] = l_num != b_num  # Any change in positive direction
            result['note'] = 'Qualitative improvement assessed'
        elif condition == 'maintain':
            result['met'] = abs(l_num - b_num) <= (threshold or 1)
    except (ValueError, TypeError):
        # Non-numeric — qualitative comparison
        if condition == 'improve':
            result['met'] = str(l_val) != str(b_val)
            result['note'] = 'Qualitative comparison'
        else:
            result['note'] = 'Non-numeric metric — manual evaluation needed'

    return result

for c in primary:
    results['primary'].append(evaluate_criterion(c, baseline, latest))
for c in secondary:
    results['secondary'].append(evaluate_criterion(c, baseline, latest))

# Compute verdict
primary_met = sum(1 for r in results['primary'] if r['met'])
secondary_met = sum(1 for r in results['secondary'] if r['met'])

# Check for side effects
side_effects = latest.get('side-effects', [])
has_significant_se = isinstance(side_effects, list) and len(side_effects) > 0 and 'none' not in side_effects

if has_significant_se and any(s not in ['none', 'other'] for s in (side_effects if isinstance(side_effects, list) else [])):
    verdict = 'stop'
    verdict_text = verdict_map.get('stop', 'Significant side effects — discontinue')
elif primary_met >= 2:
    verdict = 'clear-win'
    verdict_text = verdict_map.get('clear-win', '2+ primary criteria met')
elif primary_met >= 1 and secondary_met >= 1:
    verdict = 'probable-win'
    verdict_text = verdict_map.get('probable-win', '1 primary + 1 secondary met')
elif primary_met >= 1 or secondary_met >= 2:
    verdict = 'inconclusive'
    verdict_text = verdict_map.get('inconclusive', 'Some improvement but below thresholds')
else:
    verdict = 'not-effective'
    verdict_text = verdict_map.get('not-effective', 'No meaningful improvement')

output = {
    'experimentId': exp['id'],
    'supplement': exp['supplement']['name'],
    'goal': exp['goal']['name'],
    'verdict': verdict,
    'verdictText': verdict_text,
    'checkInsCompleted': len(check_ins),
    'criteriaResults': results,
    'summary': {
        'primaryMet': primary_met,
        'primaryTotal': len(primary),
        'secondaryMet': secondary_met,
        'secondaryTotal': len(secondary),
        'sideEffects': side_effects if isinstance(side_effects, list) else []
    }
}

print(json.dumps(output, indent=2))
" "$exp_file" "$(echo "$protocol")"

    # Save verdict to experiment file
    verdict=$(python3 -c "
import json, sys
exp = json.load(open(sys.argv[1]))
protocol = json.loads(sys.argv[2])
baseline = exp.get('baseline', {}).get('answers', {})
check_ins = exp.get('checkIns', [])
if not baseline or not check_ins:
    sys.exit(0)
latest = check_ins[-1].get('answers', {})
criteria = protocol.get('data', {}).get('successCriteria', {})
primary = criteria.get('primary', [])
pm = 0
for c in primary:
    m = c['metric']
    b, l = baseline.get(m), latest.get(m)
    if b is None or l is None: continue
    try:
        b, l = float(b), float(l)
        t = c.get('threshold', 0)
        if c['condition'] == 'increase' and (l - b) >= t: pm += 1
        elif c['condition'] == 'decrease' and (b - l) >= t: pm += 1
        elif c['condition'] == 'improve' and l != b: pm += 1
    except: pass
se = latest.get('side-effects', [])
has_se = isinstance(se, list) and len(se) > 0 and 'none' not in se
if has_se: v = 'stop'
elif pm >= 2: v = 'clear-win'
elif pm >= 1: v = 'probable-win'
else: v = 'inconclusive'
print(v)
" "$exp_file" "$(echo "$protocol")" 2>/dev/null) || true

    if [ -n "$verdict" ]; then
      jq --arg v "$verdict" '.verdict = $v' "$exp_file" > "$exp_file.tmp" && mv "$exp_file.tmp" "$exp_file"
    fi
    ;;

  # ──────────────────────────────────────────────
  # EXPERIMENT — List all experiments
  # ──────────────────────────────────────────────
  experiment-list)
    experiments_dir="$STATE_DIR/experiments"
    if [ ! -d "$experiments_dir" ] || [ -z "$(ls -A "$experiments_dir" 2>/dev/null)" ]; then
      echo '{"experiments": [], "message": "No experiments found. Start one with: experiment-start <slug> <goal>"}'
      exit 0
    fi
    jq -s '[.[] | {id, supplement: .supplement.name, goal: .goal.name, status, checkInsDone, totalCheckIns, startedAt, nextCheckIn, verdict}] | sort_by(.startedAt) | reverse' "$experiments_dir"/*.json
    ;;

  # ──────────────────────────────────────────────
  # EXPERIMENT — Get tracking questions for an experiment
  # ──────────────────────────────────────────────
  experiment-questions)
    exp_id="${1:?Usage: supstack.sh experiment-questions <experiment-id> [baseline|checkin]}"
    qtype="${2:-checkin}"

    exp_file="$STATE_DIR/experiments/${exp_id}.json"
    if [ ! -f "$exp_file" ]; then
      echo "{\"error\": \"Experiment not found: $exp_id\"}"
      exit 1
    fi

    slug=$(jq -r '.supplement.slug' "$exp_file")
    goal=$(jq -r '.goal.id' "$exp_file")

    protocol=$(fetch "$API/supplements/$slug/tracking?goal=$goal" 2>/dev/null) || true
    if [ -z "$protocol" ]; then
      echo '{"error": "Failed to fetch protocol."}'
      exit 1
    fi

    if [ "$qtype" = "baseline" ]; then
      echo "$protocol" | jq '.data.baseline'
    else
      echo "$protocol" | jq '.data.checkIn'
    fi
    ;;

  # ══════════════════════════════════════════════
  # TIMING OPTIMISER
  # ══════════════════════════════════════════════

  timing-optimize)
    # Read stack from profile or from argument
    stack_slugs="${1:-}"
    if [ -z "$stack_slugs" ]; then
      stack_slugs=$(bash "${BASH_SOURCE[0]}" profile-stack-slugs 2>/dev/null)
    fi

    if [ -z "$stack_slugs" ]; then
      echo '{"error": "No stack found. Pass slugs as argument or add supplements to your profile first.", "usage": "supstack.sh timing-optimize [slug1,slug2,...]"}'
      exit 1
    fi

    # Fetch protocol data for each supplement
    IFS=',' read -ra STACK_ARRAY <<< "$stack_slugs"
    protocols="[]"

    for slug in "${STACK_ARRAY[@]}"; do
      slug=$(echo "$slug" | xargs)
      proto=$(fetch "$API/supplements/$slug/protocol" 2>/dev/null) || continue

      # Extract relevant timing info
      entry=$(echo "$proto" | jq --arg slug "$slug" '{
        slug: $slug,
        name: .data.supplement.name,
        timing: .data.timing,
        form: .data.form,
        dosage: .data.dosage,
        withFood: .data.timing.withFood
      }' 2>/dev/null) || continue

      protocols=$(echo "$protocols" | jq --argjson entry "$entry" '. + [$entry]')
    done

    # Also fetch interactions between all stack items
    interactions="[]"
    if [ ${#STACK_ARRAY[@]} -ge 2 ]; then
      inter_slugs=$(IFS=,; echo "${STACK_ARRAY[*]}")
      inter_response=$(fetch "$API/interactions?supplements=$inter_slugs" 2>/dev/null) || true
      if [ -n "$inter_response" ]; then
        interactions=$(echo "$inter_response" | jq '.data.supplementInteractions // []' 2>/dev/null) || interactions="[]"
      fi
    fi

    # Use python to build the optimal timing schedule
    python3 -c "
import json, sys

protocols = json.loads(sys.argv[1])
interactions = json.loads(sys.argv[2])

# Classify supplements by timing
morning = []
afternoon = []
evening = []
with_food = []
empty_stomach = []
anytime = []

timing_rules = {
    'morning': ['morning', 'am', 'upon waking', 'before breakfast'],
    'afternoon': ['afternoon', 'midday', 'noon'],
    'evening': ['evening', 'before bed', 'bedtime', 'night', 'pm', 'before sleep'],
    'empty_stomach': ['empty stomach', 'before meals', 'fasted'],
}

for p in protocols:
    name = p.get('name', p.get('slug', ''))
    timing = p.get('timing', {})
    optimal = timing.get('optimal', [])
    notes = timing.get('notes', '')
    needs_food = timing.get('withFood', False) or p.get('withFood', False)

    # Use the FIRST entry in optimal array as primary recommendation
    # (it's the most important/common timing)
    primary_optimal = optimal[0].lower() if optimal else ''
    all_optimal = ' '.join(optimal).lower()
    notes_text = notes.lower()

    classified = False
    # Priority 1: Check first optimal entry (primary recommendation)
    for kw in timing_rules['evening']:
        if kw in primary_optimal:
            evening.append(name)
            classified = True
            break
    if not classified:
        for kw in timing_rules['morning']:
            if kw in primary_optimal:
                morning.append(name)
                classified = True
                break
    # Priority 2: Check all optimal entries
    if not classified:
        for kw in timing_rules['evening']:
            if kw in all_optimal:
                evening.append(name)
                classified = True
                break
    if not classified:
        for kw in timing_rules['morning']:
            if kw in all_optimal:
                morning.append(name)
                classified = True
                break
    # Priority 3: Fall back to notes
    if not classified:
        for kw in timing_rules['evening']:
            if kw in notes_text:
                evening.append(name)
                classified = True
                break
    if not classified:
        for kw in timing_rules['morning']:
            if kw in notes_text:
                morning.append(name)
                classified = True
                break
    if not classified:
        anytime.append(name)

    if needs_food:
        with_food.append(name)
    full_text = all_optimal + ' ' + notes_text
    for kw in timing_rules['empty_stomach']:
        if kw in full_text:
            empty_stomach.append(name)
            break

# Build timing windows
schedule = []

# Morning window
morning_items = []
for p in protocols:
    name = p.get('name', p.get('slug', ''))
    if name in morning or (name in anytime and name not in evening):
        food_note = '(with food)' if name in with_food else '(empty stomach OK)' if name in empty_stomach else ''
        dose = p.get('dosage', {}).get('recommended', '')
        morning_items.append({'supplement': name, 'dose': dose, 'note': food_note})

if morning_items:
    schedule.append({
        'window': 'Morning (with breakfast)',
        'supplements': morning_items
    })

# Evening window
evening_items = []
for p in protocols:
    name = p.get('name', p.get('slug', ''))
    if name in evening:
        food_note = '(with food)' if name in with_food else ''
        dose = p.get('dosage', {}).get('recommended', '')
        evening_items.append({'supplement': name, 'dose': dose, 'note': food_note})

if evening_items:
    schedule.append({
        'window': 'Evening (30-60 min before bed)',
        'supplements': evening_items
    })

# Check for conflicts
conflicts = []
for inter in interactions:
    sev = inter.get('severity', inter.get('type', ''))
    if sev in ['caution', 'moderate', 'high']:
        between = inter.get('between', [])
        desc = inter.get('description', '')
        conflicts.append({
            'between': between,
            'severity': sev,
            'description': desc,
            'recommendation': inter.get('recommendation', 'Separate by 2+ hours')
        })

# Separation rules
separations = []
for name in empty_stomach:
    if name in with_food:
        continue  # Contradictory, skip
    separations.append({
        'supplement': name,
        'rule': 'Take on an empty stomach (30 min before food)',
    })

# Build notes
notes = []
if with_food:
    notes.append(f\"Take with food: {', '.join(with_food)}\")
if empty_stomach:
    notes.append(f\"Take on empty stomach: {', '.join(empty_stomach)}\")

output = {
    'schedule': schedule,
    'conflicts': conflicts,
    'separationRules': separations,
    'notes': notes,
    'supplementCount': len(protocols)
}

print(json.dumps(output, indent=2))
" "$(echo "$protocols")" "$(echo "$interactions")"
    ;;

  # ──────────────────────────────────────────────
  # Help
  # ──────────────────────────────────────────────
  help|*)
    cat <<'EOF'
SupStack API Helper — Commands

ONBOARDING
  welcome                             First-run check (shows intro if new user)
  welcome --force                     Show intro with live stats regardless

LOOKUP & DISCOVERY
  info <slug>                         Full supplement profile
  search <query>                      Full-text search (find the right slug)
  protocol <slug>                     Dosing protocol (dose, timing, form, cycling)

GOALS & RECOMMENDATIONS
  match <g1> [g2] [g3] [limit]       Goal-based matching (weighted)
  recommend [--goals=..] [--stack=..] Smart recs (stack-aware, synergy-boosted)

SAFETY & INTERACTIONS
  safety <slug>                       Full safety profile
  interactions <slug> [medication]    Drug interactions
  interactions-multi <s1> <s2> ...    Supplement-supplement interactions

SYNERGIES
  synergies <slug>                    What pairs well with this supplement
  synergies-multi <s1> <s2> ...      Synergies between specific supplements

RESEARCH
  studies [--supplement=..] [--q=..]  Search 7,780+ research studies

RESEARCH MONITOR
  monitor-setup <s1,s2,...> [--frequency=weekly|biweekly|monthly]
                                      Start tracking supplements for new research
  monitor-check                       Check for new studies (used by cron)
  monitor-status                      Show what's being tracked
  monitor-add <slug>                  Add a supplement to monitoring
  monitor-remove <slug>              Remove a supplement from monitoring
  monitor-clear                       Stop monitoring and clear all data

USER PROFILE
  profile                             Show full user profile
  profile-get <section>               Read a specific section
  profile-update <section> <content>  Replace a section's content
  profile-add <section> <line>        Append a line to a section
  profile-stack-slugs                 Get current stack as comma-separated slugs
  profile-medications                 Get medications as JSON array
  profile-log-interest <slug> [ctx]   Log interest in a supplement (auto-increments)
  profile-log-search <type> <subj>    Log a search query to history
  profile-interests                   Get all interests sorted by frequency
  Sections: stack, medications, goals, conditions, allergies, trials, interests, history, preferences, profile, notes

N-OF-1 EXPERIMENTS
  experiment-start <slug> <goal>      Start a new experiment
  experiment-baseline <id> <json>     Record baseline answers
  experiment-checkin <id> <json>      Record a check-in
  experiment-status [id]              Show experiment status (or all if no ID)
  experiment-evaluate <id>            Compute verdict from collected data
  experiment-list                     List all experiments
  experiment-questions <id> [type]    Get questions (baseline|checkin)

TIMING OPTIMISER
  timing-optimize [slugs]             Optimal timing schedule for your stack
EOF
    ;;

esac
