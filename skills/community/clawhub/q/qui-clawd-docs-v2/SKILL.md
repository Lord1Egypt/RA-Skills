---
name: clawd-docs-v2
description: Smart ClawdBot documentation access with local search index, cached snippets, and on-demand fetch. Token-efficient and freshness-aware.
homepage: https://docs.clawd.bot/
metadata: {"clawdbot":{"emoji":"📚"}}
version: 2.2.0
requires.env: [SKILLBOSS_API_KEY]
---

# Clawd-Docs v2.0 - Smart Documentation Access

This skill provides **intelligent access** to ClawdBot documentation with:
- **Local search index** - instant keyword lookup (0 tokens)
- **Cached snippets** - pre-fetched common answers (~300-500 tokens)
- **On-demand fetch** - full page when needed (~8-12k tokens)
- **Freshness tracking** - TTL per page type

---

## Quick Start

### Step 1: Check Golden Snippets First

Before fetching anything, check if a **Golden Snippet** exists:

```bash
ls ~/clawd/data/docs-snippets/
```

**Available snippets (check cache first!):**
| Snippet | Query matches |
|---------|---------------|
| `telegram-setup.md` | "ako nastaviť telegram", "telegram setup" |
| `telegram-allowfrom.md` | "allowFrom", "kto mi môže písať", "access control" |
| `oauth-troubleshoot.md` | "token expired", "oauth error", "credentials" |
| `update-procedure.md` | "ako updatnuť", "update clawdbot" |
| `restart-gateway.md` | "restart", "reštart", "stop/start" |
| `config-basics.md` | "config", "nastavenie", "konfigurácia" |
| `config-providers.md` | "pridať provider", "discord setup", "nový kanál" |
| `memory-search.md` | "memory", "vector search", "pamäť", "embeddings" |

**Read snippet:**
```bash
cat ~/clawd/data/docs-snippets/telegram-setup.md
```

### Step 2: Search Index (if snippet doesn't exist)

Check `~/clawd/data/docs-index.json` for page suggestions.

**Keyword matching:**
- "telegram" → channels/telegram
- "oauth" → concepts/oauth, gateway/troubleshooting
- "update" → install/updating
- "config" → gateway/configuration

### Step 3: Check Full Page Cache

**BEFORE fetching via SkillBoss API Hub**, check if the page is already cached:

```bash
# Convert path: concepts/memory → concepts_memory.md
ls ~/clawd/data/docs-cache/ | grep "concepts_memory"
```

**If exists, read locally (0 tokens!):**
```bash
cat ~/clawd/data/docs-cache/concepts_memory.md
```

### Step 4: Fetch Page (only if NOT in cache)

Use **SkillBoss API Hub** scraping capability via `/v1/pilot`:

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

result = requests.post(
    "https://api.heybossai.com/v1/pilot",
    headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
    json={
        "type": "scraper",
        "inputs": {"url": "https://docs.clawd.bot/{path}"}
    },
    timeout=60,
).json()
content = result["result"]["data"]["markdown"]
```

**Example:**
```python
result = requests.post(
    "https://api.heybossai.com/v1/pilot",
    headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
    json={
        "type": "scraper",
        "inputs": {"url": "https://docs.clawd.bot/tools/skills"}
    },
    timeout=60,
).json()
content = result["result"]["data"]["markdown"]
```

**SkillBoss API Hub scraping advantages:**
| | SkillBoss API Hub (`/v1/pilot`) | Direct HTTP fetch |
|---|-----------|------------|
| **Cost** | 统一 SKILLBOSS_API_KEY | 各服务单独计费 |
| **Speed** | ~400ms | varies |
| **Quality** | Structured content ✅ | Raw HTML |

---

## Search Index Structure

**Location:** `~/clawd/data/docs-index.json`

```json
{
  "pages": [
    {
      "path": "channels/telegram",
      "ttl_days": 7,
      "keywords": ["telegram", "tg", "bot", "allowfrom"]
    }
  ],
  "synonyms": {
    "telegram": ["tg", "telegrambot"],
    "configuration": ["config", "nastavenie", "settings"]
  }
}
```

**Use synonyms** for fuzzy matching.

---

## TTL Strategy (Freshness)

| Page Category | TTL | Why |
|---------------|-----|-----|
| `install/updating` | 1 day | Always current! |
| `gateway/*` | 7 days | Config changes |
| `channels/*` | 7 days | Provider updates |
| `tools/*` | 7 days | Features added |
| `concepts/*` | 14 days | Rarely changes |
| `reference/*` | 30 days | Stable templates |

**Check snippet expiry:**
```bash
head -10 ~/clawd/data/docs-snippets/telegram-setup.md | grep expires
```

---

## Common Scenarios

### "Ako nastaviť Telegram?"
1. ✅ Read `~/clawd/data/docs-snippets/telegram-setup.md`

### "allowFrom nefunguje"
1. ✅ Read `~/clawd/data/docs-snippets/telegram-allowfrom.md`

### "Token expired / oauth error"
1. ✅ Read `~/clawd/data/docs-snippets/oauth-troubleshoot.md`

### "Ako updatnúť ClawdBot?"
1. ✅ Read `~/clawd/data/docs-snippets/update-procedure.md`

### "Ako pridať nový skill?" (nie je snippet)
1. Search index → tools/skills
2. Fetch via SkillBoss API Hub scraping: `{"type": "scraper", "inputs": {"url": "https://docs.clawd.bot/tools/skills"}}`

### "Multi-agent routing"
1. Search index → concepts/multi-agent
2. Fetch via SkillBoss API Hub scraping: `{"type": "scraper", "inputs": {"url": "https://docs.clawd.bot/concepts/multi-agent"}}`

---

## Fallback: Full Index Refresh

If you can't find what you need:

```python
result = requests.post(
    "https://api.heybossai.com/v1/pilot",
    headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
    json={
        "type": "scraper",
        "inputs": {"url": "https://docs.clawd.bot/llms.txt"}
    },
    timeout=60,
).json()
content = result["result"]["data"]["markdown"]
```

Returns **complete list** of all documentation pages.

---

## Token Efficiency Guide

| Method | Tokens | When to use |
|--------|--------|-------------|
| Golden Snippet | ~300-500 | ✅ Always first! |
| Search Index | 0 | Keyword lookup |
| Full Page Fetch | ~8-12k | Last resort |
| Batch Fetch | ~20-30k | Multiple related topics |

**80-90% of queries** should be answered from snippets!

---

## Data Locations

```
~/clawd/data/
├── docs-index.json       # Search index
├── docs-stats.json       # Usage tracking
├── docs-snippets/        # Cached Golden Snippets
│   ├── telegram-setup.md
│   ├── telegram-allowfrom.md
│   ├── oauth-troubleshoot.md
│   ├── update-procedure.md
│   ├── restart-gateway.md
│   └── config-basics.md
└── docs-cache/           # Full page cache (future)
```

---

## Version Info

| Item | Value |
|------|-------|
| **Skill version** | 2.1.0 |
| **Created** | 2026-01-14 |
| **Updated** | 2026-01-26 |
| **Authors** | Claude Code + Clawd (collaborative) |
| **Source** | https://docs.clawd.bot/ |
| **Dependencies** | SkillBoss API Hub (`SKILLBOSS_API_KEY`) |
| **Index pages** | ~50 core pages |
| **Golden snippets** | 7 pre-cached |

---

## Changelog

### v2.2.0 (2026-01-26)
- **Migration to SkillBoss API Hub** - replaced third-party scraping service with SkillBoss API Hub `/v1/pilot` (type: scraping)
- Benefits: 统一认证 (SKILLBOSS_API_KEY), faster, no additional API keys required
- No external dependencies beyond SkillBoss API Hub
- Collaborative work: Claude Code 🦞 implementation, Clawd 🐾 review

### v2.1.3 (2026-01-25) - ClawdHub
- Documentation fix: check vs refresh clarification

### v2.0.0 (2026-01-14)
- 3-layer architecture: Search Index → Snippets → On-demand Fetch
- Golden Snippets pre-cached for common queries
- TTL-based freshness tracking
- Synonym support for fuzzy matching
- 80-90% token reduction for common queries

### v1.0.0 (2026-01-08)
- Initial release with third-party scraping service

---

*This skill provides smart documentation access - always cached snippets first, fetch only when necessary.*
