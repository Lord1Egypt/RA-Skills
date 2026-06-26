# Managing Editor Value in Syncfusion React Rich Text Editor

## Table of Contents
- [Setting Initial Value](#setting-initial-value)
- [Getting Value](#getting-value)
- [Two-Way Binding](#two-way-binding)
- [Auto-Save](#auto-save)
- [Character Count and Max Length](#character-count-and-max-length)
- [Source Code View](#source-code-view)
- [Import and Export](#import-and-export)
- [Markdown Preview](#markdown-preview)
- [Placeholder Text](#placeholder-text)
- [Encoded HTML Value](#encoded-html-value)

## Setting Initial Value

```tsx
// Direct HTML string via value prop
<RichTextEditorComponent value="<p>Hello <b>World</b></p>">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

**Via ref after mount** (useful when value comes from an async source):

```tsx
const rteRef = useRef<RichTextEditorComponent>(null);

useEffect(() => {
  if (rteRef.current) {
    rteRef.current.value = fetchedContent;
  }
}, [fetchedContent]);

<RichTextEditorComponent ref={rteRef}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

## Getting Value

### Via `change` event (most common)

Fires when the editor loses focus and content has changed:

```tsx
import { ChangeEventArgs } from '@syncfusion/ej2-react-richtexteditor';

const onChange = (args: ChangeEventArgs) => {
  console.log(args.value); // HTML string
};

<RichTextEditorComponent change={onChange}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### Via ref property

```tsx
const content = rteRef.current?.value;
```

### Via public methods

```tsx
const htmlContent = rteRef.current?.getHtml();   // returns HTML string
const textContent = rteRef.current?.getText();   // returns plain text (no HTML tags)
```

## Two-Way Binding

Use React `useState` — pass state as `value` and update state in `change`:

```tsx
function App() {
  const [content, setContent] = useState('<p>Initial content</p>');

  return (
    <RichTextEditorComponent
      value={content}
      change={(e: ChangeEventArgs) => setContent(e.value)}
    >
      <Inject services={[Toolbar, HtmlEditor]} />
    </RichTextEditorComponent>
  );
}
```

When state is shared, multiple editor instances stay in sync automatically:

```tsx
function App() {
  const [content, setContent] = useState('Initial content');

  return (
    <>
      <RichTextEditorComponent value={content} change={(e) => setContent(e.value)}>
        <Inject services={[Toolbar, HtmlEditor]} />
      </RichTextEditorComponent>

      <RichTextEditorComponent value={content}>
        <Inject services={[HtmlEditor]} />
      </RichTextEditorComponent>
    </>
  );
}
```

## Auto-Save

Set `saveInterval` (milliseconds) to trigger the `change` event automatically during idle periods — great for drafting without relying on the user to tab out.

```tsx
const onAutoSave = (e: ChangeEventArgs) => {
  localStorage.setItem('draft', e.value);
};

<RichTextEditorComponent saveInterval={2000} change={onAutoSave}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

## Character Count and Max Length

Inject `Count`, set `showCharCount={true}`. Use `maxLength` to cap content length.

```tsx
import { Count } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent showCharCount={true} maxLength={500}>
  <Inject services={[Toolbar, HtmlEditor, Count]} />
</RichTextEditorComponent>
```

Character count color indicators:
- **Black** — below 70% of `maxLength`
- **Orange** — 70–90% (warning)
- **Red** — above 90% (error)

**Get count programmatically:**

```tsx
const count: number = rteRef.current?.getCharCount();
```

## Source Code View

Add `'SourceCode'` to toolbar items to let users toggle between the WYSIWYG view and the raw HTML source.

```tsx
const toolbarSettings: ToolbarSettingsModel = { items: ['Bold', 'Italic', '|', 'SourceCode'] };

// Toggle source view programmatically
rteRef.current?.showSourceCode();
```

## Import and Export

Inject `ImportExport` to add Word import and Word/PDF export capabilities.

```tsx
import { ImportExport } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = {
  items: ['ImportWord', 'ExportWord', 'ExportPdf', '|', 'Bold', 'Italic']
};

const importWord: ImportWordModel = {
  serviceUrl: 'url'
};

const exportWord: ExportWordModel = {
  serviceUrl: 'url',
  fileName: 'MyDocument.docx'
};

const exportPdf: ExportPdfModel = {
  serviceUrl: 'url',
  fileName: 'MyDocument.pdf'
};

<RichTextEditorComponent
  toolbarSettings={toolbarSettings}
  importWord={importWord}
  exportWord={exportWord}
  exportPdf={exportPdf}
>
  <Inject services={[Toolbar, HtmlEditor, ImportExport]} />
</RichTextEditorComponent>
```

## Markdown Preview

In Markdown mode, render a live preview alongside the textarea using `marked`:

```tsx
import { marked } from 'marked';

function rendereComplete() {
  const textarea = (rteRef.current as any).contentModule.getEditPanel() as HTMLTextAreaElement;
  textarea.addEventListener('keyup', () => {
    if (previewRef.current) {
      previewRef.current.innerHTML = marked(textarea.value) as string;
    }
  });
}

<RichTextEditorComponent
  ref={rteRef}
  editorMode="Markdown"
  created={rendereComplete}
>
  <Inject services={[Toolbar, MarkdownEditor]} />
</RichTextEditorComponent>
<div ref={previewRef} className="markdown-preview" />
```

## Placeholder Text

```tsx
<RichTextEditorComponent placeholder="Start typing here...">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

Style the placeholder via CSS:

```css
.e-richtexteditor .e-rte-placeholder {
  font-family: monospace;
  color: #aaa;
  font-style: italic;
}
```

## Encoded HTML Value

Set `enableHtmlEncode={true}` to store and retrieve content as HTML-encoded strings (e.g., `&lt;p&gt;` instead of `<p>`). Useful for safe storage and XSS prevention.

```tsx
<RichTextEditorComponent enableHtmlEncode={true} value={encodedHtmlString}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```
