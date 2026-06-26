#!/bin/bash
# ssh-key-setup.sh — SSH 密钥管理工具
# 用法: bash ssh-key-setup.sh <command> [args]
#
# 命令:
#   gen [name]           — 生成密钥对（默认 id_ed25519）
#   pub [name]           — 查看公钥
#   deploy <host> [user] — 部署公钥到远程主机（需要密码）
#   test <host> [user]   — 测试免密登录
#   list                 — 列出已有密钥
#   info <host>          — 查看远程主机基本信息

set -e

SSH_DIR="$HOME/.ssh"
DEFAULT_KEY="id_ed25519"
KEY_TYPE="ed25519"

cmd_list() {
    echo "🔑 已有的 SSH 密钥:"
    ls -la "$SSH_DIR"/*.pub 2>/dev/null || echo "  (无)"
}

cmd_gen() {
    local name="${1:-$DEFAULT_KEY}"
    local keyfile="$SSH_DIR/$name"
    if [ -f "$keyfile" ]; then
        echo "⚠️  密钥 $name 已存在: $keyfile"
        echo "   公钥:"
        cat "${keyfile}.pub"
        return 0
    fi
    mkdir -p "$SSH_DIR" && chmod 700 "$SSH_DIR"
    ssh-keygen -t "$KEY_TYPE" -f "$keyfile" -N "" -C "openclaw@$(hostname)" 2>&1
    echo "✅ 密钥已生成: $keyfile"
    echo "   公钥:"
    cat "${keyfile}.pub"
}

cmd_pub() {
    local name="${1:-$DEFAULT_KEY}"
    local keyfile="$SSH_DIR/${name}.pub"
    if [ -f "$keyfile" ]; then
        cat "$keyfile"
    else
        echo "❌ 公钥不存在: $keyfile"
        return 1
    fi
}

cmd_deploy() {
    local host="$1"
    local user="${2:-root}"
    local keyfile="$SSH_DIR/$DEFAULT_KEY.pub"
    
    if [ -z "$host" ]; then
        echo "❌ 用法: deploy <host> [user]"
        return 1
    fi
    
    if [ ! -f "$SSH_DIR/$DEFAULT_KEY" ]; then
        echo "❌ 私钥不存在，请先运行 gen"
        return 1
    fi
    
    if ! command -v sshpass &>/dev/null; then
        echo "正在安装 sshpass..."
        if command -v apt-get &>/dev/null; then
            DEBIAN_FRONTEND=noninteractive apt-get install -y -qq sshpass 2>&1
        elif command -v yum &>/dev/null; then
            yum install -y -q sshpass 2>&1
        fi
    fi
    
    echo "📤 部署公钥到 ${user}@${host} ..."
    sshpass -p "$SSHPASS" ssh-copy-id -o StrictHostKeyChecking=no "${user}@${host}" 2>&1
    echo "✅ 公钥已部署"
}

cmd_test() {
    local host="$1"
    local user="${2:-root}"
    
    if [ -z "$host" ]; then
        echo "❌ 用法: test <host> [user]"
        return 1
    fi
    
    echo "🔗 测试免密登录 ${user}@${host} ..."
    if ssh -o ConnectTimeout=5 -o BatchMode=yes "${user}@${host}" "echo '✅ 免密登录成功' && hostname" 2>&1; then
        echo "✅ 连接正常"
    else
        echo "❌ 免密登录失败，请检查公钥是否已部署"
        return 1
    fi
}

cmd_info() {
    local host="$1"
    local user="${2:-root}"
    
    if [ -z "$host" ]; then
        echo "❌ 用法: info <host> [user]"
        return 1
    fi
    
    echo "📊 远程主机信息: ${user}@${host}"
    ssh -o ConnectTimeout=5 "${user}@${host}" bash -c '
        echo "  主机名: $(hostname)"
        echo "  系统: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d \"\")"
        echo "  内核: $(uname -r)"
        echo "  架构: $(uname -m)"
        echo "  内存: $(free -h | awk "/^Mem:/{print \$2\" total, \"\$7\" available\"}")"
        echo "  磁盘: $(df -h / | awk "NR==2{print \$2\" total, \"\$4\" free (\"\$5\" used)\"}")"
        echo "  负载: $(uptime | awk -F: "{print \$NF}")"
    ' 2>&1
}

# Main
case "${1:-help}" in
    gen)     shift; cmd_gen "$@" ;;
    pub)     shift; cmd_pub "$@" ;;
    deploy)  shift; cmd_deploy "$@" ;;
    test)    shift; cmd_test "$@" ;;
    list)    cmd_list ;;
    info)    shift; cmd_info "$@" ;;
    help|*)
        echo "🔑 SSH 密钥管理工具"
        echo ""
        echo "用法: bash ssh-key-setup.sh <command> [args]"
        echo ""
        echo "命令:"
        echo "  gen [name]           生成密钥对"
        echo "  pub [name]           查看公钥"
        echo "  deploy <host> [user] 部署公钥到远程主机（需要 SSHPASS 环境变量）"
        echo "  test <host> [user]   测试免密登录"
        echo "  list                 列出已有密钥"
        echo "  info <host> [user]   查看远程主机信息"
        ;;
esac
