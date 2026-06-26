---
name: Skill Preflight
description: Automatically inject relevant skills and protocols into agent context using local embeddings. Free, no API calls — uses Ollama with nomic-embed-text.
status: active
tags:
  - plugin
  - rag
  - embeddings
  - context-injection
  - local-first
author: Chemdawg
license: MIT
---

# Skill Preflight

A smart plugin for OpenClaw that automatically injects the most relevant skills and protocols into your agent's context before each run. Uses Ollama embeddings — free, offline-capable, no separate embedding API key required.

## What It Does

When you run an agent, this plugin:

1. **Scans** your `skills/` and `memory/protocols/` directories for documentation
2. **Embeds** each doc using `nomic-embed-text` (via Ollama)
3. **Matches** the incoming prompt against your docs using cosine similarity
4. **Injects** only the relevant ones above a configurable threshold
5. **Deduplicates** within a session (same doc won't be re-injected)

**Result:** Agents follow custom protocols and skills without burning tokens on irrelevant context.

## Requirements

- **OpenClaw** ≥ 1.0
- **Ollama** running locally on `http://localhost:11434`
- **Model:** `nomic-embed-text` (download with `ollama pull nomic-embed-text`)

## Quick Start

### 1. Install Ollama

Download from [ollama.com](https://ollama.com) and install.

### 2. Pull the embedding model

```bash
ollama pull nomic-embed-text
```

### 3. Start Ollama

```bash
ollama serve
```

Leave this running in the background. It listens on `http://localhost:11434` by default.

### 4. Install the plugin

Add to your `openclaw.json`:

```json
{
  "plugins": {
    "skill-preflight": {
      "enabled": true,
      "config": {
        "minScore": 0.3,
        "maxResults": 3,
        "protocolDirs": ["memory/protocols"],
        "skillsDirs": ["skills"]
      }
    }
  }
}
```

### 5. Add your docs

Create your skills and protocols in:
- `skills/` — skill documentation (looks for `SKILL.md` in subdirs or loose `.md` files)
- `memory/protocols/` — protocol docs (`.md` files, 1 level deep)

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `protocolDirs` | `["memory/protocols"]` | Directories to scan for protocol docs (recursive, 1 level) |
| `skillsDirs` | `["skills"]` | Directories to scan for skill docs |
| `toolsFiles` | `["TOOLS.md"]` | Individual files to always include in the index |
| `pinnedDocs` | `[]` | Docs always injected first, regardless of score |
| `maxResults` | `3` | Max ranked docs to inject per run (pinned docs don't count toward this) |
| `maxDocLines` | `100` | Truncate injected docs to N lines (0 = no limit) |
| `minScore` | `0.3` | Cosine similarity threshold (0–1). Lower = more permissive. Tune via debug logs. |
| `embedModel` | `nomic-embed-text:latest` | Ollama embedding model |
| `ollamaBaseUrl` | `http://localhost:11434` | Ollama API base URL. For local-only privacy, keep this on `localhost`, `127.0.0.1`, or `::1`. If you point it at a remote host, prompt text and indexed doc content are sent to that host for embeddings. |
| `requestTimeoutMs` | `10000` | Timeout for embedding requests (ms) |
| `minPromptLength` | `20` | Minimum prompt length to trigger preflight. Short prompts skip embedding. |

## Pinned Docs

Pin specific docs so they're always injected first, regardless of relevance score:

```json
{
  "plugins": {
    "skill-preflight": {
      "config": {
        "pinnedDocs": ["memory/protocols/house-rules.md", "skills/ethereum/SKILL.md"]
      }
    }
  }
}
```

Pinned docs appear first and don't count toward `maxResults`.

## Tuning the Threshold

Enable debug logging in OpenClaw to see similarity scores:

```
skill-preflight: scores — DebuggingProtocol(0.72), EthereumSkill(0.51), MemoryProtocol(0.34), ...
```

Use this to dial in `minScore`. If too many irrelevant docs are injected, raise it. If relevant docs are missing, lower it.

## Troubleshooting

### "Ollama embedding unavailable"

- **Check Ollama is running:** `curl http://localhost:11434/api/tags`
- **Check model is installed:** `ollama list` (should show `nomic-embed-text`)
- **Check timeout:** If embedding is slow, increase `requestTimeoutMs` in config

### "Not injecting docs I expect"

- **Enable debug logs** in OpenClaw to see scores
- **Check file locations:** Docs must be in configured `protocolDirs` or `skillsDirs`
- **Check doc metadata:** Docs with `status: deprecated` or `status: archived` are skipped
- **Verify content:** Empty docs or docs with only frontmatter score 0 on all prompts

### "Too many/too few docs injected"

- Adjust `minScore` (lower threshold = more docs)
- Adjust `maxResults` (cap on how many ranked docs)
- Use `pinnedDocs` to always include critical docs

### Ollama is slow

- `nomic-embed-text` takes ~100–300ms per document on typical hardware
- This is a one-time cost per new doc; embeddings are cached for 1 hour
- For faster iteration during development, raise `minScore` to reduce docs being embedded

## File Format

Docs are standard Markdown with optional frontmatter:

```markdown
---
name: My Custom Skill
description: A brief description of what this does
status: active
---

# My Custom Skill

Detailed instructions, examples, step-by-step procedures...
```

Frontmatter is optional. If not provided, the first heading or filename is used as the title, and the first few lines become the description.

## How It Works Under the Hood

1. **Initialization:** Plugin scans configured dirs and builds a doc index
2. **Doc caching:** Docs are cached for 1 hour to avoid repeated disk reads
3. **Embedding:** On each agent run, the prompt is embedded via Ollama
4. **Ranking:** Docs are scored by cosine similarity, top N are selected
5. **Deduplication:** Tracked per session so the same doc isn't re-injected
6. **Injection:** Matched docs are formatted and prepended to the prompt context

## Privacy & Performance

- **No separate embedding API required** — embeddings go through your configured Ollama endpoint
- **Local-only when Ollama is local** — keep `ollamaBaseUrl` on `localhost`, `127.0.0.1`, or `::1` if you want docs and prompts to stay on the same machine
- **Remote Ollama changes the trust boundary** — if `ollamaBaseUrl` points to another host, the following are sent to that host for embedding:
  - **Prompt text** from every agent run
  - **Full indexed markdown content** including secrets, API keys, credentials, and all sensitive data in your docs
  - Any confidential information embedded in your skills, protocols, and tools documentation
- **Offline capable** — once the Ollama model is downloaded and running locally, no internet is required
- **Caching:** Docs cached for 1 hour, embeddings cached in memory per session
- **Session-aware:** Same doc won't be re-injected in a single conversation

## License

MIT

---

**Questions?** Check the OpenClaw docs at [openclaw.ai](https://openclaw.ai) or report issues on GitHub.
