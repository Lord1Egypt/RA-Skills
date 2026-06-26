---
name: undocs-page-header-links
description: Page header tools for copying markdown and opening in LLMs (ChatGPT, Claude)
---

# Page Header Links

Undocs provides page header tools for copying markdown content and opening pages in LLMs.

## Built-in Tools

Each documentation page includes a header button group with:

### Copy Page

Copies the raw markdown content of the current page to clipboard. Uses `/raw/[path].md` endpoint.

### Copy Markdown Link

Copies the URL of the raw markdown version to clipboard:

```
https://example.com/raw/guide/components/components.md
```

### View as Markdown

Opens the raw markdown URL in a new tab.

### Open in ChatGPT

Opens ChatGPT with a hint to read the page:

```
Read https://example.com/raw/guide.md so I can ask questions about it.
```

### Open in Claude

Opens Claude with a similar hint to read the page.

## Implementation

The tools are rendered by `PageHeaderLinks` component in the page header:

```vue
<template #links>
  <PageHeaderLinks />
</template>
```

## Raw Markdown URL

The raw markdown URL format:

```
{origin}{baseURL}raw{path}.md
```

Example: `https://undocs.unjs.io/raw/guide/components/components.md`

## Use Cases

### For Agents

- **Copy Page**: Get full markdown content for context
- **Copy Markdown Link**: Share link that returns raw markdown
- **Open in ChatGPT/Claude**: Feed documentation to LLMs for Q&A

### Content Negotiation

Browsers/tools can use `Accept: text/markdown` or curl to get raw markdown from the same path.

## Key Points

- Copy Page fetches `/raw/[path].md` and copies to clipboard
- Copy Markdown Link copies the raw markdown URL
- Open in ChatGPT/Claude pre-fills a read hint for the page
- Tools use VueUse's useClipboard for copy operations

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/components/PageHeaderLinks.vue
- https://github.com/unjs/undocs/blob/main/app/pages/[...slug].vue
-->
