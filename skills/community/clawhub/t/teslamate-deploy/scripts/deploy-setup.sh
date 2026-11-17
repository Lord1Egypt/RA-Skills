#!/bin/bash
# TeslaMate 远程部署脚本

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[deploy]${NC} $1"
}

ok() {
    echo -e "${GREEN}[deploy] ✓${NC} $1"
}

error() {
    echo -e "${RED}[deploy] ✗${NC} $1" >&2
}

die() {
    error "$1"
    exit 1
}

# ---- SSH 连接 ----
# 支持两种认证方式:
#   SSH key (默认) — 用 ControlMaster 复用连接，避免 MaxSessions 限制
#   SSH 密码     — 设 SSH_PASS 环境变量，走 sshpass（密码一次性输入，存于会话）
#
# 首次连接处理：两种模式都用 -o StrictHostKeyChecking=no 自动跳过 yes/no 确认，
# 配合 UserKnownHostsFile=/dev/null + LogLevel=ERROR 彻底避免交互式提示干扰 sshpass。
#
# 路径长度坑：macOS 的 Unix domain socket 路径上限 ~104 字符（含 null 终止符），
# 实际比这短就会被拒。%C 会产出 30+ 字符的 hash，HOME/.cache/... 这种路径会爆。
# 解决：用 /tmp/tm-ssh/ + 自算 8 字符 hash，整条 < 30 字符，留足 buffer。
TM_SSH_DIR="/tmp/tm-ssh"
mkdir -p "$TM_SSH_DIR"
_short_hash() {
    # shasum 不可用时 fallback 到 cksum / od
    if command -v shasum >/dev/null 2>&1; then
        echo -n "$1" | shasum -a 256 | cut -c1-8
    else
        echo -n "$1" | cksum | awk '{print $1}' | head -c 8
    fi
}
# 首次连接自动接受 host key（sshpass 模式下必须，否则 yes/no 提示会吞掉密码输入）
HOST_KEY_OPTS=(
    -o StrictHostKeyChecking=no
    -o UserKnownHostsFile=/dev/null
    -o LogLevel=ERROR
)
SSH_OPTS=(
    -o StrictHostKeyChecking=no
    -o ControlMaster=auto
    -o ControlPersist=600
)
# 实际的 ControlPath 在 _ssh_remote / _scp_local 里按 target 单独算
SSH_TARGET=""

_ssh_remote() {
    local target="$1"; shift
    SSH_TARGET="$target"

    if [ -n "${SSH_PASS:-}" ]; then
        # 密码模式：不用 ControlMaster，直接用 sshpass
        # -o StrictHostKeyChecking=no / UserKnownHostsFile / LogLevel 保证首次连接无交互
        sshpass -p "$SSH_PASS" ssh "${HOST_KEY_OPTS[@]}" "$target" "$@"
    else
        # 密钥模式：ControlMaster 复用
        local cp="$TM_SSH_DIR/$(_short_hash "$target")"
        local opts=("${SSH_OPTS[@]}" "-o" "ControlPath=$cp")
        if ! ssh -O check "${opts[@]}" "$target" 2>/dev/null; then
            ssh -fN "${opts[@]}" "$target" || die "无法建立到 $target 的 SSH 连接"
        fi
        ssh "${opts[@]}" "$target" "$@"
    fi
}

_scp_local() {
    local src="$1" dst="$2"
    if [ -n "${SSH_PASS:-}" ] && [ -n "$SSH_TARGET" ]; then
        sshpass -p "$SSH_PASS" scp "${HOST_KEY_OPTS[@]}" "$src" "$dst"
    elif [ -n "$SSH_TARGET" ]; then
        local cp="$TM_SSH_DIR/$(_short_hash "$SSH_TARGET")"
        scp "${SSH_OPTS[@]}" -o "ControlPath=$cp" "$src" "$dst"
    else
        scp "${SSH_OPTS[@]}" "$src" "$dst"
    fi
}

_cleanup_ssh_master() {
    # 密码模式没有 master connection 需要清理
    [ -n "${SSH_PASS:-}" ] && return 0
    if [ -n "$SSH_TARGET" ]; then
        local cp="$TM_SSH_DIR/$(_short_hash "$SSH_TARGET")"
        local opts=("${SSH_OPTS[@]}" "-o" "ControlPath=$cp")
        ssh -O exit "${opts[@]}" "$SSH_TARGET" 2>/dev/null || true
        rm -f "$cp" "$cp.*" 2>/dev/null
    fi
}
trap _cleanup_ssh_master EXIT

# 检查参数
if [ $# -eq 0 ]; then
    # 无参数，执行本地安装
    log "检测到无参数，执行本地安装..."
    
    # 检查本地安装脚本是否存在
    if [ ! -f "install-teslamate.sh" ]; then
        die "缺少本地安装脚本 install-teslamate.sh"
    fi
    
    # 执行本地安装脚本
    chmod +x install-teslamate.sh
    ./install-teslamate.sh
    exit $?
fi

if [ $# -ne 1 ]; then
    echo "用法: $0 [服务器IP]"
    echo ""
    echo "选项:"
    echo "  无参数                              执行本地安装"
    echo "  <服务器IP>                          执行远程部署 (默认用户 ubuntu)"
    echo "  REMOTE_USER=root \$0 <服务器IP>      指定远端用户 (如 root 配免密登录)"
    echo ""
    echo "示例:"
    echo "  \$0                            # 本地安装"
    echo "  \$0 192.0.2.1                  # 远程 ubuntu@192.0.2.1"
    echo "  REMOTE_USER=root \$0 192.0.2.1 # 远程 root@192.0.2.1 (如 Armbian 盒子)"
    exit 1
fi

SERVER_IP="$1"
# 远端用户: 默认 ubuntu；可由调用方通过环境变量 REMOTE_USER 覆盖（如 root 用于 Armbian/已配免密的盒子）
USER="${REMOTE_USER:-ubuntu}"
# REMOTE_DIR: 远端用户的 home 下的 teslamate 目录；root 走 /root，其余走 /home/$USER
case "$USER" in
    root) REMOTE_DIR="/root/teslamate" ;;
    *)    REMOTE_DIR="/home/$USER/teslamate" ;;
esac

log "开始 TeslaMate 远程部署到服务器: $SERVER_IP"

# 固定密码配置
TM_ENCRYPTION_KEY="default_encryption_key_123456789012"
TM_DB_PASS="teslamate123"

setup_server() {
    log "设置服务器环境..."

    # 用 ControlMaster 复用同一条连接，避免触发 MaxSessions
    _ssh_remote "$USER@$SERVER_IP" << 'EOF'
        set -e

        # 修复dpkg问题
        sudo dpkg --configure -a 2>/dev/null || true

        # 强制 IPv4 优先（解决 IPv6 黑洞路由问题，比如 docker.io 的 AAAA 记录到 Facebook 段）
        if ! grep -q "^precedence ::ffff:0:0/96 100" /etc/gai.conf 2>/dev/null; then
            echo "precedence ::ffff:0:0/96 100" | sudo tee -a /etc/gai.conf >/dev/null
        fi

        # 先检查 docker compose 是否已可用 —— 如果可用则跳过整个 apt install 阶段（节省 5+ 分钟）
        _has_compose=0
        if command -v docker-compose &> /dev/null; then _has_compose=1; fi
        if docker compose version &> /dev/null 2>&1; then _has_compose=1; fi
        if [ -x /usr/libexec/docker/cli-plugins/docker-compose ]; then _has_compose=1; fi
        if [ -x /usr/local/lib/docker/cli-plugins/docker-compose ]; then _has_compose=1; fi

        if [ $_has_compose -eq 0 ]; then
            echo "Docker Compose 未安装，开始安装 Docker 环境..."

            # 更新包列表
            sudo apt-get update -y

            # 直接安装Docker和Docker Compose — 兼容不同 Ubuntu/Debian 版本
            # docker-compose-plugin: Debian 12 / Ubuntu 24.04
            # docker-compose-v2:     Ubuntu 26.04+
            if ! sudo apt-get install -y docker.io docker-compose-plugin 2>/dev/null && \
               ! sudo apt-get install -y docker-compose-v2 2>/dev/null; then
                sudo apt-get install -y docker-compose-plugin
            fi
        else
            echo "Docker Compose 已安装，跳过 apt install"
        fi

        # 验证Docker Compose是否可用
        if ! docker compose version >/dev/null 2>&1; then
            echo "错误：Docker Compose安装失败，请检查系统环境"
            exit 1
        fi

        # 配置镜像加速器 — 只配能解析的 mirror
        # 优先腾讯云内网（云上机器），其次公网 mirror（家用网络）；全部解析不到则不配
        _mirror_url=""
        for url in "https://mirror.ccs.tencentyun.com" "https://docker.1ms.run" "https://docker.m.daocloud.io"; do
            _host=$(echo "$url" | sed 's|https://||')
            if getent hosts "$_host" >/dev/null 2>&1; then
                _mirror_url="$url"
                break
            fi
        done

        sudo mkdir -p /etc/docker
        if [ -n "$_mirror_url" ]; then
            echo "使用 Docker mirror: $_mirror_url"
            sudo tee /etc/docker/daemon.json > /dev/null << DOCKER_CONFIG
{
  "ipv6": false,
  "ip6tables": false,
  "registry-mirrors": ["${_mirror_url}"]
}
DOCKER_CONFIG
        else
            echo "未找到可用的 Docker mirror，跳过配置"
            sudo tee /etc/docker/daemon.json > /dev/null << 'DOCKER_CONFIG'
{
  "ipv6": false,
  "ip6tables": false
}
DOCKER_CONFIG
        fi

        sudo systemctl daemon-reload
        sudo systemctl enable docker
        sudo systemctl restart docker

        echo "服务器环境设置完成"
EOF

    ok "服务器环境设置完成"
}

deploy_teslamate() {
    log "部署TeslaMate服务..."

    # 检查本地脚本文件是否存在
    if [ ! -f "docker-compose.yml" ] || [ ! -f "install-teslamate.sh" ]; then
        die "缺少必要文件 (docker-compose.yml / install-teslamate.sh)"
    fi

    # 一次SSH连接里完成：建目录 + scp + chmod
    # 关键：把 docker-compose.yml 和 install-teslamate.sh 通过 base64 走 stdin 传过去，
    # 彻底避免多次 scp 打开新 SSH 会话。
    log "创建远程目录并传输文件（单连接）..."

    COMPOSE_B64="$(base64 < docker-compose.yml | tr -d '\n')"
    INSTALL_B64="$(base64 < install-teslamate.sh | tr -d '\n')"

    _ssh_remote "$USER@$SERVER_IP" <<EOF
        set -e
        mkdir -p $REMOTE_DIR $REMOTE_DIR/import
        # base64 解码写入
        echo '${COMPOSE_B64}'  | base64 -d > $REMOTE_DIR/docker-compose.yml
        echo '${INSTALL_B64}'  | base64 -d > $REMOTE_DIR/install-teslamate.sh
        chmod +x $REMOTE_DIR/install-teslamate.sh
        # 校验文件存在且非空
        test -s $REMOTE_DIR/docker-compose.yml
        test -s $REMOTE_DIR/install-teslamate.sh
        echo "files staged: \$(wc -c < $REMOTE_DIR/docker-compose.yml) bytes compose, \$(wc -c < $REMOTE_DIR/install-teslamate.sh) bytes install"
EOF

    # 在远程服务器上执行安装脚本（复用同一条 ControlMaster 连接）
    log "远程执行安装脚本..."
    _ssh_remote "$USER@$SERVER_IP" << EOF
        set -e
        cd $REMOTE_DIR
        sudo ./install-teslamate.sh --install-docker
EOF

    ok "TeslaMate部署成功"
}

show_result() {
    echo ""
    echo "=========================================="
    echo "✅ TeslaMate 远程部署完成"
    echo "=========================================="
    echo "访问地址:"
    echo "  TeslaMate: http://$SERVER_IP:4000"
    echo "  Grafana:   http://$SERVER_IP:3000"
    echo ""
    echo "Grafana 默认账号: admin/admin"
    echo "首次访问可能需要 1-2 分钟数据库初始化"
    echo "=========================================="
}

main() {
    log "开始TeslaMate一键部署"
    
    setup_server
    deploy_teslamate
    show_result
    
    ok "部署流程全部完成"
}

main "$@"
