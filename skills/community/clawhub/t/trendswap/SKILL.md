---
name: trendswap
description: "AI Face Swap & Viral Meme Video Generator for OpenClaw agents. Create instant motion transfer and face swap meme videos (Drake, Bulin 47, Coldplay Kiss Cam, Ozil, Flying Tesla, Spooky Skeletons) with 100% facial identity preservation and synchronized audio from a single photo."
homepage: https://trendswap.app
metadata:
  openclaw:
    emoji: "🎭"
    requires:
      bins: ["node", "curl"]
    primaryEnv: "TRENDSWAP_API_KEY"
---

# TrendSwap AI Video Studio

Official OpenClaw skill for [TrendSwap](https://trendswap.app/) — the viral AI video generator & motion transfer platform. Recast faces and animate portraits into trending video memes with 100% facial identity preservation, lip-sync, and native audio.

## 🚀 Getting Started & Authentication

To use TrendSwap in your agent workflows:

1. **Create an Account**: Sign up at [TrendSwap Registration](https://trendswap.app/auth/signup).
2. **Get your API Key**: Go to [TrendSwap API Keys](https://trendswap.app/settings/apikeys) and generate a new key (`sk_...`).
3. **Configure Environment Variable**:
   ```bash
   export TRENDSWAP_API_KEY="sk_your_api_key_here"
   ```

## 🛠️ Usage & Commands

This skill includes a lightweight CLI script `{baseDir}/scripts/trendswap.mjs` that interacts directly with the TrendSwap cloud engine.

### 1. List Available Templates
Discover trending viral video templates (e.g. `flying-tesla-roadster-ai`, `spooky-scary-skeletons`, `zombie-couple`, `hit-the-road-dude`):

```bash
node {baseDir}/scripts/trendswap.mjs list-templates
```

### 2. Check Credits Balance
Check your current credit balance:

```bash
node {baseDir}/scripts/trendswap.mjs balance
```

### 3. Generate Video
Submit a portrait image URL and template ID to generate an AI video:

```bash
node {baseDir}/scripts/trendswap.mjs create \
  --template "flying-tesla-roadster-ai" \
  --image-url "https://example.com/portrait.jpg" \
  --resolution "720p"
```

### 4. Query Task Status
Poll for generation status and retrieve the final video URL:

```bash
node {baseDir}/scripts/trendswap.mjs status --job-id "job_xxx"
```

## 🌐 Official MCP Server Endpoint

Agents supporting the Model Context Protocol (MCP) can connect directly to TrendSwap's public MCP endpoint:

- **Endpoint**: `https://trendswap.app/api/mcp`
- **Transport**: Streamable HTTP (`Accept: application/json, text/event-stream`)
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer sk_...`
- **Tools**:
  - `list_templates`: Browse catalog of viral meme templates (No auth required).
  - `get_credits_balance`: Query remaining balance.
  - `create_generation_job`: Trigger video generation with portrait recasting.
  - `get_job_status`: Fetch generation progress and final video URL.

Learn more and explore the web interface at [TrendSwap Official Website](https://trendswap.app/).
