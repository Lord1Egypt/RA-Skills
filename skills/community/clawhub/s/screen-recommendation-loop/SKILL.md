---
name: screen-recommendation-loop
description: Build and run a low-friction movie/anime recommendation + follow-up loop. Use when a user wants long-term taste profiling from watched/unfinished/dropped feedback, mixed sources (e.g., Douban/Bangumi Top lists), random title-type selection, and automatic type-based follow-up timing.
---

# Screen Recommendation Loop

## Overview
Run an ongoing recommendation system that balances consistency and low user burden. Recommend one title at a time, collect short feedback, and adapt future picks from preference signals.

## Core Workflow

1. Pick one candidate title.
2. Send one concise recommendation message.
3. Schedule follow-up based on title type.
4. Collect status in a small fixed schema.
5. Update preference weights.
6. Pick the next title with constrained randomness.

Keep each interaction short. Prioritize adherence over perfect metadata.

If the user proactively returns before scheduled follow-up (e.g., "I watched it, let's discuss"), skip waiting and immediately:

1. run the review step,
2. record status,
3. start the next recommendation cycle.

## Recommendation Rules

- Use a mixed candidate pool (example: Douban Top 250 + Bangumi Top 250).
- Select title type randomly (not strict alternation):
  - allow movie → movie
  - allow anime → anime
- Apply hard filters before scoring:
  - already completed recently
  - explicitly rejected/dropped for same strong pattern
  - duplicate title aliases
- Use constrained random ranking:
  - exploit known preferences (higher weight)
  - retain exploration quota (e.g., 15–25%) to avoid tunnel vision

## Follow-Up Timing Rules

Use automatic, content-type-based follow-up windows.

Default logic:

- Movie recommendation: follow up at `recommendedAt + 7 days`
- Anime/series recommendation: follow up at `recommendedAt + 30 days`

No manual per-user interval configuration is required; infer from recommended content type.

When asking, send at a random time inside a normal activity window (for example 10:00–22:30 in the target timezone).

## Accepted User Statuses

Treat all as valid outcomes:

- watched (completed)
- partial (started but unfinished)
- not_started
- dropped_midway
- reject_this_title

Do not frame partial/dropped as failure. Use them as preference signals.

## Feedback Prompt Template

Use a tiny response format:

- status: watched / partial / not_started / dropped_midway / reject_this_title
- one-line feeling (optional)
- next mood (optional): brainy / healing / realistic / light

## Preference Update Heuristics

- watched: reinforce nearby tags and narrative patterns
- partial: slight penalty to pacing/length mismatch factors
- dropped_midway: strong negative weight to dominant disliked traits
- reject_this_title: title-level or trope-level block depending on reason
- not_started: no strong taste penalty; treat as scheduling signal

Decay old signals slowly to avoid overfitting to one week.

## Minimal Record Schema

Keep per-title state:

- id
- title
- type (movie|anime)
- source
- recommendedAt
- followupAt
- status
- tags (optional)
- note (optional, one-line user feedback)

This can live in JSON or SQLite.

## Safety and Privacy

- Never store private identifiers in the skill package.
- Keep the skill generic: no personal names, account IDs, chat IDs, tokens, local paths, or private schedules.
- If publishing, scrub sample data and examples before packaging.
