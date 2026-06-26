#!/usr/bin/env bash
# parse-tracebit-alert.sh — Extract structured data from a Tracebit alert email
# Usage:
#   echo "$EMAIL_BODY" | bash parse-tracebit-alert.sh
#   bash parse-tracebit-alert.sh "email body text here"
#   bash parse-tracebit-alert.sh < email.txt
#
# Output: JSON object with extracted fields
set -euo pipefail

command -v jq >/dev/null 2>&1 || { echo '{"error":"jq is required but not installed"}'; exit 1; }

# ── Read input ────────────────────────────────────────────────────────────────
if [[ $# -gt 0 ]]; then
  INPUT="$*"
else
  INPUT=$(cat)
fi

if [[ -z "$INPUT" ]]; then
  echo '{"error":"No input provided. Pipe email body or pass as argument."}'
  exit 1
fi

# ── Extraction helpers ────────────────────────────────────────────────────────

# Extract first regex match (group 1 if supported, else full match)
extract() {
  local pattern="$1"
  echo "$INPUT" | grep -oP "$pattern" 2>/dev/null | head -1 || \
  echo "$INPUT" | grep -oE "$pattern" 2>/dev/null | head -1 || \
  echo ""
}

extract_line_after() {
  local keyword="$1"
  echo "$INPUT" | grep -i -A1 "$keyword" 2>/dev/null | tail -1 | xargs || echo ""
}

# ── Canary type ────────────────────────────────────────────────────────────────
# Tracebit emails typically mention the credential type
CANARY_TYPE=""
if echo "$INPUT" | grep -qi "aws\|access key\|cloudtrail"; then
  CANARY_TYPE="aws"
elif echo "$INPUT" | grep -qi "ssh\|private key"; then
  CANARY_TYPE="ssh"
elif echo "$INPUT" | grep -qi "cookie\|gitlab.*cookie\|session cookie"; then
  CANARY_TYPE="gitlab-cookie"
elif echo "$INPUT" | grep -qi "username.*password\|password.*manager"; then
  CANARY_TYPE="gitlab-username-password"
elif echo "$INPUT" | grep -qi "email canary\|mailto:"; then
  CANARY_TYPE="email"
fi

# ── Canary name ────────────────────────────────────────────────────────────────
# Look for common patterns: "canary: name", "token: name", or lines with known prefixes
CANARY_NAME=""
# Try pattern: "canary name: <value>" or "token name: <value>"
CANARY_NAME=$(echo "$INPUT" | grep -iP 'canary\s*name\s*[:\-]\s*\K\S+' 2>/dev/null | head -1 || true)
if [[ -z "$CANARY_NAME" ]]; then
  CANARY_NAME=$(echo "$INPUT" | grep -iE 'token|canary' | grep -oE '"[^"]+"' | head -1 | tr -d '"' || true)
fi
if [[ -z "$CANARY_NAME" ]]; then
  # Try label: name in brackets or quotes near "canary"
  CANARY_NAME=$(echo "$INPUT" | grep -oE 'agent-[a-z0-9_-]+' | head -1 || true)
fi

# ── Trigger timestamp ─────────────────────────────────────────────────────────
# ISO8601 or common date formats
TRIGGER_TIME=""
# ISO8601
TRIGGER_TIME=$(echo "$INPUT" | grep -oP '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?' 2>/dev/null | head -1 || true)
if [[ -z "$TRIGGER_TIME" ]]; then
  # "Mar 16, 2026 13:14 UTC" style
  TRIGGER_TIME=$(echo "$INPUT" | grep -oE '[A-Z][a-z]{2} [0-9]{1,2},? [0-9]{4}[, ]+[0-9]{1,2}:[0-9]{2}( [AP]M)?( UTC| GMT)?' | head -1 || true)
fi
if [[ -z "$TRIGGER_TIME" ]]; then
  # Unix timestamp
  TRIGGER_TIME=$(echo "$INPUT" | grep -oP '(?i)time[d:\s]+\K[0-9]{10}' 2>/dev/null | head -1 || true)
fi

# ── Source IP ─────────────────────────────────────────────────────────────────
SOURCE_IP=""
# IPv4
SOURCE_IP=$(echo "$INPUT" | grep -oP '(?:(?:source|from|ip)[:\s]+)?\K(?:\d{1,3}\.){3}\d{1,3}(?:/\d+)?' 2>/dev/null | \
  grep -vE '^(127\.|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)' | head -1 || true)
if [[ -z "$SOURCE_IP" ]]; then
  # Any IPv4 (including private, as fallback)
  SOURCE_IP=$(echo "$INPUT" | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1 || true)
fi

# ── AWS-specific fields ────────────────────────────────────────────────────────
AWS_KEY_ID=$(echo "$INPUT" | grep -oE 'AK[A-Z0-9]{18}' | head -1 || true)
AWS_REGION=$(echo "$INPUT" | grep -oP '(?:region|us-|eu-|ap-|sa-|ca-|me-|af-)\K[a-z0-9-]+' 2>/dev/null | head -1 || true)
AWS_ACTION=$(echo "$INPUT" | grep -oP '(?i)action\s*[:\-]\s*\K[A-Za-z:]+' 2>/dev/null | head -1 || true)

# ── Compose output ────────────────────────────────────────────────────────────
jq -n \
  --arg canary_type    "${CANARY_TYPE:-unknown}" \
  --arg canary_name    "${CANARY_NAME:-unknown}" \
  --arg trigger_time   "${TRIGGER_TIME:-unknown}" \
  --arg source_ip      "${SOURCE_IP:-unknown}" \
  --arg aws_key_id     "${AWS_KEY_ID:-}" \
  --arg aws_region     "${AWS_REGION:-}" \
  --arg aws_action     "${AWS_ACTION:-}" \
  '{
    canary_type:   $canary_type,
    canary_name:   $canary_name,
    trigger_time:  $trigger_time,
    source_ip:     $source_ip,
    aws: (if $aws_key_id != "" then {
      key_id:  $aws_key_id,
      region:  $aws_region,
      action:  $aws_action
    } else null end),
    parsed_at: (now | todate)
  }'
