---
name: rising-transfers-transfer-intel
description: Real-time football transfer intelligence — rumours, credibility scores, and multi-source verification
version: "1.0.0"
homepage: https://github.com/LeoandLeon/rising-transfers-clawhub-skills
metadata:
  clawdbot:
    emoji: "📡"
    requires:
      env: ["RT_API_KEY"]
    primaryEnv: "RT_API_KEY"
---

# RT Transfer Intel — Football Transfer Intelligence

Get real-time transfer rumour data aggregated from multiple sources, with AI-powered credibility assessment. Free tier includes trending topics with no credits required.

---

## External Endpoints

| Endpoint | Method | Data Sent | Purpose |
|----------|--------|-----------|---------|
| `https://api.risingtransfers.com/api/v1/intelligence/hot-topics` | GET | None | Trending transfers (free, 0 credits) |
| `https://api.risingtransfers.com/api/v1/intelligence/transfer` | POST | `{ "name": "<player_name>" }` | Player transfer rumour detail (3 credits) |
| `https://api.risingtransfers.com/api/v1/intel/verify` | GET | `?q=<player>+to+<club>` | Truth Meter credibility score (1–5 credits) |

No data is sent to any other endpoint. No conversation history is transmitted.

---

## Security & Privacy

- **What leaves your machine**: Player name and/or club name from your query only
- **What does NOT leave your machine**: Conversation history, other skills, local files, or your API key value (sent as HTTP header only)
- **Authentication**: `RT_API_KEY` is sent as `X-RT-API-Key` header to `api.risingtransfers.com` only
- **Hot topics** (trending list) can be fetched without any API key at 0 credits
- **Data retention**: Query logs kept for rate limiting (max 24 hours). No personal data stored

---

## Model Invocation Note

This skill may be invoked autonomously when you ask about transfer news, rumours, or whether a specific transfer is likely to happen. To disable autonomous invocation: `claw config set skill.auto-discover false`. Credit consumption applies only to authenticated (non-anonymous) calls for detailed intelligence.

---

## Trust Statement

By using this skill, player and club names from your queries are sent to Rising Transfers (`api.risingtransfers.com`). Rising Transfers aggregates public transfer rumour data — no sensitive or personal information is involved. Only install this skill if you trust Rising Transfers with those search terms.

---

## Trigger

When the user asks about:
- Transfer rumours for a specific player or club
- Whether a transfer deal is likely or credible
- Latest hot transfer topics or trending deals
- Verifying if a transfer story is genuine

Examples:
- "What are the latest transfer rumours for Mbappé?"
- "Is the Osimhen to Chelsea deal likely to happen?"
- "What are the hottest transfer stories right now?"
- "How credible is the Arsenal to Gyökeres link?"

---

## Instructions

### Step 1 — Determine query type

Identify which of three modes to use:

| User Intent | Mode | Credits |
|-------------|------|---------|
| "What's trending?" / general hot topics | **Hot Topics** | 0 |
| Specific player rumours | **Transfer Detail** | 3 |
| "How likely is [player] to [club]?" | **Truth Meter** | 1–5 |

---

### Mode A: Hot Topics (0 credits, no key required)

Call:
```
GET https://api.risingtransfers.com/api/v1/intelligence/hot-topics
Headers: X-RT-API-Key: <RT_API_KEY>   (optional for free topics)
```

Present the top 10 results sorted by heat_score:
- Player name → Destination club
- Heat level (🔥🔥🔥 = high, 🔥 = low)
- Last updated timestamp

---

### Mode B: Transfer Detail (3 credits)

Call:
```
POST https://api.risingtransfers.com/api/v1/intelligence/transfer
Headers:
  X-RT-API-Key: <RT_API_KEY>
  Content-Type: application/json
Body: { "name": "<player_name>", "team": "<team_if_mentioned>" }
```

Present:
- Sources citing the rumour (e.g. "Fabrizio Romano", "Sky Sports")
- Transfer probability estimate (%)
- Social media sentiment breakdown
- Timeline: when first reported, latest update
- Key facts: reported fee, contract length, competing clubs

---

### Mode C: Truth Meter (1–5 credits)

Call:
```
GET https://api.risingtransfers.com/api/v1/intel/verify?q=<player>+to+<club>
Headers: X-RT-API-Key: <RT_API_KEY>
```

Parse `audit.score` and `audit.verdict`, present as:

```
Truth Meter: [player] to [club]
Score: 74/100 — LIKELY
━━━━━━━━━━━━━━━━━━━━━

Source Authority:  32/40
Official Signals:  15/20
Progress Signals:  14/20
Market Heat:       13/20
Community Mood:    +3 (mostly believe it)
```

Include top evidence sources from `evidence.top_sources`.

---

### Error Handling

| Error | User Message |
|-------|-------------|
| 401 | "Your RT_API_KEY is invalid. Get one free at api.risingtransfers.com" |
| 403 Insufficient Credits | "Not enough credits for this query. Top up at api.risingtransfers.com/pricing" |
| 404 Player Not Found | "Player not found. Try the full name or add the current club name." |
| 429 Rate Limited | "Rate limit reached. Wait a moment or upgrade your plan for higher limits." |
| 5xx | "Rising Transfers API is temporarily unavailable. Please try again shortly." |

---

### Important: Do Not Fabricate

If the API returns no rumour data for a player, clearly state: "No active transfer rumours found for [player] in the Rising Transfers database." Do not invent rumour details or probability scores.

---

## Requirements

- **RT_API_KEY**: Rising Transfers API key. Register free at [api.risingtransfers.com](https://api.risingtransfers.com)
- Hot Topics mode works without a key (anonymous, limited results)
- **OpenClaw**: v0.8.0 or later
- **Network access**: Required

---

## Credit Usage

| Action | Credits |
|--------|---------|
| Hot Topics (trending list) | 0 — always free |
| Transfer Detail (specific player) | 3 credits |
| Truth Meter (credibility score) | 1 credit (anonymous) / 5 credits (full detail) |

Free tier: 10 hot-topic calls/day, 3 detailed queries/day.

---

## Author

risingtransfers — [api.risingtransfers.com](https://api.risingtransfers.com)
