---
name: "3-Layer Token Compressor — Cut AI API Costs 40-60%"
description: "Pre-process prompts through 3 compression layers before sending to paid APIs. Uses a local Ollama model to intelligently compress messages and summarize history. Same quality, fewer tokens, lower bills."
author: "@TheShadowRose"
version: "1.1.0"
tags: ["token-optimization", "cost-reduction", "compression", "api-costs", "prompt-optimization", "budget"]
license: "MIT"
---

# 3-Layer Token Compressor — Cut AI API Costs 40-60%

Pre-process prompts through 3 compression layers before sending to paid APIs. Uses a free local Ollama model to do the compression work — your paid API only sees the condensed result.

## Runtime Requirements

| Requirement | Details |
|-------------|---------|
| **Ollama** | Must be running locally (default: `localhost:11434`) |
| **Local model** | A small model for compression (e.g. `llama3.1:8b`). Configurable via `compressionModel` option. |
| **Node.js** | 14+ |

**Ollama is required at runtime.** The compressor sends prompts to your local model — not to any external API.

## What This Skill Sends to the Local Model

This skill sends the following to your local Ollama model:

| Operation | System prompt | User prompt |
|-----------|--------------|-------------|
| Message compression | `You are a text compression tool. Output only what is asked, nothing else.` | Your message + instruction to compress |
| History summarization | Same | Old conversation turns + instruction to summarize |

No data is sent to external APIs. All compression happens locally.

## Side Effects

| Type | Description |
|------|-------------|
| **NETWORK** | HTTP to `localhost:11434` only — your local Ollama instance |
| **MEMORY** | Response cache stored in-memory (Map, configurable size/TTL) |
| **DISK** | None — cache is not persisted to disk |

## Setup

```javascript
const TokenCompressor = require('./src/token-compressor');

const compressor = new TokenCompressor({
  ollamaHost: 'localhost',      // default
  ollamaPort: 11434,            // default
  compressionModel: 'llama3.1:8b',  // default — any Ollama model works
  maxUncompressedTurns: 10,     // keep last N turns verbatim
  cacheMaxSize: 100,
  cacheTTL: 3600000             // 1 hour
});
```

See README.md for full API documentation and usage examples.
