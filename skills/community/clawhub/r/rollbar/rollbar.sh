#!/usr/bin/env bash
# rollbar.sh — Rollbar API helper for OpenClaw
# Supports account-level and project-level tokens with MCP-compatible config.
# Usage: rollbar.sh <command> [options]

set -euo pipefail

BASE_URL="https://api.rollbar.com/api/1"

# --- MCP Config Helpers ---

# Resolve config file path:
# ROLLBAR_CONFIG_FILE env > .rollbar-mcp.json in cwd > ~/.rollbar-mcp.json
_find_mcp_config() {
  if [[ -n "${ROLLBAR_CONFIG_FILE:-}" && -f "$ROLLBAR_CONFIG_FILE" ]]; then
    echo "$ROLLBAR_CONFIG_FILE"; return
  fi
  [[ -f "$PWD/.rollbar-mcp.json" ]] && echo "$PWD/.rollbar-mcp.json" && return
  [[ -f "$HOME/.rollbar-mcp.json" ]] && echo "$HOME/.rollbar-mcp.json" && return
  echo ""
}

# Extract token from MCP config, optionally for a specific project name
_mcp_get_token() {
  local config_file="$1" project_name="${2:-}"
  [[ -z "$config_file" || ! -f "$config_file" ]] && return 1
  python3 - "$config_file" "$project_name" <<'PYEOF'
import json, sys
config_file, target = sys.argv[1], sys.argv[2]
with open(config_file) as f:
    cfg = json.load(f)
if not target:
    tok = cfg.get('token') or next((p.get('token', '') for p in cfg.get('projects', [])), '')
    if tok: print(tok); sys.exit(0)
    sys.exit(1)
for p in cfg.get('projects', []):
    if p.get('name') == target:
        print(p['token']); sys.exit(0)
sys.exit(1)
PYEOF
}

# Save/update a project token in the MCP config file (creates if missing)
_mcp_save_token() {
  local config_file="$1" project_name="$2" token="$3"
  python3 - "$config_file" "$project_name" "$token" <<'PYEOF'
import json, os, sys
config_file, project_name, token = sys.argv[1], sys.argv[2], sys.argv[3]
cfg = {}
if os.path.exists(config_file):
    with open(config_file) as f:
        cfg = json.load(f)
# Convert single-project shorthand to multi-project format
if 'token' in cfg and 'projects' not in cfg:
    cfg = {'projects': [{'name': 'default', 'token': cfg['token']}]}
if 'projects' not in cfg:
    cfg['projects'] = []
for p in cfg['projects']:
    if p.get('name') == project_name:
        p['token'] = token; break
else:
    cfg['projects'].append({'name': project_name, 'token': token})
with open(config_file, 'w') as f:
    json.dump(cfg, f, indent=2); f.write('\n')
print(f'Saved token for project: {project_name} -> {config_file}')
PYEOF
}

# --- Usage ---
usage() {
  cat <<EOF
Usage: rollbar.sh <command> [options]

Commands:
  projects                  List all projects (account token required)
  items                     List recent items
  item <id>                 Get item details
  occurrences <id>          Get occurrences for an item
  resolve <id>              Resolve an item
  mute <id>                 Mute an item
  activate <id>             Reopen an item
  deploys                   List recent deploys
  project                   Get project info
  top                       Top active items by occurrence count
  project-tokens            List access tokens for a project
  project-token-create      Create a project access token (account write token required)
  project-token-update      Update a project access token status/rate-limits

Options:
  --project-id <id>         Target project by numeric ID
  --project-name <name>     Select project by name (from .rollbar-mcp.json config)
  --status <active|resolved|muted>   Filter items by status
  --level <critical|error|warning|info>  Filter items by level
  --limit <n>               Max results (default: 20)
  --hours <n>               Time window for 'top' (default: 24)
  --name <name>             Token name (project-token-create)
  --scopes <read,write>     Comma-separated scopes (default: read,write)
  --token-status <enabled|disabled>  Token status (project-token-update)
  --save                    Save created token to .rollbar-mcp.json

Token resolution (first match wins):
  1. \$PWD/secrets/rollbar           — one-line token file
  2. .rollbar-mcp.json (cwd or ~/)  — MCP-compatible JSON config
     Single:   { "token": "tok_..." }
     Multiple: { "projects": [{ "name": "myapp", "token": "tok_..." }] }
     Also: set ROLLBAR_CONFIG_FILE env var for a custom path
  3. \$PWD/.env                      — ROLLBAR_ACCESS_TOKEN=<token>
  4. ROLLBAR_ACCESS_TOKEN           — environment variable

MCP config (.rollbar-mcp.json):
  Use --project-name to select a specific project's token from the config.
  Use 'project-token-create --save' to auto-persist new tokens to the config.
EOF
  exit 0
}

# --- Parse command ---
COMMAND="${1:-}"
[[ -z "$COMMAND" || "$COMMAND" == "--help" || "$COMMAND" == "-h" ]] && usage
shift

# --- Parse options ---
STATUS="" LEVEL="" LIMIT="20" HOURS="24" ITEM_ID=""
PROJECT_ID="" PROJECT_NAME="" TOKEN_NAME="" SCOPES="read,write"
TOKEN_STATUS_VAL="" SAVE_TOKEN=false DRY_RUN=false YES=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --status)         STATUS="$2"; shift 2 ;;
    --level)          LEVEL="$2"; shift 2 ;;
    --limit)          LIMIT="$2"; shift 2 ;;
    --hours)          HOURS="$2"; shift 2 ;;
    --project-id)     PROJECT_ID="$2"; shift 2 ;;
    --project-name)   PROJECT_NAME="$2"; shift 2 ;;
    --name)           TOKEN_NAME="$2"; shift 2 ;;
    --scopes)         SCOPES="$2"; shift 2 ;;
    --token-status)   TOKEN_STATUS_VAL="$2"; shift 2 ;;
    --save)           SAVE_TOKEN=true; shift ;;
    --dry-run)        DRY_RUN=true; shift ;;
    --yes)            YES=true; shift ;;
    *)
      if [[ -z "$ITEM_ID" ]]; then
        ITEM_ID="$1"; shift
      else
        echo "Unknown option: $1" >&2; exit 1
      fi
      ;;
  esac
done

# --- Input validation ---
if [[ -n "$ITEM_ID" && ! "$ITEM_ID" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Error: Invalid item/token ID: $ITEM_ID" >&2; exit 1
fi
if [[ -n "$PROJECT_ID" && ! "$PROJECT_ID" =~ ^[0-9]+$ ]]; then
  echo "Error: Invalid project ID: $PROJECT_ID" >&2; exit 1
fi
if [[ ! "$LIMIT" =~ ^[0-9]+$ ]]; then
  echo "Error: Invalid limit: $LIMIT" >&2; exit 1
fi
if [[ ! "$HOURS" =~ ^[0-9]+$ ]]; then
  echo "Error: Invalid hours: $HOURS" >&2; exit 1
fi

# --- Token Resolution ---
# Source workspace .env if present
[[ -f "$PWD/.env" ]] && source "$PWD/.env" 2>/dev/null || true

MCP_CONFIG="$(_find_mcp_config)"

TOKEN=""
# 1. Secrets file
if [[ -f "$PWD/secrets/rollbar" ]]; then
  TOKEN=$(cat "$PWD/secrets/rollbar" 2>/dev/null || true)
  TOKEN="${TOKEN//[$'\t\r\n ']}"
fi
# 2. MCP config (use --project-name to select specific project)
if [[ -z "$TOKEN" && -n "$MCP_CONFIG" ]]; then
  TOKEN=$(_mcp_get_token "$MCP_CONFIG" "$PROJECT_NAME" 2>/dev/null || true)
fi
# 3. ROLLBAR_ACCESS_TOKEN from .env or environment
if [[ -z "$TOKEN" ]]; then
  TOKEN="${ROLLBAR_ACCESS_TOKEN:-}"
fi

if [[ -z "$TOKEN" ]]; then
  echo "Error: No Rollbar token found." >&2
  echo "" >&2
  echo "Token resolution order (first match wins):" >&2
  echo "  1. \$PWD/secrets/rollbar           — one-line token file" >&2
  echo "  2. .rollbar-mcp.json (cwd or ~/)  — MCP-compatible JSON config" >&2
  echo "     Single:   { \"token\": \"tok_...\" }" >&2
  echo "     Multiple: { \"projects\": [{\"name\": \"myapp\", \"token\": \"tok_...\"}] }" >&2
  echo "     Custom:   set ROLLBAR_CONFIG_FILE env var" >&2
  echo "  3. \$PWD/.env                      — ROLLBAR_ACCESS_TOKEN=<token>" >&2
  echo "  4. ROLLBAR_ACCESS_TOKEN           — environment variable" >&2
  exit 1
fi

# --- HTTP Helpers ---
api_get() {
  local endpoint="$1"; shift
  curl -sf -H "X-Rollbar-Access-Token: $TOKEN" "$BASE_URL/$endpoint" "$@"
}

api_post() {
  local endpoint="$1" data="$2"
  curl -sf -X POST \
    -H "X-Rollbar-Access-Token: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$data" \
    "$BASE_URL/$endpoint"
}

api_patch() {
  local endpoint="$1" data="$2"
  curl -sf -X PATCH \
    -H "X-Rollbar-Access-Token: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$data" \
    "$BASE_URL/$endpoint"
}

# Helper: resolve a project-level read token via account token
_get_project_token() {
  local project_id="$1"
  local tmpfile
  tmpfile=$(mktemp)
  api_get "project/$project_id/access_tokens" > "$tmpfile" 2>/dev/null || { rm -f "$tmpfile"; return 1; }
  python3 - "$tmpfile" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    tokens = json.load(f).get('result', [])
for t in tokens:
    if 'read' in t.get('scopes', []):
        print(t['access_token']); break
PYEOF
  rm -f "$tmpfile"
}

# Auto-switch to project token for item commands when account token is in use
if [[ -n "$PROJECT_ID" && "$COMMAND" != "projects" && "$COMMAND" != "project-tokens" && \
      "$COMMAND" != "project-token-create" && "$COMMAND" != "project-token-update" ]]; then
  PROJECT_TOKEN=$(_get_project_token "$PROJECT_ID" 2>/dev/null || true)
  [[ -n "$PROJECT_TOKEN" ]] && TOKEN="$PROJECT_TOKEN"
fi

# --- Commands ---
case "$COMMAND" in

  projects)
    api_get "projects" | python3 -c "
import json, sys
data = json.load(sys.stdin)
projects = data.get('result', [])
print(json.dumps([{
    'id': p['id'],
    'name': p['name'],
    'status': p.get('status', '?'),
    'date_created': p.get('date_created'),
} for p in projects], indent=2))
"
    ;;

  items)
    PARAMS="?page=1&sort=last_occurrence"
    [[ -n "$STATUS" ]] && PARAMS="$PARAMS&status=$STATUS"
    [[ -n "$LEVEL" ]] && PARAMS="$PARAMS&level=$LEVEL"
    api_get "items$PARAMS" | _LIMIT="$LIMIT" python3 -c "
import json, sys, os
data = json.load(sys.stdin)
items = data.get('result', {}).get('items', data.get('result', []))
limit = int(os.environ['_LIMIT'])
if isinstance(items, list): items = items[:limit]
print(json.dumps([{
    'id': i['id'],
    'counter': i.get('counter'),
    'title': i.get('title', '')[:150],
    'level': i.get('level_string', i.get('level', '')),
    'status': i.get('status', ''),
    'total_occurrences': i.get('total_occurrences', 0),
    'last_occurrence': i.get('last_occurrence_timestamp'),
    'environment': i.get('environment', ''),
    'framework': i.get('framework', ''),
} for i in items], indent=2))
"
    ;;

  item)
    [[ -z "$ITEM_ID" ]] && { echo "Usage: rollbar.sh item <item_id>" >&2; exit 1; }
    api_get "item/$ITEM_ID" | python3 -m json.tool 2>/dev/null || api_get "item/$ITEM_ID"
    ;;

  occurrences)
    [[ -z "$ITEM_ID" ]] && { echo "Usage: rollbar.sh occurrences <item_id>" >&2; exit 1; }
    api_get "item/$ITEM_ID/instances/?page=1" | python3 -m json.tool 2>/dev/null || \
      api_get "item/$ITEM_ID/instances/?page=1"
    ;;

  resolve)
    [[ -z "$ITEM_ID" ]] && { echo "Usage: rollbar.sh resolve <item_id>" >&2; exit 1; }
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "{\"dry_run\": true, \"action\": \"resolve\", \"item_id\": \"$ITEM_ID\"}"
      exit 0
    fi
    if [[ "$YES" != "true" ]]; then
      echo "⚠️  This will resolve item $ITEM_ID and suppress future alerts. Pass --yes to confirm, or --dry-run to preview." >&2
      exit 1
    fi
    api_patch "item/$ITEM_ID" '{"status":"resolved"}' | python3 -m json.tool 2>/dev/null || \
      api_patch "item/$ITEM_ID" '{"status":"resolved"}'
    ;;

  mute)
    [[ -z "$ITEM_ID" ]] && { echo "Usage: rollbar.sh mute <item_id>" >&2; exit 1; }
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "{\"dry_run\": true, \"action\": \"mute\", \"item_id\": \"$ITEM_ID\"}"
      exit 0
    fi
    if [[ "$YES" != "true" ]]; then
      echo "⚠️  This will mute item $ITEM_ID and stop all alerts for it. Pass --yes to confirm, or --dry-run to preview." >&2
      exit 1
    fi
    api_patch "item/$ITEM_ID" '{"status":"muted"}' | python3 -m json.tool 2>/dev/null || \
      api_patch "item/$ITEM_ID" '{"status":"muted"}'
    ;;

  activate)
    [[ -z "$ITEM_ID" ]] && { echo "Usage: rollbar.sh activate <item_id>" >&2; exit 1; }
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "{\"dry_run\": true, \"action\": \"activate\", \"item_id\": \"$ITEM_ID\"}"
      exit 0
    fi
    if [[ "$YES" != "true" ]]; then
      echo "⚠️  This will reopen item $ITEM_ID. Pass --yes to confirm, or --dry-run to preview." >&2
      exit 1
    fi
    api_patch "item/$ITEM_ID" '{"status":"active"}' | python3 -m json.tool 2>/dev/null || \
      api_patch "item/$ITEM_ID" '{"status":"active"}'
    ;;

  deploys)
    api_get "deploys/?page=1" | python3 -m json.tool 2>/dev/null || api_get "deploys/?page=1"
    ;;

  project)
    api_get "project" | python3 -m json.tool 2>/dev/null || api_get "project"
    ;;

  top)
    PARAMS="?status=active&sort=total_occurrences&direction=desc&page=1"
    [[ -n "$LEVEL" ]] && PARAMS="$PARAMS&level=$LEVEL"
    api_get "items$PARAMS" | _HOURS="$HOURS" _LIMIT="$LIMIT" python3 -c "
import json, sys, os
from datetime import datetime, timedelta, timezone
data = json.load(sys.stdin)
items = data.get('result', {}).get('items', data.get('result', []))
hours = int(os.environ['_HOURS'])
limit = int(os.environ['_LIMIT'])
cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
print(json.dumps({
    'window_hours': hours,
    'items': [{
        'id': i['id'],
        'counter': i.get('counter'),
        'title': i.get('title', '')[:120],
        'level': i.get('level_string', i.get('level', '')),
        'total_occurrences': i.get('total_occurrences', 0),
        'last_occurrence': i.get('last_occurrence_timestamp'),
        'environment': i.get('environment', ''),
    } for i in (items if isinstance(items, list) else [])
      if i.get('last_occurrence_timestamp', 0) >= cutoff.timestamp()
    ][:limit]
}, indent=2))
" 2>/dev/null || api_get "items$PARAMS"
    ;;

  # --- Project Token Management ---

  project-tokens)
    [[ -z "$PROJECT_ID" ]] && { echo "Error: --project-id required" >&2; exit 1; }
    api_get "project/$PROJECT_ID/access_tokens" | python3 -c "
import json, sys
data = json.load(sys.stdin)
tokens = data.get('result', [])
print(json.dumps([{
    'access_token': t.get('access_token', '')[:8] + '...',
    'name': t.get('name', ''),
    'scopes': t.get('scopes', []),
    'status': t.get('status', ''),
    'date_created': t.get('date_created'),
    'rate_limit_window_size': t.get('rate_limit_window_size'),
    'rate_limit_window_count': t.get('rate_limit_window_count'),
} for t in tokens], indent=2))
"
    ;;

  project-token-create)
    [[ -z "$PROJECT_ID" ]] && { echo "Error: --project-id required" >&2; exit 1; }
    [[ -z "$TOKEN_NAME" ]] && { echo "Error: --name required (token name)" >&2; exit 1; }
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "{\"dry_run\": true, \"action\": \"project-token-create\", \"project_id\": \"$PROJECT_ID\", \"name\": \"$TOKEN_NAME\", \"scopes\": \"$SCOPES\"}"
      exit 0
    fi
    if [[ "$YES" != "true" ]]; then
      echo "⚠️  This will create a new $SCOPES access token for project $PROJECT_ID. Pass --yes to confirm, or --dry-run to preview." >&2
      exit 1
    fi
    # Build scopes array from comma-separated string
    SCOPES_JSON=$(python3 -c "import json; print(json.dumps('$SCOPES'.split(',')))")
    PAYLOAD=$(python3 -c "
import json
print(json.dumps({'name': '$TOKEN_NAME', 'scopes': '$SCOPES'.split(',')}))
")
    RESULT=$(api_post "project/$PROJECT_ID/access_tokens" "$PAYLOAD")
    echo "$RESULT" | python3 -m json.tool 2>/dev/null || echo "$RESULT"
    # Optionally save to .rollbar-mcp.json
    if [[ "$SAVE_TOKEN" == "true" ]]; then
      NEW_TOKEN=$(echo "$RESULT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('result', {}).get('access_token', ''))
" 2>/dev/null || true)
      if [[ -n "$NEW_TOKEN" ]]; then
        SAVE_NAME="${PROJECT_NAME:-$TOKEN_NAME}"
        CONFIG_DEST="${MCP_CONFIG:-$PWD/.rollbar-mcp.json}"
        _mcp_save_token "$CONFIG_DEST" "$SAVE_NAME" "$NEW_TOKEN"
      else
        echo "Warning: could not extract token from response; skipping save." >&2
      fi
    fi
    ;;

  project-token-update)
    # ITEM_ID is used as the token value/id to update
    [[ -z "$ITEM_ID" ]] && { echo "Error: Usage: rollbar.sh project-token-update <token_id_or_value> --project-id <id> [--token-status enabled|disabled]" >&2; exit 1; }
    [[ -z "$PROJECT_ID" ]] && { echo "Error: --project-id required" >&2; exit 1; }
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "{\"dry_run\": true, \"action\": \"project-token-update\", \"token_id\": \"$ITEM_ID\", \"project_id\": \"$PROJECT_ID\", \"token_status\": \"$TOKEN_STATUS_VAL\"}"
      exit 0
    fi
    if [[ "$YES" != "true" ]]; then
      echo "⚠️  This will update token $ITEM_ID on project $PROJECT_ID. Pass --yes to confirm, or --dry-run to preview." >&2
      exit 1
    fi
    PATCH_DATA="{}"
    [[ -n "$TOKEN_STATUS_VAL" ]] && PATCH_DATA=$(python3 -c "import json; print(json.dumps({'status': '$TOKEN_STATUS_VAL'}))")
    api_patch "project/$PROJECT_ID/access_token/$ITEM_ID" "$PATCH_DATA" | \
      python3 -m json.tool 2>/dev/null || \
      api_patch "project/$PROJECT_ID/access_token/$ITEM_ID" "$PATCH_DATA"
    ;;

  *)
    echo "Unknown command: $COMMAND" >&2
    echo "Run: rollbar.sh --help" >&2
    exit 1
    ;;
esac
