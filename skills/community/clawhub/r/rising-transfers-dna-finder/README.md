# RT DNA Finder

> Find cheaper, style-matched alternatives to any footballer using AI vector search.

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.ai/leeleon/rising-transfers-dna-finder)
[![API](https://img.shields.io/badge/Powered%20by-Rising%20Transfers%20API-green)](https://api.risingtransfers.com)
[![Credits](https://img.shields.io/badge/Cost-10%20credits%2Fsearch-orange)](https://api.risingtransfers.com/pricing)

## What It Does

RT DNA Finder uses pgvector cosine similarity search across 2,000+ footballer profiles to find players with statistically similar playing styles — ranked by similarity percentage and sorted to highlight lower-value options first.

**Example queries:**
- "Find me players similar to Bellingham but cheaper"
- "Who are the DNA alternatives to Rodri?"
- "Give me style-matched options for Salah under €20M"

## Installation

```bash
claw skill install rt-dna-finder
```

Then set your API key:

```bash
claw config set env.RT_API_KEY your_key_here
```

Get your free API key at [api.risingtransfers.com](https://api.risingtransfers.com).

## Setup

1. Register at [api.risingtransfers.com](https://api.risingtransfers.com) — free, no credit card required
2. Copy your API key from the Developer Dashboard
3. Set it in OpenClaw: `claw config set env.RT_API_KEY rt_sk_your_key`
4. Ask OpenClaw: "Find me players similar to Bellingham"

## Pricing

| Plan | Price | DNA Searches/Day |
|------|-------|-----------------|
| Free | $0 | 2 searches/day |
| Pro | $29/mo | 50 searches/day |
| Business | $99/mo | 250 searches/day |

Each DNA search costs 10 credits. [View full pricing →](https://api.risingtransfers.com/pricing)

## Example Output

```
DNA Alternatives to Jude Bellingham (Real Madrid)

| Rank | Player          | Club            | Similarity | Value  | vs Bellingham |
|------|-----------------|-----------------|-----------|--------|---------------|
| 1    | Brenden Aaronson | Union Berlin   | 89%        | €12M   | €68M cheaper  |
| 2    | Alexis Mac Allister | Liverpool  | 87%        | €55M   | €25M cheaper  |
| 3    | Ibrahim Sangaré | Nottm Forest    | 85%        | €30M   | €50M cheaper  |
```

## Privacy & Security

- Only the player name is sent to `api.risingtransfers.com`
- Your API key is stored locally in OpenClaw config
- No conversation history or personal data is transmitted
- See [Rising Transfers Privacy Policy](https://risingtransfers.com/privacy)

## Support

- Issues: [github.com/LeoandLeon/rising-transfers-clawhub-skills/issues](https://github.com/LeoandLeon/rising-transfers-clawhub-skills/issues)
- API docs: [api.risingtransfers.com/docs](https://api.risingtransfers.com/docs)
- Email: api@risingtransfers.com

## License

MIT
