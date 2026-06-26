#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
source "$SCRIPT_DIR/../../reference/config.sh"
source "$SCRIPT_DIR/../../reference/runtime.sh"

se_request "GET" "/api/analytics/summary"
