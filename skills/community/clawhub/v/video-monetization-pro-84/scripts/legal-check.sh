#!/bin/bash
# legal-check.sh - 法律合规审查脚本
# 用途：审查歌词/文案的法律风险

set -e

INPUT_FILE="$1"

if [ -z "$INPUT_FILE" ]; then
  echo "❌ 用法：./legal-check.sh [文件路径]"
  echo "示例：./legal-check.sh /path/to/lyrics.md"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "❌ 文件不存在：$INPUT_FILE"
  exit 1
fi

echo "⚖️  法律审查：$INPUT_FILE"

# 敏感词库（简化版，实际应更完整）
SENSITIVE_WORDS=(
  "最"
  "第一"
  "国家级"
  "政府"
  "共产党"
  "色情"
  "暴力"
  "赌博"
  "毒品"
)

RISK_LEVEL="🟢"
RISK_COUNT=0

echo ""
echo "## 审查开始"
echo ""

# 检查敏感词
for word in "${SENSITIVE_WORDS[@]}"; do
  if grep -q "$word" "$INPUT_FILE"; then
    echo "⚠️  发现敏感词：$word"
    RISK_COUNT=$((RISK_COUNT + 1))
  fi
done

echo ""

if [ $RISK_COUNT -eq 0 ]; then
  RISK_LEVEL="🟢"
  echo "✅ 未发现明显风险"
elif [ $RISK_COUNT -le 3 ]; then
  RISK_LEVEL="🟡"
  echo "⚠️  发现 $RISK_COUNT 个风险点，建议修改"
else
  RISK_LEVEL="🔴"
  echo "🛑 发现 $RISK_COUNT 个风险点，必须修改"
fi

echo ""
echo "## 审查结果"
echo "风险等级：$RISK_LEVEL"
echo "风险点数量：$RISK_COUNT"
echo ""

# 更新文件中的审查结果
sed -i.bak "s/### 审查结果.*/### 审查结果\n$RISK_LEVEL 风险点：$RISK_COUNT 个/" "$INPUT_FILE"

echo "📄 审查报告已更新到：$INPUT_FILE"
echo ""

if [ "$RISK_LEVEL" == "🔴" ]; then
  echo "🛑 高风险内容，需要大黄手动确认后才能发布"
  exit 2
elif [ "$RISK_LEVEL" == "🟡" ]; then
  echo "⚠️  中风险内容，建议修改后发布"
  exit 0
else
  echo "✅ 低风险内容，可以发布"
  exit 0
fi
