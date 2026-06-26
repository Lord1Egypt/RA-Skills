# File Sources

The Uploader supports multiple ways to select files: browse button, drag-and-drop, directory upload, paste from clipboard, and external button trigger.

---

## Drag and Drop

Drag-and-drop is enabled by default. The component itself acts as the drop target. The drop area highlights when files are dragged over it (via `.e-upload-drag-hover`).

No configuration is needed for default drag-and-drop behavior.

---

## Custom Drop Area

Point drag-and-drop to an external element using the `dropArea` property. Set it in the `created` event after the component mounts:

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);
  const dropRef = useRef<HTMLDivElement>(null);

  const asyncSettings = {
    saveUrl: 'https://your-server/api/FileUploader/Save',
    removeUrl: 'https://your-server/api/FileUploader/Remove',
  };

  function onCreated() {
    if (uploaderRef.current && dropRef.current) {
      uploaderRef.current.dropArea = dropRef.current;
      uploaderRef.current.dataBind();
    }
  }

  return (
    <div>
      <div
        ref={dropRef}
        style={{ border: '2px dashed #999', padding: '40px', textAlign: 'center' }}
      >
        Drop files here or{' '}
        <a href="#" onClick={e => { e.preventDefault(); document.querySelector<HTMLButtonElement>('.e-file-select-wrap button')?.click(); }}>
          Browse
        </a>
      </div>
      <UploaderComponent
        ref={uploaderRef}
        asyncSettings={asyncSettings}
        autoUpload={false}
        created={onCreated}
      />
    </div>
  );
}
```

**Hover style for custom drop area:**
```css
#dropArea.e-upload-drag-hover {
  background-color: #e0f0ff;
  border-color: #0078d4;
}
```

---

## Hiding the Default Drop Area

To suppress the built-in drop zone UI (e.g., when using a fully custom layout), hide it with CSS:

```css
.e-upload .e-file-drop {
  display: none;
}
```

Or use the `cssClass` prop to scope the style to a specific instance:

```tsx
<UploaderComponent cssClass="no-drop" asyncSettings={asyncSettings} />
```
```css
.no-drop .e-file-drop { display: none; }
```

---

## Directory Upload

Upload entire folders — all files and subdirectories — with `directoryUpload={true}`. The browser shows a folder picker instead of a file picker.

```tsx
<UploaderComponent asyncSettings={asyncSettings} directoryUpload={true} />
```

> Directory upload requires a browser that supports the HTML5 directory capability. Edge supports it via drag-and-drop. The server receives each file with its relative path in the filename (slash-separated), enabling folder reconstruction.

**Server-side: reconstruct folder structure**
```csharp
public void Save()
{
    var file = HttpContext.Current.Request.Files["UploadFiles"];
    string[] folders = file.FileName.Split('/');
    var savePath = HttpContext.Current.Server.MapPath("UploadedFiles");

    if (folders.Length > 1)
    {
        foreach (var folder in folders[..^1])
        {
            savePath = Path.Combine(savePath, folder);
            Directory.CreateDirectory(savePath);
        }
    }
    file.SaveAs(Path.Combine(savePath, folders[^1]));
}
```

---

## Paste-to-Upload (Clipboard Images)

Users can paste images from the clipboard (e.g., screenshots) directly into the uploader. The pasted image is received as `image.png` by default.

Rename the file server-side using `customFormData` to pass a unique filename:

```tsx
import { getUniqueID } from '@syncfusion/ej2-base';
import { UploaderComponent, UploadingEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://your-server/api/FileUploader/Save',
    removeUrl: 'https://your-server/api/FileUploader/Remove',
  };

  function onUploading(args: UploadingEventArgs) {
    if (args.fileData.fileSource === 'paste') {
      const baseName = args.fileData.name.replace(/\.[^.]+$/, '');
      const uniqueName = getUniqueID(baseName) + '.png';
      args.customFormData = [{ fileName: uniqueName }];
    }
  }

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      autoUpload={false}
      uploading={onUploading}
    />
  );
}
```

> Check `args.fileData.fileSource === 'paste'` in the `uploading` event to detect paste-sourced files.

---

## Trigger Browse from External Button

Programmatically open the file browser from any button outside the uploader:

```tsx
import { select } from '@syncfusion/ej2-base';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  function openBrowse(e: React.MouseEvent) {
    e.preventDefault();
    const browseBtn = select('.e-file-select-wrap button', document) as HTMLButtonElement;
    browseBtn?.click();
  }

  return (
    <div>
      <button onClick={openBrowse}>📎 Attach Files</button>
      <UploaderComponent asyncSettings={asyncSettings} />
    </div>
  );
}
```

If multiple uploaders exist on the page, scope the selector to a specific container element.

---

## Sort Selected Files

Reorder files before upload using the `selected` event. Sort by name, size, or any custom criteria:

```tsx
import { SelectedEventArgs, UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  function onSelected(args: SelectedEventArgs) {
    // Sort alphabetically by filename
    args.filesData.sort((a, b) => a.name.localeCompare(b.name));
    args.modifiedFilesData = args.filesData;
    args.isModified = true;
  }

  return (
    <UploaderComponent asyncSettings={asyncSettings} selected={onSelected} />
  );
}
```

---

## Get Total Size of Selected Files

Sum the sizes of all currently queued files:

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);

  function showTotalSize() {
    const files = uploaderRef.current?.getFilesData() ?? [];
    const totalBytes = files.reduce((sum, f) => sum + f.size, 0);
    const totalMB = (totalBytes / (1024 * 1024)).toFixed(2);
    alert(`Total: ${totalMB} MB across ${files.length} file(s)`);
  }

  return (
    <>
      <UploaderComponent ref={uploaderRef} asyncSettings={asyncSettings} autoUpload={false} />
      <button onClick={showTotalSize}>Show Total Size</button>
    </>
  );
}
```

---

## See Also

- [Validation](./validation.md) — filter files by type/size/MIME on selection or drop
- [Getting started](./getting-started.md) — basic drop area setup
- [Template customization](./template-customization.md) — invisible uploader pattern
