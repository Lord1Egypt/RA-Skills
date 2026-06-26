#!/usr/bin/env bash
# 快速自检脚本 - 5分钟完成
# 使用方法: bash ~/.openclaw/skills/self-evolution/scripts/self_check.sh

echo "🔍 小鳌总快速自检"
echo "=================="
echo ""

# 检查今天的learnings文件
TODAY=$(date +%Y-%m-%d)
LEARNINGS_FILE="$HOME/.openclaw/workspace/.learnings/LEARNINGS.md"
ERRORS_FILE="$HOME/.openclaw/workspace/.learnings/ERRORS.md"

if [ -f "$LEARNINGS_FILE" ]; then
    echo "✅ LEARNINGS.md 存在"
    TODAY_ENTRIES=$(grep -c "$TODAY" "$LEARNINGS_FILE" 2>/dev/null || echo "0")
    echo "   今日记录: $TODAY_ENTRIES 条"
else
    echo "⚠️ LEARNINGS.md 不存在"
fi

if [ -f "$ERRORS_FILE" ]; then
    echo "✅ ERRORS.md 存在"
    TODAY_ERRORS=$(grep -c "$TODAY" "$ERRORS_FILE" 2>/dev/null || echo "0")
    echo "   今日错误: $TODAY_ERRORS 条"
else
    echo "⚠️ ERRORS.md 不存在"
fi

echo ""
echo "📋 快速三问:"
echo "1. 今天老板纠正了你什么？(找到pattern)"
echo "2. 你说了哪些'可能'/'大概'/'不确定'？"
echo "3. 老板哪些事没回音？(可能不满意)"
echo ""

# 检查MEMORY.md最后更新时间（兼容Linux和macOS）
MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
    # Linux: stat -c %y  | macOS: stat -f %Sm
    if command -v stat >/dev/null 2>&1; then
        if [[ "$(uname)" == "Darwin" ]]; then
            # macOS
            LAST_MOD=$(stat -f %Sm -t %Y "$MEMORY_FILE" 2>/dev/null || echo "未知")
        else
            # Linux
            LAST_MOD=$(stat -c %y "$MEMORY_FILE" 2>/dev/null | cut -d' ' -f1)
        fi
        echo "📝 MEMORY.md 最后更新: $LAST_MOD"
    else
        echo "📝 MEMORY.md 存在（stat命令不可用，无法显示更新时间）"
    fi
fi

echo ""
echo "🎯 如需完整分析，运行: cat ~/.openclaw/skills/self-evolution/SKILL.md"
