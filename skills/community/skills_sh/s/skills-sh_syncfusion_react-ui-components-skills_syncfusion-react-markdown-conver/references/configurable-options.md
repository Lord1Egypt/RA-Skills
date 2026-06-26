# Configurable Options for Markdown Converter

The `MarkdownConverter.toHtml()` method accepts an optional second argument — a `MarkdownConverterOptions` object — that controls how Markdown is parsed and rendered.

## Method Signature with Options

```tsx
MarkdownConverter.toHtml(markdownContent: string, options?: MarkdownConverterOptions): string;
```

## MarkdownConverterOptions Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `async` | `boolean` | `false` | Enables asynchronous conversion for large content processing |
| `gfm` | `boolean` | `true` | Enables GitHub Flavored Markdown (tables, strikethrough, task lists) |
| `lineBreak` | `boolean` | `false` | Converts single line breaks into `<br>` elements |
| `silence` | `boolean` | `false` | Suppresses errors — skips invalid Markdown instead of throwing |

---

## Option Details

### `async` — Asynchronous Conversion

**Default:** `false`

When `true`, the conversion runs asynchronously, preventing the main thread from being blocked when processing large Markdown documents.

```tsx
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

const html = MarkdownConverter.toHtml(largeMarkdownContent, { async: true });
```

Use `async: true` when converting documents with thousands of lines where synchronous conversion might cause UI freezes.

---

### `gfm` — GitHub Flavored Markdown

**Default:** `true`

GitHub Flavored Markdown extends standard Markdown with:
- **Tables** using pipe syntax (`| col1 | col2 |`)
- **Strikethrough** using `~~text~~`
- **Task lists** using `- [ ]` and `- [x]`
- **Fenced code blocks** with language hints (` ```typescript `)

```tsx
// GFM enabled (default) — tables and strikethrough work
const html = MarkdownConverter.toHtml('| A | B |\n|---|---|\n| 1 | 2 |');
// Output: <table><thead>...</thead><tbody>...</tbody></table>

// GFM disabled — table rendered as plain text
const html = MarkdownConverter.toHtml('| A | B |\n|---|---|\n| 1 | 2 |', { gfm: false });
```

Disable `gfm` only when you need strict CommonMark compatibility or want to avoid GFM-specific parsing behavior.

---

### `lineBreak` — Single Line Break Conversion

**Default:** `false`

By default, a single line break in Markdown is not converted to `<br>` — a blank line is needed to start a new paragraph (standard Markdown behavior). Setting `lineBreak: true` converts every single newline into a `<br>` tag.

```tsx
const markdown = 'Line one\nLine two';

// lineBreak: false (default)
MarkdownConverter.toHtml(markdown);
// Output: <p>Line one Line two</p>

// lineBreak: true
MarkdownConverter.toHtml(markdown, { lineBreak: true });
// Output: <p>Line one<br>Line two</p>
```

Use `lineBreak: true` when your users expect line-by-line formatting, such as in poetry or structured text input.

---

### `silence` — Error Suppression

**Default:** `false`

When `false`, invalid or malformed Markdown may throw an error. When `true`, errors are suppressed and the converter skips the problematic segment rather than throwing.

```tsx
// Without silence — may throw on malformed input
const html = MarkdownConverter.toHtml(potentiallyBadMarkdown);

// With silence — safely skip bad segments
const html = MarkdownConverter.toHtml(potentiallyBadMarkdown, { silence: true });
```

Use `silence: true` when processing user-submitted Markdown where the input quality cannot be guaranteed.

---

## Using Multiple Options Together

Options can be combined freely:

```tsx
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

const markdownContent = `
# Report

Line one
Line two

| Header A | Header B |
|----------|----------|
| Cell 1   | Cell 2   |
`;

const html = MarkdownConverter.toHtml(markdownContent, {
  async: false,
  gfm: true,
  lineBreak: true,
  silence: true
});

console.log(html);
```

## Full React Component Example

```tsx
import React, { useRef, useState } from 'react';
import { RichTextEditorComponent, MarkdownEditor, Inject, Toolbar, Link, Image, Table } from '@syncfusion/ej2-react-richtexteditor';
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);
  const [previewHtml, setPreviewHtml] = useState('');

  const handleChange = () => {
    if (rteRef.current) {
      const textarea = rteRef.current.contentModule.getEditPanel() as HTMLTextAreaElement;
      const html = MarkdownConverter.toHtml(textarea.value, {
        gfm: true,
        lineBreak: false,
        silence: true
      }) as string;
      setPreviewHtml(html);
    }
  };

  return (
    <div>
      <RichTextEditorComponent
        ref={rteRef}
        editorMode="Markdown"
        height="400px"
        change={handleChange}
      >
        <Inject services={[MarkdownEditor, Toolbar, Link, Image, Table]} />
      </RichTextEditorComponent>
      <div dangerouslySetInnerHTML={{ __html: previewHtml }} />
    </div>
  );
}

export default App;
```
