#!/bin/bash
# ============================================================
# WebSocket 连接延迟检测工具 - 测试用例脚本
# 功能：验证 ws_check.sh 在各种场景下的正确性
# 用法：bash test_cases.sh
# ============================================================

set -uo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_CHECK="$SCRIPT_DIR/ws_check.sh"

TOTAL=0
PASSED=0
FAILED=0

# 测试辅助函数
run_test() {
    local name="$1"
    local cmd="$2"
    local expect="$3"  # "pass" 或 "fail"

    TOTAL=$((TOTAL + 1))
    echo -ne "  [${TOTAL}] ${name}... "

    local output
    output=$(eval "$cmd" 2>&1)
    local exit_code=$?

    if [ "$expect" = "pass" ] && [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ 通过${NC}"
        PASSED=$((PASSED + 1))
    elif [ "$expect" = "fail" ] && [ $exit_code -ne 0 ]; then
        echo -e "${GREEN}✓ 通过${NC} (预期失败, 退出码=$exit_code)"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ 失败${NC} (退出码=$exit_code, 预期=$expect)"
        echo -e "    ${YELLOW}输出: $(echo "$output" | head -3)${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# 检查输出包含指定文本
run_test_contains() {
    local name="$1"
    local cmd="$2"
    local expected_text="$3"

    TOTAL=$((TOTAL + 1))
    echo -ne "  [${TOTAL}] ${name}... "

    local output
    output=$(eval "$cmd" 2>&1)

    if echo "$output" | grep -q "$expected_text"; then
        echo -e "${GREEN}✓ 通过${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ 失败${NC} (输出中未找到: $expected_text)"
        echo -e "    ${YELLOW}前3行: $(echo "$output" | head -3)${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# ==================== 测试开始 ====================

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}  WebSocket 延迟检测工具 - 测试用例${NC}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ---- 测试组 1：参数解析 ----
echo -e "${CYAN}[测试组 1] 参数解析${NC}"

run_test "无参数时显示帮助" \
    "bash $WS_CHECK 2>&1" \
    "fail"

run_test_contains "帮助信息包含用法说明" \
    "bash $WS_CHECK --help" \
    "用法"

run_test_contains "帮助信息包含协议选项" \
    "bash $WS_CHECK -h" \
    "protocol"

run_test "未知选项报错" \
    "bash $WS_CHECK --unknown 2>&1" \
    "fail"

run_test "-p 参数缺少值时报错" \
    "bash $WS_CHECK -p 2>&1" \
    "fail"

run_test "-p 参数值非法时报错" \
    "bash $WS_CHECK -p http example.com 2>&1" \
    "fail"

echo ""

# ---- 测试组 2：URL 解析 ----
echo -e "${CYAN}[测试组 2] URL 与协议解析${NC}"

run_test_contains "wss URL 识别协议类型" \
    "bash $WS_CHECK wss://example.com/ws 1 2>&1 | head -20" \
    "wss"

run_test_contains "-p ws 覆盖 URL 中的 wss" \
    "bash $WS_CHECK -p ws wss://example.com/ws 1 2>&1 | head -20" \
    "由 -p 参数指定"

run_test "无协议前缀且无 -p 时报错" \
    "bash $WS_CHECK example.com/ws 2>&1" \
    "fail"

run_test_contains "-p wss + 无前缀 URL 正常工作" \
    "bash $WS_CHECK -p wss example.com/ws 1 2>&1 | head -20" \
    "wss"

echo ""

# ---- 测试组 3：实际连接测试（需要网络） ----
echo -e "${CYAN}[测试组 3] 实际连接测试（需要网络）${NC}"
echo -e "  ${YELLOW}注意：以下测试需要网络连接，如在离线环境会标记为失败${NC}"

# 测试公共 WebSocket 服务
run_test_contains "wss 协议连接测试" \
    "bash $WS_CHECK wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 1 2>&1" \
    "DNS解析"

run_test_contains "报告包含性能评级" \
    "bash $WS_CHECK wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 1 2>&1" \
    "性能分析报告"

run_test_contains "报告包含瓶颈分析" \
    "bash $WS_CHECK wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 1 2>&1" \
    "瓶颈分析"

run_test_contains "报告包含时序图" \
    "bash $WS_CHECK wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 1 2>&1" \
    "连接流程时序图"

echo ""

# ---- 测试组 4：wss 特有环节 ----
echo -e "${CYAN}[测试组 4] 协议差异检测${NC}"

run_test_contains "wss 模式包含 TLS 握手" \
    "bash $WS_CHECK wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 1 2>&1" \
    "TLS握手"

run_test_contains "wss 模式检测环节显示 TLS" \
    "bash $WS_CHECK wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS 1 2>&1" \
    "DNS → TCP → TLS → WS Upgrade"

echo ""

# ==================== 测试汇总 ====================
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${BOLD}测试汇总${NC}"
echo -e "  总计: ${TOTAL}  ${GREEN}通过: ${PASSED}${NC}  ${RED}失败: ${FAILED}${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "  ${GREEN}🎉 所有测试通过！${NC}"
else
    echo -e "  ${YELLOW}⚠ ${FAILED} 个测试失败，请检查上方详情${NC}"
fi
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

exit $FAILED
