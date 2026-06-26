# Advanced How-To Scenarios – Syncfusion React Uploader

## Table of Contents
- [Programmatic File Upload](#programmatic-file-upload)
- [Invisible / Background Upload](#invisible--background-upload)
- [Image Preview Before Uploading](#image-preview-before-uploading)
- [Resize Images Before Upload](#resize-images-before-upload)
- [Sort Selected Files](#sort-selected-files)
- [Check File Size Before Upload](#check-file-size-before-upload)
- [Check MIME Type Before Upload](#check-mime-type-before-upload)
- [Confirm Dialog Before File Removal](#confirm-dialog-before-file-removal)
- [Open and Edit Uploaded Files](#open-and-edit-uploaded-files)
- [Trigger File Browser from External Button](#trigger-file-browser-from-external-button)
- [Convert Uploaded Image to Binary (Server-Side)](#convert-uploaded-image-to-binary-server-side)
- [JWT Authentication](#jwt-authentication)
- [Form Support](#form-support)
- [Localization](#localization)
- [Accessibility](#accessibility)

---

## Programmatic File Upload

Upload files without user interaction using the `upload` method. Retrieve queued files with `getFilesData()`.

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const uploadAll = (): void => {
    // Upload all queued files
    uploaderRef.current?.upload(uploaderRef.current.getFilesData());
  };

  const uploadSpecific = (): void => {
    const files = uploaderRef.current?.getFilesData();
    if (files && files.length > 0) {
      // Upload only the first file
      uploaderRef.current?.upload([files[0]]);
    }
  };

  return (
    <div>
      <UploaderComponent
        ref={uploaderRef}
        asyncSettings={asyncSettings}
        autoUpload={false}
      />
      <button onClick={uploadAll}>Upload All</button>
      <button onClick={uploadSpecific}>Upload First File</button>
    </div>
  );
}
```

- `upload()` with no argument uploads all queued files.
- `upload(filesData)` uploads only the specified files.
- `getFilesData(index?)` returns current file list; optional `index` returns a specific item.

---

## Invisible / Background Upload

Trigger an invisible upload (no visible file list) by setting `showFileList={false}` and calling `upload()` in the `selected` event.

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
    // Upload immediately without showing any UI
    uploaderRef.current?.upload(args.filesData, true);
    args.cancel = true; // Prevent default file list rendering
  };

  const onSuccess = (args: any): void => {
    if (args.operation === 'upload') {
      alert(`${args.file.name} uploaded successfully!`);
    }
  };

  return (
    <UploaderComponent
      ref={uploaderRef}
      asyncSettings={asyncSettings}
      showFileList={false}
      selected={onSelected}
      success={onSuccess}
    />
  );
}
```

---

## Image Preview Before Uploading

Display image previews using the `selected` event by reading files with `FileReader`.

```tsx
import React, { useRef, useState } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const [previews, setPreviews] = useState<string[]>([]);
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSelected = (args: any): void => {
    args.filesData.forEach((fileData: any) => {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        setPreviews(prev => [...prev, e.target.result]);
      };
      reader.readAsDataURL(fileData.rawFile);
    });
  };

  return (
    <div>
      <UploaderComponent
        asyncSettings={asyncSettings}
        allowedExtensions=".jpg,.jpeg,.png,.gif"
        selected={onSelected}
      />
      <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
        {previews.map((src, i) => (
          <img key={i} src={src} style={{ width: 100, height: 100, objectFit: 'cover' }} alt="preview" />
        ))}
      </div>
    </div>
  );
}
```

> For a more complete implementation, see the [Syncfusion Image Preview Demo](https://ej2.syncfusion.com/react/demos/#/material/uploader/image-preview).

---

## Resize Images Before Upload

Resize images client-side before uploading to reduce server storage and upload time.

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

const MAX_WIDTH = 1000;
const MAX_HEIGHT = 600;

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSelected = (args: any): void => {
    args.cancel = true; // Prevent default upload
    const fileData = args.filesData[0];
    const reader = new FileReader();

    reader.onload = (e: any) => {
      const img = new Image();
      img.onload = () => {
        let { width, height } = img;

        if (width > MAX_WIDTH) { height *= MAX_WIDTH / width; width = MAX_WIDTH; }
        if (height > MAX_HEIGHT) { width *= MAX_HEIGHT / height; height = MAX_HEIGHT; }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d')!.drawImage(img, 0, 0, width, height);

        canvas.toBlob((blob) => {
          if (!blob) return;
          const resizedFile = {
            name: fileData.name,
            rawFile: blob,
            size: blob.size,
            type: fileData.type,
            validationMessage: '',
            statusCode: '1',
            status: 'Ready to Upload'
          };
          // Upload the resized image with custom UI flag
          uploaderRef.current?.upload(resizedFile as any, true);
        }, 'image/png');
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(fileData.rawFile);
  };

  return (
    <UploaderComponent
      ref={uploaderRef}
      asyncSettings={asyncSettings}
      allowedExtensions=".jpg,.jpeg,.png"
      selected={onSelected}
    />
  );
}
```

---

## Sort Selected Files

Sort files in the upload queue using the `selected` event and the built-in `sortFileList` method, or custom sort logic.

```tsx
const onSelected = (args: any): void => {
  // Sort alphabetically by file name
  args.modifiedFilesData = args.filesData.sort((a: any, b: any) =>
    a.name.localeCompare(b.name)
  );
};

<UploaderComponent asyncSettings={asyncSettings} selected={onSelected} />
```

**Using `sortFileList` method:**

```tsx
const onSelected = (args: any): void => {
  // Sort using the built-in method (alphabetically by name)
  const sorted = uploaderRef.current?.sortFileList(args.filesData as any);
  args.modifiedFilesData = sorted as any;
};
```

---

## Check File Size Before Upload

Inspect file size in the `uploading` event before the upload starts. Use `bytesToSize` for human-readable display.

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onUploading = (args: any): void => {
    const sizeStr = uploaderRef.current?.bytesToSize(args.fileData.size);
    console.log(`Uploading: ${args.fileData.name} — Size: ${sizeStr}`);

    // Block files larger than 2 MB
    if (args.fileData.size > 2 * 1024 * 1024) {
      args.cancel = true;
      alert(`File "${args.fileData.name}" (${sizeStr}) exceeds the 2 MB limit.`);
    }
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

## Check MIME Type Before Upload

Retrieve the MIME type from `args.fileData.rawFile.type` in the `uploading` event.

```tsx
const onUploading = (args: any): void => {
  const mimeType = args.fileData.rawFile.type;
  console.log('MIME type:', mimeType);

  // Only allow PDF files
  if (mimeType !== 'application/pdf') {
    args.cancel = true;
    alert(`Invalid file type: ${mimeType}. Only PDFs are allowed.`);
  }
};

<UploaderComponent asyncSettings={asyncSettings} uploading={onUploading} />
```

---

## Confirm Dialog Before File Removal

Show a confirmation dialog before removing a file from the server. Use `beforeRemove` to intercept removal.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onBeforeRemove = (args: any): void => {
    // Cancel the default removal
    args.cancel = true;

    // Show confirmation dialog
    const confirmed = window.confirm(`Remove "${args.filesData[0].name}" from the server?`);
    if (confirmed) {
      // Proceed with removal programmatically
      args.cancel = false;
    }
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      beforeRemove={onBeforeRemove}
    />
  );
}
```

> For a richer dialog, integrate the Syncfusion Dialog component (`@syncfusion/ej2-react-popups`) instead of `window.confirm`.

---

## Open and Edit Uploaded Files

After a successful upload, retrieve the server file path and attach a click handler to open/edit the file.

```tsx
const onSuccess = (args: any): void => {
  if (args.operation !== 'upload') return;

  // Server returns file path in response status text
  const filePath = args.e.target.statusText;

  // Find the rendered list item for this file
  const liElements = document.querySelectorAll('.e-upload-file-list');
  liElements.forEach((li: Element) => {
    if (li.getAttribute('data-file-name') === args.file.name) {
      li.setAttribute('file-path', filePath);
      li.addEventListener('click', () => {
        const savedPath = li.getAttribute('file-path');
        if (savedPath) {
          const xhr = new XMLHttpRequest();
          xhr.open('POST', '/api/upload/openFile');
          xhr.setRequestHeader('filePath', savedPath);
          xhr.send();
        }
      });
    }
  });
};
```

---

## Trigger File Browser from External Button

Open the file browser from any external button by clicking the hidden file input via the Uploader's browse button.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const triggerBrowse = (): void => {
    const browseBtn = document.querySelector('.e-file-select-wrap button') as HTMLElement;
    browseBtn?.click();
  };

  return (
    <div>
      <button onClick={triggerBrowse}>📎 Attach Files</button>
      <UploaderComponent asyncSettings={asyncSettings} />
    </div>
  );
}
```

---

## Convert Uploaded Image to Binary (Server-Side)

Read the uploaded file as binary bytes on the server using `BinaryReader`. Client-side upload is standard.

```csharp
[AcceptVerbs("Post")]
public void Save()
{
    try
    {
        if (System.Web.HttpContext.Current.Request.Files.AllKeys.Length > 0)
        {
            var httpPostedFile = System.Web.HttpContext.Current.Request.Files["UploadFiles"];
            if (httpPostedFile != null)
            {
                byte[] fileBytes;
                using (BinaryReader br = new BinaryReader(httpPostedFile.InputStream))
                {
                    fileBytes = br.ReadBytes((int)httpPostedFile.InputStream.Length);
                    // fileBytes now contains binary data — store in DB or process
                }
                HttpContext.Current.Response.StatusCode = 200;
            }
        }
    }
    catch (Exception e)
    {
        HttpContext.Current.Response.StatusCode = 204;
        HttpContext.Current.Response.StatusDescription = e.Message;
    }
}
```

---

## JWT Authentication

Secure upload and remove requests by adding JWT tokens to request headers in the `uploading` and `removing` events.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const token = 'your.jwt.token'; // Replace with real token from your auth system

  const asyncSettings = {
    saveUrl: 'https://your-api.com/api/upload/save',
    removeUrl: 'https://your-api.com/api/upload/remove'
  };

  const onUploading = (args: any): void => {
    args.currentRequest.setRequestHeader('Authorization', `Bearer ${token}`);
  };

  const onRemoving = (args: any): void => {
    args.postRawFile = false; // Send file name only
    args.currentRequest.setRequestHeader('Authorization', `Bearer ${token}`);
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      uploading={onUploading}
      removing={onRemoving}
    />
  );
}
```

**Server-side JWT validation (ASP.NET Core):**

```csharp
private bool IsAuthorized()
{
    var authHeader = Request.Headers["Authorization"].ToString();
    if (string.IsNullOrEmpty(authHeader) || !authHeader.StartsWith("Bearer "))
        return false;

    var token = authHeader["Bearer ".Length..];
    return ValidateToken(token); // Implement your token validation logic
}

public async Task<IActionResult> Save(IFormFile UploadFiles)
{
    if (!IsAuthorized()) return Unauthorized();
    // Process file...
    return Ok();
}
```

---

## Form Support

### HTML Form Integration

Integrate the Uploader as a standard file input within an HTML form.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  return (
    <form action="/api/submit" method="post" encType="multipart/form-data">
      <UploaderComponent
        asyncSettings={{ saveUrl: '', removeUrl: '' }}
        autoUpload={false}
        htmlAttributes={{ name: 'uploadedFiles' }}
      />
      <input type="text" name="userName" placeholder="Your name" />
      <button type="submit">Submit Form</button>
    </form>
  );
}
```

> For HTML form integration: set `saveUrl` and `removeUrl` to empty strings, disable `autoUpload`, and add a `name` attribute via `htmlAttributes`.

### React Hook Form Integration

```tsx
import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const { control, handleSubmit } = useForm();

  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSubmit = (data: any) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="files"
        control={control}
        render={({ field }) => (
          <UploaderComponent
            asyncSettings={asyncSettings}
            change={(args: any) => field.onChange(args.files)}
          />
        )}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## Localization

Customize all static text in the Uploader using the `L10n` library.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';

// Load custom locale before rendering
L10n.load({
  'fr-FR': {
    uploader: {
      Browse: 'Parcourir',
      Clear: 'Effacer',
      Upload: 'Télécharger',
      dropFilesHint: 'ou déposez des fichiers ici',
      uploadFailedMessage: 'Échec du téléchargement',
      uploadSuccessMessage: 'Téléchargement réussi',
      removedSuccessMessage: 'Fichier supprimé avec succès',
      removedFailedMessage: 'Impossible de supprimer le fichier',
      inProgress: 'En cours de téléchargement',
      readyToUploadMessage: 'Prêt à télécharger',
      pauseUpload: 'Téléchargement suspendu',
      fileUploadCancel: 'Téléchargement annulé',
      invalidMaxFileSize: 'La taille du fichier est trop grande',
      invalidFileType: 'Type de fichier non autorisé',
      invalidMinFileSize: 'La taille du fichier est trop petite',
      remove: 'Supprimer',
      cancel: 'Annuler',
      delete: 'Supprimer le fichier',
      totalFiles: 'Total des fichiers',
      size: 'Taille'
    }
  }
});

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      locale="fr-FR"
    />
  );
}
```

**All localizable keys:**

| Key | Description |
|---|---|
| `Browse` | Browse button text |
| `Clear` | Clear button text |
| `Upload` | Upload button text |
| `dropFilesHint` | Drop area hint text |
| `uploadFailedMessage` | Status on upload failure |
| `uploadSuccessMessage` | Status on upload success |
| `removedSuccessMessage` | Status on successful removal |
| `removedFailedMessage` | Status on removal failure |
| `inProgress` | Status while uploading |
| `readyToUploadMessage` | Status when file is ready |
| `pauseUpload` | Status when upload is paused |
| `fileUploadCancel` | Status when upload is canceled |
| `invalidMaxFileSize` | Validation: file too large |
| `invalidFileType` | Validation: invalid file type |
| `invalidMinFileSize` | Validation: file too small |
| `remove` | Remove icon tooltip |
| `cancel` | Cancel icon tooltip |
| `delete` | Delete icon tooltip |
| `totalFiles` | Total files tooltip |
| `size` | Size tooltip |

---

## Accessibility

The Syncfusion React Uploader is fully accessible and complies with WCAG 2.2, Section 508, and ADA standards.

**Compliance:**
- WCAG 2.2 ✓
- Section 508 ✓
- Screen reader support ✓
- RTL support (via `enableRtl`) ✓
- Color contrast compliant ✓
- Mobile device support ✓
- Keyboard navigation ✓

**Keyboard shortcuts:**

| Key | Action |
|---|---|
| `Tab` | Move focus to the next element |
| `Shift + Tab` | Move focus to the previous element |
| `Enter` | Trigger the focused button action |
| `Esc` | Close the file browser dialog / cancel |

**RTL support:**

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  enableRtl={true}
/>
```

**Security — HTML sanitizer:**

The `enableHtmlSanitizer` property (default: `true`) strips cross-site scripting code from filenames. Disable only if you fully trust the source.

```tsx
// Default: XSS prevention enabled
<UploaderComponent asyncSettings={asyncSettings} enableHtmlSanitizer={true} />
```

---

## Get Total Size of Selected Files

Calculate cumulative size of all files in the `selected` event.

```tsx
const onSelected = (args: any): void => {
  const totalBytes = args.filesData.reduce((acc: number, f: any) => acc + f.size, 0);
  const totalSizeMB = (totalBytes / (1024 * 1024)).toFixed(2);
  console.log(`Total selected size: ${totalSizeMB} MB`);
};

<UploaderComponent asyncSettings={asyncSettings} selected={onSelected} />
```
