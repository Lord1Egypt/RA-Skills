# Toolbar Tools in Syncfusion React Rich Text Editor

## Table of Contents
- [Built-in Tools Reference](#built-in-tools-reference)
- [Text Formatting Tools](#text-formatting-tools)
- [Styling Tools](#styling-tools)
- [Fullscreen Tool](#fullscreen-tool)
- [Custom Toolbar Items](#custom-toolbar-items)

## Built-in Tools Reference

All available built-in toolbar item names to use in `toolbarSettings.items`:

| Tool Name | Description |
|---|---|
| `Bold` | Bold text |
| `Italic` | Italic text |
| `Underline` | Underline text |
| `StrikeThrough` | Strikethrough text |
| `SuperScript` | Superscript |
| `SubScript` | Subscript |
| `FontName` | Font family picker |
| `FontSize` | Font size picker |
| `FontColor` | Text/foreground color |
| `BackgroundColor` | Highlight / background color |
| `LowerCase` | Convert selection to lowercase |
| `UpperCase` | Convert selection to uppercase |
| `Formats` | Heading and paragraph formats (H1–H6, blockquote, pre) |
| `Alignments` | Text alignment (left, center, right, justify) |
| `OrderedList` | Numbered list |
| `UnorderedList` | Bullet list |
| `Indent` | Increase indent |
| `Outdent` | Decrease indent |
| `CreateLink` | Insert/edit hyperlink |
| `Image` | Insert image |
| `Video` | Insert video |
| `Audio` | Insert audio |
| `CreateTable` | Insert table |
| `EmojiPicker` | Open emoji picker |
| `ClearFormat` | Remove all formatting from selection |
| `Print` | Print editor content |
| `SourceCode` | Toggle HTML source code view |
| `FullScreen` | Toggle fullscreen editor |
| `Undo` | Undo last action |
| `Redo` | Redo last undone action |
| `FormatPainter` | Copy and apply formatting |
| `ImportWord` | Import from Word document |
| `ExportWord` | Export to Word document |
| `ExportPdf` | Export to PDF |
| `CodeBlock` | Insert code block |
| `SlashMenu` | Slash command menu (also auto-triggered by `/`) |

## Text Formatting Tools

These cover the most common writing formatting needs:

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: [
    'Bold', 'Italic', 'Underline', 'StrikeThrough',
    'SuperScript', 'SubScript', '|',
    'LowerCase', 'UpperCase', '|',
    'ClearFormat'
  ]
};
```

**Formats** provides block-level formatting (headings, blockquote, code):

```tsx
// Formats dropdown includes: Paragraph, H1-H6, Pre, Blockquote
items: ['Formats', 'Alignments', 'OrderedList', 'UnorderedList']
```

## Styling Tools

Font family, size, color, and background color:

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: [
    'FontName', 'FontSize', 'FontColor', 'BackgroundColor'
  ]
};
```

**Custom font lists** — override the default font families and sizes:

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: ['FontName', 'FontSize', 'FontColor'],
};

const fontFamilySettings: FontFamilyModel = {
  items: [
    { text: 'Segoe UI', value: 'Segoe UI' },
    { text: 'Arial', value: 'Arial,Helvetica,sans-serif' },
    { text: 'Georgia', value: 'Georgia,serif' },
    { text: 'Monospace', value: '"Courier New",Courier,monospace' }
  ]
};

const fontSizeSettings: FontSizeModel = {
  items: [
    { text: '8', value: '8pt' },
    { text: '10', value: '10pt' },
    { text: '12', value: '12pt' },
    { text: '14', value: '14pt' },
    { text: '18', value: '18pt' },
    { text: '24', value: '24pt' }
  ]
};

<RichTextEditorComponent
  toolbarSettings={toolbarSettings}
  fontFamily={fontFamilySettings}
  fontSize={fontSizeSettings}
>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

## Fullscreen Tool

Add `FullScreen` to the toolbar items. When activated, the editor expands to fill the viewport.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: ['Bold', 'Italic', '|', 'FullScreen', 'SourceCode']
};
```

**Toggle fullscreen programmatically:**

```tsx
const rteRef = useRef<RichTextEditorComponent>(null);

const goFullscreen = () => {
  rteRef.current?.showFullScreen();
};
```

## Custom Toolbar Items

Add custom items by providing an object with `template`, `tooltipText`, and `click` handler in the `items` array.

```tsx
const items = [
  'Bold', 'Italic', '|',
  {
    template: '<button class="e-tbar-btn e-btn" tabindex="-1" style="width:100%">' +
              '<div class="e-tbar-btn-text" style="font-weight:500">&#937;</div></button>',
    tooltipText: 'Insert Symbol',
    undo: true,
    click: insertSymbol
  }
];

function insertSymbol() {
  // Use executeCommand to insert text at cursor
  rteRef.current?.executeCommand('insertText', 'Ω');
}

const toolbarSettings = { items };
```

**Using `executeCommand` for custom actions:**

```tsx
// Insert HTML at cursor position
rteRef.current?.executeCommand('insertHTML', '<span class="badge">NEW</span>');

// Insert plain text
rteRef.current?.executeCommand('insertText', 'Hello World');

// Bold the current selection
rteRef.current?.executeCommand('bold');
```

> Set `undo: true` in a custom item's config to make its action undoable via the undo manager.
