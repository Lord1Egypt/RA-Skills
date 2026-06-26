# Serpzilla SEO Guest Posting Skill for OpenClaw

This skill enables [OpenClaw](https://github.com/openclaw) agents to automate the purchase of guest posts and
link insertions via the [Serpzilla](https://serpzilla.com) platform. It provides a structured workflow for
SEO specialists to search donor sites, manage content, buy placements, and control the entire backlink
acquisition process.

## Features

- Create projects for your promoted websites  
- Search and filter donor sites by price, DR, language, etc.  
- Upload articles for moderation (`news` format)  
- Buy four types of placements:  
  - `news` – advertiser’s article (guest post)  
  - `review` – publisher’s written review article  
  - `link` – natural link insertion into a news article  
  - `archive` – link placed into an existing article  
- Manage purchased placements (approve, cancel, request teardown, etc.)

## Prerequisites

- [OpenClaw](https://github.com/openclaw) agent environment  
- [mcporter](https://github.com/modelcontextprotocol/mcporter) – MCP server manager  
- **Docker** – runs the Serpzilla MCP server  
- **Node.js / npm** – to install `mcporter`

## Repository contents
- `SKILL.md` – the complete skill definition, including all steps, entity descriptions, and management actions.
- `references/placement_actions.md` – detailed reference of SEO‑available placement actions
  (approve_seo, cancel_seo, terminate_seo, etc.).

## See also

* The Serpzilla MCP server Docker image is available at https://hub.docker.com/r/stanislavusbest/serpzilla-mcp-stdio-server/tags
* The MCP server source code: https://github.com/stanislav-reshetnev/serpzilla-mcp-server