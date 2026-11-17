---
name: web-snippet-extractor
description: Extract reusable code snippets, API patterns, and configuration examples from web pages. Use when you find a documentation page, blog post, or tutorial and need to pull out the actionable code blocks, CLI commands, or config snippets without manually scanning the entire page.
metadata:
  openclaw:
    emoji: "✂️"
---

# Web Snippet Extractor

Extract clean, copy-paste-ready code snippets from any web page.

## When to Use

- You found a documentation page and want just the code, not the prose
- You need to collect CLI commands from a tutorial
- You want to extract API examples or configuration blocks from a blog post
- You're building a reference library and need structured snippets with context

## Prerequisites

- `web_fetch` tool available (built into OpenClaw)
- Target URL must be publicly accessible

## Steps

### 1. Fetch the page content

```
web_fetch(url="<target-url>", extractMode="markdown", maxChars=20000)
```

Use `markdown` mode to preserve code block delimitings (```lang ... ```).

### 2. Identify and extract snippets

Look for fenced code blocks in the markdown output. Each snippet should include:

- **Language** (the tag after the opening ```)
- **Title/context** (the heading or paragraph immediately preceding the block)
- **Body** (the code content itself)

### 3. Classify snippets

Tag each extracted snippet:

| Tag | Meaning |
|-----|---------|
| `config` | Configuration files (yaml, toml, json, env) |
| `command` | CLI/shell commands |
| `code` | Source code (any language) |
| `script` | Full automation scripts (bash, python, etc.) |
| `snippet` | Short inline patterns or one-liners |

### 4. Output format

Return snippets as structured blocks:

```markdown
### Snippet 1: <short description>
- **Language:** <lang>
- **Type:** <config|command|code|script|snippet>

```<lang>
<code content>
```
```

### 5. Save to workspace (optional)

If the user wants to persist snippets, write them to a file:

```
workspace/snippets/<slug>.md
```

## Example

**Input:** A URL to a Docker documentation page about `docker compose`
**Output:**

```markdown
### Snippet 1: Start services in detached mode
- **Language:** bash
- **Type:** command

```bash
docker compose up -d
```

### Snippet 2: docker-compose.yml for a web app
- **Language:** yaml
- **Type:** config

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
```
```

## Notes

- Always include the source URL in the output header
- If a page has >10 snippets, summarize the top 5 most relevant by default and offer to list more
- Strip out boilerplate (license headers, import noise) when the user asks for "clean" snippets
- Respect the page's content license; mention attribution when requested
