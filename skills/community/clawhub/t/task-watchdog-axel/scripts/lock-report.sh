#!/usr/bin/env bash
# lock-report.sh - 扫描所有活跃 lock,生成状态报告,可定期执行
# 用法:
#   ./lock-report.sh                  # 输出完整报告
#   ./lock-report.sh --abandoned-only # 只看需要关注的任务
#   ./lock-report.sh --json           # 输出 JSON 格式

set -euo pipefail

LOCKS_ROOT="$HOME/.openclaw/agents"
GRACE_MINUTES=8

# 检查 session 是否仍活跃
session_alive() {
  local session_id="$1"
  local agent_id="$2"

  if [[ -z "$session_id" ]]; then
    return 1
  fi

  openclaw sessions list --agent "$agent_id" --format json 2>/dev/null | grep -q "$session_id"
}

# 从 lock 提取字段
get_field() {
  grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$2" 2>/dev/null | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/'
}

# 分钟前计算(简单版)
minutes_ago() {
  local ts="$1"
  local ts_h=$(echo "$ts" | sed 's/.*T\([0-9]*\):.*/\1/')
  local ts_m=$(echo "$ts" | sed 's/.*:\([0-9]*\):.*/\1/')
  local now_h=$(date -u +"%H")
  local now_m=$(date -u +"%M")
  local diff=$(( (now_h * 60 + now_m) - (ts_h * 60 + ts_m) ))
  if [[ $diff -lt -600 ]]; then diff=$((diff + 1440)); fi
  if [[ $diff -lt 0 ]]; then diff=$((diff + 1440)); fi
  echo $diff
}

echo "========================================"
echo "  Task Watchdog 状态报告"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "========================================"
echo ""

total=0
abandoned=0
heartbeat_warn=0
normal=0

while IFS= read -r lock; do
  [[ -z "$lock" || "$lock" == *"/active/"* ]] || continue
  [[ ! -f "$lock" ]] && continue

  ((total++)) || true

  agent=$(echo "$lock" | sed "s|$LOCKS_ROOT/||" | cut -d/ -f1)
  task=$(basename "$lock" .lock)
  status=$(get_field "status" "$lock"); status="${status:-unknown}"
  desc=$(get_field "description" "$lock"); desc="${desc:-无}"
  session_id=$(get_field "session_id" "$lock"); session_id="${session_id:-}"
  last_hb=$(get_field "last_heartbeat" "$lock"); last_hb="${last_hb:-unknown}"
  progress=$(get_field "progress" "$lock"); progress="${progress:-}"
  last_progress=$(get_field "last_progress" "$lock"); last_progress="${last_progress:-${last_hb:-unknown}}"
  created=$(get_field "created_at" "$lock"); created="${created:-${last_hb:-unknown}}"

  [[ "$status" != "in_progress" ]] && continue

  hb_min=$(minutes_ago "$last_hb")
  progress_min=$(minutes_ago "$last_progress")
  created_min=$(minutes_ago "$created")

  # 判断状态（与 scan-locks.sh 一致：session 死 + progress 超 GRACE×3 才归档）
  FLAG=""
  CATEGORY=""

  if ! session_alive "$session_id" "$agent"; then
    if [[ $progress_min -gt $((GRACE_MINUTES * 3)) ]]; then
      FLAG="🚫 ABANDONED"
      CATEGORY="abandoned"
      ((abandoned++)) || true
    else
      FLAG="⚠️ SESSION_DEAD"
      CATEGORY="warn"
      ((heartbeat_warn++)) || true
    fi
  elif [[ $progress_min -gt $((GRACE_MINUTES * 3)) ]]; then
    FLAG="⚠️ STALLED"
    CATEGORY="warn"
    ((heartbeat_warn++)) || true
  elif [[ $hb_min -gt $((GRACE_MINUTES * 2)) ]]; then
    FLAG="⚠️ HEARTBEAT_DELAY"
    CATEGORY="warn"
    ((heartbeat_warn++)) || true
  else
    FLAG="✅ 正常"
    CATEGORY="normal"
    ((normal++)) || true
  fi

  echo "----------------------------------------"
  echo "  [$agent] $task"
  echo "  描述: ${desc:-无}"
  echo "  状态: $FLAG"
  echo "  创建: ${created_min}分钟前"
  echo "  最新进展: ${progress_min}分钟前"
  echo "  心跳: ${hb_min}分钟前"
  [[ -n "$progress" ]] && [[ "$progress" != "任务已创建" ]] && echo "  进度: $progress"
  [[ -n "$session_id" ]] && echo "  Session: $session_id"
  echo ""

done < <(find "$LOCKS_ROOT" -path "*/locks/active/*.lock" -type f 2>/dev/null)

echo "========================================"
echo "  汇总: $total 个活跃任务"
echo "    ✅ 正常: $normal"
echo "    ⚠️ 异常: $heartbeat_warn (含 SESSION_DEAD / STALLED / HEARTBEAT_DELAY)"
echo "    🚫 abandoned 待接管: $abandoned"
echo "========================================"

if [[ $abandoned -gt 0 ]]; then
  echo ""
  echo "需要接管的任务（共 $abandoned 个）："
  echo "建议: 检查上述 🚫 ABANDONED 任务，决定是继续还是放弃"
fi
