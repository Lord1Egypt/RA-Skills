#!/bin/bash

# YiDun Defense - Configure Script
# 易盾加固工具配置脚本（AppKey 管理）

set -e

# 配置
YIDUN_DIR="$HOME/.yidun-defense"
CONFIG_FILE="$YIDUN_DIR/config.ini"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查配置文件是否存在
check_config_file() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log_error "配置文件不存在，请先运行: ./scripts/setup.sh"
        exit 1
    fi
}

# 读取当前 AppKey
get_current_appkey() {
    if [ -f "$CONFIG_FILE" ]; then
        grep "^key=" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' '
    fi
}

# 设置 AppKey
set_appkey() {
    local appkey="$1"

    if [ -z "$appkey" ]; then
        log_error "AppKey 不能为空"
        return 1
    fi

    # 基本验证（AppKey 通常是 32 位字符串）
    if [ ${#appkey} -lt 16 ]; then
        log_error "AppKey 格式不正确，长度过短"
        return 1
    fi

    # 验证 AppKey 格式（仅允许字母数字）
    if ! [[ "$appkey" =~ ^[A-Za-z0-9]+$ ]]; then
        log_error "AppKey 格式不正确（应仅包含字母和数字）"
        return 1
    fi

    # 使用 awk 安全更新配置（避免 sed 注入风险）
    awk -v key="$appkey" '
        /^\[appkey\]/ { in_section=1 }
        /^\[/ && !/^\[appkey\]/ { in_section=0 }
        in_section && /^key=/ { print "key=" key; next }
        { print }
    ' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

    log_success "AppKey 配置成功！"
    return 0
}

# 交互式配置
interactive_configure() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  易盾加固 AppKey 配置${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    # 显示当前配置
    current_appkey=$(get_current_appkey)
    if [ -n "$current_appkey" ]; then
        echo -e "当前 AppKey: ${GREEN}${current_appkey:0:8}...${NC} (已配置)"
        echo ""
        read -p "是否要更新 AppKey? (y/N): " update_choice
        if [[ ! "$update_choice" =~ ^[Yy]$ ]]; then
            log_info "取消配置"
            exit 0
        fi
    else
        echo -e "${YELLOW}尚未配置 AppKey${NC}"
    fi

    echo ""
    echo "如果您还没有 AppKey，请访问："
    echo -e "${BLUE}https://dun.163.com/dashboard#/login/${NC}"
    echo "注册账号并获取加固服务的 appkey"
    echo ""

    # 读取 AppKey（使用 -s 参数隐藏输入）
    read -s -p "请输入您的 AppKey: " new_appkey
    echo ""  # 换行，因为 -s 不会自动换行

    if [ -z "$new_appkey" ]; then
        log_error "AppKey 不能为空"
        exit 1
    fi

    # 设置 AppKey
    if set_appkey "$new_appkey"; then
        echo ""
        log_success "配置完成！现在可以开始使用加固服务了"
        echo ""
        echo "使用示例："
        echo "  ./scripts/defense-smart.sh /path/to/your-file"
    else
        exit 1
    fi
}

# 命令行配置
cli_configure() {
    local appkey="$1"

    if [ -z "$appkey" ]; then
        log_error "请提供 AppKey"
        echo "用法: $0 <appkey>"
        exit 1
    fi

    set_appkey "$appkey"
}

# 显示当前配置
show_config() {
    check_config_file

    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  当前配置${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    current_appkey=$(get_current_appkey)
    if [ -n "$current_appkey" ]; then
        echo -e "AppKey: ${GREEN}${current_appkey:0:8}...${current_appkey: -8}${NC}"
        echo -e "状态: ${GREEN}已配置${NC}"
    else
        echo -e "AppKey: ${RED}未配置${NC}"
    fi

    echo ""
    echo "配置文件: $CONFIG_FILE"
    echo ""
}

# 主函数
main() {
    # 检查配置文件
    check_config_file

    # 根据参数决定模式
    case "$1" in
        --show)
            show_config
            ;;
        --help|-h)
            echo "用法:"
            echo "  $0                  # 交互式配置"
            echo "  $0 <appkey>         # 直接设置 AppKey"
            echo "  $0 --show           # 显示当前配置"
            echo "  $0 --help           # 显示帮助"
            ;;
        "")
            interactive_configure
            ;;
        *)
            cli_configure "$1"
            ;;
    esac
}

# 执行主函数
main "$@"
