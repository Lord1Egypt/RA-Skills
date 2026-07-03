#!/bin/bash
# setup_r.sh - Cross-platform R setup and detection
# Compatible with Windows (Git Bash), macOS, Linux
# Language: auto-detects system locale — Chinese on zh-* systems, English otherwise

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Source platform detection
source "$ROOT_DIR/_platform-detect.sh"

# ============================================================
# Language Detection
# ============================================================
if [[ "${LANG:-}" == zh_* ]] || [[ "${LC_ALL:-}" == zh_* ]] || [[ "${LANGUAGE:-}" == zh_* ]]; then
    SCRIPT_LANG="zh"
else
    SCRIPT_LANG="en"
fi

log_info() { echo "[INFO] $1"; }
log_error() { echo "[ERROR] $1" >&2; }
log_success() { echo "[OK] $1"; }
log_warn() { echo "[WARN] $1" >&2; }

LANG_ZH() { [[ "$SCRIPT_LANG" == "zh" ]] && echo "$1" || echo "$2"; }

R_CMD=""
R_VERSION=""

detect_r() {
    if command -v Rscript &>/dev/null; then
        R_CMD="$(command -v Rscript)"
        R_VERSION="$("$R_CMD" --version 2>&1 | head -1)"
        log_success "$(LANG_ZH "检测到 R: $R_CMD ($R_VERSION)" "Detected R: $R_CMD ($R_VERSION)")"
        return 0
    fi

    local search_paths=()
    case "$WB_OS" in
        windows)
            search_paths=(
                "C:/Program Files/R/"
                "C:/Program Files (x86)/R/"
            )
            ;;
        mac)
            search_paths=(
                "/Library/Frameworks/R.framework/Resources/bin/"
                "/usr/local/bin/"
                "/opt/homebrew/bin/"
            )
            ;;
        linux)
            search_paths=(
                "/usr/bin/"
                "/usr/local/bin/"
            )
            ;;
    esac

    for pattern in "${search_paths[@]}"; do
        for dir in $pattern; do
            if [[ -x "$dir/Rscript" ]]; then
                R_CMD="$dir/Rscript"
                R_VERSION="$("$R_CMD" --version 2>&1 | head -1)"
                log_success "$(LANG_ZH "检测到 R: $R_CMD ($R_VERSION)" "Detected R: $R_CMD ($R_VERSION)")"
                return 0
            fi
        done
    done

    return 1
}

install_r() {
    local install_path="${1:-}"

    if [[ -z "$install_path" ]]; then
        install_path="$(get_r_default_path)"
    fi

    log_info "$(LANG_ZH "安装 R 到: $install_path" "Installing R to: $install_path")"

    case "$WB_OS" in
        windows)
            local r_url="https://cran.r-project.org/bin/windows/base/R-4.5.1-win.exe"
            local installer="${TEMP:-/tmp}/R-installer.exe"

            LANG_ZH "" ""
            echo "============================================"
            if [[ "$SCRIPT_LANG" == "zh" ]]; then
                echo "  警告: 将从 CRAN 下载 R 安装包"
                echo "  URL: $r_url"
            else
                echo "  WARNING: Will download R installer from CRAN"
                echo "  URL: $r_url"
            fi
            echo "============================================"
            read -p "$(LANG_ZH "确认下载? (y/N)" "Confirm download? (y/N)")" dl_confirm
            if [[ ! "$dl_confirm" =~ ^[Yy]$ ]]; then
                log_error "$(LANG_ZH "已取消下载" "Download cancelled")"
                return 1
            fi

            log_info "$(LANG_ZH "正在从 CRAN 下载 R 安装包..." "Downloading R installer from CRAN...")"
            if command -v curl &>/dev/null; then
                curl -fsSL -o "$installer" "$r_url"
            elif command -v wget &>/dev/null; then
                wget -q -O "$installer" "$r_url"
            else
                log_error "$(LANG_ZH "curl 或 wget required" "curl or wget required")"
                return 1
            fi

            if [[ ! -f "$installer" ]]; then
                log_error "$(LANG_ZH "下载失败" "Download failed"). $(LANG_ZH "请手动从以下地址安装 R" "Please install R manually from"): https://cran.r-project.org/bin/windows/base/"
                return 1
            fi

            log_info "$(LANG_ZH "下载完成，正在静默安装..." "Download complete. Installing silently...")"
            "$installer" /SILENT /COMPONENTS="main,x64,translations"

            local r_bin_dirs=(
                "C:/Program Files/R/bin"
                "C:/Program Files/R/R-4.5.1/bin"
                "$HOME/AppData/Local/Programs/R/bin"
            )
            for rbin in "${r_bin_dirs[@]}"; do
                if [[ -d "$rbin" ]]; then
                    export PATH="$rbin:$PATH"
                    log_success "$(LANG_ZH "已将 R 添加到 PATH: $rbin" "Added R to PATH: $rbin")"
                    break
                fi
            done

            log_info "$(LANG_ZH "安装完成" "Installation complete")."
            return 0
            ;;
        mac)
            if command -v brew &>/dev/null; then
                brew install --cask r
            else
                log_error "$(LANG_ZH "请先安装 Homebrew: https://brew.sh" "Please install Homebrew first: https://brew.sh")"
                return 1
            fi
            ;;
        linux)
            LANG_ZH "" ""
            echo "============================================"
            if [[ "$SCRIPT_LANG" == "zh" ]]; then
                echo "  警告: 将使用 sudo 安装 R"
                echo "  需要管理员权限"
            else
                echo "  WARNING: Will use sudo to install R"
                echo "  Admin privileges required"
            fi
            echo "============================================"
            read -p "$(LANG_ZH "确认继续? (y/N)" "Confirm continue? (y/N)")" sudo_confirm
            if [[ ! "$sudo_confirm" =~ ^[Yy]$ ]]; then
                log_error "$(LANG_ZH "已取消安装" "Installation cancelled")"
                return 1
            fi
            if command -v apt &>/dev/null; then
                sudo apt update
                sudo apt install -y r-base
            elif command -v yum &>/dev/null; then
                sudo yum install -y R
            elif command -v dnf &>/dev/null; then
                sudo dnf install -y R
            else
                log_error "$(LANG_ZH "未找到包管理器，请手动安装 R" "Package manager not found. Please install R manually.")"
                return 1
            fi
            ;;
    esac
}

verify_r() {
    if [[ -z "$R_CMD" ]]; then
        return 1
    fi

    if "$R_CMD" -e "print('R is connected to WorkBuddy successfully')" &>/dev/null; then
        log_success "$(LANG_ZH "R 验证通过" "R verification passed")"
        return 0
    fi

    return 1
}

scan_packages() {
    if [[ -z "$R_CMD" ]]; then
        return 1
    fi

    log_info "$(LANG_ZH "扫描已安装 R 包..." "Scanning installed R packages...")"

    local pkg_list_file="${WORKSPACE_DIR:-/tmp}/r_packages_$(date +%Y%m%d_%H%M%S).txt"

    "$R_CMD" -e "cat(installed.packages()[,'Package'], sep='\n')" 2>/dev/null > "$pkg_list_file"

    local total_count
    total_count=$(wc -l < "$pkg_list_file" | tr -d ' ')

    LANG_ZH "" ""
    echo "============================================"
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "  R 统计分析包汇总"
        echo "  总计: ${total_count} 个包"
    else
        echo "  R Statistical Package Summary"
        echo "  Total: ${total_count} packages"
    fi
    echo "============================================"
    LANG_ZH "" ""

    declare -A stat_categories
    stat_categories["描述统计 / Descriptive Statistics"]="psych pastecs DescTools summarizeR"
    stat_categories["假设检验 / Hypothesis Testing"]="stats car lmtest nortest"
    stat_categories["回归分析 / Regression"]="stats car MASS lme4 nlme survival rms"
    stat_categories["多变量分析 / Multivariate Analysis"]="stats MASS psych FactoMineR factoextra"
    stat_categories["贝叶斯统计 / Bayesian"]="rjags coda bayesrunjags"
    stat_categories["Meta 分析 / Meta Analysis"]="metafor meta"
    stat_categories["问卷与心理测量 / Psychometrics"]="psych lavaan semPlot mirt"
    stat_categories["数据操作 / Data Manipulation"]="dplyr tidyr data.table reshape2"
    stat_categories["数据可视化 / Data Visualization"]="ggplot2 plotly shiny lattice"
    stat_categories["机器学习 / Machine Learning"]="caret randomForest xgboost mlr3"
    stat_categories["时间序列 / Time Series"]="forecast tseries zoo xts"
    stat_categories["空间统计 / Spatial Statistics"]="spdep raster sf"
    stat_categories["生存分析 / Survival Analysis"]="survival cmprsk survminer"
    stat_categories["流行病学 / Epidemiology"]="Epi epitools"
    stat_categories["样本量计算 / Sample Size"]="pwr samplesize"
    stat_categories["结构方程 / SEM"]="lavaan semPlot OpenMx"

    for cat in "${!stat_categories[@]}"; do
        local found_pkgs=()
        for pkg in ${stat_categories[$cat]}; do
            if grep -qw "^${pkg}$" "$pkg_list_file" 2>/dev/null; then
                found_pkgs+=("$pkg")
            fi
        done
        if [[ ${#found_pkgs[@]} -gt 0 ]]; then
            if [[ "$SCRIPT_LANG" == "zh" ]]; then
                LANG_ZH "✅ ${cat}: ${found_pkgs[*]}" "✅ ${cat}: ${found_pkgs[*]}"
            else
                # For English, only show the English part before /
                local en_cat="${cat%% /*}"
                LANG_ZH "✅ ${en_cat}: ${found_pkgs[*]}" "✅ ${en_cat}: ${found_pkgs[*]}"
            fi
        fi
    done

    LANG_ZH "" ""
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        LANG_ZH "完整列表: ${pkg_list_file}" "完整列表: ${pkg_list_file}"
    else
        LANG_ZH "Full list: ${pkg_list_file}" "Full list: ${pkg_list_file}"
    fi
    echo "============================================"

    export R_PACKAGE_COUNT=$total_count
}

save_config() {
    local config_file="${1:-$ROOT_DIR/../config.json}"
    local r_path="${R_CMD:-not installed}"

    if [[ -f "$config_file" ]]; then
        cp "$config_file" "${config_file}.bak.$(date +%Y%m%d_%H%M%S)"
        log_info "$(LANG_ZH "配置已备份: ${config_file}.bak.*" "Config backed up: ${config_file}.bak.*")"
        log_info "$(LANG_ZH "更新已有配置: $config_file" "Updating existing config: $config_file")"
        
        if command -v python &>/dev/null; then
            python -c "
import json, sys
with open('$config_file', 'r') as f:
    config = json.load(f)
config['R'] = {
    'installed': True,
    'path': '$r_path',
    'version': '$R_VERSION',
    'platform': '$WB_OS',
    'mode': 'simple',
    'package_count': ${R_PACKAGE_COUNT:-0}
}
with open('$config_file', 'w') as f:
    json.dump(config, f, indent=2)
"
        fi
    else
        cat > "$config_file" << EOF
{
  "R": {
    "installed": true,
    "path": "$r_path",
    "version": "$R_VERSION",
    "platform": "$WB_OS",
    "mode": "simple",
    "package_count": ${R_PACKAGE_COUNT:-0}
  }
}
EOF
        log_success "$(LANG_ZH "已创建配置文件: $config_file" "Created config: $config_file")"
    fi
}

main() {
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "=== R 语言环境配置 (跨平台) ==="
    else
        echo "=== R Setup (Cross-Platform) ==="
    fi
    LANG_ZH "Platform: $WB_OS ($WB_ARCH)" "Platform: $WB_OS ($WB_ARCH)"
    LANG_ZH "" ""

    if detect_r; then
        verify_r
        save_config
        scan_packages
        return 0
    fi

    LANG_ZH "" ""
    read -p "$(LANG_ZH "未检测到 R。现在安装? (y/N)" "R not detected. Install now? (y/N)")" answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        read -p "$(LANG_ZH "自定义安装路径 (留空使用默认)" "Custom install path (leave empty for default)")" custom_path
        install_r "$custom_path"
        detect_r && verify_r && save_config
        scan_packages
        return $?
    fi

    log_error "$(LANG_ZH "R 不可用，统计分析功能将受限" "R is not available. Statistical analysis capabilities will be limited.")"
    return 1
}

main "$@"
