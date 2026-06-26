#!/usr/bin/env bash
set -euo pipefail

# Soul Searching — SOUL.md manager CLI
# Source: https://soulsearching.ai

CATALOG_URL="https://soulsearching.ai/souls.json"
SOUL_DIR="${HOME}/.openclaw/souls"
CATALOG_FILE="${SOUL_DIR}/.catalog.json"
WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"
SOUL_FILE="${WORKSPACE}/SOUL.md"
MAX_AGE=86400  # 24 hours in seconds

# ── Helpers ──

ensure_dir() {
  mkdir -p "$SOUL_DIR"
}

needs_refresh() {
  if [[ ! -f "$CATALOG_FILE" ]]; then
    return 0
  fi
  local now file_age age
  now=$(date +%s)
  if [[ "$(uname)" == "Darwin" ]]; then
    file_age=$(stat -f %m "$CATALOG_FILE")
  else
    file_age=$(stat -c %Y "$CATALOG_FILE")
  fi
  age=$((now - file_age))
  [[ $age -gt $MAX_AGE ]]
}

refresh_catalog() {
  ensure_dir
  local tmp="${CATALOG_FILE}.tmp"
  echo "📡 Fetching soul catalog from soulsearching.ai..." >&2
  if ! curl -sSfL "$CATALOG_URL" -o "$tmp" 2>/dev/null; then
    echo "❌ Failed to fetch catalog. Check your connection." >&2
    rm -f "$tmp"
    exit 1
  fi
  # Normalize: if top-level is array, wrap it; rename "soul" key → "content"
  python3 -c "
import json, sys
with open('$tmp') as f:
    data = json.load(f)
if isinstance(data, list):
    data = {'version': 1, 'source': 'https://soulsearching.ai', 'souls': data}
for s in data.get('souls', []):
    if 'soul' in s and 'content' not in s:
        s['content'] = s.pop('soul')
with open('$CATALOG_FILE', 'w') as f:
    json.dump(data, f, indent=2)
print(len(data.get('souls', [])))
" > /dev/null
  local count
  count=$(jq '.souls | length' "$CATALOG_FILE")
  rm -f "$tmp"
  echo "✅ Catalog updated ($count souls)" >&2
}

ensure_catalog() {
  ensure_dir
  if needs_refresh; then
    refresh_catalog
  fi
}

get_soul_json() {
  local id="$1"
  jq -r --arg id "$id" '.souls[] | select(.id == $id)' "$CATALOG_FILE"
}

# ── Commands ──

cmd_browse() {
  ensure_catalog
  local category="${1:-}"
  
  if [[ -n "$category" ]]; then
    echo "🔮 Souls in category: $category"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    jq -r --arg cat "$category" '
      .souls[] | select(.category == $cat) |
      "  \(.id) — \(.name)\n    \(.description)\n    ⭐ \(.stars) | tags: \(.tags | join(", "))\n"
    ' "$CATALOG_FILE"
  else
    echo "🔮 All available souls"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    for cat in professional creative technical funny specialized; do
      local count
      count=$(jq -r --arg cat "$cat" '[.souls[] | select(.category == $cat)] | length' "$CATALOG_FILE")
      if [[ "$count" -gt 0 ]]; then
        echo ""
        echo "📂 $(echo "$cat" | tr '[:lower:]' '[:upper:]') ($count)"
        jq -r --arg cat "$cat" '
          .souls[] | select(.category == $cat) |
          "  \(.id) — \(.name) (⭐ \(.stars))\n    \(.description)\n"
        ' "$CATALOG_FILE"
      fi
    done
  fi
  
  local total
  total=$(jq '.souls | length' "$CATALOG_FILE")
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Total: $total souls | Install: soul.sh install <id>"
}

cmd_search() {
  ensure_catalog
  local query="${1:-}"
  
  if [[ -z "$query" ]]; then
    echo "Usage: soul.sh search <query>" >&2
    exit 1
  fi
  
  echo "🔍 Searching for: $query"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  local results
  results=$(jq -r --arg q "$query" '
    .souls[] | select(
      (.id | ascii_downcase | contains($q | ascii_downcase)) or
      (.name | ascii_downcase | contains($q | ascii_downcase)) or
      (.description | ascii_downcase | contains($q | ascii_downcase)) or
      (.category | ascii_downcase | contains($q | ascii_downcase)) or
      (.tags[] | ascii_downcase | contains($q | ascii_downcase))
    ) |
    "  \(.id) — \(.name) [\(.category)]\n    \(.description)\n    ⭐ \(.stars) | tags: \(.tags | join(", "))\n"
  ' "$CATALOG_FILE")
  
  if [[ -z "$results" ]]; then
    echo "  No souls found matching '$query'"
    echo "  Try: soul.sh browse (to see all)"
  else
    echo "$results"
  fi
}

cmd_install() {
  ensure_catalog
  local id="${1:-}"
  local activate=false
  
  if [[ -z "$id" ]]; then
    echo "Usage: soul.sh install <soul-id> [--activate]" >&2
    exit 1
  fi
  
  # Check for --activate flag
  shift
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --activate) activate=true ;;
    esac
    shift
  done
  
  # Fetch soul data
  local soul_json
  soul_json=$(get_soul_json "$id")
  
  if [[ -z "$soul_json" ]]; then
    echo "❌ Soul '$id' not found in catalog." >&2
    echo "   Run: soul.sh browse (to see available souls)" >&2
    exit 1
  fi
  
  local name
  name=$(echo "$soul_json" | jq -r '.name')
  local content
  content=$(echo "$soul_json" | jq -r '.content')
  
  # Save to local store
  echo "$content" > "${SOUL_DIR}/${id}.md"
  echo "✅ Installed: $name → ~/.openclaw/souls/${id}.md"
  
  if [[ "$activate" == true ]]; then
    cmd_switch "$id"
  fi
}

cmd_switch() {
  local id="${1:-}"
  
  if [[ -z "$id" ]]; then
    echo "Usage: soul.sh switch <soul-id>" >&2
    echo "  Installed souls:" >&2
    cmd_list
    exit 1
  fi
  
  local soul_path="${SOUL_DIR}/${id}.md"
  
  if [[ ! -f "$soul_path" ]]; then
    echo "❌ Soul '$id' is not installed locally." >&2
    echo "   Run: soul.sh install $id" >&2
    exit 1
  fi
  
  # Backup current SOUL.md if it exists
  if [[ -f "$SOUL_FILE" ]]; then
    cp "$SOUL_FILE" "${SOUL_FILE}.bak"
    echo "📋 Backed up current SOUL.md → SOUL.md.bak"
  fi
  
  # Copy soul into place
  cp "$soul_path" "$SOUL_FILE"
  
  local name
  name=$(head -1 "$soul_path" | sed 's/^# SOUL.md — //' | sed 's/^# //')
  echo "🔮 Switched to: $name"
  echo "   Active at: $SOUL_FILE"
}

cmd_list() {
  ensure_dir
  
  local count=0
  local current_id=""
  
  # Detect current soul
  if [[ -f "$SOUL_FILE" ]]; then
    current_id=$(head -1 "$SOUL_FILE" | sed 's/^# SOUL.md — //' | sed 's/^# //')
  fi
  
  echo "📦 Installed souls (~/.openclaw/souls/)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  for f in "$SOUL_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    local basename
    basename=$(basename "$f" .md)
    local title
    title=$(head -1 "$f" | sed 's/^# SOUL.md — //' | sed 's/^# //')
    
    local marker=""
    if [[ "$title" == "$current_id" ]]; then
      marker=" ← active"
    fi
    
    echo "  ${basename} — ${title}${marker}"
    count=$((count + 1))
  done
  
  if [[ $count -eq 0 ]]; then
    echo "  (none installed)"
    echo "  Run: soul.sh browse (to discover souls)"
  fi
  echo ""
  echo "Total: $count installed"
}

cmd_current() {
  if [[ ! -f "$SOUL_FILE" ]]; then
    echo "No SOUL.md found at $SOUL_FILE"
    exit 0
  fi
  
  local title
  title=$(head -1 "$SOUL_FILE" | sed 's/^# SOUL.md — //' | sed 's/^# //')
  echo "🔮 Current soul: $title"
  echo "   File: $SOUL_FILE"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  head -20 "$SOUL_FILE"
  echo "..."
}

cmd_uninstall() {
  local id="${1:-}"
  
  if [[ -z "$id" ]]; then
    echo "Usage: soul.sh uninstall <soul-id>" >&2
    exit 1
  fi
  
  local soul_path="${SOUL_DIR}/${id}.md"
  
  if [[ ! -f "$soul_path" ]]; then
    echo "❌ Soul '$id' is not installed." >&2
    exit 1
  fi
  
  local name
  name=$(head -1 "$soul_path" | sed 's/^# SOUL.md — //' | sed 's/^# //')
  rm "$soul_path"
  echo "🗑️  Uninstalled: $name"
}

cmd_refresh() {
  refresh_catalog
}

# ── Main ──

cmd="${1:-help}"
shift 2>/dev/null || true

case "$cmd" in
  browse)     cmd_browse "$@" ;;
  search)     cmd_search "$@" ;;
  install)    cmd_install "$@" ;;
  switch)     cmd_switch "$@" ;;
  list)       cmd_list ;;
  current)    cmd_current ;;
  uninstall)  cmd_uninstall "$@" ;;
  refresh)    cmd_refresh ;;
  help|--help|-h)
    echo "🔮 Soul Searching — SOUL.md Manager"
    echo ""
    echo "Usage: soul.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  browse [category]        Browse available souls"
    echo "  search <query>           Search by name, description, or tag"
    echo "  install <id> [--activate]  Download and optionally activate a soul"
    echo "  switch <id>              Switch to an installed soul"
    echo "  list                     Show installed souls"
    echo "  current                  Show the active SOUL.md"
    echo "  uninstall <id>           Remove an installed soul"
    echo "  refresh                  Re-download the catalog"
    echo ""
    echo "Examples:"
    echo "  soul.sh browse funny"
    echo "  soul.sh install dwight-mode --activate"
    echo "  soul.sh switch researcher"
    echo ""
    echo "Directory: https://soulsearching.ai"
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    echo "Run: soul.sh help" >&2
    exit 1
    ;;
esac
