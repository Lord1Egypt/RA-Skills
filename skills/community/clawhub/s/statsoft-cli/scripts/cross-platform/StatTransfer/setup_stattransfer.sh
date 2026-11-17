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

# StatTransfer detection and configuration script
# Supported platforms: Windows, macOS, Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect platform
detect_platform() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        LANG_ZH "linux" "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        LANG_ZH "macos" "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        LANG_ZH "windows" "windows"
    else
        LANG_ZH "unknown" "unknown"
    fi
}

# Detect StatTransfer
detect_stattransfer() {
    local platform=$1
    local st_path=""
    
    log_info "检测 StatTransfer..."
    
    # First check PATH
    if command -v st &> /dev/null; then
        st_path=$(command -v st)
        if statsoft_reveal; then
            log_info "在 PATH 中找到 StatTransfer: $st_path"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        if statsoft_reveal; then
            LANG_ZH "$st_path" "$st_path"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        return 0
    fi
    
    # Platform-specific paths
    if [[ "$platform" == "windows" ]]; then
        local win_paths=(
            "C:/Program Files/StatTransfer/st.exe"
            "C:/Program Files (x86)/StatTransfer/st.exe"
        )
        
        for path in "${win_paths[@]}"; do
            if [[ -f "$path" ]]; then
                st_path="$path"
                if statsoft_reveal; then
                    log_info "找到 StatTransfer: $st_path"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                if statsoft_reveal; then
                    LANG_ZH "$st_path" "$st_path"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                return 0
            fi
        done
    elif [[ "$platform" == "macos" ]]; then
        local mac_paths=(
            "/Applications/StatTransfer/st"
            "/usr/local/bin/st"
        )
        
        for path in "${mac_paths[@]}"; do
            if [[ -f "$path" ]]; then
                st_path="$path"
                if statsoft_reveal; then
                    log_info "找到 StatTransfer: $st_path"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                if statsoft_reveal; then
                    LANG_ZH "$st_path" "$st_path"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                return 0
            fi
        done
    elif [[ "$platform" == "linux" ]]; then
        local linux_paths=(
            "/usr/local/bin/st"
            "/opt/stattransfer/st"
        )
        
        for path in "${linux_paths[@]}"; do
            if [[ -f "$path" ]]; then
                st_path="$path"
                if statsoft_reveal; then
                    log_info "找到 StatTransfer: $st_path"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                if statsoft_reveal; then
                    LANG_ZH "$st_path" "$st_path"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                return 0
            fi
        done
    fi
    
    log_warn "未找到 StatTransfer"
    LANG_ZH "" ""
    return 1
}

# Verify StatTransfer
verify_stattransfer() {
    local st_path=$1
    
    log_info "验证 StatTransfer..."
    
    if [[ -z "$st_path" ]]; then
        log_error "StatTransfer 路径为空"
        return 1
    fi
    
    # Check the executable file
    if [[ ! -f "$st_path" ]] && [[ ! -f "$st_path.exe" ]]; then
        if statsoft_reveal; then
            log_error "StatTransfer 可执行文件不存在: $st_path"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        return 1
    fi
    
    # Version verification launches the detected third-party binary.
    # It runs ONLY when explicitly opted in (STATSOFT_VERIFY=1); default
    # verification reports the path only and never executes the binary (SDI-4).
    local version_output=""
    if [[ "${STATSOFT_VERIFY:-0}" = "1" ]]; then
        if [[ "$st_path" == *.exe ]]; then
            version_output=$("$st_path" --version 2>&1 || true)
        else
            version_output=$("$st_path" --version 2>&1 || true)
        fi
    fi
    
    if [[ -n "$version_output" ]]; then
        if statsoft_reveal; then
            log_info "StatTransfer 版本信息: $version_output"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
    else
        log_warn "无法获取 StatTransfer 版本信息"
    fi
    
    log_info "StatTransfer 验证成功"
    return 0
}

# Configure StatTransfer
configure_stattransfer() {
    local st_path=$1
    local platform=$2
    local config_file="$ROOT_DIR/../config.json"

    log_info "配置 StatTransfer..."

    # Build desired config (read-only); delegate persistence to centralized gate.
    local new_config
    new_config=$(python3 - "$config_file" "$st_path" "$platform" <<'PYEOF'
import json, sys, os
config_file = sys.argv[1]
st_path = sys.argv[2]
platform = sys.argv[3]

config = {}
if os.path.exists(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except Exception:
        config = {}

config['StatTransfer'] = {
    'installed': True,
    'path': st_path,
    'platform': platform,
    'version': 'Unknown'
}
print(json.dumps(config, ensure_ascii=False))
PYEOF
)
    # Fail-closed by default — persist ONLY when explicitly opted in.
    if [ "${STATSOFT_AUTO_WRITE:-0}" = "1" ]; then
        STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$config_file" <<< "$new_config"
    elif [ "${STATSOFT_CONFIRM:-0}" = "1" ] && [ -t 0 ]; then
        printf 'Persist detected config to config.json? (y/N) '
        read -r _ans
        case "$_ans" in y|Y|yes) STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$config_file" <<< "$new_config" ;; *) echo "Detection-only: config.json NOT modified." ;; esac
    else
        echo "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt."
    fi
    log_info "StatTransfer 检测完成 (默认仅检测；设置 STATSOFT_AUTO_WRITE=1 才会写入 config.json)"
    return 0
}

# Main function
main() {
    log_info "开始 StatTransfer 检测与配置..."
    
    # Detect platform
    local platform=$(detect_platform)
    log_info "检测到平台: $platform"
    
    if [[ "$platform" == "unknown" ]]; then
        log_error "不支持的平台"
        exit 1
    fi
    
    # Detect StatTransfer
    local st_path=$(detect_stattransfer "$platform")
    
    if [[ -z "$st_path" ]]; then
        log_warn "未找到 StatTransfer，请手动指定路径"
        
        # Manual path entry requires the same explicit-authorization gate as the verify/configure flow (SDI-4)
        if [[ "${STATSOFT_VERIFY:-0}" != "1" ]] && [[ "${STATSOFT_CONFIRM:-0}" != "1" ]]; then
            log_warn "手动指定路径需显式授权：设置 STATSOFT_VERIFY=1 或 STATSOFT_CONFIRM=1"
            log_error "未配置 StatTransfer"
            exit 1
        fi
        LANG_ZH "请输入 StatTransfer 安装路径（按 Enter 跳过）: " "请输入 StatTransfer 安装路径（按 Enter 跳过）: "
        read -r user_path

        if [[ -n "$user_path" ]]; then
            # Verify it is a real executable, not merely present (SDI-4)
            if [[ -x "$user_path" ]] || [[ -f "$user_path.exe" && -x "$user_path.exe" ]]; then
                st_path="$user_path"
            else
                log_error "路径未指向可执行文件，放弃保存"
                exit 1
            fi
        else
            log_error "未配置 StatTransfer"
            exit 1
        fi
    fi
    
    # Verify StatTransfer
    if ! verify_stattransfer "$st_path"; then
        log_error "StatTransfer 验证失败"
        exit 1
    fi
    
    # Configure StatTransfer
    if ! configure_stattransfer "$st_path" "$platform"; then
        log_error "StatTransfer 配置失败"
        exit 1
    fi
    
    log_info "✅ StatTransfer 配置完成！"
    log_info ""
    log_info "⚠️ 配置完成提示:"
    log_info "  - ✅ Stat/Transfer 是纯 CLI 工具，完全无 GUI，适合自动化"
    log_info "  - ⚠️ 转换前请确认目标格式支持所需的数据类型"
    log_info "  - 💡 在 AI 工作流中的角色：数据格式转换桥梁"
    log_info ""
    log_info "📋 推荐使用方式:"
    log_info "  # 单文件转换"
    if statsoft_reveal; then
        log_info "  \"$st_path\" in.sas7bdat out.dta"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
    log_info ""
    log_info "  # 批量转换"
    if statsoft_reveal; then
        log_info "  \"$st_path\" in\\*.sav out\\*.dta"
    else
        echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
    fi
    
    return 0
}

# Run the main function
main "$@"
