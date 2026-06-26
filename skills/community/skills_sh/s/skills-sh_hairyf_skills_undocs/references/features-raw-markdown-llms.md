---
name: undocs-raw-markdown-llms
description: Raw markdown output and LLM-friendly documentation in undocs
---

# Raw Markdown & LLMs

Undocs provides raw markdown output and LLM-friendly documentation for content negotiation and AI consumption.

## Raw Markdown Endpoint

Each page is available as raw markdown at `/raw/[path].md`:

```
/raw/guide.md
/raw/guide/components/components.md
/raw/config.md
```

### Server Route

The raw markdown is served by a server route that:

1. Queries the content collection by path
2. Prepends h1 and blockquote if missing (for title and description)
3. Returns content as `text/markdown; charset=utf-8`

### Content Negotiation

When deployed on Vercel, the md-rewrite module adds routes for content negotiation:

- **Accept header**: `Accept: text/markdown` → redirects to `/raw/[path].md`
- **curl**: Requests with `User-Agent: curl/*` → redirects to raw markdown

```bash
# Fetch raw markdown via curl (automatically gets .md)
curl https://undocs.unjs.io/guide

# Or explicitly request markdown
curl -H "Accept: text/markdown" https://undocs.unjs.io/guide
```

### Alternate Link

Each page includes an alternate link in the HTML head:

```html
<link rel="alternate" href="https://example.com/raw/guide.md" type="text/markdown" />
```

This enables browsers and tools to discover the markdown version.

### Build-Time Generation (Vercel)

For Vercel deployments, the md-rewrite module:

1. After prerender: Converts each HTML page to markdown using mdream's `htmlToMarkdown`
2. Writes files to `public/raw/[path].md`
3. For index: If `llms.txt` exists, copies it as `raw/index.md` instead

This produces static `.md` files for fast content negotiation without runtime conversion.

## LLMs Integration (nuxt-llms)

Undocs integrates [nuxt-llms](https://github.com/unjs/nuxt-llms) for LLM-friendly documentation.

### Endpoints

- `/llms.txt` — Concise documentation summary
- `/llms-full.txt` — Full documentation content

### Configuration

```yaml
# .config/docs.yaml
llms:
  domain: "https://mypackage.unjs.io"
  title: "MyPackage"
  description: "Package description for LLMs"
  full:
    title: "MyPackage"
    description: "Full documentation for MyPackage"
```

### Auto-Defaults

When `llms` is not configured, defaults are derived from:

```typescript
{
  domain: docsconfig.url,
  title: docsconfig.name || "",
  description: docsconfig.description || "",
  full: {
    title: docsconfig.name || "",
    description: docsconfig.description || "",
  },
}
```

### Prerender

Both `/llms.txt` and `/llms-full.txt` are included in nitro prerender routes for static generation.

## Use Cases

### LLM Crawlers

LLM documentation crawlers can fetch `/llms.txt` or `/llms-full.txt` for training or context.

### Content Negotiation

APIs and tools can request `Accept: text/markdown` to get raw content instead of HTML.

### curl / CLI

Developers can quickly fetch documentation as markdown:

```bash
curl -s https://undocs.unjs.io/guide | head -50
```

## Key Points

- Raw markdown available at `/raw/[path].md`
- Content negotiation: Accept header and curl user-agent
- Build-time md generation on Vercel for static delivery
- `/llms.txt` and `/llms-full.txt` for LLM consumption
- Alternate link on each page for markdown discovery

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/server/routes/raw
- https://github.com/unjs/undocs/blob/main/app/modules/md-rewrite.ts
- https://github.com/unjs/undocs/blob/main/cli/setup.mjs
-->
