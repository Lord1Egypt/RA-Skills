#!/usr/bin/env bash
# skill-guard: Scan skills for security issues before installing
# Usage: safe-install.sh <skill-slug> [--version <ver>] [--force] [--skip-scan]

set -euo pipefail

SKILL_SLUG=""
VERSION=""
FORCE=false
SKIP_SCAN=false
STAGING_DIR="/tmp/skill-guard-staging"
SKILLS_DIR="${CLAWHUB_WORKDIR:-$HOME/.openclaw/workspace}/skills"
REPORTS_DIR="$STAGING_DIR/reports"
SCANNER_CMD=(uvx snyk-agent-scan@latest)

SCAN_STATUS=""
SCAN_OUTPUT=""
SCAN_EXIT_CODE=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error() { echo -e "${RED}ERROR:${NC} $1" >&2; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_info() { echo -e "${BLUE}→${NC} $1"; }

usage() {
    cat <<EOF
skill-guard: Secure skill installation with pre-install scanning

Usage: safe-install.sh <skill-slug> [options]

Options:
  --version <ver>  Install specific version
  --force          Overwrite existing installation
  --skip-scan      Skip security scan (not recommended)
  --help           Show this help

Exit codes:
  0  Installed successfully
  1  General error (args/deps/fetch/install)
  2  Security issues detected by scanner
  3  Scanner unavailable or not configured (e.g. missing SNYK_TOKEN)

Environment:
  CLAWHUB_WORKDIR  Skills parent directory (default: ~/.openclaw/workspace)
  SNYK_TOKEN       Required by snyk-agent-scan for authenticated scanning
EOF
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --version)
            if [[ $# -lt 2 ]]; then
                print_error "--version requires a value"
                exit 1
            fi
            VERSION="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --skip-scan)
            SKIP_SCAN=true
            shift
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        -* )
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [[ -n "$SKILL_SLUG" ]]; then
                print_error "Only one skill slug is supported"
                exit 1
            fi
            SKILL_SLUG="$1"
            shift
            ;;
    esac
done

if [[ -z "$SKILL_SLUG" ]]; then
    print_error "No skill slug provided"
    usage
    exit 1
fi

check_deps() {
    if ! command -v clawhub >/dev/null 2>&1; then
        print_error "clawhub CLI not found. Install with: npm i -g clawhub"
        exit 1
    fi

    if ! command -v uvx >/dev/null 2>&1; then
        if [[ -f "$HOME/.local/bin/env" ]]; then
            # shellcheck disable=SC1090
            source "$HOME/.local/bin/env"
        fi
        if ! command -v uvx >/dev/null 2>&1; then
            print_error "uvx not found. Install uv with: curl -LsSf https://astral.sh/uv/install.sh | sh"
            exit 1
        fi
    fi
}

stage_skill() {
    print_info "Fetching $SKILL_SLUG to staging area..."

    rm -rf "$STAGING_DIR/skills/$SKILL_SLUG"
    mkdir -p "$STAGING_DIR" "$REPORTS_DIR"

    local install_cmd=(clawhub install "$SKILL_SLUG" --workdir "$STAGING_DIR")
    if [[ -n "$VERSION" ]]; then
        install_cmd+=(--version "$VERSION")
    fi

    if ! "${install_cmd[@]}" 2>&1; then
        print_error "Failed to fetch skill from ClawHub"
        exit 1
    fi

    if [[ ! -d "$STAGING_DIR/skills/$SKILL_SLUG" ]]; then
        print_error "Skill not found in staging after download"
        exit 1
    fi

    print_success "Skill staged at $STAGING_DIR/skills/$SKILL_SLUG"
}

scan_skill() {
    print_info "Scanning $SKILL_SLUG for security issues..."
    echo ""

    local staged_path="$STAGING_DIR/skills/$SKILL_SLUG"
    local report_path="$REPORTS_DIR/$SKILL_SLUG.scan.log"

    if [[ -z "${SNYK_TOKEN:-}" ]]; then
        SCAN_STATUS="scanner_unavailable"
        SCAN_OUTPUT="SNYK_TOKEN is not set. snyk-agent-scan requires authentication."
        SCAN_EXIT_CODE=3
        printf '%s\n' "$SCAN_OUTPUT" | tee "$report_path"
        return 0
    fi

    local scan_cmd=("${SCANNER_CMD[@]}" --skills "$staged_path")
    local scan_output=""
    local scan_exit_code=0

    scan_output=$("${scan_cmd[@]}" 2>&1) || scan_exit_code=$?
    SCAN_OUTPUT="$scan_output"
    SCAN_EXIT_CODE=$scan_exit_code

    printf '%s\n' "$scan_output" | tee "$report_path"
    echo ""

    if echo "$scan_output" | grep -Eqi "security issues detected|prompt injection detected|malicious code pattern detected|secret found|machine state compromise attempt|third-party content exposure|critical|high risk|medium risk"; then
        SCAN_STATUS="threats_found"
        return 0
    fi

    if echo "$scan_output" | grep -Eqi "SNYK_TOKEN|requires authentication|API token|renamed to 'snyk-agent-scan'|command not found|traceback|exception"; then
        SCAN_STATUS="scanner_unavailable"
        return 0
    fi

    if [[ $scan_exit_code -ne 0 ]]; then
        SCAN_STATUS="scanner_unavailable"
        return 0
    fi

    SCAN_STATUS="clean"
    return 0
}

install_skill() {
    print_info "Installing $SKILL_SLUG to $SKILLS_DIR..."

    mkdir -p "$SKILLS_DIR"
    local staged_path="$STAGING_DIR/skills/$SKILL_SLUG"
    local final_path="$SKILLS_DIR/$SKILL_SLUG"

    if [[ -d "$final_path" ]]; then
        if [[ "$FORCE" == "true" ]]; then
            rm -rf "$final_path"
        else
            print_error "Skill already exists at $final_path (use --force to overwrite)"
            exit 1
        fi
    fi

    mv "$staged_path" "$SKILLS_DIR/"
    print_success "Installed $SKILL_SLUG to $final_path"
}

cleanup() {
    rm -rf "$STAGING_DIR/skills/$SKILL_SLUG" 2>/dev/null || true
}

main() {
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║  skill-guard: Secure Skill Installation      ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""

    check_deps
    stage_skill

    if [[ "$SKIP_SCAN" == "true" ]]; then
        print_warning "Skipping security scan (--skip-scan)"
        install_skill
        cleanup
        echo ""
        print_success "Installation complete (scan skipped)"
        exit 0
    fi

    scan_skill

    case "$SCAN_STATUS" in
        clean)
            print_success "No security issues detected"
            install_skill
            cleanup
            echo ""
            print_success "Installation complete"
            exit 0
            ;;
        threats_found)
            echo ""
            print_warning "Security issues detected in $SKILL_SLUG"
            echo ""
            echo "The skill has been staged but NOT installed."
            echo "Staged location: $STAGING_DIR/skills/$SKILL_SLUG"
            echo "Scan report: $REPORTS_DIR/$SKILL_SLUG.scan.log"
            echo ""
            echo "Options:"
            echo "  1. Review the report and inspect the staged files"
            echo "  2. Run: mv $STAGING_DIR/skills/$SKILL_SLUG $SKILLS_DIR/ to install anyway"
            echo "  3. Run: rm -rf $STAGING_DIR/skills/$SKILL_SLUG to discard"
            echo ""
            exit 2
            ;;
        scanner_unavailable)
            echo ""
            print_warning "Scanner could not complete for $SKILL_SLUG"
            echo ""
            echo "The skill has been staged but NOT installed."
            echo "Reason: scanner unavailable or not configured correctly."
            echo "Staged location: $STAGING_DIR/skills/$SKILL_SLUG"
            echo "Scan report: $REPORTS_DIR/$SKILL_SLUG.scan.log"
            echo ""
            echo "Next steps:"
            echo "  1. Set SNYK_TOKEN and rerun the scan"
            echo "  2. Review the staged skill manually if urgent"
            echo "  3. Run with --skip-scan only if you explicitly accept the risk"
            echo ""
            exit 3
            ;;
        *)
            print_error "Unexpected scan status: $SCAN_STATUS"
            exit 1
            ;;
    esac
}

main
