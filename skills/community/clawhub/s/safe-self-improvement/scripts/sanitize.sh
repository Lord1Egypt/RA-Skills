#!/usr/bin/env bash
# SECURITY MANIFEST:
# Environment variables accessed: none
# External endpoints called: none
# Local files read: $1 (the content to check)
# Local files written: none
# Purpose: Scan content for sensitive data before logging. Blocks write if found.

set -euo pipefail

CONTENT="${1:-}"

if [ -z "$CONTENT" ]; then
    echo "Usage: sanitize.sh <text>"
    exit 1
fi

# Patterns that indicate sensitive data
PATTERNS=(
    # API keys / tokens (GitHub, AWS, OpenAI, etc.)
    "(ghp_|gho_|github_pat_|sk-|AKIA|xox[baprs])[a-zA-Z0-9]{10,}"
    # Private keys
    "-----BEGIN (RSA |EC |DSA |OPENSSH )PRIVATE KEY-----"
    # Passwords in plain text (various formats)
    -E "(password|passwd|pwd|secret|passphrase)\\s*(is|:|=|:\\\\s*)\\s*[^\\\\s'\\\"]{4,}"
    # IPs
    "192\\.168\\.[0-9]+\\.[0-9]+|10\\.[0-9]+\\.[0-9]+\\.[0-9]+|172\\.(1[6-9]|2[0-9]|3[0-1])\\.[0-9]+\\.[0-9]+"
    # MAC addresses
    "([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}"
    # Phone numbers (China mobile pattern)
    "1[3-9][0-9]{9}"
    # Email (non-placeholder, simple check)
    "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
    # SSID with password
    "(ssid|wifi|wlan)\\s*[:=]\\s*[^\\\\s'\\\"]{1,30}"
    # GPS coordinates (lat, lon)
    "[0-9]+\\.[0-9]{6,},[0-9]+\\.[0-9]{6,}"
    # Device serial numbers
    "(serial|device.id|devid)\\s*[:=]\\s*[A-Z0-9]{6,}"
)

FOUND=0
MATCHES=()

for pattern in "${PATTERNS[@]}"; do
    if echo "$CONTENT" | grep -Ei "$pattern" > /dev/null 2>&1; then
        FOUND=1
        MATCHES+=("Pattern matched: $pattern")
    fi
done

if [ "$FOUND" -eq 1 ]; then
    echo "🚫 SANITIZE BLOCKED: Sensitive data detected in content."
    echo "Matches found:"
    for m in "${MATCHES[@]}"; do
        echo "  - $m"
    done
    echo ""
    echo "Replace sensitive values with <TYPE> placeholders before re-running."
    exit 1
fi

echo "✅ Sanitize check passed: no sensitive data detected."
exit 0
