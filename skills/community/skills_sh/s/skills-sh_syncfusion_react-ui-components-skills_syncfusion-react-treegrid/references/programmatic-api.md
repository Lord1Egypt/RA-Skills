---
name: programmatic-api
description: 'Programmatic API methods for TreeGrid - imperative operations, ref usage, and dynamic control.'
---

# Programmatic API

## Table of Contents
- [Component Properties](#component-properties)
- [Using Refs for Imperative Operations](#using-refs-for-imperative-operations)
- [Core Methods Data Operations](#core-methods-data-operations)
- [Complete Examples Data Operations](#complete-examples-data-operations)
- [Best Practices](#best-practices)

## Component Properties

### Basic Properties

```typescript
// DataSource
[dataSource]: Object[] | DataManager;

// Display
[rowHeight]: number; // Default: 36
[height]: string | number;
[width]: string | number;

// Features
[allowSelection]: boolean; // Default: true
[allowSorting]: boolean; // Default: false
[allowFiltering]: boolean; // Default: false
[allowPaging]: boolean; // Default: false
[allowRowDragAndDrop]: boolean; // Default: false
[allowExcelExport]: boolean; // Default: false
[allowPdfExport]: boolean; // Default: false
[enableVirtualization]: boolean; // Default: false
[enableColumnVirtualization]: boolean; // Default: false

// Child Records
[childMapping]: string; // Property name for child records
[parentValueMapping]: string; // Foreign key mapping
[expandStateMapping]: string; // Property name for expand state

// Primary Key
[idMapping]: string; // Unique identifier field
```

### Selection and Behavior

```typescript
[selectionSettings]: SelectionSettings;
// {
//   type: 'Single' | 'Multiple' | 'Checkbox'
//   mode: 'Row' | 'Cell' | 'Both'
//   cellSelectionMode: 'Flow' | 'Box' | 'BoxMultiSelect'
// }

[gridLines]: 'Both' | 'Horizontal' | 'Vertical' | 'None';
[rowTemplate]: string | Function; // Custom row template
[detailTemplate]: string | Function; // Expand/Detail template
[toolbarItems]: Object[] | string[]; // Toolbar items
[contextMenuItems]: Object[] | string[]; // Context menu items
```


## Using Refs for Imperative Operations

```tsx
import { useRef } from 'react';
import { TreeGridComponent } from '@syncfusion/ej2-react-treegrid';

function TreeGridExample() {
  const treeGridRef = useRef<TreeGridComponent>(null);

  const handleExport = () => {
    treeGridRef.current?.excelExport();
  };

  return (
    <>
      <button onClick={handleExport}>Export to Excel</button>
      <TreeGridComponent ref={treeGridRef} dataSource={data} />
    </>
  );
}
```

## Core Methods

### Data Operations

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `refresh()` | None | Refresh entire grid | `treeGridRef.current.refresh()` |
| `refreshColumns()` | None | Refresh columns only | `treeGridRef.current.refreshColumns()` |
| `addRecord(data, index, position)` | `data`: object, `index?`: number, `position?`: string | Add new record | `treeGridRef.current.addRecord({TaskID: 5, TaskName: 'New'}, 2, 'Below')` |
| `deleteRecord(fieldName, data)` | `fieldName`: string, `data`: object | Delete record | `treeGridRef.current.deleteRecord('TaskID', selectedRow)` |
| `updateRow(index, data)` | `index`: number, `data`: object | Update row | `treeGridRef.current.updateRow(2, updatedData)` |

### Tree Operations

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `expandRow(row)` | `row`: Element | Expand specific row | `treeGridRef.current.expandRow(rowElement)` |
| `collapseRow(row)` | `row`: Element | Collapse specific row | `treeGridRef.current.collapseRow(rowElement)` |
| `expandAll()` | None | Expand all rows | `treeGridRef.current.expandAll()` |
| `collapseAll()` | None | Collapse all rows | `treeGridRef.current.collapseAll()` |
| `expandAtLevel(level)` | `level`: number | Expand to level | `treeGridRef.current.expandAtLevel(2)` |
| `collapseAtLevel(level)` | `level`: number | Collapse from level | `treeGridRef.current.collapseAtLevel(2)` |

### Selection Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `selectRow(index)` | `index`: number | Select row by index | `treeGridRef.current.selectRow(3)` |
| `selectRows(indexes)` | `indexes`: number[] | Select multiple rows | `treeGridRef.current.selectRows([1, 3, 5])` |
| `clearSelection()` | None | Clear all selections | `treeGridRef.current.clearSelection()` |
| `getSelectedRows()` | None | Get selected row elements | `const rows = treeGridRef.current.getSelectedRows()` |
| `getSelectedRecords()` | None | Get selected data | `const data = treeGridRef.current.getSelectedRecords()` |
| `selectCell(cellIndex, isToggle)` | `cellIndex`: IIndex, `isToggle?`: boolean | Select cell | `treeGridRef.current.selectCell({rowIndex: 1, cellIndex: 2})` |

### Edit Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `startEdit()` | None | Start editing selected row | `treeGridRef.current.startEdit()` |
| `endEdit()` | None | End editing | `treeGridRef.current.endEdit()` |
| `closeEdit()` | None | Cancel editing | `treeGridRef.current.closeEdit()` |
| `addRecord()` | None | Show add dialog | `treeGridRef.current.addRecord()` |
| `deleteRow(tr)` | `tr`: Element | Delete row element | `treeGridRef.current.deleteRow(rowElement)` |

### Sorting Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `sortByColumn(columnName, direction)` | `columnName`: string, `direction`: string | Sort by column | `treeGridRef.current.sortByColumn('TaskName', 'Ascending')` |
| `clearSorting()` | None | Clear all sorting | `treeGridRef.current.clearSorting()` |

### Filtering Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `filterByColumn(fieldName, operator, value)` | `fieldName`: string, `operator`: string, `value`: string | Filter column | `treeGridRef.current.filterByColumn('TaskName', 'startswith', 'Plan')` |
| `clearFiltering()` | None | Clear all filters | `treeGridRef.current.clearFiltering()` |
| `removeFilteredColsByField(field)` | `field`: string | Remove filter from field | `treeGridRef.current.removeFilteredColsByField('TaskName')` |

### Search Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `search(searchString)` | `searchString`: string | Search grid | `treeGridRef.current.search('Planning')` |

### Export Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `excelExport(excelExportProperties)` | `excelExportProperties?`: object | Export to Excel | `treeGridRef.current.excelExport()` |
| `pdfExport(pdfExportProperties)` | `pdfExportProperties?`: object | Export to PDF | `treeGridRef.current.pdfExport()` |
| `csvExport(excelExportProperties)` | `excelExportProperties?`: object | Export to CSV | `treeGridRef.current.csvExport()` |
| `print()` | None | Print grid | `treeGridRef.current.print()` |

### Column Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `getColumnByField(field)` | `field`: string | Get column by field | `const col = treeGridRef.current.getColumnByField('TaskName')` |
| `getColumnByUid(uid)` | `uid`: string | Get column by UID | `const col = treeGridRef.current.getColumnByUid('grid-column1')` |
| `getColumns()` | None | Get all columns | `const cols = treeGridRef.current.getColumns()` |
| `showColumns(keys, showBy)` | `keys`: string[], `showBy?`: string | Show columns | `treeGridRef.current.showColumns(['TaskName', 'Duration'])` |
| `hideColumns(keys, hideBy)` | `keys`: string[], `hideBy?`: string | Hide columns | `treeGridRef.current.hideColumns(['Priority'])` |

### State Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `getPersistData()` | None | Get persisted state | `const state = treeGridRef.current.getPersistData()` |
| `setProperties(prop, muteOnChange)` | `prop`: object, `muteOnChange?`: boolean | Update properties | `treeGridRef.current.setProperties({allowPaging: true})` |

### Utility Methods

| Method | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| `getRowByIndex(index)` | `index`: number | Get row element | `const row = treeGridRef.current.getRowByIndex(2)` |
| `getCellFromIndex(rowIndex, columnIndex)` | `rowIndex`: number, `columnIndex`: number | Get cell element | `const cell = treeGridRef.current.getCellFromIndex(2, 1)` |
| `getContent()` | None | Get content element | `const content = treeGridRef.current.getContent()` |
| `getHeaderContent()` | None | Get header element | `const header = treeGridRef.current.getHeaderContent()` |
| `destroy()` | None | Destroy component | `treeGridRef.current.destroy()` |

## Complete Examples Data Operations

### Dynamic Add/Edit/Delete

```tsx
function TreeGridCRUD() {
  const treeGridRef = useRef<TreeGridComponent>(null);

  const handleAdd = () => {
    const newTask = {
      TaskID: Date.now(),
      TaskName: 'New Task',
      StartDate: new Date(),
      Duration: 0
    };
    
    // Add as child of selected row
    const selectedRow = treeGridRef.current?.getSelectedRecords()[0];
    if (selectedRow) {
      treeGridRef.current?.addRecord(newTask, selectedRow.index, 'Child');
    } else {
      treeGridRef.current?.addRecord(newTask);
    }
  };

  const handleEdit = () => {
    treeGridRef.current?.startEdit();
  };

  const handleDelete = () => {
    const selectedRecords = treeGridRef.current?.getSelectedRecords();
    if (selectedRecords && selectedRecords.length > 0) {
      treeGridRef.current?.deleteRecord('TaskID', selectedRecords[0]);
    }
  };

  return (
    <>
      <button onClick={handleAdd}>Add</button>
      <button onClick={handleEdit}>Edit</button>
      <button onClick={handleDelete}>Delete</button>
      <TreeGridComponent ref={treeGridRef} dataSource={data} />
    </>
  );
}
```

### Expand/Collapse Control

```tsx
function TreeGridExpandControl() {
  const treeGridRef = useRef<TreeGridComponent>(null);

  const handleExpandAll = () => {
    treeGridRef.current?.expandAll();
  };

  const handleCollapseAll = () => {
    treeGridRef.current?.collapseAll();
  };

  const handleExpandToLevel = (level: number) => {
    treeGridRef.current?.expandAtLevel(level);
  };

  return (
    <>
      <button onClick={handleExpandAll}>Expand All</button>
      <button onClick={handleCollapseAll}>Collapse All</button>
      <button onClick={() => handleExpandToLevel(2)}>Expand Level 2</button>
      <TreeGridComponent ref={treeGridRef} dataSource={data} />
    </>
  );
}
```

### Export with Options

```tsx
function TreeGridExport() {
  const treeGridRef = useRef<TreeGridComponent>(null);

  const handleExcelExport = () => {
    const excelExportProperties = {
      fileName: 'TreeGridData.xlsx',
      hierarchyExportMode: 'All' // Export all levels
    };
    treeGridRef.current?.excelExport(excelExportProperties);
  };

  const handlePDFExport = () => {
    const pdfExportProperties = {
      fileName: 'TreeGridData.pdf',
      pageOrientation: 'Landscape',
      pageSize: 'A4'
    };
    treeGridRef.current?.pdfExport(pdfExportProperties);
  };

  return (
    <>
      <button onClick={handleExcelExport}>Export Excel</button>
      <button onClick={handlePDFExport}>Export PDF</button>
      <TreeGridComponent ref={treeGridRef} dataSource={data} />
    </>
  );
}
```

### Dynamic Filtering

```tsx
function TreeGridDynamicFilter() {
  const treeGridRef = useRef<TreeGridComponent>(null);
  const [filterValue, setFilterValue] = useState('');

  const handleFilter = () => {
    if (filterValue) {
      treeGridRef.current?.filterByColumn('TaskName', 'startswith', filterValue);
    } else {
      treeGridRef.current?.clearFiltering();
    }
  };

  return (
    <>
      <input
        type="text"
        value={filterValue}
        onChange={(e) => setFilterValue(e.target.value)}
        placeholder="Filter by task name"
      />
      <button onClick={handleFilter}>Apply Filter</button>
      <button onClick={() => { setFilterValue(''); treeGridRef.current?.clearFiltering(); }}>
        Clear Filter
      </button>
      <TreeGridComponent ref={treeGridRef} dataSource={data} />
    </>
  );
}
```

### Get Selected Data

```tsx
function TreeGridSelection() {
  const treeGridRef = useRef<TreeGridComponent>(null);
  const [selectedData, setSelectedData] = useState(null);

  const handleGetSelected = () => {
    const selected = treeGridRef.current?.getSelectedRecords();
    if (selected && selected.length > 0) {
      setSelectedData(selected[0]);
      console.log('Selected:', selected);
    }
  };

  const handleSelectSpecific = () => {
    // Select row at index 3
    treeGridRef.current?.selectRow(3);
  };

  return (
    <>
      <button onClick={handleGetSelected}>Get Selected</button>
      <button onClick={handleSelectSpecific}>Select Row 3</button>
      {selectedData && <pre>{JSON.stringify(selectedData, null, 2)}</pre>}
      <TreeGridComponent 
        ref={treeGridRef} 
        dataSource={data}
        selectionSettings={{ type: 'Multiple', mode: 'Row' }}
      />
    </>
  );
}
```

## Best Practices

1. **Always check ref availability**: `treeGridRef.current?.method()`
2. **Use TypeScript types**: `useRef<TreeGridComponent>(null)`
3. **Cleanup on unmount**: Call `destroy()` in cleanup function
4. **Batch operations**: Use `setProperties()` for multiple prop updates
5. **Handle errors**: Wrap imperative calls in try-catch
6. **Refresh after manual changes**: Call `refresh()` after direct data manipulation

