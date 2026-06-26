# File Operations (CRUD)

Master file system operations: create folders, upload files, delete items, rename, and manage multiple selections using proper event handling.

## Table of Contents

1. [API Methods Quick Reference](#api-methods-quick-reference)
2. [File Selection](#file-selection)
3. [File Opening](#file-opening)
4. [Upload Operations](#upload-operations)
5. [Download Operations](#download-operations)
6. [Delete Operations](#delete-operations)
7. [Rename Operations](#rename-operations)
8. [Create Folder](#create-folder)

## API Methods Quick Reference

The File Manager component provides methods to programmatically perform operations:

```tsx
const fileManagerRef = useRef(null);

// Selection operations
fileManagerRef.current.selectAll();                          // Select all items
fileManagerRef.current.clearSelection();                     // Deselect all items
const selected = fileManagerRef.current.getSelectedFiles(); // Get selected files

// File operations
fileManagerRef.current.createFolder('NewFolder');            // Create folder
fileManagerRef.current.renameFile(fileId, 'NewName');        // Rename file/folder
fileManagerRef.current.deleteFiles([id1, id2]);              // Delete files
fileManagerRef.current.openFile(fileId);                     // Open/navigate to file
fileManagerRef.current.downloadFiles([id1, id2]);            // Download files
fileManagerRef.current.uploadFiles();                        // Open upload dialog

// Navigation & Refresh
fileManagerRef.current.refreshFiles();                       // Refresh current folder
fileManagerRef.current.refreshLayout();                      // Refresh UI layout
fileManagerRef.current.traverseBackward();                   // Go to parent directory
fileManagerRef.current.filterFiles({ key: 'search' });       // Apply custom filter

// Toolbar & Menu Control
fileManagerRef.current.disableToolbarItems(['Cut', 'Copy']);
fileManagerRef.current.enableToolbarItems(['Paste']);
fileManagerRef.current.disableMenuItems(['Delete']);
fileManagerRef.current.enableMenuItems(['Rename']);

// Dialog control
fileManagerRef.current.closeDialog();                        // Close any open dialog
```

## File Selection

### Handling File Selection

Track which files are selected using the `fileSelect` and `fileSelection` events:

```tsx
import React, { useState } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function FileSelection() {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileSelect = (args) => {
    setSelectedFiles(args.fileDetails);
    console.log('Selected:', args.fileDetails);
  };

  const handleFileSelection = (args) => {
    console.log('Selection changed:', args);
  };

  return (
    <FileManagerComponent
      fileSelect={handleFileSelect}
      fileSelection={handleFileSelection}
      ajaxSettings={{...}}
      allowMultiSelection={true}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}
```

**Event Details:**
- `fileSelect` - Triggered when file/folder is selected
- `fileSelection` - Triggered when selection changes
- `args.fileDetails` - Array of selected file objects
- `args.fileDetails[0].name` - File name
- `args.fileDetails[0].size` - File size in bytes
- `args.fileDetails[0].isFile` - True if file, false if folder

## File Opening

### Handle File Open

When user double-clicks or presses Enter on a file/folder:

```tsx
const handleFileOpen = (args) => {
  console.log('Opened:', args.fileDetails);
  console.log('Action:', args.action);
};

<FileManagerComponent
  fileOpen={handleFileOpen}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Upload Operations

### File Upload Events

Handle uploads with validation and completion tracking:

```tsx
import React from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function FileUpload() {
  const handleUploadListCreate = (args) => {
    console.log('Upload UI created:', args);
  };

  const handleBeforeSend = (args) => {
    console.log('Before sending upload request');
    // Add custom headers, validation, etc.
  };

  return (
    <FileManagerComponent
      uploadListCreate={handleUploadListCreate}
      beforeSend={handleBeforeSend}
      ajaxSettings={{
        url: "url",
        uploadUrl: "url",
        getImageUrl: "url",
        downloadUrl: "url"
      }}
      allowDragAndDrop={true}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}
```

### Upload Settings

Configure upload behavior:

```tsx
<FileManagerComponent
  uploadSettings={{
    autoUpload: true,
    minFileSize: 0,
    maxFileSize: 30000000,  // 30 MB
    allowedExtensions: '',
    autoClose: false,
    directoryUpload: false,
    sequentialUpload: false
  }}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Upload Settings Properties:**
- `autoUpload` - Start upload immediately (default: true)
- `maxFileSize` - Maximum file size in bytes
- `allowedExtensions` - Comma-separated allowed file extensions
- `autoClose` - Auto close dialog after upload (default: false)
- `directoryUpload` - Allow directory uploads (default: false)
- `sequentialUpload` - Upload files one by one (default: false)

### Backend Upload Handler

```csharp
[HttpPost]
public IActionResult Upload(string path)
{
  try
  {
    var httpRequest = Request.Form;
    foreach (var file in httpRequest.Files)
    {
      var fileName = ContentDispositionHeaderValue.Parse(file.ContentDisposition).FileName.Trim('"');
      var fullPath = Path.Combine(path, fileName);
      
      using (var stream = new FileStream(fullPath, FileMode.Create))
      {
        file.CopyTo(stream);
      }
    }
    return Ok(new { name = "Upload" });
  }
  catch (Exception e)
  {
    return BadRequest(new { error = e.Message });
  }
}
```

### Validation Example

```tsx
const handleBeforeSend = (args) => {
  const maxFileSize = 10 * 1024 * 1024; // 10 MB
  const allowedExtensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.png'];

  if (args.fileData) {
    const files = Array.isArray(args.fileData) ? args.fileData : [args.fileData];
    
    files.forEach(file => {
      // Check file size
      if (file.size > maxFileSize) {
        console.error(`File ${file.name} exceeds 10 MB limit`);
        args.cancel = true;
      }

      // Check file extension
      const ext = '.' + file.name.split('.').pop().toLowerCase();
      if (!allowedExtensions.includes(ext)) {
        console.error(`File type ${ext} not allowed`);
        args.cancel = true;
      }
    });
  }
};
```

## Download Operations

### Download Files

Trigger downloads using toolbar or programmatically:

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function FileDownload() {
  const fileManagerRef = useRef(null);

  const handleBeforeDownload = (args) => {
    console.log('Downloading:', args.fileDetails);
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      beforeDownload={handleBeforeDownload}
      ajaxSettings={{
        url: "url",
        downloadUrl: "url",
        getImageUrl: "url",
        uploadUrl: "url"
      }}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default FileDownload;
```

### Backend Download Handler

```csharp
[HttpGet]
public IActionResult Download(string path)
{
  try
  {
    var fileInfo = new FileInfo(path);
    var stream = System.IO.File.OpenRead(path);
    
    return File(stream, "application/octet-stream", fileInfo.Name);
  }
  catch (Exception e)
  {
    return NotFound(new { error = e.Message });
  }
}
```

## Delete Operations

### Delete Files and Folders

Handle deletions with the `beforeDelete` and `delete` events:

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function FileDelete() {
  const fileManagerRef = useRef(null);

  const handleBeforeDelete = (args) => {
    console.log('Deleting:', args.fileDetails);
    // Show confirmation dialog if needed
  };

  const handleDelete = (args) => {
    console.log('Delete completed:', args);
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      beforeDelete={handleBeforeDelete}
      delete={handleDelete}
      ajaxSettings={{
        url: "url",
        getImageUrl: "url",
        uploadUrl: "url",
        downloadUrl: "url"
      }}
      allowMultiSelection={true}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default FileDelete;
```

### Backend Delete Handler

```csharp
[HttpPost]
public IActionResult FileOperations([FromBody] FileManagerDirectoryContent args)
{
  if (args.Action == "delete")
  {
    foreach (var file in args.Names)
    {
      var fullPath = Path.Combine(args.Path, file);
      
      if (System.IO.File.Exists(fullPath))
      {
        System.IO.File.Delete(fullPath);
      }
      else if (Directory.Exists(fullPath))
      {
        Directory.Delete(fullPath, true);
      }
    }
    return Ok(new { success = true });
  }
}
```

## Rename Operations

### Rename Files and Folders

Use the `beforeRename` and `rename` events:

```tsx
import React from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function FileRename() {
  const handleBeforeRename = (args) => {
    console.log('Old name:', args.oldName);
    console.log('New name:', args.newName);
    
    // Validate new name
    if (args.newName.includes('/') || args.newName.includes('\\')) {
      args.cancel = true;
      console.error('Invalid characters in file name');
    }
  };

  const handleRename = (args) => {
    console.log('Rename completed');
  };

  return (
    <FileManagerComponent
      beforeRename={handleBeforeRename}
      rename={handleRename}
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

export default FileRename;
```

### Backend Rename Handler

```csharp
[HttpPost]
public IActionResult FileOperations([FromBody] FileManagerDirectoryContent args)
{
  if (args.Action == "rename")
  {
    var oldPath = Path.Combine(args.Path, args.Name);
    var newPath = Path.Combine(args.Path, args.NewName);
    
    if (System.IO.File.Exists(oldPath))
    {
      System.IO.File.Move(oldPath, newPath);
    }
    else if (Directory.Exists(oldPath))
    {
      Directory.Move(oldPath, newPath);
    }
    
    return Ok(new { success = true });
  }
}
```

## Create Folder

### Create New Folder

Create folders using toolbar or context menu:

```tsx
<FileManagerComponent
  ajaxSettings={{
    url: "url",
    getImageUrl: "url",
    uploadUrl: "url",
    downloadUrl: "url"
  }}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

The toolbar "New Folder" button triggers a dialog for folder creation.

### Backend Create Folder Handler

```csharp
[HttpPost]
public IActionResult FileOperations([FromBody] FileManagerDirectoryContent args)
{
  if (args.Action == "create")
  {
    string newPath = Path.Combine(args.Path, args.Name);
    Directory.CreateDirectory(newPath);
    return Ok(new FileManagerResponse { Success = true });
  }
}
```

## Multi-Selection

### Enable Multiple Selection

```tsx
<FileManagerComponent
  allowMultiSelection={true}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

### Getting Selected Items

```tsx
const handleFileSelection = (args) => {
  const selectedCount = args.fileDetails.length;
  const selectedSize = args.fileDetails.reduce((sum, f) => sum + f.size, 0);
  
  console.log(`Selected ${selectedCount} items, ${selectedSize} bytes total`);
};

<FileManagerComponent
  fileSelection={handleFileSelection}
  allowMultiSelection={true}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Selection Keyboard Shortcuts:**
- Click - Select single file
- Ctrl+Click - Toggle selection
- Shift+Click - Select range
- Ctrl+A - Select all

## API Methods for File Operations

Use these methods to programmatically control file operations:

```tsx
import React, { useRef } from 'react';

function FileOperationsAPI() {
  const fileManagerRef = useRef(null);

  const selectAll = () => {
    fileManagerRef.current.selectAll();
  };

  const clearSelection = () => {
    fileManagerRef.current.clearSelection();
  };

  const getSelectedFiles = () => {
    const selected = fileManagerRef.current.getSelectedFiles();
    console.log('Selected files:', selected);
  };

  const deleteFiles = () => {
    fileManagerRef.current.deleteFiles();
  };

  const downloadFiles = () => {
    fileManagerRef.current.downloadFiles();
  };

  const refreshFiles = () => {
    fileManagerRef.current.refreshFiles();
  };

  const createFolder = () => {
    fileManagerRef.current.createFolder('NewFolder');
  };

  const renameFile = () => {
    const selected = fileManagerRef.current.getSelectedFiles();
    if (selected.length > 0) {
      fileManagerRef.current.renameFile(selected[0].id, 'NewName');
    }
  };

  return (
    <div>
      <button onClick={selectAll}>Select All</button>
      <button onClick={clearSelection}>Clear Selection</button>
      <button onClick={getSelectedFiles}>Get Selected</button>
      <button onClick={deleteFiles}>Delete</button>
      <button onClick={downloadFiles}>Download</button>
      <button onClick={refreshFiles}>Refresh</button>
      <button onClick={createFolder}>New Folder</button>
      <button onClick={renameFile}>Rename</button>

      <FileManagerComponent
        ref={fileManagerRef}
        ajaxSettings={{...}}
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}
```

**Available Methods:**
- `selectAll()` - Select all files
- `clearSelection()` - Clear selection
- `getSelectedFiles()` - Get selected file list
- `deleteFiles()` - Delete selected files
- `downloadFiles()` - Download selected files
- `refreshFiles()` - Refresh file list
- `createFolder(name)` - Create new folder
- `renameFile(id, name)` - Rename file
- `uploadFiles()` - Open upload dialog

## Best Practices & Server Guidelines

### Server Response Conventions
- Always return a predictable JSON payload for `read` operations:

```json
{
  "cwd": { "name": "Documents", "path": "/Documents", "dateModified": "2024-01-01T12:00:00Z" },
  "files": [
    { "name": "file.txt", "size": 1024, "isFile": true, "dateModified": "2024-01-01T12:00:00Z", "permission": { "read": true, "write": true } },
    { "name": "subfolder", "size": 0, "isFile": false, "dateModified": "2024-01-01T12:00:00Z", "permission": { "read": true, "write": false } }
  ],
  "error": null
}
```

- On errors return an HTTP error status and a JSON body describing the error:

```json
{ "error": { "code": 403, "message": "Access denied" } }
```

### Security & Validation
- Never trust client-supplied paths or names: normalize and validate on the server.
- Validate file extensions and sizes server-side even when client-side limits exist.
- Apply authentication and authorization to every file operation endpoint.
- Use `enableHtmlSanitizer={true}` (default) to avoid rendering unsafe HTML in templates.
- For uploads, scan files for viruses if your environment requires it.

### Permissions Model
- Include a `permission` object with each file in the `read` response.
- Prevent unauthorized operations by checking permission in `before*` events and on the server.

Client-side example (disable UI actions using permissions):

```tsx
const handleFileLoad = (args) => {
  args.files.forEach(file => {
    if (file.permission && !file.permission.write) {
      // e.g. disable rename/delete in the context menu
    }
  });
};

<FileManagerComponent
  fileLoad={handleFileLoad}
  ajaxSettings={{...}}
/>
```

### Batch & Transactional Operations
- For large batch deletes or moves, implement a server-side batch endpoint that accepts arrays of identifiers and performs the operation transactionally where possible.
- Return per-item results so the client can show partial success/failure and refresh the UI accordingly.

Batch response example:

```json
{
  "results": [
    { "name": "file1.txt", "status": "success" },
    { "name": "file2.txt", "status": "error", "error": "File locked" }
  ]
}
```

Client handling pattern:
- Call your batch endpoint (e.g., `/api/FileManager/BatchDelete`).
- On success, call `fileManagerRef.current.refreshFiles()` to update the view.
- Surface per-item errors to the user and provide retry options.

### Error Handling & Retries
- Use `failure` event to surface friendly messages and logging.
- Add retry logic for transient HTTP 5xx errors (careful with non-idempotent actions).

Example:

```tsx
const handleFailure = (args) => {
  console.error('Operation failed:', args.error);
  alert(`Operation failed: ${args.error?.message || 'Unknown error'}`);
};

<FileManagerComponent
  failure={handleFailure}
  ajaxSettings={{...}}
/>
```

### Testing & Debugging
- Unit test server endpoints independently (validate `action` handling for read/create/delete/etc.).
- Use Postman or curl to simulate File Manager `action` payloads.
- Add integration tests that start the frontend and a test backend to cover flows: upload → read → download → delete.
- For end-to-end testing, use Playwright or Cypress to script user flows (create folder, upload small file, rename, delete).

### Accessibility Notes
- File Manager supports keyboard navigation; test with keyboard-only flows (Arrow keys, Enter, Delete, Ctrl/Shift modifiers).
- Ensure ARIA labels for any custom templates you introduce.

### Observability & Metrics
- Log file operations with contextual metadata (userId, path, action, timestamp).
- Monitor upload sizes, error rates, and average response times for `read` endpoints.

## Next Steps

- **Views:** Learn about details view and large icons view in [views-and-navigation.md](views-and-navigation.md)
- **Drag-Drop:** Implement drag-drop operations in [drag-and-drop.md](drag-and-drop.md)
- **Customization:** Style and customize components in [customization.md](customization.md)
