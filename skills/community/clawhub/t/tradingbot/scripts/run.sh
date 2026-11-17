#!/usr/bin/env bash
set -euo pipefail

# 该脚本从本地私有配置启动完整服务；不会读取或打印任何交易所密钥。
TARGET_DIR="${1:-${TRADINGBOT_INSTALL_DIR:-$PWD/tradingbot}}"
ENV_FILE="$TARGET_DIR/.env.local"

if [[ ! -f "$TARGET_DIR/bin/server" || ! -f "$TARGET_DIR/bin/strategy-runner" ]]; then
  printf '错误: 构建产物不完整，请先运行 install.sh\n' >&2
  exit 1
fi
if [[ ! -f "$ENV_FILE" ]]; then
  printf '错误: 缺少 %s，请先运行 install.sh\n' "$ENV_FILE" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

if [[ "${APP_ENV:-}" != "production" ]]; then
  printf '错误: APP_ENV 必须为 production，避免使用开发环境的隐式代理配置\n' >&2
  exit 1
fi
if [[ -z "${JWT_SECRET:-}" || -z "${APP_SECRET_KEY:-}" ]]; then
  printf '错误: JWT_SECRET 和 APP_SECRET_KEY 不能为空\n' >&2
  exit 1
fi
if [[ ! "${PORT:-}" =~ ^[0-9]+$ ]]; then
  printf '错误: PORT 必须是数字\n' >&2
  exit 1
fi

cd "$TARGET_DIR"
export STRATEGY_RUNNER_BIN="$TARGET_DIR/bin/strategy-runner"

printf 'TradingBot 即将启动: http://127.0.0.1:%s\n' "$PORT"
printf '首次体验请不要添加 live 交易所账户；按 Ctrl+C 停止服务。\n'
exec "$TARGET_DIR/bin/server"
