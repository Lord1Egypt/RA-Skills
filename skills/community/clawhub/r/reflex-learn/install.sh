#!/usr/bin/env bash
# ReflexLearn install.sh
# ─────────────────────────────────────────────────────────────────────────────
# This script performs ALL network operations required by ReflexLearn in one
# declared, user-visible step. After this script completes, the skill can run
# fully offline with --offline flag.
#
# Network operations performed:
#   1. pip install — pulls packages from PyPI:
#        sentence-transformers, numpy, huggingface-hub
#   2. Model pre-cache — downloads ~80 MB of weights from Hugging Face:
#        sentence-transformers/all-MiniLM-L6-v2
#
# No further network calls are made at runtime when --offline is set.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

MODEL="sentence-transformers/all-MiniLM-L6-v2"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║           ReflexLearn — Install Script               ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "This script will:"
echo "  1. Install Python packages from PyPI (sentence-transformers, numpy, huggingface-hub)"
echo "  2. Download model weights from Hugging Face (~80 MB, one-time only)"
echo ""
read -r -p "Proceed? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# ── Step 1: Install Python dependencies ──────────────────────────────────────
echo ""
echo "▶ Step 1/2: Installing Python dependencies..."
pip install --quiet -r "$SKILL_DIR/requirements.txt"
echo "  ✓ Dependencies installed."

# ── Step 2: Pre-cache model weights ──────────────────────────────────────────
echo ""
echo "▶ Step 2/2: Pre-caching model weights from Hugging Face..."
echo "  Model : $MODEL"
echo "  Size  : ~80 MB (downloaded once, cached in ~/.cache/huggingface/)"
echo ""
python3 - <<'PYEOF'
from sentence_transformers import SentenceTransformer
import sys
print("  Downloading/verifying model weights...")
model = SentenceTransformer("all-MiniLM-L6-v2")
# Quick smoke test to confirm the model works
test_emb = model.encode("test", convert_to_numpy=True)
assert test_emb.shape[0] == 384, "Unexpected embedding dimension"
print("  ✓ Model cached and verified (embedding dim=384).")
PYEOF

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  Installation complete. ReflexLearn is ready.        ║"
echo "║                                                      ║"
echo "║  Run with --offline to prevent any further network   ║"
echo "║  access at runtime:                                  ║"
echo "║    python3 reflex_learn.py --query '...' --offline   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
