#!/bin/bash
# TeslaMate 本地安装脚本

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[install]${NC} $1"
}

ok() {
    echo -e "${GREEN}[install] ✓${NC} $1"
}

error() {
    echo -e "${RED}[install] ✗${NC} $1" >&2
}

die() {
    error "$1"
    exit 1
}

# 检查Docker环境
check_docker() {
    log "检查Docker环境..."
    
    if ! command -v docker &> /dev/null; then
        log "Docker未安装，开始自动安装..."
        install_docker
        return
    fi
    
    # 多重方式检测 compose 是否可用 — 兼容 SSH 非交互模式 (docker compose version 行为可能不可靠)
    _has_compose=0
    if command -v docker-compose &> /dev/null; then _has_compose=1; fi
    if docker compose version &> /dev/null; then _has_compose=1; fi
    if [ -x /usr/libexec/docker/cli-plugins/docker-compose ]; then _has_compose=1; fi
    if [ -x /usr/local/lib/docker/cli-plugins/docker-compose ]; then _has_compose=1; fi
    if [ $_has_compose -eq 0 ]; then
        log "Docker Compose未安装，开始自动安装..."
        install_docker
        return
    fi
    
    # 检查Docker服务状态
    if ! sudo docker info &> /dev/null; then
        log "Docker服务未运行，尝试启动服务..."
        sudo systemctl start docker 2>/dev/null || sudo service docker start 2>/dev/null

        # 再次检查
        if ! sudo docker info &> /dev/null; then
            die "Docker服务启动失败，请手动检查Docker服务状态"
        fi
    fi

    # 不管 Docker 是否预装，都配置 mirror + 网络优化（对腾讯云内网机器尤其重要）
    configure_docker_network

    ok "Docker环境检查通过"
}

# 配置 Docker mirror + 网络优化（独立函数，可在 check_docker 和 install_docker 中复用）
configure_docker_network() {
    sudo mkdir -p /etc/docker
    local _mirror_url; _mirror_url=$(detect_mirror_url)
    if [ -n "$_mirror_url" ]; then
        log "配置 Docker mirror: $_mirror_url"
        sudo tee /etc/docker/daemon.json > /dev/null << DOCKER_CONFIG
{
  "ipv6": false,
  "ip6tables": false,
  "registry-mirrors": ["${_mirror_url}"]
}
DOCKER_CONFIG
    else
        sudo tee /etc/docker/daemon.json > /dev/null << 'DOCKER_CONFIG'
{
  "ipv6": false,
  "ip6tables": false
}
DOCKER_CONFIG
    fi
    # 强制 IPv4 优先
    if ! grep -q "^precedence ::ffff:0:0/96 100" /etc/gai.conf 2>/dev/null; then
        echo "precedence ::ffff:0:0/96 100" | sudo tee -a /etc/gai.conf >/dev/null
    fi
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ok "Docker 网络配置完成"
}

# 安装Docker环境（仅限Ubuntu/Debian）
install_docker() {
    log "安装Docker环境..."

    # 修复dpkg问题
    sudo dpkg --configure -a 2>/dev/null || true

    # 更新包列表
    sudo apt-get update -y

    # 安装Docker和Docker Compose — 兼容不同 Ubuntu/Debian 版本
    # docker-compose-plugin: Debian 12 / Ubuntu 24.04
    # docker-compose-v2:     Ubuntu 26.04+
    if ! sudo apt-get install -y docker.io docker-compose-plugin 2>/dev/null && \
       ! sudo apt-get install -y docker-compose-v2 2>/dev/null; then
        sudo apt-get install -y docker-compose-plugin
    fi

    configure_docker_network

    sudo systemctl enable docker

    ok "Docker环境安装完成"
}

# 检测能解析的 mirror URL，fallback 到空（不配）
# 优先腾讯云内网（云上机器），其次公网 mirror（家用网络）
detect_mirror_url() {
    for url in "https://mirror.ccs.tencentyun.com" "https://docker.1ms.run" "https://docker.m.daocloud.io"; do
        host=$(echo "$url" | sed 's|https://||')
        if getent hosts "$host" >/dev/null 2>&1; then
            echo "$url"
            return
        fi
    done
    # 全部解析不到 — 不配 mirror，让 docker 走默认 docker.io
    echo ""
}

# 从 GitHub 下载 Docker 镜像（docker pull 失败时的回退方案）
# GitHub: https://github.com/martinbj2008/docker_images
download_github_image() {
    local IMAGE="$1"
    local repo="${1%%:*}"
    local tag="${1##*:}"
    local fn="${repo}-${tag}.tar.gz"
    local raw="https://raw.githubusercontent.com/martinbj2008/docker_images/main"
    local tmpdir; tmpdir="$(mktemp -d)"

    log "从 GitHub 下载 $IMAGE ..."

    curl -sSfL -o "${tmpdir}/sha256sums.txt" "$raw/sha256sums.txt" || die "sha256sums.txt 下载失败"
    local files; files=$(grep "./$repo/$tag/" "${tmpdir}/sha256sums.txt" | awk '{print $2}' | sed 's|^./||')
    [ -z "$files" ] && die "sha256sums.txt 中未找到 $IMAGE 对应的文件"

    echo "$files" | while read -r f; do
        local out="${tmpdir}/${f//\//_}"
        curl -sSfL -o "$out" "$raw/$f" || die "$f 下载失败"
        (cd "$tmpdir" && sha256sum -c --quiet <(grep "$f" sha256sums.txt 2>/dev/null)) || die "$f SHA256 校验失败"
    done

    for f in $(echo "$files" | sort); do
        cat "${tmpdir}/${f//\//_}"
    done | gunzip | docker load

    rm -rf "$tmpdir"
    ok "$IMAGE 加载成功"
}

# 安装TeslaMate服务
install_teslamate() {
    local image_github="${1:-false}"
    log "安装TeslaMate服务..."
    
    # 检查docker-compose.yml文件是否存在
    if [ ! -f "docker-compose.yml" ]; then
        die "缺少docker-compose.yml文件"
    fi
    
    # 固定密码配置
    TM_ENCRYPTION_KEY="default_encryption_key_123456789012"
    TM_DB_PASS="teslamate123"
    
    # 创建import目录
    mkdir -p import
    
    # 创建.env文件
    tee .env > /dev/null << ENV_CONFIG
TM_ENCRYPTION_KEY=${TM_ENCRYPTION_KEY}
TM_DB_PASS=${TM_DB_PASS}
ENV_CONFIG

    # 设置权限
    chmod 600 .env
    
    # 拉取镜像
    for img in "eclipse-mosquitto:2" "postgres:17" "teslamate/teslamate:latest" "teslamate/grafana:latest"; do
        if [ "$image_github" = "true" ]; then
            log "拉取 $img (GitHub直下)..."
            download_github_image "$img"
        else
            log "拉取 $img (docker pull)..."
            if sudo docker pull "$img" 2>/dev/null; then
                ok "$img 拉取成功"
            else
                warn "docker pull $img 失败，尝试从 GitHub 下载..."
                download_github_image "$img"
            fi
        fi
    done
    
    # 启动服务
    sudo docker compose down 2>/dev/null || true
    sudo docker compose up -d
    
    # 等待服务启动
    sleep 15
    
    # 检查服务状态
    sudo docker compose ps
    
    ok "TeslaMate安装完成"
}

# 显示安装结果
show_result() {
    echo ""
    echo "=========================================="
    echo "✅ TeslaMate 安装完成"
    echo "=========================================="
    echo "访问地址:"
    echo "  TeslaMate: http://localhost:4000"
    echo "  Grafana:   http://localhost:3000"
    echo ""
    echo "Grafana 默认账号: admin/admin"
    echo "首次访问可能需要 1-2 分钟数据库初始化"
    echo "=========================================="
}

# 主函数
main() {
    local install_docker_env=false
    local image_github=false

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --install-docker)
                install_docker_env=true
                shift
                ;;
            --github-image)
                image_github=true
                shift
                ;;
            -h|--help)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --install-docker    强制重新安装Docker环境（仅限Ubuntu/Debian）"
                echo "  --github-image      从 GitHub 直接下载镜像（跳过 docker pull，适用于无镜像加速器环境）"
                echo "  -h, --help         显示帮助信息"
                echo ""
                echo "说明:"
                echo "  无参数调用时，自动检测Docker并部署，镜像从 docker pull 拉取（失败时回退 GitHub）"
                echo "  --github-image 强制走 GitHub 下载，适合 mirror 不可用的网络"
                exit 0
                ;;
            *)
                error "未知参数: $1"
                exit 1
                ;;
        esac
    done

    log "开始TeslaMate本地安装"

    if [ "$install_docker_env" = "true" ]; then
        install_docker
    else
        check_docker
    fi

    install_teslamate "$image_github"
    show_result

    ok "安装流程全部完成"
}

main "$@"
