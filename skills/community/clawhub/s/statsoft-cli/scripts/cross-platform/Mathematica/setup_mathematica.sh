#!/usr/bin/env bash

# ============================================================
# Language Detection
# ============================================================
if [[ "${LANG:-}" == zh_* ]] || [[ "${LC_ALL:-}" == zh_* ]] || [[ "${LANGUAGE:-}" == zh_* ]]; then
    SCRIPT_LANG="zh"
else
    SCRIPT_LANG="en"
fi

LANG_ZH() { [[ "$SCRIPT_LANG" == "zh" ]] && echo "$1" || echo "$2"; }

# setup_mathematica.sh — Detect and configure Mathematica (cross-platform)
# Supports Mathematica 11.0+ (WolframScript / MathKernel)

set -euo pipefail

statsoft_reveal() { [ "${STATSOFT_REVEAL:-0}" = "1" ]; }
statsoft_verify() { [ "${STATSOFT_VERIFY:-0}" = "1" ]; }

CONFIG_PATH="$(dirname "$0")/../../config.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Source platform detection
if [[ -f "$ROOT_DIR/_platform-detect.sh" ]]; then
    source "$ROOT_DIR/_platform-detect.sh"
fi

MATHKERNEL=""
WOLFRAMSCRIPT=""
INSTALL_DIR=""

detect_mathematica() {
    # Check PATH first
    if command -v wolframscript &>/dev/null; then
        WOLFRAMSCRIPT="$(command -v wolframscript)"
        INSTALL_DIR="$(dirname "$(dirname "$WOLFRAMSCRIPT")")"
        if statsoft_reveal; then
            LANG_ZH "[OK] Found wolframscript: $WOLFRAMSCRIPT" "[OK] Found wolframscript: $WOLFRAMSCRIPT"
        else
            echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
        fi
        return 0
    fi

    # Platform-specific search
    local search_paths=()
    case "${WB_OS:-$(uname -s | tr '[:upper:]' '[:lower:]')}" in
        windows|msys*|mingw*)
            search_paths=(
                "/c/Program Files/Wolfram Research/Mathematica"
                "/c/Program Files (x86)/Wolfram Research/Mathematica"
                "/c/Program Files/Wolfram Research/Wolfram Desktop"
                "$HOME/AppData/Local/Wolfram Desktop"
            )
            ;;
        mac|darwin)
            search_paths=(
                "/Applications/Mathematica.app/Contents/MacOS"
                "/Applications/Wolfram Desktop.app/Contents/MacOS"
                "/usr/local/bin"
                "/opt/local/bin"
            )
            ;;
        linux)
            search_paths=(
                "/usr/local/Wolfram"
                "/opt/Wolfram"
                "$HOME/.Wolfram"
                "/usr/local/bin"
                "/usr/bin"
            )
            ;;
    esac

    for base_path in "${search_paths[@]}"; do
        if [[ -d "$base_path" ]]; then
            # Search for WolframScript
            if [[ -x "$base_path/wolframscript" ]]; then
                WOLFRAMSCRIPT="$base_path/wolframscript"
                INSTALL_DIR="$(dirname "$(dirname "$WOLFRAMSCRIPT")")"
                if statsoft_reveal; then
                    LANG_ZH "[OK] Found wolframscript: $WOLFRAMSCRIPT" "[OK] Found wolframscript: $WOLFRAMSCRIPT"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                return 0
            fi
            # Search for MathKernel — path only disclosed when REVEAL=1 (Issue 8 fix)
            if [[ -x "$base_path/MathKernel" ]]; then
                MATHKERNEL="$base_path/MathKernel"
                INSTALL_DIR="$(dirname "$MATHKERNEL")"
                if statsoft_reveal; then
                    LANG_ZH "[OK] Found MathKernel: $MATHKERNEL" "[OK] Found MathKernel: $MATHKERNEL"
                else
                    echo "$(LANG_ZH "检测到软件（路径/版本已隐藏；设置 STATSOFT_REVEAL=1 可显示）" "Software detected (paths/versions hidden; set STATSOFT_REVEAL=1 to reveal).")"
                fi
                return 0
            fi
        fi
    done

    return 1
}

verify_mathematica() {
    if statsoft_verify && [[ -n "$WOLFRAMSCRIPT" ]] && "$WOLFRAMSCRIPT" -code "Print[\"WolframScript OK\"]" &>/dev/null; then
        LANG_ZH "[OK] WolframScript verification passed" "[OK] WolframScript verification passed"
        return 0
    fi
    if [[ -n "$MATHKERNEL" ]]; then
        LANG_ZH "[OK] MathKernel found (manual verification needed)" "[OK] MathKernel found (manual verification needed)"
        return 0
    fi
    LANG_ZH "[错误] Mathematica 验证失败" "[ERROR] Mathematica verification failed"
    return 1
}

get_version() {
    if [[ -n "$WOLFRAMSCRIPT" ]]; then
        if statsoft_verify; then
            "$WOLFRAMSCRIPT" -code "\$VersionNumber" 2>/dev/null | tr -d '\n\r '
        else
            echo "unknown (set STATSOFT_VERIFY=1)"
        fi
    elif [[ -n "$MATHKERNEL" ]]; then
        basename "$INSTALL_DIR"
    else
        LANG_ZH "unknown" "unknown"
    fi
}

save_config() {
    local version
    version=$(get_version)

    if command -v python3 &>/dev/null; then
        _NEW_CFG=$(python3 - "$CONFIG_PATH" "$MATHKERNEL" "$WOLFRAMSCRIPT" "$version" <<'PYEOF'
import json, sys, os

config_path = sys.argv[1]
mathkernel = sys.argv[2]
wolframscript = sys.argv[3]
version = sys.argv[4]

config = {}
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)

config["Mathematica"] = {
    "installed": True,
    "kernel_path": mathkernel,
    "wolframscript_path": wolframscript,
    "version": version,
    "cross_platform": True,
    "mode": "simple"
}

# Build desired config (read-only) then delegate to centralized fail-closed gate.
print(json.dumps(config, ensure_ascii=False))
PYEOF
)
        # Fail-closed by default — persist ONLY when explicitly opted in.
        if [ "${STATSOFT_AUTO_WRITE:-0}" = "1" ]; then
            STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$CONFIG_PATH" <<< "$_NEW_CFG"
        elif [ "${STATSOFT_CONFIRM:-0}" = "1" ] && [ -t 0 ]; then
            printf 'Persist detected config to config.json? (y/N) '
            read -r _ans
            case "$_ans" in y|Y|yes) STATSOFT_AUTO_WRITE=1 python3 "$(dirname "$0")/../../common/write_config.py" "$CONFIG_PATH" <<< "$_NEW_CFG" ;; *) echo "Detection-only: config.json NOT modified." ;; esac
        else
            echo "Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt."
        fi
    fi
}

main() {
    LANG_ZH "=== Mathematica 跨平台配置 ===" "=== Mathematica Setup (Cross-Platform) ==="
    if [[ -n "${WB_OS:-}" ]]; then
        LANG_ZH "平台: $WB_OS" "Platform: $WB_OS"
    fi
    LANG_ZH "" ""

    if detect_mathematica; then
        verify_mathematica
        save_config
        return 0
    fi

    LANG_ZH "" ""
    LANG_ZH "未检测到 Mathematica。" "Mathematica not detected."
    echo "  Download from https://www.wolfram.com/mathematica/"
    echo "  Or ensure wolframscript/MathKernel is in PATH"
    return 1
}

main "$@"
