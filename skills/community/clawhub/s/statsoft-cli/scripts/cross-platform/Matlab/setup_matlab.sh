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

# setup_matlab.sh - Matlab 统计软件环境检测与配置脚本
# Matlab: 工程统计软件，跨平台，有 -batch 模式（完全无 GUI）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../_platform-detect.sh"

    LANG_ZH "=== Matlab 环境检测" "Matlab Environment Detection ==="
    LANG_ZH "平台" "Platform: $WB_OS ($WB_ARCH)"
LANG_ZH "" ""

# 检测 Matlab 是否安装
detect_matlab() {
    local matlab_cmd=""
    
    if [ "$WB_OS" = "windows" ]; then
        # Windows: 检查常见安装路径
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
        
        # 检查 PATH
        if [ -z "$matlab_cmd" ]; then
            matlab_cmd=$(which matlab 2>/dev/null)
        fi
    else
        # Mac/Linux: 检查 PATH
        matlab_cmd=$(which matlab 2>/dev/null)
        
        # Mac: 检查应用程序目录
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
        
        # Linux: 检查常见安装路径
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
    
    LANG_ZH "$matlab_cmd" "$matlab_cmd"
}

# 主流程
main() {
    local matlab_path=$(detect_matlab)
    
    if [ -n "$matlab_path" ]; then
    LANG_ZH "✅ 检测到 Matlab 安装" "Matlab installation detected:"
    LANG_ZH "  路径" "Path: $matlab_path"
        
        # 获取版本信息
        local version=$($matlab_path -batch "disp(version)" 2>&1 | tail -1)
    LANG_ZH "  版本" "Version: $version"
        
        # 输出配置信息（供 AI Agent 读取）
        LANG_ZH "" ""
    LANG_ZH "=== 配置信息" "Configuration Info ==="
        LANG_ZH "MATLAB_PATH=$matlab_path" "MATLAB_PATH=$matlab_path"
        LANG_ZH "MATLAB_VERSION=$version" "MATLAB_VERSION=$version"
        LANG_ZH "MATLAB_OS=$WB_OS" "MATLAB_OS=$WB_OS"
        LANG_ZH "MATLAB_ARCH=$WB_ARCH" "MATLAB_ARCH=$WB_ARCH"
        
        # 输出使用说明
        LANG_ZH "" ""
    LANG_ZH "=== 使用说明" "Usage Instructions ==="
        LANG_ZH "批处理命令（完全无 GUI）/ Batch command (completely GUI-free):" "批处理命令（完全无 GUI）/ Batch command (completely GUI-free):"
        echo "  \"$matlab_path\" -batch \"script.m\""
        LANG_ZH "" ""
    LANG_ZH "脚本示例" "Script example:"
        echo "  % script.m"
        echo "  data = readtable('data.csv');"
        echo "  result = fitlm(data, 'y ~ x1 + x2');"
        echo "  disp(result)"
        echo "  writetable(result.Coefficients, 'results.csv');"
        LANG_ZH "" ""
    LANG_ZH "⚠️ Linux/macOS 特殊说明" "Linux/macOS Special Notes:"
        echo "  - 确保 Matlab 许可证服务器可访问（如果使用网络许可证）"
        echo "  - 如果使用个人许可证，确保已激活"
        echo "  - -batch 模式完全无 GUI，适合自动化"
        
    else
    LANG_ZH "❌ 未检测到 Matlab 安装:" "Matlab installation not found:"
        LANG_ZH "" ""
    LANG_ZH "=== 安装指南" "Installation Guide ==="
        
        if [ "$WB_OS" = "windows" ]; then
    LANG_ZH "Windows 安装步骤" "Windows installation steps:"
            echo "  1. 访问 Matlab 官网: https://www.mathworks.com/"
            echo "  2. 下载 Matlab 安装程序"
            echo "  3. 运行安装程序，登录 MathWorks 账户"
            echo "  4. 选择安装 Statistics and Machine Learning Toolbox"
            echo "  5. 安装完成后，matlab.exe 通常在 C:\\Program Files\\MATLAB\\RXXXXx\\bin\\"
        elif [ "$WB_OS" = "mac" ]; then
    LANG_ZH "macOS 安装步骤" "macOS installation steps:"
            echo "  1. 访问 Matlab 官网: https://www.mathworks.com/"
            echo "  2. 下载 Matlab 安装程序（.dmg）"
            echo "  3. 运行安装程序，登录 MathWorks 账户"
            echo "  4. 选择安装 Statistics and Machine Learning Toolbox"
            echo "  5. 安装完成后，matlab 通常在 /Applications/MATLAB_RXXXXx.app/bin/"
        else
    LANG_ZH "Linux 安装步骤" "Linux installation steps:"
            echo "  1. 访问 Matlab 官网: https://www.mathworks.com/"
            echo "  2. 下载 Matlab 安装程序（.sh）"
            echo "  3. 运行安装程序: sudo sh install_matlab.sh"
            echo "  4. 选择安装 Statistics and Machine Learning Toolbox"
            echo "  5. 安装完成后，matlab 通常在 /usr/local/MATLAB/RXXXXx/bin/"
        fi
        
        LANG_ZH "" ""
    LANG_ZH "⚠️ 重要" "Important:"
        echo "  - 必须安装 Statistics and Machine Learning Toolbox 才能使用统计功能"
        echo "  - -batch 模式需要 Matlab R2019a 或更高版本"
    fi
}

main "$@"
