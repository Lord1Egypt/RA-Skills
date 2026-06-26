#!/bin/bash
#
# track-metrics.sh - Track growth metrics
# Usage: ./track-metrics.sh [--skill <name>] [--dashboard] [--period 30d]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${GROWTH_DATA_DIR:-$SKILL_DIR/data}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
SKILL_NAME=""
DASHBOARD=false
PERIOD="30d"

while [[ $# -gt 0 ]]; do
    case $1 in
        --skill)
            SKILL_NAME="$2"
            shift 2
            ;;
        --dashboard)
            DASHBOARD=true
            shift
            ;;
        --period)
            PERIOD="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Create data directory
mkdir -p "$DATA_DIR"

METRICS_FILE="$DATA_DIR/METRICS-$(date +%Y%m%d).json"

echo -e "${BLUE}📈 Tracking growth metrics${NC}"
echo "================================"

# Generate simulated metrics
cat > "$METRICS_FILE" << EOF
{
  "dashboard": "growth-metrics",
  "period": "${PERIOD}",
  "generated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "summary": {
    "total_users": $(shuf -i 1000-5000 -n 1),
    "active_users": $(shuf -i 400-2000 -n 1),
    "new_users": $(shuf -i 50-300 -n 1),
    "growth_rate": 0.$(shuf -i 15-45 -n 1),
    "retention": 0.$(shuf -i 35-65 -n 1)
  },
  "loops": [
    {
      "name": "viral",
      "k_factor": 0.$(shuf -i 15-35 -n 1),
      "cycle_time_hours": $(shuf -i 24-72 -n 1),
      "conversion_rate": 0.$(shuf -i 10-25 -n 1),
      "status": "active"
    },
    {
      "name": "content",
      "organic_traffic": $(shuf -i 500-2000 -n 1),
      "conversion_rate": 0.0$(shuf -i 5-15 -n 1),
      "content_velocity": $(shuf -i 10-50 -n 1),
      "status": "active"
    },
    {
      "name": "network",
      "invites_per_user": $(echo "scale=1; $(shuf -i 15-35 -n 1) / 10" | bc),
      "acceptance_rate": 0.$(shuf -i 20-40 -n 1),
      "team_retention": 0.$(shuf -i 50-70 -n 1),
      "status": "active"
    },
    {
      "name": "engagement",
      "dau_mau_ratio": 0.$(shuf -i 35-55 -n 1),
      "avg_sessions_per_week": $(shuf -i 3-8 -n 1),
      "streak_retention": 0.$(shuf -i 25-45 -n 1),
      "status": "active"
    }
  ],
  "funnel": {
    "awareness": $(shuf -i 5000-20000 -n 1),
    "interest": $(shuf -i 1000-5000 -n 1),
    "consideration": $(shuf -i 500-2000 -n 1),
    "activation": $(shuf -i 200-1000 -n 1),
    "retention": $(shuf -i 100-500 -n 1),
    "referral": $(shuf -i 20-100 -n 1)
  }
}
EOF

if [[ "$DASHBOARD" == true ]]; then
    echo ""
    echo "================================"
    echo "Growth Metrics Dashboard"
    echo "================================"
    echo ""
    
    # Parse and display JSON
    if command -v jq >/dev/null 2>&1; then
        echo "Summary:"
        jq -r '.summary | to_entries[] | "  \(.key): \(.value)"' "$METRICS_FILE"
        echo ""
        echo "Loop Performance:"
        jq -r '.loops[] | "  \(.name): K=\(.k_factor // .dau_mau_ratio // .invites_per_user // .organic_traffic)"' "$METRICS_FILE"
    else
        cat "$METRICS_FILE"
    fi
fi

echo -e "${GREEN}✅ Metrics tracked${NC}"
echo -e "${BLUE}📄 Data saved: $METRICS_FILE${NC}"
