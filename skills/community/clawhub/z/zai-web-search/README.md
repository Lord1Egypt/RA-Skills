# Z.AI Web Search API

Use Zhipu AI's (Z.AI) web search API for intelligent searching, supporting multiple search engines and advanced filtering.

## Features Overview

This skill provides AI-powered web search with support for multiple Chinese search engines, optimized for Chinese content processing and LLM parsing.

### Supported Search Engines

| Engine | Provider | Description |
|--------|----------|-------------|
| `search_std` | Zhipu AI | Basic edition, fast response |
| `search_pro` | Zhipu AI | Pro edition, best quality |
| `search_pro_sogou` | Sogou | Sogou search results |
| `search_pro_quark` | Quark | Quark search results |

### Pricing Information

Official pricing page: [https://open.bigmodel.cn/pricing](https://open.bigmodel.cn/pricing)

- Web Search API uses token-based billing
- Different engines have different billing rates
- Visit the official page for the latest rates

### Comparison with Other Search Tools

| Feature | This Skill (Z.AI) | Brave Search |
|---------|-------------------|--------------|
| Chinese Support | Excellent | Limited |
| Intent Recognition | Supported | Not Supported |
| Multiple Engines | 4 engines | Single engine |
| Time Filtering | Supported | Supported |
| Domain Filtering | Supported | Not Supported |

## First-Time Setup Guide

When you use this skill in OpenClaw for the first time, the system will guide you through the configuration process.

### Configuration Steps

1. **Get API Key**: Visit [https://open.bigmodel.cn](https://open.bigmodel.cn) to register and obtain an API Key

2. **Choose Configuration Method**:
   - Create `config.json` in the skill folder (recommended)
   - Set `ZAI_API_KEY` environment variable
   - Use user config `~/.config/zai-web-search/config.json`

3. **Replace Other Search Skills** (Optional)

   This skill can replace other search-related skills:
   - **Brave Search** (OpenClaw built-in): Replace for better Chinese search experience
   - Other web search skills: Compare features before deciding whether to replace

   When asked, please indicate if you want to set this skill as your primary search tool.

### Default Behavior

After configuration, this skill will:
- Use `search_std` engine by default
- Return 10 results
- Apply no time filtering
- Use medium-length summaries

You can override these defaults with command-line arguments or the config file.

## Key Features

- Multiple search engines: Zhipu basic/pro, Sogou search, Quark search
- Intelligent intent recognition: Automatically understand query intent to optimize results
- Time filtering: Filter content by day, week, month, or year
- Multiple output formats: Markdown, JSON, compact mode

## Quick Start

### Step 1: Get API Key

1. Visit [Zhipu AI Open Platform](https://open.bigmodel.cn)
2. Register/Login to your account
3. Create an API Key in the console
4. Copy your API Key (format similar to: `xxxx.xxxxx.xxxxx`)

### Step 2: Create Configuration File

Create a `config.json` file in the skill folder:

```bash
# Enter skill folder
cd ~/.openclaw/skills/zai-web-search

# Copy example config file
cp config.json.example config.json

# Edit config file (with your preferred editor)
# For example: vim config.json, nano config.json, or open with VS Code
```

**Important Notes**:
- `config.json.example` is an **example file** with comments to help you understand
- Your `config.json` is the actual config file and must be in standard JSON format
- **Remove all comments** after copying, otherwise parsing will fail

### Step 3: Fill in Configuration

Open `config.json` and enter your API Key (after removing all comments):

```json
{
  "apiKey": "paste your API Key here",
  "engine": "search_std",
  "intent": false,
  "count": 10,
  "recency": "noLimit",
  "content": "medium",
  "domain": ""
}
```

> **Parameter Explanation**: See [config.json.example](config.json.example) for details on each parameter and its options

**Save the file and you're done!** 🎉

## Configuration Parameters

### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `apiKey` | Your Zhipu AI API Key |

### Optional Parameters

| Parameter | Description | Options |
|-----------|-------------|---------|
| `engine` | Search engine | `search_std`(basic), `search_pro`(pro), `search_pro_sogou`(Sogou), `search_pro_quark`(Quark) |
| `intent` | Enable intelligent intent recognition | `true`/`false` |
| `count` | Number of results to return | 1-50 |
| `recency` | Time filtering | `oneDay`, `oneWeek`, `oneMonth`, `oneYear`, `noLimit` |
| `content` | Content length | `medium`(medium), `high`(detailed) |
| `domain` | Domain filtering | Domain name, e.g., `"docs.openclaw.ai"` |

## Usage

### Basic Search

```bash
# Search with default config
zai-search "Harbin Ice and Snow World 2026"

# Switch to pro search engine
zai-search "AI latest developments" --engine search_pro

# Get more results
zai-search "React tutorial" --count 20
```

### Fuzzy Queries (Recommended with Intent Recognition)

When you're unsure what to search for, enabling intent recognition yields better results:

```bash
# Question-style queries
zai-search "what to eat today" --intent

zai-search "recent good movies" --intent
```

### Filter by Time

```bash
# News from the past week
zai-search "tech news" --recency oneWeek

# Today's hot topics
zai-search "trending today" --recency oneDay

# Research progress in the past year
zai-search "quantum computing progress" --recency oneYear
```

### Limit Search Domain

```bash
# Search only a specific website
zai-search "OpenClaw documentation" --domain docs.openclaw.ai

# Search React official docs
zai-search "React Hooks" --domain react.dev
```

### Get Detailed Content

```bash
# Use high mode for more complete content summaries
zai-search "React 19 new features" --content high
```

### Output Formats

```bash
# JSON format (for script processing)
zai-search "query" --json

# Compact mode (only title and link)
zai-search "query" --compact

# Default Markdown format (readable)
zai-search "query"
```

## Configuration Priority

When multiple configuration sources exist, priority from highest to lowest:

1. **Command-line arguments** (highest priority)
   ```bash
   zai-search "query" --engine search_pro  # Overrides config file
   ```

2. **Environment variables** (only affects apiKey)
   ```bash
   export ZAI_API_KEY="your API Key"
   ```

3. **User config file**
   ```bash
   ~/.config/zai-web-search/config.json
   ```

4. **Skill folder config file** (lowest priority)
   ```bash
   config.json (inside skill folder)
   ```

## Example Scenarios

### Scenario 1: Daily Chinese Content Search

```json
{
  "apiKey": "your API Key",
  "engine": "search_std",
  "intent": true,
  "count": 10
}
```

### Scenario 2: Latest Tech News

```json
{
  "apiKey": "your API Key",
  "engine": "search_pro",
  "recency": "oneWeek",
  "content": "high"
}
```

### Scenario 3: Search Specific Website Only

```json
{
  "apiKey": "your API Key",
  "engine": "search_std",
  "domain": "docs.python.org"
}
```

## FAQ

### Q: Where should I put the config file?

A: Recommended location: `~/.openclaw/skills/zai-web-search/config.json`

### Q: Why does it error after copying the example file?

A: `config.json.example` contains comments, and JSON standard doesn't support comments. Please remove all `//` comments before saving.

### Q: Where do I get the API Key?

A: Visit https://open.bigmodel.cn, register, and create an API Key in the console.

### Q: What if search returns no results?

A: Check the following:
1. Is the API Key correctly entered
2. Is the config file standard JSON (no comments)
3. Is the query too long (recommended under 70 characters)
4. Have you hit rate limits (try again after a while)

### Q: Which search engine is best?

A:
- `search_std`: Fast speed, suitable for daily searching
- `search_pro`: Highest quality, suitable for professional searching
- `search_pro_sogou`: Uses Sogou search results
- `search_pro_quark`: Uses Quark search results

## File Structure

```
zai-web-search/
├── README.md              # This file
├── README-CN.md           # Chinese documentation
├── SKILL.md               # Usage documentation
├── config.json            # Your config file (create it)
├── config.json.example    # Config example
├── scripts/
│   └── zai-search.js      # CLI script
└── .gitignore             # Ignore sensitive files
```

## Technical Support

For questions, please refer to:
- [Zhipu AI Official Documentation](https://open.bigmodel.cn)
- [API Documentation](https://open.bigmodel.cn/dev/api#web_search)
