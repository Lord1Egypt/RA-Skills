#!/usr/bin/env bash
# new-pipeline.sh — scaffold a new skelm pipeline from a template
#
# Usage:
#   bash docs/skill/skelm/scripts/new-pipeline.sh <pipeline-id> "<description>"
#   bash docs/skill/skelm/scripts/new-pipeline.sh <pipeline-id> "<description>" --agent
#
# Arguments:
#   pipeline-id    kebab-case id; output file is <pipeline-id>.pipeline.mts
#   description    one-line description of what the pipeline does
#   --agent        use the agent-step template instead of the basic code-step template
#
# The script copies the template into the current directory and substitutes
# {{ID}} and {{DESCRIPTION}}. It does not overwrite existing files.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <pipeline-id> \"<description>\" [--agent]" >&2
  exit 1
fi

PIPELINE_ID="$1"
DESCRIPTION="$2"
USE_AGENT="${3:-}"

# Validate id: lowercase letters, digits, hyphens; no leading/trailing hyphen
if ! echo "$PIPELINE_ID" | grep -qE '^[a-z0-9]([a-z0-9-]*[a-z0-9])?$'; then
  echo "Error: pipeline-id must be lowercase letters, digits, and hyphens (no leading/trailing hyphen)" >&2
  exit 1
fi

OUTPUT_FILE="${PIPELINE_ID}.pipeline.mts"

if [[ -f "$OUTPUT_FILE" ]]; then
  echo "Error: ${OUTPUT_FILE} already exists. Remove it first or choose a different id." >&2
  exit 1
fi

# Locate the template relative to this script's directory
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$USE_AGENT" == "--agent" ]]; then
  TEMPLATE="${SKILL_DIR}/assets/agent-pipeline.template.ts"
else
  TEMPLATE="${SKILL_DIR}/assets/pipeline.template.ts"
fi

if [[ ! -f "$TEMPLATE" ]]; then
  echo "Error: template not found at ${TEMPLATE}" >&2
  exit 1
fi

# Substitute placeholders
sed \
  -e "s/{{ID}}/${PIPELINE_ID}/g" \
  -e "s/{{DESCRIPTION}}/${DESCRIPTION}/g" \
  "$TEMPLATE" > "$OUTPUT_FILE"

echo "Created: ${OUTPUT_FILE}"
echo ""
echo "Next steps:"
echo "  1. Edit ${OUTPUT_FILE} — fill in input/output schemas and step logic."
if [[ "$USE_AGENT" == "--agent" ]]; then
  echo "  2. Declare your backend and MCP servers in skelm.config.ts."
  echo "  3. Set the permissions block to the minimum your agent needs."
fi
echo ""
echo "Run it:"
echo "  skelm run ./${OUTPUT_FILE} --input '{\"value\":\"hello\"}'"
