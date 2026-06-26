# Context Menu in React Grid

## Table of Contents
- [Overview](#overview)
- [Built-in Context Menu](#built-in-context-menu)
- [Custom Context Menu](#custom-context-menu)
- [Event Handling](#event-handling)

## Overview

Context menu provides quick access to common operations when right-clicking on grid cells or rows.

## Built-in Context Menu

### Enable Context Menu

```tsx
import { GridComponent, Inject, ContextMenu } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} contextMenuItems={['Copy', 'ExcelExport', 'PdfExport']}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
  <Inject services={[ContextMenu]} />
</GridComponent>
```

### Built-in Menu Items

```tsx
const contextMenuItems = [
  'Copy',              // Copy selected cells
  'CopyWithHeader',    // Copy with column headers
  'ExcelExport',       // Export selection to Excel
  'PdfExport',         // Export selection to PDF
  'CsvExport',         // Export selection to CSV
  'Edit',              // Edit selected row
  'Delete',            // Delete selected row
  'Save',              // Save edited row
  'Cancel',            // Cancel editing
  'PdfExport',
  'ExcelExport'
];

<GridComponent contextMenuItems={contextMenuItems}>
  {/* columns */}
  <Inject services={[ContextMenu, Edit, ExcelExport, PdfExport]} />
</GridComponent>
```

## Custom Context Menu

### Add Custom Menu Items

```tsx
const customContextMenu = [
  {
    text: 'Copy',
    target: '.e-gridcontent',
    id: 'grid-copy'
  },
  {
    text: 'View Details',
    target: '.e-gridcontent',
    id: 'grid-details'
  },
  {
    text: 'Send Email',
    target: '.e-gridcontent',
    id: 'grid-email'
  },
  {
    text: 'Generate Report',
    target: '.e-gridcontent',
    id: 'grid-report'
  }
];

<GridComponent
  dataSource={data}
  contextMenuItems={customContextMenu}
  contextMenuClick={handleContextMenuClick}
>
  {/* columns */}
  <Inject services={[ContextMenu]} />
</GridComponent>
```

### Context Menu with Icons

```tsx
const contextMenuItems = [
  {
    text: 'Copy',
    iconCss: 'e-icons e-copy',
    target: '.e-gridcontent',
    id: 'grid-copy'
  },
  {
    text: 'Edit',
    iconCss: 'e-icons e-edit',
    target: '.e-gridcontent',
    id: 'grid-edit'
  },
  {
    text: 'Delete',
    iconCss: 'e-icons e-delete',
    target: '.e-gridcontent',
    id: 'grid-delete'
  }
];

<GridComponent contextMenuItems={contextMenuItems}>
  {/* columns */}
</GridComponent>
```

### Submenu Items

```tsx
const contextMenuItems = [
  {
    text: 'Export',
    id: 'grid-export',
    items: [
      { text: 'Excel', id: 'grid-excel' },
      { text: 'PDF', id: 'grid-pdf' },
      { text: 'CSV', id: 'grid-csv' }
    ]
  },
  {
    text: 'Tools',
    id: 'grid-tools',
    items: [
      { text: 'Sort', id: 'grid-sort' },
      { text: 'Filter', id: 'grid-filter' }
    ]
  }
];

<GridComponent contextMenuItems={contextMenuItems}>
  {/* columns */}
</GridComponent>
```

## Event Handling

### Handle Context Menu Click

```tsx
const contextMenuClick = (args) => {
  if (args.item.id === 'grid-copy') {
    // Custom copy logic
    console.log('Copying selected data...');
  }
  
  if (args.item.id === 'grid-details') {
    // Show details dialog
    const selectedRecord = gridRef.current.getSelectedRecords()[0];
    showDetailsDialog(selectedRecord);
  }

  if (args.item.id === 'grid-email') {
    // Send email logic
    const selectedRecord = gridRef.current.getSelectedRecords()[0];
    sendEmailTo(selectedRecord.CustomerID);
  }
};

<GridComponent
  dataSource={data}
  contextMenuItems={customMenu}
  contextMenuClick={contextMenuClick}
>
  {/* columns */}
  <Inject services={[ContextMenu]} />
</GridComponent>
```

### Context Menu Before Open

```tsx
const beforeOpen = (args) => {
  console.log('Context menu opening at:', args.top, args.left);
  
  // Conditionally show/hide items
  const hasSelection = gridRef.current.getSelectedRows().length > 0;
  // args.items can be modified here
};

<GridComponent
  dataSource={data}
  beforeOpen={beforeOpen}
  contextMenuItems={contextMenuItems}
>
  {/* columns */}
  <Inject services={[ContextMenu]} />
</GridComponent>
```

### Programmatic Context Menu Trigger

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const triggerContextMenu = (e) => {
    // Right-click triggers context menu automatically
    // Or programmatically:
    // gridRef.current.contextMenuModule.contextMenu.show(e);
  };

  return (
    <GridComponent ref={gridRef} dataSource={data}>
      {/* columns */}
      <Inject services={[ContextMenu]} />
    </GridComponent>
  );
}

export default App;
```
