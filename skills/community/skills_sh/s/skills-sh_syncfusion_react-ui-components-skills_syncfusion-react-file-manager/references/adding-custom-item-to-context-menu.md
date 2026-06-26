# Adding Custom Items to Context Menu in React File Manager

The context menu in the React File Manager component can be customized to add custom menu items. You can add icons, event handlers, and control when menu items appear using events and settings.

## Table of Contents

1. [Understanding Context Menu Settings](#understanding-context-menu-settings)
2. [Adding Custom Menu Items](#adding-custom-menu-items)
3. [Adding Icons to Menu Items](#adding-icons-to-menu-items)
4. [Handling Menu Clicks](#handling-menu-clicks)
5. [Advanced Customization](#advanced-customization)
6. [Complete Example](#complete-example)

## Understanding Context Menu Settings

The `contextMenuSettings` property allows you to define menu items for different context types:

```typescript
contextMenuSettings={{
  file: ['Open', '|', 'Delete', 'Rename', '|', 'Details', 'Custom'],
  folder: ['Open', '|', 'Delete', 'Rename', '|', 'Details', 'Custom'],
  layout: ['SortBy', 'View', 'Refresh', '|', 'NewFolder', 'Upload', '|', 'Details', '|', 'SelectAll', 'Custom']
}}
```

## Adding Custom Menu Items

### Basic Custom Menu Item

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function CustomContextMenuExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const handleMenuClick = (args) => {
    if (args.item.text === 'Custom') {
      alert(`You have clicked custom menu item on: ${args.fileDetails?.name}`);
    }
  };

  const handleMenuOpen = (args) => {
    // Add custom styling to custom menu item
    for (const item of args.items) {
      if (item.id === fileManagerRef.current?.element.id + '_cm_custom') {
        item.iconCss = 'e-icons e-fe-settings';
      }
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
      contextMenuSettings={{
        file: ['Open', '|', 'Delete', 'Rename', '|', 'Details', 'Custom'],
        folder: ['Open', '|', 'Delete', 'Rename', '|', 'Details', 'Custom'],
        layout: ['SortBy', 'View', 'Refresh', '|', 'NewFolder', 'Upload', '|', 'Details', '|', 'SelectAll', 'Custom']
      }}
      menuClick={handleMenuClick}
      menuOpen={handleMenuOpen}
    >
      <Inject services={[NavigationPane, DetailsView, Toolbar]} />
    </FileManagerComponent>
  );
}

export default CustomContextMenuExample;
```

## Adding Icons to Menu Items

### Pattern 1: Using Built-in Icons

```typescript
function handleMenuOpen(args) {
  for (const item of args.items) {
    switch (item.id.split('_').pop()) {
      case 'custom_share':
        item.iconCss = 'e-icons e-share';
        break;
      case 'custom_archive':
        item.iconCss = 'e-icons e-folder';
        break;
      case 'custom_encrypt':
        item.iconCss = 'e-icons e-lock';
        break;
      case 'custom_properties':
        item.iconCss = 'e-icons e-info';
        break;
    }
  }
}
```

### Pattern 2: Using Custom Icons

```typescript
function handleMenuOpen(args) {
  for (const item of args.items) {
    if (item.text === 'Share') {
      item.iconCss = 'custom-icon-share';
    } else if (item.text === 'Archive') {
      item.iconCss = 'custom-icon-archive';
    } else if (item.text === 'Encrypt') {
      item.iconCss = 'custom-icon-encrypt';
    }
  }
}

// CSS for custom icons
const style = `
  .custom-icon-share::before {
    content: '🔗';
    font-size: 16px;
  }
  .custom-icon-archive::before {
    content: '📦';
    font-size: 16px;
  }
  .custom-icon-encrypt::before {
    content: '🔐';
    font-size: 16px;
  }
`;
```

## Handling Menu Clicks

### Pattern 1: File Operations

```typescript
function handleMenuClick(args) {
  const fileName = args.fileDetails?.name;
  
  switch (args.item.text) {
    case 'Compress':
      compressFile(fileName);
      console.log(`Compressing file: ${fileName}`);
      break;
    
    case 'Share':
      shareFile(fileName);
      console.log(`Sharing file: ${fileName}`);
      break;
    
    case 'Encrypt':
      encryptFile(fileName);
      console.log(`Encrypting file: ${fileName}`);
      break;
    
    case 'Properties':
      showFileProperties(fileName);
      console.log(`Showing properties for: ${fileName}`);
      break;
    
    default:
      console.log(`Menu item clicked: ${args.item.text}`);
  }
}

// Handler functions
function compressFile(fileName) {
  // Implementation for compression
  alert(`${fileName} has been compressed`);
}

function shareFile(fileName) {
  // Implementation for sharing
  alert(`${fileName} sharing dialog opened`);
}

function encryptFile(fileName) {
  // Implementation for encryption
  alert(`${fileName} is being encrypted`);
}

function showFileProperties(fileName) {
  // Implementation to show properties
  alert(`Properties of ${fileName}`);
}
```

### Pattern 2: Different Actions for Files vs Folders

```typescript
function handleMenuClick(args) {
  const isFile = args.fileDetails?.isFile;
  const itemName = args.fileDetails?.name;
  
  if (isFile) {
    // File-specific actions
    if (args.item.text === 'Convert') {
      convertFile(itemName);
    } else if (args.item.text === 'Preview') {
      previewFile(itemName);
    }
  } else {
    // Folder-specific actions
    if (args.item.text === 'Backup') {
      backupFolder(itemName);
    } else if (args.item.text === 'SetQuota') {
      setFolderQuota(itemName);
    }
  }
}
```

### Pattern 3: Context-Aware Actions

```typescript
function handleMenuClick(args) {
  const selectedItems = fileManagerRef.current?.getSelectedFiles();
  const itemCount = selectedItems?.length || 0;

  if (args.item.text === 'BulkOperation') {
    if (itemCount === 0) {
      alert('Please select items first');
    } else if (itemCount === 1) {
      performSingleItemOperation(selectedItems[0]);
    } else {
      performBulkOperation(selectedItems);
    }
  }
}
```

## Advanced Customization

### Pattern 1: Conditional Menu Items

```typescript
function handleMenuOpen(args) {
  const fileDetails = args.fileDetails;
  
  // Show/hide items based on file properties
  args.items = args.items.filter(item => {
    // Hide rename for system files
    if (item.text === 'Rename' && isSystemFile(fileDetails)) {
      return false;
    }
    
    // Hide download for folders
    if (item.text === 'Download' && !fileDetails.isFile) {
      return false;
    }
    
    // Show custom items only for image files
    if (item.text === 'Convert' && !isImageFile(fileDetails)) {
      return false;
    }
    
    return true;
  });
}

function isSystemFile(fileDetails) {
  const systemFiles = ['.gitignore', '.env', 'package.json'];
  return systemFiles.includes(fileDetails?.name);
}

function isImageFile(fileDetails) {
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp'];
  const ext = fileDetails?.name?.substring(fileDetails.name.lastIndexOf('.'));
  return imageExtensions.includes(ext?.toLowerCase());
}
```

### Pattern 2: Dynamic Menu Items Based on Permissions

```typescript
function handleMenuOpen(args) {
  const userRole = localStorage.getItem('userRole');
  
  // Filter menu items based on user role
  const filteredItems = args.items.filter(item => {
    const permissions = {
      'Admin': ['Open', 'Delete', 'Rename', 'Details', 'Admin-Tools'],
      'Editor': ['Open', 'Rename', 'Details', 'Custom-Edit'],
      'Viewer': ['Open', 'Details']
    };
    
    const allowedItems = permissions[userRole] || permissions['Viewer'];
    return allowedItems.includes(item.text) || item.text.includes('|');
  });
  
  args.items = filteredItems;
}
```

### Pattern 3: Nested Custom Menus

```typescript
function handleMenuOpen(args) {
  // Add submenu items dynamically
  const customItem = args.items.find(item => item.text === 'Custom');
  
  if (customItem) {
    customItem.items = [
      { text: 'Compress', id: 'custom_compress' },
      { text: 'Encrypt', id: 'custom_encrypt' },
      { text: 'Properties', id: 'custom_properties' }
    ];
  }
}
```

## Complete Example

### Full Implementation with Multiple Custom Items

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function AdvancedContextMenuExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const handleMenuClick = (args) => {
    const itemName = args.fileDetails?.name;
    const isFile = args.fileDetails?.isFile;

    switch (args.item.text) {
      case 'Compress':
        compressItem(itemName, isFile);
        break;
      
      case 'Share':
        shareItem(itemName);
        break;
      
      case 'Encrypt':
        encryptItem(itemName);
        break;
      
      case 'Properties':
        showProperties(itemName);
        break;
      
      case 'Backup':
        if (!isFile) backupFolder(itemName);
        break;
      
      case 'SetQuota':
        if (!isFile) setFolderQuota(itemName);
        break;
      
      default:
        console.log(`Menu action: ${args.item.text}`);
    }
  };

  const handleMenuOpen = (args) => {
    const fileDetails = args.fileDetails;

    // Add icons to custom items
    for (const item of args.items) {
      const itemId = item.id;
      
      if (itemId?.includes('_cm_compress')) {
        item.iconCss = 'e-icons e-redo';
      } else if (itemId?.includes('_cm_share')) {
        item.iconCss = 'e-icons e-share';
      } else if (itemId?.includes('_cm_encrypt')) {
        item.iconCss = 'e-icons e-lock';
      } else if (itemId?.includes('_cm_properties')) {
        item.iconCss = 'e-icons e-info';
      }
    }

    // Filter items based on context
    args.items = args.items.filter(item => {
      // Hide folder-specific items for files
      if (fileDetails?.isFile && ['Backup', 'SetQuota'].includes(item.text)) {
        return false;
      }
      
      // Hide file-specific items for folders
      if (!fileDetails?.isFile && ['Compress', 'Encrypt'].includes(item.text)) {
        return false;
      }
      
      return true;
    });
  };

  const compressItem = (name, isFile) => {
    const type = isFile ? 'file' : 'folder';
    alert(`${type} "${name}" has been compressed`);
  };

  const shareItem = (name) => {
    alert(`Sharing options for "${name}"`);
  };

  const encryptItem = (name) => {
    alert(`Encrypting "${name}"...`);
  };

  const showProperties = (name) => {
    alert(`Properties of "${name}"`);
  };

  const backupFolder = (name) => {
    alert(`Backing up folder "${name}"...`);
  };

  const setFolderQuota = (name) => {
    alert(`Setting quota for folder "${name}"`);
  };

  return (
    <div className="control-section">
      <FileManagerComponent
        ref={fileManagerRef}
        id="advanced-context-menu"
        height="500px"
        view="Details"
        allowDragAndDrop={true}
        allowMultiSelection={true}
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        contextMenuSettings={{
          file: [
            'Open', '|', 'Cut', 'Copy', 'Delete', 'Rename',
            '|', 'Download', 'Details', '|',
            'Compress', 'Encrypt', 'Share', 'Properties'
          ],
          folder: [
            'Open', '|', 'Cut', 'Copy', 'Delete', 'Rename',
            '|', 'Details', '|',
            'Compress', 'Share', 'Backup', 'SetQuota', 'Properties'
          ],
          layout: [
            'SortBy', 'View', 'Refresh', '|',
            'NewFolder', 'Upload', '|', 'Details', '|',
            'SelectAll'
          ]
        }}
        menuClick={handleMenuClick}
        menuOpen={handleMenuOpen}
      >
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>

      <style>{`
        .e-contextmenu .e-menu-item.e-icons::before {
          font-size: 16px;
          margin-right: 8px;
        }
      `}</style>
    </div>
  );
}

export default AdvancedContextMenuExample;
```

## Menu Item Separators

Use the pipe character `|` to add separators between menu items:

```typescript
contextMenuSettings={{
  file: [
    'Open', '|',                    // Separator
    'Cut', 'Copy', 'Delete',
    '|',                            // Separator
    'Rename', 'Download',
    '|',                            // Separator
    'Details', 'Compress', 'Share'
  ]
}}
```

## Built-in Menu Items

| Item | Context | Description |
|------|---------|-------------|
| `Open` | File, Folder | Opens file or folder |
| `Cut` | File, Folder | Cuts the item |
| `Copy` | File, Folder | Copies the item |
| `Delete` | File, Folder | Deletes the item |
| `Rename` | File, Folder | Renames the item |
| `Download` | File, Folder | Downloads the item |
| `Details` | File, Folder, Layout | Shows item details |
| `NewFolder` | Layout | Creates new folder |
| `Upload` | Layout | Opens upload dialog |
| `SortBy` | Layout | Opens sort options |
| `View` | Layout | Changes view mode |
| `Refresh` | Layout | Refreshes file list |
| `SelectAll` | Layout | Selects all items |

## Related Topics

- [Customization](customization.md)
- [Adding Custom Item to Toolbar](adding-custom-item-to-toolbar.md)
- [File Operations](file-operations.md)
- [Getting Started](getting-started.md)
