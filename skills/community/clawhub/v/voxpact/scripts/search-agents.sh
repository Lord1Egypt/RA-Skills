#!/usr/bin/env bash
# Search for agents by capability
# Usage: search-agents.sh [capability] [limit]

source "$(dirname "$0")/lib.sh"

capability="${1:-}"
limit="${2:-20}"

path="/v1/agents/search?limit=${limit}"
if [[ -n "$capability" ]]; then
  path="${path}&capability=${capability}"
fi

vox_api GET "$path" | pretty_json
