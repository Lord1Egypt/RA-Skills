#!/bin/bash

###############################################################################
# Clawhub Publish Script
#
# This script automates publishing the pylinter-assist skill to clawhub.
# It validates prerequisites, checks for required files, and runs the publish
# command with appropriate error handling.
#
# Usage:
#   ./scripts/publish.sh [--dry-run] [--verbose] [--skill-dir PATH]
#
###############################################################################

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DRY_RUN=false
VERBOSE=false
BUMP=false
BUMP_PART="minor"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

###############################################################################
# Functions
###############################################################################

print_header() {
    echo -e "${BLUE}===================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}  → $1${NC}"
    fi
}

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    --dry-run       Show what would be published without actually publishing
    --verbose       Enable verbose output
    --bump          Auto-increment the minor version in SKILL.md before publishing
    --bump-patch    Auto-increment the patch/build version (X.Y.Z+1) before publishing
    --help          Show this help message

Examples:
    # Publish normally
    ./scripts/publish.sh

    # Auto-increment minor version and publish
    ./scripts/publish.sh --bump

    # Test publish without making changes
    ./scripts/publish.sh --dry-run

    # Verbose output
    ./scripts/publish.sh --verbose
EOF
}

check_prerequisites() {
    print_info "Checking prerequisites..."

    # Check if clawhub CLI is installed
    if ! command -v clawhub &> /dev/null; then
        print_error "clawhub CLI not found. Please install clawhub first."
        echo "    Visit: https://github.com/clawai/clawhub-cli"
        exit 1
    fi
    print_success "clawhub CLI found"

    # Check if pyproject.toml exists
    if [ ! -f "$PROJECT_ROOT/pyproject.toml" ]; then
        print_error "pyproject.toml not found in project root"
        exit 1
    fi
    print_success "pyproject.toml found"

    # Check if SKILL.md exists (required for clawhub)
    if [ ! -f "$PROJECT_ROOT/SKILL.md" ]; then
        print_warning "SKILL.md not found. Creating default SKILL.md..."
        create_default_skill_md
    else
        print_success "SKILL.md found"
    fi
}

create_default_skill_md() {
    cat > "$PROJECT_ROOT/SKILL.md" << 'EOF'
# pylinter-assist — OpenClaw Skill

## Description

Context-aware Python linting with smart pattern heuristics for PR review.

## Usage

```bash
# Activate your virtual environment first
source .venv/bin/activate

lint-pr [TARGET] [OPTIONS]
```

## Targets

- `pr <number>` — lint all files changed in a GitHub PR
- `staged` — lint git-staged files
- `diff <file>` — lint files from a unified diff file
- `files <path>...` — lint explicit files or directories

## Options

| Flag | Description |
|------|-------------|
| `--format text\|json\|markdown` | Output format (default: markdown) |
| `--config <path>` | Custom `.linting-rules.yml` path |
| `--post-comment` / `--no-post-comment` | Post result as GitHub PR comment |
| `--fail-on-warning` | Also fail on warnings (default: errors only) |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

EOF
}

get_version() {
    grep -E "^version" "$PROJECT_ROOT/pyproject.toml" | head -1 | sed 's/.*"\(.*\)".*/\1/'
}

bump_version() {
    local current_version=$(get_version)
    local major minor patch build

    # Parse version (X.Y.Z or X.Y.Z+build)
    if [[ "$current_version" =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)(\+([0-9]+))?$ ]]; then
        major="${BASH_REMATCH[1]}"
        minor="${BASH_REMATCH[2]}"
        patch="${BASH_REMATCH[3]}"
        build="${BASH_REMATCH[5]:-0}"

        if [ "$BUMP_PART" = "minor" ]; then
            minor=$((minor + 1))
            patch=0
        elif [ "$BUMP_PART" = "patch" ]; then
            patch=$((patch + 1))
        fi

        local new_version="${major}.${minor}.${patch}"
        print_info "Bumping version from $current_version to $new_version"

        # Update pyproject.toml
        sed -i "s/^version = \"\(.*\)\"$/version = \"$new_version\"/" "$PROJECT_ROOT/pyproject.toml"
        print_success "Version updated in pyproject.toml"

        # Update SKILL.md if it exists — pattern matches X.Y.Z and X.Y.Z+N variants
        if [ -f "$PROJECT_ROOT/SKILL.md" ]; then
            sed -i '' "s/version: [0-9][0-9.+]*/version: $new_version/" "$PROJECT_ROOT/SKILL.md" 2>/dev/null || \
                sed -i "s/version: [0-9][0-9.+]*/version: $new_version/" "$PROJECT_ROOT/SKILL.md"
            print_success "Version updated in SKILL.md"
        fi

        echo "$new_version"
    else
        print_error "Invalid version format: $current_version"
        exit 1
    fi
}

validate_skill() {
    print_header "Validating Skill"

    # Check required files
    local required_files=("pyproject.toml" "README.md")
    for file in "${required_files[@]}"; do
        if [ -f "$PROJECT_ROOT/$file" ]; then
            print_success "Required file: $file"
        else
            print_warning "Missing optional file: $file"
        fi
    done

    # Check SKILL.md
    if [ -f "$PROJECT_ROOT/SKILL.md" ]; then
        print_success "SKILL.md present"

        # Validate SKILL.md content
        if ! grep -q "^#" "$PROJECT_ROOT/SKILL.md"; then
            print_error "SKILL.md appears to be empty or invalid"
            exit 1
        fi
    else
        print_error "SKILL.md is required for publishing"
        exit 1
    fi

    # Check pyproject.toml structure
    if ! grep -q "\[project\]" "$PROJECT_ROOT/pyproject.toml"; then
        print_error "Invalid pyproject.toml: missing [project] section"
        exit 1
    fi
    print_success "pyproject.toml structure valid"

    print_success "Validation complete"
}

publish_skill() {
    print_header "Publishing to Clawhub"

    local version=$(get_version)
    print_info "Publishing pylinter-assist v$version"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN - No changes will be made"
        echo ""
        echo "Would execute: clawhub publish --version $version $PROJECT_ROOT"
        echo ""
        print_info "Files that would be published:"
        ls -la "$PROJECT_ROOT"/*.toml "$PROJECT_ROOT"/*.md 2>/dev/null || true
        return 0
    fi

    # Run clawhub publish
    print_info "Running clawhub publish..."
    if clawhub publish --version "$version" "$PROJECT_ROOT"; then
        print_success "Publish successful!"
        print_info "Version: $version"
    else
        print_error "Publish failed"
        exit 1
    fi
}

###############################################################################
# Main
###############################################################################

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --bump)
            BUMP=true
            BUMP_PART="minor"
            shift
            ;;
        --bump-patch)
            BUMP=true
            BUMP_PART="patch"
            shift
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Run publish process
if [ "$DRY_RUN" = true ]; then
    print_header "Clawhub Publish - Dry Run"
    print_info "Project: $PROJECT_ROOT"
else
    print_header "Clawhub Publish"
fi

check_prerequisites

if [ "$BUMP" = true ]; then
    print_header "Version Bump"
    bump_version
    print_success "Version bumped successfully"
fi

validate_skill
publish_skill

print_header "Complete"
print_success "Skill published successfully!"
