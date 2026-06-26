#!/bin/bash
# ilink_probe.sh — 微信推送链路探活
#
# 用法：ilink_probe.sh
# 退出码：
#   0 = 链路健康（推送能到手机微信）
#   1 = 链路断了
#   2 = 配置错误
#
# 设计：测的是"真推送能力"——调 wechat-push 推一条 silent 测试，
# 真正能 push 通 = 链路健康。这比裸调 ilink 准（裸调可能因为网络层问题假阴性）。

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUSH="${SCRIPT_DIR}/wechat_push.py"
TEST_MSG="🔍 [probe] $(date '+%H:%M:%S') probe-id=$$"

if [ ! -f "$PUSH" ]; then
    echo "❌ CONFIG ERROR: $PUSH not found"
    exit 2
fi

OUT=$(python3 "$PUSH" --silent "$TEST_MSG" 2>&1)
RC=$?

if [ $RC -eq 0 ] && echo "$OUT" | grep -q "SUCCESS"; then
    echo "✅ HEALTHY: $OUT"
    exit 0
else
    echo "❌ DOWN: $OUT"
    exit 1
fi
