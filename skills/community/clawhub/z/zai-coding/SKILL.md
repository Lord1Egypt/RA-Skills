---
name: zai-coding
description: Configure OpenClaw to use Z.AI GLM Coding Plan models for all coding-related tasks. Set up optimal configuration for development workflows with steps: (1) Verify OpenClaw is running, (2) Choose region (international: zai-coding-global, China: zai-coding-cn), (3) Configure via onboard or manual edit of openclaw.json with ZAI_API_KEY env var, (4) Set optimal model (zai/glm-5, glm-4.7, glm-4.6), (5) Optionally enable tool_stream and adjust context tokens, (6) Restart gateway and validate, (7) Install Z.AI MCP Tools (web-search-prime, web-reader, zread). Use when configuring Z.AI Coding Plan, switching models, or optimizing coding workflows.
---

# Z.AI Coding Plan Setup

## Overview

Configure OpenClaw to use Z.AI GLM Coding Plan models for optimal coding performance. Z.AI provides multiple GLM models optimized for development tasks with varying context windows and performance characteristics.

## Prerequisites

Before configuring Z.AI Coding Plan:

1. **OpenClaw installed** - Verify with `openclaw gateway status`
2. **Z.AI API Key** - Available from https://z.ai/subscribe (international) or https://bigmodel.cn (China)
3. **Docker environment** - API key available as `ZAI_API_KEY` environment variable

## Available Models

| Model ID | Context | Best For |
|----------|---------|----------|
| glm-5 | 205K tokens | Latest flagship, best overall performance |
| glm-5-turbo | 200K tokens | Fast responses, quick iterations |
| glm-4.7 | 205K tokens | Balanced performance, strong reasoning |
| glm-4.7-flash | 200K tokens | Quick iterations, prototyping |
| glm-4.7-flashx | 200K tokens | Optimized speed |
| glm-4.6 | 205K tokens | Stable, excellent coding |
| glm-4.6v | 128K tokens | Vision + coding (UI work) |
| glm-4.5 | 131K tokens | Efficient coding |
| glm-4.5-air | 131K tokens | Lightweight operations |
| glm-4.5-flash | 131K tokens | Fast coding, cost-effective |

## Configuration Steps

### Step 1: Verify OpenClaw Status

```bash
openclaw gateway status
```

### Step 2: Choose Configuration Method

**Option A: Interactive Setup (Recommended)**

International users:
```bash
openclaw onboard --auth-choice zai-coding-global
```

China region users:
```bash
openclaw onboard --auth-choice zai-coding-cn
```

This prompts for the API key and configures everything automatically.

**Option B: Manual Configuration**

Edit `~/.openclaw/openclaw.json`:

```json
{
  "env": {
    "ZAI_API_KEY": "sk-your-api-key-here"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "zai/glm-5"
      }
    }
  }
}
```

**Important**: Model format is `zai/<model-name>`.

### Step 3: Configure Coding-Specific Settings

For optimal coding performance:

```bash
# Enable tool streaming (better for coding workflows)
openclaw config set agents.defaults.models."zai/glm-5".params.tool_stream true --json

# Set higher context for complex projects (optional)
openclaw config set agents.defaults.maxContextTokens 150000
```

### Step 4: Optional - Create Coding-Focused Agent

For dedicated coding agents:

```bash
openclaw agents create coding-assistant
```

Configure in `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "coding-assistant": {
      "model": {
        "primary": "zai/glm-5"
      },
      "systemPrompt": "You are an expert software developer. Focus on writing clean, efficient, and well-documented code. Always explain your reasoning and provide best practices.",
      "tools": ["filesystem", "shell", "browser"]
    }
  }
}
```

### Step 5: Restart and Verify

```bash
# Validate configuration
openclaw config validate

# Restart gateway
openclaw gateway restart

# Check status
openclaw status
```

### Step 6: Test Configuration

Test with a simple coding task:

```bash
openclaw chat "Write a Python function to calculate the fibonacci sequence"
```

## Model Selection Guide

Use the right model based on your needs:

- **General coding** → `zai/glm-5` - Best overall performance
- **Quick prototyping** → `zai/glm-5-turbo` - Fast responses
- **Complex refactoring** → `zai/glm-4.7` - Strong reasoning
- **Code review** → `zai/glm-4.6` - Stable, thorough
- **UI/Frontend work** → `zai/glm-4.6v` - Vision capabilities
- **Simple scripts** → `zai/glm-4.5-flash` - Cost-effective

## Region Configuration

- **International**: `zai-coding-global` endpoint → `https://api.z.ai/api/coding/paas/v4`
- **China**: `zai-coding-cn` endpoint → `https://api.bigmodel.cn/api/coding/paas/v4`

## Troubleshooting

### Authentication Error (1001)

API key missing or invalid:

```bash
openclaw config get env.ZAI_API_KEY
```

### Model Not Found

Ensure correct endpoint:

```bash
# International
https://api.z.ai/api/coding/paas/v4

# China
https://api.bigmodel.cn/api/coding/paas/v4
```

### Rate Limiting

GLM Coding Plan has usage limits based on subscription tier:

- **Lite**: 120 prompts per 5-hour cycle
- **Pro**: 600 prompts per 5-hour cycle
- **Max**: Higher limits

### Gateway Won't Start

```bash
# Check logs
openclaw gateway logs

# Validate config
openclaw config validate

# Reset if needed
openclaw config reset
```

## Switching Models

To change the default model:

```bash
# Set new model
openclaw config set agents.defaults.model.primary "zai/glm-4.7"

# Restart to apply
openclaw gateway restart
```

## Integration with Channels

This configuration works with all OpenClaw channels:

- **Feishu**: Coding model used for all coding requests
- **DingTalk**: Same model configuration
- **WeCom**: Compatible with coding workflows
- **CLI**: Direct access via `openclaw chat`

## Useful Commands

| Command | Description |
|---------|-------------|
| `openclaw config get agents.defaults.model` | Check current model |
| `openclaw config set agents.defaults.model.primary "zai/glm-5"` | Change model |
| `openclaw gateway restart` | Apply changes |
| `openclaw status` | Verify configuration |

## Z.AI MCP Tools Configuration

GLM Coding Plan includes powerful MCP tools for web access and code research. These tools are **exclusive to Coding Plan subscribers**.

### Available MCP Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| **Web Search** | Search the web for real-time information | Finding documentation, news, tutorials |
| **Web Reader** | Extract full content from any webpage | Reading articles, docs, extracting data |
| **Zread** | Access GitHub repositories documentation & code | Understanding open-source projects |

### MCP Quotas by Plan

| Plan | Web Searches + Readers + Zread |
|------|--------------------------------|
| **Lite** | 100 total |
| **Pro** | 1,000 total |
| **Max** | 4,000 total |

---

### Step 7: Install Z.AI MCP Tools

After configuring the model, add the MCP tools to enhance your coding agent.

#### Tool 1: Web Search (`web-search-prime`)

Provides real-time web search capabilities.

**One-click install (OpenClaw):**
```bash
openclaw mcp add web-search-prime --type http --url "https://api.z.ai/api/mcp/web_search_prime/mcp" --header "Authorization: Bearer YOUR_API_KEY"
```

**Manual configuration** - Add to `~/.openclaw/openclaw.json`:
```json
{
 "mcpServers": {
 "web-search-prime": {
 "type": "http",
 "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
 "headers": {
 "Authorization": "Bearer YOUR_API_KEY"
 }
 }
 }
}
```

**Available tool:** `webSearchPrime` - Search web information with titles, URLs, summaries

---

#### Tool 2: Web Reader (`web-reader`)

Extracts complete content from any webpage.

**One-click install (OpenClaw):**
```bash
openclaw mcp add web-reader --type http --url "https://api.z.ai/api/mcp/web_reader/mcp" --header "Authorization: Bearer YOUR_API_KEY"
```

**Manual configuration** - Add to `~/.openclaw/openclaw.json`:
```json
{
 "mcpServers": {
 "web-reader": {
 "type": "http",
 "url": "https://api.z.ai/api/mcp/web_reader/mcp",
 "headers": {
 "Authorization": "Bearer YOUR_API_KEY"
 }
 }
 }
}
```

**Available tool:** `webReader` - Fetch page title, main content, metadata, links

---

#### Tool 3: Zread (`zread`)

Access GitHub repositories for documentation and code analysis.

**One-click install (OpenClaw):**
```bash
openclaw mcp add zread --type http --url "https://api.z.ai/api/mcp/zread/mcp" --header "Authorization: Bearer YOUR_API_KEY"
```

**Manual configuration** - Add to `~/.openclaw/openclaw.json`:
```json
{
 "mcpServers": {
 "zread": {
 "type": "http",
 "url": "https://api.z.ai/api/mcp/zread/mcp",
 "headers": {
 "Authorization": "Bearer YOUR_API_KEY"
 }
 }
 }
}
```

**Available tools:**
| Tool | Description |
|------|-------------|
| `search_doc` | Search documentation in GitHub repositories |
| `get_repo_structure` | Get directory structure and file list |
| `read_file` | Read complete code content of files |

---

### Complete MCP Configuration Example

Here's a complete `~/.openclaw/openclaw.json` with all three MCP tools:

```json
{
 "env": {
 "ZAI_API_KEY": "sk-your-api-key-here"
 },
 "agents": {
 "defaults": {
 "model": {
 "primary": "zai/glm-5"
 }
 }
 },
 "mcpServers": {
 "web-search-prime": {
 "type": "http",
 "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
 "headers": {
 "Authorization": "Bearer sk-your-api-key-here"
 }
 },
 "web-reader": {
 "type": "http",
 "url": "https://api.z.ai/api/mcp/web_reader/mcp",
 "headers": {
 "Authorization": "Bearer sk-your-api-key-here"
 }
 },
 "zread": {
 "type": "http",
 "url": "https://api.z.ai/api/mcp/zread/mcp",
 "headers": {
 "Authorization": "Bearer sk-your-api-key-here"
 }
 }
 }
}
```

---

### Step 8: Verify MCP Tools Installation

After adding the MCP tools, restart and verify:

```bash
# Restart gateway to load MCP servers
openclaw gateway restart

# Check MCP status
openclaw mcp list

# Verify tools are available
openclaw status
```

---

### Step 9: Test the MCP Tools

Test each tool to ensure proper configuration:

**Test Web Search:**
```bash
openclaw chat "Search for the latest Python 3.12 features"
```

**Test Web Reader:**
```bash
openclaw chat "Read and summarize the content from https://docs.python.org/3/whatsnew/3.12.html"
```

**Test Zread:**
```bash
openclaw chat "Explain the structure of the fastapi/fastapi repository on GitHub"
```

---

### MCP Tools Troubleshooting

#### Invalid API Key
```
Error: Invalid access token
```
**Solutions:**
1. Verify API key is correctly copied (no extra spaces)
2. Check API key is activated at https://z.ai/manage-apikey/apikey-list
3. Ensure sufficient balance on your account
4. Verify `Authorization: Bearer` format is correct

#### Connection Timeout
**Solutions:**
1. Check network connection
2. Verify firewall allows HTTPS connections
3. Increase client timeout settings
4. Try again later (server may be busy)

#### Repository Access Failed (Zread)
**Solutions:**
1. Confirm repository exists and is public
2. Check repository name format: `owner/repo`
3. Visit https://zread.ai to verify repository is indexed

#### Quota Exceeded
```
Error: Rate limit exceeded
```
**Solution:** Wait for the next 5-hour cycle or upgrade your plan

---

### MCP Tools Use Cases

| Scenario | Tools to Use | Example Prompt |
|----------|--------------|----------------|
| Research a library | Zread + Web Search | "Research the React hooks API and find best practices" |
| Debug an issue | Web Search + Web Reader | "Search for solutions to 'Python asyncio CancelledError'" |
| Learn a new framework | Zread | "Explain the architecture of the Next.js repository" |
| Stay updated | Web Search | "What are the latest updates in TypeScript 5.4?" |
| Read documentation | Web Reader | "Read the FastAPI authentication documentation" |

## References

- **Z.AI Coding Plan**: https://z.ai/subscribe
- **OpenClaw Z.AI Provider**: https://docs.openclaw.ai/providers/zai
- **GLM Models Overview**: https://docs.openclaw.ai/providers/glm
- **Web Search MCP**: https://docs.z.ai/devpack/mcp/search-mcp-server
- **Web Reader MCP**: https://docs.z.ai/devpack/mcp/reader-mcp-server
- **Zread MCP**: https://docs.z.ai/devpack/mcp/zread-mcp-server
