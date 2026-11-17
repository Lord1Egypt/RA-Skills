# zhiyan-smart-research

[![ClawHub](https://img.shields.io/badge/ClawHub-zhiyan--smart--research-blue)](https://clawhub.ai/skills/zhiyan-smart-research)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-6366f1)](https://docs.openclaw.ai/tools/skills)

**提问即检索，结论必溯源** — An OpenClaw skill for academic literature search and citation-backed synthesis.

No backend server. No WeChat mini-program. No API keys in the skill itself.

| Layer | Role |
|-------|------|
| **smart-research** | Crossref + PubMed search (Python, stdlib only) |
| **OpenClaw LLM** | Your configured model — synthesis, reasoning, `[n]` citations |
| **OpenClaw memory** | Conversation context + `research/sessions/` for follow-ups |

## Features

- Parallel **Crossref + PubMed** literature search
- Structured JSON paper output (title, authors, year, DOI, abstract, URL)
- Agent-driven **citation-backed** reports using OpenClaw's LLM
- Local session memory under `research/sessions/`
- Zero backend dependency — calls public APIs only

## Requirements

- [OpenClaw](https://docs.openclaw.ai)
- Python 3.9+
- Network access to `api.crossref.org` and `eutils.ncbi.nlm.nih.gov`

## Install

### From ClawHub

```bash
clawhub install zhiyan-smart-research
openclaw skills install @your-owner/zhiyan-smart-research
```

### From source

```bash
git clone https://github.com/YOUR_ORG/zhiyan-smart-research.git
openclaw skills install ./zhiyan-smart-research
```

## Quick start

```bash
# Health check
python3 scripts/health_check.py

# Search papers
python3 scripts/search_literature.py "CRISPR gene editing research gap"

# In OpenClaw chat
/smart-research
# or slash command: /zhiyan-smart-research
# or: "帮我做 CRISPR 领域的文献综述"
```

### Agent workflow

1. Run `search_literature.py "<query>"` → JSON papers
2. Synthesize with **OpenClaw LLM** — keep `[1][2]` citations
3. Save via `save_research.py --topic "..." --summary "..." --papers-json papers.json`
4. On follow-up: read `research/sessions/<id>.md` + optional new search

## Environment (optional)

| Variable | Description |
|----------|-------------|
| `CROSSREF_MAILTO` | Contact email for Crossref polite pool (default: `smart-research@openclaw.local`) |

## Project structure

```
smart-research/          # repo root (rename to zhiyan-smart-research when publishing to GitHub)
├── SKILL.md              # OpenClaw skill contract
├── scripts/
│   ├── literature.py     # Crossref + PubMed core
│   ├── search_literature.py
│   ├── save_research.py
│   └── health_check.py
├── research/             # Local session memory (gitignored)
├── examples.md
├── SECURITY.md
└── LICENSE
```

## Publish to ClawHub

```bash
npm i -g clawhub   # or: npx clawhub@latest
clawhub login
clawhub skill publish . --version 1.0.0 --changelog "Initial open-source release"
```

## Security

See [SECURITY.md](SECURITY.md). No secrets, tokens, or private APIs. Session files stay local.

## License

MIT — see [LICENSE](LICENSE).

## Brand

Part of the **智研导航** (Zhiyan Navigation) research product line.

Slogan: 提问即检索，结论必溯源
