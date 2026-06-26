#!/bin/bash
# Processor 分发脚本 - PubMed 精简版
# 用法: bash run_processor.sh <processor> <file_path> <task_id>
# processor: pubmed_summary

PROCESSOR="$1"
FILE_PATH="$2"
TASK_ID="$3"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [PROCESSOR:$PROCESSOR] $1"
}

# notify 路径
NOTIFY_SCRIPT="${NOTIFY_PATH:-$(which notify 2>/dev/null || echo '/usr/local/bin/notify')}"

case "$PROCESSOR" in
    "pubmed_summary")
        if [ -z "$FILE_PATH" ] || [ -z "$TASK_ID" ]; then
            log "ERROR: pubmed_summary requires <articles_json> <task_id>"
            exit 1
        fi
        log "执行 pubmed_summary processor: articles=$FILE_PATH task=$TASK_ID"
        bash "${SCRIPT_DIR}/run_pubmed_summary.sh" "$FILE_PATH" "$TASK_ID"
        exit $?
        ;;
    *)
        log "ERROR: 未知 processor: $PROCESSOR"
        echo "可用 processor: pubmed_summary"
        exit 1
        ;;
esac
