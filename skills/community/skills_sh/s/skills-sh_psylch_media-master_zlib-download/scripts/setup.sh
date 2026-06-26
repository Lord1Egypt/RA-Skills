#!/usr/bin/env bash
# setup.sh - Check and install dependencies for book-tools skill
#
# Usage:
#   bash setup.sh check          # Check all dependencies
#   bash setup.sh install-annas  # Download and install annas-mcp binary
#   bash setup.sh install-deps   # Install Python dependencies (requests)

set -euo pipefail

ANNAS_VERSION="v0.0.4"
INSTALL_DIR="$HOME/.local/bin"

check_python() {
    if command -v python3 &>/dev/null; then
        echo "PYTHON=ok"
        echo "PYTHON_PATH=$(command -v python3)"
    else
        echo "PYTHON=missing"
    fi
}

check_requests() {
    if python3 -c "import requests" 2>/dev/null; then
        echo "REQUESTS=ok"
    else
        echo "REQUESTS=missing"
    fi
}

check_annas() {
    local binary=""
    # Check PATH
    if command -v annas-mcp &>/dev/null; then
        binary="$(command -v annas-mcp)"
    elif [ -f "$INSTALL_DIR/annas-mcp" ]; then
        binary="$INSTALL_DIR/annas-mcp"
    elif [ -f "/usr/local/bin/annas-mcp" ]; then
        binary="/usr/local/bin/annas-mcp"
    fi

    if [ -n "$binary" ]; then
        echo "ANNAS_BINARY=ok"
        echo "ANNAS_PATH=$binary"
    else
        echo "ANNAS_BINARY=missing"
    fi
}

do_check() {
    check_python
    check_requests
    check_annas
}

do_install_deps() {
    echo "Installing Python requests..."
    python3 -m pip install --user requests
    echo "INSTALL_DEPS=ok"
}

do_install_annas() {
    local arch
    arch="$(uname -m)"
    local os_name
    os_name="$(uname -s | tr '[:upper:]' '[:lower:]')"

    # Map arch
    case "$arch" in
        x86_64|amd64) arch="amd64" ;;
        arm64|aarch64) arch="arm64" ;;
        *) echo "ERROR: Unsupported architecture: $arch"; exit 1 ;;
    esac

    # Release filenames use version without 'v' prefix
    local ver_no_v="${ANNAS_VERSION#v}"
    local filename="annas-mcp_${ver_no_v}_${os_name}_${arch}.tar.xz"
    if [ "$os_name" = "windows" ]; then
        filename="annas-mcp_${ver_no_v}_${os_name}_${arch}.zip"
    fi
    local url="https://github.com/iosifache/annas-mcp/releases/download/${ANNAS_VERSION}/${filename}"

    echo "Downloading $url ..."
    mkdir -p "$INSTALL_DIR"

    local tmpdir
    tmpdir="$(mktemp -d)"
    trap 'rm -rf "${tmpdir:-}"' EXIT

    curl -fsSL "$url" -o "$tmpdir/$filename"
    tar -xJf "$tmpdir/$filename" -C "$tmpdir"

    # Find the binary in extracted files
    local binary
    binary="$(find "$tmpdir" -name 'annas-mcp' -type f | head -1)"
    if [ -z "$binary" ]; then
        echo "ERROR: annas-mcp binary not found in archive"
        exit 1
    fi

    cp "$binary" "$INSTALL_DIR/annas-mcp"
    chmod +x "$INSTALL_DIR/annas-mcp"

    echo "INSTALL_ANNAS=ok"
    echo "ANNAS_PATH=$INSTALL_DIR/annas-mcp"
    echo "Installed annas-mcp ${ANNAS_VERSION} to $INSTALL_DIR/annas-mcp"

    # Remind about PATH
    if ! echo "$PATH" | tr ':' '\n' | grep -q "$INSTALL_DIR"; then
        echo "NOTE: Add $INSTALL_DIR to your PATH if not already there"
    fi
}

case "${1:-check}" in
    check)        do_check ;;
    install-deps) do_install_deps ;;
    install-annas) do_install_annas ;;
    *)
        echo "Usage: setup.sh [check|install-deps|install-annas]"
        exit 1
        ;;
esac
