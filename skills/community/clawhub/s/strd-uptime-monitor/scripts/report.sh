#!/bin/bash
# report.sh — Generate daily uptime summary from logs
# Usage: ./report.sh [days]

DAYS="${1:-7}"
LOG_FILE="$(dirname "$0")/../logs/status.log"

if [ ! -f "$LOG_FILE" ]; then
  echo "No log file found at $LOG_FILE"
  echo "Run some checks first with check.sh"
  exit 1
fi

# Calculate cutoff timestamp
cutoff_date=$(date -u -d "$DAYS days ago" +%Y-%m-%d 2>/dev/null || date -u -v-${DAYS}d +%Y-%m-%d)

echo "# Uptime Report — Last $DAYS Days"
echo ""
echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Get unique URLs
urls=$(cut -d'|' -f2 "$LOG_FILE" | sort -u)

total_checks=0
total_up=0

for url in $urls; do
  # Count checks for this URL
  checks=$(grep "|${url}|" "$LOG_FILE" | grep -v "^${cutoff_date}" | wc -l)
  up_checks=$(grep "|${url}|OK|" "$LOG_FILE" | grep -v "^${cutoff_date}" | wc -l)
  
  if [ "$checks" -gt 0 ]; then
    uptime_pct=$(echo "scale=2; ($up_checks / $checks) * 100" | bc 2>/dev/null || echo "N/A")
    
    # Determine status emoji
    if command -v bc &>/dev/null; then
      if [ "$uptime_pct" = "100.00" ]; then
        status="✅"
      elif (( $(echo "$uptime_pct >= 99" | bc -l) )); then
        status="🟢"
      elif (( $(echo "$uptime_pct >= 95" | bc -l) )); then
        status="🟡"
      else
        status="🔴"
      fi
    else
      status="📊"
    fi
    
    echo "## $status $url"
    echo ""
    echo "| Metric | Value |"
    echo "|--------|-------|"
    echo "| Total Checks | $checks |"
    echo "| Successful | $up_checks |"
    echo "| Downtime | $((checks - up_checks)) |"
    echo "| Uptime | ${uptime_pct}% |"
    echo ""
    
    total_checks=$((total_checks + checks))
    total_up=$((total_up + up_checks))
  fi
done

if [ "$total_checks" -gt 0 ]; then
  overall_uptime=$(echo "scale=2; ($total_up / $total_checks) * 100" | bc 2>/dev/null || echo "N/A")
  echo "---"
  echo ""
  echo "**Overall: ${overall_uptime}%** uptime across all monitored services."
fi

# Recent alerts
ALERT_LOG="$(dirname "$0")/../logs/alerts.log"
if [ -f "$ALERT_LOG" ] && [ -s "$ALERT_LOG" ]; then
  echo ""
  echo "## Recent Alerts"
  echo ""
  tail -10 "$ALERT_LOG" | while read -r line; do
    echo "- \`$line\`"
  done
fi
