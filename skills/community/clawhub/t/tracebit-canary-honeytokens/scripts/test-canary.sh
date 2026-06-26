#!/usr/bin/env bash
# test-canary.sh — Trigger a Tracebit canary to test the alert pipeline
#
# Usage:
#   bash skills/tracebit-canaries/scripts/test-canary.sh           # interactive
#   bash skills/tracebit-canaries/scripts/test-canary.sh ssh       # SSH canary (fastest)
#   bash skills/tracebit-canaries/scripts/test-canary.sh aws       # AWS canary
#   bash skills/tracebit-canaries/scripts/test-canary.sh cookie    # Cookie canary
#   bash skills/tracebit-canaries/scripts/test-canary.sh email     # Email canary
#
# Expected outcome: alert email in your inbox within 1–15 minutes (SSH is fastest)

set -euo pipefail

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[test-canary]${NC} $*"; }
success() { echo -e "${GREEN}[test-canary]${NC} $*"; }
warn()    { echo -e "${YELLOW}[test-canary]${NC} $*"; }
die()     { echo -e "${RED}[test-canary] ERROR:${NC} $*" >&2; exit 1; }

# ── Check CLI installed ───────────────────────────────────────────────────────
if ! command -v tracebit >/dev/null 2>&1; then
  die "Tracebit CLI not installed. Run: bash skills/tracebit-canaries/scripts/install-tracebit.sh"
fi

# ── Check canaries are deployed ───────────────────────────────────────────────
info "Verifying canaries are deployed..."
if ! tracebit show >/dev/null 2>&1; then
  warn "Could not verify canary status. Proceeding anyway."
fi

# ── Canary type ───────────────────────────────────────────────────────────────
TYPE="${1:-}"

if [[ -z "$TYPE" ]]; then
  echo ""
  echo "Which canary type do you want to trigger?"
  echo ""
  echo "  ssh              Fastest — alert in ~1–3 minutes"
  echo "  aws              Slower  — alert in ~5–15 minutes (CloudTrail latency)"
  echo "  cookie           Alert in ~1–5 minutes"
  echo "  username-password Alert in ~1–5 minutes"
  echo "  email            Near-instant alert"
  echo "  all              Trigger all types"
  echo ""
  read -r -p "Type [ssh]: " TYPE
  TYPE="${TYPE:-ssh}"
fi

echo ""
info "Triggering $TYPE canary..."
echo ""

# ── Trigger ───────────────────────────────────────────────────────────────────
case "$TYPE" in
  all)
    tracebit trigger
    ;;
  ssh | aws | cookie | username-password | email)
    tracebit trigger "$TYPE"
    ;;
  *)
    warn "Unknown type '$TYPE'. Running interactive trigger."
    tracebit trigger
    ;;
esac

echo ""
success "Canary trigger sent."

# ── Expected outcomes ─────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Expected alert timing:"
case "$TYPE" in
  email)
    echo "  📧 Email canary: near-instant (within ~1 minute)"
    ;;
  ssh)
    echo "  🔑 SSH canary: ~1–3 minutes"
    ;;
  cookie | username-password)
    echo "  🍪 Cookie/password canary: ~1–5 minutes"
    ;;
  aws)
    echo "  ☁️  AWS canary: ~5–15 minutes (CloudTrail processing delay)"
    ;;
  all)
    echo "  SSH: ~1–3 min  |  Email: ~1 min  |  AWS: ~5–15 min"
    ;;
esac
echo ""
echo "  Watch for:"
echo "  1. Alert email in your inbox (check spam folder too)"
echo "  2. Heartbeat detects alert → agent investigates"
echo "  3. Notification in your messaging channel"
echo ""
echo "  Manual verification:"
echo "    tracebit show          — check dashboard for recent alerts"
echo "    tracebit portal        — open web dashboard"
echo "    check HEARTBEAT.md     — verify heartbeat alert check is configured"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
