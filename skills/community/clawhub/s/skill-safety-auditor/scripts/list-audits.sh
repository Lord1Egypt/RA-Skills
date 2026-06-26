#!/bin/bash
#
# list-audits.sh - List security audit reports
# Usage: ./list-audits.sh [--skill <name>] [--since YYYY-MM-DD]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${AUDIT_DATA_DIR:-$SKILL_DIR/data}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
FILTER_SKILL=""
SINCE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --skill)
            FILTER_SKILL="$2"
            shift 2
            ;;
        --since)
            SINCE="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [[ ! -d "$DATA_DIR" ]]; then
    echo "No audit data found"
    exit 0
fi

echo "Security Audit Reports"
echo "======================"
echo ""

# Find all audit reports
find "$DATA_DIR" -name "AUDIT-*.json" -type f | sort -r | while read -r audit_file; do
    audit_id=$(basename "$audit_file" .json)
    skill=$(jq -r '.skill' "$audit_file" 2>/dev/null || echo "unknown")
    timestamp=$(jq -r '.timestamp' "$audit_file" 2>/dev/null || echo "unknown")
    passed=$(jq -r '.passed' "$audit_file" 2>/dev/null || echo "false")
    critical=$(jq -r '.summary.critical' "$audit_file" 2>/dev/null || echo "0")
    high=$(jq -r '.summary.high' "$audit_file" 2>/dev/null || echo "0")
    
    # Apply filters
    if [[ -n "$FILTER_SKILL" && "$skill" != "$FILTER_SKILL" ]]; then
        continue
    fi
    
    if [[ -n "$SINCE" && "$timestamp" < "${SINCE}T00:00:00Z" ]]; then
        continue
    fi
    
    # Determine status color
    status_color=$GREEN
    if [[ "$passed" != "true" ]]; then
        status_color=$RED
    elif [[ $critical -gt 0 || $high -gt 0 ]]; then
        status_color=$YELLOW
    fi
    
    echo -e "${BLUE}$audit_id${NC} | Skill: $skill | Date: $timestamp"
    echo -e "  Status: ${status_color}$([[ "$passed" == "true" ]] && echo "PASSED" || echo "FAILED")${NC}"
    echo -e "  Issues: Critical=$critical, High=$high"
    echo ""
done
