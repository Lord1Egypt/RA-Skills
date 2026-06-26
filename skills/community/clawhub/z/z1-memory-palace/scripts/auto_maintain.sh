#!/bin/bash
# BGE palace index auto-maintenance
# Runs: cold zone check → BGE index → graph router
# Called by LaunchAgent daily at 3 AM
set -e
cd /Users/zhouyi0415126.com/ai_matrix/vault/01_core
python3 scripts/watchdog/cold_zone_blinding_patch.py --quiet 2>/dev/null || true
python3 scripts/watchdog/build_index_bge.py
python3 scripts/watchdog/graph_router.py
