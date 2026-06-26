# Inserting Media in Syncfusion React Rich Text Editor

## Table of Contents
- [Inserting Images](#inserting-images)
- [Image Save Formats](#image-save-formats)
- [Server-Side Image Upload](#server-side-image-upload)
- [Inserting Videos](#inserting-videos)
- [Inserting Audio](#inserting-audio)
- [File Browser Integration](#file-browser-integration)

## Inserting Images

Inject the `Image` module and add `'Image'` to toolbar items. Users can insert images via URL or file upload from the insert image dialog.

```tsx
import {
  HtmlEditor, Image, Inject, Link,
  QuickToolbar, RichTextEditorComponent, Toolbar
} from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = { items: ['Image', 'Bold', 'Italic'] };

function App() {
  return (
    <RichTextEditorComponent height={450} toolbarSettings={toolbarSettings}>
      <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

### Configuring Image Insert Settings

Use `insertImageSettings` to control how images are saved and displayed:

```tsx
const insertImageSettings: ImageSettingsModel = {
  saveFormat: 'Base64',       // 'Base64' or 'Blob'
  width: '300px',             // default image width
  height: 'auto',             // default image height
  minWidth: '10px',
  minHeight: '10px',
  maxWidth: '100%',
  maxHeight: '600px',
  display: 'inline',          // 'inline' or 'break' (block)
  allowedTypes: ['.jpg', '.png', '.gif', '.webp'],  // restrict file types
};

<RichTextEditorComponent insertImageSettings={insertImageSettings}>
  <Inject services={[Toolbar, Image, HtmlEditor, QuickToolbar]} />
</RichTextEditorComponent>
```

## Image Save Formats

| Format | Behavior |
|---|---|
| `Base64` | Image is embedded as a base64 data URL in the HTML. No server required. Best for small images. |
| `Blob` | Image is saved as a blob URL (`blob:http://...`). Ephemeral — use with `saveUrl` for persistence. |

```tsx
// Base64 embedding (no server needed)
const insertImageSettings: ImageSettingsModel = { saveFormat: 'Base64' };

// Blob with server upload
const insertImageSettings: ImageSettingsModel = {
  saveFormat: 'Blob',
  saveUrl: 'url',
  path: 'url'
};
```

## Server-Side Image Upload

Configure `saveUrl` for automatic upload when images are inserted via the dialog:

```tsx
const insertImageSettings: ImageSettingsModel = {
  saveUrl: 'url',
  path: 'url',
  // Optionally remove saved images
  removeUrl: 'url',
};

<RichTextEditorComponent insertImageSettings={insertImageSettings}>
  <Inject services={[Toolbar, Image, HtmlEditor, QuickToolbar]} />
</RichTextEditorComponent>
```

**Handle the `imageUploadSuccess` event** to process the server's response:

```tsx
const onImageUploadSuccess = (args: ImageSuccessEventArgs) => {
  // args.e.currentTarget.response — server JSON response
  const response = JSON.parse(args.e.currentTarget.response);
  args.file.name = response.name;   // update image name if server renames it
};

<RichTextEditorComponent
  insertImageSettings={insertImageSettings}
  imageUploadSuccess={onImageUploadSuccess}
>
  <Inject services={[Toolbar, Image, HtmlEditor, QuickToolbar]} />
</RichTextEditorComponent>
```

## Inserting Videos

Inject `Video` and add `'Video'` to toolbar items. Supports embedded video URLs (YouTube, Vimeo) and direct file uploads.

```tsx
import { Video } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = { items: ['Video', 'Bold'] };
const insertVideoSettings: VideoSettingsModel = {
  saveUrl: 'url',
  path: 'url',
  minWidth: '100px',
  minHeight: '70px',
  width: '300px',
  height: '200px',
};

function App() {
  return (
    <RichTextEditorComponent
      toolbarSettings={toolbarSettings}
      insertVideoSettings={insertVideoSettings}
    >
      <Inject services={[Toolbar, HtmlEditor, Video, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

## Inserting Audio

Inject `Audio` and add `'Audio'` to toolbar items. Supports URL embedding and file upload.

```tsx
import { Audio } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = { items: ['Audio', 'Bold'] };
const insertAudioSettings: AudioSettingsModel = {
  saveUrl: 'url',
  path: 'url',
  allowedTypes: ['.mp3', '.wav', '.ogg'],
};

function App() {
  return (
    <RichTextEditorComponent
      toolbarSettings={toolbarSettings}
      insertAudioSettings={insertAudioSettings}
    >
      <Inject services={[Toolbar, HtmlEditor, Audio, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

## File Browser Integration

Inject `FileManager` to let users browse files from a server-side file system and insert them directly into the editor.

```tsx
import { FileManager } from '@syncfusion/ej2-react-richtexteditor';

const fileManagerSettings: FileManagerSettingsModel = {
  enable: true,
  path: '/Pictures/Food',
  ajaxSettings: {
    url: 'url',
    getImageUrl: 'url',
    uploadUrl: 'url',
    downloadUrl: 'url'
  }
};

const toolbarSettings: ToolbarSettingsModel = { items: ['Image'] };

function App() {
  return (
    <RichTextEditorComponent
      toolbarSettings={toolbarSettings}
      fileManagerSettings={fileManagerSettings}
    >
      <Inject services={[Toolbar, HtmlEditor, Image, FileManager, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

> The `FileManager` module requires a server-side file management controller. See Syncfusion's FileManager documentation for the API contract.
