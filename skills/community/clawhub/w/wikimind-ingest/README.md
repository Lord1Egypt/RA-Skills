<div align="center">

# wiki-ingest

**A CatDesk / OpenClaw skill for ingesting content into your [WikiMind](https://github.com/HAL-9909/llm-wikimind) knowledge base.**

[![ClawHub](https://img.shields.io/badge/ClawHub-wikimind--ingest-blue?style=flat-square)](https://clawhub.ai/skills/wikimind-ingest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

**English** | [中文](README.zh.md)

*Part of the [WikiMind](https://github.com/HAL-9909/llm-wikimind) ecosystem — a production implementation of [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).*

</div>

---

## What it does

Say **"add this to my knowledge base"** and the AI will:

1. Read your wiki's schema to understand the domain structure
2. Classify the content (`concept` / `entity` / `comparison` / `source-summary`)
3. Write a properly formatted Markdown page with frontmatter
4. Update the BM25 search index
5. Log the operation

Next time you ask about that topic, your AI searches your wiki first — before going to the web.

---

## Prerequisites

- [WikiMind](https://github.com/HAL-9909/llm-wikimind) installed and configured
- `wiki-kb` MCP server registered in CatDesk/OpenClaw
- `qmd` installed: `pip3 install qmd`

---

## Install

```bash
# Via ClawHub
npx clawhub@latest install wikimind-ingest

# Manual
cp SKILL.md ~/.catpaw/skills/wiki-ingest/SKILL.md
```

---

## Trigger phrases

| Language | Phrases |
|----------|---------|
| English | `add to knowledge base`, `ingest this`, `save to wiki`, `store this note`, `wiki_ingest` |
| Chinese | `加到知识库`, `写入知识库`, `保存到 wiki`, `记录到知识库`, `把这个存起来` |

---

## Related

- [WikiMind](https://github.com/HAL-9909/llm-wikimind) — the knowledge base system this skill writes to
- [Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the original methodology

---

## License

MIT
