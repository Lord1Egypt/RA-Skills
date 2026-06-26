# WeChat Article to Obsidian

An AI Agent skill that saves WeChat public account articles (微信公众号文章) as clean Markdown notes in your Obsidian vault.

No browser needed. No plugins. No login. Just give it a link.

Works with any AI coding agent that can run shell commands — Claude Code, OpenClaw, Cursor, Windsurf, etc.

## Features

- **Fast path + browser fallback** — first tries `curl`, then falls back to Playwright + Chrome when WeChat only returns a shell page
- **Zero mandatory browser dependency on happy path** — simple articles still work with just `curl` and `Node.js`
- **Clean Markdown output** — proper headings, bold/italic, code blocks, blockquotes, lists, links
- **Images preserved** — all article images kept as WeChat CDN links (renders in Obsidian)
- **Smart cleanup** — auto-removes WeChat decoration text (THUMB/STOPPING), merges PART headings, strips promotional tails (关注/点赞/在看)
- **YAML frontmatter** — title, author, publish date, source URL
- **Batch support** — save multiple articles at once
- **Natural language paths** — tell your AI agent where to save: "存到 reading/tech 目录"
- **One-time config** — set your vault name and default path once, then it just works

## How it works

The skill now uses a two-stage strategy:

1. **Fast path**: try a simple `curl` request first.
2. **Fallback path**: if WeChat only returns a shell page and `#js_content` is missing, use Playwright + Chrome to open the page in a real browser context and extract the rendered article body.

Then a Node.js parser converts the HTML into clean Markdown and saves it to your Obsidian vault.

## Installation

### Claude Code

```bash
cp -r wechat-article-to-obsidian ~/.claude/skills/
```

### OpenClaw (小龙虾)

```bash
# Option A: manual install
cp -r wechat-article-to-obsidian ~/.openclaw/workspace/skills/

# Option B: if published to ClawHub
openclaw skill install wechat-article-to-obsidian
```

The included `skill.json` provides OpenClaw-compatible metadata (triggers, config schema, script paths).

### Other AI Agents

The core scripts work standalone. Point your agent to use:

- `scripts/fetch.sh <url> <output.html>` — fetch the article HTML with curl
- `scripts/fetch-browser.py <url> <output.html>` — fetch rendered article HTML with Python Playwright fallback
- `scripts/parse.mjs <input.html>` — convert to Markdown (stdout)
- `scripts/parse.mjs <input.html> --json` — get metadata as JSON
- `scripts/save.mjs --markdown <file> --config <config.json> --title <title> [--target-path <path>]` — save safely to Obsidian by direct write inside the configured vault root

Feed the `SKILL.md` file to your agent as a system prompt or instruction file so it knows how to orchestrate the workflow.

## Usage

Just give your AI agent a WeChat article link:

```
帮我把这篇文章存到 Obsidian
https://mp.weixin.qq.com/s/xxxxx
```

On first use, the agent will ask you for the needed vault config if it's missing.

Recommended setup:
1. Vault name: your Obsidian vault name (optional reference)
2. Default save path: `notes/wechat`
3. Vault disk root: your Obsidian vault's absolute disk path

After that, it's fully automatic.

### More examples

```
# Save to a specific folder
把这篇微信文章导入到 Obsidian 的 reading/ai 目录
https://mp.weixin.qq.com/s/xxxxx

# Batch save
帮我把下面几篇文章都存到 Obsidian
https://mp.weixin.qq.com/s/aaa
https://mp.weixin.qq.com/s/bbb
https://mp.weixin.qq.com/s/ccc
```

## Output example

```markdown
---
title: "Article Title Here"
author: "公众号名称"
publish_date: "2026-03-31 19:45:08"
saved_date: "2026-03-31"
source: "wechat"
url: "https://mp.weixin.qq.com/s/xxxxx"
---

# Article Title Here

Article content with **bold**, *italic*, `code`, and images preserved...
```

## File structure

```
wechat-article-to-obsidian/
├── SKILL.md        # Agent instructions (workflow + config)
├── skill.json      # OpenClaw-compatible metadata (triggers, config schema)
├── config.json     # Your vault config (auto-filled on first use)
├── README.md       # This file
└── scripts/
    ├── fetch.sh          # curl wrapper with browser-like headers
    ├── fetch-browser.py  # Python Playwright + Chrome fallback fetcher
    ├── parse.mjs         # HTML → Markdown parser with cleanup
    └── save.mjs          # Safe save helper: direct-write inside configured vault root
```

## How articles are saved to Obsidian

The skill now uses a dedicated safe saver script:

- resolve the final path only under the configured vault root
- reject unsafe output paths that try to escape the vault root
- create parent folders as needed
- write Markdown directly to disk

This is intentionally stricter to avoid command-execution style save flows.

For example, `notes/wechat` should resolve to:
`<vault_disk_root>/notes/wechat`

It should not be rewritten to an app-specific subfolder unless the user explicitly asked for that.

## Requirements

- An AI coding agent (Claude Code, OpenClaw, Cursor, or any agent that can run shell commands)
- [Obsidian](https://obsidian.md)
- [obsidian-cli](https://github.com/Yakitrak/obsidian-cli) (optional)
- Node.js >= 18
- curl

## Limitations

- Some special article types (mini-programs, video-only posts) are not supported
- WeChat may rate-limit heavy usage — wait 30 seconds and retry
- Images use WeChat CDN links (`mmbiz.qpic.cn`) which may not render outside Obsidian/Typora

## License

MIT
