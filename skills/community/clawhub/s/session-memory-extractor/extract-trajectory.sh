#!/bin/bash
# Session Memory Extractor — Trajectory Recovery v1.0.6
# 用法: bash extract-trajectory.sh --agent main --parallel 3
#
# v1.0.6 关键能力：从孤儿 .trajectory.jsonl 恢复对话内容（之前 session-memory-extractor 误删 .jsonl 后留下）
#
# 工作流：
#   1. 扫描 SESSIONS_DIR 找所有 .trajectory.jsonl（无对应 .jsonl 的叫 orphan）
#   2. 对每个 orphan，调用 extract_session.py --source trajectory --file <path>
#   3. 提炼成功 → 写入 memory/ + 删除 trajectory
#   4. 提炼失败 → quarantine 保留（永不丢失）
#   5. 输出飞书报告（可选）

set -eo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${WORKDIR}/config.env"

# --- Load config.env ---
load_config() {
    [[ -f "$CONFIG_FILE" ]] || { echo "ERROR: config.env not found at $CONFIG_FILE"; exit 1; }
    while IFS= read -r line || [[ -n "$line" ]]; do
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$line" ]] && continue
        [[ "$line" != *=* ]] && continue
        key="${line%%=*}"
        val="${line#*=}"
        key="$(echo "$key" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
        val="$(echo "$val" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
        if [[ -n "$key" ]] && [[ -z "${!key}" ]]; then
            export "$key=$val"
        fi
    done < "$CONFIG_FILE"
}

load_config

# --- Defaults ---
EXTRACTION_MODEL="${EXTRACTION_MODEL:-MiniMax-M2}"
AGENT_ID="main"
REPORT_DIR="${WORKDIR}/reports"
PARALLEL=3
PREVIEW=false
DRY_RUN=false
# Trajectory recovery: ignore config.env's MIN_AGE_DAYS (we want ALL orphans, no time filter)
MIN_AGE_DAYS=0
MIN_SIZE="${MIN_SIZE:-500}"        # 太小的 trajectory 没意义（< 500 字节）

# --- Args ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --agent) AGENT_ID="$2"; shift 2 ;;
        --preview) PREVIEW=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --min-age) MIN_AGE_DAYS="$2"; shift 2 ;;
        --min-size) MIN_SIZE="$2"; shift 2 ;;
        --parallel) PARALLEL="$2"; shift 2 ;;
        --model) EXTRACTION_MODEL="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# --- Paths ---
AGENT_DIR="${HOME}/.openclaw/agents/${AGENT_ID}"
SESSIONS_DIR="${AGENT_DIR}/sessions"
if [[ "$AGENT_ID" == "main" ]]; then
    MEMORY_DIR="${HOME}/.openclaw/workspace/memory"
else
    MEMORY_DIR="${AGENT_DIR}/workspace/memory"
fi
SESSIONS_JSON="${SESSIONS_DIR}/sessions.json"

# --- Validate ---
[[ -d "$SESSIONS_DIR" ]] || { echo "ERROR: sessions dir not found: $SESSIONS_DIR"; exit 1; }
mkdir -p "$REPORT_DIR"

# --- Date logic ---
if [[ "$(uname)" == "Darwin" ]]; then
    CUTOFF_DATE=$(date -v-${MIN_AGE_DAYS}d +%s 2>/dev/null || date +%s)
else
    CUTOFF_DATE=$(date -d "${MIN_AGE_DAYS} days ago" +%s 2>/dev/null || date +%s)
fi
TODAY=$(date +%Y-%m-%d)
TOKEN=$(sqlite3 "${AGENT_DIR}/agent/openclaw-agent.sqlite" "SELECT json_extract(store_json, '\$.profiles.\"minimax-portal:default\".access') FROM auth_profile_store;" 2>/dev/null | tr -d '\n')
[[ -z "$TOKEN" ]] && TOKEN="${MINIMAX_API_KEY:-}"

# --- Find orphan trajectories ---
echo "=== Trajectory Recovery v1.0.6 ==="
echo "Agent: $AGENT_ID"
echo "Sessions: $SESSIONS_DIR"
echo "Memory: $MEMORY_DIR"
echo "Model: $EXTRACTION_MODEL"
echo "Parallel: $PARALLEL"
echo "Min size: ${MIN_SIZE}B"
echo ""

TMP_ORPHANS=$(mktemp)
TOTAL=0
RECOVERABLE=0
TOTAL_SIZE=0
SKIP_RECENT=0
SKIP_TOO_SMALL=0

# 1. 找所有 .trajectory.jsonl
ALL_TRAJ=$(find "$SESSIONS_DIR" -maxdepth 1 -name "*.trajectory.jsonl" -type f 2>/dev/null)

# 2. 过滤出 orphan（对应 .jsonl 不存在）
for traj in $ALL_TRAJ; do
    TOTAL=$((TOTAL+1))
    base=$(basename "$traj" .trajectory.jsonl)
    jsonl="$SESSIONS_DIR/${base}.jsonl"
    size=$(stat -f %z "$traj" 2>/dev/null || stat -c %s "$traj" 2>/dev/null || echo 0)
    mtime=$(stat -f %m "$traj" 2>/dev/null || stat -c %Y "$traj" 2>/dev/null || echo 0)

    if [[ -f "$jsonl" ]]; then
        continue  # not orphan
    fi
    if [[ "$size" -lt "$MIN_SIZE" ]]; then
        SKIP_TOO_SMALL=$((SKIP_TOO_SMALL+1))
        continue
    fi
    if [[ "$MIN_AGE_DAYS" -gt 0 ]] && [[ "$mtime" -ge "$CUTOFF_DATE" ]]; then
        SKIP_RECENT=$((SKIP_RECENT+1))
        continue
    fi
    RECOVERABLE=$((RECOVERABLE+1))
    TOTAL_SIZE=$((TOTAL_SIZE+size))
    echo "$traj" >> "$TMP_ORPHANS"
done

fmt_size() {
    local bytes=$1
    if [[ $bytes -lt 1024 ]]; then echo "${bytes}B"
    elif [[ $bytes -lt 1048576 ]]; then echo "$((bytes / 1024))KB"
    elif [[ $bytes -lt 1073741824 ]]; then echo "$((bytes / 1048576))MB"
    else echo "$((bytes / 1073741824))GB"
    fi
}

TOTAL_HUMAN=$(fmt_size $TOTAL_SIZE)
SERIAL_EST=$((RECOVERABLE * 10))
PARALLEL_EST=$((RECOVERABLE * 10 / PARALLEL))
SERIAL_MIN=$((SERIAL_EST / 60))
PARALLEL_MIN=$((PARALLEL_EST / 60))

echo "===PREVIEW_START==="
echo "total_trajectories=$TOTAL"
echo "orphan_count=$RECOVERABLE"
echo "skip_recent=$SKIP_RECENT"
echo "skip_too_small=$SKIP_TOO_SMALL"
echo "total_recoverable_size=$TOTAL_HUMAN"
echo "serial_est_min=$SERIAL_MIN"
echo "parallel_est_min=$PARALLEL_MIN"
echo "parallel=$PARALLEL"
echo "agent=$AGENT_ID"
echo "model=$EXTRACTION_MODEL"
echo "===PREVIEW_END==="

if [[ "$PREVIEW" == "true" ]]; then
    rm -f "$TMP_ORPHANS"
    exit 0
fi

if [[ "$RECOVERABLE" == "0" ]]; then
    echo "NO_ORPHAN_TRAJECTORIES"
    rm -f "$TMP_ORPHANS"
    exit 0
fi

# --- Process each orphan ---
echo ""
echo "===RUN_START==="
REPORT_FILE="$REPORT_DIR/trajectory-recovery-${AGENT_ID}-${TODAY}.json"
QUARANTINE_LOG="$REPORT_DIR/quarantine.log"
mkdir -p "$MEMORY_DIR"
MEMORY_FILE="$MEMORY_DIR/${TODAY}.md"

# JSON results
RESULTS_JSON="[]"
PROCESSED=0
QUARANTINED=0
EXTRACTED_TOTAL=0
FREED_TOTAL=0
LOCKFILE="/tmp/trajectory-recovery-${AGENT_ID}.lock"

# trap to clean up lockfile
trap 'rm -f "$LOCKFILE" "$TMP_ORPHANS"' EXIT

process_orphan() {
    local traj=$1
    local base=$(basename "$traj" .trajectory.jsonl)
    local size=$(stat -f %z "$traj" 2>/dev/null || stat -c %s "$traj" 2>/dev/null || echo 0)

    echo "[PROCESS] $base ($size bytes)"

    # Call extract_session.py with --source trajectory
    local output
    output=$(MINIMAX_API_KEY="$TOKEN" python3 "${WORKDIR}/extract_session.py" \
        --session-id "$base" \
        --source trajectory \
        --file "$traj" \
        --model "$EXTRACTION_MODEL" 2>&1) || true

    # Check for __EXTRACT_OK__ marker
    if ! echo "$output" | grep -q "^__EXTRACT_OK__$"; then
        local reason="unknown"
        if echo "$output" | grep -q "Trajectory transcript too short"; then reason="transcript_too_short"
        elif echo "$output" | grep -q "No model.completed"; then reason="no_model_completed"
        elif echo "$output" | grep -q "Empty messagesSnapshot"; then reason="empty_snapshot"
        elif echo "$output" | grep -q "MiniMax API error"; then reason="api_error"
        elif echo "$output" | grep -q "API returned empty"; then reason="api_empty"
        elif echo "$output" | grep -q "Traceback"; then reason="exception"
        fi
        local err_preview=$(echo "$output" | tail -3 | head -1 | head -c 200)
        echo "[QUARANTINE] $base (reason: $reason)"
        echo "$(date -Iseconds)	$base	$reason	$size	$traj" >> "$QUARANTINE_LOG"
        echo "QUARANTINE|$base|$reason|$size"
        return
    fi

    # Extract content (everything after __EXTRACT_OK__)
    local extraction=$(echo "$output" | sed -n '/^__EXTRACT_OK__$/,$p' | tail -n +2)
    local entry_count=$(echo "$extraction" | grep -c "^\- \*\*\[")

    # Validate content (same as run_extractor.py: ≥ 50 chars + structured entries)
    # Special case: AI returned "NO_MEMORIES" — valid empty result, not invalid
    if [[ ${#extraction} -lt 50 ]] || [[ "$entry_count" -eq 0 ]]; then
        local reason="invalid_extraction"
        if echo "$extraction" | grep -q "NO_MEMORIES"; then
            reason="no_memories"
        fi
        echo "[QUARANTINE] $base (reason: $reason)"
        echo "$(date -Iseconds)	$base	$reason	$size	$traj" >> "$QUARANTINE_LOG"
        echo "QUARANTINE|$base|$reason|$size"
        return
    fi

    # Success: write to memory + delete trajectory
    # v1.0.6 safety: verify memory write succeeded BEFORE deleting trajectory
    local memory_size_before=0
    [[ -f "$MEMORY_FILE" ]] && memory_size_before=$(stat -f %z "$MEMORY_FILE" 2>/dev/null || stat -c %s "$MEMORY_FILE" 2>/dev/null || echo 0)
    
    {
        echo ""
        echo "## Recovered from trajectory: $base"
        echo "Original file: $traj"
        echo "File size: $size bytes"
        echo ""
        echo "$extraction"
        echo ""
    } >> "$MEMORY_FILE" || {
        echo "[QUARANTINE] $base (reason: memory_write_failed)"
        echo "$(date -Iseconds)	$base	memory_write_failed	$size	$traj" >> "$QUARANTINE_LOG"
        echo "QUARANTINE|$base|memory_write_failed|$size"
        return
    }

    # Verify memory file grew
    local memory_size_after=0
    [[ -f "$MEMORY_FILE" ]] && memory_size_after=$(stat -f %z "$MEMORY_FILE" 2>/dev/null || stat -c %s "$MEMORY_FILE" 2>/dev/null || echo 0)
    local memory_growth=$((memory_size_after - memory_size_before))
    if [[ "$memory_growth" -lt 50 ]]; then
        echo "[QUARANTINE] $base (reason: memory_write_verification_failed (growth=${memory_growth}))"
        echo "$(date -Iseconds)	$base	memory_write_verification_failed	$size	$traj" >> "$QUARANTINE_LOG"
        echo "QUARANTINE|$base|memory_write_verification_failed|$size"
        return
    fi

    # Memory write confirmed → now safe to delete trajectory
    if [[ -f "$traj" ]]; then
        rm -f "$traj"
    fi

    # Also clean up related files
    for suffix in ".jsonl" ".jsonl.lock" ".deleted."*; do
        local f="${traj%.trajectory.jsonl}${suffix}"
        [[ -e "$f" ]] && rm -f "$f"
    done

    # Remove from sessions.json
    if [[ -f "$SESSIONS_JSON" ]]; then
        python3 -c "
import json, sys
try:
    with open('$SESSIONS_JSON') as f: data = json.load(f)
    keys_to_del = []
    for k, v in list(data.items()):
        if v.get('sessionId') == '$base' or k == '$base':
            keys_to_del.append(k)
    for k in keys_to_del:
        del data[k]
    with open('$SESSIONS_JSON', 'w') as f: json.dump(data, f, indent=2)
except Exception as e:
    pass
" 2>/dev/null || true
    fi

    echo "[DONE] $base — $entry_count entries recovered, $size bytes freed"
    echo "DONE|$base|$entry_count|$size"
}

export -f process_orphan
export WORKDIR TOKEN QUARANTINE_LOG MEMORY_FILE SESSIONS_JSON

# --- Run serial or parallel ---
if [[ "$PARALLEL" -le 1 ]]; then
    while IFS= read -r traj; do
        [[ -z "$traj" ]] && continue
        result=$(process_orphan "$traj" 2>&1)
        echo "$result" >> "$LOCKFILE.tmp"
    done < "$TMP_ORPHANS"
else
    echo "[PARALLEL] Running with $PARALLEL workers..."
    cat "$TMP_ORPHANS" | xargs -P "$PARALLEL" -I {} bash -c 'process_orphan "$@"' _ {} >> "$LOCKFILE.tmp" 2>&1
fi

# --- Aggregate results ---
if [[ -f "$LOCKFILE.tmp" ]]; then
    while IFS='|' read -r status sid entries size; do
        if [[ "$status" == "DONE" ]]; then
            PROCESSED=$((PROCESSED+1))
            EXTRACTED_TOTAL=$((EXTRACTED_TOTAL+entries))
            FREED_TOTAL=$((FREED_TOTAL+size))
        elif [[ "$status" == "QUARANTINE" ]]; then
            QUARANTINED=$((QUARANTINED+1))
        fi
    done < "$LOCKFILE.tmp"
    rm -f "$LOCKFILE.tmp"
fi

# --- Report ---
cat > "$REPORT_FILE" << EOF
{
  "version": "1.0.6",
  "date": "$TODAY",
  "agent": "$AGENT_ID",
  "orphan_total": $RECOVERABLE,
  "recovered": $PROCESSED,
  "quarantined": $QUARANTINED,
  "entries_extracted": $EXTRACTED_TOTAL,
  "bytes_freed": $FREED_TOTAL,
  "bytes_freed_human": "$(fmt_size $FREED_TOTAL)",
  "memory_file": "$MEMORY_FILE",
  "model": "$EXTRACTION_MODEL"
}
EOF

echo ""
echo "=== Summary ==="
echo "Orphan trajectories: $RECOVERABLE"
echo "Recovered: $PROCESSED"
echo "Quarantined: $QUARANTINED"
echo "Entries extracted: $EXTRACTED_TOTAL"
echo "Bytes freed: $FREED_TOTAL ($(fmt_size $FREED_TOTAL))"
echo "Memory: $MEMORY_FILE"
echo "Report: $REPORT_FILE"
echo "Done."
