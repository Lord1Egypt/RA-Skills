#!/bin/bash
# ============================================================
# WebSocket 连接延迟检测工具 - 依赖安装脚本
# 功能：自动检测并安装 ws_check.sh 运行所需的全部依赖
# 支持：CentOS/RHEL、Ubuntu/Debian、macOS
# 用法：sudo bash install_dependencies.sh
# ============================================================

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 所需依赖列表：工具名 -> 描述
declare -A DEPS_DESC=(
    ["curl"]="HTTP 客户端，用于发送 WebSocket Upgrade 请求并测量各阶段耗时"
    ["dig"]="DNS 查询工具，用于独立诊断 DNS 解析详情"
    ["awk"]="文本处理工具，用于计算和格式化耗时数据"
    ["sed"]="流式文本编辑器，用于解析 URL 和 curl 输出"
)

# 检测操作系统类型
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS_ID="$ID"
        OS_NAME="$NAME"
        OS_VERSION="${VERSION_ID:-unknown}"
    elif [ -f /etc/redhat-release ]; then
        OS_ID="centos"
        OS_NAME="CentOS"
        OS_VERSION=$(cat /etc/redhat-release | grep -oP '\d+\.\d+' | head -1)
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS_ID="macos"
        OS_NAME="macOS"
        OS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "unknown")
    else
        OS_ID="unknown"
        OS_NAME="Unknown"
        OS_VERSION="unknown"
    fi
}

# 打印系统信息
print_system_info() {
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}  WebSocket 延迟检测工具 - 依赖安装程序${NC}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  操作系统：${CYAN}${OS_NAME} ${OS_VERSION}${NC}"
    echo -e "  内核版本：${CYAN}$(uname -r)${NC}"
    echo -e "  系统架构：${CYAN}$(uname -m)${NC}"
    echo -e "  当前用户：${CYAN}$(whoami)${NC}"
    echo ""
}

# 检查单个依赖是否已安装
check_dep() {
    local tool="$1"
    if command -v "$tool" &>/dev/null; then
        local version
        case "$tool" in
            curl) version=$(curl --version 2>/dev/null | head -1 | awk '{print $2}') ;;
            dig)  version=$(dig -v 2>&1 | head -1 | grep -oP '[\d.]+' || echo "已安装") ;;
            awk)  version=$(awk --version 2>/dev/null | head -1 | grep -oP '[\d.]+' || echo "已安装") ;;
            sed)  version=$(sed --version 2>/dev/null | head -1 | grep -oP '[\d.]+' || echo "已安装") ;;
            *)    version="已安装" ;;
        esac
        echo -e "  ${GREEN}✓${NC} ${tool}  ${CYAN}v${version}${NC}  — ${DEPS_DESC[$tool]}"
        return 0
    else
        echo -e "  ${RED}✗${NC} ${tool}  ${RED}未安装${NC}  — ${DEPS_DESC[$tool]}"
        return 1
    fi
}

# 检查所有依赖
check_all_deps() {
    echo -e "${BOLD}[1/3] 检查依赖工具${NC}"
    echo ""

    local missing=()
    for tool in curl dig awk sed; do
        if ! check_dep "$tool"; then
            missing+=("$tool")
        fi
    done

    echo ""

    if [ ${#missing[@]} -eq 0 ]; then
        echo -e "  ${GREEN}✅ 所有依赖已就绪，无需安装！${NC}"
        echo ""
        # 额外检查 curl 版本是否支持 -w 格式化输出
        check_curl_features
        return 0
    else
        echo -e "  ${YELLOW}⚠ 缺少 ${#missing[@]} 个依赖：${missing[*]}${NC}"
        echo ""
        MISSING_DEPS=("${missing[@]}")
        return 1
    fi
}

# 检查 curl 的关键特性
check_curl_features() {
    echo -e "${BOLD}[附加] curl 特性检查${NC}"
    echo ""

    # 检查 curl 是否支持 HTTPS
    if curl --version 2>/dev/null | grep -qi "https"; then
        echo -e "  ${GREEN}✓${NC} HTTPS 支持：已启用"
    else
        echo -e "  ${RED}✗${NC} HTTPS 支持：未启用（wss 协议需要 HTTPS 支持）"
        echo -e "    ${YELLOW}建议重新安装 curl 并确保包含 openssl 支持${NC}"
    fi

    # 检查 -w 格式化输出支持（测试一下）
    local test_output
    test_output=$(curl -s -o /dev/null -w "%{time_namelookup}" https://example.com --max-time 5 2>/dev/null || true)
    if [ -n "$test_output" ] && [ "$test_output" != "0" ]; then
        echo -e "  ${GREEN}✓${NC} -w 格式化输出：正常"
    else
        echo -e "  ${YELLOW}~${NC} -w 格式化输出：无法验证（可能是网络问题）"
    fi

    echo ""
}

# 安装缺失的依赖
install_deps() {
    local missing=("${MISSING_DEPS[@]}")

    echo -e "${BOLD}[2/3] 安装缺失的依赖${NC}"
    echo ""

    # 构建安装命令
    case "$OS_ID" in
        centos|rhel|fedora|rocky|almalinux|amzn)
            echo -e "  包管理器：${CYAN}yum/dnf${NC}"
            echo ""
            local pkgs=()
            for dep in "${missing[@]}"; do
                case "$dep" in
                    curl) pkgs+=("curl") ;;
                    dig)  pkgs+=("bind-utils") ;;
                    awk)  pkgs+=("gawk") ;;
                    sed)  pkgs+=("sed") ;;
                esac
            done
            echo -e "  执行命令：${BOLD}yum install -y ${pkgs[*]}${NC}"
            echo ""
            if command -v dnf &>/dev/null; then
                dnf install -y "${pkgs[@]}"
            else
                yum install -y "${pkgs[@]}"
            fi
            ;;

        ubuntu|debian|linuxmint|pop)
            echo -e "  包管理器：${CYAN}apt${NC}"
            echo ""
            local pkgs=()
            for dep in "${missing[@]}"; do
                case "$dep" in
                    curl) pkgs+=("curl") ;;
                    dig)  pkgs+=("dnsutils") ;;
                    awk)  pkgs+=("gawk") ;;
                    sed)  pkgs+=("sed") ;;
                esac
            done
            echo -e "  执行命令：${BOLD}apt install -y ${pkgs[*]}${NC}"
            echo ""
            apt update -qq
            apt install -y "${pkgs[@]}"
            ;;

        macos)
            echo -e "  包管理器：${CYAN}Homebrew${NC}"
            echo ""
            # 检查 Homebrew 是否已安装
            if ! command -v brew &>/dev/null; then
                echo -e "  ${YELLOW}Homebrew 未安装，正在安装...${NC}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            for dep in "${missing[@]}"; do
                case "$dep" in
                    curl) brew install curl ;;
                    dig)  brew install bind ;;
                    awk)  brew install gawk ;;
                    sed)  brew install gnu-sed ;;
                esac
            done
            ;;

        *)
            echo -e "  ${RED}不支持的操作系统：${OS_NAME}${NC}"
            echo -e "  请手动安装以下工具：${missing[*]}"
            echo ""
            echo -e "  通用安装方式参考："
            echo -e "    curl   : https://curl.se/download.html"
            echo -e "    dig    : https://www.isc.org/bind/ (bind-utils)"
            echo -e "    awk    : https://www.gnu.org/software/gawk/"
            echo -e "    sed    : https://www.gnu.org/software/sed/"
            exit 1
            ;;
    esac

    echo ""
}

# 验证安装结果
verify_installation() {
    echo -e "${BOLD}[3/3] 验证安装结果${NC}"
    echo ""

    local all_ok=true
    for tool in curl dig awk sed; do
        if ! check_dep "$tool"; then
            all_ok=false
        fi
    done

    echo ""

    if $all_ok; then
        echo -e "  ${GREEN}✅ 所有依赖安装成功！${NC}"
        echo ""
        check_curl_features
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "  ${GREEN}现在可以运行：${NC}"
        echo -e "  ${BOLD}  ./ws_check.sh wss://your-websocket-url${NC}"
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    else
        echo -e "  ${RED}⚠ 部分依赖安装失败，请检查上方错误信息${NC}"
        exit 1
    fi
}

# ===================== 主流程 =====================

main() {
    detect_os
    print_system_info

    if check_all_deps; then
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "  ${GREEN}一切就绪！可以直接运行：${NC}"
        echo -e "  ${BOLD}  ./ws_check.sh wss://your-websocket-url${NC}"
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        exit 0
    fi

    # 需要 root 权限安装（macOS 除外）
    if [ "$OS_ID" != "macos" ] && [ "$(id -u)" -ne 0 ]; then
        echo -e "  ${RED}安装依赖需要 root 权限，请使用 sudo 运行：${NC}"
        echo -e "  ${BOLD}  sudo bash $0${NC}"
        exit 1
    fi

    install_deps
    verify_installation
}

main
