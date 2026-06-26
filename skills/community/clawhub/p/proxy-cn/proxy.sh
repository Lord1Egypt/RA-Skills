#!/usr/bin/env bash
# 外网智能代理包装器：根据参数中是否出现常见境外域名，自动注入 http(s)_proxy 与 ALL_PROXY（SOCKS5）。
# 平台：macOS、Linux、WSL、Git Bash / MSYS2（需 Bash）。Windows 原生 PowerShell 请用同目录 proxy.ps1。
#
# 用法：
#   ./proxy.sh curl -sI https://api.github.com
#   PROXY_AUTO_FORCE=1 ./proxy.sh npm install
#
# 环境变量（可选）：
#   PROXY_AUTO_FORCE=1   强制走代理（忽略域名检测）
#   PROXY_SOCKS_HOST     默认 127.0.0.1:10808
#   PROXY_HTTP_HOST      默认 127.0.0.1:10809
#   PROXY_AUTO_NO_LOCAL  默认 1：设置 no_proxy，避免内网走代理

set -euo pipefail

PROXY_SOCKS_HOST="${PROXY_SOCKS_HOST:-127.0.0.1:10808}"
PROXY_HTTP_HOST="${PROXY_HTTP_HOST:-127.0.0.1:10809}"
PROXY_AUTO_NO_LOCAL="${PROXY_AUTO_NO_LOCAL:-1}"

_apply_proxy() {
  export http_proxy="http://${PROXY_HTTP_HOST}"
  export https_proxy="http://${PROXY_HTTP_HOST}"
  export HTTP_PROXY="$http_proxy"
  export HTTPS_PROXY="$https_proxy"
  export ALL_PROXY="socks5://${PROXY_SOCKS_HOST}"
  export all_proxy="$ALL_PROXY"
  if [[ "${PROXY_AUTO_NO_LOCAL}" == "1" ]]; then
    export no_proxy="localhost,127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,169.254.0.0/16"
    export NO_PROXY="$no_proxy"
  fi
  echo "[proxy-cn] 已启用 HTTP 代理 ${PROXY_HTTP_HOST}，SOCKS5 ${PROXY_SOCKS_HOST}" >&2
}

_proxy_match() {
  local a
  shopt -s nocasematch
  for a in "$@"; do
    case "$a" in
      *github.com*|*githubusercontent.com*|*raw.githubusercontent.com*|*ghcr.io*|*gist.github.com*)
        shopt -u nocasematch; return 0 ;;
      *google.com*|*googleapis.com*|*gstatic.com*|*googleusercontent.com*|*golang.org*)
        shopt -u nocasematch; return 0 ;;
      *openai.com*|*anthropic.com*|*claude.ai*|*cursor.com*|*huggingface.co*|*hf.co*)
        shopt -u nocasematch; return 0 ;;
      *npmjs.org*|*registry.npmjs.org*|*yarnpkg.com*|*pnpm.io*)
        shopt -u nocasematch; return 0 ;;
      *pypi.org*|*pythonhosted.org*|*files.pythonhosted.org*)
        shopt -u nocasematch; return 0 ;;
      *docker.io*|*docker.com*|*quay.io*|*registry.k8s.io*)
        shopt -u nocasematch; return 0 ;;
      *rust-lang.org*|*crates.io*)
        shopt -u nocasematch; return 0 ;;
      *kubernetes.io*|*helm.sh*)
        shopt -u nocasematch; return 0 ;;
      *cloudflare.com*|*fastly.com*)
        shopt -u nocasematch; return 0 ;;
      *stackoverflow.com*|*stackexchange.com*)
        shopt -u nocasematch; return 0 ;;
      *medium.com*|*wikipedia.org*)
        shopt -u nocasematch; return 0 ;;
    esac
  done
  shopt -u nocasematch
  return 1
}

if [[ $# -eq 0 ]]; then
  echo "用法: $0 <命令> [参数...]" >&2
  echo "  例: $0 curl -sI https://api.github.com" >&2
  echo "  例: PROXY_AUTO_FORCE=1 $0 npm install some-pkg" >&2
  exit 1
fi

if [[ "${PROXY_AUTO_FORCE:-}" == "1" ]] || _proxy_match "$@"; then
  _apply_proxy
else
  echo "[proxy-cn] 未匹配境外域名关键字，未设置代理（需要时设 PROXY_AUTO_FORCE=1）" >&2
fi

exec "$@"
