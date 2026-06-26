#!/bin/bash
# Setup YNAB automation - test configuration and list available report scripts
# Usage: ./setup-automation.sh

set -e

SKILL_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load config - env vars take priority, then config file
if [ -n "${YNAB_API_KEY:-}" ] && [ -n "${YNAB_BUDGET_ID:-}" ]; then
  API_KEY="$YNAB_API_KEY"
  BUDGET_ID="$YNAB_BUDGET_ID"
elif [ -f ~/.config/ynab/config.json ]; then
  API_KEY=$(jq -r '.api_key' ~/.config/ynab/config.json)
  BUDGET_ID=$(jq -r '.budget_id // "last-used"' ~/.config/ynab/config.json)
else
  echo "Error: YNAB config not found." >&2
  echo "Set YNAB_API_KEY and YNAB_BUDGET_ID env vars, or create ~/.config/ynab/config.json" >&2
  exit 1
fi

if [ "$API_KEY" = "null" ] || [ -z "$API_KEY" ]; then
  echo "Error: YNAB API key not configured" >&2
  exit 1
fi

echo "Configuration found"
echo ""

# Test API connection
echo "Testing YNAB API connection..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  "https://api.ynab.com/v1/budgets/$BUDGET_ID/months/current" \
  -H "Authorization: Bearer $API_KEY")

if [ "$HTTP_CODE" = "200" ]; then
  echo "API connection OK"
else
  echo "API returned HTTP $HTTP_CODE - check your credentials" >&2
  exit 1
fi

echo ""
echo "Available report scripts:"
echo "  $SKILL_PATH/scripts/daily-budget-check.sh    # Morning budget overview"
echo "  $SKILL_PATH/scripts/goals-progress.sh        # Category goal progress"
echo "  $SKILL_PATH/scripts/scheduled-upcoming.sh     # Upcoming bills"
echo "  $SKILL_PATH/scripts/month-comparison.sh       # Month-over-month spending"
echo "  $SKILL_PATH/scripts/transfer.sh               # Account transfers"
echo "  $SKILL_PATH/scripts/ynab-helper.sh            # General helper (categories, search, etc.)"
echo ""
echo "Schedule these scripts with your platform's cron/scheduler."
echo "All scripts output to stdout -- pipe to any notification channel."
