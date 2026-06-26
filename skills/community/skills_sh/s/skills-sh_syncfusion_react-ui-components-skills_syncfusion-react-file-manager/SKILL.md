---
name: syncfusion-react-file-manager
description: Implement Syncfusion React File Manager component for file system navigation and management. Use when users need file browsing, upload/download, file operations (create, delete, rename), multiple views, drag-drop, customization, or accessibility features. Supports local and remote file systems with comprehensive customization options.
metadata:
    author: "Syncfusion Inc"
    version: "33.1.44"
---

# Syncfusion React File Manager

A comprehensive guide to implementing the Syncfusion React File Manager component for building file system interfaces with rich features like drag-drop, multi-view support, custom operations, and full accessibility.

## Quick Navigation

**🚀 Just Getting Started?**  
→ Read [Getting Started](references/getting-started.md) for installation and basic setup

**🛠️ Need to Build File Operations?**  
→ Check [File Operations (CRUD)](references/file-operations.md) for create, read, update, delete patterns

**📊 Working with Local Data?**  
→ See [Flat Data Structure](references/flat-data.md) for in-memory files and event-driven operations

**✅ Need Multiple File Selection?**  
→ Learn [Multiple Selection & Range Selection](references/multiple-selection.md) for Ctrl+Click, Shift+Click, drag selection

**⚡ Handling Large File Lists?**  
→ Use [Virtualization](references/virtualization.md) for smooth scrolling with 1000+ files

**🎨 Want to Customize the UI?**  
→ See [Customization & Styling](references/customization.md) for theming and layout options

**⚙️ Looking for Advanced Features?**  
→ Explore [Advanced Features](references/advanced-features.md) for performance, custom providers, and API integration

**♿ Need Accessibility or Multi-Language?**  
→ Visit [Accessibility & Localization](references/accessibility-localization.md) for WCAG and i18n

**🔐 Need User Access Control?**  
→ Learn [Access Control](references/access-control.md) for role-based permissions and security

**📤 Passing Custom Headers to Server?**  
→ See [Pass Custom Value to Server](references/pass-custom-value-to-server.md) for setRequestHeader and authentication

**🎯 Need Advanced Customization?**  
→ Check [Adding Custom Item to Context Menu](references/adding-custom-item-to-context-menu.md) and [Adding Custom Item to Toolbar](references/adding-custom-item-to-toolbar.md)

**🔧 Want to Enable/Disable Toolbar Items?**  
→ See [Enable/Disable Toolbar Item](references/enable-disable-toolbar-item.md) for programmatic control

**🖼️ Customizing Thumbnails & Icons?**  
→ Learn [Customize Custom Thumbnail](references/customize-custom-thumbnail.md) for icon templates

**📁 Customizing Navigation Pane?**  
→ See [Customize Navigation Pane](references/customize-navigation-items.md) for tree view customization

**✨ Pre-selecting Items?**  
→ Learn [Preselect Items](references/preselect-the-items.md) for default selections

**📦 File Manager Inside Dialog/Tabs?**  
→ See [Nested Items](references/nested-items.md) for embedding in other components

## When to Use This Skill

Use this skill when you need to:
- Create a file browser interface for your application
- Implement file upload and download functionality
- Build file management features (create, delete, rename, refresh)
- Support multiple view options (details and large icons)
- Add drag-and-drop capability to file management
- Customize context menus, toolbars, and styling
- Integrate accessibility features (keyboard navigation, ARIA)
- Support internationalization and RTL languages
- Connect to local or remote file systems

## Component Overview

The **File Manager** is a graphical user interface component for managing file systems. It enables users to:

- **File Operations:** Read, create, delete, rename, upload, download, and refresh files
- **Multiple Views:** Switch between details view (sorted list) and large icons view (thumbnails)
- **Navigation:** Breadcrumb trails and navigation pane with tree view for hierarchy exploration
- **Context Menu:** Right-click menus with customizable options
- **Drag-and-Drop:** Drag files between folders with configurable drop zones
- **Accessibility:** Full WCAG compliance with keyboard navigation and screen reader support
- **Localization:** Multi-language support with RTL direction for right-to-left languages
- **Customization:** Extensive API for styling, theming, and behavior customization

## Documentation and Navigation Guide

### Core Features

#### Getting Started & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic file manager implementation
- CSS imports and theme configuration
- Initial configuration and setup
- Connection to file service (AjaxSettings)

#### File Operations (CRUD)
📄 **Read:** [references/file-operations.md](references/file-operations.md)
- Create folders and files
- Read and browse file systems
- Update/rename operations
- Delete files and folders
- Upload and download functionality
- Multi-file selection and bulk operations
- File provider patterns and custom implementations

#### Views & Navigation
📄 **Read:** [references/views-and-navigation.md](references/views-and-navigation.md)
- Details view with columns
- Large icon view with thumbnails
- View switching and configuration
- Breadcrumb navigation control
- Navigation pane (tree view sidebar)
- Toolbar features and layout

### Data Management

#### Flat Data Structure
📄 **Read:** [references/flat-data.md](references/flat-data.md)
- Use local JSON data instead of server calls
- FileData interface and properties
- Permission management per item
- Event-driven file operations (create, delete, rename, search)
- State management with React hooks
- Backend synchronization patterns
- Large dataset performance optimization

#### Multiple Selection & Range Selection
📄 **Read:** [references/multiple-selection.md](references/multiple-selection.md)
- Enable/disable multi-select capability
- Range selection by mouse drag
- Checkbox selection support
- Selection state management
- Selected items API and events
- Pre-selecting items on load
- Keyboard shortcuts (Ctrl+A, Shift+Click)

#### Preselect Items
📄 **Read:** [references/preselect-the-items.md](references/preselect-the-items.md)
- Programmatically select items on load
- Preselect based on file type, size, or date
- Context-aware preselection
- Selection methods (selectAll, clearSelection)
- Get selected items programmatically

### Performance & Optimization

#### Virtualization & Performance
📄 **Read:** [references/virtualization.md](references/virtualization.md)
- Enable virtual scrolling for large datasets
- Dynamic loading of files and folders
- Viewport-based rendering optimization
- Module injection and setup
- Performance limitations and workarounds
- Best practices for handling 1000+ items

### User Interactions

#### Drag-and-Drop Features
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Enable/disable drag-drop functionality
- Drop area configuration
- Event handling (fileDragStart, fileDragStop, fileDropped)
- Cross-folder drag-drop
- Custom drag-drop behavior

#### Customization & Styling
📄 **Read:** [references/customization.md](references/customization.md)
- Context menu customization
- Toolbar customization
- Details view column customization
- Navigation pane customization
- Tooltip customization
- Show/hide file extensions and hidden files
- Thumbnail configuration for large icons view
- CSS class and theme customization

### Advanced Customization

#### Adding Custom Item to Context Menu
📄 **Read:** [references/adding-custom-item-to-context-menu.md](references/adding-custom-item-to-context-menu.md)
- Add custom menu items to context menu
- Add icons to menu items
- Handle menu click events
- Conditional menu items based on file properties
- Dynamic menu customization

#### Adding Custom Item to Toolbar
📄 **Read:** [references/adding-custom-item-to-toolbar.md](references/adding-custom-item-to-toolbar.md)
- Modify default toolbar items
- Add custom toolbar items
- Custom templates for toolbar
- Toolbar click handling
- Custom buttons, checkboxes, and dropdowns

#### Enable/Disable Toolbar Item
📄 **Read:** [references/enable-disable-toolbar-item.md](references/enable-disable-toolbar-item.md)
- Enable/disable toolbar items programmatically
- Enable/disable based on selection
- Role-based toolbar control
- Disable during operations
- Permission-based toolbar control

#### Customize Custom Thumbnail
📄 **Read:** [references/customize-custom-thumbnail.md](references/customize-custom-thumbnail.md)
- Hide/show thumbnails
- Custom templates for large icon view
- File type-based icons
- Size-based color coding
- Date-based icon indicators

#### Customize Navigation Pane
📄 **Read:** [references/customize-navigation-items.md](references/customize-navigation-items.md)
- Control navigation pane visibility and width
- Custom templates for navigation nodes
- Add file counts and metadata
- Color-coded folders
- Icon-based navigation styling
- Responsive navigation pane

#### Nested Items
📄 **Read:** [references/nested-items.md](references/nested-items.md)
- Embed File Manager inside Dialog
- Embed File Manager inside Tab
- Embed File Manager inside Splitter
- File selector with File Manager
- Multi-panel layouts with File Manager

### Security & Integration

#### Access Control
📄 **Read:** [references/access-control.md](references/access-control.md)
- Define access permissions for folders/files
- Permission types (Allow/Deny)
- Role-based access control
- Access rules for different user roles
- Backend permission validation

#### Pass Custom Value to Server
📄 **Read:** [references/pass-custom-value-to-server.md](references/pass-custom-value-to-server.md)
- Setting custom HTTP headers with setRequestHeader
- User authentication headers
- User identification headers
- Tracking file operations
- Department-based access
- Download operation customization
- Image loading customization
- Complete server integration patterns

### Accessibility & Localization

#### Accessibility & Localization
📄 **Read:** [references/accessibility-localization.md](references/accessibility-localization.md)
- WCAG 2.1 compliance
- Keyboard navigation (arrow keys, enter, delete)
- ARIA attributes and roles
- Screen reader support
- Internationalization (i18n)
- Right-to-left (RTL) support
- Date and number formatting for different locales

### Advanced Features

#### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Custom file system provider implementation
- API integration patterns
- Performance optimization techniques
- Error handling and edge cases
- Event system and hooks
- Advanced search and filtering
- Custom sorting and comparison
- Nested components (File Manager in Dialog/Tabs)

## Quick Start Example

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-icons/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-splitbuttons/styles/material.css';
import '@syncfusion/ej2-navigations/styles/material.css';
import '@syncfusion/ej2-layouts/styles/material.css';
import '@syncfusion/ej2-grids/styles/material.css';
import '@syncfusion/ej2-react-filemanager/styles/material.css';

function App() {
  const hostUrl = "url";

  return (
    <div>
      <FileManagerComponent
        id="file"
        ajaxSettings={{
          url: hostUrl + "api/FileManager/FileOperations",
          getImageUrl: hostUrl + "api/FileManager/GetImage",
          uploadUrl: hostUrl + "api/FileManager/Upload",
          downloadUrl: hostUrl + "api/FileManager/Download"
        }}
        view="Details"
        height="375px"
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default App;
```

## Methods Reference

The File Manager provides programmatic methods to control operations:

### Selection & View Control
| Method | Parameters | Purpose |
|--------|-----------|---------|
| `selectAll()` | - | Select all files and folders in current path |
| `clearSelection()` | - | Deselect all items |
| `getSelectedFiles()` | - | Get array of selected file objects |

### File Operations
| Method | Parameters | Purpose |
|--------|-----------|---------|
| `createFolder(name?)` | name: string (optional) | Create new folder; opens dialog if name not provided |
| `renameFile(id?, name?)` | id: string, name: string | Rename file/folder; opens dialog if params not provided |
| `deleteFiles(ids?)` | ids: string[] | Delete files/folders; opens confirmation if not provided |
| `openFile(id)` | id: string | Open file or navigate to folder |
| `downloadFiles(ids?)` | ids: string[] (optional) | Download selected files; downloads selection if not provided |
| `uploadFiles()` | - | Open file upload dialog |

### Navigation & Refresh
| Method | Parameters | Purpose |
|--------|-----------|---------|
| `refreshFiles()` | - | Refresh current folder contents |
| `refreshLayout()` | - | Refresh component layout |
| `traverseBackward()` | - | Navigate to parent directory |
| `filterFiles(filterData?)` | filterData: Object | Apply custom filter to displayed files |

### Toolbar & Menu Control
| Method | Parameters | Purpose |
|--------|-----------|---------|
| `disableToolbarItems(items)` | items: string[] | Disable specific toolbar buttons |
| `enableToolbarItems(items)` | items: string[] | Enable specific toolbar buttons |
| `getToolbarItemIndex(item)` | item: string | Get toolbar item position |
| `disableMenuItems(items)` | items: string[] | Disable context menu items |
| `enableMenuItems(items)` | items: string[] | Enable context menu items |
| `getMenuItemIndex(item)` | item: string | Get context menu item position |

### Dialog Control
| Method | Parameters | Purpose |
|--------|-----------|---------|
| `closeDialog()` | - | Close any open dialog |

### Component Lifecycle
| Method | Parameters | Purpose |
|--------|-----------|---------|
| `destroy()` | - | Clean up component resources |

## Events Reference

File Manager provides comprehensive event hooks for customization:

### File Selection Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `fileSelection` | FileSelectionEventArgs | File/folder about to be selected (cancelable) |
| `fileSelect` | FileSelectEventArgs | File/folder is selected/unselected |

### File Navigation Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `fileOpen` | FileOpenEventArgs | File/folder about to be opened |
| `fileLoad` | FileLoadEventArgs | File/folder item is rendered |

### File Operation Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `beforeFolderCreate` | FolderCreateEventArgs | Folder creation requested (cancelable) |
| `folderCreate` | FolderCreateEventArgs | Folder successfully created |
| `beforeRename` | RenameEventArgs | Rename operation requested (cancelable) |
| `rename` | RenameEventArgs | File/folder successfully renamed |
| `beforeDelete` | DeleteEventArgs | Deletion requested (cancelable) |
| `delete` | DeleteEventArgs | File/folder successfully deleted |
| `beforeMove` | MoveEventArgs | Move/copy operation started |
| `move` | MoveEventArgs | File/folder successfully moved/copied |

### Drag & Drop Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `fileDragStart` | FileDragEventArgs | Drag operation begins |
| `fileDragging` | FileDragEventArgs | Dragging is in progress |
| `fileDragStop` | FileDragEventArgs | Drag about to be dropped (cancelable) |
| `fileDropped` | FileDragEventArgs | File/folder successfully dropped |

### Upload Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `uploadListCreate` | UploadListCreateArgs | Upload UI created (pre-upload validation) |
| `beforeDownload` | BeforeDownloadEventArgs | Download requested |

### Menu & Context Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `menuOpen` | MenuOpenEventArgs | Context menu about to open |
| `menuClose` | MenuCloseEventArgs | Context menu closed |
| `menuClick` | MenuClickEventArgs | Context menu item clicked |

### Search & Dialog Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `search` | SearchEventArgs | User types in search box |
| `beforePopupOpen` | BeforePopupOpenCloseEventArgs | Dialog about to open |
| `popupOpen` | PopupOpenCloseEventArgs | Dialog opened |
| `beforePopupClose` | BeforePopupOpenCloseEventArgs | Dialog about to close |
| `popupClose` | PopupOpenCloseEventArgs | Dialog closed |

### AJAX & Server Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `beforeSend` | BeforeSendEventArgs | AJAX request sent (add custom headers) |
| `success` | SuccessEventArgs | AJAX request succeeded |
| `failure` | FailureEventArgs | AJAX request failed |
| `beforeImageLoad` | BeforeImageLoadEventArgs | Image/thumbnail request sent |

### Lifecycle Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `created` | Object | Component initialization complete |
| `destroyed` | Object | Component destroyed |

### Toolbar Events
| Event | Args | Triggered When |
|-------|------|----------------|
| `toolbarCreate` | ToolbarCreateEventArgs | Toolbar being created |
| `toolbarClick` | ToolbarClickEventArgs | Toolbar button clicked |

## Common Patterns

### 1. Basic Setup Pattern
```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';
import '@syncfusion/ej2-react-filemanager/styles/material.css';

export default function BasicFileManager() {
  return (
    <FileManagerComponent
      id="file"
      ajaxSettings={{
        url: "url",
        getImageUrl: "url",
        uploadUrl: "url",
        downloadUrl: "url"
      }}
      view="Details"
      height="500px"
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}
```

**Setup Steps:**
1. Install `@syncfusion/ej2-react-filemanager` and all peer dependencies
2. Import CSS theme (material, bootstrap, bootstrap4, fabric, or tailwind)
3. Configure `ajaxSettings` endpoints
4. Choose view (Details or LargeIcons)
5. Inject required services (features to enable)

### 2. File Service Backend Pattern

**Expected Endpoint Structure:**

```tsx
ajaxSettings={{
  url: "url",
  getImageUrl: "url",
  uploadUrl: "url",
  downloadUrl: "url"
}}
```

**Backend Implementation (ASP.NET Core Example):**

```csharp
[ApiController]
[Route("api/[controller]")]
public class FileManagerController : ControllerBase
{
    [HttpPost("FileOperations")]
    public IActionResult FileOperations(
        [FromForm] string action,
        [FromForm] string path,
        [FromForm] string name = null,
        [FromForm] IFormFile uploadFiles = null)
    {
        switch (action)
        {
            case "read":
                // Return files and folders at given path
                return Ok(new { files = GetDirectoryContents(path) });
            case "create":
                // Create new folder
                Directory.CreateDirectory(Path.Combine(path, name));
                return Ok();
            case "delete":
                // Delete files/folders
                return Ok();
            case "rename":
                // Rename file/folder
                return Ok();
            case "move":
                // Move or copy files
                return Ok();
            default:
                return BadRequest("Invalid action");
        }
    }

    [HttpGet("GetImage")]
    public IActionResult GetImage([FromQuery] string path)
    {
        // Return thumbnail or image file
        var filePath = ResolvePath(path);
        return PhysicalFile(filePath, "image/jpeg");
    }

    [HttpPost("Upload")]
    public IActionResult Upload([FromForm] IFormFile uploadFiles, [FromForm] string path)
    {
        // Handle file upload
        var filePath = Path.Combine(path, uploadFiles.FileName);
        using (var stream = new FileStream(filePath, FileMode.Create))
        {
            uploadFiles.CopyTo(stream);
        }
        return Ok();
    }

    [HttpGet("Download")]
    public IActionResult Download([FromQuery] string path)
    {
        // Return file for download
        var file = System.IO.File.ReadAllBytes(path);
        var fileName = Path.GetFileName(path);
        return File(file, "application/octet-stream", fileName);
    }
}
```

### 3. State Management Pattern
```tsx
import React, { useRef, useState } from 'react';

export default function FileManagerWithState() {
  const fileManagerRef = useRef(null);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [currentPath, setCurrentPath] = useState('/');

  const handleFileSelect = (args) => {
    setSelectedFiles(args.fileDetails);
  };

  const handleCreateFolder = () => {
    fileManagerRef.current?.createFolder('NewFolder');
  };

  const handleDeleteSelected = () => {
    const ids = selectedFiles.map(f => f.name);
    fileManagerRef.current?.deleteFiles(ids);
  };

  return (
    <div>
      <div className="toolbar">
        <button onClick={handleCreateFolder}>Create Folder</button>
        <button onClick={handleDeleteSelected} disabled={!selectedFiles.length}>
          Delete ({selectedFiles.length})
        </button>
        <span>Path: {currentPath}</span>
      </div>
      <FileManagerComponent
        ref={fileManagerRef}
        fileSelect={handleFileSelect}
        ajaxSettings={{...}}
        height="400px"
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}
```

### 4. Event-Driven Custom Logic Pattern
```tsx
<FileManagerComponent
  // Prevent deletion of certain files
  beforeDelete={(args) => {
    if (args.fileDetails[0].name.startsWith('.')) {
      args.cancel = true;
      alert('Cannot delete system files');
    }
  }}
  
  // Add headers to AJAX requests
  beforeSend={(args) => {
    args.headers = { ...args.headers, 'Authorization': `Bearer ${token}` };
  }}
  
  // Validate before upload
  uploadListCreate={(args) => {
    args.fileDetails.forEach(file => {
      if (file.size > 5000000) { // 5MB limit
        args.cancel = true;
      }
    });
  }}
  
  // Track successful operations
  success={(args) => {
    console.log('Operation successful:', args.action, args.result);
  }}
  
  // Handle errors
  failure={(args) => {
    console.error('Operation failed:', args.error);
  }}
/>
```

### 5. Customization Pattern
```tsx
<FileManagerComponent
  // Customize toolbar
  toolbarSettings={{
    items: ['NewFolder', 'Upload', '|', 'Cut', 'Copy', 'Paste', '|', 'Delete', 'Download'],
    visible: true
  }}
  
  // Customize context menu
  contextMenuSettings={{
    file: ['Open', '|', 'Cut', 'Copy', '|', 'Delete', 'Rename', '|', 'Details'],
    folder: ['Open', '|', 'Cut', 'Copy', 'Paste', '|', 'Delete', 'Rename'],
    layout: ['SortBy', 'View', 'Refresh', '|', 'NewFolder', 'Upload'],
    visible: true
  }}
  
  // Customize columns in details view
  detailsViewSettings={{
    columns: [
      {
        field: 'name',
        headerText: 'Name',
        minWidth: 120,
        template: '<span class="custom-name">${name}</span>'
      },
      {
        field: '_fm_modified',
        headerText: 'Modified',
        type: 'dateTime',
        format: 'MMMM dd, yyyy HH:mm',
        minWidth: 120
      },
      {
        field: 'size',
        headerText: 'Size',
        minWidth: 90,
        template: '<span>${size}</span>'
      }
    ]
  }}
  
  // Customize navigation pane
  navigationPaneSettings={{
    maxWidth: '650px',
    minWidth: '240px',
    visible: true,
    sortOrder: 'None'
  }}
/>
```

### 6. Performance Optimization Pattern
```tsx
<FileManagerComponent
  // Enable virtualization for large datasets
  enableVirtualization={true}
  
  // Enable persistence to maintain state
  enablePersistence={true}
  
  // Configure search settings
  searchSettings={{
    allowSearchOnTyping: true,
    filterType: 'contains',
    ignoreCase: true
  }}
  
  // Configure upload settings
  uploadSettings={{
    autoUpload: true,
    minFileSize: 0,
    maxFileSize: 30000000, // 30MB
    allowedExtensions: '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx',
    autoClose: false,
    directoryUpload: false,
    sequentialUpload: false
  }}
  
  // Sort optimization
  sortBy="name"
  sortOrder="Ascending"
/>
```

## Key Props

### Core Configuration
| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `ajaxSettings` | Object | See below | Configure backend endpoints for file operations |
| `path` | string | "/" | Current folder path |
| `view` | string | "LargeIcons" | View type: "Details" or "LargeIcons" |
| `width` | string | "100%" | Component width |
| `height` | string | "400px" | Component height |

### Display & Behavior
| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `showFileExtension` | boolean | true | Display file extensions |
| `showHiddenItems` | boolean | false | Display hidden files/folders |
| `showThumbnail` | boolean | true | Show thumbnails in large icons view |
| `showItemCheckBoxes` | boolean | true | Display checkboxes on hover |
| `sortBy` | string | "name" | Sort field: "name", "dateModified", "size" |
| `sortOrder` | string | "Ascending" | Sort direction: "Ascending", "Descending", or "None" |
| `enableRtl` | boolean | false | Right-to-left layout support |
| `locale` | string | "en-US" | Localization language code |

### Selection & Navigation
| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `allowMultiSelection` | boolean | true | Allow selecting multiple files |
| `enableRangeSelection` | boolean | false | Select multiple items by dragging mouse |
| `selectedItems` | string[] | [] | Initially selected file names |
| `allowDragAndDrop` | boolean | false | Enable drag-drop operations |

### Performance & Features
| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `enableVirtualization` | boolean | false | Virtual scrolling for large datasets |
| `enablePersistence` | boolean | false | Persist view, path, and selection state |
| `enableHtmlSanitizer` | boolean | true | Sanitize HTML to prevent XSS attacks |
| `cssClass` | string | "" | Custom CSS class for styling |
| `rootAliasName` | string | null | Display name for root folder |
| `popupTarget` | HTMLElement | null | Dialog popup target element |

### Data & Settings Objects
| Prop | Type | Purpose |
|------|------|---------|
| `fileSystemData` | Object[] | Flat data structure for local files |
| `contextMenuSettings` | Object | Customize context menu items |
| `toolbarSettings` | Object | Configure toolbar items and layout |
| `detailsViewSettings` | Object | Customize columns and column widths |
| `navigationPaneSettings` | Object | Configure sidebar behavior and appearance |
| `searchSettings` | Object | Configure search filtering options |
| `uploadSettings` | Object | Configure upload behavior |
| `sortComparer` | Function | Custom sorting function |
| `largeIconsTemplate` | string \| Function | Custom template for large icons view |
| `navigationPaneTemplate` | string \| Function | Custom template for navigation pane |

### AJAX Settings Configuration
```tsx
ajaxSettings={{
  url: "url",     // Main CRUD endpoint (required)
  getImageUrl: "url",   // Thumbnail retrieval
  uploadUrl: "url",       // File upload endpoint
  downloadUrl: "url",   // File download endpoint
  // Optional: Add custom headers
  // headers: { 'Authorization': 'Bearer token' }
}}
```

**Backend Endpoint Expectations:**
- **url** - Receives POST requests with `action` parameter:
  - `read`: List files in path
  - `create`: Create new folder
  - `delete`: Delete file/folder
  - `rename`: Rename file/folder
  - `move`: Move/copy file (copy or cut)
  - `search`: Search files
  - `upload`: Handle file uploads
  - `download`: Prepare download
  
- **getImageUrl** - GET request with `path` parameter for thumbnail image URL
- **uploadUrl** - POST multipart form data with file upload
- **downloadUrl** - Initiate file download stream

## Common Use Cases

### Case 1: Document Management System
Implement a document browser with upload, download, and folder organization:
- Use Details view for metadata display
- Configure context menu for document operations
- Add search functionality
- Implement access control on backend

### Case 2: Media File Browser
Build a gallery with image/video thumbnails:
- Use Large Icons view for thumbnail display
- Configure `getImageUrl` for preview generation
- Implement lazy loading for performance
- Add drag-drop for organization

### Case 3: Admin File Manager
Create an internal file management tool:
- Customize toolbar with admin-specific actions
- Implement advanced context menu options
- Add logging and audit trails
- Configure permissions on backend

### Case 4: Localized File Manager
Support multiple languages and RTL:
- Set `locale` to user's language
- Enable `enableRtl` for RTL languages
- Customize context menu labels per language
- Format dates and sizes per locale

---

## Next Steps

1. **Start:** Read [references/getting-started.md](references/getting-started.md) for installation and basic setup
2. **Implement:** Choose the feature references that match your requirements
3. **Customize:** Review [references/customization.md](references/customization.md) for styling and configuration
4. **Optimize:** Check [references/advanced-features.md](references/advanced-features.md) for performance and edge cases
5. **Accessibility:** Ensure compliance with [references/accessibility-localization.md](references/accessibility-localization.md)

---