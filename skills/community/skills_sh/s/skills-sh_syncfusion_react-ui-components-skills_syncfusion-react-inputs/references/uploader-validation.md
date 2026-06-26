# Validation – Syncfusion React Uploader

## Table of Contents
- [Overview](#overview)
- [File Type Validation](#file-type-validation)
- [File Size Validation](#file-size-validation)
- [Maximum Files Count](#maximum-files-count)
- [Duplicate File Prevention](#duplicate-file-prevention)
- [Drag-and-Drop Image Validation](#drag-and-drop-image-validation)
- [Required Field Validation](#required-field-validation)
- [Gotchas](#gotchas)

---

## Overview

The Uploader validates files by extension and size using built-in properties. Custom logic for max file count, duplicates, and drag-and-drop validation is handled via the `selected` event. Validation runs during both file selection (browse button) and drag-and-drop operations.

---

## File Type Validation

Use `allowedExtensions` to restrict accepted file formats. Specify a comma-separated list of extensions (with leading dots).

```tsx
// Allow only PDF and Word documents
<UploaderComponent
  asyncSettings={asyncSettings}
  allowedExtensions=".pdf,.doc,.docx"
/>

// Allow only images
<UploaderComponent
  asyncSettings={asyncSettings}
  allowedExtensions=".jpg,.jpeg,.png,.gif,.bmp"
/>
```

> **Drag-and-drop limitation** — `allowedExtensions` filters files in the browse dialog but does **not** automatically filter drag-and-drop files. Use the `selected` event to manually validate dropped files (see [Drag-and-Drop Image Validation](#drag-and-drop-image-validation)).

You can also set the HTML `accept` attribute via `htmlAttributes`:

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  htmlAttributes={{ accept: '.pdf,.docx' }}
/>
```

---

## File Size Validation

Set `minFileSize` and `maxFileSize` (in bytes) to reject files outside the acceptable size range.

| Property | Default | Description |
|---|---|---|
| `minFileSize` | `0` | Minimum allowed size in bytes |
| `maxFileSize` | `30000000` (~28.6 MB) | Maximum allowed size in bytes |

```tsx
// Allow only files between 1 KB and 5 MB
<UploaderComponent
  asyncSettings={asyncSettings}
  minFileSize={1024}
  maxFileSize={5242880}
/>
```

**Convert bytes to human-readable format** using `bytesToSize`:

```tsx
import { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);

  const onUploading = (args: any): void => {
    // Convert file size to KB/MB string
    const sizeStr = uploaderRef.current?.bytesToSize(args.fileData.size);
    console.log('File size:', sizeStr);
  };

  return (
    <UploaderComponent
      ref={uploaderRef}
      asyncSettings={asyncSettings}
      uploading={onUploading}
    />
  );
}
```

---

## Maximum Files Count

Limit the number of files in the upload queue using the `selected` event. Access current files with `getFilesData()` and modify `eventArgs.modifiedFilesData` to filter selections.

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

const MAX_FILES = 5;

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);

  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSelected = (args: any): void => {
    const existingFiles = uploaderRef.current?.getFilesData() ?? [];
    const totalCount = existingFiles.length + args.filesData.length;

    if (totalCount > MAX_FILES) {
      // Keep only up to MAX_FILES
      const allowed = MAX_FILES - existingFiles.length;
      args.modifiedFilesData = args.filesData.slice(0, allowed);
      console.warn(`Max ${MAX_FILES} files allowed. Extra files removed.`);
    }
  };

  return (
    <UploaderComponent
      ref={uploaderRef}
      asyncSettings={asyncSettings}
      selected={onSelected}
    />
  );
}
```

---

## Duplicate File Prevention

Prevent the same file from being added twice by comparing names in the `selected` event.

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);

  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSelected = (args: any): void => {
    const existingFiles = uploaderRef.current?.getFilesData() ?? [];
    const existingNames = new Set(existingFiles.map((f: any) => f.name));

    // Remove duplicates from new selection
    args.modifiedFilesData = args.filesData.filter(
      (file: any) => !existingNames.has(file.name)
    );

    if (args.modifiedFilesData.length < args.filesData.length) {
      console.warn('Duplicate files removed from selection.');
    }
  };

  return (
    <UploaderComponent
      ref={uploaderRef}
      asyncSettings={asyncSettings}
      selected={onSelected}
    />
  );
}
```

---

## Drag-and-Drop Image Validation

By default, `allowedExtensions` is not enforced during drag-and-drop. Validate dropped files manually in the `selected` event.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

const ALLOWED_IMAGE_TYPES = ['image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/tiff'];

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSelected = (args: any): void => {
    // Filter to images only (for drag-and-drop scenarios)
    args.modifiedFilesData = args.filesData.filter((file: any) =>
      ALLOWED_IMAGE_TYPES.includes(file.rawFile.type)
    );
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      allowedExtensions=".jpg,.jpeg,.png,.gif,.bmp,.tiff"
      selected={onSelected}
    />
  );
}
```

> Setting `allowedExtensions="image/*"` restricts the browse dialog to images, but drag-and-drop still needs the `selected` event filter.

---

## Required Field Validation

Apply the `required` attribute via `htmlAttributes` to enforce that the uploader has files before form submission. Use `data-required-message` for a custom validation message.

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  htmlAttributes={{
    required: 'required',
    'data-required-message': 'Please select at least one file'
  }}
/>
```

---

## Gotchas

- **Drag-and-drop bypasses `allowedExtensions`** — Always add manual validation in `selected` for dropped files.
- **`minFileSize` default is 0** — Empty files (0 bytes) are allowed by default unless you set `minFileSize > 0`.
- **`maxFileSize` default is ~28.6 MB** (30,000,000 bytes) — Override if your server has a different limit.
- **`modifiedFilesData` must be set** — In the `selected` event, setting `args.modifiedFilesData` replaces the file queue; not setting it leaves all files in.
- **`getFilesData()` returns current queue** — Use it to count existing files before adding new ones.
