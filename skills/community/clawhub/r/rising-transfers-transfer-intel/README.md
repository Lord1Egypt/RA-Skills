# RT Transfer Intel

> Real-time football transfer intelligence with AI-powered credibility scoring.

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai/leeleon/rising-transfers-transfer-intel)
[![API](https://img.shields.io/badge/Powered%20by-Rising%20Transfers%20API-green)](https://api.risingtransfers.com)
[![Free Tier](https://img.shields.io/badge/Free%20tier-Hot%20Topics%20free-brightgreen)](https://api.risingtransfers.com/pricing)

## What It Does

Three modes in one skill:

1. **Hot Topics** — Get trending transfer rumours right now (free, no credits)
2. **Transfer Detail** — Deep-dive on a specific player's rumour: sources, probability, social sentiment
3. **Truth Meter** — AI credibility score for any transfer link (0–100 scale with verdict)

**Example queries:**
- "What are the hottest transfer stories right now?"
- "What are the latest rumours for Gyökeres?"
- "How likely is Osimhen to Chelsea?"

## Installation

```bash
claw skill install rt-transfer-intel
```

Set your API key (optional — hot topics work without it):

```bash
claw config set env.RT_API_KEY your_key_here
```

Get your free key at [api.risingtransfers.com](https://api.risingtransfers.com).

## Example Output

### Hot Topics

```
🔥 Trending Transfers — Updated 4 minutes ago

1. 🔥🔥🔥 Viktor Gyökeres → Arsenal         (Heat: 94)
2. 🔥🔥🔥 Khvicha Kvaratskhelia → PSG       (Heat: 91)
3. 🔥🔥   Evan Ferguson → Brighton (stay)   (Heat: 78)
...
```

### Truth Meter

```
Truth Meter: Gyökeres to Arsenal
Score: 81/100 — HIGHLY LIKELY ✅

Source Authority:   36/40   ████████████████████▌
Official Signals:   18/20   ██████████████████
Progress Signals:   16/20   ████████████████
Market Heat:        11/20   ███████████

Top Sources: Fabrizio Romano ✓, Sky Sports ✓, The Athletic ✓
Community: 78% believe it, 22% sceptical
```

## Pricing

| Plan | Price | Detailed Queries/Day | Truth Meter/Day |
|------|-------|---------------------|-----------------|
| Free | $0 | 3 queries | 10 verifications |
| Pro | $29/mo | 500 queries | 1,000 verifications |
| Business | $99/mo | 5,000 queries | Unlimited |

Hot Topics always free. [View full pricing →](https://api.risingtransfers.com/pricing)

## Privacy & Security

- Player/club names only are sent to `api.risingtransfers.com`
- Hot topics require no credentials at all
- No conversation history or local data transmitted
- [Privacy Policy](https://risingtransfers.com/privacy)

## Support

- Issues: [github.com/LeoandLeon/rising-transfers-clawhub-skills/issues](https://github.com/LeoandLeon/rising-transfers-clawhub-skills/issues)
- API docs: [api.risingtransfers.com/docs](https://api.risingtransfers.com/docs)
- Email: api@risingtransfers.com

## License

MIT
