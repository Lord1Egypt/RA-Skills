# SurfAgent Skill

> Give your AI agent a real Chrome browser. No headless, no cloud, no bot detection.

This is an [agentskills.io](https://agentskills.io)-compatible skill for [SurfAgent](https://surfagent.app) — the Windows desktop app that gives AI agents full control of a real, persistent Chrome browser.

## Install

### Hermes Agent
```bash
hermes skills install github:surfagentapp/surfagent-skill
```

Or manually copy `SKILL.md` to `~/.hermes/skills/browser-automation/surfagent/SKILL.md`.

### OpenClaw
Copy to your OpenClaw skills directory:
```bash
cp SKILL.md ~/clawd/skills/surfagent/SKILL.md
```

### ClawHub
```bash
npx clawhub@latest install surfagent
```

## What You Get

24 MCP tools for complete browser control:

- **Navigate** — open URLs, go back/forward
- **Interact** — click, type, fill forms, select dropdowns, scroll
- **Observe** — screenshot, get text/HTML/URL/title, find elements
- **Tabs** — list, open, switch, close tabs
- **Extract** — structured data extraction with optional LLM
- **Crawl** — BFS site crawling with content extraction
- **Map** — fast URL discovery across a domain
- **JavaScript** — evaluate arbitrary JS in page context
- **Cookies** — get/set browser cookies

## Requirements

1. **SurfAgent** installed and running — [surfagent.app](https://surfagent.app)
2. Windows 10/11 + Google Chrome
3. Connect via MCP: `hermes mcp add surfagent --command npx --args -y surfagent-mcp`

## Why SurfAgent?

| Feature | SurfAgent | Cloud browsers | Playwright MCP |
|---------|-----------|---------------|----------------|
| Real Chrome | ✅ | ❌ Headless | ❌ Chromium |
| Persistent logins | ✅ | ❌ Ephemeral | ❌ Fresh each time |
| Bot detection bypass | ✅ | ⚠️ Sometimes | ❌ |
| 100% local | ✅ | ❌ Cloud | ✅ |
| Price | $49 one-time | $19-399/mo | Free |

## Links

- [SurfAgent](https://surfagent.app) — Download
- [MCP Server](https://github.com/surfagentapp/surfagent-mcp) — Source
- [Documentation](https://github.com/surfagentapp/surfagent-docs) — Full docs
- [License API](https://api.surfagent.app) — Backend

## License

MIT
