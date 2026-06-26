#!/bin/bash
set -e
echo "Initializing SPM project structure..."
mkdir -p src tests docs/spm/specs docs/spm/plans
echo "dirs: src/ tests/ docs/spm/" 
echo "To create WBS ledger: copy from references/task-ledger-template.md to docs/spm/ledger.md"
echo "Done."
