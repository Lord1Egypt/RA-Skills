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

# setup_minitab.sh - Minitab statistical software environment detection and configuration script
# Minitab: industrial statistics software, primarily Windows, with CLI support

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../_platform-detect.sh"

    LANG_ZH "=== Minitab 环境检测" "Minitab Environment Detection ==="
    LANG_ZH "平台" "Platform: $WB_OS ($WB_ARCH)"
LANG_ZH "" ""

# Detect whether Minitab is installed
detect_minitab() {
    local minitab_cmd=""
    
    if [ "$WB_OS" = "windows" ]; then
        # Windows: check common installation paths
        local win_paths=(
            "C:/Program Files/Minitab/Minitab 23/mtb.exe"
            "C:/Program Files/Minitab/Minitab 22/mtb.exe"
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
        
        # Check PATH
        if [ -z "$minitab_cmd" ]; then
            minitab_cmd=$(command -v mtb 2>/dev/null)
        fi
    elif [ "$WB_OS" = "mac" ]; then
        # Mac: Minitab is mainly accessed via the cloud version or remote access
        LANG_ZH "⚠️ Minitab 在 macOS 上主要通过 Minitab Web App 或远程桌面访问" "⚠️ Minitab 在 macOS 上主要通过 Minitab Web App 或远程桌面访问"
        echo "   Minitab Web App: https://app.minitab.com/"
    elif [ "$WB_OS" = "linux" ]; then
        # Linux: Minitab is mainly accessed via the cloud version or remote access
        LANG_ZH "⚠️ Minitab 在 Linux 上主要通过 Minitab Web App 或远程桌面访问" "⚠️ Minitab 在 Linux 上主要通过 Minitab Web App 或远程桌面访问"
        echo "   Minitab Web App: https://app.minitab.com/"
    fi
    
    if statsoft_reveal; then
        LANG_ZH "$minitab_cmd" "$minitab_cmd"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
}
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

# Main flow
main() {
    if [ "$WB_OS" != "windows" ]; then
        LANG_ZH "⚠️ Minitab 主要在 Windows 上运行" "Minitab mainly runs on Windows"
        echo "$(LANG_ZH "   macOS/Linux 用户可以使用:" "   macOS/Linux users can use:")"
        echo "   - Minitab Web App: https://app.minitab.com/"
        echo "$(LANG_ZH "   - 远程桌面访问 Windows 上的 Minitab" "   - Remote desktop to access Minitab on Windows")"
        LANG_ZH "" ""
    LANG_ZH "=== 配置信息" "Configuration Info ==="
        LANG_ZH "MINITAB_AVAILABLE=false" "MINITAB_AVAILABLE=false"
        LANG_ZH "MINITAB_WEB_APP=https://app.minitab.com/" "MINITAB_WEB_APP=https://app.minitab.com/"
        return 0
    fi
    
    local minitab_path=$(detect_minitab)
    
    if [ -n "$minitab_path" ]; then
    LANG_ZH "✅ 检测到 Minitab 安装" "Minitab installation detected:"
    if statsoft_reveal; then
        LANG_ZH "  路径" "Path: $minitab_path"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
        
        # Output configuration info (for the AI Agent to read)
        LANG_ZH "" ""
    LANG_ZH "=== 配置信息" "Configuration Info ==="
        if statsoft_reveal; then
            LANG_ZH "MINITAB_PATH=$minitab_path" "MINITAB_PATH=$minitab_path"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        LANG_ZH "MINITAB_OS=$WB_OS" "MINITAB_OS=$WB_OS"
        LANG_ZH "MINITAB_ARCH=$WB_ARCH" "MINITAB_ARCH=$WB_ARCH"
        
        # Output usage instructions
        LANG_ZH "" ""
    LANG_ZH "=== 使用说明" "Usage Instructions ==="
    LANG_ZH "批处理命令" "Batch command:"
        if statsoft_reveal; then
            echo "  $minitab_path  (GUI-only: 'mtb.exe /run' opens the Minitab GUI, not headless)"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        LANG_ZH "" ""
    LANG_ZH "脚本示例" "Script example:"
        echo "  # script.mtb"
        echo "  ALT 2"
        echo "  DSCR y x1 x2"
        echo "  REG y x1 x2"
        echo "  PRT"
        LANG_ZH "" ""
    LANG_ZH "⚠️ 注意事项" "Notes:"
        echo "$(LANG_ZH "  - Minitab 是 GUI 软件：mtb.exe /run 会弹出 Minitab 主窗口，并非无头批处理" "  - Minitab is GUI software: 'mtb.exe /run' opens the Minitab main window, NOT headless batch")"
        echo "$(LANG_ZH "  - 分析请在 Minitab GUI 中交互进行，或由用户手动启动" "  - Run analyses interactively in the Minitab GUI, or launch it manually")"
        
    else
    LANG_ZH "❌ 未检测到 Minitab 安装" "Minitab installation not found"
        LANG_ZH "" ""
    LANG_ZH "=== 安装指南" "Installation Guide ==="
    LANG_ZH "Windows 安装步骤" "Windows installation steps:"
        echo "$(LANG_ZH "  1. 访问 Minitab 官网: https://www.minitab.com/" "  1. Visit the Minitab official website: https://www.minitab.com/")"
        echo "$(LANG_ZH "  2. 下载 Minitab 试用版或输入许可证" "  2. Download the Minitab trial or enter a license")"
        echo "$(LANG_ZH "  3. 运行安装程序，按默认设置安装" "  3. Run the installer and install with default settings")"
        if statsoft_reveal; then
            echo "$(LANG_ZH "  4. 安装完成后，mtb.exe 通常在 C:\\Program Files\\Minitab\\Minitab XX\\" "  4. After installation, mtb.exe is usually at C:\\Program Files\\Minitab\\Minitab XX\\")"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
    fi
}

main "$@"
