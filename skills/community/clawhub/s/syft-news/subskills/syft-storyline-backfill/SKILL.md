---
name: syft-storyline-backfill
description: Use when the user wants to extend an existing storyline trunk or branch with Syft search results across a time window in Codex or Claude Code without local Python scripts. Also use when the user asks to backfill a branch timeline, repair a thin storyline, derive keyword strategies, merge known events with search evidence on one timeline, or extend hobby-interest logic lines such as IP merch cadence or onsen destination updates.
---

# Syft Storyline Backfill

Use this skill after a storyline tree already exists and the user wants one branch, one trunk, or the full tree extended with older or missing events.

## Inputs

Prefer to have:

- an existing storyline tree markdown file
- optional html or notes version of the same tree
- `profiles/following_topics.md`
- `profiles/profile_summary.md`
- optional guidance rules

## What this skill produces

Create:

- `storylines/storyline_backfill_<date>.md`
- optionally an updated storyline tree markdown file
- optionally an updated storyline tree html file
- optionally an updated storyline tree json file
- optionally `storylines/backfill_keyword_strategy_<date>.md`

Important:

- `storyline_backfill_<date>.md` is a working-facing explanation artifact
- the updated storyline tree files are user-facing final artifacts

Do not confuse the two.
Working-note language is acceptable in the backfill memo.
It is not acceptable in the final tree outputs.

## Workflow

1. Choose the target.
   The user may specify:
   - one branch
   - one trunk
   - all branches

2. Restate the target meaning in one sentence before searching.
   Do not search from labels alone.
   If the branch is a hobby or travel line, restate the branch logic precisely.

   Examples:
   - not just `Fate`
   - but `Fate official merch / collab / event cadence`

   - not just `Japanese onsen`
   - but `high-quality scenic ryokan / seasonal opening / local cuisine line`

3. Use the retrieval ladder.
   Before broad search, check whether the branch maps to a followed topic id.
   Default order:

   1. existing known events
   2. topic top via `syft top --topic-id <TOPIC_ID> --days <N> --limit 20 --rich`
   3. targeted `syft search`

   Topic top should be the normal second step because it often returns higher-quality branch-local material than free-text search.
   Start with `limit 20`.
   In most branches, the first 20 topic-local items are enough to show whether the branch can be filled cleanly.
   Only widen the limit if the branch remains obviously thin after triage.

   Use search when:
   - the branch spans multiple topics
   - the topic top is still thin
   - the branch logic is narrower than the topic title

4. Generate 3 to 6 query angles only when search is still needed.
   Use:
   - main actors
   - causal mechanism
   - market or policy consequence
   - geographic theater
   - domain jargon
   - fandom or collector cadence terms where relevant

5. Run `syft search "<query>" --days <N> --limit <M> --rich`.
   Use multiple small queries rather than one overloaded query.

6. Triage results into:
   - primary evidence
   - secondary evidence
   - discard

7. Merge accepted topic-top and search results into the same branch timeline as known events.
   Do not create a separate extension pane.

8. Sort the merged timeline chronologically.

9. Preserve the existing tree identity unless the user explicitly asks for a reframe.
   Backfill should usually enrich the existing trunks and branches, not invent a new ontology.

## Primary vs secondary evidence

Primary evidence:

- directly advances the branch storyline
- adds a missing step in the time chain
- sharpens causality or escalation
- for hobby branches, may represent a locally important official release, collab, event, or merch step inside that IP or collector world

Secondary evidence:

- does not advance the core chain directly
- but helps explain spillover, validation, or outer context

Discard:

- same domain but wrong storyline
- generic commentary without event value
- noisy duplicates

## Query design rules

- For macro branches, include actors plus mechanism.
- For semiconductor branches, include supply, policy, and market phrases.
- For ACG branches, include IP, event, creator, merch, collab, cafe, exhibition, campaign, and official store language.
- For photography branches, include product line, rumored body or lens names, and release language.
- For travel or onsen branches, include place name, ryokan / hotel / onsen terms, seasonality, scenery, food, promotion, reopening, and local experience words.

## Importance rule

Do not filter only by mainstream importance.

- For macro branches, ask whether the result advances the structural chain.
- For hobby branches, ask whether the result would be seen as a meaningful update inside that interest world.

Examples:

- an EVA official collab drop can be primary evidence on an EVA merch branch
- a Fate exhibition or campaign launch can be primary evidence on a Fate release branch
- a new onsen plan or scenic ryokan promotion can be primary evidence on a destination-experience branch if that is the branch logic

## Voice rule

When you summarize the extended branch, match the lane:

- macro: analytical and causal
- ACG: scene-aware and cadence-aware
- photography: enthusiast and collector aware
- travel: experiential and local-texture aware

Do not summarize a fandom branch in dry institutional language if that would sound alien to the people who actually care about it.

## Backfill boundary rule

This skill extends an existing tree.
It should not casually rewrite the editorial taxonomy.

Default behavior:

- keep existing trunk ids
- keep existing branch ids
- keep existing trunk and branch names unless the original names are clearly bad
- enrich timelines
- upgrade thin orphan highlights only when the new evidence is truly strong enough

Do not turn a backfill run into a brand-new classification exercise unless the user explicitly asks for that.

## Failure modes to avoid

- adding many search hits that do not deepen the branch
- letting secondary evidence drown out the main chain
- leaving known and extended events in separate panes
- forgetting chronological sorting
- assuming hobby branches need war-or-macro style causality before they can be extended
- skipping topic top even when a clean followed topic id exists
- widening topic top too early instead of probing with the first 20 items
- using the backfill memo tone inside the final HTML or markdown tree
- rebuilding the whole tree into a noisier structure during full-tree backfill
- exposing route labels like `topic top 路` or `targeted search 路` in user-facing output

## Reference files

Read:

- `references/keyword-strategy.md`
- `references/merge-template.md`
- `../syft-storyline-tree/references/render-template.md`
