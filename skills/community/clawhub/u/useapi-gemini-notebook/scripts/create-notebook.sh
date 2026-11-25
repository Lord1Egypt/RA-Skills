#!/usr/bin/env bash
# Create an empty notebook and print its id.
# Usage: create-notebook.sh "<title>"
# With USEAPI_EMAIL set, the notebook goes on that connected Google account; otherwise the API picks one.
source "$(dirname "$0")/_common.sh"
TITLE="${1:?Usage: create-notebook.sh \"<title>\"}"

BODY=$(jq -n --arg t "$TITLE" --arg e "${USEAPI_EMAIL:-}" '{title: $t} + (if $e != "" then {email: $e} else {} end)')
api POST notebooks "$BODY" | jq -r .notebook
