#!/bin/bash
# Create a Zoom meeting and add it to a Google Calendar event
# Usage: zoom_meeting.sh <event_id> <topic> <start_time> <duration_minutes>
# Example: zoom_meeting.sh abc123 "Team Meeting" "2026-03-01T11:50:00" 60

set -euo pipefail

EVENT_ID="${1:?Usage: zoom_meeting.sh <event_id> <topic> <start_time> <duration>}"
TOPIC="${2:?Missing topic}"
START_TIME="${3:?Missing start_time (format: YYYY-MM-DDTHH:MM:SS)}"
DURATION="${4:-60}"

CREDS_FILE="${ZOOM_CREDENTIALS:-$HOME/.openclaw/workspace/.credentials/zoom.json}"

# --- Step 1: Create Zoom Meeting ---
ACCOUNT_ID=$(jq -r '.account_id' "$CREDS_FILE")
CLIENT_ID=$(jq -r '.client_id' "$CREDS_FILE")
CLIENT_SECRET=$(jq -r '.client_secret' "$CREDS_FILE")

ZOOM_TOKEN=$(curl -s -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n "${CLIENT_ID}:${CLIENT_SECRET}" | base64)" \
  -d "grant_type=account_credentials&account_id=${ACCOUNT_ID}" | jq -r '.access_token')

if [ -z "$ZOOM_TOKEN" ] || [ "$ZOOM_TOKEN" = "null" ]; then
  echo "ERROR: Failed to get Zoom access token" >&2
  exit 1
fi

ZOOM_RESPONSE=$(curl -s -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer $ZOOM_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"topic\": \"$TOPIC\",
    \"type\": 2,
    \"start_time\": \"$START_TIME\",
    \"duration\": $DURATION,
    \"timezone\": \"Asia/Jerusalem\",
    \"settings\": {
      \"host_video\": true,
      \"participant_video\": true,
      \"join_before_host\": true
    }
  }")

JOIN_URL=$(echo "$ZOOM_RESPONSE" | jq -r '.join_url')
MEETING_ID=$(echo "$ZOOM_RESPONSE" | jq -r '.id')
PASSWORD=$(echo "$ZOOM_RESPONSE" | jq -r '.password')

if [ -z "$JOIN_URL" ] || [ "$JOIN_URL" = "null" ]; then
  echo "ERROR: Failed to create Zoom meeting" >&2
  echo "$ZOOM_RESPONSE" >&2
  exit 1
fi

echo "Zoom meeting created: $JOIN_URL (ID: $MEETING_ID, Pass: $PASSWORD)"

# --- Step 2: Get Google Calendar access token ---
if [ -z "${GOG_KEYRING_PASSWORD:-}" ]; then
  echo "ERROR: GOG_KEYRING_PASSWORD env var is required" >&2
  exit 1
fi
if [ -z "${GOG_ACCOUNT:-}" ]; then
  echo "ERROR: GOG_ACCOUNT env var is required" >&2
  exit 1
fi
export GOG_KEYRING_PASSWORD
export GOG_ACCOUNT

GOG_TOKEN_FILE=$(mktemp)
gog auth tokens export "$GOG_ACCOUNT" --out "$GOG_TOKEN_FILE" --overwrite 2>/dev/null

REFRESH_TOKEN=$(jq -r '.refresh_token' "$GOG_TOKEN_FILE")
GOG_CREDS_FILE="${GOG_CREDENTIALS:-$HOME/.config/gogcli/credentials.json}"
if [ ! -f "$GOG_CREDS_FILE" ]; then
  echo "ERROR: Google credentials not found at $GOG_CREDS_FILE" >&2
  echo "Set GOG_CREDENTIALS env var or install gog CLI first" >&2
  exit 1
fi
GCAL_CLIENT_ID=$(jq -r '.client_id' "$GOG_CREDS_FILE")
GCAL_CLIENT_SECRET=$(jq -r '.client_secret' "$GOG_CREDS_FILE")
rm -f "$GOG_TOKEN_FILE"

ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=$GCAL_CLIENT_ID" \
  -d "client_secret=$GCAL_CLIENT_SECRET" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | jq -r '.access_token')

if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
  echo "ERROR: Failed to get Google access token" >&2
  exit 1
fi

# --- Step 3: Patch Google Calendar event with conferenceData ---
PATCH_RESULT=$(curl -s -X PATCH \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events/${EVENT_ID}?conferenceDataVersion=1" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"conferenceData\": {
      \"conferenceSolution\": {
        \"key\": {\"type\": \"addOn\"},
        \"name\": \"Zoom Meeting\",
        \"iconUri\": \"https://lh3.googleusercontent.com/pw/AM-JKLUkiyTEgH-6DiQP85RGtd_BORvAuFnS9katNMgwYQBJUTiDh12qtQxMJFWYH2Dj30hNsNUrr-kzKMl7jX-Qd0FR7JmVSx-Fhruf8xTPPI-wdsMYez6WJE7tz7KmqsORKBEnBTiILtMJXuMvphqKdB9X=s128-no\"
      },
      \"conferenceId\": \"${MEETING_ID}\",
      \"entryPoints\": [{
        \"entryPointType\": \"video\",
        \"uri\": \"${JOIN_URL}\",
        \"label\": \"Join Zoom Meeting\",
        \"meetingCode\": \"${MEETING_ID}\",
        \"passcode\": \"${PASSWORD}\"
      }],
      \"notes\": \"Meeting host: ${GOG_ACCOUNT}<br /><br />Join Zoom Meeting:<br />${JOIN_URL}\"
    }
  }")

ERROR=$(echo "$PATCH_RESULT" | jq -r '.error.message // empty')
if [ -n "$ERROR" ]; then
  echo "ERROR: Failed to patch calendar event: $ERROR" >&2
  exit 1
fi

echo "SUCCESS: Zoom added to calendar event $EVENT_ID"
echo "Join URL: $JOIN_URL"
echo "Meeting ID: $MEETING_ID"
echo "Password: $PASSWORD"
