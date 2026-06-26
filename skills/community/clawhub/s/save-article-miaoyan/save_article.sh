#!/bin/bash
# save-article-miaoyan 集成脚本
# 用法: bash save_article.sh <url>

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SKILL_DIR/save_article_to_miaoyan.py"

if [ -z "$1" ]; then
    echo "Usage: bash save_article.sh <article_url>"
    exit 1
fi

python3 "$SCRIPT" "$1"
