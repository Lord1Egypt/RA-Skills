#!/usr/bin/env bash
#
# Telnyx Embeddings - Setup Script
#
# Validates requirements and optionally sets up a bucket for embeddings.
#
# Usage:
#   ./setup.sh              # Full setup
#   ./setup.sh --check      # Validation only (no changes)
#   ./setup.sh --help       # Show help
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}i${NC} $1"; }
log_ok()   { echo -e "${GREEN}+${NC} $1"; }
log_warn() { echo -e "${YELLOW}!${NC} $1"; }
log_err()  { echo -e "${RED}x${NC} $1"; }

# Track results
CHECKS_PASSED=0
CHECKS_FAILED=0
SETUP_ERRORS=()

check_python() {
    log_info "Checking Python installation..."

    if ! command -v python3 &> /dev/null; then
        log_err "Python 3 is required but not installed"
        SETUP_ERRORS+=("Python 3 not found")
        ((++CHECKS_FAILED))
        return 1
    fi

    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        log_ok "Python $python_version found"
        ((++CHECKS_PASSED))
    else
        log_err "Python 3.8+ required, found $python_version"
        SETUP_ERRORS+=("Python version too old: $python_version")
        ((++CHECKS_FAILED))
        return 1
    fi
}

check_syntax() {
    log_info "Validating script syntax..."

    local all_ok=true

    # Check Python files
    for py_file in "$SCRIPT_DIR"/*.py; do
        if [[ -f "$py_file" ]]; then
            if python3 -c "import py_compile; py_compile.compile('$py_file', doraise=True)" 2>/dev/null; then
                log_ok "$(basename "$py_file") syntax OK"
            else
                log_err "$(basename "$py_file") has syntax errors"
                SETUP_ERRORS+=("Syntax error in $(basename "$py_file")")
                all_ok=false
            fi
        fi
    done

    # Check bash files
    for sh_file in "$SCRIPT_DIR"/*.sh; do
        if [[ -f "$sh_file" ]]; then
            if bash -n "$sh_file" 2>/dev/null; then
                log_ok "$(basename "$sh_file") syntax OK"
            else
                log_err "$(basename "$sh_file") has syntax errors"
                SETUP_ERRORS+=("Syntax error in $(basename "$sh_file")")
                all_ok=false
            fi
        fi
    done

    if $all_ok; then
        ((++CHECKS_PASSED))
    else
        ((++CHECKS_FAILED))
        return 1
    fi
}

check_credentials() {
    log_info "Checking Telnyx API credentials..."

    # Check for API key
    if [[ -n "${TELNYX_API_KEY:-}" ]]; then
        log_ok "TELNYX_API_KEY found in environment"
    elif [[ -f "$SCRIPT_DIR/.env" ]]; then
        log_ok ".env file found"
        set -a
        source "$SCRIPT_DIR/.env"
        set +a
    else
        log_err "No Telnyx API key found"
        echo ""
        echo "   Set your API key using one of these methods:"
        echo ""
        echo "   Option 1: Environment variable"
        echo "     export TELNYX_API_KEY=\"KEY....\""
        echo ""
        echo "   Option 2: Create .env file"
        echo "     echo 'TELNYX_API_KEY=KEY....' > $SCRIPT_DIR/.env"
        echo ""
        echo "   Get your API key at: https://portal.telnyx.com/#/app/api-keys"
        echo ""
        SETUP_ERRORS+=("No API key found")
        ((++CHECKS_FAILED))
        return 1
    fi

    # Test API key validity
    if [[ -n "${TELNYX_API_KEY:-}" ]]; then
        log_info "Testing API key validity..."

        local response
        response=$(curl -s -w "%{http_code}" -o /dev/null \
            -H "Authorization: Bearer $TELNYX_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.telnyx.com/v2/ai/embeddings/similarity-search" \
            -d '{"bucket_name":"test-nonexistent-embeddings","query":"test","num_docs":1}' \
            2>/dev/null || echo "000")

        # We expect 404 (bucket not found) = API key works
        # 401/403 = bad/expired key
        if [[ "$response" =~ ^[2-4][0-9][0-9]$ ]]; then
            log_ok "API key is valid"
            ((++CHECKS_PASSED))
        else
            log_err "API key test failed (HTTP $response)"
            SETUP_ERRORS+=("Invalid or expired API key")
            ((++CHECKS_FAILED))
            return 1
        fi
    else
        log_warn "Could not load API key for testing"
        ((++CHECKS_FAILED))
        return 1
    fi
}

check_config() {
    log_info "Validating configuration..."

    if [[ ! -f "$SCRIPT_DIR/config.json" ]]; then
        log_err "config.json not found"
        SETUP_ERRORS+=("Missing config.json")
        ((++CHECKS_FAILED))
        return 1
    fi

    if python3 -c "import json; json.load(open('$SCRIPT_DIR/config.json'))" 2>/dev/null; then
        log_ok "config.json is valid JSON"
        ((++CHECKS_PASSED))
    else
        log_err "config.json has invalid JSON syntax"
        SETUP_ERRORS+=("Invalid config.json syntax")
        ((++CHECKS_FAILED))
        return 1
    fi
}

make_executable() {
    log_info "Making scripts executable..."

    if chmod +x "$SCRIPT_DIR"/*.py "$SCRIPT_DIR"/*.sh 2>/dev/null; then
        log_ok "Scripts marked executable"
        ((++CHECKS_PASSED))
    else
        log_warn "Could not make all scripts executable"
    fi
}

create_bucket_if_needed() {
    log_info "Checking bucket..."

    local bucket
    bucket=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/config.json')).get('bucket', 'openclaw-main'))" 2>/dev/null || echo "openclaw-main")

    log_info "Creating bucket '$bucket' (if it doesn't exist)..."

    if python3 "$SCRIPT_DIR/index.py" create-bucket "$bucket" 2>/dev/null; then
        log_ok "Bucket '$bucket' ready"
        ((++CHECKS_PASSED))
    else
        log_warn "Could not create/verify bucket (it may already exist)"
    fi
}

test_search() {
    log_info "Testing search connectivity..."

    local bucket
    bucket=$(python3 -c "import json; print(json.load(open('$SCRIPT_DIR/config.json')).get('bucket', 'openclaw-main'))" 2>/dev/null || echo "openclaw-main")

    local response
    response=$(curl -s -w "\n%{http_code}" \
        -H "Authorization: Bearer $TELNYX_API_KEY" \
        -H "Content-Type: application/json" \
        "https://api.telnyx.com/v2/ai/embeddings/similarity-search" \
        -d "{\"bucket_name\":\"$bucket\",\"query\":\"test\",\"num_docs\":1}" \
        2>/dev/null)

    local status
    status=$(echo "$response" | tail -1)

    if [[ "$status" == "200" ]]; then
        log_ok "Search endpoint responding (bucket: $bucket)"
        ((++CHECKS_PASSED))
    elif [[ "$status" == "404" ]]; then
        log_warn "Bucket '$bucket' not found or embeddings not enabled"
        echo "   Upload files and run: ./index.py embed --bucket $bucket"
    else
        log_warn "Search test returned HTTP $status"
    fi
}

show_summary() {
    echo ""
    echo "================================================"
    echo ""

    if [[ $CHECKS_FAILED -eq 0 ]]; then
        log_ok "All checks passed ($CHECKS_PASSED/$CHECKS_PASSED)"
        echo ""
        echo "Usage:"
        echo "  Search:   ./search.py \"your query\""
        echo "  Upload:   ./index.py upload path/to/file.md"
        echo "  Embed:    ./index.py embed"
        echo "  Status:   ./index.py status <task_id>"
        echo ""
    else
        log_err "Completed with $CHECKS_FAILED error(s):"
        echo ""
        for error in "${SETUP_ERRORS[@]}"; do
            echo "  - $error"
        done
        echo ""
        echo "Fix the above issues and run setup again."
        echo ""
        return 1
    fi
}

show_help() {
    cat << EOF
Telnyx Embeddings - Setup Script

Usage: $0 [OPTIONS]

OPTIONS:
  --check     Validate requirements without making changes
  --help      Show this help message

REQUIREMENTS:
  - Python 3.8+
  - TELNYX_API_KEY environment variable or .env file
  - Network access to Telnyx APIs

EXAMPLES:
  $0              # Full setup
  $0 --check      # Validation only

Get your API key at: https://portal.telnyx.com/#/app/api-keys
EOF
}

main() {
    case "${1:-}" in
        --check)
            DRY_RUN=true
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        --*)
            log_err "Unknown option: $1"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac

    echo ""
    echo "Telnyx Embeddings Setup"
    echo "======================="
    echo ""
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "Mode: Validation Only (--check)"
        echo ""
    fi

    # Run checks
    check_python
    check_syntax
    check_credentials
    check_config

    if [[ "$DRY_RUN" == "true" ]]; then
        echo ""
        log_info "Dry-run complete. No changes were made."
        show_summary
        return $?
    fi

    # Full setup
    if [[ $CHECKS_FAILED -eq 0 ]]; then
        make_executable
        create_bucket_if_needed
        test_search
    fi

    show_summary
}

main "$@"
