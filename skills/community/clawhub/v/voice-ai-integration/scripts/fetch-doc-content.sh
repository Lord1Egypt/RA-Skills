#!/bin/bash
# Fetch a single Shengwang doc by URI and output Markdown content to stdout.
# Usage: bash skills/voice-ai-integration/scripts/fetch-doc-content.sh <doc_uri>
#
# Examples:
#   bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/convoai/restful/get-started/quick-start"
#   bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/rtc/javascript/get-started/quick-start"
#
# The doc_uri is the part after ?uri= in doc-mcp URLs found in docs.txt.

set -uo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <doc_uri>" >&2
  echo "Example: $0 \"docs://default/convoai/restful/get-started/quick-start\"" >&2
  exit 1
fi

DOC_URI="$1"
BASE_URL="https://doc-mcp.shengwang.cn/doc-content-by-uri"
FULL_URL="${BASE_URL}?uri=${DOC_URI}"

if ! curl -fSL --max-time 30 --retry 2 "$FULL_URL" 2>/dev/null; then
  echo "ERROR: Failed to fetch doc" >&2
  echo "URL: ${FULL_URL}" >&2
  echo "" >&2
  echo "Fallback: try the doc site URL instead:" >&2
  # Convert docs://default/product/platform/path → https://doc.shengwang.cn/doc/product/platform/path
  FALLBACK=$(echo "$DOC_URI" | sed 's|^docs://default/|https://doc.shengwang.cn/doc/|')
  echo "  ${FALLBACK}" >&2
  exit 1
fi
