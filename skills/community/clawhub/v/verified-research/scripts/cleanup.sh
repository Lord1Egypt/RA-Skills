#!/usr/bin/env bash
#===========================================================
# cleanup.sh — 3-day cache cleanup with MEMORY.md write-back
#
# Inputs:
#   CACHE_DIR  — cache root (default: /tmp/deep-research-cache)
#
# Logic:
#   For each research dir:
#     - If .cleanup_scheduled exists AND age > 3 days:
#         1. Read report_final.md
#         2. Append summary to /root/.openclaw/workspace/MEMORY.md
#         3. Delete the research dir
#     - If user continued research (new claims/rounds after .cleanup_scheduled):
#         delete .cleanup_scheduled (cancel pending cleanup)
#===========================================================

set -e

CACHE_DIR="${CACHE_DIR:-/tmp/deep-research-cache}"
MEMORY_PATH="/root/.openclaw/workspace/MEMORY.md"

if [ ! -d "${CACHE_DIR}" ]; then
  echo "cleanup: cache dir ${CACHE_DIR} does not exist, nothing to do"
  exit 0
fi

# Ensure MEMORY_PATH exists
if [ ! -f "${MEMORY_PATH}" ]; then
  touch "${MEMORY_PATH}"
fi

NOW=$(date +%s)
THREE_DAYS_SECS=259200  # 3 * 24 * 60 * 60

echo "cleanup: scanning ${CACHE_DIR}"

# Iterate over topic directories (each contains timestamped session dirs)
for topic_dir in "${CACHE_DIR}"/*/; do
  [ -d "${topic_dir}" ] || continue
  TOPIC_SLUG=$(basename "${topic_dir}")

  # Check for cleanup marker at topic level
  MARKER="${topic_dir}.cleanup_scheduled"

  if [ ! -f "${MARKER}" ]; then
    echo "cleanup: ${TOPIC_SLUG} — no cleanup marker, skipping"
    continue
  fi

  # Parse scheduled_at from marker
  SCHEDULED_AT=$(python3 -c "import json,sys; d=json.load(open('${MARKER}')); print(d.get('scheduled_at',''))" 2>/dev/null || echo "")

  if [ -z "${SCHEDULED_AT}" ]; then
    echo "cleanup: ${TOPIC_SLUG} — invalid marker, removing"
    rm -f "${MARKER}"
    continue
  fi

  SCHEDULED_SECS=$(date -d "${SCHEDULED_AT}" +%s 2>/dev/null || echo 0)
  if [ "${SCHEDULED_SECS}" -eq 0 ]; then
    echo "cleanup: ${TOPIC_SLUG} — could not parse scheduled_at, removing marker"
    rm -f "${MARKER}"
    continue
  fi

  AGE_SECS=$((NOW - SCHEDULED_SECS))

  # Check for continued activity: find the latest session dir and compare timestamps
  # The cleanup is cancelled if any session was updated after the scheduled time
  continued=0
  for session_dir in "${topic_dir}"*/; do
    [ -d "${session_dir}" ] || continue
    MANIFEST="${session_dir}manifest.json"
    if [ -f "${MANIFEST}" ]; then
      MANIFEST_UPDATED=$(python3 -c "import json; d=json.load(open('${MANIFEST}')); print(d.get('updated_at',''))" 2>/dev/null || echo "")
      if [ -n "${MANIFEST_UPDATED}" ]; then
        MANIFEST_SECS=$(date -d "${MANIFEST_UPDATED}" +%s 2>/dev/null || echo 0)
        if [ "${MANIFEST_SECS}" -gt "${SCHEDULED_SECS}" ]; then
          echo "cleanup: ${TOPIC_SLUG} — user continued research after cleanup scheduled, cancelling"
          continued=1
          break
        fi
      fi
    fi
  done

  if [ "${continued}" -eq 1 ]; then
    rm -f "${MARKER}"
    continue
  fi

  # Check age
  if [ "${AGE_SECS}" -lt "${THREE_DAYS_SECS}" ]; then
    REMAINING=$((THREE_DAYS_SECS - AGE_SECS))
    REMAINING_HRS=$((REMAINING / 3600))
    echo "cleanup: ${TOPIC_SLUG} — ${REMAINING_HRS}h remaining before cleanup"
    continue
  fi

  # === Time to archive and delete ===
  echo "cleanup: ${TOPIC_SLUG} — archiving and deleting (age: ${AGE_SECS}s)"

  # Find the latest session dir (most recent report)
  latest_session=""
  latest_report_mtime=0
  for session_dir in "${topic_dir}"*/; do
    [ -d "${session_dir}" ] || continue
    REPORT="${session_dir}report_final.md"
    if [ -f "${REPORT}" ]; then
      mtime=$(stat -c %Y "${REPORT}" 2>/dev/null || echo 0)
      if [ "${mtime}" -gt "${latest_report_mtime}" ]; then
        latest_report_mtime=${mtime}
        latest_session="${session_dir}"
      fi
    fi
  done

  MANIFEST="${latest_session}manifest.json"
  REPORT="${latest_session}report_final.md"

  # Extract metadata
  TOPIC_NAME="${TOPIC_SLUG}"
  TOTAL_CLAIMS=0
  T1=0; T2=0; T3=0; T4=0
  CORE_CONCLUSION=""
  ARCHIVE_DATE=$(date -u +"%Y-%m-%d")

  if [ -f "${MANIFEST}" ]; then
    TOPIC_NAME=$(python3 -c "import json; d=json.load(open('${MANIFEST}')); print(d.get('topic','${TOPIC_SLUG}'))" 2>/dev/null || echo "${TOPIC_SLUG}")
    TOTAL_CLAIMS=$(python3 -c "import json; d=json.load(open('${MANIFEST}')); print(d.get('total_claims',0))" 2>/dev/null || echo 0)
    TIERS=$(python3 -c "import json; d=json.load(open('${MANIFEST}')); t=d.get('source_tier_counts',{}); print(f'T1={t.get(\"T1\",0)} T2={t.get(\"T2\",0)} T3={t.get(\"T3\",0)} T4={t.get(\"T4\",0)}')" 2>/dev/null || echo "T1=0 T2=0 T3=0 T4=0")
    T1=$(echo "${TIERS}" | grep -oP 'T1=\K\d+' || echo 0)
    T2=$(echo "${TIERS}" | grep -oP 'T2=\K\d+' || echo 0)
    T3=$(echo "${TIERS}" | grep -oP 'T3=\K\d+' || echo 0)
    T4=$(echo "${TIERS}" | grep -oP 'T4=\K\d+' || echo 0)

    # Core conclusion: first 2 confirmed claim previews
    CORE_CONCLUSION=$(python3 -c "
import json
try:
    d=json.load(open('${MANIFEST}'))
    confirmed=[c.get('content_preview','') for c in d.get('claims',[]) if c.get('verification_status')=='confirmed']
    confirmed=[c for c in confirmed if c]
    if confirmed:
        print('; '.join(confirmed[:2]))
    else:
        print('')
except:
    print('')
" 2>/dev/null || echo "")
  fi

  if [ -z "${CORE_CONCLUSION}" ] && [ -f "${REPORT}" ]; then
    CORE_CONCLUSION=$(sed -n '/## 关键结论/,/##/p' "${REPORT}" 2>/dev/null | head -n 10 | tr '\n' ' ' | sed 's/^ *//; s/  */ /g' | cut -c1-300)
  fi

  # Append to MEMORY.md under "## Recent Research Cache (Auto-archived)"
  SECTION_MARKER="## Recent Research Cache (Auto-archived)"
  ENTRY="
${SECTION_MARKER}

**Topic:** ${TOPIC_NAME}
**Archived:** ${ARCHIVE_DATE}
**Core conclusion:** ${CORE_CONCLUSION:-（研究已完成，详见原始报告）}
**Sources:** T1:${T1} / T2:${T2} / T3:${T3} / T4:${T4}（共 ${TOTAL_CLAIMS} 条）
**Full report:** /tmp/deep-research-cache/${TOPIC_SLUG}/（即将删除，如需查阅请在3天内操作）"

  {
    # Add newline if MEMORY.md doesn't end with one
    if [ -s "${MEMORY_PATH}" ]; then
      last_char=$(tail -c1 "${MEMORY_PATH}" | xxd -p 2>/dev/null || echo "")
      [ "${last_char}" != "0a" ] && echo ""
    fi
    echo "${ENTRY}"
  } >> "${MEMORY_PATH}"

  echo "cleanup: wrote summary to ${MEMORY_PATH}"

  # Delete the entire topic dir (all sessions)
  rm -rf "${topic_dir}"
  echo "cleanup: deleted ${topic_dir}"
done

exit 0
