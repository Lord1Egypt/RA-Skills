#!/usr/bin/env bash
# List UniFi Integration API sites
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/unifi-api.sh"

FORMAT="${1:-table}"

data=$(curl -sk \
  -H "X-API-KEY: $UNIFI_TOKEN" \
  -H "Accept: application/json" \
  "$UNIFI_URL/proxy/network/integration/v1/sites")

if [ "$FORMAT" = "json" ]; then
  echo "$data"
else
  echo "$data" | jq -r '
    ["SITE ID", "REF", "NAME"],
    ["-------", "---", "----"],
    (.data[] | [
      .id,
      (.internalReference // "N/A"),
      (.name // "N/A")
    ]) | @tsv
  ' | column -t -s $'\t'
fi
