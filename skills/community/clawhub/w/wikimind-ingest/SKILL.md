---
name: wiki-ingest
version: 1.1.0
description: "Ingest articles, docs, notes, and web pages into your local LLM-WikiMind knowledge base (Karpathy's LLM Wiki pattern). Triggers: add to knowledge base, ingest, save to wiki, write to wiki, store this, wiki_ingest, 加到知识库, 写入知识库."
author: HAL-9909
homepage: https://github.com/HAL-9909/llm-wikimind-skill
license: MIT
tags: ["knowledge-base", "wiki", "second-brain", "MCP", "markdown", "local-first", "llm-wiki", "karpathy"]
requires:
  bins: ["python3", "qmd"]
  env: []
  os: ["darwin", "linux"]
---

# wiki-ingest Skill

Ingest content into your local [LLM-WikiMind](https://github.com/HAL-9909/llm-wikimind) knowledge base — a production implementation of [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Prerequisites

1. **LLM-WikiMind installed** — see [setup guide](https://github.com/HAL-9909/llm-wikimind#quick-start)
2. **`wiki-kb` MCP server registered** in CatDesk/OpenClaw
3. **`qmd` installed**: `pip3 install qmd`

## Trigger phrases

- "Add this to my knowledge base"
- "Ingest this article"
- "Save to wiki" / "Write to knowledge base"
- "Store this note"
- `wiki_ingest`
- 加到知识库 / 写入知识库 / 保存到 wiki / 记录到知识库 / 把这个存起来

## Workflow

### Step 1: Read global schema

```bash
cat "$WIKIMIND_ROOT/CLAUDE.md"
```

### Step 2: Classify the content

| Type | Directory | When to use |
|------|-----------|-------------|
| `concept` | `concepts/` | Explaining a concept, pattern, or mechanism |
| `entity` | `entities/` | Describing an API object or class |
| `comparison` | `comparisons/` | Comparing two approaches |
| `source-summary` | `sources/` | Summarizing an article or doc |

### Step 3: Identify the domain

- Use an existing domain (check `CLAUDE.md` for the list)
- Or create a new one: make a directory + `DOMAIN.md` with `keywords` frontmatter

### Step 4: Write the page

**Preferred — use the MCP tool** (if `wiki-kb` server is loaded):

```
wiki_ingest_note(
  title="Page Title",
  content="# Page Title\n\nContent here...",
  domain="my-domain",
  page_type="concept",
  source="https://example.com",
  summary="One-line summary",
  tags=["tag1", "tag2"]
)
```

**Fallback — write the file directly:**

```markdown
---
title: "Page Title"
type: concept
domain: my-domain
source: "https://example.com"
summary: "One-line summary (<=150 chars)"
tags: ["tag1"]
related: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
---

# Page Title

Content here.
```

Save to: `$WIKIMIND_ROOT/<domain>/concepts/page-title.md`

### Step 5: Update the search index

```bash
cd "$WIKIMIND_ROOT" && qmd update
```

### Step 6: Append to log

```bash
echo "## [$(date +%Y-%m-%d)] ingest | Page Title | domain" >> "$WIKIMIND_ROOT/<domain>/log.md"
```

## Quality Standards

**concept pages must include:** definition, motivation, code example, common pitfalls, related links

**entity pages must include:** description, key properties with types, key methods with signatures, usage example, gotchas

**comparison pages must include:** comparison table, when to use each, migration notes

**source-summary pages must include:** original URL, key takeaways (3-7 points), what this adds vs existing knowledge

## Notes

- Never write into `refs/` — that's for bulk-imported raw docs
- `confidence`: `high` for official docs, `medium` for your summaries, `low` for speculation
- After writing, tell the user the file path and a good search query to find it
