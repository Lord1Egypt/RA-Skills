---
name: recent-news-article-aggregator
description: "Recent News Article Aggregator: Search global news database with 1M+ weekly articles. Filter by locale, language, category, date. Boolean search supported. Use when an agent needs recent news article aggregator, access recent news for up to date content generation. augment decision making processes in stock, crypto, forex, etc. aggregate, search, topic, news type through AgentPMT-hosted remote tool calls. Discovery terms: recent news article aggregator."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/recent-news-article-aggregator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/recent-news-article-aggregator"}}
---
# Recent News Article Aggregator

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Access current events and knowledge through this large global news database, adding over 1 million articles weekly from thousands of sources.

Filter news by locale (country codes) and a wide range of languages (e.g., English, Spanish, Chinese, Korean, etc.).
Boolean Search: Perform advanced text searches within article titles and bodies using boolean operators: AND (+), OR (|), and NOT (-).
Categorization: Filter by article categories (e.g., business, tech) and exclude specific ones.
Time: Request articles published on or after a specified date.

Article Data
The tool response include rich article objects, including:
Title, description, and a 60-character snippet.
The full URL to the article and an image URL.
The language, source domain, and publication date.

## Product Instructions
### Recent News Article Aggregator

Search and retrieve recent news articles from multiple sources. Use this tool for current-events lookup, topical monitoring, daily briefings, and source discovery across global news coverage.

The tool exposes an AgentPMT-level interface. Use the canonical AgentPMT categories listed below; do not try to use provider-specific category names or adapt parameters for individual upstream news providers.

#### Actions

##### search

Search for news articles by topic, category, country, and language.

**Required Fields:** None. A bare search returns general US English news.

**Optional Fields:**

| Field | Type | Description |
|---|---|---|
| `topic` | string | Concise news search phrase. Use 1-4 core keywords or a short phrase. Longer natural-language text makes the search more specific and can reduce results. Supports `+` (AND), `|` (OR), `-` (NOT), quotes for exact phrases, and `*` for prefix matching. |
| `news_type` | string | `"all_news"` (default) for broad results or `"top_stories"` for major headlines only. |
| `categories` | array of strings | Include only these canonical AgentPMT categories: `general`, `science`, `sports`, `business`, `health`, `entertainment`, `tech`, `politics`, `food`, `travel`. Omit categories, or use `general`, for broad general news. |
| `exclude_categories` | array of strings | Exclude canonical AgentPMT categories. Same options as `categories`. |
| `max_age_in_days` | integer | Limit results to articles published within the past N days (minimum 1). Use a wider window if the first query is too specific or sparse. |
| `country` | string | Two-letter country code (default: `"us"`). |
| `language` | string | Language code (default: `"en"`). |

#### Search Query Guidance

Use short search phrases, not full task descriptions. More words usually make the search narrower, not broader.

When the user gives a long or specific request, extract the core news concepts before calling the tool:

- User request: `sending flowers surprise gift no address privacy`
  - Good first `topic`: `flower delivery privacy`
  - Good related follow-ups if results are sparse: `gift delivery privacy`, `anonymous delivery`, `flower delivery`
  - Avoid sending the full phrase as-is unless the user explicitly wants an exact niche match.
- User request: `what is happening with AI regulation in Europe this week`
  - Good `topic`: `AI regulation Europe`
- User request: `latest market reaction to interest rate cuts and inflation`
  - Good `topic`: `interest rates inflation market`

For related-news discovery:

1. Start broad with 1-4 core concepts.
2. Use `all_news` unless the user specifically asks for major headlines.
3. Add `categories` only when they help scope the result set.
4. If results are sparse, make a second call with fewer terms, a broader phrase, or a wider `max_age_in_days`.
5. Do not conclude that no relevant news exists after only one overly-specific query.

Use operators deliberately:

- Use quotes for exact phrases: `"flower delivery"`
- Use `|` for alternatives: `"flower delivery" | florist | gifting`
- Use `+` only when terms must co-occur: `privacy + delivery`
- Use `-` to exclude a distracting term: `apple -iphone`

#### Examples

**Search by concise topic:**
```json
{
  "action": "search",
  "topic": "artificial intelligence regulation",
  "max_age_in_days": 7
}
```

**Search related news from a long user request:**
```json
{
  "action": "search",
  "topic": "flower delivery privacy",
  "news_type": "all_news",
  "categories": ["business", "tech"],
  "max_age_in_days": 30
}
```

**Top stories in broad categories:**
```json
{
  "action": "search",
  "news_type": "top_stories",
  "categories": ["business", "tech"]
}
```

**Exclude categories and target a country:**
```json
{
  "action": "search",
  "topic": "climate change",
  "exclude_categories": ["sports", "entertainment"],
  "country": "gb",
  "language": "en"
}
```

**Use OR for related terms:**
```json
{
  "action": "search",
  "topic": "\"flower delivery\" | florist | gifting",
  "max_age_in_days": 30
}
```

#### Common Workflows

1. **Daily news briefing** — Use `news_type: "top_stories"` with no topic to get current headlines.
2. **Topic monitoring** — Provide a concise `topic` with `max_age_in_days` to track a subject over a rolling window.
3. **Related-news discovery** — Convert long user text into broader concepts, then run one or more concise searches.
4. **Category-filtered research** — Combine `categories` with a topic to narrow results, such as `health` + `pandemic`.
5. **International coverage** — Set `country` and `language` to retrieve region-specific articles.
6. **Exclusion filtering** — Use `exclude_categories` to remove irrelevant results, such as excluding sports and entertainment for a business report.

#### Response Format

Each article in the response includes:

- `title` — Article headline
- `description` — Summary or snippet
- `url` — Link to the full article
- `image_url` — Associated image, if available
- `source` — Publishing source name
- `published_at` — Publication timestamp
- `categories` — Article categories
- `language` — Article language

The response may also include provider or filter warnings. If warnings are present, explain that results may be partial or broadened, but do not retry with provider-specific parameter values.

#### Important Notes

- Use only the canonical AgentPMT category values shown in the schema.
- Do not use provider-specific category values such as `technology`, `tourism`, `top`, `world`, or `other` unless they are added to the AgentPMT schema in the future.
- When no `topic` is provided, results are based on category and region filters only.
- Crypto-related topics (bitcoin, ethereum, blockchain, etc.) and financial/market topics (stocks, forex, inflation, etc.) may be routed to specialized news endpoints for better coverage.
- The `max_age_in_days` field must be at least 1.
- Default behavior returns US English news across all categories.

## When To Use
- Use this skill for `Recent News Article Aggregator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: recent news article aggregator, access recent news for up to date content generation. augment decision making processes in stock, crypto, forex, etc. aggregate, search, topic, news type.
- Supported action names: `search`.

## Use Cases
- Access recent news for up to date content generation. Augment decision making processes in stock
- crypto
- forex
- etc. Aggregate
- filter
- and summarize most relevant news

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `search` (action slug: `search`): Search for recent news articles by concise topic, category, country, and language. Use short search phrases rather than long natural-language requests; broad or related-news requests work best with 1-4 core concepts and optional categories. Price: `10` credits. Parameters: `categories`, `country`, `exclude_categories`, `language`, `max_age_in_days`, `news_type`, `topic`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "recent-news-article-aggregator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "recent-news-article-aggregator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "recent-news-article-aggregator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "recent-news-article-aggregator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "recent-news-article-aggregator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "recent-news-article-aggregator"
  }
}
```

## Call This Tool
Product slug: `recent-news-article-aggregator`

Marketplace page: https://www.agentpmt.com/marketplace/recent-news-article-aggregator

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Recent-News-Article-Aggregator",
    "arguments": {
      "action": "search",
      "categories": [
        "general"
      ],
      "country": "us",
      "exclude_categories": [
        "general"
      ],
      "language": "en",
      "max_age_in_days": 1,
      "news_type": "all_news",
      "topic": "example topic"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "recent-news-article-aggregator",
  "parameters": {
    "action": "search",
    "categories": [
      "general"
    ],
    "country": "us",
    "exclude_categories": [
      "general"
    ],
    "language": "en",
    "max_age_in_days": 1,
    "news_type": "all_news",
    "topic": "example topic"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `search` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/recent-news-article-aggregator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
