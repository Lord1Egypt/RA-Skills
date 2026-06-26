# Enter Key & Selection in Syncfusion React Rich Text Editor

## Table of Contents
- [Enter Key Configuration](#enter-key-configuration)
- [Shift+Enter Key Configuration](#shiftenter-key-configuration)
- [Selection API](#selection-api)
- [Cursor Positioning](#cursor-positioning)

## Enter Key Configuration

By default, pressing `Enter` creates a new `<p>` paragraph tag. Change this to `<br>` or `<div>` to match your content requirements.

```tsx
// Default: Enter creates a <p> tag
<RichTextEditorComponent enterKey="P">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>

// Enter creates a <br> line break
<RichTextEditorComponent enterKey="BR">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>

// Enter creates a <div> block
<RichTextEditorComponent enterKey="DIV">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

**When to use each:**
- `P` (default) — standard blog/article content where paragraphs are semantically correct
- `BR` — chat messages, compact text inputs where line breaks are expected
- `DIV` — custom layout scenarios where `<p>` styling causes unwanted margins

## Shift+Enter Key Configuration

Control what `Shift + Enter` produces (default: `<br>`):

```tsx
<RichTextEditorComponent shiftEnterKey="P">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

| Value | Output tag |
|---|---|
| `P` | `<p>` — new paragraph |
| `BR` | `<br>` — line break (default) |
| `DIV` | `<div>` — new div block |

## Selection API

Work with the current text selection in the editor:

```tsx
const rteRef = useRef<RichTextEditorComponent>(null);

// Get selected text (plain text)
const getSelection = () => {
  const selectedText = rteRef.current?.getSelection();
  console.log('Selected:', selectedText);
};

// Select all content in the editor
const selectAll = () => {
  rteRef.current?.selectAll();
};

// Get selection range
const getRange = () => {
  const selection = window.getSelection();
  if (selection && selection.rangeCount > 0) {
    return selection.getRangeAt(0);
  }
};
```

**Listening for selection changes:**

```tsx
const onSelect = (args: SelectEventArgs) => {
  console.log('Selection changed:', args.requestType);
};

<RichTextEditorComponent select={onSelect}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

## Cursor Positioning

### Position cursor at end of content

After setting or updating the value, move the cursor to the end:

```tsx
const rteRef = useRef<RichTextEditorComponent>(null);

const moveCursorToEnd = () => {
  const rte = rteRef.current as any;
  if (rte) {
    const editPanel = rte.contentModule.getEditPanel();
    const range = document.createRange();
    const sel = window.getSelection();
    range.selectNodeContents(editPanel);
    range.collapse(false); // false = collapse to end
    sel?.removeAllRanges();
    sel?.addRange(range);
    editPanel.focus();
  }
};

useEffect(() => {
  moveCursorToEnd();
}, []);
```

### Set cursor at a specific range

```tsx
import { NodeSelection } from '@syncfusion/ej2-react-richtexteditor';

const setCursorAtRange = (range: Range) => {
  const nodeSelection = new NodeSelection();
  nodeSelection.setRange(document, range);
};
```

### Focus the editor programmatically

```tsx
rteRef.current?.focusIn();
```
