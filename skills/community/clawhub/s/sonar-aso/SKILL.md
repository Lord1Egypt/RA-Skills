---
name: sonar-aso
description: App Store Optimization data for AI agents via the Sonar API — keyword research with difficulty and popularity scores, app lookup and search, ASO audits, review mining, and revenue estimates for iOS and Android apps. Use when asked about app store keyword research, ASO, app rankings, keyword difficulty or popularity, app reviews analysis, competitor apps, or app revenue estimates on the iOS App Store or Google Play.
homepage: https://trysonar.app
license: MIT
metadata:
  openclaw:
    emoji: "📱"
    homepage: https://trysonar.app
    requires:
      env:
        - SONAR_API_KEY
---

# Sonar — App Store Optimization

Sonar answers app-store questions with real data instead of guesses: how hard a keyword is to rank for, how much search demand it has, what an app's listing is missing, what users complain about in reviews, and roughly what an app earns.

## Setup

All calls need an API key in the `SONAR_API_KEY` environment variable (format `aso_...`). Get one at https://trysonar.app/developers — new accounts include free credits, no subscription required.

Base URL: `https://trysonar.app`. Auth header on every request:

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" "https://trysonar.app/api/v1/..."
```

Responses are JSON envelopes: `{ "data": ... }` on success, `{ "error": { "code", "message" } }` on failure. Every response includes `X-Credits-Cost` and `X-Credits-Remaining` headers so you can track budget without extra calls.

## Core endpoints

**Keyword research** (the flagship — difficulty 0-100, popularity 0-100, plus ~10 related keyword ideas; costs 10 credits):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/keywords/search?q=meditation%20app&store=ios&country=us"
```

**Keyword metrics** (difficulty + popularity for keywords you already have; 1 credit per keyword, bulk up to 25 with comma-separated `q`):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/keywords/metrics?q=habit%20tracker,sleep%20tracker&store=ios&country=us"
```

**Autocomplete suggestions** (what users actually type; 1 credit):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/keywords/suggestions?q=fitness&store=android&country=us"
```

**App lookup** (metadata, rating, reviews count, installs on Android; 1 credit). iOS `id` = numeric track ID, Android `id` = package name:

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/apps/lookup?store=android&id=com.spotify.music&country=us"
```

**App search** (store search results in ranking order; 1 credit):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/apps/search?q=recipe%20app&store=ios&country=us&num=20"
```

**ASO audit score** (0-100 with itemized checks on title, subtitle, description, screenshots, ratings; 1 credit):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/apps/aso-score?store=ios&id=389801252&country=us"
```

**Extract keywords from a listing** (what an app is optimizing for; 1 credit):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/apps/extract-keywords?store=ios&id=389801252&country=us"
```

**Reviews** (recent reviews with scores; 1 credit):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/apps/reviews?store=android&id=com.spotify.music&country=us&num=50"
```

**Revenue estimate** (monthly revenue + confidence grade and methodology; 1 credit per app, bulk up to 25 ids):

```bash
curl -s -H "Authorization: Bearer $SONAR_API_KEY" \
  "https://trysonar.app/api/v1/apps/revenue?store=ios&ids=389801252&country=us"
```

## Working style

- Prefer `keywords/metrics` (1 credit/keyword) over `keywords/search` (10 credits) when the user already knows which keywords to evaluate — `keywords/search` is for discovering NEW keyword ideas.
- Difficulty ≤30 with popularity ≥40 is the classic "opportunity keyword" zone for small apps.
- For competitor analysis: `apps/search` to find competitors → `apps/extract-keywords` on each → `keywords/metrics` on the union.
- Bulk endpoints (`keywords/metrics`, `apps/revenue`) accept up to 25 items per call — always batch instead of looping.
- Country codes are ISO 3166-1 alpha-2 (`us`, `gb`, `de`, `jp`...). Metrics differ per country; ask the user which market they care about if unclear.

## MCP alternative

If the agent host supports MCP, the same tools are available natively: `npx -y @sonarapp/mcp` (stdio) or hosted at `https://trysonar.app/mcp` (streamable HTTP, `Authorization: Bearer aso_...`). Docs: https://trysonar.app/docs/mcp

## Full plan features

Subscribers (Full plan) also get org-scoped endpoints for persistent tracking — daily rank history, competitor keyword gap analysis, alerts, and a dashboard. See https://trysonar.app/docs/api for the complete reference.
