#!/bin/bash
#===============================================================================
# 环境检查脚本 - Environment Check Script
# 
# 功能：检查运行豆包文生图脚本所需的环境和依赖
# 版本：1.0.0
# 作者：YangYang
#===============================================================================

set -euo pipefail

readonly SCRIPT_NAME=$(basename "$0")
readonly VERSION="1.0.0"

# 颜色输出
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# 统计
ERRORS=0
WARNINGS=0

#-------------------------------------------------------------------------------
# 日志函数
#-------------------------------------------------------------------------------
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    ERRORS=$((ERRORS + 1))
}

log_header() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
}

#-------------------------------------------------------------------------------
# 检查函数
#-------------------------------------------------------------------------------
check_env_variable() {
    local var_name="$1"
    local var_value="${!var_name:-}"
    
    if [ -z "$var_value" ]; then
        log_error "环境变量 $var_name 未设置"
        return 1
    else
        # 只显示前 10 个字符用于验证
        local display_value="${var_value:0:10}"
        if [ ${#var_value} -gt 10 ]; then
            display_value="${display_value}..."
        fi
        log_info "✓ $var_name 已设置 ($display_value)"
        return 0
    fi
}

check_command() {
    local cmd="$1"
    local description="$2"
    
    if command -v "$cmd" &> /dev/null; then
        local version
        version=$("$cmd" --version 2>&1 | head -n1) || version=$("$cmd" -version 2>&1 | head -n1) || version="版本未知"
        log_info "✓ $description 已安装 ($version)"
        return 0
    else
        log_error "✗ $description 未安装"
        return 1
    fi
}

check_python_package() {
    local package="$1"
    local description="$2"
    
    if python3 -c "import $package" 2>/dev/null; then
        local version
        version=$(python3 -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
        log_info "✓ Python 包 $description 已安装 (v$version)"
        return 0
    else
        log_warn "Python 包 $description 未安装（可选）"
        return 1
    fi
}

check_directory() {
    local dir="$1"
    local permission="$2"
    
    if [ -d "$dir" ]; then
        if [ "$permission" = "write" ] && [ -w "$dir" ]; then
            log_info "✓ 目录 $dir 可写"
            return 0
        elif [ "$permission" = "read" ] && [ -r "$dir" ]; then
            log_info "✓ 目录 $dir 可读"
            return 0
        else
            log_warn "目录 $dir 权限不足 ($permission)"
            return 1
        fi
    else
        log_warn "目录 $dir 不存在（将自动创建）"
        return 0
    fi
}

check_file() {
    local file="$1"
    local permission="$2"
    
    if [ -f "$file" ]; then
        if [ "$permission" = "execute" ] && [ -x "$file" ]; then
            log_info "✓ 文件 $file 可执行"
            return 0
        elif [ "$permission" = "read" ] && [ -r "$file" ]; then
            log_info "✓ 文件 $file 可读"
            return 0
        else
            log_error "文件 $file 权限不足 ($permission)"
            return 1
        fi
    else
        log_error "文件 $file 不存在"
        return 1
    fi
}

#-------------------------------------------------------------------------------
# 主检查流程
#-------------------------------------------------------------------------------
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  豆包文生图 - 环境检查工具 v${VERSION}  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
    
    # 1. 检查环境变量
    log_header "1. 检查环境变量"
    check_env_variable "ARK_API_KEY" || true
    
    # 可选环境变量
    if [ -n "${DOUBAO_API_TIMEOUT:-}" ]; then
        log_info "✓ DOUBAO_API_TIMEOUT = $DOUBAO_API_TIMEOUT"
    else
        log_info "ℹ DOUBAO_API_TIMEOUT 未设置（使用默认值：60）"
    fi
    
    if [ -n "${DOUBAO_RETRY_COUNT:-}" ]; then
        log_info "✓ DOUBAO_RETRY_COUNT = $DOUBAO_RETRY_COUNT"
    else
        log_info "ℹ DOUBAO_RETRY_COUNT 未设置（使用默认值：3）"
    fi
    
    if [ -n "${DOUBAO_OUTPUT_DIR:-}" ]; then
        log_info "✓ DOUBAO_OUTPUT_DIR = $DOUBAO_OUTPUT_DIR"
    else
        log_info "ℹ DOUBAO_OUTPUT_DIR 未设置（使用默认值：generated-images）"
    fi
    
    if [ "${DOUBAO_VERBOSE:-false}" = "true" ]; then
        log_info "✓ DOUBAO_VERBOSE = true"
    else
        log_info "ℹ DOUBAO_VERBOSE = false (默认)"
    fi
    
    # 2. 检查系统依赖
    log_header "2. 检查系统依赖"
    check_command "curl" "curl" || true
    check_command "python3" "Python 3" || true
    check_command "bash" "Bash" || true
    
    # 3. 检查 Python 包（可选）
    log_header "3. 检查 Python 包（可选）"
    check_python_package "requests" "requests" || true
    
    # 4. 检查脚本文件
    log_header "4. 检查脚本文件"
    local script_dir
    script_dir=$(cd "$(dirname "$0")" && pwd)
    
    check_file "$script_dir/doubao-image-generate.sh" "execute" || true
    check_file "$script_dir/doubao-image-generate.py" "execute" || true
    
    # 5. 检查输出目录
    log_header "5. 检查输出目录"
    local output_dir="${DOUBAO_OUTPUT_DIR:-generated-images}"
    check_directory "$output_dir" "write" || true
    
    # 6. 系统信息
    log_header "6. 系统信息"
    log_info "操作系统：$(uname -s) $(uname -r)"
    log_info "主机名：$(uname -n)"
    log_info "架构：$(uname -m)"
    log_info "当前用户：$(whoami)"
    log_info "工作目录：$(pwd)"
    
    # 7. 网络连通性测试（可选）
    log_header "7. 网络连通性测试"
    if ping -c 1 -W 2 ark.cn-beijing.volces.com &> /dev/null; then
        log_info "✓ 火山引擎 API 服务器可达"
    else
        log_warn "无法 ping 通火山引擎 API 服务器（可能被防火墙阻止）"
    fi
    
    if curl -s --connect-timeout 5 https://ark.cn-beijing.volces.com &> /dev/null; then
        log_info "✓ HTTPS 连接正常"
    else
        log_warn "HTTPS 连接测试失败"
    fi
    
    # 总结
    log_header "检查总结"
    
    if [ $ERRORS -gt 0 ]; then
        echo -e "${RED}发现 $ERRORS 个错误，$WARNINGS 个警告${NC}"
        echo ""
        echo "请修复上述错误后重试！"
        echo ""
        
        if [ -z "${ARK_API_KEY:-}" ]; then
            echo "提示：设置 ARK_API_KEY 环境变量："
            echo "  export ARK_API_KEY=\"your_api_key\""
            echo ""
            echo "获取 API Key：https://console.volcengine.com/ark"
        fi
        
        exit 1
    elif [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}发现 $WARNINGS 个警告，0 个错误${NC}"
        echo ""
        echo "环境基本就绪，可以运行（建议关注上述警告）"
        exit 0
    else
        echo -e "${GREEN}✓ 所有检查通过！环境配置完美！${NC}"
        echo ""
        echo "可以开始使用豆包文生图功能了！"
        echo ""
        echo "使用示例："
        echo "  ./doubao-image-generate.sh \"一只在月光下的白色小猫\""
        echo "  python3 doubao-image-generate.py --prompt \"一只在月光下的白色小猫\""
        exit 0
    fi
}

# 显示帮助
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    cat << EOF
$SCRIPT_NAME v$VERSION - 环境检查工具

用法:
  $SCRIPT_NAME [选项]

选项:
  -h, --help     显示此帮助信息

说明:
  本脚本用于检查运行豆包文生图脚本所需的环境和依赖。
  检查项目包括：
  - 环境变量配置
  - 系统依赖（curl, python3, bash）
  - Python 包（requests，可选）
  - 脚本文件权限
  - 输出目录权限
  - 网络连通性

退出码:
  0 - 所有检查通过
  1 - 发现错误，需要修复

EOF
    exit 0
fi

# 执行主函数
main
