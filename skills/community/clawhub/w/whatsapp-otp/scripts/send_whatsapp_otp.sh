#!/bin/bash
# Send WhatsApp OTP via CMI OmniChannel RCS API (curl version)
# Usage: ./send_whatsapp_otp.sh <access_key_id> <access_key_secret> <app_name> <app_secret> <to_number> <otp_code>

ACCESS_KEY_ID="$1"
ACCESS_KEY_SECRET="$2"
APP_NAME="${3:-default}"
APP_SECRET="$4"
TO_NUMBER="$5"
OTP_CODE="$6"

# Validate input
if [ -z "$ACCESS_KEY_ID" ] || [ -z "$ACCESS_KEY_SECRET" ] || [ -z "$APP_SECRET" ] || [ -z "$TO_NUMBER" ] || [ -z "$OTP_CODE" ]; then
    echo "[ERROR] Missing required parameters"
    echo "Usage: $0 <access_key_id> <access_key_secret> <app_name> <app_secret> <to_number> <otp_code>"
    exit 1
fi

# Validate phone number format (should not start with +)
if [[ "$TO_NUMBER" == +* ]]; then
    echo "[ERROR] Phone number should NOT include + prefix"
    echo "  Correct format: 8613800138000"
    echo "  Your input: $TO_NUMBER"
    exit 1
fi

# Generate timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Build JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "Method": "SingleSend",
  "AccessKeyId": "$ACCESS_KEY_ID",
  "AccessKeySecret": "$ACCESS_KEY_SECRET",
  "Timestamp": "$TIMESTAMP",
  "ApplicationName": "$APP_NAME",
  "ApplicationSecret": "$APP_SECRET",
  "From": "+8618247665684",
  "To": "$TO_NUMBER",
  "Type": "template",
  "Content": {
    "template": {
      "name": "test_otp_cn_111501",
      "language": {"code": "zh_CN"},
      "components": [
        {"type": "body", "parameters": [{"type": "text", "text": "$OTP_CODE"}]},
        {"type": "button", "sub_type": "url", "index": 0, "parameters": [{"type": "text", "text": "$OTP_CODE"}]}
      ]
    }
  },
  "TemplateName": "test_otp_cn_111501"
}
EOF
)

# Send request
echo "[INFO] Sending WhatsApp OTP to $TO_NUMBER..."
RESPONSE=$(curl --noproxy "*" -s -X POST https://cpaas-rcs.cmidict.com:7081/singleSend \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Parse response
CODE=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('Code', 'N/A'))" 2>/dev/null || echo "N/A")

if [ "$CODE" = "0" ]; then
    echo "[SUCCESS] WhatsApp OTP sent successfully!"
    echo "$RESPONSE" | python -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 0
else
    echo "[ERROR] Failed to send WhatsApp OTP"
    echo "$RESPONSE" | python -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 1
fi
