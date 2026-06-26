#!/usr/bin/env bash
# tc-memory — TruContext wrapper for OpenClaw agents
#
# Resolves agent config from ~/.trucontext/openclaw-state.json
# and executes the correct trucontext CLI command.
#
# Usage: tc-memory <verb> [args...]
#   tc-memory ingest "<text>" [--permanent]
#   tc-memory recall "<query>" [--limit N]
#   tc-memory query "<question>" [--limit N]
#   tc-memory gaps
#   tc-memory health
#   tc-memory node find "<name>"
#   tc-memory node create --type <type> --id <id> --name "<name>" [--permanent]
#   tc-memory node get <id>
#   tc-memory node link <id> --rel <REL> --to <id2>

set -euo pipefail

STATE_FILE="$HOME/.trucontext/openclaw-state.json"

# Wrapper around trucontext CLI that detects auth errors and surfaces
# a clear recovery message instead of a raw CLI error.
tc() {
  local output
  local exit_code
  output=$(trucontext "$@" 2>&1) && exit_code=$? || exit_code=$?
  if [ $exit_code -ne 0 ]; then
    if echo "$output" | grep -qiE "unauthorized|unauthenticated|token.*expired|not logged in|401|403"; then
      echo "ERROR: TruContext auth expired or invalid." >&2
      echo "Run: npx trucontext login" >&2
      exit 1
    fi
    echo "$output" >&2
    exit $exit_code
  fi
  echo "$output"
}

# --- Resolve agent config ---
# Try to detect which agent is calling based on CWD matching workspace paths
resolve_config() {
  if [ ! -f "$STATE_FILE" ]; then
    echo "ERROR: tc-memory not configured. Run: trucontext-openclaw install" >&2
    exit 1
  fi

  # Match CWD to a registered agent's workspace
  local cwd
  cwd=$(pwd)
  local agent_id root_node user_root primary_about

  # Use python to parse the state JSON and find matching agent
  read -r agent_id root_node user_root primary_about < <(python3 -c "
import json, sys, os
state = json.load(open('$STATE_FILE'))
cwd = '$cwd'
for aid, a in state.get('agents', {}).items():
    ws = a.get('workspace', '')
    if ws and cwd.startswith(ws):
        print(aid, a.get('root_node', aid), a.get('user_root', 'dustin'), a.get('primary_about', aid))
        sys.exit(0)
# Fallback: use first agent or default
agents = list(state.get('agents', {}).items())
if agents:
    aid, a = agents[0]
    print(aid, a.get('root_node', aid), a.get('user_root', 'dustin'), a.get('primary_about', aid))
else:
    print('unknown', 'unknown', state.get('user_root_node', 'dustin'), 'unknown')
")

  echo "$agent_id $root_node $user_root $primary_about"
}

# Parse config
IFS=' ' read -r AGENT_ID ROOT_NODE USER_ROOT PRIMARY_ABOUT < <(resolve_config)

VERB="${1:-}"
shift || true

case "$VERB" in

  ingest)
    TEXT="${1:-}"
    shift || true
    PERMANENT=false
    CONFIDENCE=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --permanent) PERMANENT=true; shift ;;
        --confidence) CONFIDENCE="$2"; shift 2 ;;
        *) shift ;;
      esac
    done

    ARGS=(ingest "$TEXT"
      --context "${ROOT_NODE}:BY"
      --context "${PRIMARY_ABOUT}:ABOUT"
    )
    if [ "$PERMANENT" = "true" ]; then
      ARGS+=(--no-temporal)
    fi
    if [ -n "$CONFIDENCE" ]; then
      ARGS+=(--confidence "$CONFIDENCE")
    fi
    tc "${ARGS[@]}"
    ;;

  recall)
    QUERY="${1:-recent context}"
    shift || true
    LIMIT=10
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --limit) LIMIT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    tc recall "$QUERY" --root "$ROOT_NODE" --limit "$LIMIT"
    ;;

  query)
    QUESTION="${1:-}"
    shift || true
    LIMIT=20
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --limit) LIMIT="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    tc query "$QUESTION" --root "$ROOT_NODE" --limit "$LIMIT"
    ;;

  gaps)
    tc curiosity list --root "$ROOT_NODE"
    ;;

  health)
    tc mind thoughts --limit 3
    ;;

  node)
    SUBCMD="${1:-}"
    shift || true
    case "$SUBCMD" in
      find)
        QUERY="${1:-}"
        tc graph search "$QUERY"
        ;;
      create)
        TYPE="" ID="" NAME="" PERMANENT=false
        while [[ $# -gt 0 ]]; do
          case "$1" in
            --type)  TYPE="$2";  shift 2 ;;
            --id)    ID="$2";    shift 2 ;;
            --name)  NAME="$2";  shift 2 ;;
            --permanent) PERMANENT=true; shift ;;
            *) shift ;;
          esac
        done
        ARGS=(entities create --id "$ID" --type "$TYPE"
          --properties "{\"name\":\"$NAME\"}"
          --context "${ROOT_NODE}:ABOUT"
        )
        tc "${ARGS[@]}"
        ;;
      get)
        NODE_ID="${1:-}"
        tc entities get "$NODE_ID"
        ;;
      link)
        FROM_ID="${1:-}"
        shift || true
        REL="" TO_ID=""
        while [[ $# -gt 0 ]]; do
          case "$1" in
            --rel) REL="$2"; shift 2 ;;
            --to)  TO_ID="$2"; shift 2 ;;
            *) shift ;;
          esac
        done
        # TODO: Replace with `trucontext entities edges create` once available in TC CLI.
        # Currently, TC CLI `entities edges` is list-only — no create command exists.
        # Workaround: ingest the relationship as content. TC's intelligence layer will
        # detect and formalize the edge during entity-linking dream cycles.
        tc ingest "Relationship declared: ${FROM_ID} ${REL} ${TO_ID}" \
          --context "${FROM_ID}:ABOUT" \
          --context "${TO_ID}:ABOUT" \
          --context "${ROOT_NODE}:BY" \
          --no-temporal
        echo "Note: Edge creation via CLI not yet available. Relationship ingested as content."
        echo "TC's intelligence layer will formalize it during the next dream cycle."
        ;;
      *)
        echo "Usage: tc-memory node <find|create|get|link>" >&2
        exit 1
        ;;
    esac
    ;;

  *)
    echo "Usage: tc-memory <ingest|recall|query|gaps|health|node>" >&2
    echo "  tc-memory ingest \"<narrative>\" [--permanent]"
    echo "  tc-memory recall \"<query>\" [--limit N]"
    echo "  tc-memory query \"<question>\" [--limit N]"
    echo "  tc-memory gaps"
    echo "  tc-memory health"
    echo "  tc-memory node find \"<name>\""
    echo "  tc-memory node create --type <type> --id <id> --name \"<name>\" [--permanent]"
    echo "  tc-memory node get <id>"
    echo "  tc-memory node link <id> --rel <REL> --to <id2>"
    exit 1
    ;;
esac
