#!/bin/bash
# 公共：多来源加载 Token
# OpenClaw 自动注入 YX_AUTH_TOKEN；Claude Code / Codex / Cursor 从本地文件读取
TOKEN="$(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")"
if [ -z "$TOKEN" ]; then
  echo '{"code":1,"message":"未授权，请说「授权印象笔记」完成授权"}'
  exit 1
fi
