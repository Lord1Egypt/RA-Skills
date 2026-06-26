#!/bin/bash
# Viking Memory System - sv_decompress
# Phase 3: Archive 逆向解压
#
# 功能：
# 1. 读取 archive 文件的 summary 摘要
# 2. 按需解压完整内容（从 .archive.full 文件）
# 3. 可将解压后的内容合并回原文件
#
# 用法:
#   sv_decompress.sh <archive_file>           # 只显示摘要
#   sv_decompress.sh <archive_file> --show    # 显示完整内容
#   sv_decompress.sh <archive_file> --restore # 恢复到原目录（promote 回 hot）
#   sv_decompress.sh <archive_file> --restore --layer warm # 指定恢复到 warm 层

set -e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"
WORKSPACE="${SV_WORKSPACE:-$HOME/.openclaw/viking-maojingli}"
SHOW_FULL=false
RESTORE=false
TARGET_LAYER="hot"

# 解析参数
while [ $# -gt 0 ]; do
    case "$1" in
        --show) SHOW_FULL=true; shift ;;
        --restore) RESTORE=true; shift ;;
        --layer) TARGET_LAYER="$2"; shift 2 ;;
        *) [ -z "$FILE" ] && FILE="$1"; shift ;;
    esac
done

[ -z "$FILE" ] && { echo "用法: sv_decompress <file> [--show] [--restore] [--layer warm]"; exit 1; }
[ ! -f "$FILE" ] && { echo "文件不存在: $FILE"; exit 1; }

# ============ 解析 frontmatter ============
parse_fm() {
    awk -v key="$2" -- '
        BEGIN { in_fm=0 }
        /^---$/ { in_fm=1; next }
        /^---$/ && in_fm { exit }
        in_fm && $0 ~ "^" key ": *" {
            sub("^" key ": *", "")
            gsub(/^[ \t]+|[ \t]+$/, "")
            print; exit
        }
    ' "$1" 2>/dev/null
}

echo "=== Phase 3: Archive 逆向解压 ==="
echo "文件: $(basename "$FILE")"
echo ""

# ============ 读取摘要 ============
SUMMARY=$(parse_fm "$FILE" "summary")
FULL_CONTENT_FILE=$(parse_fm "$FILE" "full_content_file")
CURRENT_LAYER=$(parse_fm "$FILE" "current_layer")

echo "【Archive 摘要】"
if [ -n "$SUMMARY" ]; then
    echo "$SUMMARY"
else
    echo "（无摘要，请使用 sv_archive_summary.sh 先生成）"
fi
echo ""

# ============ 检查完整内容 ============
if [ -n "$FULL_CONTENT_FILE" ]; then
    FULL_PATH="$(dirname "$FILE")/$FULL_CONTENT_FILE"
    if [ -f "$FULL_PATH" ]; then
        echo "✓ 完整内容可用: $(basename "$FULL_PATH")"
    else
        echo "⚠ 完整内容文件丢失: $FULL_CONTENT_FILE"
        FULL_PATH=""
    fi
else
    echo "⚠ 未找到完整内容记录（文件未用 --keep 保存）"
    FULL_PATH=""
fi

# ============ 显示完整内容 ============
if [ "$SHOW_FULL" = true ]; then
    echo ""
    echo "=== 完整内容 ==="
    if [ -n "$FULL_PATH" ] && [ -f "$FULL_PATH" ]; then
        cat "$FULL_PATH"
    else
        # 尝试从文件末尾读取（如果没有单独存储）
        CONTENT=$(sed -n '/^---$/,/^---$/d; p' "$FILE" 2>/dev/null)
        if [ -n "$CONTENT" ] && [ "${#CONTENT}" -gt 100 ]; then
            echo "$CONTENT"
        else
            echo "（完整内容不可用）"
        fi
    fi
fi

# ============ 恢复到目标层 ============
if [ "$RESTORE" = true ]; then
    echo ""
    echo "=== 恢复到 $TARGET_LAYER 层 ==="

    if [ "$CURRENT_LAYER" != "L0" ] && [ "$CURRENT_LAYER" != "L1" ] && [ "$CURRENT_LAYER" != "L2" ] && [ "$CURRENT_LAYER" != "L3" ] && [ "$CURRENT_LAYER" != "L4" ]; then
        CURRENT_LAYER="L4"
    fi

    # 确定层级名称
    case "$TARGET_LAYER" in
        hot) LAYER_NAME="hot";;
        warm) LAYER_NAME="warm";;
        cold) LAYER_NAME="cold";;
        archive) LAYER_NAME="archive";;
        *) LAYER_NAME="hot";;
    esac

    # 计算目标路径
    local memories_dir
    memories_dir=$(dirname "$(dirname -- "$FILE")")  # .../memories/{layer}/file.md
    memories_dir=$(dirname "$memories_dir")           # .../memories
    TARGET_DIR="$memories_dir/$LAYER_NAME"
    TARGET_PATH="$TARGET_DIR/$(basename "$FILE")"

    echo "目标: $TARGET_PATH"

    mkdir -p "$TARGET_DIR"

    # 检查目标是否已存在
    if [ -f "$TARGET_PATH" ]; then
        echo "⚠ 目标文件已存在，跳过"
        exit 1
    fi

    # 读取完整内容
    RESTORE_CONTENT=""
    if [ -n "$FULL_PATH" ] && [ -f "$FULL_PATH" ]; then
        RESTORE_CONTENT=$(cat "$FULL_PATH")
    else
        RESTORE_CONTENT=$(sed -n '/^---$/,/^---$/d; p' "$FILE" 2>/dev/null)
    fi

    # 创建恢复后的文件（保留 frontmatter，更新层级）
    TMP_FILE="${FILE}.decompress.tmp"
    {
        # 保留原始 frontmatter 但更新 current_layer 和 target_layer
        awk -- '
        BEGIN { in_fm=0 }
        /^---$/ { in_fm=1; print; next }
        /^---$/ && in_fm { in_fm=0; print; next }
        in_fm && /^current_layer:/ { print "current_layer: L0"; next }
        in_fm && /^target_layer:/ { print "target_layer: hot"; next }
        { print }
        ' "$FILE" | sed '/^summary:/d' | sed '/^full_content_file:/d'
        echo "---"
        echo ""
        echo "$RESTORE_CONTENT"
    } > "$TMP_FILE"

    mv -f "$TMP_FILE" "$TARGET_PATH"
    echo "✓ 已恢复到 $LAYER_NAME 层"
    echo "✓ 文件: $(basename "$TARGET_PATH")"

    # 可选：删除 archive 文件
    # rm -f "$FILE"
fi

echo ""
echo "=== 完成 ==="
exit 0
