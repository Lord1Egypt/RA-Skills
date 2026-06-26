#!/bin/bash
# Query Synapse memory records
# Usage: /synapse-code query <project> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUERY_SCRIPT="$SCRIPT_DIR/../scripts/query_memory.py"

if [ ! -f "$QUERY_SCRIPT" ]; then
    echo "Error: query_memory.py not found at $QUERY_SCRIPT"
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: /synapse-code query <project> [options]"
    echo ""
    echo "Options:"
    echo "  --task-type, -t <type>  Filter by task type (debug, refactor, etc.)"
    echo "  --contains, -c <kw>     Search by keyword"
    echo "  --list-types, -l        List all task types"
    echo "  --recent-logs, -r       Show recent log entries"
    echo "  --limit, -n <num>       Max results to return (default: 10)"
    echo "  --json, -j              Output as JSON"
    echo ""
    echo "Examples:"
    echo "  /synapse-code query /path/to/project --task-type debug"
    echo "  /synapse-code query /path/to/project --contains '登录 bug'"
    echo "  /synapse-code query /path/to/project --list-types"
    exit 1
fi

python3 "$QUERY_SCRIPT" "$@"
