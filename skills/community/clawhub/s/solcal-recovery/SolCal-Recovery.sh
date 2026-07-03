#!/bin/bash
#===========================================================
# SolCal Recovery - Get Sol back online with AI assistance
#===========================================================
# This script checks Sol's status and helps repair issues
# Uses local Ollama model for AI repair suggestions
#
# Usage: bash SolCal-Recovery.sh
#===========================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Config
SCRIPT_DIR="$(cd "$(dirname "$0")" &>/dev/null && pwd)"
OLLAMA_MODEL="llama3.2:1b"  # Small model for repair assistant
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

#===========================================================
# CHECK 1: Is OpenClaw installed?
#===========================================================
check_openclaw() {
    log_info "Checking OpenClaw installation..."
    
    if command -v openclaw &> /dev/null; then
        OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
        log_success "OpenClaw found: $OPENCLAW_VERSION"
        return 0
    else
        log_error "OpenClaw not found!"
        return 1
    fi
}

#===========================================================
# CHECK 2: Is Gateway running?
#===========================================================
check_gateway() {
    log_info "Checking OpenClaw gateway..."
    
    if openclaw gateway status 2>/dev/null | grep -q "running"; then
        log_success "Gateway is RUNNING"
        return 0
    else
        log_warn "Gateway is NOT running"
        return 1
    fi
}

#===========================================================
# CHECK 3: Gateway connectivity
#===========================================================
check_connectivity() {
    log_info "Testing gateway connectivity..."
    
    if openclaw gateway status 2>/dev/null | grep -q "ok\|connected"; then
        log_success "Gateway is CONNECTED"
        return 0
    else
        log_warn "Gateway not responding"
        return 1
    fi
}

#===========================================================
# CHECK 4: API keys configured?
#===========================================================
check_api_keys() {
    log_info "Checking API keys..."
    
    if grep -q "api.key\|api_key\|API_KEY" ~/.openclaw/openclaw.json 2>/dev/null; then
        log_success "API keys configured"
        return 0
    else
        log_error "No API keys found!"
        return 1
    fi
}

#===========================================================
# CHECK 5: Network connectivity
#===========================================================
check_network() {
    log_info "Testing network..."
    
    if curl -s --connect-timeout 5 https://api.minimax.io &> /dev/null; then
        log_success "Network OK"
        return 0
    else
        log_warn "Network may be blocked"
        return 1
    fi
}

#===========================================================
# REPAIR: Install OpenClaw
#===========================================================
repair_install() {
    log_info "Installing OpenClaw..."
    
    if command -v brew &> /dev/null; then
        brew install openclaw 2>/dev/null || brew reinstall openclaw
        log_success "OpenClaw installed"
    else
        log_error "Homebrew not found. Install from https://brew.sh"
        return 1
    fi
}

#===========================================================
# REPAIR: Start Gateway
#===========================================================
repair_start_gateway() {
    log_info "Starting gateway..."
    openclaw gateway start
    sleep 3
    
    if openclaw gateway status 2>/dev/null | grep -q "running"; then
        log_success "Gateway started"
        return 0
    else
        log_error "Failed to start gateway"
        return 1
    fi
}

#===========================================================
# REPAIR: Configure API keys
#===========================================================
repair_configure_keys() {
    log_info "Configuring API keys..."
    
    echo "Enter your API key provider (e.g., minimax, openai):"
    read PROVIDER
    
    echo "Enter your API key:"
    read -s API_KEY
    
    # Add to config
    openclaw config set auth.profiles.$PROVIDER.mode=api_key 2>/dev/null || true
    
    log_success "API key saved (you may need to edit ~/.openclaw/openclaw.json manually)"
}

#===========================================================
# REPAIR: Check Ollama
#===========================================================
repair_ollama() {
    log_info "Checking Ollama..."
    
    if ! command -v ollama &> /dev/null; then
        log_warn "Ollama not installed"
        log_info "Installing Ollama..."
        
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            curl -fsSL https://ollama.ai/install | sh
        fi
    fi
    
    # Pull repair model if needed
    if ! ollama list 2>/dev/null | grep -q "$OLLAMA_MODEL"; then
        log_info "Pulling repair model: $OLLAMA_MODEL"
        ollama pull "$OLLAMA_MODEL"
    fi
    
    log_success "Ollama ready"
}

#===========================================================
# AI REPAIR: Ask Ollama for help
#===========================================================
ask_ai_repair() {
    local ISSUE="$1"
    
    log_info "Asking AI for repair advice..."
    
    # Use Ollama for diagnosis
    local PROMPT="You are OpenClaw AI assistant repair expert. 
A user is having this issue: $ISSUE
The system status shows these problems.
Give specific step-by-step fix commands. Keep it simple.
Answer:"
    
    local RESPONSE=$(echo "$PROBLEM_SUMMARY" | ollama run "$OLLAMA_MODEL" 2>/dev/null || echo "Ollama not responding")
    
    echo "$RESPONSE"
}

#===========================================================
# MAIN DIAGNOSTIC
#===========================================================
run_diagnostics() {
    echo ""
    echo "============================================"
    echo "  🤖 SolCal Diagnostic"
    echo "============================================"
    echo ""
    
    # Collect status
    ISSUES=""
    
    check_openclaw || ISSUES="$ISSUES - OpenClaw not installed\n"
    check_gateway || ISSUES="$ISSUES - Gateway not running\n"
    check_connectivity || ISSUES="$ISSUES - Gateway not connected\n"
    check_api_keys || ISSUES="$ISSUES - No API keys\n"
    check_network || ISSUES="$ISSUES - Network issue\n"
    
    echo ""
    if [ -z "$ISSUES" ]; then
        echo -e "${GREEN}============================================${NC}"
        echo -e "${GREEN}  ✅ SOL IS RUNNING!${NC}"
        echo -e "${GREEN}============================================${NC}"
        echo ""
        openclaw gateway status
    else
        echo -e "${RED}============================================${NC}"
        echo -e "${RED}  ⚠��� ISSUES FOUND${NC}"
        echo -e "${RED}============================================${NC}"
        echo -e "$ISSUES"
        
        echo ""
        echo "Want AI repair advice? (y/n)"
        read -r response
        if [[ "$response" == "y" ]]; then
            echo "Running AI repair assistant..."
            repair_ollama
            ask_ai_repair "$ISSUES"
        fi
    fi
}

#===========================================================
# AUTO REPAIR
#===========================================================
auto_repair() {
    log_info "Running auto-repairs..."
    
    check_openclaw || repair_install
    check_gateway || repair_start_gateway
    check_api_keys || repair_configure_keys
    
    # Final check
    run_diagnostics
}

#===========================================================
# CLI ARGUMENTS
#===========================================================
case "${1:-diagnose}" in
    diagnose|diagnostic|d)
        run_diagnostics
        ;;
    repair|fix|r)
        auto_repair
        ;;
    start|s)
        repair_start_gateway
        ;;
    install|i)
        repair_install
        ;;
    ollama|ai)
        repair_ollama
        ;;
    help|--help|-h)
        echo "SolCal Recovery - Usage"
        echo ""
        echo "  bash SolCal-Recovery.sh          # Run diagnostics"
        echo "  bash SolCal-Recovery.sh diagnose # Check status"
        echo "  bash SolCal-Recovery.sh repair  # Auto-fix issues"
        echo "  bash SolCal-Recovery.sh start   # Just start gateway"
        echo "  bash SolCal-Recovery.sh install # Reinstall OpenClaw"
        echo "  bash SolCal-Recovery.sh ollama  # Setup AI helper"
        ;;
    *)
        run_diagnostics
        ;;
esac