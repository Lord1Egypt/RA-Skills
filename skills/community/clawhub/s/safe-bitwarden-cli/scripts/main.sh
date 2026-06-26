#!/bin/bash

# Safe Bitwarden CLI - Pure Shell Edition (v1.5.1)
# Hardened version: Zero eval, Zero-trust piping.

set -e

PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')

# --- CLIPPER RESOLUTION (HARDENED) ---
# We store the binary and arguments separately to avoid using 'eval'.
CLIPPER_BIN=""
declare -a CLIPPER_ARGS=()

resolve_clipper() {
    if [[ "$PLATFORM" == "darwin" ]]; then
        CLIPPER_BIN=$(command -v pbcopy || true)
    elif [[ "$PLATFORM" == "linux" ]]; then
        if command -v wl-copy >/dev/null 2>&1; then
            CLIPPER_BIN=$(command -v wl-copy)
        elif command -v xclip >/dev/null 2>&1; then
            CLIPPER_BIN=$(command -v xclip)
            CLIPPER_ARGS=("-selection" "clipboard")
        fi
    elif [[ "$PLATFORM" == *"mingw"* || "$PLATFORM" == *"cygwin"* || "$PLATFORM" == *"msys"* ]]; then
        CLIPPER_BIN=$(command -v clip || true)
    elif command -v clip.exe >/dev/null 2>&1; then
        CLIPPER_BIN=$(command -v clip.exe)
    fi
}

# --- DEPENDENCY CHECK ---
handle_setup() {
    resolve_clipper
    
    BW_PATH=$(command -v bw || true)
    PYTHON_PATH=$(command -v python3 || true)

    echo "{"
    echo "  \"platform\": \"$PLATFORM\","
    echo "  \"bwInstalled\": $([ -n "$BW_PATH" ] && echo "true" || echo "false"),"
    echo "  \"clipperDetected\": $([ -n "$CLIPPER_BIN" ] && echo "true" || echo "false"),"
    echo "  \"clipperPath\": \"$CLIPPER_BIN\","
    echo "  \"pythonInstalled\": $([ -n "$PYTHON_PATH" ] && echo "true" || echo "false")"
    echo "}"
}

# --- SEARCH LOGIC (MEMORY SAFE) ---
handle_search() {
    QUERY="$1"
    if [[ -z "$QUERY" ]]; then
        echo "Error: Missing query" >&2
        exit 1
    fi

    # Retrieve and parse using Python3
    bw list items --search "$QUERY" | python3 -c '
import sys, json
try:
    data = json.load(sys.stdin)
    results = [{"id": i.get("id"), "name": i.get("name"), "username": i.get("login", {}).get("username", "N/A")} for i in data]
    print(json.dumps(results, indent=2))
except Exception:
    print(json.dumps([]))
'
}

# --- SECURE COPY (EVAL-FREE PIPE) ---
handle_copy() {
    ID="$1"
    if [[ -z "$ID" ]]; then
        echo "Error: Missing ID" >&2
        exit 1
    fi

    resolve_clipper
    if [[ -z "$CLIPPER_BIN" ]]; then
        echo "Error: No native clipper found." >&2
        exit 1
    fi

    echo "[Info] Direct kernel-pipe transmission initiated (Password)..."
    
    # SECURITY: Direct pipe between BW and Clipper.
    bw get password "$ID" | "$CLIPPER_BIN" "${CLIPPER_ARGS[@]}"

    if [[ ${PIPESTATUS[0]} -eq 0 && ${PIPESTATUS[1]} -eq 0 ]]; then
        echo "[Success] Secure copy complete. Password is in your NATIVE clipboard."
    else
        echo "[Error] Transmission failed."
        exit 1
    fi
}

# --- SECURE TOTP COPY (EVAL-FREE PIPE) ---
handle_totp() {
    ID="$1"
    if [[ -z "$ID" ]]; then
        echo "Error: Missing ID" >&2
        exit 1
    fi

    resolve_clipper
    if [[ -z "$CLIPPER_BIN" ]]; then
        echo "Error: No native clipper found." >&2
        exit 1
    fi

    echo "[Info] Direct kernel-pipe transmission initiated (TOTP)..."
    
    # SECURITY: Using same hardened pipe for TOTP codes.
    bw get totp "$ID" | "$CLIPPER_BIN" "${CLIPPER_ARGS[@]}"

    if [[ ${PIPESTATUS[0]} -eq 0 && ${PIPESTATUS[1]} -eq 0 ]]; then
        echo "[Success] TOTP copy complete. 2FA code is in your NATIVE clipboard."
    else
        echo "[Error] TOTP retrieval failed (ensure item has TOTP configured)."
        exit 1
    fi
}

# --- ROUTER ---
ACTION="$1"
PARAM="$2"

case "$ACTION" in
    setup)  handle_setup ;;
    search) handle_search "$PARAM" ;;
    copy)   handle_copy "$PARAM" ;;
    totp)   handle_totp "$PARAM" ;;
    *)      echo "Usage: $0 {setup|search|copy|totp} [param]"; exit 1 ;;
esac
