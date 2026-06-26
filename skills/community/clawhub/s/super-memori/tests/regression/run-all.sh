#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
python3 tests/test_temporal_retrieval.py
python3 tests/test_relation_target_validation.py
python3 tests/test_repair_plan.py
python3 tests/test_semantic_unbuilt_state.py
python3 tests/test_promotion_candidates.py
python3 tests/test_hot_change_buffer.py
python3 tests/test_startup_self_check_surface.py
