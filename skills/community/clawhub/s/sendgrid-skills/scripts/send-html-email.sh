#!/bin/bash
set -e

# send-html-email.sh
# Send HTML email via SendGrid API
# LIVE SEND: approve sender, recipients, exact HTML and any file before running.
# Only read explicitly approved files; extension/path checks are not a privacy sandbox.

show_help() {
  cat << EOF
Usage: $(basename "$0") <recipient> <subject> [--html|--file] <content-or-file>

Send HTML-formatted email via SendGrid API.

LIVE SEND: approve sender, recipients and exact content before running.
Data goes to SendGrid and recipients; minimize sensitive data. Use a Mail Send-only key.
Only read explicitly approved HTML files; path checks do not prevent sensitive-file disclosure.
This helper has no dry-run or approval prompt. Requires curl, jq 1.6+ and realpath for files.

ARGUMENTS:
  recipient           Recipient email address
  subject             Email subject line
  html-content        HTML content string OR path to HTML file
  --html              Treat content literally, even if it looks like a filename
  --file              Require an existing .html/.htm file

Without a mode, paths and bare .html/.htm names (any case) are files; markup is inline.
File input and resolved paths must still use lowercase .html/.htm extensions.
Use --html for ambiguous literal text ending in .html or .htm.

ENVIRONMENT VARIABLES:
  SENDGRID_API_KEY    SendGrid API key (required)
  SENDGRID_FROM       Sender email address (default: test@example.com)

EXAMPLES:
  # Send HTML string
  $(basename "$0") user@example.com "Welcome" "<h1>Hello!</h1><p>Welcome to our service.</p>"

  # Send HTML file
  $(basename "$0") user@example.com "Daily Report" --file /path/to/report.html

  # With custom sender
  export SENDGRID_FROM="noreply@example.com"
  $(basename "$0") user@example.com "Newsletter" --file newsletter.html

EXIT CODES:
  0   Email sent successfully
  1   Error (missing args, API key, or SendGrid API failure)
  Other nonzero statuses preserve curl transport errors; delivery may be unknown.

EOF
}

# Parse help flag
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
  show_help
  exit 0
fi

# Validate arguments
if [[ $# -lt 3 ]]; then
  echo "❌ Error: Missing required arguments"
  echo ""
  show_help
  exit 1
fi

RECIPIENT="$1"
SUBJECT="$2"
HTML_INPUT="$3"
INPUT_MODE=auto
if [[ "$3" == --html || "$3" == --file ]]; then
  if [[ $# -ne 4 ]]; then
    echo "❌ Error: $3 requires exactly one content or file argument" >&2
    exit 1
  fi
  INPUT_MODE="${3#--}"
  HTML_INPUT="$4"
elif [[ "$3" == --* || $# -ne 3 ]]; then
  echo "❌ Error: Unexpected arguments; use --html or --file" >&2
  exit 1
fi

# Check for API key
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


# Set default sender if not provided
FROM_EMAIL="${SENDGRID_FROM:-test@example.com}"

# File checks reduce accidental reads; they are not a privacy or race sandbox.
if [[ "$INPUT_MODE" == auto ]]; then
  if [[ "$HTML_INPUT" == *'<'* || "$HTML_INPUT" == *'>'* ]]; then
    INPUT_MODE=html
  elif [[ "$HTML_INPUT" == /* || "$HTML_INPUT" == ./* || "$HTML_INPUT" == ../* ||
          "$HTML_INPUT" == *.[hH][tT][mM][lL] || "$HTML_INPUT" == *.[hH][tT][mM] ||
          -e "$HTML_INPUT" || -L "$HTML_INPUT" ]]; then
    INPUT_MODE=file
  else
    INPUT_MODE=html
  fi
fi
if [[ "$INPUT_MODE" == file ]]; then
  # Reject directory traversal attempts
  if [[ "$HTML_INPUT" == *..* ]]; then
    echo "❌ Error: File path must not contain '..' (directory traversal is not allowed)"
    exit 1
  fi
  # Require .html or .htm extension
  if [[ "$HTML_INPUT" != *.html ]] && [[ "$HTML_INPUT" != *.htm ]]; then
    echo "❌ Error: File path must end in .html or .htm"
    exit 1
  fi
  # Resolve to canonical path and confirm it exists
  if [[ ! -f "$HTML_INPUT" ]]; then
    echo "❌ Error: HTML file must exist and be a regular file: $HTML_INPUT" >&2
    exit 1
  fi
  # Prefix relative paths so a leading '-' cannot become a realpath option.
  FILE_PATH="$HTML_INPUT"
  [[ "$FILE_PATH" == /* ]] || FILE_PATH="$PWD/$FILE_PATH"
  RESOLVED_PATH=$(realpath "$FILE_PATH" 2>/dev/null) || {
    echo "❌ Error: File not found or path could not be resolved: $HTML_INPUT"
    exit 1
  }
  if [[ "$RESOLVED_PATH" != *.html && "$RESOLVED_PATH" != *.htm ]]; then
    echo "❌ Error: Resolved file path must end in .html or .htm" >&2
    exit 1
  fi
  # Input is a validated file path — read its contents
  HTML_CONTENT=$(cat "$RESOLVED_PATH")
else
  # Input is an inline HTML string
  HTML_CONTENT="$HTML_INPUT"
fi

# Validate HTML content is not empty
if [[ -z "$HTML_CONTENT" ]]; then
  echo "❌ Error: HTML content is empty"
  exit 1
fi

echo "LIVE SEND: sending approved recipient/content data to SendGrid. No dry-run."
echo "📧 Sending HTML email..."
echo "  From: $FROM_EMAIL"
echo "  To: $RECIPIENT"
echo "  Subject: $SUBJECT"
echo ""

# Builtin printf supplies each field through a descriptor, keeping content off argv.
# jq 1.6+ --rawfile avoids UTF-8 corruption seen with -Rs on jq 1.7.1-apple.
# Shell strings cannot contain NUL. Encode successfully before starting curl.
JSON_PAYLOAD=$(jq -n \
  --rawfile to <(printf '%s' "$RECIPIENT") \
  --rawfile from <(printf '%s' "$FROM_EMAIL") \
  --rawfile subject <(printf '%s' "$SUBJECT") \
  --rawfile html <(printf '%s' "$HTML_CONTENT") \
  '{
    personalizations: [{
      to: [{email: $to}]
    }],
    from: {email: $from},
    subject: $subject,
    content: [{
      type: "text/html",
      value: $html
    }]
  }') || {
  ENCODER_STATUS=$?
  echo "❌ Error: JSON encoding failed (jq exit $ENCODER_STATUS); no email request was made. Requires jq 1.6+." >&2
  exit "$ENCODER_STATUS"
}

# Send via SendGrid API
RESPONSE=$(curl --disable -sS --connect-timeout 10 --max-time 60 \
  --proto =https --noproxy '*' -w "\n%{http_code}" \
  --request POST \
  --url https://api.sendgrid.com/v3/mail/send \
  --config <(printf 'header = "Authorization: Bearer %s"\n' "$SENDGRID_API_KEY") \
  --header 'Content-Type: application/json' \
  --data-binary @- <<<"$JSON_PAYLOAD") || {
  CURL_STATUS=$?
  echo "❌ Error: request to SendGrid failed (curl exit $CURL_STATUS); delivery status is unknown. Do not retry automatically." >&2
  exit "$CURL_STATUS"
}

# Extract HTTP status code (last line)
HTTP_CODE=${RESPONSE##*$'\n'}
RESPONSE_BODY=${RESPONSE%$'\n'*}

# Check response
if [[ "$HTTP_CODE" == "202" ]]; then
  echo "✅ Success! Email queued for delivery (HTTP $HTTP_CODE)"
  echo ""
  echo "Note: Check recipient inbox/spam folder in ~1 minute"
  exit 0
else
  echo "❌ Error: Unexpected response (HTTP $HTTP_CODE)"
  echo ""
  if [[ -n "$RESPONSE_BODY" ]]; then
    echo "Response: $RESPONSE_BODY"
  fi
  exit 1
fi
