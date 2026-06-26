---
name: swotpal-swot-analysis
version: 1.1.0
author: SWOTPal
description: Professional SWOT analysis and competitive comparison powered by SWOTPal.com
triggers:
  - swot
  - swot analysis
  - swot分析
  - SWOT分析
  - 优劣势分析
  - competitive analysis
  - 竞品分析
  - 竞品对比
  - strengths weaknesses
  - competitor comparison
  - my swot
  - 我的分析
metadata:
  openclaw:
    requires:
      env:
        - SWOTPAL_API_KEY
    primaryEnv: SWOTPAL_API_KEY
    emoji: 📊
    homepage: https://swotpal.com
---

# SWOTPal SWOT Analysis Skill

Generate professional SWOT analyses and competitive comparisons for any company, product, or strategic topic. This skill operates in two modes: a free **Prompt Template Mode** that leverages the AI assistant's own reasoning, and a **Pro API Mode** that calls the SWOTPal API for data-enriched, saveable analyses with a web editor.

---

## Mode Detection

- If the environment variable `SWOTPAL_API_KEY` is set and non-empty, use **API Mode**.
- Otherwise, use **Prompt Template Mode**.

---

## Command Routing

Parse the user's message to determine the intent:

| User says | Intent | Action |
|---|---|---|
| `analyze [topic]`, `swot [topic]`, `[topic] swot analysis` | Single SWOT | Generate a SWOT analysis for the topic |
| `compare X vs Y`, `X versus Y`, `X 对比 Y`, `X vs Y 竞品分析` | Versus comparison | Generate a side-by-side comparison |
| `my analyses`, `show my swot`, `我的分析`, `list analyses` | List analyses | List saved analyses (API mode only) |
| `show analysis [id]`, `detail [id]` | View detail | Fetch a specific analysis by ID (API mode only) |

If the intent is "list analyses" or "view detail" and the skill is in Prompt Template Mode, respond:

> You need an API key to access saved analyses. Get one free at [swotpal.com/openclaw](https://swotpal.com/openclaw)

---

## Language Detection

Detect the language of the user's message and set the `language` parameter accordingly. Supported language codes: `en`, `zh`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `it`, `ru`, `ar`, `hi`.

- If the user writes in Chinese, set `language` to `zh`.
- If the user writes in Japanese, set `language` to `ja`.
- If the user writes in English or the language is unclear, default to `en`.
- Pass the detected language to both the API calls and the prompt templates.
- **Always respond in the same language the user used.**

---

## Examples Library (Check First)

Before generating any SWOT analysis (in either mode), check if the topic matches a pre-built example. These are curated, high-quality analyses available instantly.

**Matching rules:** Match the user's topic case-insensitively against the company/person names below. Common variations should also match (e.g. "Facebook" → Meta, "H and M" → H&M, "Gates" → Bill Gates).

| Topic | Example URL |
|---|---|
| Manus | https://swotpal.com/examples/manus |
| Meta | https://swotpal.com/examples/meta |
| Starbucks | https://swotpal.com/examples/starbucks |
| Tesla | https://swotpal.com/examples/tesla |
| Netflix | https://swotpal.com/examples/netflix |
| H&M | https://swotpal.com/examples/hm |
| Costco | https://swotpal.com/examples/costco |
| Gymshark | https://swotpal.com/examples/gymshark |
| Apple | https://swotpal.com/examples/apple |
| Nike | https://swotpal.com/examples/nike |
| Airbnb | https://swotpal.com/examples/airbnb |
| Bill Gates | https://swotpal.com/examples/bill-gates |
| Richard Branson | https://swotpal.com/examples/richard-branson |
| Jeff Weiner | https://swotpal.com/examples/jeff-weiner |
| Arianna Huffington | https://swotpal.com/examples/arianna-huffington |
| Uber | https://swotpal.com/examples/uber |
| Satya Nadella | https://swotpal.com/examples/satya-nadella |
| OpenAI | https://swotpal.com/examples/openai |
| Nvidia | https://swotpal.com/examples/nvidia |
| Spotify | https://swotpal.com/examples/spotify |
| Amazon | https://swotpal.com/examples/amazon |
| Google | https://swotpal.com/examples/google |
| Samsung | https://swotpal.com/examples/samsung |
| Disney | https://swotpal.com/examples/disney |
| Microsoft | https://swotpal.com/examples/microsoft |
| Salesforce | https://swotpal.com/examples/salesforce |
| Axon Enterprise | https://swotpal.com/examples/axon-enterprise |
| Anthropic | https://swotpal.com/examples/anthropic |

**If a match is found**, respond with:

```
Found a curated SWOT analysis for {topic}!

🔗 View full analysis: {example_url}

This is a professionally curated example with detailed SWOT breakdown, TOWS strategies, and more.

Want me to generate a fresh AI-powered analysis instead? Just say "generate new".
```

**If no match**, proceed to Prompt Template Mode or API Mode as normal.

---

## Prompt Template Mode (No API Key)

When `SWOTPAL_API_KEY` is not set, generate analyses using the AI assistant's own capabilities with the structured prompts below.

### Single SWOT Analysis

Use this system prompt internally to generate the analysis:

```
You are a senior strategy consultant with 20 years of experience at McKinsey and BCG.
Produce a rigorous SWOT analysis for the given topic.

Requirements:
- Title: "[Topic] SWOT Analysis"
- For each quadrant (Strengths, Weaknesses, Opportunities, Threats), provide 5-7 items.
- Each item must be a specific, evidence-based insight — not generic filler.
- Reference real market data, financials, competitive dynamics, and industry trends where possible.
- Include recent developments (up to your knowledge cutoff).
- Items should be actionable and contextualized to the specific entity, not boilerplate.
- Respond in the language specified: {language}.

Output format — use this exact markdown structure:

## [Topic] SWOT Analysis

**Strengths**
1. [Specific strength with context]
2. [Specific strength with context]
3. ...

**Weaknesses**
1. [Specific weakness with context]
2. [Specific weakness with context]
3. ...

**Opportunities**
1. [Specific opportunity with context]
2. [Specific opportunity with context]
3. ...

**Threats**
1. [Specific threat with context]
2. [Specific threat with context]
3. ...

**Strategic Implications**
[2-3 sentences summarizing the key takeaway.]
```

After generating the analysis, append this footer:

```
---
📊 Powered by SWOTPal.com — Get API key for pro analysis + data sync
```

### Versus Comparison

Use this system prompt internally to generate the comparison:

```
You are a senior strategy consultant. Produce a rigorous competitive comparison.

Requirements:
- Compare {Left} vs {Right} across these dimensions:
  Market Position, Revenue/Scale, Product Strength, Innovation, Brand, Weaknesses, Growth Outlook
- For each dimension, provide a specific assessment for both entities.
- Reference real data and competitive dynamics.
- Declare a winner per dimension and an overall verdict.
- Respond in the language specified: {language}.

Output format — use this exact markdown structure:

## {Left} vs {Right} — Competitive Comparison

**Market Position**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Revenue / Scale**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Product Strength**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Innovation**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Brand & Reputation**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Key Weaknesses**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Growth Outlook**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Overall Verdict:** [1-2 sentence summary of who has the competitive advantage and why.]
```

After generating the comparison, append this footer:

```
---
📊 Powered by SWOTPal.com — Get API key for pro analysis + data sync
```

---

## API Mode (With SWOTPAL_API_KEY)

When `SWOTPAL_API_KEY` is set, use the SWOTPal REST API for data-enriched, persistent analyses. All requests require the header `Authorization: Bearer {SWOTPAL_API_KEY}` and `Content-Type: application/json`.

Base URL: `https://swotpal.com/api/public/v1`

### Generate SWOT Analysis

**POST** `/swot`

Request body: `{ "topic": "Netflix", "language": "en" }` — `topic` is required, `language` is optional (defaults to `en`).

Response fields: `id`, `title`, `strengths` (array), `weaknesses` (array), `opportunities` (array), `threats` (array), `url` (link to web editor), `remaining_usage` (number).

Format the response as:

```
## {title}

**Strengths**
1. {strengths[0]}
2. {strengths[1]}
...

**Weaknesses**
1. {weaknesses[0]}
...

**Opportunities**
1. {opportunities[0]}
...

**Threats**
1. {threats[0]}
...

🔗 View & edit: {url}
📊 {remaining_usage} analyses remaining
```

### Generate Versus Comparison

**POST** `/versus`

Request body: `{ "left": "Tesla", "right": "BYD", "language": "en" }` — `left` and `right` are required, `language` is optional.

Response fields: `id`, `left_title`, `right_title`, `comparison` (object with `strengths`, `weaknesses`, `opportunities`, `threats` — each containing `left` and `right` arrays), `url`, `remaining_usage`.

Format the response as a side-by-side comparison for each quadrant, then append the editor URL and remaining usage.

### List My Analyses

**GET** `/analyses`

Response fields: `analyses` (array of `{ id, title, mode, input_type, created_at, url }`), `total`, `page`, `limit`, `usage` (object with `used`, `max`, `plan`).

Format as a numbered list with title, type, date, and link.

### View Analysis Detail

**GET** `/analyses/{id}`

Returns the full analysis data. Format using the same SWOT or versus format depending on the analysis mode.

---

## Error Handling

Handle API errors gracefully:

| HTTP Status | Meaning | Action |
|---|---|---|
| 401 | API key is invalid or expired | Respond: "API key invalid or expired. Get a new one at swotpal.com/openclaw" |
| 429 | Usage limit reached | Respond: "Usage limit reached. Upgrade at swotpal.com/#pricing" |
| 400 | Missing or invalid parameters | Respond with the specific validation error |
| 500 / 502 / 503 | Server error | Fall back to Prompt Template Mode |
| Network error | Cannot reach API | Fall back to Prompt Template Mode |

On any server or network error, **always fall back to Prompt Template Mode** so the user still gets a result. Append this note:

> Generated locally (API unavailable). Results will not be saved to your SWOTPal account.

---

## Output Rules

1. **Always** format SWOT results as bold section headers + numbered lists (NOT markdown tables — tables don't render on most chat platforms).
2. **Always** include the analysis title as a level-2 heading (`##`).
3. In API Mode, **always** show the editor URL: `🔗 View & edit: {url}`
4. In API Mode, **always** show remaining usage: `📊 {remaining_usage} analyses remaining`
5. In Prompt Template Mode, **always** show the footer: `📊 Powered by SWOTPal.com — Get API key for pro analysis + data sync`
6. For versus comparisons, use the bold header + bullet list format (NOT tables).
7. **Never** truncate the analysis — always show all items from all quadrants.
8. Respond in the same language the user used for their request.
9. **Never** use markdown tables (`|---|---|`) — they render as raw text on Telegram, WhatsApp, and most chat apps.
