#!/usr/bin/env bash
# RepoRead REST API helper — fallback when MCP server is not configured
# Requires: REPOREAD_API_KEY environment variable

set -euo pipefail

API_KEY="${REPOREAD_API_KEY:-}"
BASE_URL="https://api.reporead.com/public/v1"

if [ -z "$API_KEY" ]; then
  echo "Error: REPOREAD_API_KEY is not set."
  echo "Get an API key at https://www.reporead.com/settings"
  echo "Then run: export REPOREAD_API_KEY=\"rrk_your_key_here\""
  exit 1
fi

auth_header="Authorization: Bearer $API_KEY"

# Sanitize a value for safe JSON string embedding.
# Escapes backslashes, double quotes, and rejects control characters
# including $, `, and newlines that could enable command substitution.
sanitize_json_value() {
  local val="$1"
  if [[ "$val" =~ [\$\`\&\;\|\>\<\!\\n\\r] ]]; then
    echo "Error: Input contains unsafe characters." >&2
    exit 1
  fi
  # Escape backslashes first, then double quotes
  val="${val//\\/\\\\}"
  val="${val//\"/\\\"}"
  printf '%s' "$val"
}

# Validate that a value is safe for use in a URL path segment.
# Only allows alphanumeric characters, hyphens, and underscores.
validate_path_segment() {
  local val="$1"
  if ! [[ "$val" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: Invalid ID format. IDs must contain only alphanumeric characters, hyphens, and underscores." >&2
    exit 1
  fi
  printf '%s' "$val"
}

usage() {
  echo "Usage: reporead-api.sh <command> [args]"
  echo ""
  echo "Commands:"
  echo "  balance                          Check token balance"
  echo "  repos                            List imported repositories"
  echo "  import <github_url>              Import a GitHub repository"
  echo "  analyze <repo_id> <type>         Start analysis (types: readme, technical, security, mermaid, llmstxt)"
  echo "  status <analysis_id>             Check analysis status"
  echo "  results <analysis_id>            Get full analysis results"
  exit 1
}

cmd="${1:-}"
[ -z "$cmd" ] && usage

case "$cmd" in
  balance)
    curl -sf -H "$auth_header" "$BASE_URL/tokens/balance"
    ;;
  repos)
    page="${2:-1}"
    if ! [[ "$page" =~ ^[0-9]+$ ]]; then
      echo "Error: Page must be a number." >&2
      exit 1
    fi
    curl -sf -H "$auth_header" "$BASE_URL/repositories?page=$page&per_page=20"
    ;;
  import)
    url="${2:-}"
    [ -z "$url" ] && { echo "Error: GitHub URL required. Usage: reporead-api.sh import <github_url>"; exit 1; }
    safe_url=$(sanitize_json_value "$url")
    json_body=$(printf '{"github_url": "%s"}' "$safe_url")
    curl -sf -X POST -H "$auth_header" -H "Content-Type: application/json" \
      -d "$json_body" "$BASE_URL/repositories"
    ;;
  analyze)
    repo_id="${2:-}"
    analysis_type="${3:-}"
    [ -z "$repo_id" ] || [ -z "$analysis_type" ] && { echo "Error: Usage: reporead-api.sh analyze <repo_id> <type>"; exit 1; }
    safe_repo_id=$(sanitize_json_value "$repo_id")
    safe_type=$(sanitize_json_value "$analysis_type")
    json_body=$(printf '{"repository_id": "%s", "analysis_type": "%s"}' "$safe_repo_id" "$safe_type")
    curl -sf -X POST -H "$auth_header" -H "Content-Type: application/json" \
      -d "$json_body" "$BASE_URL/analyses"
    ;;
  status)
    analysis_id="${2:-}"
    [ -z "$analysis_id" ] && { echo "Error: Analysis ID required. Usage: reporead-api.sh status <analysis_id>"; exit 1; }
    safe_id=$(validate_path_segment "$analysis_id")
    curl -sf -H "$auth_header" "$BASE_URL/analyses/$safe_id/status"
    ;;
  results)
    analysis_id="${2:-}"
    [ -z "$analysis_id" ] && { echo "Error: Analysis ID required. Usage: reporead-api.sh results <analysis_id>"; exit 1; }
    safe_id=$(validate_path_segment "$analysis_id")
    curl -sf -H "$auth_header" "$BASE_URL/analyses/$safe_id"
    ;;
  *)
    echo "Unknown command: $cmd"
    usage
    ;;
esac
echo ""
