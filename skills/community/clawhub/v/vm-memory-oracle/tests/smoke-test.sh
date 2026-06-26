#!/bin/bash
# VM Memory Oracle — Smoke Test Suite
# Run after installation to verify the memory system is functional.
# Exit codes: 0 = all tests pass, 1 = failure
#
# Usage: bash smoke-test.sh [data_path]
# Default data_path: /data/memory

set -euo pipefail

DATA_PATH="${1:-/data/memory}"
PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" = "true" ]; then
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== VM Memory Oracle Smoke Tests ==="
echo "Host: $(hostname)"
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Data path: $DATA_PATH"
echo ""

# --- Section 1: Directory Structure ---
echo "[1/5] Directory structure"
run_test "Data path exists" "$([ -d "$DATA_PATH" ] && echo true || echo false)"
run_test "knowledge-graph/ exists" "$([ -d "$DATA_PATH/knowledge-graph" ] && echo true || echo false)"
run_test "embeddings/ exists" "$([ -d "$DATA_PATH/embeddings" ] && echo true || echo false)"
run_test "daily/ exists" "$([ -d "$DATA_PATH/daily" ] && echo true || echo false)"
run_test "sessions/ exists" "$([ -d "$DATA_PATH/sessions" ] && echo true || echo false)"
echo ""

# --- Section 2: Core Files ---
echo "[2/5] Core files"
run_test "activation-metadata.json exists" "$([ -f "$DATA_PATH/activation-metadata.json" ] && echo true || echo false)"
run_test "MEMORY.md exists" "$([ -f "$DATA_PATH/MEMORY.md" ] && echo true || echo false)"
run_test "health.json exists" "$([ -f "$DATA_PATH/health.json" ] && echo true || echo false)"

# Validate JSON files are parseable
if [ -f "$DATA_PATH/activation-metadata.json" ]; then
    run_test "activation-metadata.json is valid JSON" "$(jq empty "$DATA_PATH/activation-metadata.json" 2>/dev/null && echo true || echo false)"
else
    run_test "activation-metadata.json is valid JSON" "false"
fi

if [ -f "$DATA_PATH/health.json" ]; then
    run_test "health.json is valid JSON" "$(jq empty "$DATA_PATH/health.json" 2>/dev/null && echo true || echo false)"
else
    run_test "health.json is valid JSON" "false"
fi
echo ""

# --- Section 3: Disk Mount ---
echo "[3/5] Disk mount"
run_test "Data path is a mount point" "$(mountpoint -q "$DATA_PATH" 2>/dev/null && echo true || echo false)"
DISK_USAGE=$(df "$DATA_PATH" --output=pcent 2>/dev/null | tail -1 | tr -d ' %' || echo "0")
run_test "Disk usage below 90%" "$([ "$DISK_USAGE" -lt 90 ] && echo true || echo false)"
echo "  Info: Disk usage at ${DISK_USAGE}%"
echo ""

# --- Section 4: File Permissions ---
echo "[4/5] File permissions"
run_test "Data path is writable" "$([ -w "$DATA_PATH" ] && echo true || echo false)"
run_test "knowledge-graph/ is writable" "$([ -w "$DATA_PATH/knowledge-graph" ] && echo true || echo false)"
run_test "daily/ is writable" "$([ -w "$DATA_PATH/daily" ] && echo true || echo false)"
echo ""

# --- Section 5: Cron Jobs ---
echo "[5/5] Cron configuration"
CRON_FILE="/etc/cron.d/openclaw-vm-memory-oracle"
run_test "Cron file exists" "$([ -f "$CRON_FILE" ] && echo true || echo false)"
if [ -f "$CRON_FILE" ]; then
    run_test "Summarize job configured" "$(grep -q 'summarize' "$CRON_FILE" && echo true || echo false)"
    run_test "Consolidate job configured" "$(grep -q 'consolidate' "$CRON_FILE" && echo true || echo false)"
    run_test "Health-check job configured" "$(grep -q 'health-check' "$CRON_FILE" && echo true || echo false)"
    run_test "Quality-probe job configured" "$(grep -q 'quality-probe' "$CRON_FILE" && echo true || echo false)"
fi
echo ""

# --- Summary ---
echo "=== Results ==="
echo "Passed: $PASS / $TOTAL"
echo "Failed: $FAIL / $TOTAL"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "STATUS: FAIL"
    exit 1
else
    echo "STATUS: PASS"
    exit 0
fi
