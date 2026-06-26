# Drag-and-Drop Features

Master drag-and-drop functionality for moving files between folders and handling custom drop zones.

## Table of Contents

1. [Enable Drag-and-Drop](#enable-drag-and-drop)
2. [Drag-and-Drop Events](#drag-and-drop-events)
3. [Drag-and-Drop Validation](#drag-and-drop-validation)
4. [Advanced Drag-and-Drop](#advanced-drag-and-drop)
5. [Complete Example](#complete-example)
6. [Common Patterns](#common-patterns)
7. [Edge Cases](#edge-cases)
8. [Next Steps](#next-steps)

## Enable Drag-and-Drop

### Basic Drag-and-Drop

Enable by default or explicitly configure:

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function DragDropExample() {
  return (
    <FileManagerComponent
      allowDragAndDrop={true}
      ajaxSettings={{
        url: "url",
        getImageUrl: "url",
        uploadUrl: "url",
        downloadUrl: "url"
      }}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default DragDropExample;
```

**What Drag-Drop Enables:**
- Drag files between folders
- Drag from file manager to other drop zones
- Visual feedback during drag
- Move operations (files are moved, not copied)

## Drag-and-Drop Events

### Handle Drag Start

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function DragStartExample() {
  const fileManagerRef = useRef(null);

  const handleFileDragStart = (args) => {
    console.log('Drag started:', args.fileDetails);
    console.log('Source element:', args.target);
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      fileDragStart={handleFileDragStart}
      ajaxSettings={{...}}
      allowDragAndDrop={true}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default DragStartExample;
```

**Available Events:**
- `fileDragStart` - Drag operation starts
- `fileDragStop` - Drag ends (drop or cancel)
- `fileDropped` - File successfully dropped

### Handle File Drop

```tsx
const handleFileDropped = (args) => {
  console.log('Files dropped:', args.fileDetails);
  console.log('Target path:', args.path);
  
  // Validate drop operation
  if (args.path.includes('/restricted')) {
    args.cancel = true;
    console.error('Cannot drop in restricted folder');
  }
};

<FileManagerComponent
  fileDropped={handleFileDropped}
  ajaxSettings={{...}}
  allowDragAndDrop={true}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

### Handle Drag Stop

```tsx
const handleFileDragStop = (args) => {
  console.log('Drag ended');
  console.log('Drop cancelled:', args.cancel);
};

<FileManagerComponent
  fileDragStop={handleFileDragStop}
  ajaxSettings={{...}}
  allowDragAndDrop={true}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Drag-and-Drop Validation

### Prevent Drag of Specific Files

```tsx
const handleFileDragStart = (args) => {
  const restrictedExtensions = ['.exe', '.bat', '.cmd'];
  
  args.fileDetails.forEach(file => {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (restrictedExtensions.includes(ext)) {
      args.cancel = true;
      console.error(`Cannot drag ${ext} files`);
    }
  });
};

<FileManagerComponent
  fileDragStart={handleFileDragStart}
  allowDragAndDrop={true}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

### Prevent Drop in Specific Folders

```tsx
const handleFileDropped = (args) => {
  const restrictedPaths = ['/System', '/bin', '/root'];
  
  if (restrictedPaths.some(path => args.path.startsWith(path))) {
    args.cancel = true;
    console.error('Cannot drop in protected folders');
  }
};

<FileManagerComponent
  fileDropped={handleFileDropped}
  allowDragAndDrop={true}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Advanced Drag-and-Drop

### Drag Multiple Files

```tsx
const handleFileDragStart = (args) => {
  const fileCount = args.fileDetails.length;
  const totalSize = args.fileDetails.reduce((sum, f) => sum + f.size, 0);
  
  console.log(`Dragging ${fileCount} files, ${totalSize} bytes`);
  
  // Validate total size
  const maxTotalSize = 500 * 1024 * 1024; // 500 MB
  if (totalSize > maxTotalSize) {
    args.cancel = true;
    console.error('Total drag size exceeds limit');
  }
};

<FileManagerComponent
  fileDragStart={handleFileDragStart}
  allowMultiSelection={true}
  allowDragAndDrop={true}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

### Drag from External Sources

Allow dragging files from file explorer into File Manager:

```tsx
<FileManagerComponent
  allowDragAndDrop={true}
  ajaxSettings={{
    url: "url",
    uploadUrl: "url",
    getImageUrl: "url",
    downloadUrl: "url"
  }}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Behavior:**
- Drag files from OS file explorer
- Drop into File Manager
- Automatically uploads via `uploadUrl`
- Same validation as manual upload applies

## Complete Example

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function AdvancedDragDrop() {
  const handleFileDragStart = (args) => {
    console.log('Drag started:', args.fileDetails.length, 'files');
  };

  const handleFileDragStop = (args) => {
    console.log('Drag stopped');
  };

  const handleFileDropped = (args) => {
    console.log('Dropped at:', args.path);
    
    // Validate before drop
    const protectedFolders = ['/System', '/Admin'];
    if (protectedFolders.some(f => args.path.startsWith(f))) {
      args.cancel = true;
      alert('Cannot drop in protected folders');
    }
  };

  return (
    <FileManagerComponent
      allowDragAndDrop={true}
      allowMultiSelection={true}
      fileDragStart={handleFileDragStart}
      fileDragStop={handleFileDragStop}
      fileDropped={handleFileDropped}
      ajaxSettings={{
        url: "url",
        getImageUrl: "url",
        uploadUrl: "url",
        downloadUrl: "url"
      }}
      height="600px"
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default AdvancedDragDrop;
```

## Common Patterns

### Drag with Permission Check

```tsx
const handleFileDropped = (args) => {
  const userPermissions = ['Documents', 'Downloads'];
  
  if (!userPermissions.some(p => args.path.includes(p))) {
    args.cancel = true;
    alert('You do not have permission to drop here');
  }
};
```

### Drag with Size Validation

```tsx
const handleFileDragStart = (args) => {
  const maxDragSize = 1024 * 1024 * 1024; // 1 GB
  const totalSize = args.fileDetails.reduce((sum, f) => sum + f.size, 0);
  
  if (totalSize > maxDragSize) {
    args.cancel = true;
    alert('Cannot drag files exceeding 1 GB');
  }
};
```

## Edge Cases

**Issue: Drag-drop doesn't work**
- Verify `allowDragAndDrop={true}`
- Check browser console for errors
- Ensure drop target is valid

**Issue: Files duplicate on drop**
- Verify backend move operation (not copy)
- Check if `fileDropped` event has `args.cancel = true`

**Issue: Large file drag is slow**
- Consider showing progress indicator
- Implement backend optimization
- Use virtual scrolling for large file lists

## Next Steps

- **Customization:** Style and customize in [customization.md](customization.md)
- **File Operations:** Learn CRUD operations in [file-operations.md](file-operations.md)
- **Advanced:** Performance tips in [advanced-features.md](advanced-features.md)
