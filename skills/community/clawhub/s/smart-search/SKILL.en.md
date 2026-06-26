---
name: smart-search
description: FREE unlimited search! Exa MCP (zero-config) + SearX (privacy) + Tavily (AI summaries). No API key required.
author: Li Yang
version: 4.0.0
tags:
  - search
  - exa
  - mcp
  - searx
  - tavily
  - web-search
  - english
  - chinese
  - free
triggers:
  - "search"
  - "find"
  - "latest"
  - "2026"
  - "write"
  - "copywriting"
  - "deep"
metadata: {
  "emoji": "🔍",
  "requires": {
    "bins": ["curl", "python3"],
    "env": ["SEARXNG_URL", "TAVILY_API_KEY"]
  }
}
---

# Smart Search v4.0 - FREE Unlimited Search

**Exa MCP (Main·Zero-Config·Free Unlimited) + SearX (Privacy) + Tavily (AI Summaries)**

---

## 🎉 Core Advantages

### v4.0 Major Upgrade

- ✅ **Zero Configuration** - No API key required, works out of the box
- ✅ **Free Unlimited** - Exa MCP officially free, no usage limits
- ✅ **Three Engines** - Exa MCP + SearX + Tavily, intelligent switching
- ✅ **Privacy Protection** - Sensitive queries automatically use SearX
- ✅ **AI Summaries** - Optional Tavily support for content creation

### Why Choose v4.0?

| Feature | v3.0 | v4.0 |
|------|------|------|
| **Configuration** | Exa API Key | Zero-config ✅ |
| **Free Quota** | 1000 times (one-time) | Unlimited ✅ |
| **Long-term Use** | Pay after quota | Forever free ✅ |
| **For Everyone** | ❌ Needs API Key | ✅ Out of box |

---

## Decision Logic

### Intelligent Scenario Recognition

| Scenario Type | Keywords | Recommended Engine | Reason |
|---------|--------|---------|------|
| **Daily Query** | What is, how to, tutorial, news | Exa MCP | Free unlimited, fast |
| **Technical Docs** | API, GitHub, code, technical, docs | Exa MCP | Structured data, precise |
| **Deep Research** ✨ | Deep analysis, detailed research, industry report, white paper | Tavily | AI summaries, insights |
| **Summary** 📝 | Summary, abstract, extract, organize | Tavily | AI-assisted organization |
| **Privacy Sensitive** 🔒 | Password, privacy, disease, medical, adult, sexual health, finance, legal, local, security, token, config, personal data | SearX | No tracking, privacy |
| **AI Creation** | Copywriting, create, draft, title | Tavily | AI summaries for creation |
| **User Specified** | use exa, use searx, use tavily | As user | Respect choice |

### Priority

| Priority | Engine | Usage Scenario | Ratio | Cost |
|--------|------|---------|------|------|
| 1️⃣ | **Exa MCP** | Tech/business/academic search, daily queries | 70% | **Free Unlimited** ✅ |
| 2️⃣ | **SearX** | Privacy sensitive, local queries | 20% | Free unlimited |
| 3️⃣ | **Tavily** | AI content creation, backup | 10% | Free 1000/month |

**Failover Strategy:**
```
Exa MCP → SearX → Tavily (Three-level backup)
```

---

## Configuration

### 🎉 Zero Configuration! Out of the Box

**v4.0 Biggest Advantage: No API Key Required!**

```bash
# ~/.openclaw/.env
# Nothing to configure! Just use it!
```

### Optional Configuration (Enhanced Features)

```bash
# ~/.openclaw/.env

# SearX (Privacy protection, optional)
SEARXNG_URL=http://localhost:8080

# Tavily (AI summaries, optional)
TAVILY_API_KEY=your_tavily_key_here
```

### Configuration Comparison

| Setup | Exa MCP | SearX | Tavily | Use Case |
|------|---------|-------|--------|---------|
| **Zero Config** ✅ | ✅ | ❌ | ❌ | Personal users, quick start |
| **Privacy Protection** | ✅ | ✅ | ❌ | Privacy-conscious users |
| **Full Experience** | ✅ | ✅ | ✅ | Need AI summaries |
| **Local Only** | ❌ | ✅ | ❌ | Fully offline environment |

**Deploy SearX (Optional):**
```bash
cd /home/admin/.openclaw/workspace/skills/smart-search
chmod +x deploy-searx.sh
./deploy-searx.sh
```

**Get Tavily API Key (Optional):**
1. Visit https://tavily.com
2. Register free account (1000/month free)
3. Get API Key

---

## Usage Examples

**Daily Search**
```bash
./search.sh "AI latest news"
# → Exa MCP (Free unlimited)
```

**Technical Query**
```bash
./search.sh "Python async tutorial"
# → Exa MCP (Precise tech docs)
```

**Privacy Query**
```bash
./search.sh "local privacy configuration"
# → SearX (Privacy protection)
```

**AI Creation** (Requires Tavily config)
```bash
./search.sh "how to write copywriting"
# → Tavily (With AI summaries)
```

**Specify Engine**
```bash
./search.sh "use searx to search XXX"
# → SearX (Respect user.com/user choice)
```

---

## Cost Comparison

### v3.0 vs v4.0

**v3.0 (Exa API):**
```
Free quota: 1000 times (one-time gift)
After quota: $7/1000 times (≈ ¥50/1000 times)
Monthly cost (1000 times/month): ≈ ¥50/month
```

**v4.0 (Exa MCP):**
```
Free quota: ♾️ Unlimited
After quota: ¥0 (Forever free)
Monthly cost (1000 times/month): ¥0 ✅
```

**Annual Savings:**
```
v3.0: ¥50 × 12 = ¥600/year
v4.0: ¥0/year
Savings: ¥600/year ✅
```

---

## Architecture Advantages

### Why Choose Exa MCP?

| Feature | Exa MCP | Exa API | SearX |
|------|---------|---------|-------|
| **Cost** | Free unlimited | $7/1000 times | Free unlimited |
| **Configuration** | Zero config | Needs API Key | Needs deployment |
| **Response Time** | ~1s | ~500ms | ~2s |
| **Result Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Privacy** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Exa MCP Core Advantages:**
- 🎯 **Officially Free** - Free service provided by Exa
- 🔌 **Zero Configuration** - No registration, no API key
- ♾️ **Unlimited Use** - No usage limits
- 📊 **High Quality** - 1B+ page index, precise search
- 🚀 **Fast Response** - Usually returns within 1 second

---

## Troubleshooting

### Exa MCP Unavailable
```bash
# Test Exa MCP
curl -X POST https://mcp.exa.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```

### SearX Unavailable
```bash
# Check container status
docker ps | grep searx
docker logs searx --tail 20
docker restart searx
```

### Failover Logic
- **Automatic trigger**, no manual intervention
- **Log提示**: `⚠️  Exa MCP temporarily unavailable, failing over to SearX...`
- **Three-level backup**: Exa MCP → SearX → Tavily

---

## Technical Details

### Exa MCP Call Format

```bash
curl -X POST https://mcp.exa.ai/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "web_search_exa",
      "arguments": {
        "query": "search query",
        "numResults": 5
      }
    }
  }'
```

### Response Format

Exa MCP returns structured data:
- Title: Title
- URL: Link
- Published: Publish date
- Author: Author
- Highlights: Content summary

---

## FAQ

### Q: Is Exa MCP really completely free?
A: Yes! Exa MCP is a free service provided officially by Exa, with no usage limits.

### Q: Why still configure SearX and Tavily?
A: 
- SearX: Privacy protection scenarios (local deployment, no external requests)
- Tavily: AI content creation (with AI summaries, assists creation)

### Q: What's the difference between Exa MCP and Exa API?
A:
- MCP: Free unlimited, zero config, basic search features
- API: Paid (with free gift), full features, customizable parameters

### Q: What scenarios is it suitable for?
A: 
- ✅ Personal daily search
- ✅ Technical documentation query
- ✅ News information retrieval
- ✅ Academic research
- ✅ Business research

---

**Last Updated:** 2026-03-30  
**Version:** 4.0.0 (Exa MCP Free Unlimited)

**Changelog:**
- v4.0 - Use Exa MCP, zero config, free unlimited
- v3.0.4 - Exa API + SearX + Tavily three engines
- v2.0 - SearX + Tavily dual engines
