#!/bin/bash
# Theta量化交易系统发布脚本

echo "================================================================================"
echo "🚀 Theta量化交易系统 - ClawHub发布"
echo "================================================================================"

# 检查技能目录
if [ ! -d "/root/.openclaw/workspace/skills/theta-trading-system" ]; then
    echo "❌ 技能目录不存在"
    exit 1
fi

# 显示技能信息
echo ""
echo "📊 技能信息:"
echo "  名称: theta-trading-system"
echo "  版本: 1.0.0"
echo "  作者: Theta Team"
echo "  描述: 基于真实A股涨停股数据的智能选股系统"

# 显示文件结构
echo ""
echo "📁 文件结构:"
cd /root/.openclaw/workspace/skills/theta-trading-system
find . -type f -name "*.py" -o -name "*.md" -o -name "*.json" | head -20

# 检查必要文件
echo ""
echo "✅ 检查必要文件:"
if [ -f "SKILL.md" ]; then
    echo "  ✓ SKILL.md 存在"
else
    echo "  ❌ SKILL.md 缺失"
fi

if [ -f "README.md" ]; then
    echo "  ✓ README.md 存在"
else
    echo "  ❌ README.md 缺失"
fi

if [ -f "clawhub.json" ]; then
    echo "  ✓ clawhub.json 存在"
else
    echo "  ❌ clawhub.json 缺失"
fi

# 显示技能包大小
echo ""
echo "📦 技能包大小:"
ls -lh /root/.openclaw/workspace/skills/theta-trading-system.tar.gz 2>/dev/null || echo "  未创建技能包"

echo ""
echo "================================================================================"
echo "📋 发布步骤:"
echo "================================================================================"
echo ""
echo "1. 登录ClawHub:"
echo "   $ clawhub login"
echo ""
echo "2. 发布技能:"
echo "   $ cd /root/.openclaw/workspace/skills"
echo "   $ clawhub publish theta-trading-system"
echo ""
echo "3. 验证发布:"
echo "   $ clawhub search theta"
echo ""
echo "================================================================================"
echo "✅ 准备完成！"
echo "================================================================================"
