---
description: Use ZHIPU AI's Web Search API to search the web (optimized for Chinese, supports 4 engines). Use when user asks to search, especially for Chinese content.
---

# Z.AI Web Search API Skill

Search the web using ZHIPU AI's Web Search API —— an LLM-optimized search engine that returns structured results (title, URL, snippet, site name, icon) with intent recognition.

## Overview

This skill provides AI-powered web search with support for multiple Chinese search engines. It's particularly optimized for Chinese-language content and LLM processing.

### Search Engines Available

| Engine | Provider | Description |
|--------|----------|-------------|
| `search_std` | 智谱 AI | 基础版，快速响应 |
| `search_pro` | 智谱 AI | 高阶版，最佳质量 |
| `search_pro_sogou` | 搜狗 | 搜狗搜索结果 |
| `search_pro_quark` | 夸克 | 夸克搜索结果 |

### Pricing

See the official pricing page: [https://open.bigmodel.cn/pricing](https://open.bigmodel.cn/pricing)

- Web Search API uses token-based pricing
- Different engines have different rates
- Check the official page for the latest rates

### Comparison with Other Search Tools

| Feature | This Skill (Z.AI) | Brave Search |
|---------|-------------------|--------------|
| Chinese Support | ✅ Excellent | ⚠️ Limited |
| Intent Recognition | ✅ Yes | ❌ No |
| Multiple Engines | ✅ 4 engines | ❌ 1 engine |
| Time Filters | ✅ Yes | ✅ Yes |
| Domain Filter | ✅ Yes | ❌ No |

## First-Time Setup (For Users)

When you use this skill for the first time in OpenClaw, you'll be asked to configure it.

### Configuration Steps

1. **Get an API Key**: Visit [https://open.bigmodel.cn](https://open.bigmodel.cn) to register and get your API key

2. **Choose Configuration Method**:
   - Create `config.json` in this skill folder (recommended)
   - Set `ZAI_API_KEY` environment variable
   - Use user config at `~/.config/zai-web-search/config.json`

3. **Replace Other Search Skills** (Optional)

   This skill can potentially replace other search-related skills:
   - **Brave Search** (OpenClaw built-in): Replace for better Chinese search
   - Other web search skills: Compare features before replacing

   When asked, indicate if you want this skill to be your primary search tool.

### Default Behavior

After setup, this skill will:
- Use `search_std` engine by default
- Return 10 results
- Apply no time filter
- Use medium content summary

You can override these defaults via CLI arguments or config file.

## When to Use

- The user asks to search the web (especially in Chinese)
- You need up-to-date information from Chinese-language sources
- `web_search` (Brave) is unavailable or insufficient
- You want intent-enhanced search with better results for LLM processing

## Agent Instructions (For First-Time Use)

When the user invokes this skill for the first time:

1. **Display an Overview**:
   ```
   Z.AI Web Search API Skill
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   This skill provides AI-powered web search with 4 Chinese search engines.

   Available Engines:
   • search_std (智谱基础版) - Fast, default
   • search_pro (智谱高阶版) - Best quality
   • search_pro_sogou (搜狗) - Sogou search
   • search_pro_quark (夸克) - Quark search

   Pricing: https://open.bigmodel.cn/pricing
   ```

2. **Check Configuration Status**:
   - Verify if `config.json` exists or `ZAI_API_KEY` is set
   - If not configured, guide the user through setup

3. **Ask About Replacing Other Search Tools**:
   ```
   This skill can potentially replace your current search setup:

   1. Brave Search (OpenClaw built-in) - Replace for better Chinese support?
   2. Other search skills - Check which ones are installed and ask

   Would you like to:
   [1] Use this as your primary search tool
   [2] Keep your current search setup and use this as needed
   [3] See more details first
   ```

4. **Check for Other Search Skills** (if user chooses option 3 or asks for details):
   - Use Glob to search for other search-related skills
   - Compare features and present options to the user

5. **After Configuration**:
   - Confirm the setup is complete
   - Show a quick example usage

## Prerequisites

- **API Key:** A Z.AI (智谱) API key from https://open.bigmodel.cn
- **Config:** Set via environment variable `ZAI_API_KEY` or create `config.json` in this skill folder

### Quick Setup

**Option 1: Config file in skill folder (recommended, easy to share)**

```bash
# Copy example and edit
cp config.json.example config.json
# Edit config.json with your settings
```

**Important**: `config.json.example` contains comments for reference only. Your `config.json` must be valid JSON without any comments. Remove all `//` comments before saving.

The config.json supports all search parameters:
```json
{
  "apiKey": "your-api-key-here",
  "engine": "search_std",
  "intent": false,
  "count": 10,
  "recency": "noLimit",
  "content": "medium",
  "domain": ""
}
```

See [config.json.example](config.json.example) for detailed parameter descriptions and available values.

**Option 2: Environment variable**

```bash
export ZAI_API_KEY="your-api-key-here"
```

**Option 3: User config file (overrides skill folder config)**

```bash
mkdir -p ~/.config/zai-web-search
# Copy the example from skill folder
cp config.json.example ~/.config/zai-web-search/config.json
# Edit with your settings
```

### Config Priority

1. Command-line arguments (highest priority)
2. Environment variable `ZAI_API_KEY`
3. `~/.config/zai-web-search/config.json` (user config)
4. `config.json` in skill folder (lowest priority)

Add `export ZAI_API_KEY="..."` to your shell profile for persistence.

## CLI Usage

The skill provides a CLI script `zai-search`:

### Basic Search

```bash
# Default: search_std engine, 10 results
zai-search "哈尔滨冰雪大世界 2026"

# Specify engine
zai-search "北京天气预报" --engine search_pro

# Intent-aware search (recommended for ambiguous queries)
zai-search "今天吃什么" --intent

# More results
zai-search "人工智能最新进展" --count 20

# Recent results only
zai-search "乒乓球比赛" --recency oneWeek

# Detailed content (high instead of medium summary)
zai-search "React 19 new features" --content high

# Filter to specific domains
zai-search "OpenClaw documentation" --domain docs.openclaw.ai
```

### Output Formats

```bash
# Markdown (default, human-readable)
zai-search "query"

# JSON (for scripting / parsing)
zai-search "query" --json

# Compact (title + URL only)
zai-search "query" --compact
```

### Available Engines

| Engine | Description |
|--------|-------------|
| `search_std` | 智谱基础版 (default) |
| `search_pro` | 智谱高阶版 (best quality) |
| `search_pro_sogou` | 搜狗搜索 |
| `search_pro_quark` | 夸克搜索 |

### Other Options

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--engine` | `-e` | search_std, search_pro, search_pro_sogou, search_pro_quark | search_std |
| `--intent` | `-i` | flag (enable intent recognition) | false |
| `--count` | `-c` | 1-50 | 10 |
| `--recency` | `-r` | oneDay, oneWeek, oneMonth, oneYear, noLimit | noLimit |
| `--content` | `-s` | medium, high | medium |
| `--domain` | `-d` | domain string | (none) |
| `--json` | `-j` | flag (JSON output) | false |
| `--compact` | `-k` | flag (compact output) | false |

## Agent Integration

You can also call the API directly via curl:

```bash
curl -s https://open.bigmodel.cn/api/paas/v4/web_search \
  -H "Authorization: Bearer $ZAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "search term",
    "search_engine": "search_pro",
    "search_intent": false,
    "count": 10
  }' | jq .
```

## Response Format (JSON)

```json
{
  "id": "search-task-id",
  "created": 1740000000,
  "request_id": "req-xxx",
  "search_intent": [
    {
      "query": "original query",
      "intent": "SEARCH_ALL",
      "keywords": "rewritten keywords"
    }
  ],
  "search_result": [
    {
      "title": "Page Title",
      "content": "Summary snippet...",
      "link": "https://example.com/page",
      "media": "Example Site",
      "icon": "https://example.com/favicon.ico",
      "refer": "1",
      "publish_date": "2026-01-15"
    }
  ]
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 1701 | Concurrent search limit reached, retry later |
| 1702 | No search engine available |
| 1703 | Search engine returned no valid data |

## Notes

- Search query should not exceed 70 characters
- `count` for `search_pro_sogou` only supports 10, 20, 30, 40, 50
- `search_domain_filter` only works with search_std, search_pro, search_pro_sogou
- The API is optimized for Chinese-language search but works for English too
- Rate limits apply; don't burst too many requests

## Script Location

The CLI script lives at: `scripts/zai-search.js` (relative to this skill directory).
