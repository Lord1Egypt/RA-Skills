#!/bin/bash
# scripts/distill.sh
# 火种·灵魂 v2.0 - 批量蒸馏脚本

echo "🔥 火种·灵魂 v2.0 - 人格蒸馏工具"
echo "================================"

# 默认参数
OUTPUT_FILE="user-data/persona/profile.md"
DAYS=30

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --days|-d)
            DAYS="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: ./distill.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --output, -o FILE   输出文件路径 (默认: user-data/persona/profile.md)"
            echo "  --days, -d NUM      回溯天数 (默认: 30)"
            echo "  --help, -h          显示帮助信息"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

echo "📂 输出文件: $OUTPUT_FILE"
echo "📅 回溯天数: $DAYS"
echo ""

# 执行蒸馏
python3 -c "
import sys
import os
sys.path.insert(0, 'lib')

from distiller import FossilDistiller
from utils import load_all_fossils

# 加载化石
print('📚 加载化石...')
fossils = load_all_fossils('user-data/fossils/')
print(f'  找到 {len(fossils)} 个化石')

if len(fossils) == 0:
    print('❌ 错误: 未找到化石，请先运行提取')
    sys.exit(1)

# 蒸馏
print('🔬 开始蒸馏...')
distiller = FossilDistiller()
persona = distiller.distill(fossils)

print(f'✅ 蒸馏完成！版本: {persona.version}')

# 生成报告
print('📝 生成报告...')
report = distiller.generate_evolution_report(days=$DAYS)

# 保存报告
os.makedirs(os.path.dirname('$OUTPUT_FILE'), exist_ok=True)
with open('$OUTPUT_FILE', 'w', encoding='utf-8') as f:
    f.write(report)

print(f'💾 报告已保存: $OUTPUT_FILE')

# 显示概览
print(f'\n📊 人格概览:')
for dim_name, dim_data in persona.dimensions.items():
    print(f'  {dim_name}: {dim_data[\"confidence\"]:.2f}')
"

echo ""
echo "✨ 完成！"
