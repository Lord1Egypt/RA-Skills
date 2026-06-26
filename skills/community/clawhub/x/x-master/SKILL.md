---
name: x-master
description: Master routing skill for all X/Twitter operations — reading, researching, posting, and engaging. Routes to the correct sub-tool based on the task. Covers reading tweets by URL, searching X, trend research, posting tweets/replies, and handling mentions.
license: MIT
compatibility: Requires fxtwitter API access. All X/Twitter operations route through this skill.
metadata:
  author: x-master-contributors
  version: 1.0.0
  tags:
    - x
    - twitter
    - social-media
    - routing
    - content
---

# X Master Skill — Master Routing for X/Twitter Operations

This skill is the single entry point for all X/Twitter work. Read it first, then route to the correct sub-tool based on your task. Never attempt raw x.com fetches. Never guess at routing.

---

## ⚠️ ABSOLUTE RULE: Never fetch x.com directly

Direct `web_fetch` of x.com or twitter.com URLs will fail silently or return garbage.

**Always use fxtwitter for reading tweet content:**
```
https://api.fxtwitter.com/{username}/status/{tweet_id}
```

Extract `username` and `tweet_id` from the x.com URL:
- `https://x.com/example/status/1234567890` → `api.fxtwitter.com/example/status/1234567890`
- `https://twitter.com/example/status/1234567890` → same pattern

This is a hard rule. No exceptions. See `references/fxtwitter-pattern.md` for full details.

---

## Account Configuration

This skill routes posting operations to one or more X accounts. Before using, configure your target account(s):

| Configuration | What It Means | Approval Required? |
|---------------|---------------|--------------------|
| Single account | All posts go to one account | Yes — always. Get human approval before posting. |
| Multiple accounts | Route based on content type | Yes — always. Confirm account + text before posting. |
| Draft-only mode | Generate drafts, never auto-post | Recommended for new users. Learn the flow first. |

**Golden rule:** Never post autonomously to X. Always draft first, get human approval before publishing.

Posting flow:
1. Draft the post in your voice
2. Share draft with the human for approval (via chat, email, or local review)
3. Only after approval: execute posting script
4. Log the URL and confirmation

---

## Task Router

### 1. Read a tweet or thread by URL
**Tool:** fxtwitter API via `web_fetch`
**When:** You have an x.com/twitter.com link and need to read the content
**How:**
```
web_fetch("https://api.fxtwitter.com/{username}/status/{id}")
```
**Response includes:** full text, author, engagement stats, media URLs, thread context via `reply_to`

**If fxtwitter is unavailable** (5xx errors or timeout): fall back to `x-research-skill` for tweet content retrieval.

---

### 2. Search X for real-time opinions or discourse
**Tool:** `xai-grok-search` skill
**When:** "What are people saying about X", "search X for Y", real-time pulse check, breaking news context
**Notes:**
- Responses may take 30–60s (involves reasoning)
- Results include citations with URLs
- Use for real-time social sentiment

---

### 3. Deep X research — threads, profiles, discourse
**Tool:** `x-research-skill`
**When:** Need to research a topic across many tweets, follow a conversation, understand discourse depth, or cache results
**Supports:** Filtering by handle, sorting by engagement, saving results for reuse

---

### 4. Multi-platform trend research (last 30 days)
**Tool:** `last30days-skill`
**When:** "What's trending about X topic", understanding broader cultural moments across Reddit + X + HN + YouTube
**Triggers:** Trend research requests, topic popularity analysis

---

### 5. Post a tweet, reply, or quote tweet
**Tool:** Custom posting script (see Setup)
**When:** Any posting action. Always requires human approval first.

**Posting flow:**
1. Draft the tweet in your voice
2. Share draft with human for approval
3. After approval: execute posting script
4. Log the URL in your conversation/record

**Never skip the approval step.** Even if you think you have permission, confirm the exact text before executing.

---

### 6. Handle mentions / replies to your account
**Tool:** `x-engage` skill
**When:** Your account receives a mention, reply, or engagement
**Notes:**
- Drafts replies automatically
- Always get human approval before posting
- Provides thread context for informed responses

---

### 7. Direct X API v2 calls
**Tool:** `xurl` skill (or your configured X API client)
**When:** Specific API operations — follower management, analytics, batch operations, anything not covered above
**Requires:** X OAuth configured in your environment

---

## Decision Tree (Quick Reference)

```
Got an x.com URL?
  → Read it: fxtwitter (NEVER direct web_fetch)

Need to search X for discourse?
  → Real-time pulse: xai-grok-search
  → Deep thread context: x-research-skill
  → Last 30 days across platforms: last30days-skill

Need to post/reply?
  → Draft → get human approval → execute script

Received a mention/reply?
  → x-engage (generates draft, awaits approval)

Need raw API access?
  → xurl or your configured X API client
```

---

## Key Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| fxtwitter pattern | `references/fxtwitter-pattern.md` | How and why to use fxtwitter; error handling |
| Algorithm intelligence | `references/algo-intel.md` | 2026 X ranking signals, engagement weights, strategy |
| Skill dependencies | README.md § Sub-Skills | What to install and when |
| Account config template | `config/accounts.json.example` | Starting point for posting setup |
| Posting script | `scripts/x-post.js` (if bundled) | Executes approved posts |
| xurl skill docs | `~/.openclaw/skills/xurl/` or clawhub | Direct X API v2 access |
| x-engage skill docs | `~/.openclaw/skills/x-engage/` or clawhub | Mention handling pipeline |

## What Was Deprecated / Removed from X Tooling

If you're migrating from older X agent setups, be aware:

| Tool/Pattern | Status | Replacement |
|-------------|--------|-------------|
| Herald/Barker agent | Deprecated — purpose-built X agents are fragile | x-engage skill handles mentions |
| x-twitter-api npm package | Deleted — third-party duplicate | xurl (first-party) |
| x-react.js / x-poll.js | Archived — standalone reaction scripts | Covered by xurl |
| Direct x.com web_fetch | Never worked reliably | fxtwitter (mandatory) |

---

## Algorithm Intelligence (Updated 2026-03-13)

*For full details, see `references/algo-intel.md`*

### Key Takeaways
- **Engagement hierarchy:** Replies (27x) and conversations (150x) beat likes *(human accounts — see note below)*
- **Velocity window:** Posts live or die in first 30 minutes
- **Content format:** Native video > threads > articles > images > text
- **Account signals:** X Premium, verification, consistency matter
- **Posting frequency:** >5x/day triggers suppression

> ⚠️ **Bot/AI account note:** Engagement weights above apply to human accounts. AI assistant or bot accounts are weighted differently by the algorithm. See `references/algo-intel.md` § "Strategy by Account Type" for bot-specific guidance.

> ⚠️ **Freshness:** Algorithm data last verified 2026-03-13. If today is past 2026-06-13, check `references/algo-intel.md` for a newer version before relying on specific weights.

### For Best Results
- Lead with video (15–30s, captions, motion hook)
- Reply to your own posts within 15 minutes of publishing
- Post at your audience's peak times
- Engagement pods and clickbait are algorithmically penalized

---

*This skill was created for AI agents to route X/Twitter work correctly. Adapt the account routing and approval flow to your needs, but keep the fxtwitter rule and task router structure unchanged.*

*Version: 1.0.0 | License: MIT*
