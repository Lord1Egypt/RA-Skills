#!/usr/bin/env bash
# 沙雕动画小助手（Web 社区版）安装 / 启动 / 自检
# 用法：bash setup_app.sh [doctor|install|start|start-tts|path]
set -euo pipefail

REPO="https://github.com/wormsun/FunnyAnimationAssitant.git"
APP_DIR="${FAA_HOME:-$HOME/FunnyAnimationAssitant}"
CMD="${1:-help}"

info()  { printf '\033[36m[信息]\033[0m %s\n' "$*"; }
ok()    { printf '\033[32m[通过]\033[0m %s\n' "$*"; }
warn()  { printf '\033[33m[注意]\033[0m %s\n' "$*"; }
die()   { printf '\033[31m[失败]\033[0m %s\n' "$*" >&2; exit 1; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "缺少 $1，请先安装。"
}

doctor() {
  info "检查运行环境"
  need_cmd node
  need_cmd npm
  need_cmd git

  local node_major
  node_major="$(node -p 'process.versions.node.split(".")[0]')"
  if [ "$node_major" -lt 18 ]; then
    die "Node.js 需要 18+，当前 $(node -v)"
  fi
  ok "node $(node -v)"

  local npm_major
  npm_major="$(npm -v | cut -d. -f1)"
  if [ "$npm_major" -lt 9 ]; then
    warn "npm 建议 9+，当前 $(npm -v)"
  else
    ok "npm $(npm -v)"
  fi

  if command -v ffmpeg >/dev/null 2>&1; then
    ok "ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
  else
    warn "未装 ffmpeg（只影响 05-出片 的收尾）"
  fi

  if [ -d "$APP_DIR/.git" ]; then
    ok "app 已安装：$APP_DIR"
    info "commit: $(git -C "$APP_DIR" rev-parse --short HEAD)"
  else
    warn "app 未安装，运行：bash setup_app.sh install"
  fi

  if lsof -nP -iTCP:5173 -sTCP:LISTEN >/dev/null 2>&1; then
    warn "5173 端口已被占用（可能 app 已在运行）"
  else
    ok "5173 端口可用"
  fi
}

install_app() {
  need_cmd node
  need_cmd npm
  need_cmd git

  if [ -d "$APP_DIR/.git" ]; then
    info "已存在仓库，执行 npm install：$APP_DIR"
  else
    info "clone 到 $APP_DIR"
    mkdir -p "$(dirname "$APP_DIR")"
    git clone --depth 1 "$REPO" "$APP_DIR"
  fi

  cd "$APP_DIR"
  npm install

  # 宿主 app 自己的运行时配置由它自己管：本 skill 的脚本不读、不写任何配置文件
  ok "安装完成：$APP_DIR"
  info "启动：bash 00-工作台/setup_app.sh start"
}

start_app() {
  [ -d "$APP_DIR" ] || die "尚未安装，先运行：bash setup_app.sh install"
  cd "$APP_DIR"
  exec npm run dev
}

start_tts() {
  [ -d "$APP_DIR" ] || die "尚未安装，先运行：bash setup_app.sh install"
  cd "$APP_DIR"
  if [ ! -d examples/tts-provider ]; then
    warn "这个版本的 app 没有 examples/tts-provider，TTS Provider 可能启动失败（见 app 自己的 README）"
  fi
  exec npm run dev:with-tts
}

case "$CMD" in
  doctor)    doctor ;;
  install)   install_app ;;
  start)     start_app ;;
  start-tts) start_tts ;;
  path)      echo "$APP_DIR" ;;
  *)
    cat <<'EOF'
用法：bash setup_app.sh <命令>

  doctor     检查 node / npm / git / ffmpeg / 端口
  install    clone 仓库并 npm install
  start      启动主应用
  start-tts  同时启动本地 TTS Provider
  path       打印安装路径
EOF
    ;;
esac
