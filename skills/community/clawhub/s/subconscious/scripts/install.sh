#!/bin/bash
# Subconscious Skill Installer — Universal (any OpenClaw workspace)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Auto-detect workspace: find the openclaw workspace dir
# Walk up from skill dir: subconscious/ -> skills/ -> ~/.openclaw/ -> any dir with memory/
_detect_workspace() {
    local _parent="$(dirname "$(dirname "$SKILL_DIR")")"  # ~/.openclaw/
    for _candidate in "$_parent"/*; do
        if [ -d "$_candidate/memory" ]; then
            echo "$_candidate"
            return 0
        fi
    done
    echo "$_parent/workspace-alfred"  # fallback
}

WORKSPACE_DIR="${SUBCONSCIOUS_WORKSPACE:-$(_detect_workspace)}"
MEMORY_DIR="$WORKSPACE_DIR/memory/subconscious"
LOGS_DIR="$WORKSPACE_DIR/logs"

echo "=== Subconscious Skill Installer ==="
echo "Skill dir: $SKILL_DIR"
echo "Workspace dir: $WORKSPACE_DIR"
echo "Memory dir: $MEMORY_DIR"
echo

# Validate workspace
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "Error: Workspace not found at $WORKSPACE_DIR"
    echo "Set SUBCONSCIOUS_WORKSPACE env var to specify a different workspace."
    exit 1
fi

if [ ! -d "$WORKSPACE_DIR/memory" ]; then
    echo "Error: $WORKSPACE_DIR does not look like an OpenClaw workspace (no memory/ dir)"
    exit 1
fi

# Step 1: Create memory directory and initialize store if needed
echo "[1/5] Setting up memory store at $MEMORY_DIR..."
mkdir -p "$MEMORY_DIR/snapshots"

if [ ! -f "$MEMORY_DIR/core.json" ]; then
    echo '{"version": "1.5", "items": []}' > "$MEMORY_DIR/core.json"
    echo "  Created core.json"
fi

if [ ! -f "$MEMORY_DIR/live.json" ]; then
    echo '{"version": "1.5", "items": []}' > "$MEMORY_DIR/live.json"
    echo "  Created live.json"
fi

if [ ! -f "$MEMORY_DIR/pending.jsonl" ]; then
    touch "$MEMORY_DIR/pending.jsonl"
    echo "  Created pending.jsonl"
fi

echo "  Memory store ready."

# Step 2: Install self-improving-agent hooks (optional — requires confirmation)
echo "[2/5] Hooks setup..."
if [ -d "$SKILL_DIR/self-improving-agent/hooks/openclaw" ]; then
    echo "  self-improving-agent hooks found at $SKILL_DIR/self-improving-agent/hooks/openclaw"
    echo "  NOTE: These are DISABLED by default. To enable, copy hooks to your OpenClaw hooks directory manually."
    echo "  Hooks include: sessions_history, sessions_send, sessions_spawn — review before enabling."
fi

# Step 3: Install cron jobs
echo "[3/5] Installing cron jobs..."

_tick_cmd="cd $SKILL_DIR/scripts && python3 subconscious_metabolism.py tick"
_rotate_cmd="cd $SKILL_DIR/scripts && python3 subconscious_metabolism.py rotate --enable-promotion"
_review_cmd="cd $SKILL_DIR/scripts && python3 subconscious_metabolism.py review"
_bench_cmd="cd $SKILL_DIR/scripts && python3 subconscious_benchmark.py"

# Tick every 5 minutes
( crontab -l 2>/dev/null | grep -v "subconscious_metabolism.py tick"; \
  echo "*/5 * * * * $_tick_cmd >> $LOGS_DIR/subconscious_tick.log 2>&1" \
) | crontab -

# Rotate every hour (with promotion)
( crontab -l 2>/dev/null | grep -v "subconscious_metabolism.py rotate"; \
  echo "0 * * * * $_rotate_cmd >> $LOGS_DIR/subconscious_rotate.log 2>&1" \
) | crontab -

# Daily review at 6am
( crontab -l 2>/dev/null | grep -v "subconscious_metabolism.py review"; \
  echo "0 6 * * * $_review_cmd >> $LOGS_DIR/subconscious_review.log 2>&1" \
) | crontab -

# Weekly benchmark Monday 9am
( crontab -l 2>/dev/null | grep -v "subconscious_benchmark"; \
  echo "0 9 * * 1 $_bench_cmd >> $LOGS_DIR/subconscious_benchmark.log 2>&1" \
) | crontab -

echo "  Cron jobs installed."
echo "  NOTE: --enable-promotion means items auto-promote to live. Remove this flag if you want manual-only promotion."

# Step 4: Create logs directory
echo "[4/5] Creating logs directory..."
mkdir -p "$LOGS_DIR"
touch "$LOGS_DIR/subconscious_tick.log"
touch "$LOGS_DIR/subconscious_rotate.log"
touch "$LOGS_DIR/subconscious_review.log"
touch "$LOGS_DIR/subconscious_benchmark.log"
echo "  Logs ready."

# Step 5: Verify installation
echo "[5/5] Verifying installation..."
cd "$SKILL_DIR/scripts"
SUBCONSCIOUS_WORKSPACE="$WORKSPACE_DIR" python3 subconscious_metabolism.py status
echo
echo "=== Installation complete ==="
echo
echo "Workspace: $WORKSPACE_DIR"
echo "Memory: $MEMORY_DIR"
echo
echo "IMPORTANT:"
echo "  - Cron jobs are ACTIVE (tick/rotate/review/benchmark)"
echo "  - --enable-promotion is set on rotate — items auto-promote to live"
echo "  - To disable auto-promotion: crontab -e and remove --enable-promotion from hourly cron"
echo "  - Hooks in self-improving-agent/ are DISABLED by default"
echo
echo "Run these to check:"
echo "  SUBCONSCIOUS_WORKSPACE=$WORKSPACE_DIR python3 $SKILL_DIR/scripts/subconscious_metabolism.py status"
echo "  SUBCONSCIOUS_WORKSPACE=$WORKSPACE_DIR python3 $SKILL_DIR/scripts/subconscious_cli.py bias"
