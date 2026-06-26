#!/usr/bin/env bash
# rules-of-the-claw installer
# Installs production-grade security rules for OpenClaw Guardian
#
# Requires: Node.js v18+

set -euo pipefail

GUARDIAN_DIR="${HOME}/.openclaw/extensions/guardian"
RULES_FILE="${GUARDIAN_DIR}/guardian-rules.json"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_RULES="${SKILL_DIR}/rules-of-the-claw.json"
BACKUP_FILE="${RULES_FILE}.bak.$(date +%Y%m%d_%H%M%S)"

echo ""
echo "🛡️  rules-of-the-claw installer"
echo "================================"
echo ""

# Step 0: Check Node.js is available
if ! command -v node &>/dev/null; then
  echo "❌ Node.js is required but not found."
  echo "   Install Node.js v18+ from https://nodejs.org/"
  exit 1
fi

# Step 1: Check Guardian is installed
if [ ! -d "${GUARDIAN_DIR}" ]; then
  echo "❌ Guardian plugin not found at: ${GUARDIAN_DIR}"
  echo ""
  echo "Install Guardian first:"
  echo "  clawhub install openclaw-guardian"
  echo "  # or follow: https://github.com/fatcatMaoFei/openclaw-guardian"
  echo ""
  echo "Then re-run this installer."
  exit 1
fi

echo "✅ Guardian plugin found at: ${GUARDIAN_DIR}"

# Step 2: Backup existing rules if present
if [ -f "${RULES_FILE}" ]; then
  echo "📦 Backing up existing rules to: ${BACKUP_FILE}"
  cp "${RULES_FILE}" "${BACKUP_FILE}"
  echo "   Backup saved."
else
  echo "ℹ️  No existing rules file found — fresh install."
fi

# Step 3: Install new rules
echo ""
echo "📥 Installing rules-of-the-claw..."
cp "${SOURCE_RULES}" "${RULES_FILE}"

# Step 4: Validate JSON and count rules
echo ""
echo "🔍 Validating installed rules..."

RULE_COUNT=$(node -e "
const fs = require('fs');
try {
  const rules = JSON.parse(fs.readFileSync('${RULES_FILE}', 'utf8'));
  if (!Array.isArray(rules)) { console.log('ERROR:expected JSON array'); process.exit(1); }
  const enabled = rules.filter(r => r.enabled !== false).length;
  console.log(rules.length + ':' + enabled);
} catch (e) {
  console.log('JSON_ERROR:' + e.message);
  process.exit(1);
}
")

if [[ "${RULE_COUNT}" == JSON_ERROR* ]] || [[ "${RULE_COUNT}" == ERROR* ]]; then
  echo "❌ JSON validation failed: ${RULE_COUNT}"
  echo "   Restoring backup..."
  if [ -f "${BACKUP_FILE}" ]; then
    cp "${BACKUP_FILE}" "${RULES_FILE}"
    echo "   Backup restored."
  fi
  exit 1
fi

TOTAL=$(echo "${RULE_COUNT}" | cut -d: -f1)
ENABLED=$(echo "${RULE_COUNT}" | cut -d: -f2)

# Step 4b: Validate all regex patterns compile
echo ""
echo "🔍 Validating regex patterns..."

REGEX_RESULT=$(node -e "
const fs = require('fs');
try {
  const rules = JSON.parse(fs.readFileSync('${RULES_FILE}', 'utf8'));
  const broken = [];
  for (const r of rules) {
    try {
      const p = r.pattern.replace(/\(\?[imsx]+\)/g, '');
      new RegExp(p);
    } catch (e) { broken.push(r.id + ': ' + e.message); }
    if (r.exclude) {
      try {
        const e = r.exclude.replace(/\(\?[imsx]+\)/g, '');
        new RegExp(e);
      } catch (e) { broken.push(r.id + ' (exclude): ' + e.message); }
    }
  }
  if (broken.length > 0) {
    broken.forEach(b => console.error('REGEX_ERROR:' + b));
    process.exit(1);
  }
  console.log('OK');
} catch (e) {
  console.log('REGEX_ERROR:' + e.message);
  process.exit(1);
}
")

if [[ "${REGEX_RESULT}" == REGEX_ERROR* ]]; then
  echo "❌ Regex validation failed:"
  echo "   ${REGEX_RESULT}"
  echo "   Restoring backup..."
  if [ -f "${BACKUP_FILE}" ]; then
    cp "${BACKUP_FILE}" "${RULES_FILE}"
    echo "   Backup restored."
  fi
  exit 1
fi

echo "   All regex patterns compile successfully."

echo ""
echo "✅ Installation complete!"
echo ""
echo "   Rules installed : ${TOTAL}"
echo "   Rules enabled   : ${ENABLED}"
echo "   Rules disabled  : $((TOTAL - ENABLED))"
echo "   Location        : ${RULES_FILE}"
if [ -f "${BACKUP_FILE}" ]; then
  echo "   Backup at       : ${BACKUP_FILE}"
fi
echo ""
echo "🔧 Customize by editing: ${RULES_FILE}"
echo "   - Replace your_app with your app name in DB/Docker rules"
echo "   - Replace YOUR_ORG with your GitHub org in git remote rules"
echo "   - Replace YOUR_OWNER with your name in block messages"
echo "   - Set \"enabled\": false on rules you don't need"
echo ""
echo "📖 Docs: https://github.com/bahuleyandr/rules-of-the-claw"
echo ""
