#!/bin/bash
set -e  # 遇错退出
set -u  # 未定义变量报错
set -o pipefail  # 管道命令失败检测

# 自媒体写作助手 - 保存文章脚本
# 用途：将写好的文章保存到当前项目目录

echo "📝 自媒体写作助手 - 保存文章"
echo "======================================"
echo ""

# 检查参数
if [ -z "$1" ]; then
    echo "❌ 请提供文章标题"
    echo "用法: ./保存文章.sh \"文章标题\""
    echo ""
    echo "示例:"
    echo "  ./保存文章.sh \"Claude Code 使用体验\""
    exit 1
fi

ARTICLE_TITLE="$1"
DATE=$(date +%Y.%m.%d)
FILENAME="$DATE $ARTICLE_TITLE.md"
FILEPATH="./$FILENAME"

# 验证文件名（避免特殊字符）
if [[ "$ARTICLE_TITLE" =~ [/\\:\*\?\"\<\>\|] ]]; then
    echo "❌ 文件名包含非法字符: / \\ : * ? \" < > |"
    echo "请使用合法的文件名"
    exit 1
fi

# 检查文件是否已存在
if [ -f "$FILEPATH" ]; then
    echo "⚠️  文件已存在：$FILEPATH"
    echo ""
    read -p "是否覆盖？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 1
    fi
fi

# 从标准输入读取文章内容
echo "📝 请粘贴文章内容（按 Ctrl+D 结束输入）："
echo ""

cat > "$FILEPATH"

echo ""
echo "✅ 文章已保存：$FILEPATH"
echo ""
echo "📊 文章信息："
WORD_COUNT=$(cat "$FILEPATH" | wc -m | xargs)
LINE_COUNT=$(cat "$FILEPATH" | wc -l | xargs)
echo "   - 文件大小：$WORD_COUNT 字符"
echo "   - 行数：$LINE_COUNT"
echo "   - 保存时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "💡 下一步："
echo "   - 如果需要修改，请手动编辑该文件"
echo "   - 发布后将文件移动到 \`../历史存档/\` 目录"
