# Changelog



## 1.0.3 (2026-03-16)

# wip-xai-grok v1.0.3

Fix: add @modelcontextprotocol/sdk to dependencies. MCP server was failing with ERR_MODULE_NOT_FOUND when deployed via ldm install.

## Issues closed

- Closes #8

## 1.0.2 (2026-02-21)

Release.

## 1.0.1 (2026-02-21)

Release.

## 1.0.0 (2026-02-21)

Initial release. All xAI Grok API functions in one repo.

### Sensor (Search)
- `search_web` ... web search via Grok Responses API
- `search_x` ... X/Twitter search via Grok Responses API

### Actuator (Generate)
- `generate_image` ... text-to-image via Grok Imagine ($0.02/image)
- `edit_image` ... image editing with natural language (up to 3 source images)
- `generate_video` ... text-to-video and image-to-video (1-15 sec, 480p/720p)
- `poll_video` / `wait_for_video` ... async video status polling

### Interfaces
- CLI (`wip-grok`)
- MCP server (6 tools)
- ES module (importable)
- SKILL.md (agent instructions)

Ported search functions from grok-search v1.0.4 by Christopher Stanley (ClawHub).
