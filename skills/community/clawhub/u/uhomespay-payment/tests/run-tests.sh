#!/usr/bin/env bash
# uhomespay-payment Skill 测试脚本
# 优先使用 openclaw test，回退到 yq 手动验证模式

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEST_FILE="$SCRIPT_DIR/test-cases.yaml"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================"
echo "  uhomespay-payment Skill 测试"
echo "============================================"
echo ""

# 检查测试文件是否存在
if [[ ! -f "$TEST_FILE" ]]; then
  echo -e "${RED}错误：测试文件不存在: $TEST_FILE${NC}"
  exit 1
fi

# 方式 1：尝试使用 openclaw test
if command -v openclaw &> /dev/null; then
  echo -e "${GREEN}检测到 openclaw，使用原生测试模式...${NC}"
  echo ""
  cd "$SKILL_DIR"
  openclaw test --cases "$TEST_FILE"
  exit $?
fi

# 方式 2：回退到 yq 手动验证
if ! command -v yq &> /dev/null; then
  echo -e "${YELLOW}未检测到 openclaw 或 yq。${NC}"
  echo ""
  echo "请安装以下工具之一："
  echo "  - openclaw: 参见 https://openclaw.dev/docs/cli"
  echo "  - yq:       brew install yq"
  echo ""
  echo "或者手动检查测试用例文件："
  echo "  $TEST_FILE"
  exit 1
fi

echo -e "${YELLOW}未检测到 openclaw，使用 yq 解析模式（仅验证 YAML 格式）...${NC}"
echo ""

# 解析并展示测试用例
TOTAL=$(yq 'length' "$TEST_FILE")
PASS=0
FAIL=0

for i in $(seq 0 $((TOTAL - 1))); do
  ID=$(yq ".[$i].id" "$TEST_FILE")
  DESC=$(yq ".[$i].description" "$TEST_FILE")
  INPUT=$(yq ".[$i].input" "$TEST_FILE")
  EXPECTED_COUNT=$(yq ".[$i].expected_contains | length" "$TEST_FILE")
  NOT_EXPECTED_COUNT=$(yq ".[$i].expected_not_contains | length" "$TEST_FILE")

  # 验证必要字段存在
  if [[ "$ID" == "null" || "$INPUT" == "null" ]]; then
    echo -e "${RED}✗ 用例 #$((i+1)): 缺少必要字段 (id 或 input)${NC}"
    FAIL=$((FAIL + 1))
    continue
  fi

  echo -e "${GREEN}✓ [$ID]${NC} $DESC"
  echo "  输入: $INPUT"
  echo "  期望包含: $EXPECTED_COUNT 个关键词"
  echo "  期望不包含: $NOT_EXPECTED_COUNT 个关键词"
  echo ""
  PASS=$((PASS + 1))
done

echo "============================================"
echo -e "  解析结果: ${GREEN}$PASS 通过${NC} / ${RED}$FAIL 失败${NC} / 共 $TOTAL 个用例"
echo "============================================"
echo ""

if [[ $FAIL -gt 0 ]]; then
  echo -e "${RED}存在格式错误的测试用例，请修复后重试。${NC}"
  exit 1
fi

echo -e "${GREEN}所有测试用例 YAML 格式正确。${NC}"
echo ""
echo "要进行完整的功能测试，请安装 openclaw CLI 后运行："
echo "  cd $SKILL_DIR && openclaw test --cases $TEST_FILE"
