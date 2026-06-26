#!/bin/bash
# Invoke the batch_solution_workflow MCP tool
# Usage: ./call_batch_solution_workflow.sh '<workflow_type>' '<problems_json>'
# workflow_type example: 'INNOVATION'
# problems_json example: '[{"problem_type":"xxx","problem_description":"xxx"}]'

MCP_URL="https://qa-eureka-service.zhihuiya.com/eureka-rd-agent-mcp/rd-agent-mcp-triz-mind/mcp"

WORKFLOW_TYPE="$1"
PROBLEMS_JSON="$2"

if [ -z "$WORKFLOW_TYPE" ] || [ -z "$PROBLEMS_JSON" ]; then
    echo "Usage: ./call_batch_solution_workflow.sh '<workflow_type>' '<problems_json>'"
    exit 1
fi

curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  --data "$(jq -n \
    --arg workflow_type "$WORKFLOW_TYPE" \
    --argjson problems "$PROBLEMS_JSON" \
    '{
      "jsonrpc": "2.0",
      "id": 1,
      "method": "tools/call",
      "params": {
        "name": "batch_solution_workflow",
        "arguments": {
          "workflow_type": $workflow_type,
          "problems": $problems
        }
      }
    }')"
