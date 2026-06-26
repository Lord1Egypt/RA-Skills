#!/usr/bin/env bash
set -euo pipefail

# SkillGuard Safe Install — pre-install security audit wrapper for clawhub
# Usage: bash safe-install.sh [--force] <skill-name>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_SCRIPT="$SCRIPT_DIR/audit.sh"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

usage() {
  echo -e "${BOLD}🛡️  SkillGuard Safe Install${RESET}"
  echo ""
  echo -e "Usage: ${CYAN}bash safe-install.sh [--force] <skill-name>${RESET}"
  echo ""
  echo "  --force    Skip audit and install directly"
  echo ""
  exit 1
}

# Parse args
FORCE=false
SKILL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=true; shift ;;
    -h|--help) usage ;;
    -*) echo "Unknown option: $1"; usage ;;
    *) SKILL="$1"; shift ;;
  esac
done

[[ -z "$SKILL" ]] && usage

echo -e ""
echo -e "${BOLD}🛡️  SkillGuard Safe Install${RESET}"
echo -e "${DIM}────────────────────────────────────${RESET}"
echo -e "📦 Skill: ${CYAN}${SKILL}${RESET}"
echo ""

# Force mode — skip audit
if $FORCE; then
  echo -e "⚠️  ${YELLOW}--force mode: skipping security audit${RESET}"
  echo ""
  exec clawhub install "$SKILL"
fi

# Run audit
echo -e "🔍 Running security audit..."
echo ""

AUDIT_OUTPUT=$(bash "$AUDIT_SCRIPT" --name "$SKILL" 2>&1) || true

# Extract JSON (last line or last JSON block)
AUDIT_JSON=$(echo "$AUDIT_OUTPUT" | grep -E '^\{' | tail -1)

if [[ -z "$AUDIT_JSON" ]]; then
  # Try to get any JSON from output
  AUDIT_JSON=$(echo "$AUDIT_OUTPUT" | sed -n '/^{/,/^}/p' | tail -n +1)
fi

if [[ -z "$AUDIT_JSON" ]] || ! echo "$AUDIT_JSON" | jq . >/dev/null 2>&1; then
  echo -e "${YELLOW}⚠️  Could not parse audit result${RESET}"
  echo -e "${DIM}$AUDIT_OUTPUT${RESET}"
  echo ""
  read -rp "Install anyway? (y/n) " answer
  [[ "$answer" =~ ^[Yy] ]] && exec clawhub install "$SKILL"
  echo -e "❌ Installation cancelled."
  exit 1
fi

VERDICT=$(echo "$AUDIT_JSON" | jq -r '.verdict // "UNKNOWN"')
RISK_SCORE=$(echo "$AUDIT_JSON" | jq -r '.riskScore // -1')
THREATS=$(echo "$AUDIT_JSON" | jq -r '.threats // []')
THREAT_COUNT=$(echo "$THREATS" | jq 'length')

# Display result
case "$VERDICT" in
  SAFE)
    echo -e "✅ Verdict: ${GREEN}${BOLD}SAFE${RESET}"
    echo -e "📊 Risk Score: ${GREEN}${RISK_SCORE}/100${RESET}"
    ;;
  LOW_RISK)
    echo -e "✅ Verdict: ${GREEN}${BOLD}LOW RISK${RESET}"
    echo -e "📊 Risk Score: ${GREEN}${RISK_SCORE}/100${RESET}"
    ;;
  CAUTION)
    echo -e "⚠️  Verdict: ${YELLOW}${BOLD}CAUTION${RESET}"
    echo -e "📊 Risk Score: ${YELLOW}${RISK_SCORE}/100${RESET}"
    ;;
  DANGEROUS)
    echo -e "🚨 Verdict: ${RED}${BOLD}DANGEROUS${RESET}"
    echo -e "📊 Risk Score: ${RED}${RISK_SCORE}/100${RESET}"
    ;;
  *)
    echo -e "❓ Verdict: ${BOLD}${VERDICT}${RESET}"
    echo -e "📊 Risk Score: ${RISK_SCORE}/100"
    ;;
esac

# Show threats
if [[ "$THREAT_COUNT" -gt 0 ]]; then
  echo ""
  echo -e "${BOLD}🔎 Threats found (${THREAT_COUNT}):${RESET}"
  echo "$THREATS" | jq -r '.[] | if type == "string" then . else (.category // "unknown") + ": " + (.description // .severity // tostring) end' 2>/dev/null | while read -r t; do
    echo -e "   ${RED}•${RESET} $t"
  done
fi

echo -e "${DIM}────────────────────────────────────${RESET}"
echo ""

# Decision
case "$VERDICT" in
  SAFE|LOW_RISK)
    echo -e "✅ Skill looks safe. Installing..."
    echo ""
    exec clawhub install "$SKILL"
    ;;
  CAUTION)
    echo -e "${YELLOW}⚠️  This skill has potential risks.${RESET}"
    read -rp "Continue with installation? (y/n) " answer
    if [[ "$answer" =~ ^[Yy] ]]; then
      echo ""
      exec clawhub install "$SKILL"
    else
      echo -e "❌ Installation cancelled."
      exit 1
    fi
    ;;
  DANGEROUS)
    echo -e "${RED}${BOLD}🚫 DANGEROUS — Installation blocked.${RESET}"
    echo -e "${RED}This skill poses significant security risks.${RESET}"
    echo -e "${DIM}Use --force to override: bash safe-install.sh --force ${SKILL}${RESET}"
    exit 1
    ;;
  *)
    echo -e "${YELLOW}⚠️  Unknown verdict. Proceed with caution.${RESET}"
    read -rp "Install anyway? (y/n) " answer
    [[ "$answer" =~ ^[Yy] ]] && exec clawhub install "$SKILL"
    echo -e "❌ Installation cancelled."
    exit 1
    ;;
esac
