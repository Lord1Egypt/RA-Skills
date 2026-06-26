# MarkdownConverter.toHtml() API

The `toHtml` method is the core API of the Syncfusion Markdown Converter. It converts a Markdown string into clean, semantic HTML.

## Method Signature

```tsx
MarkdownConverter.toHtml(
  markdownContent: string,
  options?: MarkdownConverterOptions
): string
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `markdownContent` | `string` | ✓ | The Markdown text to convert |
| `options` | `MarkdownConverterOptions` | ✗ | Optional configuration (see configurable-options.md) |

**Returns:** `string` — the converted HTML markup.

## Import

```tsx
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';
```

## Basic Usage

```tsx
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

const markdownContent = '# Hello World\nThis is **Markdown** text.';
const htmlOutput = MarkdownConverter.toHtml(markdownContent);
console.log(htmlOutput);
// Output: <h1>Hello World</h1><p>This is <strong>Markdown</strong> text.</p>
```

## Supported Markdown Elements

`toHtml` handles all common Markdown syntax out of the box:

| Markdown Syntax | HTML Output |
|-----------------|-------------|
| `# Heading 1` | `<h1>Heading 1</h1>` |
| `## Heading 2` | `<h2>Heading 2</h2>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` or `_italic_` | `<em>italic</em>` |
| `~~strikethrough~~` | `<del>strikethrough</del>` |
| `[link](url)` | `<a href="url">link</a>` |
| `![alt](src)` | `<img alt="alt" src="src">` |
| `` `inline code` `` | `<code>inline code</code>` |
| `> blockquote` | `<blockquote>blockquote</blockquote>` |
| `- item` or `+ item` | `<ul><li>item</li></ul>` |
| `1. item` | `<ol><li>item</li></ol>` |
| `---` | `<hr>` |
| GFM tables | `<table>...</table>` |
| Fenced code blocks (` ``` `) | `<pre><code>...</code></pre>` |

> **GitHub Flavored Markdown (GFM)** is enabled by default, which adds support for tables, strikethrough, and task lists. Disable it by passing `{ gfm: false }` in options.

## Using the Return Value in React

### Binding to dangerouslySetInnerHTML

The most common usage is setting the `innerHTML` of a preview element:

```tsx
import React, { useState } from 'react';
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

function Preview() {
  const [previewHtml, setPreviewHtml] = useState('');

  const onInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const html = MarkdownConverter.toHtml(e.target.value) as string;
    setPreviewHtml(html);
  };

  return (
    <>
      <textarea onInput={onInput} />
      <div dangerouslySetInnerHTML={{ __html: previewHtml }} />
    </>
  );
}
```

> **Security note:** When binding converted HTML to `[innerHTML]`, Use React's `dangerouslySetInnerHTML` only for trusted content. For user-generated content from unknown sources, sanitize the HTML output before binding.

### Direct DOM Manipulation

When working with the Rich Text Editor, direct DOM assignment is typical:

```tsx
const previewEl = document.getElementById('html-preview') as HTMLElement;
previewEl.innerHTML = MarkdownConverter.toHtml(markdownString) as string;
```

## Edge Cases

- **Empty string:** `toHtml('')` returns an empty string — no error thrown.
- **Invalid Markdown:** By default, the converter attempts best-effort conversion. Pass `{ silence: true }` to suppress any errors on malformed input.
- **Large content:** For large documents, pass `{ async: true }` to avoid blocking the main thread.
- **Custom list syntax:** If using `MarkdownFormatter` with custom list tags (e.g., `'+ '` for unordered), the `toHtml` output reflects those custom tags correctly.
