# searxng-web-search

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-blue)](https://agentskills.io)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-published-orange)](https://clawhub.ai)

A privacy-respecting web search skill for AI agents, powered by [SearXNG](https://docs.searxng.org/) metasearch engine. Follows the [agentskills.io](https://agentskills.io) standard.

Rewritten from [PulseBot](https://github.com/timeplus-io/PulseBot)'s built-in `web_search` skill to use SearXNG as a self-hosted, privacy-first search backend.

## Features

- **Privacy-first**: SearXNG aggregates 243+ search engines without tracking users
- **Self-hosted**: Full control over your search infrastructure
- **Multi-category**: Search general web, news, images, IT, science, and more
- **Structured output**: JSON results with title, URL, snippet, score, and engine attribution
- **Agent-ready**: Works with PulseBot, Claude Code, OpenClaw, GitHub Copilot, and any agentskills.io-compatible agent
- **Robust error handling**: Graceful failures with structured error responses

## Quick Start

### 1. Install the Skill

**Via ClawHub CLI:**

```bash
npm i -g clawhub
clawhub install searxng-web-search
```

**Via Git:**

```bash
git clone https://github.com/timeplus-io/searxng-web-search.git
cp -r searxng-web-search ~/.openclaw/workspace/skills/
# or for Claude Code:
cp -r searxng-web-search .claude/skills/
```

### 2. Start SearXNG

```bash
docker run -d --name searxng -p 8080:8080 \
  -v "$(pwd)/searxng:/etc/searxng" searxng/searxng:latest
```

> **Important**: Enable JSON API in your SearXNG `settings.yml` — see [references/REFERENCE.md](references/REFERENCE.md).

### 3. Install Python Dependency

```bash
pip install requests
```

### 4. Search

```bash
# CLI
python scripts/searxng_search.py "latest streaming SQL developments"

# Human-readable output
python scripts/searxng_search.py "SearXNG setup guide" --text

# News search, last 24 hours
python scripts/searxng_search.py "AI agents" --categories news --time-range day

# Health check
python scripts/searxng_search.py --health
```

## Directory Structure

```
searxng-web-search/
├── SKILL.md                    # Skill metadata + instructions (agentskills.io)
├── README.md                   # This file
├── LICENSE                     # Apache 2.0
├── scripts/
│   └── searxng_search.py       # Main search tool (CLI + importable module)
├── references/
│   └── REFERENCE.md            # SearXNG API reference & setup guide
└── assets/
    └── settings.example.yml    # Example SearXNG configuration
```

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `SEARXNG_BASE_URL` | `http://localhost:8080` | SearXNG instance URL |
| `SEARXNG_MAX_RESULTS` | `10` | Max results per query |
| `SEARXNG_LANGUAGE` | `all` | Default language |
| `SEARXNG_SAFESEARCH` | `0` | Safe search (0/1/2) |
| `SEARXNG_TIMEOUT` | `15` | Request timeout (seconds) |
| `SEARXNG_CATEGORIES` | `general` | Default categories |

## Compatibility

This skill follows the [agentskills.io specification](https://agentskills.io/specification) and works with:

- [PulseBot](https://github.com/timeplus-io/PulseBot) — Stream-native AI agent framework
- [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) — Anthropic's coding agent
- [OpenClaw / ClawHub](https://clawhub.ai) — Open-source AI agent platform
- [GitHub Copilot](https://code.visualstudio.com/docs/copilot/customization/agent-skills) — VS Code agent skills
- [OpenAI Codex](https://developers.openai.com/codex/skills/) — OpenAI's coding agent
- Any agent that supports the agentskills.io SKILL.md standard

## Publishing to ClawHub

```bash
npm i -g clawhub
clawhub login
clawhub publish ./searxng-web-search \
  --slug searxng-web-search \
  --name "SearXNG Web Search" \
  --version 1.0.0 \
  --changelog "Initial release: SearXNG-powered web search skill" \
  --tags "search,web,searxng,privacy,metasearch"
```

## License

Apache 2.0 — see [LICENSE](LICENSE).

## Credits

- Originally based on [PulseBot](https://github.com/timeplus-io/PulseBot) by [Timeplus](https://www.timeplus.com)
- Powered by [SearXNG](https://github.com/searxng/searxng)
- Follows the [Agent Skills](https://agentskills.io) open standard
