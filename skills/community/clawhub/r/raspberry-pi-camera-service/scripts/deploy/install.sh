#!/bin/bash
# 摄像头服务部署脚本
# 安装 systemd 常驻服务

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置
SERVICE_NAME="camera-service"
SERVICE_USER=$(id -un)
SERVICE_GROUP=$(id -gn)
WORKING_DIR="/opt/camera-service"
PYTHON_CMD="python3"
PORT=27793

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/templates"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用 sudo 运行此脚本"
        exit 1
    fi
}

check_system() {
    if ! command -v systemctl &> /dev/null; then
        log_error "未检测到 systemd，此脚本仅支持 systemd 系统"
        exit 1
    fi
    log_info "检测到 systemd 系统"
}

check_python() {
    if ! command -v $PYTHON_CMD &> /dev/null; then
        log_error "未找到 Python3，请先安装"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    log_info "Python 版本: $PYTHON_VERSION"

    log_info "检查 Python 依赖..."
    $PYTHON_CMD -c "import fastapi" 2>/dev/null || log_warn "未安装 fastapi，将在虚拟环境中安装"
    $PYTHON_CMD -c "import uvicorn" 2>/dev/null || log_warn "未安装 uvicorn，将在虚拟环境中安装"
}

check_ffmpeg() {
    if command -v ffmpeg &> /dev/null; then
        FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | cut -d' ' -f3)
        log_info "FFmpeg 版本: $FFMPEG_VERSION"
    else
        log_warn "未检测到 FFmpeg，USB 摄像头和格式转换功能将不可用"
        log_warn "建议安装: sudo apt-get install ffmpeg"
    fi
}

check_picamera() {
    if $PYTHON_CMD -c "import picamera2" 2>/dev/null; then
        log_info "已安装 Picamera2，CSI 摄像头可用"
    else
        log_warn "未检测到 Picamera2，CSI 摄像头功能将不可用"
        log_warn "树莓派系统建议安装: sudo apt-get install python3-picamera2"
    fi
}

render_template() {
    local template_file="$1"
    local output_file="$2"

    if [ ! -f "$template_file" ]; then
        log_error "模板文件不存在: $template_file"
        exit 1
    fi

    # 使用 sed 替换变量
    sed -e "s|{{SERVICE_NAME}}|$SERVICE_NAME|g" \
        -e "s|{{SERVICE_USER}}|$SERVICE_USER|g" \
        -e "s|{{SERVICE_GROUP}}|$SERVICE_GROUP|g" \
        -e "s|{{WORKING_DIR}}|$WORKING_DIR|g" \
        -e "s|{{PORT}}|$PORT|g" \
        "$template_file" > "$output_file"

    log_info "生成文件: $output_file"
}

create_directories() {
    log_info "创建工作目录: $WORKING_DIR"
    mkdir -p "$WORKING_DIR"
    mkdir -p "$WORKING_DIR/logs"
    mkdir -p "$WORKING_DIR/output"

    # 复制项目文件
    log_info "复制项目文件..."
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

    cp -r "$PROJECT_DIR"/*.py "$WORKING_DIR/"
    cp "$PROJECT_DIR/requirements.txt" "$WORKING_DIR/"

    # 设置权限
    chown -R $SERVICE_USER:$SERVICE_GROUP "$WORKING_DIR"
    chmod 755 "$WORKING_DIR"
    chmod 775 "$WORKING_DIR/output"
}

setup_venv() {
    log_info "创建 Python 虚拟环境..."
    cd "$WORKING_DIR"
    $PYTHON_CMD -m venv venv
    source venv/bin/activate

    log_info "安装依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt

    chown -R $SERVICE_USER:$SERVICE_GROUP "$WORKING_DIR/venv"
}

create_configs() {
    log_info "从模板生成配置文件..."

    render_template \
        "$TEMPLATE_DIR/service_template.service.txt" \
        "/etc/systemd/system/${SERVICE_NAME}.service"

    render_template \
        "$TEMPLATE_DIR/service_template.logrotate.txt" \
        "/etc/logrotate.d/${SERVICE_NAME}"

    render_template \
        "$TEMPLATE_DIR/.env.example.txt" \
        "$WORKING_DIR/.env"

    chown $SERVICE_USER:$SERVICE_GROUP "$WORKING_DIR/.env"
    chmod 600 "$WORKING_DIR/.env"
}

install_client_package() {
    log_info "打包并安装客户端 SDK..."

    # 获取 client.py 路径
    local client_source
    client_source="$(dirname "$SCRIPT_DIR")/client.py"

    if [ ! -f "$client_source" ]; then
        log_warn "未找到 client.py，跳过客户端安装"
        return 0
    fi

    # 创建临时包目录
    local pkg_dir
    pkg_dir=$(mktemp -d)

    # 创建包结构
    mkdir -p "$pkg_dir/camera_client"

    # 复制 client.py
    cp "$client_source" "$pkg_dir/camera_client/"

    # 创建 __init__.py，导出主要类
    cat > "$pkg_dir/camera_client/__init__.py" << 'EOF'
"""树莓派摄像头服务客户端 SDK"""

from .client import CameraClient, CameraClientError, ServiceBusyError, APIError

__all__ = ["CameraClient", "CameraClientError", "ServiceBusyError", "APIError"]
__version__ = "1.0.0"
EOF

    # 创建 pyproject.toml
    cat > "$pkg_dir/pyproject.toml" << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "camera-client"
version = "1.0.0"
description = "树莓派摄像头服务客户端 SDK"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["camera_client*"]
EOF

    # 安装到系统 Python（使用 --break-system-packages 绕过 PEP 668 限制）
    log_info "安装 camera-client 包..."
    pip install "$pkg_dir" --quiet --break-system-packages

    # 清理临时目录
    rm -rf "$pkg_dir"

    log_info "客户端 SDK 安装完成: from camera_client import CameraClient"
}

start_service() {
    log_info "重新加载 systemd..."
    systemctl daemon-reload

    log_info "启用服务开机自启..."
    systemctl enable "$SERVICE_NAME"

    log_info "启动服务..."
    systemctl start "$SERVICE_NAME"

    sleep 2

    # 检查状态
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_info "服务启动成功！"
        systemctl status "$SERVICE_NAME" --no-pager
    else
        log_error "服务启动失败，查看日志:"
        journalctl -u "$SERVICE_NAME" -n 20 --no-pager
        exit 1
    fi
}

show_usage() {
    echo ""
    echo "  树莓派摄像头服务部署完成"
    echo ""
    echo "服务名称: $SERVICE_NAME"
    echo "工作目录: $WORKING_DIR"
    echo "服务端口: $PORT"
    echo ""
    echo "配置文件:"
    echo "  systemd: /etc/systemd/system/${SERVICE_NAME}.service"
    echo "  logrotate: /etc/logrotate.d/${SERVICE_NAME}"
    echo "  环境变量: $WORKING_DIR/.env"
    echo ""
    echo "常用命令:"
    echo "  查看状态: sudo systemctl status $SERVICE_NAME"
    echo "  启动服务: sudo systemctl start $SERVICE_NAME"
    echo "  停止服务: sudo systemctl stop $SERVICE_NAME"
    echo "  重启服务: sudo systemctl restart $SERVICE_NAME"
    echo "  查看日志: sudo journalctl -u $SERVICE_NAME -f"
    echo ""
    echo "视频文件目录: $WORKING_DIR/output"
    echo "========================================"
}

main() {
    check_root
    check_system
    check_python
    check_ffmpeg
    check_picamera

    create_directories
    install_client_package  # 先安装客户端到系统 Python
    setup_venv              # 再创建虚拟环境（服务端）
    create_configs
    start_service
    show_usage
}

main "$@"
