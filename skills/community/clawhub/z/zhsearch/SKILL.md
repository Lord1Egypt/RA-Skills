---
name: zhsearch
description: "Chinese search enhancement: search Baidu, Zhihu, and WeChat articles. Returns AI-optimized structured results in Chinese. Paid skill (0.001 USDT/call via SkillPay)."
version: 1.0.0
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["node"]}}}
---

# Chinese Search Enhancement (中文搜索增强)

Search Chinese-language content across **Baidu**, **Zhihu**, and **WeChat public accounts** in a single command. Returns structured, AI-friendly JSON results.

This skill fills the gap left by English-centric search tools (Brave, Perplexity, etc.) that return poor results for Chinese queries.

## Usage

### Search all sources (default)

```bash
node {baseDir}/search.mjs "人工智能最新进展"
```

### Search specific sources

```bash
node {baseDir}/search.mjs "新能源汽车" -s baidu
node {baseDir}/search.mjs "React性能优化" -s zhihu
node {baseDir}/search.mjs "大模型应用" -s wechat
node {baseDir}/search.mjs "量子计算" -s baidu,zhihu
```

### Control result count

```bash
node {baseDir}/search.mjs "ChatGPT" -n 10
node {baseDir}/search.mjs "深度学习" -s baidu,zhihu -n 3
```

## Options

- First argument (required): search query in Chinese or English
- `-s, --sources <sources>`: Comma-separated sources — `baidu`, `zhihu`, `wechat` (default: all three)
- `-n, --limit <count>`: Results per source, 1-20 (default: 5)
- `--no-billing`: Skip billing check (local testing only, do not use in production)

## Sources

| Source | What it searches | Best for |
|--------|-----------------|----------|
| `baidu` | Baidu web search | General Chinese web content, news, tech articles |
| `zhihu` | Zhihu Q&A platform | Expert opinions, in-depth discussions, how-to guides |
| `wechat` | WeChat public account articles via Sogou | Original analysis, industry insights, opinion pieces |

## Output Format

Returns JSON with results grouped by source:

```json
{
  "query": "人工智能",
  "total": 15,
  "sources": ["baidu", "zhihu", "wechat"],
  "results": {
    "baidu": [
      { "title": "...", "snippet": "...", "url": "..." }
    ],
    "zhihu": [
      { "title": "...", "snippet": "...", "url": "..." }
    ],
    "wechat": [
      { "title": "...", "snippet": "...", "url": "...", "account": "...", "date": "..." }
    ]
  }
}
```

## When to use this skill

- User asks a question that requires Chinese-language information
- You need to find Chinese news, articles, or expert discussions
- The built-in `web_search` tool returns poor results for Chinese queries
- You need information from Chinese platforms (Baidu, Zhihu, WeChat)

## Billing

This is a paid skill. Each search call costs **0.001 USDT** (about 0.007 RMB). If the user's balance is insufficient, the skill returns a `payment_url` — show it to the user so they can top up.

## Setup

No configuration needed. Billing is handled automatically by the skill publisher via SkillPay. Just install and use.

## Security & Privacy

- **External endpoints accessed**: Baidu (baidu.com), Sogou (sogou.com, weixin.sogou.com), Zhihu (zhihu.com), SkillPay (skillpay.me)
- **Local files**: None read or written
- **Data handling**: Search queries are sent to the above search engines. No user data is stored. Billing is processed via SkillPay with anonymous caller IDs.
