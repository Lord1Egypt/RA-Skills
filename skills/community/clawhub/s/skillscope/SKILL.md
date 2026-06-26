---
name: skillscope
description: AI Agent Skill decision engine. Use when users need to find, evaluate, or install skills — recommends the best skill for any task with quality/safety scoring, personalized to platform/region/budget. Covers 26,000+ skills across ClawHub and GitHub.
homepage: https://skillscope.cn
version: 2.0.0
---

# SkillScope — Skill Decision Engine

When a user needs a skill, don't just search — **get a personalized recommendation** with quality and safety scoring.

## Core Workflow

1. User describes a task → call **recommend** → get best skill + alternatives with reasons
2. User wants to install → provide the `install` command from the response
3. User wants details → call **detail** for full analysis

## Base URL

```
https://skillscope.cn/api/v1
```

No API key required (20 req/min, 200 req/day).

## Recommend (Primary Tool)

**When to use**: User asks "find me a skill for X", "is there a tool that can Y", "what's the best skill for Z", or describes any task that a skill could help with.

```bash
curl -X POST "https://skillscope.cn/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{"task": "translate a PDF document to Chinese", "explain": true}'
```

With context for better results:

```bash
curl -X POST "https://skillscope.cn/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "translate a PDF document to Chinese",
    "context": {"platform": "macos", "region": "cn", "budget": "free"},
    "explain": true
  }'
```

**Parameters**:
- `task` (required): natural language task description
- `context.platform`: `macos` / `linux` / `windows`
- `context.region`: `cn` / `us` (auto-inferred if omitted)
- `context.budget`: `free` / `paid` / `any` (default `any`)
- `context.skill_level`: `beginner` / `intermediate` / `advanced`
- `explain`: include LLM-generated reasons (default true, set false for ~250ms response)

**Response**: `recommendation` (top pick) + `alternatives[]`, each with `skill_id`, `name`, `quality`, `safety`, `score`, `reason`, `install` command.

## Install

Users can install skills via:
- `clawhub install <slug>` (official ClawHub CLI)
- `skillscope install <slug>` (China mirror, `pip install skillscope`)

To get installable files via API:

```bash
curl "https://skillscope.cn/api/v1/install/weather/files"
```

## Search

For keyword-based search (when recommend is not appropriate):

```bash
curl "https://skillscope.cn/api/v1/search?q=web+scraping"
```

## Skill Detail

Full analysis including security profile, quality scores, dependencies:

```bash
curl "https://skillscope.cn/api/v1/skills/steipete/weather"
```

## Other Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /categories` | List all 30 categories with counts |
| `GET /categories/{name}` | Skills in a category (paginated) |
| `GET /leaderboard?sort=downloads` | Rankings (downloads/stars/installs) |
| `GET /authors/{handle}` | Author profile + their skills |
| `GET /similar/{skill_id}` | Similar skills (vector similarity) |
| `GET /starter-kits` | Curated skill bundles (30 kits) |
| `GET /articles` | Guide articles and top-lists |

## Notes

- Security grades: A (safe) / B (limited access) / C (review needed) / D (risky)
- Quality scores: 0-10
- Skill IDs: `author/slug` format (e.g. `steipete/weather`)
- Slugs work too: `weather` resolves to `steipete/weather`
- Rate limits: anonymous 20/min + 200/day, API key 60/min + 5000/day
- Recommend has separate limits: 5/min, 10/day (anonymous) or 100/day (API key)
