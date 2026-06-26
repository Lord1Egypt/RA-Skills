---
name: syft-storyline-tree
description: Use when the user wants to turn Syft CLI news into a trunk-branch storyline tree, attach timelines, render markdown plus html plus json outputs, or prepare branches for later Syft search extension in Codex or Claude Code without local Python scripts. Also use when the user asks for event trees, storyline timelines, branch relationship mapping, hobby-interest logic lines, or a relationship-first reading view.
---

# Syft Storyline Tree

Use this skill when the user wants a relationship-first view instead of a flat news list.

## Inputs

Prefer to have one of:

- an aggregated daily news pool
- a finished daily briefing
- both

Also load:

- `profiles/profile_summary.md`
- `profiles/following_topics.md`
- optional confirmed guidance rules
- optional heuristic `profiles/raw_interest_block.txt` if one was derived from follows

## What this skill produces

Create:

- `storylines/storyline_tree_<date>.md`
- `storylines/storyline_tree_<date>.html`
- `storylines/storyline_tree_<date>.json`
- optionally `storylines/storyline_notes_<date>.md`

These are final-facing deliverables, not rough drafts.
The visible outputs should read like editorial products a real user can browse directly.
Do not leak retrieval bookkeeping, query wording, internal route notes, or draft-stage shorthand into the final prose.

## Core model

Do not flatten everything into one list.
Organize information into:

1. facts
2. events
3. branches
4. trunks

Each trunk should explain one structural storyline.
Each branch should represent one interpretable angle attached to that trunk, such as:

- structural driver
- market validation
- policy or military signal
- personal-interest side branch
- cultural or community branch
- merch / collab / official release branch
- destination / seasonal-experience branch

## Build order

1. Identify 3 to 8 candidate trunks from the cleaned pool.
2. Test whether each candidate really deserves trunk status.
3. Only then create branches.
4. Only after the tree is coherent should you consider extra topic-top or search-based extension.

Do not start by creating many branches and hoping a trunk appears later.

## Tree identity rule

The tree is not a bag of interesting topics.
It is a stable editorial ontology for this user's day.

That means:

- do not let every search hit create a new trunk
- do not re-taxonomize the whole tree just because one narrow cluster became temporarily dense
- do not replace a high-quality existing trunk structure with a noisier and more fragmented one unless the evidence clearly demands a regime shift

When in doubt:

- keep the strongest 4 to 8 trunks
- keep branch logic interpretable
- move thin or narrow but relevant material into watchlists or orphan highlights

The goal is not maximum coverage at trunk level.
The goal is maximum clarity without losing on-profile material.

## Retrieval ladder

Use this evidence order when the cleaned global pool is not enough:

1. global top
2. topic top
3. targeted search

Topic top should be treated as a normal extension layer, not a rare exception.
If a branch is clearly declared by the user's follow list but thin in the global top pool, use the topic id from `syft following` and pull:

- `syft top --topic-id <TOPIC_ID> --days <N> --limit 20 --rich`

Start with `limit 20`.
That is the default probe size.
For most topics, 20 items are enough to reveal whether the branch has real event density.
Only expand past 20 if the branch still feels clearly under-filled after deduping and clustering.

Use topic top especially for:

- explicit niche follows
- ACG lines
- collector / camera lines
- travel / onsen lines
- narrower macro or sector lines that the platform-wide top may underweight

Only after topic top still leaves a real gap should you move to `syft search`.

## Trunk admission rule

A trunk usually needs at least two of the following:

- structural consequence beyond one actor
- multi-event continuity
- clear causal chain
- strong match to the user's declared macro or identity interests
- ability to support more than one meaningful branch

If a topic is interesting but too thin, keep it as a branch or a supplement note, not a trunk.
If it still clearly matters inside one followed interest world, keep it visible somewhere in the final outputs.

## Hobby and culture rule

When you need to decide whether a smaller hobby or community line deserves its own branch or trunk, use:

- `following_topics.md` to confirm that the user explicitly followed that area
- `profile_summary.md` to judge how identity-defining that area likely is

For hobby lines:

- do not merge unrelated IPs
- do not merge different collector logics
- do not merge travel with ACG just because both are soft interests
- if Fate, EVA, photography, and Japan travel are all separately meaningful, keep them separate

Also allow hobby branches that are organized by recurring logic line rather than one giant singular event.
Examples:

- EVA official merch / collab cadence
- Fate licensed releases / exhibitions / campaign rhythm
- camera body rumor -> tease -> launch -> review chain
- onsen / ryokan seasonal opening -> promotion -> experience update

Do not require every hobby branch to mimic a geopolitical cause-effect chain.

## Role-aware branch handling

Different trunks need different editorial eyes.

- macro / geopolitics / finance:
  focus on causality, regime stress, market repricing, supply-chain propagation
- semiconductor / AI industry:
  focus on demand, supply, policy, valuation, ecosystem shifts
- ACG:
  respect IP boundaries, fandom logic, event cadence, creator or merch context
  treat collabs, official goods, exhibitions, cafes, concerts, and campaign cycles as valid branch logic when they matter inside that fandom
  the prose should feel scene-aware rather than institutional
- photography:
  focus on product line, rumor credibility, lens rarity, market behavior
  the prose should sound like an informed enthusiast or collector summary
- travel:
  focus on destination character, seasonality, experience quality, local texture
  treat local promotions, scenic windows, food-view combinations, and ryokan / onsen openings as valid branch logic when they are on-profile
  the prose should feel like editorial travel curation, not macro commentary

Do not treat hobby lines with the same coarse lens you would use for macro news.
Also do not let the high-level profile summary wash out niche followed interests that the user explicitly chose.

## Naming rule

Trunk titles and branch titles must read like names, not like commentary.

Good trunk titles:

- `EVA 30 周年商品与内容热度延续`
- `FGO 新章预热与 Fate 周边节奏`
- `初夏温泉旅宿上新`

Bad trunk titles:

- `EVA 30 周年这一波还在接力，不是零散周边，是整套热度延长线`
- `T1. ACG 与二创生态：授权、AI 生成、同人流通同时加速`

The title should be:

- concise
- name-like
- stable enough to act as an index label
- usually a noun phrase, not a full self-explanatory sentence

Put the interpretation, emphasis, and editorial color into:

- `why this trunk matters`
- `summary`
- `rationale`

Do not stuff those functions into the title itself.
Do not append process labels like `路`, `axis`, `lane`, `query`, `topic_top`, or `search` to user-facing titles.

## Timeline rule

Known events and later topic-top / search-extended events belong on one merged timeline.
Differentiate by label or color if rendering HTML, but do not split them into separate reading panes.

Always sort timelines chronologically.

Timeline item writing should be natural Chinese.
Do not write in stiff translationese or note-taking fragments.

Weak:

- `《序》CGI 制作秘话再被翻出来讲`

Better:

- `《序》的CG制作内幕再度成为周年讨论焦点`
- `《序》幕后制作往事又被周年节目重新带热`

Prefer:

- complete and readable Chinese
- natural word order
- no half-translated oral filler
- no model self-talk phrasing
- no process-note phrasing
- no bullet-dump shorthand pretending to be prose
- no machine-stitched mixed registers inside one sentence

Do not write things like:

- `T1-B2 路 ...`
- `topic top 路`
- `targeted search 路`
- `thin: ...`
- `discard_note`

Those may exist in working notes, but never in the final-facing tree copy.

## Coverage completeness rule

The tree should not only show what chained cleanly.
It should also make visible what was clearly relevant but remained thin.

Use one of these fallback placements when needed:

- a small branch under the right trunk
- an `interest_watch` appendix in markdown
- an `orphan_interest_highlights` block in JSON

Do not silently drop a clearly on-profile EVA / Fate / camera / onsen item just because it lacks mainstream importance.

## Importance rule

Importance is relative to the branch world.

- For macro branches, importance usually comes from structural consequence.
- For hobby branches, importance may come from local salience inside that fandom, product line, collector market, or travel niche.

Examples:

- an EVA collaboration launch can be high-importance for an EVA branch
- a Fate official merch wave can be core evidence for a Fate branch
- a ryokan seasonal reopening can be meaningful on a Japan onsen branch

## Syft-only input rule

In this environment, there is usually no original scored interest list.
Treat inputs with this order of authority:

1. `following_topics.md`
2. `profile_summary.md`
3. confirmed guidance rules
4. optional heuristic `raw_interest_block.txt`

If these sources disagree, prefer the following list for declared taste boundaries and the profile summary for interpretation.

## Failure modes to avoid

- turning one big storyline into many shallow trunks
- forcing many unrelated hobby lines under one soft-interest umbrella
- creating trunks from one-off weak stories
- presenting support evidence out of chronological order
- suppressing interest-world-important hobby events because they are globally small
- skipping topic top and jumping straight from a weak global pool to broad search
- opening topic top with oversized limits before checking whether the first 20 already solve the branch
- writing ACG, photography, or travel branches in the same cold style as Fed or war branches
- using commentary-like full sentences as trunk names
- writing unnatural Chinese such as note fragments, translationese, or self-talk phrasing
- exposing route labels or retrieval jargon in user-facing prose
- producing a generic debug-style HTML page when a polished editorial card page is expected

## Rendering

Read `references/render-template.md`.
Prefer:

- a clean markdown tree for portability
- a local HTML view for visual inspection
- a structured JSON view for later merging, backfill, or rendering

The HTML should follow one canonical visual family:

- warm editorial card layout
- one hero block
- trunk cards
- branch cards
- one merged timeline per branch
- one compact appendix area for interest-side material

Do not fall back to a plain admin dashboard or generic debug page unless the user explicitly asks for a utilitarian debug render.

## Final quality gate

Before you finalize, run a manual quality pass against the visible outputs.

Check all of these:

1. trunk titles read like names, not explanations
2. branch titles read like labels, not notes to self
3. no route labels or process jargon leak into the visible content
4. timelines are chronologically sorted
5. HTML has no broken tags or obviously malformed structure
6. Chinese reads naturally in at least:
   - hero title
   - all trunk titles
   - first sentence of each trunk summary
   - first timeline item of each branch
7. visible Chinese is not garbled; if the HTML renders mojibake, fix encoding or re-save as UTF-8 before delivering
8. hobby trunks sound like they belong to their subculture
9. thin but relevant interests are visible somewhere, not silently dropped

If any of these fail, revise before delivering.

If the user wants deeper timeline completion, use `syft-storyline-backfill`.
