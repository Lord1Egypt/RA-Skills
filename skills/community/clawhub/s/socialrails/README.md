# SocialRails OpenClaw Skill

[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-purple)](https://openclaw.dev)

Manage your social media from chat using the SocialRails Public API.

## Quick Install

```bash
openclaw install socialrails
```

## Setup

1. **Get an API key** from [SocialRails Dashboard](https://socialrails.com/dashboard/settings) (requires Creator plan or above)

2. **Install the skill:**
   ```bash
   openclaw install socialrails
   ```

3. **Configure your API key:**
   ```bash
   openclaw config socialrails apiKey sr_live_your_key_here
   ```

## Commands

| Command | Description |
|---------|-------------|
| `schedule-post` | Schedule a social media post |
| `show-analytics` | View posting analytics |
| `generate-caption` | Generate AI content |
| `list-posts` | List your posts |
| `list-accounts` | List connected accounts |

## Examples

```text
> Schedule a tweet about our product launch for next Monday at 9am
> Show me analytics for the last 30 days
> Generate an Instagram caption for a photo of our new office
> List my scheduled posts
> What accounts do I have connected?
```

## Configuration

Configuration is stored in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "socialrails": {
      "apiKey": "sr_live_your_key_here",
      "baseUrl": "https://socialrails.com/api/v1"
    }
  }
}
```

## API Key Scopes

Your API key needs the right scopes for each command:

- `read` — list-posts, show-analytics, list-accounts
- `write` — schedule-post
- `ai` — generate-caption

For full access, create a key with all three scopes.

## Links

- [API Documentation](https://socialrails.com/documentation/api-overview)
- [OpenClaw Setup Guide](https://socialrails.com/documentation/openclaw-setup)
- [SocialRails Dashboard](https://socialrails.com/dashboard)
