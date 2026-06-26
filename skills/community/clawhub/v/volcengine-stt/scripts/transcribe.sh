#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  transcribe.sh <audio-file> [--out <path>] [--json] [--language <code>] [--resource-id <id>] [--app-id <id>] [--access-token <token>] [--mode standard|flash]

Modes:
  standard (default): submit + query polling (AUC standard API)
  flash: single request (AUC flash API)

Env:
  VOLC_APP_ID
  VOLC_ACCESS_TOKEN
  VOLC_RESOURCE_ID
  VOLC_STT_MODE                 default: standard
  VOLC_POLL_INTERVAL_SEC        default: 2
  VOLC_POLL_TIMEOUT_SEC         default: 90

Config fallback (~/.openclaw/openclaw.json):
  skills.entries["volcengine-stt"].appId
  skills.entries["volcengine-stt"].accessToken
  skills.entries["volcengine-stt"].resourceId
EOF
}

[[ $# -lt 1 ]] && usage && exit 1

AUDIO=""
OUT=""
JSON_MODE=0
LANG=""
MODE="${VOLC_STT_MODE:-standard}"
APP_ID="${VOLC_APP_ID:-}"
ACCESS_TOKEN="${VOLC_ACCESS_TOKEN:-}"
RESOURCE_ID="${VOLC_RESOURCE_ID:-volc.seedasr.auc}"
POLL_INTERVAL="${VOLC_POLL_INTERVAL_SEC:-2}"
POLL_TIMEOUT="${VOLC_POLL_TIMEOUT_SEC:-90}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="${2:-}"; shift 2 ;;
    --json) JSON_MODE=1; shift ;;
    --language) LANG="${2:-}"; shift 2 ;;
    --resource-id) RESOURCE_ID="${2:-}"; shift 2 ;;
    --app-id) APP_ID="${2:-}"; shift 2 ;;
    --access-token) ACCESS_TOKEN="${2:-}"; shift 2 ;;
    --mode) MODE="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *)
      if [[ -z "$AUDIO" ]]; then AUDIO="$1"; shift; else echo "Unknown arg: $1" >&2; exit 1; fi
      ;;
  esac
done

[[ -z "$AUDIO" || ! -f "$AUDIO" ]] && echo "Audio file not found: $AUDIO" >&2 && exit 1

# Config fallback
if [[ -z "$APP_ID" || -z "$ACCESS_TOKEN" ]]; then
  CFG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
  if [[ -f "$CFG" ]] && command -v jq >/dev/null 2>&1; then
    [[ -z "$APP_ID" ]] && APP_ID="$(jq -r '.skills.entries["volcengine-stt"].appId // .skills.entries["volcengine-stt"].env.VOLC_APP_ID // .skills["volcengine-stt"].appId // .skills["volcengine-stt"].env.VOLC_APP_ID // empty' "$CFG")"
    [[ -z "$ACCESS_TOKEN" ]] && ACCESS_TOKEN="$(jq -r '.skills.entries["volcengine-stt"].accessToken // .skills.entries["volcengine-stt"].env.VOLC_ACCESS_TOKEN // .skills["volcengine-stt"].accessToken // .skills["volcengine-stt"].env.VOLC_ACCESS_TOKEN // empty' "$CFG")"
    CFG_RES="$(jq -r '.skills.entries["volcengine-stt"].resourceId // .skills.entries["volcengine-stt"].env.VOLC_RESOURCE_ID // .skills["volcengine-stt"].resourceId // .skills["volcengine-stt"].env.VOLC_RESOURCE_ID // empty' "$CFG")"
    [[ -n "$CFG_RES" ]] && RESOURCE_ID="$CFG_RES"
  fi
fi

[[ -z "$APP_ID" || -z "$ACCESS_TOKEN" ]] && echo "Missing VOLC_APP_ID/VOLC_ACCESS_TOKEN" >&2 && exit 1

if [[ -z "$OUT" ]]; then
  [[ $JSON_MODE -eq 1 ]] && OUT="${AUDIO%.*}.json" || OUT="${AUDIO%.*}.txt"
fi

REQ_ID="$(cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen)"
HEADERS=(-H "Content-Type: application/json" -H "X-Api-App-Key: $APP_ID" -H "X-Api-Access-Key: $ACCESS_TOKEN" -H "X-Api-Resource-Id: $RESOURCE_ID" -H "X-Api-Request-Id: $REQ_ID" -H "X-Api-Sequence: -1")

ext="${AUDIO##*.}"; ext="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
format="$ext"
case "$ext" in oga|opus) format="ogg" ;; wav|mp3|ogg) ;; *) format="mp3" ;; esac
codec="raw"; [[ "$format" == "ogg" ]] && codec="opus"
AUDIO_B64="$(base64 -w 0 "$AUDIO" 2>/dev/null || base64 "$AUDIO" | tr -d '\n')"

TMP_REQ="$(mktemp)"; TMP_RES="$(mktemp)"; TMP_H="$(mktemp)"
trap 'rm -f "$TMP_REQ" "$TMP_RES" "$TMP_H"' EXIT

if [[ "$MODE" == "flash" ]]; then
  ENDPOINT="https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash"
  if [[ -n "$LANG" ]]; then
    jq -n --arg app "$APP_ID" --arg data "$AUDIO_B64" --arg fmt "$format" --arg lang "$LANG" '{user:{uid:$app},audio:{data:$data,format:$fmt,codec:"opus"},request:{model_name:"bigmodel",language:$lang,enable_itn:true,enable_punc:true}}' > "$TMP_REQ"
  else
    jq -n --arg app "$APP_ID" --arg data "$AUDIO_B64" --arg fmt "$format" '{user:{uid:$app},audio:{data:$data,format:$fmt,codec:"opus"},request:{model_name:"bigmodel",enable_itn:true,enable_punc:true}}' > "$TMP_REQ"
  fi
  curl -sS "$ENDPOINT" "${HEADERS[@]}" -d @"$TMP_REQ" -D "$TMP_H" -o "$TMP_RES"
else
  SUBMIT="https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
  QUERY="https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

  # Standard API doc uses audio.url; here we try data for local file use.
  if [[ -n "$LANG" ]]; then
    jq -n --arg app "$APP_ID" --arg data "$AUDIO_B64" --arg fmt "$format" --arg codec "$codec" --arg lang "$LANG" '{user:{uid:$app},audio:{data:$data,format:$fmt,codec:$codec},request:{model_name:"bigmodel",language:$lang,enable_itn:true,enable_punc:true}}' > "$TMP_REQ"
  else
    jq -n --arg app "$APP_ID" --arg data "$AUDIO_B64" --arg fmt "$format" --arg codec "$codec" '{user:{uid:$app},audio:{data:$data,format:$fmt,codec:$codec},request:{model_name:"bigmodel",enable_itn:true,enable_punc:true}}' > "$TMP_REQ"
  fi

  curl -sS "$SUBMIT" "${HEADERS[@]}" -d @"$TMP_REQ" -D "$TMP_H" -o "$TMP_RES"
  sub_code="$(grep -i '^X-Api-Status-Code:' "$TMP_H" | awk '{print $2}' | tr -d '\r' || true)"
  [[ "$sub_code" != "20000000" ]] && echo "Submit failed: $sub_code" >&2 && grep -i '^X-Api-Message:' "$TMP_H" >&2 && cat "$TMP_RES" >&2 && exit 2

  start_ts="$(date +%s)"
  while :; do
    echo '{}' > "$TMP_REQ"
    curl -sS "$QUERY" "${HEADERS[@]}" -d @"$TMP_REQ" -D "$TMP_H" -o "$TMP_RES"
    q_code="$(grep -i '^X-Api-Status-Code:' "$TMP_H" | awk '{print $2}' | tr -d '\r' || true)"
    if [[ "$q_code" == "20000000" ]]; then
      break
    elif [[ "$q_code" == "20000001" || "$q_code" == "20000002" ]]; then
      now="$(date +%s)"
      [[ $((now-start_ts)) -ge $POLL_TIMEOUT ]] && echo "Query timeout after ${POLL_TIMEOUT}s" >&2 && cat "$TMP_RES" >&2 && exit 3
      sleep "$POLL_INTERVAL"
    else
      echo "Query failed: $q_code" >&2
      grep -i '^X-Api-Message:' "$TMP_H" >&2 || true
      cat "$TMP_RES" >&2
      exit 2
    fi
  done
fi

if [[ $JSON_MODE -eq 1 ]]; then
  cp "$TMP_RES" "$OUT"
else
  jq -r '.result.text // .text // empty' "$TMP_RES" > "$OUT"
fi

if [[ ! -s "$OUT" ]]; then
  echo "Transcription output empty. Raw response:" >&2
  cat "$TMP_RES" >&2
  exit 2
fi

echo "$OUT"
