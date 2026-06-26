# Integration and Security

This reference covers HTML form integration, JWT-secured uploads, localization of text content, and EJ1-to-EJ2 migration notes.

---

## HTML Form Integration

The Uploader works inside HTML forms like a standard `<input type="file">`. When integrated with a form:

- Set `saveUrl` and `removeUrl` to `null` (or omit `asyncSettings`)
- Set `autoUpload={false}`
- Add a `name` attribute to the input element

When the form submits, selected files are sent as a collection to the form action.

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    form.submit(); // Selected files are included in the form POST
  }

  return (
    <form id="uploadForm" method="post" action="/submit" onSubmit={onSubmit}>
      <UploaderComponent
        id="fileUpload"
        name="uploadedFiles"
        autoUpload={false}
        allowedExtensions="image/*"
      />
      <button type="submit">Submit Form</button>
    </form>
  );
}
```

> Resetting the form (`form.reset()`) also clears the uploader's file list and all associated data.

---

## Form Integration with Syncfusion FormValidator

Use Syncfusion's `FormValidator` to validate form fields including the file upload field:

```tsx
import { select } from '@syncfusion/ej2-base';
import { FormValidator, FormValidatorModel } from '@syncfusion/ej2-inputs';
import { SelectedEventArgs, UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { useEffect, useRef } from 'react';

function PhotoUploadForm() {
  const formRef = useRef<HTMLFormElement>(null);
  let formValidator: FormValidator;

  useEffect(() => {
    const options: FormValidatorModel = {
      rules: {
        name: { required: [true, '* Name is required'] },
        email: { required: [true, '* Email is required'] },
        upload: { required: [true, '* Please select a file'] },
      },
    };
    formValidator = new FormValidator('#photoForm', options);
  }, []);

  function onFileSelected(args: SelectedEventArgs) {
    // Mirror the selected filename into the hidden text input for validation
    const input = document.getElementById('upload') as HTMLInputElement;
    if (input) input.value = args.filesData[0]?.name ?? '';
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (formValidator?.validate()) {
      formValidator.element.reset();
      alert('Form submitted successfully!');
    }
  }

  function openBrowse(e: React.MouseEvent) {
    e.preventDefault();
    (select('.e-file-select-wrap button', document) as HTMLButtonElement)?.click();
  }

  return (
    <form id="photoForm" method="post" onSubmit={onSubmit}>
      <div>
        <label>Name</label>
        <input type="text" name="name" id="name" />
      </div>

      <div>
        <label>Email</label>
        <input type="email" name="email" id="Email" />
      </div>

      <div>
        {/* Visible text input shows selected filename — used for FormValidator */}
        <input type="text" readOnly id="upload" name="upload" />
        <button type="button" onClick={openBrowse}>Browse...</button>

        {/* Hidden uploader — no async, form mode */}
        <UploaderComponent
          id="fileUpload"
          autoUpload={false}
          allowedExtensions="image/*"
          selected={onFileSelected}
        />
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

**Key pattern:** A visible readonly `<input>` captures the selected filename for `FormValidator`. The actual `UploaderComponent` handles file selection. When the user picks a file, `onFileSelected` populates the text input, which then satisfies the `required` rule.

---

## JWT Authentication

Inject a JWT token into upload and remove requests using the `uploading` and `removing` events. The `currentRequest` property exposes the underlying `XMLHttpRequest`.

**Client-side:**
```tsx
import { UploaderComponent, UploadingEventArgs, RemovingEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  const token = 'your.jwt.token'; // In production: fetch from auth service

  const asyncSettings = {
    saveUrl: 'https://your-server/api/FileUploader/Save',
    removeUrl: 'https://your-server/api/FileUploader/Remove',
  };

  function onUploading(args: UploadingEventArgs) {
    (args.currentRequest as XMLHttpRequest)
      .setRequestHeader('Authorization', `Bearer ${token}`);
  }

  function onRemoving(args: RemovingEventArgs) {
    args.postRawFile = false; // Send filename only
    (args.currentRequest as XMLHttpRequest)
      .setRequestHeader('Authorization', `Bearer ${token}`);
  }

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      uploading={onUploading}
      removing={onRemoving}
    />
  );
}
```

> Replace the hardcoded token with a dynamic token from your auth context or a token refresh mechanism in production.

**Server-side validation (ASP.NET Core):**
```csharp
public async Task<IActionResult> Save(IFormFile UploadFiles)
{
    if (!IsAuthorized()) return Unauthorized();

    Directory.CreateDirectory(_uploads);
    var filePath = Path.Combine(_uploads, UploadFiles.FileName);
    var isChunk = UploadFiles.ContentType == "application/octet-stream";
    using var stream = new FileStream(filePath, isChunk ? FileMode.Append : FileMode.Create);
    await UploadFiles.CopyToAsync(stream);
    return Ok();
}

private bool IsAuthorized()
{
    var header = Request.Headers["Authorization"].ToString();
    if (!header.StartsWith("Bearer ")) return false;
    var token = header["Bearer ".Length..];
    return ValidateToken(token); // Replace with real JWT validation
}

public IActionResult Remove(string UploadFiles)
{
    if (!IsAuthorized()) return Unauthorized();
    var path = Path.Combine(_uploads, UploadFiles);
    if (System.IO.File.Exists(path)) System.IO.File.Delete(path);
    return Ok();
}
```

---

## Localization

Customize all static text in the Uploader — button labels, status messages, tooltips, and drop area text — using Syncfusion's `L10n` (localization) service.

**Available text keys:**

| Key | Default (en-US) | Description |
|-----|-----------------|-------------|
| `Browse` | Browse | Browse button label |
| `Clear` | Clear | Clear button label |
| `Upload` | Upload | Upload button label |
| `dropFilesHint` | or Drop files here | Drop area text |
| `uploadSuccessMessage` | File uploaded successfully | Success status |
| `uploadFailedMessage` | File failed to upload | Failure status |
| `removedSuccessMessage` | File removed successfully | Remove success |
| `removedFailedMessage` | File failed to remove | Remove failure |
| `inProgress` | Uploading | In-progress status |
| `readyToUploadMessage` | Ready to upload | File selected state |
| `invalidMaxFileSize` | File size is too large | Size validation error |
| `invalidMinFileSize` | File size is too small | Min size error |
| `invalidFileType` | File type is not allowed | Extension error |
| `remove` | Remove | Remove icon tooltip |
| `cancel` | Cancel | Cancel icon tooltip |
| `delete` | Delete file | Delete icon tooltip |
| `pauseUpload` | File upload paused | Chunk pause status |
| `fileUploadCancel` | File upload cancelled | Cancel status |

**Example — French (fr-CH) localization:**

```tsx
import { L10n } from '@syncfusion/ej2-base';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { useEffect } from 'react';

function App() {
  const asyncSettings = {
    saveUrl: 'https://your-server/api/FileUploader/Save',
    removeUrl: 'https://your-server/api/FileUploader/Remove',
  };

  useEffect(() => {
    L10n.load({
      'fr-CH': {
        uploader: {
          Browse: 'Feuilleter',
          Clear: 'Clair',
          Upload: 'Télécharger',
          cancel: 'Annuler',
          delete: 'Supprimer le fichier',
          totalFiles: 'Total des fichiers',
          size: 'taille',
          dropFilesHint: 'ou Déposer des fichiers ici',
          inProgress: 'Téléchargement',
          invalidFileType: 'Le type de fichier n\'est pas autorisé',
          invalidMaxFileSize: 'La taille du fichier dépasse 28 Mo',
          readyToUploadMessage: 'Prêt à télécharger',
          remove: 'Retirer',
          removedSuccessMessage: 'Fichier supprimé avec succès',
          uploadFailedMessage: 'Impossible d\'importer le fichier',
          uploadSuccessMessage: 'Fichier téléchargé avec succès',
        },
      },
    });
  }, []);

  return <UploaderComponent asyncSettings={asyncSettings} locale="fr-CH" />;
}
```

> Load locale strings before the component renders (in `useEffect` with `[]` or outside the component). The `locale` prop on `UploaderComponent` activates the loaded locale.

**Combining localization with RTL:**
```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  locale="ar"
  enableRtl={true}
/>
```

---

## EJ1 to EJ2 Migration

Key differences between EJ1 (`ej.Uploader`) and EJ2 (`UploaderComponent`):

| Feature | EJ1 | EJ2 |
|---------|-----|-----|
| Package | `@syncfusion/ej2` (monolith) | `@syncfusion/ej2-react-inputs` |
| Component | `ej.Uploader` | `UploaderComponent` |
| Async config | `saveUrl`, `removeUrl` as direct props | `asyncSettings={{ saveUrl, removeUrl }}` |
| Auto upload | `autoUpload` prop | `autoUpload` prop (same) |
| Events | jQuery-style callbacks | React event props (`success`, `failure`, etc.) |
| File list access | `getFilesData()` | `getFilesData()` (same) |
| Template | String-based HTML template | JSX function or HTML string |

---

## See Also

- [Async upload](./async-upload.md) — `uploading` event and custom headers
- [Events](./events.md) — full event reference for `removing`, `uploading`
- [Style & accessibility](./style-accessibility.md) — RTL support, theme imports
