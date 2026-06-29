#!/usr/bin/env bash
# setup.sh - md2wechat 微信公众号配置检查
# Usage: ./setup.sh

set -euo pipefail

if ! command -v md2wechat >/dev/null 2>&1; then
  echo "❌ md2wechat CLI 未安装或不在 PATH"
  echo "请先安装 md2wechat，并确认 md2wechat --help 可用"
  exit 1
fi

CONFIG="$HOME/.config/md2wechat/config.yaml"

if [ ! -f "$CONFIG" ]; then
  echo "❌ 找不到 md2wechat 配置文件: $CONFIG"
  echo "可先运行：md2wechat config init"
  echo "然后配置 wechat.appid / wechat.secret"
  exit 1
fi

md2wechat config validate --json

echo "✅ md2wechat 配置校验完成"
echo "配置文件: $CONFIG"
echo "提示：当前公网 IP 必须在微信公众号后台 IP 白名单中"
