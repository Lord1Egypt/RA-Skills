# Uploader Events

## Table of Contents
- [Event Reference](#event-reference)
- [Lifecycle Events](#lifecycle-events)
- [Selection Events](#selection-events)
- [Pre-Upload Events](#pre-upload-events)
- [Upload Progress Events](#upload-progress-events)
- [Post-Upload Events](#post-upload-events)
- [Remove Events](#remove-events)
- [State Change Events](#state-change-events)
- [Chunk Upload Events](#chunk-upload-events)
- [Common Patterns](#common-patterns)

---

## Event Reference

| Event | Type | Cancelable | When it fires |
|-------|------|-----------|---------------|
| `created` | `EmitType<Object>` | No | Component rendered in DOM |
| `selected` | `EmitType<SelectedEventArgs>` | No | Files selected or dropped |
| `rendering` | `EmitType<RenderingEventArgs>` | Yes | Before each file item renders in list |
| `beforeUpload` | `EmitType<BeforeUploadEventArgs>` | Yes | Before upload request is sent |
| `uploading` | `EmitType<UploadingEventArgs>` | Yes | Immediately before each file is sent (add headers here) |
| `progress` | `EmitType<ProgressEventArgs>` | No | During upload — fires repeatedly as data transfers |
| `success` | `EmitType<SuccessEventArgs>` | No | After file uploads or removes successfully |
| `failure` | `EmitType<FailureEventArgs>` | No | After file upload/remove fails |
| `removing` | `EmitType<RemovingEventArgs>` | Yes | Before a file is removed |
| `fileRemoved` | `EmitType<RemovingEventArgs>` | No | After a file is removed from the list |
| `clearing` | `EmitType<ClearingEventArgs>` | Yes | Before all files are cleared |
| `cleared` | `EmitType<Object>` | No | After all files are cleared |
| `canceling` | `EmitType<CancelEventArgs>` | No | When upload is cancelled |
| `actionComplete` | `EmitType<ActionCompleteEventArgs>` | No | After all queued uploads/removes complete |
| `chunkSuccess` | `EmitType<Object>` | No | After each chunk successfully uploads |
| `chunkFailure` | `EmitType<Object>` | No | After a chunk upload fails |
| `pausing` | `EmitType<PauseResumeEventArgs>` | No | When chunk upload is paused |
| `resuming` | `EmitType<PauseResumeEventArgs>` | No | When chunk upload resumes |

---

## Lifecycle Events

### `created`
Fires after the component mounts. Use to configure drop areas or initialize external state.

```tsx
function onCreated() {
  console.log('Uploader ready');
  // Safe to call .dropArea = ... here
}
<UploaderComponent asyncSettings={asyncSettings} created={onCreated} />
```

### `actionComplete`
Fires once after **all** upload/remove operations in the current batch finish. Provides a summary of all processed files.

```tsx
import { ActionCompleteEventArgs } from '@syncfusion/ej2-react-inputs';

function onActionComplete(args: ActionCompleteEventArgs) {
  const succeeded = args.filesData.filter(f => f.statusCode === '3').length;
  const failed = args.filesData.filter(f => f.statusCode === '0').length;
  console.log(`Complete — ${succeeded} succeeded, ${failed} failed`);
}
<UploaderComponent asyncSettings={asyncSettings} actionComplete={onActionComplete} />
```

---

## Selection Events

### `selected`
Fires after the user selects or drops files. Modify the file list here before upload starts.

```tsx
import { SelectedEventArgs } from '@syncfusion/ej2-react-inputs';

function onSelected(args: SelectedEventArgs) {
  // args.filesData — newly selected files
  // args.modifiedFilesData — set this to override the final file list
  // args.isModified — must be true for modifiedFilesData to take effect

  // Example: filter to images only
  args.filesData = args.filesData.filter(f => (f.rawFile as File).type.startsWith('image/'));
  args.modifiedFilesData = args.filesData;
  args.isModified = true;
}
```

> `args.modifiedFilesData` requires `args.isModified = true` to be honoured.

### `rendering`
Fires before each file item is rendered in the list. Cancel to prevent a specific item from appearing.

```tsx
import { RenderingEventArgs } from '@syncfusion/ej2-react-inputs';

function onRendering(args: RenderingEventArgs) {
  if (args.fileInfo.name.startsWith('_')) {
    args.cancel = true; // hide files starting with underscore
  }
}
<UploaderComponent asyncSettings={asyncSettings} rendering={onRendering} />
```

---

## Pre-Upload Events

### `beforeUpload`
Fires before the upload request is initiated. Cancel here to block the upload entirely.

```tsx
import { BeforeUploadEventArgs } from '@syncfusion/ej2-react-inputs';

function onBeforeUpload(args: BeforeUploadEventArgs) {
  if (!isUserAuthenticated()) {
    args.cancel = true;
    alert('Please log in before uploading files.');
  }
}
<UploaderComponent asyncSettings={asyncSettings} beforeUpload={onBeforeUpload} />
```

### `uploading`
Fires immediately before each file request is sent. The best place to add custom HTTP headers, inject form data, or perform last-minute validation.

```tsx
import { UploadingEventArgs } from '@syncfusion/ej2-react-inputs';

function onUploading(args: UploadingEventArgs) {
  // Add authentication header
  (args.currentRequest as XMLHttpRequest).setRequestHeader('Authorization', `Bearer ${token}`);

  // Attach additional form data
  args.customFormData = [
    { userId: currentUser.id },
    { uploadedAt: new Date().toISOString() },
  ];

  // Cancel if needed
  if (args.fileData.size > 10_000_000) {
    args.cancel = true;
  }
}
```

Key `UploadingEventArgs` properties:
- `currentRequest` — the `XMLHttpRequest` object (set headers here)
- `fileData` — the `FileInfo` for the file being uploaded
- `customFormData` — array of key-value objects to append to the form data
- `cancel` — set to `true` to abort this upload

---

## Upload Progress Events

### `progress`
Fires repeatedly during file transfer. Use to build custom progress indicators.

```tsx
import { ProgressEventArgs } from '@syncfusion/ej2-react-inputs';

function onProgress(args: ProgressEventArgs) {
  const percent = Math.round((args.e.loaded / args.e.total) * 100);
  console.log(`${args.file.name}: ${percent}%`);
  // Update your own progress bar state here
}
<UploaderComponent asyncSettings={asyncSettings} progress={onProgress} />
```

---

## Post-Upload Events

### `success`
Fires after a file uploads or is removed successfully. Differentiate with `args.operation`.

```tsx
import { SuccessEventArgs } from '@syncfusion/ej2-react-inputs';

function onSuccess(args: SuccessEventArgs) {
  if (args.operation === 'upload') {
    console.log('Uploaded:', args.file?.name);
    // Parse server response
    const response = JSON.parse((args.e?.target as XMLHttpRequest).responseText || '{}');
  } else if (args.operation === 'remove') {
    console.log('Removed from server:', args.file?.name);
  }
}
```

### `failure`
Fires when an upload or remove request fails (after all retries are exhausted for chunk uploads).

```tsx
import { FailureEventArgs } from '@syncfusion/ej2-react-inputs';

function onFailure(args: FailureEventArgs) {
  console.error(`Failed: ${args.file?.name}`, {
    statusCode: args.statusCode,
    statusText: args.statusText,
    operation: args.operation,
  });
}
```

---

## Remove Events

### `removing`
Fires before a file is removed. Cancel to prevent removal (e.g., show a confirm dialog first).

```tsx
import { RemovingEventArgs } from '@syncfusion/ej2-react-inputs';

function onRemoving(args: RemovingEventArgs) {
  // Send only filename to server (not raw file binary)
  args.postRawFile = false;

  // Block removal with a confirm
  if (!window.confirm(`Remove ${args.filesData[0]?.name}?`)) {
    args.cancel = true;
  }
}
<UploaderComponent asyncSettings={asyncSettings} removing={onRemoving} />
```

### `fileRemoved`
Fires after a file is removed from the list (local or server).

```tsx
function onFileRemoved(args: RemovingEventArgs) {
  console.log('File removed from list:', args.filesData[0]?.name);
}
```

---

## State Change Events

### `clearing` / `cleared`
`clearing` fires before the Clear All button action — cancel to prevent it. `cleared` fires after all files are removed.

```tsx
import { ClearingEventArgs } from '@syncfusion/ej2-react-inputs';

function onClearing(args: ClearingEventArgs) {
  if (!window.confirm('Clear all files?')) {
    args.cancel = true;
  }
}

function onCleared() {
  console.log('File list cleared');
}

<UploaderComponent
  asyncSettings={asyncSettings}
  clearing={onClearing}
  cleared={onCleared}
/>
```

### `canceling`
Fires when an in-progress upload is cancelled (e.g., via the cancel icon).

```tsx
function onCanceling(args: any) {
  console.log('Upload cancelled:', args.fileData?.name);
}
```

---

## Chunk Upload Events

### `chunkSuccess` / `chunkFailure`
Fire after each chunk succeeds or fails during chunk upload.

```tsx
import { ChunkSuccessEventArgs, ChunkFailureEventArgs } from '@syncfusion/ej2-react-inputs';

function onChunkSuccess(args: ChunkSuccessEventArgs) {
  console.log(`Chunk ${args.chunkIndex + 1}/${args.totalChunk} sent for ${args.file.name}`);
}

function onChunkFailure(args: ChunkFailureEventArgs) {
  console.error(`Chunk ${args.chunkIndex} failed — retrying...`);
}

<UploaderComponent
  asyncSettings={asyncSettings}
  chunkSuccess={onChunkSuccess}
  chunkFailure={onChunkFailure}
/>
```

---

## Common Patterns

### Add custom form data to every upload
```tsx
function onUploading(args: UploadingEventArgs) {
  args.customFormData = [
    { folder: 'user-uploads' },
    { userId: '12345' },
  ];
}
```

### Add a confirm dialog before file removal
```tsx
import { DialogComponent } from '@syncfusion/ej2-react-popups';

function onRemoving(args: RemovingEventArgs) {
  args.cancel = true; // always block immediate removal
  if (window.confirm(`Remove "${args.filesData[0]?.name}" from server?`)) {
    // Manually trigger removal after confirmation
    uploaderRef.current?.remove(args.filesData[0]);
  }
}
```

### Cancel upload based on file content
```tsx
function onUploading(args: UploadingEventArgs) {
  const raw = args.fileData.rawFile as File;
  if (raw.size === 0) {
    args.cancel = true;
    console.warn('Empty file rejected:', args.fileData.name);
  }
}
```

---

## See Also

- [Async upload](./async-upload.md) — `uploading` and `removing` event usage for headers
- [Validation](./validation.md) — using `selected` and `uploading` for file filtering
- [Sequential upload](./sequential-upload.md) — per-file event flow in sequential mode
- [Chunk upload](./chunk-upload.md) — `chunkSuccess`, `chunkFailure` events
