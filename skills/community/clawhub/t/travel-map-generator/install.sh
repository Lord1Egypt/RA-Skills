#!/usr/bin/env bash
# Cross-platform installer for travel-map-generator-skill
# Supports: Claude Code, Cursor, GitHub Copilot, Windsurf, Cline, and more

set -e

SKILL_NAME="travel-map-generator-skill"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect platform
detect_platform() {
    if [ -n "$1" ]; then
        echo "$1"
        return
    fi

    # Check for various platform indicators
    if [ -d "$HOME/.claude" ] || [ -d ".claude" ]; then
        echo "claude"
    elif [ -d ".cursor" ] || [ -d "$HOME/.cursor" ]; then
        echo "cursor"
    elif [ -d ".github" ]; then
        echo "copilot"
    elif [ -d ".windsurf" ] || [ -d "$HOME/.windsurf" ]; then
        echo "windsurf"
    elif [ -f ".clinerules" ] || [ -d ".clinerules" ]; then
        echo "cline"
    elif [ -d "$HOME/.gemini" ]; then
        echo "gemini"
    elif [ -d ".kiro" ]; then
        echo "kiro"
    elif [ -d ".trae" ]; then
        echo "trae"
    elif [ -d ".roo" ]; then
        echo "roo"
    elif [ -d "$HOME/.config/goose" ]; then
        echo "goose"
    elif [ -d "$HOME/.agents" ]; then
        echo "universal"
    else
        echo "unknown"
    fi
}

# Get install path for platform
get_install_path() {
    local platform=$1
    local user_level=$2

    case "$platform" in
        claude)
            if [ "$user_level" = "true" ]; then
                echo "$HOME/.claude/skills/$SKILL_NAME"
            else
                echo ".claude/skills/$SKILL_NAME"
            fi
            ;;
        cursor)
            if [ "$user_level" = "true" ]; then
                echo "$HOME/.cursor/rules/$SKILL_NAME"
            else
                echo ".cursor/rules/$SKILL_NAME"
            fi
            ;;
        copilot)
            echo ".github/skills/$SKILL_NAME"
            ;;
        windsurf)
            if [ "$user_level" = "true" ]; then
                echo "$HOME/.windsurf/rules/$SKILL_NAME"
            else
                echo ".windsurf/rules/$SKILL_NAME"
            fi
            ;;
        cline)
            echo ".clinerules/$SKILL_NAME"
            ;;
        gemini)
            echo "$HOME/.gemini/skills/$SKILL_NAME"
            ;;
        kiro)
            echo ".kiro/skills/$SKILL_NAME"
            ;;
        trae)
            echo ".trae/rules/$SKILL_NAME"
            ;;
        roo)
            echo ".roo/rules/$SKILL_NAME"
            ;;
        goose)
            echo "$HOME/.config/goose/skills/$SKILL_NAME"
            ;;
        opencode)
            echo "$HOME/.config/opencode/skills/$SKILL_NAME"
            ;;
        universal)
            if [ "$user_level" = "true" ]; then
                echo "$HOME/.agents/skills/$SKILL_NAME"
            else
                echo ".agents/skills/$SKILL_NAME"
            fi
            ;;
        *)
            echo ""
            ;;
    esac
}

# Install the skill
install_skill() {
    local platform=$1
    local install_path=$2
    local dry_run=$3

    log_info "Installing $SKILL_NAME for $platform..."
    log_info "Target path: $install_path"

    if [ "$dry_run" = "true" ]; then
        log_info "[DRY RUN] Would copy files from $SCRIPT_DIR to $install_path"
        return 0
    fi

    # Create parent directory if needed
    mkdir -p "$(dirname "$install_path")"

    # Remove existing installation
    if [ -d "$install_path" ]; then
        log_warn "Removing existing installation at $install_path"
        rm -rf "$install_path"
    fi

    # Copy skill files
    cp -R "$SCRIPT_DIR" "$install_path"

    # Remove install.sh from installed copy (not needed there)
    rm -f "$install_path/install.sh"

    log_success "Installed to $install_path"
}

# Install to all detected platforms
install_all() {
    local dry_run=$1
    local installed=()

    log_info "Installing to all detected platforms..."

    for platform in claude cursor copilot windsurf cline gemini kiro trae roo goose opencode universal; do
        local path=$(get_install_path "$platform" "true")
        if [ -n "$path" ]; then
            # Check if platform directory exists
            local parent_dir=$(dirname "$path")
            if [ -d "$parent_dir" ]; then
                install_skill "$platform" "$path" "$dry_run"
                installed+=("$platform")
            fi
        fi
    done

    if [ ${#installed[@]} -eq 0 ]; then
        log_warn "No platforms detected. Install manually using --platform <name>"
        return 1
    fi

    log_success "Installed to ${#installed[@]} platform(s): ${installed[*]}"
}

# Print usage
print_usage() {
    cat << EOF
Usage: ./install.sh [OPTIONS]

Install travel-map-generator-skill to your AI coding assistant.

OPTIONS:
    -p, --platform <name>    Target platform (claude, cursor, copilot, windsurf, cline, etc.)
    -u, --user               Install to user-level config (default: project-level)
    -a, --all                Install to all detected platforms
    -d, --dry-run            Show what would be done without making changes
    -h, --help               Show this help message

PLATFORMS:
    claude       Claude Code (~/.claude/skills/)
    cursor       Cursor (.cursor/rules/)
    copilot      GitHub Copilot (.github/skills/)
    windsurf     Windsurf (.windsurf/rules/)
    cline        Cline (.clinerules/)
    gemini       Gemini CLI (~/.gemini/skills/)
    kiro         Kiro (.kiro/skills/)
    trae         Trae (.trae/rules/)
    roo          Roo Code (.roo/rules/)
    goose        Goose (~/.config/goose/skills/)
    opencode     OpenCode (~/.config/opencode/skills/)
    universal    Universal path (~/.agents/skills/)

EXAMPLES:
    ./install.sh                          # Auto-detect platform
    ./install.sh --platform claude        # Install for Claude Code
    ./install.sh --platform cursor --user # Install to user-level Cursor config
    ./install.sh --all                    # Install to all detected platforms
    ./install.sh --dry-run                # Preview changes

After installation, use the skill by typing:
    /travel-map-generator Create a map of Tokyo
EOF
}

# Main
main() {
    local platform=""
    local user_level="false"
    local dry_run="false"
    local install_all_flag="false"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--platform)
                platform="$2"
                shift 2
                ;;
            -u|--user)
                user_level="true"
                shift
                ;;
            -a|--all)
                install_all_flag="true"
                shift
                ;;
            -d|--dry-run)
                dry_run="true"
                shift
                ;;
            -h|--help)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done

    log_info "Travel Map Generator Skill Installer"
    echo ""

    # Handle --all
    if [ "$install_all_flag" = "true" ]; then
        install_all "$dry_run"
        echo ""
        log_success "Installation complete!"
        echo ""
        echo "To use the skill, type:"
        echo "  /travel-map-generator Create a map of Tokyo"
        exit 0
    fi

    # Auto-detect platform if not specified
    if [ -z "$platform" ]; then
        platform=$(detect_platform)
        if [ "$platform" = "unknown" ]; then
            log_error "Could not auto-detect platform. Please specify with --platform <name>"
            echo ""
            print_usage
            exit 1
        fi
        log_info "Auto-detected platform: $platform"
    fi

    # Get install path
    local install_path=$(get_install_path "$platform" "$user_level")
    if [ -z "$install_path" ]; then
        log_error "Unknown platform: $platform"
        exit 1
    fi

    # Install
    install_skill "$platform" "$install_path" "$dry_run"

    echo ""
    log_success "Installation complete!"
    echo ""
    echo "To use the skill, type:"
    echo "  /travel-map-generator Create a map of <city>"
    echo ""
    echo "Example:"
    echo "  /travel-map-generator Create a Ghibli-style map of Tokyo with Tokyo Tower, Senso-ji, and Shibuya Crossing"
}

main "$@"
