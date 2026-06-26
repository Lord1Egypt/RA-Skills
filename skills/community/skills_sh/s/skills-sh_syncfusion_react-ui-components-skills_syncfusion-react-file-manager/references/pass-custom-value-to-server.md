# Pass Custom Value to Server in React File Manager

The React File Manager component allows you to pass custom values to the server using HTTP headers, query parameters, or request bodies. This is essential for authentication, user identification, logging, and role-based file operations.

## Table of Contents

1. [Setting Custom Headers with setRequestHeader](#setting-custom-headers-with-setrequestheader)
2. [File Operations Custom Values](#file-operations-custom-values)
3. [Download Operations](#download-operations)
4. [Image Loading](#image-loading)
5. [Complete Implementation Example](#complete-implementation-example)

## Setting Custom Headers with setRequestHeader

### Using beforeSend Event with setRequestHeader

The `beforeSend` event allows you to add custom HTTP headers to all file operation requests (Read, Create, Delete, Rename, Move, Copy, Search, Upload).

#### Basic Authorization Header

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function CustomHeaderExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const handleBeforeSend = (args) => {
    // Add custom headers to all AJAX requests
    if (args.ajaxSettings) {
      args.ajaxSettings.beforeSend = function(requestArgs) {
        // Set Authorization header
        requestArgs.httpRequest.setRequestHeader('Authorization', 'Bearer your-token-here');
        
        // Set custom user identification
        requestArgs.httpRequest.setRequestHeader('X-User-Id', 'user123');
        
        // Set custom role header
        requestArgs.httpRequest.setRequestHeader('X-User-Role', 'Administrator');
        
        // Set tenant identification for multi-tenant systems
        requestArgs.httpRequest.setRequestHeader('X-Tenant-Id', 'tenant001');
      };
    }
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
      beforeSend={handleBeforeSend}
    >
      <Inject services={[NavigationPane, DetailsView, Toolbar]} />
    </FileManagerComponent>
  );
}

export default CustomHeaderExample;
```

### Server-Side Header Access

```typescript
// Backend: Access custom headers in C# / ASP.NET Core

[Route("FileOperations")]
public object FileOperations([FromBody] FileManagerDirectoryContent args)
{
    // Access custom headers from the request
    var authHeader = HttpContext.Request.Headers["Authorization"];
    var userId = HttpContext.Request.Headers["X-User-Id"];
    var userRole = HttpContext.Request.Headers["X-User-Role"];
    var tenantId = HttpContext.Request.Headers["X-Tenant-Id"];

    // Validate authorization
    if (string.IsNullOrEmpty(authHeader))
    {
        return BadRequest("Authorization header is required");
    }

    // Perform user-specific operations
    try
    {
        // Log the operation with user context
        Logger.LogInfo($"User {userId} performing {args.Action} operation in tenant {tenantId}");

        // Perform file operation with access control based on user role
        return this.operation.ToCamelCase(this.operation.GetFiles(args.Path, true));
    }
    catch (Exception ex)
    {
        Logger.LogError($"Error for user {userId}: {ex.Message}");
        return StatusCode(500, ex.Message);
    }
}

[Route("Upload")]
public IActionResult Upload(string path, long size, IList<IFormFile> uploadFiles, string action)
{
    var userId = HttpContext.Request.Headers["X-User-Id"];
    var userRole = HttpContext.Request.Headers["X-User-Role"];

    // Verify upload permissions for the user
    if (!userRole.Equals("Administrator") && !userRole.Equals("Editor"))
    {
        return Forbid();
    }

    try
    {
        Logger.LogInfo($"User {userId} uploading {uploadFiles.Count} files");
        return this.operation.Upload(path, uploadFiles);
    }
    catch (Exception ex)
    {
        Logger.LogError($"Upload error for user {userId}: {ex.Message}");
        return StatusCode(500, ex.Message);
    }
}
```

## File Operations Custom Values

### Pattern 1: User Authentication

```typescript
function onBeforeSend(args) {
    if (args.ajaxSettings) {
        args.ajaxSettings.beforeSend = function(requestArgs) {
            // Retrieve token from localStorage
            const token = localStorage.getItem('authToken');
            requestArgs.httpRequest.setRequestHeader('Authorization', `Bearer ${token}`);
            requestArgs.httpRequest.setRequestHeader('Content-Type', 'application/json');
        };
    }
}

return (
  <FileManagerComponent
    beforeSend={onBeforeSend.bind(this)}
    // ... other properties
  />
);
```

### Pattern 2: User Identification

```typescript
function onBeforeSend(args) {
    if (args.ajaxSettings) {
        args.ajaxSettings.beforeSend = function(requestArgs) {
            // Add user information
            const userId = localStorage.getItem('userId');
            const userName = localStorage.getItem('userName');
            
            requestArgs.httpRequest.setRequestHeader('X-User-Id', userId);
            requestArgs.httpRequest.setRequestHeader('X-User-Name', userName);
            requestArgs.httpRequest.setRequestHeader('X-Timestamp', new Date().toISOString());
        };
    }
}
```

### Pattern 3: Tracking File Operations

```typescript
function onBeforeSend(args) {
    if (args.ajaxSettings) {
        args.ajaxSettings.beforeSend = function(requestArgs) {
            // Track operation type
            const action = args.action; // Read, Create, Delete, Rename, Move, Copy, Search, Upload
            
            requestArgs.httpRequest.setRequestHeader('X-Operation', action);
            requestArgs.httpRequest.setRequestHeader('X-Request-Id', generateRequestId());
            requestArgs.httpRequest.setRequestHeader('X-Client-Version', '2.1.0');
        };
    }
}

function generateRequestId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
```

### Pattern 4: Department-Based Access

```typescript
function onBeforeSend(args) {
    if (args.ajaxSettings) {
        args.ajaxSettings.beforeSend = function(requestArgs) {
            const department = localStorage.getItem('department');
            const costCenter = localStorage.getItem('costCenter');
            
            requestArgs.httpRequest.setRequestHeader('X-Department', department);
            requestArgs.httpRequest.setRequestHeader('X-Cost-Center', costCenter);
            
            // Add custom metadata
            requestArgs.httpRequest.setRequestHeader('X-Metadata', JSON.stringify({
                source: 'web-app',
                platform: 'react',
                timestamp: Date.now()
            }));
        };
    }
}
```

## Download Operations

### Using beforeDownload Event

For download operations, use the `beforeDownload` event and set `useFormPost` to false to use fetch requests:

```typescript
function onBeforeDownload(args) {
    // Use fetch instead of form post
    args.useFormPost = false;
    
    if (args.ajaxSettings) {
        args.ajaxSettings.beforeSend = function(requestArgs) {
            // Add authorization to fetch request
            const token = localStorage.getItem('authToken');
            requestArgs.fetchRequest.headers.append('Authorization', `Bearer ${token}`);
            requestArgs.fetchRequest.headers.append('X-User-Id', localStorage.getItem('userId'));
            requestArgs.fetchRequest.headers.append('X-Download-Timestamp', new Date().toISOString());
        };
    }
}

return (
  <FileManagerComponent
    beforeDownload={onBeforeDownload.bind(this)}
    // ... other properties
  />
);
```

### Server-Side Download Handler

```typescript
[Route("Download")]
public object Download([FromBody] FileManagerDirectoryContent args)
{
    var authHeader = HttpContext.Request.Headers["Authorization"];
    var userId = HttpContext.Request.Headers["X-User-Id"];
    var downloadTime = HttpContext.Request.Headers["X-Download-Timestamp"];

    // Verify authorization
    if (string.IsNullOrEmpty(authHeader))
    {
        return BadRequest("Authorization required for download");
    }

    try
    {
        Logger.LogInfo($"Download initiated by user {userId} at {downloadTime}");
        return this.operation.Download(args.Path, args.Names);
    }
    catch (Exception ex)
    {
        Logger.LogError($"Download error: {ex.Message}");
        return StatusCode(500, ex.Message);
    }
}
```

## Image Loading

### Using beforeImageLoad Event

For image loading operations, use the `beforeImageLoad` event:

```typescript
function onBeforeImageLoad(args) {
    // Use fetch instead of direct URL
    args.useImageAsUrl = false;
    
    if (args.ajaxSettings) {
        args.ajaxSettings.beforeSend = function(requestArgs) {
            const token = localStorage.getItem('authToken');
            requestArgs.fetchRequest.headers.append('Authorization', `Bearer ${token}`);
            requestArgs.fetchRequest.headers.append('X-User-Id', localStorage.getItem('userId'));
        };
    }
}

return (
  <FileManagerComponent
    beforeImageLoad={onBeforeImageLoad.bind(this)}
    // ... other properties
  />
);
```

### Server-Side Image Handler

```typescript
[Route("GetImage")]
public object GetImage([FromBody] FileManagerDirectoryContent args)
{
    var authHeader = HttpContext.Request.Headers["Authorization"];
    var userId = HttpContext.Request.Headers["X-User-Id"];

    if (string.IsNullOrEmpty(authHeader))
    {
        return BadRequest("Authorization required");
    }

    try
    {
        return this.operation.GetImage(args.Path, args.Id, false, null, null);
    }
    catch (Exception ex)
    {
        return StatusCode(500, ex.Message);
    }
}
```

## Complete Implementation Example

### Full React Component with Custom Headers

```typescript
import React, { useRef, useEffect, useState } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function AdvancedCustomHeaderExample() {
  const fileManagerRef = useRef(null);
  const [userContext, setUserContext] = useState(null);
  const hostUrl = "url";

  useEffect(() => {
    // Initialize user context
    const context = {
      userId: localStorage.getItem('userId'),
      userName: localStorage.getItem('userName'),
      authToken: localStorage.getItem('authToken'),
      department: localStorage.getItem('department'),
      role: localStorage.getItem('role')
    };
    setUserContext(context);
  }, []);

  // Handle all file operation requests
  const handleBeforeSend = (args) => {
    if (args.ajaxSettings && userContext) {
      args.ajaxSettings.beforeSend = function(requestArgs) {
        // Core authentication
        requestArgs.httpRequest.setRequestHeader(
          'Authorization', 
          `Bearer ${userContext.authToken}`
        );

        // User identification
        requestArgs.httpRequest.setRequestHeader('X-User-Id', userContext.userId);
        requestArgs.httpRequest.setRequestHeader('X-User-Name', userContext.userName);
        requestArgs.httpRequest.setRequestHeader('X-User-Role', userContext.role);
        requestArgs.httpRequest.setRequestHeader('X-Department', userContext.department);

        // Request tracking
        requestArgs.httpRequest.setRequestHeader('X-Request-Id', `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
        requestArgs.httpRequest.setRequestHeader('X-Timestamp', new Date().toISOString());
        requestArgs.httpRequest.setRequestHeader('X-Action', args.action || 'unknown');

        // Custom metadata
        requestArgs.httpRequest.setRequestHeader('X-Client', 'react-filemanager/1.0');
      };
    }
  };

  // Handle download requests
  const handleBeforeDownload = (args) => {
    args.useFormPost = false;
    
    if (args.ajaxSettings && userContext) {
      args.ajaxSettings.beforeSend = function(requestArgs) {
        requestArgs.fetchRequest.headers.append(
          'Authorization', 
          `Bearer ${userContext.authToken}`
        );
        requestArgs.fetchRequest.headers.append('X-User-Id', userContext.userId);
        requestArgs.fetchRequest.headers.append('X-Download-Time', new Date().toISOString());
      };
    }
  };

  // Handle image load requests
  const handleBeforeImageLoad = (args) => {
    args.useImageAsUrl = false;
    
    if (args.ajaxSettings && userContext) {
      args.ajaxSettings.beforeSend = function(requestArgs) {
        requestArgs.fetchRequest.headers.append(
          'Authorization', 
          `Bearer ${userContext.authToken}`
        );
        requestArgs.fetchRequest.headers.append('X-User-Id', userContext.userId);
      };
    }
  };

  const handleSuccess = (args) => {
    console.log(`Operation completed successfully: ${args.action}`);
  };

  const handleFailure = (args) => {
    console.error(`Operation failed: ${args.error}`);
    // Handle specific errors
    if (args.error && args.error.includes('Unauthorized')) {
      // Token expired, redirect to login
      window.location.href = '/login';
    }
  };

  if (!userContext) {
    return <div>Loading...</div>;
  }

  return (
    <div className="control-section">
      <div className="user-info">
        <h3>Logged in as: {userContext.userName} ({userContext.role})</h3>
        <p>Department: {userContext.department}</p>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        id="advanced-file-manager"
        height="500px"
        view="Details"
        allowDragAndDrop={true}
        allowMultiSelection={true}
        showFileExtension={true}
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        toolbarSettings={{
          items: ['NewFolder', 'Upload', 'Delete', 'Cut', 'Copy', 'Paste', 'Rename', 'SortBy', 'Refresh', 'View', 'Details']
        }}
        beforeSend={handleBeforeSend}
        beforeDownload={handleBeforeDownload}
        beforeImageLoad={handleBeforeImageLoad}
        success={handleSuccess}
        failure={handleFailure}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default AdvancedCustomHeaderExample;
```

### Server Response Handling

```typescript
// Backend: C# / ASP.NET Core Example

public class FileManagerController : Controller
{
    [Route("FileOperations")]
    public object FileOperations([FromBody] FileManagerDirectoryContent args)
    {
        try
        {
            // Extract custom headers
            var authHeader = HttpContext.Request.Headers["Authorization"];
            var userId = HttpContext.Request.Headers["X-User-Id"];
            var requestId = HttpContext.Request.Headers["X-Request-Id"];
            var action = HttpContext.Request.Headers["X-Action"];

            // Validate authorization
            if (!ValidateToken(authHeader))
            {
                return Unauthorized(new { message = "Invalid authorization token" });
            }

            // Perform operation with audit logging
            AuditLog.Log(new AuditEntry
            {
                UserId = userId,
                Action = action,
                Path = args.Path,
                RequestId = requestId,
                Timestamp = DateTime.UtcNow
            });

            // Return results
            return this.operation.ToCamelCase(this.operation.GetFiles(args.Path, true));
        }
        catch (UnauthorizedAccessException)
        {
            return Forbid();
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = ex.Message });
        }
    }

    private bool ValidateToken(string authHeader)
    {
        // Token validation logic
        if (string.IsNullOrEmpty(authHeader)) return false;
        
        try
        {
            var token = authHeader.Replace("Bearer ", "");
            return ValidateJWT(token);
        }
        catch
        {
            return false;
        }
    }
}
```

## Security Best Practices

1. **Use HTTPS** - Always encrypt communication between client and server
2. **Validate Headers** - Never trust client-provided headers for security decisions
3. **Token Refresh** - Implement token expiration and refresh mechanisms
4. **Sanitize Input** - Validate all server-side data before processing
5. **Log Access** - Maintain audit logs of all file operations
6. **Rate Limiting** - Implement rate limiting to prevent abuse
7. **CORS** - Configure CORS properly for secure cross-origin requests

## Related Topics

- [Access Control](access-control.md)
- [File Operations](file-operations.md)
- [Getting Started](getting-started.md)
- [Customization](customization.md)
