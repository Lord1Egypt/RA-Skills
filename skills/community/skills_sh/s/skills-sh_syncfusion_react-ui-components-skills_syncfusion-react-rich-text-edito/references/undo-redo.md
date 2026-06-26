# Undo / Redo in Syncfusion React Rich Text Editor

## Overview

The Rich Text Editor includes a built-in undo/redo manager that tracks all content changes. The undo stack is maintained automatically — every formatting action, text input, and paste is recorded.

## Toolbar Buttons

Add `'Undo'` and `'Redo'` to toolbar items:

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: ['Bold', 'Italic', '|', 'Undo', 'Redo']
};

<RichTextEditorComponent toolbarSettings={toolbarSettings}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + Z` | Undo last action |
| `Ctrl + Y` | Redo last undone action |
| `Ctrl + Shift + Z` | Redo (alternate shortcut) |

These shortcuts work out of the box with no configuration.

## Programmatic Undo / Redo

Access the undo/redo manager via the formatter:

```tsx
const rteRef = useRef<RichTextEditorComponent>(null);

// Programmatically undo
const handleUndo = () => {
  (rteRef.current as any).formatter.editorManager.undoRedoManager.undo();
};

// Programmatically redo
const handleRedo = () => {
  (rteRef.current as any).formatter.editorManager.undoRedoManager.redo();
};
```

## Custom Tool with Undo Support

When creating custom toolbar items, set `undo: true` so the action is added to the undo stack:

```tsx
const items = [
  'Bold', 'Italic', '|',
  {
    template: '<button class="e-tbar-btn e-btn">Insert Tag</button>',
    tooltipText: 'Insert custom tag',
    undo: true,  // registers this action in the undo manager
    click: () => {
      rteRef.current?.executeCommand('insertHTML', '<mark>highlighted</mark>');
    }
  },
  '|', 'Undo', 'Redo'
];
```

## Undo Stack Configuration

Control how many steps are retained in the undo history:

```tsx
<RichTextEditorComponent undoRedoSteps={30} undoRedoTimer={300}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

- `undoRedoSteps` — maximum undo history entries (default: 30)
- `undoRedoTimer` — debounce time (ms) before a keystroke is recorded as an undo step (default: 300ms). Lower values = more granular history; higher values = fewer but chunkier steps.
