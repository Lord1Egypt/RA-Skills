# Sequential Upload

By default, the Uploader sends all selected files to the server simultaneously (parallel). Sequential upload changes this so files are processed **one at a time** — the next file only starts after the current one completes (success or failure). This reduces server load and upload failures when handling many or large files.

---

## When to Use Sequential Upload

| Use parallel (default) | Use sequential |
|------------------------|----------------|
| Few small files | Many files or large files |
| Server handles concurrent requests well | Server has concurrency limits |
| Upload speed is priority | Upload stability is priority |
| — | Need per-file status logs |

---

## Enabling Sequential Upload

Set `sequentialUpload={true}` on the component. No other configuration is required.

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://your-server/api/FileUploader/Save',
    removeUrl: 'https://your-server/api/FileUploader/Remove',
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      sequentialUpload={true}
    />
  );
}
```

Files are queued in the order they were selected or dropped. The first file uploads immediately; each subsequent file waits for the previous to finish.

---

## Sequential Upload with Manual Trigger

Combine `sequentialUpload` with `autoUpload={false}` to let the user review files before starting the sequential process:

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  sequentialUpload={true}
  autoUpload={false}
/>
```

The Upload button triggers sequential processing. Files are still sent one at a time after the user clicks Upload.

---

## Per-File Progress Tracking

In sequential mode, each file fires its own `progress`, `success`, and `failure` events — making per-file status displays straightforward:

```tsx
import { UploaderComponent, ProgressEventArgs, SuccessEventArgs, FailureEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

interface FileStatus {
  name: string;
  status: 'uploading' | 'success' | 'failed';
  percent?: number;
}

function App() {
  const [fileLog, setFileLog] = useState<FileStatus[]>([]);

  function onProgress(args: ProgressEventArgs) {
    const percent = Math.round((args.e.loaded / args.e.total) * 100);
    setFileLog(prev => {
      const exists = prev.find(f => f.name === args.file.name);
      if (exists) return prev.map(f => f.name === args.file.name ? { ...f, percent } : f);
      return [...prev, { name: args.file.name, status: 'uploading', percent }];
    });
  }

  function onSuccess(args: SuccessEventArgs) {
    if (args.operation === 'upload') {
      setFileLog(prev =>
        prev.map(f => f.name === args.file?.name ? { ...f, status: 'success' } : f)
      );
    }
  }

  function onFailure(args: FailureEventArgs) {
    setFileLog(prev =>
      prev.map(f => f.name === args.file?.name ? { ...f, status: 'failed' } : f)
    );
  }

  return (
    <>
      <UploaderComponent
        asyncSettings={asyncSettings}
        sequentialUpload={true}
        progress={onProgress}
        success={onSuccess}
        failure={onFailure}
      />
      <ul>
        {fileLog.map(f => (
          <li key={f.name}>{f.name} — {f.status} {f.percent !== undefined ? `(${f.percent}%)` : ''}</li>
        ))}
      </ul>
    </>
  );
}
```

---

## Custom HTTP Headers Per File

The `uploading` event fires separately for each file in sequential mode, so headers can be set or customized per file:

```tsx
import { UploaderComponent, UploadingEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  function onUploading(args: UploadingEventArgs) {
    (args.currentRequest as XMLHttpRequest).setRequestHeader('Authorization', `Bearer ${getToken()}`);
    // Can also use per-file metadata if needed
    (args.currentRequest as XMLHttpRequest).setRequestHeader('X-File-Name', args.fileData.name);
  }

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      sequentialUpload={true}
      uploading={onUploading}
    />
  );
}
```

---

## actionComplete: After All Files Finish

The `actionComplete` event fires once after **all files** in the sequential queue have been processed. Use this for final notifications, redirects, or summary views:

```tsx
import { UploaderComponent, ActionCompleteEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  function onActionComplete(args: ActionCompleteEventArgs) {
    const succeeded = args.fileData.filter(f => f.status === 'File uploaded successfully');
    const failed = args.fileData.filter(f => f.statusCode === '0');
    console.log(`Done: ${succeeded.length} succeeded, ${failed.length} failed`);
  }

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      sequentialUpload={true}
      actionComplete={onActionComplete}
    />
  );
}
```

---

## Dynamically Toggling Sequential Upload

Toggle sequential mode at runtime (e.g., via a user preference) using a ref and `dataBind()`:

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useState } from 'react';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);
  const [isSequential, setIsSequential] = useState(false);

  function toggleMode() {
    const next = !isSequential;
    setIsSequential(next);
    if (uploaderRef.current) {
      uploaderRef.current.sequentialUpload = next;
      uploaderRef.current.dataBind();
    }
  }

  return (
    <>
      <button onClick={toggleMode}>
        Mode: {isSequential ? 'Sequential' : 'Parallel'}
      </button>
      <UploaderComponent
        ref={uploaderRef}
        asyncSettings={asyncSettings}
        sequentialUpload={isSequential}
      />
    </>
  );
}
```

> Always call `dataBind()` after updating a property programmatically to ensure the component reflects the new value.

---

## Key Events in Sequential Mode

| Event | When it fires |
|-------|---------------|
| `uploading` | Before each individual file is sent |
| `progress` | During upload of each file |
| `success` | After each file successfully uploads |
| `failure` | If a file fails — next file starts automatically |
| `actionComplete` | After all files in queue are processed |

> A failed file remains in the list with error status and can be retried using the component's `retry` method. Failure does not stop the queue.

---

## See Also

- [Async upload](./async-upload.md) — save/remove config, auto/manual upload
- [Chunk upload](./chunk-upload.md) — large file uploads with pause/resume
- [Events](./events.md) — full event reference
