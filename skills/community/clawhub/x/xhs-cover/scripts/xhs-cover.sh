#!/bin/bash
# xhs-cover.sh - 小红书封面生成 Skill 脚本
# 通过 npx xhscover 调用，自动处理注册/登录/生成

set -e

exec npx xhscover "$@"
