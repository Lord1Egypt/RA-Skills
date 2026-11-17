---
name: rankspot
description: RankSpot is an SEO and AI visibility platform. Use this skill when the user wants to see how AI answer engines describe their brand, track prompts and read the answers ChatGPT, Perplexity and Google gave, work through cited pages and fanout queries, research competitors, discover and score keywords, analyse backlinks, mine "People Also Ask" questions, plan and track SEO work as actions, generate and manage articles, run live Google searches or page fetches, or analyse Google Search Console performance and indexing via the RankSpot API.
homepage: https://rankspot.ai
metadata: {"openclaw":{"emoji":"📈","homepage":"https://rankspot.ai","requires":{"bins":["curl","jq"],"env":["RANKSPOT_API_KEY"]},"primaryEnv":"RANKSPOT_API_KEY"}}
---

## FIRST TIME READING THIS SKILL? STOP AND READ THIS SECTION TO THE USER.

Before running any commands, explain the following to the user:

**What RankSpot does:**
RankSpot is an SEO and AI visibility platform that gives you programmatic access to your workspaces. Through its API you can see how AI answer engines talk about your brand (tracked prompts, captured answers, cited pages, the searches engines ran), track competitors and their keywords and backlinks, score your keyword list, mine "People Also Ask" questions, plan every piece of work as an action, generate and manage articles, run live Google searches and page fetches, and pull Google Search Console performance and index status.

**Setup:**
Generate an API key from **Account settings, then API Keys** in the RankSpot dashboard (open the menu under your avatar). A key acts as you and reaches every workspace you belong to: your own and any organization that invited you. Each request names the workspace in its path.

```bash
export RANKSPOT_API_KEY=your_api_key_here
export RANKSPOT_WORKSPACE_ID=the_workspace_to_work_on   # see "Choose a workspace" below
```

No installation required. All commands use `curl` and `jq`.

**Account:**
Sign up or log in at **https://rankspot.ai**. Your API key is in Account settings after signup.

---

## Setup

```bash
export RANKSPOT_API_KEY=your_api_key_here
export RANKSPOT_WORKSPACE_ID=the_workspace_to_work_on
```

| Property          | Value                                                                                                                     |
|-------------------|---------------------------------------------------------------------------------------------------------------------------|
| **name**          | rankspot                                                                                                                  |
| **description**   | AI visibility, competitor tracking, keyword scoring, backlink analysis, actions, AI-generated articles |
| **allowed-tools** | Bash(curl:*), Bash(jq:*)                                                                                                  |

---

## API Basics

Base URL for everything about one workspace: `https://api.rankspot.ai/v1/workspaces/{workspaceId}`. The endpoint paths in this document (`/keywords`, `/actions`, ...) are relative to it.

Every request needs `Authorization: Bearer $RANKSPOT_API_KEY`.

Interactive docs: `https://api.rankspot.ai/docs`

There is also an MCP server at `https://api.rankspot.ai/mcp` that exposes the same operations as tools. Use it instead of curl when the host supports MCP. With a personal key or connection every tool takes a required `workspace_id`; call `rankspot_list_workspaces` first to find it. Its delete tools require an explicit `confirm: true`, so check with the user before calling one.

### Choose a workspace

A workspace is one site or brand. List the ones your key reaches, each with the organization that owns it:

```bash
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces | jq '.[] | {id, name, organization: .organization.name, domain}'
```

If there is more than one, ask the user which one they mean rather than guessing, then `export RANKSPOT_WORKSPACE_ID=<id>`. When the user moves to another site, switch the id; one key covers them all.

**Older keys.** A key created before personal keys reaches only the workspace it was made in. `GET /v1/workspaces` lists just that one, and it also works on the old paths without the workspace part (`https://api.rankspot.ai/v1/keywords`). A personal key on those old paths gets `400` with `workspace-required`.

`GET https://api.rankspot.ai/health` needs no auth and is outside the `/v1` prefix. Use it to tell "the API is down" apart from "my key is wrong".

### Validate your API key

```bash
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID | jq .
```

`Missing API key` or `Invalid API key` means the key is wrong. Ask the user to check **Account settings, then API Keys**. `403` with "does not reach that workspace" means the key is fine but `RANKSPOT_WORKSPACE_ID` is not one of its workspaces: list them again.

### Response shapes

**List endpoints** wrap results in a `data` envelope:

```json
{
  "data": {
    "total": 120,
    "offset": 0,
    "limit": 20,
    "count": 20,
    "items": []
  }
}
```

**Everything else returns the object directly, with no envelope.** A single article, a created action, a keyword cluster, a Search Console report and a research result all come back at the top level. So use `jq '.data.items[]'` for lists and `jq '.title'` for a single resource.

### Pagination

Query parameters: `offset` (default 0) and `limit` (default 20, max 100).

Trial and inactive subscriptions are capped at `offset=0` and `limit<=20`. Active subscriptions paginate freely.

### Dates

AI visibility and Search Console take calendar days as `YYYY-MM-DD` in UTC. Full timestamps are rejected. If you hold a JavaScript `Date`, send `.toISOString().slice(0, 10)`.

---

## What You Get

| Capability              | What it is                                                                                              | Endpoints                                                                 |
|-------------------------|---------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| **Workspace**           | Brand, domain, what the business does and who it sells to. Read this first.                              | `GET /v1/workspaces/{workspaceId}`                                        |
| **AI Visibility**       | Tracked prompts, captured answers, cited pages, fanout queries, and a scored summary                     | `/ai-visibility/prompts`, `/responses`, `/citations`, `/fanouts`, `/summary` |
| **Actions**             | Every piece of planned work, typed. Only `write_article` turns into an article.                          | `POST/GET/PATCH/DELETE /actions`, `POST /actions/:id/generate`             |
| **Articles**            | AI-generated articles with full HTML, publish dates and index status                                     | `GET/PATCH/DELETE /articles`                                              |
| **Keywords**            | Scored keyword list with semantic clustering                                                             | `POST/GET /keywords`, `GET /keywords/:id/cluster`                          |
| **Backlinks**           | Competitor backlinks you do not have yet, plus your own link profile                                     | `GET/PATCH/DELETE /backlinks`                                             |
| **Competitors**         | Brands you track, plus brands RankSpot discovered in AI answers                                          | `POST/GET/DELETE /competitors`                                            |
| **People Also Ask**     | PAA questions mined from search results for your keywords                                                | `GET/PATCH/DELETE /people-also-ask`                                       |
| **Categories**          | Group actions and articles                                                                               | `POST/GET/PATCH/DELETE /categories`                                       |
| **Research**            | Live Google search and page fetch. Costs credits per call.                                               | `POST /research/google`, `POST /research/fetch`                           |
| **Search Console**      | Clicks, impressions, CTR, position, index status, indexing requests                                      | `POST /gsc/performance`, `/gsc/inspect`, `/gsc/index`                     |

---

## Start Here: Read the Workspace

A keyword, a cited page or a competitor backlink only means something in the context of a particular business. Read the workspace before deciding what work is worth doing.

```bash
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID | jq .
```

**Response (200):**
```json
{
  "id": "clx...",
  "name": "Screen Studio",
  "brandName": "Screen Studio",
  "domain": "https://screen.studio/",
  "businessDescription": "A macOS app that records your screen and polishes the footage automatically.",
  "targetAudience": "Indie developers, designers and founders who publish demo videos.",
  "benefits": "Automatic zooms, no editing skills needed, exports in 4K.",
  "toneOfVoice": "Direct and practical, no marketing filler.",
  "industry": "Software",
  "location": "US",
  "language": "en"
}
```

All fields are read-only and any of them can be null. They are edited in the dashboard because they shape article generation and the AI visibility analysis.

`domain` is stored as the user typed it, so it may be a bare hostname or a full URL. Everywhere else in the API a domain is a bare hostname, so strip the scheme and trailing slash before comparing.

---

## Core Workflow: AI Visibility

The question this answers: when someone asks ChatGPT or Perplexity what your product does, do you show up, and if not, what do you do about it?

```bash
# 1. Score the period. Both dates are required.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/summary?startDate=2026-08-01&endDate=2026-08-31" | jq .

# 2. See which pages the engines cited. These are pages you want to be on.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/citations?type=new&limit=50" | jq \
  '.data.items[] | {id, url, domain, citations, isOwnDomain}'

# 3. See what the engines actually searched for while answering. Content gaps in their own words.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts?type=new&limit=50" | jq \
  '.data.items[] | {id, query, searches}'

# 4. Pull the full cluster for a gap worth covering, so one article answers every phrasing.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts/<fanout-id>/cluster | jq .

# 5. Turn it into work. A get_cited action for a page, a write_article action for a gap.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "get_cited",
    "title": "Get listed in Zapier best screen recorders roundup",
    "shortDescription": "Cited in 6 ChatGPT answers, and you are in none of them.",
    "citationId": "<citation-id>"
  }' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions | jq .
```

Prompts are run by RankSpot on a daily schedule. Adding a prompt does not produce an answer immediately, it produces one on the next run.

---

## Core Workflow: Keywords to Article

```bash
# 1. The worklist: keywords with no article planned and none written.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords?type=new&sortBy=compositeScore&sortOrder=desc&limit=50" | jq \
  '.data.items[] | {id, keyword, compositeScore, searchVolume, competitionIndex}'

# 2. Get the semantic cluster for your best seed keyword. Returns a bare array.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords/<seed-id>/cluster | jq .

# 3. Plan the work as a write_article action.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "write_article",
    "title": "How to Do Keyword Research in 2026",
    "description": "A step-by-step guide for beginners targeting informational intent.",
    "keywordIds": ["<seed-id>", "<cluster-id-1>", "<cluster-id-2>"]
  }' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions | jq '{id, type, status}'

# 4. Trigger generation. The action must be write_article with status new.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<action-id>/generate | jq .

# 5. Poll until the action reports processed, then read articleId off it.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<action-id> | jq '{status, articleId}'

# 6. Fetch the article with full HTML.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<article-id> | jq '{title, slug, contentHtml}'
```

Generation is asynchronous and takes roughly 5 to 10 minutes. Space your polls, do not loop tightly.

---

## Core Workflow: Competitor Intelligence

```bash
# 1. See who RankSpot already found in AI answers before adding anyone by hand.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/competitors?scope=discovered&limit=20" | jq \
  '.data.items[] | {id, name, domain, mentionCount}'

# 2. Promote one to tracked, or add a brand of your own. Same endpoint either way.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ahrefs", "domain": "ahrefs.com"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/competitors | jq '.id'
# Keyword and backlink discovery runs on a background sync every 1 to 2 weeks.
# If the user needs data sooner, point them at dan@rankspot.ai.

# 3. Their keywords you have no content for.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords?competitorId=<id>&type=new&sortBy=compositeScore&sortOrder=desc" | jq \
  '.data.items[] | {keyword, compositeScore, searchVolume}'

# 4. The domains linking to them, which is your link gap.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=competitors&competitorId=<id>" | jq \
  '.data.items[] | {domainFrom, domainFromRank, competitorCount, pages: [.links[].urlFrom]}'
```

---

## Commands Reference

### AI Visibility

RankSpot asks your tracked prompts on ChatGPT, Perplexity, Google AI Overview and Google AI Mode on a daily schedule, then analyses the answers. Platform values are `chatgpt`, `perplexity`, `google_ai_overview`, `google_ai_mode`.

The list endpoints take optional `startDate` and `endDate`. Omit both and you get the full history, paginated. Either bound works alone.

#### Summary

```bash
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/summary?startDate=2026-08-01&endDate=2026-08-31" | jq .
```

Both dates are **required** here. A score without a period means nothing.

**Response (200):**
```json
{
  "startDate": "2026-08-01",
  "endDate": "2026-08-31",
  "visibilityScore": 42.9,
  "shareOfVoice": 22.5,
  "citationShare": 8.1,
  "categoryRank": 3,
  "responsesCounted": 112,
  "platforms": { "chatgpt": 66.7, "perplexity": 25, "google_ai_overview": null, "google_ai_mode": 0 },
  "leaderboard": [
    { "competitorId": "clx...", "name": "RankSpot", "domain": "rankspot.ai", "isOwnBrand": true, "mentions": 31, "shareOfVoice": 27.7, "position": 1, "sentiment": 82 }
  ]
}
```

| Field              | Meaning                                                                                       |
|--------------------|-----------------------------------------------------------------------------------------------|
| `visibilityScore`  | Share of answers naming your brand, 0 to 100, as the mean of the per-platform scores          |
| `shareOfVoice`     | Your mentions as a share of all brand mentions                                                 |
| `citationShare`    | Citations pointing at your domain as a share of all citations                                  |
| `categoryRank`     | Your 1-based position in the leaderboard                                                       |
| `responsesCounted` | Answers behind the scores. Read this before quoting any of the others.                         |
| `platforms`        | Per-platform visibility. `null` means the platform produced no answer, `0` means it never named you. |
| `leaderboard`      | Ten most-mentioned brands, with yours always included                                          |

**Every score is nullable and null means "no data in the period", never zero.** Failed or incomplete runs are excluded everywhere, so an outage does not read as poor visibility.

There is no built-in period comparison. Call it twice with two periods of equal length. Comparing 30 days against 7 measures the calendar, not your visibility.

#### Prompts

```bash
# List tracked prompts
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/prompts" | jq '.data.items[]'

# Archived prompts instead
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/prompts?type=archived" | jq .

# Track a new prompt. Max 2000 characters.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "best seo tools for small business"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/prompts | jq .

# Reword an existing prompt. The run history stays attached.
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "best seo tools for small businesses in 2026"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/prompts/<id> | jq .

# Archive (frees an allowance slot) and restore
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/prompts/<id>
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/prompts/<id>/unarchive
```

Prompts are archived, never deleted: the run history is the only source for the reporting, so removing it would rewrite past results. Resubmitting a prompt you archived restores it instead of failing.

**Allowances:** 5 prompts with no subscription, 10 on trial, and whatever the plan sets once subscribed (25 if the plan does not say).

**Errors:** `400 ai-prompt-limit-exceeded`, `400 ai-prompt-already-exists`, `400 ai-prompt-text-required`.

#### Responses

```bash
# Captured answers, newest first
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/responses?startDate=2026-08-01&endDate=2026-08-31&limit=50" | jq \
  '.data.items[] | {id, platform, runDate, promptText, ownBrandMentioned, citationsCount}'

# Only answers that did not name you, on two platforms
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/responses?mentioned=false&platform=chatgpt,perplexity" | jq .

# Only answers to one tracked prompt
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/responses?promptId=<id>" | jq .

# The full answer, its citations in order, the searches it ran, every brand it named
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/responses/<id> | jq .
```

Runs that failed or are still in flight are never returned, so an absent response is not counted as a miss.

The detail view adds `answerMarkdown`, `citations`, `fanoutQueries` and a richer `brands` array carrying `competitorId`, `position`, `sentiment` (0 to 100, where 0 to 33 is negative, 34 to 66 neutral, 67 to 100 positive) and `isOwnBrand`.

#### Cited pages

```bash
# The worklist: cited pages you have not acted on, most cited first
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/citations?type=new&limit=50" | jq \
  '.data.items[] | {id, url, domain, citations, platforms, isOwnDomain}'

# Narrow to one site, over a period
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/citations?domain=reddit&startDate=2026-08-01&endDate=2026-08-31" | jq .

# Mark one handled, or put it back on the worklist
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "processed"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/citations/<id> | jq .

# Archive and restore
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/citations/<id>
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/citations/<id>/unarchive
```

| Parameter               | Values                                     | Default     |
|-------------------------|--------------------------------------------|-------------|
| `type`                  | `new`, `processed`, `archived`             | `new`       |
| `domain`                | Substring, case-insensitive                 | none        |
| `startDate` / `endDate` | `YYYY-MM-DD`                                | full history |
| `sortBy`                | `citations`, `lastSeenAt`, `firstSeenAt`, `domain` | `citations` |
| `sortOrder`             | `asc`, `desc`                               | `desc`      |

`citations` counts only what falls inside the requested period. `firstSeenAt` and `lastSeenAt` are all-time and are not clipped to it. Status and archive are separate axes: `PATCH` sets status, `DELETE` and `/unarchive` handle archiving. Archiving a page does not remove it from the reporting, because it is a statement about your workflow, not about what the engines cited.

#### Fanout queries

The searches an engine ran while composing an answer. A citation tells you which page an engine trusted. A fanout query tells you what it decided it needed to know, so a query you rank for nowhere is a content gap in the engine's own words.

```bash
# The worklist: queries with no article planned and none written
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts?type=new&limit=50" | jq \
  '.data.items[] | {id, query, searches, platforms}'

# Everything about one theme
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts?query=screen%20recorder&type=all" | jq .

# The cluster: every phrasing of the same intent, seed first
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts/<id>/cluster | jq .

# Archive and restore
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts/<id>
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts/<id>/unarchive
```

| Parameter               | Values                                              | Default      |
|-------------------------|-----------------------------------------------------|--------------|
| `type`                  | `new`, `planned`, `processed`, `all`, `archived`    | `new`        |
| `query`                 | Substring, case-insensitive                          | none         |
| `startDate` / `endDate` | `YYYY-MM-DD`                                         | full history |
| `sortBy`                | `searches`, `lastSeenAt`, `firstSeenAt`, `query`     | `searches`   |
| `sortOrder`             | `asc`, `desc`                                        | `desc`       |

State is derived from the work linked to the query, the same rule keywords use, so it moves on its own: `planned` means a `write_article` action exists but no article, `processed` means an article exists.

The cluster returns up to 100 related searches with the seed leading (the seed reports `searches: 0`). Pass those ids straight to `POST /actions` as `fanoutQueryIds`. Engines phrase one intent many ways, so an action should carry the whole cluster rather than whichever phrasing you happened to pick.

---

### Actions

An action is one piece of planned work. Every action has a `type` that says what kind of work it is and which target it needs. Actions replace the old topics endpoints.

| Type               | What it means                                                    | Required target |
|--------------------|------------------------------------------------------------------|-----------------|
| `write_article`    | Plan a piece of content, then call `/generate` to write it        | none            |
| `update_article`   | Any edit to an existing article                                   | `articleId`     |
| `publish_article`  | Push a finished article to the workspace integrations             | `articleId`     |
| `request_indexing` | Ask Google to index a published page it has missed                | `articleId`     |
| `earn_link`        | Go after a referring domain your competitors have                 | `backlinkId`    |
| `get_cited`        | Get onto a page AI engines already cite                           | `citationId`    |
| `reply_thread`     | Reply on a cited Reddit or Quora thread                           | `citationId`    |
| `record_video`     | Make a video of your own, since you cannot be added to someone else's | `citationId` |
| `track_competitor` | Start tracking a brand RankSpot discovered in AI answers          | `competitorId`  |
| `add_prompt`       | Track a question buyers ask that no existing prompt covers        | none            |
| `other`            | Anything you just want written down                               | none            |

**Only `write_article` produces an article.** The rest are a person's job, and you close them by hand.

#### Create an action

```bash
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "write_article",
    "title": "How to Do Keyword Research in 2026",
    "shortDescription": "Engines ran this search 14 times and cited nobody you compete with.",
    "description": "A step-by-step guide for beginners targeting informational intent.",
    "additionalInstructions": "Include a comparison table of top tools.",
    "slug": "keyword-research-2026",
    "categoryId": "<category-id>",
    "keywordIds": ["<id1>", "<id2>"],
    "fanoutQueryIds": ["<id3>", "<id4>"]
  }' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions | jq .
```

| Field                    | Applies to                                    | Notes                                                         |
|--------------------------|-----------------------------------------------|---------------------------------------------------------------|
| `type`                   | all, required                                  | No default                                                    |
| `title`                  | all, required                                  | Max 500 chars, unique per workspace, archived rows ignored     |
| `shortDescription`       | all                                            | Max 200. The one line shown under the title, usually the only text anyone reads. Lead with evidence and numbers, do not restate the title. |
| `description`            | all                                            | Max 2000. On `write_article` this is the generation brief, elsewhere the fuller explanation |
| `additionalInstructions` | all                                            | Max 2000. On `update_article` this carries the actual edit instruction |
| `slug`                   | `write_article` only                           | Validated, not rewritten. Unique across actions and articles. Omit to derive it from the title at generation time. |
| `categoryId`             | `write_article` only                           |                                                               |
| `keywordIds`             | `write_article` only                           | Broadens semantic coverage                                    |
| `fanoutQueryIds`         | `write_article`, `update_article`, `add_prompt` | Provenance, not a target. Send the whole cluster.             |
| target id                | per the table above                            | `articleId`, `backlinkId`, `citationId` or `competitorId`      |

Fields that do not apply to the type are dropped silently rather than rejected. A target that does not exist in your workspace is a 400.

Only one open action per target per type. Three types share `articleId` because publishing, indexing and editing an article are different work.

#### List, read, update

```bash
# List. Archived actions are never returned.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions?status=new,in_progress&types=write_article,get_cited&limit=50" | jq \
  '.data.items[] | {id, type, title, status}'

# Search by title or description
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions?search=keyword%20research" | jq .

# One action, with its targets and linked keywords embedded
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<id> | jq .

# Edit the content (only while status is new)
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Keyword Research Guide 2026", "keywordIds": ["<id1>", "<id4>"]}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<id> | jq .

# Close it, which also marks the citation or backlink behind it handled
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "processed"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<id> | jq .

# Dismiss it without deciding it. Nothing is deleted.
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"archived": true}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<id> | jq .
```

**Statuses:** `new` (not started), `in_progress` (an executor is running), `processed` (finished).

Content can only be edited while the action is `new`. Once an executor starts, a content edit returns `action-locked`. Bookkeeping stays open: `archived` at any point, and `status` on anything that is not currently `in_progress`.

`status: "processed"` stamps `completedAt` and marks the evidence behind the action handled. `status: "new"` clears `completedAt`, puts that evidence back on the worklist and undoes a dismissal. This runs both ways: un-archiving a citation, or setting it back to `new`, reopens its action.

Passing `keywordIds` replaces the full set of linked keywords.

#### Generate an article

```bash
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<id>/generate | jq .
```

**Response (201):** `{ "success": true }`

The action must be `type: "write_article"` with `status: "new"`. Generation is asynchronous and takes roughly 5 to 10 minutes. Poll `GET /actions/:id` until `status` is `processed`, then read `articleId`.

#### Delete an action

```bash
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<id>
```

Returns `204`. Hard delete, permanent. Any generated article is preserved and only the link is removed. To take an action off the board reversibly, use `{"archived": true}` instead.

**Errors:** `400 action-title-already-exists`, `action-slug-already-exists`, `action-reference-not-found`, `action-target-occupied`, `action-locked`, `action-in-progress`, `action-type-not-generatable`.

---

### Articles

Articles come from `write_article` actions. They cannot be created directly. Their body is editable as Markdown, every edit lands in the revision history, and nothing goes live until you publish.

```bash
# List. contentHtml is omitted to keep payloads small.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles?limit=50" | jq '.data.items[] | {id, title, slug, status}'

# Published pages Google has not indexed. The set worth acting on.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles?status=published&indexed=false" | jq \
  '.data.items[] | {title, slug, indexCoverageState, indexCheckedAt}'

# Go from a published URL back to its article, by the last path segment.
# This is how a page URL from /gsc/performance becomes an articleId.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles?slug=how-to-start-a-blog" | jq '.data.items[0]'

# Check whether you already covered a subject before planning another article
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles?search=screen%20recording" | jq '.data.items[] | .title'

# One article, with the body as HTML and as Markdown. No data envelope.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<id> | jq '{title, slug, status, contentMarkdown}'

# Edit: send the WHOLE edited Markdown back. Anything left out is deleted.
# Reuse one sessionId for every write in a conversation so it shows as one revision.
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" -H "Content-Type: application/json" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<id> \
  -d '{"contentMarkdown": "## Why start a blog\n\n...", "sessionId": "chat-2026-11-07-pricing"}'

# Publish (or update in place if already live) to a connected integration.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" -H "Content-Type: application/json" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<id>/publish -d '{"integration": "wordpress"}'

# History: the last 10 revisions, newest first, and undo by restoring one.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<id>/revisions | jq '.[] | {id, source, updatedAt, live}'
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<id>/revisions/<revision-id>/restore
```

**Editing the Markdown:** keep lines of HTML (videos and similar) as they are. Links are `[text](url)`; internal links are dofollow and external ones nofollow automatically. Only for an external link that must be dofollow, write `<a href="https://example.com" rel="dofollow">anchor</a>` (`rel="nofollow"` does the reverse for an internal link).

| Parameter    | Values                                                | Default |
|--------------|-------------------------------------------------------|---------|
| `search`     | Title or description substring                         | none    |
| `slug`       | Slug substring                                         | none    |
| `status`     | `draft`, `generating`, `generated`, `published`        | none    |
| `indexed`    | `true`, `false`                                        | none    |
| `categoryId` | UUID                                                   | none    |

**Statuses:** `generated` means the article exists in RankSpot and has never been sent anywhere. `published` means it reached at least one integration.

**Dates matter here.** Three fields look similar and answer different questions:

| Field              | Answers                                                                  |
|--------------------|---------------------------------------------------------------------------|
| `firstPublishedAt` | When it first went live. The publication date. Does not move on re-publish. |
| `lastPublishedAt`  | When the content last reached readers. This is your "last updated".        |
| `updatedAt`        | Any write at all, including a metadata edit. Not a publish date.           |

**Index fields** are refreshed by a weekly job, so they report the last check rather than this instant:

| Field                | Meaning                                                                          |
|----------------------|-----------------------------------------------------------------------------------|
| `isIndexed`          | Whether Search Console reports the page as indexed                                |
| `indexCoverageState` | Google's own reason when it is not. This decides what to do about it.             |
| `indexCheckedAt`     | When the status was last checked. Null means never checked, which is not the same as not indexed. |
| `indexRequestedAt`   | When indexing was last requested. Throttled to one per page per week.             |

Reading `indexCoverageState`: "Crawled - currently not indexed" means Google looked and declined, so the page needs work. "Discovered - currently not indexed" means it has not been crawled yet. A canonical or noindex reason means neither requesting nor rewriting will help.

```bash
# Update metadata
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Keyword Research Guide 2026", "slug": "keyword-research-guide-2026", "categoryId": "<id>"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<id> | jq .

# Delete. Permanent. Action and keyword links are preserved.
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles/<id>
```

Updatable: `title`, `description`, `slug` (unique per workspace), `coverImageUrl`, `categoryId`.

---

### Keywords

```bash
# Add keywords. Duplicates are silently skipped.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["seo tools", "keyword research", "link building"]}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords | jq .
# Response (201): { "count": 3 }

# The worklist, which is the default: no article planned and none written
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords?sortBy=compositeScore&sortOrder=desc&limit=50" | jq '.data.items[]'

# Scoped to one competitor
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords?type=new&competitorId=<id>&sortBy=compositeScore&sortOrder=desc" | jq .

# Substring search across everything non-archived
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords?type=all&keyword=seo&sortBy=searchVolume&sortOrder=desc" | jq .

# Archive and restore. Both return 204.
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords/<id>
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords/<id>/unarchive

# Semantic cluster. Returns a bare array, no data envelope.
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/keywords/<id>/cluster | jq .
```

| Parameter      | Values                                                                     | Default          |
|----------------|----------------------------------------------------------------------------|------------------|
| `type`         | `new`, `planned`, `processed`, `all`, `archived`                            | `new`            |
| `keyword`      | Substring filter                                                            | none             |
| `competitorId` | UUID. Omit for keywords across all competitors.                             | none             |
| `sortBy`       | `compositeScore`, `opportunityIndex`, `searchVolume`, `competitionIndex`, `aiScore` | `compositeScore` |
| `sortOrder`    | `asc`, `desc`                                                               | `desc`           |

**Type meanings.** State is derived from the actions and articles linked to the keyword, so it moves on its own.

- `new` is the default and the worklist: no article planned, none written
- `planned` has a `write_article` action but no article yet
- `processed` has a linked article
- `all` is every non-archived keyword
- `archived` is the soft-deleted set

**Keyword fields:**

| Field              | Description                                                       |
|--------------------|-------------------------------------------------------------------|
| `keyword`          | The keyword string                                                |
| `searchVolume`     | Monthly search volume                                             |
| `competition`      | `LOW`, `MEDIUM`, `HIGH`                                           |
| `competitionIndex` | 0 to 100 competition level                                        |
| `opportunityIndex` | 0 to 100, high volume plus low competition                        |
| `aiScore`          | 0 to 100 relevance to your business                               |
| `compositeScore`   | 0 to 100 blend of opportunity and AI score. The primary sort signal. |
| `actionIds`        | Actions this keyword is linked to                                 |
| `articleIds`       | Articles written for it                                           |

The cluster walks pgvector cosine similarity at threshold 0.87 and returns up to 100 keywords as `[{ id, keyword }]`, sorted by composite score. An empty array means the seed has not been embedded yet, which happens on a background schedule. Use a cluster when planning a `write_article` action so the piece covers a broader semantic range.

---

### Backlinks

Backlinks are discovered by a background sync and cannot be created through the API. Each row is one referring domain: `competitorCount` says how many of your competitors it links to, `linksToYou` whether it already links to you, and `links[]` holds every link from it, one per target, with the page (`urlFrom`), `anchor`, `dofollow` and `backlinkSpamScore`. A link with `competitor: null` points to you. The default view is your link gap, domains linking to competitors but not to you, sorted by `competitorCount` so a site that lists several competitors comes first: it already writes about your market.

```bash
# The prospecting list, domains linking to the most competitors first
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=competitors" | jq \
  '.data.items[] | {id, domainFrom, domainFromRank, competitorCount, links: [.links[] | {competitor: .competitor.domain, urlFrom, anchor, dofollow}]}'

# Strongest domains first instead
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=competitors&sortBy=domainFromRank&sortOrder=desc" | jq .

# Domains linking to one competitor
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=competitors&competitorId=<id>" | jq .

# Does a specific site link to any competitor?
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=competitors&domainFrom=producthunt" | jq .

# Your own profile
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=mine&sortBy=domainFromRank&sortOrder=desc" | jq .

# Mark one handled after outreach. Note the /update suffix. Returns 204.
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "processed"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks/<id>/update

# Archive and restore
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks/<id>
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks/<id>/unarchive
```

| Parameter      | Values                                              | Default          |
|----------------|-----------------------------------------------------|------------------|
| `type`         | `competitors`, `mine`, `processed`, `archived`      | `competitors`    |
| `competitorId` | UUID. Only applies when `type=competitors`.         | none             |
| `domainFrom`   | Substring filter on the linking domain              | none             |
| `sortBy`       | `domainFromRank`, `firstSeen`, `backlinkSpamScore`  | `domainFromRank` |
| `sortOrder`    | `asc`, `desc`                                       | `desc`           |

**Backlink fields:**

| Field               | Description                                                  |
|---------------------|--------------------------------------------------------------|
| `domainFrom`        | The linking domain                                           |
| `urlFrom`           | The exact linking page                                       |
| `urlTo` / `domainTo`| Where the link points                                        |
| `domainFromRank`    | Authority of the linking domain, higher is stronger          |
| `pageFromRank`      | Authority of the linking page                                |
| `rank`              | Combined authority score                                     |
| `dofollow`          | `true` when the link passes equity                           |
| `backlinkSpamScore` | Lower is cleaner                                             |
| `anchor`            | Anchor text                                                  |
| `firstSeen`         | When it was first detected                                   |
| `attributes`        | `rel` values, for example `["noopener", "noreferrer"]`       |
| `competitorId`      | Which competitor it belongs to. Null means it is your own.   |
| `status`            | `new` or `processed`                                         |

Once RankSpot verifies a competitor backlink also points at your domain, it moves to `type=mine` and its status resets to `new`.

To track outreach properly, create an `earn_link` action against the backlink. Closing the action marks the backlink processed, and reopening it puts the backlink back on the worklist.

---

### Competitors

```bash
# Brands you track (default), newest first
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/competitors?scope=tracked&limit=20" | jq '.data.items[]'

# Brands RankSpot found in AI answers but is not tracking, most mentioned first
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/competitors?scope=discovered" | jq \
  '.data.items[] | {id, name, domain, mentionCount}'

# Add a brand, or promote a discovered one. Same call.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ahrefs", "domain": "ahrefs.com"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/competitors | jq .

# Stop tracking. Returns 204.
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/competitors/<id>
```

`scope` takes `tracked` (default), `discovered` or `all`.

**Response (201) from POST, no data envelope:**
```json
{
  "id": "clx...",
  "name": "Ahrefs",
  "domain": "ahrefs.com",
  "isTracked": true,
  "autoDiscovered": false,
  "mentionCount": 12,
  "createdAt": "2026-08-31T00:00:00.000Z",
  "updatedAt": "2026-08-31T00:00:00.000Z"
}
```

`domain` must be a bare hostname such as `ahrefs.com`, with no scheme and no path.

Your plan sets how many competitors you can track, and the default is 3. Auto-discovered brands cost nothing against that limit until you promote them. Posting a domain RankSpot already discovered promotes that row and keeps the mentions attributed to it, rather than creating a second one.

Keyword and backlink discovery starts on the next background sync, which runs every 1 to 2 weeks. If the user needs data sooner, point them at **dan@rankspot.ai**.

Deleting a competitor stops tracking it and removes it from every scope. The AI answers already attributed to it are kept so past visibility scores do not change. Keywords and backlinks are preserved. Adding the same domain again restores it.

**Errors:** `400 competitor-limit-exceeded` (plan limit reached, do not retry), `400 competitor-already-exists` (already tracked, or it is your own brand).

---

### People Also Ask

Questions discovered from search results for your tracked keywords. Read and manage only, no create.

```bash
# The worklist
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/people-also-ask?status=new&limit=50" | jq '.data.items[] | .question'

# Mark handled once the question is answered in your content
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "processed"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/people-also-ask/<id> | jq .

# Archive
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/people-also-ask/<id>
```

Fields: `id`, `question`, `status` (`new` or `processed`), `articleId` (the article that answers it, once one exists), `createdAt`, `updatedAt`.

---

### Categories

```bash
# Create. A colour is assigned automatically.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "SEO Guides"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/categories | jq .

# List
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/categories | jq '.data.items[]'

# Rename
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Keyword Research"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/categories/<id> | jq .

# Delete. Actions and articles in it keep existing with categoryId set to null.
curl -s -X DELETE -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/categories/<id>
```

Names must be unique within a workspace.

---

### Research

Two live lookups against the open web. **These are the only endpoints that spend credits per call.** Neither response reports what it cost. The remaining balance is visible in the RankSpot dashboard.

#### Search Google

```bash
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "best screen recording software for mac"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/research/google | jq .

# Ask for other blocks when you will actually read them
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "best screen recorder", "types": ["organic", "ai_overview", "people_also_ask"]}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/research/google | jq '.items[] | select(.type == "ai_overview") | .markdown'
```

**Response (201):**
```json
{
  "query": "best screen recording software for mac",
  "location": "United States",
  "language": "en",
  "items": [
    { "type": "organic", "rank": 1, "page": 1, "domain": "screen.studio", "title": "Screen Studio", "url": "https://screen.studio", "description": "..." }
  ]
}
```

`items` are the blocks of the results page in page order. Read `type` first and branch on it.

`types` chooses which blocks come back and defaults to `organic` and `discussions_and_forums`. Available: `organic`, `ai_overview`, `people_also_ask`, `discussions_and_forums`, `video`, `related_searches`. The others are opt-in because they are large: one `ai_overview` block often outweighs all ten organic results together, and the call costs the same either way.

On `organic` blocks, `rank` is the position among the organic results, not the page-wide position, which moves whenever Google adds a block above them. Container blocks carry their entries in a nested `items` array.

Always the top 10. Location and language come from the workspace, so results match what the rest of RankSpot reports.

#### Fetch a page

```bash
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/blog/post"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/research/fetch | jq -r .markdown
```

**Response (201):** `{ "markdown": "# ..." }` and nothing else.

Two providers are tried in turn, so pages that block the first one (Reddit most notably) still come back. The call can take up to about 2 minutes when it falls through to the second provider, so give your client a generous timeout. Flat cost per fetch however many providers it took. A page nothing could read is a 503 with the charge refunded, never a 200 with an empty string.

Use it to settle a specific question, not to crawl. One page, one charge.

**Errors for both:** `402 ai-credits-exhausted` with a `usage` block carrying `creditsUsed`, `creditsLimit` and `creditsRemaining`. `502` when the provider fails, `503` when no provider could read the page. A failed provider call costs nothing.

---

### Search Console

**Prerequisite:** the user must connect Google Search Console from the dashboard under **Integrations, then Google Search Console, then Connect, then select a property**. Without it every request here returns `401`.

These three endpoints return Google's payload directly, with no `data` envelope, and are rate limited to 100 requests per minute.

#### Performance data

```bash
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2026-08-01", "endDate": "2026-08-31", "dimensions": ["query"]}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/performance | jq .
```

| Field                   | Required | Description                                                        |
|-------------------------|----------|--------------------------------------------------------------------|
| `startDate`             | Yes      | `YYYY-MM-DD`. Data lags by about 2 to 3 days.                       |
| `endDate`               | Yes      | `YYYY-MM-DD`. Maximum range 16 months.                              |
| `dimensions`            | No       | Group by. Combine up to 3. Defaults to `["query"]` when omitted.     |
| `dimensionFilterGroups` | No       | Filters, ANDed within a group                                       |
| `startRow`              | No       | Zero-based offset for pagination                                    |
| `rowLimit`              | No       | 1 to 25000. Google's default of 1000 when omitted.                   |

**Dimension values:** `query`, `page`, `country`, `device`, `date`, `searchAppearance`

**Response (200):**
```json
{
  "siteUrl": "https://example.com/",
  "startDate": "2026-08-01",
  "endDate": "2026-08-31",
  "dimensions": ["query"],
  "rows": [
    { "keys": ["rankspot seo tool"], "clicks": 120, "impressions": 980, "ctr": 12.24, "position": 3.2 }
  ]
}
```

`ctr` is a percentage, so `12.24` means 12.24%. `position` is rounded to 1 decimal.

**Common queries:**

```bash
# Top queries by clicks
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2026-08-01", "endDate": "2026-08-31", "dimensions": ["query"], "rowLimit": 50}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/performance | jq '.rows | sort_by(-.clicks)[:10]'

# Trend over time
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2026-08-01", "endDate": "2026-08-31", "dimensions": ["date"]}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/performance | jq '.rows[] | {date: .keys[0], clicks, impressions, ctr, position}'

# Quick wins: high impressions, low CTR, already on page one
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2026-08-01", "endDate": "2026-08-31", "dimensions": ["query"], "rowLimit": 500}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/performance | \
  jq '[.rows[] | select(.impressions > 100 and .ctr < 3 and .position < 10)] | sort_by(-.impressions)[:10]'

# What one page ranks for
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2026-08-01",
    "endDate": "2026-08-31",
    "dimensions": ["query"],
    "dimensionFilterGroups": [
      { "filters": [{ "dimension": "page", "expression": "https://example.com/blog/seo-guide" }] }
    ]
  }' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/performance | jq '.rows | sort_by(-.clicks)'

# Brand vs non-brand
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2026-08-01",
    "endDate": "2026-08-31",
    "dimensions": ["query"],
    "dimensionFilterGroups": [
      { "filters": [{ "dimension": "query", "expression": "rankspot", "operator": "contains" }] }
    ]
  }' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/performance | jq '.rows'
```

Filter `operator` values: `equals` (default), `notEquals`, `contains`, `notContains`, `includingRegex`, `excludingRegex`.

Country codes are ISO 3166-1 alpha-3 (`usa`, `gbr`, `deu`, `fra`, `ind`), not alpha-2. Device values are `DESKTOP`, `MOBILE`, `TABLET`.

#### Check whether a page is indexed

```bash
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/blog/my-post"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/inspect \
  | jq '{indexed: (.indexStatusResult.verdict == "PASS"), state: .indexStatusResult.coverageState, lastCrawl: .indexStatusResult.lastCrawlTime}'
```

Takes `url` (required, must belong to the connected property) and `languageCode` (optional, default `en-US`). Returns Google's raw `inspectionResult`.

The page is indexed when `indexStatusResult.verdict` is `PASS`. When it is not, `indexStatusResult.coverageState` says why.

Google limits this API to roughly 2,000 queries per day and 600 per minute per property.

For a whole-site view, `GET /articles?status=published&indexed=false` answers the same question from RankSpot's weekly index sweep without spending an inspection quota.

#### Submit a page for indexing

```bash
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/blog/my-post", "type": "URL_UPDATED"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/index | jq .
```

Takes `url` (required) and `type` (`URL_UPDATED` by default, or `URL_DELETED` to request removal). Returns Google's raw `urlNotificationMetadata`.

- Needs a connection with the **indexing** OAuth scope and a Google account that is a **verified owner** of the property. A connection predating indexing support returns `401` until the user reconnects from the dashboard.
- A `201` means Google received the notification. It does not confirm indexing. Check with `/gsc/inspect` afterwards.
- Google's default quota is about 200 URLs per day per project.

**Search Console errors:**
- `401 Google Search Console is not connected`
- `401 No Search Console property selected`
- `401 Failed to refresh Google Search Console token`, meaning the token was revoked and the user must reconnect
- `502` when Google's API itself failed, with its message forwarded

---

## Workflow: Find Where AI Engines Ignore You

Use this when the user asks:
- "Does ChatGPT mention us?"
- "Why do we never show up in AI answers?"
- "Who is winning in AI search in our category?"

```bash
# Step 1: Score the last full month
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/summary?startDate=2026-08-01&endDate=2026-08-31" | \
  jq '{visibilityScore, shareOfVoice, citationShare, categoryRank, responsesCounted, platforms}'

# Step 2: Compare against the previous month of equal length
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/summary?startDate=2026-07-01&endDate=2026-07-31" | \
  jq '{visibilityScore, shareOfVoice}'

# Step 3: See who is being named instead
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/summary?startDate=2026-08-01&endDate=2026-08-31" | \
  jq '.leaderboard[] | {position, name, mentions, shareOfVoice, sentiment}'

# Step 4: Read answers that did not name you at all
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/responses?mentioned=false&startDate=2026-08-01&endDate=2026-08-31" | \
  jq '.data.items[] | {id, platform, promptText}'

# Step 5: Open one and see which pages it trusted instead
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/responses/<id> | \
  jq '{answerMarkdown, citations: [.citations[] | {position, domain, url, isOwnDomain}]}'

# Step 6: Turn the strongest pages into get_cited actions
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "get_cited", "title": "Get into the Zapier roundup", "shortDescription": "Cited in 6 answers, none naming us.", "citationId": "<citation-id>"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions | jq '{id, type, status}'
```

---

## Workflow: Fanout Gaps to Articles

Use this when the user asks:
- "What should we write next?"
- "What are AI engines actually searching for?"
- "Where are our content gaps?"

```bash
# Step 1: The most-run searches you have no content for
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts?type=new&sortBy=searches&sortOrder=desc&limit=50" | \
  jq '.data.items[] | {id, query, searches, platforms}'

# Step 2: Pull the cluster for the best one, so a single article covers every phrasing
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/ai-visibility/fanouts/<id>/cluster | jq .

# Step 3: Check you have not already written this
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles?search=screen%20recorder%20mac" | jq '.data.items[] | {title, slug, status}'

# Step 4: Plan it, carrying the whole cluster as provenance
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "write_article",
    "title": "The Best Mac Screen Recorders in 2026",
    "shortDescription": "Engines ran this search 41 times last month and never cited us.",
    "description": "Comparison guide covering editing, export quality and price.",
    "fanoutQueryIds": ["<seed-id>", "<cluster-id-1>", "<cluster-id-2>"],
    "keywordIds": ["<keyword-id>"]
  }' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions | jq '{id, type, status}'

# Step 5: Generate, then poll
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<action-id>/generate | jq .
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<action-id> | jq '{status, articleId}'
```

---

## Workflow: Competitor Backlink Gap

Use this when the user asks:
- "Show me backlinks my competitors have that I don't"
- "Where are my competitors getting links from?"

```bash
# Step 1: Their highest-authority links, which is your prospect list
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=competitors&sortBy=domainFromRank&sortOrder=desc&limit=100" | \
  jq '.data.items[] | {id, domainFrom, domainFromRank, dofollow, anchor, urlFrom}'

# Step 2: Compare against your own profile
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/backlinks?type=mine&sortBy=domainFromRank&sortOrder=desc" | \
  jq '.data.items[] | {domainFrom, domainFromRank, dofollow}'

# Step 3: Turn a prospect into tracked work
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "earn_link", "title": "Pitch Ahrefs blog for a mention", "shortDescription": "DR 91, dofollow, links to two competitors.", "backlinkId": "<backlink-id>"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions | jq '{id, status}'

# Step 4: Close the action once outreach lands. The backlink is marked processed with it.
curl -s -X PATCH -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "processed"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions/<action-id> | jq '{status, completedAt}'
```

---

## Workflow: Published but Not Indexed

Use this when the user asks:
- "Why isn't my article showing up in Google?"
- "Which pages has Google not indexed?"

```bash
# Step 1: Published pages Google has not indexed, with its stated reason
curl -s -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  "https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/articles?status=published&indexed=false&limit=100" | \
  jq '.data.items[] | {id, title, slug, indexCoverageState, indexCheckedAt, indexRequestedAt}'

# Step 2: Confirm live rather than trusting the weekly sweep
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/blog/my-post"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/inspect | jq '.indexStatusResult | {verdict, coverageState, lastCrawlTime}'

# Step 3: If it is simply undiscovered, ask Google to index it
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/blog/my-post"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/gsc/index | jq .

# Step 4: If Google crawled and declined, the page needs work. Track that.
curl -s -X POST -H "Authorization: Bearer $RANKSPOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "update_article", "title": "Rewrite the thin sections of the Mac recorder guide", "additionalInstructions": "Add original benchmarks and a comparison table.", "articleId": "<article-id>"}' \
  https://api.rankspot.ai/v1/workspaces/$RANKSPOT_WORKSPACE_ID/actions | jq '{id, type}'
```

"Crawled - currently not indexed" means Google looked and declined, so submitting again will not help. "Discovered - currently not indexed" means it has not been crawled yet, which is exactly what `/gsc/index` is for.

---

## Error Handling

All error responses are JSON.

| Status | Meaning                                                              |
|--------|----------------------------------------------------------------------|
| 200    | Success                                                              |
| 201    | Created                                                              |
| 204    | No content, returned by delete, archive and unarchive                |
| 400    | Validation error or business rule violation                          |
| 400    | Also `workspace-required`: a personal key called a path with no workspace |
| 401    | Missing, invalid or expired API key, or Search Console not connected |
| 402    | Out of AI credits, on the research endpoints only                    |
| 403    | The workspace in the path is not one this key reaches                |
| 404    | Not found, or belongs to another workspace                           |
| 429    | Rate limited                                                         |
| 502    | An upstream provider failed                                          |
| 503    | No provider could read the page, on `/research/fetch`                |

Anything you might branch on carries a `type` slug alongside the message, so match on the slug and show the sentence:

```json
{ "type": "competitor-limit-exceeded", "message": "..." }
```

| Slug                                                     | Where                                    |
|----------------------------------------------------------|------------------------------------------|
| `workspace-required`                                      | A personal key on a path with no workspace |
| `subscription-inactive`, `trial-pagination-limit`         | Guards                                   |
| `competitor-limit-exceeded`, `competitor-already-exists`  | Competitors                              |
| `ai-prompt-limit-exceeded`, `ai-prompt-already-exists`, `ai-prompt-text-required` | AI prompts       |
| `ai-credits-exhausted`                                    | Research, on the 402, with a `usage` block |
| `action-title-already-exists`, `action-slug-already-exists`, `action-reference-not-found`, `action-target-occupied`, `action-locked`, `action-in-progress`, `action-type-not-generatable` | Actions |
| `invalid-date-range`                                      | AI visibility summary                    |

**Handling 429:** wait 10 seconds and retry, then 20, then 40. Do not hammer the API in a loop. Space sequential requests by at least a second.

**Write blocking:** if the subscription is neither `active` nor `trialing`, every non-GET request is rejected with `subscription-inactive`. Reads still work.

---

## Rate Limits

| Endpoint group                                       | Limit                        |
|------------------------------------------------------|------------------------------|
| Everything (global)                                  | 5,000 requests per minute per API key |
| `POST /gsc/performance`, `/gsc/inspect`, `/gsc/index` | 100 requests per minute per API key   |

Google applies its own quotas on top: roughly 2,000 URL inspections per day and about 200 indexing requests per day.

---

## Tips

**Reading the API**
- Lists wrap in `data`, single resources do not. `jq '.data.items[]'` for lists, `jq '.title'` for one thing.
- Pick the workspace with `GET /v1/workspaces` and ask the user when there is more than one. Then read `GET /v1/workspaces/{workspaceId}` first: every other endpoint returns opportunities that only mean something for a particular business.
- `startDate` and `endDate` are calendar days, `YYYY-MM-DD`. A full ISO timestamp is rejected.

**AI visibility**
- Check `responsesCounted` before quoting any score. 100% visibility across two answers is not the same claim as 100% across two hundred.
- A `null` score means no data in the period, never zero.
- Compare periods of equal length, or you are measuring the calendar.
- Prompts run on a daily schedule, so a new prompt has no answers until the next run.
- Fanout queries are content gaps in the engine's own words. Pull the cluster before planning, so one article answers every phrasing.
- Archiving a citation or a query is a statement about your workflow. It never changes the reporting.

**Actions**
- Everything is an action, and the type decides what else the body needs. Only `write_article` generates.
- `shortDescription` is usually the only text anyone reads. Lead with the evidence and the numbers.
- Closing an action marks the citation or backlink behind it handled. Reopening puts it back. Use this instead of touching both sides by hand.
- Content is editable only while the action is `new`. Once generation starts it is locked.
- Prefer `{"archived": true}` over `DELETE`. Archiving is reversible, deleting is not.

**Keywords and content**
- `type=new` is the default and it is the worklist. Start there.
- Sort by `compositeScore`. It blends opportunity with AI relevance and is the best single signal.
- Use `/cluster` before planning an article so the piece covers a broader semantic range.
- Search `GET /articles?search=` before planning a new one, so you do not write the same piece twice.
- `contentHtml` and `contentMarkdown` are only in single-article responses. Fetch by ID for the full content.
- For "when was this last refreshed" use `lastPublishedAt`, not `updatedAt`. For the publication date use `firstPublishedAt`.

**Competitors and links**
- Check `scope=discovered` before adding a competitor by hand. RankSpot may already have found them, and discovered brands cost nothing against your plan limit.
- Competitor sync runs every 1 to 2 weeks. Data does not appear immediately. For a manual sync, point the user at **dan@rankspot.ai**.
- Competitor backlinks are your warmest prospects. Those sites already decided the niche is link-worthy.

**Research and Search Console**
- Research costs credits per call. Spend one when the answer changes what you do, such as who already ranks before you propose an article. Do not spend one confirming something the other endpoints already told you, and never crawl a site page by page.
- On `/research/google`, leave `types` alone unless you will read the extra blocks. `ai_overview` and `people_also_ask` dwarf the organic results.
- Search Console data lags 2 to 3 days. An `endDate` of yesterday often returns nothing.
- `dimensions` defaults to `["query"]`. Pass `["date"]` for trends or `["page"]` for page-level performance.
- To act on a GSC row, feed its page URL into `GET /articles?slug=` (last path segment) to get the article, then plan an `update_article` action against it.
- High impressions plus low CTR plus position under 10 is a quick win. The page is visible but not clicked, so the title or meta description is the fix.
- Country codes are alpha-3 (`usa`, `gbr`), not alpha-2.
- For a whole-site index view use `GET /articles?status=published&indexed=false`. Save `/gsc/inspect` for confirming one page.
- Submitting for indexing is a request, not a guarantee. Confirm with `/gsc/inspect` afterwards.

**Limits**
- Trial and inactive subscriptions are capped at `offset=0` and `limit<=20`, and inactive ones are read-only. Upgrade at https://rankspot.ai.
