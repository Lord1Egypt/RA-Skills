#!/bin/bash
# SKILL 关键词搜索脚本
# 用法: bash scripts/skill-search.sh <关键词>
# 示例: bash scripts/skill-search.sh 阑尾炎

SEARCH_TERM="$1"

if [ -z "$SEARCH_TERM" ]; then
    echo "用法: bash scripts/skill-search.sh <关键词>"
    echo "示例: bash scripts/skill-search.sh 骨折"
    exit 1
fi

echo "🔍 搜索技能关键词: $SEARCH_TERM"
echo "================================================"

# 在 SKILL.md 中搜索匹配的技能条目
grep -B1 -A3 "display:.*$SEARCH_TERM\|trigger:.*$SEARCH_TERM\|name:.*$SEARCH_TERM" SKILL.md \
  | grep -v "^--$" \
  | sed 's/^- name:/📌 技能ID:/' \
  | sed 's/^  display:/📋 名称:/' \
  | sed 's/^  trigger:/🎯 触发条件:/' \
  | sed 's/^  ref:/📄 文档:/'

echo ""
echo "================================================"
echo "也可直接搜索: grep -ri \"$SEARCH_TERM\" */SKILL.md"
