#!/usr/bin/env bash
# setup.sh — Initial setup for self-smarter-everyday skill
#
# Creates directory structure, initial config files, cron job, and verifies installation.
#
# Usage:
#   bash setup.sh [--skip-cron]
#
# This script is idempotent — safe to run multiple times.

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR="${HOME}/self-smarter"
STATE_DIR="${BASE_DIR}/state"
LOG_DIR="${BASE_DIR}/logs"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_SCHEDULE="0 2 * * *"  # 2:00 AM daily
CRON_CMD="python3 ${SCRIPT_DIR}/nightly_routine.py >> ${LOG_DIR}/cron.log 2>&1"
SKIP_CRON=false

# Parse arguments
for arg in "$@"; do
    case "$arg" in
        --skip-cron) SKIP_CRON=true ;;
        *) echo "Unknown argument: $arg"; exit 1 ;;
    esac
done

echo "============================================"
echo "  self-smarter-everyday — Setup"
echo "============================================"
echo ""

# ---------------------------------------------------------------------------
# Step 1: Create directory structure
# ---------------------------------------------------------------------------
echo "▶ Creating directory structure..."

DIRS=(
    "${BASE_DIR}"
    "${STATE_DIR}"
    "${STATE_DIR}/memory/hot"
    "${STATE_DIR}/memory/warm"
    "${STATE_DIR}/memory/cold"
    "${STATE_DIR}/memory/archive"
    "${STATE_DIR}/reflections"
    "${STATE_DIR}/prompts"
    "${LOG_DIR}"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
    echo "  ✓ ${dir}"
done

echo ""

# ---------------------------------------------------------------------------
# Step 2: Create initial config files
# ---------------------------------------------------------------------------
echo "▶ Creating initial config files..."

# State file
STATE_FILE="${STATE_DIR}/routine_state.json"
if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << 'STATEEOF'
{
  "last_run": null,
  "phase_results": {},
  "run_count": 0,
  "created": "SETUP_TIMESTAMP"
}
STATEEOF
    sed -i "s|SETUP_TIMESTAMP|$(date -Iseconds)|" "$STATE_FILE"
    echo "  ✓ routine_state.json"
else
    echo "  ⋯ routine_state.json (already exists, skipping)"
fi

# Initial prompt variant
PROMPT_INDEX="${STATE_DIR}/prompts/index.json"
if [ ! -f "$PROMPT_INDEX" ]; then
    cat > "$PROMPT_INDEX" << 'PROMPTEOF'
{
  "variants": [
    {
      "id": "v0_baseline",
      "name": "Baseline Prompt",
      "instructions": [
        "Analyze the task carefully before executing",
        "Break complex tasks into smaller steps",
        "Verify output before delivering",
        "Log lessons learned for future reference"
      ],
      "constraints": [
        "Stay within token budget",
        "Prefer cached data over external calls",
        "Validate all outputs against requirements"
      ],
      "generation": 0,
      "mutation": "original",
      "fitness": 0.5,
      "created": "SETUP_TIMESTAMP"
    }
  ],
  "generation": 0,
  "best_variant_id": "v0_baseline"
}
PROMPTEOF
    sed -i "s|SETUP_TIMESTAMP|$(date -Iseconds)|" "$PROMPT_INDEX"
    echo "  ✓ prompts/index.json (baseline variant)"
else
    echo "  ⋯ prompts/index.json (already exists, skipping)"
fi

# Memory sample entry
SAMPLE_MEMORY="${STATE_DIR}/memory/warm/sample_entry.json"
if [ ! -f "$SAMPLE_MEMORY" ]; then
    cat > "$SAMPLE_MEMORY" << 'MEMEOF'
{
  "id": "sample_entry",
  "content": "This is a sample memory entry. Replace with actual learned patterns.",
  "category": "general",
  "created": "SETUP_TIMESTAMP",
  "last_accessed": "SETUP_TIMESTAMP",
  "access_count": 0,
  "summary": "Sample entry for testing memory compaction"
}
MEMEOF
    sed -i "s|SETUP_TIMESTAMP|$(date -Iseconds)|g" "$SAMPLE_MEMORY"
    echo "  ✓ memory/warm/sample_entry.json"
else
    echo "  ⋯ memory/warm/sample_entry.json (already exists, skipping)"
fi

echo ""

# ---------------------------------------------------------------------------
# Step 3: Set up cron job
# ---------------------------------------------------------------------------
if [ "$SKIP_CRON" = true ]; then
    echo "▶ Skipping cron job setup (--skip-cron)"
else
    echo "▶ Setting up cron job (daily at 2:00 AM)..."

    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "nightly_routine.py"; then
        echo "  ⋯ Cron job already exists, skipping"
    else
        # Add cron job
        (crontab -l 2>/dev/null; echo "${CRON_SCHEDULE} ${CRON_CMD}") | crontab -
        echo "  ✓ Cron job added: ${CRON_SCHEDULE}"
    fi
fi

echo ""

# ---------------------------------------------------------------------------
# Step 4: Verify installation
# ---------------------------------------------------------------------------
echo "▶ Verifying installation..."

ERRORS=0

# Check Python3
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version 2>&1)
    echo "  ✓ Python3: ${PY_VERSION}"
else
    echo "  ✗ Python3 not found!"
    ERRORS=$((ERRORS + 1))
fi

# Check scripts exist
for script in nightly_routine.py self_audit.py memory_compact.py prompt_evolve.py; do
    if [ -f "${SCRIPT_DIR}/${script}" ]; then
        echo "  ✓ Script: ${script}"
    else
        echo "  ✗ Missing script: ${script}"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check directories
for dir in "${STATE_DIR}" "${LOG_DIR}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ Directory: ${dir}"
    else
        echo "  ✗ Missing directory: ${dir}"
        ERRORS=$((ERRORS + 1))
    fi
done

# Dry-run test
echo ""
echo "▶ Running dry-run test..."
if python3 "${SCRIPT_DIR}/nightly_routine.py" --dry-run --state-dir "${STATE_DIR}" 2>&1 | tail -3; then
    echo "  ✓ Dry-run completed successfully"
else
    echo "  ✗ Dry-run failed"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "============================================"
if [ $ERRORS -eq 0 ]; then
    echo "  ✓ Setup complete — all checks passed!"
else
    echo "  ✗ Setup complete with ${ERRORS} error(s)"
fi
echo "============================================"
echo ""
echo "Directory: ${BASE_DIR}"
echo "Scripts:   ${SCRIPT_DIR}"
echo "Cron:      ${CRON_SCHEDULE} (nightly at 2 AM)"
echo ""
echo "Manual run: python3 ${SCRIPT_DIR}/nightly_routine.py"
echo "Dry run:    python3 ${SCRIPT_DIR}/nightly_routine.py --dry-run"
