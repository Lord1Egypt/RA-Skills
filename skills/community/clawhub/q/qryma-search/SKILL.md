---
name: qryma-search
description: "Qryma AI Search retrieves Web information and returns LLM-friendly data. Get started for free, just sign up."
homepage: https://qryma.com
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python"],"env":["QRYMA_API_KEY"]},"primaryEnv":"QRYMA_API_KEY"}}
---

# Qryma Search

Qryma AI Web Search SKILL, The World's Fastest and Cheapest Search API for LLM and AI Agents.

Search the web using the Qryma API - fast, reliable, and built for developers.

Start free now. Get your free key now [qryma.com](https://qryma.com).


## Setup

### Authenticate

Get your free QRYMA_API_KEY from [qryma.com](https://qryma.com). Chat with your AI assistant and ask it to help you complete the configuration.

```text
Please configure qryma search with the QRYMA_API_KEY set to ak-your-api-key-here.
```

从 qryma.com 获取免费的 QRYMA_API_KEY，直接发送给你的 AI 助手，让他帮你自动配置。

```text
请帮我配置好 qryma search，设置 QRYMA_API_KEY 为 ak-your-api-key-here
```

### Manual Configuration

First, configure your API key. Choose one of these methods:


### Option 1 - Environment Variable

**Linux/macOS:**
```bash
export QRYMA_API_KEY="your-key-here"
```

**Windows (PowerShell):**
```powershell
$env:QRYMA_API_KEY="your-key-here"
```


### Option 2 - Config File

Create `~/.qryma/.env` with:
```
QRYMA_API_KEY=your-key-here
```


## Quick Start

```bash
# Default: human-readable Markdown
python scripts/qryma_search.py --query "how to learn Python" --format md

# With specific language
python scripts/qryma_search.py --query "Python编程学习" --lang "zh-CN" --format md

# Safe search enabled
python scripts/qryma_search.py --query "adult content" --safe --format md

# Fulltext search mode
python scripts/qryma_search.py --query "AI research" --mode fulltext --format raw

# Snippet search mode
python scripts/qryma_search.py --query "AI research" --mode snippet --format raw

# Brave-compatible JSON
python scripts/qryma_search.py --query "latest AI news" --format brave

# Raw API response
python scripts/qryma_search.py --query "top tech trends" --format raw
```


## Options

- **`--api-key`** (string): Qryma API key

- **`--query`** (string, required): Search query text

- **`--max-results`** (number, default: 5): Results to return (1-10)

- **`--lang`** (string): Language code - [See available languages](https://developers.google.com/custom-search/docs/xml_results_appendices#interfaceLanguages) (auto-detect if not specified)


- **`--safe`** (flag, default: false): Enable safe search

- **`--mode`** (string, default: fulltext): Search mode - fulltext for detailed results, snippet for basic results

- **`--format`** (raw/brave/md, default: md): Output format


## Output Formats

### `md` (default)

Clean, readable Markdown list:

```
1. Page Title Here
   https://example.com/page
   - Brief snippet from the page...
```


### `brave`

Brave Search compatible JSON for easy integration:

```json
{
  "query": "search term",
  "results": [{"title": "...", "url": "...", "snippet": "..."}]
}
```


### `raw`

Full API response with all available fields.


## Best Practices

- Use `--max-results 3-5` for most queries

- Prefer `--format md` for human consumption

- Use `--format brave` when integrating with other tools

- Use `--safe` for family-friendly content

- Use `--lang` to search in specific languages


## Advanced Configuration

- Custom endpoint: Set `QRYMA_ENDPOINT` env var or config line

- Default endpoint: `https://search.qryma.com/api/web`
