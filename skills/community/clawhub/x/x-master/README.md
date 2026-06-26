# x-master — Master Routing Skill for X/Twitter Operations

Master routing skill for all X/Twitter operations in an AI agent. Routes to the correct sub-tool based on the task: reading tweets, searching X, trend research, posting, and handling mentions.

## What It Does

- **Read tweets by URL** — fxtwitter pattern (never direct fetch)
- **Search X for real-time discourse** — powered by xai-grok-search
- **Deep research** — threads, profiles, conversations via x-research-skill
- **Trend analysis** — last 30 days across Reddit, X, HN, YouTube via last30days-skill
- **Post/reply** — routes to posting scripts with approval flow
- **Handle mentions** — automated draft generation via x-engage
- **Raw API access** — direct X API v2 calls via xurl

## Why the fxtwitter Rule Exists

Direct HTTP fetches of x.com or twitter.com URLs fail because:
1. Twitter/X blocks raw HTTP crawling (JavaScript-rendered content)
2. Rate limiting on direct requests
3. Authentication/cookie requirements for full content

**fxtwitter** is a free, open-source API proxy that:
- Renders the page server-side
- Returns clean, structured JSON
- No authentication required
- Optimized for bot/agent usage

See `references/fxtwitter-pattern.md` for the complete pattern and error handling.

## Install

```bash
git clone https://github.com/your-username/x-master.git
cd x-master
```

Or add as a git submodule to your agent skills directory:
```bash
git submodule add https://github.com/your-username/x-master.git skills/x-master
```

## Setup

### 1. Install Dependencies

**TL;DR: Start with x-master alone. You can read tweets immediately. Install sub-skills only as you need them.**

#### Essential (built-in, no install needed)
- `web_fetch` — Built into your agent. Required for reading tweets via fxtwitter. No setup.

#### Optional (install as needed)

| Skill | Purpose | Install if... |
|-------|---------|---------------|
| `xai-grok-search` | Real-time X/web search | You need "what are people saying about X right now" |
| `x-research-skill` | Deep X thread research | You need historical or conversational context |
| `last30days-skill` | 30-day cross-platform trends | You want Reddit + X + HN + YouTube combined |
| `x-engage` | Incoming mention handling | You're running a bot account that receives replies |
| `xurl` | Direct X API v2 access | You need follower management, analytics, or batch ops |

Verify installed sub-skills (replace `$AGENT_SKILLS_DIR` with your framework's skills path):
```bash
ls $AGENT_SKILLS_DIR | grep -E "grok|x-research|last30days|x-engage|xurl"
# OpenClaw default: ls ~/.openclaw/skills/
```

### 2. Configure Environment Variables

Create `.env` in your agent's working directory or add to your shell profile:

```bash
# X API credentials (optional, required for direct API calls)
export X_BEARER_TOKEN="your_x_bearer_token"
export X_OAUTH_TOKEN="your_oauth_token"
export X_OAUTH_SECRET="your_oauth_secret"

# For xai-grok-search (optional, uses free tier by default)
export XAI_API_KEY="your_xai_key"

# For last30days-skill (optional)
export SCRAPECREATORS_API_KEY="your_scrapecreators_key"
```

### 3. Configure Your Accounts (Posting Only)

Only needed if you plan to post to X (Task 5). Skip if you're only reading tweets.

Copy the template and edit with your handle:
```bash
cp config/accounts.json.example config/accounts.json
```

Example config:
```json
{
  "accounts": [
    {
      "name": "primary",
      "handle": "@your_handle",
      "role": "general",
      "approvalRequired": true
    }
  ],
  "defaultAccount": "primary",
  "approvalMode": "manual"
}
```

All posting requires human approval before execution. Leave `approvalRequired: true` unless you have a specific reason to change it.

### 4. Test fxtwitter Access

```bash
curl "https://api.fxtwitter.com/example/status/1234567890" | jq .
```

You should get JSON response with tweet content.

## Usage Examples

### Reading a Tweet by URL

```
User: Read this tweet: https://x.com/example/status/1234567890
```

Routes to fxtwitter. Returns full tweet content, author, engagement metrics.

### Searching X for Discourse

```
User: What are people saying about AI agents on X right now?
```

Routes to `xai-grok-search`. Real-time results with citations.

### Deep X Research

```
User: Research the AI safety conversation on X over the last week
```

Routes to `x-research-skill`. Returns key threads, voices, sentiment.

### Checking 30-Day Trends

```
User: What's trending about crypto in the last 30 days?
```

Routes to `last30days-skill`. Cross-platform analysis: Reddit, X, HN, YouTube.

### Posting (Approval Required)

**Step 1:** You request a draft:
```
User: Draft a post about our launch
```

**Step 2:** Agent generates a draft and surfaces it for approval:
```
[Draft] Ready for your approval:
"Something big is launching. Here's what we built and why it matters."

Reply ✅ to approve and post, or ❌ to discard.
```

**Step 3:** You approve → agent executes posting script and logs the URL:
```
✓ Posted: https://x.com/your_account/status/...
```

**Never skip the approval step**, even if the draft looks perfect.

## Task Router Quick Reference

| Task | Skill/Tool | When to Use |
|------|-----------|-----------|
| Read tweet by URL | fxtwitter (web_fetch) | Any x.com/twitter.com link |
| Real-time X search | xai-grok-search | "What are people saying..." |
| Deep thread research | x-research-skill | Topic research, conversation analysis |
| 30-day trends | last30days-skill | Trend analysis, cultural context |
| Post/reply | x-post script | Posting to X (requires approval) |
| Handle mentions | x-engage | Incoming mentions, replies |
| Raw API calls | xurl | Direct X API v2 operations |

## Algorithm Intelligence Summary

The current X algorithm (Jan 2026, Grok-powered) prioritizes:

1. **Engagement type:** Replies (27x) and conversations (150x) beat likes
2. **Velocity:** Posts live/die in first 30 minutes
3. **Content format:** Video > threads > articles > images > text
4. **Account signals:** Premium status, verification, consistency
5. **Frequency:** >5x/day triggers suppression

**Best practices:**
- Lead with native video (15–30s, captions)
- Reply within 15 minutes of posting
- Post at audience peak times
- Avoid engagement pods and clickbait

See `references/algo-intel.md` for full algorithm intelligence including engagement weight tables and detailed strategy by account type.

## Sub-Skills & Dependencies

This skill routes to and depends on:

| Skill | Purpose | OpenClaw Install | Other Frameworks |
|-------|---------|-----------------|-----------------|
| xai-grok-search | Real-time X/web search | `clawhub install xai-grok-search` | Clone from ClaWHub or equivalent |
| x-research-skill | Deep X research | `clawhub install x-research-skill` | Clone from ClaWHub or equivalent |
| last30days-skill | 30-day trend analysis | `clawhub install last30days-skill` | Clone from ClaWHub or equivalent |
| x-engage | Mention handling | `clawhub install x-engage` | Clone from ClaWHub or equivalent |
| xurl | X API v2 access | `clawhub install xurl` | Clone from ClaWHub or equivalent |

**All are optional.** For reading tweets, nothing to install — fxtwitter works via built-in `web_fetch`.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "fxtwitter API returned 404" | Tweet deleted or wrong ID | Verify URL and tweet still exists |
| "fxtwitter API unavailable" | Temporary service outage | Try again in 5 minutes; check https://status.fxtwitter.com |
| "xai-grok-search timeout" | Reasoning model taking >60s | Reduce query complexity or try again |
| "Post failed: not approved" | Skipped approval flow | Always draft first, get human approval before posting |
| "x-research-skill requires X_BEARER_TOKEN" | Environment variable missing | Set `X_BEARER_TOKEN` in `.env` or shell |

## File Structure

```
x-master/
├── SKILL.md                      # Main skill definition and task router
├── README.md                     # This file
├── LICENSE.txt                   # MIT license
├── .gitignore                    # Git ignore rules
├── references/
│   ├── algo-intel.md            # X algorithm intelligence (updated 2026-03-13)
│   └── fxtwitter-pattern.md     # fxtwitter usage, error handling, examples
├── config/
│   └── accounts.json.example    # Account configuration template (copy to accounts.json)
└── scripts/
    └── (add your posting scripts here — see SKILL.md § Task Router, task 5)
```

## Algorithm Intelligence Preview

This skill includes comprehensive analysis of the current X algorithm (Jan 2026, Grok-powered). Key findings:

- **New:** Semantic understanding of content via Grok transformer
- **Weight hierarchy:** Single conversation (150x) beats 10 likes
- **Video boost:** Native video gets 10x vs text
- **Article reversal:** External articles NOW boosted (opposite of 2018–2024)
- **Premium requirement:** Payouts only for Premium engager activity

Full details in `references/algo-intel.md` with sourcing and last-updated timestamp.

## License

MIT © 2026, x-master contributors

## Contributing

Submit issues or PRs with evidence of bugs or improvements. Update `references/algo-intel.md` if you have fresh X algorithm findings.

---

For questions or contributions, see the full documentation in SKILL.md and references/.
