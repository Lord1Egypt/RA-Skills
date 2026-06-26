#!/bin/bash
# SPM Project Initializer
# Creates the standard SPM directory structure and copies templates
# Usage: bash scripts/init-spm.sh

set -e

echo "🚀 SPM Project Initializer"
echo "=========================="
echo ""

# Create directory structure
mkdir -p docs/spm/{ledgers,specs,plans,checkpoints}
mkdir -p .spm

# Copy WBS Ledger template if not exists
if [ ! -f docs/spm/ledger.md ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  TEMPLATE="$SCRIPT_DIR/../templates/wbs-ledger.md"
  if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" docs/spm/ledger.md
    echo "✅ docs/spm/ledger.md created from template"
  else
    # Create minimal ledger inline
    cat > docs/spm/ledger.md << 'LEDGEREOF'
# WBS Task Ledger — [Project Name]

## Task Summary
- Assignment: [one-line description]
- Outcome: [what working software looks like]
- Success criteria: [how we verify completion]

## WBS
| ID | Work Package | Dependencies | Context Brief | Exit Criteria | Evidence | Status |
|----|-------------|---------|---------------|---------------|----------|--------|
| 1  | Project setup | - | Cold-start: init project structure | Structure created, deps installed | Directory listing | todo |

## Mutation Log
| Time | Mutation Type | Affected IDs | Reason | New IDs |
|------|--------------|-------------|--------|---------|

## Active State
- Current item:
- Last completed:
- Last checkpoint:
- Resume from here:

## Heartbeat Log
| Time | Active | Completed | Evidence | Resume Point |
|------|--------|-----------|----------|-------------|

## Delivery Summary
[Final output mapping back to original assignment]
LEDGEREOF
    echo "✅ docs/spm/ledger.md created (minimal inline)"
  fi
else
  echo "⏭️  docs/spm/ledger.md already exists"
fi

echo ""
echo "📁 Structure created:"
echo "   docs/spm/"
echo "   ├── ledger.md           ← WBS Task Ledger"
echo "   ├── ledgers/             ← Multi-task ledgers"
echo "   ├── specs/                ← Design documents"
echo "   ├── plans/                ← Implementation plans"
echo "   └── checkpoints/          ← Phase checkpoints"
echo "   .spm/"
echo "   └── wbs-attestation       ← WBS integrity hash"

echo ""
echo "▶️  Next steps:"
echo "   1. Edit docs/spm/ledger.md with your project details"
echo "   2. Run: bash scripts/attest-wbs.sh     (secure your WBS)"
echo "   3. Start: /spm:start"
echo ""
echo "   Optional:"
echo "   - Enable checkpointing:  bash scripts/setup-checkpoints.sh"
echo "   - Multi-task:            bash scripts/switch-ledger.sh <name>"
