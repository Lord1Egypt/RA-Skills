---
name: syft-daily-briefing
description: Use when the user wants a personalized daily news briefing from Syft CLI following topics in Codex or Claude Code without relying on local Python scripts. Also use when the user wants a profile-aware editorial edition, issue clustering, mainline plus supplement structure, stronger interest coverage, or a richer daily briefing from `syft top`.
---

# Syft Daily Briefing

Use this skill when the user wants a daily briefing generated directly from Syft CLI plus the agent's own model.

## Inputs

Prefer to have these available first:

- `profiles/following_topics.md`
- `profiles/profile_summary.md`
- optional `profiles/user_guidance_rulebook.md` or another confirmed guidance file
- optional `profiles/raw_interest_block.txt` if the profile skill generated a heuristic interest map
- optional explicit aversion notes if the user has provided them later

If they do not exist yet, suggest running `syft-profile-summary` first.

## What this skill produces

Create:

- `briefings/daily_briefing_<date>.md`
- `briefings/coverage_watchlist_<date>.md`
- optionally `briefings/raw_news_pool_<date>.md`
- optionally `briefings/aggregated_news_pool_<date>.md`
- optionally `briefings/editorial_notes_<date>.md`

## Workflow

1. Check Syft availability.
   Run `syft status`.

2. Read following topics with ids.
   Run `syft following`.
   Preserve both:
   - the topic title
   - the topic id

   Topic ids matter because they are the bridge from a user's declared interest list to `syft top --topic-id`.

3. Pull a first-pass global pool.
   Start with:
   - `syft top --days <N> --limit <M> --rich`

4. Do pool triage before writing anything.
   Split results into:
   - `keep`: structurally important or clearly high-match
   - `maybe`: potentially useful but not yet clear
   - `discard`: promo, coupon, generic shopping, shallow affiliate content, obvious noise

5. Normalize multilingual titles before selection.
   If titles are in multiple languages, first translate or paraphrase them into one working language for your own reasoning.
   Do not let language fragmentation hide a strong event cluster.

6. Build an event-level pool, not an article pile.
   Merge duplicates when they describe the same event, actor move, or causal development.
   Preserve factual anchors during the merge.

7. Build an interest coverage map before final selection.
   Use `following_topics.md` plus `profile_summary.md` to list:
   - main structural axes
   - identity-defining hobby / culture axes
   - thin but still important side interests

   For each axis, ask:
   - is there a strong chainable storyline
   - is there at least one high-salience item even if it does not chain well
   - is the pool empty, weak, or noisy

8. Repair obvious coverage gaps with topic top before broad search.
   Use this retrieval ladder by default:

   1. global top
   2. topic top
   3. targeted search

   If the first-pass global top pool is weak on a clearly important axis, do not jump straight to search.
   First use the topic id from `syft following` and pull:
   - `syft top --topic-id <TOPIC_ID> --days <N> --limit 20 --rich`

   Topic top is usually the most efficient second-pass repair because it already carries topic-aware recall.
   Start with `limit 20`.
   In most topics, the top 20 items already carry enough signal for editorial recovery.
   Only expand beyond 20 if:
   - the line is still clearly thin
   - the returned 20 are dominated by duplicates or low-value items
   - the topic is known to have a dense event cadence and still needs more chronology

   Use it for:
   - explicitly followed niche interests
   - hobby lines that global top often misses
   - narrower structural lines that matter to this user but not to the whole platform

   Only after global top plus topic top still leave a real gap should you add 2 to 5 targeted `syft search` queries.
   Search is the third layer, not the default second layer.

9. Select for editorial value with profile awareness.
   In Syft-only environments, use these layers in priority order:
   - following topics as the canonical declared-interest source
   - profile summary as the high-level interpretive lens
   - confirmed guidance rules
   - optional heuristic `raw_interest_block.txt`
   - optional explicit aversion notes, only if the user later supplied them

   Do not assume you have user-authored scores. Most of the time you will not.

10. Judge importance relative to the interest domain, not only by universal news value.
    For macro, finance, geopolitics, and war:
    - importance usually comes from structural consequence, causality, repricing, or regime stress

    For hobby, fandom, collecting, and travel:
    - importance may come from local cadence inside that interest world
    - official collab drops
    - merch or peripheral releases
    - exhibition or event announcements
    - creator statements
    - store / pop-up / cafe / campaign cycles
    - seasonal ryokan / onsen / local experience openings or promotions

    Example:
    - a new EVA collab may be globally minor but highly important inside EVA fandom
    - a Fate merch release can be a real event if the line being watched is official content cadence

11. Match prose voice to the lane.
    Do not write every line in the same analytical register.

    Use:
    - macro / market / geopolitics:
      restrained, causal, analytical, briefing-like
    - ACG / fandom:
      more scene-aware and community-native
      allowed to sound warmer, more release- and cadence-sensitive, less like a policy memo
    - photography:
      enthusiast-facing, concrete, product- and collector-aware
    - travel / onsen:
      texture-rich, experience-aware, less boardroom-analytical

    Example:
    - weak: `GU 联名说明 EVA 仍在向大流通服饰端扩散`
    - better: `EVA 这轮已经不只是零星周边，而是连 GU 和伊势丹线都在接力，30 周年的商业联动热度明显还在往上走`

    The goal is not roleplay or slang overload.
    The goal is that each lane sounds like it was written by someone who actually knows that audience.

12. Keep titles disciplined.
    Headlines should look like publishable titles or section names, not like the model talking to itself.

    Avoid:
    - overlong explanation jammed into the title
    - sentence fragments that sound like live note-taking
    - staged phrasing that sounds like commentary rather than editing

13. Write natural Chinese.
    The body must read like edited Chinese prose.

    Avoid:
    - translationese
    - awkward oral filler
    - shorthand note fragments

    Example:
    - weak: `《序》CGI 制作秘话再被翻出来讲`
    - better: `《序》的CG制作内幕又被周年节目重新带热`

14. Separate the edition into:
    - `今日新闻池概览`
    - `主线`
    - `副刊 / 兴趣侧翼`
    - `兴趣雷达 / 未成线但值得看`
    - `本轮新闻池覆盖不足`

15. Keep bodies publishable.
    The article body must read like news briefing prose, not instructions to the user.
    Do not write things like `对你来说` or `你需要知道`.

## Editorial heuristics

- Major macro, geopolitical, and market-moving issues should usually appear in `主线`.
- Personal but identity-defining interests should still be deliberately represented in `副刊 / 兴趣侧翼`, not forgotten.
- If an interest hit is important inside its own micro-domain but too thin to support a dense writeup, surface it in `兴趣雷达 / 未成线但值得看` rather than hiding it.
- On one issue, prefer one denser item over many repetitive short items.
- If a quiet macro signal has structural downstream impact, it should surface naturally through the chain, not because of a hard-coded rule.
- When the only explicit declared-interest source is `following_topics.md`, use that file to make sure side-interests are not erased by the profile summary's main-axis abstraction.
- Distinguish between true hobby noise and domain-important hobby updates.
  A random coupon list is noise, but a new official Fate collaboration, EVA merchandise cycle, or ryokan seasonal opening may be a real hit.
- Topic top should be the normal middle layer between global top and search whenever an explicitly followed axis feels under-covered.

## Failure modes to avoid

- treating promo and affiliate content as real editorial candidates
- letting multilingual duplication fragment one big event into many weak-looking fragments
- over-indexing on the profile summary and accidentally dropping explicitly followed niche interests
- forcing all personal interests into one generic supplement section without respecting their own logic
- assuming hobby importance must pass a mainstream-news threshold before it can appear
- hiding unchained but clearly relevant interest hits just because they do not fit the mainline logic
- jumping from weak global top straight to broad search without trying topic top first
- blindly starting topic top with oversized limits when a `limit 20` probe would have been enough
- writing ACG or travel lines in the same flat institutional tone used for Fed or war coverage
- writing titles that sound like explanation blurts instead of edited headlines
- leaving behind unnatural Chinese such as translationese or note-fragment prose

## Prompt and output shape

Read:

- `references/editorial-prompt.md`
- `references/output-template.md`

Use them as scaffolding, but adapt the section logic to the specific user's profile.
