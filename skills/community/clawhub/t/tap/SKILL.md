---
name: tap
description: "AI browser automation protocol — run pre-built skills for 41 sites, or forge new ones. MCP native, deterministic, zero AI at runtime."
version: 0.1.2
metadata:
  openclaw:
    requires:
      bins:
        - tap
    install:
      - kind: brew
        formula: LeonTing1010/tap/tap
        bins: [tap]
    emoji: "🪶"
    homepage: https://github.com/LeonTing1010/tap
---

# Tap — The Interface Protocol for AI Agents

Tap gives you deterministic browser automation. Instead of burning tokens on every click, **forge a script once and run it forever — zero AI at runtime.**

## How It Works

Tap exposes MCP tools in 6 categories:

### Run Pre-Built Skills (zero AI, instant results)

Use `tap.list` to see all 81 available skills, then `tap.run` to execute:

```
tap.run({ site: "github", name: "trending" })        → trending repos
tap.run({ site: "hackernews", name: "hot" })          → top HN stories
tap.run({ site: "zhihu", name: "hot" })               → Zhihu trending
tap.run({ site: "xiaohongshu", name: "search", args: { keyword: "AI" } })
```

These run in under 1 second, cost $0, and return structured data every time.

**81 skills across 41 sites**: X/Twitter, Reddit, GitHub, YouTube, Bilibili, Zhihu, Xiaohongshu, Weibo, Medium, arXiv, Hacker News, Product Hunt, Bluesky, Steam, CoinGecko, and more.

### Forge New Skills (AI creates, then never needed again)

When you need a site that doesn't have a pre-built skill:

1. **Inspect** — `forge.inspect({ url: "https://example.com" })` analyzes the page structure and available data sources
2. **Verify** — `forge.verify({ url: "...", expression: "..." })` tests the extraction logic live
3. **Save** — `forge.save({ site: "example", name: "data" })` persists the skill

After saving, `tap.run({ site: "example", name: "data" })` works forever. No AI needed.

### Direct Browser Control

Operate the browser via the page API for one-off interactions:

- `page.nav({ url })` — navigate to a page
- `page.click({ target })` — click by selector or visible text
- `page.type({ selector, text })` — type into input fields
- `page.find({ query })` — find elements by text
- `page.screenshot()` — capture the current page
- `page.scroll`, `page.hover`, `page.pressKey`, `page.select`
- `page.fetch({ url })` — make API requests in the page context

### Inspect & Debug

- `inspect.dom` — page DOM structure
- `inspect.a11y` — accessibility tree
- `inspect.page` — page metadata and state
- `inspect.resources` — loaded resources

### Tab Management

- `tab.list` — all open tabs
- `tab.new({ url })` — open new tab
- `tab.close({ tabId })` — close tab

## Setup

### 1. Install Tap

Download the latest binary from [GitHub Releases](https://github.com/LeonTing1010/tap/releases/latest) and add to PATH.

Or build from source (requires Deno):

```bash
git clone https://github.com/LeonTing1010/tap && cd tap
deno compile --allow-read --allow-write --allow-net --allow-env --allow-run --output tap src/cli.ts
```

### 2. Install Chrome Extension

Download `tap-extension.zip` from the [latest release](https://github.com/LeonTing1010/tap/releases/latest), unzip, load as unpacked extension in `chrome://extensions/`.

### 3. Install Community Skills (optional)

```bash
tap install    # 81 skills across 41 sites
```

### 4. Add MCP Server

Add to your OpenClaw MCP configuration:

```json
{
  "mcpServers": {
    "tap": {
      "command": "tap",
      "args": ["mcp"]
    }
  }
}
```

## Common Workflows

### Research: aggregate trending across platforms

```
1. tap.run github/trending
2. tap.run hackernews/hot
3. tap.run reddit/hot
→ Cross-reference results for emerging topics
```

### Monitor: track topics across sites

```
1. tap.run x/search { keyword: "AI agents" }
2. tap.run zhihu/search { keyword: "AI agents" }
3. tap.run xiaohongshu/search { keyword: "AI agents" }
→ Compare discussion across platforms
```

### Publish: cross-post content

```
1. tap.run x/post { content: "..." }
2. tap.run xiaohongshu/publish { title: "...", content: "..." }
3. tap.run telegraph/publish { title: "...", content: "..." }
```

### Forge: create a skill for any new site

```
1. forge.inspect { url: "https://newsite.com" }
2. forge.verify { url: "...", expression: "..." }
3. forge.save { site: "newsite", name: "data" }
4. tap.run newsite/data  ← works forever, zero AI
```

## Security & Trust

**Provenance.** Tap is open source (AGPL-3.0) at [github.com/LeonTing1010/tap](https://github.com/LeonTing1010/tap). All release binaries are built via GitHub Actions — verify by checking the [CI workflow](https://github.com/LeonTing1010/tap/actions/workflows/release.yml).

**Chrome extension permissions.** The extension requires `debugger` permission to send CDP commands to the active tab. It does NOT request `<all_urls>`, `cookies`, or `webRequest` in its manifest. The extension only activates when Tap is explicitly invoked.

**Community skills.** `tap install` clones scripts from [tap-skills](https://github.com/LeonTing1010/tap-skills). All scripts are plain `.tap.js` files (readable JavaScript) — review before running. User-forged taps are stored locally in `~/.tap/taps/`.

**Scope of access.** Tap operates on the active browser tab when invoked. It does not run in the background, does not access tabs you haven't navigated to, and does not persist any data beyond `~/.tap/`.

**Recommendation.** Review the [source code](https://github.com/LeonTing1010/tap/tree/master/src) (~1,800 lines) and [extension manifest](https://github.com/LeonTing1010/tap/blob/master/extension/manifest.json) before installing.
