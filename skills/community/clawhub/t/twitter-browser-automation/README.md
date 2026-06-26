# twitter

OpenClaw skill to interact with Twitter/X through Chrome browser via browser-relay MCP — no API keys required.

---

## Installation

### Via ClawHub (recommended)

```bash
clawhub install twitter
```

If you don't have `clawhub` installed:

```bash
npm install -g clawhub
clawhub install twitter
```

### Manual (from this repository)

1. Copy the `twitter/` folder into the `skills/` directory of your OpenClaw project:

```bash
cp -r twitter/ /path/to/your/openclaw-project/skills/
```

---

## Prerequisites

1. **browser-relay MCP** server installed and connected to your OpenClaw session
2. **Google Chrome** open with an active, logged-in session at [x.com](https://x.com)
3. **macOS or Linux** (Windows not supported)

> The skill will NOT attempt to log you in. You must already be authenticated on x.com in Chrome before using this skill.

---

## Browser-Relay Setup

If browser-relay MCP is not yet configured in your OpenClaw project, add it to your MCP configuration:

```json
{
  "mcpServers": {
    "browser-relay": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/browser-relay"]
    }
  }
}
```

Verify the connection by asking your agent to navigate to a page and take a screenshot.

---

## Capabilities

| Capability | Description |
|-----------|-------------|
| **Post Tweet** | Compose and publish tweets with character count validation |
| **Create Thread** | Post multi-tweet threads (4–8 tweets, optimal engagement) |
| **Search Trends** | Find and display current trending topics on X |
| **Search Hashtags** | Explore tweets by hashtag, switch between Top and Latest |
| **Analyze Performance** | Read engagement metrics: likes, retweets, replies, bookmarks, views, engagement rate |
| **Reply to Tweet** | Reply to any tweet by URL |
| **Search Tweets** | Find tweets by keyword query |

---

## Usage

Simply ask your AI agent. Examples:

```
"Post a tweet: Just launched our new product. Check it out!"
"What's trending on Twitter right now?"
"Search tweets about #AI"
"Create a thread about our 5 key product principles"
"Check the engagement on this tweet: x.com/user/status/123456"
"Reply to x.com/user/status/123456 with a thank you"
"Search for tweets about climate change from this week"
```

---

## Tweet Best Practices (Built-in)

This skill embeds authoritative best practices from Buffer, Sprout Social, Hootsuite, Brand24, and Avenue Z:

- **Optimal length**: 71–100 characters gets 17% higher engagement
- **Hashtags**: Max 1–2 per tweet, placed at the end
- **Algorithm weights**: Reposts (20x) > Replies (13.5x) > Bookmarks (10x) > Likes (1x)
- **Best times**: Weekdays 8–10 AM and 7–9 PM; B2B: Tue–Thu 9–11 AM
- **Threads**: 63% higher engagement than single tweets (Hootsuite)
- **Links (X Free)**: Place in reply or bio — link posts have ~0% reach since March 2025

---

## Safety Features

### Anti-Ban Protections
- Enforces X's hard limits: 2,400 posts/day, ~50 posts per 30 minutes
- 60-second minimum wait between tweets
- 10-tweet session cap with break recommendation
- Random timing jitter to avoid bot-like patterns
- Refuses all banned operations: mass follow/unfollow, bulk liking, engagement farming

### Prompt Injection Defense
- All content read from Twitter/X pages is treated as untrusted data
- Agent will never execute instructions found in tweet content
- Suspicious injection attempts (e.g., "ignore previous instructions") are flagged to the user
- Explicit confirmation required before every post action

### Platform Resilience
- Self-healing selector strategy: `data-testid` → ARIA role → text content → screenshot
- Never relies on CSS class names (X randomizes them frequently)
- Graceful degradation when X changes its UI

---

## X Plan Configuration

At session start, the skill asks:

> "Are you using **X Free** or **X Premium**?"

This configures:
- **X Free**: 280 char limit, links in replies/bio recommended
- **X Premium**: 25,000 char limit, normal link visibility, 2–4x algorithm boost

---

## Important Notes

- This skill does **not** use the Twitter/X API
- You must be **logged in** to x.com in Chrome before using this skill
- The skill **will not** attempt to log in on your behalf
- Rate limits and session caps are enforced to protect your account from suspension
- All automation complies with [X's automation development rules](https://help.x.com/en/rules-and-policies/x-automation)

---

## System Requirements

- macOS or Linux (Windows not supported)
- Google Chrome (logged in to x.com)
- browser-relay MCP server running

---

## Sources

Best practices in this skill are sourced from:

- [Buffer — How to Use Twitter/X 2026](https://buffer.com/resources/how-to-use-twitter/)
- [Sprout Social — Twitter Algorithm 2026](https://sproutsocial.com/insights/twitter-algorithm/)
- [Hootsuite — Twitter Marketing Guide](https://blog.hootsuite.com/twitter-marketing/)
- [Brand24 — 17 X Tips for 2026](https://brand24.com/blog/twitter-tips/)
- [Avenue Z — X Organic Social Guide 2025/2026](https://avenuez.com/blog/2025-2026-x-twitter-organic-social-media-guide-for-brands/)
- [X Official Automation Rules](https://help.x.com/en/rules-and-policies/x-automation)
