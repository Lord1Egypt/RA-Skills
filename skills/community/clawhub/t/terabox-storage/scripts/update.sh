#!/bin/bash
# terabox-storage Skill auto-update script
# Checks TeraBox TCC config API for newer Skill version and applies updates
#
# NOTE: This script manages Skill-level updates (documentation, scripts, etc.)
# CLI binary updates are now managed by the CLI's built-in auto-update system:
#   - `terabox update`       - Check and update CLI
#   - `terabox update check` - Check only
#   - `terabox update rollback` - Rollback to previous version
#   - The CLI also auto-checks for updates on every command execution
#     (disable with --no-check-update flag)

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Config (supports TERABOX_UPDATE_API env override for testing)
CONFIG_API="${TERABOX_UPDATE_API:-https://www.terabox.com/rest/1.0/operation/tcc/query}"
CONFIG_KEY="terabox_storage_skill"
CONFIG_BODY="{\"app_id\":102,\"keys\":[\"${CONFIG_KEY}\"]}"

# Script directory (used to locate Skill files)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION_FILE="${SKILL_DIR}/VERSION"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Version comparison: returns 0 if $1 > $2, 1 if $1 = $2, 2 if $1 < $2
version_compare() {
    if [ "$1" = "$2" ]; then
        return 1
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++)); do
        if [ -z "${ver2[i]}" ]; then
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]})); then
            return 0
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 2
        fi
    done
    return 1
}

# Strip leading 'v' prefix (e.g., v1.2.0 -> 1.2.0)
strip_v_prefix() {
    echo "$1" | sed 's/^v//'
}

# Get local Skill version
get_local_version() {
    if [ -f "$VERSION_FILE" ]; then
        local raw=$(cat "$VERSION_FILE" | tr -d '[:space:]')
        strip_v_prefix "$raw"
    else
        echo "unknown"
    fi
}

# Extract value for a key from query string
# Usage: query_get "version=1.1.2&url=https://..." "version"
query_get() {
    local qs="$1"
    local key="$2"
    echo "$qs" | tr '&' '\n' | while IFS='=' read -r k v; do
        if [ "$k" = "$key" ]; then
            echo "$v"
            return 0
        fi
    done
}

# Fetch skill config from TeraBox TCC API, return skills_info query string
fetch_skills_info() {
    local response=""

    if command -v curl &> /dev/null; then
        response=$(curl -s --location -X GET "$CONFIG_API" \
            -H 'User_login_country: US' \
            -H 'Content-Type: text/plain' \
            -d "$CONFIG_BODY" \
            --connect-timeout 10 --max-time 30 2>/dev/null) || {
            log_error "Cannot connect to config server, please check network"
            return 1
        }
    elif command -v wget &> /dev/null; then
        response=$(wget -qO- --timeout=30 \
            --header='User_login_country: US' \
            --header='Content-Type: text/plain' \
            --post-data="$CONFIG_BODY" \
            "$CONFIG_API" 2>/dev/null) || {
            log_error "Cannot connect to config server, please check network"
            return 1
        }
    else
        log_error "curl or wget not found"
        return 1
    fi

    # Validate response - check for errno: 0
    local errno=$(echo "$response" | grep -o '"errno"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | grep -o '[0-9]*$')
    if [ "$errno" != "0" ]; then
        log_error "Config API returned error (errno: ${errno:-unknown})"
        return 1
    fi

    # Extract the config value for our key from the TCC response
    # TCC API returns JSON like: {"errno":0,"data":{"terabox_storage_skill":"version=x.x.x&url=...&checksum=..."}}
    # The value may have \u0026 for &, need to restore
    local skills_info=$(echo "$response" | sed 's/\\u0026/\&/g' | grep -o 'version=[^"]*' | head -1 | sed 's/\\//g')

    if [ -z "$skills_info" ]; then
        log_error "No version config found in response"
        return 1
    fi

    echo "$skills_info"
}

# Perform the actual update
do_update() {
    local remote_url="$1"
    local remote_version="$2"

    if [ -z "$remote_url" ]; then
        log_error "No Skill download URL found"
        return 1
    fi

    log_info "Downloading Skill update package (v${remote_version})..."
    log_info "Download URL: ${remote_url}"

    # Create temp directory
    local tmp_dir=$(mktemp -d)
    trap "rm -rf '$tmp_dir'" EXIT

    # Download zip
    local zip_path="${tmp_dir}/terabox-storage.zip"
    if command -v curl &> /dev/null; then
        curl -fsSL -o "$zip_path" "$remote_url" || {
            log_error "Failed to download Skill update package"
            return 1
        }
    elif command -v wget &> /dev/null; then
        wget -q -O "$zip_path" "$remote_url" || {
            log_error "Failed to download Skill update package"
            return 1
        }
    fi

    # Verify checksum if provided
    local checksum=$(query_get "$SKILLS_INFO" "checksum")
    if [ -n "$checksum" ]; then
        local actual=""
        if command -v sha256sum &> /dev/null; then
            actual=$(sha256sum "$zip_path" | awk '{print $1}')
        elif command -v shasum &> /dev/null; then
            actual=$(shasum -a 256 "$zip_path" | awk '{print $1}')
        fi

        if [ -n "$actual" ]; then
            if [ "$actual" != "$checksum" ]; then
                log_error "SHA256 verification failed! File may have been tampered with"
                log_error "  Expected: ${checksum}"
                log_error "  Actual:   ${actual}"
                return 1
            fi
            log_info "SHA256 verification passed"
        else
            log_warn "sha256sum/shasum not found, skipping verification"
        fi
    fi

    # Extract and overwrite
    log_info "Extracting update..."
    if command -v unzip &> /dev/null; then
        unzip -qo "$zip_path" -d "$SKILL_DIR" || {
            log_error "Failed to extract update"
            return 1
        }
    else
        log_error "unzip tool not found"
        return 1
    fi

    # Update VERSION file
    echo "$remote_version" > "$VERSION_FILE"

    # If the update contains a new terabox binary, install it
    if [ -f "$SKILL_DIR/terabox" ] && [ -x "$SKILL_DIR/terabox" ]; then
        if [ -d "$HOME/.local/bin" ]; then
            cp "$SKILL_DIR/terabox" "$HOME/.local/bin/terabox"
            chmod +x "$HOME/.local/bin/terabox"
            log_info "CLI binary updated in ~/.local/bin/terabox"
        fi
    fi

    log_info "Skill updated to v${remote_version}"
}

# Global variable
SKILLS_INFO=""

# Main function
main() {
    local check_only="no"
    local auto_yes="no"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --check|-c)
                check_only="yes"
                shift
                ;;
            --yes|-y)
                auto_yes="yes"
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [options]"
                echo ""
                echo "Options:"
                echo "  --check, -c   Check for updates only, do not install"
                echo "  --yes, -y     Skip confirmation, auto-update"
                echo "  --help        Show help"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for help"
                exit 1
                ;;
        esac
    done

    # Get local version
    local local_version=$(get_local_version)

    # Fetch remote config
    log_info "Checking for updates..."
    SKILLS_INFO=$(fetch_skills_info) || {
        log_warn "Unable to fetch update info, please try again later"
        exit 1
    }

    # Parse remote version and download URL (strip v prefix for comparison)
    local remote_version=$(query_get "$SKILLS_INFO" "version")
    local remote_version_clean=$(strip_v_prefix "$remote_version")
    local remote_url=$(query_get "$SKILLS_INFO" "url")

    if [ -z "$remote_version" ]; then
        log_error "No version info found in config"
        exit 1
    fi

    # Display status
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  terabox-storage Skill Update Check${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "  Local version:  ${local_version}"
    echo -e "  Latest version: ${remote_version}"

    # Version comparison
    local needs_update="no"
    if [ "$local_version" = "unknown" ]; then
        echo -e "  Status:         ${YELLOW}Version unknown, update recommended${NC}"
        needs_update="yes"
    else
        set +e
        version_compare "$remote_version_clean" "$local_version"
        local cmp_result=$?
        set -e

        if [ $cmp_result -eq 0 ]; then
            echo -e "  Status:         ${YELLOW}New version available${NC}"
            needs_update="yes"
        else
            echo -e "  Status:         ${GREEN}Already up to date${NC}"
        fi
    fi

    echo ""

    # No update needed
    if [ "$needs_update" = "no" ]; then
        log_info "Skill is already up to date"
        exit 0
    fi

    # Check-only mode
    if [ "$check_only" = "yes" ]; then
        exit 0
    fi

    # User confirmation
    if [ "$auto_yes" != "yes" ]; then
        echo -n -e "${YELLOW}Update Skill to v${remote_version}? [y/N] ${NC}"
        read -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Update cancelled"
            exit 0
        fi
    fi

    echo ""

    # Execute update
    do_update "$remote_url" "$remote_version" || {
        log_error "Skill update failed"
        exit 1
    }

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Update complete${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
}

# Execute main function
main "$@"
