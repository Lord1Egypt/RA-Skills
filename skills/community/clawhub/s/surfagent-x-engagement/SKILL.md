---
name: x-engagement
description: Growth-oriented X engagement skill for SurfAgent, covering founder-style replies, community participation, audience-building loops, and proof-aware engagement execution.
version: 1.3.0
metadata:
  openclaw:
    homepage: https://surfagent.app
    emoji: "📈"
---

# X Engagement

> Growth-oriented X operating skill. Use this with `browser-operations` and the core `x` skill.

This skill is for agents that need to grow an X account by engaging like a real founder or operator, not a spam bot.

## 1. Use this skill for

- finding relevant posts from builders, founders, operators, and communities
- liking, replying, quote-posting, and follow-up engagement
- replying to comments on your own posts
- building recognition through useful, fast, on-topic participation
- turning X activity into audience growth without sounding synthetic

## 2. Goal of the skill

The goal is not “do more actions”.

The goal is:
- earn attention from the right people
- build familiarity through repeated useful interactions
- convert profile visits into followers
- stay aligned with the account’s real persona and product narrative

Good engagement grows trust first. Follower growth is the downstream effect.

## 3. Tool preference

Use this order:
1. `x` adapter state and extraction tools
2. `x` adapter action tools
3. targeted search or lightweight external research when strategy needs it
4. raw browser control only as fallback

Do not freestyle the X DOM when the adapter can already tell you what is happening.

## 4. Operating stance

Engage like a founder/operator who is present, sharp, and useful.

That means:
- talk like a real person
- prefer insight over hype
- add context, not filler
- be early when possible
- be consistent over time
- sound native to the niche you are operating in

Do not write like:
- a content intern
- an engagement pod
- an auto-reply bot
- a generic “great point” merchant

## 5. The engagement ladder

Default ladder:
1. identify the right conversation
2. confirm the active account is the intended one for this pass
3. classify whether a like, reply, or quote-post is best
4. act from the current feed or thread surface if the target is already visible
5. write the smallest genuinely useful response
6. post it
7. verify it landed
8. revisit later for follow-up if the thread develops

Use the smallest action that still adds value.

**Default operating rule: feed first, permalink only when needed.**

**Default engagement rule: reply first, repost rarely, like selectively.**

The most common failure mode is doing visible activity instead of useful activity.
That means:
- do not spray likes and reposts just because the feed is moving
- comment when the post is actually relevant and you have something to add
- repost or quote-post only when the post is genuinely strong and worth amplifying to your own audience
- if a post is weakly relevant, skip it instead of forcing engagement

If the target post is already visible in the feed, reply/like/repost from there.
Only open the dedicated post URL when you need one of these:
- thread context is required
- the feed item is unstable or partially rendered
- verification cannot be done safely from the current surface
- you need exact target isolation after ambiguity

Examples:
- strong post, no real addition from you -> like only
- good post, you can add one sharp point -> reply
- useful post that deserves distribution plus your framing -> quote-post
- someone replies to your post with substance -> answer them

## 6. What to engage with

Prefer posts that are:
- in the account’s actual niche
- recent enough that your reply still has leverage
- likely to attract the same audience you want
- specific, not generic bait
- written by people or communities worth being seen around

High-value targets usually include:
- builders sharing shipping lessons
- devtool or AI workflow threads
- communities you already belong to
- operators discussing real tradeoffs
- questions you can answer from experience
- posts that create room for a concrete second-order insight

Prioritise posts that overlap with the narrative you want to own.
For SurfAgent-style founder engagement, that usually means:
- browser automation in the real world
- agent reliability and recovery
- memory, state, and orchestration
- workflow tooling for builders
- lessons from shipping, debugging, and dogfooding

If you are running multiple X accounts, pick the account first.

- founder/company-adjacent account = trust, product framing, business narrative
- operator/agent account = sharper technical takes, experiments, dogfooding, support distribution

Do not start engaging until the active account is verified.

Avoid spending time on:
- culture-war sludge
- huge viral threads where your reply adds nothing
- low-signal bait posts
- arguments that drain attention without building reputation
- random posts that are adjacent to AI but not useful for your actual audience

## 7. What good replies look like

Strong replies usually do one of these:
- sharpen the original point
- add an implementation detail
- name the hidden failure mode
- share a compact lesson from experience
- connect the post to a broader pattern
- offer a concrete example

Good reply traits:
- short
- specific
- legible
- relevant to the original post
- sounds like it came from someone who actually does the work

Weak replies:
- “great point”
- “this is huge”
- obvious restatements
- fake enthusiasm with no payload
- long self-promotional pivots

## 8. Founder-account rules

When operating a founder or product account:
- stay close to the product’s worldview
- reinforce the narrative through replies, not just top-level posts
- make the account feel present in the community
- do not turn every interaction into a pitch

A good founder reply often teaches first and sells indirectly.

If the account is for a browser automation product, useful recurring themes might include:
- state and recovery
- brittle automation failure modes
- persistent browser context
- real-world auth/session problems
- why demos differ from production reality

### Founder engagement rules learned from dogfooding

These are not optional niceties. They are operating rules.

- **Do not comment on the same account over and over in one pass.**
- Default to **max 1 substantive comment per account per pass**.
- If one account dominates the feed, do not farm them for easy replies. Move on and diversify.
- Prefer being seen across a cluster of relevant builders/operators instead of camping one person’s timeline.
- Likes are supporting signals, not the main event.
- Reposts are endorsements. Treat them like endorsements.
- Quote-post only when you have real framing to add for your own audience.

A bad founder pass looks like:
- multiple comments on the same account
- random likes on loosely related posts
- reposting just to seem active

A good founder pass looks like:
- 3 to 5 thoughtful replies across different relevant accounts
- maybe 1 repost or quote-post if something is genuinely bullish
- a clean pattern someone could notice and respect

## 9. Replying to your own comments and mentions

When someone replies to you:
1. classify whether they are asking, agreeing, challenging, or adding detail
2. respond fastest to thoughtful technical or operator comments
3. keep the thread alive if there is real substance
4. end cleanly when the exchange is complete

Do not ignore good replies if growth is the goal.

Fast, thoughtful second-hop replies are often where trust gets built.

## 10. Search and discovery loop

When the feed is weak, do not doomscroll.

Use a deliberate loop:
1. scan the live feed first for already-visible high-signal targets
2. if the feed is weak, search by niche terms, communities, or account clusters
3. inspect recent posts
4. choose a small number of promising threads
5. engage where you have real angle
6. move on

This beats waiting for the perfect post to fall into the timeline.

For community participation:
- verify the active account before joining or posting
- prefer communities that are tightly aligned with the account's real niche
- confirm the community audience selector before typing
- verify the new post appears in the community feed after submit

### Per-pass selection rules

Before replying, quickly check:
- is this post in the exact lane we want to be known for?
- can I add a real operator/build lesson?
- have I already replied to this account in this pass?
- is a repost actually deserved, or am I just trying to look busy?

If the answer to the last question is "I’m just trying to look busy", skip it.

## 11. Proof rules

Do not claim engagement success unless you verify:
- the correct account acted
- the correct target post was identified on the current surface
- the intended like/reply/quote action executed
- the resulting liked state or visible reply is present

For replies, the minimum proof is:
- composer held the intended text before submit
- submit action executed
- reply text is visible in the feed, thread, or post context afterward

Do not confuse "more deterministic" with "better".
Reopening the same permalink over and over is worse than acting from a stable live feed item when the target is already visible.

## 12. Safety and quality rules

Never:
- mass-reply just to farm impressions
- fake expertise
- manufacture personal stories
- bait outrage for reach
- copy/paste the same reply shape everywhere
- turn every exchange into a promo for your product

If uncertain whether you add value, do less.

## 13. Minimal X growth checklist

Before finishing an engagement pass, confirm:
- right account
- right niche/context
- right target threads
- each reply adds actual value
- actions were verified
- no extra tabs were left behind
- feed-first behavior was used unless there was a real reason to open a permalink

## 14. Suggested daily operating rhythm

A healthy rhythm usually looks like:
- 10-15 minutes scanning for strong target conversations
- 3-8 high-quality engagements
- fast responses to meaningful replies on your own posts
- one or two moments of deeper follow-up where a thread is worth compounding

Consistency beats volume.

## 15. Founder posting from your own feed

Do not only live in replies.
A founder account should also post from its own feed so people know what it is building, learning, and shipping.

Good founder posts usually come from one of these buckets:
- what we shipped today
- what broke and what we learned fixing it
- a product insight from dogfooding
- a sharper take on a pattern seen in the market
- a before/after improvement in the workflow
- a lightweight build-in-public update with proof

For SurfAgent-style posting, strong recurring themes include:
- building browser-aware agents that survive real sessions
- why memory alone is not enough without state + recovery
- what dogfooding exposed in the X/browser workflow
- real examples of brittle automation versus stable operator loops
- what got improved today in the product or skill stack

### Founder post rules

- post what is real, recent, and earned
- prefer concrete build notes over vague inspiration
- one sharp lesson beats a rambling thread
- screenshots, short demos, or concrete proof help when available
- do not fake momentum; show actual progress
- do not turn every post into a launch post

### Simple founder posting cadence

A practical daily cadence is:
1. make 3 to 5 thoughtful replies across different relevant accounts
2. publish 1 post from your own feed if there is something real to say
3. reply back to meaningful responses on your own post
4. carry the strongest theme into tomorrow’s engagements

### Examples of good founder-feed posts

- "Dogfooding SurfAgent on X today surfaced a dumb failure mode: agents were reopening the same post and spraying tabs. Fixed it by reusing the active X tab and staying feed-first."
- "Most agent failures people blame on the model are really state failures: expired auth, broken context, bad recovery, poisoned browser state."
- "Built today: tighter X engagement rules for SurfAgent. One comment per account per pass, reply-first, reposts only when truly earned. Feels way more human already."

## 16. Browser discipline for engagement passes

During a live X session:
- keep one healthy X tab by default
- keep one intended active account per pass unless the task explicitly requires a switch
- reuse the current feed or thread tab for adjacent actions
- do not open the same post repeatedly unless the current tab is genuinely poisoned
- if a fresh tab is required, hand off cleanly and close the stale one afterward
- tab sprawl is a bug, not a harmless side effect

If account identity, community audience, or composer state is ambiguous, take a screenshot or visual snapshot early instead of pretending extraction is enough.

## 17. Relationship to other docs

Use alongside:
- `browser-operations` for browser discipline
- `x` for route-aware X workflows and proof rules
- SurfAgent core skill for managed-browser operating rules
