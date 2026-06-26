#!/usr/bin/env bash
#===========================================================
# claim-card.sh — Generate an evidence card .md file
#
# Inputs (env/args):
#   CLAIM_ID      — e.g. "claim_001"
#   TOPIC         — topic/slug for this research session
#   CONTENT       — the claim text
#   SOURCE        — source URL or name
#   SOURCE_TIER   — T1|T2|T3|T4
#   VERIFICATION_STATUS — confirmed|pending|contradicted
#   ROUND         — research round number
#   CACHE_DIR     — full path to the session cache dir
#===========================================================

set -e

CLAIM_ID="${CLAIM_ID:?missing CLAIM_ID}"
TOPIC="${TOPIC:?missing TOPIC}"
CONTENT="${CONTENT:?missing CONTENT}"
SOURCE="${SOURCE:-unknown}"
SOURCE_TIER="${SOURCE_TIER:-T4}"
VERIFICATION_STATUS="${VERIFICATION_STATUS:-pending}"
ROUND="${ROUND:-1}"
CACHE_DIR="${CACHE_DIR:?missing CACHE_DIR}"

CLAIMS_DIR="${CACHE_DIR}/claims"
mkdir -p "${CLAIMS_DIR}"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Escape CONTENT for YAML (basic: collapse lines, escape special chars)
CONTENT_ESCAPED=$(echo "${CONTENT}" | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/"/\\"/g')

cat > "${CLAIMS_DIR}/${CLAIM_ID}.md" <<EOF
---
id: ${CLAIM_ID}
topic: ${TOPIC}
round: ${ROUND}
source: ${SOURCE}
source_tier: ${SOURCE_TIER}
verification_status: ${VERIFICATION_STATUS}
created_at: ${TIMESTAMP}
---

${CONTENT}
EOF

echo "claim-card: wrote ${CLAIMS_DIR}/${CLAIM_ID}.md"
