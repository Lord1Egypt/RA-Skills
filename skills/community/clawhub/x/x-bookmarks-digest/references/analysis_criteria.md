# Bookmark Analysis Criteria

## Categories

| Category | What It Means | Examples |
|----------|--------------|---------|
| **tool** | CLI tools, libraries, frameworks, SDKs, packages | "Just released a new Python CLI for...", npm/pip/brew packages |
| **project** | GitHub repos, open-source projects, shipped code | Links to github.com repos, "just shipped v2.0" |
| **product** | SaaS apps, services, startups, commercial tools | "Launched our new platform...", pricing pages, beta invites |
| **insight** | Tips, techniques, architectural patterns, lessons | "Here's what I learned...", design patterns, threads with advice |
| **resource** | Articles, papers, tutorials, guides, videos | Blog posts, arxiv papers, YouTube talks, documentation |
| **other** | Doesn't fit above — memes, opinions, personal updates | Hot takes, jokes, personal announcements |

## Relevance Scoring (1-5)

| Score | Meaning | Typical Signals |
|-------|---------|----------------|
| **5** | Must-act — directly useful for current projects | Stack-relevant tool/project + GitHub link + matches active work |
| **4** | High value — worth investigating or installing | GitHub repo + relevant domain + actionable content |
| **3** | Medium — interesting but not urgent | Good insight or resource, loosely related to stack |
| **2** | Low — mildly interesting | General tech content, tangentially related |
| **1** | Noise — skip in digest | Memes, off-topic, duplicate of known tool |

## Action Decision Matrix

| Category + Score | Recommended Action |
|-----------------|-------------------|
| tool (4-5) | Install it (`brew install`, `pip install`, `cargo install`) |
| project (4-5) | Clone repo, evaluate, consider integrating |
| product (4-5) | Sign up / bookmark for trial |
| insight (4-5) | Save to Obsidian vault or OpenClaw memory |
| resource (4-5) | Save link to Obsidian, read later queue |
| Any (3) | Mention in digest, let user decide |
| Any (1-2) | Skip or brief mention only |

## Stack-Relevance Keywords

These keywords boost relevance because they match the user's tech stack:

Python, TypeScript, Swift, FastAPI, React, PostgreSQL, Docker,
Cloudflare, LLM, AI, Agent, Automation, MCP, Claude, Anthropic,
OpenAI, GPT, Embedding, RAG, Vector, DuckDB, SQLite, Hetzner, Caddy

## Clawhub Install Criteria

A bookmark qualifies for "install via clawhub" if:
1. It references an agent skill, Claude tool, or MCP server
2. It has a clawhub slug or is listed on clawhub.ai
3. It's a standalone automation that fits the OpenClaw skill model

Otherwise, if it's a promising automation idea but not packaged as a skill,
propose scaffolding it as a new skill under `skills/`.
