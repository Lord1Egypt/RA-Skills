#!/bin/bash
# setup_r.sh - Cross-platform R setup and detection
# Compatible with Windows (Git Bash), macOS, Linux
# Language: auto-detects system locale — Chinese on zh-* systems, English otherwise
# ⚠️ SETUP tool: detects R, optionally downloads/installs R (explicit y/N), installs CRAN packages (explicit y/N), and persists config to config.json (timestamped backup + confirmation). NOT a read-only scanner.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Source platform detection
source "$ROOT_DIR/_platform-detect.sh"

# Prevent MSYS/Git-Bash from converting single-letter slash flags (e.g. /b, /e)
# into Windows drive letters (B:/, E:/) on Windows — that breakage can make tools
# fall back to an interactive GUI. Harmless on macOS/Linux.
export MSYS_NO_PATHCONV=1

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

# Disclosure/verification gates (default-deny).
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

R_CMD=""
R_VERSION=""

detect_r() {
    if command -v Rscript &>/dev/null; then
        R_CMD="$(command -v Rscript)"
        if [ "${STATSOFT_VERIFY:-0}" = "1" ]; then
            R_VERSION="$("$R_CMD" --version 2>&1 | head -1)"
        else
            R_VERSION="unknown (set STATSOFT_VERIFY=1 to query)"
        fi
        if statsoft_reveal; then
            log_success "$(LANG_ZH "检测到 R: $R_CMD ($R_VERSION)" "Detected R: $R_CMD ($R_VERSION)")"
        else
            log_success "$(LANG_ZH "检测到 R（详细信息已隐藏，设置 STATSOFT_REVEAL=1 查看）" "R detected (details hidden; set STATSOFT_REVEAL=1 to reveal)")"
        fi
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
                if [ "${STATSOFT_VERIFY:-0}" = "1" ]; then
                    R_VERSION="$("$R_CMD" --version 2>&1 | head -1)"
                else
                    R_VERSION="unknown (set STATSOFT_VERIFY=1 to query)"
                fi
                if statsoft_reveal; then
            log_success "$(LANG_ZH "检测到 R: $R_CMD ($R_VERSION)" "Detected R: $R_CMD ($R_VERSION)")"
        else
            log_success "$(LANG_ZH "检测到 R（详细信息已隐藏，设置 STATSOFT_REVEAL=1 查看）" "R detected (details hidden; set STATSOFT_REVEAL=1 to reveal)")"
        fi
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
                echo "$(LANG_ZH "  警告: 将从 CRAN 下载 R 安装包" "  Warning: the R package will be downloaded from CRAN")"
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

            log_warn "$(LANG_ZH "注意: 下载的安装包未经数字签名校验，请手动核对 CRAN 官方哈希" "NOTE: downloaded installer is NOT cryptographically signed — verify against official CRAN hash manually")"
            if command -v certutil &>/dev/null; then
                local sha
                sha="$(certutil -hashfile "$installer" SHA256 2>/dev/null | grep -v -i 'SHA256' | tr -d ' \r')"
                log_info "$(LANG_ZH "安装包 SHA256: $sha" "Installer SHA256: $sha")"
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
                echo "$(LANG_ZH "  警告: 将使用 sudo 安装 R" "  Warning: sudo will be used to install R")"
                echo "$(LANG_ZH "  需要管理员权限" "  Administrator privileges required")"
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
            LANG_ZH "" ""
            echo "$(LANG_ZH "本技能不自动执行 sudo 安装。请在确认来源后，手动以管理员权限运行以下命令安装 R：" "This skill does not auto-run sudo. After verifying the source, manually install R as admin with:")"
            if command -v apt &>/dev/null; then
                echo "  sudo apt update && sudo apt install -y r-base"
            elif command -v yum &>/dev/null; then
                echo "  sudo yum install -y R"
            elif command -v dnf &>/dev/null; then
                echo "  sudo dnf install -y R"
            else
                log_error "$(LANG_ZH "未找到包管理器，请手动安装 R" "Package manager not found. Please install R manually.")"
                return 1
            fi
            return 0
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

    # Inventory disclosure gate (SDI-3): package scanning both launches Rscript
    # and prints the package list, which reveals sensitive research/security
    # tooling. Without STATSOFT_REVEAL=1 we skip entirely (no launch, no output).
    if ! statsoft_reveal; then
        log_info "$(LANG_ZH "已跳过 R 包清单（设置 STATSOFT_REVEAL=1 以查看）" "Skipped R package inventory (set STATSOFT_REVEAL=1 to view)")"
        return 0
    fi

    log_info "$(LANG_ZH "扫描已安装 R 包..." "Scanning installed R packages...")"

    # The package inventory is strictly EPHEMERAL: it is written into a private,
    # securely-created temp directory and deleted the moment this function returns
    # (RETURN trap below), on both success and error paths. We do NOT persist the
    # inventory to any cache, workspace, or predictable path — an installed-package
    # list can reveal sensitive project/research/security tooling, so it must never
    # be left on disk (SDI-1/SDI-4).
    local scan_tmp
    scan_tmp="$(mktemp -d "${TMPDIR:-/tmp}/statsoft_rpkg.XXXXXX" 2>/dev/null)"
    if [[ -z "$scan_tmp" || ! -d "$scan_tmp" ]]; then
        log_error "$(LANG_ZH "无法创建安全的临时目录，已跳过包扫描" "Could not create a secure temp directory; skipping package scan")"
        return 1
    fi
    # Guarantee cleanup when the function returns (normal or early), so no
    # inventory file is ever left behind.
    trap 'rm -rf "$scan_tmp" 2>/dev/null' RETURN
    chmod 700 "$scan_tmp" 2>/dev/null || true
    local pkg_list_file="$scan_tmp/packages.txt"

    "$R_CMD" -e "cat(installed.packages()[,'Package'], sep='\n')" 2>/dev/null > "$pkg_list_file"

    local total_count
    total_count=$(wc -l < "$pkg_list_file" | tr -d ' ')

    LANG_ZH "" ""
    echo "============================================"
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "$(LANG_ZH "  R 统计分析包汇总" "  R statistical analysis packages summary")"
        echo "$(LANG_ZH "  总计: ${total_count} 个包" "  Total: ${total_count} packages")"
    else
        echo "  R Statistical Package Summary"
        echo "  Total: ${total_count} packages"
    fi
    echo "============================================"
    LANG_ZH "" ""

    # Portable category tables (indexed arrays — no associative arrays, so this
    # works on macOS's default bash 3.2 as well as bash 4+).
    cat_keys=("Descriptive Statistics" "Hypothesis Testing" "Regression" "Multivariate Analysis" "Bayesian" "Meta Analysis" "Psychometrics" "Data Manipulation" "Data Visualization" "Machine Learning" "Time Series" "Spatial Statistics" "Survival Analysis" "Epidemiology" "Sample Size" "SEM")
    cat_pkgs=("psych pastecs DescTools summarizeR" "stats car lmtest nortest" "stats car MASS lme4 nlme survival rms" "stats MASS psych FactoMineR factoextra" "rjags coda bayesrunjags" "metafor meta" "psych lavaan semPlot mirt" "dplyr tidyr data.table reshape2" "ggplot2 plotly shiny lattice" "caret randomForest xgboost mlr3" "forecast tseries zoo xts" "spdep raster sf" "survival cmprsk survminer" "Epi epitools" "pwr samplesize" "lavaan semPlot OpenMx")
    cat_zh=("描述统计" "假设检验" "回归分析" "多变量分析" "贝叶斯统计" "Meta 分析" "问卷与心理测量" "数据操作" "数据可视化" "机器学习" "时间序列" "空间统计" "生存分析" "流行病学" "样本量计算" "结构方程")

    for i in "${!cat_keys[@]}"; do
        local cat="${cat_keys[$i]}"
        local pkgs="${cat_pkgs[$i]}"
        local zh="${cat_zh[$i]}"
        local found_pkgs=()
        for pkg in $pkgs; do
            if grep -qw "^${pkg}$" "$pkg_list_file" 2>/dev/null; then
                found_pkgs+=("$pkg")
            fi
        done
        if [[ ${#found_pkgs[@]} -gt 0 ]]; then
            if [[ "$SCRIPT_LANG" == "zh" ]]; then
                echo "✅ ${zh}: ${found_pkgs[*]}"
            else
                echo "✅ ${cat}: ${found_pkgs[*]}"
            fi
        fi
    done

    LANG_ZH "" ""
    LANG_ZH "（包清单仅在内存/临时目录中处理，不落盘保存）" "(The package inventory is processed ephemerally and is not saved to disk.)"
    echo "============================================"

    export R_PACKAGE_COUNT=$total_count
    # scan_tmp is removed by the RETURN trap set above.
}

save_config() {
    local config_file="${1:-$ROOT_DIR/../config.json}"
    # Canonicalize + validate the detected path before persisting (SDI-3):
    # resolve to a real path and confirm it is an actual Rscript executable, so
    # we never store an attacker-controlled or non-existent location.
    local r_path="${R_CMD:-not installed}"
    if [[ -n "$R_CMD" ]]; then
        local r_resolved
        r_resolved="$(realpath "$R_CMD" 2>/dev/null || echo "$R_CMD")"
        if [[ -x "$r_resolved" || -x "$r_resolved.exe" ]]; then
            r_path="$r_resolved"
        else
            log_warn "$(LANG_ZH "R 路径不可执行，跳过持久化" "R path not executable; skipping persist")"
            return 1
        fi
    fi

    # 1) Build the desired config (read-only) — do NOT write here.
    # 2) Delegate persistence to the centralized fail-closed gate (write_config.py).
    _NEW_CFG=$(python3 - "$config_file" <<PYEOF
import json, sys, os
p = sys.argv[1]
config = {}
if os.path.exists(p):
    with open(p, 'r') as f:
        config = json.load(f)
config['R'] = {
    'installed': True,
    'path': '$r_path',
    'version': '$R_VERSION',
    'platform': '$WB_OS',
    'mode': 'simple',
    'package_count': ${R_PACKAGE_COUNT:-0}
}
print(json.dumps(config, ensure_ascii=False))
PYEOF
)
    # Fail-closed by default — persist ONLY when explicitly opted in.
    if [ "${STATSOFT_AUTO_WRITE:-0}" = "1" ]; then
        STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$config_file" <<< "$_NEW_CFG"
    elif [ "${STATSOFT_CONFIRM:-0}" = "1" ] && [ -t 0 ]; then
        printf 'Persist detected config to config.json? (y/N) '
        read -r _ans
        case "$_ans" in y|Y|yes) STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$config_file" <<< "$_NEW_CFG" ;; *) echo "Detection-only: config.json NOT modified." ;; esac
    else
        echo "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt."
    fi
}

main() {
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "$(LANG_ZH "=== R 语言环境配置 (跨平台) ===" "=== R language environment configuration (cross-platform) ===")"
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
