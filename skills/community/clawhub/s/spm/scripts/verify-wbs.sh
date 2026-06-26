#!/bin/bash
# SPM WBS Integrity Verification
# Compares stored hash against current WBS Ledger
# Returns 0 if valid, 1 if tampered
# Usage: bash scripts/verify-wbs.sh [ledger_path]

LEDGER="${1:-docs/spm/ledger.md}"
ATTEST_FILE=".spm/wbs-attestation"

# No attestation yet = first run, skip
if [ ! -f "$ATTEST_FILE" ]; then
  echo "⚠️  [SPM] No attestation found — run 'bash scripts/attest-wbs.sh' to create one"
  exit 0
fi

if [ ! -f "$LEDGER" ]; then
  echo "❌ [SPM] WBS Ledger not found: $LEDGER"
  exit 1
fi

STORED_HASH=$(head -1 "$ATTEST_FILE" | awk '{print $1}')
CURRENT_HASH=$(shasum -a 256 "$LEDGER" | awk '{print $1}')

if [ "$STORED_HASH" = "$CURRENT_HASH" ]; then
  echo "✅ [SPM] WBS integrity verified"
  exit 0
else
  echo ""
  echo "╔══════════════════════════════════════════╗"
  echo "║  🚨 [SPM] WBS TAMPERED                   ║"
  echo "╠══════════════════════════════════════════╣"
  echo "║  Stored:  $STORED_HASH"
  echo "║  Current: $CURRENT_HASH"
  echo "║                                          ║"
  echo "║  The WBS Ledger has been modified        ║"
  echo "║  since last attestation.                 ║"
  echo "║  Verify docs/spm/ledger.md manually.     ║"
  echo "║  Run 'bash scripts/attest-wbs.sh' to     ║"
  echo "║  re-attest after manual verification.    ║"
  echo "╚══════════════════════════════════════════╝"
  echo ""
  exit 1
fi
