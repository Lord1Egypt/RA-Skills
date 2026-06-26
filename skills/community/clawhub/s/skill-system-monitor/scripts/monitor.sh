#!/bin/bash
# 系统监控主脚本 - 自动检测系统类型并调用对应脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISTORY_DIR="$SCRIPT_DIR/../history"

# 清理超过 7 天的历史日志
cleanup_old_logs() {
    if [ -d "$HISTORY_DIR" ]; then
        local deleted=$(find "$HISTORY_DIR" -type f -name "*.json" -o -name "*.log" 2>/dev/null | xargs -r stat --format="%Y %n" 2>/dev/null | while read timestamp filepath; do
            local age_days=$(( ($(date +%s) - timestamp) / 86400 ))
            if [ "$age_days" -gt 7 ]; then
                rm -f "$filepath"
                echo "$filepath"
            fi
        done)
        if [ -n "$deleted" ] && [ -n "$(echo "$deleted" | tr -d '[:space:]')" ]; then
            echo "🧹 已清理超过 7 天的历史日志"
        fi
    fi
}

# 执行清理
cleanup_old_logs

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux" ;;
        Darwin*)    echo "macos" ;;
        CYGWIN*)    echo "windows" ;;
        MINGW*)     echo "windows" ;;
        MSYS*)      echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

OS=$(detect_os)

case "$OS" in
    linux)
        if [ -f "$SCRIPT_DIR/monitor-linux.sh" ]; then
            bash "$SCRIPT_DIR/monitor-linux.sh"
        else
            echo "❌ 错误: 找不到 monitor-linux.sh"
            exit 1
        fi
        ;;
    macos)
        if [ -f "$SCRIPT_DIR/monitor-macos.sh" ]; then
            bash "$SCRIPT_DIR/monitor-macos.sh"
        else
            echo "❌ 错误: 找不到 monitor-macos.sh (尚未实现)"
            exit 1
        fi
        ;;
    windows)
        if [ -f "$SCRIPT_DIR/monitor-windows.ps1" ]; then
            powershell.exe -ExecutionPolicy Bypass -File "$SCRIPT_DIR/monitor-windows.ps1"
        else
            echo "❌ 错误: 找不到 monitor-windows.ps1"
            exit 1
        fi
        ;;
    *)
        echo "❌ 错误: 不支持的操作系统 $(uname -s)"
        exit 1
        ;;
esac
