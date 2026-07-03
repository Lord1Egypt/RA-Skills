#!/bin/bash
# setup_stata.sh - Cross-platform Stata edition detection and setup
# Compatible with Windows (Git Bash), macOS, Linux
# Language: auto-detects system locale — Chinese on zh-* systems, English otherwise

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

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

STATA_CMD=""
STATA_EDITION=""
STATA_VERSION=""

detect_stata() {
    # Note: Stata 14/15 use StataMP, StataSE, StataBE (no -64 suffix)
    # Stata 16+ use StataMP-64, StataSE-64, StataBE-64 (with -64 suffix)
    local edisions=("StataMP-64" "StataSE-64" "StataBE-64" "StataMP" "StataSE" "StataBE" "stata-mp" "stata-se" "stata")
    local search_paths=()

    case "$WB_OS" in
        windows)
            search_paths=(
                "C:/Program Files/Stata19"
                "C:/Program Files/Stata18"
                "C:/Program Files/Stata17"
                "C:/Program Files/Stata16"
                "C:/Program Files/Stata15"
                "C:/Program Files/Stata14"
                "D:/Stata19"
                "D:/Stata18"
                "D:/Stata17"
                "D:/Stata16"
                "D:/Stata15"
                "D:/Stata14"
            )
            ;;
        mac)
            search_paths=(
                "/Applications/Stata"
            )
            ;;
        linux)
            search_paths=(
                "/usr/local/stata19"
                "/usr/local/stata18"
                "/usr/local/stata17"
                "/usr/local/stata16"
                "/usr/local/stata15"
                "/usr/local/stata14"
                "/opt/stata19"
                "/opt/stata18"
                "/opt/stata17"
                "/opt/stata16"
                "/opt/stata15"
                "/opt/stata14"
            )
            ;;
    esac

    for dir in "${search_paths[@]}"; do
        for exe_name in "${edisions[@]}"; do
            if [[ -x "$dir/$exe_name" ]] || [[ -x "$dir/$exe_name.exe" ]]; then
                STATA_CMD="$dir/$exe_name"
                [[ -x "$dir/$exe_name.exe" ]] && STATA_CMD="$dir/$exe_name.exe"
                if [[ "$exe_name" == *"MP"* ]] || [[ "$exe_name" == *"mp"* ]]; then
                    STATA_EDITION="MP"
                elif [[ "$exe_name" == *"SE"* ]] || [[ "$exe_name" == *"se"* ]]; then
                    STATA_EDITION="SE"
                else
                    STATA_EDITION="BE"
                fi
                STATA_VERSION="${dir##*Stata}"
                STATA_VERSION="${STATA_VERSION%%/*}"
                log_success "$(LANG_ZH "检测到 Stata $STATA_VERSION ($STATA_EDITION): $STATA_CMD" "Detected Stata $STATA_VERSION ($STATA_EDITION): $STATA_CMD")"
                return 0
            fi
        done
    done

    return 1
}

verify_stata() {
    if [[ -z "$STATA_CMD" ]]; then
        return 1
    fi

    cd /tmp
    LANG_ZH "display 1" "display 1"
    "$STATA_CMD" /b do test_stata.do &>/dev/null 2>&1
    local exit_code=$?

    return $exit_code
}

save_config() {
    local config_file="${1:-$ROOT_DIR/../config.json}"

    if [[ -f "$config_file" ]]; then
        cp "$config_file" "${config_file}.bak.$(date +%Y%m%d_%H%M%S)"
        log_info "$(LANG_ZH "配置已备份: ${config_file}.bak.*" "Config backed up: ${config_file}.bak.*")"
        log_info "$(LANG_ZH "更新已有配置: $config_file" "Updating existing config: $config_file")"
        
        if command -v python &>/dev/null; then
            python -c "
import json, sys
with open('$config_file', 'r') as f:
    config = json.load(f)
config['Stata'] = {
    'installed': True,
    'path': '$STATA_CMD',
    'edition': '$STATA_EDITION',
    'version': '$STATA_VERSION',
    'platform': '$WB_OS',
    'mode': 'simple'
}
with open('$config_file', 'w') as f:
    json.dump(config, f, indent=2)
"
        fi
    else
        cat > "$config_file" << EOF
{
  "Stata": {
    "installed": true,
    "path": "$STATA_CMD",
    "edition": "$STATA_EDITION",
    "version": "$STATA_VERSION",
    "platform": "$WB_OS",
    "mode": "simple"
  }
}
EOF
        log_success "$(LANG_ZH "已创建配置文件: $config_file" "Created config: $config_file")"
    fi
}

main() {
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "=== Stata 配置 (跨平台) ==="
    else
        echo "=== Stata Setup (Cross-Platform) ==="
    fi
    LANG_ZH "Platform: $WB_OS ($WB_ARCH)" "Platform: $WB_OS ($WB_ARCH)"
    LANG_ZH "" ""

    if detect_stata; then
        log_info "$(LANG_ZH "Stata 版本: $STATA_EDITION" "Stata edition: $STATA_EDITION")"
        LANG_ZH "" ""
        read -p "$(LANG_ZH "正确? (Y/n, 或输入 MP/SE/BE 修改)" "Correct? (Y/n, or type MP/SE/BE to change)"): " confirm
        if [[ "$confirm" == "n" || "$confirm" == "N" ]]; then
            detect_stata
        elif [[ -n "$confirm" ]]; then
            STATA_EDITION="$confirm"
            STATA_CMD="${STATA_CMD/MP/$STATA_EDITION}"
            STATA_CMD="${STATA_CMD/SE/$STATA_EDITION}"
            STATA_CMD="${STATA_CMD/BE/$STATA_EDITION}"
        fi
        save_config
        return 0
    fi

    log_error "$(LANG_ZH "未检测到 Stata" "Stata not detected")."
    LANG_ZH "" ""
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        LANG_ZH "请确认:" "请确认:"
        echo "  1. Stata 已安装?"
        echo "  2. 版本 (16/17/18)?"
        echo "  3. 版本类型 (MP/SE/BE)?"
        LANG_ZH "" ""
        LANG_ZH "版本类型说明:" "版本类型说明:"
        echo "  MP = 多核并行版 (Multi-Processor)"
        echo "  SE = 标准版 (Standard Edition)"
        echo "  BE = 基础版 (Basic Edition)"
    else
        LANG_ZH "请确认:" "Please confirm:"
        echo "  1. Stata 已安装?"
        echo "  2. 版本 (16/17/18)?"
        echo "  3. 版本类型 (MP/SE/BE)?"
        LANG_ZH "" ""
        LANG_ZH "版本类型说明:" "Edition Guide:"
        echo "  MP = 多核并行版 (Multi-Processor)"
        echo "  SE = 标准版 (Standard Edition)"
        echo "  BE = 基础版 (Basic Edition)"
    fi

    local manual_path
    read -p "$(LANG_ZH "输入 Stata 路径 (例如: /usr/local/stata18)" "Enter Stata path (e.g., /usr/local/stata18)"): " manual_path
    if [[ -n "$manual_path" ]] && [[ -d "$manual_path" ]]; then
        STATA_CMD="$manual_path"
        save_config
        verify_stata
        return $?
    fi

    return 1
}

main "$@"
