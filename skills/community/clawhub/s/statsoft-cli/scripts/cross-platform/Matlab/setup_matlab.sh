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

# setup_matlab.sh - Matlab statistical software environment detection and configuration script
# Matlab: engineering statistics software; cross-platform, with a -batch mode (fully GUI-free)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../_platform-detect.sh"

    LANG_ZH "=== Matlab 环境检测" "Matlab Environment Detection ==="
    LANG_ZH "平台" "Platform: $WB_OS ($WB_ARCH)"
LANG_ZH "" ""

# Detect whether Matlab is installed
detect_matlab() {
    local matlab_cmd=""
    
    if [ "$WB_OS" = "windows" ]; then
        # Windows: check common installation paths
        local win_paths=(
            "C:/Program Files/MATLAB/R2023b/bin/matlab.exe"
            "C:/Program Files/MATLAB/R2023a/bin/matlab.exe"
            "C:/Program Files/MATLAB/R2022b/bin/matlab.exe"
            "C:/Program Files/MATLAB/R2022a/bin/matlab.exe"
        )
        for path in "${win_paths[@]}"; do
            if [ -f "$path" ]; then
                matlab_cmd="$path"
                break
            fi
        done
        
        # Check PATH
        if [ -z "$matlab_cmd" ]; then
            matlab_cmd=$(command -v matlab 2>/dev/null)
        fi
    else
        # Mac/Linux: check PATH
        matlab_cmd=$(command -v matlab 2>/dev/null)
        
        # Mac: check the Applications directory
        if [ -z "$matlab_cmd" ] && [ "$WB_OS" = "mac" ]; then
            local mac_paths=(
                "/Applications/MATLAB_R2023b.app/bin/matlab"
                "/Applications/MATLAB_R2023a.app/bin/matlab"
            )
            for path in "${mac_paths[@]}"; do
                if [ -f "$path" ]; then
                    matlab_cmd="$path"
                    break
                fi
            done
        fi
        
        # Linux: check common installation paths
        if [ -z "$matlab_cmd" ] && [ "$WB_OS" = "linux" ]; then
            local linux_paths=(
                "/usr/local/MATLAB/R2023b/bin/matlab"
                "/usr/local/MATLAB/R2023a/bin/matlab"
            )
            for path in "${linux_paths[@]}"; do
                if [ -f "$path" ]; then
                    matlab_cmd="$path"
                    break
                fi
            done
        fi
    fi
    
    if statsoft_reveal; then
        LANG_ZH "$matlab_cmd" "$matlab_cmd"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
}
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

# Main flow
main() {
    local matlab_path=$(detect_matlab)
    
    if [ -n "$matlab_path" ]; then
    LANG_ZH "✅ 检测到 Matlab 安装" "Matlab installation detected:"
    if statsoft_reveal; then
        LANG_ZH "  路径" "Path: $matlab_path"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
        
        # Get version info (path check only, do not execute binary / Check path only, do not execute)
        local version="unknown"
        if [ -f "$matlab_path" ]; then
            version=$(basename "$(dirname "$(dirname "$matlab_path")")")
            version=${version#R}
        fi
    if statsoft_reveal; then
        LANG_ZH "  版本" "Version: $version"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
        
        # Output configuration info (for the AI Agent to read)
        LANG_ZH "" ""
    LANG_ZH "=== 配置信息" "Configuration Info ==="
        if statsoft_reveal; then
            LANG_ZH "MATLAB_PATH=$matlab_path" "MATLAB_PATH=$matlab_path"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        if statsoft_reveal; then
            LANG_ZH "MATLAB_VERSION=$version" "MATLAB_VERSION=$version"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        LANG_ZH "MATLAB_OS=$WB_OS" "MATLAB_OS=$WB_OS"
        LANG_ZH "MATLAB_ARCH=$WB_ARCH" "MATLAB_ARCH=$WB_ARCH"
        
        # Output usage instructions
        LANG_ZH "" ""
    LANG_ZH "=== 使用说明" "Usage Instructions ==="
        LANG_ZH "批处理命令（完全无 GUI）" "Batch command (completely GUI-free):"
        if statsoft_reveal; then
            echo "  \"$matlab_path\" -batch \"script.m\""
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        LANG_ZH "" ""
    LANG_ZH "脚本示例" "Script example:"
        echo "  % script.m"
        echo "  data = readtable('data.csv');"
        echo "  result = fitlm(data, 'y ~ x1 + x2');"
        echo "  disp(result)"
        echo "  writetable(result.Coefficients, 'results.csv');"
        LANG_ZH "" ""
    LANG_ZH "⚠️ Linux/macOS 特殊说明" "Linux/macOS Special Notes:"
        echo "$(LANG_ZH "  - 确保 Matlab 许可证服务器可访问（如果使用网络许可证）" "  - Ensure the Matlab license server is reachable (if using a network license)")"
        echo "$(LANG_ZH "  - 如果使用个人许可证，确保已激活" "  - If using a personal license, ensure it is activated")"
        echo "$(LANG_ZH "  - -batch 模式完全无 GUI，适合自动化" "  - -batch mode is completely GUI-free, suitable for automation")"
        
    else
    LANG_ZH "❌ 未检测到 Matlab 安装:" "Matlab installation not found:"
        LANG_ZH "" ""
    LANG_ZH "=== 安装指南" "Installation Guide ==="
        
        if [ "$WB_OS" = "windows" ]; then
    LANG_ZH "Windows 安装步骤" "Windows installation steps:"
            echo "$(LANG_ZH "  1. 访问 Matlab 官网: https://www.mathworks.com/" "  1. Visit the Matlab official website: https://www.mathworks.com/")"
            echo "$(LANG_ZH "  2. 下载 Matlab 安装程序" "  2. Download the Matlab installer")"
            echo "$(LANG_ZH "  3. 运行安装程序，登录 MathWorks 账户" "  3. Run the installer and sign in to your MathWorks account")"
            echo "$(LANG_ZH "  4. 选择安装 Statistics and Machine Learning Toolbox" "  4. Select and install the Statistics and Machine Learning Toolbox")"
            if statsoft_reveal; then
                echo "$(LANG_ZH "  5. 安装完成后，matlab.exe 通常在 C:\\Program Files\\MATLAB\\RXXXXx\\bin\\" "  5. After installation, matlab.exe is usually at C:\\Program Files\\MATLAB\\RXXXXx\\bin\\")"
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
        elif [ "$WB_OS" = "mac" ]; then
    LANG_ZH "macOS 安装步骤" "macOS installation steps:"
            echo "$(LANG_ZH "  1. 访问 Matlab 官网: https://www.mathworks.com/" "  1. Visit the Matlab official website: https://www.mathworks.com/")"
            echo "$(LANG_ZH "  2. 下载 Matlab 安装程序（.dmg）" "  2. Download the Matlab installer (.dmg)")"
            echo "$(LANG_ZH "  3. 运行安装程序，登录 MathWorks 账户" "  3. Run the installer and sign in to your MathWorks account")"
            echo "$(LANG_ZH "  4. 选择安装 Statistics and Machine Learning Toolbox" "  4. Select and install the Statistics and Machine Learning Toolbox")"
            if statsoft_reveal; then
                echo "$(LANG_ZH "  5. 安装完成后，matlab 通常在 /Applications/MATLAB_RXXXXx.app/bin/" "  5. After installation, matlab is usually at /Applications/MATLAB_RXXXXx.app/bin/")"
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
        else
    LANG_ZH "Linux 安装步骤" "Linux installation steps:"
            echo "$(LANG_ZH "  1. 访问 Matlab 官网: https://www.mathworks.com/" "  1. Visit the Matlab official website: https://www.mathworks.com/")"
            echo "$(LANG_ZH "  2. 下载 Matlab 安装程序（.sh）" "  2. Download the Matlab installer (.sh)")"
            echo "$(LANG_ZH "  3. 运行安装程序: sudo sh install_matlab.sh" "  3. Run the installer: sudo sh install_matlab.sh")"
            echo "$(LANG_ZH "  4. 选择安装 Statistics and Machine Learning Toolbox" "  4. Select and install the Statistics and Machine Learning Toolbox")"
            if statsoft_reveal; then
                echo "$(LANG_ZH "  5. 安装完成后，matlab 通常在 /usr/local/MATLAB/RXXXXx/bin/" "  5. After installation, matlab is usually at /usr/local/MATLAB/RXXXXx/bin/")"
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
        fi
        
        LANG_ZH "" ""
    LANG_ZH "⚠️ 重要" "Important:"
        echo "$(LANG_ZH "  - 必须安装 Statistics and Machine Learning Toolbox 才能使用统计功能" "  - You must install the Statistics and Machine Learning Toolbox to use statistical features")"
        echo "$(LANG_ZH "  - -batch 模式需要 Matlab R2019a 或更高版本" "  - -batch mode requires Matlab R2019a or later")"
    fi
}

main "$@"
