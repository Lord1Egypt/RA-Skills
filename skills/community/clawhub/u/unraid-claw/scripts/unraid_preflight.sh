#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/unraid_common.sh"

require_base_url
require_api_key
require_timeout
require_command "curl" "required for Unraid API calls"

if command -v jq >/dev/null 2>&1; then
  echo "INFO: jq detected. JSON-rich output is enabled."
else
  echo "WARN: jq is not installed. Some scripts will require jq."
fi

echo "INFO: Running Unraid connection smoke test..."
"${SCRIPT_DIR}/unraid_connection_test.sh"
status=$?

if [[ $status -ne 0 ]]; then
  echo "FAIL: Preflight failed because connection smoke test returned ${status}."
  exit $status
fi

echo "PASS: Preflight checks completed."
exit 0