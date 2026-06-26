#!/bin/bash
# WSL-PowerShell 控制脚本
# 用法：./psctl.sh [选项] "PowerShell 命令"
# 许可证：Apache-2.0

set -e

# 配置
PWSH="/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
PWSH_CORE="/mnt/c/Program Files/PowerShell/7/pwsh.exe"
DEBUG=${DEBUG:-0}
VERBOSE=${VERBOSE:-0}

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
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_debug() {
    if [ "$DEBUG" -eq 1 ]; then
        echo -e "[DEBUG] $1" >&2
    fi
}

show_help() {
    cat << EOF
WSL-PowerShell 控制脚本

用法：$0 [选项] <命令>

选项:
  -h, --help          显示帮助信息
  -v, --verbose       详细输出模式
  -d, --debug         调试模式
  -f, --file <路径>   执行 PowerShell 脚本文件
  -c, --cmd <命令>    执行 PowerShell 命令 (默认)
  -p, --pwsh          使用 PowerShell Core (pwsh.exe)
  -w, --wslpath       自动转换 WSL 路径到 Windows 路径
  --check             检查 PowerShell 是否可用
  --version           显示版本信息

示例:
  $0 "Get-Process | Select-Object -First 5 Name,Id"
  $0 -f /mnt/c/scripts/test.ps1
  $0 -w "Get-ChildItem /mnt/c/Users"
  $0 --check

环境变量:
  DEBUG=1             启用调试模式
  VERBOSE=1           启用详细模式
  PWSH_PATH           自定义 PowerShell 路径
EOF
}

show_version() {
    echo "psctl version 1.0.0"
    echo "License: Apache-2.0"
}

find_pwsh() {
    local use_pwsh_core="$1"
    
    if [ "$use_pwsh_core" -eq 1 ] && [ -x "$PWSH_CORE" ]; then
        echo "$PWSH_CORE"
        return 0
    elif [ -x "$PWSH" ]; then
        echo "$PWSH"
        return 0
    elif [ -x "$PWSH_CORE" ]; then
        echo "$PWSH_CORE"
        return 0
    else
        return 1
    fi
}

process_wsl_paths() {
    local cmd="$1"
    echo "$cmd" | sed -E 's|/mnt/([a-zA-Z])/|\1:\\|g'
}

main() {
    local cmd=""
    local file=""
    local use_pwsh_core=0
    local auto_wsl_path=0
    local mode="command"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            --version)
                show_version
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=1
                shift
                ;;
            -d|--debug)
                DEBUG=1
                shift
                ;;
            -f|--file)
                file="$2"
                mode="file"
                shift 2
                ;;
            -c|--cmd)
                cmd="$2"
                mode="command"
                shift 2
                ;;
            -p|--pwsh)
                use_pwsh_core=1
                shift
                ;;
            -w|--wslpath)
                auto_wsl_path=1
                shift
                ;;
            --check)
                log_info "检查 PowerShell..."
                if pwsh_path=$(find_pwsh $use_pwsh_core); then
                    log_info "PowerShell 可用：$pwsh_path"
                    "$pwsh_path" -Command "Write-Output 'PowerShell 测试成功'"
                    exit 0
                else
                    log_error "未找到可用的 PowerShell"
                    exit 1
                fi
                ;;
            -*)
                log_error "未知选项：$1"
                echo "使用 --help 查看帮助"
                exit 1
                ;;
            *)
                if [ -z "$cmd" ]; then
                    cmd="$1"
                else
                    cmd="$cmd $1"
                fi
                shift
                ;;
        esac
    done
    
    if [ -z "$cmd" ] && [ -z "$file" ]; then
        log_error "未提供命令或脚本文件"
        echo "使用 --help 查看帮助"
        exit 1
    fi
    
    local pwsh_path
    if ! pwsh_path=$(find_pwsh $use_pwsh_core); then
        log_error "未找到可用的 PowerShell"
        log_info "请确保 Windows PowerShell 或 PowerShell Core 已安装"
        exit 1
    fi
    
    log_debug "使用 PowerShell: $pwsh_path"
    
    if [ "$mode" = "file" ]; then
        if [ ! -f "$file" ]; then
            log_error "脚本文件不存在：$file"
            exit 1
        fi
        
        local win_file=""
        if [[ "$file" == /mnt/[a-zA-Z]/* ]]; then
            win_file=$(wslpath -w "$file" 2>/dev/null)
            if [ $? -eq 0 ]; then
                log_debug "WSL 路径：$file -> Windows 路径：$win_file"
            fi
        fi
        
        if [ -z "$win_file" ] || [[ "$win_file" == \\\\wsl* ]]; then
            log_debug "WSL 原生路径，使用 stdin 传输"
            
            if [ "$VERBOSE" -eq 1 ]; then
                log_info "执行脚本 (stdin 模式): $file"
            fi
            
            cat "$file" | "$pwsh_path" -ExecutionPolicy Bypass -NoProfile -Command -
            exit $?
        fi
        
        log_debug "执行脚本：$win_file"
        
        if [ "$VERBOSE" -eq 1 ]; then
            log_info "执行脚本：$win_file"
        fi
        
        "$pwsh_path" -File "$win_file"
        exit $?
    fi
    
    if [ "$mode" = "command" ]; then
        if [ "$auto_wsl_path" -eq 1 ]; then
            cmd=$(process_wsl_paths "$cmd")
            log_debug "转换后的命令：$cmd"
        fi
        
        log_debug "执行命令：$cmd"
        
        if [ "$VERBOSE" -eq 1 ]; then
            log_info "执行命令：$cmd"
        fi
        
        "$pwsh_path" -NoProfile -Command "$cmd"
        exit $?
    fi
}

main "$@"
