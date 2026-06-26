---
name: user-layer
description: Use this skill when the user wants a UserLayer report for an App Store or Google Play app, including full analysis, polling, and follow-up questions grounded in real reviews. Trigger it for competitor review analysis, user pain point extraction, segment discovery, and opportunity validation tasks.
homepage: https://github.com/houyongsheng/userlayer
metadata:
  clawdbot:
    requires:
      env:
        - API_KEY
    primaryEnv: API_KEY
    optionalEnv:
      - LAUNCHBASE_API_URL
    files:
      - scripts/main.py
      - scripts/call_api.py
---

# UserLayer

UserLayer turns App Store and Google Play reviews into structured research outputs:

- pain points
- user segments
- market opportunities
- follow-up answers grounded in cited reviews

Use the bundled wrappers in `scripts/main.py`. Do not hand-roll raw HTTP requests when this skill is available.

## Use This Skill When

- The user gives you an App Store or Google Play URL and wants review-backed insights.
- The user wants to ask follow-up questions about a completed full analysis.

## Prerequisites

- `API_KEY` must be set to a valid UserLayer API key.
- `LAUNCHBASE_API_URL` is optional.
  Default: `https://lb-api.workflowhunt.com`

## Credentials and Host

- Primary credential: `API_KEY`
- Default API host: `https://lb-api.workflowhunt.com`
- `API_KEY` should be scoped only for UserLayer API access and treated as a paid production credential.

## Available Wrappers

- `analyze(app_url: str, max_reviews: int | None = None)`
- `check_status(analysis_id: str)`
- `query(pain_point_id: str, question: str)`

## Typical Flow

1. Call `analyze()` to start a full async run.
2. Poll with `check_status()` until the report is complete.
3. Read the returned `pain_points`.
4. Use a `pain_point.id` with `query()` for targeted follow-up questions.

You do not need a separate preview step. `analyze()` is the main public entry point.

## Pricing Baseline

- One `analyze()` run costs `$2.99` and includes retrieval plus full analysis of the latest `100` reviews.
- If `max_reviews` is raised above `100`, extra reviews are billed as add-ons at `$0.01` per extra review.
- `query()` is billed at `$0.01 / 1K tokens`.

## Key Response Shapes

- `analyze()` starts an async job and returns a lightweight payload with:
  - `success`
  - `data.analysis_id`
  - `data.status`
- `check_status()` returns the full completed report when ready, including:
  - `data.pain_points`
  - `data.user_segments`
  - `data.opportunities`
  - `sources`
  - `usage`
- `query()` returns a follow-up answer for a specific pain point, including:
  - `data.answer`
  - `data.confidence`
  - `sources`
  - `usage`

Treat `pain_points[].id` from a completed analysis as the required input for `query()`.

## Operating Rules

- Default review count is `100` latest reviews.
- `analyze()` includes retrieval and analysis of `100` latest reviews by default.
- If `max_reviews` is raised above `100`, extra reviews are billed as add-ons.
- `analyze()` is asynchronous and returns an `analysis_id`; poll with `check_status()`.
- Use `query()` only after a completed full analysis returns a valid `pain_point_id`.
- Treat `sources` and cited review evidence as the source of truth.
- If `DATA_INDEX_NOT_FOUND` is returned, rerun a full analysis before querying again.
