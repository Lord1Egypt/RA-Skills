#!/bin/bash
# system-healthcheck 测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
cd "$SKILL_DIR"

echo "======================================"
echo "system-healthcheck Test Suite"
echo "======================================"
echo ""

# 测试 1: L1 快速检查
echo "Test 1: L1 Fast Check"
echo "--------------------------------------"
python scripts/l1_fast_check.py
L1_EXIT=$?
echo "Exit code: $L1_EXIT"
echo ""

# 测试 2: L2 小时级检查
echo "Test 2: L2 Hourly Check"
echo "--------------------------------------"
python scripts/l2_hourly_check.py
L2_EXIT=$?
echo "Exit code: $L2_EXIT"
echo ""

# 测试 3: JSON 输出
echo "Test 3: JSON Output"
echo "--------------------------------------"
python scripts/l2_hourly_check.py --json | head -20
echo "..."
echo ""

# 测试 4: 心跳检查（强制）
echo "Test 4: Heartbeat Check (--force)"
echo "--------------------------------------"
python scripts/heartbeat.py --force
HB_EXIT=$?
echo "Exit code: $HB_EXIT"
echo ""

# 测试 5: 国际化
echo "Test 5: Internationalization"
echo "--------------------------------------"
echo "English:"
OPENCLAW_LOCALE=en python scripts/l1_fast_check.py --quiet && echo "OK" || echo "Failed"
echo ""
echo "Chinese:"
OPENCLAW_LOCALE=zh-CN python scripts/l1_fast_check.py --quiet && echo "OK" || echo "Failed"
echo ""

# 总结
echo "======================================"
echo "Test Summary"
echo "======================================"
echo "L1 Check: $([ $L1_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
echo "L2 Check: $([ $L2_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL (expected if services not running)')"
echo "Heartbeat: $([ $HB_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL (expected if issues detected)')"
echo ""
echo "All core tests completed!"
