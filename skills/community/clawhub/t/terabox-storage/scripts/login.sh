#!/bin/bash
# TeraBox Login Script
# Secure OAuth authorization login flow

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
SKIP_CONFIRM="no"
while [[ $# -gt 0 ]]; do
    case $1 in
        --yes|-y)
            SKIP_CONFIRM="yes"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --yes, -y    Skip security confirmation (for automation)"
            echo "  --help       Show help information"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if terabox is installed
if ! command -v terabox &> /dev/null; then
    # Try running from skill directory
    PROJECT_BIN="/root/.claude/skills/terabox-storage/terabox"
    if [ -x "$PROJECT_BIN" ]; then
        TERABOX_CMD="$PROJECT_BIN"
    else
        log_error "terabox is not installed"
        log_error "Please run first: bash scripts/install.sh"
        exit 1
    fi
else
    TERABOX_CMD="terabox"
fi

# Check current login status
log_info "Checking login status..."

if $TERABOX_CMD whoami 2>/dev/null | grep -q "Logged in"; then
    log_warn "Already logged in, no need to log in again"
    $TERABOX_CMD whoami
    exit 0
fi

log_info "Not logged in, starting authorization flow..."

# Security disclaimer
echo ""
echo -e "${RED}+--------------------------------------------------------------+${NC}"
echo -e "${RED}|        WARNING: terabox-storage Beta Security Notice          |${NC}"
echo -e "${RED}+--------------------------------------------------------------+${NC}"
echo -e "${RED}|${NC} 1. [Beta Stage] This tool is in beta, for technical use only. ${RED}|${NC}"
echo -e "${RED}|${NC}    Please BACK UP important cloud storage data.              ${RED}|${NC}"
echo -e "${RED}|${NC} 2. [User Responsibility] AI Agent behavior can be            ${RED}|${NC}"
echo -e "${RED}|${NC}    unpredictable. MANUALLY REVIEW all command executions      ${RED}|${NC}"
echo -e "${RED}|${NC}    and take responsibility for the outcomes.                 ${RED}|${NC}"
echo -e "${RED}|${NC} 3. [Security Warning] NEVER authorize login on shared,       ${RED}|${NC}"
echo -e "${RED}|${NC}    public, or untrusted environments to prevent data theft!  ${RED}|${NC}"
echo -e "${RED}|${NC}    After using in public environments, always run            ${RED}|${NC}"
echo -e "${RED}|${NC}    [terabox logout] to clear authorization completely.       ${RED}|${NC}"
echo -e "${RED}|${NC} 4. [No Leaks] Strictly protect config files and Tokens.      ${RED}|${NC}"
echo -e "${RED}|${NC}    NEVER expose them in public repos or conversations!       ${RED}|${NC}"
echo -e "${RED}+--------------------------------------------------------------+${NC}"
echo -e "${RED}|${NC} By using this tool, you acknowledge and accept the above.    ${RED}|${NC}"
echo -e "${RED}|${NC} Data security is everyone's responsibility.                  ${RED}|${NC}"
echo -e "${RED}+--------------------------------------------------------------+${NC}"
echo ""

# User confirmation
if [ "$SKIP_CONFIRM" = "yes" ]; then
    log_info "Auto mode, skipping security confirmation"
else
    echo -n -e "${YELLOW}I have read the security notice above. Continue login? [y/N] ${NC}"
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Login cancelled"
        exit 0
    fi
fi

# OAuth authorization URL
AUTH_URL="https://www.terabox.com/weboauth/ai?client_id=no0UBVGmwye33e-rq_VTIPf-dlMuZkYn"

# Display authorization link
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Open the following link in your browser to authorize:${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}${AUTH_URL}${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}Tips:${NC}"
echo -e "${YELLOW}1. Click the link above to open in browser${NC}"
echo -e "${YELLOW}2. The link is valid for 10 minutes${NC}"
echo -e "${YELLOW}3. After authorization, the browser will display an authorization code${NC}"
echo -e "${YELLOW}4. Copy the code and paste it below${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Prompt user to enter authorization code
echo -n "Enter the authorization code shown in your browser: "
read -r AUTH_CODE

if [ -z "$AUTH_CODE" ]; then
    log_error "Authorization code cannot be empty"
    exit 1
fi

# Validate authorization code format (alphanumeric, typically 32+ chars)
if ! echo "$AUTH_CODE" | grep -qE '^[a-zA-Z0-9_-]{10,}$'; then
    log_error "Authorization code format is invalid"
    log_error "Please make sure you copied the complete code from the browser"
    unset AUTH_CODE
    exit 1
fi

# Complete login with authorization code
log_info "Completing login with authorization code..."

# Security: pass auth code via stdin to avoid leaking in ps / /proc/PID/cmdline
if $TERABOX_CMD login --help 2>/dev/null | grep -q "code-stdin"; then
    # Secure path: pipe auth code via stdin
    echo "$AUTH_CODE" | $TERABOX_CMD login --code-stdin
else
    # Hard-fail: refuse to login with insecure --code flag
    unset AUTH_CODE
    log_error "Current terabox CLI does not support --code-stdin (secure auth code passing)"
    log_error "Auth code via --code flag is visible in ps / /proc/PID/cmdline"
    log_error "Please upgrade terabox CLI: bash scripts/install.sh --force"
    exit 1
fi

# Immediately clear auth code from memory
unset AUTH_CODE

# Verify login
if $TERABOX_CMD whoami &> /dev/null; then
    echo ""
    log_info "Login successful!"
    $TERABOX_CMD whoami
else
    log_error "Login failed, please check if the authorization code is correct"
    exit 1
fi
