#!/bin/bash
# SSL Certificate Monitor - Check Script
# Usage: ./check-ssl.sh [domains_file] [warning_days] [critical_days]

DOMAINS_FILE="${1:-$HOME/.openclaw/workspace/ssl-domains.txt}"
WARNING_DAYS=${2:-30}
CRITICAL_DAYS=${3:-7}
OUTPUT_FORMAT="${4:-text}"  # text, json, markdown

# Check if domains file exists
if [ ! -f "$DOMAINS_FILE" ]; then
  echo "[ERROR] Domain list not found: $DOMAINS_FILE"
  echo "Creating template at: $DOMAINS_FILE"
  mkdir -p "$(dirname "$DOMAINS_FILE")"
  cat > "$DOMAINS_FILE" << 'EOF'
# SSL Certificate Monitor - Domain List
# Add one domain per line (comments start with #)
example.com
api.example.com
EOF
  exit 1
fi

# Initialize counters
total=0
ok=0
warning=0
critical=0
failed=0

# Results array for JSON output
declare -a results

echo "SSL Certificate Monitor"
echo "======================="
echo "Thresholds: Warning < $WARNING_DAYS days | Critical < $CRITICAL_DAYS days"
echo ""

while IFS= read -r domain || [ -n "$domain" ]; do
  # Skip empty lines and comments
  [ -z "$domain" ] && continue
  [[ "$domain" =~ ^[[:space:]]*# ]] && continue
  
  # Trim whitespace
  domain=$(echo "$domain" | xargs)
  
  total=$((total + 1))
  
  # Get certificate expiry
  expiry=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  
  if [ -z "$expiry" ]; then
    echo "[FAILED]   $domain"
    failed=$((failed + 1))
    results+=("{\"domain\":\"$domain\",\"status\":\"failed\",\"days_left\":null,\"expiry\":null}")
    continue
  fi
  
  # Calculate days remaining
  expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null)
  if [ $? -ne 0 ]; then
    # Try macOS format
    expiry_epoch=$(date -j -f "%b %d %T %Y %Z" "$expiry" +%s 2>/dev/null)
  fi
  
  now_epoch=$(date +%s)
  days_left=$(( ($expiry_epoch - $now_epoch) / 86400 ))
  
  # Determine status
  if [ $days_left -lt $CRITICAL_DAYS ]; then
    status="CRITICAL"
    status_key="critical"
    critical=$((critical + 1))
  elif [ $days_left -lt $WARNING_DAYS ]; then
    status="WARNING"
    status_key="warning"
    warning=$((warning + 1))
  else
    status="OK"
    status_key="ok"
    ok=$((ok + 1))
  fi
  
  printf "%-12s %-35s %3d days\n" "$status" "$domain" "$days_left"
  results+=("{\"domain\":\"$domain\",\"status\":\"$status_key\",\"days_left\":$days_left,\"expiry\":\"$expiry\"}")
  
done < "$DOMAINS_FILE"

echo ""
echo "========================="
echo "Summary: $total total | $ok OK | $warning Warning | $critical Critical | $failed Failed"

# Output JSON if requested
if [ "$OUTPUT_FORMAT" = "json" ]; then
  echo ""
  echo "{"
  echo "  \"timestamp\": \"$(date -Iseconds)\","
  echo "  \"summary\": {"
  echo "    \"total\": $total,"
  echo "    \"ok\": $ok,"
  echo "    \"warning\": $warning,"
  echo "    \"critical\": $critical,"
  echo "    \"failed\": $failed"
  echo "  },"
  echo "  \"domains\": ["
  
  for i in "${!results[@]}"; do
    if [ $i -eq $((${#results[@]} - 1)) ]; then
      echo "    ${results[$i]}"
    else
      echo "    ${results[$i]},"
    fi
  done
  
  echo "  ]"
  echo "}"
fi

# Exit with error if any critical or failed
if [ $critical -gt 0 ] || [ $failed -gt 0 ]; then
  exit 1
fi

exit 0
