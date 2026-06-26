# Tavily API Reference & Technical Specifications

This reference document outlines parameters, constraints, response fields, and cost structures for all core Tavily API endpoints.

---

## 1. Search API (`POST https://api.tavily.com/search`)

| Parameter | Type | Required | Default | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- |
| `query` | String | Yes | - | The search string. Best as a natural language question. |
| `search_depth` | String | No | `basic` | `basic`, `advanced`, `fast`, `ultra-fast` |
| `topic` | String | No | `general` | `general`, `news`, `finance` |
| `time_range` | String | No | `null` | `day`, `week`, `month`, `year` |
| `max_results` | Integer | No | `5` | `1` to `20` |
| `include_domains`| Array | No | `[]` | List of domain names to prioritize (max 300) |
| `exclude_domains`| Array | No | `[]` | List of domain names to block (max 150) |
| `include_answer` | Boolean | No | `false` | Synthesizes a concise answer to the query |
| `include_raw_content` | Boolean | No | `false` | Includes fully cleaned markdown text of pages |
| `exact_match` | Boolean | No | `false` | Forces verbatim matching of double-quoted phrases |
| `include_usage` | Boolean | No | `false` | Includes credit consumption metadata |

---

## 2. Extract API (`POST https://api.tavily.com/extract`)

Extracts raw content from specific URLs without executing a search.

| Parameter | Type | Required | Default | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- |
| `urls` | Array | Yes | - | List of target URLs (max 20) |
| `extract_depth` | String | No | `basic` | `basic` (fast, raw text), `advanced` (handles JS rendering) |
| `query` | String | No | `null` | Activates Intent-Based Extraction when provided |
| `chunks_per_source`| Integer | No | `3` | Chunks returned per URL if query is provided (`1` to `5`) |
| `include_images` | Boolean | No | `false` | Extracts and returns image URLs found in pages |

---

## 3. Crawl API (`POST https://api.tavily.com/crawl`)

Traverses a website's link graph and extracts content.

| Parameter | Type | Required | Default | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- |
| `url` | String | Yes | - | Starting (root) URL |
| `max_depth` | Integer | No | `1` | `1` to `5` |
| `max_breadth` | Integer | No | `20` | `1` to `100` |
| `limit` | Integer | No | `50` | Hard cap on total pages crawled |
| `instructions` | String | No | `null` | Natural-language semantic guidance for filtering pages |
| `select_paths` | Array | No | `[]` | Regex patterns of paths to include |
| `exclude_paths` | Array | No | `[]` | Regex patterns of paths to exclude |

---

## 4. Map API (`POST https://api.tavily.com/map`)

Quickly maps the URL topology of a target domain without extracting page content.

| Parameter | Type | Required | Default | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- |
| `url` | String | Yes | - | Target domain URL |
| `max_depth` | Integer | No | `1` | `1` to `5` |
| `max_breadth` | Integer | No | `20` | `1` to `100` |
| `limit` | Integer | No | `50` | Hard cap on total URLs returned |
| `instructions` | String | No | `null` | Natural-language guidance to filter discovered URLs |

---

## 5. Research API (`POST https://api.tavily.com/research`)

Asynchronous deep research execution.

| Parameter | Type | Required | Default | Allowed Values / Ranges |
| :--- | :--- | :--- | :--- | :--- |
| `input` | String | Yes | - | Core research question or objective |
| `model` | String | No | `auto` | `mini` (fast), `pro` (multi-agent), `auto` |
| `output_schema` | Object | No | `null` | JSON Schema for structured data extraction |
| `output_length` | String | No | `standard`| `short`, `standard`, `long` |
| `stream` | Boolean | No | `false` | Stream agent progress via Server-Sent Events (SSE) |
