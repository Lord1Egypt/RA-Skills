#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "缺少要转告给管家的内容。" >&2
  exit 1
fi

USER_TEXT="$*"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
printf '%s\n' "$USER_TEXT" > "${SKILL_DIR}/xiaoai_to_butler_last_message.txt"
OPENCLAW_BIN="${OPENCLAW_BIN:-openclaw}"
MAX_CHARS=120

PROMPT=$(cat <<EOF
【来自小爱语音】
用户原话：${USER_TEXT}

请按以下规则处理：
1. 你是管家，先判断这句话是否应由你自己处理，还是转给其他子 agent。
2. 如果适合派单，你负责自行分配给对应子 agent。
3. 请返回一段适合小爱口播的简短中文，不要太长，尽量控制在 40 字以内。
4. 如果任务会异步处理，请明确说“已收到，正在处理”之类的确认话术。
5. 不要输出 markdown，不要分点，不要带多余解释。
EOF
)

RAW_REPLY="$($OPENCLAW_BIN agent --agent main --message "$PROMPT" 2>/dev/null || true)"
RAW_REPLY="$(printf '%s' "$RAW_REPLY" | tail -n 1 | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g' | sed 's/^ //; s/ $//')"

if [ -z "$RAW_REPLY" ]; then
  echo "已转告管家。"
  exit 0
fi

SHORT_REPLY="$(printf '%s' "$RAW_REPLY" | cut -c1-${MAX_CHARS})"

echo "$SHORT_REPLY"
