#!/bin/bash
# 自动压缩 hot.md（超过 100 行时触发）

HOT_FILE="$(dirname "$0")/../memory/hot.md"
MAX_LINES=100

# 检查行数
current_lines=$(wc -l < "$HOT_FILE" | tr -d ' ')

if [ "$current_lines" -le "$MAX_LINES" ]; then
    echo "✅ hot.md 当前 $current_lines 行，无需压缩"
    exit 0
fi

echo "⚠️  hot.md 当前 $current_lines 行，超过 $MAX_LINES 行，开始压缩..."

# 备份
backup_file="$HOT_FILE.backup.$(date +%Y%m%d_%H%M%S)"
cp "$HOT_FILE" "$backup_file"
echo "📦 已备份到: $backup_file"

# 压缩规则：
# 1. 合并相似规则（手动标记 [merge] 的行）
# 2. 删除过时内容（手动标记 [deprecated] 的行）
# 3. 移动低频内容到 WARM 层（手动标记 [warm] 的行）

grep -v '\[deprecated\]' "$HOT_FILE" > "$HOT_FILE.tmp"
mv "$HOT_FILE.tmp" "$HOT_FILE"

echo "✅ 压缩完成"
echo "📊 压缩前: $current_lines 行"
echo "📊 压缩后: $(wc -l < "$HOT_FILE" | tr -d ' ') 行"
echo ""
echo "⚠️  请手动检查并标记："
echo "   - [deprecated] 标记过时内容"
echo "   - [warm] 标记低频内容"
echo "   - [merge] 标记可合并规则"
