# Web Search, Web Scraping, Crawl, Reddit, YouTube & App Research API

Web research and public data MCP for AI agents: scrape, crawl and map websites; search the web; retrieve brand assets and style guides; research App Store and Google Play apps; search Google Maps and Shopping; access YouTube, Reddit, Instagram, TikTok and Hacker News.

Install from the ReplyNodes agent-skills repository:

```bash
clawhub install @replynodes-ai/web-research-public-data --dir ./skills
```

Or install from a reviewed Git tag:

```bash
git clone --depth 1 --branch v1.0.2 https://github.com/replynodes/replynodes-agent-skills.git
# use the package SKILL.md as the skill entrypoint
```

The package is a portable instruction-only skill. It calls the public
ReplyNodes read gateway at `https://api.replynodes.com`; it has no runtime
dependencies, credentials, OAuth flow, telemetry, or social write path.

Before a paid operation, fetch `/v1/<provider>/capabilities` and use the
live provider capability and pricing contract, including any package-credit
entitlement required by that provider. Never paste a key into an agent
conversation. A `401` means the required access is missing or invalid.

Supported routing includes Web Search, Scrape Markdown, Web Crawl, Website
Map, Brand Info, Retrieve Brand, Search Brand, Get Styleguide, Get Fonts,
Reddit, YouTube, and the existing read-only ReplyNodes provider APIs. See
[`SKILL.md`](SKILL.md) for the exact routing and safety contract.

## Version

This release is `v1.0.2`.
