#!/bin/bash
set -e

# SigmaFlow Deployment Script
# Builds and deploys the SvelteKit application to the Git repository

# Configuration
REPO_URL="http://git.homelab:3000/vitali/SigmaFlow-Svelte.git"
TOKEN="c865b793f09a3b79b65ebdfbd75c5b17395188d2"
REPO_DIR="${1:-./SigmaFlow-Svelte}"
BRANCH="${2:-main}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if repo directory exists
if [ ! -d "$REPO_DIR" ]; then
    log_info "Cloning repository from $REPO_URL"
    git clone "http://$TOKEN@git.homelab:3000/vitali/SigmaFlow-Svelte.git" "$REPO_DIR"
else
    log_info "Repository already exists at $REPO_DIR"
fi

cd "$REPO_DIR"

# Check if dependencies exist
if [ ! -d "node_modules" ]; then
    log_info "Installing dependencies..."
    npm install
fi

# Build the application
log_info "Building SvelteKit application..."
npm run build

# Add all changes
log_info "Staging changes..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    log_warn "No changes to commit. Deployment complete (no new changes)."
    exit 0
fi

# Commit changes with timestamp
COMMIT_MESSAGE="Deploy $(date +'%Y-%m-%d %H:%M:%S UTC')"

log_info "Committing changes: $COMMIT_MESSAGE"
git commit -m "$COMMIT_MESSAGE"

# Push to remote
log_info "Pushing to $BRANCH branch..."
git push "http://$TOKEN@git.homelab:3000/vitali/SigmaFlow-Svelte.git" "$BRANCH"

log_info "Deployment successful!"
echo "Application URL: (configure based on your hosting setup)"
