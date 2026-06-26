---
name: signal-track
description: "Track persistent topics (stocks, companies, AI, and policy events) and monitor them continuously. Use this for recurring updates, trend monitoring, and structured summaries. Use this when users want recent news about a specific event, person, company, or topic. (追踪)"
metadata:
  tags: [information-tracking, topic-tracking, news-intelligence, continuous-monitoring, one-off-news-search]
  version: 0.1.0
  required_config_paths:
    - path: ~/.openclaw/openclaw.json
      note: Primary config file. If present, signal-track reads/writes `skills.entries.signal-track.apiKey`.
    - path: ~/.signal-track/config.json
      note: Legacy config fallback path used for backwards compatibility.

---

## What it does

signal-track is an AI-native information tracking system and a CLI tool for continuous, topic-based intelligence monitoring. signal-track is not a traditional news reader and not a general recommendation feed. The system is built around long-running topics: users define persistent tracking tasks, and the platform continuously monitors information sources, detects meaningful updates, filters noise, and surfaces high-value signals. In other words, it converts one-time information queries into persistent tracking tasks.

* Track ongoing topics (e.g. "OpenAI releases", "NVIDIA earnings", "China policy changes")
* Aggregate updates from multiple information sources
* Deduplicate and structure incoming information
* Provide summarized updates and timelines
* Support deep-dive analysis on specific events

## When to use

Use signal-track when:

* You need continuous monitoring of a topic over time
* You want to avoid missing important updates
* You are tracking fast-moving domains (AI, finance, policy, etc.)
* You need structured, decision-relevant information instead of raw news

Do NOT use signal-track for:

* General browsing or entertainment content
* Pure one-off trivia or random browsing (unless the user explicitly asks for one-off news/article search or browsing)

## Core concepts

* **Topic**: A long-running information tracking task that can be expressed through a natural language description, structured keywords, and entity references.
* **NewsCard**: The atomic information unit delivered to users(or agents).
  * Typical contents: `title`, `overview`, `ELI5`, `sources`, `timestamp`, and `topic mapping`.
* **Source**: Any information producer the system monitors.
  * Examples: `news websites`, `blogs`, `social media`, `research publications`, `official announcements`, and `company releases`.
* **Feed**: A stream of news cards associated with a topic or a user's followed topics, ordered recency.

## Key capabilities

* Create and manage topics
* Subscribe/unsubscribe to topics
* Retrieve topic details by id
* Search within tracked signals
* Fetch full article content
* Trigger deep analysis on selected items

## Example use cases

* Track a company (e.g. Tesla, Apple) for investment decisions
* Monitor AI model releases and benchmark progress
* Follow policy or regulatory changes in a region
* Track competitors or specific products
* Provide simplified explanations of complex information (easy-to-understand summaries)

## CLI surface covered

All existing `signal-track` CLI commands are supported through the helper script:

- Command runner: `signal-track <args>`

### Auth

- `signal-track login --api-key <api_key>` validates the key using the backend endpoint and stores user context locally.

### Topic commands

- `signal-track topic show --topic-id <topic_id> [--cursor <cursor>] [--page-size <page_size>]`

### Topics commands

- `signal-track topics my`
- `signal-track topics list`
- `signal-track topics follow --topic-id <topic_id>`
- `signal-track topics unfollow --topic-id <topic_id>`
- `signal-track topics search --scope my --query <keyword> [--page-size <page_size>] [--page-number <page_number>]`
- `signal-track topics search --scope square --query <keyword> [--page-size <page_size>] [--page-number <page_number>]`

### News cards

- `signal-track news_cards feed my [--cursor <cursor>] [--page-size <page_size>]`
- `signal-track news_cards feed --topic-id <topic_id> [--cursor <cursor>] [--page-size <page_size>]`
- `signal-track news_cards get --news-id <news_id>`
- `signal-track news_cards get <news_id>` *(positional alias)*
- `signal-track news_cards search --query <keyword>`

### Articles

- `signal-track articles content --article-id <article_id>`


## Execution notes

- Always keep commands in English.
- Default environment:
  - Requires Node.js 22+.
- API base URL defaults to `https://younews.k.sohu.com/`.
- Required local config state:
  - Reads auth from `~/.openclaw/openclaw.json` (preferred). If absent, falls back to legacy `~/.signal-track/config.json`.
  - Writes login state to the detected existing config path (`openclaw` if present, otherwise legacy config path).
 - If `--json` is missing, output is human-readable JSON-style pretty print except for special card-get behavior where the first card is printed.

## Installation and deployment

- Prerequisite: Node.js 22+ (`node -v`).
- Install from local source:
  - `npm install`
- `npm install -g .`
  - `signal-track --help`
  - `signal-track <command>`

## Error handling

- If not logged in, commands return a clear message prompting `signal-track login --api-key <api_key>`.
- Missing required flags (for example, `--topic-id`, `--news-id`, `--article-id`, `--query`, or `--scope`) are reported and command help is printed.
- Invalid pagination values (negative/zero/non-integer) return validation errors before any network call.

## Platform notes

signal-track is powered by YouNews as its underlying engine and can be considered the CLI version of YouNews; it is available exclusively to YouNews members — see younews.cn for more information.
