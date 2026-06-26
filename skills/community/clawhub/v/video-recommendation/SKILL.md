---
name: video-recommendation
description: Recommend videos with precision, not addiction. Use when a user asks what to watch, wants video recommendations, wants a curated watchlist, wants direct video links, or wants suggestions based on recent chat instead of generic platform algorithms. Best for context-aware, taste-driven, non-feed-based video discovery. Supports: direct links, themed watchlists, project-aligned recommendations, mood-based picks, and bilingual curation.
---

# Video Recommendation

Recommend videos with precision, not addiction.

This skill is for users who want:
- recommendations based on live context, not addictive feeds
- discovery without endless scrolling
- direct links instead of vague search terms
- a curated shortlist, not an algorithmic trap

## Core promise

This skill should feel like the opposite of passive recommendation systems.

- **Not TikTok**: no captive loop, no infinite feed
- **Not default YouTube**: not subscription-first, not search-first, not popularity-first
- **Instead**: context-aware, taste-driven, and precise

The goal is to recommend the right videos for **this user, in this moment**, using recent chat, current projects, mood, and known interests.

## What this skill should optimize for

1. Relevance to the user's recent chat and known interests
2. Freshness of fit, not just popularity
3. Low-noise recommendations
4. Actionability: give direct links when possible
5. Intent alignment: fun, insight, inspiration, research, or creative fuel

## Trigger patterns

Use this skill when the user asks things like:
- what should I watch?
- recommend some videos
- give me 10 video links
- based on what we've been talking about, what should I watch?
- give me something fun but not dumb
- recommend videos for this project / topic / mood
- find videos I may be interested in
- suggest something interesting to watch tonight

## Default outputs

Choose one of these depending on the request:
- **Quick list**: 5-10 direct video links
- **Curated pack**: grouped by theme, each with a 1-line why
- **Tight shortlist**: top 3 only, when the user wants something immediately
- **Strategic set**: videos that match a project, product direction, or current obsession

## Workflow

### 1. Infer recommendation intent from recent chat

Determine:
- What is the user actually in the mood for?
- Are they looking for fun, depth, inspiration, practical learning, or background stimulation?
- Is the request broad or connected to a current project?

Use recent conversation as the primary signal.
If there is durable preference information in memory, use it.

### 2. Build an interest profile for this request

Summarize internally:
- current topics
- recurring interests
- energy level / mood if visible
- language preference
- desired content density
- whether the user wants specific links or categories

If needed, read `references/personalization.md`.

### 3. Select recommendation angles

Pick 2-4 angles, for example:
- frontier AI / future-of-humanity
- product and founder judgment
- AI filmmaking and creative tooling
- documentaries with strong systems thinking
- weird / fun / beautiful internet finds

Do not over-diversify. A focused set beats a random sampler.
If useful, read `references/taste-profiles.md`.

### 4. Find concrete videos

Prefer sources with high signal:
- YouTube
- Vimeo
- official conference talks
- creator channels with strong editorial quality
- playlists only when the user asks for a set

Avoid generic search-result dumping. Prefer exact video pages.
If needed, read `references/source-strategy.md`.

### 5. Rank and prune

For each candidate, ask:
- Why this one for this user right now?
- Is it likely to feel alive, useful, or delightful?
- Is it too generic, too obvious, too long, or too low-signal?

Prune aggressively.
If needed, read `references/scoring-rubric.md`.

### 6. Deliver cleanly

Default format:
- title
- direct link
- one-line why it matches

If the user only asks for links, keep commentary minimal.
If needed, read `references/output-patterns.md`.

## Output style

Be concise and taste-driven.
Do not sound like an algorithm.
Do not pad with generic “you might like” language.
Give the feeling of a smart friend with context.

## Heuristics

### Good recommendations should feel like:
- “how did you know I’d want this?”
- “this is exactly the rabbit hole I wanted”
- “this fits what I’m thinking about lately”

### Avoid:
- bloated top-20 lists unless asked
- repeating only the most famous channels
- shallow “motivation” sludge
- engagement bait
- links without rationale, unless the user explicitly wants links only

## Modes

### Mode A: Immediate watch
User wants something to watch now.
- Give 3-10 links
- Bias toward immediate clickability
- Minimize explanation

### Mode B: Taste curation
User wants discovery.
- Group by theme
- Add short rationale per video
- Show range without losing coherence

### Mode C: Project fuel
User wants videos useful for a project.
- Tie each recommendation to the project
- Prefer technical breakdowns, talks, interviews, or showcases

### Mode D: Mood rescue
User wants something fun or alive.
- Bias toward delight, surprise, and energy
- Keep the list short and varied

## Tooling guidance

When web search or fetch tools are blocked or low quality, use browser automation to get exact links.
For YouTube results, prefer extracting exact watch URLs instead of pasting search URLs.
Use `scripts/extract_youtube_links.js` as a simple DOM extractor pattern when needed.

## References

Read these only when needed:
- `references/source-strategy.md` for how to search and rank across platforms
- `references/output-patterns.md` for response formats
- `references/personalization.md` for building a recommendation profile from chat context
- `references/examples.md` for concrete usage patterns
- `references/scoring-rubric.md` for ranking candidates
- `references/testing.md` for test cases and evaluation
- `references/iteration-notes.md` for refining the skill over time
- `references/sample-runs.md` for example outputs and quality calibration
- `references/taste-profiles.md` for user-archetype-based recommendation shaping
- `references/publish-checklist.md` for pre-publish review

## Future upgrades

Potential additions later:
- source allowlists / denylists
- quality scoring persistence
- support for bilingual recommendations
- saveable watchlists by theme
- per-user taste memory
