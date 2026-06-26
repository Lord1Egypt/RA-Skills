# Preselect Items in React File Manager

You can programmatically preselect items in the React File Manager component using the `fileLoad` event and the `selectedItems` property. This allows you to automatically select specific files and folders when the File Manager loads or when navigating to different directories.

## Table of Contents

1. [Basic Preselection](#basic-preselection)
2. [Advanced Preselection Patterns](#advanced-preselection-patterns)
3. [Programmatic Selection Management](#programmatic-selection-management)
4. [Complete Example with Advanced Preselection](#complete-example-with-advanced-preselection)
5. [Selection Methods Reference](#selection-methods-reference)
6. [Best Practices](#best-practices)
7. [Related Topics](#related-topics)

## Basic Preselection

### Pattern 1: Simple Preselection in fileLoad Event

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function BasicPreselectExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  // Items to preselect
  const preselectItems = [
    'File1.docx',
    'File2.pdf',
    'FolderA',
    'Image.png'
  ];

  const handleFileLoad = (args) => {
    // Set the array of file names to enable selection
    fileManagerRef.current.selectedItems = preselectItems;
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      id="file-manager"
      height="500px"
      view="Details"
      ajaxSettings={{
        url: hostUrl + 'api/FileManager/FileOperations',
        downloadUrl: hostUrl + 'api/FileManager/Download',
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        getImageUrl: hostUrl + 'api/FileManager/GetImage'
      }}
      fileLoad={handleFileLoad}
    >
      <Inject services={[NavigationPane, DetailsView, Toolbar]} />
    </FileManagerComponent>
  );
}

export default BasicPreselectExample;
```

## Advanced Preselection Patterns

### Pattern 1: Preselect Based on File Type

```typescript
function PreselectByFileTypeExample() {
  const fileManagerRef = useRef(null);

  const handleFileLoad = (args) => {
    // Get all files in current directory
    const files = args.files || [];
    
    // Filter by file type
    const imageFiles = files
      .filter(file => /\.(jpg|jpeg|png|gif|bmp)$/i.test(file.name))
      .map(file => file.name);
    
    // Preselect all image files
    fileManagerRef.current.selectedItems = imageFiles;
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      fileLoad={handleFileLoad}
      // ... other props
    />
  );
}
```

### Pattern 2: Preselect Based on File Size

```typescript
function PreselectByFileSizeExample() {
  const fileManagerRef = useRef(null);
  const sizeThreshold = 10 * 1024 * 1024; // 10MB

  const handleFileLoad = (args) => {
    const files = args.files || [];
    
    // Select files larger than threshold
    const largeFiles = files
      .filter(file => file.size >= sizeThreshold && file.isFile)
      .map(file => file.name);
    
    fileManagerRef.current.selectedItems = largeFiles;
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      fileLoad={handleFileLoad}
      // ... other props
    />
  );
}
```

### Pattern 3: Preselect Based on Date

```typescript
function PreselectByDateExample() {
  const fileManagerRef = useRef(null);
  const daysOld = 7; // Select files modified in last 7 days

  const handleFileLoad = (args) => {
    const files = args.files || [];
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysOld);
    
    const recentFiles = files
      .filter(file => new Date(file.dateModified) >= cutoffDate)
      .map(file => file.name);
    
    fileManagerRef.current.selectedItems = recentFiles;
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      fileLoad={handleFileLoad}
      // ... other props
    />
  );
}
```

### Pattern 4: Preselect with Pattern Matching

```typescript
function PreselectByPatternExample() {
  const fileManagerRef = useRef(null);
  const pattern = /^report.*\.xlsx$/i; // Select files matching pattern

  const handleFileLoad = (args) => {
    const files = args.files || [];
    
    const matchingFiles = files
      .filter(file => pattern.test(file.name))
      .map(file => file.name);
    
    fileManagerRef.current.selectedItems = matchingFiles;
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      fileLoad={handleFileLoad}
      // ... other props
    />
  );
}
```

### Pattern 5: Context-Aware Preselection

```typescript
function ContextAwarePreselectExample() {
  const fileManagerRef = useRef(null);
  const userRole = localStorage.getItem('userRole');

  const handleFileLoad = (args) => {
    const files = args.files || [];
    let itemsToSelect = [];

    switch (userRole) {
      case 'Administrator':
        // Admin sees all files
        itemsToSelect = files.map(f => f.name);
        break;
      
      case 'Manager':
        // Manager sees reports
        itemsToSelect = files
          .filter(f => /report|summary/i.test(f.name))
          .map(f => f.name);
        break;
      
      case 'Employee':
        // Employees see only recent files
        const recent = new Date();
        recent.setDate(recent.getDate() - 1);
        itemsToSelect = files
          .filter(f => new Date(f.dateModified) >= recent)
          .map(f => f.name);
        break;
    }

    fileManagerRef.current.selectedItems = itemsToSelect;
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      fileLoad={handleFileLoad}
      // ... other props
    />
  );
}
```

## Programmatic Selection Management

### Pattern 1: Select/Deselect on Command

```typescript
import React, { useRef } from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function ProgrammaticSelectionExample() {
  const fileManagerRef = useRef(null);

  const handleSelectAll = () => {
    fileManagerRef.current?.selectAll();
  };

  const handleClearSelection = () => {
    fileManagerRef.current?.clearSelection();
  };

  const handleSelectImages = () => {
    const files = fileManagerRef.current?.getSelectedFiles?.();
    // Note: You need to access files from the component's current state
    // This is a simplified example
    fileManagerRef.current.selectedItems = ['photo1.jpg', 'photo2.png'];
  };

  return (
    <div>
      <div className="button-group" style={{ marginBottom: '20px' }}>
        <ButtonComponent onClick={handleSelectAll}>
          Select All
        </ButtonComponent>
        <ButtonComponent onClick={handleSelectImages}>
          Select Images
        </ButtonComponent>
        <ButtonComponent onClick={handleClearSelection}>
          Clear Selection
        </ButtonComponent>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        height="400px"
        view="Details"
        allowMultiSelection={true}
        // ... other props
      />
    </div>
  );
}

export default ProgrammaticSelectionExample;
```

### Pattern 2: Get Selected Items

```typescript
function GetSelectedItemsExample() {
  const fileManagerRef = useRef(null);

  const handleShowSelected = () => {
    const selectedItems = fileManagerRef.current?.getSelectedFiles?.();
    console.log('Selected items:', selectedItems);
    alert(`Selected ${selectedItems?.length || 0} items`);
  };

  const handleProcessSelected = () => {
    const selectedItems = fileManagerRef.current?.getSelectedFiles?.();
    
    if (selectedItems && selectedItems.length > 0) {
      console.log('Processing selected items:');
      selectedItems.forEach(item => {
        console.log(`- ${item}`);
      });
    }
  };

  return (
    <div>
      <div className="button-group">
        <ButtonComponent onClick={handleShowSelected}>
          Show Selected
        </ButtonComponent>
        <ButtonComponent onClick={handleProcessSelected}>
          Process Selected
        </ButtonComponent>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        height="400px"
        // ... other props
      />
    </div>
  );
}

export default GetSelectedItemsExample;
```

## Complete Example with Advanced Preselection

```typescript
import React, { useRef, useState } from 'react';
import {
  FileManagerComponent,
  Inject,
  NavigationPane,
  DetailsView,
  Toolbar
} from '@syncfusion/ej2-react-filemanager';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

function AdvancedPreselectExample() {
  const fileManagerRef = useRef(null);
  const [selectionMode, setSelectionMode] = useState('all');
  const hostUrl = "url";

  const selectionModes = [
    { text: 'All Files', value: 'all' },
    { text: 'Recent Files', value: 'recent' },
    { text: 'Large Files', value: 'large' },
    { text: 'Images Only', value: 'images' },
    { text: 'Documents Only', value: 'documents' },
    { text: 'No Selection', value: 'none' }
  ];

  const getItemsToSelect = (files, mode) => {
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    const sizeTreshold = 5 * 1024 * 1024; // 5MB

    switch (mode) {
      case 'all':
        return files.map(f => f.name);
      
      case 'recent':
        return files
          .filter(f => new Date(f.dateModified) >= oneWeekAgo)
          .map(f => f.name);
      
      case 'large':
        return files
          .filter(f => f.size >= sizeTreshold && f.isFile)
          .map(f => f.name);
      
      case 'images':
        return files
          .filter(f => /\.(jpg|jpeg|png|gif|bmp)$/i.test(f.name))
          .map(f => f.name);
      
      case 'documents':
        return files
          .filter(f => /\.(doc|docx|pdf|xls|xlsx|ppt|pptx)$/i.test(f.name))
          .map(f => f.name);
      
      case 'none':
        return [];
      
      default:
        return [];
    }
  };

  const handleFileLoad = (args) => {
    const files = args.files || [];
    const itemsToSelect = getItemsToSelect(files, selectionMode);
    fileManagerRef.current.selectedItems = itemsToSelect;
  };

  const handleSelectionModeChange = (args) => {
    setSelectionMode(args.value);
    // Trigger file load to update selection
    fileManagerRef.current?.refresh?.();
  };

  const handleClearSelection = () => {
    fileManagerRef.current?.clearSelection?.();
  };

  const handleSelectAll = () => {
    fileManagerRef.current?.selectAll?.();
  };

  const handleShowInfo = () => {
    const selectedItems = fileManagerRef.current?.getSelectedFiles?.();
    alert(`${selectedItems?.length || 0} items selected in "${selectionMode}" mode`);
  };

  return (
    <div className="control-section">
      <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label>Selection Mode: </label>
          <DropDownListComponent
            dataSource={selectionModes}
            fields={{ text: 'text', value: 'value' }}
            value={selectionMode}
            change={handleSelectionModeChange}
            style={{ width: '200px' }}
          />
        </div>

        <div className="button-group">
          <ButtonComponent onClick={handleSelectAll} cssClass='e-small'>
            Select All
          </ButtonComponent>
          <ButtonComponent onClick={handleClearSelection} cssClass='e-small'>
            Clear Selection
          </ButtonComponent>
          <ButtonComponent onClick={handleShowInfo} cssClass='e-small'>
            Show Info
          </ButtonComponent>
        </div>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        id="advanced-preselect"
        height="500px"
        view="Details"
        allowMultiSelection={true}
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        fileLoad={handleFileLoad}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default AdvancedPreselectExample;
```

## Selection Methods Reference

| Method | Description |
|--------|-------------|
| `selectAll()` | Select all items in current directory |
| `clearSelection()` | Clear all selections |
| `getSelectedFiles()` | Get array of selected file names |
| `selectedItems` | Property to set/get selected items |

## Best Practices

1. **Use fileLoad Event** - Wait for files to load before selecting
2. **Validate Selection** - Ensure selected items exist
3. **Provide User Feedback** - Show which items are selected
4. **Respect Permissions** - Only select accessible items
5. **Handle Edge Cases** - Account for empty directories
6. **Performance** - Avoid selecting too many items at once

## Related Topics

- [Multiple Selection](multiple-selection.md)
- [File Operations](file-operations.md)
- [Getting Started](getting-started.md)
