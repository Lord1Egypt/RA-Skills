#!/bin/bash
# SPM WBS Attestation Script
# Generates SHA-256 hash of WBS Ledger for integrity verification
# Usage: bash scripts/attest-wbs.sh [ledger_path]

set -e

LEDGER="${1:-docs/spm/ledger.md}"
ATTEST_DIR=".spm"
ATTEST_FILE="$ATTEST_DIR/wbs-attestation"

if [ ! -f "$LEDGER" ]; then
  echo "❌ [SPM] WBS Ledger not found: $LEDGER"
  echo "   Run: bash scripts/init-spm.sh first"
  exit 1
fi

# Ensure attestation directory exists
mkdir -p "$ATTEST_DIR"

# Calculate SHA-256
HASH=$(shasum -a 256 "$LEDGER" | awk '{print $1}')
TIMESTAMP=$(date -u +%s)

# Store hash + timestamp
echo "$HASH $TIMESTAMP" > "$ATTEST_FILE"

# Also store a human-readable log
echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] attested: $HASH" >> "$ATTEST_DIR/attestation.log"

echo "✅ [SPM] WBS attested"
echo "   Hash:  $HASH"
echo "   Time:  $(date)"
echo "   Stored: $ATTEST_FILE"
echo ""
echo "   Next: Your WBS Ledger is now protected."
echo "   Any modification will be detected by verify-wbs.sh."
