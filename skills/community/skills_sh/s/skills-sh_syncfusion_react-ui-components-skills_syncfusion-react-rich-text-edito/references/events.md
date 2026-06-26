# Rich Text Editor Events

## Table of Contents
- [Lifecycle Events](#lifecycle-events)
- [Content Change Events](#content-change-events)
- [Action Events](#action-events)
- [Toolbar Events](#toolbar-events)
- [Dialog & Popup Events](#dialog--popup-events)
- [Media & File Events](#media--file-events)
- [Paste & Clipboard Events](#paste--clipboard-events)
- [AI Assistant Events](#ai-assistant-events)
- [Resize Events](#resize-events)
- [Slash Menu & Selection Events](#slash-menu--selection-events)
- [Quick Toolbar Events](#quick-toolbar-events)
- [Import / Export Events](#import--export-events)

---

## Lifecycle Events

### `created` — Type: `object` (plain)
Fires when the component is first rendered. Use it to run any post-mount logic. No typed arguments.

```tsx
<RichTextEditorComponent created={() => console.log('RTE ready')}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### `destroyed` — Type: `object` (plain)
Fires when the component is destroyed (unmounted / `destroy()` called). No typed arguments.

```tsx
<RichTextEditorComponent destroyed={() => console.log('RTE destroyed')}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### `focus` — Type: `object` (plain)
Fires when the editor gains focus. No typed arguments.

### `blur` — Type: `object` (plain)
Fires when the editor loses focus. No typed arguments.

```tsx
<RichTextEditorComponent
  focus={() => console.log('focused')}
  blur={() => console.log('blurred')}
>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## Content Change Events

### `change` ← most commonly used — Type: `ChangeEventArgs`
Fires on focus-out when content has been modified.

| Arg | Type | Description |
|---|---|---|
| `value` | `string` | Current HTML (or Markdown) content |
| `isInteracted` | `boolean` | Whether the change was user-driven |
| `name` | `string` | Event name |

```tsx
import { ChangeEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent change={(args: ChangeEventArgs) => {
  console.log(args.value); // HTML string
}}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

**Auto-Save Pattern:**
```tsx
<RichTextEditorComponent
  value={content}
  change={(args: ChangeEventArgs) => setContent(args.value)}
  saveInterval={1000} // Fires change event every 1 second when idle
>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## Action Events

### `actionBegin` — Type: `ActionBeginEventArgs`
Fires **before** a toolbar command executes. Set `args.cancel = true` to prevent it.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to `true` to abort the action |
| `requestType` | `string` | The command being executed (e.g. `'Bold'`) |
| `selectType` | `string` | Selection type |
| `originalEvent` | `MouseEvent \| KeyboardEvent \| DragEvent` | Source event |
| `name` | `string` | Event name |

```tsx
import { ActionBeginEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent actionBegin={(args: ActionBeginEventArgs) => {
  if (args.requestType === 'SourceCode') {
    args.cancel = true; // block source code view
  }
}}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### `actionComplete` — Type: `ActionCompleteEventArgs`
Fires **after** a toolbar command finishes.

| Arg | Type | Description |
|---|---|---|
| `requestType` | `string` | The completed command |
| `editorMode` | `string` | Current editor mode |
| `event` | `MouseEvent \| KeyboardEvent` | Source event |
| `name` | `string` | Event name |

```tsx
import { ActionCompleteEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent actionComplete={(args: ActionCompleteEventArgs) => {
  console.log('Completed:', args.requestType);
}}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## Toolbar Events

### `toolbarClick` — Type: `object` (plain)
Fires when any toolbar item is clicked.

| Arg | Type | Description |
|---|---|---|
| `item` | `ToolbarItemModel` | Clicked toolbar item |
| `originalEvent` | `Event` | Source click event |

```tsx
<RichTextEditorComponent toolbarClick={(args: any) => {
  console.log('Toolbar item clicked:', args.item?.tooltipText);
}}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### `updatedToolbarStatus` — Type: `ToolbarStatusEventArgs`
Fires when toolbar item states (bold/italic/undo/redo active states) are refreshed.

| Arg | Type | Description |
|---|---|---|
| `undo` | `boolean` | Whether undo is available |
| `redo` | `boolean` | Whether redo is available |
| `html` | `object` | HTML mode toolbar state map |
| `markdown` | `object` | Markdown mode toolbar state map |
| `name` | `string` | Event name |

> **Deprecated:** `toolbarStatusUpdate` — use `updatedToolbarStatus` instead.

---

## Dialog & Popup Events

### `beforeDialogOpen` — Type: `BeforeOpenEventArgs`
Fires before any insert dialog (Image, Link, Table, etc.) opens. Cancel with `args.cancel = true`.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to prevent dialog open |
| `maxHeight` | `string` | Dialog max height |
| `container` | `HTMLElement` | Dialog container |
| `element` | `Element` | Dialog element |

### `beforeDialogClose` — Type: `BeforeCloseEventArgs`
Fires before any dialog closes. Cancel with `args.cancel = true`.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to prevent dialog close |
| `isInteracted` | `boolean` | Whether user interacted |
| `container` | `HTMLElement` | Dialog container |
| `element` | `Element` | Dialog element |
| `event` | `Event` | Triggered event |
| `closedBy` | `string` (optional) | How dialog was closed |

```tsx
import { BeforeOpenEventArgs, BeforeCloseEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  beforeDialogOpen={(args: BeforeOpenEventArgs) => {
    console.log('Dialog about to open');
  }}
  beforeDialogClose={(args: BeforeCloseEventArgs) => {
    if (someCondition) args.cancel = true; // prevent close
  }}
>
  <Inject services={[Toolbar, HtmlEditor, Image, Link]} />
</RichTextEditorComponent>
```

### `dialogOpen` / `dialogClose` — Type: `object` (plain)
Fire after a dialog opens or closes. No typed arguments.

### `beforePopupOpen` / `beforePopupClose` — Type: `BeforePopupOpenCloseEventArgs`
Fire before any popup (emoji, link, image) opens or closes. Cancel with `args.cancel = true`.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to prevent popup open/close |
| `element` | `HTMLElement` | Popup element |
| `originalEvent` | `Event` | Source event |
| `popup` | `Popup` | Popup instance |
| `type` | `EditorPopupType` | Type of popup |

---

## Media & File Events

### Image Events

| Event | When | EventArgs Type |
|---|---|---|
| `imageSelected` | Image file selected/dropped into the insert dialog | `SelectedEventArgs` |
| `imageUploading` | During image upload progress | `UploadingEventArgs` |
| `imageUploadSuccess` | Image upload succeeded | `ImageSuccessEventArgs` |
| `imageUploadFailed` | Image upload failed | `ImageFailedEventArgs` |
| `imageRemoving` | Image removed from the insert dialog | `RemovingEventArgs` |
| `afterImageDelete` | Selected image removed from editor content | `AfterImageDeleteEventArgs` |
| `beforeImageDrop` | Before dropping an image into the editor | `ImageDropEventArgs` |

**Image Upload Success Example:**
```tsx
import { ImageSuccessEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  imageUploadSuccess={(args: ImageSuccessEventArgs) => {
    // args.response — server response
    // args.file — FileInfo
    // args.element — the inserted <img> element
    // args.detectImageSource — ImageInputSource
    // args.operation — string
    // args.statusText — string
    const serverPath = JSON.parse(args.response.responseText).url;
    (args.element as HTMLImageElement).setAttribute('src', serverPath);
  }}
>
  <Inject services={[Toolbar, HtmlEditor, Image]} />
</RichTextEditorComponent>
```

**Image Upload Failed Example:**
```tsx
import { ImageFailedEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  imageUploadFailed={(args: ImageFailedEventArgs) => {
    console.log('Upload failed:', args.statusText);
    console.log('File:', args.file);
  }}
>
  <Inject services={[Toolbar, HtmlEditor, Image]} />
</RichTextEditorComponent>
```

### Audio / Video Events

| Event | When | EventArgs Type |
|---|---|---|
| `fileSelected` | Media file selected/dropped | `SelectedEventArgs` |
| `fileUploading` | During media upload progress | `UploadingEventArgs` |
| `fileUploadSuccess` | Media upload succeeded | `object` (plain) |
| `fileUploadFailed` | Media upload failed | `object` (plain) |
| `fileRemoving` | Media removed from insert dialog | `RemovingEventArgs` |
| `afterMediaDelete` | Selected audio/video removed from editor | `AfterMediaDeleteEventArgs` |
| `beforeMediaDrop` | Before dropping media into editor | `MediaDropEventArgs` |

---

## Paste & Clipboard Events

### `beforePasteCleanup` — Type: `PasteCleanupArgs`
Fires before pasted content is cleaned. Inspect or modify the pasted value.

| Arg | Type | Description |
|---|---|---|
| `value` | `string` | Pasted HTML content |
| `filesData` | `FileInfo[]` | Files attached to paste |

```tsx
import { PasteCleanupArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  beforePasteCleanup={(args: PasteCleanupArgs) => {
    console.log('Pasted value:', args.value);
  }}
>
  <Inject services={[Toolbar, HtmlEditor, PasteCleanup]} />
</RichTextEditorComponent>
```

### `afterPasteCleanup` — Type: `object` (plain)
Fires after paste cleanup finishes. No typed arguments.

### `beforeClipboardWrite` — Type: `ClipboardWriteEventArgs`
Fires before writing to clipboard (copy/cut). Can be cancelled.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to prevent clipboard write |
| `clipboardData` | `DataTransfer` | Clipboard data |

---

## AI Assistant Events

### `aiAssistantPromptRequest` — Type: `AIAssistantPromptRequestArgs`
Fires when the user submits a prompt in the AI Assistant. Use it to integrate a custom AI service instead of (or in addition to) the built-in `serviceUrl`.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set `true` to cancel built-in request |
| `prompt` | `string` | User's prompt text |
| `html` | `string` | Selected HTML in editor |
| `text` | `string` | Selected plain text |
| `promptSuggestions` | `string[]` | Available suggestions |
| `responseToolbarItems` | `ToolbarItemModel[]` | Response toolbar config |

```tsx
import { AIAssistantPromptRequestArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  aiAssistantPromptRequest={async (args: AIAssistantPromptRequestArgs) => {
    args.cancel = true; // handle manually
    const reply = await myAIService(args.prompt, args.text);
    rteRef.current?.addAIPromptResponse(reply, true);
  }}
>
  <Inject services={[Toolbar, HtmlEditor, AIAssistant]} />
</RichTextEditorComponent>
```

### `aiAssistantToolbarClick` — Type: `AIAssitantToolbarClickEventArgs`
Fires when the user clicks an item in the AI Assistant response toolbar.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to prevent default action |
| `requestType` | `AssistantToolbarType` | Type of toolbar action |
| `item` | `IAIAssistantToolbarItem` | Clicked item |
| `dataIndex` | `number` | Index of AI response |
| `originalEvent` | `Event` | Source event |

### `aiAssistantStopRespondingClick` — Type: `AIAssistantStopRespondingArgs`
Fires when the user clicks "Stop responding" in the AI Assistant.

| Arg | Type | Description |
|---|---|---|
| `prompt` | `string` | The prompt being responded to |
| `dataIndex` | `number` | Index of AI response |
| `event` | `Event` | Stop click event |

---

## Resize Events

### `resizeStart` / `resizing` / `resizeStop` — Type: `ResizeArgs`
Fire during resize operations (table cells, images, video, or editor body when `enableResize` is true).

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set on `resizeStart` to prevent resize |
| `event` | `MouseEvent \| TouchEvent` | Source event |
| `requestType` | `string` | What is being resized |

```tsx
import { ResizeArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  enableResize={true}
  resizeStart={(args: ResizeArgs) => {
    if (args.requestType === 'Image') {
      args.cancel = true; // prevent image resize
    }
  }}
  resizing={(args: ResizeArgs) => {
    console.log('Resizing:', args.requestType);
  }}
  resizeStop={(args: ResizeArgs) => {
    console.log('Resize stopped:', args.requestType);
  }}
>
  <Inject services={[Toolbar, HtmlEditor, Resize]} />
</RichTextEditorComponent>
```

---

## Slash Menu & Selection Events

### `slashMenuItemSelect` — Type: `SlashMenuItemSelectArgs`
Fires when the user picks an item from the `/` slash menu.

| Arg | Type | Description |
|---|---|---|
| `itemData` | `ISlashMenuItem` | The selected menu item |
| `item` | `HTMLLIElement` | Item DOM element |
| `originalEvent` | `MouseEvent \| KeyboardEvent \| TouchEvent` | Source event |
| `cancel` | `boolean` (optional) | Set to prevent default action |
| `isInteracted` | `boolean` (optional) | Whether user interacted |

```tsx
import { SlashMenuItemSelectArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  slashMenuItemSelect={(args: SlashMenuItemSelectArgs) => {
    if (args.itemData?.text === 'Table') {
      args.cancel = true; // handle Table insertion yourself
    }
  }}
>
  <Inject services={[Toolbar, HtmlEditor, SlashMenu]} />
</RichTextEditorComponent>
```

### `selectionChanged` — Type: `SelectionChangedEventArgs`
Fires when the user makes a non-empty text selection.

| Arg | Type | Description |
|---|---|---|
| `selectedContent` | `string` | Selected HTML content |
| `selection` | `Selection` | Selection object |
| `editorMode` | `EditorMode \| string` | Current editor mode |

---

## Quick Toolbar Events

### `beforeQuickToolbarOpen` — Type: `BeforeQuickToolbarOpenArgs`
Fires before the quick (inline) toolbar opens. Cancel with `args.cancel = true`.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to prevent toolbar open |
| `targetElement` | `Element` | Image/link/table that triggered the toolbar |

```tsx
import { BeforeQuickToolbarOpenArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  beforeQuickToolbarOpen={(args: BeforeQuickToolbarOpenArgs) => {
    if (args.targetElement.tagName === 'IMG') {
      console.log('Opening quick toolbar for image');
    }
  }}
>
  <Inject services={[Toolbar, HtmlEditor, Image, QuickToolbar]} />
</RichTextEditorComponent>
```

### `quickToolbarOpen` / `quickToolbarClose` — Type: `object` (plain)
Fire after the quick toolbar opens or closes. No typed arguments.

---

## Import / Export Events

### `wordImporting` — Type: `UploadingEventArgs`
Fires when a Word import upload begins. Use to add custom form data or headers.

| Arg | Type | Description |
|---|---|---|
| `fileData` | `FileInfo` | Imported file info |
| `customFormData` | `{ [key: string]: Object }[]` | Custom form data to send |
| `cancel` | `boolean` | Set to cancel import |
| `chunkSize` | `number` (optional) | Upload chunk size |
| `currentChunkIndex` | `number` (optional) | Current chunk index |

```tsx
import { UploadingEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  wordImporting={(args: UploadingEventArgs) => {
    args.customFormData = [{ userId: '123', dept: 'admin' }];
  }}
>
  <Inject services={[Toolbar, HtmlEditor, ImportExport]} />
</RichTextEditorComponent>
```

### `documentExporting` — Type: `ExportingEventArgs`
Fires before Word/PDF export request is sent. Use to add custom form data.

| Arg | Type | Description |
|---|---|---|
| `exportType` | `ExportDocumentType` | `'Word'` or `'Pdf'` |
| `customFormData` | `{ [key: string]: Object }[]` | Custom form data to send |
| `currentRequest` | `{ [key: string]: string }[]` | Export request data |

```tsx
import { ExportingEventArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  documentExporting={(args: ExportingEventArgs) => {
    if (args.exportType === 'Word') {
      args.customFormData = [{ userId: '42', format: 'docx' }];
    }
  }}
>
  <Inject services={[Toolbar, HtmlEditor, ImportExport]} />
</RichTextEditorComponent>
```

### `beforeSanitizeHtml` — Type: `BeforeSanitizeHtmlArgs`
Fires before HTML sanitization (HTML mode only). Override sanitization rules or cancel.

| Arg | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to cancel sanitization |
| `selectors` | `SanitizeSelectors` (optional) | Sanitization rules |
| `helper` | `Function` (optional) | Sanitization helper function |

```tsx
import { BeforeSanitizeHtmlArgs } from '@syncfusion/ej2-react-richtexteditor';

<RichTextEditorComponent
  beforeSanitizeHtml={(args: BeforeSanitizeHtmlArgs) => {
    // Custom sanitization logic
  }}
>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```
