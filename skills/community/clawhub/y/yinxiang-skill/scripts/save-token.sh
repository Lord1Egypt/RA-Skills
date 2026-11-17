#!/bin/bash
# 用于 Claude Code / Codex 平台保存 Token
# 用法: ./save-token.sh <YX_AUTH_TOKEN>
TOKEN="$1"
if [ -z "$TOKEN" ]; then
  echo "用法: $0 <Token>"
  echo "Token 是以 S=s 开头的字符串，从 https://app.yinxiang.com/third/skills-oauth/ 获取"
  exit 1
fi
mkdir -p ~/.config/yinxiang-skill
echo "$TOKEN" > ~/.config/yinxiang-skill/token
chmod 600 ~/.config/yinxiang-skill/token
echo "Token 已保存到 ~/.config/yinxiang-skill/token"
