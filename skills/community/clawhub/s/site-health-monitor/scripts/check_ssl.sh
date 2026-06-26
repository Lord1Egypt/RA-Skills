#!/usr/bin/env bash
# Check SSL certificate health for a domain
# Usage: check_ssl.sh <domain>
# Output: JSON with SSL certificate data

set -euo pipefail

DOMAIN="${1:?Usage: check_ssl.sh <domain>}"

# Strip protocol and path if provided
DOMAIN=$(echo "$DOMAIN" | sed -E 's|^https?://||' | sed 's|/.*||' | sed 's|:.*||')

# Get certificate info
CERT_INFO=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null) || {
  echo "{\"domain\":\"$DOMAIN\",\"status\":\"error\",\"error\":\"Could not connect to $DOMAIN:443\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
  exit 0
}

# Extract certificate details
CERT_TEXT=$(echo "$CERT_INFO" | openssl x509 -noout -dates -issuer -subject 2>/dev/null) || {
  echo "{\"domain\":\"$DOMAIN\",\"status\":\"error\",\"error\":\"Could not parse certificate\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
  exit 0
}

# Parse dates
NOT_BEFORE=$(echo "$CERT_TEXT" | grep "notBefore=" | cut -d= -f2-)
NOT_AFTER=$(echo "$CERT_TEXT" | grep "notAfter=" | cut -d= -f2-)
ISSUER=$(echo "$CERT_TEXT" | grep "issuer=" | sed 's/^issuer= *//')
SUBJECT=$(echo "$CERT_TEXT" | grep "subject=" | sed 's/^subject= *//')

# Calculate days until expiry
EXPIRY_EPOCH=$(date -d "$NOT_AFTER" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$NOT_AFTER" +%s 2>/dev/null || echo "0")
NOW_EPOCH=$(date +%s)
DAYS_REMAINING=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))

# Determine status
if [[ "$DAYS_REMAINING" -le 0 ]]; then
  STATUS="expired"
elif [[ "$DAYS_REMAINING" -le 7 ]]; then
  STATUS="critical"
elif [[ "$DAYS_REMAINING" -le 30 ]]; then
  STATUS="warning"
else
  STATUS="valid"
fi

# Format expiry date
EXPIRY_DATE=$(date -d "$NOT_AFTER" +%Y-%m-%d 2>/dev/null || echo "$NOT_AFTER")

cat <<EOF
{
  "domain": "$DOMAIN",
  "status": "$STATUS",
  "issuer": "$ISSUER",
  "subject": "$SUBJECT",
  "not_before": "$NOT_BEFORE",
  "not_after": "$NOT_AFTER",
  "expiry_date": "$EXPIRY_DATE",
  "days_remaining": $DAYS_REMAINING,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
