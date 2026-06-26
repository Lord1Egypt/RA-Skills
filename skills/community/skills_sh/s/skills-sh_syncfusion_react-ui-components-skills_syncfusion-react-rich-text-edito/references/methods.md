# Rich Text Editor Methods

## Table of Contents
- [Focus & Content Methods](#focus--content-methods)
- [Toolbar Methods](#toolbar-methods)
- [Dialog Methods](#dialog-methods)
- [Selection Methods](#selection-methods)
- [Undo / Redo Methods](#undo--redo-methods)
- [AI Assistant Methods](#ai-assistant-methods)
- [Utility Methods](#utility-methods)
- [Using Methods via Ref](#using-methods-via-ref)

---

## Using Methods via Ref

Access all public methods through a React ref:

```tsx
import { useRef } from 'react';
import { RichTextEditorComponent, Inject, Toolbar, HtmlEditor } from '@syncfusion/ej2-react-richtexteditor';

function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);

  const handleGetContent = () => {
    const html = rteRef.current?.getHtml();
    console.log(html);
  };

  return (
    <>
      <button onClick={handleGetContent}>Get HTML</button>
      <RichTextEditorComponent ref={rteRef}>
        <Inject services={[Toolbar, HtmlEditor]} />
      </RichTextEditorComponent>
    </>
  );
}
```

---

## Focus & Content Methods

### `focusIn(): void`
Programmatically focus the editor.

```tsx
rteRef.current?.focusIn();
```

### `focusOut(): void`
Remove focus from the editor.

```tsx
rteRef.current?.focusOut();
```

### `getHtml(): string`
Returns the full HTML content of the editor.

```tsx
const html: string = rteRef.current?.getHtml();
```

### `getText(): string`
Returns the plain text content (HTML tags stripped).

```tsx
const text: string = rteRef.current?.getText();
```

### `getContent(): Element`
Returns the inner `Element` node of the editor content area.

```tsx
const el: Element = rteRef.current?.getContent();
```

### `getSelectedHtml(): string`
Returns the HTML of the currently selected text.

```tsx
const selectedHtml: string = rteRef.current?.getSelectedHtml();
```

### `getSelection(): string`
Returns the HTML markup of the current selection.

```tsx
const sel: string = rteRef.current?.getSelection();
```

### `getXhtml(): string`
Returns XHTML-validated HTML. Only meaningful when `enableXhtml={true}`.

```tsx
const xhtml: string = rteRef.current?.getXhtml();
```

### `getCharCount(): number`
Returns the current character count.

```tsx
const count: number = rteRef.current?.getCharCount();
```

### `print(): void`
Opens the browser print dialog for the editor content.

```tsx
rteRef.current?.print();
```

### `refreshUI(): void`
Re-renders the editor view. Useful after programmatic DOM changes.

```tsx
rteRef.current?.refreshUI();
```

### `showSourceCode(): void`
Toggles the HTML source code view on/off.

```tsx
rteRef.current?.showSourceCode();
```

### `showFullScreen(): void`
Expands the editor into full-screen mode.

```tsx
rteRef.current?.showFullScreen();
```

### `sanitizeHtml(value: string): string`
Sanitizes an HTML string against XSS. Applicable when editor mode is HTML.

```tsx
const clean: string = rteRef.current?.sanitizeHtml('<script>alert(1)</script><p>safe</p>');
// → '<p>safe</p>'
```

---

## Toolbar Methods

### `enableToolbarItem(items: string | string[], muteToolbarUpdate?: boolean): void`
Enables one or more toolbar items by name.

```tsx
rteRef.current?.enableToolbarItem(['Bold', 'Italic']);
```

### `disableToolbarItem(items: string | string[], muteToolbarUpdate?: boolean): void`
Disables one or more toolbar items.

```tsx
rteRef.current?.disableToolbarItem('Image');
```

> Set `muteToolbarUpdate: true` to suppress the visual toolbar refresh when updating multiple items.

### `removeToolbarItem(items: string | string[]): void`
Permanently removes toolbar items from the toolbar.

```tsx
rteRef.current?.removeToolbarItem(['CreateLink', 'Image']);
```

### `hideInlineToolbar(): void`
Hides the inline/quick toolbar if it is open.

```tsx
rteRef.current?.hideInlineToolbar();
```

### `showInlineToolbar(): void`
Forces the inline/quick toolbar to display.

```tsx
rteRef.current?.showInlineToolbar();
```

---

## Dialog Methods

### `showDialog(type: DialogType): void`
Programmatically opens an insert dialog.

```tsx
import { DialogType } from '@syncfusion/ej2-react-richtexteditor';

rteRef.current?.showDialog(DialogType.InsertImage);
rteRef.current?.showDialog(DialogType.InsertLink);
rteRef.current?.showDialog(DialogType.InsertTable);
rteRef.current?.showDialog(DialogType.InsertAudio);
rteRef.current?.showDialog(DialogType.InsertVideo);
```

### `closeDialog(type: DialogType): void`
Programmatically closes an open dialog.

```tsx
rteRef.current?.closeDialog(DialogType.InsertImage);
```

### `showEmojiPicker(x?: number, y?: number): void`
Opens the emoji picker. Optionally position it at `(x, y)`.

```tsx
rteRef.current?.showEmojiPicker();
rteRef.current?.showEmojiPicker(200, 400); // positioned
```

---

## Selection Methods

### `selectAll(): void`
Selects all content in the editor.

```tsx
rteRef.current?.selectAll();
```

### `getRange(): Range`
Returns the current `Range` object from the editor's selection.

```tsx
const range: Range = rteRef.current?.getRange();
```

### `selectRange(range: Range): void`
Restores a previously captured range (useful for re-focusing after an async operation).

```tsx
const range = rteRef.current?.getRange();
// ... do something async ...
rteRef.current?.selectRange(range);
```

---

## Undo / Redo Methods

### `clearUndoRedo(): void`
Clears both the undo and redo stacks and disables their toolbar buttons.

```tsx
rteRef.current?.clearUndoRedo();
```

---

## AI Assistant Methods

### `executeAIPrompt(prompt: string): void`
Sends a prompt string directly to the AI Assistant for processing.

```tsx
rteRef.current?.executeAIPrompt('Summarize the selected text');
```

### `addAIPromptResponse(outputResponse: string | Object, isFinalUpdate?: boolean): void`
Adds a response to the AI Assistant's last prompt, or appends a new prompt+response object.

- `outputResponse`: Markdown string (auto-converted to HTML) or an object with prompt+response.
- `isFinalUpdate`: Pass `true` when the complete streamed response has been received (hides the stop button).

```tsx
// Streaming response — call multiple times, then finalize:
rteRef.current?.addAIPromptResponse('Here is a partial...', false);
rteRef.current?.addAIPromptResponse('... and the full answer.', true);
```

### `getAIPromptHistory(): PromptModel[]`
Returns the full conversation history (prompts + responses) from the AI Assistant.

```tsx
const history = rteRef.current?.getAIPromptHistory();
console.log(history); // PromptModel[]
```

### `clearAIPromptHistory(): void`
Clears all AI Assistant conversation history.

```tsx
rteRef.current?.clearAIPromptHistory();
```

### `showAIAssistantPopup(): void`
Programmatically opens the AI Assistant popup.

```tsx
rteRef.current?.showAIAssistantPopup();
```

### `hideAIAssistantPopup(): void`
Programmatically closes the AI Assistant popup.

```tsx
rteRef.current?.hideAIAssistantPopup();
```

---

## Utility Methods

### `executeCommand(commandName: CommandName, value?, option?): void`
Executes a built-in editor command programmatically. Covers all formatting, insertion, and navigation commands.

**Common `CommandName` values:**

| Command | Effect |
|---|---|
| `'bold'` | Toggle bold on selection |
| `'italic'` | Toggle italic |
| `'underline'` | Toggle underline |
| `'insertHTML'` | Insert raw HTML at cursor |
| `'insertText'` | Insert plain text at cursor |
| `'insertImage'` | Insert an image |
| `'insertLink'` | Insert a hyperlink |
| `'insertTable'` | Insert a table |
| `'insertAudio'` | Insert audio |
| `'insertVideo'` | Insert video |
| `'undo'` | Undo last action |
| `'redo'` | Redo last undone action |
| `'removeFormat'` | Strip formatting from selection |
| `'importWord'` | Trigger Word import |

```tsx
import { CommandName } from '@syncfusion/ej2-react-richtexteditor';

// Insert bold text
rteRef.current?.executeCommand('bold');

// Insert HTML at cursor
rteRef.current?.executeCommand('insertHTML', '<strong>Injected</strong>');

// Insert a link
rteRef.current?.executeCommand('insertLink', {
  url: 'https://syncfusion.com',
  text: 'Syncfusion',
  title: 'Syncfusion website',
  target: '_blank',
  selection: null
});

// Insert an image
rteRef.current?.executeCommand('insertImage', {
  url: 'url',
  altText: 'Example image',
  width: { width: '300px' },
  height: { height: 'auto' },
  selection: null
});

// Insert a table (3 columns × 2 rows)
rteRef.current?.executeCommand('insertTable', {
  rows: 2,
  columns: 3,
  selection: null
});
```

### `destroy(): void`
Destroys the component, removing all event handlers, attributes, and DOM content.

```tsx
rteRef.current?.destroy();
```
