#!/usr/bin/env bash
# setup-checkpoints.sh — Initialize Checkpoint and Checklist templates in the current project
#
# Run this in an SPM project root to enable the Checkpoint + Checklist system.
#
# Usage:
#   cd /path/to/spm-project
#   bash skills/spm/scripts/setup-checkpoints.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(pwd)"

echo "=== SPM Checkpoint & Checklist Setup ==="
echo ""

# Create directories
mkdir -p "$PROJECT_ROOT/CHECKPOINTS"
mkdir -p "$PROJECT_ROOT/CHECKLISTS"
mkdir -p "$PROJECT_ROOT/docs/checkpoints"
mkdir -p "$PROJECT_ROOT/docs/checklists"

# Copy templates from skill repo if different locations
# (In a real installed skill, templates are in the skill directory)
# Here we assume they're already in the project CHECKPOINTS/ and CHECKLISTS/ if script is run from there

if [[ -d "$SCRIPT_DIR/../CHECKPOINTS" ]]; then
  cp -r "$SCRIPT_DIR/../CHECKPOINTS/"* "$PROJECT_ROOT/CHECKPOINTS/"
  echo "✓ Checkpoint templates installed to CHECKPOINTS/"
else
  echo "⚠ No CHECKPOINTS templates found in skill directory — you may need to add them manually"
fi

if [[ -d "$SCRIPT_DIR/../CHECKLISTS" ]]; then
  cp -r "$SCRIPT_DIR/../CHECKLISTS/"* "$PROJECT_ROOT/CHECKLISTS/"
  echo "✓ Checklist templates installed to CHECKLISTS/"
else
  echo "⚠ No CHECKLISTS templates found in skill directory — you may need to add them manually"
fi

# Create verification script if not exists
if [[ ! -f "$PROJECT_ROOT/scripts/verify_checklists.py" ]]; then
  cp "$SCRIPT_DIR/verify_checklists.py" "$PROJECT_ROOT/scripts/"
  chmod +x "$PROJECT_ROOT/scripts/verify_checklists.py"
  echo "✓ verify_checklists.py installed"
fi

# Create checkpoint runner if not exists
if [[ ! -f "$PROJECT_ROOT/scripts/checkpoint.sh" ]]; then
  cp "$SCRIPT_DIR/checkpoint.sh" "$PROJECT_ROOT/scripts/"
  chmod +x "$PROJECT_ROOT/scripts/checkpoint.sh"
  echo "✓ checkpoint.sh installed"
fi

# Create E2E script if not exists (Phase 2)
if [[ ! -f "$PROJECT_ROOT/scripts/e2e.sh" ]]; then
  cp "$SCRIPT_DIR/e2e.sh" "$PROJECT_ROOT/scripts/"
  chmod +x "$PROJECT_ROOT/scripts/e2e.sh"
  echo "✓ e2e.sh installed"
fi

# Create contract generation/validation scripts if not exists (Phase 2)
for script in generate.sh validate_contract.sh; do
  if [[ ! -f "$PROJECT_ROOT/scripts/$script" ]]; then
    cp "$SCRIPT_DIR/$script" "$PROJECT_ROOT/scripts/"
    chmod +x "$PROJECT_ROOT/scripts/$script"
    echo "✓ $script installed"
  fi
done

# Add npm scripts to package.json if node project
if [[ -f "$PROJECT_ROOT/package.json" ]]; then
  node -e '
    const fs = require("fs");
    const p = JSON.parse(fs.readFileSync("package.json", "utf8"));
    p.scripts = Object.assign({}, p.scripts, {
      "e2e": "bash scripts/e2e.sh",
      "generate:contract": "bash scripts/generate.sh",
      "validate:contract": "bash scripts/validate_contract.sh",
      "verify:checklists": "python3 scripts/verify_checklists.py all",
      "verify:code": "python3 scripts/verify_checklists.py code",
      "verify:deploy": "python3 scripts/verify_checklists.py deploy",
      "checkpoint": "bash scripts/checkpoint.sh"
    });
    fs.writeFileSync("package.json", JSON.stringify(p, null, 2) + "\n");
    console.log("✓ npm scripts added: e2e, generate:contract, validate:contract, verify:checklists, verify:code, verify:deploy, checkpoint");
  '
else
  echo "⚠ No package.json found — skipping npm script setup"
fi

# Create docs/checkpoints and docs/checklists dirs if not exist (for generated reports)
mkdir -p "$PROJECT_ROOT/docs/checkpoints"
mkdir -p "$PROJECT_ROOT/docs/checklists"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. For Phase 1: run './scripts/checkpoint.sh phase-1' after writing docs/requirements.md"
echo "  2. For code completion: run 'npm run verify:code' before requesting review"
echo "  3. For deployment: run 'npm run verify:deploy' and ensure all green"
echo ""
echo "Generated checkpoint reports will appear in docs/checkpoints/"
echo "Checklist verification report: docs/checklists/verification-report.json"
