# Customization

Customize appearance, themes, toolbars, context menus, and component structure.

## Table of Contents

1. [CSS Theming](#css-theming)
2. [Toolbar Customization](#toolbar-customization)
3. [Context Menu Customization](#context-menu-customization)
4. [View Customization](#view-customization)
5. [Complete Example](#complete-example)

## CSS Theming

### Built-in Themes

Syncfusion File Manager includes Material, Bootstrap, Bootstrap4, Fabric, and Tailwind themes:

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

// Import theme CSS
import '@syncfusion/ej2-react-filemanager/styles/material.css';
// Or other themes:
// import '@syncfusion/ej2-react-filemanager/styles/bootstrap.css';
// import '@syncfusion/ej2-react-filemanager/styles/bootstrap4.css';
// import '@syncfusion/ej2-react-filemanager/styles/fabric.css';
// import '@syncfusion/ej2-react-filemanager/styles/tailwind.css';

function ThemedFileManager() {
  return (
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
  );
}

export default ThemedFileManager;
```

**Available Themes:**
- Material (Default, Modern design)
- Bootstrap (Bootstrap styling)
- Bootstrap4 (Bootstrap 4 styling)
- Fabric (Fluent Design)
- Tailwind (Tailwind CSS compatible)

### CSS Variables

Override default colors with CSS custom properties:

```css
/* styles/custom-theme.css */
:root {
  --ej2-fm-toolbar-bg: #3f51b5;
  --ej2-fm-toolbar-text: #ffffff;
  --ej2-fm-selection-bg: #e3f2fd;
  --ej2-fm-border: #e0e0e0;
  --ej2-fm-hover-bg: #f5f5f5;
}

.e-filemanager {
  --ej2-fm-hover-bg: #f0f4ff;
}
```

Usage:

```tsx
import React from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';
import './styles/custom-theme.css';

function CustomTheme() {
  return <FileManagerComponent {...props} />;
}

export default CustomTheme;
```

## Toolbar Customization

### Configure Toolbar Items

```tsx
import React from 'react';
import { FileManagerComponent, Inject, Toolbar } from '@syncfusion/ej2-react-filemanager';

function CustomToolbar() {
  const toolbarSettings = {
    items: [
      'NewFolder',
      'Upload',
      'Delete',
      'Download',
      'Rename',
      'SortBy',
      'Refresh',
      'Selection',
      'View',
      'Details'
    ]
  };

  return (
    <FileManagerComponent
      toolbarSettings={toolbarSettings}
      ajaxSettings={{...}}
    >
      <Inject services={[Toolbar]} />
    </FileManagerComponent>
  );
}

export default CustomToolbar;
```

**Available Items:**
- NewFolder, Upload, Delete, Download, Rename
- SortBy, Refresh, Selection, View, Details
- Custom items (see below)

### Add Custom Toolbar Items

```tsx
const toolbarSettings = {
  items: [
    'NewFolder',
    'Upload',
    { 
      name: 'Share',
      text: 'Share',
      icon: 'e-icons e-share',
      id: 'share-btn'
    },
    'Delete',
    'Download'
  ]
};

const handleToolbarClick = (args) => {
  if (args.item.id === 'share-btn') {
    console.log('Share button clicked');
    // Open share dialog
  }
};

<FileManagerComponent
  toolbarSettings={toolbarSettings}
  toolbarClick={handleToolbarClick}
  ajaxSettings={{...}}
>
  <Inject services={[Toolbar]} />
</FileManagerComponent>
```

## Context Menu Customization

### Configure Context Menu Items

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane } from '@syncfusion/ej2-react-filemanager';

function CustomContextMenu() {
  const contextMenuSettings = {
    file: [
      'Open',
      'Edit',
      'Download',
      'Cut',
      'Copy',
      'Delete',
      'Rename',
      'Properties'
    ],
    folder: [
      'Open',
      'Cut',
      'Copy',
      'Delete',
      'Rename',
      'NewFolder',
      'Properties'
    ]
  };

  return (
    <FileManagerComponent
      contextMenuSettings={contextMenuSettings}
      ajaxSettings={{...}}
    >
      <Inject services={[DetailsView, NavigationPane]} />
    </FileManagerComponent>
  );
}

export default CustomContextMenu;
```

### Add Custom Menu Items

```tsx
const contextMenuSettings = {
  file: [
    'Download',
    'Cut',
    'Copy',
    'Delete',
    { text: 'Compress', id: 'compress' },
    { text: 'Encrypt', id: 'encrypt' }
  ]
};

const handleMenuClick = (args) => {
  if (args.item.id === 'compress') {
    console.log('Compress:', args.fileDetails);
    // Call compress API
  } else if (args.item.id === 'encrypt') {
    console.log('Encrypt:', args.fileDetails);
    // Call encrypt API
  }
};

<FileManagerComponent
  contextMenuSettings={contextMenuSettings}
  menuClick={handleMenuClick}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane]} />
</FileManagerComponent>
```

## View Customization

### Details View Settings

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView } from '@syncfusion/ej2-react-filemanager';

function CustomDetailsView() {
  const detailsViewSettings = {
    columns: [
      { field: 'name', headerText: 'Name', width: '200px' },
      { field: 'dateModified', headerText: 'Modified', width: '150px' },
      { field: 'size', headerText: 'Size', width: '100px' },
      { field: 'type', headerText: 'Type', width: '100px' }
    ]
  };

  return (
    <FileManagerComponent
      view="Details"
      detailsViewSettings={detailsViewSettings}
      ajaxSettings={{...}}
    >
      <Inject services={[DetailsView]} />
    </FileManagerComponent>
  );
}

export default CustomDetailsView;
```

### Navigation Pane Settings

```tsx
const navigationPaneSettings = {
  maxWidth: '300px',
  minWidth: '150px',
  expandedWidth: '250px'
};

<FileManagerComponent
  navigationPaneSettings={navigationPaneSettings}
  ajaxSettings={{...}}
>
  <Inject services={[NavigationPane]} />
</FileManagerComponent>
```

## Complete Example

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';
import '@syncfusion/ej2-react-filemanager/styles/material.css';
import './custom-theme.css';

function FullyCustomizedFileManager() {
  const toolbarSettings = {
    items: [
      'NewFolder',
      'Upload',
      { text: 'Archive', id: 'archive' },
      { text: 'Share', id: 'share' },
      'Delete',
      'Download',
      'Refresh'
    ]
  };

  const contextMenuSettings = {
    file: ['Download', 'Cut', 'Copy', 'Delete', { text: 'Compress', id: 'compress' }],
    folder: ['Open', 'Cut', 'Copy', 'Delete', 'Rename']
  };

  const detailsViewSettings = {
    columns: [
      { field: 'name', headerText: 'File Name', width: '300px' },
      { field: 'dateModified', headerText: 'Date Modified', width: '200px' },
      { field: 'size', headerText: 'File Size', width: '150px' }
    ]
  };

  const navigationPaneSettings = {
    maxWidth: '350px'
  };

  const handleToolbarClick = (args) => {
    if (args.item.id === 'archive') {
      alert('Archive selected files');
    } else if (args.item.id === 'share') {
      alert('Share selected files');
    }
  };

  const handleMenuClick = (args) => {
    if (args.item.id === 'compress') {
      alert('Compress: ' + args.fileDetails[0].name);
    }
  };

  return (
    <FileManagerComponent
      view="Details"
      sortBy="name"
      sortOrder="Ascending"
      toolbarSettings={toolbarSettings}
      contextMenuSettings={contextMenuSettings}
      detailsViewSettings={detailsViewSettings}
      navigationPaneSettings={navigationPaneSettings}
      toolbarClick={handleToolbarClick}
      menuClick={handleMenuClick}
      ajaxSettings={{
        url: "url",
        getImageUrl: "url",
        uploadUrl: "url",
        downloadUrl: "url"
      }}
      height="700px"
      cssClass="custom-file-manager"
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default FullyCustomizedFileManager;
```

## Common Patterns

### Dark Theme

```css
:root {
  --ej2-fm-bg: #1e1e1e;
  --ej2-fm-text: #ffffff;
  --ej2-fm-toolbar-bg: #2d2d2d;
  --ej2-fm-border: #404040;
  --ej2-fm-hover-bg: #3a3a3a;
}

.dark-mode .e-filemanager {
  background: var(--ej2-fm-bg);
  color: var(--ej2-fm-text);
}
```

### Compact View

```tsx
const compactSettings = {
  detailsViewSettings: {
    columns: [
      { field: 'name', headerText: 'Name', width: '250px' },
      { field: 'size', headerText: 'Size', width: '80px' }
    ]
  },
  navigationPaneSettings: {
    maxWidth: '200px'
  },
  height: '400px'
};
```

### Mobile-Responsive

```tsx
<FileManagerComponent
  view={window.innerWidth < 768 ? 'LargeIcons' : 'Details'}
  navigationPaneSettings={{
    maxWidth: window.innerWidth < 768 ? '150px' : '250px'
  }}
  height={window.innerHeight - 100 + 'px'}
  ajaxSettings={{...}}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Next Steps

- **Drag-and-Drop:** Master drag operations in [drag-and-drop.md](drag-and-drop.md)
- **Accessibility:** WCAG compliance in [accessibility-localization.md](accessibility-localization.md)
- **Advanced:** Performance and custom providers in [advanced-features.md](advanced-features.md)
