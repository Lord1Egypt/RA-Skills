#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  cat >&2 <<'EOF'
Usage:
  conversation_bridge.sh preview --message "<text>" [--account <account>] [--date <yyyy-mm-dd>] [--category <category>]
  conversation_bridge.sh write --message "<text>" [--account <account>] [--date <yyyy-mm-dd>] [--category <category>] [--skip-duplicate-check] [--node-id <id>]
  conversation_bridge.sh learn --message "<text>" --category "<category>"
  conversation_bridge.sh classify-reply --state-json "<json>" --reply "<text>"
EOF
  exit 1
}

json_error() {
  local node_id="${1:-UNKNOWN}"
  local message="${2:-unknown error}"
  jq -nc \
    --arg nodeId "$node_id" \
    --arg error "$message" \
    '{ok:false,nodeId:$nodeId,status:"failed",error:$error}'
}

normalize_category_name() {
  python3 - "$1" <<'PY'
import re
import sys

raw = sys.argv[1].strip().lower()
raw = re.sub(r'[^a-z0-9\s]', ' ', raw)
raw = ' '.join(raw.split())

categories = {
    "housing": "Housing",
    "transport": "Transport",
    "groceries": "Groceries",
    "grocery": "Groceries",
    "dining out": "Dining Out",
    "dining": "Dining Out",
    "personal care": "Personal Care",
    "shopping": "Shopping",
    "utilities": "Utilities",
    "utility": "Utilities",
    "fun": "Fun",
    "business": "Business",
    "other": "Other",
    "donation": "Donation",
    "charity": "Donation",
    "childcare": "Childcare",
    "travel": "Travel",
    "zakat": "Zakat",
    "debt payment": "Debt Payment",
    "debt": "Debt Payment",
    "fitness": "Fitness",
    "family support": "Family Support",
    "taxes": "Taxes",
    "tax": "Taxes",
    "maintenance": "Maintenance",
    "painting": "Painting",
    "testground": "TestGround",
    "learning": "Learning",
    "sports": "Sports",
    "pet": "Pet",
    "gifts": "Gifts",
    "gift": "Gifts",
    "special occasions": "Special Occasions",
    "special occasion": "Special Occasions",
    "dress": "Dress",
    "clothes": "Dress",
    "clothing": "Dress",
    "hobby": "Hobby",
    "insurance": "Insurance",
    "medical": "Medical",
}

print(categories.get(raw, ""))
PY
}

run_preview() {
  local message=""
  local account=""
  local date_arg=""
  local category=""

  while (($#)); do
    case "$1" in
      --message) message="${2:-}"; shift 2 ;;
      --account) account="${2:-}"; shift 2 ;;
      --date) date_arg="${2:-}"; shift 2 ;;
      --category) category="${2:-}"; shift 2 ;;
      *) usage ;;
    esac
  done

  [[ -n "$message" ]] || usage

  local cmd=(bash "${SCRIPT_DIR}/log.sh" --preview "$message")
  [[ -n "$date_arg" ]] && cmd+=(--date "$date_arg")
  [[ -n "$account" ]] && cmd+=(--account "$account")
  [[ -n "$category" ]] && cmd+=(--category "$category")

  local output
  if ! output="$("${cmd[@]}" 2>&1)"; then
    json_error "PREVIEW" "$output"
    return 0
  fi

  local explicit
  local category_source
  explicit="$(jq -r '.explicitCategory' <<<"$output")"
  category_source="$(jq -r '.categorySource // "none"' <<<"$output")"

  if [[ "$explicit" == "true" ]]; then
    jq -nc \
      --argjson preview "$output" \
      '{ok:true,nodeId:"PREVIEW",status:"ready_to_log",decision:"LOG_DIRECT",preview:$preview}'
    return 0
  fi

  if [[ "$category_source" == "builtin" || "$category_source" == "learned" ]]; then
    jq -nc \
      --argjson preview "$output" \
      '{ok:true,nodeId:"CONFIDENCE",status:"awaiting_category_confirmation",decision:"ASK_CONFIRM",preview:$preview}'
    return 0
  fi

  jq -nc \
    --argjson preview "$output" \
    '{ok:true,nodeId:"CONFIDENCE",status:"awaiting_category_selection",decision:"ASK_CATEGORY",preview:$preview}'
}

run_write() {
  local message=""
  local account=""
  local date_arg=""
  local category=""
  local skip_duplicate_check="0"
  local node_id="LOG_DIRECT"

  while (($#)); do
    case "$1" in
      --message) message="${2:-}"; shift 2 ;;
      --account) account="${2:-}"; shift 2 ;;
      --date) date_arg="${2:-}"; shift 2 ;;
      --category) category="${2:-}"; shift 2 ;;
      --skip-duplicate-check) skip_duplicate_check="1"; shift ;;
      --node-id) node_id="${2:-}"; shift 2 ;;
      *) usage ;;
    esac
  done

  [[ -n "$message" ]] || usage

  local cmd=(bash "${SCRIPT_DIR}/log.sh" "$message")
  [[ -n "$date_arg" ]] && cmd+=(--date "$date_arg")
  [[ -n "$account" ]] && cmd+=(--account "$account")
  [[ -n "$category" ]] && cmd+=(--category "$category")
  [[ "$skip_duplicate_check" == "1" ]] && cmd+=(--skip-duplicate-check)

  local output=""
  if ! output="$("${cmd[@]}" 2>&1)"; then
    json_error "$node_id" "$output"
    return 0
  fi

  local duplicate_line=""
  duplicate_line="$(printf '%s\n' "$output" | rg '^DUPLICATE_FOUND:' -N || true)"
  if [[ -n "$duplicate_line" ]]; then
    jq -nc \
      --arg duplicateMessage "$duplicate_line" \
      '{ok:true,nodeId:"DUPLICATE",status:"awaiting_duplicate_confirmation",decision:"ASK_DUP",duplicateMessage:$duplicateMessage}'
    return 0
  fi

  local reply_line=""
  reply_line="$(printf '%s\n' "$output" | sed -n 's/^REPLY: //p' | tail -n 1)"
  if [[ -z "$reply_line" ]]; then
    json_error "$node_id" "missing REPLY line from log.sh"
    return 0
  fi

  jq -nc \
    --arg nodeId "$node_id" \
    --arg replyText "$reply_line" \
    --arg rawOutput "$output" \
    '{ok:true,nodeId:$nodeId,status:"logged",replyText:$replyText,rawOutput:$rawOutput}'
}

run_learn() {
  local message=""
  local category=""

  while (($#)); do
    case "$1" in
      --message) message="${2:-}"; shift 2 ;;
      --category) category="${2:-}"; shift 2 ;;
      *) usage ;;
    esac
  done

  [[ -n "$message" && -n "$category" ]] || usage

  local output=""
  if ! output="$(bash "${SCRIPT_DIR}/learn_category_alias.sh" "$message" "$category" 2>&1)"; then
    json_error "LEARN" "$output"
    return 0
  fi

  jq -nc \
    --arg learnOutput "$output" \
    '{ok:true,nodeId:"LEARN",status:"learned",learnOutput:$learnOutput}'
}

run_classify_reply() {
  local state_json=""
  local reply=""

  while (($#)); do
    case "$1" in
      --state-json) state_json="${2:-}"; shift 2 ;;
      --reply) reply="${2:-}"; shift 2 ;;
      *) usage ;;
    esac
  done

  [[ -n "$state_json" && -n "$reply" ]] || usage

  python3 - "$state_json" "$reply" <<'PY'
import json
import re
import sys

state = json.loads(sys.argv[1])
reply = sys.argv[2]

YES = {"y", "yes", "yeah", "yep", "ok", "okay", "sure", "go ahead", "confirm", "do it", "proceed"}
NO = {"n", "no", "nope", "cancel", "stop", "dont", "don't", "skip", "nevermind", "never mind"}

ALIASES = {
    "housing": "Housing",
    "transport": "Transport",
    "groceries": "Groceries",
    "grocery": "Groceries",
    "dining out": "Dining Out",
    "dining": "Dining Out",
    "personal care": "Personal Care",
    "shopping": "Shopping",
    "utilities": "Utilities",
    "utility": "Utilities",
    "fun": "Fun",
    "business": "Business",
    "other": "Other",
    "donation": "Donation",
    "charity": "Donation",
    "childcare": "Childcare",
    "travel": "Travel",
    "zakat": "Zakat",
    "debt payment": "Debt Payment",
    "debt": "Debt Payment",
    "fitness": "Fitness",
    "family support": "Family Support",
    "taxes": "Taxes",
    "tax": "Taxes",
    "maintenance": "Maintenance",
    "painting": "Painting",
    "testground": "TestGround",
    "learning": "Learning",
    "sports": "Sports",
    "pet": "Pet",
    "gifts": "Gifts",
    "gift": "Gifts",
    "special occasions": "Special Occasions",
    "special occasion": "Special Occasions",
    "dress": "Dress",
    "clothes": "Dress",
    "clothing": "Dress",
    "hobby": "Hobby",
    "insurance": "Insurance",
    "medical": "Medical",
}

def norm(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())

reply_norm = norm(reply)
kind = state.get("kind", "")
node_id = "DUP_REPLY" if kind == "awaiting_duplicate_confirmation" else "REPLY_KIND"

category = ALIASES.get(reply_norm, "")
if not category:
    for alias, name in ALIASES.items():
        if reply_norm == alias or reply_norm.startswith(alias + " "):
            category = name
            break

if kind == "awaiting_duplicate_confirmation":
    if reply_norm in YES:
        payload = {"ok": True, "nodeId": node_id, "replyKind": "yes"}
    elif reply_norm in NO:
        payload = {"ok": True, "nodeId": node_id, "replyKind": "cancel"}
    else:
        payload = {"ok": True, "nodeId": node_id, "replyKind": "unrelated"}
    print(json.dumps(payload))
    raise SystemExit(0)

if reply_norm in YES:
    print(json.dumps({"ok": True, "nodeId": node_id, "replyKind": "yes"}))
    raise SystemExit(0)

if reply_norm in NO:
    print(json.dumps({"ok": True, "nodeId": node_id, "replyKind": "cancel"}))
    raise SystemExit(0)

if category:
    print(json.dumps({"ok": True, "nodeId": node_id, "replyKind": "category", "category": category}))
    raise SystemExit(0)

print(json.dumps({"ok": True, "nodeId": node_id, "replyKind": "unrelated"}))
PY
}

action="${1:-}"
[[ -n "$action" ]] || usage
shift || true

case "$action" in
  preview) run_preview "$@" ;;
  write) run_write "$@" ;;
  learn) run_learn "$@" ;;
  classify-reply) run_classify_reply "$@" ;;
  *) usage ;;
esac
