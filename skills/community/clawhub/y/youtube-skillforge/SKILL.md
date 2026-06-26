---
name: skillforge
description: Turn YouTube videos into structured, reusable skill files that make any AI agent smarter. Forge, compound, and recall creator-attributed knowledge.
version: 4.1.0
metadata:
  openclaw:
    requires:
      bins:
        - yt-dlp
    install:
      - kind: node
        package: youtube-skillforge
        bins: [skillforge]
        label: "Install SkillForge CLI (npm)"
      - kind: brew
        formula: yt-dlp
        bins: [yt-dlp]
        label: "Install yt-dlp (Homebrew)"
---

# SkillForge

Turn YouTube videos into structured, reusable skill files that make any AI agent smarter.

## Credential Requirements

SkillForge requires **no API keys or credentials** of its own. It produces structured skill files from YouTube transcripts; transcript synthesis uses whatever LLM the user's OpenClaw agent is already configured with (e.g. Claude via `ANTHROPIC_API_KEY`). SkillForge never stores, proxies, or manages provider credentials.

## File System Behavior

SkillForge writes to `~/.skillforge/` on first use. Before creating this directory, the CLI prompts for explicit user consent.

Contents of `~/.skillforge/`:
- `library/` — Skill files organized by creator slug and topic (e.g. `library/alex-hormozi/lead-magnets/SKILL.md`)
- `config.json` — User preferences (trusted creators list, consent flag)
- `proposals/` — Saved scan proposals for deferred builds
- `skills.db` — SQLite full-text search index used by the MCP server and `recall` command

SkillForge does not write outside `~/.skillforge/` unless the user provides an explicit `--output` path.

## MCP Server Behavior

The `skillforge serve` command starts an MCP server using **stdio transport** (`StdioServerTransport` from `@modelcontextprotocol/sdk`). It communicates via stdin/stdout as a subprocess — there is no HTTP server, no port binding, and no network exposure. The host agent (e.g. Claude Desktop) launches SkillForge as a child process and exchanges JSON-RPC messages over the stdio pipe.

The server exposes two tools:
- `skillforge_recall` — Full-text search across indexed skills
- `skillforge_list` — List all skills grouped by creator

On startup, the server rebuilds the SQLite index at `~/.skillforge/skills.db` from skill files on disk.

## Commands

| Command | Writes to `~/.skillforge/` | Description |
|---------|---------------------------|-------------|
| `watch <url>` | Yes | Build a skill from a single YouTube video |
| `build [url]` | Yes | Build from URL, channel, topic, or proposal |
| `scan <url>` | Yes | Score videos by relevance and save a proposal |
| `serve` | Yes | Start the MCP server (stdio transport) |
| `forge` | Yes | Alias for build |
| `trust add/remove` | Yes | Manage trusted creators |
| `recall` | No | Search the skill library by intent |
| `list` | No | List all saved skills |
| `check` | No | Check if a skill exists for an intent |
| `suggest` | No | Search YouTube for channels by topic |
| `share` | No | Export a skill with attribution |
| `check-auth` | No | Verify provider authentication |
