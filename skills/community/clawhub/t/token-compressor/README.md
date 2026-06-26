# 3-Layer Token Compressor v1.1.0

Reduce AI API costs 40-60% by routing compression work through a free local Ollama model. Your paid API only sees the condensed result.

## How It Works

Instead of sending verbose user messages and full conversation history to expensive APIs, this middleware:
1. **Compresses user messages** — strips filler, hedging, and social padding via local model
2. **Summarizes old history** — rolling summary of old turns, keeps last N verbatim
3. **Caches responses** — serves cached answers for semantically similar questions

**All compression runs locally on your machine.** The local model is free. The paid API sees fewer tokens = lower bill.

---

## Requirements

- **Ollama** running locally (default: `localhost:11434`)
- A local model pulled (default: `llama3.1:8b` — any Ollama model works)
- Node.js 14+

---

## Quick Start

```javascript
const TokenCompressor = require('./src/token-compressor');

const compressor = new TokenCompressor({
  compressionModel: 'llama3.1:8b',  // any Ollama model
  ollamaHost: 'localhost',
  ollamaPort: 11434
});

// Layer 1: Compress a message before sending to paid API
const { compressed, saved } = await compressor.compressMessage(userInput);
const response = await expensiveAPI.chat(compressed);

// Layer 2: Compress conversation history (keeps last 10 turns verbatim)
const compressedHistory = await compressor.compressHistory(conversationHistory);
const response2 = await expensiveAPI.chat({ messages: compressedHistory });

// Layer 3: Cache — check before calling API
const cached = compressor.checkCache(userInput);
if (cached) return cached;
const result = await expensiveAPI.chat(userInput);
compressor.cacheResponse(userInput, result);
```

---

## API Reference

### `new TokenCompressor(config)`

| Option | Default | Description |
|--------|---------|-------------|
| `ollamaHost` | `'localhost'` | Ollama hostname |
| `ollamaPort` | `11434` | Ollama port |
| `compressionModel` | `'llama3.1:8b'` | Model to use for compression |
| `maxUncompressedTurns` | `10` | Keep last N turns verbatim; summarize everything before |
| `summaryMaxTokens` | `300` | Max tokens for history summary |
| `cacheMaxSize` | `100` | Max cached responses (LRU eviction) |
| `cacheTTL` | `3600000` | Cache expiry in ms (default: 1 hour) |
| `enabled` | `true` | Set `false` to disable all compression (passthrough mode) |

### `compressMessage(message)` → `{ compressed, original, saved, charsSaved? }`

Compresses a single user message. Skips messages under 15 words (not worth the cost). Returns original unchanged if compression fails or saves < 15%.

### `compressHistory(history, systemPrompt?)` → `Message[]`

Compresses a conversation history array. Returns unmodified history if under `maxUncompressedTurns * 2` turns. On longer histories, replaces old turns with a rolling summary block.

### `checkCache(message)` → `string | null`

Checks if a semantically similar message was already answered. Returns the cached response or `null`.

### `cacheResponse(message, response)`

Stores a response in cache for future similar questions.

### `getStats()` → `{ messagesCompressed, historySummaries, cacheHits, estimatedTokensSaved, cacheSize }`

Returns running compression statistics.

### `reset()`

Clears history summary and cache. Call at the start of a new conversation.

---

## Full Middleware Example

```javascript
const TokenCompressor = require('./src/token-compressor');

const compressor = new TokenCompressor({ compressionModel: 'llama3.1:8b' });

async function chat(userMessage, history) {
  // Check cache first
  const cached = compressor.checkCache(userMessage);
  if (cached) return cached;

  // Compress the user message
  const { compressed } = await compressor.compressMessage(userMessage);

  // Compress old history
  const compressedHistory = await compressor.compressHistory([
    ...history,
    { role: 'user', content: compressed }
  ]);

  // Send to paid API — fewer tokens
  const response = await expensiveAPI.chat({ messages: compressedHistory });

  // Cache the result
  compressor.cacheResponse(userMessage, response);

  return response;
}
```

---

## Typical Savings

| Content Type | Compression | Notes |
|-------------|-------------|-------|
| Chat conversations | 40-50% | Filler removal + history summarization |
| Long documents | 50-60% | Dense summarization of old context |
| Code + explanation | 25-35% | Code preserved verbatim, prose compressed |
| Short prompts (<15 words) | 0% | Skipped — overhead not worth it |

---

## What This Sends to Your Local Model

| Operation | What's sent |
|-----------|-------------|
| Message compression | Your message + "compress this" instruction |
| History summarization | Old conversation turns + "summarize" instruction |
| Cache lookup | Nothing — pure local keyword matching |

No data leaves your machine. Everything goes to `localhost:11434` only.

---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from
  the use or misuse of this software — including but not limited to financial loss,
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness
  for any particular purpose.

By downloading, installing, or using this software, you acknowledge that you have read
this disclaimer and agree to use the software entirely at your own risk.

**DATA DISCLAIMER:** This software processes data locally on your system and sends it
to a local Ollama instance only. No data is transmitted to external services.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw)*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $30. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
