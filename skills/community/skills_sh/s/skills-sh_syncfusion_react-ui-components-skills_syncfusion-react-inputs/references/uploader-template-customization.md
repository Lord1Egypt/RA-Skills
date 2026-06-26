# Template and Customization – Syncfusion React Uploader

## Table of Contents
- [File List Template](#file-list-template)
- [Custom Upload UI (showFileList)](#custom-upload-ui-showfilelist)
- [Custom Buttons](#custom-buttons)
- [CSS Class](#css-class)
- [Style and Appearance](#style-and-appearance)
- [Customize Progress Bar](#customize-progress-bar)
- [Hide Default Drop Area](#hide-default-drop-area)
- [fileListRendering Event](#filelistrendering-event)
- [Gotchas](#gotchas)

---

## File List Template

Use the `template` property to customize how each file is rendered in the file list. Provide an HTML string or a function returning HTML.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  // Template as a function returning JSX
  const fileListTemplate = () => {
    return (
      <div className="custom-file-item">
        <span className="file-icon e-icons e-file-document"></span>
        <div className="file-info">
          <span className="file-name">${name}</span>
          <span className="file-size">${size} bytes</span>
        </div>
      </div>
    );
  }

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      template={fileListTemplate}
    />
  );
}
```

> When a `template` is used, remove and progress bar actions are handled through `removing` and `progress` events — the default icons are replaced by your template.

---

## Custom Upload UI (showFileList)

Build a fully custom file list UI by hiding the default list with `showFileList={false}` and rendering your own.

When using `showFileList={false}`, pass `true` as the second argument to `upload()` and `remove()` to indicate a custom UI:

```tsx
// upload(filesData, customUI=true)
uploaderRef.current?.upload(filesData, true);

// remove(filesData, customUI=true)
uploaderRef.current?.remove(filesData, true);
```

**Full example — custom file list with progress tracking:**

```tsx
import React, { useRef, useState } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);
  const [fileList, setFileList] = useState<any[]>([]);

  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSelected = (args: any): void => {
    setFileList(prev => [...prev, ...args.filesData]);
  };

  const onProgress = (args: any): void => {
    const progress = Math.round((args.e.loaded / args.e.total) * 100);
    setFileList(prev =>
      prev.map(f => f.name === args.file.name ? { ...f, progress } : f)
    );
  };

  const onSuccess = (args: any): void => {
    if (args.operation === 'upload') {
      setFileList(prev =>
        prev.map(f => f.name === args.file.name ? { ...f, status: 'done' } : f)
      );
    }
  };

  const handleUpload = (file: any): void => {
    uploaderRef.current?.upload([file], true);
  };

  const handleRemove = (file: any): void => {
    uploaderRef.current?.remove([file], true);
    setFileList(prev => prev.filter(f => f.name !== file.name));
  };

  return (
    <div>
      <UploaderComponent
        ref={uploaderRef}
        asyncSettings={asyncSettings}
        showFileList={false}
        autoUpload={false}
        selected={onSelected}
        progress={onProgress}
        success={onSuccess}
      />
      <ul>
        {fileList.map(file => (
          <li key={file.name}>
            <span>{file.name}</span>
            {file.progress !== undefined && <span> — {file.progress}%</span>}
            {file.status === 'done' && <span> ✓ Uploaded</span>}
            <button onClick={() => handleUpload(file)}>Upload</button>
            <button onClick={() => handleRemove(file)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Custom Buttons

Customize the Browse, Clear, and Upload button labels using the `buttons` property. Accepts plain text strings or HTML element strings.

```tsx
// Text labels
<UploaderComponent
  asyncSettings={asyncSettings}
  autoUpload={false}
  buttons={{
    browse: 'Choose File',
    clear: 'Clear All',
    upload: 'Upload All'
  }}
/>
```

**HTML element buttons:**

```tsx
const customButtons = {
  browse: '<span class="e-icons e-browse"> Browse Files</span>',
  clear: '<span class="e-icons e-clear"> Clear</span>',
  upload: '<span class="e-icons e-upload"> Upload</span>'
};

<UploaderComponent
  asyncSettings={asyncSettings}
  autoUpload={false}
  buttons={customButtons}
/>
```

> The `buttons` property takes precedence over locale strings. If both are configured, `buttons` wins.

---

## CSS Class

Add custom CSS classes to the Uploader root element using `cssClass`.

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  cssClass="my-custom-uploader dark-theme"
/>
```

```css
.my-custom-uploader {
  border: 2px solid #007bff;
  border-radius: 8px;
}
```

---

## Style and Appearance

Override Syncfusion CSS classes to customize the uploader's visual appearance.

### Uploader Wrapper Dimensions

```css
.e-upload.e-control-wrapper,
.e-bigger.e-small .e-upload.e-control-wrapper {
  height: 300px;
  width: 400px;
}
```

### Browse Button Style

```css
.e-upload .e-file-select-wrap .e-btn,
.e-upload .e-upload-actions .e-btn,
.e-bigger.e-small .e-upload .e-file-select-wrap .e-btn,
.e-bigger.e-small .e-upload .e-upload-actions .e-btn {
  font-family: cursive;
  height: 40px;
  background-color: #4CAF50;
  color: white;
}
```

### Drop Area Text Style

```css
.e-upload .e-file-select-wrap .e-file-drop,
.e-bigger.e-small .e-upload .e-file-select-wrap .e-file-drop {
  font-size: 18px;
  color: #555;
}
```

### File List Container Style

```css
.e-upload .e-upload-files .e-upload-file-list {
  background-color: #f0f4f8;
}
```

---

## Customize Progress Bar

Override the progress bar's color and height by targeting the Syncfusion progress bar classes.

```css
/* Progress bar track (background) */
.e-upload .e-upload-files .e-file-progress-wrap {
  background-color: #e0e0e0;
  border-radius: 4px;
  height: 6px;
}

/* Progress bar fill */
.e-upload .e-upload-files .e-file-progress-wrap .e-upload-progress-line {
  background-color: #007bff;
  height: 6px;
}
```

---

## Hide Default Drop Area

Hide the default drop area while keeping the Uploader functional for programmatic or custom use.

```css
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

> This is useful when implementing a completely custom file selection UI using an external button to trigger the file browser.

---

## fileListRendering Event

The `fileListRendering` event fires before each file item is rendered in the list. Use it to customize individual file item elements.

```tsx
const onFileListRendering = (args: any): void => {
  // args.element — the LI element being rendered
  // args.fileInfo — file data for this item
  if (args.fileInfo.size > 1000000) {
    args.element.style.backgroundColor = '#fff3cd'; // Highlight large files
  }
};

<UploaderComponent
  asyncSettings={asyncSettings}
  fileListRendering={onFileListRendering}
/>
```

> The deprecated `rendering` event is replaced by `fileListRendering`. Use `fileListRendering` in new implementations.

---

## Gotchas

- **Template + remove/progress** — When using a `template`, the default remove icon and progress bar are replaced. Hook into `removing` and `progress` events to implement these in your template.
- **`showFileList={false}` + upload/remove** — Always pass `true` as the second argument (`custom`) when calling `upload()` and `remove()` with a custom UI.
- **`buttons` overrides locale** — If both `buttons` and `locale` are set, `buttons` property values take precedence.
- **`cssClass` appends** — `cssClass` adds to the existing root class, not replaces it.
- **CSS specificity** — Syncfusion styles have high specificity; use `!important` or add a more specific selector when overriding.
