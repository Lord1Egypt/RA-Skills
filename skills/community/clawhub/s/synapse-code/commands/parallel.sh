#!/bin/bash
# Multi-agent parallel execution for complex tasks
# Usage: /synapse-code parallel <project> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_WORKSPACE="$HOME/pipeline-workspace"
PARALLEL_SCRIPT="$PIPELINE_WORKSPACE/parallel_executor.py"

if [ ! -f "$PARALLEL_SCRIPT" ]; then
    echo "Error: parallel_executor.py not found at $PARALLEL_SCRIPT"
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: /synapse-code parallel <project> [options]"
    echo ""
    echo "Options:"
    echo "  --modules, -m <list>     Comma-separated module names"
    echo "  --auto-detect, -a        Auto-detect modules from ARCH contract"
    echo "  --max-workers, -w <n>    Max parallel workers (default: 3)"
    echo "  --timeout, -t <seconds>  Timeout per module (default: 300)"
    echo "  --verbose, -v            Verbose output"
    echo ""
    echo "Examples:"
    echo "  /synapse-code parallel my-project --auto-detect"
    echo "  /synapse-code parallel my-project -m user,auth,product -w 5"
    echo "  /synapse-code parallel my-project -a -v"
    exit 1
fi

python3 "$PARALLEL_SCRIPT" "$@"
