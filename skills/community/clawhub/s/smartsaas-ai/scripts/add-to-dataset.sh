#!/usr/bin/env bash
# Add an item to a SmartSaaS data folder (dataset).
# Usage: add-to-dataset.sh <folder_id_or_name> <json_payload>
#   folder_id_or_name - folder _id (24 hex chars, e.g. 69b675c43dcf271d3396630d) OR folder title (e.g. "Investor 1")
#   json_payload      - JSON object for the item (e.g. '{"name":"Jane Doe","description":"..."}')
# With 3 args: add-to-dataset.sh <item_label> <folder_id_or_name> <json_payload> (item_label is ignored)
# Requires: SMARTSAAS_BASE_URL, SMARTSAAS_API_KEY (set in env or openclaw.json skill env)
set -e
BASE="${SMARTSAAS_BASE_URL}"
KEY="${SMARTSAAS_API_KEY}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "Error: SMARTSAAS_BASE_URL and SMARTSAAS_API_KEY must be set." >&2
  exit 1
fi
BASE="${BASE%/}"
AUTH_HEADER="Authorization: Bearer $KEY"
CURL_OPTS="-s -S"
[[ "$BASE" == https://* ]] && CURL_OPTS="$CURL_OPTS -k"

# Reject flags: positional args only
if [ -n "$1" ] && [ "${1#-}" != "$1" ]; then
  echo "Error: Positional args only. Usage: add-to-dataset.sh [item_label] <folder_name_or_id> '<itemJson>'." >&2
  echo "Example: add-to-dataset.sh \"Investor 1\" '{\"name\":\"Jane Doe\",\"description\":\"...\"}'" >&2
  exit 1
fi

# Two args: <folder_id_or_name> <json_payload>
# Three args: <item_label> <folder_id_or_name> <json_payload> (item_label unused)
if [ $# -eq 3 ]; then
  FOLDER_REF="$2"
  PAYLOAD="$3"
elif [ $# -eq 2 ]; then
  FOLDER_REF="$1"
  PAYLOAD="$2"
else
  echo "Usage: $0 <folder_id_or_name> <json_payload>" >&2
  echo "   or: $0 <item_label> <folder_id_or_name> <json_payload>" >&2
  echo "Example (by ID):  $0 69b675c43dcf271d3396630d '{\"name\":\"Jane Doe\",\"company\":\"XYZ\"}'" >&2
  echo "Example (by name): $0 \"Investor 1\" '{\"name\":\"Jane Doe\"}'" >&2
  exit 1
fi

# Trim whitespace so IDs are recognized reliably
FOLDER_REF="${FOLDER_REF#"${FOLDER_REF%%[![:space:]]*}"}"
FOLDER_REF="${FOLDER_REF%"${FOLDER_REF##*[![:space:]]}"}"

# If first arg is 24 hex chars, treat as folder ID and skip name lookup
if [[ "$FOLDER_REF" =~ ^[a-fA-F0-9]{24}$ ]]; then
  FOLDER_ID="$FOLDER_REF"
else
  echo "Resolving folder by name: $FOLDER_REF" >&2
  RESP=$(curl $CURL_OPTS -H "$AUTH_HEADER" "$BASE/api/protected/data/folders?limit=100")
  if ! echo "$RESP" | grep -q '"success":true'; then
    echo "Failed to list folders: $RESP" >&2
    exit 2
  fi
  FOLDER_ID=$(echo "$RESP" | python3 -c "
import sys, json
ref = '''$FOLDER_REF'''.strip().lower().replace(' ', '_')
data = json.load(sys.stdin)
for item in (data.get('data') or []):
    title = (item.get('dataTitle') or '').strip().lower()
    if title == ref or ref in title or ref.replace('_', ' ') in title.replace('_', ' '):
        print(item.get('_id', ''))
        break
" 2>/dev/null)
  if [ -z "$FOLDER_ID" ]; then
    echo "Folder not found: $FOLDER_REF" >&2
    echo "Create it first: curl -k -X POST -H \"Authorization: Bearer \$SMARTSAAS_API_KEY\" -H \"Content-Type: application/json\" -d '{\"name\":\"$FOLDER_REF\"}' \$SMARTSAAS_BASE_URL/api/protected/data/folders" >&2
    exit 3
  fi
  echo "Using folder id: $FOLDER_ID" >&2
fi

# Add item: body is the item JSON directly (no "data" wrapper)
RES=$(curl $CURL_OPTS -w "\n%{http_code}" -X POST -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d "$PAYLOAD" "$BASE/api/protected/data/folders/$FOLDER_ID/items")
HTTP=$(echo "$RES" | tail -n1)
BODY_RES=$(echo "$RES" | sed '$d')

if [ "$HTTP" -ge 200 ] && [ "$HTTP" -lt 300 ]; then
  echo "Item added to dataset $FOLDER_ID."
  echo "$BODY_RES"
else
  echo "Failed (HTTP $HTTP): $BODY_RES" >&2
  exit 4
fi
