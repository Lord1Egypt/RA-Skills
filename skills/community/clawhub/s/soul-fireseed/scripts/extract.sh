#!/bin/bash
# scripts/extract.sh
# 火种·灵魂 v2.0 - 快速提取脚本

echo "🔥 火种·灵魂 v2.0 - 化石提取工具"
echo "================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

# 默认参数
INPUT_FILE=""
OUTPUT_DIR="user-data/fossils/"
PARALLEL=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --input|-i)
            INPUT_FILE="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --parallel|-p)
            PARALLEL=true
            shift
            ;;
        --help|-h)
            echo "用法: ./extract.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --input, -i FILE    输入文件路径"
            echo "  --output, -o DIR    输出目录 (默认: user-data/fossils/)"
            echo "  --parallel, -p      启用并行提取"
            echo "  --help, -h          显示帮助信息"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

# 检查输入文件
if [ -z "$INPUT_FILE" ]; then
    echo "❌ 错误: 请指定输入文件 (--input)"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ 错误: 文件不存在: $INPUT_FILE"
    exit 1
fi

echo "📝 输入文件: $INPUT_FILE"
echo "📂 输出目录: $OUTPUT_DIR"
echo "⚡ 并行模式: $PARALLEL"
echo ""

# 执行提取
python3 -c "
import sys
sys.path.insert(0, 'lib')

from extractor import FossilExtractor
from utils import save_fossil

# 读取输入
with open('$INPUT_FILE', 'r', encoding='utf-8') as f:
    text = f.read()

# 提取化石
extractor = FossilExtractor(parallel=$PARALLEL)
fossils = extractor.extract(text)

print(f'✅ 提取了 {len(fossils)} 个化石')

# 保存化石
for fossil in fossils:
    path = save_fossil(fossil, '$OUTPUT_DIR')
    print(f'  💾 {path}')

# 显示统计
stats = extractor.get_extraction_stats()
print(f'\n📊 统计信息:')
print(f'  提取次数: {stats[\"extraction_count\"]}')
print(f'  总化石数: {stats[\"total_fossils_extracted\"]}')
print(f'  平均每次: {stats[\"avg_fossils_per_extraction\"]:.2f}')
"

echo ""
echo "✨ 完成！"
