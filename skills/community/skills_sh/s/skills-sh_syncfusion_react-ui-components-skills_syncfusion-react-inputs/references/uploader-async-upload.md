# Asynchronous File Upload – Syncfusion React Uploader

## Table of Contents
- [Overview](#overview)
- [asyncSettings Configuration](#asyncsettings-configuration)
- [Multiple File Upload](#multiple-file-upload)
- [Single File Upload](#single-file-upload)
- [Save Action](#save-action)
- [Remove Action](#remove-action)
- [Auto Upload](#auto-upload)
- [Sequential Upload](#sequential-upload)
- [Preloaded Files](#preloaded-files)
- [Adding Custom HTTP Headers](#adding-custom-http-headers)
- [Adding Custom Form Data](#adding-custom-form-data)
- [Server-Side Examples](#server-side-examples)

---

## Overview

The Uploader supports asynchronous file uploads. Configure `asyncSettings` with `saveUrl` and optionally `removeUrl` to handle server operations. Files can be uploaded automatically or manually.

---

## asyncSettings Configuration

`asyncSettings` is an `AsyncSettingsModel` object with the following fields:

| Field | Type | Default | Description |
|---|---|---|---|
| `saveUrl` | `string` | `''` | URL to handle file save on the server |
| `removeUrl` | `string` | `''` | URL to handle file removal from the server |
| `chunkSize` | `number` | `0` | Size of each chunk in bytes (0 = no chunking) |
| `retryCount` | `number` | `3` | Number of retry attempts for failed chunk uploads |
| `retryAfterDelay` | `number` | `500` | Delay in milliseconds before retrying a failed chunk |

```tsx
const asyncSettings = {
  saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
  removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
};

<UploaderComponent asyncSettings={asyncSettings} />
```

---

## Multiple File Upload

By default, `multiple` is `true`. Users can select and upload multiple files simultaneously. Selected files appear in a list and persist until cleared.

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  multiple={true}
/>
```

> The `multiple` attribute is added to the underlying `<input>` element when `multiple={true}`.

---

## Single File Upload

Set `multiple={false}` to restrict selection to one file at a time. Each new selection replaces the previous file in the list.

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  multiple={false}
/>
```

---

## Save Action

The `saveUrl` handler processes uploaded files on the server. After a successful upload, the file name turns green. Use the `success` and `failure` events to handle outcomes.

```tsx
function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSuccess = (args: any): void => {
    console.log(`${args.operation} succeeded:`, args.file.name);
  };

  const onFailure = (args: any): void => {
    console.error(`${args.operation} failed:`, args.file.name);
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      success={onSuccess}
      failure={onFailure}
    />
  );
}
```

> Differentiate upload vs. remove by checking `args.operation` (`'upload'` or `'remove'`).

**Cancel upload in the `uploading` event** by setting `args.cancel = true`:

```tsx
const onUploading = (args: any): void => {
  if (someCondition) {
    args.cancel = true; // Cancel this upload
  }
};

<UploaderComponent asyncSettings={asyncSettings} uploading={onUploading} />
```

---

## Remove Action

`removeUrl` is optional. When provided, clicking the delete icon sends a remove request to the server.

```tsx
const asyncSettings = {
  saveUrl: '/api/upload/save',
  removeUrl: '/api/upload/remove'
};

// Only send file name (not full file data) to the server
const onRemoving = (args: any): void => {
  args.postRawFile = false; // Send file name only
};

<UploaderComponent asyncSettings={asyncSettings} removing={onRemoving} />
```

> When `postRawFile` is `true` (default), the full file binary is sent to the remove URL. Set it to `false` to send only the file name.

Files not yet uploaded to the server can be removed without triggering `success`/`failure` events.

---

## Auto Upload

By default, `autoUpload` is `true` — files start uploading immediately on selection. Set `autoUpload={false}` to show Upload All / Clear All action buttons for manual control.

```tsx
// Manual upload — shows "Upload" and "Clear" buttons
<UploaderComponent
  asyncSettings={asyncSettings}
  autoUpload={false}
  buttons={{ browse: 'Choose File', clear: 'Clear All', upload: 'Upload All' }}
/>
```

---

## Sequential Upload

By default, multiple files upload in parallel. Enable `sequentialUpload` to upload one file at a time. The next file starts only after the current one succeeds or fails — reducing server traffic and upload failures.

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  sequentialUpload={true}
/>
```

---

## Preloaded Files

Use the `files` prop to display previously uploaded files on render. Users can view and remove them without re-uploading. Required fields per file: `name`, `size`, `type`.

```tsx
import * as React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const preloadedFiles = [
    { name: 'Nature', size: 500000, type: '.png' },
    { name: 'Report', size: 120000, type: '.pdf' },
    { name: 'Specs', size: 45000, type: '.docx' }
  ];

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      files={preloadedFiles}
    />
  );
}
```

> Preloaded files are rendered with "uploaded successfully" status by default.

---

## Adding Custom HTTP Headers

Use the `uploading` and `removing` events to add request headers (e.g., auth tokens) via `args.currentRequest.setRequestHeader()`.

```tsx
function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const addHeaders = (args: any): void => {
    args.currentRequest.setRequestHeader('custom-header', 'Syncfusion');
    // Or add auth token:
    // args.currentRequest.setRequestHeader('Authorization', 'Bearer ' + token);
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      autoUpload={false}
      uploading={addHeaders}
      removing={addHeaders}
    />
  );
}
```

---

## Adding Custom Form Data

Send additional key-value pairs with each upload request using `args.customFormData` in the `uploading` event.

```tsx
const onUploading = (args: any): void => {
  // Add extra form fields to the upload request
  args.customFormData = [{ companyName: 'Syncfusion INC' }, { userId: '12345' }];
};

<UploaderComponent asyncSettings={asyncSettings} uploading={onUploading} />
```

**Server-side retrieval (C#):**
```csharp
var companyName = HttpContext.Current.Request.Form["companyName"];
var userId = HttpContext.Current.Request.Form["userId"];
```

---

## Server-Side Examples

### Save Action (ASP.NET Core)

```csharp
public async Task<IActionResult> Save(IFormFile UploadFiles)
{
    if (UploadFiles.Length > 0)
    {
        if (!Directory.Exists(uploads))
            Directory.CreateDirectory(uploads);

        var filePath = Path.Combine(uploads, UploadFiles.FileName);
        using (var fileStream = new FileStream(filePath, FileMode.Create))
        {
            await UploadFiles.CopyToAsync(fileStream);
        }
    }
    return Ok();
}
```

### Remove Action (ASP.NET Core)

```csharp
public void Remove(string UploadFiles)
{
    if (UploadFiles != null)
    {
        var filePath = Path.Combine(uploads, UploadFiles);
        if (System.IO.File.Exists(filePath))
            System.IO.File.Delete(filePath);
    }
}
```

### Returning JSON/String/File Response

```csharp
[AcceptVerbs("Post")]
public IActionResult Save()
{
    // JSON response
    try {
        return Json(new { Success = true, Message = "Files uploaded successfully" });
    }
    catch (Exception e) {
        return Json(new { Success = false, Message = "Upload failed: " + e.Message });
    }
}
```

---

## Gotchas

- **`saveUrl` is required** for async upload to work; without it, files cannot be uploaded.
- **`removeUrl` is optional** — if omitted, the delete icon still appears but no server call is made.
- **`autoUpload` defaults to `true`** — set it to `false` explicitly to show manual Upload/Clear buttons.
- **`postRawFile` defaults to `true`** — set to `false` in the `removing` event to send only the filename.
- **Sequential vs. parallel** — parallel is the default; sequential is safer for server rate limits.
