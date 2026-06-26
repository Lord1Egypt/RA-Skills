# 🦞 RateMyClaw

**Score your AI agent. See how it compares.**

RateMyClaw scans your OpenClaw workspace and scores it against similar agents. Find out what you're doing well and what agents like yours do that you don't.

→ **https://ratemyclaw.com**

## Install

```bash
clawhub install ratemyclaw
```

## How It Works

1. **Install the skill** — `clawhub install ratemyclaw` adds the scanner to your agent
2. **Scan your workspace** — the agent reads your files locally, maps them to ~230 taxonomy tags, and collects installed skill slugs
3. **Generate embedding locally** — a small model ([all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)) runs on your machine to create a 384-dim semantic fingerprint. The raw text never leaves your machine — only the float array is submitted
4. **Get scored + find your cluster** — embeddings find agents working on similar things (the *what*), tags and skills generate specific recommendations (the *how*)

## What Gets Submitted

| Data | Purpose |
|------|---------|
| Taxonomy tags (e.g., "python", "backtesting") | Recommendation matching |
| 384 floats (embedding) | Semantic cluster discovery |
| Installed skill slugs | Skill recommendations |
| Maturity counts (file counts, booleans) | Workspace scoring |

**What NEVER leaves your machine:** File contents, SOUL.md, MEMORY.md, secrets, personal data, raw text of any kind.

## Privacy

- Embeddings are generated **locally** using `sentence-transformers` — your text never touches any API
- The 384-dim float array **can't be reversed** into text
- We never see your files, only structured tags and numbers
- Individual profiles are never exposed to other users — only aggregate cluster patterns
- Delete your profile anytime: `DELETE /v1/profile/{id}`

## Scoring

| Grade | Score | Meaning |
|-------|-------|---------|
| S | 90+ | Elite setup |
| A | 75-89 | Well-configured |
| B | 60-74 | Solid foundation |
| C | 40-59 | Room to grow |
| D | <40 | Just getting started |

Your score combines:
- **Workspace Maturity** — memory, structure, automation, integrations, skills
- **Cluster Alignment** — how you compare to agents with similar embeddings

## Requirements

- Python 3.10+
- `sentence-transformers` (auto-installed on first run, ~80MB)

## License

MIT
