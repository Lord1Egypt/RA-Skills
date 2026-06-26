#!/bin/bash

# OpenClaw Self-Backup Script (Generic Version)
# Backs up important workspace files to any GitHub repository

set -e

# CONFIGURATION - Edit these variables for your setup
REPO_URL="${BACKUP_REPO_URL:-https://github.com/YOUR_USERNAME/YOUR_BACKUP_REPO.git}"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"

# Runtime variables
BACKUP_DIR="/tmp/openclaw_backup_$(date +%s)"
DRY_RUN=false
FORCE=false

# Check if repository URL is configured
if [[ "$REPO_URL" == *"YOUR_USERNAME"* ]]; then
    echo "ERROR: Please configure your repository URL first!"
    echo ""
    echo "Option 1: Set environment variable:"
    echo "  export BACKUP_REPO_URL=\"https://github.com/yourusername/your-backup-repo.git\""
    echo ""
    echo "Option 2: Edit this script and change REPO_URL variable"
    echo ""
    echo "Option 3: Create repository with:"
    echo "  gh repo create yourusername/openclaw-backup --private"
    exit 1
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--dry-run] [--force] [--help]"
            echo "  --dry-run  Show what would be backed up without doing it"
            echo "  --force    Force push even with conflicts"
            echo "  --help     Show this help message"
            echo ""
            echo "Configuration:"
            echo "  Set BACKUP_REPO_URL environment variable or edit REPO_URL in script"
            echo "  Current repository: $REPO_URL"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting OpenClaw self-backup..."
log "Repository: $REPO_URL"

if [ "$DRY_RUN" = true ]; then
    log "DRY RUN MODE - No changes will be made"
fi

# Check if workspace exists
if [ ! -d "$WORKSPACE_DIR" ]; then
    log "ERROR: Workspace directory not found: $WORKSPACE_DIR"
    log "Set OPENCLAW_WORKSPACE environment variable if using custom location"
    exit 1
fi

# Check if git is available
if ! command -v git &> /dev/null; then
    log "ERROR: git is not installed"
    exit 1
fi

# Check if gh CLI is available for authentication
if ! command -v gh &> /dev/null; then
    log "WARNING: GitHub CLI (gh) not found. Using HTTPS authentication."
    log "Install with: sudo apt install gh   OR   brew install gh"
fi

if [ "$DRY_RUN" = false ]; then
    # Clone or update the backup repository
    log "Setting up backup repository..."
    git clone "$REPO_URL" "$BACKUP_DIR" 2>/dev/null || {
        log "ERROR: Failed to clone repository. Check:"
        log "  1. Repository exists: $REPO_URL"
        log "  2. You have access to it"
        log "  3. GitHub authentication is working"
        exit 1
    }
    
    cd "$BACKUP_DIR"
else
    log "Would clone repository to: $BACKUP_DIR"
fi

# Create directory structure
DIRS=("config" "scripts" "memory" "skills")
for dir in "${DIRS[@]}"; do
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$dir"
    else
        log "Would create directory: $dir"
    fi
done

# Core configuration files to backup
CONFIG_FILES=(
    "AGENTS.md"
    "SOUL.md" 
    "USER.md"
    "MEMORY.md"
    "IDENTITY.md"
    "TOOLS.md"
    "AUTOMATION.md"
    "HEARTBEAT.md"
)

# OpenClaw system configuration file
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

log "Backing up core configuration files..."
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$WORKSPACE_DIR/$file" ]; then
        if [ "$DRY_RUN" = false ]; then
            cp "$WORKSPACE_DIR/$file" "config/"
            log "  ✓ Backed up: $file"
        else
            log "  Would backup: $file"
        fi
    else
        log "  ⚠ Skipping missing file: $file"
    fi
done

# Backup OpenClaw system configuration
log "Backing up OpenClaw system configuration..."
if [ -f "$OPENCLAW_CONFIG" ]; then
    if [ "$DRY_RUN" = false ]; then
        # Sanitize the config file to remove sensitive tokens
        if command -v jq &> /dev/null; then
            log "  Sanitizing openclaw.json (removing sensitive tokens)..."
            
            # Get script directory relative to this script
            SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
            
            if [ -f "$SCRIPT_DIR/sanitize-config.sh" ]; then
                "$SCRIPT_DIR/sanitize-config.sh" "$OPENCLAW_CONFIG" "config/openclaw.json"
                log "  ✓ Backed up: openclaw.json (sanitized)"
            else
                log "  ⚠ Sanitizer script not found, skipping openclaw.json"
            fi
        else
            log "  ⚠ jq not found, skipping openclaw.json (contains sensitive data)"
            log "    Install jq: sudo apt install jq  OR  brew install jq"
        fi
    else
        log "  Would backup: openclaw.json (sanitized)"
    fi
else
    log "  ⚠ Skipping missing file: openclaw.json"
fi

# Backup scripts directory
if [ -d "$WORKSPACE_DIR/scripts" ]; then
    log "Backing up scripts directory..."
    if [ "$DRY_RUN" = false ]; then
        cp -r "$WORKSPACE_DIR/scripts/"* "scripts/" 2>/dev/null || log "  No scripts to backup"
    else
        log "  Would backup scripts directory"
    fi
else
    log "  No scripts directory found"
fi

# Backup memory directory (last 30 days)
if [ -d "$WORKSPACE_DIR/memory" ]; then
    log "Backing up recent memory files..."
    if [ "$DRY_RUN" = false ]; then
        find "$WORKSPACE_DIR/memory" -name "*.md" -mtime -30 -exec cp {} "memory/" \; 2>/dev/null || log "  No recent memory files"
    else
        log "  Would backup recent memory files (last 30 days)"
    fi
else
    log "  No memory directory found"
fi

# Backup skills configurations (metadata only)
if [ -d "$WORKSPACE_DIR/skills" ]; then
    log "Backing up skills metadata..."
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "skills"
        find "$WORKSPACE_DIR/skills" -name "SKILL.md" -exec dirname {} \; | while read skilldir; do
            skillname=$(basename "$skilldir")
            mkdir -p "skills/$skillname"
            cp "$skilldir/SKILL.md" "skills/$skillname/" 2>/dev/null || true
        done
    else
        log "  Would backup skills metadata"
    fi
else
    log "  No skills directory found"
fi

# Create backup info file
BACKUP_INFO="backup-info.md"
if [ "$DRY_RUN" = false ]; then
    cat > "$BACKUP_INFO" << EOF
# OpenClaw Self-Backup Information

**Backup Date:** $(date)
**Hostname:** $(hostname)
**OpenClaw Version:** $(openclaw --version 2>/dev/null || echo "Unknown")
**Workspace:** $WORKSPACE_DIR
**Repository:** $REPO_URL

## Backup Contents

### Configuration Files
$(cd config 2>/dev/null && ls -la | tail -n +4 | awk '{print "- " $9 " (" $5 " bytes)"}' || echo "None")

**OpenClaw Settings:** $([ -f config/openclaw.json ] && echo "✓ openclaw.json (sanitized)" || echo "✗ Not backed up")

### Scripts
$(cd scripts 2>/dev/null && find . -type f | sed 's|^\./|- |' || echo "None")

### Memory Files
$(cd memory 2>/dev/null && ls -1 *.md 2>/dev/null | sed 's/^/- /' || echo "None")

### Skills
$(cd skills 2>/dev/null && find . -name "SKILL.md" | sed 's|/SKILL.md||' | sed 's|^\./|- |' || echo "None")

## Notes

This backup was created automatically by the self-backup skill.

**Security:** All sensitive tokens have been redacted from openclaw.json.
To restore, copy files back and re-enter your actual tokens.

**Repository:** $REPO_URL
EOF
    log "Created backup information file"
else
    log "Would create backup-info.md with metadata"
fi

if [ "$DRY_RUN" = false ]; then
    # Commit and push changes
    log "Committing changes..."
    git add .
    
    if git diff --staged --quiet; then
        log "No changes to commit"
    else
        git commit -m "Automated OpenClaw backup - $(date)"
        
        if [ "$FORCE" = true ]; then
            log "Force pushing to repository..."
            git push origin main --force
        else
            log "Pushing to repository..."
            git push origin main || {
                log "ERROR: Push failed. Use --force if you want to overwrite remote changes."
                exit 1
            }
        fi
        
        log "✓ Backup completed successfully!"
        log "Repository: $REPO_URL"
    fi
    
    # Cleanup
    cd /tmp
    rm -rf "$BACKUP_DIR"
    log "Cleanup completed"
else
    log "DRY RUN COMPLETE - No actual backup was performed"
fi

log "Backup process finished"