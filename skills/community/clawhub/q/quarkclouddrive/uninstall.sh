#!/usr/bin/env bash

set -euo pipefail


INSTALL_DIR="$HOME/.quarkclouddrive"


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

info()  { printf "${GREEN}[info]${NC}  %s\n" "$*"; }
warn()  { printf "${YELLOW}[warn]${NC}  %s\n" "$*"; }
error() { printf "${RED}[error]${NC} %s\n" "$*" >&2; }


OS_TYPE=""
detect_os() {
  info "Step 1: 检测运行环境..."

  case "$(uname -s)" in
    Linux*)   OS_TYPE="linux" ;;
    Darwin*)  OS_TYPE="mac" ;;
    CYGWIN*|MINGW*|MSYS*) OS_TYPE="windows" ;;
    *)
      error "不支持的操作系统: $(uname -s)"
      return 1
      ;;
  esac

  info "检测到操作系统: ${OS_TYPE}"
}


revoke_auth() {
  info "Step 2: 撤销本机授权 (logout)..."

  local cli_bin="$INSTALL_DIR/quarkclouddrive"

  if [ -x "$cli_bin" ]; then
    if "$cli_bin" logout >/dev/null 2>&1; then
      info "已撤销本机授权"
    else
      warn "撤销本机授权失败（可能未登录或网络异常），继续卸载"
    fi
  elif command -v quarkclouddrive &>/dev/null; then
    if quarkclouddrive logout >/dev/null 2>&1; then
      info "已撤销本机授权"
    else
      warn "撤销本机授权失败（可能未登录或网络异常），继续卸载"
    fi
  else
    info "未找到 quarkclouddrive 可执行文件，跳过授权撤销"
  fi

  return 0
}


remove_install_dir() {
  info "Step 3: 删除安装目录..."

  if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    info "已删除安装目录: $INSTALL_DIR"
  else
    warn "安装目录不存在，跳过: $INSTALL_DIR"
  fi
}


remove_global_command() {
  info "Step 4: 移除全局命令注册..."

  case "$OS_TYPE" in
    mac|linux)
      remove_symlink
      remove_path_from_shell_rc
      ;;
    windows)
      remove_path_from_shell_rc
      ;;
  esac
}

remove_symlink() {
  local symlink_path="/usr/local/bin/quarkclouddrive"

  if [ -L "$symlink_path" ]; then
    rm -f "$symlink_path"
    info "已删除符号链接: $symlink_path"
  elif [ -f "$symlink_path" ]; then
    rm -f "$symlink_path"
    info "已删除文件: $symlink_path"
  else
    info "符号链接不存在，跳过: $symlink_path"
  fi
}

remove_path_from_shell_rc() {
  local shell_rc_files=(
    "$HOME/.zshrc"
    "$HOME/.bashrc"
    "$HOME/.bash_profile"
    "$HOME/.profile"
    "$HOME/.config/fish/config.fish"
  )

  local found=false

  for rc_file in "${shell_rc_files[@]}"; do
    if [ ! -f "$rc_file" ]; then
      continue
    fi

    if grep -qF "$INSTALL_DIR" "$rc_file" 2>/dev/null; then
      local tmp_file
      tmp_file=$(mktemp)
      awk -v install_dir="$INSTALL_DIR" '
        /^# quarkclouddrive CLI$/ { skip_next = 1; next }
        skip_next == 1 { skip_next = 0; next }
        index($0, install_dir) { next }
        { print }
      ' "$rc_file" > "$tmp_file"
      mv "$tmp_file" "$rc_file"
      info "已从 $rc_file 中移除 quarkclouddrive PATH 配置"
      found=true
    fi
  done

  if [ "$found" = false ]; then
    info "未在 shell 配置文件中发现 quarkclouddrive PATH 配置"
  fi
}


verify_uninstall() {
  info "Step 5: 验证卸载结果..."

  local has_issue=false

  if [ -d "$INSTALL_DIR" ]; then
    error "安装目录仍然存在: $INSTALL_DIR"
    has_issue=true
  fi

  if command -v quarkclouddrive &>/dev/null; then
    warn "quarkclouddrive 命令仍然可用（可能需要重启终端才能完全生效）"
  else
    info "quarkclouddrive 命令已不可用"
  fi

  if [ "$has_issue" = true ]; then
    return 1
  fi
  return 0
}


print_result() {
  local success="$1"
  local divider
  divider=$(printf '%0.s─' {1..50})

  printf '\n%s\n' "$divider"

  if [ "$success" = "true" ]; then
    printf "${GREEN}${BOLD}✅ quarkclouddrive CLI 卸载完成${NC}\n\n"
    printf "  已清理以下内容:\n"
    printf "  • 安装目录  ${BOLD}%s${NC}\n" "$INSTALL_DIR"
    printf "  • 全局命令  ${BOLD}quarkclouddrive${NC}\n"
    printf "  • shell 配置中的 PATH 条目\n\n"
    printf "  请${BOLD}重新打开终端${NC}以确保环境变量完全生效\n"
  else
    printf "${RED}${BOLD}❌ quarkclouddrive CLI 卸载未完全成功${NC}\n\n"
    printf "  请检查以上错误信息并手动清理\n"
  fi

  printf '%s\n\n' "$divider"
}


main() {
  info "=== quarkclouddrive CLI 卸载脚本 ==="
  echo ""

  if ! detect_os; then
    print_result "false"
    exit 1
  fi

  revoke_auth

  if ! remove_install_dir; then
    print_result "false"
    exit 1
  fi

  if ! remove_global_command; then
    print_result "false"
    exit 1
  fi

  if ! verify_uninstall; then
    print_result "false"
    exit 1
  fi

  print_result "true"
}

main "$@"
