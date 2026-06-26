---
name: wikipedia
version: 1.0.1
description: Access Wikipedia via MCP — search articles, get summaries, random facts, and dinosaur-specific facts. Great for research, hooks, and general knowledge lookups.
---

# Wikipedia MCP

Access Wikipedia via Model Context Protocol (MCP). No API key required.

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search Wikipedia for articles |
| `summary` | Get article summary + image by title |
| `random` | Random Wikipedia article |
| `did_you_know` | Random "Did You Know" fact |
| `dino_fact` | Dinosaur/prehistory fact (specific species or random) |

## Installation (Universal)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

(Requires Python 3.10+ and `requests>=2.28.0`)

### 2. Find your install path

After `clawhub install wikipedia`, the skill lands in your skills directory. The MCP server is at:

```
<install-dir>/src/server.py
```

For example, if you installed into `~/.openclaw/workspace/skills/`:

```bash
# Confirm the path
ls ~/.openclaw/workspace/skills/wikipedia/src/server.py
```

### 3. Add to mcporter

Add this to your mcporter config (e.g. `~/.openclaw/workspace/config/mcporter.json`):

```json
{
  "mcpServers": {
    "wikipedia": {
      "command": "python3",
      "args": ["<path-to>/src/server.py"]
    }
  }
}
```

Replace `<path-to>` with the actual install location from step 2.

### 4. Test

```bash
mcporter call wikipedia search --args '{"query": "velociraptor", "limit": 5}'
```

## Usage Examples

```
mcporter call wikipedia search --args '{"query": "velociraptor", "limit": 5}'
mcporter call wikipedia summary --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia dino_fact --args '{"species": "Spinosaurus"}'
mcporter call wikipedia dino_fact
mcporter call wikipedia did_you_know
```

## Data Source

Uses Wikipedia's free public REST API — no API key required.

- Search: MediaWiki Action API
- Summary: REST API v1 (`/page/summary/{title}`)
- Random: REST API v1 (`/page/random/summary`)

## Notes

- User-Agent is set to `wikipedia-mcp/1.0` for Wikipedia API etiquette
- All responses include links back to the source article on en.wikipedia.org
- `dino_fact` falls back to a random species if the requested one isn't found
