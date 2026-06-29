#!/usr/bin/env bash
# seddo — Agent coordination via GitHub Gist
# Wolof: séddo = partager, la répartition
# A seddo is a sharing space where agents exchange tasks, knowledge, and progress.
#
# Architecture:
#   ~/.seddo.d/                   → multi-seddo workspace
#   ~/.seddo.d/active             → name of the active seddo
#   ~/.seddo.d/<name>/config      → per-seddo config (gist IDs, role, etc.)
#   ~/.seddo.d/<name>/state.json  → hub/spoke metadata
#
# Role:
#   - HUB: created the original gist, owns the canonical source
#   - SPOKE: forked the gist, syncs via hub pull-based merge

set -euo pipefail

SEDDO_ROOT="${SEDDO_ROOT:-$HOME/.seddo.d}"
SEDDO_ACTIVE_FILE="${SEDDO_ROOT}/active"
# Version: auto-detected from git tag or SHA if available
SEDDO_VERSION="2.6.5"

# Read version from .version file (publish-time, travels with skill)
# Fallback to git describe, then hardcoded SEDDO_VERSION
_seddo_version() {
  local dir; dir="$(dirname "$0")/.."
  if [[ -f "${dir}/.version" ]]; then
    local v; v=$(cat "${dir}/.version" 2>/dev/null | tr -d '[:space:]')
    [[ -n "$v" ]] && echo "$v" && return
  fi
  local git_dir="${dir}/.git"
  if [[ -d "$git_dir" ]]; then
    git --git-dir="$git_dir" describe --tags 2>/dev/null || git --git-dir="$git_dir" rev-parse --short HEAD 2>/dev/null || echo "$SEDDO_VERSION"
  else
    echo "$SEDDO_VERSION"
  fi
}

_seddo_hash() {
  if command -v sha256sum &>/dev/null; then
    local dir; dir="$(cd "$(dirname "$0")/.." && pwd)"
    cat "${dir}/SKILL.md" "$0" "${dir}/AGENTS.md" 2>/dev/null | sha256sum | cut -c1-12 || echo "unknown"
  else
    echo "unknown"
  fi
}

# Per-seddo paths (set by load_config)
seddo_name=""
seddo_config=""
seddo_state=""

# Active seddo config (from files)
GIST_ID=""
AGENT_NAME=""
ROLE=""           # hub | spoke
FORK_OF=""        # gist ID of hub (for spokes)
FORK_GIST_ID=""   # our fork's gist ID (for spokes)
GH_USER=""

# ─── Timestamp ───────────────────────────────────────────
now() { date -u +"%Y-%m-%dT%H:%MZ"; }

# ─── Config I/O ──────────────────────────────────────────
ensure_seddo_root() {
  # Auto-migrate old ~/.seddo file to new directory structure
  if [[ -f "$HOME/.seddo" ]] && [[ ! -d "$SEDDO_ROOT" ]]; then
    local old_gist_id old_agent_name old_swarm_name old_gist_url
    old_gist_id=$(grep '^SWARM_GIST_ID=' "$HOME/.seddo" 2>/dev/null | cut -d= -f2-)
    old_agent_name=$(grep '^AGENT_NAME=' "$HOME/.seddo" 2>/dev/null | cut -d= -f2-)
    old_swarm_name=$(grep '^SWARM_NAME=' "$HOME/.seddo" 2>/dev/null | cut -d= -f2-)
    old_gist_url=$(grep '^GIST_URL=' "$HOME/.seddo" 2>/dev/null | cut -d= -f2-)

    if [[ -n "$old_gist_id" ]]; then
      echo "📦 Auto-migrating old seddo config to new format..."
      mkdir -p "$SEDDO_ROOT"
      local seddo_dir="${SEDDO_ROOT}/${old_swarm_name}"
      mkdir -p "$seddo_dir"
      cat > "$seddo_dir/config" << EOF
GIST_ID=${old_gist_id}
GIST_URL=${old_gist_url}
AGENT_NAME=${old_agent_name}
ROLE=hub
FORK_OF=
FORK_GIST_ID=
EOF
      echo "${old_swarm_name}" > "$SEDDO_ROOT/active"
      local bak_ts
      bak_ts=$(date +%s)
      mv "$HOME/.seddo" "$HOME/.seddo.bak.${bak_ts}"
      echo "   ✅ Migrated: ${old_swarm_name}"
      echo "   📁 Old config backed up to ~/.seddo.bak.${bak_ts}"
    fi
  fi
  mkdir -p "$SEDDO_ROOT"
}

load_active_seddo() {
  if [[ ! -f "$SEDDO_ACTIVE_FILE" ]]; then return 1; fi
  seddo_name=$(cat "$SEDDO_ACTIVE_FILE")
  load_seddo_config "$seddo_name"
}

load_seddo_config() {
  local name="$1"
  seddo_config="${SEDDO_ROOT}/${name}/config"
  seddo_state="${SEDDO_ROOT}/${name}/state.json"

  if [[ -f "$seddo_config" ]]; then
    GIST_ID=$(grep '^GIST_ID=' "$seddo_config" | cut -d= -f2-)
    AGENT_NAME=$(grep '^AGENT_NAME=' "$seddo_config" | cut -d= -f2-)
  fi
  GIST_ID="${GIST_ID:-${SWARM_GIST_ID:-}}"
  AGENT_NAME="${AGENT_NAME:-${SEDDO_AGENT:-}}"
  ROLE=$(grep '^ROLE=' "$seddo_config" 2>/dev/null | cut -d= -f2- || echo "hub")
  FORK_OF=$(grep '^FORK_OF=' "$seddo_config" 2>/dev/null | cut -d= -f2- || echo "")
  FORK_GIST_ID=$(grep '^FORK_GIST_ID=' "$seddo_config" 2>/dev/null | cut -d= -f2- || echo "")
}

save_seddo_config() {
  local name="$1"
  seddo_config="${SEDDO_ROOT}/${name}/config"
  mkdir -p "$(dirname "$seddo_config")"
  cat > "$seddo_config"
  echo "$name" > "$SEDDO_ACTIVE_FILE"
  seddo_name="$name"
}

save_state_json() {
  local name="$1"
  local state_file="${SEDDO_ROOT}/${name}/state.json"
  mkdir -p "$(dirname "$state_file")"
  cat > "$state_file"
}

# ─── Prerequisites ───────────────────────────────────────
require_gh() {
  if ! command -v gh &>/dev/null; then
    echo "❌ gh (GitHub CLI) not found."
    echo "   Install: https://cli.github.com/"
    exit 1
  fi
  if ! gh auth status &>/dev/null 2>&1; then
    echo "❌ gh not authenticated. Run: gh auth login"
    exit 1
  fi
}

require_seddo() {
  if [[ -z "$seddo_name" ]]; then
    echo "❌ No active seddo."
    echo "   Run: seddo list   (to see available seddos)"
    echo "   Run: seddo init   (to create a new seddo)"
    echo "   Run: seddo join   (to join an existing seddo)"
    exit 1
  fi
}

require_role() {
  if [[ -z "$ROLE" ]]; then
    echo "❌ No role configured for seddo « $seddo_name »"
    exit 1
  fi
}

# ─── Gist helpers ────────────────────────────────────────
extract_gist_id() {
  local url="$1"
  local id
  id=$(echo "$url" | grep -oP '[a-f0-9]{32}' | head -1)
  [[ -n "$id" ]] && echo "$id" && return
  id=$(echo "$url" | grep -oP '[a-f0-9]{20,}' | head -1)
  [[ -n "$id" ]] && echo "$id" && return
  return 1
}

fetch_file() {
  local filename="$1"
  local out
  if ! out=$(gh gist view "$GIST_ID" -f "$filename" 2>&1); then
    echo "❌ fetch_file: failed to fetch ${filename} from gist ${GIST_ID:0:8}..." >&2
    echo "   ${out}" >&2
    return 1
  fi
  printf '%s' "$out"
}

fetch_from() {
  local gist_id="$1"
  local filename="$2"
  local out
  if ! out=$(gh gist view "$gist_id" -f "$filename" 2>&1); then
    echo "❌ fetch_from: failed to fetch ${filename} from gist ${gist_id:0:8}..." >&2
    echo "   ${out}" >&2
    return 1
  fi
  printf '%s' "$out"
}

list_forks() {
  local gist_id="$1"
  gh api --paginate "/gists/${gist_id}/forks" 2>/dev/null || echo "[]"
}

fetch_all() {
  local gist_id="${1:-$GIST_ID}"
  gh gist view "$gist_id" --raw
}

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\r'/}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

edit_file() {
  local gist_id filename content
  gist_id="${1:-$GIST_ID}"
  filename="${2:-}"
  content="${3:-}"
  if [[ -z "$filename" ]] || [[ -z "$content" ]]; then
    echo "❌ edit_file: requires gist_id, filename, content" >&2
    return 1
  fi
  local esc_name esc_content
  esc_name=$(json_escape "$filename")
  esc_content=$(json_escape "$content")
  printf '{"files":{"%s":{"content":"%s"}}}' "$esc_name" "$esc_content" \
    | gh api --method PATCH "/gists/${gist_id}" --input - >/dev/null
}

# Atomic multi-file edit via single PATCH — avoids race window from multiple calls.
# Usage: edit_files <gist_id> <file1> <content1> [<file2> <content2> [...]]
edit_files() {
  local gist_id="${1:-$GIST_ID}"
  shift
  local files_json=""
  local first=true
  while [[ $# -ge 2 ]]; do
    local fname="$1" content="$2"
    shift 2
    local esc_name esc_content
    esc_name=$(json_escape "$fname")
    esc_content=$(json_escape "$content")
    if $first; then
      files_json+="\"$esc_name\":{\"content\":\"$esc_content\"}"
      first=false
    else
      files_json+=",\"$esc_name\":{\"content\":\"$esc_content\"}"
    fi
  done
  printf '{"files":{%s}}' "$files_json" \
    | gh api --method PATCH "/gists/${gist_id}" --input - >/dev/null
}

update_task_field() {
  local content="${1:-}"
  local task_id="${2:-}"
  local field="${3:-}"
  local value="${4:-}"
  if [[ -z "$task_id" ]] || [[ -z "$field" ]]; then
    echo "❌ update_task_field: requires content, task_id, field, value" >&2
    return 1
  fi
  echo "$content" | awk -v tid="$task_id" -v fld="$field" -v val="$value" '
    /^### / { in_task = ($0 ~ "### " tid ":") }
    in_task && $0 ~ "^- " fld ":" { sub("^- " fld ":.*", "- " fld ": " val) }
    { print }
  '
}

fork_gist() {
  local gist_id="$1"
  curl -s -X POST \
    -H "Authorization: Bearer $(gh auth token)" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/gists/${gist_id}/forks"
}

get_gh_user() {
  gh api user --jq .login 2>/dev/null || echo ""
}

# ─── Merge helpers ───────────────────────────────────────

# Merge append-only files (INBOX, ACTIVITY, LESSONS).
# Takes base as canonical; appends lines from incoming not already in base.
# Skips headers, blank lines, and separators from dedup check.
merge_append() {
  local base="$1"
  local incoming="$2"
  local result="$base"
  while IFS= read -r line; do
    [[ -z "$line" ]]          && continue
    [[ "$line" =~ ^# ]]       && continue
    [[ "$line" == "---" ]]    && continue
    if ! grep -qxF -- "$line" <<< "$base" 2>/dev/null; then
      result+=$'\n'"$line"
    fi
  done <<< "$incoming"
  printf '%s' "$result"
}

# Merge TASKS.md: block-based, last-write-wins by updated: timestamp.
# Tasks only in incoming are appended. Preserves base preamble.
merge_tasks() {
  local base="$1"
  local incoming="$2"
  # Implemented in awk to avoid bash associative-array + set -u incompatibilities.
  # Sentinel separates base from incoming; last-write-wins by updated: timestamp.
  printf '%s\n---SEDDO_MERGE_INCOMING---\n%s\n' "$base" "$incoming" | awk '
    BEGIN { mode="base"; in_block=0; cur_id=""; cur_block=""; preamble="" }

    /^### T-[0-9]+:/ {
      if (cur_id != "") {
        if (mode == "base") base_block[cur_id] = cur_block
        else                inc_block[cur_id]  = cur_block
      }
      cur_id = $0
      sub(/^### /, "", cur_id)
      sub(/:.*$/,  "", cur_id)
      cur_block = $0 "\n"
      in_block = 1
      next
    }

    /^---SEDDO_MERGE_INCOMING---$/ {
      if (cur_id != "") { base_block[cur_id] = cur_block; cur_id = ""; cur_block = "" }
      mode = "incoming"; in_block = 0
      next
    }

    in_block {
      cur_block = cur_block $0 "\n"
      if (match($0, /^- updated: /)) {
        ts = substr($0, RSTART + length("- updated: "))
        if (mode == "base") base_ts[cur_id] = ts
        else                inc_ts[cur_id]  = ts
      }
      next
    }

    mode == "base" && !in_block { preamble = preamble $0 "\n" }

    END {
      if (cur_id != "") {
        if (mode == "base") base_block[cur_id] = cur_block
        else                inc_block[cur_id]  = cur_block
      }
      printf "%s", preamble
      for (id in base_block) all[id] = 1
      for (id in inc_block)  all[id] = 1
      n = 0
      for (id in all) ids[n++] = id
      for (i = 0; i < n-1; i++)
        for (j = i+1; j < n; j++) {
          split(ids[i], a, "-"); split(ids[j], b, "-")
          if (a[2]+0 > b[2]+0) { t=ids[i]; ids[i]=ids[j]; ids[j]=t }
        }
      for (i = 0; i < n; i++) {
        id = ids[i]
        if (id in base_block && id in inc_block)
          printf "\n%s", (inc_ts[id] > base_ts[id] ? inc_block[id] : base_block[id])
        else if (id in base_block)
          printf "\n%s", base_block[id]
        else
          printf "\n%s", inc_block[id]
      }
    }
  '
}

# ─── COMMANDS ────────────────────────────────────────────

# ── seddo init ──────────────────────────────────────────
cmd_init() {
  echo "🤝 Seddo — Create a new coordination space"
  echo "   (wolof: séddo = partager)"
  echo ""

  require_gh

  GH_USER=$(get_gh_user)
  echo "✅ Authenticated as: @${GH_USER}"
  echo ""

  echo "🔍 Testing GitHub permissions..."
  local test_tmp
  test_tmp=$(mktemp)
  echo "seddo-test" > "$test_tmp"
  local test_url
  test_url=$(gh gist create -d "seddo-test" -f "test.md" < "$test_tmp" 2>&1 | head -1)
  rm -f "$test_tmp"

  if [[ -z "$test_url" ]]; then
    echo "❌ Cannot create gists. Check gist scope: gh auth status"
    exit 1
  fi
  local test_id
  test_id=$(extract_gist_id "$test_url")
  gh gist delete "$test_id" --yes &>/dev/null || true
  echo "✅ Secret gist creatable"
  echo ""

  echo "📂 Seddo name? (no spaces, used as folder name)"
  read -rp "   → " name_input
  name_input="${name_input:-seddo}"
  name_input=$(echo "$name_input" | tr -cd 'a-zA-Z0-9_-')
  if [[ -z "$name_input" ]]; then
    echo "❌ Invalid name."
    exit 1
  fi

  if [[ -d "${SEDDO_ROOT}/${name_input}" ]]; then
    echo "⚠️  Seddo « ${name_input} » already exists locally."
    read -rp "   Overwrite? [y/N] → " confirm
    [[ "$confirm" != "y" ]] && exit 0
  fi

  echo ""
  echo "👤 Agent name? (your identity in this seddo)"
  local detected=""
  if [[ -n "$AGENT_NAME" ]]; then
    detected="$AGENT_NAME"
  elif [[ -d "$HOME/.claude" ]]; then
    detected="claude-code"
  elif command -v openclaw &>/dev/null; then
    detected="kocc"
  elif [[ -d "$HOME/.opencode" ]]; then
    detected="opencode"
  fi
  echo "   (Enter for: ${detected:-agent})"
  read -rp "   → " agent_input
  local agent_name="${agent_input:-${detected:-agent}}"

  echo ""
  echo "📋 Other agents in this seddo? (comma-separated, optional)"
  read -rp "   → " other_agents

  echo ""
  echo "🤖 Creating hub gist..."

  local ts nl
  ts=$(now)
  nl=$'\n'

  # Build gist files — templates inlined, no external files needed
  local tmpdir
  tmpdir=$(mktemp -d)

  cat > "$tmpdir/PROTOCOL.md" << EOF
# ${name_input} — Seddo Protocol

Rules all agents must follow. Read first.

## Agent Behavior Rules

1. **Read before write** — \`gh gist view\` before editing
2. **Append, don't overwrite** — add at end, don't remove others' content
3. **Sign everything** — every entry includes \`— @name timestamp\`
4. **Update status promptly** — when starting/finishing a task
5. **Acknowledge messages** — mark read (✅) after acting
6. **Share lessons** — add to LESSONS.md when you learn something
7. **Log activity** — ACTIVITY.md for significant actions

## Message Format (INBOX.md)
\`\`\`
→ @agent-name : message — @from-agent YYYY-MM-DDTHH:MMZ
→ @all : broadcast — @from-agent YYYY-MM-DDTHH:MMZ
\`\`\`
Status: ✅ read · ⏳ in-progress · ✓ resolved

## Task Format (TASKS.md)
\`\`\`
### T-XXX: Task title
- status: DRAFT | ASSIGNED | WIP | REVIEW | DONE | BLOCKED | NEEDS_HUMAN
- assigned: @agent or @any
- priority: LOW | MEDIUM | HIGH | URGENT
- input: what needs to be done
- output: (filled when done)
- created: YYYY-MM-DDTHH:MMZ by @agent
- updated: YYYY-MM-DDTHH:MMZ
\`\`\`

## Conflict Resolution
Gists use last-write-wins per file.
- Always pull latest before editing
- Don't edit same file within same minute as another agent
- If contention: add \`LOCK:\` at top of file while editing, remove after
EOF

  cat > "$tmpdir/ROSTER.md" << EOF
# Roster — ${name_input}

| Agent | Capacités | Localisation |
|-------|-------------|-------------|
EOF

  cat > "$tmpdir/INBOX.md" << EOF
# ${name_input} — Inbox

Messages between agents. Append only. Sign every entry.

---
EOF

  cat > "$tmpdir/TASKS.md" << EOF
# ${name_input} — Task Board

Append only. Do not edit others' tasks without permission.

---
EOF

  cat > "$tmpdir/LESSONS.md" << EOF
# ${name_input} — Lessons Learned

Shared knowledge. Append only. Sign every entry.

---
EOF

  printf '%s\n' "# Activity — ${name_input}${nl}${nl}${ts} @${agent_name} — Seddo « ${name_input} » created (hub) 🤝" \
    > "$tmpdir/ACTIVITY.md"
  printf '%s\n' "# Registry — ${name_input}${nl}${nl}| Agent | Fork Gist ID | Fork URL | Registered |${nl}|-------|-------------|----------|-------------|${nl}| @${agent_name} | (hub) | (hub) | ${ts} |" \
    > "$tmpdir/REGISTRY.md"

  local gist_url
  gist_url=$(gh gist create \
    -d "🤝 Seddo: ${name_input} (hub)" \
    "$tmpdir/PROTOCOL.md" \
    "$tmpdir/ROSTER.md" \
    "$tmpdir/INBOX.md" \
    "$tmpdir/TASKS.md" \
    "$tmpdir/LESSONS.md" \
    "$tmpdir/ACTIVITY.md" \
    "$tmpdir/REGISTRY.md" \
    2>&1 | head -1)
  rm -rf "$tmpdir"

  local gist_id
  gist_id=$(extract_gist_id "$gist_url")

  if [[ -z "$gist_id" ]]; then
    echo "❌ Failed to create gist."
    exit 1
  fi

  local canonical_url="https://gist.github.com/${gist_id}"
  [[ -n "$GH_USER" ]] && canonical_url="https://gist.github.com/${GH_USER}/${gist_id}"

  ensure_seddo_root
  save_seddo_config "$name_input" <<EOF
GIST_ID=${gist_id}
GIST_URL=${canonical_url}
AGENT_NAME=${agent_name}
ROLE=hub
FORK_OF=
FORK_GIST_ID=
EOF

  save_state_json "$name_input" <<EOF
{
  "role": "hub",
  "gist_id": "${gist_id}",
  "gist_url": "${canonical_url}",
  "created_at": "${ts}",
  "forks": []
}
EOF

  echo ""
  echo "✅ Hub seddo « ${name_input} » created!"
  echo "   Gist ID : ${gist_id}"
  echo "   URL     : ${canonical_url}"
  echo "   Role    : HUB (you own the canonical source)"
  echo ""

  if [[ -n "$other_agents" ]]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔑 JOIN TOKEN — share with other agents:"
    echo ""
    echo "   seddo join ${gist_id}"
    echo ""
    echo "   They will be prompted for their agent name,"
    echo "   then the script will fork this gist automatically."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
  fi

  echo "Next steps:"
  echo "  seddo list      — verify seddo is active"
  echo "  seddo sync      — read all files"
  echo "  seddo inbox     — check messages"
}

# ── seddo join ──────────────────────────────────────────
cmd_join() {
  local input="${1:-}"
  require_gh

  if [[ -z "$input" ]]; then
    echo "Usage: seddo join <gist-id-or-url>"
    exit 1
  fi

  GH_USER=$(get_gh_user)
  local hub_gist_id
  hub_gist_id=$(extract_gist_id "$input")
  if [[ -z "$hub_gist_id" ]]; then
    hub_gist_id="$input"
  fi

  echo "🔍 Connecting to hub gist ${hub_gist_id:0:8}..."

  local raw
  raw=$(gh gist view "$hub_gist_id" --raw 2>/dev/null) || {
    echo "❌ Cannot access gist: ${hub_gist_id}"
    exit 1
  }

  local swarm_name
  swarm_name=$(echo "$raw" | grep -m1 '^# Roster\|^# Protocol\|^# Tasks\|^# .*—' \
    | head -1 | sed 's/^# //' | sed 's/ —.*//' | xargs)
  [[ -z "$swarm_name" ]] && swarm_name="seddo"

  local detected=""
  if [[ -n "$AGENT_NAME" ]]; then
    detected="$AGENT_NAME"
  elif [[ -d "$HOME/.claude" ]]; then
    detected="claude-code"
  elif command -v openclaw &>/dev/null; then
    detected="kocc"
  elif [[ -d "$HOME/.opencode" ]]; then
    detected="opencode"
  fi

  echo "✅ Hub gist accessible: ${swarm_name}"
  echo ""
  echo "👤 Your agent name?"
  echo "   (Enter for: ${detected:-agent})"
  read -rp "   → " agent_input
  local agent_name="${agent_input:-${detected:-agent}}"

  echo ""
  echo "🔱 Forking hub gist (this gives you write access)..."
  local fork_json fork_id fork_url fork_error
  fork_json=$(fork_gist "$hub_gist_id")

  fork_id=$(echo "$fork_json" | grep -oP '"id":\s*"\K[a-f0-9]{32}' | head -1 || true)
  fork_url=$(echo "$fork_json" | grep -oP '"html_url":\s*"\Khttps://gist.github.com[^"]+' | head -1 || true)
  fork_error=$(echo "$fork_json" | grep -oP '"message":\s*"\K[^"]+' | head -1 || true)

  # If user owns the hub gist, configure as hub mode instead
  if [[ "$fork_error" == *"cannot fork your own gist"* ]]; then
    echo "⚠️  You own this gist — configuring as HUB mode (no fork needed)"

    ensure_seddo_root

    local local_name="${swarm_name}"
    local counter=1
    while [[ -d "${SEDDO_ROOT}/${local_name}" ]] && [[ "$counter" -lt 100 ]]; do
      local_name="${swarm_name}-${counter}"
      ((counter++))
    done

    local canonical_url="https://gist.github.com/${hub_gist_id}"
    [[ -n "$GH_USER" ]] && canonical_url="https://gist.github.com/${GH_USER}/${hub_gist_id}"

    save_seddo_config "$local_name" <<EOF
GIST_ID=${hub_gist_id}
GIST_URL=${canonical_url}
AGENT_NAME=${agent_name}
ROLE=hub
FORK_OF=
FORK_GIST_ID=
EOF

    save_state_json "$local_name" <<EOF
{
  "role": "hub",
  "gist_id": "${hub_gist_id}",
  "gist_url": "${canonical_url}",
  "mode": "own-gist",
  "joined_at": "$(now)",
  "agent_name": "${agent_name}"
}
EOF

    echo ""
    echo "✅ Joined seddo « ${local_name} » as @${agent_name}"
    echo "   Role    : HUB (you own this gist)"
    echo "   Gist    : ${hub_gist_id}"
    echo ""
    echo "Next steps:"
    echo "  seddo sync      — read all files"
    echo "  seddo inbox     — check messages"
    return 0
  fi

  if [[ -z "$fork_id" ]]; then
    echo "❌ Fork failed. GitHub said: ${fork_error:-unknown}"
    echo "   Tip: check gist scope → gh auth status"
    exit 1
  fi

  echo "✅ Fork created: ${fork_id:0:8}..."

  ensure_seddo_root

  local local_name="${swarm_name}"
  local counter=1
  while [[ -d "${SEDDO_ROOT}/${local_name}" ]] && [[ "$counter" -lt 100 ]]; do
    local_name="${swarm_name}-${counter}"
    ((counter++))
  done

  local canonical_url="https://gist.github.com/${fork_id}"
  [[ -n "$GH_USER" ]] && canonical_url="https://gist.github.com/${GH_USER}/${fork_id}"

  save_seddo_config "$local_name" <<EOF
GIST_ID=${fork_id}
GIST_URL=${canonical_url}
AGENT_NAME=${agent_name}
ROLE=spoke
FORK_OF=${hub_gist_id}
FORK_GIST_ID=${fork_id}
EOF

  save_state_json "$local_name" <<EOF
{
  "role": "spoke",
  "gist_id": "${fork_id}",
  "gist_url": "${canonical_url}",
  "hub_gist_id": "${hub_gist_id}",
  "joined_at": "$(now)",
  "agent_name": "${agent_name}"
}
EOF

  # Auto-enroll: register in spoke fork ROSTER.md and log arrival
  local ts; ts=$(now)
  local roster
  roster=$(fetch_from "$fork_id" "ROSTER.md" 2>/dev/null || true)
  local ver; ver=$(_seddo_version)
  local hash; hash=$(_seddo_hash)
  local new_roster="${roster}
- ${agent_name} | ${canonical_url} | ${ts} | fork | v${ver} | sha:${hash}"
  edit_file "$fork_id" "ROSTER.md" "$new_roster"
  local inbox
  inbox=$(fetch_from "$fork_id" "INBOX.md" 2>/dev/null || true)
  local new_inbox="${inbox}
→ @all : Joined the seddo — @${agent_name} ${ts}"
  edit_file "$fork_id" "INBOX.md" "$new_inbox"

  echo ""
  echo "✅ Joined seddo « ${local_name} » as @${agent_name}"
  echo "   Role     : SPOKE (fork of hub)"
  echo "   Hub      : ${hub_gist_id}"
  echo "   Your fork: ${fork_id}"
  echo "   Local    : ${local_name}"
  echo ""
  echo "Next steps:"
  echo "  seddo sync      — pull hub → your fork (merges all content)"
  echo "  seddo inbox     — check messages"
  echo "  seddo tasks     — check tasks"
}

# ── seddo list ──────────────────────────────────────────
cmd_list() {
  ensure_seddo_root

  local active_name=""
  if [[ -f "$SEDDO_ACTIVE_FILE" ]]; then
    active_name=$(cat "$SEDDO_ACTIVE_FILE")
  fi

  echo "🤝 Seddo workspaces"
  echo "   Root: ${SEDDO_ROOT}"
  echo ""

  local found=false
  for dir in "$SEDDO_ROOT"/*/; do
    [[ -d "$dir" ]] || continue
    [[ -f "${dir}config" ]] || continue

    local name
    name=$(basename "$dir")
    local is_active="  "
    [[ "$name" == "$active_name" ]] && is_active="⭐"

    local role
    role=$(grep '^ROLE=' "${dir}config" 2>/dev/null | cut -d= -f2- || echo "?")
    local gist_id
    gist_id=$(grep '^GIST_ID=' "${dir}config" 2>/dev/null | cut -d= -f2- | cut -c1-8)
    local agent
    agent=$(grep '^AGENT_NAME=' "${dir}config" 2>/dev/null | cut -d= -f2-)

    echo " ${is_active} ${name}"
    echo "    Role  : ${role}"
    echo "    Agent : @${agent}"
    echo "    Gist  : ${gist_id}..."
    echo ""

    found=true
  done

  if ! $found; then
    echo "   No seddos found."
    echo "   Run: seddo init   (create a new hub)"
    echo "   Run: seddo join   (join an existing seddo)"
  fi
}

# ── seddo switch ────────────────────────────────────────
cmd_switch() {
  local name="$1"
  if [[ -z "$name" ]]; then
    echo "Usage: seddo switch <seddo-name>"
    echo "   Available seddos:"
    ls "$SEDDO_ROOT" 2>/dev/null | grep -v '^active$' || true
    exit 1
  fi

  if [[ ! -d "${SEDDO_ROOT}/${name}" ]]; then
    echo "❌ Seddo « ${name} » not found."
    exit 1
  fi

  echo "$name" > "$SEDDO_ACTIVE_FILE"
  load_seddo_config "$name"

  local role_display="HUB"
  [[ "$ROLE" == "spoke" ]] && role_display="SPOKE"
  echo "✅ Switched to « ${name} » (${role_display})"
  echo "   Gist ID : ${GIST_ID:0:8}..."
  echo "   Agent   : @${AGENT_NAME}"
}

# ── seddo remove ─────────────────────────────────────────
cmd_remove() {
  local name="$1"
  if [[ -z "$name" ]]; then
    echo "Usage: seddo remove <seddo-name>"
    exit 1
  fi

  if [[ ! -d "${SEDDO_ROOT}/${name}" ]]; then
    echo "❌ Seddo « ${name} » not found."
    exit 1
  fi

  local active_name=""
  [[ -f "$SEDDO_ACTIVE_FILE" ]] && active_name=$(cat "$SEDDO_ACTIVE_FILE")

  echo "⚠️  This only removes the LOCAL workspace (${SEDDO_ROOT}/${name}/)."
  echo "   The GitHub gist/fork is NOT deleted."
  echo ""
  read -rp "   Remove « ${name} »? [y/N] → " confirm
  [[ "$confirm" != "y" ]] && exit 0

  rm -rf "${SEDDO_ROOT}/${name}"
  echo "✅ Removed « ${name} » locally."

  if [[ "$name" == "$active_name" ]]; then
    rm -f "$SEDDO_ACTIVE_FILE"
    echo "   (was active — no active seddo now)"
  fi
}

# ── seddo status ────────────────────────────────────────
cmd_status() {
  require_seddo
  require_role

  local role_display="HUB"
  [[ "$ROLE" == "spoke" ]] && role_display="SPOKE (fork)"

  echo "🤝 Seddo: ${seddo_name}"
  echo "   Role    : ${role_display}"
  echo "   Agent   : @${AGENT_NAME}"
  echo "   Gist    : ${GIST_ID}"
  echo ""

  if [[ "$ROLE" == "spoke" ]]; then
    echo "   Hub gist : ${FORK_OF}"
    echo "   Your fork: ${GIST_ID}"
    echo ""
    echo "   Sync: seddo sync"
    echo "     → pulls hub + merges into your fork (bi-directional)"
  else
    echo "   Hub gist : ${GIST_ID} (you own it)"
    local fork_count
    fork_count=$(gh api --paginate "/gists/${GIST_ID}/forks" 2>/dev/null \
      | grep -c '"id":' || echo "0")
    echo "   Forks    : ${fork_count}"
    echo ""
    echo "   Sync: seddo sync"
    echo "     → discovers all forks, merges their content into hub"
  fi

  echo ""
  echo "📋 Recent activity (last 10 lines):"
  echo ""
  fetch_file "ACTIVITY.md" | tail -10
}

# ── seddo sync ──────────────────────────────────────────
# Hub:  discover all forks via GitHub API → merge INBOX/ACTIVITY/LESSONS/TASKS
#       into hub gist (hub is owner, so write works)
# Spoke: pull hub files → merge with own fork → write to fork
cmd_sync() {
  require_seddo
  require_role
  local mode="${1:-}"

  if [[ "$ROLE" == "hub" ]]; then
    echo "🔄 [HUB] Discovering forks..."

    local forks_json
    forks_json=$(gh api --paginate "/gists/${GIST_ID}/forks" 2>/dev/null || echo "[]")

    # Extract 32-char hex gist IDs (not node_id or other IDs)
    local fork_ids=()
    while IFS= read -r fid; do
      [[ -n "$fid" ]] && fork_ids+=("$fid")
    done < <(echo "$forks_json" | grep -oP '"id":\s*"\K[a-f0-9]{32}' || true)

    if [[ "${#fork_ids[@]}" -eq 0 ]]; then
      echo "   No forks found yet."
      echo "✅ Hub up to date."
      return 0
    fi

    echo "   Found ${#fork_ids[@]} fork(s). Merging..."

    # Read current hub state
    local hub_inbox hub_activity hub_lessons hub_tasks
    hub_inbox=$(fetch_file "INBOX.md") || { echo "❌ Abort sync: fetch hub INBOX.md failed" >&2; exit 1; }
    hub_activity=$(fetch_file "ACTIVITY.md") || { echo "❌ Abort sync: fetch hub ACTIVITY.md failed" >&2; exit 1; }
    hub_lessons=$(fetch_file "LESSONS.md") || { echo "❌ Abort sync: fetch hub LESSONS.md failed" >&2; exit 1; }
    hub_tasks=$(fetch_file "TASKS.md") || { echo "❌ Abort sync: fetch hub TASKS.md failed" >&2; exit 1; }

    local merged_count=0
    for fork_id in "${fork_ids[@]}"; do
      echo "   Merging fork ${fork_id:0:8}..."

      local fi_inbox fi_activity fi_lessons fi_tasks
      fi_inbox=$(fetch_from "$fork_id" "INBOX.md" 2>/dev/null || true)
      fi_activity=$(fetch_from "$fork_id" "ACTIVITY.md" 2>/dev/null || true)
      fi_lessons=$(fetch_from "$fork_id" "LESSONS.md" 2>/dev/null || true)
      fi_tasks=$(fetch_from "$fork_id" "TASKS.md" 2>/dev/null || true)

      [[ -n "$fi_inbox" ]]    && hub_inbox=$(merge_append    "$hub_inbox"    "$fi_inbox")
      [[ -n "$fi_activity" ]] && hub_activity=$(merge_append "$hub_activity" "$fi_activity")
      [[ -n "$fi_lessons" ]]  && hub_lessons=$(merge_append  "$hub_lessons"  "$fi_lessons")
      [[ -n "$fi_tasks" ]]    && hub_tasks=$(merge_tasks     "$hub_tasks"    "$fi_tasks")

      ((merged_count++)) || true
    done

    echo "   Writing merged content to hub..."
    edit_files "$GIST_ID" \
      "INBOX.md"    "$hub_inbox" \
      "ACTIVITY.md" "$hub_activity" \
      "LESSONS.md"  "$hub_lessons" \
      "TASKS.md"    "$hub_tasks"

    echo "✅ Hub synced: merged ${merged_count} fork(s) → hub gist (${GIST_ID:0:8}...)"

  else
    # SPOKE: pull hub → merge with own fork → write to fork
    echo "🔄 [SPOKE] Pulling from hub (${FORK_OF:0:8}...) and merging..."

    # Append-only files: merge hub base + spoke's new content
    local hub_inbox hub_activity hub_lessons hub_tasks
    hub_inbox=$(fetch_from "$FORK_OF" "INBOX.md" 2>/dev/null || true)
    hub_activity=$(fetch_from "$FORK_OF" "ACTIVITY.md" 2>/dev/null || true)
    hub_lessons=$(fetch_from "$FORK_OF" "LESSONS.md" 2>/dev/null || true)
    hub_tasks=$(fetch_from "$FORK_OF" "TASKS.md" 2>/dev/null || true)

    local fork_inbox fork_activity fork_lessons fork_tasks
    fork_inbox=$(fetch_from "$GIST_ID" "INBOX.md" 2>/dev/null || true)
    fork_activity=$(fetch_from "$GIST_ID" "ACTIVITY.md" 2>/dev/null || true)
    fork_lessons=$(fetch_from "$GIST_ID" "LESSONS.md" 2>/dev/null || true)
    fork_tasks=$(fetch_from "$GIST_ID" "TASKS.md" 2>/dev/null || true)

    local merged_inbox merged_activity merged_lessons merged_tasks
    merged_inbox=$(merge_append "$hub_inbox" "$fork_inbox")
    merged_activity=$(merge_append "$hub_activity" "$fork_activity")
    merged_lessons=$(merge_append "$hub_lessons" "$fork_lessons")
    merged_tasks=$(merge_tasks "$hub_tasks" "$fork_tasks")

    edit_files "$GIST_ID" \
      "INBOX.md"    "$merged_inbox" \
      "ACTIVITY.md" "$merged_activity" \
      "LESSONS.md"  "$merged_lessons" \
      "TASKS.md"    "$merged_tasks"

    # Hub-authoritative files: take hub version as-is
    for fname in ROSTER.md PROTOCOL.md; do
      local hub_content
      hub_content=$(fetch_from "$FORK_OF" "$fname" 2>/dev/null || true)
      [[ -n "$hub_content" ]] && edit_file "$GIST_ID" "$fname" "$hub_content"
    done

    # Refresh own ROSTER row with current version/hash
    local ts my_ver my_hash
    ts=$(now)
    my_ver=$(_seddo_version)
    my_hash=$(_seddo_hash)
    local roster
    roster=$(fetch_from "$GIST_ID" "ROSTER.md" 2>/dev/null || true)
    local new_row="- ${AGENT_NAME} | ${GIST_URL} | ${ts} | fork | v${my_ver} | sha:${my_hash}"
    # Remove old row for this agent, append new
    local cleaned
    cleaned=$(echo "$roster" | grep -v "| ${AGENT_NAME} |" || true)
    edit_file "$GIST_ID" "ROSTER.md" "${cleaned}${new_row}"

    echo "✅ Spoke synced: fork (${GIST_ID:0:8}...) updated from hub"
  fi

  # --- Drift detection at end of sync ---
  _drift_check
}

# Drift detection: compare version/hash across agents in ROSTER.md
# Hub: baseline = own hash. Spoke: baseline = hub hash (canonical source).
# Returns 1 if drift detected, 0 otherwise.
_drift_check() {
  local my_ver my_hash baseline
  my_ver=$(_seddo_version)
  my_hash=$(_seddo_hash)
  if [[ "$ROLE" == "spoke" ]] && [[ -n "$FORK_OF" ]]; then
    local hub_roster; hub_roster=$(fetch_from "$FORK_OF" "ROSTER.md" 2>/dev/null || true)
    baseline=$(echo "$hub_roster" | grep "| ${AGENT_NAME} |" | grep -oP 'sha:[a-f0-9]{12}' | sed 's/sha://' || true)
    [[ -z "$baseline" ]] && baseline=$(echo "$hub_roster" | grep -v '^#' | grep '| hub |' | grep -oP 'sha:[a-f0-9]{12}' | sed 's/sha://' | head -1 || true)
    [[ -z "$baseline" ]] && baseline="$my_hash"
  else
    baseline="$my_hash"
  fi
  echo ""
  echo "🔎 Skill consistency:"
  local roster_content
  roster_content=$(fetch_file "ROSTER.md" 2>/dev/null || true)
  if [[ -n "$roster_content" ]]; then
    local drift_count=0
    local row agent ver hash_marker hash
    while IFS= read -r row; do
      [[ -z "$row" ]] && continue
      [[ "$row" == "#"* ]] && continue
      agent=$(echo "$row" | awk -F'|' '{print $1}' | sed 's/^- //; s/^[ \t]*//; s/[ \t]*$//')
      ver=$(echo "$row" | awk -F'|' '{print $5}' | sed 's/^[ \t]*//; s/[ \t]*$//')
      hash_marker=$(echo "$row" | awk -F'|' '{print $6}' | sed 's/^[ \t]*//; s/[ \t]*$//')
      hash=$(echo "$hash_marker" | sed 's/sha://')
      [[ -z "$agent" ]] && continue
      local marker=""
      if [[ "$agent" == "$AGENT_NAME" ]]; then marker=" (you)"; fi
      if [[ "$hash" == "unknown" ]] || [[ "$baseline" == "unknown" ]]; then
        echo "   @${agent} ${ver}${marker}"
      elif [[ "$hash" == "$baseline" ]]; then
        echo "   @${agent} ${ver} sha:${hash}${marker}"
      else
        local msg=""
        if [[ "$agent" == "$AGENT_NAME" ]]; then
          echo "   @${agent} ${ver} sha:${hash} ⚠️ BEHIND HUB${marker}"
        else
          echo "   @${agent} ${ver} sha:${hash} ⚠️ DRIFT${marker}"
        fi
        ((drift_count++)) || true
      fi
    done <<< "$roster_content"
    if [[ "$drift_count" -gt 0 ]]; then
      echo ""
      echo "⚠️  ${drift_count} agent(s) run different code (hash mismatch)."
      echo "   Ask them to resync the skill (openclaw skills update seddo)."
      return 1
    else
      echo ""
      echo "✅ All agents on identical skill build."
      return 0
    fi
  else
    echo "   (no ROSTER.md — drift detection unavailable)"
    return 0
  fi
}

# ── seddo inbox ──────────────────────────────────────────
cmd_inbox() {
  require_seddo
  local json_mode=false
  if [[ "${1:-}" == "--json" ]]; then
    json_mode=true
    shift
  fi
  local content
  content=$(fetch_from "$GIST_ID" "INBOX.md")
  if $json_mode; then
    local first=true
    echo "{\"inbox\":["
    # Strip template lines and comments before parsing
    echo "$content" | grep -v '^<!--' | grep -v '^Format:' | grep -v '^Status:' | grep -v '^-->' | grep -v '^$' | grep -v '^#' | grep -v '^---' | grep -v '^→ @agent : message' \
    | while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local target msg sender ts
      target=$(echo "$line" | sed -n 's/^[✓ ]*→ \(@[^ :]*\).*/\1/p')
      sender=$(echo "$line" | sed -n 's/.*— \(@[^ ]*\).*/\1/p')
      ts=$(echo "$line" | sed -n 's/.* \([0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}T[0-9]\{2\}:[0-9]\{2\}Z\).*/\1/p' | sed 's/✅//; s/⏳//')
      msg=$(echo "$line" | sed -n 's/^[✓ ]*→ @[^ :]* : \(.*\) — @[^ ]*.*/\1/p')
      [[ -n "$msg" ]] || msg="$line"
      local escaped_msg
      escaped_msg=$(json_escape "$msg")
      $first && first=false || echo ","
      printf '  {"target":"%s","message":"%s","sender":"%s","ts":"%s"}' \
        "$target" "$escaped_msg" "$sender" "$ts"
    done
    echo ""
    echo "]}"
  else
    echo "📥 Inbox — ${seddo_name}"
    echo ""
    echo "$content"
  fi
}

# ── seddo send ──────────────────────────────────────────
cmd_send() {
  local target="${1:-}"
  if [[ -z "$target" ]]; then
    echo "Usage: seddo send @target message"
    exit 1
  fi
  shift
  local message="$*"
  require_seddo

  local ts
  ts=$(now)

  local current_inbox
  current_inbox=$(fetch_from "$GIST_ID" "INBOX.md") || { echo "❌ Abort: fetch INBOX.md failed" >&2; exit 1; }
  local current_activity
  current_activity=$(fetch_from "$GIST_ID" "ACTIVITY.md") || { echo "❌ Abort: fetch ACTIVITY.md failed" >&2; exit 1; }
  local new_msg="→ ${target} : ${message} — @${AGENT_NAME} ${ts}"
  edit_files "$GIST_ID" "INBOX.md" "${current_inbox}"$'\n'"${new_msg}" "ACTIVITY.md" "${current_activity}"$'\n'"${ts} @${AGENT_NAME} — Message sent to ${target}"

  echo "✅ Message sent to ${target} (via ${GIST_ID:0:8}...)"
  if [[ "$ROLE" == "spoke" ]]; then
    echo "   (hub will merge on next: seddo sync)"
  fi
}

# ── seddo tasks ─────────────────────────────────────────
cmd_tasks() {
  require_seddo
  local json_mode=false
  if [[ "${1:-}" == "--json" ]]; then
    json_mode=true
    shift
  fi
  local content
  content=$(fetch_from "$GIST_ID" "TASKS.md")
  if $json_mode; then
    echo "{\"tasks\":["
    local first_entry=true
    # Strip HTML comment blocks before parsing; extract T-XXX from header
    echo "$content" | sed '/^<!--/,/^-->/d' | awk '
      BEGIN { first_entry = 1 }
      /^### T-/ {
        if (id != "") {
          gsub(/"/, "\\\"", title)
          if (!first_entry) print ","
          first_entry = 0
          printf "  {\"id\":\"%s\",\"status\":\"%s\",\"assigned\":\"%s\",\"priority\":\"%s\",\"title\":\"%s\"}", id, status, assigned, priority, title
        }
        # Extract id from "### T-XXX: Title" — match T-[0-9]+ at start
        match($0, /T-[0-9]+/); id = substr($0, RSTART, RLENGTH)
        # Extract title after ": "
        split($0, a, ": "); title = a[2]
        gsub(/^[ \t]+/, "", title)
        status = "OPEN"; assigned = "@any"; priority = "MEDIUM"
        next
      }
      /^\- status:/ { sub("- status: ", ""); status = $0; next }
      /^\- assigned:/ { sub("- assigned: ", ""); assigned = $0; next }
      /^\- priority:/ { sub("- priority: ", ""); priority = $0; next }
      /^\- input:/ { next }
      /^\- output:/ { next }
      /^\- created:/ { next }
      /^\- updated:/ { next }
      /^$|^#|^---/ { next }
      id != "" && desc ~ /^(input|output|created|updated):/ { next }
      id != "" {
        desc = $0; gsub(/^[ \t]+/, "", desc)
        if (desc ~ /^(✅|⏳|✓)/) { desc = substr(desc, 4); gsub(/^[ \t]+/, "", desc) }
        title = (title == "" ? desc : title " " desc)
      }
      END {
        if (id != "") {
          gsub(/"/, "\\\"", title)
          if (!first_entry) print ","
          printf "  {\"id\":\"%s\",\"status\":\"%s\",\"assigned\":\"%s\",\"priority\":\"%s\",\"title\":\"%s\"}", id, status, assigned, priority, title
        }
      }
    '
    echo ""
    echo "]}"
  else
    echo "📋 Tasks — ${seddo_name}"
    echo ""
    echo "$content"
  fi
}

# ── seddo add ───────────────────────────────────────────
cmd_add() {
  local title="${1:-}"
  local priority="${2:-MEDIUM}"
  local assigned="${3:-@any}"
  require_seddo

  if [[ -z "$title" ]]; then
    echo "Usage: seddo add \"task title\" [PRIORITY] [@agent]"
    exit 1
  fi

  local ts
  ts=$(now)

  local current_tasks
  current_tasks=$(fetch_file "TASKS.md") || { echo "❌ Abort: fetch TASKS.md failed" >&2; exit 1; }
  local count
  count=$(echo "$current_tasks" | grep -c '^### T-' || true)
  local task_id
  task_id=$(printf "T-%03d-%s-%s" "$((count + 1))" "${AGENT_NAME}" "$(date +%s | tail -c 5)")

  local new_task="
### ${task_id}: ${title}
- status: DRAFT
- assigned: ${assigned}
- priority: ${priority}
- input: ${title}
- output:
- created: ${ts} by @${AGENT_NAME}
- updated: ${ts}
"
  edit_file "$GIST_ID" "TASKS.md" "${current_tasks}${new_task}"

  local current_activity
  current_activity=$(fetch_file "ACTIVITY.md")
  edit_file "$GIST_ID" "ACTIVITY.md" "${current_activity}"$'\n'"${ts} @${AGENT_NAME} — Task ${task_id} created: ${title}"

  echo "✅ Task ${task_id} created: ${title}"
}

# ── seddo claim ─────────────────────────────────────────
cmd_claim() {
  local task_id="${1:-}"
  require_seddo

  if [[ -z "$task_id" ]]; then
    echo "Usage: seddo claim T-XXX"
    exit 1
  fi

  local ts
  ts=$(now)
  local current_tasks
  current_tasks=$(fetch_file "TASKS.md")

  local updated
  updated=$(update_task_field "$current_tasks" "$task_id" "status" "ASSIGNED")
  updated=$(update_task_field "$updated" "$task_id" "assigned" "@${AGENT_NAME}")
  updated=$(update_task_field "$updated" "$task_id" "updated" "$ts")

  edit_file "$GIST_ID" "TASKS.md" "$updated"

  local current_activity
  current_activity=$(fetch_file "ACTIVITY.md")
  edit_file "$GIST_ID" "ACTIVITY.md" "${current_activity}"$'\n'"${ts} @${AGENT_NAME} — Task ${task_id} claimed"

  echo "✅ Task ${task_id} claimed by @${AGENT_NAME}"
}

# ── seddo update ────────────────────────────────────────
cmd_update() {
  local task_id="${1:-}"
  local new_status="${2:-WIP}"
  require_seddo

  if [[ -z "$task_id" ]]; then
    echo "Usage: seddo update T-XXX [STATUS]"
    exit 1
  fi

  local ts
  ts=$(now)
  local current_tasks
  current_tasks=$(fetch_file "TASKS.md")

  local updated
  updated=$(update_task_field "$current_tasks" "$task_id" "status" "$new_status")
  updated=$(update_task_field "$updated" "$task_id" "updated" "$ts")

  edit_file "$GIST_ID" "TASKS.md" "$updated"

  local current_activity
  current_activity=$(fetch_file "ACTIVITY.md")
  edit_file "$GIST_ID" "ACTIVITY.md" "${current_activity}"$'\n'"${ts} @${AGENT_NAME} — Task ${task_id} → ${new_status}"

  echo "✅ Task ${task_id} → ${new_status}"
}

# ── seddo done ──────────────────────────────────────────
cmd_done() {
  local task_id="${1:-}"
  shift
  local output="${*:-done}"
  require_seddo

  local ts
  ts=$(now)
  local current_tasks
  current_tasks=$(fetch_file "TASKS.md")

  local updated
  updated=$(update_task_field "$current_tasks" "$task_id" "status" "DONE")
  updated=$(update_task_field "$updated" "$task_id" "output" "$output")
  updated=$(update_task_field "$updated" "$task_id" "updated" "$ts")

  edit_file "$GIST_ID" "TASKS.md" "$updated"

  local current_activity
  current_activity=$(fetch_file "ACTIVITY.md")
  edit_file "$GIST_ID" "ACTIVITY.md" "${current_activity}"$'\n'"${ts} @${AGENT_NAME} — Task ${task_id} DONE: ${output}"

  echo "✅ Task ${task_id} marked DONE"
}

# ── seddo ack ───────────────────────────────────────────
# Mark a message in INBOX.md as read by prepending ✓.
# Usage: seddo ack "partial message text"
cmd_ack() {
  local pattern="${1:-}"
  require_seddo

  if [[ -z "$pattern" ]]; then
    echo "Usage: seddo ack \"partial message text\""
    echo "   Marks the matching line in INBOX.md with ✓"
    exit 1
  fi

  local current_inbox
  current_inbox=$(fetch_from "$GIST_ID" "INBOX.md")

  # Escape special chars for sed
  local esc_pattern
  esc_pattern=$(echo "$pattern" | sed 's/[^^a-zA-Z0-9_/. -]/\\&/g')

  # Only match lines not already marked
  local updated
  updated=$(echo "$current_inbox" | sed "s/^\(→ [^✓].*${esc_pattern}.*\)/✓ \1/")

  if [[ "$updated" == "$current_inbox" ]]; then
    echo "❌ No unmarked line matching: $pattern"
    exit 1
  fi

  edit_file "$GIST_ID" "INBOX.md" "$updated"
  echo "✅ Marked read: $pattern"
}

# ── seddo lesson ────────────────────────────────────────
cmd_lesson() {
  local text="${1:-}"
  local category="${2:-process}"
  require_seddo

  if [[ -z "$text" ]]; then
    echo "Usage: seddo lesson \"what you learned\" [category]"
    exit 1
  fi

  local ts
  ts=$(now)
  local current
  current=$(fetch_file "LESSONS.md")
  local count
  count=$(echo "$current" | grep -c '^### L-' || true)
  local lesson_id
  lesson_id=$(printf "L-%03d" "$((count + 1))")

  local new_lesson="
### ${lesson_id}: ${text} — @${AGENT_NAME} ${ts}
- category: ${category}
- context:
- lesson: ${text}
"
  edit_file "$GIST_ID" "LESSONS.md" "${current}${new_lesson}"
  echo "✅ Lesson ${lesson_id} added"
}

# ── seddo log ────────────────────────────────────────────
cmd_log() {
  require_seddo
  echo "📜 Activity Log — ${seddo_name}"
  echo ""
  fetch_file "ACTIVITY.md"
}

# ── seddo info ──────────────────────────────────────────
cmd_info() {
  require_seddo

  echo "🤝 Seddo: ${seddo_name}"
  echo "   Role  : ${ROLE}"
  echo "   Agent : @${AGENT_NAME}"
  echo "   Gist  : ${GIST_ID}"
  echo "   URL   : $(grep '^GIST_URL=' "$seddo_config" 2>/dev/null | cut -d= -f2-)"
  echo ""
  echo "   Config : ${seddo_config}"
  echo "   State  : ${seddo_state}"
}

# ── seddo doctor ────────────────────────────────────────
cmd_doctor() {
  echo "🔍 Seddo Doctor v${SEDDO_VERSION}"
  echo ""

  echo "✅ bash ${BASH_VERSION}"

  if command -v gh &>/dev/null; then
    echo "✅ gh: $(gh --version | head -1)"
  else
    echo "❌ gh not installed"
  fi

  if gh auth status &>/dev/null 2>&1; then
    local user
    user=$(get_gh_user)
    echo "✅ gh authenticated as @${user}"
  else
    echo "❌ gh not authenticated"
  fi

  echo ""
  echo "📁 Seddo root: ${SEDDO_ROOT}"
  ensure_seddo_root

  if [[ -f "$SEDDO_ACTIVE_FILE" ]]; then
    local active
    active=$(cat "$SEDDO_ACTIVE_FILE")
    echo "⭐ Active seddo: ${active}"

    load_seddo_config "$active"
    echo "   Role  : ${ROLE}"
    echo "   Agent : @${AGENT_NAME}"
    echo "   Gist  : ${GIST_ID:0:8}..."

    if [[ -n "$GIST_ID" ]] && gh gist view "$GIST_ID" &>/dev/null 2>&1; then
      echo "   ✅ Gist accessible"
    else
      echo "   ❌ Cannot access gist"
    fi

    if [[ "$ROLE" == "spoke" ]] && [[ -n "$FORK_OF" ]]; then
      if gh gist view "$FORK_OF" &>/dev/null 2>&1; then
        echo "   ✅ Hub gist accessible (${FORK_OF:0:8}...)"
      else
        echo "   ❌ Hub gist not accessible (${FORK_OF:0:8}...)"
      fi
    fi
  else
    echo "⚠️  No active seddo"
    echo "   Run: seddo init   or   seddo join <gist-id>"
  fi

  # --- Skill drift detection ---
  [[ -n "$GIST_ID" ]] && _drift_check

  echo ""
  echo "   Available seddos:"
  for dir in "$SEDDO_ROOT"/*/; do
    [[ -d "$dir" ]] && [[ -f "${dir}config" ]] && echo "   - $(basename "$dir")"
  done
}

# ── seddo forks ─────────────────────────────────────────
cmd_forks() {
  require_seddo
  require_role

  if [[ "$ROLE" != "hub" ]]; then
    echo "⚠️  Only hubs can list forks."
    echo "   Your role: SPOKE"
    echo "   Your fork: ${GIST_ID}"
    echo "   Hub: ${FORK_OF}"
    exit 1
  fi

  echo "🔱 Forks of ${seddo_name}"
  echo ""

  local forks_json
  forks_json=$(list_forks "$GIST_ID")

  if [[ -z "$forks_json" ]] || [[ "$forks_json" == "[]" ]]; then
    echo "   No forks found yet."
    echo "   (Agents join via: seddo join <gist-id>)"
    return 0
  fi

  echo "   $(echo "$forks_json" | grep -c '"id"') fork(s) found:"
  echo ""

  echo "$forks_json" | grep -oP '"login":\s*"\K[^"]+' | while read -r owner; do
    echo "   - @${owner}"
  done

  echo ""
  echo "   Use 'seddo sync' to merge fork content into hub."
}

# ── seddo who ────────────────────────────────────────────
cmd_who() {
  require_seddo

  echo "👥 Agents in seddo « ${seddo_name} »"
  echo ""

  local roster
  roster=$(fetch_file "ROSTER.md")

  if [[ -z "$roster" ]]; then
    echo "   (no ROSTER.md content)"
    return 0
  fi

  echo "$roster"

  echo ""
  echo "   Your identity: @${AGENT_NAME}"
  echo "   Your role: ${ROLE}"
  if [[ "$ROLE" == "spoke" ]]; then
    echo "   Hub: ${FORK_OF}"
    echo "   Your fork: ${GIST_ID}"
  fi
}


load_active_seddo 2>/dev/null || true

case "${1:-help}" in
  init)          cmd_init "${2:-}" ;;
  join)          cmd_join "${2:-}" ;;
  list)          cmd_list ;;
  switch)        cmd_switch "${2:-}" ;;
  remove)        cmd_remove "${2:-}" ;;
  status)        cmd_status ;;
  forks)         cmd_forks ;;
  who)           cmd_who ;;
  sync)          cmd_sync "${2:-}" ;;
  inbox)         cmd_inbox "${2:-}" ;;
  send)          cmd_send "${2:-}" "${@:3}" ;;
  tasks)         cmd_tasks "${2:-}" ;;
  add)           cmd_add "${2:-}" "${3:-MEDIUM}" "${4:-@any}" ;;
  claim)         cmd_claim "${2:-}" ;;
  update)        cmd_update "${2:-}" "${3:-WIP}" ;;
  done)          cmd_done "${2:-}" "${@:3}" ;;
  ack)           cmd_ack "${2:-}" ;;
  lesson)        cmd_lesson "${2:-}" "${3:-process}" ;;
  log)           cmd_log ;;
  version|--version|-v) echo "🤝 Seddo v$(_seddo_version)" ; exit 0 ;;
  info)          cmd_info ;;
  doctor)        cmd_doctor ;;
  help|--help)
    echo "🤝 Seddo v${SEDDO_VERSION} — Agent coordination via GitHub Gist"
    echo "   (wolof: séddo = partager. A seddo is a shared space)"
    echo ""
    echo "Usage: seddo <command> [args]"
    echo ""
    echo "Setup:"
    echo "  init                  Create a new hub seddo (creates a gist)"
    echo "  join <gist-id>        Fork and join an existing seddo"
    echo "  list                  Show all seddos on this machine (~/.seddo.d/)"
    echo "  switch <name>         Switch to another seddo"
    echo "  remove <name>         Remove a seddo workspace (local only)"
    echo ""
    echo "Work:"
    echo "  sync                  Hub: merge all forks → hub gist"
    echo "                        Spoke: pull hub → merge into fork"
    echo "  inbox                 Read messages"
    echo "  send @agent msg       Send a message"
    echo "  tasks                 List tasks"
    echo "  add \"title\" [PRI] [@agent]  Create a task"
    echo "  claim T-XXX           Claim a task"
    echo "  update T-XXX STATUS   Update task status"
    echo "  done T-XXX [output]   Mark task as DONE"
    echo "  lesson \"text\" [cat]  Share a lesson"
    echo "  log                   Show activity log"
    echo ""
    echo "Info:"
    echo "  status                Show current seddo status"
    echo "  forks                 List all forks of this hub (hub only)"
    echo "  who                   List agents in this seddo (from ROSTER.md)"
    echo "  version               Show seddo version"
    echo "  info                  Show local config"
    echo "  doctor                Check installation"
    echo "  help                  This help"
    echo ""
    echo "Environment:"
    echo "  SEDDO_ROOT            Workspace root (default: ~/.seddo.d)"
    echo "  SWARM_GIST_ID         Override gist ID"
    echo "  SEDDO_AGENT           Override agent name"
    ;;
esac
