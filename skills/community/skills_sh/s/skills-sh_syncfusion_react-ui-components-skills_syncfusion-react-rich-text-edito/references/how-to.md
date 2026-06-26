# How-To Guides for Syncfusion React Rich Text Editor

## Table of Contents
- [Capture Ctrl Keys to Update the Value](#capture-ctrl-keys-to-update-the-value)
- [Change Default Font Family](#change-default-font-family)
- [Check Image Size on Upload](#check-image-size-on-upload)
- [Customize Placeholder Style](#customize-placeholder-style)
- [Customize Shortcut Keys](#customize-shortcut-keys)
- [File Attachment](#file-attachment)
- [Format Code Blocks](#format-code-blocks)
- [Position Cursor at End of Content](#position-cursor-at-end-of-content)
- [Rename Images on Server](#rename-images-on-server)
- [RTE Inside a Dialog](#rte-inside-a-dialog)
- [RTE Inside a Tab](#rte-inside-a-tab)
- [Set Cursor at Specific Range](#set-cursor-at-specific-range)
- [Tailwind CSS Preflight Fix](#tailwind-css-preflight-fix)
- [Update Value Programmatically](#update-value-programmatically)

---

## Capture Ctrl Keys to Update the Value

Capture `Ctrl+S` or other key combos to trigger a manual save:

```tsx
const onKeyDown = (args: KeyboardEvent) => {
  if (args.ctrlKey && args.key === 's') {
    args.preventDefault();
    const value = rteRef.current?.value;
    saveToServer(value);
  }
};

<RichTextEditorComponent
  ref={rteRef}
  keyDown={onKeyDown as any}
>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## Change Default Font Family

Set the default font by overriding the editor's CSS and optionally configuring the font picker:

```css
/* Override editor content area font */
.e-richtexteditor .e-rte-content {
  font-family: 'Segoe UI', sans-serif;
}
```

For the font picker dropdown default:

```tsx
const fontFamily: FontFamilyModel = {
  default: 'Segoe UI',
  items: [
    { text: 'Segoe UI', value: 'Segoe UI' },
    { text: 'Arial', value: 'Arial,Helvetica,sans-serif' },
    { text: 'Georgia', value: 'Georgia,serif' },
  ]
};

<RichTextEditorComponent fontFamily={fontFamily}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## Check Image Size on Upload

Validate image file size before allowing the upload using the `imageUploadFailed` or `beforeImageUpload` event:

```tsx
const beforeImageUpload = (args: ImageUploadingEventArgs) => {
  const file = args.filesData[0].rawFile as File;
  const maxSizeKB = 500;
  if (file.size / 1024 > maxSizeKB) {
    args.cancel = true;
    alert(`Image size exceeds ${maxSizeKB}KB. Please upload a smaller file.`);
  }
};

<RichTextEditorComponent
  insertImageSettings={{ saveUrl: 'url' }}
  beforeImageUpload={beforeImageUpload}
>
  <Inject services={[Toolbar, HtmlEditor, Image, QuickToolbar]} />
</RichTextEditorComponent>
```

---

## Customize Placeholder Style

Target the `.e-rte-placeholder` class to style the placeholder text:

```css
.e-richtexteditor .e-rte-placeholder {
  font-family: 'Georgia', serif;
  color: #aaa;
  font-style: italic;
  font-size: 16px;
}
```

---

## Customize Shortcut Keys

Override default shortcuts by configuring the `formatter`:

```tsx
const customShortcuts = {
  keyConfig: {
    bold: 'ctrl+alt+b',
    italic: 'ctrl+alt+i',
    underline: 'ctrl+alt+u',
  }
};

<RichTextEditorComponent formatter={customShortcuts}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## File Attachment

To support file attachments (non-image files), handle them via the `fileAttachmentInserted` event or integrate the `FileManager` module. For custom file attachments with a server upload:

```tsx
const insertFileLink = (fileName: string, fileUrl: string) => {
  const html = `<a href="${fileUrl}" target="_blank">${fileName}</a>`;
  rteRef.current?.executeCommand('insertHTML', html);
};

// Call after uploading file to your server:
insertFileLink('report.pdf', 'url');
```

---

## Format Code Blocks

Using the `CodeBlock` module for inline code:

```tsx
import { CodeBlock } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = { items: ['CodeBlock', 'Bold', 'Italic'] };

<RichTextEditorComponent toolbarSettings={toolbarSettings}>
  <Inject services={[Toolbar, HtmlEditor, CodeBlock]} />
</RichTextEditorComponent>
```

For multi-line code blocks, use `Pre` from the Formats dropdown or insert a `<pre>` block programmatically:

```tsx
rteRef.current?.executeCommand('insertHTML', '<pre><code>const x = 1;</code></pre>');
```

---

## Position Cursor at End of Content

After setting new content or on component creation, move the cursor to the end:

```tsx
const onCreated = () => {
  const rte = rteRef.current as any;
  const editPanel = rte.contentModule.getEditPanel();
  const range = document.createRange();
  const sel = window.getSelection();
  range.selectNodeContents(editPanel);
  range.collapse(false);
  sel?.removeAllRanges();
  sel?.addRange(range);
};

<RichTextEditorComponent ref={rteRef} created={onCreated}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## Rename Images on Server

Use `imageUploadSuccess` to update the image `src` after the server renames the file:

```tsx
const onImageUploadSuccess = (args: ImageSuccessEventArgs) => {
  if (args.e.currentTarget.getResponseHeader('name')) {
    const newName = args.e.currentTarget.getResponseHeader('name');
    const imgUrl = `url/${newName}`;
    (args.file as any).statusCode = '2'; // success
    args.file.name = newName;
    // Update the image src in the editor
    const img = (rteRef.current as any).element.querySelector(`img[data-upload-id="${args.file.id}"]`);
    if (img) img.src = imgUrl;
  }
};
```

---

## RTE Inside a Dialog

When the RTE is inside a dialog (e.g., Syncfusion DialogComponent), the toolbar may not render correctly on first open. Refresh the editor after the dialog opens:

```tsx
const onDialogOpen = () => {
  setTimeout(() => {
    rteRef.current?.refresh();
  }, 100);
};

<DialogComponent opened={onDialogOpen}>
  <RichTextEditorComponent ref={rteRef}>
    <Inject services={[Toolbar, HtmlEditor]} />
  </RichTextEditorComponent>
</DialogComponent>
```

---

## RTE Inside a Tab

Similar to dialog — when a tab containing the RTE becomes active, refresh it:

```tsx
const onTabSelect = (args: SelectEventArgs) => {
  if (args.selectedIndex === 1) { // the tab index containing RTE
    setTimeout(() => {
      rteRef.current?.refresh();
    }, 100);
  }
};
```

---

## Set Cursor at Specific Range

Save a range and restore it later (useful for custom toolbar actions):

```tsx
import { NodeSelection } from '@syncfusion/ej2-react-richtexteditor';

let savedRange: Range;
const nodeSelection = new NodeSelection();

// Save current cursor position
const saveRange = () => {
  savedRange = nodeSelection.getRange(document);
};

// Restore saved cursor position
const restoreRange = () => {
  if (savedRange) {
    nodeSelection.setRange(document, savedRange);
  }
};
```

---

## Tailwind CSS Preflight Fix

If Tailwind's preflight resets are breaking the RTE's styles (buttons appearing unstyled, margins wrong), scope the conflict:

```css
/* In your tailwind.css / global.css */
/* Option 1: Disable preflight in tailwind.config.js */
/* corePlugins: { preflight: false } */

/* Option 2: Reset Tailwind overrides inside RTE only */
.e-richtexteditor button {
  all: revert;
}

.e-richtexteditor * {
  box-sizing: content-box;
}
```

Or in `tailwind.config.js`:
```js
module.exports = {
  corePlugins: {
    preflight: false,
  },
};
```

---

## Update Value Programmatically

Set the editor's value after mount using the ref:

```tsx
// Via property assignment
rteRef.current.value = '<p>New content</p>';

// Via property + dataBind (forces re-render)
if (rteRef.current) {
  rteRef.current.value = '<p>Updated content</p>';
  rteRef.current.dataBind();
}
```

For React state-driven updates, just update the state variable bound to `value`:
```tsx
setContent('<p>Updated via state</p>');
```
