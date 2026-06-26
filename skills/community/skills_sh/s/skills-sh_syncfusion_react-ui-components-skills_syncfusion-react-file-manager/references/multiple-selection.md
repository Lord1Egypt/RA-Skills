# Multiple Selection & Range Selection in React File Manager

Enable users to select multiple files and folders at once using different methods like keyboard shortcuts, mouse drag, and checkboxes.

## Table of Contents

1. [Overview](#overview)
2. [Basic Multi-Selection](#basic-multi-selection)
3. [Range Selection](#range-selection)
4. [Disable Multi-Selection](#disable-multi-selection)
5. [Checkbox Selection](#checkbox-selection)
6. [Programmatic Selection](#programmatic-selection)
7. [Selection Events](#selection-events)
8. [Advanced Selection Patterns](#advanced-selection-patterns)
9. [Keyboard Shortcuts](#keyboard-shortcuts)
10. [Configuration Reference](#configuration-reference)

## Overview

File Manager supports multiple selection with flexible configuration:
- **Standard Multi-Select**: Ctrl+Click or Shift+Click to select multiple items
- **Range Selection**: Click and drag to select contiguous items
- **Checkbox Selection**: Visible checkboxes for direct selection
- **Select All**: Ctrl+A keyboard shortcut or API method
- **Programmatic Selection**: Set selectedItems initially or via API

## Basic Multi-Selection

### Enable Multi-Selection (Default)

Multi-selection is enabled by default on File Manager. Users can select multiple files using:
- **Ctrl+Click**: Select individual non-contiguous items
- **Shift+Click**: Select contiguous range
- **Checkboxes**: Click checkboxes to select items (visible on hover)
- **Ctrl+A**: Select all items in current folder

```tsx
import React from 'react';
import { 
  FileManagerComponent, 
  Inject, 
  DetailsView, 
  NavigationPane, 
  Toolbar 
} from '@syncfusion/ej2-react-filemanager';

function MultiSelectFileManager() {
  const hostUrl = "url";

  const handleFileSelect = (args: any) => {
    console.log(
      args.fileDetails.name + " has been " + args.action + "ed"
    );
    // args.action = 'select' or 'unselect'
  };

  return (
    <FileManagerComponent
      id="file"
      view="Details"
      height="375px"
      allowMultiSelection={true}  // Default, can be omitted
      ajaxSettings={{
        downloadUrl: hostUrl + 'api/FileManager/Download',
        getImageUrl: hostUrl + "api/FileManager/GetImage",
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        url: hostUrl + "api/FileManager/FileOperations"
      }}
      fileSelect={handleFileSelect}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default MultiSelectFileManager;
```

## Range Selection

### Enable Range Selection

Range selection allows users to select multiple contiguous items by clicking and dragging:

```tsx
import React from 'react';
import { 
  FileManagerComponent, 
  Inject, 
  DetailsView, 
  NavigationPane, 
  Toolbar 
} from '@syncfusion/ej2-react-filemanager';

function RangeSelectionFileManager() {
  const hostUrl = "url";

  return (
    <FileManagerComponent
      id="file"
      view="Details"
      height="375px"
      allowMultiSelection={true}
      enableRangeSelection={true}  // Enable range selection
      ajaxSettings={{
        downloadUrl: hostUrl + 'api/FileManager/Download',
        getImageUrl: hostUrl + "api/FileManager/GetImage",
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        url: hostUrl + "api/FileManager/FileOperations"
      }}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default RangeSelectionFileManager;
```

**How it works:**
1. Click on first item
2. Drag mouse down to last item you want to select
3. All items in the range are selected

## Disable Multi-Selection

### Single Select Mode

To force single file selection only:

```tsx
import React from 'react';
import { 
  FileManagerComponent, 
  Inject, 
  DetailsView, 
  NavigationPane, 
  Toolbar 
} from '@syncfusion/ej2-react-filemanager';

function SingleSelectFileManager() {
  const hostUrl = "url";

  return (
    <FileManagerComponent
      id="file"
      height="375px"
      allowMultiSelection={false}  // Disable multi-selection
      showItemCheckBoxes={false}   // Hide checkboxes
      ajaxSettings={{
        downloadUrl: hostUrl + 'api/FileManager/Download',
        getImageUrl: hostUrl + "api/FileManager/GetImage",
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        url: hostUrl + "api/FileManager/FileOperations"
      }}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default SingleSelectFileManager;
```

> **Important**: Setting both `allowMultiSelection={false}` and `showItemCheckBoxes={false}` prevents all multi-selection methods.

## Checkbox Selection

### Show/Hide Item Checkboxes

Control checkbox visibility for multi-select:

```tsx
// Show checkboxes (visible on hover)
<FileManagerComponent
  showItemCheckBoxes={true}  // Default
/>

// Hide checkboxes (no click-to-select via checkboxes)
<FileManagerComponent
  showItemCheckBoxes={false}
/>
```

## Programmatic Selection

### Pre-select Items on Load

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function PreselectedFileManager() {
  return (
    <FileManagerComponent
      id="file"
      height="375px"
      // Pre-select items by name
      selectedItems={['Documents', 'Pictures']}
      ajaxSettings={{
        url: "url"
      }}
    />
  );
}

export default PreselectedFileManager;
```

### Select/Deselect Items via API

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function ProgrammaticSelectionFileManager() {
  const fileManagerRef = useRef<FileManagerComponent>(null);

  const handleSelectAll = () => {
    // Select all items in current folder
    fileManagerRef.current?.selectAll();
  };

  const handleClearSelection = () => {
    // Clear all selections
    fileManagerRef.current?.clearSelection();
  };

  const handleGetSelected = () => {
    // Get array of selected file objects
    const selected = fileManagerRef.current?.getSelectedFiles();
    console.log('Selected files:', selected);
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={handleSelectAll}>Select All</button>
        <button onClick={handleClearSelection} style={{ marginLeft: '5px' }}>
          Clear Selection
        </button>
        <button onClick={handleGetSelected} style={{ marginLeft: '5px' }}>
          Get Selected Files
        </button>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        id="file"
        height="375px"
        allowMultiSelection={true}
        ajaxSettings={{
          url: "url"
        }}
      />
    </div>
  );
}

export default ProgrammaticSelectionFileManager;
```

## Selection Events

### File Selection Event

The `fileSelect` event is triggered when files are selected or deselected:

```tsx
import React from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function SelectionEventsFileManager() {
  const handleFileSelect = (args: any) => {
    // args.fileDetails - The selected/deselected file object
    // args.action - 'select' or 'unselect'
    
    console.log('File:', args.fileDetails.name);
    console.log('Action:', args.action);
    
    // Multiple items selected
    if (Array.isArray(args.fileDetails)) {
      console.log('Selected count:', args.fileDetails.length);
      console.log('Names:', args.fileDetails.map((f: any) => f.name));
    }
  };

  return (
    <FileManagerComponent
      id="file"
      height="375px"
      allowMultiSelection={true}
      ajaxSettings={{
        url: "url"
      }}
      fileSelect={handleFileSelect}
    />
  );
}

export default SelectionEventsFileManager;
```

### File Selection Event (Before Selection)

The `fileSelection` event is triggered before selection (cancelable):

```tsx
const handleFileSelection = (args: any) => {
  // args.fileDetails - The file about to be selected
  // args.cancel - Set to true to prevent selection
  
  // Prevent selecting hidden files
  if (args.fileDetails.name.startsWith('.')) {
    args.cancel = true;
    console.log('Cannot select hidden files');
  }
};

<FileManagerComponent
  fileSelection={handleFileSelection}
/>
```

## Advanced Selection Patterns

### Selection with Filtering

```tsx
import React, { useState } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function FilteredSelectionFileManager() {
  const [selectedFiles, setSelectedFiles] = useState<any[]>([]);

  const handleFileSelect = (args: any) => {
    if (args.action === 'select') {
      setSelectedFiles(prev => [...prev, args.fileDetails]);
    } else {
      setSelectedFiles(prev =>
        prev.filter(f => f.id !== args.fileDetails.id)
      );
    }
  };

  const handleSelectDocuments = () => {
    // Get file manager instance and select PDF files
    // Implementation depends on your data structure
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <h3>Selected: {selectedFiles.length}</h3>
        <ul>
          {selectedFiles.map((f: any) => (
            <li key={f.id}>{f.name}</li>
          ))}
        </ul>
      </div>

      <FileManagerComponent
        id="file"
        height="375px"
        allowMultiSelection={true}
        ajaxSettings={{
          url: "url"
        }}
        fileSelect={handleFileSelect}
      />
    </div>
  );
}

export default FilteredSelectionFileManager;
```

### Select by File Type

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function SelectByTypeFileManager() {
  const fileManagerRef = useRef<FileManagerComponent>(null);

  const selectPDFFiles = () => {
    const allFiles = fileManagerRef.current?.getSelectedFiles();
    // Filter and select only PDF files
    // Implementation varies by data structure
  };

  const selectByExtension = (extension: string) => {
    // Custom logic to select files by extension
    // Uses fileSelect event to track selections
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={selectPDFFiles}>Select PDFs</button>
        <button onClick={() => selectByExtension('.docx')}>
          Select Documents
        </button>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        id="file"
        height="375px"
        allowMultiSelection={true}
        ajaxSettings={{
          url: "url"
        }}
      />
    </div>
  );
}

export default SelectByTypeFileManager;
```

## Keyboard Shortcuts

### Supported Shortcuts for Selection

| Shortcut | Action |
|----------|--------|
| **Ctrl+A** | Select all items in current folder |
| **Ctrl+Click** | Add/remove individual item to/from selection |
| **Shift+Click** | Select contiguous range from last selected to clicked item |
| **Space** | Toggle checkbox for current item (when enabled) |

> **Note**: With virtualization enabled, Ctrl+A only selects visible items in viewport.

## Configuration Reference

### Props

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `allowMultiSelection` | boolean | true | Enable/disable multi-selection |
| `enableRangeSelection` | boolean | false | Enable click-drag range selection |
| `showItemCheckBoxes` | boolean | true | Show checkboxes on hover |
| `selectedItems` | string[] | [] | Pre-select items by name on load |

### Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `selectAll()` | Select all items in current path | `ref.current?.selectAll()` |
| `clearSelection()` | Deselect all items | `ref.current?.clearSelection()` |
| `getSelectedFiles()` | Get array of selected items | `const items = ref.current?.getSelectedFiles()` |

### Events

| Event | Args | When Triggered |
|-------|------|----------------|
| `fileSelection` | FileSelectionEventArgs | Before item selection (cancelable) |
| `fileSelect` | FileSelectEventArgs | After item selected/deselected |

## Best Practices

1. **User Feedback**: Show selection count and preview of selected items
2. **Large Selections**: Batch process operations on multiple selected files
3. **Keyboard Support**: Always ensure keyboard shortcuts are available
4. **Accessibility**: Test with screen readers for selection announcements
5. **Performance**: Use virtualization when selecting from large lists
6. **Confirmation**: Ask for confirmation before bulk operations
7. **Visual Feedback**: Maintain clear visual indication of selected items

## Common Use Cases

### Case 1: Bulk Download
```tsx
const handleBulkDownload = () => {
  const selected = fileManagerRef.current?.getSelectedFiles();
  selected?.forEach(file => {
    // Trigger download for each file
  });
};
```

### Case 2: Bulk Delete
```tsx
const handleBulkDelete = () => {
  const selected = fileManagerRef.current?.getSelectedFiles();
  const confirmed = window.confirm(
    `Delete ${selected?.length} items?`
  );
  if (confirmed) {
    fileManagerRef.current?.deleteFiles(
      selected?.map(f => f.id)
    );
  }
};
```

### Case 3: Move Multiple Files
```tsx
const handleMoveSelected = (targetFolderId: string) => {
  const selected = fileManagerRef.current?.getSelectedFiles();
  // Call backend to move files
};
```

---

**Next:** Learn about [Virtualization](virtualization.md) for handling large file lists efficiently.
