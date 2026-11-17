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
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }

# setup_julia.sh - Julia statistical computing environment detection and configuration script
# Julia: high-performance statistical computing language; cross-platform, pure CLI, suited to Bayesian statistics and machine learning

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../_platform-detect.sh"

    LANG_ZH "=== Julia 环境检测" "Julia Environment Detection ==="
    LANG_ZH "平台: $WB_OS ($WB_ARCH)" "Platform: $WB_OS ($WB_ARCH)"
LANG_ZH "" ""

# Detect whether Julia is installed
detect_julia() {
    local julia_cmd=""
    
    # All platforms: check PATH
    julia_cmd=$(command -v julia 2>/dev/null)
    
    if [ -z "$julia_cmd" ]; then
        # Windows: check common installation paths
        if [ "$WB_OS" = "windows" ]; then
            local win_paths=(
                "C:/Users/$USER/AppData/Local/Programs/Julia-1.9.4/bin/julia.exe"
                "C:/Users/$USER/AppData/Local/Programs/Julia-1.9.3/bin/julia.exe"
            )
            for path in "${win_paths[@]}"; do
                if [ -f "$path" ]; then
                    julia_cmd="$path"
                    break
                fi
            done
        fi
    fi
    
    if statsoft_reveal; then
        LANG_ZH "$julia_cmd" "$julia_cmd"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
}

# Main flow
main() {
    local julia_path=$(detect_julia)
    
    if [ -n "$julia_path" ]; then
    LANG_ZH "✅ 检测到 Julia 安装:" "Julia installation detected:"
        if statsoft_reveal; then
            LANG_ZH "  路径: $julia_path" "Path: $julia_path"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        
        # Version verification launches the detected third-party binary.
        # It runs ONLY when explicitly opted in (STATSOFT_VERIFY=1); default
        # detection reports the path only and never executes the binary (SDI-4).
        local version="unknown"
        if [ "${STATSOFT_VERIFY:-0}" = "1" ]; then
            version=$($julia_path --version 2>&1 | head -1)
        fi
    if statsoft_reveal; then
        LANG_ZH "  版本: $version" "Version: $version"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
        
        # Output configuration info (for the AI Agent to read)
        LANG_ZH "" ""
    LANG_ZH "=== 配置信息" "Configuration Info ==="
        if statsoft_reveal; then
            LANG_ZH "JULIA_PATH=$julia_path" "JULIA_PATH=$julia_path"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        if statsoft_reveal; then
            LANG_ZH "JULIA_VERSION=$version" "JULIA_VERSION=$version"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        LANG_ZH "JULIA_OS=$WB_OS" "JULIA_OS=$WB_OS"
        LANG_ZH "JULIA_ARCH=$WB_ARCH" "JULIA_ARCH=$WB_ARCH"
        # Output usage instructions
        LANG_ZH "" ""
    LANG_ZH "=== 使用说明" "Usage Instructions ==="
        LANG_ZH "批处理命令:" "Batch command:"
        if statsoft_reveal; then
            echo "  $julia_path script.jl"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        
        # Output usage instructions
        LANG_ZH "" ""
    LANG_ZH "=== 使用说明" "Usage Instructions ==="
        LANG_ZH "批处理命令（完全无 GUI）" "Batch command (completely GUI-free):"
        if statsoft_reveal; then
            echo "  $julia_path script.jl"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        LANG_ZH "" ""
    LANG_ZH "脚本示例" "Script example:"
        echo "  # script.jl"
        echo "  using Statistics, GLM, CSV"
        echo "  data = CSV.read(\"data.csv\", DataFrame)"
        echo "  model = lm(@formula(y ~ x1 + x2), data)"
        echo "  println(model)"
        echo "  CSV.write(\"results.csv\", DataFrame(coef=coef(model)))"
        LANG_ZH "" ""
    LANG_ZH "常用统计包" "Common statistical packages:"
        echo "$(LANG_ZH "  - Statistics: 基础统计（已内置）" "  - Statistics: basic statistics (built-in)")"
        echo "$(LANG_ZH "  - GLM: 广义线性模型" "  - GLM: generalized linear models")"
        echo "$(LANG_ZH "  - CSV: 读写 CSV 文件" "  - CSV: read/write CSV files")"
        echo "$(LANG_ZH "  - DataFrames: 数据处理" "  - DataFrames: data manipulation")"
        echo "$(LANG_ZH "  - Turing: 贝叶斯统计" "  - Turing: Bayesian statistics")"
        echo "$(LANG_ZH "  - MLJ: 机器学习" "  - MLJ: machine learning")"
        LANG_ZH "" ""
    LANG_ZH "⚠️ Linux/macOS 特殊说明" "Linux/macOS Special Notes:"
        echo "$(LANG_ZH "  - Linux: 可以使用包管理器安装: apt/yum/brew install julia" "  - Linux: install via package manager: apt/yum/brew install julia")"
        echo "$(LANG_ZH "  - macOS: 推荐使用 Homebrew: brew install julia" "  - macOS: recommended to use Homebrew: brew install julia")"
        echo "$(LANG_ZH "  - 所有平台：首次使用包时需要下载，可能较慢" "  - All platforms: downloading packages on first use may be slow")"
        
    else
    LANG_ZH "❌ 未检测到 Julia 安装:" "Julia installation not found:"
        LANG_ZH "" ""
    LANG_ZH "=== 安装指南" "Installation Guide ==="
        
        if [ "$WB_OS" = "windows" ]; then
    LANG_ZH "Windows 安装步骤" "Windows installation steps:"
            echo "$(LANG_ZH "  1. 访问 Julia 官网: https://julialang.org/downloads/" "  1. Visit the Julia official website: https://julialang.org/downloads/")"
            echo "$(LANG_ZH "  2. 下载 Windows 安装包（.exe）" "  2. Download the Windows installer (.exe)")"
            echo "$(LANG_ZH "  3. 运行安装程序，按默认设置安装" "  3. Run the installer and install with default settings")"
            if statsoft_reveal; then
                echo "$(LANG_ZH "  4. 安装完成后，julia.exe 通常在 C:\\Users\\[USER]\\AppData\\Local\\Programs\\Julia-XX.X.X\\bin\\" "  4. After installation, julia.exe is usually at C:\\Users\\[USER]\\AppData\\Local\\Programs\\Julia-XX.X.X\\bin\\")"
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
        elif [ "$WB_OS" = "mac" ]; then
    LANG_ZH "macOS 安装步骤" "macOS installation steps:"
            echo "$(LANG_ZH "  1. 使用 Homebrew: brew install julia" "  1. Using Homebrew: brew install julia")"
            echo "$(LANG_ZH "  2. 或下载 .dmg 安装包: https://julialang.org/downloads/" "  2. Or download the .dmg installer: https://julialang.org/downloads/")"
            if statsoft_reveal; then
                echo "$(LANG_ZH "  3. 安装完成后，命令行工具在 /Applications/Julia-*.app/Contents/Resources/julia/bin/julia" "  3. After installation, the CLI tool is at /Applications/Julia-*.app/Contents/Resources/julia/bin/julia")"
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
        else
    LANG_ZH "Linux 安装步骤" "Linux installation steps:"
            echo "  Ubuntu/Debian: sudo apt install julia"
            echo "  Fedora/RHEL: sudo dnf install julia"
            echo "  Arch Linux: sudo pacman -S julia"
            echo "$(LANG_ZH "  或从官网下载 .tar.gz: https://julialang.org/downloads/" "  Or download the .tar.gz from the official site: https://julialang.org/downloads/")"
        fi
        
        LANG_ZH "" ""
    LANG_ZH "⚠️ 重要" "Important:"
        echo "$(LANG_ZH "  - 安装后需要安装统计包: julia -e 'using Pkg; Pkg.add(\"GLM\")'" "  - After installation you need to install statistical packages: julia -e 'using Pkg; Pkg.add("GLM")'")"
        echo "$(LANG_ZH "  - 首次使用包时需要下载，可能较慢（耐心等待）" "  - Downloading packages on first use may be slow (please be patient)")"
        echo "$(LANG_ZH "  - Julia 是即时编译（JIT），首次运行可能较慢" "  - Julia is just-in-time (JIT) compiled, so the first run may be slow")"
    fi
}

main "$@"
