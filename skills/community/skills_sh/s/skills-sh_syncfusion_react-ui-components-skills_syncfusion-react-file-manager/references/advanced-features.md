# Advanced Features

Master performance optimization, custom file providers, API integration patterns, and advanced implementations.

> **Note**: For detailed guides on specific features, see:
> - **Virtualization**: [virtualization.md](virtualization.md) - Virtual scrolling for 1000+ items
> - **Flat Data**: [flat-data.md](flat-data.md) - Local JSON data structures with events
> - **Multiple Selection**: [multiple-selection.md](multiple-selection.md) - Multi-select, range selection, and checkboxes

## Table of Contents

1. [Custom File Provider](#custom-file-provider)
2. [API Integration](#api-integration)
3. [Performance Optimization](#performance-optimization)
4. [Error Handling](#error-handling)
5. [Complete Example](#complete-example)
6. [Best Practices](#best-practices-checklist)

## Custom File Provider

### Override Default Behavior

Use `beforeSend` to customize AJAX requests:

```tsx
import React from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function CustomProviderFileManager() {
  const handleBeforeSend = (args) => {
    // Intercept request
    console.log('Request:', args.action, args.data);
    
    // Add authorization header
    args.ajaxSettings.headers = {
      ...args.ajaxSettings.headers,
      'Authorization': 'Bearer ' + getAccessToken(),
      'X-Custom-Header': 'CustomValue'
    };
    
    // Validate or modify request
    if (args.action === 'delete') {
      args.data.confirmDelete = true;
    }
  };

  return (
    <FileManagerComponent
      beforeSend={handleBeforeSend}
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

export default CustomProviderFileManager;

function getAccessToken() {
  // Get token from localStorage or auth service
  return localStorage.getItem('access_token');
}
```

## API Integration

### Real-time Backend Integration

```tsx
import React, { useState, useRef } from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function RealTimeAPIIntegration() {
  const fileManagerRef = useRef(null);
  const [status, setStatus] = useState('Ready');

  const handleBeforeSend = (args) => {
    // Add user context
    args.ajaxSettings.data = {
      ...args.ajaxSettings.data,
      userId: getCurrentUserId(),
      tenantId: getCurrentTenantId()
    };

    // Log operations
    console.log(`${args.action}: ${JSON.stringify(args.data)}`);
    setStatus(`${args.action}...`);
  };

  const handleCreated = () => {
    console.log('File Manager initialized');
    setStatus('Ready');
  };

  const handleError = (args) => {
    console.error('Error:', args);
    setStatus(`Error: ${args.error?.message || 'Unknown'}`);
  };

  return (
    <>
      <div>Status: {status}</div>
      <FileManagerComponent
        ref={fileManagerRef}
        beforeSend={handleBeforeSend}
        created={handleCreated}
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
    </>
  );
}

export default RealTimeAPIIntegration;

function getCurrentUserId() {
  return JSON.parse(localStorage.getItem('user'))?.id;
}

function getCurrentTenantId() {
  return JSON.parse(localStorage.getItem('tenant'))?.id;
}
```

### Multi-Tenant Support

```tsx
const handleBeforeSend = (args) => {
  const tenantId = localStorage.getItem('tenantId');
  
  // Include tenant in all requests
  args.ajaxSettings.url = 'url';
  args.ajaxSettings.headers = {
    'X-Tenant-ID': tenantId,
    'Authorization': 'Bearer ' + getAccessToken()
  };
};
```

## Performance Optimization

### Lazy Loading

```tsx
import React, { useState } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function LazyLoadedFileManager() {
  const [path, setPath] = useState('/');
  const [isLoading, setIsLoading] = useState(false);

  const handleBeforeSend = (args) => {
    if (args.action === 'read') {
      setIsLoading(true);
    }
  };

  const handleFileOpen = (args) => {
    // Load file metadata on demand
    console.log('Opening:', args.fileDetails[0]);
    setPath(args.fileDetails[0].filterPath);
  };

  const handleCreated = () => {
    setIsLoading(false);
  };

  return (
    <FileManagerComponent
      beforeSend={handleBeforeSend}
      fileOpen={handleFileOpen}
      created={handleCreated}
      enableVirtualization={true}
      ajaxSettings={{...}}
      height="600px"
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default LazyLoadedFileManager;
```

### Caching Strategy

```tsx
const fileCache = new Map();

const handleBeforeSend = (args) => {
  if (args.action === 'read') {
    const cacheKey = args.data.path;
    
    if (fileCache.has(cacheKey)) {
      console.log('Loading from cache:', cacheKey);
      args.cancel = true;
      // Use cached data
    } else {
      // Cache will be populated on response
    }
  }
};
```

### Batch Operations

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function BatchOperationFileManager() {
  const fileManagerRef = useRef(null);
  const [batchInProgress, setBatchInProgress] = useState(false);

  const performBatchDelete = async (fileIds) => {
    setBatchInProgress(true);
    try {
      const response = await fetch('url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileIds })
      });
      
      if (response.ok) {
        fileManagerRef.current?.refreshFiles();
      }
    } finally {
      setBatchInProgress(false);
    }
  };

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      ajaxSettings={{...}}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default BatchOperationFileManager;
```

## Error Handling

### Graceful Error Handling

```tsx
import React, { useState } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function ErrorHandlingFileManager() {
  const [error, setError] = useState(null);

  const handleBeforeSend = (args) => {
    // Add timeout
    args.ajaxSettings.timeout = 30000; // 30 seconds
  };

  const handleCreated = () => {
    setError(null);
  };

  const handleDestroyed = () => {
    console.log('File Manager destroyed');
  };

  return (
    <>
      {error && (
        <div className="error-message" role="alert">
          <button onClick={() => setError(null)}>×</button>
          {error}
        </div>
      )}
      
      <FileManagerComponent
        beforeSend={handleBeforeSend}
        created={handleCreated}
        destroyed={handleDestroyed}
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
    </>
  );
}

export default ErrorHandlingFileManager;
```

### Retry Logic

```tsx
const handleBeforeSend = (args) => {
  let retryCount = 0;
  const maxRetries = 3;

  const originalUrl = args.ajaxSettings.url;

  args.ajaxSettings.error = (xhr) => {
    if (retryCount < maxRetries && xhr.status >= 500) {
      retryCount++;
      console.log(`Retry attempt ${retryCount}/${maxRetries}`);
      // Retry logic handled by Syncfusion
    } else {
      console.error('Failed after retries:', xhr.statusText);
    }
  };
};
```

## Complete Example

```tsx
import React, { useRef, useState } from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';
import '@syncfusion/ej2-react-filemanager/styles/material.css';

function AdvancedFileManagerExample() {
  const fileManagerRef = useRef(null);
  const [status, setStatus] = useState('Ready');
  const [error, setError] = useState(null);

  const handleBeforeSend = (args) => {
    // Add auth headers
    args.ajaxSettings.headers = {
      'Authorization': 'Bearer ' + getAccessToken(),
      'X-Tenant-ID': getTenantId()
    };

    // Add timeout
    args.ajaxSettings.timeout = 30000;

    // Track operation
    console.log(`Operation: ${args.action}`);
    setStatus(args.action);

    // Log detailed request
    if (args.action === 'read') {
      console.log('Reading files from:', args.data.path);
    }
  };

  const handleCreated = () => {
    setStatus('Ready');
    setError(null);
  };

  const handleFileOpen = (args) => {
    console.log('File opened:', args.fileDetails[0].name);
    setStatus(`Viewing: ${args.fileDetails[0].name}`);
  };

  const handleDelete = (args) => {
    console.log('Files deleted:', args.fileDetails.length);
  };

  return (
    <>
      {error && (
        <div style={{
          padding: '10px',
          marginBottom: '10px',
          background: '#fee',
          border: '1px solid #f00',
          borderRadius: '4px'
        }}>
          <strong>Error:</strong> {error}
          <button onClick={() => setError(null)} style={{ marginLeft: '10px' }}>
            Dismiss
          </button>
        </div>
      )}

      <div style={{ marginBottom: '10px', fontSize: '14px', color: '#666' }}>
        Status: {status}
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        enableVirtualization={true}
        view="Details"
        beforeSend={handleBeforeSend}
        created={handleCreated}
        fileOpen={handleFileOpen}
        delete={handleDelete}
        ajaxSettings={{
          url: "url",
          getImageUrl: "url",
          uploadUrl: "url",
          downloadUrl: "url"
        }}
        height="700px"
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </>
  );
}

export default AdvancedFileManagerExample;

function getAccessToken() {
  return localStorage.getItem('access_token') || '';
}

function getTenantId() {
  return localStorage.getItem('tenant_id') || '';
}
```

## Common Patterns

### Pagination Support

```tsx
const handleBeforeSend = (args) => {
  if (args.action === 'read') {
    // Add pagination to request
    args.data = {
      ...args.data,
      pageSize: 50,
      pageNumber: 1
    };
  }
};
```

### Real-time Sync

```tsx
const syncWithServer = setInterval(async () => {
  try {
    await fileManagerRef.current?.refreshFiles();
  } catch (err) {
    console.error('Sync failed:', err);
  }
}, 5000); // Every 5 seconds
```

### Search Integration

```tsx
const handleSearch = (args) => {
  console.log('Searching for:', args.searchString);
  // Delegate to server-side search
};

<FileManagerComponent
  search={handleSearch}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Best Practices Checklist

- **Return predictable server payloads** for `read` and batch endpoints (include `cwd`, `files`, and per-item `permission`).
- **Validate everything server-side** (paths, sizes, extensions) even when client limits exist.
- **Use per-item permissions** to enable/disable UI actions and enforce checks server-side.
- **Prefer transactional batch endpoints** for large delete/move operations and return per-item results.
- **Enable virtualization** for lists with 1000+ items to reduce memory and improve UX.
- **Use `beforeSend` to attach auth/tenant headers** and to add telemetry/logging context.
- **Sanitize custom templates** and keep `enableHtmlSanitizer` enabled unless you sanitize server-side.
- **Monitor and log** operation latencies, error rates, and upload sizes.

## Compact Custom Provider Example

A minimal `beforeSend` pattern to route requests to tenant-aware endpoints and attach auth:

```tsx
const handleBeforeSend = (args) => {
  const tenantId = localStorage.getItem('tenantId');
  const token = localStorage.getItem('access_token');

  // Route to tenant-scoped API
  args.ajaxSettings.url = 'url';

  // Attach headers
  args.ajaxSettings.headers = {
    ...(args.ajaxSettings.headers || {}),
    'Authorization': `Bearer ${token}`,
    'X-Tenant-ID': tenantId
  };

  // Add contextual metadata for server-side auditing
  args.ajaxSettings.data = {
    ...(args.ajaxSettings.data || {}),
    clientTimestamp: new Date().toISOString(),
    clientVersion: '1.0.0'
  };
};

<FileManagerComponent
  beforeSend={handleBeforeSend}
  ajaxSettings={{
    url: 'url',
    getImageUrl: 'url',
    uploadUrl: 'url',
    downloadUrl: 'url'
  }}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Next Steps

- **Customization:** Styling in [customization.md](customization.md)
- **File Operations:** CRUD operations in [file-operations.md](file-operations.md)
- **Drag-Drop:** Drag-drop features in [drag-and-drop.md](drag-and-drop.md)
