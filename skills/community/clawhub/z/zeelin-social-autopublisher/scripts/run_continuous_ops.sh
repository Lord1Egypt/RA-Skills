#!/bin/bash
# THUQX AutoOps — Continuous mode
# 用法: bash scripts/run_continuous_ops.sh "主题"
# 每轮运行 run_social_ops_v5.sh，然后随机等待 4-12 小时再继续。
set -euo pipefail

TOPIC="${1:-AI认知债务}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

while true; do
  echo ""
  echo "========== AutoOps continuous =========="
  echo "Topic: ${TOPIC}"
  echo "Start: $(date)"
  echo "======================================="

  bash "${SCRIPT_DIR}/run_social_ops_v5.sh" "${TOPIC}"

  WAIT_HOURS=$((4 + RANDOM % 9))   # 4..12
  WAIT_MIN=$((RANDOM % 60))        # 0..59
  echo ""
  echo "下一轮运营将在 ${WAIT_HOURS} 小时 ${WAIT_MIN} 分钟后执行"
  sleep $((WAIT_HOURS * 3600 + WAIT_MIN * 60))
done

