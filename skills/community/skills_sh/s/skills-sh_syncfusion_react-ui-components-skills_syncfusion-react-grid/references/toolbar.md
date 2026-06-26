# Toolbar in React Grid

## Table of Contents
- [Overview](#overview)
- [Mandatory Rules](#mandatory-rules)
- [Built-in Toolbar Items](#built-in-toolbar-items)
- [Custom Toolbar](#custom-toolbar)
- [Event Handling](#event-handling)

## Overview

The toolbar provides quick access to common grid operations like CRUD, export, and custom actions.

## Mandatory Rules
 
### Rule 1: GridComponent ID is REQUIRED for Toolbar Click Events (Export/Import)
 
When using toolbar click events to handle export (Excel, PDF) or custom actions, you **MUST** provide an `id` attribute on the `<GridComponent>` element.
 
❌ **WRONG** - No ID, toolbar event cannot find the grid:
```tsx
<GridComponent dataSource={data} toolbar={['ExcelExport', 'PdfExport']}>
  {/* columns */}
  <Inject services={[Toolbar, ExcelExport, PdfExport]} />
</GridComponent>
```
 
✅ **CORRECT** - ID attribute provided:
```tsx
<GridComponent
  id='grid'
  dataSource={data}
  toolbar={['ExcelExport', 'PdfExport']}
  toolbarClick={onToolbarClick}
>
  {/* columns */}
  <Inject services={[Toolbar, ExcelExport, PdfExport]} />
</GridComponent>
```

## Built-in Toolbar Items

### Add Standard Toolbar

```tsx
import { GridComponent, Inject, Toolbar } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
  <Inject services={[Toolbar, Edit]} />
</GridComponent>
```

### Available Toolbar Items

```tsx
const toolbarItems = [
  'Add',           // Add new record
  'Edit',          // Edit selected record
  'Delete',        // Delete selected record
  'Update',        // Save changes
  'Cancel',        // Cancel editing
  'Search',        // Search box
  'ExcelExport',   // Export to Excel
  'PdfExport',     // Export to PDF
  'CsvExport',     // Export to CSV
  'Print'          // Print grid
];

<GridComponent toolbar={toolbarItems}>
  {/* columns */}
  <Inject services={[Toolbar, Edit, ExcelExport, PdfExport]] />
</GridComponent>
```

### Edit Toolbar Setup

```tsx
<GridComponent
  dataSource={data}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'Search']}
  editSettings={{ mode: 'Dialog', allowEditing: true, allowAdding: true, allowDeleting: true }}
>
  {/* columns */}
  <Inject services={[Toolbar, Edit] }/>
</GridComponent>
```

## Custom Toolbar

### Add Custom Button

```tsx
const customToolbar = [
  'Add',
  'Edit',
  'Delete',
  {
    text: 'Refresh',
    tooltipText: 'Refresh Data',
    prefixIcon: 'e-icons e-refresh',
    id: 'grid-refresh',
    align: 'Right'
  }
];

const toolbarClick = (args) => {
  if (args.item.id === 'grid-refresh') {
    gridRef.current.refresh();
  }
};

<GridComponent
  toolbar={customToolbar}
  toolbarClick={toolbarClick}
>
  {/* columns */}
  <Inject services={[Toolbar]} />
</GridComponent>
```

### Custom React Component in Toolbar

```tsx
const CustomToolbar = () => {
  return (
    <div className='e-toolbar-items'>
      <button className='e-btn'>
        <span className='e-btn-icon e-icons e-add-new'></span>
        Add New
      </button>
      <button className='e-btn'>
        <span className='e-btn-icon e-icons e-refresh'></span>
        Refresh
      </button>
    </div>
  );
};

<GridComponent
  toolbarTemplate={CustomToolbar}
>
  {/* columns */}
</GridComponent>
```

### Template-Based Toolbar

```tsx
const toolbarTemplate = () => {
  return (
    <div style={{ display: 'flex', gap: '10px' }}>
      <input
        type='text'
        placeholder='Quick Search...'
        onChange={(e) => gridRef.current.search(e.target.value)}
      />
      <button onClick={() => gridRef.current.refresh()}>
        Refresh
      </button>
      <button onClick={() => gridRef.current.excelExport()}>
        Export
      </button>
    </div>
  );
};

<GridComponent
  dataSource={data}
  toolbarTemplate={toolbarTemplate}
>
  {/* columns */}
</GridComponent>
```

## Event Handling

### Handle Toolbar Click Events

```tsx
const toolbarClick = (args) => {
  if (args.item.text === 'Add') {
    console.log('Add button clicked');
  }
  if (args.item.text === 'Delete') {
    console.log('Delete button clicked');
  }
  if (args.item.id === 'grid-search') {
    console.log('Search:', args.value);
  }
};

<GridComponent
  toolbar={['Add', 'Edit', 'Delete', 'Search']}
  toolbarClick={toolbarClick}
>
  {/* columns */}
  <Inject services={[Toolbar, Edit]} />
</GridComponent>
```

### Disable Toolbar Items

```tsx
const onActionComplete = (args) => {
  if (args.requestType === 'save') {
    // Disable delete after save
    gridRef.current.toolbarModule.enableItems(['Delete'], false);
  }
};

<GridComponent
  dataSource={data}
  actionComplete={onActionComplete}
>
  {/* columns */}
</GridComponent>
```

### Conditional Toolbar Items

```tsx
const getToolbarItems = () => {
  const items = ['Add', 'Edit'];
  
  if (userRole === 'admin') {
    items.push('Delete');
  }
  
  items.push('Search', 'ExcelExport');
  return items;
};

<GridComponent toolbar={getToolbarItems()}>
  {/* columns */}
</GridComponent>
```

## Advanced Toolbar Patterns

### Role-Based Conditional Toolbar

```tsx
function GridWithRoleBasedToolbar() {
  const [userRole, setUserRole] = useState('viewer');

  const getToolbarItems = () => {
    const baseItems = ['Search'];
    
    if (userRole === 'editor') {
      return ['Add', 'Edit', 'Delete', ...baseItems, 'ExcelExport'];
    }
    
    if (userRole === 'admin') {
      return ['Add', 'Edit', 'Delete', ...baseItems, 'ExcelExport', 'PdfExport', 'CsvExport'];
    }
    
    return [...baseItems, 'ExcelExport']; // viewer only
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <label>User Role: </label>
        <select value={userRole} onChange={(e) => setUserRole(e.target.value)}>
          <option>viewer</option>
          <option>editor</option>
          <option>admin</option>
        </select>
      </div>
      <GridComponent
        dataSource={data}
        toolbar={getToolbarItems()}
        editSettings={{ mode: 'Dialog', allowEditing: true, allowAdding: true, allowDeleting: true }}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='Freight' headerText='Freight' format='C2' />
        </ColumnsDirective>
        <Inject services={[Toolbar, Edit, ExcelExport, PdfExport]} />
      </GridComponent>
    </div>
  );
}

export default GridWithRoleBasedToolbar;
```

### Custom Toolbar with State Management

```tsx
function GridWithCustomToolbar() {
  const gridRef = useRef(null);
  const [selectedCount, setSelectedCount] = useState(0);

  const customToolbar = [
    {
      text: 'Add Order',
      prefixIcon: 'e-icons e-add-new',
      id: 'custom-add',
      align: 'Left'
    },
    {
      text: 'Delete Selected',
      prefixIcon: 'e-icons e-delete',
      id: 'custom-delete',
      align: 'Left'
    },
    {
      text: 'Refresh Data',
      prefixIcon: 'e-icons e-refresh',
      id: 'custom-refresh',
      align: 'Right'
    },
    {
      text: 'Export',
      prefixIcon: 'e-icons e-export-excel',
      id: 'custom-export',
      align: 'Right'
    }
  ];

  const handleToolbarClick = (args) => {
    if (args.item.id === 'custom-add') {
      gridRef.current.addRecord();
    } else if (args.item.id === 'custom-delete') {
      const selectedRecords = gridRef.current.getSelectedRecords();
      if (selectedRecords.length > 0) {
        gridRef.current.deleteRecord(selectedRecords);
      }
    } else if (args.item.id === 'custom-refresh') {
      gridRef.current.refresh();
    } else if (args.item.id === 'custom-export') {
      gridRef.current.excelExport();
    }
  };

  const onRecordSelectionChange = (args) => {
    setSelectedCount(gridRef.current.getSelectedRowIndexes().length);
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      toolbar={customToolbar}
      toolbarClick={handleToolbarClick}
      allowSelection={true}
      selectionSettings={{ type: 'Multiple', mode: 'Row' }}
      rowSelected={onRecordSelectionChange}
      editSettings={{ mode: 'Dialog', allowEditing: true, allowAdding: true, allowDeleting: true }}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' />
      </ColumnsDirective>
      <Inject services={[Toolbar, Edit, Selection, ExcelExport]} />
    </GridComponent>
  );
}

export default GridWithCustomToolbar;
```

### Toolbar Styling and Customization

```tsx
// Custom CSS for toolbar styling
const toolbarStyles = `
  .e-toolbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: 3px solid #764ba2;
    padding: 12px 20px;
  }

  .e-toolbar .e-btn {
    background-color: white;
    color: #667eea;
    border: 1px solid #667eea;
    border-radius: 4px;
    margin: 0 5px;
    padding: 8px 16px;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .e-toolbar .e-btn:hover {
    background-color: #667eea;
    color: white;
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
  }

  .e-toolbar .e-btn.e-active {
    background-color: #667eea;
    color: white;
  }

  .e-toolbar .e-btn-icon {
    margin-right: 6px;
  }

  .e-toolbar-separator {
    background-color: rgba(255, 255, 255, 0.3);
    margin: 0 10px;
  }
`;

function GridWithStyledToolbar() {
  return (
    <>
      <style>{toolbarStyles}</style>
      <GridComponent
        dataSource={data}
        toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel', '|', 'ExcelExport', 'PdfExport', 'Print']}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        </ColumnsDirective>
        <Inject services={[Toolbar, Edit, ExcelExport, PdfExport, Print]} />
      </GridComponent>
    </>
  );
}

export default GridWithStyledToolbar;
```

### Toolbar with Search and Filter

```tsx
function GridWithSearchToolbar() {
  const gridRef = useRef(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterColumn, setFilterColumn] = useState('CustomerID');

  const customToolbar = () => {
    return (
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center', padding: '10px 0' }}>
        <select 
          value={filterColumn}
          onChange={(e) => setFilterColumn(e.target.value)}
          style={{ padding: '6px 10px', borderRadius: '4px', border: '1px solid #ccc' }}
        >
          <option value='CustomerID'>Customer ID</option>
          <option value='OrderID'>Order ID</option>
          <option value='ShipCountry'>Ship Country</option>
        </select>
        <input
          type='text'
          placeholder={`Search in ${filterColumn}...`}
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            gridRef.current.search(e.target.value);
          }}
          style={{ 
            padding: '6px 10px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            width: '250px'
          }}
        />
        <button 
          onClick={() => {
            setSearchTerm('');
            gridRef.current.clearFiltering();
          }}
          style={{
            padding: '6px 12px',
            borderRadius: '4px',
            border: 'none',
            background: '#f44336',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          Clear
        </button>
      </div>
    );
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      toolbarTemplate={customToolbar}
      allowSearching={true}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='ShipCountry' headerText='Ship Country' width='150' />
      </ColumnsDirective>
      <Inject services={[Toolbar, Search]} />
    </GridComponent>
  );
}

export default GridWithSearchToolbar;
```
