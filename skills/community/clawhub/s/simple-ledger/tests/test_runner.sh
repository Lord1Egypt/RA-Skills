#!/usr/bin/env bash
# ─────────────────────────────────────────────────────
# 个人记账 Skill - 测试运行脚本
# 支持 CI 集成，退出码反映测试结果
# ─────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TEST_SCRIPT="$SCRIPT_DIR/run_tests.py"
RESULTS_DIR="$SCRIPT_DIR/results"

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🧪 个人记账 Skill - 测试运行器${NC}"
echo "────────────────────────────────────────"

# 检查 Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ python3 未安装${NC}"
    exit 1
fi

# 检查测试用例文件
if [ ! -f "$SCRIPT_DIR/eval_cases.yaml" ]; then
    echo -e "${RED}❌ 测试用例文件不存在: eval_cases.yaml${NC}"
    exit 1
fi

# 检查测试账本
if [ ! -f "$SCRIPT_DIR/fixtures/sample.ledger" ]; then
    echo -e "${RED}❌ 测试账本不存在: fixtures/sample.ledger${NC}"
    exit 1
fi

# 创建结果目录
mkdir -p "$RESULTS_DIR"

# 运行测试
echo ""
if python3 "$TEST_SCRIPT"; then
    echo -e "${GREEN}✅ 所有测试通过${NC}"
    exit 0
else
    echo -e "${RED}⚠️  存在失败的测试用例${NC}"
    exit 1
fi
