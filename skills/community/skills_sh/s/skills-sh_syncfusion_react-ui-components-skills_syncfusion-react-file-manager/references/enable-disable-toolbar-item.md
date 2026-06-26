# Enable/Disable Toolbar Items in React File Manager

The toolbar items in the React File Manager component can be dynamically enabled or disabled based on user actions, permissions, or application state using the `enableToolbarItems()` and `disableToolbarItems()` methods.

## Table of Contents

1. [Enable/Disable Methods](#enabledisable-methods)
2. [Basic Implementation](#basic-implementation)
3. [Advanced Patterns](#advanced-patterns)
4. [Complete Examples](#complete-examples)

## Enable/Disable Methods

### enableToolbarItems()

Enables specific toolbar items:

```typescript
// Enable single item
fileManagerRef.current?.enableToolbarItems(['delete']);

// Enable multiple items
fileManagerRef.current?.enableToolbarItems(['delete', 'rename', 'copy']);

// Enable all items
fileManagerRef.current?.enableToolbarItems(['newfolder', 'upload', 'delete', 'cut', 'copy', 'paste', 'rename', 'refresh']);
```

### disableToolbarItems()

Disables specific toolbar items:

```typescript
// Disable single item
fileManagerRef.current?.disableToolbarItems(['delete']);

// Disable multiple items
fileManagerRef.current?.disableToolbarItems(['delete', 'rename', 'copy', 'paste']);

// Disable all items
fileManagerRef.current?.disableToolbarItems(['newfolder', 'upload', 'delete', 'cut', 'copy', 'paste', 'rename', 'refresh']);
```

## Basic Implementation

### Pattern 1: Enable/Disable on Button Click

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function BasicEnableDisableExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const handleEnableDelete = () => {
    fileManagerRef.current?.enableToolbarItems(['delete']);
    alert('Delete toolbar item enabled');
  };

  const handleDisableDelete = () => {
    fileManagerRef.current?.disableToolbarItems(['delete']);
    alert('Delete toolbar item disabled');
  };

  const handleEnableAll = () => {
    fileManagerRef.current?.enableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste']);
    alert('All toolbar items enabled');
  };

  const handleDisableAll = () => {
    fileManagerRef.current?.disableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste']);
    alert('Destructive toolbar items disabled');
  };

  return (
    <div>
      <div className="button-group" style={{ marginBottom: '20px' }}>
        <ButtonComponent onClick={handleEnableDelete} cssClass='e-success'>
          Enable Delete
        </ButtonComponent>
        <ButtonComponent onClick={handleDisableDelete} cssClass='e-danger'>
          Disable Delete
        </ButtonComponent>
        <ButtonComponent onClick={handleEnableAll} cssClass='e-success'>
          Enable All
        </ButtonComponent>
        <ButtonComponent onClick={handleDisableAll} cssClass='e-danger'>
          Disable All
        </ButtonComponent>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        id="file-manager"
        height="400px"
        view="Details"
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        toolbarSettings={{
          items: ['NewFolder', 'Upload', 'Delete', 'Cut', 'Copy', 'Paste', 'Rename', 'Refresh', 'Details']
        }}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default BasicEnableDisableExample;
```

## Advanced Patterns

### Pattern 1: Enable/Disable Based on Selection

```typescript
function handleFileSelect(args) {
  const selectedItems = fileManagerRef.current?.getSelectedFiles();
  const itemCount = selectedItems?.length || 0;

  if (itemCount === 0) {
    // No selection - disable edit operations
    fileManagerRef.current?.disableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste']);
  } else if (itemCount === 1) {
    // Single item - enable all operations
    fileManagerRef.current?.enableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste']);
  } else {
    // Multiple items - disable rename (only works on single items)
    fileManagerRef.current?.disableToolbarItems(['rename']);
    fileManagerRef.current?.enableToolbarItems(['delete', 'cut', 'copy', 'paste']);
  }
}
```

### Pattern 2: Enable/Disable Based on File Type

```typescript
function handleFileSelect(args) {
  const selectedItems = fileManagerRef.current?.getSelectedFiles();
  
  if (selectedItems?.length === 1) {
    const fileName = selectedItems[0];
    const isImage = /\.(jpg|jpeg|png|gif|bmp)$/i.test(fileName);
    const isPdf = /\.pdf$/i.test(fileName);
    const isFolder = !fileName.includes('.');

    // Enable/disable based on file type
    if (isImage) {
      fileManagerRef.current?.enableToolbarItems(['preview']);
      fileManagerRef.current?.enableToolbarItems(['convert']);
    } else {
      fileManagerRef.current?.disableToolbarItems(['preview', 'convert']);
    }

    if (isPdf) {
      fileManagerRef.current?.enableToolbarItems(['extract']);
    }

    if (isFolder) {
      fileManagerRef.current?.disableToolbarItems(['rename', 'delete']);
    }
  }
}
```

### Pattern 3: Enable/Disable Based on User Role

```typescript
function initializeFileManager() {
  const userRole = localStorage.getItem('userRole');

  // Default state - disable all destructive operations
  fileManagerRef.current?.disableToolbarItems(['delete', 'rename', 'cut', 'paste']);

  // Enable based on role
  switch (userRole) {
    case 'Administrator':
      fileManagerRef.current?.enableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste', 'upload']);
      break;
    
    case 'Editor':
      fileManagerRef.current?.enableToolbarItems(['rename', 'cut', 'copy', 'paste', 'upload']);
      break;
    
    case 'Viewer':
      fileManagerRef.current?.disableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste', 'upload', 'newfolder']);
      break;
  }
}
```

### Pattern 4: Enable/Disable During Operations

```typescript
function handleBeforeSend(args) {
  // Disable toolbar during AJAX request
  fileManagerRef.current?.disableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste', 'newfolder', 'upload']);
}

function handleSuccess(args) {
  // Re-enable toolbar after successful operation
  fileManagerRef.current?.enableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste', 'newfolder', 'upload']);
}

function handleFailure(args) {
  // Re-enable toolbar after failed operation
  fileManagerRef.current?.enableToolbarItems(['delete', 'rename', 'cut', 'copy', 'paste', 'newfolder', 'upload']);
}
```

### Pattern 5: Enable/Disable Based on Permissions

```typescript
async function loadFilePermissions() {
  try {
    const selectedItems = fileManagerRef.current?.getSelectedFiles();
    
    if (selectedItems?.length === 1) {
      const fileName = selectedItems[0];
      const permissions = await fetchFilePermissions(fileName);

      if (permissions.canDelete) {
        fileManagerRef.current?.enableToolbarItems(['delete']);
      } else {
        fileManagerRef.current?.disableToolbarItems(['delete']);
      }

      if (permissions.canRename) {
        fileManagerRef.current?.enableToolbarItems(['rename']);
      } else {
        fileManagerRef.current?.disableToolbarItems(['rename']);
      }

      if (permissions.canCopy) {
        fileManagerRef.current?.enableToolbarItems(['copy']);
      } else {
        fileManagerRef.current?.disableToolbarItems(['copy']);
      }
    }
  } catch (error) {
    console.error('Error loading permissions:', error);
  }
}

async function fetchFilePermissions(fileName) {
  const response = await fetch(`/api/files/${fileName}/permissions`);
  return response.json();
}
```

## Complete Examples

### Full Implementation with Dynamic Enabling/Disabling

```typescript
import React, { useRef, useEffect } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function AdvancedEnableDisableExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  useEffect(() => {
    // Initialize toolbar state based on user role
    initializeToolbar();
  }, []);

  const initializeToolbar = () => {
    const userRole = localStorage.getItem('userRole') || 'Viewer';
    
    // Start with destructive operations disabled
    fileManagerRef.current?.disableToolbarItems(['delete', 'paste']);

    if (userRole === 'Administrator') {
      fileManagerRef.current?.enableToolbarItems(['delete', 'paste', 'cut', 'rename']);
    } else if (userRole === 'Editor') {
      fileManagerRef.current?.enableToolbarItems(['paste', 'cut', 'rename']);
    }
  };

  const handleFileSelection = (args) => {
    const selectedItems = fileManagerRef.current?.getSelectedFiles();
    const itemCount = selectedItems?.length || 0;

    // Update toolbar based on selection
    if (itemCount === 0) {
      fileManagerRef.current?.disableToolbarItems(['delete', 'cut', 'rename', 'copy']);
    } else if (itemCount === 1) {
      fileManagerRef.current?.enableToolbarItems(['delete', 'cut', 'rename', 'copy']);
    } else {
      // Disable rename for multiple selections
      fileManagerRef.current?.disableToolbarItems(['rename']);
      fileManagerRef.current?.enableToolbarItems(['delete', 'cut', 'copy']);
    }
  };

  const handleBeforeSend = (args) => {
    // Disable all operations during request
    fileManagerRef.current?.disableToolbarItems(['newfolder', 'upload', 'delete', 'cut', 'copy', 'paste', 'rename', 'refresh']);
  };

  const handleSuccess = (args) => {
    // Re-enable operations after success
    const userRole = localStorage.getItem('userRole') || 'Viewer';
    fileManagerRef.current?.enableToolbarItems(['newfolder', 'upload', 'refresh']);
    
    if (userRole !== 'Viewer') {
      fileManagerRef.current?.enableToolbarItems(['delete', 'cut', 'paste', 'rename']);
    }
  };

  const handleFailure = (args) => {
    // Re-enable operations after failure
    fileManagerRef.current?.enableToolbarItems(['newfolder', 'upload', 'delete', 'cut', 'copy', 'paste', 'rename', 'refresh']);
    alert('Operation failed. Please try again.');
  };

  const handleResetToolbar = () => {
    fileManagerRef.current?.enableToolbarItems(['newfolder', 'upload', 'delete', 'cut', 'copy', 'paste', 'rename', 'refresh']);
  };

  return (
    <div className="control-section">
      <div className="button-group" style={{ marginBottom: '20px' }}>
        <ButtonComponent onClick={handleResetToolbar} cssClass='e-outline'>
          Reset Toolbar
        </ButtonComponent>
        <span style={{ marginLeft: '20px', fontSize: '14px' }}>
          User Role: {localStorage.getItem('userRole')}
        </span>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        id="advanced-enable-disable"
        height="500px"
        view="Details"
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        toolbarSettings={{
          items: ['NewFolder', 'Upload', '|', 'Delete', 'Cut', 'Copy', 'Paste', 'Rename', '|', 'Refresh', 'View', 'Details']
        }}
        fileSelect={handleFileSelection}
        beforeSend={handleBeforeSend}
        success={handleSuccess}
        failure={handleFailure}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default AdvancedEnableDisableExample;
```

## Toolbar Item Names (for enable/disable)

| Item Name | Description |
|-----------|-------------|
| `newfolder` | Create new folder |
| `upload` | Upload files |
| `cut` | Cut operation |
| `copy` | Copy operation |
| `paste` | Paste operation |
| `delete` | Delete files/folders |
| `rename` | Rename file/folder |
| `refresh` | Refresh file list |
| `sortby` | Sort options |
| `view` | View mode options |
| `details` | Details view |
| `selection` | Selection options |
| `download` | Download files |

## Best Practices

1. **Always Enable After Operations** - Re-enable items after success or failure
2. **Respect User Permissions** - Check server permissions before enabling items
3. **Provide Feedback** - Show why items are disabled using tooltips
4. **Batch Operations** - Use arrays for multiple items to improve performance
5. **Test Edge Cases** - Test with empty selection, single item, multiple items

## Related Topics

- [Adding Custom Item to Toolbar](adding-custom-item-to-toolbar.md)
- [File Operations](file-operations.md)
- [Customization](customization.md)
- [Getting Started](getting-started.md)
