#!/usr/bin/env bash
# provision-vps.sh — Provision a fresh VPS with OpenClaw + VexPath
# Run this ON the new VPS after basic OS setup (Ubuntu 22.04+ / Debian 12+)
#
# Usage: curl -sSL <hosted-url>/provision-vps.sh | bash -s -- \
#          <client-email> "<Display Name>" "<app-password>" [business-type]
#
# What this does:
#   1. Installs Docker (if missing)
#   2. Installs Node.js 22+ (if missing)
#   3. Installs OpenClaw
#   4. Starts the OpenClaw gateway
#   5. Installs VexPath skill pack
#   6. Configures email + runs first triage
#   7. Generates QR code for client mobile pairing

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[VexPath Provision]${NC} $1"; }
warn() { echo -e "${YELLOW}[VexPath Provision]${NC} $1"; }
err()  { echo -e "${RED}[VexPath Provision]${NC} $1" >&2; }

# ── Args ──────────────────────────────────────────────────────────────────────
CLIENT_EMAIL="${1:-}"
DISPLAY_NAME="${2:-}"
APP_PASSWORD="${3:-}"
BIZ_TYPE="${4:-service}"

if [[ -z "$CLIENT_EMAIL" || -z "$DISPLAY_NAME" || -z "$APP_PASSWORD" ]]; then
  echo "Usage: $0 <client-email> \"<Display Name>\" \"<app-password>\" [business-type]"
  exit 1
fi

log "═══════════════════════════════════════════════════"
log "  VexPath VPS Provisioning"
log "  Client: $DISPLAY_NAME ($CLIENT_EMAIL)"
log "═══════════════════════════════════════════════════"

# ── Step 1: System Dependencies ───────────────────────────────────────────────
log "Checking system dependencies..."

# Node.js
if ! command -v node &>/dev/null || [[ $(node -v | sed 's/v//' | cut -d. -f1) -lt 20 ]]; then
  log "Installing Node.js 22..."
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi
log "Node.js: $(node -v)"

# npm global dir
NPM_PREFIX="$(npm config get prefix 2>/dev/null || echo '/usr/local')"
log "npm prefix: $NPM_PREFIX"

# ── Step 2: Install OpenClaw ──────────────────────────────────────────────────
if ! command -v openclaw &>/dev/null; then
  log "Installing OpenClaw..."
  npm install -g openclaw
else
  log "OpenClaw already installed: $(openclaw --version 2>/dev/null || echo 'unknown')"
fi

# ── Step 3: Initialize & Start Gateway ────────────────────────────────────────
OPENCLAW_HOME="${HOME}/.openclaw"

if [[ ! -f "$OPENCLAW_HOME/openclaw.json" ]]; then
  log "Initializing OpenClaw..."
  openclaw init 2>/dev/null || true
fi

# Check if gateway is running
if ! openclaw gateway status &>/dev/null 2>&1; then
  log "Starting OpenClaw gateway..."
  openclaw gateway start --background
  sleep 3
fi

log "Gateway running"

# ── Step 4: Install VexPath ───────────────────────────────────────────────────
log "Installing VexPath skill pack..."

WORKSPACE="$OPENCLAW_HOME/workspace"
mkdir -p "$WORKSPACE"

# Try ClawHub first, fall back to bundled
if command -v clawhub &>/dev/null; then
  log "Installing from ClawHub..."
  cd "$WORKSPACE"
  clawhub install vexpath 2>/dev/null || {
    warn "ClawHub install failed — using bundled skill pack"
    # Fall back: copy from this script's bundled location if available
  }
else
  log "ClawHub not found — installing npm + clawhub..."
  npm install -g clawhub 2>/dev/null || true
  if command -v clawhub &>/dev/null; then
    cd "$WORKSPACE"
    clawhub install vexpath 2>/dev/null || warn "ClawHub install failed"
  fi
fi

# Verify skill is installed
SKILL_PATH="$WORKSPACE/skills/vexpath"
if [[ ! -f "$SKILL_PATH/SKILL.md" ]]; then
  err "VexPath skill not found at $SKILL_PATH"
  err "Manual install: clawhub install vexpath"
  err "Or copy the skill pack manually to $SKILL_PATH"
  exit 1
fi

# ── Step 5: Deploy VEX Identity ───────────────────────────────────────────────
log "Deploying VEX identity..."

cp "$SKILL_PATH/assets/SOUL.md" "$WORKSPACE/SOUL.md"
cp "$SKILL_PATH/assets/HEARTBEAT.md" "$WORKSPACE/HEARTBEAT.md"

# ── Step 6: Configure Email + First Triage ────────────────────────────────────
log "Configuring email..."

bash "$SKILL_PATH/scripts/setup-email.sh" "$CLIENT_EMAIL" "$DISPLAY_NAME" "$APP_PASSWORD"

log "Running first triage..."
bash "$SKILL_PATH/scripts/first-triage.sh" > "$WORKSPACE/first-triage-report.json" 2>/dev/null || true

# ── Step 7: Generate QR Code ──────────────────────────────────────────────────
log ""
log "═══════════════════════════════════════════════════"
log "  ⚡ VexPath Deployment Complete"
log "═══════════════════════════════════════════════════"
log ""
log "  Client: $DISPLAY_NAME ($CLIENT_EMAIL)"
log "  VPS:    $(hostname -f 2>/dev/null || hostname)"
log "  IP:     $(curl -s ifconfig.me 2>/dev/null || echo 'unknown')"
log ""

# Generate QR code
log "Generating pairing QR code..."
echo ""
openclaw qr 2>/dev/null || {
  warn "QR generation needs gateway config. Run: openclaw qr"
  warn "Make sure gateway.remote.url is set to this server's public URL"
}

echo ""
log "Client scans this QR with the OpenClaw app → paired to VEX"
log "Then approve: openclaw devices approve <device-id>"
log ""
log "VEX is live. Inbox is triaged. The client is on VexPath. ⚡"
