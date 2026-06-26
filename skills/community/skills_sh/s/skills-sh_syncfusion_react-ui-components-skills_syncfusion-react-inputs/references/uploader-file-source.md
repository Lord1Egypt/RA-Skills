# File Sources – Syncfusion React Uploader

## Table of Contents
- [Paste to Upload](#paste-to-upload)
- [Directory Upload](#directory-upload)
- [Drag and Drop](#drag-and-drop)
- [Custom Drop Area](#custom-drop-area)
- [Customize Drop Area Appearance](#customize-drop-area-appearance)
- [Drop Effect](#drop-effect)
- [Gotchas](#gotchas)

---

## Paste to Upload

The Uploader supports pasting images directly from the clipboard (Ctrl+V). The pasted image is saved on the server with the default filename `image.png`. Rename it server-side using a unique ID.

```tsx
import React from 'react';
import { UploaderComponent, getUniqueID } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  return (
    <div>
      <p>Press Ctrl+V to paste an image from clipboard</p>
      <UploaderComponent asyncSettings={asyncSettings} />
    </div>
  );
}
```

**Server-side: rename pasted file**

```csharp
public void Save() {
    var httpPostedFile = System.Web.HttpContext.Current.Request.Files["UploadFiles"];
    var fileSave = System.Web.HttpContext.Current.Server.MapPath("UploadedFiles");
    var fileSavePath = Path.Combine(fileSave, httpPostedFile.FileName);

    if (!System.IO.File.Exists(fileSavePath)) {
        httpPostedFile.SaveAs(fileSavePath);
        var newName = System.Web.HttpContext.Current.Request.Form["fileName"];
        var newPath = Path.Combine(fileSave, newName);
        System.IO.File.Move(fileSavePath, newPath);
    }
}
```

> Use the `getUniqueID` utility from `@syncfusion/ej2-base` to generate unique filenames and avoid collisions.

---

## Directory Upload

Enable `directoryUpload` to allow users to select an entire folder. All files and subdirectory files in the selected folder are uploaded.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      directoryUpload={true}
    />
  );
}
```

> - Directory upload is supported only in browsers with HTML5 directory selection support.
> - In Microsoft Edge, use **drag-and-drop** to upload directories (the browse button may not work).
> - When `directoryUpload` is enabled, only folder selection is permitted — individual files cannot be browsed or dropped.

**Server-side: preserve folder structure**

```csharp
public void Save() {
    var httpPostedFile = HttpContext.Current.Request.Files["UploadFiles"];
    var fileSave = HttpContext.Current.Server.MapPath("UploadedFiles");
    // File name contains the relative path: "folder/subfolder/file.txt"
    string[] folders = httpPostedFile.FileName.Split('/');
    string fileSavePath;

    if (folders.Length > 1)
    {
        for (var i = 0; i < folders.Length - 1; i++)
        {
            var newFolder = Path.Combine(fileSave, folders[i]);
            Directory.CreateDirectory(newFolder);
            fileSave = newFolder;
        }
        fileSavePath = Path.Combine(fileSave, folders[folders.Length - 1]);
    }
    else
    {
        fileSavePath = Path.Combine(fileSave, httpPostedFile.FileName);
    }

    if (!System.IO.File.Exists(fileSavePath))
        httpPostedFile.SaveAs(fileSavePath);
}
```

---

## Drag and Drop

By default, the Uploader component itself acts as the drop target. Users can drag files from the file system and drop them onto the uploader area, which highlights on hover.

```tsx
// Default drag-and-drop (no extra config needed)
<UploaderComponent asyncSettings={asyncSettings} />
```

The drop area highlights with the `e-upload-drag-hover` CSS class when files are dragged over it.

---

## Custom Drop Area

Configure any external HTML element as the drop target using the `dropArea` property.

```tsx
import React, { useRef, useEffect, useState } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const dropAreaRef = useRef<HTMLDivElement>(null);
  const [dropAreaEl, setDropAreaEl] = useState<HTMLElement | null>(null);

  // Set after DOM mounts
  useEffect(() => {
    setDropAreaEl(dropAreaRef.current);
  }, []);

  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  return (
    <div>
      <div
        ref={dropAreaRef}
        id="customDropArea"
        style={{
          border: '2px dashed #999',
          padding: '60px',
          textAlign: 'center',
          background: '#f9f9f9'
        }}
      >
        Drop files here or use the Browse button
      </div>
      <UploaderComponent
        asyncSettings={asyncSettings}
        dropArea={dropAreaEl}
      />
    </div>
  );
}
```

> `dropArea` accepts an `HTMLElement` reference or a CSS selector ID string (e.g., `'#customDropArea'`).

**Using a string selector:**
```tsx
<UploaderComponent asyncSettings={asyncSettings} dropArea="#customDropArea" />
```

---

## Customize Drop Area Appearance

Override the `.e-upload-drag-hover` CSS class to change the drop area style when files are dragged over it.

```css
/* Custom drag-hover style */
.e-upload-drag-hover {
  border: 2px solid #007bff !important;
  background-color: #e8f0fe !important;
}
```

**Hide the default drop area** by overriding these CSS classes:

```css
/* Hide the built-in Uploader container and file-select/drop area */
.e-upload.e-control-wrapper {
  border: none !important;
}

.e-upload .e-file-select {
  display: none;
}

.e-upload .e-file-drop {
  display: none;
}
```

---

## Drop Effect

Control the drag-and-drop cursor effect using the `dropEffect` property.

| Value | Description |
|---|---|
| `'Default'` | Uses the browser default drag effect |
| `'Copy'` | Shows a copy cursor |
| `'Move'` | Shows a move cursor |
| `'Link'` | Shows a link cursor |
| `'None'` | Disables the drop effect visual |

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  dropEffect="Copy"
/>
```

---

## Gotchas

- **`directoryUpload` restricts to folders only** — Individual file browsing/dropping is disabled when enabled.
- **Directory upload + Edge** — Use drag-and-drop in Edge; the browse button may not support folder selection.
- **`dropArea` ref timing** — Pass the element after it mounts. Use `useEffect` + `useState` to avoid passing `null`.
- **Paste upload filename** — Pasted images default to `image.png`; implement server-side renaming to avoid collisions.
- **Drag-and-drop bypasses extension validation** — Add manual validation in the `selected` event for dropped files.
