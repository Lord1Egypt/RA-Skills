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
        WOLFRAMSCRIPT="$(which wolframscript)"
        INSTALL_DIR="$(dirname "$(dirname "$WOLFRAMSCRIPT")")"
        LANG_ZH "[OK] Found wolframscript: $WOLFRAMSCRIPT" "[OK] Found wolframscript: $WOLFRAMSCRIPT"
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
                LANG_ZH "[OK] Found wolframscript: $WOLFRAMSCRIPT" "[OK] Found wolframscript: $WOLFRAMSCRIPT"
                return 0
            fi
            # Search for MathKernel
            if [[ -x "$base_path/MathKernel" ]]; then
                MATHKERNEL="$base_path/MathKernel"
                INSTALL_DIR="$(dirname "$MATHKERNEL")"
                LANG_ZH "[OK] Found MathKernel: $MATHKERNEL" "[OK] Found MathKernel: $MATHKERNEL"
                return 0
            fi
        fi
    done

    return 1
}

verify_mathematica() {
    if [[ -n "$WOLFRAMSCRIPT" ]] && "$WOLFRAMSCRIPT" -code "Print[\"WolframScript OK\"]" &>/dev/null; then
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
        "$WOLFRAMSCRIPT" -code "\$VersionNumber" 2>/dev/null | tr -d '\n\r '
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
        python3 - "$CONFIG_PATH" "$MATHKERNEL" "$WOLFRAMSCRIPT" "$version" <<'PYEOF'
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

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print(f"Config updated: {config_path}")
PYEOF
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
