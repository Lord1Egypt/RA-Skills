#!/usr/bin/env bash
# platform-detect.sh - Cross-platform OS detection for WorkBuddy
# Usage: source platform-detect.sh
# Sets: WB_OS (windows|mac|linux), WB_ARCH (x64|arm64)

detect_platform() {
    local uname_out
    uname_out="$(uname -s)"

    case "$uname_out" in
        Linux*)
            WB_OS="linux"
            ;;
        Darwin*)
            WB_OS="mac"
            ;;
        MINGW*|MSYS*|CYGWIN*|Windows*)
            WB_OS="windows"
            ;;
        *)
            # Fallback: check for Windows-specific env vars
            if [ -n "$WINDIR" ] || [ -n "$OS" ]; then
                WB_OS="windows"
            else
                WB_OS="linux"  # Default fallback
            fi
            ;;
    esac

    # Detect architecture
    local arch
    arch="$(uname -m)"
    case "$arch" in
        x86_64|amd64)
            WB_ARCH="x64"
            ;;
        arm64|aarch64)
            WB_ARCH="arm64"
            ;;
        *)
            WB_ARCH="x64"
            ;;
    esac

    export WB_OS
    export WB_ARCH
}

# Get default R paths per platform
get_r_default_path() {
    case "$WB_OS" in
        windows)
            echo "C:/Program Files/R/"
            ;;
        mac)
            echo "/Library/Frameworks/R.framework/Resources/"
            ;;
        linux)
            echo "/usr/lib/R/"
            ;;
    esac
}

# Get default Stata paths per platform
get_stata_default_path() {
    case "$WB_OS" in
        windows)
            echo "C:/Program Files/Stata18"
            ;;
        mac)
            echo "/Applications/Stata"
            ;;
        linux)
            echo "/usr/local/stata18"
            ;;
    esac
}

# Get default SAS paths per platform
get_sas_default_path() {
    case "$WB_OS" in
        windows)
            echo "C:/Program Files/SASFoundation/9.4"
            ;;
        mac)
            echo "/Applications/SASFoundation/9.4"
            ;;
        linux)
            echo "/opt/SASFoundation/9.4/sas"
            ;;
    esac
}

# Auto-detect
detect_platform
