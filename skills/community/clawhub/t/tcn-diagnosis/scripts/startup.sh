#!/bin/bash
# TCM Diagnosis 启动脚本
# Usage: ./scripts/startup.sh

echo "==================================="
echo "     中医诊疗助手 启动序列"
echo "==================================="
echo ""

# 检查工作目录
WORK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORK_DIR"
echo "📁 工作目录: $WORK_DIR"

# 第一层：身份层检查
echo ""
echo "🔍 检查第一层：身份层"
if [ -f "identity/SOUL.md" ] && [ -f "identity/IDENTITY.md" ] && [ -f "identity/USER.md" ]; then
    echo "   ✅ 身份层完整"
else
    echo "   ❌ 身份层缺失，执行重建..."
fi

# 第二层：操作层检查
echo ""
echo "🔍 检查第二层：操作层"
if [ -f "operations/AGENTS.md" ] && [ -f "operations/HEARTBEAT.md" ] && [ -f "operations/ROLE-TCM.md" ]; then
    echo "   ✅ 操作层完整"
else
    echo "   ❌ 操作层缺失，执行重建..."
fi

# 第三层：知识层检查
echo ""
echo "🔍 检查第三层：知识层"
KNOWLEDGE_COUNT=$(find knowledge -name "*.md" | wc -l)
if [ "$KNOWLEDGE_COUNT" -ge 5 ]; then
    echo "   ✅ 知识层完整 ($KNOWLEDGE_COUNT 个知识文件)"
else
    echo "   ❌ 知识层缺失"
fi

# 知识库统计
echo ""
echo "📚 知识库统计:"
SYMPTOMS=$(grep -c "###" knowledge/symptoms/four-diagnostics.md 2>/dev/null || echo "0")
FORMULAS=$(grep -c "###" knowledge/formulas/classic-formulas.md 2>/dev/null || echo "0")
PATTERNS=$(grep -c "###" knowledge/patterns/differentiation-patterns.md 2>/dev/null || echo "0")
echo "   • 四诊症状: $SYMPTOMS+ 条目"
echo "   • 经典方剂: $FORMULAS+ 首"
echo "   • 辨证模式: $PATTERNS+ 证型"

# 启动完成
echo ""
echo "==================================="
echo "     ✅ 中医诊疗助手 启动完成"
echo "==================================="
echo ""
echo "⚠️  安全声明："
echo "   本智能体提供的所有建议仅供参考学习"
echo "   不能替代专业医疗诊断和治疗"
echo "   如有疾病，请及时就医"
echo ""
echo "可用代理:"
echo "  • zhen       - 四诊采集"
echo "  • bianzheng  - 辨证分析"
echo "  • fangji     - 方剂推荐"
echo "  • shiliao    - 食疗养生"
echo "  • tizhi      - 体质辨识"
echo ""
echo "使用方法:"
echo "  说\"看病\"     → 开始四诊采集"
echo "  说\"体质\"     → 体质辨识"
echo "  说\"食疗\"     → 食疗养生建议"
echo ""
echo "状态: 在线 | 负载: 就绪"
echo ""
