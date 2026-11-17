#!/bin/bash
# setup_stata.sh - Cross-platform Stata edition detection and setup
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
                if statsoft_reveal; then
                    log_success "$(LANG_ZH "检测到 Stata $STATA_VERSION ($STATA_EDITION): $STATA_CMD" "Detected Stata $STATA_VERSION ($STATA_EDITION): $STATA_CMD")"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                return 0
            fi
        done
    done

    return 1
}
statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

verify_stata() {
    if [[ -z "$STATA_CMD" ]]; then
        return 1
    fi

    # Run a trivial verification inside a private temp dir with a self-generated
    # do-file, then remove it. This avoids changing into world-writable /tmp as the
    # working directory and never executes a do-file that a third party may have
    # planted in a shared location (SDI-4).
    local verify_dir do_file exit_code
    verify_dir=$(mktemp -d "${TMPDIR:-/tmp}/statsoft_stata.XXXXXX") || return 1
    do_file="$verify_dir/verify.do"
    printf 'display 1\nexit, clear\n' > "$do_file"
    ( cd "$verify_dir" && "$STATA_CMD" /b do "$do_file" ) >/dev/null 2>&1
    exit_code=$?
    rm -rf "$verify_dir"

    return $exit_code
}

save_config() {
    local config_file="${1:-$ROOT_DIR/../config.json}"

    # 1) Build the desired config (read-only) — do NOT write here.
    # 2) Delegate persistence to the centralized fail-closed gate (write_config.py).
    _NEW_CFG=$(python3 - "$config_file" <<PYEOF
import json, sys, os
p = sys.argv[1]
config = {}
if os.path.exists(p):
    with open(p, 'r') as f:
        config = json.load(f)
config['Stata'] = {
    'installed': True,
    'path': '$STATA_CMD',
    'edition': '$STATA_EDITION',
    'version': '$STATA_VERSION',
    'platform': '$WB_OS',
    'mode': 'simple'
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
        echo "$(LANG_ZH "=== Stata 配置 (跨平台) ===" "=== Stata configuration (cross-platform) ===")"
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
        # Unified verification: auto / manual / edition-rewrite all require a real executable (SDI-1)
        if [[ ! ( -x "$STATA_CMD" || -x "$STATA_CMD.exe" ) ]]; then
            log_error "$(LANG_ZH "解析后 Stata 二进制不可执行，放弃保存" "Stata binary not executable after resolution; not saving")"
            return 1
        fi
        if verify_stata; then
            save_config
            return 0
        else
            log_error "$(LANG_ZH "Stata 验证失败，未持久化配置" "Stata verification failed; config not persisted")"
            return 1
        fi
    fi

    log_error "$(LANG_ZH "未检测到 Stata" "Stata not detected")."
    LANG_ZH "" ""
    if [[ "$SCRIPT_LANG" == "zh" ]]; then
        LANG_ZH "请确认:" "请确认:"
        echo "$(LANG_ZH "  1. Stata 已安装?" "  1. Is Stata installed?")"
        echo "$(LANG_ZH "  2. 版本 (16/17/18)?" "  2. Version (16/17/18)?")"
        echo "$(LANG_ZH "  3. 版本类型 (MP/SE/BE)?" "  3. Edition (MP/SE/BE)?")"
        LANG_ZH "" ""
        LANG_ZH "版本类型说明:" "版本类型说明:"
        echo "$(LANG_ZH "  MP = 多核并行版 (Multi-Processor)" "  MP = multi-processor edition (Multi-Processor)")"
        echo "$(LANG_ZH "  SE = 标准版 (Standard Edition)" "  SE = standard edition (Standard Edition)")"
        echo "$(LANG_ZH "  BE = 基础版 (Basic Edition)" "  BE = basic edition (Basic Edition)")"
    else
        LANG_ZH "请确认:" "Please confirm:"
        echo "$(LANG_ZH "  1. Stata 已安装?" "  1. Is Stata installed?")"
        echo "$(LANG_ZH "  2. 版本 (16/17/18)?" "  2. Version (16/17/18)?")"
        echo "$(LANG_ZH "  3. 版本类型 (MP/SE/BE)?" "  3. Edition (MP/SE/BE)?")"
        LANG_ZH "" ""
        LANG_ZH "版本类型说明:" "Edition Guide:"
        echo "$(LANG_ZH "  MP = 多核并行版 (Multi-Processor)" "  MP = multi-processor edition (Multi-Processor)")"
        echo "$(LANG_ZH "  SE = 标准版 (Standard Edition)" "  SE = standard edition (Standard Edition)")"
        echo "$(LANG_ZH "  BE = 基础版 (Basic Edition)" "  BE = basic edition (Basic Edition)")"
    fi

    local manual_path resolved
    read -p "$(LANG_ZH "输入 Stata 路径 (例如: /usr/local/stata18 或其下的可执行文件)" "Enter Stata path (e.g. /usr/local/stata18 or the executable within it)"): " manual_path
    if [[ -n "$manual_path" ]]; then
        # Never persist a bare directory as the executable. Resolve to a real
        # Stata binary (-f and -x), or search the given directory for a known
        # Stata executable name (SDI-1).
        resolved=""
        if [[ -f "$manual_path" && -x "$manual_path" ]]; then
            resolved="$manual_path"
        elif [[ -d "$manual_path" ]]; then
            for _exe in "StataMP-64" "StataSE-64" "StataBE-64" "StataMP" "StataSE" "StataBE" "stata-mp" "stata-se" "stata"; do
                if [[ -x "$manual_path/$_exe" ]]; then
                    resolved="$manual_path/$_exe"; break
                fi
                if [[ -x "$manual_path/$_exe.exe" ]]; then
                    resolved="$manual_path/$_exe.exe"; break
                fi
            done
        fi
        if [[ -z "$resolved" ]]; then
            log_error "$(LANG_ZH "路径未指向有效的 Stata 可执行文件，放弃保存" "Path does not resolve to a valid Stata executable; not saving")"
            return 1
        fi
        STATA_CMD="$resolved"
        case "$(basename "$resolved")" in
            *MP*|*mp*) STATA_EDITION="MP" ;;
            *SE*|*se*) STATA_EDITION="SE" ;;
            *)         STATA_EDITION="BE" ;;
        esac
        # Unified verification pipeline: verify runs before save (SDI-1/SDI-4)
        if verify_stata; then
            save_config
            return 0
        else
            log_error "$(LANG_ZH "Stata 验证失败，未持久化配置" "Stata verification failed; config not persisted")"
            return 1
        fi
    fi

    return 1
}

main "$@"
