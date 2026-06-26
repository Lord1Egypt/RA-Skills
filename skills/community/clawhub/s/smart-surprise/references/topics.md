# Smart Surprise — Topics Reference

The single source of truth for all content topics and user preferences.

**This file is read and updated by the agent on every run.**

## Topics

**The agent may add new topics here during runtime based on the user's interests.** The 11 below are the initial set.

### greeting [interaction] [normal]
A warm, casual greeting. Match the tone to the time of day. Be friendly and a bit playful — never robotic.

### time-care [interaction] [normal]
Time-aware care or a contextual nudge. Something relevant to the current hour or moment in the user's day. Keep it short and actionable.

### weather [information] [normal]
A brief weather observation with one practical suggestion based on conditions. Requires `location` in config.

### calendar [information] [normal]
A reminder of today's upcoming calendar events from Google Calendar. Brief and scannable. Skip silently if no events.

### health [information] [normal]
A single, short health micro-tip. Rotate across hydration, movement, posture, eye rest. Never preachy.

### tips [information] [normal]
One useful or interesting tip, life hack, or productivity suggestion. Always include a brief "why it matters."

### history [information] [normal]
Something fascinating that happened on this exact date in history. Engaging, not dry. Pick something that sparks curiosity.

### entertainment [information] [normal]
A recommendation for a movie, song, book, or show. Keep it brief — one sentence on why it's worth it.

### quote [information] [normal]
A meaningful quote, line of poetry, or saying. Match the mood or season. Source it properly.

### news [information] [normal]
One interesting or thought-provoking news story of the day. Not just a headline — explain why it's worth knowing.

### check-in [interaction] [normal]
A warm, genuine question about how the user is doing. This is the most important interaction topic — it must appear in every message. Keep it casual and caring.

---

## Preference Learning

After each message, the agent silently updates the `preference` field of the topics in this file.

**Three states:**

| State | Meaning |
|-------|---------|
| `normal` | Default — selected at normal frequency |
| `preferred` | User likes this topic — selected more often |
| `dislike` | User dislikes this topic — selected much less often |

**How to update:**

| Signal | New preference |
|--------|---------------|
| User says "I love X" / responds very positively | `preferred` |
| User explicitly asks for more of this topic | `preferred` |
| User says "I don't like X" / "please stop" | `dislike` |
| User reacts negatively or ignores this topic repeatedly | downgrade one level |
| User says "wish you talked about Y more" | `preferred` |

**Rules:**
- `check-in` can never be set to `dislike` — always keep at minimum `normal`
- `dislike` means rarely selected, not fully excluded

**📋 Silent Preference Updates:**
The agent updates preferences silently after each interaction — this is intentional to keep the conversation flow natural. However, you can monitor all preference changes at any time by reading `topics.md`. If you notice any topic has been wrongly classified (e.g., `dislike` when you actually liked it), simply edit `topics.md` to correct it — the agent will respect your manual override on the next run.

---

## Topic Selection

On each run, the agent:

1. Filters out topics marked `dislike`
2. Selects 2–3 topics, favoring those marked `preferred` when possible
3. Always selects at least 1 `type: interaction` topic
4. Places `check-in` as either the opening or the closing of the message

**Message structure:**
```
Opening:  greeting or time-care
Body:     1–2 information topics
Closing:  check-in or time-care
```
