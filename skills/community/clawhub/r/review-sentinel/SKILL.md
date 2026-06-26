---
name: review-sentinel
description: Monitor, analyze, and respond to Google reviews for local businesses. Use when asked to check reviews, analyze review trends, draft review responses, generate reputation reports, or monitor a business's online reputation. Supports any business findable on Google Maps. Tracks review changes over time using local state files.
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_PLACES_API_KEY
    primaryEnv: GOOGLE_PLACES_API_KEY
---

# Review Sentinel

Automated Google review monitoring, analysis, and response drafting for any local business.

## What It Does

- **Fetches** current Google reviews and ratings via Google Places API
- **Tracks** rating/review count changes over time with local state files
- **Analyzes** sentiment, topics, and trends across reviews
- **Drafts** owner responses matched to review tone and business type
- **Generates** reputation reports with competitor comparison
- **Alerts** on new negative reviews (pair with a cron job for daily monitoring)

## Prerequisites

- Python 3.8+ (stdlib only — no pip installs)
- **Google Places API key** (required) — provide via one of:
  1. `GOOGLE_PLACES_API_KEY` environment variable (recommended)
  2. `credentials/google-places-api-key` file (relative to working directory)
  - Enable "Places API (New)" in Google Cloud Console
  - Free tier: $200/month credit (~5,000 searches)
- Fallback: web scraping scripts included but fragile

## Limitations

- Places API returns max 5 most relevant reviews per request (Google API limit)
- Web scraping fallback may break if Google changes their page structure
- No real-time alerts without a cron job configured
- Review response posting requires manual copy-paste (no API write access)

## Setup

On first use, ask the user for:
1. **Business name** and **location** (city or address)
2. **Google Maps Place ID** (optional — will search if not provided)

Store config in the skill directory at `review-sentinel/config.json`:
```json
{
  "businesses": [
    {
      "name": "Business Name",
      "placeId": "ChIJ...",
      "location": "City, State",
      "searchQuery": "Business Name City",
      "lastChecked": null,
      "reviewCount": 0,
      "rating": 0
    }
  ]
}
```

## Core Workflows

### 1. Check Reviews
Trigger: "check reviews", "how are our reviews", "any new reviews"

1. Run `scripts/fetch_reviews_places.py <search_query>` to fetch current review data via Google Places API (preferred)
   - Fallback: `scripts/fetch_reviews.py <search_query>` (web scraping, fragile)
2. Compare with stored state in `review-sentinel/state/<business-slug>.json`
3. Report: new reviews since last check, rating changes, review count changes
4. Update state file

### 2. Analyze Reviews
Trigger: "analyze reviews", "review trends", "what are people saying"

1. Fetch current reviews using the fetch script
2. Parse review text, ratings, dates
3. Categorize by sentiment and topic (service, wait time, staff, price, quality)
4. Identify patterns: recurring complaints, seasonal trends, rating trajectory
5. Compare against competitors if configured

### 3. Draft Responses
Trigger: "respond to reviews", "draft responses", "reply to reviews"

For each unresponded review:
- **5-star:** Thank specifically for what they praised, invite return
- **4-star:** Thank warmly, acknowledge any mild concern
- **3-star:** Thank, address specific concern, offer resolution
- **1-2 star:** Empathize, apologize without admitting fault, offer offline resolution, keep professional

Guidelines:
- Keep responses under 100 words
- Never be defensive or argumentative
- Reference specific details from the review (shows it was read by a human)
- Include business name naturally
- Vary templates — don't use identical responses

### 4. Reputation Report
Trigger: "reputation report", "review report", "monthly report"

Generate a structured report:
- Overall rating & trend (up/down/stable)
- Review velocity (reviews per week/month)
- Sentiment breakdown
- Top praised aspects
- Top complaints
- Competitor comparison (if configured)
- Recommended actions

Save reports to `review-sentinel/reports/YYYY-MM-DD-report.md`.

### 5. Review Alerts (Cron)
For automated monitoring, suggest the user set up a cron job:
```
Schedule: daily at 9 AM
Task: Check for new reviews, alert on any 1-2 star reviews immediately
```

## Response Tone Guide

Match response tone to the business type:
- **Medical/Professional:** Formal, empathetic, privacy-aware (never reference specific treatments/conditions)
- **Retail/Restaurant:** Warm, friendly, conversational
- **Service business:** Professional, solution-oriented

## Competitor Tracking

When configured with competitor businesses, the analysis workflow includes:
- Side-by-side rating comparison
- Review velocity comparison
- Sentiment gap analysis
- Competitive positioning summary

## State Management

All state stored in `review-sentinel/state/`:
- `<business-slug>.json` — latest review snapshot, history
- `config.json` — business configuration

Read `references/state-schema.md` for the full state file schema.

## Quickstart Example

```
User: "Check reviews for my clinic"
Agent: Runs fetch_reviews_places.py "My Clinic Seattle"
Agent: Compares with stored state, reports:
  - Rating: 4.6★ (stable)
  - 3 new reviews since last check (2 positive, 1 negative)
  - Alert: 1-star review from "Jane D." needs response
  - Drafts response for approval
```

## Important Notes

- Google review scraping is rate-limited. Don't run more than a few times per day per business.
- Review response drafts should ALWAYS be presented to the user for approval before posting.
- Never auto-post responses — always human-in-the-loop.
- For businesses with health privacy concerns (HIPAA/PIPEDA), never reference patient conditions in responses.
