# Editor Modes in Syncfusion React Rich Text Editor

## Table of Contents
- [HTML Editor Mode](#html-editor-mode)
- [Markdown Editor Mode](#markdown-editor-mode)
- [IFrame Mode](#iframe-mode)
- [Inline Editing](#inline-editing)
- [Resizable Editor](#resizable-editor)

## HTML Editor Mode

The default mode. The editor operates as a WYSIWYG HTML editor — the user sees formatted output while the component returns valid HTML markup. Inject `HtmlEditor` to enable it.

```tsx
import { HtmlEditor, Image, Inject, Link, QuickToolbar, RichTextEditorComponent, Toolbar } from '@syncfusion/ej2-react-richtexteditor';

function App() {
  const content = '<p>Edit <b>rich text</b> as HTML.</p>';

  return (
    <RichTextEditorComponent height={450} value={content}>
      <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

> The `editorMode` prop defaults to `'HTML'`. You only need to set it explicitly when switching away from HTML.

### IFrame vs DIV Mode

By default the editor renders in a `<div>` (DIV mode). Use `iframeSettings.enable: true` to isolate the editor content inside an `<iframe>` — this prevents parent page styles from leaking into the editor content area.

```tsx
const iframeSettings: IFrameSettingsModel = { enable: true };

<RichTextEditorComponent iframeSettings={iframeSettings}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

When to use IFrame mode:
- Your page has global CSS that interferes with editor content styling
- You need strict style isolation between the editor and the host page
- Embedding the editor inside complex layout systems

## Markdown Editor Mode

Set `editorMode="Markdown"` and inject `MarkdownEditor`. The editor operates on raw Markdown text. Use a third-party library like `marked` to render the Markdown as HTML for preview.

```bash
npm install marked
```

```tsx
import { MarkdownEditor, Image, Inject, Link, RichTextEditorComponent, Toolbar } from '@syncfusion/ej2-react-richtexteditor';
import { marked } from 'marked';
import { useRef, useEffect } from 'react';

function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);
  const initialValue = '**Bold text** and *italic text*\n\n- List item 1\n- List item 2';

  const toolbarSettings: ToolbarSettingsModel = {
    items: [
      'Bold', 'Italic', 'StrikeThrough', '|',
      'Formats', 'OrderedList', 'UnorderedList', '|',
      'CreateLink', 'Image', '|', 'Undo', 'Redo'
    ]
  };

  return (
    <RichTextEditorComponent
      ref={rteRef}
      editorMode="Markdown"
      value={initialValue}
      toolbarSettings={toolbarSettings}
      height={400}
    >
      <Inject services={[Toolbar, MarkdownEditor, Image, Link]} />
    </RichTextEditorComponent>
  );
}
```

### Markdown Preview

To show a live HTML preview alongside the editor, listen to `keyup` on the textarea and render the Markdown:

```tsx
function rendereComplete() {
  const textArea = (rteRef.current as any).contentModule.getEditPanel() as HTMLTextAreaElement;
  textArea.addEventListener('keyup', () => {
    // render into your preview div
    previewRef.current.innerHTML = marked(textArea.value);
  });
}

<RichTextEditorComponent editorMode="Markdown" created={rendereComplete}>
  <Inject services={[Toolbar, MarkdownEditor]} />
</RichTextEditorComponent>
```

### Supported Markdown Tags and Syntax

Block-level: `h1`–`h6`, `blockquote`, `pre`, `p`, `ol`, `ul`  
Inline: `Bold`, `Italic`, `StrikeThrough`, `InlineCode`, `SubScript`, `SuperScript`, `UpperCase`, `LowerCase`

## Inline Editing

Inline editing turns any existing HTML element into an editable RTE without a visible border or toolbar until the user clicks into it. Useful for in-place editing in cards, lists, or dashboards.

```tsx
<RichTextEditorComponent inlineMode={{ enable: true, onSelection: true }}>
  <Inject services={[HtmlEditor, QuickToolbar]} />
</RichTextEditorComponent>
```

- `onSelection: true` — toolbar appears only when user selects text
- `onSelection: false` — toolbar appears on focus

## Resizable Editor

Inject `Resize` to let users drag-resize the editor's height at runtime.

```tsx
import { Resize } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent enableResize={true}>
  <Inject services={[Toolbar, HtmlEditor, Resize]} />
</RichTextEditorComponent>
```

You can also set min/max dimensions:

```tsx
<RichTextEditorComponent
  enableResize={true}
  minHeight="200px"
  maxHeight="600px"
>
  <Inject services={[Toolbar, HtmlEditor, Resize]} />
</RichTextEditorComponent>
```
