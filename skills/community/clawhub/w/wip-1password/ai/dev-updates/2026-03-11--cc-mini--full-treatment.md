# Dev Update: Full Treatment

**Date:** 2026-03-11
**Author:** CC-Mini
**Version:** 0.1.0 -> 0.2.0

## What Changed

- **Root SKILL.md** added, conforming to agentskills.io spec (lowercase-hyphen name, metadata block, openclaw install instructions)
- **README reformatted** to WIP Computer standard via `wip-readme-format`. Technical content split to `TECHNICAL.md`.
- **License compliance**: dual MIT+AGPL via `wip-license-guard --from-standard`. CLA.md generated. Attribution added.
- **MCP server** (`mcp-server.mjs`) added for Claude Code access. Uses `op` CLI with service account token. Provides `op_read_secret`, `op_list_items`, `op_test` tools.
- **MCP SDK** added as dependency.

## Why

Part of the distribution fix initiative across all WIP repos. Every tool should have: SKILL.md, license compliance, standard README, npm publish, public repo sync. This repo was missing all of them.

## What's Next

- npm publish from public repo (deploy-public.sh handles this)
- ClawHub publish (blocked by upstream bug #109)
- Consider promoting MCP server to Claude Code MCP registry
