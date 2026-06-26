#!/bin/bash

# OpenClaw Self-Backup Setup Script
# Helps users configure their backup repository

set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "OpenClaw Self-Backup Setup"
log "=========================="

# Check if GitHub CLI is available
if ! command -v gh &> /dev/null; then
    log "GitHub CLI not found."
    log ""
    log "To install GitHub CLI:"
    log "  Ubuntu/Debian: sudo apt install gh"
    log "  macOS: brew install gh"
    log "  Other: https://cli.github.com/"
    log ""
    echo -n "Do you want to continue with manual setup? (y/n): "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 0
    fi
    MANUAL_SETUP=true
else
    log "GitHub CLI found ✓"
    MANUAL_SETUP=false
fi

# Check authentication
if [ "$MANUAL_SETUP" = false ]; then
    if ! gh auth status &>/dev/null; then
        log "Please login to GitHub CLI first:"
        log "  gh auth login"
        log ""
        echo -n "Would you like to login now? (y/n): "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            gh auth login
        else
            log "Please run 'gh auth login' then run this setup again"
            exit 1
        fi
    else
        log "GitHub authentication verified ✓"
    fi
fi

# Get user information
if [ "$MANUAL_SETUP" = false ]; then
    USERNAME=$(gh api user --jq '.login' 2>/dev/null || echo "")
    if [ -n "$USERNAME" ]; then
        log "GitHub username: $USERNAME"
        SUGGESTED_REPO="$USERNAME/openclaw-backup"
    else
        log "Warning: Could not detect GitHub username"
        SUGGESTED_REPO="YOUR_USERNAME/openclaw-backup"
    fi
else
    log "Manual setup mode"
    echo -n "Enter your GitHub username: "
    read -r USERNAME
    SUGGESTED_REPO="$USERNAME/openclaw-backup"
fi

# Ask about repository
log ""
log "Repository Configuration"
log "------------------------"
echo -n "Repository name (default: $SUGGESTED_REPO): "
read -r REPO_NAME

if [ -z "$REPO_NAME" ]; then
    REPO_NAME="$SUGGESTED_REPO"
fi

REPO_URL="https://github.com/$REPO_NAME.git"

# Create repository
if [ "$MANUAL_SETUP" = false ]; then
    log "Checking if repository exists..."
    
    # Extract owner and repo from REPO_NAME
    IFS='/' read -r OWNER REPO <<< "$REPO_NAME"
    
    if gh repo view "$REPO_NAME" &>/dev/null; then
        log "Repository already exists: $REPO_URL"
    else
        echo -n "Create private repository '$REPO_NAME'? (y/n): "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            log "Creating repository..."
            gh repo create "$REPO_NAME" --private --description "OpenClaw workspace backup repository"
            log "✓ Repository created: $REPO_URL"
        else
            log "Please create the repository manually at: https://github.com/new"
            log "Repository name: $REPO"
            log "Make it private for security!"
        fi
    fi
else
    log "Please create your repository manually:"
    log "  1. Go to: https://github.com/new"
    log "  2. Repository name: ${REPO_NAME##*/}"
    log "  3. Make it PRIVATE (important for security)"
    log "  4. Click 'Create repository'"
fi

# Configure backup script
log ""
log "Configuring backup script..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/backup.sh"

# Create a configuration file for the user
cat > "$SCRIPT_DIR/../backup-config.sh" << EOF
#!/bin/bash
# Self-Backup Configuration
# Source this file or export these variables before running backup.sh

export BACKUP_REPO_URL="$REPO_URL"
export OPENCLAW_WORKSPACE="\$HOME/.openclaw/workspace"

echo "Self-backup configured for repository: $REPO_URL"
EOF

chmod +x "$SCRIPT_DIR/../backup-config.sh"

log "✓ Configuration saved to: backup-config.sh"

# Test the backup script
log ""
log "Testing backup script..."

# Set the environment variable for testing
export BACKUP_REPO_URL="$REPO_URL"

if "$BACKUP_SCRIPT" --dry-run; then
    log "✓ Backup script test completed successfully"
else
    log "✗ Backup script test failed"
    exit 1
fi

log ""
log "Setup completed successfully!"
log ""
log "Next steps:"
log "1. Test backup: source backup-config.sh && scripts/backup.sh --dry-run"
log "2. Run actual backup: source backup-config.sh && scripts/backup.sh"
log "3. View your backups at: $REPO_URL"
log ""
log "Configuration file: backup-config.sh"
log "Repository: $REPO_URL"