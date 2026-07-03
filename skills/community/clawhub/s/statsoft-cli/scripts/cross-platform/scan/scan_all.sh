#!/usr/bin/env bash
# scan_all.sh — 跨平台批量检测已安装统计软件
# 输出 JSON 格式：{"R":{"installed":true,"path":"...","version":"..."},...}
# 支持 Linux / macOS / Windows (Git Bash / WSL)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../_platform-detect.sh" ]]; then
    source "$SCRIPT_DIR/../_platform-detect.sh"
fi

json_output() {
    local -n arr=$1
    echo "{"
    local first=true
    for key in "${!arr[@]}"; do
        if [[ "$first" == "true" ]]; then
            first=false
        else
            echo ","
        fi
        printf '  "%s": %s' "$key" "${arr[$key]}"
    done
    echo ""
    echo "}"
}

declare -A RESULTS

add_result() {
    local name=$1
    local installed=$2
    local path=${3:-null}
    local version=${4:-null}
    local os=${WB_OS:-$(uname -s | tr '[:upper:]' '[:lower:]')}
    
    if [[ "$installed" == "true" ]]; then
        RESULTS["$name"]="{\"installed\":true,\"path\":\"$path\",\"version\":\"$version\",\"platform\":\"$os\"}"
    fi
}

detect_by_command() {
    local cmd=$1
    command -v "$cmd" &>/dev/null
}

get_version_from_command() {
    local cmd=$1
    "$cmd" --version 2>&1 | head -1 | grep -oP '[\d.]+' | head -1
}

check_path_exists() {
    local path=$1
    [[ -e "$path" ]] && echo "$path" || return 1
}

# ─────────── PLATFORM-SPECIFIC DETECTION ───────────

case "${WB_OS:-$(uname -s | tr '[:upper:]' '[:lower:]')}" in
    linux)
        # R
        if detect_by_command R; then
            add_result "R" true "$(which R)" "$(get_version_from_command R)"
        fi

        # Stata
        for s in stata-mp stata-se stata; do
            if detect_by_command "$s"; then
                add_result "Stata" true "$(which "$s")" "unknown"
                break
            fi
        done

        # Julia
        if detect_by_command julia; then
            add_result "Julia" true "$(which julia)" "$(get_version_from_command julia)"
        fi

        # Python
        for py in python3 python; do
            if detect_by_command "$py"; then
                add_result "Python" true "$(which "$py")" "$(get_version_from_command "$py")"
                break
            fi
        done

        # Gretl
        if detect_by_command gretlcli; then
            add_result "Gretl" true "$(which gretlcli)" "$(get_version_from_command gretlcli)"
        fi

        # PSPP
        if detect_by_command pspp; then
            add_result "PSPP" true "$(which pspp)" "unknown"
        fi

        # JAGS
        if detect_by_command jags; then
            add_result "JAGS" true "$(which jags)" "unknown"
        fi

        # KNIME
        if detect_by_command knime; then
            add_result "KNIME" true "$(which knime)" "unknown"
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
            add_result "H2O.ai" true "$(python3 -c 'import h2o; print(h2o.__path__[0])')" "unknown"
        fi

        # Octave
        if detect_by_command octave; then
            add_result "Octave" true "$(which octave)" "$(get_version_from_command octave)"
        fi
        ;;

    mac|darwin)
        # R
        if detect_by_command R; then
            add_result "R" true "$(which R)" "$(get_version_from_command R)"
        fi

        # Stata
        for s in stata-mp stata-se stata; do
            if detect_by_command "$s"; then
                add_result "Stata" true "$(which "$s")" "unknown"
                break
            fi
        done

        # Julia
        if detect_by_command julia; then
            add_result "Julia" true "$(which julia)" "$(get_version_from_command julia)"
        fi

        # Python
        for py in python3 python; do
            if detect_by_command "$py"; then
                add_result "Python" true "$(which "$py")" "$(get_version_from_command "$py")"
                break
            fi
        done

        # Gretl
        if detect_by_command gretlcli; then
            add_result "Gretl" true "$(which gretlcli)" "$(get_version_from_command gretlcli)"
        fi

        # Mathematica (WolframScript)
        if detect_by_command wolframscript; then
            add_result "Mathematica" true "$(which wolframscript)" "unknown"
        fi

        # Matlab
        if detect_by_command matlab; then
            add_result "Matlab" true "$(which matlab)" "unknown"
        fi

        # PSPP
        if detect_by_command pspp; then
            add_result "PSPP" true "$(which pspp)" "unknown"
        fi

        # JAGS
        if detect_by_command jags; then
            add_result "JAGS" true "$(which jags)" "unknown"
        fi

        # KNIME
        if detect_by_command knime; then
            add_result "KNIME" true "$(which knime)" "unknown"
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
            add_result "H2O.ai" true "$(python3 -c 'import h2o; print(h2o.__path__[0])')" "unknown"
        fi
        ;;

    windows|msys*|mingw*|cygwin*)
        # R
        if detect_by_command R; then
            add_result "R" true "$(which R)" "unknown"
        fi

        # Julia
        if detect_by_command julia; then
            add_result "Julia" true "$(which julia)" "unknown"
        fi

        # Python
        for py in python3 python py; do
            if detect_by_command "$py"; then
                add_result "Python" true "$(which "$py")" "unknown"
                break
            fi
        done

        # Gretl
        if detect_by_command gretlcli; then
            add_result "Gretl" true "$(which gretlcli)" "unknown"
        fi

        # WolframScript (Mathematica)
        if detect_by_command wolframscript; then
            add_result "Mathematica" true "$(which wolframscript)" "unknown"
        fi

        # KNIME
        if detect_by_command knime; then
            add_result "KNIME" true "$(which knime)" "unknown"
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
