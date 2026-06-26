#!/usr/bin/env bash
set -euo pipefail

# Pull upstream OpenAPI spec + regenerate local endpoint summary.

ROOT="/root/.openclaw/workspace"
SKILL_DIR="$ROOT/skills/sure-api"
REF_DIR="$SKILL_DIR/references"

OPENAPI_URL="https://raw.githubusercontent.com/we-promise/sure/main/docs/api/openapi.yaml"
OPENAPI_PATH="$REF_DIR/openapi.yaml"
SUMMARY_PATH="$REF_DIR/api_endpoints_summary.md"

mkdir -p "$REF_DIR"

echo "Downloading: $OPENAPI_URL"
curl -fsSL --max-time 30 "$OPENAPI_URL" -o "$OPENAPI_PATH"

echo "Generating: $SUMMARY_PATH"
node "$SKILL_DIR/scripts/sure_openapi_summarize.js" "$OPENAPI_PATH" > "$SUMMARY_PATH"

echo "OK"
