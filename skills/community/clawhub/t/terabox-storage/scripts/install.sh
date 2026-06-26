#!/bin/bash
# TeraBox CLI Installation Script
# Download and install terabox CLI from CDN

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
VERSION="1.1.0"
CDN_BASE="https://s5.teraboxcdn.com/ai-terabox/terabox-cli/${VERSION}"
INSTALL_DIR="$HOME/.local/bin"
TERABOX_BIN="$INSTALL_DIR/terabox"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS and architecture, return the CDN download URL
get_download_url() {
    local os arch

    case "$(uname -s)" in
        Linux*)  os="linux" ;;
        Darwin*) os="darwin" ;;
        MINGW*|MSYS*|CYGWIN*) os="windows" ;;
        *)
            log_error "Unsupported OS: $(uname -s)"
            exit 1
            ;;
    esac

    case "$(uname -m)" in
        x86_64|amd64)  arch="amd64" ;;
        aarch64|arm64) arch="arm64" ;;
        *)
            log_error "Unsupported architecture: $(uname -m)"
            exit 1
            ;;
    esac

    if [ "$os" = "windows" ]; then
        echo "${CDN_BASE}/terabox-${VERSION}-${os}-amd64.zip"
    else
        echo "${CDN_BASE}/terabox-${VERSION}-${os}-${arch}.tar.gz"
    fi
}

# Main function
main() {
    local force="no"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --yes|-y|--force|-f)
                force="yes"
                shift
                ;;
            --version|-v)
                echo "terabox install script v${VERSION}"
                exit 0
                ;;
            --help|-h)
                echo "Usage: $0 [options]"
                echo ""
                echo "Options:"
                echo "  --yes, -y, --force, -f    Force reinstall"
                echo "  --version                  Show version"
                echo "  --help                     Show help"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for help"
                exit 1
                ;;
        esac
    done

    # Check if already installed
    if command -v terabox &> /dev/null; then
        local installed_version=$(terabox --version 2>/dev/null | head -1 || echo "unknown")
        log_warn "terabox CLI already installed (version: ${installed_version})"
        if [ "$force" = "yes" ]; then
            log_info "Force reinstalling..."
        else
            read -p "Reinstall? [y/N] " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log_info "Installation cancelled"
                exit 0
            fi
        fi
    fi

    # Determine download URL
    local download_url
    download_url="$(get_download_url)"
    log_info "Detected platform: $(uname -s) $(uname -m)"
    log_info "Download URL: ${download_url}"

    # Create install directory
    mkdir -p "$INSTALL_DIR"

    # Download to a temporary directory
    local tmp_dir
    tmp_dir=$(mktemp -d)
    trap "rm -rf '$tmp_dir'" EXIT

    local filename
    filename=$(basename "$download_url")
    local tmp_file="${tmp_dir}/${filename}"

    log_info "Downloading terabox CLI v${VERSION}..."
    if command -v curl &> /dev/null; then
        curl -fSL --progress-bar -o "$tmp_file" "$download_url"
    elif command -v wget &> /dev/null; then
        wget -q --show-progress -O "$tmp_file" "$download_url"
    else
        log_error "Neither curl nor wget found. Please install one of them."
        exit 1
    fi

    # Extract archive
    log_info "Extracting..."
    if [[ "$filename" == *.tar.gz ]]; then
        tar -xzf "$tmp_file" -C "$tmp_dir"
    elif [[ "$filename" == *.zip ]]; then
        if command -v unzip &> /dev/null; then
            unzip -q "$tmp_file" -d "$tmp_dir"
        else
            log_error "unzip not found. Please install unzip."
            exit 1
        fi
    fi

    # Find the terabox binary in extracted files
    local extracted_bin
    extracted_bin=$(find "$tmp_dir" -name "terabox" -type f ! -name "*.tar.gz" ! -name "*.zip" | head -1)
    if [ -z "$extracted_bin" ]; then
        # On Windows, look for .exe
        extracted_bin=$(find "$tmp_dir" -name "terabox.exe" -type f | head -1)
    fi

    if [ -z "$extracted_bin" ]; then
        log_error "Could not find terabox binary in the downloaded archive"
        exit 1
    fi

    # Install binary
    cp "$extracted_bin" "$TERABOX_BIN"
    chmod +x "$TERABOX_BIN"

    # Verify installation
    log_info "Verifying installation..."
    if [ -x "$TERABOX_BIN" ]; then
        # Check PATH
        if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
            log_warn "Please add ~/.local/bin to your PATH:"
            echo ""
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            log_info "Then run: source ~/.bashrc"
        fi

        local installed_version=$("$TERABOX_BIN" --version 2>/dev/null | head -1 || echo "unknown")
        log_info "terabox CLI installed successfully! (version: ${installed_version})"
        echo ""

        # Security disclaimer
        echo -e "${RED}┌──────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${RED}│          ⚠️  terabox-storage Beta Security Notice            │${NC}"
        echo -e "${RED}├──────────────────────────────────────────────────────────────┤${NC}"
        echo -e "${RED}│${NC} 1. [BETA] This tool is in beta, for technical exchange only. ${RED}│${NC}"
        echo -e "${RED}│${NC}    Please BACKUP your important cloud data.                  ${RED}│${NC}"
        echo -e "${RED}│${NC} 2. [RESPONSIBILITY] AI Agent behavior is unpredictable.      ${RED}│${NC}"
        echo -e "${RED}│${NC}    Please REVIEW command execution in real-time.             ${RED}│${NC}"
        echo -e "${RED}│${NC} 3. [SECURITY] NEVER authorize login in untrusted             ${RED}│${NC}"
        echo -e "${RED}│${NC}    environments to prevent data theft!                       ${RED}│${NC}"
        echo -e "${RED}│${NC}    After use in public environments, run:                    ${RED}│${NC}"
        echo -e "${RED}│${NC}    【terabox logout】 to clear authorization.                ${RED}│${NC}"
        echo -e "${RED}│${NC} 4. [CONFIDENTIAL] Protect config files and tokens.           ${RED}│${NC}"
        echo -e "${RED}│${NC}    NEVER expose in public repos or conversations!            ${RED}│${NC}"
        echo -e "${RED}├──────────────────────────────────────────────────────────────┤${NC}"
        echo -e "${RED}│${NC} Using this tool means you accept the above terms.            ${RED}│${NC}"
        echo -e "${RED}└──────────────────────────────────────────────────────────────┘${NC}"
        echo ""

        echo "Quick Start:"
        echo "  1. Login: bash $(dirname $0)/login.sh"
        echo "  2. Help:  terabox --help"
        echo ""
    else
        log_error "Installation failed"
        exit 1
    fi
}

# Execute main function
main "$@"
