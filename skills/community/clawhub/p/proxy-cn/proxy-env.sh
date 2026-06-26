#!/usr/bin/env bash
# 在当前 shell 会话中直接导出代理环境变量（不经过域名检测）。
# 平台：macOS、Linux、WSL、Git Bash。Windows PowerShell 请用 proxy-env.ps1（点源）。
# 用法：source "$(dirname "$0")/proxy-env.sh"
# 或与 SKILL 中路径一致：source /path/to/proxy-cn/proxy-env.sh

PROXY_SOCKS_HOST="${PROXY_SOCKS_HOST:-127.0.0.1:10808}"
PROXY_HTTP_HOST="${PROXY_HTTP_HOST:-127.0.0.1:10809}"

export http_proxy="http://${PROXY_HTTP_HOST}"
export https_proxy="http://${PROXY_HTTP_HOST}"
export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$https_proxy"
export ALL_PROXY="socks5://${PROXY_SOCKS_HOST}"
export all_proxy="$ALL_PROXY"
export no_proxy="localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16"
export NO_PROXY="$no_proxy"

echo "[proxy-cn] 已在当前 shell 启用代理（HTTP ${PROXY_HTTP_HOST}，SOCKS5 ${PROXY_SOCKS_HOST}）" >&2
