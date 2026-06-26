---
name: syncfusion-react-markdown-converter
description: Implement the Syncfusion Markdown Converter in React to convert Markdown text into clean HTML. Use this when converting Markdown to HTML in React, integrating a live Markdown preview with the Rich Text Editor in Markdown mode, configuring GFM or line break options, or working with MarkdownConverter.toHtml() and MarkdownConverterOptions. This skill covers the @syncfusion/ej2-markdown-converter package and Markdown Editor integration with HTML preview in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "File Viewers & Editors"
---

# Implementing Syncfusion React Markdown Converter

The Syncfusion Markdown Converter is a lightweight utility that transforms Markdown-formatted text into clean, semantic HTML. It is typically used alongside the Syncfusion React Rich Text Editor (`RichTextEditorComponent`) in Markdown editing mode to provide a live preview of rendered content.

## When to Use This Skill

- Convert Markdown text to HTML in a React application
- Display a live preview of Markdown content as the user types
- Configure conversion behavior (GFM support, line breaks, async mode, error suppression)
- Build a Markdown editor with HTML preview using `RichTextEditorComponent` in Markdown mode
- Integrate `MarkdownConverter.toHtml()` with the Syncfusion React Rich Text Editor

## Documentation and Navigation Guide

### Getting Started
- React setup and project creation (Vite / CRA)
- Installing `@syncfusion/ej2-markdown-converter` and `@syncfusion/ej2-react-richtexteditor`
- CSS imports for the material3 theme
- Module injection (`MarkdownEditor`, `Toolbar`, `Image`, `Link`, `Table`)
- Running the application

### Convert Markdown to HTML — toHtml API
- `MarkdownConverter.toHtml()` method signature
- Basic usage example (standalone, no editor required)
- Supported Markdown elements (headings, lists, tables, links, images, inline styles)
- Using the return value with `dangerouslySetInnerHTML`

### Configurable Options
- `MarkdownConverterOptions` interface
- `async` — asynchronous conversion for large content
- `gfm` — GitHub Flavored Markdown support (default: true)
- `lineBreak` — convert single line breaks to `<br>` (default: false)
- `silence` — suppress errors on invalid Markdown (default: false)
- Full example passing options to `toHtml()`

### Rich Text Editor Integration
- Markdown mode with `editorMode="Markdown"`
- Live preview using `created`, `change`, and `actionComplete` events
- Toolbar configuration for Markdown editing
- `MarkdownFormatter` for custom Markdown syntax
- Custom preview toggle button (full preview pattern)
- Full working example with preview toggle

## Quick Start

Install packages and wire up the converter in three steps:

**1. Install packages:**
```bash
npm install @syncfusion/ej2-markdown-converter
npm install @syncfusion/ej2-react-richtexteditor
```

**2. Import CSS in `src/styles.css`:**
```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-richtexteditor/styles/material3.css';
```

**3. Convert Markdown to HTML:**
```tsx
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

const markdown = '# Hello World\nThis is **Markdown** text.';
const html = MarkdownConverter.toHtml(markdown);
console.log(html);
// Output: <h1>Hello World</h1><p>This is <strong>Markdown</strong> text.</p>
```

## Common Patterns

### Pattern 1: Standalone Conversion (No Editor)
When you only need to convert a Markdown string to HTML without an editor UI:
```tsx
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

const html = MarkdownConverter.toHtml(markdownString);
document.getElementById('preview')!.innerHTML = html as string;
```

### Pattern 2: Live Preview on Keyup
Convert on every keystroke inside a Rich Text Editor textarea:
```tsx
const markdownConversion = () => {
  if (mdsource?.classList.contains('e-active')) {
    const htmlPreview = rteObj.element.querySelector('#' + rteObj.getID() + 'html-view') as HTMLElement;
    htmlPreview.innerHTML = MarkdownConverter.toHtml(
      (rteObj.contentModule.getEditPanel() as HTMLTextAreaElement).value
    ) as string;
  }
};
```

### Pattern 3: Conversion with Options
Disable GFM and enable line-break conversion:
```tsx
const html = MarkdownConverter.toHtml(markdownString, {
  gfm: false,
  lineBreak: true
});
```

### Pattern 4: Side-by-Side Preview with Splitter
For a full editor + preview experience, use the Syncfusion Splitter component alongside the Rich Text Editor in Markdown mode. The preview pane is updated via `updateValue()` on every change event.
📄 **Read:** [references/richtexteditor-integration.md](references/richtexteditor-integration.md) for the full implementation.

## Key Props / API

| API | Type | Default | Purpose |
|-----|------|---------|---------|
| `MarkdownConverter.toHtml(content, options?)` | static method | — | Converts Markdown string to HTML |
| `options.async` | boolean | `false` | Async conversion for large content |
| `options.gfm` | boolean | `true` | GitHub Flavored Markdown support |
| `options.lineBreak` | boolean | `false` | Single line breaks → `<br>` |
| `options.silence` | boolean | `false` | Suppress errors on invalid Markdown |
