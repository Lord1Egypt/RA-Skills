#!/bin/bash
#
# Web Reader Pro - Scrapling Dependency Auto-Installer
#
# This script installs the Scrapling tool required for Tier 2 extraction.
# Scrapling is a Node.js-based web scraping tool.
#
# Usage:
#   ./scripts/install_scrapling.sh [--check-only] [--reinstall]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/bin"
SCRAPLING_VERSION="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
CHECK_ONLY=false
REINSTALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --check-only)
            CHECK_ONLY=true
            shift
            ;;
        --reinstall)
            REINSTALL=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--check-only] [--reinstall]"
            echo ""
            echo "Options:"
            echo "  --check-only   Only check if scrapling is installed"
            echo "  --reinstall    Force reinstall even if already installed"
            echo "  --help, -h     Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

check_node_installed() {
    log_info "Checking Node.js installation..."
    
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_success "Node.js is installed: $NODE_VERSION"
        return 0
    else
        log_error "Node.js is not installed."
        echo ""
        echo "Please install Node.js first:"
        echo "  - macOS:    brew install node"
        echo "  - Ubuntu:   sudo apt install nodejs npm"
        echo "  - Windows:  Download from https://nodejs.org/"
        echo "  - Or visit: https://nodejs.org/ for installer"
        return 1
    fi
}

check_npm_installed() {
    log_info "Checking npm installation..."
    
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        log_success "npm is installed: v$NPM_VERSION"
        return 0
    else
        log_error "npm is not installed."
        return 1
    fi
}

check_scrapling_installed() {
    if command -v scrapling &> /dev/null; then
        SCRAPLING_VERSION=$(scrapling --version 2>/dev/null || echo "unknown")
        log_success "Scrapling is installed: $SCRAPLING_VERSION"
        return 0
    else
        log_warning "Scrapling is not installed."
        return 1
    fi
}

install_scrapling() {
    log_info "Installing Scrapling..."
    
    # Try global npm install first
    if command -v npm &> /dev/null; then
        log_info "Installing via npm (global)..."
        
        if npm install -g @scrapinghub/scrapling 2>/dev/null; then
            log_success "Scrapling installed successfully via npm!"
        elif npm install -g scrapling 2>/dev/null; then
            log_success "Scrapling installed successfully via npm!"
        else
            # Try alternative package name
            log_info "Trying alternative package..."
            npm install -g @scrapinghub/scrapling --force 2>/dev/null || \
            npm install -g scrapling --force 2>/dev/null || true
        fi
        
        # Verify installation
        if command -v scrapling &> /dev/null; then
            log_success "Scrapling is now available!"
            return 0
        fi
    fi
    
    # Try npx approach as fallback
    log_info "Trying npx as alternative..."
    
    if npx --yes scrapling --version &> /dev/null; then
        log_success "Scrapling available via npx"
        # Create a wrapper script
        create_scrapling_wrapper
        return 0
    fi
    
    log_error "Failed to install Scrapling via npm/npx"
    return 1
}

create_scrapling_wrapper() {
    log_info "Creating scrapling wrapper script..."
    
    WRAPPER_PATH="${INSTALL_DIR}/scrapling"
    
    mkdir -p "${INSTALL_DIR}"
    
    cat > "${WRAPPER_PATH}" << 'WRAPPER_EOF'
#!/bin/bash
# Scrapling wrapper script - calls npx scrapling
exec npx --yes scrapling "$@"
WRAPPER_EOF
    
    chmod +x "${WRAPPER_PATH}"
    log_success "Wrapper created at: ${WRAPPER_PATH}"
    
    # Add to PATH if needed
    if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
        log_warning "${INSTALL_DIR} is not in your PATH."
        echo ""
        echo "Add this to your ~/.bashrc or ~/.zshrc:"
        echo "  export PATH=\"${INSTALL_DIR}:\$PATH\""
    fi
}

verify_installation() {
    log_info "Verifying installation..."
    
    if command -v scrapling &> /dev/null; then
        SCRAPLING_VERSION=$(scrapling --version 2>&1 || echo "v0.x.x")
        log_success "✓ Scrapling installed: $SCRAPLING_VERSION"
        
        # Test basic functionality
        log_info "Testing scrapling availability..."
        if scrapling --help &> /dev/null; then
            log_success "✓ Scrapling is functional"
            return 0
        fi
    fi
    
    log_warning "Scrapling command not found in PATH"
    
    # Check if npx can run it
    if npx --yes scrapling --version &> /dev/null; then
        log_info "Scrapling works via npx"
        log_success "You can use web-reader-pro with npx fallback"
        return 0
    fi
    
    return 1
}

print_installation_guide() {
    echo ""
    echo "=========================================="
    echo "       Installation Guide Summary"
    echo "=========================================="
    echo ""
    echo "For Tier 2 (Scrapling) extraction, you need:"
    echo ""
    echo "1. Node.js (>=14 recommended)"
    echo "   Install: https://nodejs.org/"
    echo ""
    echo "2. npm (comes with Node.js)"
    echo ""
    echo "3. Scrapling package"
    echo "   Install: npm install -g @scrapinghub/scrapling"
    echo ""
    echo "Alternative: Use Tier 1 (Jina) or Tier 3 (WebFetch)"
    echo ""
    echo "For help, visit:"
    echo "  https://github.com/0xcjl/web-reader-pro"
    echo ""
}

# Main execution
main() {
    echo ""
    echo "=========================================="
    echo "   Web Reader Pro - Scrapling Installer"
    echo "=========================================="
    echo ""
    
    # Check Node.js
    if ! check_node_installed; then
        print_installation_guide
        exit 1
    fi
    
    # Check npm
    if ! check_npm_installed; then
        log_error "npm is required but not installed"
        print_installation_guide
        exit 1
    fi
    
    # Check if already installed
    if check_scrapling_installed; then
        if [ "$REINSTALL" = true ]; then
            log_info "Reinstalling..."
        else
            log_success "Scrapling is already installed!"
            log_info "Use --reinstall to force reinstall"
            exit 0
        fi
    fi
    
    # Exit if check-only mode
    if [ "$CHECK_ONLY" = true ]; then
        exit 1
    fi
    
    # Install
    if install_scrapling; then
        verify_installation
        log_success "Installation complete!"
    else
        log_error "Installation failed"
        print_installation_guide
        exit 1
    fi
}

main
