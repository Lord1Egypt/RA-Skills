---
id: tg-news-digest-lite
name: "Telegram News Digest (Lite)"
version: "1.0.0"
description: |
  Monitors public Telegram channels via web scraping (t.me/s/*), extracts new messages,
  generates AI-powered summaries, and delivers structured digests to your configured
  OpenClaw notification channel. Zero authentication required — just provide channel names.
author: "your-github-handle"
license: "MIT"
tags: ["telegram", "news-monitoring", "web-scraping", "ai-summarization", "digest", "russian", "english"]
category: "information-retrieval"
minOpenClawVersion: "2026.4.0"
runtime: "node20"
permissions:
  network: ["t.me", "*.t.me", "api.openai.com", "*.openrouter.ai", "*.deepinfra.com"]
  filesystem: ["./state", "./config.yaml"]
  env: ["OPENCLAW_GATEWAY_URL", "OPENCLAW_GATEWAY_TOKEN"]
---

# Telegram News Digest (Lite)

> 🤖 **Autonomous AI agent for monitoring public Telegram channels**  
> ✅ No Telegram API keys • ✅ No authentication • ✅ Zero-config startup • ✅ Works with any LLM provider

## 🎯 What Problem Does This Solve?

### Real-world scenario
You're a product manager tracking competitor announcements, a journalist monitoring breaking news, or a crypto trader watching market signals. Manually checking 10+ Telegram channels every hour is unsustainable. This skill automates the entire workflow:

```
[10 Telegram channels] 
        ↓
[Fetch new messages every 30 min]
        ↓
[Filter duplicates + detect novelty]
        ↓
[Generate AI summary: "Key facts in 3 bullets"]
        ↓
[Send digest to your Telegram/Discord/Email]
```

### Before vs After

| Task | Manual Approach | With tg-news-digest-lite |
|------|----------------|-------------------------|
| Check 10 channels | ~15 min/hour | 0 min (fully automated) |
| Detect new posts | Scroll + mental dedup | SHA256 hash comparison |
| Summarize content | Read + mentally condense | LLM generates structured bullets |
| Notify yourself | Copy-paste to chat | Auto-deliver to configured channel |
| Missed updates | High risk (human error) | Guaranteed (persistent state) |

## 🏗 How It Works: Architecture Deep Dive

### Data Flow Diagram
```mermaid
graph LR
    A[OpenClaw Cron/Heartbeat] --> B[run_digest_cycle]
    B --> C[Load config.yaml]
    B --> D[Initialize TelegramWebScraper]
    B --> E[Initialize StateManager]
    B --> F[Initialize Summarizer]
    
    C --> G[Channel list: durov, tjournal, roem...]
    
    D --> H[Fetch https://t.me/s/{channel}]
    H --> I[Parse HTML with Cheerio]
    I --> J[Extract message text + timestamp]
    J --> K[Generate SHA256 hash per message]
    
    E --> L[Load seen_hashes from state/seen_messages.json]
    K --> M[Filter: hash NOT IN seen_hashes]
    
    M --> N{New messages?}
    N -->|Yes| O[Send to Summarizer]
    N -->|No| P[Skip channel]
    
    O --> Q[LLM prompt: "Summarize these messages"]
    Q --> R[Parse JSON response: {summary, tags, sentiment}]
    
    R --> S[Format digest with markdown]
    S --> T[Send via ctx.send to notify_channel]
    
    K --> U[Update seen_hashes cache]
    U --> V[Save to state/seen_messages.json]
```

### Component Responsibilities

| Component | Responsibility | Key Design Decisions |
|-----------|---------------|---------------------|
| `TelegramWebScraper` | Fetch + parse t.me/s/* pages | • Uses `axios` with custom User-Agent to avoid bot detection<br>• Resilient HTML parsing: fallback selectors if Telegram changes structure<br>• Rate limiting: configurable delay between requests (default: 2000ms) |
| `StateManager` | Track which messages were already processed | • SHA256 hash of normalized text (case-insensitive, whitespace-trimmed)<br>• Rolling cache: keeps last 100 hashes per channel to bound memory<br>• Atomic JSON writes to prevent corruption on crash |
| `Summarizer` | Generate concise summaries via LLM | • OpenAI-compatible API (works with OpenRouter, DeepInfra, local Ollama)<br>• JSON-mode enforcement for structured output<br>• Fallback: returns raw messages if LLM is unavailable |
| `index.js` (tools) | Orchestrate the pipeline + expose CLI tools | • Three tools: `run_digest_cycle`, `configure_channels`, `get_status`<br>• Graceful error handling: continues processing other channels if one fails<br>• Token usage reporting for cost tracking |

## ⚙️ Configuration: Real Examples

### Basic Setup (30 seconds)
```yaml
# config.yaml
monitoring:
  channels:
    - "durov"                    # Pavel Durov's channel
    - "telegram"                 # Official Telegram News
    - "tjournal"                 # Russian tech media
    - "https://t.me/s/roem"      # Full URL format also supported
    - "@coindesk"                # With @ prefix — also works
  
  fetch_window: 20              # Check last 20 messages per channel (catch up on missed updates)
  rate_limit_ms: 2000           # Delay between requests to avoid IP throttling

digest:
  language: "en"                # Summary language: "en", "ru", "es", etc.
  max_tokens_per_channel: 300   # Limit summary length (~2-3 short paragraphs)
  format: "markdown"            # Output format: "markdown", "html", or "text"
  group_by: "time"              # Organize digest: "time" (chronological), "channel", or "none"
  notify_channel: "default"     # Where to send: "default", "telegram", "discord", "webhook"
  min_messages_for_summary: 2   # Don't summarize if <2 new messages (avoid noise)
```

### Advanced: Custom LLM Provider
```yaml
# If you use OpenRouter instead of default gateway:
# Set in ~/.openclaw/openclaw.json:
{
  "models": {
    "providers": {
      "openrouter": {
        "baseUrl": "https://openrouter.ai/api/v1",
        "apiKey": "${OPENROUTER_KEY}"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "openrouter/qwen/qwen3.5-35b" }
    }
  }
}
```

Then in `config.yaml`:
```yaml
digest:
  language: "en"
  # Skill automatically uses context.model.primary from OpenClaw
```

### Use Case: Crypto Trader Monitoring
```yaml
monitoring:
  channels:
    - "coindesk"
    - "theblock__"
    - "cryptobriefing"
    - "binance"
    - "elonmusk"  # For meme-coin signals 😅
  
  fetch_window: 50  # Deeper history for volatile markets
  rate_limit_ms: 3000  # Conservative to avoid blocks

digest:
  language: "en"
  max_tokens_per_channel: 200  # Ultra-concise for quick scanning
  format: "text"  # Plain text for SMS/Telegram compatibility
  group_by: "channel"  # Group by source for attribution
  min_messages_for_summary: 1  # Even single important message triggers alert
```

## ▶️ Usage Examples

### Run a Manual Check
```bash
# Check all configured channels
openclaw skills exec tg-news-digest-lite/run_digest_cycle

# Override channels for one-off check
openclaw skills exec tg-news-digest-lite/run_digest_cycle \
  --args '{"channels": ["durov", "https://t.me/s/roem"]}'

# Force re-fetch even if messages seem "seen" (debugging)
openclaw skills exec tg-news-digest-lite/run_digest_cycle \
  --args '{"force": true}'
```

### Manage Channel List Dynamically
```bash
# Add new channels
openclaw skills exec tg-news-digest-lite/configure_channels \
  --args '{"add": ["techcrunch", "wired"]}'

# Remove channels you no longer care about
openclaw skills exec tg-news-digest-lite/configure_channels \
  --args '{"remove": ["old-channel"]}'

# View current configuration
openclaw skills exec tg-news-digest-lite/get_status
```

**Example output of `get_status`:**
```json
{
  "tracked_channels": 7,
  "channels": ["durov", "telegram", "tjournal", "roem", "coindesk", "techcrunch", "wired"],
  "cache_entries": 342,
  "rate_limit_ms": 2000
}
```

### Sample Digest Output
When new messages are detected, you'll receive a formatted digest like:

```markdown
📰 **Telegram News Digest**
🕒 2026-04-28 14:30:00 UTC

🔹 **@durov** (3 msg)
• Telegram announces new bot API features for group management
• Privacy update: end-to-end encryption now available for group calls
• Q2 2026 roadmap teaser: "Something big coming in July"
🏷 privacy, api, roadmap

🔹 **@coindesk** (5 msg)
• Bitcoin holds $67K amid ETF inflow reports
• SEC delays decision on Ethereum futures ETF again
• New DeFi protocol raises $12M seed round
🏷 bitcoin, etf, defi, regulation

🔹 **@tjournal** (2 msg)
• Russian tech startups face new compliance requirements
• Yandex announces AI assistant integration across products
🏷 russia, startups, ai
```

## 🔄 Automation: Run on Schedule

### Option 1: OpenClaw Cron (Recommended)
Add to `~/.openclaw/openclaw.json`:
```json
{
  "cron": [
    {
      "id": "tg-digest-morning",
      "schedule": "0 9 * * *",
      "tool": "tg-news-digest-lite/run_digest_cycle",
      "isolate": true,
      "description": "Morning news digest at 9 AM"
    },
    {
      "id": "tg-digest-evening",
      "schedule": "0 18 * * *",
      "tool": "tg-news-digest-lite/run_digest_cycle",
      "isolate": true,
      "description": "Evening recap at 6 PM"
    }
  ]
}
```

### Option 2: Heartbeat Integration
Create `~/workspace/HEARTBEAT.md`:
```markdown
## Telegram News Check
- Run `tg-news-digest-lite/run_digest_cycle` every 30 minutes
- Only send digest if new messages detected
- Use `qwen3.5-35b` for summarization, `gpt-4o-mini` for routing
```

Then configure heartbeat in `openclaw.json`:
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",
        "lightContext": true,
        "isolatedSession": true
      }
    }
  }
}
```

## ⚠️ Limitations & Edge Cases (Be Aware)

### What Works ✅
- Public channels with `https://t.me/s/{username}` accessible in browser
- Text-only messages (including formatted text: bold, italic, links)
- Channels with 1–1000+ messages (pagination handled internally)
- Multi-language content (LLM handles translation if configured)

### What Doesn't Work ❌
- Private channels or groups (require authentication — use `tg-news-digest` Pro version)
- Messages with only media (no text) — skipped silently
- Channels that block scrapers via Cloudflare (rare, but possible)
- Very high-frequency channels (>100 msgs/hour) — may hit rate limits

### Known Quirks 🔧
| Symptom | Likely Cause | Workaround |
|---------|-------------|------------|
| "Канал не найден" (Channel not found) | Channel is private or username changed | Verify URL works in browser: `https://t.me/s/username` |
| Empty digest despite new messages | `min_messages_for_summary` too high | Lower to `1` or check `fetch_window` size |
| LLM returns malformed JSON | Model doesn't support `response_format: json_object` | Switch to `qwen3.5-35b`, `claude-3.5`, or `gpt-4o` |
| Repeated messages in digest | State file corrupted or deleted | Delete `state/seen_messages.json` to reset cache |
| Slow execution (>30s) | Many channels + high `fetch_window` | Reduce `fetch_window` or increase `rate_limit_ms` |

## 🛡️ Security & Privacy Considerations

### Data Flow Transparency
```
Your machine 
  → HTTPS GET to t.me/s/{channel} (public webpage)
  → Local text extraction + hashing
  → LLM API call (only message text, no metadata)
  → Digest sent to your configured channel
```

**No data leaves your control except:**
1. Public Telegram webpage requests (same as opening in browser)
2. Message text sent to your chosen LLM provider (configurable)

### Best Practices
- ✅ Run on trusted infrastructure (your laptop, private server)
- ✅ Use `isolate: true` in cron jobs to contain context growth
- ✅ Rotate `OPENCLAW_GATEWAY_TOKEN` periodically if using remote gateway
- ✅ Monitor `state/seen_messages.json` size (auto-truncated to 100 hashes/channel)

### What This Skill Does NOT Do
- ❌ Does not store Telegram credentials (none required)
- ❌ Does not forward raw messages to third parties
- ❌ Does not modify Telegram content in any way
- ❌ Does not interact with Telegram APIs (only public web pages)

## 📊 Performance Characteristics

### Resource Usage (Typical Run)
| Metric | Value | Notes |
|--------|-------|-------|
| Execution time | 15–45 seconds | Depends on #channels and network latency |
| Memory footprint | ~50–150 MB | Node.js + Cheerio + LLM response buffering |
| Network requests | 1 per channel + 1 LLM call | With 2s rate limit between Telegram requests |
| Token consumption | ~200–800 tokens/channel | For summarization only (not raw messages) |

### Cost Estimate (Using OpenRouter)
Assuming `qwen/qwen3.5-35b` at $1.30/1M output tokens:
```
10 channels × 300 tokens × $1.30/1M = $0.0039 per run
Hourly execution (24×) = ~$0.09/day = ~$2.70/month
```

> 💡 Tip: Use cheaper models (`gpt-4o-mini`, `qwen2.5-7b`) for summarization if cost-sensitive.

## 🐛 Troubleshooting Guide

### Error: `Skill execution failed: Network timeout`
```bash
# Check your internet connection
ping t.me

# Increase timeout in config.yaml
monitoring:
  rate_limit_ms: 5000  # More conservative

# Test scraper directly
node -e "
  import('./src/scraper.js').then(m => {
    const s = new m.TelegramWebScraper({rate_limit_ms: 1000}, console);
    s.fetchChannelMessages('durov', 5).then(console.log);
  });
"
```

### Error: `LLM response parse failed`
```bash
# Check which model is being used
openclaw config get agents.defaults.model.primary

# Test LLM connectivity manually
curl -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen/qwen3.5-35b","messages":[{"role":"user","content":"test"}]}' \
  https://your-gateway/v1/chat/completions

# Fallback: switch to a model known to support JSON mode
# Update ~/.openclaw/openclaw.json:
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-3.5-sonnet" }
    }
  }
}
```

### Debug Mode: See Internal Logs
```bash
# Enable verbose logging
export DEBUG=tg-news:*
openclaw skills exec tg-news-digest-lite/run_digest_cycle --args '{"channels":["durov"]}'

# Or check OpenClaw logs
openclaw logs --grep "tg-news" --tail 50
```

### Reset State (Start Fresh)
```bash
# Backup then delete state
mv ~/.openclaw/skills/tg-news-digest-lite/state/seen_messages.json \
   ~/.openclaw/skills/tg-news-digest-lite/state/seen_messages.json.bak

# Next run will treat all messages as "new"
```

## 🔄 Upgrading from Older Versions

### v0.x → v1.0.0 Breaking Changes
- State file format changed: now uses SHA256 hashes instead of raw text
- Migration: automatic on first run (old entries marked as "seen")
- Config key renamed: `telegram_channels` → `monitoring.channels`

### Upgrade Steps
```bash
# 1. Backup your config
cp ~/.openclaw/skills/tg-news-digest-lite/config.yaml ~/backup-config.yaml

# 2. Update the skill
openclaw skills update tg-news-digest-lite

# 3. Verify config structure
openclaw skills exec tg-news-digest-lite/get_status

# 4. (Optional) Migrate channel list format if needed
```

## 🤝 Contributing & Feedback

Found a bug? Have a feature request?

1. Check existing issues: https://github.com/your-org/tg-news-digest-lite/issues
2. For HTML parsing issues: include the raw HTML snippet (use `--debug` flag)
3. For LLM issues: specify your model provider and version
4. Submit PRs with tests for new channel formats

## 📜 License

MIT License — use freely in personal and commercial projects.  
See [LICENSE](./LICENSE) for details.

---

*Built with ❤️ for the OpenClaw community.  
Questions? Open an issue or ping @your-handle on Discord.*
```