#!/bin/bash
# WhatsApp Lead Hunter - Batch Send Script
# Sends personalized messages to leads via WAHA API
#
# Usage:
#   batch_send.sh --leads leads.json --message "Your message" --waha-url http://localhost:3000 --waha-key KEY --delay 120
#
# Arguments:
#   --leads         Path to JSON file with leads (must have "phone" field)
#   --message       Message text (use {name} for business name placeholder)
#   --waha-url      WAHA API URL (default: http://localhost:3000)
#   --waha-key      WAHA API key
#   --delay         Delay between messages in seconds (default: 120, minimum: 60)
#   --ignore-file   Path to ignore list file (appends sent numbers)
#   --dry-run       Print messages without sending
#   --session       WAHA session name (default: "default")

set -e

LEADS=""
MESSAGE=""
WAHA_URL="http://localhost:3000"
WAHA_KEY=""
DELAY=120
IGNORE_FILE=""
DRY_RUN=false
SESSION="default"

while [[ $# -gt 0 ]]; do
  case $1 in
    --leads) LEADS="$2"; shift 2 ;;
    --message) MESSAGE="$2"; shift 2 ;;
    --waha-url) WAHA_URL="$2"; shift 2 ;;
    --waha-key) WAHA_KEY="$2"; shift 2 ;;
    --delay) DELAY="$2"; shift 2 ;;
    --ignore-file) IGNORE_FILE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --session) SESSION="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$LEADS" ] || [ -z "$WAHA_KEY" ]; then
  echo "Usage: batch_send.sh --leads FILE --waha-key KEY [--message MSG] [--delay SECS]"
  exit 1
fi

if [ "$DELAY" -lt 60 ]; then
  echo "⚠️  Minimum delay is 60 seconds to avoid WhatsApp spam detection"
  DELAY=60
fi

if [ ! -f "$LEADS" ]; then
  echo "❌ Leads file not found: $LEADS"
  exit 1
fi

# Count leads
TOTAL=$(python3 -c "import json; print(len(json.load(open('$LEADS'))))")
echo "📋 $TOTAL leads loaded from $LEADS"
echo "⏱️  Delay: ${DELAY}s between messages"
echo "📡 WAHA: $WAHA_URL (session: $SESSION)"
[ "$DRY_RUN" = true ] && echo "🔍 DRY RUN MODE — no messages will be sent"
echo ""

SENT=0
FAILED=0

# Process each lead
python3 -c "
import json, sys
leads = json.load(open('$LEADS'))
for lead in leads:
    name = lead.get('name', 'Unknown')
    phone = lead.get('phone', '').replace('+', '').replace(' ', '').replace('-', '')
    if phone:
        print(f'{phone}|{name}')
" | while IFS='|' read -r PHONE NAME; do
  SENT=$((SENT + 1))
  
  # Personalize message
  MSG=$(echo "$MESSAGE" | sed "s/{name}/$NAME/g" | sed "s/{business_name}/$NAME/g")
  
  if [ "$DRY_RUN" = true ]; then
    echo "[$SENT/$TOTAL] 📝 Would send to $NAME ($PHONE)"
  else
    RESULT=$(curl -s -X POST "$WAHA_URL/api/sendText" \
      -H "X-Api-Key: $WAHA_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"session\": \"$SESSION\", \"chatId\": \"${PHONE}@c.us\", \"text\": $(echo "$MSG" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}" 2>/dev/null)
    
    if echo "$RESULT" | grep -q '"id"'; then
      echo "$(date '+%H:%M:%S') ✅ [$SENT/$TOTAL] $NAME ($PHONE)"
      
      # Add to ignore list
      if [ -n "$IGNORE_FILE" ]; then
        echo "$PHONE" >> "$IGNORE_FILE"
      fi
    else
      echo "$(date '+%H:%M:%S') ❌ [$SENT/$TOTAL] $NAME ($PHONE) — Failed (no WhatsApp?)"
      FAILED=$((FAILED + 1))
    fi
    
    # Delay between messages (skip after last)
    if [ "$SENT" -lt "$TOTAL" ]; then
      echo "⏳ Waiting ${DELAY}s..."
      sleep "$DELAY"
    fi
  fi
done

echo ""
echo "🎯 Complete! Sent: $((SENT - FAILED)) | Failed: $FAILED | Total: $TOTAL"
