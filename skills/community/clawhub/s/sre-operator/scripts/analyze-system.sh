#!/bin/bash
#
# OpenClaw 系统信息收集脚本
# 功能：安全地收集系统基础信息，用于运维诊断
# 特点：只读操作，无破坏性，适配 Linux/macOS
#

set -e

# 默认输出格式
OUTPUT_FORMAT="text"
OUTPUT_FILE=""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 帮助信息
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

安全地收集系统基础信息，用于运维诊断。

OPTIONS:
    --json          输出 JSON 格式
    --output FILE   保存到文件
    --help          显示帮助信息

示例:
    $0                          # 标准输出
    $0 --json                  # JSON 格式输出
    $0 --json --output report.json  # 保存到文件

EOF
    exit 0
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        *)
            echo -e "${RED}错误: 未知参数 $1${NC}"
            usage
            ;;
    esac
done

# 检测系统类型
detect_system_type() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# 收集 Linux 系统信息
collect_linux_info() {
    local os_info=""
    local kernel_info=""
    local uptime_info=""
    local cpu_info=""
    local mem_info=""
    local disk_info=""
    local load_info=""
    local process_info=""

    # 操作系统信息
    if [[ -f /etc/os-release ]]; then
        os_info=$(cat /etc/os-release 2>/dev/null | grep -E "^(NAME|VERSION|PRETTY_NAME)" | tr '\n' ' ')
    elif [[ -f /etc/redhat-release ]]; then
        os_info=$(cat /etc/redhat-release 2>/dev/null)
    elif [[ -f /etc/lsb-release ]]; then
        os_info=$(cat /etc/lsb-release 2>/dev/null)
    fi

    # 内核信息
    kernel_info=$(uname -r 2>/dev/null)
    [[ -z "$kernel_info" ]] && kernel_info="N/A"

    # 系统运行时间
    uptime_info=$(uptime 2>/dev/null)
    [[ -z "$uptime_info" ]] && uptime_info="N/A"

    # CPU 信息
    if command -v lscpu &>/dev/null; then
        cpu_info=$(lscpu 2>/dev/null | grep -E "^CPU\(s\)|^Model name|^Architecture" | tr '\n' ' | ')
    else
        cpu_info=$(grep -E "model name|cpu cores" /proc/cpuinfo 2>/dev/null | head -2 | tr '\n' ' ')
    fi
    [[ -z "$cpu_info" ]] && cpu_info="N/A"

    # 内存信息
    if command -v free &>/dev/null; then
        mem_info=$(free -h 2>/dev/null | grep -E "Mem:|Swap:" | tr '\n' ' | ')
    else
        mem_info="N/A"
    fi

    # 磁盘信息
    if command -v df &>/dev/null; then
        disk_info=$(df -h 2>/dev/null | grep -E "^/dev/" | head -10 | tr '\n' ' | ')
    else
        disk_info="N/A"
    fi

    # 负载信息
    load_info=$(cat /proc/loadavg 2>/dev/null)
    [[ -z "$load_info" ]] && load_info="N/A"

    # 进程信息
    process_info=$(ps aux 2>/dev/null | wc -l)

    echo "system_type:linux"
    echo "os_info:$os_info"
    echo "kernel_info:$kernel_info"
    echo "uptime_info:$uptime_info"
    echo "cpu_info:$cpu_info"
    echo "mem_info:$mem_info"
    echo "disk_info:$disk_info"
    echo "load_info:$load_info"
    echo "process_count:$process_info"
}

# 收集 macOS 系统信息
collect_macos_info() {
    local os_info=""
    local kernel_info=""
    local uptime_info=""
    local cpu_info=""
    local mem_info=""
    local disk_info=""
    local load_info=""
    local process_info=""

    # 操作系统信息
    os_info=$(sw_vers 2>/dev/null | tr '\n' ' | ')
    [[ -z "$os_info" ]] && os_info="N/A"

    # 内核信息
    kernel_info=$(uname -r 2>/dev/null)
    [[ -z "$kernel_info" ]] && kernel_info="N/A"

    # 系统运行时间
    uptime_info=$(uptime 2>/dev/null)
    [[ -z "$uptime_info" ]] && uptime_info="N/A"

    # CPU 信息
    cpu_info=$(sysctl -n machdep.cpu.brand_string 2>/dev/null)
    cpu_info="CPU: $cpu_info Cores: $(sysctl -n hw.ncpu 2>/dev/null)"
    [[ -z "$cpu_info" ]] && cpu_info="N/A"

    # 内存信息
    local total_mem=$(sysctl -n hw.memsize 2>/dev/null)
    if [[ -n "$total_mem" ]]; then
        total_mem=$((total_mem / 1024 / 1024 / 1024))
        local used_mem=$((total_mem - $(vm_stat 2>/dev/null | grep "Pages free" | awk '{print $3}' | sed 's/\.//' 2>/dev/null) * 4096 / 1024 / 1024 / 1024))
        mem_info="Total: ${total_mem}GB Used: ${used_mem}GB"
    else
        mem_info="N/A"
    fi

    # 磁盘信息
    if command -v df &>/dev/null; then
        disk_info=$(df -h 2>/dev/null | grep -E "^/dev/" | head -10 | tr '\n' ' | ')
    else
        disk_info="N/A"
    fi

    # 负载信息
    load_info=$(sysctl -n vm.loadavg 2>/dev/null)
    [[ -z "$load_info" ]] && load_info="N/A"

    # 进程信息
    process_info=$(ps aux 2>/dev/null | wc -l)

    echo "system_type:macos"
    echo "os_info:$os_info"
    echo "kernel_info:$kernel_info"
    echo "uptime_info:$uptime_info"
    echo "cpu_info:$cpu_info"
    echo "mem_info:$mem_info"
    echo "disk_info:$disk_info"
    echo "load_info:$load_info"
    echo "process_count:$process_info"
}

# 输出文本格式
output_text() {
    local system_type=$1
    echo "========================================"
    echo "  OpenClaw 系统信息报告"
    echo "========================================"
    echo ""
    echo "[系统类型] $system_type"
    echo ""
    echo "[基本信息]"
    shift
    while [[ $# -gt 0 ]]; do
        local line="$1"
        local key="${line%%:*}"
        local value="${line#*:}"
        case "$key" in
            system_type) ;;
            os_info) echo "  操作系统: $value" ;;
            kernel_info) echo "  内核版本: $value" ;;
            uptime_info) echo "  运行时间: $value" ;;
            cpu_info) echo "  CPU 信息: $value" ;;
            mem_info) echo "  内存信息: $value" ;;
            disk_info) echo "  磁盘信息: $value" ;;
            load_info) echo "  系统负载: $value" ;;
            process_count) echo "  进程数量: $value" ;;
        esac
        shift
    done
    echo ""
    echo "========================================"
    echo "  收集时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "========================================"
}

# 输出 JSON 格式
output_json() {
    local system_type=$1
    shift
    echo "{"
    echo "  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\","
    echo "  \"system_type\": \"$system_type\","
    echo "  \"system_info\": {"
    local first=true
    while [[ $# -gt 0 ]]; do
        local line="$1"
        local key="${line%%:*}"
        local value="${line#*:}"
        # 转义特殊字符
        value=$(echo "$value" | sed 's/"/\\"/g' | sed 's/\n/\\n/g')
        [[ "$key" != "system_type" ]] && [[ "$first" == "false" ]] && echo ","
        [[ "$key" != "system_type" ]] && echo -n "    \"$key\": \"$value\"" || first=false
        shift
    done
    echo ""
    echo "  }"
    echo "}"
}

# 主函数
main() {
    local system_type=$(detect_system_type)
    local output=""

    echo -e "${GREEN}正在收集系统信息...${NC}"

    # 根据系统类型收集信息
    case "$system_type" in
        linux)
            output=$(collect_linux_info)
            ;;
        macos)
            output=$(collect_macos_info)
            ;;
        *)
            echo -e "${RED}错误: 不支持的系统类型${NC}"
            exit 1
            ;;
    esac

    # 输出结果
    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        result=$(output_json $output)
    else
        result=$(output_text $output)
    fi

    # 保存到文件或输出到标准输出
    if [[ -n "$OUTPUT_FILE" ]]; then
        echo "$result" > "$OUTPUT_FILE"
        echo -e "${GREEN}系统信息已保存到: $OUTPUT_FILE${NC}"
    else
        echo "$result"
    fi

    echo -e "${GREEN}收集完成！${NC}"
}

# 执行主函数
main
