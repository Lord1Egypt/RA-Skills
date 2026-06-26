# API Reference – Syncfusion React UploaderComponent

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Model Interfaces](#model-interfaces)

---

## Import

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
```

**JSX usage:**
```tsx
<UploaderComponent ref={uploaderRef} asyncSettings={asyncSettings} />
```

**Ref type:**
```tsx
import React, { useRef } from 'react';
const uploaderRef = useRef<UploaderComponent>(null);
```

---

## Properties

### allowedExtensions
**Type:** `string` | **Default:** `''`

Specifies accepted file extensions as a comma-separated list with leading dots. Files not matching these extensions are rejected.

```tsx
<UploaderComponent allowedExtensions=".jpg,.png,.pdf,.docx" />
```

---

### asyncSettings
**Type:** `AsyncSettingsModel` | **Default:** `{ saveUrl: '', removeUrl: '' }`

Configures the server URLs for save and remove operations, plus chunk upload settings.

```tsx
const asyncSettings = {
  saveUrl: 'https://your-server.com/api/upload/save',
  removeUrl: 'https://your-server.com/api/upload/remove',
  chunkSize: 500000,       // bytes per chunk; 0 = no chunking
  retryCount: 3,           // retry attempts on chunk failure
  retryAfterDelay: 500     // ms delay between retries
};
<UploaderComponent asyncSettings={asyncSettings} />
```

See [AsyncSettingsModel](#asyncsettingsmodel) for the full interface.

---

### autoUpload
**Type:** `boolean` | **Default:** `true`

When `true`, files upload immediately after selection. When `false`, Upload All and Clear All action buttons are displayed for manual control.

```tsx
<UploaderComponent asyncSettings={asyncSettings} autoUpload={false} />
```

---

### buttons
**Type:** `ButtonsPropsModel` | **Default:** `{ browse: 'Browse…', clear: 'Clear', upload: 'Upload' }`

Customizes the text or HTML content of the Browse, Clear, and Upload action buttons.

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  autoUpload={false}
  buttons={{ browse: 'Choose File', clear: 'Clear All', upload: 'Upload All' }}
/>
```

See [ButtonsPropsModel](#buttonspropsmodel) for the interface.

---

### cssClass
**Type:** `string` | **Default:** `''`

Appends one or more custom CSS class names to the Uploader root element.

```tsx
<UploaderComponent asyncSettings={asyncSettings} cssClass="my-uploader compact" />
```

---

### directoryUpload
**Type:** `boolean` | **Default:** `false`

When `true`, allows browsing and uploading an entire folder. All files in the selected directory and its subdirectories are uploaded. Individual file selection is disabled when this is `true`.

```tsx
<UploaderComponent asyncSettings={asyncSettings} directoryUpload={true} />
```

---

### dropArea
**Type:** `string | HTMLElement` | **Default:** `null`

Specifies an external element as the drag-and-drop target. Accepts an `HTMLElement` reference or a CSS selector string. By default, the component itself acts as the drop target.

```tsx
<UploaderComponent asyncSettings={asyncSettings} dropArea="#myDropZone" />
// or
<UploaderComponent asyncSettings={asyncSettings} dropArea={dropAreaRef.current} />
```

---

### dropEffect
**Type:** `DropEffect` | **Default:** `'Default'`

Controls the visual drag effect shown on the drop target. Possible values: `'Default'`, `'Copy'`, `'Move'`, `'Link'`, `'None'`.

```tsx
<UploaderComponent asyncSettings={asyncSettings} dropEffect="Copy" />
```

---

### enableHtmlSanitizer
**Type:** `boolean` | **Default:** `true`

When `true`, strips cross-site scripting (XSS) code from filenames and shows a validation error. Recommended to keep enabled.

```tsx
<UploaderComponent asyncSettings={asyncSettings} enableHtmlSanitizer={true} />
```

---

### enablePersistence
**Type:** `boolean` | **Default:** `false`

Enables state persistence across page reloads.

```tsx
<UploaderComponent asyncSettings={asyncSettings} enablePersistence={true} />
```

---

### enableRtl
**Type:** `boolean` | **Default:** `false`

Renders the component in right-to-left direction for RTL language support.

```tsx
<UploaderComponent asyncSettings={asyncSettings} enableRtl={true} />
```

---

### enabled
**Type:** `boolean` | **Default:** `true`

Enables or disables the component. When `false`, all interactions are blocked.

```tsx
<UploaderComponent asyncSettings={asyncSettings} enabled={false} />
```

---

### files
**Type:** `FilesPropModel[]` | **Default:** `{ name: '', size: null, type: '' }`

Specifies a list of files preloaded on render (previously uploaded files). Required fields: `name`, `size`, `type`.

```tsx
const preloadedFiles = [
  { name: 'Report', size: 120000, type: '.pdf' },
  { name: 'Image',  size: 500000, type: '.png' }
];
<UploaderComponent asyncSettings={asyncSettings} files={preloadedFiles} />
```

See [FilesPropModel](#filespropmodel) for the interface.

---

### htmlAttributes
**Type:** `{ [key: string]: string }` | **Default:** `{}`

Adds arbitrary HTML attributes to the underlying file input element (e.g., `name`, `required`, `accept`).

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  htmlAttributes={{ name: 'uploadedFiles', required: 'required' }}
/>
```

---

### locale
**Type:** `string` | **Default:** `''` (uses global culture `'en-US'`)

Overrides the locale for this component instance. Load translations using `L10n.load()` before setting this.

```tsx
<UploaderComponent asyncSettings={asyncSettings} locale="fr-FR" />
```

---

### maxFileSize
**Type:** `number` | **Default:** `30000000` (~28.6 MB)

Maximum allowed upload file size in bytes. Files exceeding this limit are rejected with a validation error.

```tsx
<UploaderComponent asyncSettings={asyncSettings} maxFileSize={5242880} /> {/* 5 MB */}
```

---

### minFileSize
**Type:** `number` | **Default:** `0`

Minimum required upload file size in bytes. Files below this limit are rejected.

```tsx
<UploaderComponent asyncSettings={asyncSettings} minFileSize={1024} /> {/* 1 KB min */}
```

---

### multiple
**Type:** `boolean` | **Default:** `true`

Allows selecting and uploading multiple files when `true`. When `false`, only a single file can be selected at a time (new selection replaces the previous).

```tsx
<UploaderComponent asyncSettings={asyncSettings} multiple={false} />
```

---

### sequentialUpload
**Type:** `boolean` | **Default:** `false`

When `true`, uploads files one after another (sequentially) instead of simultaneously. The next file starts only after the previous succeeds or fails.

```tsx
<UploaderComponent asyncSettings={asyncSettings} sequentialUpload={true} />
```

---

### showFileList
**Type:** `boolean` | **Default:** `true`

Controls whether the default file list is rendered. Set to `false` to build a fully custom file list UI.

```tsx
<UploaderComponent asyncSettings={asyncSettings} showFileList={false} />
```

---

### template
**Type:** `string | Function` | **Default:** `null`

Specifies an HTML string or function to customize the appearance of each file item in the list.

```tsx
const fileTemplate = () => {
  return (
    <div className="file-row">
      <span className="file-name">${name}</span>
      <span className="file-size">${size} bytes</span>
    </div>
  );
}
<UploaderComponent asyncSettings={asyncSettings} template={fileTemplate} />
```

---

## Methods

All methods are accessed via a component `ref`.

```tsx
const uploaderRef = useRef<UploaderComponent>(null);
// Access: uploaderRef.current?.methodName(...)
```

---

### upload

```ts
upload(files?: FileInfo | FileInfo[], custom?: boolean): void
```

Triggers the upload process for specified files or all queued files.

| Parameter | Type | Description |
|---|---|---|
| `files` | `FileInfo \| FileInfo[]` | Files to upload. If omitted, uploads all queued files. |
| `custom` | `boolean` | Set `true` when using a custom file list UI (`showFileList={false}`). |

```tsx
// Upload all
uploaderRef.current?.upload(uploaderRef.current.getFilesData());

// Upload specific files
uploaderRef.current?.upload([files[0]]);

// Upload with custom UI
uploaderRef.current?.upload(filesData, true);
```

---

### remove

```ts
remove(fileData?: FileInfo | FileInfo[], customTemplate?: boolean, postRawFile?: boolean, args?: MouseEvent | TouchEvent | KeyboardEvent): void
```

Removes a file from the list and optionally calls the remove URL to delete it from the server.

| Parameter | Type | Description |
|---|---|---|
| `fileData` | `FileInfo \| FileInfo[]` | File(s) to remove. If omitted, clears all. |
| `customTemplate` | `boolean` | Set `true` when using custom UI. |

```tsx
uploaderRef.current?.remove(filesData, true);
```

---

### cancel

```ts
cancel(fileData?: FileInfo[]): void
```

Cancels in-progress chunk uploads. Partially uploaded files are removed from the server.

```tsx
const files = uploaderRef.current?.getFilesData();
uploaderRef.current?.cancel(files);
```

---

### pause

```ts
pause(fileData?: FileInfo | FileInfo[], custom?: boolean): void
```

Pauses in-progress chunk uploads. Only available when chunk upload is enabled.

| Parameter | Type | Description |
|---|---|---|
| `fileData` | `FileInfo \| FileInfo[]` | File(s) to pause. |
| `custom` | `boolean` | Set `true` for custom UI. |

```tsx
uploaderRef.current?.pause(files[0]);
```

---

### resume

```ts
resume(fileData?: FileInfo | FileInfo[], custom?: boolean): void
```

Resumes previously paused chunk uploads.

| Parameter | Type | Description |
|---|---|---|
| `fileData` | `FileInfo \| FileInfo[]` | File(s) to resume. |
| `custom` | `boolean` | Set `true` for custom UI. |

```tsx
uploaderRef.current?.resume(files[0]);
```

---

### retry

```ts
retry(fileData?: FileInfo | FileInfo[], fromcanceledStage?: boolean, custom?: boolean): void
```

Retries a canceled or failed file upload.

| Parameter | Type | Description |
|---|---|---|
| `fileData` | `FileInfo \| FileInfo[]` | File(s) to retry. |
| `fromcanceledStage` | `boolean` | `true` = resume from failed chunk; `false` = restart from beginning. |
| `custom` | `boolean` | Set `true` for custom UI. |

```tsx
uploaderRef.current?.retry(files, false); // Restart from beginning
uploaderRef.current?.retry(files, true);  // Resume from failed chunk
```

---

### clearAll

```ts
clearAll(): void
```

Clears all file entries from the list (both queued and uploaded).

```tsx
uploaderRef.current?.clearAll();
```

---

### getFilesData

```ts
getFilesData(index?: number): FileInfo[]
```

Returns the data of all files currently shown in the file list.

| Parameter | Type | Description |
|---|---|---|
| `index` | `number` | Optional. Returns only the file at the specified list index. |

```tsx
const allFiles = uploaderRef.current?.getFilesData();
const firstFile = uploaderRef.current?.getFilesData(0);
```

---

### bytesToSize

```ts
bytesToSize(bytes: number): string
```

Converts a byte value to a human-readable string using binary prefix (KB, MB, GB).

```tsx
const size = uploaderRef.current?.bytesToSize(1048576); // "1 MB"
```

---

### createFileList

```ts
createFileList(fileData: FileInfo[]): void
```

Creates file list items in the UI for the specified file data array.

```tsx
uploaderRef.current?.createFileList(filesData);
```

---

### sortFileList

```ts
sortFileList(filesData?: FileList): File[]
```

Sorts file data alphabetically by file name.

```tsx
const sorted = uploaderRef.current?.sortFileList(rawFileList);
```

---

### getModuleName

```ts
getModuleName(): string
```

Returns the module name of the component (`'uploader'`).

---

### destroy

```ts
destroy(): void
```

Removes the component from the DOM and detaches all event handlers, attributes, and classes.

```tsx
uploaderRef.current?.destroy();
```

---

## Events

All events are passed as props to `UploaderComponent`.

---

### uploading
**Type:** `EmitType<UploadingEventArgs>`

Fires when each file upload process starts. Use to add custom headers or form data.

```tsx
const onUploading = (args: any): void => {
  args.currentRequest.setRequestHeader('Authorization', 'Bearer ' + token);
  args.customFormData = [{ key: 'value' }];
  // args.cancel = true; // Cancel this upload
};
<UploaderComponent asyncSettings={asyncSettings} uploading={onUploading} />
```

**Key args:** `currentRequest` (XMLHttpRequest), `customFormData`, `fileData`, `cancel`

---

### success
**Type:** `EmitType<Object>`

Fires when an upload or remove operation completes successfully.

```tsx
const onSuccess = (args: any): void => {
  // args.operation: 'upload' | 'remove'
  // args.file: FileInfo
  // args.event: Ajax progress event
};
<UploaderComponent asyncSettings={asyncSettings} success={onSuccess} />
```

---

### failure
**Type:** `EmitType<Object>`

Fires when an upload or remove operation fails.

```tsx
const onFailure = (args: any): void => {
  // args.operation: 'upload' | 'remove'
  // args.file: FileInfo
  // args.event: Ajax progress event
};
<UploaderComponent asyncSettings={asyncSettings} failure={onFailure} />
```

---

### selected
**Type:** `EmitType<SelectedEventArgs>`

Fires after files are selected or dropped, before they are added to the upload queue.

```tsx
const onSelected = (args: any): void => {
  // args.filesData: FileInfo[] — selected files
  // args.modifiedFilesData: FileInfo[] — set to filter/sort files
  // args.cancel = true; — cancel adding files to queue
};
<UploaderComponent asyncSettings={asyncSettings} selected={onSelected} />
```

---

### removing
**Type:** `EmitType<RemovingEventArgs>`

Fires before a file is removed from the server. Use to set `postRawFile` or add headers.

```tsx
const onRemoving = (args: any): void => {
  args.postRawFile = false; // Send only file name, not raw file
  args.currentRequest.setRequestHeader('Authorization', 'Bearer ' + token);
};
<UploaderComponent asyncSettings={asyncSettings} removing={onRemoving} />
```

---

### beforeRemove
**Type:** `EmitType<BeforeRemoveEventArgs>`

Fires before the removal request is sent to the server. Use to confirm or cancel removal.

```tsx
const onBeforeRemove = (args: any): void => {
  args.cancel = !window.confirm('Remove this file?');
};
<UploaderComponent asyncSettings={asyncSettings} beforeRemove={onBeforeRemove} />
```

---

### beforeUpload
**Type:** `EmitType<BeforeUploadEventArgs>`

Fires before the upload process starts. Use to add additional parameters.

```tsx
const onBeforeUpload = (args: any): void => {
  // Inspect or modify before upload begins
};
<UploaderComponent asyncSettings={asyncSettings} beforeUpload={onBeforeUpload} />
```

---

### change
**Type:** `EmitType<Object>`

Fires when the file list changes (files added or removed).

```tsx
const onChange = (args: any): void => {
  // args.file: FileInfo — file added or removed
};
<UploaderComponent asyncSettings={asyncSettings} change={onChange} />
```

---

### progress
**Type:** `EmitType<Object>`

Fires during upload to report progress.

```tsx
const onProgress = (args: any): void => {
  const percent = Math.round((args.e.loaded / args.e.total) * 100);
  console.log(`${args.file.name}: ${percent}%`);
};
<UploaderComponent asyncSettings={asyncSettings} progress={onProgress} />
```

**Key args:** `e` (Ajax progress event with `loaded`/`total`), `file` (FileInfo), `name`

---

### chunkSuccess
**Type:** `EmitType<Object>`

Fires when each chunk uploads successfully.

```tsx
const onChunkSuccess = (args: any): void => {
  // args.chunkIndex, args.chunkSize, args.file, args.totalChunk
  console.log(`Chunk ${args.chunkIndex + 1}/${args.totalChunk} done`);
};
<UploaderComponent asyncSettings={asyncSettings} chunkSuccess={onChunkSuccess} />
```

---

### chunkFailure
**Type:** `EmitType<Object>`

Fires when a chunk fails to upload.

```tsx
const onChunkFailure = (args: any): void => {
  // args.chunkIndex, args.file, args.totalChunk
  // args.cancel = true; — prevent triggering the failure event
};
<UploaderComponent asyncSettings={asyncSettings} chunkFailure={onChunkFailure} />
```

---

### chunkUploading
**Type:** `EmitType<UploadingEventArgs>`

Fires before each chunk upload starts. Use to add headers per chunk.

```tsx
const onChunkUploading = (args: any): void => {
  args.currentRequest.setRequestHeader('X-Chunk-Index', args.chunkIndex);
};
<UploaderComponent asyncSettings={asyncSettings} chunkUploading={onChunkUploading} />
```

---

### actionComplete
**Type:** `EmitType<ActionCompleteEventArgs>`

Fires after all selected files have either uploaded successfully or failed.

```tsx
const onActionComplete = (args: any): void => {
  console.log('All uploads complete. Files:', args.fileData);
};
<UploaderComponent asyncSettings={asyncSettings} actionComplete={onActionComplete} />
```

---

### canceling
**Type:** `EmitType<CancelEventArgs>`

Fires when a chunk upload is canceled.

```tsx
<UploaderComponent asyncSettings={asyncSettings} canceling={(args) => console.log('Canceled:', args)} />
```

---

### clearing
**Type:** `EmitType<ClearingEventArgs>`

Fires before the file list is cleared (when the Clear button is clicked).

```tsx
const onClearing = (args: any): void => {
  // args.cancel = true; — prevent clearing
};
<UploaderComponent asyncSettings={asyncSettings} clearing={onClearing} />
```

---

### created
**Type:** `EmitType<Object>`

Fires when the component is created and fully initialized.

```tsx
<UploaderComponent asyncSettings={asyncSettings} created={() => console.log('Uploader ready')} />
```

---

### fileListRendering
**Type:** `EmitType<FileListRenderingEventArgs>`

Fires before each file item is rendered in the list. Use to customize individual list items.

```tsx
const onFileListRendering = (args: any): void => {
  // args.element — the LI element
  // args.fileInfo — FileInfo for this item
  if (args.fileInfo.size > 1000000) {
    args.element.classList.add('large-file');
  }
};
<UploaderComponent asyncSettings={asyncSettings} fileListRendering={onFileListRendering} />
```

---

### pausing
**Type:** `EmitType<PauseResumeEventArgs>`

Fires when a chunk upload is paused.

```tsx
<UploaderComponent asyncSettings={asyncSettings} pausing={(args) => console.log('Paused:', args.file.name)} />
```

---

### resuming
**Type:** `EmitType<PauseResumeEventArgs>`

Fires when a paused chunk upload resumes.

```tsx
<UploaderComponent asyncSettings={asyncSettings} resuming={(args) => console.log('Resumed:', args.file.name)} />
```

---

### rendering *(deprecated)*
**Type:** `EmitType<RenderingEventArgs>`

> **Deprecated.** Use `fileListRendering` instead.

---

## Model Interfaces

### AsyncSettingsModel

```ts
interface AsyncSettingsModel {
  saveUrl?: string;         // URL to handle file save on server
  removeUrl?: string;       // URL to handle file removal from server
  chunkSize?: number;       // Chunk size in bytes (0 = disabled)
  retryCount?: number;      // Retry attempts on chunk failure (default: 3)
  retryAfterDelay?: number; // Delay in ms before retry (default: 500)
}
```

---

### ButtonsPropsModel

```ts
interface ButtonsPropsModel {
  browse?: string | HTMLElement;  // Browse button text/element
  clear?: string | HTMLElement;   // Clear button text/element
  upload?: string | HTMLElement;  // Upload button text/element
}
```

---

### FilesPropModel

```ts
interface FilesPropModel {
  name?: string;   // Required: file name (without path)
  size?: number;   // Required: file size in bytes
  type?: string;   // Required: file extension (e.g., '.pdf')
}
```

---

### FileInfo

```ts
interface FileInfo {
  name: string;             // File name
  size: number;             // File size in bytes
  type: string;             // File extension
  status: string;           // Current status string
  statusCode: string;       // '1' = ready, '2' = uploading, '3' = success, '4' = failed
  rawFile: File | string;   // Raw File object (or string for preloaded)
  validationMessage: string;// Validation error message (if any)
  id?: string;              // Unique identifier
}
```
