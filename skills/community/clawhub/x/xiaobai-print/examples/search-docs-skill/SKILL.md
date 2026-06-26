---
name: search-docs-skill
description: "Use this skill when the user needs capabilities exposed by the local MCP bridge. It wraps 1 MCP tool behind a local Node.js wrapper."
allowed-tools: Bash, Read
metadata: {"openclaw":{"emoji":"🧰","requires":{"bins":["node"],"env":["MY_MCP_TOKEN"]},"primaryEnv":"MY_MCP_TOKEN"}}
---

# search-docs-skill

Use this skill when the user needs capabilities exposed by the local MCP bridge. It wraps 1 MCP tool behind a local Node.js wrapper.

This skill targets the local MCP bridge at `http://localhost:8787` by default. Tool schemas are cached in `{baseDir}/schema/tools.json`.

## Available tools

### search_docs
Search documents by keyword

Arguments:
- query (string, required)
- limit (number, optional)

## How to invoke

When you need one of the tools above, run:

`node {baseDir}/scripts/invoke.js <tool-name> '<json-args>'`

Pass valid JSON as the second argument.
Do not invent fields not present in the tool schema.
If the skill is unavailable, configure `skills.entries.search-docs-skill.apiKey` first.
Optionally set `skills.entries.search-docs-skill.env.MY_MCP_BASE_URL` to point at your local bridge.
