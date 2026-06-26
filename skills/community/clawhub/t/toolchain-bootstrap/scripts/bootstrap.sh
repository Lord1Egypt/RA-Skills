#!/bin/bash
#===========================================================
# OpenClaw Toolchain Bootstrapper
#===========================================================
set -e

TOOLCHAIN="/workspace/toolchain"
REPO="TurinFohlen/openclaw-toolchain"
RELEASE_URL="https://github.com/$REPO/releases/download/v2.0/toolchain_v2.tar.gz"

# Color output
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[ OK ]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()   { echo -e "${RED}[ ERR]${NC} $1"; }

#-----------------------------------------------------------
do_setup() {
  info "开始工具链引导安装..."

  # 如果已有完整工具链，跳过下载
  if [ -x "$TOOLCHAIN/go/bin/go" ] && [ -x "$TOOLCHAIN/erlang/bin/erl" ]; then
    ok "工具链已存在，跳过下载"
  else
    info "下载工具链包 (~590MB)..."
    curl -L --progress-bar "$RELEASE_URL" -o /tmp/toolchain_v2.tar.gz
    info "解压到 /workspace/ ..."
    tar -xzf /tmp/toolchain_v2.tar.gz -C /workspace/
    rm -f /tmp/toolchain_v2.tar.gz
  fi

  # 配置环境变量
  info "配置环境变量..."
  TOOLCHAIN="$TOOLCHAIN" bash "$(dirname "$0")/setup-env.sh"

  do_verify
  ok "工具链安装完成！"
  echo ""
  echo "加载环境变量: source ~/.bashrc"
}

#-----------------------------------------------------------
do_verify() {
  info "验证已安装工具..."
  local failed=0

  check_tool() {
    local path="$1"; local name="$2"; local cmd="$3"
    if [ -x "$path" ]; then
      local ver=$(eval "$cmd" 2>/dev/null | head -1 | tr -d '\n' || echo "OK")
      ok "$name: $ver"
    else
      err "$name: 未安装"
      failed=$((failed+1))
    fi
  }

  check_tool "$TOOLCHAIN/go/bin/go"                    "Go"      "$TOOLCHAIN/go/bin/go version"
  check_tool "$TOOLCHAIN/jdk-21.0.10+7/bin/java"    "Java"    "$TOOLCHAIN/jdk-21.0.10+7/bin/java -version 2>&1 | head -1"
  check_tool "$TOOLCHAIN/apache-maven-3.9.6/bin/mvn"  "Maven"   "$TOOLCHAIN/apache-maven-3.9.6/bin/mvn -version 2>&1 | head -1"
  check_tool "$TOOLCHAIN/erlang/bin/erl"              "Erlang"  "$TOOLCHAIN/erlang/bin/erl -eval 'erlang:display(erlang:system_info(otp_release)),halt().' -noshell 2>/dev/null"
  check_tool "$TOOLCHAIN/elixir/bin/elixir"           "Elixir"  "$TOOLCHAIN/elixir/bin/elixir --version 2>&1 | head -1"
  RUST_BIN=$(ls $TOOLCHAIN/rust/rustup/toolchains/*/bin/rustc 2>/dev/null | head -1)
  if [ -n "$RUST_BIN" ] && [ -x "$RUST_BIN" ]; then
    ok "Rust:   $($RUST_BIN --version 2>&1 | awk '{print $2}')"
  else
    err "Rust:   未安装"
    failed=$((failed+1))
  fi
  check_tool "$TOOLCHAIN/ruby/bin/ruby"               "Ruby"    "$TOOLCHAIN/ruby/bin/ruby --version 2>&1 | head -1"
  check_tool "$TOOLCHAIN/lua/bin/lua"                 "Lua"     "$TOOLCHAIN/lua/bin/lua -v 2>&1 | head -1"

  command -v node   &>/dev/null && ok "Node.js: $(node --version)"       || warn "Node.js: 未安装"
  command -v python3 &>/dev/null && ok "Python: $(python3 --version 2>&1 | awk '{print $2}')" || warn "Python: 未安装"
  command -v gcc     &>/dev/null && ok "GCC:     $(gcc --version 2>&1 | head -1 | awk '{print $3}')" || warn "GCC: 未安装"

  echo ""
  if [ $failed -eq 0 ]; then
    ok "全部工具验证通过！"
  else
    warn "$failed 个工具缺失"
  fi
}

#-----------------------------------------------------------
do_list() {
  echo "=== OpenClaw 工具链 ==="
  echo ""
  [ -x "$TOOLCHAIN/go/bin/go" ]         && echo "Go       $($TOOLCHAIN/go/bin/go version 2>/dev/null | awk '{print $3}')"
  [ -x "$TOOLCHAIN/jdk-21.0.10+7/bin/java" ] && echo "Java     $($TOOLCHAIN/jdk-21.0.10+7/bin/java -version 2>&1 | head -1 | awk '{print $3}')"
  [ -x "$TOOLCHAIN/erlang/bin/erl" ]    && echo "Erlang   OTP $($TOOLCHAIN/erlang/bin/erl -eval 'erlang:display(erlang:system_info(otp_release)),halt().' -noshell 2>/dev/null)"
  [ -x "$TOOLCHAIN/elixir/bin/elixir" ]  && echo "Elixir   $($TOOLCHAIN/elixir/bin/elixir --version 2>&1 | head -1 | awk '{print $2}')"
  RUST_BIN=$(ls $TOOLCHAIN/rust/rustup/toolchains/*/bin/rustc 2>/dev/null | head -1)
  [ -n "$RUST_BIN" ] && [ -x "$RUST_BIN" ] && echo "Rust     $($RUST_BIN --version 2>&1 | awk '{print $2}')"
  [ -x "$TOOLCHAIN/ruby/bin/ruby" ]      && echo "Ruby     $($TOOLCHAIN/ruby/bin/ruby --version 2>&1 | awk '{print $2}')"
  [ -x "$TOOLCHAIN/lua/bin/lua" ]        && echo "Lua      $($TOOLCHAIN/lua/bin/lua -v 2>&1 | awk '{print $2}')"
  [ -x "$TOOLCHAIN/apache-maven-3.9.6/bin/mvn" ] && echo "Maven    $($TOOLCHAIN/apache-maven-3.9.6/bin/mvn -version 2>&1 | head -1 | awk '{print $3}')"
  echo ""
  echo "系统工具:"
  command -v node   &>/dev/null && echo "Node.js  $(node --version)"    || echo "Node.js  -"
  command -v python3 &>/dev/null && echo "Python   $(python3 --version 2>&1 | awk '{print $2}')" || echo "Python   -"
  command -v gcc     &>/dev/null && echo "GCC      $(gcc --version 2>&1 | head -1 | awk '{print $3}')" || echo "GCC      -"
}

#-----------------------------------------------------------
# Main
ACTION="${1:-setup}"
case "$ACTION" in
  setup|install)  do_setup ;;
  verify|check)   do_verify ;;
  list|ls)       do_list ;;
  *)              echo "用法: $0 [setup|verify|list]"; exit 1 ;;
esac
