#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONV_FILE="${SKILL_DIR}/ha_conversation_content.txt"
LAST_FILE="${SKILL_DIR}/xiaoai_to_butler_last_message.txt"
REPLY_FILE="${SKILL_DIR}/xiaoai_to_butler_reply.txt"
ERROR_FILE="${SKILL_DIR}/xiaoai_to_butler_error.txt"

USER_TEXT="${*:-}"
printf '%s\n' "$USER_TEXT" > "$CONV_FILE"
printf '%s\n' "$USER_TEXT" > "$LAST_FILE"

if [ -z "$USER_TEXT" ]; then
  echo "没有读取到小爱对话内容。" > "$REPLY_FILE"
  echo "EMPTY_USER_TEXT" > "$ERROR_FILE"
  exit 1
fi

if bash "${SCRIPT_DIR}/xiaoai_to_butler.sh" "$USER_TEXT" > "$REPLY_FILE" 2> "$ERROR_FILE"; then
  exit 0
else
  if [ ! -s "$REPLY_FILE" ]; then
    echo "转告管家失败，请稍后再试。" > "$REPLY_FILE"
  fi
  exit 1
fi
