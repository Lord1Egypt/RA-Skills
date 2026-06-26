---
name: x-analytics-loop
description: Review X performance and choose next experiments. Use when analyzing weekly post metrics, diagnosing winners and losers, or planning what to repeat.
---

# X Analytics Loop

Run this weekly.

## Collect

For each post, ask for or infer:

- date/time
- topic
- format
- hook
- impressions
- likes
- replies
- reposts/quotes
- bookmarks if visible
- profile visits
- follows
- link clicks if relevant

## Calculate

Use:

- engagement rate = engagements / impressions
- reply rate = replies / impressions
- repost rate = reposts / impressions
- profile-click rate = profile visits / impressions
- follow conversion = follows / profile visits

If data is missing, continue with qualitative diagnosis and mark assumptions.

## Diagnose

- High impressions, low engagement: hook/retrieval worked, post underdelivered.
- Low impressions, high engagement: content resonated, distribution needs work.
- High replies, low follows: conversation works, profile may be weak.
- High profile clicks, low follows: bio/pinned post problem.
- High likes, low reposts: agreeable, not share-worthy.
- High reposts/bookmarks: make more templates/frameworks.

## Decide

Pick:

- 3 things to repeat
- 3 things to stop
- 3 experiments for next week

## Output

Return:

- **Top winners**
- **Hidden winners**
- **Losers**
- **Signal diagnosis**
- **Next week’s experiments**
- **Posting plan**

## Operating Principle

Treat the public X algorithm as a signal map, not a cheat code. Optimize for posts and replies that earn useful positive actions (dwell, replies, reposts, shares, profile clicks, follows) while avoiding negative actions (not interested, mute, block, report, fast skips).
