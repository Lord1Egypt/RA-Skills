#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../xyq.config.json"

usage() {
    echo "Usage: $0 -r <region> -p <prompt> [-t <thread_id>]"
    echo "  -r: Region (oversea or domestic)"
    echo "  -p: Prompt text"
    echo "  -t: Thread ID (optional, will generate if not provided)"
    exit 1
}

generate_uuid() {
    if command -v uuidgen &> /dev/null; then
        uuidgen | tr '[:upper:]' '[:lower:]'
    elif command -v python3 &> /dev/null; then
        python3 -c "import uuid; print(uuid.uuid4())"
    else
        echo "Error: Neither uuidgen nor python3 found to generate UUID" >&2
        exit 1
    fi
}

get_config_value() {
    local region="$1"
    local key="$2"
    python3 -c "import json; import sys; 
config = json.load(open('$CONFIG_FILE')); 
print(config.get('$region', {}).get('$key', ''))"
}

REGION=""
PROMPT=""
THREAD_ID=""

while getopts "r:p:t:" opt; do
    case $opt in
        r) REGION="$OPTARG" ;;
        p) PROMPT="$OPTARG" ;;
        t) THREAD_ID="$OPTARG" ;;
        *) usage ;;
    esac
done

if [ -z "$REGION" ] || [ -z "$PROMPT" ]; then
    usage
fi

if [ "$REGION" != "oversea" ] && [ "$REGION" != "domestic" ]; then
    echo "Error: Region must be either 'oversea' or 'domestic'" >&2
    usage
fi

CONSUMER_UID=$(get_config_value "$REGION" "uid")
WORKSPACE_ID=$(get_config_value "$REGION" "workspace_id")
SPACE_ID=$(get_config_value "$REGION" "space_id")

if [ -z "$CONSUMER_UID" ] || [ -z "$WORKSPACE_ID" ] || [ -z "$SPACE_ID" ]; then
    echo "Error: Missing uid, workspace_id, or space_id in config.json for region $REGION" >&2
    exit 1
fi

[ -z "$THREAD_ID" ] && THREAD_ID=$(generate_uuid)
RUN_ID=$(generate_uuid)
MESSAGE_ID=$(generate_uuid)
REQUEST_ID=$(generate_uuid)
CREATED_AT=0

if [ "$REGION" = "oversea" ]; then
    AGENT_NAME="pippit_compose_agent"
else
    AGENT_NAME="pippit_nest_agent"
fi

python3 -c "
import json
data = {
    'message': {
        'role': 'user',
        'content': [
            {
                'type': 'text',
                'data': '$PROMPT',
                'sub_type': 'plain/text'
            }
        ],
        'thread_id': '$THREAD_ID',
        'run_id': '$RUN_ID',
        'message_id': '$MESSAGE_ID',
        'created_at': $CREATED_AT
    },
    'request_id': '$REQUEST_ID',
    'user_info': {
        'consumer_uid': '$CONSUMER_UID',
        'workspace_id': '$WORKSPACE_ID',
        'space_id': '$SPACE_ID'
    },
    'agent_name': '$AGENT_NAME'
}
print(json.dumps(data, indent=4, ensure_ascii=False))
"
