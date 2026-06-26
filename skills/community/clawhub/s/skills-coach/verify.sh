#!/bin/bash
# Skills-Coach v2.0.0 功能验证脚本

echo "=========================================="
echo "Skills-Coach v2.0.0 功能验证"
echo "=========================================="
echo ""

# 1. 检查版本
echo "1. 检查版本..."
VERSION=$(cat VERSION)
echo "   ✓ 版本: $VERSION"
echo ""

# 2. 检查核心文件
echo "2. 检查核心文件..."
files=(
    "orchestrator.py"
    "config.yaml"
    "SKILL.md"
    "README_TRAINING_FREE_GRPO.md"
    "subskills/optimize-agent/training_free_grpo_optimizer.py"
    "subskills/optimize-agent/grpo_optimizer.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file (缺失)"
    fi
done
echo ""

# 3. 检查 Python 语法
echo "3. 检查 Python 语法..."
python3 -m py_compile subskills/optimize-agent/training_free_grpo_optimizer.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ training_free_grpo_optimizer.py 语法正确"
else
    echo "   ✗ training_free_grpo_optimizer.py 语法错误"
fi
echo ""

# 4. 检查依赖
echo "4. 检查依赖..."
python3 -c "import anthropic; print('   ✓ anthropic SDK 已安装')" 2>/dev/null || echo "   ⚠ anthropic SDK 未安装（部分功能受限）"
python3 -c "import yaml; print('   ✓ yaml 已安装')" 2>/dev/null || echo "   ✗ yaml 未安装"
echo ""

# 5. 检查配置
echo "5. 检查配置..."
METHOD=$(python3 -c "import yaml; c=yaml.safe_load(open('config.yaml')); print(c.get('optimization', {}).get('method', 'N/A'))")
echo "   优化方法: $METHOD"

if [ "$METHOD" = "training_free_grpo" ]; then
    echo "   ✓ 已配置为 Training-Free GRPO"
else
    echo "   ⚠ 当前使用: $METHOD"
fi
echo ""

# 6. 统计代码行数
echo "6. 代码统计..."
LINES=$(wc -l subskills/optimize-agent/training_free_grpo_optimizer.py | awk '{print $1}')
echo "   Training-Free GRPO 优化器: $LINES 行"
echo ""

# 7. 检查文档
echo "7. 检查文档..."
if grep -q "Training-Free GRPO" SKILL.md; then
    echo "   ✓ SKILL.md 包含 Training-Free GRPO 说明"
fi
if grep -q "v2.0.0" SKILL.md; then
    echo "   ✓ SKILL.md 版本已更新"
fi
echo ""

echo "=========================================="
echo "验证完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  python orchestrator.py /path/to/target-skill"
echo ""
echo "配置文件:"
echo "  config.yaml - 修改 optimization.method 选择优化方法"
echo ""
echo "文档:"
echo "  SKILL.md - 主文档"
echo "  README_TRAINING_FREE_GRPO.md - 详细说明"
echo "  COMPLETION_SUMMARY.md - 完成总结"
echo ""
