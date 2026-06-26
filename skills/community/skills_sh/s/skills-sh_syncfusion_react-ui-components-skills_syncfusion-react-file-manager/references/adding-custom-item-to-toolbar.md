# Adding Custom Items to Toolbar in React File Manager

The toolbar in the React File Manager component can be extensively customized using `ToolbarItemsDirective` and `ToolbarItemDirective` components. You can modify default items, add custom items with templates, and control toolbar appearance and behavior.

## Table of Contents

1. [Toolbar Configuration](#toolbar-configuration)
2. [Modifying Default Items](#modifying-default-items)
3. [Adding Custom Items](#adding-custom-items)
4. [Custom Templates](#custom-templates)
5. [Toolbar Click Handling](#toolbar-click-handling)
6. [Complete Examples](#complete-examples)

## Toolbar Configuration

### Using toolbarSettings Property

```typescript
import React from 'react';
import { FileManagerComponent, Inject, NavigationPane, DetailsView, Toolbar } from '@syncfusion/ej2-react-filemanager';

function BasicToolbarExample() {
  const hostUrl = "url";
  
  return (
    <FileManagerComponent
      height="500px"
      view="Details"
      ajaxSettings={{
        url: hostUrl + 'api/FileManager/FileOperations',
        downloadUrl: hostUrl + 'api/FileManager/Download',
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        getImageUrl: hostUrl + 'api/FileManager/GetImage'
      }}
      toolbarSettings={{
        items: [
          'NewFolder', 'Upload', 'Delete', 'Cut', 'Copy', 'Paste',
          'Rename', 'SortBy', 'Refresh', 'Selection', 'View', 'Details'
        ]
      }}
    >
      <Inject services={[NavigationPane, DetailsView, Toolbar]} />
    </FileManagerComponent>
  );
}

export default BasicToolbarExample;
```

### Using ToolbarItemsDirective (Advanced)

```typescript
import React from 'react';
import {
  FileManagerComponent,
  Inject,
  NavigationPane,
  DetailsView,
  Toolbar,
  ToolbarItemsDirective,
  ToolbarItemDirective
} from '@syncfusion/ej2-react-filemanager';

function AdvancedToolbarExample() {
  const hostUrl = "url";
  
  return (
    <FileManagerComponent 
      height="500px" 
      view="Details"
      ajaxSettings={{
        url: hostUrl + 'api/FileManager/FileOperations',
        downloadUrl: hostUrl + 'api/FileManager/Download',
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        getImageUrl: hostUrl + 'api/FileManager/GetImage'
      }}
    >
      <ToolbarItemsDirective>
        <ToolbarItemDirective name="NewFolder" />
        <ToolbarItemDirective name="Upload" />
        <ToolbarItemDirective name="Delete" />
        <ToolbarItemDirective name="Cut" />
        <ToolbarItemDirective name="Copy" />
        <ToolbarItemDirective name="Paste" />
        <ToolbarItemDirective name="Rename" />
        <ToolbarItemDirective name="SortBy" />
        <ToolbarItemDirective name="View" />
        <ToolbarItemDirective name="Details" />
      </ToolbarItemsDirective>
      <Inject services={[NavigationPane, DetailsView, Toolbar]} />
    </FileManagerComponent>
  );
}

export default AdvancedToolbarExample;
```

## Modifying Default Items

### Pattern 1: Customize Item Text and Icon

```typescript
<ToolbarItemsDirective>
  <ToolbarItemDirective
    name="NewFolder"
    text="Create Folder"
    prefixIcon="e-plus"
    tooltipText="Create a new folder"
  />
  <ToolbarItemDirective
    name="Upload"
    text="Add Files"
    prefixIcon="e-upload"
    tooltipText="Upload files to this folder"
  />
  <ToolbarItemDirective
    name="Delete"
    text="Remove"
    prefixIcon="e-delete"
    tooltipText="Delete selected items"
  />
</ToolbarItemsDirective>
```

### Pattern 2: Reorder Toolbar Items

```typescript
<ToolbarItemsDirective>
  <ToolbarItemDirective name="Refresh" />
  <ToolbarItemDirective name="NewFolder" />
  <ToolbarItemDirective name="Upload" />
  <ToolbarItemDirective name="Cut" />
  <ToolbarItemDirective name="Copy" />
  <ToolbarItemDirective name="Paste" />
  <ToolbarItemDirective name="Delete" />
  <ToolbarItemDirective name="Rename" />
  <ToolbarItemDirective name="SortBy" />
  <ToolbarItemDirective name="View" />
  <ToolbarItemDirective name="Details" />
</ToolbarItemsDirective>
```

### Pattern 3: Hide/Show Items

```typescript
<ToolbarItemsDirective>
  <ToolbarItemDirective name="NewFolder" />
  <ToolbarItemDirective name="Upload" />
  <ToolbarItemDirective name="Delete" visible={userRole !== 'Viewer'} />
  <ToolbarItemDirective name="Rename" visible={userRole !== 'Viewer'} />
  <ToolbarItemDirective name="SortBy" />
  <ToolbarItemDirective name="Refresh" />
  <ToolbarItemDirective name="View" />
  <ToolbarItemDirective name="Details" />
</ToolbarItemsDirective>
```

## Adding Custom Items

### Pattern 1: Custom Button Item

```typescript
<ToolbarItemsDirective>
  <ToolbarItemDirective name="NewFolder" />
  <ToolbarItemDirective name="Upload" />
  <ToolbarItemDirective name="Separator" />
  <ToolbarItemDirective
    name="CustomAction"
    text="Custom Action"
    prefixIcon="e-execute"
    tooltipText="Perform custom action"
  />
  <ToolbarItemDirective name="Delete" />
  <ToolbarItemDirective name="Details" />
</ToolbarItemsDirective>
```

### Pattern 2: Custom Template Item (Checkbox)

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, ToolbarItemsDirective, ToolbarItemDirective } from '@syncfusion/ej2-react-filemanager';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';

function CheckboxToolbarExample() {
  const fileManagerRef = useRef(null);
  const checkboxRef = useRef(null);
  const hostUrl = "url";

  const handleCheckboxChange = (args) => {
    if (args.checked) {
      fileManagerRef.current?.selectAll();
      checkboxRef.current.label = 'Unselect All';
    } else {
      fileManagerRef.current?.clearSelection();
      checkboxRef.current.label = 'Select All';
    }
  };

  const checkboxTemplate = () => (
    <CheckBoxComponent
      ref={checkboxRef}
      label="Select All"
      checked={false}
      change={handleCheckboxChange}
    />
  );

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      height="500px"
      view="Details"
      ajaxSettings={{
        url: hostUrl + 'api/FileManager/FileOperations',
        downloadUrl: hostUrl + 'api/FileManager/Download',
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        getImageUrl: hostUrl + 'api/FileManager/GetImage'
      }}
    >
      <ToolbarItemsDirective>
        <ToolbarItemDirective name="NewFolder" />
        <ToolbarItemDirective name="Upload" />
        <ToolbarItemDirective name="Separator" />
        <ToolbarItemDirective
          name="SelectAll"
          template={checkboxTemplate}
        />
        <ToolbarItemDirective name="Separator" />
        <ToolbarItemDirective name="Delete" />
        <ToolbarItemDirective name="Details" />
      </ToolbarItemsDirective>
      <Inject services={[/* services */]} />
    </FileManagerComponent>
  );
}

export default CheckboxToolbarExample;
```

### Pattern 3: Custom Dropdown Item

```typescript
import React, { useRef } from 'react';
import { FileManagerComponent, Inject, ToolbarItemsDirective, ToolbarItemDirective } from '@syncfusion/ej2-react-filemanager';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

function DropdownToolbarExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";
  const fileTypesData = [
    { text: 'All Files', value: '*' },
    { text: 'Images', value: '*.jpg,*.png,*.gif' },
    { text: 'Documents', value: '*.pdf,*.docx,*.xlsx' },
    { text: 'Videos', value: '*.mp4,*.avi,*.mov' }
  ];

  const handleFilterChange = (args) => {
    // Apply filter based on selected file type
    console.log(`Filtering by: ${args.itemData?.text}`);
  };

  const dropdownTemplate = () => (
    <DropDownListComponent
      dataSource={fileTypesData}
      fields={{ text: 'text', value: 'value' }}
      change={handleFilterChange}
      placeholder="Filter by type"
      popupHeight="200px"
    />
  );

  return (
    <FileManagerComponent
      ref={fileManagerRef}
      height="500px"
      view="Details"
      ajaxSettings={{
        url: hostUrl + 'api/FileManager/FileOperations',
        downloadUrl: hostUrl + 'api/FileManager/Download',
        uploadUrl: hostUrl + 'api/FileManager/Upload',
        getImageUrl: hostUrl + 'api/FileManager/GetImage'
      }}
    >
      <ToolbarItemsDirective>
        <ToolbarItemDirective name="NewFolder" />
        <ToolbarItemDirective name="Upload" />
        <ToolbarItemDirective name="Separator" />
        <ToolbarItemDirective
          name="FilterType"
          text="Filter:"
          template={dropdownTemplate}
        />
        <ToolbarItemDirective name="Separator" />
        <ToolbarItemDirective name="Refresh" />
        <ToolbarItemDirective name="Details" />
      </ToolbarItemsDirective>
      <Inject services={[/* services */]} />
    </FileManagerComponent>
  );
}

export default DropdownToolbarExample;
```

## Toolbar Click Handling

### Pattern 1: Handle Toolbar Clicks

```typescript
function handleToolbarClick(args) {
  if (args.item.name === 'CustomAction') {
    performCustomAction();
  } else if (args.item.name === 'Share') {
    shareSelectedFiles();
  } else if (args.item.name === 'Archive') {
    archiveSelectedFiles();
  }
}

function performCustomAction() {
  console.log('Custom action performed');
  alert('Custom action executed');
}

function shareSelectedFiles() {
  const selectedItems = fileManagerRef.current?.getSelectedFiles();
  alert(`Sharing ${selectedItems?.length} items`);
}

function archiveSelectedFiles() {
  const selectedItems = fileManagerRef.current?.getSelectedFiles();
  alert(`Archiving ${selectedItems?.length} items`);
}
```

### Pattern 2: Enable/Disable Toolbar Items

```typescript
import React, { useRef } from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { FileManagerComponent, Inject } from '@syncfusion/ej2-react-filemanager';

function EnableDisableToolbarExample() {
  const fileManagerRef = useRef(null);
  const hostUrl = "url";

  const handleEnableDelete = () => {
    fileManagerRef.current?.enableToolbarItems(['delete']);
    alert('Delete toolbar item enabled');
  };

  const handleDisableDelete = () => {
    fileManagerRef.current?.disableToolbarItems(['delete']);
    alert('Delete toolbar item disabled');
  };

  return (
    <div>
      <div className="button-group">
        <ButtonComponent onClick={handleEnableDelete}>
          Enable Delete
        </ButtonComponent>
        <ButtonComponent onClick={handleDisableDelete}>
          Disable Delete
        </ButtonComponent>
      </div>

      <FileManagerComponent
        ref={fileManagerRef}
        height="500px"
        view="Details"
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        toolbarSettings={{
          items: ['NewFolder', 'Upload', 'Delete', 'Refresh', 'Details']
        }}
      >
        <Inject services={[/* services */]} />
      </FileManagerComponent>
    </div>
  );
}

export default EnableDisableToolbarExample;
```

## Complete Examples

### Full Implementation with Custom Toolbar

```typescript
import React, { useRef } from 'react';
import {
  FileManagerComponent,
  Inject,
  NavigationPane,
  DetailsView,
  Toolbar,
  ToolbarItemsDirective,
  ToolbarItemDirective
} from '@syncfusion/ej2-react-filemanager';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function AdvancedToolbarCustomization() {
  const fileManagerRef = useRef(null);
  const checkboxRef = useRef(null);
  const hostUrl = "url";

  const handleCheckboxChange = (args) => {
    if (args.checked) {
      fileManagerRef.current?.selectAll();
      checkboxRef.current.label = 'Unselect All';
    } else {
      fileManagerRef.current?.clearSelection();
      checkboxRef.current.label = 'Select All';
    }
  };

  const handleToolbarClick = (args) => {
    const selectedItems = fileManagerRef.current?.getSelectedFiles();
    
    switch (args.item.name) {
      case 'Compress':
        handleCompress(selectedItems);
        break;
      
      case 'Share':
        handleShare(selectedItems);
        break;
      
      case 'Encrypt':
        handleEncrypt(selectedItems);
        break;
      
      case 'Properties':
        handleProperties(selectedItems);
        break;
      
      default:
        console.log(`Toolbar action: ${args.item.name}`);
    }
  };

  const handleCompress = (items) => {
    alert(`Compressing ${items?.length} items...`);
  };

  const handleShare = (items) => {
    alert(`Sharing ${items?.length} items...`);
  };

  const handleEncrypt = (items) => {
    alert(`Encrypting ${items?.length} items...`);
  };

  const handleProperties = (items) => {
    if (items?.length === 1) {
      alert(`Properties of ${items[0]}`);
    } else {
      alert('Please select a single item');
    }
  };

  const checkboxTemplate = () => (
    <CheckBoxComponent
      ref={checkboxRef}
      label="Select All"
      checked={false}
      change={handleCheckboxChange}
    />
  );

  const refreshButtonTemplate = () => (
    <TooltipComponent content="Refresh the file list">
      <ButtonComponent
        onClick={() => fileManagerRef.current?.refreshFiles()}
        cssClass="e-small"
        iconCss="e-icons e-refresh"
      />
    </TooltipComponent>
  );

  return (
    <div className="control-section">
      <FileManagerComponent
        ref={fileManagerRef}
        id="advanced-toolbar"
        height="500px"
        view="Details"
        ajaxSettings={{
          url: hostUrl + 'api/FileManager/FileOperations',
          downloadUrl: hostUrl + 'api/FileManager/Download',
          uploadUrl: hostUrl + 'api/FileManager/Upload',
          getImageUrl: hostUrl + 'api/FileManager/GetImage'
        }}
        toolbarClick={handleToolbarClick}
      >
        <ToolbarItemsDirective>
          <ToolbarItemDirective
            name="NewFolder"
            text="New Folder"
            prefixIcon="e-folder-new"
            tooltipText="Create new folder"
          />
          <ToolbarItemDirective
            name="Upload"
            text="Upload"
            prefixIcon="e-upload"
            tooltipText="Upload files"
          />
          <ToolbarItemDirective name="Separator" />
          <ToolbarItemDirective
            name="SelectAll"
            template={checkboxTemplate}
          />
          <ToolbarItemDirective name="Separator" />
          <ToolbarItemDirective
            name="Delete"
            text="Delete"
            prefixIcon="e-delete"
            tooltipText="Delete selected items"
          />
          <ToolbarItemDirective
            name="Compress"
            text="Compress"
            prefixIcon="e-redo"
            tooltipText="Compress selected items"
          />
          <ToolbarItemDirective
            name="Share"
            text="Share"
            prefixIcon="e-share"
            tooltipText="Share selected items"
          />
          <ToolbarItemDirective
            name="Encrypt"
            text="Encrypt"
            prefixIcon="e-lock"
            tooltipText="Encrypt selected items"
          />
          <ToolbarItemDirective name="Separator" />
          <ToolbarItemDirective
            name="Refresh"
            template={refreshButtonTemplate}
          />
          <ToolbarItemDirective
            name="View"
            prefixIcon="e-view"
          />
          <ToolbarItemDirective
            name="Details"
            text="Details"
            prefixIcon="e-info"
            tooltipText="Show details"
          />
        </ToolbarItemsDirective>
        <Inject services={[NavigationPane, DetailsView, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default AdvancedToolbarCustomization;
```

## Toolbar Item Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Unique identifier for toolbar item |
| `text` | string | Display text for the item |
| `prefixIcon` | string | Icon class for item |
| `suffixIcon` | string | Suffix icon for item |
| `tooltipText` | string | Tooltip text on hover |
| `template` | function/JSX | Custom template for item |
| `visible` | boolean | Show/hide the item |
| `id` | string | HTML id attribute |
| `cssClass` | string | Custom CSS class |

## Built-in Toolbar Items

| Item Name | Icon | Description |
|-----------|------|-------------|
| `NewFolder` | e-folder-new | Create new folder |
| `Upload` | e-upload | Upload files |
| `Cut` | e-cut | Cut selected items |
| `Copy` | e-copy | Copy selected items |
| `Paste` | e-paste | Paste items |
| `Delete` | e-delete | Delete selected items |
| `Rename` | e-rename | Rename selected item |
| `Refresh` | e-refresh | Refresh file list |
| `SortBy` | e-sort | Sort options |
| `View` | e-view | Change view mode |
| `Details` | e-details | Show details |
| `Download` | e-download | Download selected items |
| `Selection` | e-selection | Selection options |
| `Separator` | - | Visual separator |

## Related Topics

- [Adding Custom Item to Context Menu](adding-custom-item-to-context-menu.md)
- [Enable Disable Toolbar Item](enable-disable-toolbar-item.md)
- [Customization](customization.md)
- [File Operations](file-operations.md)
