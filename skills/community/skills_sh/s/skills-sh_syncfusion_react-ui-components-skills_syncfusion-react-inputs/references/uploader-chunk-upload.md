# Chunk Upload – Syncfusion React Uploader

## Table of Contents
- [Overview](#overview)
- [Enabling Chunk Upload](#enabling-chunk-upload)
- [Retry Configuration](#retry-configuration)
- [Pause and Resume](#pause-and-resume)
- [Cancel Upload](#cancel-upload)
- [Chunk Events](#chunk-events)
- [Server-Side Configuration](#server-side-configuration)
- [Gotchas](#gotchas)

---

## Overview

Chunk upload splits large files into smaller pieces and transmits them sequentially to the server using AJAX. Chunks are sent in order; if one fails, subsequent chunks are not sent. Chunk upload also enables pause, resume, and retry for interrupted uploads.

> - Chunk upload works **only in asynchronous mode** (with `asyncSettings.saveUrl`).
> - Only files **larger than `chunkSize`** are chunked. Smaller files upload normally.
> - Pause/Resume is available **only when chunk upload is enabled**.

---

## Enabling Chunk Upload

Set `asyncSettings.chunkSize` to a positive byte value to activate chunking.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove',
    chunkSize: 500000   // 500 KB per chunk
  };

  return <UploaderComponent asyncSettings={asyncSettings} />;
}
```

> `chunkSize` is specified in **bytes**. Example: `500000` = 500 KB, `1000000` = 1 MB.

---

## Retry Configuration

Control retry behavior for failed chunks using `retryCount` and `retryAfterDelay`:

| Property | Default | Description |
|---|---|---|
| `retryCount` | `3` | Number of retry attempts before triggering `failure` |
| `retryAfterDelay` | `500` | Milliseconds to wait before each retry |

```tsx
const asyncSettings = {
  saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
  removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove',
  chunkSize: 500000,
  retryCount: 5,          // Retry up to 5 times
  retryAfterDelay: 3000   // Wait 3 seconds between retries
};

<UploaderComponent asyncSettings={asyncSettings} />
```

> After all retries are exhausted, the upload aborts and the `failure` event fires.

---

## Pause and Resume

Pause and resume in-progress chunk uploads programmatically using the `pause` and `resume` methods, or via the UI pause icon (appears once upload begins).

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);

  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove',
    chunkSize: 500000
  };

  const handlePause = (): void => {
    const files = uploaderRef.current?.getFilesData();
    if (files && files.length > 0) {
      uploaderRef.current?.pause(files[0]);   // Pause the first file
    }
  };

  const handleResume = (): void => {
    const files = uploaderRef.current?.getFilesData();
    if (files && files.length > 0) {
      uploaderRef.current?.resume(files[0]);  // Resume the first file
    }
  };

  return (
    <div>
      <UploaderComponent ref={uploaderRef} asyncSettings={asyncSettings} />
      <button onClick={handlePause}>Pause</button>
      <button onClick={handleResume}>Resume</button>
    </div>
  );
}
```

**Method signatures:**
- `pause(fileData?: FileInfo | FileInfo[], custom?: boolean): void`
- `resume(fileData?: FileInfo | FileInfo[], custom?: boolean): void`

Set `custom = true` when using a custom file list UI.

---

## Cancel Upload

Cancel an in-progress chunk upload using the `cancel` method or the UI cancel icon. When canceled, the partially uploaded file is removed from the server.

```tsx
const handleCancel = (): void => {
  const files = uploaderRef.current?.getFilesData();
  if (files && files.length > 0) {
    uploaderRef.current?.cancel(files);  // Cancel all or specific file(s)
  }
};
```

**After canceling:** The pause icon changes to a retry icon in the UI. Users can click retry to restart the upload from the beginning.

**Retry a canceled file:**
```tsx
const handleRetry = (): void => {
  const files = uploaderRef.current?.getFilesData();
  if (files) {
    // fromcanceledStage=false → restart from the beginning
    uploaderRef.current?.retry(files, false);
  }
};
```

**Method signature:**
- `cancel(fileData?: FileInfo[]): void`
- `retry(fileData?: FileInfo | FileInfo[], fromcanceledStage?: boolean, custom?: boolean): void`

> **Retry behavior difference:**
> - Chunk upload: Resumes from the failed chunk (when `fromcanceledStage=true`)
> - Default upload: Always restarts from the beginning

---

## Chunk Events

| Event | Trigger |
|---|---|
| `chunkSuccess` | Each chunk successfully uploaded |
| `chunkFailure` | A chunk failed to upload |
| `chunkUploading` | Before each chunk upload starts (add params here) |
| `pausing` | When a chunk upload is paused |
| `resuming` | When a paused chunk upload resumes |
| `canceling` | When an upload is canceled |
| `success` | All chunks uploaded successfully (entire file complete) |
| `failure` | All retries exhausted, file upload failed |

```tsx
const onChunkSuccess = (args: any): void => {
  console.log(`Chunk ${args.chunkIndex + 1} of ${args.totalChunk} uploaded`);
  console.log('Chunk size:', args.chunkSize);
};

const onChunkFailure = (args: any): void => {
  console.error(`Chunk ${args.chunkIndex} failed for:`, args.file.name);
  // Set args.cancel = true to prevent triggering the failure event
};

const onChunkUploading = (args: any): void => {
  // Add custom headers for each chunk request
  args.currentRequest.setRequestHeader('chunk-custom', 'value');
};

<UploaderComponent
  asyncSettings={asyncSettings}
  chunkSuccess={onChunkSuccess}
  chunkFailure={onChunkFailure}
  chunkUploading={onChunkUploading}
/>
```

**`chunkSuccess` / `chunkFailure` event arguments:**

| Argument | Description |
|---|---|
| `chunkIndex` | Current chunk index (0-based) |
| `chunkSize` | Size of the current chunk in bytes |
| `file` | FileInfo of the uploading file |
| `totalChunk` | Total number of chunks for this file |
| `cancel` (chunkFailure only) | Set `true` to prevent triggering the `failure` event |

---

## Server-Side Configuration

The server receives chunk data with form fields `chunk-index` and `total-chunk`. Use these to reconstruct the file from parts.

```csharp
public async Task<IActionResult> Save(IFormFile UploadFiles)
{
    try
    {
        if (UploadFiles.Length > 0)
        {
            var fileName = UploadFiles.FileName;

            if (!Directory.Exists(uploads))
                Directory.CreateDirectory(uploads);

            if (UploadFiles.ContentType == "application/octet-stream") // Chunk upload
            {
                var chunkIndex = Request.Form["chunk-index"];
                var totalChunk = Request.Form["total-chunk"];
                var tempFilePath = Path.Combine(uploads, fileName + ".part");

                // Append or create file
                using (var fileStream = new FileStream(
                    tempFilePath,
                    chunkIndex == "0" ? FileMode.Create : FileMode.Append))
                {
                    await UploadFiles.CopyToAsync(fileStream);
                }

                // Last chunk — move to final path
                if (Convert.ToInt32(chunkIndex) == Convert.ToInt32(totalChunk) - 1)
                {
                    var finalPath = Path.Combine(uploads, fileName);
                    System.IO.File.Move(tempFilePath, finalPath);
                    return Ok(new { status = "File uploaded successfully" });
                }

                return Ok(new { status = "Chunk uploaded" });
            }
            else // Normal upload
            {
                var filePath = Path.Combine(uploads, fileName);
                using (var fileStream = new FileStream(filePath, FileMode.Create))
                {
                    await UploadFiles.CopyToAsync(fileStream);
                }
                return Ok(new { status = "File uploaded successfully" });
            }
        }
        return BadRequest(new { status = "No file" });
    }
    catch (Exception ex)
    {
        return StatusCode(500, new { status = "Error", message = ex.Message });
    }
}
```

> Access chunk metadata from form data:
> - `Request.Form["chunk-index"]` — Zero-based index of the current chunk
> - `Request.Form["total-chunk"]` — Total number of chunks for the file

---

## Gotchas

- **`chunkSize` must be positive** — `chunkSize: 0` disables chunking entirely.
- **Chunk upload is sequential** — Chunks are sent one at a time; the next chunk only starts after the previous succeeds.
- **Files smaller than `chunkSize`** upload normally without chunking.
- **Pause/Resume requires chunk upload** — These features do nothing without `chunkSize`.
- **`cancel` removes partial file** — The server should handle incomplete `.part` files; partially uploaded chunks are removed.
- **Retry from canceled stage** — Pass `fromcanceledStage=true` to `retry()` to resume from the failed chunk; `false` restarts from the beginning.
