# Recent News Article Aggregator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `recent-news-article-aggregator`

x402 availability: not enabled for this product.

## `search`

Action slug: `search`

Price: `10` credits

Search for recent news articles by concise topic, category, country, and language. Use short search phrases rather than long natural-language requests; broad or related-news requests work best with 1-4 core concepts and optional categories.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `categories` | `array` | no | Canonical AgentPMT categories to include. Use these broad categories for topical scoping; do not use provider-specific category names. Omit categories, or use 'general', for broad general news. |
| `country` | `string` | no | Two-letter country code to filter news by region. Default: us. |
| `exclude_categories` | `array` | no | Canonical AgentPMT categories to exclude. Use only the listed categories; do not use provider-specific category names. |
| `language` | `string` | no | Language code for article language. Default: en. |
| `max_age_in_days` | `integer` | no | Limit results to articles published within the past N days. Use a wider window if the first query is too specific or has sparse results. |
| `news_type` | `string` | no | Result scope: 'all_news' for broader matching across the news database or 'top_stories' for major headlines only. Default: all_news. |
| `topic` | `string` | no | Concise news search phrase. Use 1-4 core keywords or a short phrase; longer natural-language text makes the search more specific and can reduce results. For related news, extract the main concepts and search broad terms first (for example, use 'flower delivery privacy' instead of 'sending flowers surprise gift no address privacy'). Supports + (AND), \| (OR), - (NOT), quotes for exact phrases, and * for prefix matching. |

Sample parameters:

```json
{
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
```

Generated JSON parameter schema:

```json
{
  "categories": {
    "description": "Canonical AgentPMT categories to include. Use these broad categories for topical scoping; do not use provider-specific category names. Omit categories, or use 'general', for broad general news.",
    "items": {
      "enum": [
        "general",
        "science",
        "sports",
        "business",
        "health",
        "entertainment",
        "tech",
        "politics",
        "food",
        "travel"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "country": {
    "default": "us",
    "description": "Two-letter country code to filter news by region. Default: us.",
    "required": false,
    "type": "string"
  },
  "exclude_categories": {
    "description": "Canonical AgentPMT categories to exclude. Use only the listed categories; do not use provider-specific category names.",
    "items": {
      "enum": [
        "general",
        "science",
        "sports",
        "business",
        "health",
        "entertainment",
        "tech",
        "politics",
        "food",
        "travel"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "language": {
    "default": "en",
    "description": "Language code for article language. Default: en.",
    "required": false,
    "type": "string"
  },
  "max_age_in_days": {
    "description": "Limit results to articles published within the past N days. Use a wider window if the first query is too specific or has sparse results.",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "news_type": {
    "default": "all_news",
    "description": "Result scope: 'all_news' for broader matching across the news database or 'top_stories' for major headlines only. Default: all_news.",
    "enum": [
      "top_stories",
      "all_news"
    ],
    "required": false,
    "type": "string"
  },
  "topic": {
    "description": "Concise news search phrase. Use 1-4 core keywords or a short phrase; longer natural-language text makes the search more specific and can reduce results. For related news, extract the main concepts and search broad terms first (for example, use 'flower delivery privacy' instead of 'sending flowers surprise gift no address privacy'). Supports + (AND), | (OR), - (NOT), quotes for exact phrases, and * for prefix matching.",
    "required": false,
    "type": "string"
  }
}
```
