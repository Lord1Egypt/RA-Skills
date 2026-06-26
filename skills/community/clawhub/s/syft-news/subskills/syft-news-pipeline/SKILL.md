---
name: syft-news-pipeline
description: Coordinate Syft-only personalized news workflows in Codex or Claude Code using only `syft following`, `syft top`, and `syft search`. Use when Codex needs to decide or run the right path for building profile artifacts, capturing durable guidance, drafting daily briefings, generating trunk-branch storyline trees, or backfilling an existing storyline without local Python pipelines, dashboard artifacts, or trace URLs.
---

# Syft News Pipeline

## Overview

Use this skill as the entry point for the Syft-only news workflow.
Route the request to the right sub-workflow, preserve shared editorial rules, and keep all final outputs publishable rather than debug-like.

Assume the user only has:

- `syft following`
- `syft top`
- `syft search`
- the current agent's reasoning ability

Do not assume local Python pipelines, dashboard exports, trace URLs, or richer internal data products unless the user explicitly provides them.

## Routing

Choose one route first.
If the request spans multiple stages, chain the routes in the order listed in [references/workflow-map.md](references/workflow-map.md).

1. Build or refresh a user profile.
Read [references/profile-summary.md](references/profile-summary.md).

2. Capture a durable preference or editorial rule.
Read [references/guidance-rulebook.md](references/guidance-rulebook.md).

3. Produce a personalized daily briefing.
Read [references/daily-briefing.md](references/daily-briefing.md).
If profile artifacts do not exist yet, build them first.

4. Build a storyline tree.
Read [references/storyline-tree.md](references/storyline-tree.md).
Prefer to start from a cleaned daily news pool or a finished briefing.

5. Backfill an existing storyline.
Read [references/storyline-backfill.md](references/storyline-backfill.md).
Preserve the existing trunk and branch identity unless the user explicitly asks for a reframe.

## Shared Rules

Apply these rules across every route:

1. Confirm `syft` is available before doing workflow work.
Run `syft status`.

2. Treat `syft following` as the declared-interest source of truth in Syft-only environments.
If you also have a profile summary or a confirmed rulebook, use them as interpretation layers rather than replacements for the following list.

3. Use the retrieval ladder in this order:
   1. global top
   2. topic top
   3. targeted search

When a clearly followed axis is thin, probe topic-local recall first with:
`syft top --topic-id <TOPIC_ID> --days <N> --limit 20 --rich`

Only widen beyond 20 when the first probe is still obviously thin after triage.
Do not jump from weak global coverage straight to broad search unless topic top is unavailable or still insufficient.

4. Build event-level reasoning, not article piles.
Deduplicate overlapping items, merge multilingual duplicates, and preserve factual anchors.

5. Judge importance relative to the interest world.
Macro importance usually comes from structural consequence.
Hobby, fandom, collector, and travel importance may come from local cadence, official releases, collaborations, exhibitions, destination updates, or experience windows.

6. Keep final outputs readable and user-facing.
Write final deliverables in Simplified Chinese unless the user asks otherwise.
Do not leak search queries, route labels, triage notes, or working shorthand into final-facing outputs.

7. Match voice to the lane.
Use restrained causal prose for macro and markets.
Use scene-aware prose for ACG and fandom lines.
Use enthusiast-aware prose for cameras and collector lines.
Use texture-aware editorial prose for travel and onsen lines.

8. Keep visible titles disciplined.
Trunk titles, branch titles, section titles, and headlines should read like publishable labels, not the model talking to itself.

## Output Families

Use these canonical directories when the workspace does not already have an established equivalent:

- `profiles/`
- `briefings/`
- `storylines/`

Prefer reusing an existing directory instead of creating a duplicate parallel structure.

## Reference Files

Read only the route you need plus [references/workflow-map.md](references/workflow-map.md) when orchestration decisions are unclear.

- [references/workflow-map.md](references/workflow-map.md)
- [references/profile-summary.md](references/profile-summary.md)
- [references/guidance-rulebook.md](references/guidance-rulebook.md)
- [references/daily-briefing.md](references/daily-briefing.md)
- [references/storyline-tree.md](references/storyline-tree.md)
- [references/storyline-backfill.md](references/storyline-backfill.md)
