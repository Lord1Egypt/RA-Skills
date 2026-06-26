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
    curl -sf -H "$auth_header" "$BASE_URL/repositories?page=$page&per_page=20"
    ;;
  import)
    url="${2:-}"
    [ -z "$url" ] && { echo "Error: GitHub URL required. Usage: reporead-api.sh import <github_url>"; exit 1; }
    curl -sf -X POST -H "$auth_header" -H "Content-Type: application/json" \
      -d "{\"github_url\": \"$url\"}" "$BASE_URL/repositories"
    ;;
  analyze)
    repo_id="${2:-}"
    analysis_type="${3:-}"
    [ -z "$repo_id" ] || [ -z "$analysis_type" ] && { echo "Error: Usage: reporead-api.sh analyze <repo_id> <type>"; exit 1; }
    curl -sf -X POST -H "$auth_header" -H "Content-Type: application/json" \
      -d "{\"repository_id\": \"$repo_id\", \"analysis_type\": \"$analysis_type\"}" "$BASE_URL/analyses"
    ;;
  status)
    analysis_id="${2:-}"
    [ -z "$analysis_id" ] && { echo "Error: Analysis ID required. Usage: reporead-api.sh status <analysis_id>"; exit 1; }
    curl -sf -H "$auth_header" "$BASE_URL/analyses/$analysis_id/status"
    ;;
  results)
    analysis_id="${2:-}"
    [ -z "$analysis_id" ] && { echo "Error: Analysis ID required. Usage: reporead-api.sh results <analysis_id>"; exit 1; }
    curl -sf -H "$auth_header" "$BASE_URL/analyses/$analysis_id"
    ;;
  *)
    echo "Unknown command: $cmd"
    usage
    ;;
esac
echo ""
