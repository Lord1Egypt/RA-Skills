# Paste & Clipboard in Syncfusion React Rich Text Editor

## Table of Contents
- [Paste Cleanup](#paste-cleanup)
- [Clipboard Cleanup](#clipboard-cleanup)
- [Exec Command](#exec-command)

## Paste Cleanup

When users paste content from Word, websites, or other editors, it often carries inline styles, classes, and tags that break the editor's visual consistency. Inject `PasteCleanup` to automatically clean pasted content.

```tsx
import { PasteCleanup } from '@syncfusion/ej2-react-richtexteditor';

function App() {
  return (
    <RichTextEditorComponent>
      <Inject services={[Toolbar, HtmlEditor, PasteCleanup]} />
    </RichTextEditorComponent>
  );
}
```

### Paste Cleanup Configuration

Use `pasteCleanupSettings` to control what gets removed or kept:

```tsx
const pasteCleanupSettings = {
  prompt: true,               // Show a dialog asking user to choose paste mode
  plainText: false,           // Paste as plain text (strips all formatting)
  keepFormat: false,          // Keep source formatting
  deniedTags: ['a'],          // Remove these tags from pasted content
  deniedAttrs: ['class', 'id', 'style'],  // Remove these attributes
  allowedStyleProps: ['color', 'font-size', 'font-weight'],  // Keep only these CSS properties
};

<RichTextEditorComponent pasteCleanupSettings={pasteCleanupSettings}>
  <Inject services={[Toolbar, HtmlEditor, PasteCleanup]} />
</RichTextEditorComponent>
```

**Paste modes:**
- `prompt: true` — dialog lets user pick between "Keep Text Only", "Keep Formatting", or "Clean Up CSS"
- `plainText: true` — always paste as plain text, stripping all HTML
- `keepFormat: true` — always keep source formatting (default behavior without PasteCleanup)

### Handling the afterPasteCleanup Event

```tsx
const afterPasteCleanup = (args: PasteCleanupArgs) => {
  console.log('Cleaned paste content:', args.value);
}

<RichTextEditorComponent
  pasteCleanupSettings={pasteCleanupSettings}
  afterPasteCleanup={afterPasteCleanup}
>
  <Inject services={[Toolbar, HtmlEditor, PasteCleanup]} />
</RichTextEditorComponent>
```

## Clipboard Cleanup

Inject `ClipboardCleanup` to clean content automatically when users copy or cut from the editor. This removes unwanted inline styles while preserving the content structure — useful when users copy from the RTE and paste into another application.

```tsx
import { ClipboardCleanup } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent>
  <Inject services={[Toolbar, HtmlEditor, ClipboardCleanup]} />
</RichTextEditorComponent>
```

> `ClipboardCleanup` operates silently on copy/cut. No configuration needed for basic use.

## Exec Command

Use `executeCommand` to programmatically apply formatting or insert content at the cursor position.

```tsx
const rteRef = useRef<RichTextEditorComponent>(null);

// Apply bold to current selection
rteRef.current?.executeCommand('bold');

// Insert HTML at cursor
rteRef.current?.executeCommand('insertHTML', '<strong>Inserted text</strong>');

// Insert plain text
rteRef.current?.executeCommand('insertText', 'Hello World');

// Create a link around selected text
rteRef.current?.executeCommand('createLink', {
  url: 'https://syncfusion.com',
  text: 'Syncfusion',
  title: 'Go to Syncfusion'
});
```

**Common commands:**

| Command | Description |
|---|---|
| `bold` | Toggle bold on selection |
| `italic` | Toggle italic on selection |
| `underline` | Toggle underline on selection |
| `insertHTML` | Insert HTML at cursor |
| `insertText` | Insert plain text at cursor |
| `createLink` | Wrap selection in a link |
| `insertImage` | Insert image at cursor |
| `fontSize` | Set font size (e.g., `'14pt'`) |
| `fontName` | Set font family |
| `foreColor` | Set text color |
| `backColor` | Set background color |

> Always check that the RTE is focused before running `executeCommand`, otherwise the cursor position may be lost.
