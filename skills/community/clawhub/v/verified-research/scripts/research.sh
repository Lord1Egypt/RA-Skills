#!/usr/bin/env bash
#===========================================================
# research.sh — Main controller for deep-research workflow
#
# Inputs:
#   TOPIC      — research topic (required)
#   SESSION_ID — optional session identifier
#
# This script orchestrates the workflow but does NOT run AI.
# The AI agent running this script PROVIDES reasoning/analysis.
# This script handles caching/persistence only.
#
# Cache structure:
#   /tmp/deep-research-cache/{slugified_topic}/{unix_timestamp}/
#     claims/
#     rounds/
#     manifest.json
#     report_final.md
#     .cleanup_scheduled
#===========================================================

set -e

TOPIC="${TOPIC:?Usage: TOPIC='...' SESSION_ID='...' bash research.sh}"
SESSION_ID="${SESSION_ID:-$(date +%s)}"

# Slugify topic
# Slugify topic (fallback to MD5 of topic if no alphanumeric chars)
SLUG=$(echo "${TOPIC}" | sed 's/[^a-zA-Z0-9_-]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g; s/^-//; s/-$//')
if [ -z "${SLUG}" ]; then
  SLUG="topic-$(echo "${TOPIC}" | md5sum | cut -c1-8)"
fi
TIMESTAMP=$(date +%s)

CACHE_BASE="/tmp/deep-research-cache"
CACHE_DIR="${CACHE_BASE}/${SLUG}/${TIMESTAMP}"

# Skill dir
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "research: TOPIC='${TOPIC}'"
echo "research: SESSION_ID='${SESSION_ID}'"
echo "research: CACHE_DIR='${CACHE_DIR}'"

# Create cache structure
mkdir -p "${CACHE_DIR}/claims"
mkdir -p "${CACHE_DIR}/rounds"

# Export for child scripts
export CACHE_DIR
export TOPIC
export SESSION_ID
export NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Write initial manifest (empty)
"${SCRIPT_DIR}/manifest.sh"

echo ""
echo "=== Deep Research Started ==="
echo "Topic: ${TOPIC}"
echo "Cache: ${CACHE_DIR}"
echo ""
echo "The AI agent will now perform research rounds using web_search + web_fetch."
echo "For each claim found, call claim-card.sh:"
echo "  CLAIM_ID=claim_NNN CONTENT='...' SOURCE='...' SOURCE_TIER='T1' VERIFICATION_STATUS='pending' ROUND=N bash ${SCRIPT_DIR}/claim-card.sh"
echo ""
echo "After each round, call manifest.sh:"
echo "  bash ${SCRIPT_DIR}/manifest.sh"
echo ""
echo "When research is complete, call finalize.sh:"
echo "  bash ${SCRIPT_DIR}/finalize.sh"
echo ""
echo "To schedule cleanup (3-day auto-archive), call cleanup.sh:"
echo "  bash ${SCRIPT_DIR}/cleanup.sh"
echo ""

# Note: actual research rounds are performed by the AI agent
# This script just sets up the cache structure and prints guidance
