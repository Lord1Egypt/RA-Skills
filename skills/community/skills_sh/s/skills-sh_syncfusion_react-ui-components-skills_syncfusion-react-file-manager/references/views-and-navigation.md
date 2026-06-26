# Views and Navigation

Explore different view modes, navigation options, and how to customize the user interface for browsing file systems.

## Table of Contents

1. [Details View](#details-view)
2. [Large Icons View](#large-icons-view)
3. [View Switching](#view-switching)
4. [Navigation Pane](#navigation-pane)
5. [Toolbar Customization](#toolbar-customization)
6. [Complete Layout Example](#complete-layout-example)
7. [Common Patterns](#common-patterns)
8. [Next Steps](#next-steps)

## Details View

### Basic Details View

Shows files in a sortable table format with columns:

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function DetailsViewExample() {
  return (
    <FileManagerComponent
      view="Details"
      ajaxSettings={{
        url: "url",
        getImageUrl: "url",
        uploadUrl: "url",
        downloadUrl: "url"
      }}
      detailsViewSettings={{
        columns: [
          { field: 'name', headerText: 'Name', width: '30%' },
          { field: 'dateModified', headerText: 'Date Modified', width: '30%' },
          { field: 'type', headerText: 'Type', width: '15%' },
          { field: 'size', headerText: 'Size', width: '25%' }
        ]
      }}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default DetailsViewExample;
```

**Default Columns:**
- **name** - File or folder name with icon
- **dateModified** - Last modification date (formatted as _fm_modified in API)
- **type** - File type or "Folder"
- **size** - File size (folders show as "-")

### Sorting in Details View

Click column headers to sort:

```tsx
// Default sort by Name, ascending
<FileManagerComponent
  sortBy="name"
  sortOrder="Ascending"
  view="Details"
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Sort Options:**
- `sortBy` - Field to sort: "name", "dateModified", "size"
- `sortOrder` - Direction: "Ascending" or "Descending"

### Customizing Columns

```tsx
<FileManagerComponent
  view="Details"
  detailsViewSettings={{
    columns: [
      { 
        field: 'name', 
        headerText: 'File Name', 
        width: '40%',
        template: '${name}'
      },
      { 
        field: 'size', 
        headerText: 'File Size (KB)', 
        width: '20%',
        template: '${size > 0 ? (size / 1024).toFixed(2) : "-"}'
      },
      { 
        field: '_fm_modified', 
        headerText: 'Modified', 
        width: '30%'
      }
    ]
  }}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Large Icons View

### Basic Large Icons View

Displays files as thumbnails in a grid:

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function LargeIconsViewExample() {
  return (
    <FileManagerComponent
      view="LargeIcons"
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

export default LargeIconsViewExample;
```

**Features:**
- Image previews for image/video files
- Folder icons for directories
- File type icons for documents
- Larger touch targets for mobile

### Thumbnail Configuration

```tsx
<FileManagerComponent
  view="LargeIcons"
  showThumbnail={true}
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

**Backend GetImage Handler:**

```csharp
[HttpGet]
public IActionResult GetImage(string path)
{
  try
  {
    var imageFormats = new[] { ".jpg", ".jpeg", ".png", ".gif", ".bmp" };
    var videoFormats = new[] { ".mp4", ".avi", ".mov" };
    var ext = Path.GetExtension(path).ToLower();

    if (imageFormats.Contains(ext))
    {
      // Return actual image
      return PhysicalFile(path, "image/*");
    }
    else if (videoFormats.Contains(ext))
    {
      // Generate video thumbnail
      return GenerateVideoThumbnail(path);
    }
    else
    {
      // Return default file type icon
      return GetDefaultIcon(ext);
    }
  }
  catch
  {
    return NotFound();
  }
}
```

## View Switching

### Allow Users to Switch Views

```tsx
import React, { useState } from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function ViewSwitcher() {
  const [view, setView] = useState('Details');

  return (
    <div>
      <div className="view-switcher">
        <button onClick={() => setView('Details')}>Details View</button>
        <button onClick={() => setView('LargeIcons')}>Thumbnail View</button>
      </div>

      <FileManagerComponent
        view={view}
        ajaxSettings={{...}}
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}
```

## Navigation Pane

### Navigation Pane (Sidebar)

Shows folder tree for quick navigation:

```tsx
<FileManagerComponent
  navigationPaneSettings={{
    visible: true,
    minWidth: '240px',
    maxWidth: '650px'
  }}
  ajaxSettings={{...}}
>
  <Inject services={[NavigationPane, DetailsView, Toolbar]} />
</FileManagerComponent>
```

**Navigation Pane Settings:**
- `visible` - Show/hide pane (default: true)
- `minWidth` - Minimum width (default: 240px)
- `maxWidth` - Maximum width (default: 650px)

### Customizing Navigation Pane

```tsx
<FileManagerComponent
  navigationPaneSettings={{
    visible: true,
    minWidth: '240px',
    maxWidth: '400px'
  }}
  ajaxSettings={{
    url: "url",
    getImageUrl: "url",
    uploadUrl: "url",
    downloadUrl: "url"
  }}
>
  <Inject services={[NavigationPane, DetailsView, Toolbar]} />
</FileManagerComponent>
```

## Toolbar Customization

### Default Toolbar

```tsx
<FileManagerComponent
  toolbarSettings={{
    items: ['NewFolder', 'Upload', 'Delete', 'Download', 'Rename', 'Refresh'],
    visible: true
  }}
  ajaxSettings={{...}}
>
  <Inject services={[Toolbar, DetailsView, NavigationPane]} />
</FileManagerComponent>
```

**Available Toolbar Items:**
- NewFolder - Create new folder
- Upload - Upload files
- Delete - Delete selected files
- Download - Download selected files
- Rename - Rename selected file
- Refresh - Refresh current folder
- View - Toggle view mode
- Details - Show/hide columns

### Context Menu Customization

```tsx
<FileManagerComponent
  contextMenuSettings={{
    file: ['Open', 'Cut', 'Copy', 'Delete', 'Rename', 'Details'],
    folder: ['Open', 'Cut', 'Copy', 'Paste', 'Delete', 'Rename', 'Details'],
    layout: ['SortBy', 'View', 'Refresh', 'Paste', 'NewFolder', 'Upload', 'Details', 'SelectAll'],
    visible: true
  }}
  menuClick={(args) => {
    if (args.item.text === 'Copy') {
      console.log('Copy clicked');
    }
  }}
  ajaxSettings={{...}}
>
  <Inject services={[Toolbar, DetailsView, NavigationPane]} />
</FileManagerComponent>
```

**Context Menu Settings:**
- `file` - Items shown on file right-click
- `folder` - Items shown on folder right-click
- `layout` - Items shown on empty space right-click
- `visible` - Show/hide context menu (default: true)

**Available Menu Items:**
- Open, Cut, Copy, Paste, Delete, Rename, Details
- SortBy, View, Refresh, Upload, NewFolder, SelectAll

## Complete Layout Example

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function FullFeaturedFileManager() {
  const handleToolbarClick = (args) => {
    console.log('Toolbar item clicked:', args.item.text);
  };

  const handleMenuClick = (args) => {
    console.log('Context menu clicked:', args.item.text);
  };

  return (
    <FileManagerComponent
      id="file-manager"
      view="Details"
      path="/root"
      height="600px"
      width="100%"
      sortBy="name"
      sortOrder="Ascending"
      allowDragAndDrop={true}
      allowMultiSelection={true}
      showFileExtension={true}
      showHiddenItems={false}
      navigationPaneSettings={{
        visible: true,
        minWidth: '240px',
        maxWidth: '400px'
      }}
      toolbarSettings={{
        items: ['NewFolder', 'Upload', 'Delete', 'Download', 'Rename', 'Refresh'],
        visible: true
      }}
      contextMenuSettings={{
        file: ['Open', 'Cut', 'Copy', 'Delete', 'Rename', 'Details'],
        folder: ['Open', 'Cut', 'Copy', 'Paste', 'Delete', 'Rename', 'Details'],
        layout: ['SortBy', 'View', 'Refresh', 'Paste', 'NewFolder', 'Upload', 'Details']
      }}
      detailsViewSettings={{
        columns: [
          { field: 'name', headerText: 'Name', width: '40%' },
          { field: '_fm_modified', headerText: 'Modified', width: '30%' },
          { field: 'type', headerText: 'Type', width: '15%' },
          { field: 'size', headerText: 'Size', width: '15%' }
        ]
      }}
      toolbarClick={handleToolbarClick}
      menuClick={handleMenuClick}
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

export default FullFeaturedFileManager;
```

## Common Patterns

### Responsive Layout

```tsx
<FileManagerComponent
  view={isMobile ? 'LargeIcons' : 'Details'}
  navigationPaneSettings={{ visible: !isMobile }}
  height={isMobile ? '500px' : '600px'}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

### Minimal Toolbar

```tsx
<FileManagerComponent
  toolbarSettings={{
    items: ['Upload', 'Download', 'Refresh']
  }}
  contextMenuSettings={{
    visible: false
  }}
  navigationPaneSettings={{
    visible: false
  }}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, Toolbar]} />
</FileManagerComponent>
```

## Next Steps

- **Drag-and-Drop:** Implement drag-drop operations in [drag-and-drop.md](drag-and-drop.md)
- **File Operations:** Learn CRUD operations in [file-operations.md](file-operations.md)
- **Customization:** Style and customize components in [customization.md](customization.md)
