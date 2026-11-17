#!/usr/bin/env bash
# scan_all.sh — Cross-platform batch detection of installed statistical software
# Output JSON: {"R":{"installed":true,"path":"...","version":"..."},...}
# Supports Linux / macOS / Windows (Git Bash / WSL)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../_platform-detect.sh" ]]; then
    source "$SCRIPT_DIR/../_platform-detect.sh"
fi

# Language detection (auto-switch: zh locale -> Chinese, otherwise English)
if [[ "${LANG:-}" == zh_* ]] || [[ "${LC_ALL:-}" == zh_* ]] || [[ "${LANGUAGE:-}" == zh_* ]]; then
    SCRIPT_LANG="zh"
else
    SCRIPT_LANG="en"
fi
LANG_ZH() { [[ "$SCRIPT_LANG" == "zh" ]] && echo "$1" || echo "$2"; }

RESULTS=()

add_result() {
    local name=$1
    local installed=$2
    local path=${3:-null}
    local version=${4:-null}
    local os=${WB_OS:-$(uname -s | tr '[:upper:]' '[:lower:]')}

    if [[ "$installed" == "true" ]]; then
        RESULTS+=("\"$name\": {\"installed\":true,\"path\":\"$path\",\"version\":\"$version\",\"platform\":\"$os\"}")
    fi
}

json_output() {
    echo "{"
    local first=true
    if [[ ${#RESULTS[@]} -gt 0 ]]; then
        for entry in "${RESULTS[@]}"; do
            if $first; then first=false; else echo ","; fi
            printf '  %s' "$entry"
        done
    fi
    echo ""
    echo "}"
}

detect_by_command() {
    local cmd=$1
    command -v "$cmd" &>/dev/null
}

get_version_from_command() {
    local cmd=$1
    "$cmd" --version 2>&1 | head -1 | grep -oE '[0-9]+(\.[0-9]+)+' | head -1
}

check_path_exists() {
    local path=$1
    [[ -e "$path" ]] && echo "$path" || return 1
}

# ─────────── CONSENT GATE (SQP-2) ───────────
# Host-wide inventory exposes local tooling paths and versions. Require explicit
# opt-in before running: STATSOFT_AUTO_WRITE=1 (non-interactive) or
# STATSOFT_CONFIRM=1 + a real TTY (interactive y/N). Otherwise abort with notice.
if [[ "${STATSOFT_AUTO_WRITE:-}" == "1" ]]; then
    : # auto-proceed
elif [[ "${STATSOFT_CONFIRM:-}" == "1" && -t 0 ]]; then
    LANG_ZH "本操作将盘点本机上已安装的统计软件（包含安装路径与版本）。" "This will inventory installed statistical software (paths + versions) on this host."
    read -p "$(LANG_ZH "是否继续进行全面检测？(y/N) " "Proceed with host-wide detection? (y/N) ")" _ans
    case "$_ans" in y|Y|yes) : ;; *) LANG_ZH "已中止：全面检测需要明确同意。" "Aborted: host-wide detection requires explicit consent."; exit 0 ;; esac
else
    LANG_ZH "已跳过全面检测：需要明确同意。" "Host-wide detection skipped: requires explicit consent."
    LANG_ZH "设置 STATSOFT_AUTO_WRITE=1 以非交互方式运行，或设置 STATSOFT_CONFIRM=1 以进入交互式提示。" "Set STATSOFT_AUTO_WRITE=1 to run non-interactively, or STATSOFT_CONFIRM=1 for an interactive prompt."
    exit 0
fi

# ─────────── PLATFORM-SPECIFIC DETECTION ───────────

case "${WB_OS:-$(uname -s | tr '[:upper:]' '[:lower:]')}" in
    linux)
        # R
        if detect_by_command R; then
            add_result "R" true "$(command -v R)" "$(get_version_from_command R)"
        fi

        # Stata
        for s in stata-mp stata-se stata; do
            if detect_by_command "$s"; then
                add_result "Stata" true "$(command -v "$s")" "unknown"
                break
            fi
        done

        # Julia
        if detect_by_command julia; then
            add_result "Julia" true "$(command -v julia)" "$(get_version_from_command julia)"
        fi

        # Python
        for py in python3 python; do
            if detect_by_command "$py"; then
                add_result "Python" true "$(command -v "$py")" "$(get_version_from_command "$py")"
                break
            fi
        done

        # Gretl
        if detect_by_command gretlcli; then
            add_result "Gretl" true "$(command -v gretlcli)" "$(get_version_from_command gretlcli)"
        fi

        # PSPP
        if detect_by_command pspp; then
            add_result "PSPP" true "$(command -v pspp)" "unknown"
        fi

        # JAGS
        if detect_by_command jags; then
            add_result "JAGS" true "$(command -v jags)" "unknown"
        fi

        # KNIME
        if detect_by_command knime; then
            add_result "KNIME" true "$(command -v knime)" "unknown"
        elif [[ -d "/opt/knime" ]]; then
            add_result "KNIME" true "/opt/knime/knime" "unknown"
        fi

        # Weka
        for wp in /usr/share/weka/weka.jar /usr/local/weka/weka.jar; do
            if [[ -f "$wp" ]]; then
                add_result "Weka" true "$wp" "unknown"
                break
            fi
        done

        # H2O (Python package)
        if detect_by_command python3 && python3 -c "import h2o" 2>/dev/null; then
            add_result "H2O" true "$(python3 -c 'import h2o; print(h2o.__path__[0])')" "unknown"
        fi

        # Octave
        if detect_by_command octave; then
            add_result "Octave" true "$(command -v octave)" "$(get_version_from_command octave)"
        fi
        ;;

    mac|darwin)
        # R
        if detect_by_command R; then
            add_result "R" true "$(command -v R)" "$(get_version_from_command R)"
        fi

        # Stata
        for s in stata-mp stata-se stata; do
            if detect_by_command "$s"; then
                add_result "Stata" true "$(command -v "$s")" "unknown"
                break
            fi
        done

        # Julia
        if detect_by_command julia; then
            add_result "Julia" true "$(command -v julia)" "$(get_version_from_command julia)"
        fi

        # Python
        for py in python3 python; do
            if detect_by_command "$py"; then
                add_result "Python" true "$(command -v "$py")" "$(get_version_from_command "$py")"
                break
            fi
        done

        # Gretl
        if detect_by_command gretlcli; then
            add_result "Gretl" true "$(command -v gretlcli)" "$(get_version_from_command gretlcli)"
        fi

        # Mathematica (WolframScript)
        if detect_by_command wolframscript; then
            add_result "Mathematica" true "$(command -v wolframscript)" "unknown"
        fi

        # Matlab
        if detect_by_command matlab; then
            add_result "Matlab" true "$(command -v matlab)" "unknown"
        fi

        # PSPP
        if detect_by_command pspp; then
            add_result "PSPP" true "$(command -v pspp)" "unknown"
        fi

        # JAGS
        if detect_by_command jags; then
            add_result "JAGS" true "$(command -v jags)" "unknown"
        fi

        # KNIME
        if detect_by_command knime; then
            add_result "KNIME" true "$(command -v knime)" "unknown"
        elif [[ -d "/Applications/KNIME"* ]]; then
            for app in /Applications/KNIME*; do
                [[ -d "$app" ]] && add_result "KNIME" true "$app" "unknown" && break
            done
        fi

        # Weka
        for wp in /usr/local/weka/weka.jar /Applications/weka/weka.jar; do
            if [[ -f "$wp" ]]; then
                add_result "Weka" true "$wp" "unknown"
                break
            fi
        done

        # Orange
        if python3 -c "import Orange" 2>/dev/null; then
            add_result "Orange" true "$(python3 -c 'import Orange; print(Orange.__path__[0])')" "unknown"
        fi

        # H2O
        if detect_by_command python3 && python3 -c "import h2o" 2>/dev/null; then
            add_result "H2O" true "$(python3 -c 'import h2o; print(h2o.__path__[0])')" "unknown"
        fi
        ;;

    windows|msys*|mingw*|cygwin*)
        # R
        if detect_by_command R; then
            add_result "R" true "$(command -v R)" "unknown"
        fi

        # Julia
        if detect_by_command julia; then
            add_result "Julia" true "$(command -v julia)" "unknown"
        fi

        # Python
        for py in python3 python py; do
            if detect_by_command "$py"; then
                add_result "Python" true "$(command -v "$py")" "unknown"
                break
            fi
        done

        # Gretl
        if detect_by_command gretlcli; then
            add_result "Gretl" true "$(command -v gretlcli)" "unknown"
        fi

        # WolframScript (Mathematica)
        if detect_by_command wolframscript; then
            add_result "Mathematica" true "$(command -v wolframscript)" "unknown"
        fi

        # KNIME
        if detect_by_command knime; then
            add_result "KNIME" true "$(command -v knime)" "unknown"
        fi

        # Weka
        for wp in "/c/Program Files/Weka"* "/c/Program Files (x86)/Weka"*/weka.jar; do
            if [[ -f "$wp" ]]; then
                add_result "Weka" true "$wp" "unknown"
                break
            fi
        done
        ;;
esac

json_output RESULTS
