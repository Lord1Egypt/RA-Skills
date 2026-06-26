#!/usr/bin/env bash
# deploy-client.sh — Full VexPath client deployment script
# Deploys VexPath on a fresh or existing OpenClaw instance
#
# Usage: ./deploy-client.sh <client-email> "<Display Name>" "<app-password>" [business-type]
# Business types: agency | service | ecommerce | local | saas
#
# This script:
#   1. Installs VexPath skill pack into the OpenClaw workspace
#   2. Deploys VEX identity (SOUL.md + HEARTBEAT.md)
#   3. Configures email via himalaya
#   4. Runs first inbox triage
#   5. Outputs QR pairing instructions

set -euo pipefail

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[VexPath]${NC} $1"; }
warn() { echo -e "${YELLOW}[VexPath]${NC} $1"; }
err()  { echo -e "${RED}[VexPath]${NC} $1" >&2; }

# ── Args ──────────────────────────────────────────────────────────────────────
if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <client-email> \"<Display Name>\" \"<app-password>\" [business-type]"
  echo "Business types: agency | service | ecommerce | local | saas"
  exit 1
fi

CLIENT_EMAIL="$1"
DISPLAY_NAME="$2"
APP_PASSWORD="$3"
BIZ_TYPE="${4:-service}"

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-${HOME}/.openclaw/workspace}"

log "Starting VexPath deployment for: $CLIENT_EMAIL"
log "Business type: $BIZ_TYPE"
log "Workspace: $WORKSPACE"

# ── Step 1: Install VexPath Skill Pack ────────────────────────────────────────
log "Step 1/5: Installing VexPath skill pack..."

SKILL_DEST="${WORKSPACE}/skills/vexpath"
if [[ -d "$SKILL_DEST" ]]; then
  warn "VexPath skill already exists at $SKILL_DEST — updating..."
  rm -rf "$SKILL_DEST"
fi

mkdir -p "$SKILL_DEST"
cp -r "$SKILL_DIR/SKILL.md" "$SKILL_DEST/"
cp -r "$SKILL_DIR/references" "$SKILL_DEST/" 2>/dev/null || true
cp -r "$SKILL_DIR/scripts" "$SKILL_DEST/" 2>/dev/null || true
cp -r "$SKILL_DIR/assets" "$SKILL_DEST/" 2>/dev/null || true
chmod +x "$SKILL_DEST/scripts/"*.sh 2>/dev/null || true

log "Skill pack installed at: $SKILL_DEST"

# ── Step 2: Deploy VEX Identity ───────────────────────────────────────────────
log "Step 2/5: Deploying VEX identity..."

# SOUL.md — only deploy if not already customized
if [[ -f "$WORKSPACE/SOUL.md" ]]; then
  warn "SOUL.md exists — backing up to SOUL.md.backup"
  cp "$WORKSPACE/SOUL.md" "$WORKSPACE/SOUL.md.backup"
fi
cp "$SKILL_DIR/assets/SOUL.md" "$WORKSPACE/SOUL.md"

# HEARTBEAT.md
if [[ -f "$WORKSPACE/HEARTBEAT.md" ]]; then
  warn "HEARTBEAT.md exists — backing up to HEARTBEAT.md.backup"
  cp "$WORKSPACE/HEARTBEAT.md" "$WORKSPACE/HEARTBEAT.md.backup"
fi
cp "$SKILL_DIR/assets/HEARTBEAT.md" "$WORKSPACE/HEARTBEAT.md"

log "VEX identity deployed (SOUL.md + HEARTBEAT.md)"

# ── Step 3: Configure Email ───────────────────────────────────────────────────
log "Step 3/5: Configuring email..."

bash "$SKILL_DIR/scripts/setup-email.sh" "$CLIENT_EMAIL" "$DISPLAY_NAME" "$APP_PASSWORD"

if [[ $? -eq 0 ]]; then
  log "Email configured successfully"
else
  err "Email setup failed — check credentials and try again"
  err "See: $SKILL_DEST/references/gmail-setup.md for troubleshooting"
  exit 1
fi

# ── Step 4: Run First Triage ──────────────────────────────────────────────────
log "Step 4/5: Running first inbox triage..."

TRIAGE_OUTPUT=$(bash "$SKILL_DIR/scripts/first-triage.sh" 2>/dev/null) || true

if [[ -n "$TRIAGE_OUTPUT" ]]; then
  TRIAGE_FILE="$WORKSPACE/first-triage-report.json"
  echo "$TRIAGE_OUTPUT" > "$TRIAGE_FILE"
  log "Triage complete — report saved to: $TRIAGE_FILE"
else
  warn "Triage returned no data — inbox may be empty or script needs manual run"
fi

# ── Step 5: QR Pairing Setup ─────────────────────────────────────────────────
log "Step 5/5: Preparing mobile access..."

echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  VexPath Deployment Complete ⚡${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  Client:        ${GREEN}$DISPLAY_NAME${NC} ($CLIENT_EMAIL)"
echo -e "  Business Type: ${GREEN}$BIZ_TYPE${NC}"
echo -e "  Skill Pack:    ${GREEN}$SKILL_DEST${NC}"
echo -e "  Email:         ${GREEN}Connected${NC}"
echo ""
echo -e "${YELLOW}  📱 Mobile Pairing:${NC}"
echo -e "  To connect the client's phone to VEX, run:"
echo ""
echo -e "    ${CYAN}openclaw qr${NC}"
echo ""
echo -e "  This generates a QR code the client scans with the"
echo -e "  OpenClaw mobile app (iOS/Android) to pair their device."
echo -e "  Once paired, they talk to VEX directly from their phone."
echo ""
echo -e "${YELLOW}  🔑 After pairing, approve the device:${NC}"
echo ""
echo -e "    ${CYAN}openclaw devices list${NC}        # see pending requests"
echo -e "    ${CYAN}openclaw devices approve <id>${NC} # approve the client"
echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo ""
log "VexPath is live. VEX is ready to triage."
