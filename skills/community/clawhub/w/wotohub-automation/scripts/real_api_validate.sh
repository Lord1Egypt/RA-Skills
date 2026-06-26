#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${WOTO_VALIDATION_OUT_DIR:-/tmp/wotohub-real-api-validation}"
mkdir -p "$OUT_DIR"

TOKEN="${WOTOHUB_API_KEY:-}"
INVALID_TOKEN="${WOTOHUB_INVALID_API_KEY:-}"
CAMPAIGN_ID="${WOTOHUB_CAMPAIGN_ID:-}"

usage() {
  cat <<'EOF'
Usage:
  scripts/real_api_validate.sh monitor_replies [request.json]
  scripts/real_api_validate.sh reply_preview [analysis.json]
  scripts/real_api_validate.sh reply_send [preview.json]
  scripts/real_api_validate.sh cycle_blocked [brief.json]
  scripts/real_api_validate.sh cycle_success [brief.json]
  scripts/real_api_validate.sh cycle_failed [brief.json]

Env:
  WOTOHUB_API_KEY           real API key
  WOTOHUB_INVALID_API_KEY   known invalid API key for failed-case validation
  WOTOHUB_CAMPAIGN_ID       test campaign id
  WOTO_VALIDATION_OUT_DIR   output dir, default /tmp/wotohub-real-api-validation
EOF
}

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "missing env: $name" >&2
    exit 2
  fi
}

materialize_json_with_env() {
  local input="$1"
  local output="$2"
  python3 - "$input" "$output" <<'PY'
import json
import os
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
text = src.read_text(encoding='utf-8')
replacements = {
    'REPLACE_WITH_REAL_API_KEY': os.environ.get('WOTOHUB_API_KEY', ''),
    'REPLACE_WITH_REAL_CAMPAIGN_ID': os.environ.get('WOTOHUB_CAMPAIGN_ID', ''),
    'REPLACE_WITH_SENDER_NAME': os.environ.get('WOTOHUB_SENDER_NAME', 'Validation Sender'),
    'REPLACE_WITH_CONTACTED_BLOGGER_ID_1': os.environ.get('WOTOHUB_CONTACTED_BLOGGER_ID_1', ''),
    'REPLACE_WITH_CONTACTED_BLOGGER_ID_2': os.environ.get('WOTOHUB_CONTACTED_BLOGGER_ID_2', ''),
    'REPLACE_WITH_LOW_RISK_REPLY_ID': os.environ.get('WOTOHUB_LOW_RISK_REPLY_ID', ''),
    'REPLACE_WITH_LOW_RISK_CHAT_ID': os.environ.get('WOTOHUB_LOW_RISK_CHAT_ID', ''),
    'REPLACE_WITH_LOW_RISK_BLOGGER_ID': os.environ.get('WOTOHUB_LOW_RISK_BLOGGER_ID', ''),
    'REPLACE_WITH_HIGH_RISK_REPLY_ID': os.environ.get('WOTOHUB_HIGH_RISK_REPLY_ID', ''),
    'REPLACE_WITH_HIGH_RISK_CHAT_ID': os.environ.get('WOTOHUB_HIGH_RISK_CHAT_ID', ''),
    'REPLACE_WITH_HIGH_RISK_BLOGGER_ID': os.environ.get('WOTOHUB_HIGH_RISK_BLOGGER_ID', ''),
}
for key, value in replacements.items():
    if value:
        text = text.replace(key, value)

contacted = os.environ.get('WOTOHUB_CONTACTED_BLOGGER_IDS', '').strip()
if contacted:
    try:
        ids = [x.strip() for x in contacted.split(',') if x.strip()]
        payload = json.loads(text)
        if src.name == 'real-api-monitor-replies.json':
            payload.setdefault('input', {})['contactedBloggerIds'] = ids
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    except Exception:
        pass

placeholder_prefix = 'REPLACE_WITH_'
remaining = sorted({token.strip('" ,[]') for token in text.split() if placeholder_prefix in token})
if remaining:
    raise SystemExit('unresolved placeholders: ' + ', '.join(remaining))

dst.write_text(text, encoding='utf-8')
PY
}

run_monitor_replies() {
  local request="${1:-$ROOT/references/examples/real-api-monitor-replies.json}"
  require_env TOKEN
  require_env CAMPAIGN_ID
  local materialized="$OUT_DIR/monitor_replies.request.json"
  local output="$OUT_DIR/monitor_replies.response.json"
  materialize_json_with_env "$request" "$materialized"
  python3 "$ROOT/wotohub_skill.py" < "$materialized" | tee "$output"
  echo "saved: $materialized"
  echo "saved: $output"
}

run_reply_preview() {
  local analysis="${1:-$ROOT/references/examples/real-api-reply-model-analysis.json}"
  require_env TOKEN
  local output="$OUT_DIR/reply_preview.json"
  python3 "$ROOT/scripts/generate_reply_preview.py" \
    --token "$TOKEN" \
    --model-analysis-file "$analysis" \
    --output "$output"
  cat "$output"
  echo
  echo "saved: $output"
}

run_reply_send() {
  local preview="${1:-$OUT_DIR/reply_preview.json}"
  require_env CAMPAIGN_ID
  python3 "$ROOT/scripts/send_reply_previews.py" \
    "$preview" \
    --campaign-id "$CAMPAIGN_ID" \
    --limit "${WOTO_REPLY_SEND_LIMIT:-1}" \
    ${WOTO_REPLY_SEND_DRY_RUN:+--dry-run}
}

run_cycle_blocked() {
  local brief="${1:-$ROOT/references/examples/real-api-cycle-blocked-brief.json}"
  require_env TOKEN
  require_env CAMPAIGN_ID
  local output="$OUT_DIR/cycle_blocked.output.json"
  local host_request="$OUT_DIR/cycle_blocked.host-request.json"
  local host_payload="$OUT_DIR/cycle_blocked.host-bridge-payload.json"
  set +e
  python3 "$ROOT/run_campaign_cycle.py" \
    --campaign-id "$CAMPAIGN_ID" \
    --brief "$brief" \
    --token "$TOKEN" \
    --mode scheduled_cycle \
    --send-policy prepare_only \
    --host-bridge-request "$host_request" \
    --host-bridge-payload "$host_payload" \
    --output "$output"
  local code=$?
  set -e
  echo "exit_code=$code"
  echo "saved: $output"
  echo "saved: $host_request"
  echo "saved: $host_payload"
  return "$code"
}

run_cycle_success() {
  local brief="${1:-$ROOT/references/examples/real-api-cycle-blocked-brief.json}"
  require_env TOKEN
  require_env CAMPAIGN_ID
  local blocked_output="$OUT_DIR/cycle_success.blocked.output.json"
  local host_request="$OUT_DIR/cycle_success.host-request.json"
  local host_payload="$OUT_DIR/cycle_success.host-bridge-payload.json"
  local host_drafts="$OUT_DIR/cycle_success.host-drafts.json"
  local success_output="$OUT_DIR/cycle_success.output.json"

  set +e
  python3 "$ROOT/run_campaign_cycle.py" \
    --campaign-id "$CAMPAIGN_ID" \
    --brief "$brief" \
    --token "$TOKEN" \
    --mode scheduled_cycle \
    --send-policy prepare_only \
    --host-bridge-request "$host_request" \
    --host-bridge-payload "$host_payload" \
    --output "$blocked_output"
  local blocked_code=$?
  set -e
  echo "first_exit_code=$blocked_code"

  python3 "$ROOT/scripts/host_model_bridge_executor_example.py" \
    --input "$host_payload" \
    --output "$host_drafts" \
    --mode mock

  set +e
  python3 "$ROOT/run_campaign_cycle.py" \
    --campaign-id "$CAMPAIGN_ID" \
    --brief "$brief" \
    --token "$TOKEN" \
    --mode scheduled_cycle \
    --send-policy prepare_only \
    --host-bridge-drafts "$host_drafts" \
    --output "$success_output"
  local success_code=$?
  set -e
  echo "second_exit_code=$success_code"
  echo "saved: $blocked_output"
  echo "saved: $host_request"
  echo "saved: $host_payload"
  echo "saved: $host_drafts"
  echo "saved: $success_output"
  if [[ "$blocked_code" -ne 2 ]]; then
    echo "unexpected blocked exit code: expected 2, got $blocked_code" >&2
    return "$blocked_code"
  fi
  return "$success_code"
}

run_cycle_failed() {
  local brief="${1:-$ROOT/references/examples/real-api-cycle-blocked-brief.json}"
  require_env INVALID_TOKEN
  require_env CAMPAIGN_ID
  local output="$OUT_DIR/cycle_failed.output.json"
  set +e
  python3 "$ROOT/run_campaign_cycle.py" \
    --campaign-id "$CAMPAIGN_ID" \
    --brief "$brief" \
    --token "$INVALID_TOKEN" \
    --mode scheduled_cycle \
    --send-policy prepare_only \
    --output "$output"
  local code=$?
  set -e
  echo "exit_code=$code"
  echo "saved: $output"
  return "$code"
}

cmd="${1:-}"
arg="${2:-}"
case "$cmd" in
  monitor_replies) run_monitor_replies "$arg" ;;
  reply_preview) run_reply_preview "$arg" ;;
  reply_send) run_reply_send "$arg" ;;
  cycle_blocked) run_cycle_blocked "$arg" ;;
  cycle_success) run_cycle_success "$arg" ;;
  cycle_failed) run_cycle_failed "$arg" ;;
  ""|-h|--help|help) usage ;;
  *)
    echo "unknown command: $cmd" >&2
    usage
    exit 2
    ;;
esac
