#!/bin/bash
# send-test-email.sh - Send a test email via SendGrid to validate configuration
# LIVE SEND: obtain approval for sender, all recipients and exact content first.
# Recipient/content data goes to SendGrid; minimize sensitive data. Mail Send key only.
#
# Usage: ./send-test-email.sh <recipient-email> [subject] [message]
#
# Examples:
#   ./send-test-email.sh vince@example.com
#   ./send-test-email.sh vince@example.com "Test Subject" "Test message body"

set -e

# Help
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
  echo "Usage: $0 <recipient-email> [subject] [message]"
  echo ""
  echo "Send a test email via SendGrid to validate API key and configuration."
  echo "LIVE SEND: approve sender, recipients and exact content before running."
  echo "Data goes to SendGrid and recipients; minimize sensitive data. Use a Mail Send-only key."
  echo "Requires curl and jq 1.6+. This helper has no dry-run or approval prompt."
  echo ""
  echo "Examples:"
  echo "  $0 vince@example.com"
  echo "  $0 vince@example.com \"Test Subject\" \"Test message\""
  echo ""
  echo "Environment variables:"
  echo "  SENDGRID_API_KEY - SendGrid API key (required)"
  echo "  SENDGRID_FROM    - Sender email (default: test@example.com)"
  exit 0
fi

# Validate API key
if [[ -z "$SENDGRID_API_KEY" ]]; then
  echo "❌ Error: SENDGRID_API_KEY environment variable not set"
  echo ""
  echo "Get your API key at: https://app.sendgrid.com/settings/api_keys"
  echo "Then set it: export SENDGRID_API_KEY=SG.xxxxxxxxx"
  exit 1
fi
# Restrict the key alphabet before writing a curl config/header. Reject controls,
# quotes and backslashes rather than interpreting or trying to escape them.
if [[ ! "$SENDGRID_API_KEY" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "❌ Error: SENDGRID_API_KEY contains unsupported characters" >&2
  exit 1
fi


# Validate recipient
if [[ -z "$1" ]]; then
  echo "❌ Error: Recipient email required"
  echo "Usage: $0 <recipient-email> [subject] [message]"
  exit 1
fi

RECIPIENT="$1"
SUBJECT="${2:-SendGrid Test Email}"
MESSAGE="${3:-This is a test email sent via SendGrid API to validate configuration.}"
FROM="${SENDGRID_FROM:-test@example.com}"

echo "LIVE SEND: sending approved recipient/content data to SendGrid. No dry-run."
echo "📧 Sending test email..."
echo "  From: $FROM"
echo "  To: $RECIPIENT"
echo "  Subject: $SUBJECT"
echo ""

# Builtin printf supplies each field through a descriptor, keeping content off argv.
# jq 1.6+ --rawfile avoids UTF-8 corruption seen with -Rs on jq 1.7.1-apple.
# Shell strings cannot contain NUL. jq failure stops the send before transport.
JSON_PAYLOAD=$(jq -n \
  --rawfile to <(printf '%s' "$RECIPIENT") \
  --rawfile from <(printf '%s' "$FROM") \
  --rawfile subject <(printf '%s' "$SUBJECT") \
  --rawfile message <(printf '%s' "$MESSAGE") \
  '{
    personalizations: [{to: [{email: $to}]}],
    from: {email: $from},
    subject: $subject,
    content: [
      {type: "text/plain", value: $message},
      {type: "text/html", value: ("<p>" + ($message | gsub("&"; "&amp;") | gsub("<"; "&lt;") | gsub(">"; "&gt;") | gsub("\r\n|\r|\n"; "<br>")) + "</p>")}
    ]
  }') || {
  ENCODER_STATUS=$?
  echo "❌ Error: JSON encoding failed (jq exit $ENCODER_STATUS); no email request was made. Requires jq 1.6+." >&2
  exit "$ENCODER_STATUS"
}

# Send email via SendGrid API
RESPONSE=$(curl --disable -sS --connect-timeout 10 --max-time 60 \
  --proto =https --noproxy '*' -w "\n%{http_code}" -X POST \
  https://api.sendgrid.com/v3/mail/send \
  --config <(printf 'header = "Authorization: Bearer %s"\n' "$SENDGRID_API_KEY") \
  -H "Content-Type: application/json" \
  --data-binary @- <<<"$JSON_PAYLOAD") || {
  CURL_STATUS=$?
  echo "❌ Error: request to SendGrid failed (curl exit $CURL_STATUS); delivery status is unknown. Do not retry automatically." >&2
  exit "$CURL_STATUS"
}

# Extract status code and body
HTTP_CODE=${RESPONSE##*$'\n'}
BODY=${RESPONSE%$'\n'*}

# Check response
if [[ "$HTTP_CODE" == "202" ]]; then
  echo "✅ Success! Email queued for delivery (HTTP $HTTP_CODE)"
  echo ""
  echo "Note: Check recipient inbox/spam folder in ~1 minute"
elif [[ "$HTTP_CODE" == "401" ]]; then
  echo "❌ Error: Unauthorized (HTTP $HTTP_CODE)"
  echo "API key is invalid or missing Mail Send permissions"
  echo ""
  echo "Response: $BODY"
  exit 1
elif [[ "$HTTP_CODE" == "403" ]]; then
  echo "❌ Error: Forbidden (HTTP $HTTP_CODE)"
  echo "Sender email '$FROM' may not be verified"
  echo ""
  echo "Verify sender at: https://app.sendgrid.com/settings/sender_auth"
  echo ""
  echo "Response: $BODY"
  exit 1
else
  echo "❌ Error: Unexpected response (HTTP $HTTP_CODE)"
  echo ""
  echo "Response: $BODY"
  exit 1
fi
