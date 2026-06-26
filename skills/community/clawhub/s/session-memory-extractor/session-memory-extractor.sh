#!/bin/bash
# Session Memory Extractor for OpenClaw v1.0.6
# Usage: bash session-memory-extractor.sh --agent main --preview
#        bash session-memory-extractor.sh --agent main --parallel 3 --yes

# v1.0.6 safety: failed extractions are QUARANTINED, not deleted.
# Quarantined files are renamed to *.quarantined-<reason>-<ts>.jsonl and
# skipped on subsequent runs. See run_extractor.py: _quarantine_session().

set -eo pipefail

WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${WORKDIR}/config.env"

# --- Load config.env ---
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "ERROR: config.env not found at $CONFIG_FILE"
        exit 1
    fi

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

# --- Config with defaults ---
EXTRACTION_MODEL="${EXTRACTION_MODEL:-MiniMax-M2}"
NOTIFY_TARGET="${NOTIFY_TARGET:-}"
NOTIFY_ENABLED="${NOTIFY_ENABLED:-false}"
PREVIEW=false
DRY_RUN=false
MIN_AGE_DAYS="${MIN_AGE_DAYS:-7}"
AGENT_ID="main"
REPORT_DIR="${WORKDIR}/reports"
PARALLEL=1

# --- Args ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --agent) AGENT_ID="$2"; shift 2 ;;
        --preview) PREVIEW=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --min-age) MIN_AGE_DAYS="$2"; shift 2 ;;
        --parallel) PARALLEL="$2"; shift 2 ;;
        --yes) shift ;;  # 忽略，由调用者控制确认
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
RUNNER="${WORKDIR}/run_extractor.py"

# --- Validate ---
if [[ ! -d "$SESSIONS_DIR" ]]; then
    echo "ERROR: Sessions directory not found: $SESSIONS_DIR"
    exit 1
fi

mkdir -p "$REPORT_DIR"

# --- Find sessions ---
if [[ "$(uname)" == "Darwin" ]]; then
    CUTOFF_DATE=$(date -v-${MIN_AGE_DAYS}d +%s)
    CUTOFF_DISPLAY=$(date -r $CUTOFF_DATE '+%Y-%m-%d')
else
    CUTOFF_DATE=$(date -d "${MIN_AGE_DAYS} days ago" +%s)
    CUTOFF_DISPLAY=$(date -d "${MIN_AGE_DAYS} days ago" '+%Y-%m-%d')
fi

# 快速扫描
TMP_FILES=$(mktemp)
find "$SESSIONS_DIR" -maxdepth 1 -name "*.jsonl" \
    ! -name "*.trajectory.jsonl" \
    ! -name "*.deleted.*" \
    ! -name "*.quarantined-*" \
    ! -name "*checkpoint*" -type f > "$TMP_FILES" 2>/dev/null || true

FILE_COUNT=$(wc -l < "$TMP_FILES" 2>/dev/null || echo 0)

OLDEST_TS=""
NEWEST_TS=""
TOTAL_SIZE=0
SKIP_COUNT=0
OLD_COUNT=0

while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    
    # v1.0.3: use -f %z (apparent size in bytes) instead of -f %s (blocks)
    # On macOS: stat -f %z = size in bytes, stat -f %s = 512-byte blocks (wrong)
    size=$(stat -f %z "$f" 2>/dev/null || stat -c %s "$f" 2>/dev/null || echo 0)
    mtime=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
    TOTAL_SIZE=$((TOTAL_SIZE + size))
    
    if [[ "$mtime" -lt "$CUTOFF_DATE" ]]; then
        OLD_COUNT=$((OLD_COUNT + 1))
        [[ -z "$OLDEST_TS" ]] && OLDEST_TS="$mtime"
        [[ "$mtime" -lt "$OLDEST_TS" ]] && OLDEST_TS="$mtime"
        [[ "$mtime" -gt "$NEWEST_TS" ]] && NEWEST_TS="$mtime"
    else
        SKIP_COUNT=$((SKIP_COUNT + 1))
    fi
done < "$TMP_FILES"

# 格式化大小
fmt_size() {
    local bytes=$1
    if [[ $bytes -lt 1024 ]]; then
        echo "${bytes}B"
    elif [[ $bytes -lt 1048576 ]]; then
        echo "$((bytes / 1024))KB"
    elif [[ $bytes -lt 1073741824 ]]; then
        echo "$((bytes / 1048576))MB"
    else
        echo "$((bytes / 1073741824))GB"
    fi
}

TOTAL_SIZE_HUMAN=$(fmt_size $TOTAL_SIZE)

# 估算时间：单文件 ~10s
SERIAL_EST=$((OLD_COUNT * 10))
PARALLEL_EST=$((OLD_COUNT * 10 / PARALLEL))
SERIAL_MIN=$((SERIAL_EST / 60))
PARALLEL_MIN=$((PARALLEL_EST / 60))

# --- 输出分隔符（用于解析） ---
echo "===PREVIEW_START==="
echo "total_files=$FILE_COUNT"
echo "old_files=$OLD_COUNT"
echo "skip_files=$SKIP_COUNT"
echo "total_size=$TOTAL_SIZE_HUMAN"
echo "oldest=$(date -r $OLDEST_TS '+%Y-%m-%d' 2>/dev/null || echo 'unknown')"
echo "newest=$(date -r $NEWEST_TS '+%Y-%m-%d' 2>/dev/null || echo 'unknown')"
echo "cutoff=$CUTOFF_DISPLAY"
echo "serial_est_min=$SERIAL_MIN"
echo "parallel_est_min=$PARALLEL_MIN"
echo "parallel=$PARALLEL"
echo "agent=$AGENT_ID"
echo "model=$EXTRACTION_MODEL"
echo "===PREVIEW_END==="

if [[ "$PREVIEW" == "true" ]]; then
    rm -f "$TMP_FILES"
    exit 0
fi

# --- 执行模式 ---
if [[ "$OLD_COUNT" == "0" ]]; then
    echo "NO_FILES_TO_PROCESS"
    rm -f "$TMP_FILES"
    exit 0
fi

# 过滤只要旧文件
TMP_OLD=$(mktemp)
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    mtime=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
    [[ "$mtime" -lt "$CUTOFF_DATE" ]] && echo "$f"
done < "$TMP_FILES" > "$TMP_OLD"

TODAY=$(date +%Y-%m-%d)

# --- Run processor ---
echo "===RUN_START==="
EXTRACTION_MODEL="$EXTRACTION_MODEL" \
DRY_RUN="$DRY_RUN" \
MIN_AGE_DAYS="$MIN_AGE_DAYS" \
CUTOFF_DATE="$CUTOFF_DATE" \
CUTOFF_DISPLAY="$CUTOFF_DISPLAY" \
TODAY="$TODAY" \
AGENT_ID="$AGENT_ID" \
MEMORY_DIR="$MEMORY_DIR" \
SESSIONS_DIR="$SESSIONS_DIR" \
SESSIONS_JSON="$SESSIONS_JSON" \
EXTRACT_SCRIPT="${WORKDIR}/extract_session.py" \
REPORT_DIR="$REPORT_DIR" \
WORKDIR="$WORKDIR" \
CLEAN_TRAJECTORY="${CLEAN_TRAJECTORY:-true}" \
LOG_LEVEL="${LOG_LEVEL:-info}" \
PARALLEL="$PARALLEL" \
python3 "$RUNNER" < "$TMP_OLD"
echo "===RUN_END==="

# --- Notify ---
if [[ "$NOTIFY_ENABLED" == "true" ]] && [[ -n "$NOTIFY_TARGET" ]]; then
    REPORT_FILE="${REPORT_DIR}/extract-report-${AGENT_ID}-${TODAY}.json"
    if [[ -f "$REPORT_FILE" ]]; then
        echo "[NOTIFY] Sending report to Feishu..."
        python3 "${WORKDIR}/feishu_notify.py" --report "$REPORT_FILE" --target "$NOTIFY_TARGET" 2>&1 || true
    fi
fi

rm -f "$TMP_FILES" "$TMP_OLD"