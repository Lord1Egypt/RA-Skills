#!/bin/bash
# Environment setup script for weekly-report skill
# Supports: macOS, Ubuntu/Debian, and other Linux distributions
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IN_CHINA=false
PYTHON_CMD=""
UV_JUST_INSTALLED=false

# Print colored message
print_info() { echo -e "${CYAN}$1${NC}"; }
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Darwin*)  echo "macos" ;;
        Linux*)   echo "linux" ;;
        *)        echo "unknown" ;;
    esac
}

# Check if running in China (Google unreachable)
check_network() {
    print_info "Checking network connectivity..."

    if curl -s --connect-timeout 5 https://www.google.com > /dev/null 2>&1; then
        IN_CHINA=false
        print_success "Global network accessible"
    else
        IN_CHINA=true
        print_warning "Cannot reach Google, will use China mirrors"
    fi
}

# Check Python 3.10+
check_python() {
    print_info "Checking Python installation..."

    # Try python3 first, then python
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python not found!"
        echo ""
        echo "Please install Python 3.10 or higher:"
        echo "  macOS:   brew install python@3.11"
        echo "  Ubuntu:  sudo apt install python3 python3-pip python3-venv"
        echo "  Or download from: https://www.python.org/downloads/"
        exit 1
    fi

    # Check version
    VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    MAJOR=$(echo "$VERSION" | cut -d. -f1)
    MINOR=$(echo "$VERSION" | cut -d. -f2)

    if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]; }; then
        print_error "Python version $VERSION is too old. Need 3.10+"
        exit 1
    fi

    print_success "Found Python $VERSION ($PYTHON_CMD)"
}

# Check and install uv
check_uv() {
    print_info "Checking uv package manager..."

    # Ensure ~/.local/bin is in PATH (uv's default install location)
    export PATH="$HOME/.local/bin:$PATH"

    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version 2>&1 | head -1)
        print_success "uv is installed: $UV_VERSION"
        return 0
    fi

    print_warning "uv not found. Installing..."

    # Install uv
    if [ "$IN_CHINA" = true ]; then
        print_info "Installing uv (may use alternative sources)..."
    fi

    # Use official installer (works in most cases)
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Source shell profile if it exists (uv installer adds to profile)
    if [ -f "$HOME/.bashrc" ]; then
        source "$HOME/.bashrc" 2>/dev/null || true
    fi
    if [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc" 2>/dev/null || true
    fi

    # Ensure PATH is updated for current session
    export PATH="$HOME/.local/bin:$PATH"

    # Verify installation
    if command -v uv &> /dev/null; then
        print_success "uv installed successfully: $(uv --version)"
        UV_JUST_INSTALLED=true
    else
        print_error "Failed to install uv"
        echo "Please install manually: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."

    cd "$SCRIPT_DIR"

    if [ "$IN_CHINA" = true ]; then
        print_info "Using China PyPI mirror..."
        uv sync --index-url https://mirrors.aliyun.com/pypi/simple
    else
        uv sync
    fi

    print_success "Python dependencies installed"
}

# Check if Playwright Chromium is installed
check_playwright_chromium() {
    # Check common cache locations
    local CACHE_DIRS=(
        "$HOME/.cache/ms-playwright"
        "$HOME/Library/Caches/ms-playwright"
        "$HOME/.local/share/ms-playwright"
    )

    for dir in "${CACHE_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            # Check for chromium directory
            if ls "$dir"/chromium-* 1> /dev/null 2>&1; then
                return 0
            fi
        fi
    done

    return 1
}

# Install Playwright browsers
install_playwright() {
    print_info "Checking Playwright Chromium..."

    if check_playwright_chromium; then
        print_success "Playwright Chromium already installed"
        return 0
    fi

    print_warning "Playwright Chromium not found. Installing..."

    cd "$SCRIPT_DIR"
    uv run playwright install chromium

    print_success "Playwright Chromium installed"
}

# Install Playwright system dependencies (Linux only)
install_system_deps() {
    local OS=$(detect_os)

    if [ "$OS" = "linux" ]; then
        print_info "Installing Playwright system dependencies..."

        cd "$SCRIPT_DIR"

        # Check if we have sudo access
        if sudo -n true 2>/dev/null; then
            uv run playwright install-deps chromium
            print_success "System dependencies installed"
        else
            print_warning "sudo access required for system dependencies"
            echo "Run manually: uv run playwright install-deps chromium"
            echo "Or with sudo: sudo uv run playwright install-deps chromium"
        fi
    else
        print_info "Skipping system dependencies (not needed on $OS)"
    fi
}

# Print summary
print_summary() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Setup Complete!${NC}"
    echo -e "${CYAN}════════════════════════════════════════${NC}"
    echo ""
    echo "Environment is ready. You can now:"
    echo ""
    echo "  1. Configure environment variables:"
    echo "     export WEEKLY_REPORT_USERNAME=\"your_username\""
    echo "     export WEEKLY_REPORT_PASSWORD=\"your_password\""
    echo "     export DEEPSEEK_API_KEY=\"your_api_key\""
    echo ""
    echo "  2. Generate weekly report:"
    echo "     cd $SCRIPT_DIR"
    echo "     uv run python generate.py --week today"
    echo ""
    if [ "$UV_JUST_INSTALLED" = true ]; then
        echo -e "${YELLOW}Note: uv was just installed. Run 'source ~/.profile' or start a new terminal${NC}"
        echo ""
    fi
}

# Main function
main() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║       Weekly Report Skill - Environment Setup                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""

    local OS=$(detect_os)

    if [ "$OS" = "unknown" ]; then
        print_error "Unsupported operating system: $(uname -s)"
        exit 1
    fi

    print_info "Detected OS: $OS"
    echo ""

    # Run setup steps
    check_network
    echo ""
    check_python
    echo ""
    check_uv
    echo ""
    install_python_deps
    echo ""
    install_playwright
    echo ""
    install_system_deps
    echo ""

    print_summary
}

# Run main
main "$@"
