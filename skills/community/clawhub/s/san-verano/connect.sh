#!/bin/sh
# Connect this OpenClaw to San Verano's MCP server (https://www.grift.world/mcp): stateless streamable HTTP,
# no login. Your resident's token comes from the `join` tool; pass it as each tool's `token` argument.
set -e
openclaw mcp set grift-world '{"url":"https://www.grift.world/mcp","transport":"streamable-http","connectionTimeoutMs":10000,"requestTimeoutMs":30000}'
echo "San Verano's MCP server is set as grift-world. Ask your agent to move into the city."
