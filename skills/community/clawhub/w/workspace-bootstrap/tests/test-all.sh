#!/bin/bash

# 总测试入口脚本
# 运行所有 5 个测试场景

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "workspace-bootstrap 测试套件"
echo "========================================="
echo ""

# 计数器
TOTAL=0
PASSED=0
FAILED=0
FAILED_SCENARIOS=""

# 运行每个测试场景
for i in 1 2 3 4 5; do
    echo ""
    echo "运行测试场景 $i..."
    
    TOTAL=$((TOTAL + 1))
    
    if bash "$SCRIPT_DIR/test-scenario-$i.sh"; then
        PASSED=$((PASSED + 1))
        echo "✅ 场景 $i 通过"
    else
        FAILED=$((FAILED + 1))
        FAILED_SCENARIOS="$FAILED_SCENARIOS $i"
        echo "❌ 场景 $i 失败"
    fi
    
    echo ""
    echo "----------------------------------------"
done

# 输出测试报告
echo ""
echo "========================================="
echo "测试报告"
echo "========================================="
echo ""
echo "总计：$TOTAL 个场景"
echo "通过：$PASSED 个场景"
echo "失败：$FAILED 个场景"
echo ""

# 计算通过率
PASS_RATE=$(awk "BEGIN {printf \"%.2f\", $PASSED * 100 / $TOTAL}")
echo "通过率：$PASS_RATE%"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "失败的场景：$FAILED_SCENARIOS"
    echo ""
fi

# 验收标准：通过率 ≥ 80%
if (( $(awk "BEGIN {print ($PASS_RATE >= 80.00) ? 1 : 0}") )); then
    echo "✅ 测试通过（通过率 ≥ 80%）"
    exit 0
else
    echo "❌ 测试失败（通过率 < 80%）"
    exit 1
fi
