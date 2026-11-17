---
name: headroom-token-compression
description: "Compress AI Agent tool outputs, logs, and RAG content using Headroom — reduce token usage by 20-95%"
version: 1.1.0
author: weekly-skill-discovery
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [token-compression, cost-reduction, mcp, agent-optimization]
---

# Headroom Token Compression

Compress content sent to LLMs (tool outputs, logs, RAG chunks, files) while maintaining answer quality — reduces token consumption by 20-95%.

## 🚨 Privacy & Data Security Warning (Read Before Use)

Headroom caches **raw uncompressed content** locally (for later retrieval). This means:
- Your prompts, tool outputs, logs, etc. will be cached on your local machine
- Data is **NOT sent to external services** (all processing is local)
- But cached files are stored on local disk — ensure your device is secure

**Data that should NOT be processed:**
- Content containing API keys, passwords, or private tokens
- Personally identifiable information (PII)
- Internal company code or proprietary business information
- Any content you don't want stored on local disk

If processing sensitive data, ensure: ① device has encrypted storage; ② regularly clean headroom cache directory (`~/.headroom/cache`).

---

## Trigger Conditions

**Only use this skill in the following explicit scenarios:**

- You **actively request** compression of specific content (e.g., "compress these logs", "reduce tokens in this code search")
- You are dealing with obvious **large redundant data** (e.g., 100+ search results, extremely long logs, duplicate JSON)
- You have confirmed the content does **NOT contain sensitive information** (see privacy warning above)
- You are experiencing high token costs in Claude Code, Codex, Cursor, etc.

**NOT suitable for:**
- Routine conversations or general Q&A
- Processing logs or code containing sensitive data
- Ordinary tasks without explicit compression needs

---

## Source

- GitHub: https://github.com/headroomlabs-ai/headroom
- Stars: ~71,000
- License: MIT

---

## Installation

```bash
# Using uv (recommended)
uv tool install --python 3.13 "headroom-ai[all]"

# Or using pip
pip install "headroom-ai[all]"
```

---

## Usage

### 1. One-Click Deploy (Simplest)
```bash
headroom deploy
```
Automatically configures local deployment and agent integration.

### 2. Wrap Common Agents
```bash
# Wrap Claude Code
headroom wrap claude

# Wrap Codex
headroom wrap codex

# Wrap OpenCode
headroom wrap opencode
```
Use `headroom unwrap <tool>` to remove wrapping.

> **Note**: Wrap operations modify agent startup configuration. Make sure you know what you're doing.

### 3. Proxy Mode (Zero Code Changes)
```bash
headroom proxy --port 8787
```
Any OpenAI-compatible client can use this proxy by setting API base URL.

### 4. Python Library (Inline Use)
```python
from headroom import compress
from openai import OpenAI

messages = [{"role": "user", "content": "Analyze these results"}]
result = compress(messages, model="gpt-4o")

client = OpenAI()
response = client.chat.completions.create(model="gpt-4o", messages=result.messages)
print(f"Saved {result.tokens_saved} tokens ({result.compression_ratio:.0%})")
```

### 5. MCP Server Mode
```bash
headroom mcp install
```
Provides `headroom_compress`, `headroom_retrieve`, `headroom_stats` tools to any MCP client.

---

## Verify Installation

```bash
# Health check
headroom doctor

# View savings stats
headroom perf

# Real-time dashboard (requires running proxy)
headroom dashboard
```

---

## Compression Results

| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| Code search (100 results) | 17,199 tokens | 13,597 tokens | **21%** |
| SRE incident debugging | 55,957 tokens | 24,340 tokens | **57%** |
| Codebase exploration | 58,801 tokens | 33,895 tokens | **42%** |
| GitHub Issue classification | 46,067 tokens | 32,429 tokens | **30%** |

JSON duplicate data can save 90%+. Plain text content compresses less.

---

## Output Compression (Reduce Model Response Tokens)

```bash
# Enable output compression
export HEADROOM_OUTPUT_SHAPER=1
headroom proxy --port 8787

# Auto-learn your verbosity preferences
headroom learn --verbosity
headroom learn --verbosity --apply
```

---

## Supported Agents

| Agent | Support |
|-------|---------|
| Claude Code | ✅ |
| Codex | ✅ |
| OpenCode | ✅ |
| Cursor | Manual config |
| Aider | ✅ |
| Copilot CLI | ✅ |
| Cline | ✅ |
| Continue | ✅ |
| Goose | ✅ |
| OpenHands | ✅ |

---

## Pitfalls

- **Local caching**: Raw content cached on local disk, models can retrieve full content via `headroom_retrieve`. To clear cache, delete `~/.headroom/cache` directory.
- **Proxy mode**: When using proxy mode, configure client to use `http://localhost:8787` as API base.
- **Output shaping is optional**: Disabled by default, must be enabled manually.
- **Sensitive data risk**: As mentioned, raw data is cached locally. Ensure device security before processing sensitive content.

---

## References

- GitHub: https://github.com/headroomlabs-ai/headroom
- Docs: https://docs.headroomlabs.ai/docs
- Benchmarks: https://docs.headroomlabs.ai/docs/benchmarks
