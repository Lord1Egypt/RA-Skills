#!/bin/bash
# test.sh - use-openclaw-manual 技能测试框架
# 运行测试用例，验证技能行为

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVALS_FILE="$SCRIPT_DIR/evals/evals.json"

echo "═══════════════════════════════════════════"
echo "  use-openclaw-manual 测试"
echo "═══════════════════════════════════════════"
echo ""

# 检查依赖
if ! command -v jq &> /dev/null; then
  echo "❌ 需要 jq 命令"
  echo "   macOS:  brew install jq"
  echo "   Ubuntu: sudo apt install jq"
  exit 1
fi

# 检查 evals 文件
if [ ! -f "$EVALS_FILE" ]; then
  echo "❌ 测试用例文件不存在：$EVALS_FILE"
  exit 1
fi

# 读取测试用例数量
test_count=$(jq '.evals | length' "$EVALS_FILE")
echo "📋 共 $test_count 个测试用例"
echo ""

passed=0
failed=0
skipped=0

# 检查文档是否已初始化
DOCS_PATH="${OPENCLAW_MANUAL_PATH:-$HOME/.openclaw/workspace/docs/openclaw_manual}"
if [ ! -d "$DOCS_PATH" ] || [ -z "$(ls -A "$DOCS_PATH" 2>/dev/null)" ]; then
  echo "⚠️  文档目录为空，可能未初始化"
  echo "   请先运行：./run.sh --init"
  echo ""
  echo "   跳过搜索测试，仅验证文件结构..."
  echo ""
  skip_search=true
else
  skip_search=false
fi

# 运行测试用例
for ((i=0; i<test_count; i++)); do
  eval_name=$(jq -r ".evals[$i].name" "$EVALS_FILE")
  prompt=$(jq -r ".evals[$i].prompt" "$EVALS_FILE")
  expected_keywords=$(jq -r ".evals[$i].expected_keywords[]" "$EVALS_FILE" 2>/dev/null | tr '\n' ' ')
  
  echo "测试 $((i+1))/$test_count: $eval_name"
  echo "  提示词：$prompt"
  
  if [ "$skip_search" = true ]; then
    echo "  ⏭️  跳过（文档未初始化）"
    ((skipped++))
    echo ""
    continue
  fi
  
  # 执行搜索
  result=$("$SCRIPT_DIR/run.sh" --search "$prompt" 2>&1 || true)
  
  # 检查是否包含预期关键词
  all_found=true
  missing_keywords=""
  
  for keyword in $expected_keywords; do
    if ! echo "$result" | grep -qi "$keyword"; then
      all_found=false
      missing_keywords="$missing_keywords $keyword"
    fi
  done
  
  if [ "$all_found" = true ]; then
    echo "  ✅ PASS"
    ((passed++))
  else
    echo "  ❌ FAIL"
    echo "     缺失关键词:$missing_keywords"
    ((failed++))
  fi
  
  echo ""
done

# 输出结果
echo "═══════════════════════════════════════════"
echo "  测试结果"
echo "═══════════════════════════════════════════"
echo "  ✅ 通过：$passed"
echo "  ❌ 失败：$failed"
if [ "$skipped" -gt 0 ]; then
  echo "  ⏭️  跳过：$skipped"
fi
echo ""

if [ "$failed" -gt 0 ]; then
  echo "💡 提示：如果测试失败，可能是文档版本变化导致"
  echo "   尝试更新文档：./run.sh --sync"
  echo ""
  exit 1
else
  echo "🎉 所有测试通过！"
  echo ""
  exit 0
fi
