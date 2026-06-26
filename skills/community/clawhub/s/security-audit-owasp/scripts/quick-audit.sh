#!/bin/bash
# Quick Infrastructure Audit — Security Audit Skill
# Scans target for open ports, services, web vulnerabilities, and SSL issues
#
# Usage: bash quick-audit.sh <target> [output_dir]
#
# WARNING: Only use on infrastructure you own or have explicit permission to test.

set -euo pipefail

TARGET="${1:?Usage: quick-audit.sh <target> [output_dir]}"
OUTPUT_DIR="${2:-./audit-reports}"
DATE=$(date +%Y-%m-%d_%H%M%S)
REPORT="$OUTPUT_DIR/audit-${TARGET//\//-}-$DATE.txt"

mkdir -p "$OUTPUT_DIR"

echo "========================================" | tee "$REPORT"
echo "Security Audit: $TARGET" | tee -a "$REPORT"
echo "Date: $(date)" | tee -a "$REPORT"
echo "========================================" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

# 1. Port scan
echo "--- Port Scan (top 1000) ---" | tee -a "$REPORT"
nmap -sV --top-ports 1000 "$TARGET" 2>&1 | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

# 2. SSL/TLS check (if HTTPS)
echo "--- SSL/TLS Check ---" | tee -a "$REPORT"
nmap --script ssl-cert,ssl-enum-ciphers -p 443 "$TARGET" 2>&1 | tee -a "$REPORT" || true
echo "" | tee -a "$REPORT"

# 3. HTTP headers
echo "--- HTTP Headers ---" | tee -a "$REPORT"
curl -sI "http://$TARGET" 2>&1 | tee -a "$REPORT" || true
curl -sI "https://$TARGET" 2>&1 | tee -a "$REPORT" || true
echo "" | tee -a "$REPORT"

# 4. Nikto web scan (if nikto available)
if command -v nikto &>/dev/null; then
    echo "--- Nikto Web Scan ---" | tee -a "$REPORT"
    nikto -h "http://$TARGET" -maxtime 300 2>&1 | tee -a "$REPORT" || true
    echo "" | tee -a "$REPORT"
else
    echo "--- Nikto: Not installed (apt install nikto) ---" | tee -a "$REPORT"
fi

echo "========================================" | tee -a "$REPORT"
echo "Audit complete. Report saved to: $REPORT"
echo "========================================"