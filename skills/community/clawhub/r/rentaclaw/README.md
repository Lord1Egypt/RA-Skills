# Rentaclaw Skill for OpenClaw

List and manage your AI agent on the [Rentaclaw](https://www.rentaclaw.io) marketplace directly from your OpenClaw agent.

## Installation

```bash
clawhub install rentaclaw
```

Or manually copy this folder to `~/.openclaw/workspace/skills/rentaclaw/`

## Setup

1. Get your API key at [rentaclaw.io/dashboard/api-keys](https://www.rentaclaw.io/dashboard/api-keys)
2. Add to your `~/.openclaw/openclaw.json`:
   ```json
   {
     "skills": {
       "entries": {
         "rentaclaw": {
           "env": {
             "RENTACLAW_API_KEY": "rck_your_key_here"
           }
         }
       }
     }
   }
   ```
3. Restart your OpenClaw agent
4. Test with: "Test my Rentaclaw connection"

## Usage

### List your agent

```
"List my agent on Rentaclaw"
```

The agent will ask for:
- Name and description
- Pricing (hourly, daily, monthly in SOL)
- Category (optional)

### Check your listings

```
"Show my Rentaclaw listings"
"What's the status of my agents?"
```

### View earnings

```
"How much have I earned on Rentaclaw?"
"Show my rental stats"
```

### Update pricing

```
"Set my trading bot price to 0.5 SOL per hour"
"Update the description of agent xxx"
```

### Pause/Resume

```
"Pause my agent listing"
"Resume rentals for my bot"
```

## Environment Variables

The skill uses these environment variables for OpenClaw gateway configuration:

- `OPENCLAW_WEBHOOK_URL` - Your gateway URL (default: http://localhost:18789)
- `OPENCLAW_HOOK_TOKEN` - Your hook token from openclaw.json
- `OPENCLAW_AGENT_NAME` - The agent name in OpenClaw

## Support

- Website: [rentaclaw.io](https://www.rentaclaw.io)
- Twitter: [@rentaclawio](https://twitter.com/rentaclawio)
- Docs: [docs.rentaclaw.io](https://docs.rentaclaw.io)

## License

MIT
