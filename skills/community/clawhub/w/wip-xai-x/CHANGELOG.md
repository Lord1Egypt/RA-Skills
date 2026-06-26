# Changelog

## 1.0.4 (2026-03-16)

# wip-xai-x v1.0.4

Two fixes for MCP server startup:

1. v1.0.3: Added @modelcontextprotocol/sdk to dependencies (was imported but not declared). Closes wipcomputer/wip-xai-x#3
2. v1.0.4: Fixed schema imports (ListToolsRequestSchema/CallToolRequestSchema instead of method literals). Closes wipcomputer/wip-xai-x#4

## Issues closed

- Closes #4

## 1.0.3 (2026-03-16)

# wip-xai-x v1.0.3

Fix: add @modelcontextprotocol/sdk to dependencies. MCP server was failing with ERR_MODULE_NOT_FOUND when deployed via ldm install.

## Issues closed

- Closes #3

## 1.0.2 (2026-02-28)

- Rename wip-x to wip-xai-x across all internal references
- Add ai/ folder for private repo pattern

## 1.0.1 (2026-02-21)

Rename doors to interfaces in README. Auth config env vars.

## 1.0.0 (2026-02-20)

Initial release. X Platform API wrapper built on @xdevplatform/xdk.
