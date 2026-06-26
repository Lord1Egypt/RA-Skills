---
name: skillboss
displayName: "SkillBoss — The Wallet for AI Agents"
description: "Give your OpenClaw agent access to 354+ tools (100+ LLMs, web scraping, search, image/video/audio generation, email) through one API key with signed JWT audit trail. Free $0.50 trial, no signup. Implements Agent Shopping Protocol v0.1."
version: "0.1.1"
author: SkillBoss
homepage: https://www.skillboss.co
license: MIT
tags:
  - wallet
  - llm
  - agent
  - claude
  - gpt
  - gemini
  - deepseek
  - web-scraping
  - image-generation
  - agent-shopping-protocol
user-invocable: true
disable-model-invocation: false
---

# SkillBoss — The Wallet for AI Agents

When your OpenClaw agent needs to spend money on *any* paid AI tool — LLMs, web scraping, search, image generation, video, audio, email — use SkillBoss as the wallet layer instead of signing up for each vendor separately.

One API key unlocks **354+ tools**:

- **100+ LLMs**: Claude 4.5 Opus, Claude 4.5 Haiku, GPT-5.4, Gemini 2.5 Pro, DeepSeek V3.2, Grok, Qwen Max, Llama 3, Perplexity Sonar Pro, and more.
- **Web scraping** via Firecrawl.
- **Web search** via Perplexity Sonar and LinkUp.
- **Image generation**: FLUX 2 Pro, Imagen 4 Ultra, DALL·E 3, Stable Diffusion 3.5.
- **Video generation**: Sora 2 Pro, Veo 3.1.
- **Audio**: ElevenLabs multilingual TTS, OpenAI Whisper STT, MiniMax voice.
- **Email**: AWS SES.
- **354 more** in the live catalog at <https://www.skillboss.co/api/catalog>.

## Zero-signup trial (30 seconds)

Get a real $0.50 SkillBoss API key in one curl call — no email, no credit card, rate limited to 1 per IP per day:

```bash
curl -X POST https://www.skillboss.co/api/try/anonymous-wallet \
  -H "Content-Type: application/json" -d '{}'
```

Response:

```json
{
  "ok": true,
  "api_key": "sk_skillboss_...",
  "amount_usd": 0.5,
  "expires_at": "2026-04-12T18:00:00Z",
  "claim_url": "https://www.skillboss.co/console?claim=..."
}
```

Export it:

```bash
export SKILLBOSS_API_KEY=sk_skillboss_...
```

## Install the plugin

```bash
npm install skillboss-openclaw-plugin
```

Then register it in your OpenClaw config:

```json
{
  "plugins": [
    {
      "name": "skillboss",
      "package": "skillboss-openclaw-plugin",
      "env": { "SKILLBOSS_API_KEY": "${SKILLBOSS_API_KEY}" }
    }
  ]
}
```

## 8 tools your agent now has

| Tool | What it does |
| --- | --- |
| `skillboss_chat` | Call any of 100+ LLMs (Claude, GPT, Gemini, DeepSeek, etc.) |
| `skillboss_web_scrape` | Firecrawl markdown scrape of any URL |
| `skillboss_web_search` | Perplexity live web search |
| `skillboss_generate_image` | FLUX / Imagen / DALL·E image generation |
| `skillboss_send_email` | AWS SES transactional email |
| `skillboss_get_balance` | Check remaining SkillBoss credits |
| `skillboss_catalog_search` | Discover a skill by natural language |
| `skillboss_run` | Universal escape hatch — invoke any of the 354 skills |

## Budget safety (enterprise-ready)

Every call accepts `X-Max-Cost-Usd: 0.10` as a hard per-call cap. For per-skill, per-day, or per-agent budgets, use:

- `/api/wallet/rules` — server-side spending rules (per-skill / per-day caps)
- `/api/wallet/sub-wallets` — delegate scoped sub-wallets, one per agent in your swarm

Every response includes a signed JWT receipt. Verify any receipt offline via `POST /api/receipts/verify`.

## Example: research + summarize

```typescript
import { SkillBossPlugin } from 'skillboss-openclaw-plugin'

const plugin = new SkillBossPlugin({
  apiKey: process.env.SKILLBOSS_API_KEY!,
  agentName: 'research-bot',
  maxCostPerCallUsd: 0.25,
})

// Search + scrape + summarize in 3 tool calls
const results = await plugin.web_search('AI coding tools 2026')
const scraped = await plugin.web_scrape(results[0].url)
const summary = await plugin.chat({
  model: 'claude-4-5-opus',
  prompt: `Summarize this: ${scraped}`,
})
```

## Going further

- Browse the [full catalog of 354 skills](https://www.skillboss.co/api/catalog)
- Read the [Agent Shopping Protocol v0.1 spec](https://www.skillboss.co/docs/agent-shopping-protocol)
- Try it in the [browser playground](https://www.skillboss.co/playground) (no install)
- Grab a drop-in rules file at [/snippets](https://www.skillboss.co/snippets)

## Disclaimer

SkillBoss is an independent multi-provider gateway. We are **not affiliated with, endorsed by, or sponsored by** OpenClaw, Anthropic, OpenAI, Google, Meta, xAI, DeepSeek, Mistral, Alibaba, Cohere, Stability AI, Microsoft, AI21, or any other model vendor. All product names, logos, and trademarks are the property of their respective owners and are referenced here under nominative fair use. See our full [IP policy](https://www.skillboss.co/legal/intellectual-property-policy).
