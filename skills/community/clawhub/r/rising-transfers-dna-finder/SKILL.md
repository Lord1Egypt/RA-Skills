---
name: rising-transfers-dna-finder
description: Find cheaper, style-matched footballer alternatives using Rising Transfers vector DNA search
version: "1.0.0"
homepage: https://github.com/LeoandLeon/rising-transfers-clawhub-skills
metadata:
  clawdbot:
    emoji: "🧬"
    requires:
      env: ["RT_API_KEY"]
    primaryEnv: "RT_API_KEY"
---

# RT DNA Finder — Football Player Similarity Search

Find statistically similar footballers at lower market values. Powered by the Rising Transfers Intelligence API using pgvector cosine similarity across 2,000+ player profiles.

---

## External Endpoints

| Endpoint | Method | Data Sent | Purpose |
|----------|--------|-----------|---------|
| `https://api.risingtransfers.com/api/v1/intelligence/dna-search` | POST | `{ "name": "<player_name>" }` | DNA vector similarity search |
| `https://api.risingtransfers.com/api/v1/intelligence/player` | POST | `{ "name": "<player_name>" }` | Player profile lookup (optional enrichment) |

No data is sent to any other endpoint. No data is stored locally.

---

## Security & Privacy

- **What leaves your machine**: Only the player name(s) you provide in the query
- **What does NOT leave your machine**: Conversation history, other installed skills, local files, API keys (the key is sent as an HTTP header, never in the request body or logs)
- **Data retention by Rising Transfers**: API calls are logged for rate limiting and billing. Player name queries are not stored beyond 24 hours. See [privacy policy](https://risingtransfers.com/privacy)
- **Authentication**: Your `RT_API_KEY` is sent as `X-RT-API-Key` header on every request to `api.risingtransfers.com` only

---

## Model Invocation Note

This skill may be invoked autonomously by OpenClaw when you ask about finding similar players, cheaper alternatives, or DNA-matched footballers. You can disable autonomous invocation by setting `skill.auto-discover false` in your OpenClaw config. Every API call consumes credits from your Rising Transfers account (10 credits per DNA search).

---

## Trust Statement

By using this skill, the player name you query is sent to Rising Transfers (`api.risingtransfers.com`). Only install this skill if you trust Rising Transfers with that information. Rising Transfers is a football intelligence platform — no financial, personal, or sensitive data is involved in these queries.

---

## Trigger

When the user asks to:
- Find similar players to a named footballer
- Find cheaper alternatives to a specific player
- Find DNA-matched or style-matched player options
- Identify replacement candidates for a player

Examples:
- "Find me players similar to Bellingham but cheaper"
- "Who are the DNA alternatives to Rodri?"
- "Give me a style-matched backup to Salah under €20M"

---

## Instructions

1. Extract the target player name from the user's request. If a team is mentioned, note it for disambiguation.

2. Call the DNA search endpoint:
   ```
   POST https://api.risingtransfers.com/api/v1/intelligence/dna-search
   Headers:
     X-RT-API-Key: <RT_API_KEY>
     Content-Type: application/json
   Body:
     { "name": "<player_name>", "team": "<team_name_if_provided>" }
   ```

3. If the response contains `error: "INSUFFICIENT_CREDITS"`, inform the user their Rising Transfers credits are exhausted and direct them to `api.risingtransfers.com` to top up.

4. If the response contains `error: "PLAYER_NOT_FOUND"`, ask the user to clarify the player name or provide the current club.

5. Parse the `data.alternatives` array from the response. For each alternative player, present:
   - Player name and current club
   - DNA similarity percentage (e.g. "91% similar")
   - Market value and difference vs target (e.g. "€65M cheaper")
   - Position and key playing style tags

6. Present results as a ranked table, most similar first. Example format:

   | Rank | Player | Club | Similarity | Value | Saving vs [Target] |
   |------|--------|------|-----------|-------|-------------------|
   | 1 | Name | Club | 91% | €15M | €65M cheaper |

7. After the table, offer to dive deeper: "Want a full scout report on any of these players?"

8. Do not fabricate statistics. If the API returns no alternatives, say so clearly and suggest the user try a different player.

---

## Error Handling

| Error | User Message |
|-------|-------------|
| 401 Unauthorized | "Your RT_API_KEY is invalid or expired. Get a key at api.risingtransfers.com" |
| 403 Insufficient Credits | "You've used all your DNA search credits. Top up at api.risingtransfers.com" |
| 404 Player Not Found | "Player not found. Try the full name (e.g. 'Jude Bellingham') or add the club name." |
| 429 Rate Limited | "Too many requests. Please wait a moment before trying again." |
| 5xx Server Error | "Rising Transfers API is temporarily unavailable. Please try again in a few minutes." |

---

## Requirements

- **RT_API_KEY**: A valid Rising Transfers API key. Register for free at [api.risingtransfers.com](https://api.risingtransfers.com). Free tier includes 2 DNA searches per day.
- **OpenClaw**: v0.8.0 or later
- **Network access**: Required (calls `api.risingtransfers.com`)

---

## Credit Usage

| Action | Credits Consumed |
|--------|-----------------|
| DNA similarity search | 10 credits |
| Player profile enrichment (optional) | 1 credit |

Free tier: 2 DNA searches/day (20 credits/day total for this skill).
Pro tier ($29/mo): 50 DNA searches/day.

---

## Author

risingtransfers — [api.risingtransfers.com](https://api.risingtransfers.com)
