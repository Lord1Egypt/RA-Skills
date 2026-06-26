# Flat Data in React File Manager

Use local flat JSON data structures instead of remote server calls for file system operations. Perfect for in-memory data, local storage, or API integration with event-driven updates.

## Table of Contents

1. [Overview](#overview)
2. [Key Differences](#key-differences)
3. [Core Concepts](#core-concepts)
4. [Basic Implementation](#basic-implementation)
5. [Complete Example with Event Handling](#complete-example-with-event-handling)
6. [Event-Driven Operations](#event-driven-operations)
7. [Permissions Management](#permissions-management)
8. [Performance Optimization](#performance-optimization)
9. [Integration Patterns](#integration-patterns)
10. [Common Patterns](#common-patterns)
11. [Best Practices](#best-practices)

## Overview

The File Manager's `fileSystemData` property enables flat data rendering without backend Ajax calls. This approach is ideal for:
- **In-memory file systems** managed by your application
- **Custom cloud service integration** (Google Drive, OneDrive, S3, etc.)
- **Event-driven file operations** with complete control
- **Offline-first applications** with local data caching
- **Testing and demos** without server setup

## Key Differences

| Aspect | Ajax Mode | Flat Data Mode |
|--------|-----------|----------------|
| **Data Source** | Remote server endpoints | Local JavaScript object |
| **File Operations** | Automatic server calls | Manual event handling |
| **Use Case** | Traditional file server | Custom storage/API |
| **Performance** | Network dependent | Immediate (local) |
| **Control** | Framework-driven | Application-driven |

## Core Concepts

### 1. FileData Interface

Each item requires these properties:

```typescript
interface FileData {
  // Unique identifier for the file/folder
  id: string;
  
  // Display name
  name: string;
  
  // Parent folder ID (null for root)
  parentId: string | null;
  
  // Whether it's a file (true) or folder (false)
  isFile: boolean;
  
  // File size in bytes
  size: number;
  
  // File type (folder, .pdf, .docx, etc.)
  type: string;
  
  // Creation timestamp
  dateCreated: Date;
  
  // Last modified timestamp
  dateModified: Date;
  
  // Path to current item
  filterPath: string;
  
  // Whether folder has children (for optimization)
  hasChild?: boolean;
  
  // Permissions object (optional)
  permission?: Permission;
  
  // Image URL for thumbnails (optional, for images/videos)
  imageUrl?: string;
}
```

### 2. Permission Object

Control what operations are allowed on files/folders:

```typescript
interface Permission {
  copy: boolean;      // Allow copying
  download: boolean;  // Allow downloading
  read: boolean;      // Allow reading/viewing
  write: boolean;     // Allow modifying content
  upload: boolean;    // Allow uploading to folder
  message: string;    // Custom permission message
}
```

## Basic Implementation

### Simple Flat Data Structure

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';
import { FileData } from '@syncfusion/ej2-react-filemanager';

function FlatDataFileManager() {
  const fileData: FileData[] = [
    {
      id: '1',
      name: 'Documents',
      parentId: null,
      isFile: false,
      size: 0,
      type: 'folder',
      dateCreated: new Date('2024-01-15'),
      dateModified: new Date('2024-01-15'),
      filterPath: '',
      hasChild: true
    },
    {
      id: '2',
      name: 'Report.pdf',
      parentId: '1',
      isFile: true,
      size: 256000,
      type: '.pdf',
      dateCreated: new Date('2024-01-10'),
      dateModified: new Date('2024-01-12'),
      filterPath: 'Documents\\',
      hasChild: false
    },
    {
      id: '3',
      name: 'Spreadsheet.xlsx',
      parentId: '1',
      isFile: true,
      size: 102400,
      type: '.xlsx',
      dateCreated: new Date('2024-01-08'),
      dateModified: new Date('2024-01-14'),
      filterPath: 'Documents\\',
      hasChild: false
    },
    {
      id: '4',
      name: 'Images',
      parentId: null,
      isFile: false,
      size: 0,
      type: 'folder',
      dateCreated: new Date('2024-01-01'),
      dateModified: new Date('2024-01-14'),
      filterPath: '',
      hasChild: true
    },
    {
      id: '5',
      name: 'photo.jpg',
      parentId: '4',
      isFile: true,
      size: 1024000,
      type: '.jpg',
      dateCreated: new Date('2024-01-05'),
      dateModified: new Date('2024-01-05'),
      filterPath: 'Images\\',
      hasChild: false,
      imageUrl: 'url'
    }
  ];

  return (
    <FileManagerComponent
      id="filemanager"
      fileSystemData={fileData}
      view="Details"
      height="500px"
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default FlatDataFileManager;
```

## Complete Example with Event Handling

```tsx
import React, { useState } from 'react';
import { 
  FileManagerComponent, 
  Inject, 
  DetailsView, 
  NavigationPane, 
  Toolbar,
  FileData,
  Permission
} from '@syncfusion/ej2-react-filemanager';

function EventDrivenFileManager() {
  const [files, setFiles] = useState<FileData[]>([
    {
      id: '0',
      name: 'Files',
      parentId: null,
      isFile: false,
      size: 0,
      type: 'folder',
      dateCreated: new Date('2023-11-15'),
      dateModified: new Date('2024-01-08'),
      filterPath: '',
      hasChild: true
    },
    {
      id: '1',
      name: 'Documents',
      parentId: '0',
      isFile: false,
      size: 680786,
      type: 'folder',
      dateCreated: new Date('2023-11-15'),
      dateModified: new Date('2024-01-08'),
      filterPath: '\\',
      hasChild: false
    },
    {
      id: '2',
      name: 'Pictures',
      parentId: '0',
      isFile: false,
      size: 228465,
      type: 'folder',
      dateCreated: new Date('2023-11-15'),
      dateModified: new Date('2024-01-08'),
      filterPath: '\\',
      hasChild: true
    }
  ]);

  // Handle folder creation
  const handleFolderCreate = (args: any) => {
    const newId = String(Math.max(...files.map(f => parseInt(f.id) || 0)) + 1);
    const parentId = args.path === '/' ? null : args.path;
    
    const newFolder: FileData = {
      id: newId,
      name: args.folderName,
      parentId: parentId,
      isFile: false,
      size: 0,
      type: 'folder',
      dateCreated: new Date(),
      dateModified: new Date(),
      filterPath: args.path,
      hasChild: false
    };
    
    setFiles([...files, newFolder]);
    args.cancel = false;
  };

  // Handle file deletion
  const handleDelete = (args: any) => {
    const idsToDelete = args.fileDetails.map((f: FileData) => f.id);
    setFiles(files.filter(f => !idsToDelete.includes(f.id)));
    args.cancel = false;
  };

  // Handle rename
  const handleRename = (args: any) => {
    setFiles(files.map(f => 
      f.id === args.fileDetails.id 
        ? { ...f, name: args.newName } 
        : f
    ));
    args.cancel = false;
  };

  // Handle search
  const handleSearch = (args: any) => {
    const searchTerm = args.searchText.toLowerCase();
    const filtered = files.filter(f => 
      f.name.toLowerCase().includes(searchTerm)
    );
    // Update file manager data with filtered results
    args.cancel = false;
  };

  return (
    <FileManagerComponent
      id="filemanager"
      fileSystemData={files}
      view="Details"
      height="500px"
      toolbarSettings={{
        items: ['NewFolder', 'Cut', 'Copy', 'Paste', 'Delete', 'Refresh', 'Details']
      }}
      contextMenuSettings={{
        file: ['Open', '|', 'Cut', 'Copy', 'Delete', 'Rename', '|', 'Details'],
        folder: ['Open', '|', 'Cut', 'Copy', 'Paste', 'Delete', 'Rename'],
        layout: ['Refresh', '|', 'NewFolder', 'Paste']
      }}
      folderCreate={handleFolderCreate}
      delete={handleDelete}
      rename={handleRename}
      search={handleSearch}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default EventDrivenFileManager;
```

## Event-Driven Operations

### Key Events for Flat Data

| Event | Use Case | Example |
|-------|----------|---------|
| `beforeFolderCreate` | Validate before creating | Check name length, permissions |
| `folderCreate` | Handle folder creation | Add to state, backend sync |
| `beforeDelete` | Confirm deletion | Show confirmation dialog |
| `delete` | Clean up after deletion | Remove from state, cleanup refs |
| `beforeRename` | Validate new name | Check for duplicates |
| `rename` | Update file name | Update state |
| `beforeMove` | Validate move operation | Check target permissions |
| `move` | Handle move/copy | Update parent ID, sync |
| `search` | Filter display | Update visible files |

### Before Operations (Cancelable)

```tsx
<FileManagerComponent
  // Prevent creation of folders starting with underscore
  beforeFolderCreate={(args) => {
    if (args.folderName.startsWith('_')) {
      args.cancel = true;
      alert('Folder names cannot start with underscore');
    }
  }}
  
  // Confirm deletion
  beforeDelete={(args) => {
    const shouldDelete = window.confirm(
      `Delete ${args.fileDetails.length} item(s)?`
    );
    args.cancel = !shouldDelete;
  }}
  
  // Validate rename
  beforeRename={(args) => {
    if (args.newName.length === 0) {
      args.cancel = true;
      alert('Name cannot be empty');
    }
  }}
/>
```

### After Operations (Handle State)

```tsx
const handleFolderCreate = (args: any) => {
  const newFolder: FileData = {
    id: generateId(),
    name: args.folderName,
    parentId: getCurrentParentId(),
    isFile: false,
    size: 0,
    type: 'folder',
    dateCreated: new Date(),
    dateModified: new Date(),
    filterPath: args.path,
    hasChild: false
  };
  
  setFiles(prev => [...prev, newFolder]);
  
  // Optional: Sync to backend
  syncToBackend('create', newFolder);
};

const handleDelete = (args: any) => {
  const deletedIds = args.fileDetails.map((f: FileData) => f.id);
  
  setFiles(prev => 
    prev.filter(f => !deletedIds.includes(f.id))
  );
  
  // Optional: Sync to backend
  syncToBackend('delete', deletedIds);
};
```

## Permissions Management

### Define Permissions per Item

```tsx
const readOnlyPermission: Permission = {
  copy: true,
  download: true,
  write: false,    // Cannot modify
  read: true,
  upload: false,   // Cannot upload
  message: 'This folder is read-only'
};

const restrictedPermission: Permission = {
  copy: false,     // Cannot copy
  download: false, // Cannot download
  write: true,
  read: true,
  upload: true,
  message: 'Restricted access'
};

const files: FileData[] = [
  {
    id: '1',
    name: 'Shared Folder',
    parentId: null,
    isFile: false,
    size: 0,
    type: 'folder',
    dateCreated: new Date(),
    dateModified: new Date(),
    filterPath: '',
    hasChild: true,
    permission: readOnlyPermission  // Read-only
  },
  {
    id: '2',
    name: 'System Folder',
    parentId: null,
    isFile: false,
    size: 0,
    type: 'folder',
    dateCreated: new Date(),
    dateModified: new Date(),
    filterPath: '',
    hasChild: false,
    permission: restrictedPermission  // Restricted
  }
];

<FileManagerComponent
  fileSystemData={files}
  // File Manager respects permission settings
/>
```

## Performance Optimization

### 1. Large Dataset Handling

```tsx
// For large datasets, enable virtualization
<FileManagerComponent
  fileSystemData={largeFileList}
  enableVirtualization={true}
  view="Details"
  detailsViewSettings={{
    columns: [
      { field: 'name', headerText: 'Name', width: '250px' },
      { field: 'dateModified', headerText: 'Date', width: '150px' },
      { field: 'size', headerText: 'Size', width: '100px' }
    ]
  }}
/>
```

### 2. State Management Best Practices

```tsx
import React, { useCallback } from 'react';

function OptimizedFileManager() {
  const [files, setFiles] = useState<FileData[]>(initialFiles);

  // Memoize callbacks to prevent unnecessary re-renders
  const handleFolderCreate = useCallback((args: any) => {
    setFiles(prev => [
      ...prev,
      {
        id: generateId(),
        name: args.folderName,
        parentId: args.parentId,
        isFile: false,
        size: 0,
        type: 'folder',
        dateCreated: new Date(),
        dateModified: new Date(),
        filterPath: args.path,
        hasChild: false
      }
    ]);
  }, []);

  const handleDelete = useCallback((args: any) => {
    const ids = new Set(args.fileDetails.map((f: FileData) => f.id));
    setFiles(prev => prev.filter(f => !ids.has(f.id)));
  }, []);

  return (
    <FileManagerComponent
      fileSystemData={files}
      folderCreate={handleFolderCreate}
      delete={handleDelete}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}
```

## Integration Patterns

### Backend Sync Pattern

```tsx
// Sync local changes to backend
const handleFileOperation = async (operation: string, data: any) => {
  try {
    const response = await fetch('/api/filemanager/operations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ operation, data })
    });
    
    if (!response.ok) throw new Error('Sync failed');
    return await response.json();
  } catch (error) {
    console.error('Backend sync error:', error);
    // Revert local changes
  }
};

// In event handlers:
folderCreate={(args) => {
  handleFileOperation('create', {
    name: args.folderName,
    parentId: args.parentId
  });
}}
```

### Cloud Service Integration

```tsx
// Example: Integrate with cloud API
const integrateCloudService = async (fileData: FileData[]) => {
  // Transform to cloud format
  const cloudItems = fileData.map(f => ({
    id: f.id,
    name: f.name,
    parent_id: f.parentId,
    is_file: f.isFile,
    size: f.size
  }));
  
  // Send to cloud service
  const response = await cloudAPI.sync(cloudItems);
  return response;
};
```

## Common Patterns

### Pattern 1: Read-Only Mode
```tsx
<FileManagerComponent
  fileSystemData={files}
  toolbarSettings={{ visible: false }}
  contextMenuSettings={{ visible: false }}
  allowDragAndDrop={false}
/>
```

### Pattern 2: Upload Only
```tsx
<FileManagerComponent
  fileSystemData={files}
  toolbarSettings={{
    items: ['Upload', 'Refresh']
  }}
  contextMenuSettings={{ visible: false }}
/>
```

### Pattern 3: Filtered View
```tsx
const [filter, setFilter] = useState('');

const filteredFiles = files.filter(f => 
  f.name.toLowerCase().includes(filter.toLowerCase())
);

<FileManagerComponent
  fileSystemData={filteredFiles}
  // Update on filter change
/>
```

## Best Practices

1. **Always Set hasChild**: Helps File Manager optimize rendering
2. **Use Consistent IDs**: Make IDs unique and immutable
3. **Handle Errors**: Wrap operations in try-catch
4. **Debounce Updates**: Batch state updates for performance
5. **Maintain Hierarchy**: Ensure parentId references exist
6. **Optimize Dates**: Use ISO format for consistency
7. **Test Edge Cases**: Empty folders, special characters, permissions

---

**Next:** Learn about [Virtual Scrolling](advanced-features.md#virtual-scrolling) for handling large datasets efficiently.
