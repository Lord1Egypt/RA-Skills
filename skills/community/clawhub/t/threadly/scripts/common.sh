#!/bin/sh
# Sourced by the other scripts in this directory. Not meant to be run directly.

if [ -z "$THREADLY_API_KEY" ]; then
  echo "THREADLY_API_KEY is not set." >&2
  exit 1
fi

BASE="${THREADLY_BASE_URL:-https://api.usethreadly.co}"
AUTH_HEADER="Authorization: Bearer $THREADLY_API_KEY"

# Prints curl's stdout through jq if it's available and the output looks like JSON,
# otherwise prints it raw — jq is a nice-to-have, never a hard requirement. Reads stdin
# into a variable first so a failed jq parse (which would otherwise consume the pipe)
# doesn't leave the raw-output fallback with nothing left to print.
print_response() {
  body="$(cat)"
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$body" | jq . 2>/dev/null || printf '%s\n' "$body"
  else
    printf '%s\n' "$body"
  fi
}
