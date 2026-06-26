# Access Control in React File Manager

The React File Manager component allows you to define granular access permissions for folders and files using access rules and role-based permissions. This is essential for multi-user systems where different users should have different access levels to files and folders.

## Table of Contents

1. [Understanding Access Rules](#understanding-access-rules)
2. [Permission Types](#permission-types)
3. [Implementing Role-Based Access](#implementing-role-based-access)
4. [Access Rules for Different User Roles](#access-rules-for-different-user-roles)
5. [Complete Implementation Example](#complete-implementation-example)

## Understanding Access Rules

Access rules define what operations users in specific roles can perform on files and folders. Each rule specifies:

- **Path**: The file or folder path to which the rule applies
- **Role**: The user role for which the rule applies
- **IsFile**: Whether the rule applies to files (true) or folders (false)
- **Permissions**: Individual permission flags (Read, Write, Copy, Download, Upload, etc.)

### Access Rule Properties

| Property | Applicable to Files | Applicable to Folders | Description |
|----------|-------------------|----------------------|-------------|
| `copy` | ✓ | ✓ | Allows copying files or folders |
| `read` | ✓ | ✓ | Allows reading/viewing files or folders |
| `write` | ✓ | ✓ | Allows modifying files or folders |
| `writeContents` | ✗ | ✓ | Allows modifying folder contents |
| `download` | ✓ | ✓ | Allows downloading files or folders |
| `upload` | ✗ | ✓ | Allows uploading files to folders |

## Permission Types

### Allow vs Deny

```typescript
// Permission values
enum Permission {
  Allow = 'Allow',    // Allows the operation
  Deny = 'Deny'       // Denies the operation
}
```

## Implementing Role-Based Access

### Step 1: Backend Configuration (Server-Side)

First, define access rules on your backend file provider:

```typescript
// Backend Access Rules Example (C# / ASP.NET Core)

public class FileManagerController : Controller
{
    private FileAccessController fileAccessController;

    public FileManagerController()
    {
        // Initialize with access rules
        this.fileAccessController = new FileAccessController();
        this.fileAccessController.SetRules(GetAccessRules());
    }

    private List<AccessRule> GetAccessRules()
    {
        return new List<AccessRule>
        {
            // Administrator - Full access to all files
            new AccessRule 
            { 
                Path = "/*.*", 
                Role = "Administrator", 
                Read = Permission.Allow, 
                Write = Permission.Allow, 
                Copy = Permission.Allow, 
                Download = Permission.Allow, 
                IsFile = true 
            },
            
            // Administrator - Full access to all folders
            new AccessRule 
            { 
                Path = "*", 
                Role = "Administrator", 
                Read = Permission.Allow, 
                Write = Permission.Allow, 
                Copy = Permission.Allow, 
                WriteContents = Permission.Allow, 
                Upload = Permission.Allow, 
                Download = Permission.Deny, 
                IsFile = false 
            },
            
            // Default User - Restricted access
            new AccessRule 
            { 
                Path = "/*.*", 
                Role = "Default User", 
                Read = Permission.Deny, 
                Write = Permission.Deny, 
                Copy = Permission.Deny, 
                Download = Permission.Deny, 
                IsFile = true 
            },
            
            // Document Manager - Specific folder access
            new AccessRule 
            { 
                Path = "/Documents", 
                Role = "Document Manager", 
                Read = Permission.Allow, 
                Write = Permission.Allow, 
                Copy = Permission.Allow, 
                WriteContents = Permission.Allow, 
                Upload = Permission.Allow, 
                Download = Permission.Allow, 
                IsFile = false 
            },
            
            // Document Manager - Deny access to specific file
            new AccessRule 
            { 
                Path = "/Documents/Confidential.docx", 
                Role = "Document Manager", 
                Read = Permission.Deny, 
                Write = Permission.Deny, 
                Copy = Permission.Deny, 
                Download = Permission.Deny, 
                IsFile = true 
            }
        };
    }

    [Route("FileOperations")]
    public object FileOperations([FromBody] FileManagerDirectoryContent args)
    {
        // Access control is enforced through FileAccessController
        return this.fileAccessController.ToCamelCase(this.fileAccessController.GetFiles(args.Path, true));
    }

    [Route("Upload")]
    public IActionResult Upload(string path, long size, IList<IFormFile> uploadFiles, string action)
    {
        // Access rules prevent unauthorized uploads
        return this.fileAccessController.Upload(path, uploadFiles);
    }
}
```

### Step 2: Frontend Implementation

React File Manager automatically respects backend access rules. Configure the component to communicate with your access-controlled endpoints:

```typescript
import React from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function AccessControlExample() {
  const hostUrl = "url";

  return (
    <div className="control-section">
      <FileManagerComponent
        id="file-manager"
        height="500px"
        view="Details"
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default AccessControlExample;
```

## Access Rules for Different User Roles

### Administrator Access

Full access to all files and folders:

```typescript
// Administrator - Full access to files
new AccessRule 
{ 
  Path = "/*.*", 
  Role = "Administrator", 
  Read = Permission.Allow, 
  Write = Permission.Allow, 
  Copy = Permission.Allow, 
  Download = Permission.Allow, 
  IsFile = true 
},

// Administrator - Full access to folders
new AccessRule 
{ 
  Path = "*", 
  Role = "Administrator", 
  Read = Permission.Allow, 
  Write = Permission.Allow, 
  Copy = Permission.Allow, 
  WriteContents = Permission.Allow, 
  Upload = Permission.Allow, 
  Download = Permission.Allow, 
  IsFile = false 
}
```

### Document Manager Access

Limited access to specific folders:

```typescript
// Document Manager - Read-only access to Documents folder
new AccessRule 
{ 
  Path = "/Documents", 
  Role = "Document Manager", 
  Read = Permission.Allow, 
  Write = Permission.Deny, 
  Copy = Permission.Allow, 
  WriteContents = Permission.Deny, 
  Upload = Permission.Deny, 
  Download = Permission.Allow, 
  IsFile = false 
},

// Document Manager - No access to Archives folder
new AccessRule 
{ 
  Path = "/Archives", 
  Role = "Document Manager", 
  Read = Permission.Deny, 
  Write = Permission.Deny, 
  Copy = Permission.Deny, 
  WriteContents = Permission.Deny, 
  Upload = Permission.Deny, 
  Download = Permission.Deny, 
  IsFile = false 
}
```

### Guest User Access

Minimal read-only access:

```typescript
// Guest - Read-only access to shared files
new AccessRule 
{ 
  Path = "/Shared/*.*", 
  Role = "Guest", 
  Read = Permission.Allow, 
  Write = Permission.Deny, 
  Copy = Permission.Deny, 
  Download = Permission.Allow, 
  IsFile = true 
},

// Guest - No folder modification access
new AccessRule 
{ 
  Path = "*", 
  Role = "Guest", 
  Read = Permission.Allow, 
  Write = Permission.Deny, 
  Copy = Permission.Deny, 
  WriteContents = Permission.Deny, 
  Upload = Permission.Deny, 
  Download = Permission.Deny, 
  IsFile = false 
}
```

## Complete Implementation Example

### Frontend Component with Access Control

```typescript
import React, { useRef, useEffect } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar, ContextMenu } from '@syncfusion/ej2-react-filemanager';

function AccessControlledFileManager() {
  const fileManagerRef = useRef(null);
  const userRole = localStorage.getItem('userRole') || 'Guest';
  const hostUrl = "url";

  useEffect(() => {
    // You could validate access on component load
    console.log(`File Manager loaded for role: ${userRole}`);
  }, [userRole]);

  const handleFileOpen = (args) => {
    console.log(`Opening file: ${args.fileDetails.name}`);
    // Access control is enforced server-side, but you can add client-side checks
  };

  const handleBeforeSend = (args) => {
    // Optionally add user role to request headers
    if (args.ajaxSettings) {
      args.ajaxSettings.beforeSend = function(requestArgs) {
        requestArgs.httpRequest.setRequestHeader('X-User-Role', userRole);
      };
    }
  };

  const handleDeleteFile = (args) => {
    // Server will validate delete permission based on access rules
    console.log(`Delete attempted on: ${args.fileDetails?.name}`);
  };

  return (
    <div className="control-section">
      <div className="header">
        <h2>File Manager - {userRole} Access</h2>
        <p>Your actions are restricted based on access control rules</p>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        id="access-controlled-file-manager"
        height="500px"
        view="Details"
        allowDragAndDrop={true}
        allowMultiSelection={true}
        showFileExtension={true}
        showHiddenItems={false}
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        toolbarSettings={{
          items: ['NewFolder', 'Upload', 'Delete', 'Cut', 'Copy', 'Paste', 'Rename', 'SortBy', 'Refresh', 'Selection', 'View', 'Details']
        }}
        contextMenuSettings={{
          file: ['Open', '|', 'Cut', 'Copy', 'Delete', 'Rename', '|', 'Download', 'Details'],
          folder: ['Open', '|', 'Cut', 'Copy', 'Delete', 'Rename', '|', 'Details'],
          layout: ['SortBy', 'View', 'Refresh', '|', 'NewFolder', 'Upload', '|', 'Details', '|', 'SelectAll']
        }}
        navigationPaneSettings={{
          width: '200px',
          visible: true
        }}
        detailsViewSettings={{
          columns: [
            { field: 'name', headerText: 'File Name', width: '150px' },
            { field: 'dateModified', headerText: 'Date Modified', width: '150px' },
            { field: 'size', headerText: 'Size', width: '100px' }
          ]
        }}
        beforeSend={handleBeforeSend}
        fileOpen={handleFileOpen}
        beforeDelete={handleDeleteFile}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar, ContextMenu]} />
      </FileManagerComponent>
    </div>
  );
}

export default AccessControlledFileManager;
```

### Testing Access Control

Test different user roles to verify access restrictions:

```typescript
// Test script to verify access control

// Simulate Admin access
localStorage.setItem('userRole', 'Administrator');
// Should have full access to all operations

// Simulate Document Manager access
localStorage.setItem('userRole', 'Document Manager');
// Should have limited access to Documents folder only

// Simulate Guest access
localStorage.setItem('userRole', 'Guest');
// Should have read-only access to Shared folder only
```

## Best Practices for Access Control

1. **Always validate on server-side** - Never rely solely on client-side validation
2. **Use specific paths** - Define rules for specific folders/files, not just wildcards
3. **Principle of least privilege** - Grant only necessary permissions
4. **Test access rules** - Verify restrictions with different user roles
5. **Log access attempts** - Track file access for audit purposes
6. **Use HTTPS** - Encrypt communication with the server
7. **Implement authentication** - Ensure users are properly authenticated before access control

## Common Scenarios

### Read-Only Access to Public Folder

```typescript
new AccessRule 
{ 
  Path = "/Public/*.*", 
  Role = "Everyone", 
  Read = Permission.Allow, 
  Write = Permission.Deny, 
  Copy = Permission.Deny, 
  Download = Permission.Allow, 
  IsFile = true 
}
```

### Upload-Only Access to Submissions Folder

```typescript
new AccessRule 
{ 
  Path = "/Submissions", 
  Role = "Student", 
  Read = Permission.Allow, 
  Write = Permission.Allow, 
  WriteContents = Permission.Allow, 
  Upload = Permission.Allow, 
  Copy = Permission.Deny, 
  Download = Permission.Deny, 
  IsFile = false 
}
```

### Deny Access to Specific File Type

```typescript
new AccessRule 
{ 
  Path = "/*.exe", 
  Role = "User", 
  Read = Permission.Deny, 
  Write = Permission.Deny, 
  Download = Permission.Deny, 
  IsFile = true 
}
```

## Related Topics

- [Pass Custom Value to Server](pass-custom-value-to-server.md)
- [Customization](customization.md)
- [File Operations](file-operations.md)
- [Getting Started](getting-started.md)
