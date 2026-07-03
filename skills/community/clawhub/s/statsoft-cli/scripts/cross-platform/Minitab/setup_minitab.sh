#!/bin/bash

# ============================================================
# Language Detection
# ============================================================
if [[ "${LANG:-}" == zh_* ]] || [[ "${LC_ALL:-}" == zh_* ]] || [[ "${LANGUAGE:-}" == zh_* ]]; then
    SCRIPT_LANG="zh"
else
    SCRIPT_LANG="en"
fi

LANG_ZH() { [[ "$SCRIPT_LANG" == "zh" ]] && echo "$1" || echo "$2"; }

# setup_minitab.sh - Minitab 统计软件环境检测与配置脚本
# Minitab: 工业统计软件，Windows 为主，有 CLI 支持

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../_platform-detect.sh"

    LANG_ZH "=== Minitab 环境检测" "Minitab Environment Detection ==="
    LANG_ZH "平台" "Platform: $WB_OS ($WB_ARCH)"
LANG_ZH "" ""

# 检测 Minitab 是否安装
detect_minitab() {
    local minitab_cmd=""
    
    if [ "$WB_OS" = "windows" ]; then
        # Windows: 检查常见安装路径
        local win_paths=(
            "C:/Program Files/Minitab/Minitab 21/mtb.exe"
            "C:/Program Files/Minitab/Minitab 20/mtb.exe"
            "C:/Program Files/Minitab/Minitab 19/mtb.exe"
            "C:/Program Files (x86)/Minitab/Minitab 18/mtb.exe"
        )
        for path in "${win_paths[@]}"; do
            if [ -f "$path" ]; then
                minitab_cmd="$path"
                break
            fi
        done
        
        # 检查 PATH
        if [ -z "$minitab_cmd" ]; then
            minitab_cmd=$(which mtb 2>/dev/null)
        fi
    elif [ "$WB_OS" = "mac" ]; then
        # Mac: Minitab 主要通过云版本或远程访问
        LANG_ZH "⚠️ Minitab 在 macOS 上主要通过 Minitab Web App 或远程桌面访问" "⚠️ Minitab 在 macOS 上主要通过 Minitab Web App 或远程桌面访问"
        echo "   Minitab Web App: https://app.minitab.com/"
    elif [ "$WB_OS" = "linux" ]; then
        # Linux: Minitab 主要通过云版本或远程访问
        LANG_ZH "⚠️ Minitab 在 Linux 上主要通过 Minitab Web App 或远程桌面访问" "⚠️ Minitab 在 Linux 上主要通过 Minitab Web App 或远程桌面访问"
        echo "   Minitab Web App: https://app.minitab.com/"
    fi
    
    LANG_ZH "$minitab_cmd" "$minitab_cmd"
}

# 主流程
main() {
    if [ "$WB_OS" != "windows" ]; then
        LANG_ZH "⚠️ Minitab 主要在 Windows 上运行" "⚠️ Minitab 主要在 Windows 上运行"
        echo "   macOS/Linux 用户可以使用:"
        echo "   - Minitab Web App: https://app.minitab.com/"
        echo "   - 远程桌面访问 Windows 上的 Minitab"
        LANG_ZH "" ""
    LANG_ZH "=== 配置信息" "Configuration Info ==="
        LANG_ZH "MINITAB_AVAILABLE=false" "MINITAB_AVAILABLE=false"
        LANG_ZH "MINITAB_WEB_APP=https://app.minitab.com/" "MINITAB_WEB_APP=https://app.minitab.com/"
        return 0
    fi
    
    local minitab_path=$(detect_minitab)
    
    if [ -n "$minitab_path" ]; then
    LANG_ZH "✅ 检测到 Minitab 安装" "Minitab installation detected:"
    LANG_ZH "  路径" "Path: $minitab_path"
        
        # 输出配置信息（供 AI Agent 读取）
        LANG_ZH "" ""
    LANG_ZH "=== 配置信息" "Configuration Info ==="
        LANG_ZH "MINITAB_PATH=$minitab_path" "MINITAB_PATH=$minitab_path"
        LANG_ZH "MINITAB_OS=$WB_OS" "MINITAB_OS=$WB_OS"
        LANG_ZH "MINITAB_ARCH=$WB_ARCH" "MINITAB_ARCH=$WB_ARCH"
        
        # 输出使用说明
        LANG_ZH "" ""
    LANG_ZH "=== 使用说明" "Usage Instructions ==="
    LANG_ZH "批处理命令" "Batch command:"
        echo "  \"$minitab_path\" /run script.mtb"
        LANG_ZH "" ""
    LANG_ZH "脚本示例" "Script example:"
        echo "  # script.mtb"
        echo "  ALT 2"
        echo "  DSCR y x1 x2"
        echo "  REG y x1 x2"
        echo "  PRT"
        LANG_ZH "" ""
    LANG_ZH "⚠️ 注意事项" "Notes:"
        echo "  - Minitab 运行时可能有短暂闪屏（1-2秒）"
        echo "  - 脚本末尾加 'STOP' 命令可自动退出 Minitab"
        
    else
    LANG_ZH "❌ 未检测到 Minitab 安装" "Minitab installation not found"
        LANG_ZH "" ""
    LANG_ZH "=== 安装指南" "Installation Guide ==="
    LANG_ZH "Windows 安装步骤" "Windows installation steps:"
        echo "  1. 访问 Minitab 官网: https://www.minitab.com/"
        echo "  2. 下载 Minitab 试用版或输入许可证"
        echo "  3. 运行安装程序，按默认设置安装"
        echo "  4. 安装完成后，mtb.exe 通常在 C:\\Program Files\\Minitab\\Minitab XX\\"
    fi
}

main "$@"
