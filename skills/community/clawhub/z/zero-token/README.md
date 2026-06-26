## Has Your Agent Ever Gone Silent?

API balance ran out. DeepSeek hit rate limit. OpenAI went down. Your agent was 80% done — then silence.

Your users don't understand infrastructure. They just know "it broke again." Three strikes and they're gone.

---

## What Zero Token Does

Not a "backup plan." Not a "degraded fallback." It's **invisible takeover**.

The second your main model dies, 13 free LLMs are already running. Same agent personality. Same decisions. Same voice. Your users won't even notice the switch.

**$0. Zero downtime. Zero detection.**

---

## Two Lines. One Minute.

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

[Free-Way](https://github.com/GoDiao/Free-Way) gateway aggregates 13+ free LLM providers behind a single `/v1` endpoint. OpenClaw uses it as fallback. Main model fails → auto switch. Your agent keeps going.

---

## Two Modes

| Mode | Trigger | Result |
|------|---------|--------|
| 🆓 Free Mode | No paid API key | Agent runs entirely on free models, full SOUL personality |
| 🛡️ Takeover Mode | Main model down / tokens depleted | Auto-switch to free providers, work continues seamlessly |

---

## Full Transparency

Zero Token never hides the switch. When fallback activates, your agent is running on free-tier providers — not your primary model. Every provider has its own privacy policy and data retention. **Review each provider's terms before routing sensitive data.** The setup script shows exactly which providers are configured. You control which keys you add.

> 💡 This is a transparent, user-controlled failover. You hold the keys. You decide the providers.

---

## Free Isn't Junk

Raw free model output is meh. But layer `::GENE{}` behavioral DNA on top — same personality, same reasoning, same voice. Users can't tell if DeepSeek V4 Pro or Llama 3.3 70B is running.

---

## Why It's Free

Free-Way + Zero Token are open source. Every provider gives a free tier:

| Provider | Free Limit | Best Model |
|----------|-----------|------------|
| Groq | 1000 req/day | Llama 3.3 70B |
| Gemini Flash | 1500 req/day | Gemini 2.5 Flash |
| Cerebras | 1700 req/day | Llama 3.3 70B |
| Cloudflare | 10k neurons/day | Llama 3.1 8B |
| OpenRouter | 200 req/day | Multiple free models |
| Mistral | 1 req/sec | Mistral Small |
| Cohere | 20 req/min | Command R+ |
| NVIDIA NIM | Free tier | Llama 3.3 70B |

Each key takes 30 seconds to register. Setup walks you through it.

---

## The Comparison

| | Typical Setup | Zero Token |
|---|---|---|
| Model Cost | $0.14–$15.00/M tokens | **$0.00** |
| Outage Handling | Dead in the water | Invisible failover |
| Backup Models | 0 | 13+ |
| Agent Personality | Lost on fallback | Always consistent |
| Setup Time | Half a day (load balancing) | 1 minute |

---

## When to Upgrade

Zero Token keeps you online. For the best output quality — DeepSeek V4 Pro + full genome, at 3% of Opus price:

```bash
openclaw skills install poor-mans-opus
```

---

## Links

- [Free-Way Gateway](https://github.com/GoDiao/Free-Way)
- [I-Lang Protocol](https://ilang.ai)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Poor Man's Opus](https://github.com/mtmpss/poor-mans-opus)
- [ClawHub](https://clawhub.ai/mtmpss/zero-token)
