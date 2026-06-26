# whatpeoplepayfor

Agent-first market intelligence API for the gig economy.

Monthly Fiverr dataset with **274 categories** and **17,000+ gig snapshots**, queryable via natural language or structured endpoints. Built for AI agents that need grounded market data.

## What it does

- **Natural language market analysis** — ask "What are the fastest-growing freelance categories?" and get structured answers with evidence
- **274 freelance categories** tracked monthly with revenue, order volume, and growth metrics
- **Pain point extraction** — discover what customers repeatedly complain about
- **Gig tracking** — follow individual gigs across months to spot trends
- **Focus system** — save and rerun analyses against new monthly data

## Install

```bash
clawhub install whatpeoplepayfor
```

## Setup

1. Sign up at [whatpeoplepayfor.com](https://whatpeoplepayfor.com)
2. Choose a plan ($19.90/mo or $99.90 lifetime)
3. Copy your API key
4. Set the environment variable:

```bash
export WPP_API_KEY="your_api_key_here"
```

## Usage

Once installed, your agent can ask market questions directly:

> "What are the fastest-growing freelance categories this month?"

> "Which pain points repeat most often in business plans?"

> "Help me find the strongest revenue opportunity in March"

## Requirements

- `WPP_API_KEY` — API key from [whatpeoplepayfor.com](https://whatpeoplepayfor.com)
- `curl` — for HTTP requests

## Links

- Website: [whatpeoplepayfor.com](https://whatpeoplepayfor.com)
- API docs: See SKILL.md for full endpoint reference

## License

MIT-0
