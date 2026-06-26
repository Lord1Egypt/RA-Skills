# Opening and Saving Images

## Table of Contents
- [Supported Formats](#supported-formats)
- [Opening Images](#opening-images)
- [Saving and Exporting](#saving-and-exporting)
- [Image Events](#image-events)
- [Advanced Scenarios](#advanced-scenarios)

## Supported Formats

**Supported for Opening:** PNG, JPEG, JPG, SVG, WEBP, BMP (from URLs, files, base64, blobs)
**Default Save Format:** PNG
**Supported for Saving:** PNG, JPEG, SVG, WEBP

## Opening Images

### From URL

Open images from a publicly accessible URL:

```tsx
function imageEditorCreated(): void {
  imgObj.open('https://ej2.syncfusion.com/react/documentation/image-editor/images/bridge.jpeg');
}
```

### From Base64 String

Open images stored as base64 encoded strings:

```tsx
let base64String: string = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...';
imgObj.open(base64String);
```

Export as base64 or blob:

```tsx
function exportImage(): void {
  // Export as PNG file
  imgObj.export('image/png', 'edited-image');
  
  // Or get image data for processing
  const imageData = imgObj.getImageData();
  if (imageData) {
    console.log('Image data captured');
  }
}
```

### From Blob

Open images from blob objects:

```tsx
function openFromBlob(blob: Blob): void {
  // Create object URL from blob
  const blobUrl = URL.createObjectURL(blob);
  imgObj.open(blobUrl);
  
  // Clean up after loading
  setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
}

function exportToBlob(): void {
  // Export will generate downloadable file
  imgObj.export('image/png', 'edited-image');
}
```

### From File Uploader

Integrate with Syncfusion Uploader for file selection:

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function selected(args: any): void {
  if (args.filesData.length > 0) {
    const reader = new FileReader();
    reader.onload = () => {
      imgObj.open(reader.result);
    };
    reader.readAsDataURL(args.filesData[0].rawFile);
  }
}

return (
  <div>
    <UploaderComponent selected={selected} showFileList={false} />
    <ImageEditorComponent ref={(img) => { imgObj = img }} />
  </div>
);
```

### From File Manager

Use Syncfusion File Manager for browsing and selecting images:

```tsx
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

const fileOpen = (args: any) => {
  if (args.fileDetails.isFile && args.fileDetails.imageUrl) {
    args.cancel = true;
    imgObj.open(args.fileDetails.imageUrl);
  }
};

return (
  <div>
    <FileManagerComponent fileOpen={fileOpen} />
    <ImageEditorComponent ref={(img) => { imgObj = img }} />
  </div>
);
```

### From TreeView

Select images from a hierarchical tree structure:

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const clicked = (args: any) => {
  const nodeData = treeView.getTreeData(args.node.getAttribute('data-uid'))[0];
  if (nodeData && nodeData.image) {
    imgObj.open(nodeData.image);
  }
};

return (
  <div>
    <TreeViewComponent nodeClicked={clicked} />
    <ImageEditorComponent ref={(img) => { imgObj = img }} />
  </div>
);
```

### Open Image from Different Sources

Open images using the open method with URL or ImageData:

```tsx
// Open from URL
imgObj.open('https://example.com/image.jpg');

// Open from base64 string
imgObj.open('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...');

// Open from blob
const blob = new Blob([imageData], { type: 'image/png' });
const blobUrl = URL.createObjectURL(blob);
imgObj.open(blobUrl);
```

## Saving and Exporting

### Export with Format

Export edited image with specific format and filename:

```tsx
// Save as PNG
imgObj.export('image/png', 'my-edited-image');

// Save as JPEG
imgObj.export('image/jpeg', 'my-edited-image', 0.95);

// Save as SVG
imgObj.export('image/svg+xml', 'my-edited-image');

// Save as WEBP
imgObj.export('image/webp', 'my-edited-image');
```

### Quick Save with Keyboard Shortcut

Users can press `Ctrl+S` to download the image in its original format.

### Save to Server

Export edited image for storage or transmission:

```tsx
function saveToServer(): void {
  // Export image (triggers download)
  imgObj.export('image/png', 'edited-image');
  
  // For API upload, use export event
  // The export method handles file download automatically
}

function setupCustomExport(): void {
  // Listen to saving event to intercept before export
  const onSaving = (args: any) => {
    console.log('Image being saved', args);
  };
}
```

### Save with Format Selection

Export in multiple formats:

```tsx
function exportInFormat(format: 'PNG' | 'JPEG' | 'SVG' | 'WEBP'): void {
  const mimeType = {
    PNG: 'image/png',
    JPEG: 'image/jpeg',
    SVG: 'image/svg+xml',
    WEBP: 'image/webp'
  }[format];
  
  imgObj.export(mimeType, `edited-image.${format.toLowerCase()}`);
}

// Usage
exportInFormat('PNG');
exportInFormat('JPEG');
```

### Get Image Dimensions

Retrieve edited image dimensions:

```tsx
function getImageDimensions(): void {
  const dimension = imgObj.getImageDimension();
  if (dimension) {
    console.log(`Image size: ${dimension.width}x${dimension.height}`);
  }
}

function resizeAndExport(newWidth: number, newHeight: number): void {
  imgObj.resize(newWidth, newHeight);
  imgObj.export('image/png', 'resized-image');
}
```

## Image Events

### File Opened Event

Triggered after image is successfully loaded:

```tsx
function fileOpened(args: any): void {
  console.log('Filename:', args.fileName);
  console.log('Filetype:', args.fileType);
  // Add watermark or apply defaults here
}

<ImageEditorComponent fileOpened={fileOpened} />
```

### BeforeSave Event

Triggered before image is saved/exported:

```tsx
function beforeSave(args: any): void {
  console.log('About to save image');
  // args.cancel = true; // Prevent default save
}

<ImageEditorComponent beforeSave={beforeSave} />
```

### Created Event

Triggered when component is initialized:

```tsx
function created(): void {
  console.log('Image Editor ready');
}

<ImageEditorComponent created={created} />
```

### Destroyed Event

Triggered when component is removed:

```tsx
function destroyed(): void {
  console.log('Image Editor cleaned up');
}

<ImageEditorComponent destroyed={destroyed} />
```

## Advanced Scenarios

### Add Watermark on Open

Automatically add watermark when image opens:

```tsx
function fileOpened(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Syncfusion',
    'Arial',
    40,
    false,
    false,
    '#80330075' // Semi-transparent color
  );
}

<ImageEditorComponent fileOpened={fileOpened} />
```

### Custom Save with Server Upload

Intercept save event for custom handling:

```tsx
function onSaving(args: any): void {
  // Handle pre-save logic
  console.log('Image is being saved');
  
  // Export with specific format
  imgObj.export('image/png', 'edited-image');
  
  // Optionally send to server
  fetch('/api/image-saved', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }).then(res => res.json()).then(data => {
      console.log('Uploaded:', data);
    });
  });
}

<ImageEditorComponent beforeSave={beforeSave} />
```
