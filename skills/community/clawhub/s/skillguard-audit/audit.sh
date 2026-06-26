#!/usr/bin/env bash
set -euo pipefail

API_URL="https://api.agentsouls.io/api/audit"

usage() {
  echo "Usage: audit.sh --name <skill-slug> | --code <file>"
  echo ""
  echo "Modes:"
  echo "  --name <slug>   Fetch skill from ClawHub and audit"
  echo "  --code <file>   Audit a local file"
  exit 1
}

audit_code() {
  local code="$1"
  local source="${2:-local}"

  response=$(curl -sf -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg code "$code" --arg source "$source" \
      '{code: $code, source: $source}')" 2>&1) || {
    # If API is unreachable or returns error, provide fallback
    echo '{"verdict":"UNKNOWN","riskScore":-1,"threats":["API unreachable or returned error"],"raw":"'"$(echo "$response" | head -c 200)"'"}'
    return 1
  }

  echo "$response" | jq '{verdict, riskScore, threats}' 2>/dev/null || echo "$response"
}

# Parse args
MODE=""
VALUE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) MODE="name"; VALUE="$2"; shift 2 ;;
    --code) MODE="code"; VALUE="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

[[ -z "$MODE" ]] && usage

if [[ "$MODE" == "name" ]]; then
  echo "🛡️ Fetching skill '$VALUE' from ClawHub..."

  # Get file list
  files=$(clawhub inspect "$VALUE" --files --json 2>/dev/null) || {
    echo "❌ Could not fetch skill '$VALUE' from ClawHub"
    exit 1
  }

  # Collect code from SKILL.md and any .sh/.js/.py/.ts files
  code=""

  for fname in SKILL.md $(echo "$files" | jq -r '.files[]?.path // empty' 2>/dev/null | grep -E '\.(sh|js|ts|py|md)$'); do
    content=$(clawhub inspect "$VALUE" --file "$fname" 2>/dev/null) || continue
    code+="--- FILE: $fname ---"$'\n'"$content"$'\n\n'
  done

  if [[ -z "$code" ]]; then
    echo "❌ No auditable files found for '$VALUE'"
    exit 1
  fi

  echo "🔍 Auditing..."
  audit_code "$code" "clawhub:$VALUE"

elif [[ "$MODE" == "code" ]]; then
  [[ ! -f "$VALUE" ]] && { echo "❌ File not found: $VALUE"; exit 1; }

  echo "🔍 Auditing file: $VALUE"
  code=$(cat "$VALUE")
  audit_code "$code" "local:$VALUE"
fi
