# Mission Schema

`mission.json` contains the strategy and safety envelope for the skill.

The mission is the source of truth for what the account is trying to grow. Do not assume a default topic or product category outside the mission.

## Core Fields

- `name`: short mission name
- `goal`: concrete growth objective
- `account_handle`: target X account
- `audience`: target audience description
- `voice`: desired tone
- `primary_topics`: topics to prioritize
- `watch_keywords`: keywords or phrases worth monitoring
- `watch_accounts`: KOLs or competitor handles to monitor
- `banned_topics`: topics never to touch
- `cta`: preferred call to action
- `risk_tolerance`: `low`, `medium`, or `high`
- `autonomy_mode`: `manual`, `review`, or `auto`

## Scoring Logic

Opportunity scoring combines:

- relevance to mission topics and keywords
- urgency based on recency and growth rate
- engagement potential from current traction
- authority fit based on source type or watched accounts
- risk penalty from banned topics, negative sentiment, or low confidence

## Action Selection

Prefer:

- `reply` for timely discussions where a specific post already has momentum
- `quote_post` when a post is useful context but needs a stronger original angle
- `post` when the mission needs a standalone stance
- `observe` when opportunity quality is weak or risk is too high

## Algorithm Heuristics

When scoring or drafting, also apply these posting heuristics:

- the first two hours matter most for reply-driven growth
- prefer replying to an active discussion over creating a standalone post when timing is critical
- avoid external links in the main post body when possible; place them in a follow-up reply
- add a question or disagreement surface when the goal is to trigger replies
- prefer a thread over an overlong single post
- reduce standalone posting confidence if the operator cannot stay online to engage

## Memory Schema

`memory.json` stores cross-run learnings:

- `successful_topics`: topics that historically performed well
- `successful_action_types`: counts of action types with good outcomes
- `high_signal_accounts`: accounts that repeatedly produced useful opportunities
- `avoid_accounts`: accounts that repeatedly led to low-value or risky actions
- `feedback_events`: append-only summary of reviewed outcomes

Use memory to bias future ranking and action selection, not to override mission safety rules.
