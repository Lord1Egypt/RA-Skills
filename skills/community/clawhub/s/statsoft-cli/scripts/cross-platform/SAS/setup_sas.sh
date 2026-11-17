#!/bin/bash
# setup_sas.sh - Cross-platform SAS detection and setup
# Compatible with Windows (Git Bash), macOS, Linux
# Language: auto-detects system locale — Chinese on zh-* systems, English otherwise
# ⚠️ SETUP tool: detects software AND persists config to config.json (timestamped backup + explicit y/N confirmation). NOT a read-only scanner.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

source "$ROOT_DIR/_platform-detect.sh"

# Prevent MSYS/Git-Bash from converting single-letter slash flags (e.g. /b, /e)
# into Windows drive letters (B:/, E:/) on Windows — that breakage makes Stata/SAS
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
                if statsoft_reveal; then
                    log_success "$(LANG_ZH "检测到 SAS $SAS_VERSION: $SAS_CMD" "Detected SAS $SAS_VERSION: $SAS_CMD")"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
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
                        if statsoft_reveal; then
                            log_success "$(LANG_ZH "从注册表检测到 SAS: $SAS_CMD" "Detected SAS via registry: $SAS_CMD")"
                        else
                            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                        fi
                        return 0
                    fi
                fi
            fi
        done
    fi

    # Try command -v as fallback
    if command -v sas &>/dev/null; then
        SAS_CMD="$(command -v sas)"
        if statsoft_reveal; then
            log_success "$(LANG_ZH "在 PATH 中检测到 SAS: $SAS_CMD" "Detected SAS in PATH: $SAS_CMD")"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        return 0
    fi

    return 1
}
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

verify_sas() {
    if [[ -z "$SAS_CMD" ]]; then
        return 1
    fi

    LANG_ZH "" ""
    echo "============================================"
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "$(LANG_ZH "  警告: 即将执行 SAS 验证" "  Warning: about to run SAS verification")"
        if statsoft_reveal; then
            echo "$(LANG_ZH "  将运行: $SAS_CMD -sysin test_sas.sas" "  Will run: $SAS_CMD -sysin test_sas.sas")"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
    else
        echo "  WARNING: About to execute SAS verification"
        if statsoft_reveal; then
            echo "  Will run: $SAS_CMD -sysin test_sas.sas"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
    fi
    echo "============================================"
    LANG_ZH "" ""
    # Fail-closed opt-in: executing SAS is an external action, so default = detection-only (skip).
    # Only proceed when explicitly opted in: STATSOFT_AUTO_WRITE=1, or STATSOFT_CONFIRM=1 + a real TTY.
    if [[ "${STATSOFT_AUTO_WRITE:-}" == "1" ]]; then
        : # auto-proceed
    elif [[ "${STATSOFT_CONFIRM:-}" == "1" && -t 0 ]]; then
        read -p "$(LANG_ZH "确认执行? (y/N)" "Confirm execution? (y/N)")" confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            log_info "$(LANG_ZH "跳过 SAS 验证" "Skipping SAS verification")"
            return 0
        fi
    else
        log_info "$(LANG_ZH "仅检测：跳过 SAS 验证（设置 STATSOFT_AUTO_WRITE=1 执行，或 STATSOFT_CONFIRM=1 交互确认）" "Detection-only: skipping SAS verification (set STATSOFT_AUTO_WRITE=1 to run, or STATSOFT_CONFIRM=1 for an interactive prompt)")"
        return 0
    fi

    # Run SAS verification inside a unique, private temp dir and clean it up on
    # exit — never leave test_sas.sas/.log/.lst behind in world-writable /tmp
    # (disclosed artifacts, removed after use; SDI-1/SDI-4).
    (
      local _sas_tmp
      _sas_tmp="$(mktemp -d 2>/dev/null || echo "/tmp/statsoft_sas_$$")"
      mkdir -p "$_sas_tmp" || exit 1
      trap 'rm -rf "$_sas_tmp"' EXIT
      cd "$_sas_tmp" || exit 1
      echo "proc options; run;" > test_sas.sas
      "$SAS_CMD" -sysin test_sas.sas -log test_sas.log -print test_sas.lst &>/dev/null 2>&1
      exit $?
    )
    local exit_code=$?

    return $exit_code
}

save_config() {
    local config_file="${1:-$ROOT_DIR/../config.json}"

    _NEW_CFG=$(python3 - "$config_file" <<PYEOF
import json, sys, os
p = sys.argv[1]
config = {}
if os.path.exists(p):
    with open(p, 'r') as f:
        config = json.load(f)
config['SAS'] = {
    'installed': True,
    'path': '$SAS_CMD',
    'version': '$SAS_VERSION',
    'platform': '$WB_OS',
    'mode': 'simple'
}
# Build desired config (read-only) then delegate to centralized fail-closed gate.
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
        echo "$(LANG_ZH "=== SAS 配置 (跨平台) ===" "=== SAS configuration (cross-platform) ===")"
    else
        echo "=== SAS Setup (Cross-Platform) ==="
    fi
    LANG_ZH "Platform: $WB_OS ($WB_ARCH)" "Platform: $WB_OS ($WB_ARCH)"
    LANG_ZH "" ""

    if detect_sas; then
        if statsoft_reveal; then
            log_success "$(LANG_ZH "SAS 已检测到: $SAS_CMD" "SAS detected: $SAS_CMD")"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        save_config
        verify_sas
        LANG_ZH "" ""
        if [[ "$SCRIPT_LANG" == "zh" ]]; then
            echo "$(LANG_ZH "=== 批处理调用示例 ===" "=== Batch invocation example ===")"
            LANG_ZH "简单批处理:" "简单批处理:"
            if statsoft_reveal; then
                echo "  $SAS_CMD -sysin \"path/to/program.sas\" -log \"path/to/output.log\" -print \"path/to/output.lst\""
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
            LANG_ZH "" ""
            LANG_ZH "静默批处理 (无界面):" "静默批处理 (无界面):"
            if statsoft_reveal; then
                echo "  $SAS_CMD -batch -nosplash -sysin \"path/to/program.sas\" -log \"path/to/output.log\""
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
        else
            echo "$(LANG_ZH "=== 批处理调用示例 ===" "=== Batch invocation example ===")"
            LANG_ZH "简单批处理:" "Simple batch:"
            if statsoft_reveal; then
                echo "  $SAS_CMD -sysin \"path/to/program.sas\" -log \"path/to/output.log\" -print \"path/to/output.lst\""
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
            LANG_ZH "" ""
            LANG_ZH "静默批处理 (无界面):" "Silent batch (no GUI):"
            if statsoft_reveal; then
                echo "  $SAS_CMD -batch -nosplash -sysin \"path/to/program.sas\" -log \"path/to/output.log\""
            else
                echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
            fi
        fi
        return 0
    fi

    log_error "$(LANG_ZH "未检测到 SAS" "SAS not detected")."
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        LANG_ZH "请确认:" "请确认:"
        echo "$(LANG_ZH "  1. SAS Foundation 已安装?" "  1. Is SAS Foundation installed?")"
        echo "$(LANG_ZH "  2. 安装路径?" "  2. Installation path?")"
    else
        LANG_ZH "请确认:" "Please confirm:"
        echo "  1. SAS Foundation installed?"
        echo "  2. Installation path?"
    fi

    # Detection-only: do NOT solicit a manual path or write config here. If SAS is
    # installed in a non-standard location, the user configures it explicitly.
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        echo "$(LANG_ZH "  3. 若已安装但未检测到，请在 config.json 的 SAS.Path 中手动填写路径，" "  3. If installed but not detected, manually fill in the path in config.json under SAS.Path,")"
        echo "$(LANG_ZH "     或设置环境变量 STATSOFT_AUTO_WRITE=1 后重新运行本脚本以持久化检测结果。" "     or set the environment variable STATSOFT_AUTO_WRITE=1 and re-run this script to persist the detection result.")"
    else
        echo "  3. If installed but not detected, set SAS.Path manually in config.json,"
        echo "     or re-run this script with STATSOFT_AUTO_WRITE=1 to persist a detected result."
    fi

    return 1
}

main "$@"
