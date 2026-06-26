# Toolbar Configuration in Syncfusion React Rich Text Editor

## Table of Contents
- [Default Toolbar Items](#default-toolbar-items)
- [Toolbar Types](#toolbar-types)
- [Toolbar Position](#toolbar-position)
- [Sticky / Floating Toolbar](#sticky--floating-toolbar)
- [Quick Toolbar](#quick-toolbar)

## Default Toolbar Items

When no `toolbarSettings` is provided, the editor shows a minimal default set. Always configure `toolbarSettings.items` explicitly to control what appears.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: [
    'Bold', 'Italic', 'Underline', 'StrikeThrough',
    'FontName', 'FontSize', 'FontColor', 'BackgroundColor',
    'LowerCase', 'UpperCase', '|',
    'Formats', 'Alignments', 'OrderedList', 'UnorderedList',
    'Outdent', 'Indent', '|',
    'CreateLink', 'Image', '|',
    'ClearFormat', 'Print', 'SourceCode', 'FullScreen', '|',
    'Undo', 'Redo'
  ]
};
```

> `|` inserts a vertical separator. `-` inserts a horizontal separator (MultiRow mode).

## Toolbar Types

Set `toolbarSettings.type` to control how overflow items are handled.

### Expand (default)

Hides overflowing items in a second row. Users click an arrow to reveal them. Best for compact layouts.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  type: 'Expand',
  items: ['Bold', 'Italic', 'Underline', 'FontName', 'FontSize',
          'FontColor', 'Formats', 'Alignments', 'OrderedList',
          'UnorderedList', 'CreateLink', 'Image', 'Undo', 'Redo']
};

<RichTextEditorComponent toolbarSettings={toolbarSettings}>
  <Inject services={[Toolbar, HtmlEditor, Link, Image]} />
</RichTextEditorComponent>
```

### MultiRow

Wraps all items across multiple rows. All items always visible — good for wide screens where every tool needs to be reachable.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  type: 'MultiRow',
  items: ['Bold', 'Italic', 'Underline', 'FontName', 'FontSize',
          'FontColor', 'Formats', 'Alignments', 'OrderedList',
          'UnorderedList', 'CreateLink', 'Image', 'Undo', 'Redo']
};
```

### Scrollable

All items on a single line; the row scrolls horizontally when items overflow. Good when screen space is constrained and you want to avoid wrapping.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  type: 'Scrollable',
  items: ['Bold', 'Italic', 'Underline', 'FontName', 'FontSize',
          'CreateLink', 'Image', 'Undo', 'Redo']
};
```

## Toolbar Position

By default the toolbar sits at the top. Use `toolbarSettings.position` to move it to the bottom.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  position: 'Bottom',
  items: ['Bold', 'Italic', 'Underline', 'CreateLink', 'Undo', 'Redo']
};
```

For precise docs see: [toolbar/toolbar-position.md](https://ej2.syncfusion.com/react/documentation/rich-text-editor/toolbar/toolbar-position)

## Sticky / Floating Toolbar

By default, the toolbar sticks to the top of the viewport while the user scrolls through long content. Control this with `enableFloating` and `floatingToolbarOffset`.

```tsx
// Disable sticky toolbar
const toolbarSettings: ToolbarSettingsModel = {
  enableFloating: false,
  items: ['Bold', 'Italic', 'CreateLink', 'Undo', 'Redo']
};

// Adjust sticky toolbar offset (default 0)
<RichTextEditorComponent
  toolbarSettings={toolbarSettings}
  floatingToolbarOffset={60}  // e.g., accommodate a 60px fixed header
>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

**Toggle sticky toolbar dynamically:**

```tsx
function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);

  const toggleFloating = (enabled: boolean) => {
    if (rteRef.current) {
      rteRef.current.toolbarSettings.enableFloating = enabled;
      rteRef.current.dataBind(); // required to apply property change
    }
  };

  return (
    <>
      <button onClick={() => toggleFloating(true)}>Enable Floating</button>
      <button onClick={() => toggleFloating(false)}>Disable Floating</button>
      <RichTextEditorComponent ref={rteRef} toolbarSettings={{ enableFloating: false, items: ['Bold', 'Italic'] }}>
        <Inject services={[Toolbar, HtmlEditor]} />
      </RichTextEditorComponent>
    </>
  );
}
```

## Quick Toolbar

The quick toolbar is a context-sensitive floating toolbar that appears when users click on specific content (images, links, tables). Inject `QuickToolbar` to enable it.

```tsx
// Default quick toolbar items appear automatically for images and links
<RichTextEditorComponent>
  <Inject services={[Toolbar, HtmlEditor, Image, Link, QuickToolbar]} />
</RichTextEditorComponent>
```

### Customizing Quick Toolbar Items

Use `quickToolbarSettings` to control which actions appear:

```tsx
const quickToolbarSettings: QuickToolbarSettingsModel = {
  image: [
    'Replace', 'Align', 'Caption', 'Remove', 'InsertLink',
    'OpenImageLink', '|', 'EditImageLink', 'RemoveImageLink',
    'Display', 'AltText', 'Dimension'
  ],
  link: ['Open', 'Edit', 'UnLink'],
  table: [
    'TableHeader', 'TableRows', 'TableColumns',
    'TableCell', '|', 'BackgroundColor', 'TableRemove',
    'TableCellVerticalAlign', 'Styles'
  ]
};

<RichTextEditorComponent quickToolbarSettings={quickToolbarSettings}>
  <Inject services={[Toolbar, HtmlEditor, Image, Link, Table, QuickToolbar]} />
</RichTextEditorComponent>
```
