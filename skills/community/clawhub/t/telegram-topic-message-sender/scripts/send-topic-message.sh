#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  send-topic-message.sh [--chat-id <id>] [--topic-id <id>] [--channel <name>] <message>

Env:
  TG_DEFAULT_CHAT_ID   Optional default chat id.
  TG_DEFAULT_TOPIC_ID  Optional default topic id.
  TG_DEFAULT_CHANNEL   Optional default channel (default: telegram).

Examples:
  send-topic-message.sh "hello"
  send-topic-message.sh --chat-id -1003574630717 --topic-id 96 "部署完成 ✅"
EOF
}

CHAT_ID="${TG_DEFAULT_CHAT_ID:-}"
TOPIC_ID="${TG_DEFAULT_TOPIC_ID:-}"
CHANNEL="${TG_DEFAULT_CHANNEL:-telegram}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --chat-id)
      CHAT_ID="$2"
      shift 2
      ;;
    --topic-id)
      TOPIC_ID="$2"
      shift 2
      ;;
    --channel)
      CHANNEL="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -lt 1 ]]; then
  echo "Missing message text" >&2
  usage
  exit 1
fi

if [[ -z "$CHAT_ID" ]]; then
  echo "chat id is required (use --chat-id or TG_DEFAULT_CHAT_ID)" >&2
  exit 1
fi

if [[ -z "$TOPIC_ID" ]]; then
  echo "topic id is required (use --topic-id or TG_DEFAULT_TOPIC_ID)" >&2
  exit 1
fi

MESSAGE="$*"

openclaw message send \
  --channel "$CHANNEL" \
  --target "$CHAT_ID" \
  --thread-id "$TOPIC_ID" \
  --message "$MESSAGE"
