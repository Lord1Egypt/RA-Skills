#!/bin/bash
# Download Shengwang documentation index to local cache
# Usage: bash skills/voice-ai-integration/scripts/fetch-docs.sh

set -euo pipefail

DOCS_URL="https://doc.shengwang.cn/llms.txt"
SCRIPT_DIR="$(dirname "$0")"
OUTPUT_FILE="${SCRIPT_DIR}/../references/docs.txt"
MAX_RETRIES=3

for i in $(seq 1 $MAX_RETRIES); do
  echo "Downloading doc index (attempt ${i}/${MAX_RETRIES}) ..."
  if curl -fSL --retry 2 --max-time 120 -o "${OUTPUT_FILE}" "${DOCS_URL}"; then
    echo "Saved to ${OUTPUT_FILE}"
    exit 0
  fi
  echo "Attempt ${i} failed."
  sleep 2
done

echo "ERROR: Failed after ${MAX_RETRIES} attempts. Check your network and try again."
exit 1
