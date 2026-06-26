# Module System in React Grid

## Table of Contents
- [Overview](#overview)
- [Module Injection Pattern](#module-injection-pattern)
- [Available Modules](#available-modules)
- [Module Dependencies](#module-dependencies)
- [Bundle Optimization](#bundle-optimization)
- [Feature-Module Mapping](#feature-module-mapping)

## Overview

Syncfusion React Grid uses a modular architecture where features are provided as separate modules. This allows you to include only the features you need, reducing bundle size and improving performance.

Modules are injected using the `<Inject>` component, passing an array of required services via the `services` prop.

## Module Injection Pattern

### Basic Injection

```tsx
import { GridComponent, Inject, Page, Sort, Filter } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter]} />
</GridComponent>
```

### Multiple Modules

```tsx
import {
  GridComponent,
  ColumnsDirective,
  ColumnDirective,
  Inject,
  Page,
  Sort,
  Filter,
  Group,
  Edit,
  Toolbar,
  ExcelExport,
  PdfExport
} from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data}>
  <ColumnsDirective>
    {/* columns */}
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter, Group, Edit, Toolbar, ExcelExport, PdfExport]} />
</GridComponent>
```

### Conditional Injection

```tsx
const getRequiredModules = (features) => {
  const modules = [];
  
  if (features.includes('paging')) modules.push(Page);
  if (features.includes('sorting')) modules.push(Sort);
  if (features.includes('filtering')) modules.push(Filter);
  if (features.includes('grouping')) modules.push(Group);
  if (features.includes('editing')) modules.push(Edit, Toolbar);
  if (features.includes('export')) modules.push(ExcelExport, PdfExport);
  
  return modules;
};

const requiredModules = getRequiredModules(['paging', 'sorting', 'filtering']);

<GridComponent dataSource={data}>
  <ColumnsDirective>
    {/* columns */}
  </ColumnsDirective>
  <Inject services={requiredModules} />
</GridComponent>
```

## Available Modules

### Data Operation Modules

| Module | Import | Purpose | Required For |
|--------|--------|---------|---------------|
| `Page` | `@syncfusion/ej2-react-grids` | Pagination | `allowPaging={true}` |
| `Sort` | `@syncfusion/ej2-react-grids` | Column sorting | `allowSorting={true}` |
| `Filter` | `@syncfusion/ej2-react-grids` | Data filtering | `allowFiltering={true}` |
| `Group` | `@syncfusion/ej2-react-grids` | Row grouping | `allowGrouping={true}` |
| `Selection` | `@syncfusion/ej2-react-grids` | Row/cell selection | `allowSelection={true}` |
| `Aggregate` | `@syncfusion/ej2-react-grids` | Summary aggregates | Aggregate components |
| `Search` | `@syncfusion/ej2-react-grids` | Global search | Search toolbar item |

### UI & Interaction Modules

| Module | Import | Purpose | Required For |
|--------|--------|---------|---------------|
| `Toolbar` | `@syncfusion/ej2-react-grids` | Toolbar functionality | `toolbar={[...]}` |
| `Edit` | `@syncfusion/ej2-react-grids` | Row editing | `editSettings={{...}}` |
| `ContextMenu` | `@syncfusion/ej2-react-grids` | Right-click context menu | `contextMenuItems={[...]}` |
| `Clipboard` | `@syncfusion/ej2-react-grids` | Copy/paste operations | Copy/paste functionality |

### Display & Layout Modules

| Module | Import | Purpose | Required For |
|--------|--------|---------|---------------|
| `VirtualScroll` | `@syncfusion/ej2-react-grids` | Virtual scrolling | `enableVirtualization={true}` |
| `InfiniteScroll` | `@syncfusion/ej2-react-grids` | Infinite scrolling | `enableInfiniteScrolling={true}` |
| `DetailRow` | `@syncfusion/ej2-react-grids` | Master-detail hierarchy | `detailTemplate={...}` |
| `ColumnMenu` | `@syncfusion/ej2-react-grids` | Column header menu | `showColumnMenu={true}` |
| `ColumnChooser` | `@syncfusion/ej2-react-grids` | Column visibility toggle | Column chooser toolbar |
| `Resize` | `@syncfusion/ej2-react-grids` | Column resizing | `allowResizing={true}` |
| `Reorder` | `@syncfusion/ej2-react-grids` | Column reordering | `allowReordering={true}` |

### Export & Print Modules

| Module | Import | Purpose | Required For |
|--------|--------|---------|---------------|
| `ExcelExport` | `@syncfusion/ej2-react-grids` | Excel export | `allowExcelExport={true}` |
| `PdfExport` | `@syncfusion/ej2-react-grids` | PDF export | `allowPdfExport={true}` |
| `Print` | `@syncfusion/ej2-react-grids` | Grid printing | Print toolbar item |

### Advanced Modules

| Module | Import | Purpose | Required For |
|--------|--------|---------|---------------|
| `RowDD` | `@syncfusion/ej2-react-grids` | Row drag & drop | `allowRowDragAndDrop={true}` |
| `RowPinning` | `@syncfusion/ej2-react-grids` | Row pinning/freezing | `allowRowPinning={true}` |

## Module Dependencies

Some modules require other modules to function properly:

```
Edit ──────┐
           ├─> Toolbar (required)
Filtering──┘

Sorting
Filtering
Grouping ──> Requires individual setup

ExcelExport
PdfExport ──> Can work independently

VirtualScroll
InfiniteScroll ──> Cannot be used together

DetailRow ──> Independent

ColumnMenu ──> Independent
Reorder ────> Independent
Resize─────-> Independent
```

### Edit Mode Dependencies

```tsx
// Dialog Edit requires Toolbar
const editSettings = {
  allowEditing: true,
  allowAdding: true,
  mode: 'Dialog'
};

<GridComponent
  dataSource={data}
  editSettings={editSettings}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  {/* columns */}
  <Inject services={[Edit, Toolbar]} />  // Both required
</GridComponent>
```

## Bundle Optimization

### Minimal Bundle (Core Only)

Includes only basic grid display:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

// No Inject needed = smallest bundle
<GridComponent dataSource={data}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
  </ColumnsDirective>
</GridComponent>
```

### Read-Only Grid with Pagination

```tsx
import { GridComponent, Inject, Page } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowPaging={true}>
  {/* columns */}
  <Inject services={[Page]} />  // Only 1 module
</GridComponent>
```

### Full-Featured Grid

```tsx
import {
  GridComponent,
  Inject,
  Page,
  Sort,
  Filter,
  Group,
  Edit,
  Toolbar,
  ExcelExport,
  PdfExport,
  DetailRow,
  Selection,
  Aggregate,
  ColumnMenu,
  Resize,
  Reorder,
  ContextMenu,
  Clipboard,
  Print
} from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  allowPaging={true}
  allowSorting={true}
  allowFiltering={true}
  allowGrouping={true}
  allowSelection={true}
  editSettings={{ mode: 'Dialog', allowEditing: true, allowAdding: true, allowDeleting: true }}
  toolbar={['Add', 'Edit', 'Delete', 'ExcelExport', 'PdfExport', 'Print', 'Search']}
  contextMenuItems={['Copy', 'ExcelExport', 'PdfExport']}
  showColumnMenu={true}
  allowExcelExport={true}
  allowPdfExport={true}
  allowResizing={true}
  allowReordering={true}
  detailTemplate={detailTemplate}
>
  {/* columns */}
  <Inject services={[
    Page, Sort, Filter, Group, Edit, Toolbar, ExcelExport, PdfExport,
    DetailRow, Selection, Aggregate, ColumnMenu, Resize, Reorder,
    ContextMenu, Clipboard, Print
  ]} />
</GridComponent>
```

### Estimated Bundle Sizes

```
Core Grid Only:          ~45 KB
+ Paging:               ~55 KB
+ Paging + Sorting:     ~65 KB
+ Paging + All Data Ops: ~90 KB
+ All Modules:          ~200 KB
```

## Feature-Module Mapping

### Table: Which Module for Which Feature

| Feature | Module | Optional | Notes |
|---------|--------|----------|-------|
| Display data | None | No | Core grid only |
| Pagination | `Page` | Yes | |
| Sorting | `Sort` | Yes | |
| Column Filtering | `Filter` | Yes | |
| Global Search | `Search` | Yes | Requires Toolbar |
| Row Grouping | `Group` | Yes | |
| Row/Cell Selection | `Selection` | Yes | Built-in, but enhance with module |
| Aggregates (Sum, Avg) | `Aggregate` | Yes | |
| Inline Editing | `Edit` | Yes | |
| Dialog Editing | `Edit, Toolbar` | Yes | Toolbar required |
| Batch Editing | `Edit` | Yes | |
| Add/Delete Toolbar | `Toolbar` | Yes | Usually with Edit |
| Excel Export | `ExcelExport` | Yes | |
| PDF Export | `PdfExport` | Yes | |
| Print | `Print` | Yes | Usually with Toolbar |
| Virtual Scrolling | `VirtualScroll` | Yes | Alternative to pagination |
| Infinite Scrolling | `InfiniteScroll` | Yes | Cannot use with VirtualScroll |
| Master-Detail | `DetailRow` | Yes | |
| Right-Click Menu | `ContextMenu` | Yes | |
| Column Resizing | `Resize` | Yes | |
| Column Reordering | `Reorder` | Yes | |
| Column Menu | `ColumnMenu` | Yes | |
| Column Chooser | `ColumnChooser` | Yes | Usually in toolbar |
| Row Drag & Drop | `RowDD` | Yes | |
| Row Pinning | `RowPinning` | Yes | |
| Copy/Paste | `Clipboard` | Yes | |

### Common Feature Combinations

#### Read-Only Grid with Search & Paging
```tsx
<Inject services={[Page, Search, Toolbar]} />
```

#### Data Entry Grid (Inline Editing)
```tsx
<Inject services={[Edit]} />
```

#### Data Entry Grid (Dialog Editing with Validation)
```tsx
<Inject services={[Edit, Toolbar]} />
```

#### Analytics Grid (Grouping with Aggregates)
```tsx
<Inject services={[Group, Aggregate, Page, Sort, Filter]} />
```

#### Master-Detail Reporting
```tsx
<Inject services={[DetailRow, Page, Sort, Filter, Aggregate]} />
```

#### Exportable Data Grid
```tsx
<Inject services={[Page, Sort, Filter, ColumnMenu, Resize, Reorder, ExcelExport, PdfExport, Print, Toolbar]} />
```

#### Real-Time Data Grid
```tsx
<Inject services={[VirtualScroll, Page, Sort, Filter]} />
```

#### Mobile-Optimized Grid
```tsx
<Inject services={[ColumnChooser, ColumnMenu, Resize, Reorder, Page, Sort, Filter]} />
```

## Advanced Scenarios

### Lazy Module Loading

```tsx
import React, { useState, useEffect } from 'react';
import { GridComponent, Inject } from '@syncfusion/ej2-react-grids';

function App() {
  const [modules, setModules] = useState([]);

  useEffect(() => {
    const loadModules = async () => {
      const Page = (await import('@syncfusion/ej2-react-grids')).Page;
      setModules([Page]);
    };
    loadModules();
  }, []);

  return (
    <GridComponent dataSource={data}>
      {/* columns */}
      {modules.length > 0 && <Inject services={modules} />}
    </GridComponent>
  );
}

export default App;
```

### Dynamic Module Management

```tsx
import React, { useRef, useState } from 'react';
import { GridComponent, Inject, Page, Sort, Filter, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

function App() {
  const gridRef = useRef(null);
  const [enableEdit, setEnableEdit] = useState(false);

  const toggleEditMode = () => {
    const modules = enableEdit ? [Page, Sort, Filter] : [Page, Sort, Filter, Edit, Toolbar];
    setEnableEdit(!enableEdit);
    // Re-inject would require re-rendering
  };

  return (
    <div>
      <button onClick={toggleEditMode}>
        {enableEdit ? 'Disable' : 'Enable'} Edit
      </button>
      
      <GridComponent
        ref={gridRef}
        dataSource={data}
        allowPaging={true}
        allowSorting={true}
        allowFiltering={true}
        editSettings={enableEdit ? { mode: 'Dialog', allowEditing: true } : {}}
        toolbar={enableEdit ? ['Add', 'Edit', 'Delete', 'Update', 'Cancel'] : []}
      >
        {/* columns */}
        <Inject services={enableEdit ? [Page, Sort, Filter, Edit, Toolbar] : [Page, Sort, Filter]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

### Check if Module is Injected

```tsx
const gridRef = useRef(null);

useEffect(() => {
  // Check available modules
  console.log('Grid modules:', gridRef.current?.allowPaging); // Returns boolean
  console.log('Edit enabled:', gridRef.current?.editSettings);
}, []);
```
