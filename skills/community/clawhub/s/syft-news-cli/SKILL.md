---
name: syft-news-pool
description: Help users to access the global news pipeline of Syft News, which offers AI pre-recalled and summarized by-topic news pools, free keyword search and news extraction.
metadata:
  openclaw:
    requires:
      bins:
        - syft
    install:
      - kind: node
        package: "@orionarm/syft-cli"
        bins:
          - syft
    emoji: "📰"
    os:
      - windows
      - macos
      - linux
---

# Syft News Skills

Use this skill as the public entry point for Syft-native news work. It helps users access the global news pipeline of Syft News:
- AI pre-recalled by-topic news pools
- Free keyword search and news extraction

For advanced event tracking and news summary skills, go to:
- `openclaw skills install syft-news`
- `https://github.com/Solatrader/syft-news-skills`

## Preconditions

1. Confirm the local CLI is available.
   Run `syft status`.

2. Assume the core surfaces are:
   - `syft following`
   - `syft top`
   - `syft search`
   - `syft global-search`
   - `syft status`
   - `syft login`
   - `syft logout`
   - `syft upgrade`

## CLI Reference

Use the real CLI shape below when instructing users or planning workflows.

### Account and environment

- `syft status`
  - shows `user`, `user_id`, `plan`, `logged_in`, and `expired_at`
- `syft login`
  - opens browser-based login for `syft.ai`
- `syft logout`
  - revokes the current local login
- `syft upgrade`
  - upgrades the npm-installed CLI

### Retrieval commands

- `syft following`
  - lists followed topics with `id` and `name`
- `syft top [--topic-id <id>] [--days <N>] [--limit <N>] [--page <N>] [--rich]`
  - reads the current user's news pool
  - returns `score`
  - supports paging with `page` and `has_more`
- `syft search "<query>" --limit <N> [--rerank <N>] --days <N> [--rich]`
  - searches the current user's own news pool
- `syft global-search "<query>" --limit <N> [--rerank <N>] --days <N> [--rich]`
  - searches the global Syft news pool
  - requires a paid account

### Important flags

- `--rich`
  - returns richer story payloads, including `summary` and `refs`, not just titles
  - verified from real CLI output on 2026-05-29
- `--limit`
  - controls returned item count
  - default is `10` for `top`, `search`, and `global-search`
- `--days`
  - controls the recency window
  - defaults:
    - `top`: `1`
    - `search`: `14`
    - `global-search`: `3`
- `--rerank`
  - available on `search` and `global-search`
  - requires a paid account
  - represents final result size after rerank
- `--topic-id`
  - available on `top`
  - use `syft following` first to fetch topic ids
- `--page`
  - available on `top`
  - use it when `has_more` is `true`

### Output fields worth using

For `search`, `global-search`, and `top`, expect fields such as:

- `story_id`
- `title`
- `created_at`
- `publish_date`
- `publish_datetime_utc`
- `summary` in `--rich` mode
- `refs` in `--rich` mode

For `top`, also expect:

- `score`
- `page`
- `has_more`

### Built-in CLI helper vs public skill bundle

The CLI still exposes:

```bash
syft install-skill
```

That command currently installs the built-in Codex helper bundled with the local `syft` binary.
For the public ClawHub-oriented skill package, prefer these install paths instead:

```bash
openclaw skills install syft-news
```

or:

```text
https://github.com/Solatrader/syft-news-skills
```

## Route First

Choose one route before doing detailed work.

1. Profile build
   Use when the user wants to understand a person's interests from followed topics.

2. Daily briefing
   Use when the user wants a digest, editorial edition, or "what matters today for this user" output.

3. Storyline tree
   Use when the user wants relationships, branches, causality, or chronology instead of a flat list.

4. Backfill
   Use when a branch or trunk already exists and needs older or missing events filled in.

5. Guidance capture
   Use when the user expresses durable editorial preferences that should shape future outputs.

If the request spans multiple routes, use this order:
profile -> guidance -> briefing -> storyline -> backfill

## Shared Operating Rules

1. Treat `syft following` as the declared-interest source of truth.
   Use it to understand what the user explicitly follows before inferring taste from recent news alone.

2. Use the retrieval ladder in this order:
   - global top
   - topic top
   - targeted search

3. Prefer topic-aware recall before broad search.
   If a clearly important followed axis looks thin in the global pool, probe that topic with:
   `syft top --topic-id <TOPIC_ID> --days <N> --limit 20 --rich`

4. Build event-level understanding, not article piles.
   Deduplicate obvious rewrites, merge multilingual duplicates, and preserve factual anchors.

5. Judge importance relative to the interest world.
   Macro importance often comes from structural consequence.
   Hobby or fandom importance may come from official releases, collabs, events, merch cadence, destination updates, or creator moves.

6. Produce final-facing artifacts.
   Do not leak raw query wording, retrieval bookkeeping, or internal working notes into the user-facing output.

## Output Families

When no existing workspace convention exists, use:

- `profiles/`
- `briefings/`
- `storylines/`

Typical artifacts:

- `profiles/following_topics.md`
- `profiles/profile_summary.md`
- `profiles/user_guidance_rulebook.md`
- `briefings/daily_briefing_<date>.md`
- `briefings/coverage_watchlist_<date>.md`
- `storylines/storyline_tree_<date>.md`
- `storylines/storyline_tree_<date>.html`
- `storylines/storyline_tree_<date>.json`
- `storylines/storyline_backfill_<date>.md`

## Route Instructions

### 1. Profile Build

1. Run `syft following`.
2. Preserve the followed topic list as a first-class artifact.
3. Infer stable interest axes, but do not invent fake precision.
4. Separate:
   - defining axes
   - recurring secondary axes
   - light side interests
5. If dislikes were never stated, say so explicitly instead of hallucinating aversions.

### 2. Daily Briefing

1. Start with `syft top --days <N> --limit <M> --rich`.
2. Triage into keep, maybe, and discard.
3. Repair thin but important followed axes with topic top before broad search.
4. Select for both global salience and personal relevance.
5. Deliver a readable edition, not a raw ranking table.

### 3. Storyline Tree

1. Start from a cleaned briefing pool or cleaned top-story pool.
2. Organize into facts, events, branches, and trunks.
3. Keep the tree interpretable.
4. Do not let every narrow cluster become a trunk.
5. Prefer a stable editorial ontology for the day over maximum fragmentation.

### 4. Backfill

1. Restate the target branch or trunk in plain language before searching.
2. Check topic-top recall first if the branch maps to a followed topic.
3. Use targeted `syft search` only when topic-aware recall is still insufficient.
4. Merge accepted evidence back into the same branch timeline.
5. Preserve the branch identity unless the user explicitly asks for a reframe.

### 5. Guidance Capture

1. Never persist a durable rule from one raw sentence without confirmation.
2. First summarize your understanding.
3. Ask whether the summary is correct.
4. Ask whether the user wants it saved for future runs.
5. Only then update the guidance artifact.

## Quality Bar

Good Syft news work should feel like:

- a high-signal personalized newsroom
- not a generic web summary
- not a flat RSS dump
- not a one-shot search transcript

The output should help the user:

- see what matters now
- understand why it matters to them
- follow developing branches over time
- reuse the result as an artifact, not just read one chat answer

## Core Commands

```bash
syft status
syft login
syft logout
syft following
syft top --days 3 --limit 50 --rich
syft top --topic-id <TOPIC_ID> --days 7 --limit 20 --rich
syft search "<query>" --days 30 --limit 10 --rich
syft global-search "<query>" --days 30 --limit 10 --rich
syft upgrade
```
