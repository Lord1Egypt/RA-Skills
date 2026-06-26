# Virtualization & Performance in React File Manager

Optimize File Manager performance for handling large datasets (1000+ files) using virtual scrolling to render only visible items.

## Table of Contents

1. [Overview](#overview)
2. [Key Benefits](#key-benefits)
3. [Basic Setup](#basic-setup)
4. [How Virtualization Works](#how-virtualization-works)
5. [Configuration](#configuration)
6. [Complete Example with Large Dataset](#complete-example-with-large-dataset)
7. [Performance Optimization Tips](#performance-optimization-tips)
8. [Limitations & Workarounds](#limitations--workarounds)
9. [Virtualization with Flat Data](#virtualization-with-flat-data)
10. [Monitoring Performance](#monitoring-performance)
11. [Best Practices](#best-practices)
12. [Next Steps](#next-steps)

## Overview

Virtualization dynamically loads files and folders based on viewport visibility:
- **Renders only visible items** in the current view
- **Smooth scrolling** through large file lists
- **Reduced memory usage** and improved performance
- **Maintains scrolling position** on navigation
- **Works with both details and large icons views**

## Key Benefits

| Benefit | Impact |
|---------|--------|
| **Performance** | Handle 10,000+ files without lag |
| **Memory** | ~90% reduction for large datasets |
| **Load Time** | Instant rendering of visible items |
| **Responsiveness** | Smooth UI even with huge file lists |
| **Scalability** | Linear performance regardless of dataset size |

## Basic Setup

### Enable Virtualization

```tsx
import React from 'react';
import { 
  FileManagerComponent, 
  Inject, 
  DetailsView, 
  NavigationPane, 
  Toolbar,
  Virtualization  // Import Virtualization service
} from '@syncfusion/ej2-react-filemanager';

function VirtualizedFileManager() {
  const hostUrl = "url";

  return (
    <FileManagerComponent
      id="filemanager"
      ajaxSettings={{
        url: hostUrl + "api/FileManager/FileOperations",
        getImageUrl: hostUrl + "api/FileManager/GetImage",
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        downloadUrl: hostUrl + 'api/FileManager/Download'
      }}
      enableVirtualization={true}  // Enable virtual scrolling
      view="Details"
      height="500px"
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar, Virtualization]} />
    </FileManagerComponent>
  );
}

export default VirtualizedFileManager;
```

## How Virtualization Works

### 1. Viewport-Based Rendering

Only items visible in the viewport are rendered to the DOM:

```
┌─────────────────────────┐
│  Item 1 (rendered)      │ ← Visible in viewport
│  Item 2 (rendered)      │ ← Visible in viewport
│  Item 3 (rendered)      │ ← Visible in viewport
├─────────────────────────┤
│  Item 4 (NOT rendered)  │ ← Below viewport (virtual)
│  Item 5 (NOT rendered)  │ ← Below viewport (virtual)
│  ... 9990 more ...      │ ← All virtual (not in DOM)
└─────────────────────────┘
```

### 2. Performance Metrics

```tsx
// Without virtualization (1000 files)
// - DOM elements: 1000+
// - Memory: ~2-5 MB
// - Rendering: 100-500ms
// - Scroll: Choppy, laggy

// With virtualization (1000 files)
// - DOM elements: ~20 (visible items)
// - Memory: ~200-400 KB
// - Rendering: <10ms
// - Scroll: Smooth, responsive
```

## Configuration

### Details View with Virtualization

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, Virtualization } from '@syncfusion/ej2-react-filemanager';

function DetailsViewVirtualized() {
  return (
    <FileManagerComponent
      id="filemanager"
      enableVirtualization={true}
      view="Details"
      height="600px"
      detailsViewSettings={{
        columns: [
          {
            field: 'name',
            headerText: 'Name',
            minWidth: 250
          },
          {
            field: '_fm_modified',
            headerText: 'Date Modified',
            type: 'dateTime',
            format: 'MMMM dd, yyyy HH:mm',
            minWidth: 150
          },
          {
            field: 'size',
            headerText: 'Size',
            minWidth: 100,
            template: '<span>${size} bytes</span>'
          }
        ]
      }}
      ajaxSettings={{
        url: "url"
      }}
    >
      <Inject services={[DetailsView, Virtualization]} />
    </FileManagerComponent>
  );
}

export default DetailsViewVirtualized;
```

### Large Icons View with Virtualization

```tsx
<FileManagerComponent
  id="filemanager"
  enableVirtualization={true}
  view="LargeIcons"  // Large icons view
  height="600px"
  showThumbnail={true}
  ajaxSettings={{
    url: "url",
    getImageUrl: "url"
  }}
>
  <Inject services={[Virtualization]} />
</FileManagerComponent>
```

## Complete Example with Large Dataset

```tsx
import React, { useState } from 'react';
import { 
  FileManagerComponent, 
  Inject, 
  DetailsView, 
  NavigationPane, 
  Toolbar,
  Virtualization
} from '@syncfusion/ej2-react-filemanager';

function LargeDatasetFileManager() {
  const hostUrl = "url";
  const [isLoading, setIsLoading] = useState(true);

  const handleBeforeSend = (args: any) => {
    // Add custom headers for authentication
    args.ajaxSettings.beforeSend = function (args: any) {
      args.httpRequest.setRequestHeader('Authorization', 'Bearer token');
    };
  };

  const handleSuccess = (args: any) => {
    console.log('Operation successful:', args.action);
    setIsLoading(false);
  };

  const handleFailure = (args: any) => {
    console.error('Operation failed:', args.error);
    setIsLoading(false);
  };

  return (
    <div>
      {isLoading && <div>Loading...</div>}
      
      <FileManagerComponent
        id="filemanager"
        ajaxSettings={{
          url: hostUrl + "api/Virtualization/FileOperations",
          getImageUrl: hostUrl + "api/Virtualization/GetImage",
          uploadUrl: hostUrl + 'api/Virtualization/Upload',
          downloadUrl: hostUrl + 'api/Virtualization/Download'
        }}
        enableVirtualization={true}
        view="Details"
        height="500px"
        beforeSend={handleBeforeSend}
        success={handleSuccess}
        failure={handleFailure}
        detailsViewSettings={{
          columns: [
            { field: 'name', headerText: 'Name', minWidth: 250 },
            { field: '_fm_modified', headerText: 'Date Modified', minWidth: 150 },
            { field: 'size', headerText: 'Size', minWidth: 100 }
          ]
        }}
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar, Virtualization]} />
      </FileManagerComponent>
    </div>
  );
}

export default LargeDatasetFileManager;
```

## Performance Optimization Tips

### 1. Column Configuration for Details View

```tsx
// Optimize columns for rendering speed
detailsViewSettings={{
  columns: [
    {
      field: 'name',
      headerText: 'Name',
      minWidth: 250,
      maxWidth: 400,
      width: '300px'
    },
    {
      field: '_fm_modified',
      headerText: 'Date Modified',
      minWidth: 120,
      width: '150px'
    },
    {
      field: 'size',
      headerText: 'Size (KB)',
      minWidth: 80,
      width: '100px',
      template: '<span>${size/1024}</span>'  // Pre-calculate in template
    }
  ]
}}
```

### 2. Smart Thumbnail Loading

```tsx
// Load thumbnails only when visible
<FileManagerComponent
  enableVirtualization={true}
  showThumbnail={true}
  view="LargeIcons"
  // Thumbnails load only for visible items
/>
```

### 3. Search Filtering with Virtualization

```tsx
import React, { useState } from 'react';

function SearchableVirtualizedFileManager() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (args: any) => {
    // Virtualization works with search results
    // Only matching items in viewport are rendered
    setSearchTerm(args.searchText);
  };

  return (
    <FileManagerComponent
      enableVirtualization={true}
      search={handleSearch}
      searchSettings={{
        allowSearchOnTyping: true,
        ignoreCase: true
      }}
    />
  );
}
```

### 4. Sort Optimization

```tsx
// Virtualization maintains performance during sorting
<FileManagerComponent
  enableVirtualization={true}
  sortBy="name"           // Sort column
  sortOrder="Ascending"   // Sort direction
/>
```

## Limitations & Workarounds

### 1. Select All Limitation

❌ **Issue**: `Ctrl+A` with virtualization only selects visible items

✅ **Workaround**: Implement server-side bulk selection

```tsx
const handleSelectAll = async () => {
  // Server-side selection for all items
  const response = await fetch('/api/selectAll', { method: 'POST' });
  const allIds = await response.json();
  
  // Apply selections
  fileManagerRef.current?.clearSelection();
  allIds.forEach(id => {
    // Select each item
  });
};
```

### 2. Programmatic Selection Limitation

❌ **Issue**: Selection state not maintained while scrolling

✅ **Workaround**: Use backend persistence

```tsx
const persistSelection = async (selectedIds: string[]) => {
  // Save selection to server
  await fetch('/api/saveSelection', {
    method: 'POST',
    body: JSON.stringify({ ids: selectedIds })
  });
};
```

### 3. Keyboard Navigation

❌ **Issue**: Arrow keys may skip virtual items

✅ **Solution**: Ensure backend returns items in correct order

```tsx
ajaxSettings={{
  url: "url",
  // Backend should sort consistently
}}
```

## Virtualization with Flat Data

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, Virtualization, FileData } from '@syncfusion/ej2-react-filemanager';

function VirtualizedFlatData() {
  // Generate large flat dataset
  const generateLargeDataset = (): FileData[] => {
    const data: FileData[] = [];
    for (let i = 0; i < 10000; i++) {
      data.push({
        id: i.toString(),
        name: `File_${i}`,
        parentId: i < 100 ? '0' : null,
        isFile: Math.random() > 0.3,
        size: Math.floor(Math.random() * 1000000),
        type: i % 2 === 0 ? '.pdf' : '.docx',
        dateCreated: new Date(),
        dateModified: new Date(),
        filterPath: '\\',
        hasChild: false
      });
    }
    return data;
  };

  const fileData = generateLargeDataset();

  return (
    <FileManagerComponent
      id="filemanager"
      fileSystemData={fileData}
      enableVirtualization={true}
      view="Details"
      height="500px"
    >
      <Inject services={[DetailsView, Virtualization]} />
    </FileManagerComponent>
  );
}

export default VirtualizedFlatData;
```

## Monitoring Performance

### Performance Metrics

```tsx
function PerformanceMonitor() {
  const handleCreated = () => {
    console.time('File Manager Render');
  };

  const handleDestroyed = () => {
    console.timeEnd('File Manager Render');
  };

  return (
    <FileManagerComponent
      enableVirtualization={true}
      created={handleCreated}
      destroyed={handleDestroyed}
    />
  );
}
```

### Debug Information

```tsx
// Monitor virtual scroll performance
const handleFileLoad = (args: any) => {
  console.log('File loaded:', args.fileDetails?.name);
  // Tracks files being rendered in the viewport
};

const handleSuccess = (args: any) => {
  const now = performance.now();
  console.log('Operation successful:', args.action);
};

<FileManagerComponent
  fileLoad={handleFileLoad}
  success={handleSuccess}
/>
```

## Best Practices

1. **Always Enable for Large Datasets**: Use virtualization when you anticipate 1000+ items
2. **Optimize Columns**: Reduce number of columns in details view
3. **Lazy Load Images**: Only load thumbnails for visible items
4. **Server-Side Sorting**: Sort on backend before sending to client
5. **Debounce Events**: Batch process multiple events
6. **Monitor Memory**: Use Chrome DevTools to track memory usage
7. **Test Performance**: Benchmark with realistic data sizes

## Common Patterns

### Pattern 1: Folder with Heavy Load Indication

```tsx
<FileManagerComponent
  enableVirtualization={true}
  beforeSend={(args) => {
    if (args.action === 'read') {
      showLoadingSpinner();  // Show for folder reads
    }
  }}
  success={(args) => {
    if (args.action === 'read') {
      hideLoadingSpinner();
    }
  }}
/>
```

### Pattern 2: Adaptive Virtualization

```tsx
const useAdaptiveVirtualization = (itemCount: number) => {
  return itemCount > 500;  // Enable only for large lists
};

const enableVirt = useAdaptiveVirtualization(items.length);

<FileManagerComponent
  enableVirtualization={enableVirt}
/>
```

### Pattern 3: Progressive Loading

```tsx
// Load data in chunks as user scrolls
<FileManagerComponent
  enableVirtualization={true}
  beforeSend={(args) => {
    // Can add pagination parameters
    args.data.pageNumber = currentPage;
    args.data.pageSize = 100;
  }}
/>
```

---

**Next:** Explore [Advanced Features](advanced-features.md) for custom providers and API integration patterns.
