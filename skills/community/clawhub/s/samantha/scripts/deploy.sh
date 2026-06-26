#!/bin/bash

# Samantha AI伴侣部署脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装，请先安装"
        exit 1
    fi
}

# 显示横幅
show_banner() {
    echo -e "${BLUE}"
    echo "=========================================="
    echo "    Samantha AI伴侣部署脚本"
    echo "=========================================="
    echo -e "${NC}"
}

# 检查环境
check_environment() {
    log_info "检查部署环境..."
    
    # 检查Python
    check_command python3
    python_version=$(python3 --version | cut -d' ' -f2)
    log_info "Python版本: $python_version"
    
    # 检查Docker
    if command -v docker &> /dev/null; then
        docker_version=$(docker --version | cut -d' ' -f3 | tr -d ',')
        log_info "Docker版本: $docker_version"
    else
        log_warning "Docker未安装，跳过容器化部署"
    fi
    
    # 检查Docker Compose
    if command -v docker-compose &> /dev/null; then
        docker_compose_version=$(docker-compose --version | cut -d' ' -f3 | tr -d ',')
        log_info "Docker Compose版本: $docker_compose_version"
    fi
    
    # 检查Git
    check_command git
    git_version=$(git --version | cut -d' ' -f3)
    log_info "Git版本: $git_version"
}

# 安装依赖
install_dependencies() {
    log_info "安装Python依赖..."
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        log_info "创建虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级pip
    log_info "升级pip..."
    pip install --upgrade pip
    
    # 安装依赖
    log_info "安装项目依赖..."
    pip install -r requirements.txt
    
    if [ -f "requirements-dev.txt" ]; then
        log_info "安装开发依赖..."
        pip install -r requirements-dev.txt
    fi
    
    log_success "依赖安装完成"
}

# 初始化数据库
init_database() {
    log_info "初始化数据库..."
    
    if [ -f "scripts/init_db.py" ]; then
        python scripts/init_db.py
        log_success "数据库初始化完成"
    else
        log_warning "数据库初始化脚本不存在，跳过"
    fi
}

# 运行测试
run_tests() {
    log_info "运行测试..."
    
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --cov=src
        if [ $? -eq 0 ]; then
            log_success "测试通过"
        else
            log_error "测试失败"
            exit 1
        fi
    else
        log_warning "pytest未安装，跳过测试"
    fi
}

# 构建Docker镜像
build_docker() {
    if command -v docker &> /dev/null; then
        log_info "构建Docker镜像..."
        docker build -t samantha-ai:latest .
        log_success "Docker镜像构建完成"
    fi
}

# 启动服务
start_services() {
    log_info "启动服务..."
    
    local mode=$1
    
    case $mode in
        "dev")
            log_info "启动开发模式..."
            uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
            ;;
        "prod")
            if command -v docker-compose &> /dev/null; then
                log_info "使用Docker Compose启动生产环境..."
                docker-compose up -d
                log_success "服务已启动"
                log_info "访问地址: http://localhost:8000"
            else
                log_info "启动生产模式..."
                uvicorn src.main:app --host 0.0.0.0 --port 8000
            fi
            ;;
        "test")
            log_info "启动测试模式..."
            pytest tests/ -v
            ;;
        *)
            log_error "未知模式: $mode"
            log_info "可用模式: dev, prod, test"
            exit 1
            ;;
    esac
}

# 显示状态
show_status() {
    log_info "服务状态检查..."
    
    if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
        docker-compose ps
    fi
    
    # 检查API健康状态
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log_success "API服务运行正常"
    else
        log_warning "API服务可能未运行"
    fi
}

# 停止服务
stop_services() {
    log_info "停止服务..."
    
    if command -v docker-compose &> /dev/null && [ -f "docker-compose.yml" ]; then
        docker-compose down
        log_success "服务已停止"
    else
        log_warning "未找到Docker Compose配置，请手动停止服务"
    fi
}

# 清理环境
cleanup() {
    log_info "清理环境..."
    
    # 删除虚拟环境
    if [ -d "venv" ]; then
        rm -rf venv
        log_info "虚拟环境已删除"
    fi
    
    # 删除缓存文件
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    log_success "环境清理完成"
}

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  install     安装依赖和初始化"
    echo "  start MODE  启动服务 (dev/prod/test)"
    echo "  stop        停止服务"
    echo "  status      显示服务状态"
    echo "  test        运行测试"
    echo "  build       构建Docker镜像"
    echo "  clean       清理环境"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 install      # 安装依赖"
    echo "  $0 start dev    # 启动开发模式"
    echo "  $0 start prod   # 启动生产模式"
    echo "  $0 status       # 查看状态"
}

# 主函数
main() {
    show_banner
    
    local action=$1
    local mode=$2
    
    case $action in
        "install")
            check_environment
            install_dependencies
            init_database
            run_tests
            ;;
        "start")
            if [ -z "$mode" ]; then
                log_error "请指定启动模式 (dev/prod/test)"
                exit 1
            fi
            start_services $mode
            ;;
        "stop")
            stop_services
            ;;
        "status")
            show_status
            ;;
        "test")
            run_tests
            ;;
        "build")
            build_docker
            ;;
        "clean")
            cleanup
            ;;
        "help"|"")
            show_help
            ;;
        *)
            log_error "未知操作: $action"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"