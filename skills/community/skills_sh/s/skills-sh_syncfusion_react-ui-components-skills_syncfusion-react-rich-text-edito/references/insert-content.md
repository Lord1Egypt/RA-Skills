# Inserting Content in Syncfusion React Rich Text Editor

## Table of Contents
- [Inserting Tables](#inserting-tables)
- [Inserting Hyperlinks](#inserting-hyperlinks)
- [Code Blocks](#code-blocks)
- [Custom Format Blocks](#custom-format-blocks)

## Inserting Tables

Inject `Table` and add `'CreateTable'` to toolbar items. The editor provides a grid picker to choose rows and columns.

```tsx
import { HtmlEditor, Image, Inject, Link, Table, QuickToolbar, RichTextEditorComponent, Toolbar } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = {
  items: ['Bold', 'Italic', '|', 'CreateTable', '|', 'Undo', 'Redo']
};

function App() {
  return (
    <RichTextEditorComponent toolbarSettings={toolbarSettings}>
      <Inject services={[Toolbar, HtmlEditor, Table, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

### Table Quick Toolbar

When `QuickToolbar` is injected, clicking a table cell shows a context toolbar for table editing. Customize with `quickToolbarSettings.table`:

```tsx
const quickToolbarSettings: QuickToolbarSettingsModel = {
  table: [
    'TableHeader', 'TableRows', 'TableColumns', 'TableCell', '|',
    'BackgroundColor', 'TableRemove', 'TableCellVerticalAlign', 'Styles'
  ]
};

<RichTextEditorComponent quickToolbarSettings={quickToolbarSettings}>
  <Inject services={[Toolbar, HtmlEditor, Table, QuickToolbar]} />
</RichTextEditorComponent>
```

### Table Styles

The `Styles` quick toolbar item provides options to apply alternate row styling and border styles to the table.

## Inserting Hyperlinks

Inject `Link` and add `'CreateLink'` to toolbar items. Users can insert, edit, open, and remove links via the link dialog.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: ['Bold', 'Italic', '|', 'CreateLink', '|', 'Undo', 'Redo']
};

function App() {
  return (
    <RichTextEditorComponent toolbarSettings={toolbarSettings}>
      <Inject services={[Toolbar, HtmlEditor, Link, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

### Configuring Link Settings

```tsx
// Auto-detect and convert URLs to links as user types
<RichTextEditorComponent enableAutoUrl={true}>
  <Inject services={[Toolbar, HtmlEditor, Link]} />
</RichTextEditorComponent>
```

### Link Quick Toolbar

Clicking on an inserted link shows the quick toolbar:

```tsx
const quickToolbarSettings: QuickToolbarSettingsModel = {
  link: ['Open', 'Edit', 'UnLink']
};
```

## Code Blocks

Inject `CodeBlock` and add `'CodeBlock'` to toolbar items. This formats selected inline text as a code snippet with syntax-aware styling.

```tsx
import { CodeBlock } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings = {
  items: ['Bold', 'Italic', '|', 'CodeBlock', '|', 'Undo', 'Redo']
};

function App() {
  return (
    <RichTextEditorComponent toolbarSettings={toolbarSettings}>
      <Inject services={[Toolbar, HtmlEditor, CodeBlock]} />
    </RichTextEditorComponent>
  );
}
```

> `CodeBlock` formats selected text as `<code>` tags. For full code editor panels, consider integrating CodeMirror (see styling-customization.md).

## Custom Format Blocks

Use the `Formats` toolbar item to apply block-level formatting. You can customize the available format options:

```tsx
const format: FormatModel = {
  items: [
    { text: 'Paragraph', value: 'P' },
    { text: 'Heading 1', value: 'H1' },
    { text: 'Heading 2', value: 'H2' },
    { text: 'Heading 3', value: 'H3' },
    { text: 'Blockquote', value: 'BlockQuote' },
    { text: 'Preformatted', value: 'Pre' },
    { text: 'Code', value: 'Code' },
  ]
};

const toolbarSettings = { items: ['Formats'] };

<RichTextEditorComponent toolbarSettings={toolbarSettings} format={format}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### AutoFormat Module

Inject `AutoFormat` to automatically convert Markdown syntax into HTML while the user types — for example typing `**word**` converts to bold without needing the toolbar.

```tsx
import { AutoFormat } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent>
  <Inject services={[Toolbar, HtmlEditor, AutoFormat]} />
</RichTextEditorComponent>
```

Supported auto-conversions include: `**bold**`, `*italic*`, `~~strikethrough~~`, headings, lists, blockquotes, and horizontal rules.
