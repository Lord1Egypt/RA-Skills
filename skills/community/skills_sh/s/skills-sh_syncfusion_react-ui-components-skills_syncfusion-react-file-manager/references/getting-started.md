# Getting Started with File Manager

Learn how to install, configure, and initialize the Syncfusion React File Manager component in your application.

## Table of Contents

1. [Installation](#installation)
2. [CSS Theme Setup](#css-theme-setup)
3. [Basic Component Setup](#basic-component-setup)
4. [AJAX Configuration](#ajax-configuration)
5. [View Types](#view-types)
6. [Enabling Features](#enabling-features)
7. [Common Configuration](#common-configuration)
8. [Complete API Configuration Reference](#complete-api-configuration-reference)

## Installation

### Dependencies

The File Manager component requires the following packages:

```bash
npm install @syncfusion/ej2-react-filemanager @syncfusion/ej2-base @syncfusion/ej2-grids @syncfusion/ej2-buttons @syncfusion/ej2-layouts @syncfusion/ej2-navigations
```

**Dependency Tree:**
- `@syncfusion/ej2-react-filemanager` - Main File Manager component
- `@syncfusion/ej2-base` - Base utilities and CSS framework
- `@syncfusion/ej2-grids` - Grid component (used for details view)
- `@syncfusion/ej2-buttons` - Button components
- `@syncfusion/ej2-layouts` - Layout components (splitter)
- `@syncfusion/ej2-navigations` - Navigation components (toolbar, context menu)

### Project Setup

**Using Vite (Recommended):**
```bash
npm create vite@latest my-file-manager -- --template react-ts
cd my-file-manager
npm install @syncfusion/ej2-react-filemanager
npm run dev
```

**Using Create React App:**
```bash
npx create-react-app my-file-manager
cd my-file-manager
npm install @syncfusion/ej2-react-filemanager
npm start
```

## CSS Theme Setup

Import the required CSS files for your chosen theme. Material theme is shown below:

```css
/* App.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../node_modules/@syncfusion/ej2-icons/styles/material.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material.css';
@import '../node_modules/@syncfusion/ej2-layouts/styles/material.css';
@import '../node_modules/@syncfusion/ej2-grids/styles/material.css';
@import '../node_modules/@syncfusion/ej2-react-filemanager/styles/material.css';
```

**Available Themes:**
- Material (default): `material.css`
- Bootstrap: `bootstrap.css`
- Bootstrap 4: `bootstrap4.css`
- Fabric: `fabric.css`
- Tailwind: `tailwind.css`

## Basic Implementation

### Minimal Setup

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';
import './App.css';

function App() {
  const hostUrl = "url";

  return (
    <FileManagerComponent
      id="file"
      ajaxSettings={{
        url: hostUrl + "api/FileManager/FileOperations",
        getImageUrl: hostUrl + "api/FileManager/GetImage",
        uploadUrl: hostUrl + "api/FileManager/Upload",
        downloadUrl: hostUrl + "api/FileManager/Download"
      }}
      height="375px"
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default App;
```

**Explanation:**
- `ajaxSettings` - Endpoints for backend file operations
- `height` - Component height (CSS value)
- `<Inject>` - Enables required features (details view, sidebar, toolbar)

### Understanding AjaxSettings

The `ajaxSettings` object configures communication with your backend:

```tsx
ajaxSettings={{
  url: "url",           // Main operations
  getImageUrl: "url",        // Fetch thumbnails
  uploadUrl: "url",            // Upload files
  downloadUrl: "url"         // Download files
}}
```

**Backend Expectations:**
- `url` endpoint receives POST requests with `action` (read, create, delete, rename, upload)
- `getImageUrl` endpoint receives GET requests for image thumbnails with `path` parameter
- `uploadUrl` endpoint receives multipart form data for file uploads
- `downloadUrl` endpoint initiates file downloads

### Setting Initial Path

Load a specific folder on component initialization:

```tsx
<FileManagerComponent
  path="/Documents"
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## View Types

### Details View (Default)

Shows files in a sorted list with columns:

```tsx
<FileManagerComponent
  view="Details"
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Features:**
- Sortable columns (Name, Date Modified, Type, Size)
- Click column header to sort ascending/descending
- Hover for tooltips with full paths
- Details view settings for column customization

### Large Icons View

Shows thumbnail previews in a grid layout:

```tsx
<FileManagerComponent
  view="LargeIcons"
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Features:**
- Image thumbnails for image/video files
- Folder icons for directories
- Larger click targets for touch devices
- Thumbnail generation via `getImageUrl` endpoint

## Enabling Features

### Enable/Disable Features

```tsx
<FileManagerComponent
  allowDragAndDrop={true}
  allowMultiSelection={true}
  showFileExtension={true}
  showHiddenItems={false}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Feature Properties:**
- `allowDragAndDrop` - Enable drag-drop (default: false)
- `allowMultiSelection` - Multiple file selection (default: true)
- `showFileExtension` - Show file extensions (default: true)
- `showHiddenItems` - Show hidden/system files (default: false)

### Required Services

```tsx
<Inject services={[
  DetailsView,       // Enables details view option
  NavigationPane,    // Enables sidebar with folder tree
  Toolbar            // Enables toolbar with action buttons
]} />
```

**Optional Services:**
- `DetailsView` - Details view mode
- `NavigationPane` - Navigation pane (tree view)
- `Toolbar` - Toolbar with action buttons

## Common Configuration

### Production Setup

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function FileManager() {
  const fileManagerRef = useRef(null);
  const apiBaseUrl = process.env.REACT_APP_API_URL || "url";

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      id="file-manager"
      path="/root"
      view="Details"
      sortBy="name"
      allowDragAndDrop={true}
      allowMultiSelection={true}
      showFileExtension={true}
      showHiddenItems={false}
      height="600px"
      ajaxSettings={{
        url: `${apiBaseUrl}/api/FileManager/FileOperations`,
        getImageUrl: `${apiBaseUrl}/api/FileManager/GetImage`,
        uploadUrl: `${apiBaseUrl}/api/FileManager/Upload`,
        downloadUrl: `${apiBaseUrl}/api/FileManager/Download`
      }}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default FileManager;
```

## Complete API Configuration Reference

### All Configuration Options

```tsx
<FileManagerComponent
  // Core Setup
  id="file-manager"
  path="/Documents"
  view="Details"
  
  // Dimensions
  height="500px"
  width="100%"
  
  // Display Options
  showFileExtension={true}
  showHiddenItems={false}
  showThumbnail={true}
  showItemCheckBoxes={true}
  
  // Sorting
  sortBy="name"                         // "name" | "dateModified" | "size"
  sortOrder="Ascending"                 // "Ascending" | "Descending" | "None"
  sortComparer={(a, b) => {            // Custom sort function
    return a.name.localeCompare(b.name);
  }}
  
  // Selection
  allowMultiSelection={true}
  enableRangeSelection={false}
  selectedItems={['file1.txt', 'file2.pdf']}
  
  // Drag & Drop
  allowDragAndDrop={true}
  
  // Search
  searchSettings={{
    allowSearchOnTyping: true,          // Search as user types
    filterType: 'contains',             // "startsWith" | "contains" | "endsWith"
    ignoreCase: true
  }}
  
  // Upload
  uploadSettings={{
    autoUpload: true,
    minFileSize: 0,
    maxFileSize: 30000000,              // 30MB
    allowedExtensions: '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx',
    autoClose: false,
    directoryUpload: false,
    sequentialUpload: false
  }}
  
  // Customization
  cssClass="my-custom-fm"
  rootAliasName="My Files"
  popupTarget={document.getElementById('popup-container')}
  locale="en-US"
  enableRtl={false}
  
  // Performance
  enableVirtualization={false}
  enablePersistence={false}
  enableHtmlSanitizer={true}
  fileSystemData={[]}                   // For local data binding
  
  // Settings Objects
  contextMenuSettings={{
    file: ['Open', '|', 'Cut', 'Copy', '|', 'Delete', 'Rename'],
    folder: ['Open', '|', 'Cut', 'Copy', 'Paste', '|', 'Delete', 'Rename'],
    layout: ['SortBy', 'View', 'Refresh', '|', 'Paste', '|', 'NewFolder', 'Upload'],
    visible: true
  }}
  
  toolbarSettings={{
    items: ['NewFolder', 'Upload', 'Cut', 'Copy', 'Paste', 'Delete', 'Download', 'Refresh'],
    visible: true
  }}
  
  detailsViewSettings={{
    columns: [
      { field: 'name', headerText: 'Name', minWidth: 120 },
      { field: '_fm_modified', headerText: 'Modified', type: 'dateTime', minWidth: 120 },
      { field: 'size', headerText: 'Size', minWidth: 90 }
    ]
  }}
  
  navigationPaneSettings={{
    maxWidth: '650px',
    minWidth: '240px',
    visible: true,
    sortOrder: 'None'
  }}
  
  // AJAX Configuration
  ajaxSettings={{
    url: 'url',
    getImageUrl: 'url',
    uploadUrl: 'url',
    downloadUrl: 'url',
    // headers: { 'Authorization': 'Bearer token' }  // Optional custom headers
  }}
  
  // Templates
  largeIconsTemplate={(props) => (
    `<div class="custom-icon">${props.name}</div>`
  )}
  navigationPaneTemplate={(props) => (
    `<span class="custom-nav">${props.name}</span>`
  )}
/>
```

### AJAX Settings Deep Dive

The `ajaxSettings` prop is critical for backend integration:

```tsx
ajaxSettings={{
  // Main file operations endpoint
  url: "url",
  
  // Image/thumbnail retrieval
  getImageUrl: "url",
  
  // File upload endpoint
  uploadUrl: "url",
  
  // File download endpoint
  downloadUrl: "url"
}}
```

**Request Format for Main Endpoint:**
- All requests are POST
- Content-Type: `application/x-www-form-urlencoded`
- Request parameters include: `action`, `path`, `name`, `names[]`, etc.

**Actions Sent to Main Endpoint:**
1. `action=read&path=/folder` - List folder contents
2. `action=create&path=/folder&name=NewFolder` - Create folder
3. `action=delete&names[]=file1.txt&names[]=file2.pdf` - Delete files
4. `action=rename&path=/file.txt&name=newname.txt` - Rename file
5. `action=move&sourceNames[]=file.txt&targetPath=/backup&action=cut` - Move/Copy
6. `action=search&path=/&searchString=*.pdf` - Search files

**Expected Response Format:**
```json
{
  "cwd": { "name": "folder", "size": 0, "dateModified": "2024-01-01" },
  "files": [
    { "name": "file.txt", "size": 1024, "isFile": true, "dateModified": "2024-01-01" },
    { "name": "subfolder", "size": 0, "isFile": false, "dateModified": "2024-01-01" }
  ],
  "error": null
}
```

## Event Handling

The File Manager provides several events for custom behavior:

```tsx
<FileManagerComponent
  // File operations events
  fileOpen={(args) => console.log('File opened:', args)}
  fileSelect={(args) => console.log('File selected:', args)}
  beforeRename={(args) => console.log('Before rename:', args)}
  
  // Upload events
  uploadListCreate={(args) => console.log('Upload list created')}
  
  // Menu and toolbar events
  menuClick={(args) => console.log('Menu clicked:', args)}
  toolbarClick={(args) => console.log('Toolbar clicked:', args)}
  
  // Drag-drop events
  fileDragStart={(args) => console.log('Drag started:', args)}
  fileDropped={(args) => console.log('File dropped:', args)}
  fileDragStop={(args) => console.log('Drag stopped:', args)}
  
  // Creation/destruction
  created={(args) => console.log('File Manager created')}
  destroyed={(args) => console.log('File Manager destroyed')}
  
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

**Available Events:**
- `fileOpen` - File or folder opened
- `fileSelect` - File or folder selected
- `fileSelection` - File selection changed
- `beforeRename` - Before rename operation
- `rename` - After successful rename
- `beforeDelete` - Before delete operation
- `delete` - After successful delete
- `beforeDownload` - Before download starts
- `menuClick` - Context menu item clicked
- `toolbarClick` - Toolbar item clicked
- `fileDragStart`, `fileDragStop`, `fileDragging`, `fileDropped` - Drag-drop events
- `created`, `destroyed` - Lifecycle events
- `search` - Search performed
- `beforeSend` - Before AJAX request

## Next Steps

- **File Operations:** Explore create, delete, rename, upload/download in [file-operations.md](file-operations.md)
- **Views:** Learn about details view and large icons view in [views-and-navigation.md](views-and-navigation.md)
- **Customization:** Customize context menu and toolbar in [customization.md](customization.md)
- **Advanced:** Enable virtual scrolling and other performance features in [advanced-features.md](advanced-features.md)

## Troubleshooting

**Issue: Theme not applied**
- Verify all CSS imports are correct
- Check CSS file paths in `node_modules`
- Ensure import order: base, icons, inputs, popups, buttons, navigations, layouts, grids, filemanager

**Issue: Backend endpoints not working**
- Verify `ajaxSettings` URLs match your backend API
- Check CORS headers if using different domain
- Ensure backend implements required file operation actions

**Issue: Component not displaying**
- Verify `@Inject` has required services: DetailsView, NavigationPane, Toolbar
- Check browser console for errors
- Ensure CSS is imported before component usage
