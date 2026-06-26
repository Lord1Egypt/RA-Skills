#!/bin/bash
#
# 树莓派摄像头服务卸载脚本
#

set -e

# 配置
SERVICE_NAME="camera-service"
WORKING_DIR="/opt/camera-service"
PYTHON_CMD="python3"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 root 权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用 sudo 运行此脚本"
        exit 1
    fi
}

# 停止并禁用服务
stop_service() {
    if systemctl list-unit-files | grep -q "^${SERVICE_NAME}.service"; then
        log_info "停止服务..."
        systemctl stop "$SERVICE_NAME" 2>/dev/null || true

        log_info "禁用服务开机自启..."
        systemctl disable "$SERVICE_NAME" 2>/dev/null || true

        log_info "删除服务文件..."
        rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
        systemctl daemon-reload
    else
        log_warn "服务未安装"
    fi
}

# 删除日志轮转配置
remove_logrotate() {
    if [ -f "/etc/logrotate.d/${SERVICE_NAME}" ]; then
        log_info "删除日志轮转配置..."
        rm -f "/etc/logrotate.d/${SERVICE_NAME}"
    fi
}

# 删除工作目录
remove_working_dir() {
    if [ -d "$WORKING_DIR" ]; then
        log_info "删除工作目录..."
        rm -rf "$WORKING_DIR"
    fi
}

# 卸载客户端 SDK
remove_client_package() {
    if pip show camera-client >/dev/null 2>&1; then
        log_info "卸载客户端 SDK (camera-client)..."
        pip uninstall -y camera-client --break-system-packages
    else
        log_warn "客户端 SDK 未安装"
    fi
}

# 主函数
main() {
    check_root
    stop_service
    remove_logrotate
    remove_working_dir
    remove_client_package

    log_info "卸载完成"
    echo ""
    echo "如需重新安装，请运行: sudo ./install.sh"
}

main "$@"
