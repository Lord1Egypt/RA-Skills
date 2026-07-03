#!/bin/bash
# setup_sas.sh - Cross-platform SAS detection and setup
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

LANG_ZH() { [[ "$SCRIPT_LANG" == "zh" ]] && echo "$1" || echo "$2"; }

SAS_CMD=""
SAS_VERSION=""

detect_sas() {
    local search_paths=()

    case "$WB_OS" in
        windows)
            search_paths=(
                "C:/Program Files/SASFoundation/9.4"
                "C:/Program Files/SASFoundation/9.3"
                "C:/Program Files/SASFoundation/9.2"
                "C:/Program Files (x86)/SASFoundation/9.4"
                "D:/SASFoundation/9.4"
            )
            ;;
        mac)
            search_paths=(
                "/Applications/SASFoundation/9.4"
            )
            ;;
        linux)
            search_paths=(
                "/opt/SASFoundation/9.4"
                "/usr/local/SASFoundation/9.4"
            )
            ;;
    esac

    for dir in "${search_paths[@]}"; do
        local sas_names=("sas.exe" "sas" "sas_en" "sas_zh")
        for sas_name in "${sas_names[@]}"; do
            if [[ -x "$dir/$sas_name" ]]; then
                SAS_CMD="$dir/$sas_name"
                SAS_VERSION="${dir##*SASFoundation/}"
                SAS_VERSION="${SAS_VERSION%%/*}"
                log_success "$(LANG_ZH "检测到 SAS $SAS_VERSION: $SAS_CMD" "Detected SAS $SAS_VERSION: $SAS_CMD")"
                return 0
            fi
        done
    done

    # Windows: try registry
    if [[ "$WB_OS" == "windows" ]]; then
        local reg_bases=(
            "HKLM\\SOFTWARE\\SAS Institute Inc."
            "HKLM\\SOFTWARE\\Wow6432Node\\SAS Institute Inc."
        )
        for reg_base in "${reg_bases[@]}"; do
            local reg_output
            reg_output=$(reg query "$reg_base" /s 2>/dev/null | grep -i "InstallLocation" | head -1)
            if [[ -n "$reg_output" ]]; then
                local install_dir
                install_dir=$(echo "$reg_output" | awk -F'REG_SZ' '{print $2}' | xargs)
                if [[ -n "$install_dir" && -d "$install_dir" ]]; then
                    local exe="$install_dir/sas.exe"
                    if [[ -x "$exe" ]]; then
                        SAS_CMD="$exe"
                        SAS_VERSION="${install_dir##*SASFoundation/}"
                        SAS_VERSION="${SAS_VERSION%%/*}"
                        log_success "$(LANG_ZH "从注册表检测到 SAS: $SAS_CMD" "Detected SAS via registry: $SAS_CMD")"
                        return 0
                    fi
                fi
            fi
        done
    fi

    # Try command -v as fallback
    if command -v sas &>/dev/null; then
        SAS_CMD="$(command -v sas)"
        log_success "$(LANG_ZH "在 PATH 中检测到 SAS: $SAS_CMD" "Detected SAS in PATH: $SAS_CMD")"
        return 0
    fi

    return 1
}

verify_sas() {
    if [[ -z "$SAS_CMD" ]]; then
        return 1
    fi

    LANG_ZH "" ""
    echo "============================================"
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "  警告: 即将执行 SAS 验证"
        echo "  将运行: $SAS_CMD -sysin test_sas.sas"
    else
        echo "  WARNING: About to execute SAS verification"
        echo "  Will run: $SAS_CMD -sysin test_sas.sas"
    fi
    echo "============================================"
    LANG_ZH "" ""
    read -p "$(LANG_ZH "确认执行? (y/N)" "Confirm execution? (y/N)")" confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        log_info "$(LANG_ZH "跳过 SAS 验证" "Skipping SAS verification")"
        return 0
    fi

    cd /tmp
    echo "proc options; run;" > test_sas.sas
    "$SAS_CMD" -sysin test_sas.sas -log test_sas.log -print test_sas.lst &>/dev/null 2>&1
    local exit_code=$?

    return $exit_code
}

save_config() {
    local config_file="${1:-$ROOT_DIR/../config.json}"

    if [[ -f "$config_file" ]]; then
        log_info "$(LANG_ZH "更新已有配置: $config_file" "Updating existing config: $config_file")"
        if command -v python &>/dev/null; then
            python -c "
import json, sys
with open('$config_file', 'r') as f:
    config = json.load(f)
config['SAS'] = {
    'installed': True,
    'path': '$SAS_CMD',
    'version': '$SAS_VERSION',
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
  "SAS": {
    "installed": true,
    "path": "$SAS_CMD",
    "version": "$SAS_VERSION",
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
        echo "=== SAS 配置 (跨平台) ==="
    else
        echo "=== SAS Setup (Cross-Platform) ==="
    fi
    LANG_ZH "Platform: $WB_OS ($WB_ARCH)" "Platform: $WB_OS ($WB_ARCH)"
    LANG_ZH "" ""

    if detect_sas; then
        log_success "$(LANG_ZH "SAS 已检测到: $SAS_CMD" "SAS detected: $SAS_CMD")"
        save_config
        verify_sas
        LANG_ZH "" ""
        if [[ "$SCRIPT_LANG" == "zh" ]]; then
            echo "=== 批处理调用示例 ==="
            LANG_ZH "简单批处理:" "简单批处理:"
            echo "  $SAS_CMD -sysin \"path/to/program.sas\" -log \"path/to/output.log\" -print \"path/to/output.lst\""
            LANG_ZH "" ""
            LANG_ZH "静默批处理 (无界面):" "静默批处理 (无界面):"
            echo "  $SAS_CMD -batch -nosplash -sysin \"path/to/program.sas\" -log \"path/to/output.log\""
        else
            echo "=== 批处理调用示例 ==="
            LANG_ZH "简单批处理:" "Simple batch:"
            echo "  $SAS_CMD -sysin \"path/to/program.sas\" -log \"path/to/output.log\" -print \"path/to/output.lst\""
            LANG_ZH "" ""
            LANG_ZH "静默批处理 (无界面):" "Silent batch (no GUI):"
            echo "  $SAS_CMD -batch -nosplash -sysin \"path/to/program.sas\" -log \"path/to/output.log\""
        fi
        return 0
    fi

    log_error "$(LANG_ZH "未检测到 SAS" "SAS not detected")."
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        LANG_ZH "请确认:" "请确认:"
        echo "  1. SAS Foundation 已安装?"
        echo "  2. 安装路径?"
    else
        LANG_ZH "请确认:" "Please confirm:"
        echo "  1. SAS Foundation installed?"
        echo "  2. Installation path?"
    fi

    local manual_path
    read -p "$(LANG_ZH "输入 SAS 路径" "Enter SAS path")" manual_path
    if [[ -n "$manual_path" ]] && [[ -d "$manual_path" ]]; then
        SAS_CMD="$manual_path/sas"
        [[ "$WB_OS" == "windows" ]] && SAS_CMD="$manual_path/sas.exe"
        save_config
        verify_sas
        return $?
    fi

    return 1
}

main "$@"
