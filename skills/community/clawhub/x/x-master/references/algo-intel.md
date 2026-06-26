# Algorithm Intelligence — X Ranking Signals (2026)

**Last Updated:** 2026-03-13  
**Relevance:** Active as of January 19, 2026 (Grok transformer rollout)  
**Next Review:** 2026-06-13  
**Sources:** xai-org/x-algorithm (Apache 2.0, 16K⭐) + community analysis  
**Maintenance Note:** Community contributors should update this quarterly as X refines the algorithm. Open a PR with evidence if you have fresher data.

> ⚠️ **Freshness check:** If today is past 2026-06-13, verify engagement weights are still current before relying on them for strategy. The algorithm evolves every 3–6 months.
>
> ⚠️ **Bot/AI accounts:** Engagement weights in this document apply to human accounts. AI assistant and bot accounts are weighted differently. See "Strategy by Account Type" below for bot-specific guidance before using the weight table.

---

## Overview: The Grok Transformer Era

In January 2026, X completed the rollout of Grok as its ranking engine. This replaced the legacy hand-engineered rules-based system.

**What changed:** The algorithm now **semantically understands content** — reads text, watches video, predicts engagement probability from learned patterns. Everything is learned from user behavior, not hand-coded.

**Impact:** Signal strength shifted. Old tactics (likes, follows) matter less. New tactics (conversation depth, content quality, early velocity) matter exponentially more.

---

## Engagement Weight Hierarchy

When X's ranking system decides which posts to promote, different actions carry different weight. All weights are normalized relative to a "like":

| Action Type | Weight | Notes |
|-------------|--------|-------|
| Like | 1x | Baseline |
| Bookmark | 10x | Signal of "save for later" intent — high quality indicator |
| Profile click | 12x | User curiosity about author |
| Repost / Retweet | 20x | Sharing amplifies reach |
| Quote Tweet | 25x | Quote adds commentary — harder than retweet |
| Reply | **27x** | Engagement + content creation |
| Reply to your own post (within 15 min) | **150x** | Thread = conversation = highest signal |
| **Blocks / Mutes / "Not interested"** | **Severe negative** | Suppresses post and damages account score |

**Critical insight:** A single conversation thread (you reply, user replies back) is worth **150 likes**. This is the single most actionable lever for reach.

---

## The 30-Minute Velocity Window

Posts have a critical launch window: **the first 30 minutes** (especially first 15 minutes).

**Why:** X's algorithm uses early engagement velocity as a predictor of total engagement. High early adoption triggers broader distribution to the For You feed.

### Velocity Strategy

| Window | Action | Impact |
|--------|--------|--------|
| -5 min before | Pre-announce to community | Primes audience |
| 0 min (post) | Drop the post | Live |
| 0–5 min | Be online, watch replies | Catch and reply to early comments |
| 5–15 min | Reply to comments | **Each reply = 27x signal** |
| 15–30 min | Encourage reshares | Last chance for velocity window |
| 30+ min | Post is ranked | Velocity window closed; recovery rare |

**Worst outcome:** Post drops at 2 AM when your audience is asleep. Even great content will miss the velocity window and die.

**Best outcome:** Post at 9 AM on Wednesday (confirmed peak across all accounts). Be at your desk. Reply to comments in real-time. One thread = 150x boost.

### Peak Posting Times (By Day of Week)

| Day | Peak Window | Notes |
|-----|-------------|-------|
| Monday | 8–10 AM, 12–1 PM | Work hours, higher engagement |
| Tuesday | 8–10 AM, 12–1 PM | Strong day |
| **Wednesday** | **8–10 AM** | **Statistically confirmed peak** |
| Thursday | 8–10 AM, 12–1 PM | Good day |
| Friday | 8–9 AM | Morning only; attention drops afternoon |
| Saturday | 10–11 AM | Lower engagement overall |
| Sunday | 9–10 AM | Lower engagement overall |

**Timezone note:** All times above are in ET. Adjust for your audience's timezone if different.

---

## Content Format Ranking

### 1. Native Video (10x vs Text)

Short-form native video is the strongest format. No Twitter links, no uploads — *native* video means uploaded directly to X.

**Optimal specs:**
- **Duration:** 15–30 seconds (sweet spot)
- **Captions:** Burned-in or overlay required (60% of users watch muted)
- **Hook:** First 3 frames must grab attention
- **Motion:** Avoid static text — movement drives watch time
- **Aspect ratio:** 9:16 (vertical) or 16:9 (horizontal). Portrait performs better on mobile.

**Engagement boost:** 10x vs text posts.

### 2. Threads (Dwell Time)

Threads force users to stay in your conversation longer. Each reply bumps the original post's visibility score.

**Why it works:** Dwell time (seconds spent in thread) is a strong engagement signal. Long threads = more dwell.

**Best practice:** Threads of 5–7 replies. Longer threads lose readers; shorter threads waste the format.

### 3. Articles (2026 Reversal)

In 2018–2024, external article links were algorithmically suppressed (X wanted to keep users on X). In 2026, this flipped.

**2026 change:** External article links now get a boost. Long-form expertise on external sites (Substack, Medium, your blog) is now promoted.

**Best format:** Article + thread hybrid. Post your article link, then drop 3–4 key takeaways as a thread. Users click the link for depth, X sees the external link engagement.

**Engagement boost:** 3x vs pure threads.

### 4. Images

Static images boost engagement 2–3x vs text, but below video.

**Best practice:** High-contrast, text-forward images. Memes, charts, screenshots perform best.

### 5. Text Only

Baseline. No boost, no penalty.

### 6. External Links (Non-Premium)

For non-Premium accounts, external links without additional context (e.g., bare URL) get near-zero engagement lift.

**Workaround:** Add text context ("Read this →") or combine with media.

---

## Account Signals

These factors affect your baseline reach and distribution:

### X Premium Subscription ($8/mo)

**Mandatory for serious reach.** Why:

1. **Payouts:** Only Premium engager activity counts toward creator revenue payouts
2. **Amplification:** Premium accounts get distribution boosts on For You feeds
3. **Credibility:** Signals commitment to the platform
4. **Feed placement:** Small but measurable boost in algorithm ranking

**Fact:** A small audience of Premium users engaging with your content is worth more than a large non-Premium audience.

### Verification Status

Verified accounts get a baseline boost. Unverified accounts rank lower, especially in For You feeds.

### Posting Frequency

- **1–3 posts/day:** Optimal range
- **4–5 posts/day:** Acceptable
- **>5 posts/day:** Triggers suppression. Algorithm deprioritizes prolific low-quality accounts.

**Rule:** Quality over quantity. One excellent post beats 5 mediocre ones.

### Consistency

Accounts that post daily compound engagement faster than one-off viral posts. The algorithm rewards consistency.

**Why:** Predictable, consistent accounts build trust and audience expectations.

---

## What to Avoid

These tactics are either suppressed or penalized:

### Clickbait / Engagement Bait

Posts like "Like if you agree" or "This will blow your mind!" are detected and suppressed. The algorithm learned to hate them.

**Why:** Users hate them. Blocks/mutes spike. Negative signal.

### Engagement Pods

Coordinated groups artificially boosting each other's posts. X detects these via behavior patterns.

**Penalty:** Accounts in pods get suppressed across the platform. Severe.

### Low-Effort Replies

One-word replies ("Great!", "lol") or non-substantive engagement.

**Why:** Dwell time is zero. No signal value.

### Posting When Audience Is Offline

A great post at 3 AM gets 50% visibility loss every 6 hours. By the time your audience wakes up, the post is buried.

**Rule:** Know your audience's timezone and peak hours.

### Copying/Plagiarism

Reposting others' content verbatim triggers suppression. The algorithm detects duplicates.

---

## Strategy by Account Type

### For Brand / Public Figure Accounts

- **Lead with video:** Events, behind-the-scenes, quick takes
- **Daily posting:** 1–3 posts per day minimum
- **Conversation:** Reply within 15 minutes to spike engagement threads
- **Articles:** Long-form strategy is correct now (2026 reversal)
- **Community:** Engage replies personally; builds loyalty signal

### For AI Assistant / Bot Accounts

- **High-quality replies:** One thoughtful reply > 10 likes
- **Conversation depth:** Reply depth matters more than post frequency
- **No low-effort engagement:** Avoid "Great post!" type replies
- **Strategic engagement:** Choose high-quality posts to engage with
- **Credibility:** Depth signals assistant intelligence to algorithms and humans alike

### For Creator / Content Accounts

- **Consistency:** Daily content schedule
- **Hybrid format:** Article + thread beats either alone
- **Niche authority:** Focus depth over breadth; specialist beats generalist
- **Community building:** Engage your audience, not cold accounts
- **Video first:** Lead with native video when possible

---

## Measurement & Iteration

Track these metrics weekly:

| Metric | What It Means | Target |
|--------|---------------|--------|
| Impressions | Total views (first signal of distribution) | Growing +10% WoW |
| Engagement rate | (Replies + Reposts + Likes) / Impressions | 2–5% for brands, 5–10% for creators |
| Reply ratio | Replies / Impressions | 0.5–2% (high indicates conversation) |
| Bookmark rate | Bookmarks / Impressions | 0.5–1.5% (quality signal) |
| Audience growth | New followers | +50–100/week for consistent posting |

**Iteration:** If impressions drop, check:
1. Posting time (moved outside peak window?)
2. Content format (shifted away from video?)
3. Engagement rate (too low? improve reply quality)
4. Posting frequency (too high or too low?)

---

## Key Takeaways

1. **Replies are gold.** One good reply (27x) or conversation thread (150x) beats 10 likes.
2. **Velocity matters.** First 30 minutes determine reach. Be online to reply.
3. **Video first.** Native video gets 10x boost. Make it short, captioned, motion-driven.
4. **Articles work now.** Combine external articles with threads for 3x boost.
5. **Premium + consistency.** X Premium + daily posting = compounding reach.
6. **Quality over quantity.** >5 posts/day triggers suppression. One excellent post beats five mediocre ones.

---

## Sources & Further Reading

- **xai-org/x-algorithm** — https://github.com/xai-org/x-algorithm (Apache 2.0, Jan 19 2026 release, 16K⭐)
- **X Creator Academy** — https://creator.x.com/
- **X Premium Features** — https://x.com/Premium
- **Community Analysis** — Twitter Algorithm Exposed series (multiple independent researchers)

---

## Maintenance Note

This document was created 2026-03-13 and reflects algorithm state as of January 19, 2026. X updates its algorithm every 3–6 months. **Update this file quarterly** with:

- Any new engagement weight changes
- Peak posting time shifts
- New content format boosts (e.g., spaces, live video)
- Verification/Premium requirement changes
- Community feedback on tactics that stopped working

To contribute updates: File an issue or PR with evidence (X creator reports, community data, GitHub findings).

---

*Last updated: 2026-03-13*  
*Next review: 2026-06-13*  
*Responsibility: Maintainers and community contributors*
