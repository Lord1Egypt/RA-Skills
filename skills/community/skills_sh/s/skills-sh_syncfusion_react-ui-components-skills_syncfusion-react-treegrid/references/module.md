# Module Registration

## Table of Contents
- [Module Injection Rules](#module-injection-rules)
- [Critical Rule](#critical-rule)
- [Module Types](#module-types)
- [Module Registration Example](#module-registration-example)
- [Module Dependencies](#module-dependencies)
- [Performance Considerations](#performance-considerations)
- [Optional vs Required](#optional-vs-required)
- [DataManager Module](#datamanager-module)
- [Checking TreeGrid API with VS IntelliSense](#checking-treegrid-api-with-vs-intellisense)


The Syncfusion React TreeGrid uses a modular architecture where each feature must be registered using the `Inject` component. Only the modules you explicitly inject are bundled, keeping your application bundle size minimal.

## Module Injection Rules

### Rule 1: Module Injection via Inject Component (Feature-Specific)
**Severity**: 🟠 IMPORTANT - Some features require module injection via Inject component

**Feature-Based Requirements in React**:

```jsx
// ✅ REQUIRED MODULES - Must be injected:

// For Paging
import { Page } from '@syncfusion/ej2-react-treegrid';
<TreeGridComponent allowPaging={true}>
  <Inject services={[Page]} />  {/* MANDATORY */}
</TreeGridComponent>

// For Sorting
import { Sort } from '@syncfusion/ej2-react-treegrid';
<TreeGridComponent allowSorting={true}>
  <Inject services={[Sort]} />  {/* MANDATORY */}
</TreeGridComponent>

// For Filtering
import { Filter } from '@syncfusion/ej2-react-treegrid';
<TreeGridComponent allowFiltering={true}>
  <Inject services={[Filter]} />  {/* MANDATORY */}
</TreeGridComponent>

// For Editing
import { Edit } from '@syncfusion/ej2-react-treegrid';
<TreeGridComponent editSettings={editSettings}>
  <Inject services={[Edit]} />  {/* MANDATORY */}
</TreeGridComponent>
```

**⚠️ BUILT-IN FEATURES (Do NOT need Inject)**:
```jsx
// ✅ BUILT-IN FEATURES (No Inject needed):

// Selection - BUILT-IN
<TreeGridComponent 
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}>
  {/* No Inject required! */}
</TreeGridComponent>

// Column Definition - BUILT-IN
<ColumnsDirective>
  <ColumnDirective field='TaskID'></ColumnDirective>
</ColumnsDirective>

// Child Mapping - BUILT-IN
<TreeGridComponent childMapping='subtasks'>
  {/* No Inject required! */}
</TreeGridComponent>

// Basic Data Binding - BUILT-IN
<TreeGridComponent dataSource={data}>
  {/* No Inject required! */}
</TreeGridComponent>
```

---

### Rule 2: Inject Component Placement is CRITICAL
**Severity**: 🔴 CRITICAL - Must be LAST child of TreeGridComponent

**Requirement**:
```jsx
// ✅ CORRECT - Inject as LAST child
<TreeGridComponent dataSource={data} allowPaging={true}>
  <ColumnsDirective>
    <ColumnDirective field='TaskID'></ColumnDirective>
  </ColumnsDirective>
  <Inject services={[Page]} />  {/* LAST child */}
</TreeGridComponent>

// ❌ WRONG - Inject in middle
<TreeGridComponent dataSource={data} allowPaging={true}>
  <Inject services={[Page]} />  {/* TOO EARLY */}
  <ColumnsDirective>
    <ColumnDirective field='TaskID'></ColumnDirective>
  </ColumnsDirective>
</TreeGridComponent>

// ❌ WRONG - Missing Inject
<TreeGridComponent dataSource={data} allowPaging={true}>
  <ColumnsDirective>
    {/* Feature will not work without Inject */}
  </ColumnsDirective>
</TreeGridComponent>
```

**Complete Module Setup for Full-Featured Grid in React**:
```jsx
// ✅ COMPLETE SETUP - All common features
import { 
  TreeGridComponent, 
  ColumnsDirective, 
  ColumnDirective,
  Inject,
  Page,
  Sort,
  Filter,
  Edit,
  ExcelExport,
  PdfExport,
  Print,
  Aggregate,
  Toolbar,
  ColumnMenu,
  Resize,
  Reorder,
  ContextMenu,
  RowDD,
  VirtualScroll
} from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const editSettings = { mode: 'Dialog', allowEditing: true, allowAdding: true, allowDeleting: true };
  const toolbar = ['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'ExcelExport', 'PdfExport'];
  
  return (
    <TreeGridComponent 
      dataSource={data}
      childMapping='subtasks'
      allowPaging={true}
      allowSorting={true}
      allowFiltering={true}
      allowExcelExport={true}
      allowPdfExport={true}
      editSettings={editSettings}
      toolbar={toolbar}>
      
      <ColumnsDirective>
        <ColumnDirective field='TaskID' headerText='ID' isPrimaryKey={true}></ColumnDirective>
        <ColumnDirective field='TaskName' headerText='Task'></ColumnDirective>
      </ColumnsDirective>
      
      <Inject services={[Page, Sort, Filter, Edit, ExcelExport, PdfExport, Print, Aggregate, Toolbar, ColumnMenu, Resize, Reorder, ContextMenu, RowDD, VirtualScroll]} />
      
    </TreeGridComponent>
  );
}
```
---

## Critical Rule

⚠️ `<Inject services={[...]} />` must be the **last child** inside `<TreeGridComponent>`.

```tsx
// ✅ CORRECT
<TreeGridComponent dataSource={data}>
  <ColumnsDirective>{/* columns */}</ColumnsDirective>
  <Inject services={[Page, Sort, Filter]} /> {/* LAST CHILD */}
</TreeGridComponent>

// ❌ WRONG - Inject is not last
<TreeGridComponent dataSource={data}>
  <Inject services={[Page, Sort, Filter]} />
  <ColumnsDirective>{/* columns */}</ColumnsDirective> {/* After Inject = WRONG */}
</TreeGridComponent>
```

## Module Types

### Core Modules

**Page Module** - Paging functionality
```tsx
import { Inject, Page } from '@syncfusion/ej2-react-treegrid';

<TreeGridComponent allowPaging>
  {/* ... */}
  <Inject services={[Page]} />
</TreeGridComponent>
```

**Sort Module** - Sorting capability
```tsx
import { Inject, Sort } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Sort]} />
```

**Filter Module** - Filtering functionality (includes Filter Bar and Filter Menu)
```tsx
import { Inject, Filter } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Filter]} />
```

**Search Module** - Global search across columns
```tsx
import { Inject, Search } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Search]} />
```

**Selection Module** - Row and cell selection
```tsx
import { Inject, Selection } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Selection]} />
```

**Edit Module** - All editing modes (cell, row, dialog, batch)
```tsx
import { Inject, Edit } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Edit]} />
```

**CommandColumn Module** - Command column buttons (Edit, Delete, Cancel)
```tsx
import { Inject, CommandColumn } from '@syncfusion/ej2-react-treegrid';

<Inject services={[CommandColumn]} />
```

**Toolbar Module** - Toolbar with predefined items
```tsx
import { Inject, Toolbar } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Toolbar]} />
```

**ContextMenu Module** - Context menu on right-click
```tsx
import { Inject, ContextMenu } from '@syncfusion/ej2-react-treegrid';

<Inject services={[ContextMenu]} />
```

**ExcelExport Module** - Export to Excel format
```tsx
import { Inject, ExcelExport } from '@syncfusion/ej2-react-treegrid';

<Inject services={[ExcelExport]} />
```

**PdfExport Module** - Export to PDF format
```tsx
import { Inject, PdfExport } from '@syncfusion/ej2-react-treegrid';

<Inject services={[PdfExport]} />
```

**Resize Module** - Column resizing functionality
```tsx
import { Inject, Resize } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Resize]} />
```

**Reorder Module** - Column reordering
```tsx
import { Inject, Reorder } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Reorder]} />
```

**RowDD Module** - Row drag-and-drop
```tsx
import { Inject, RowDD } from '@syncfusion/ej2-react-treegrid';

<Inject services={[RowDD]} />
```

**Aggregate Module** - Aggregation (sum, average, etc.)
```tsx
import { Inject, Aggregate } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Aggregate]} />
```

**VirtualScroll Module** - Virtual scrolling for large datasets
```tsx
import { Inject, VirtualScroll } from '@syncfusion/ej2-react-treegrid';

<Inject services={[VirtualScroll]} />
```

**Print Module** - Print functionality
```tsx
import { Inject, Print } from '@syncfusion/ej2-react-treegrid';

<Inject services={[Print]} />
```

## Module Registration Example

### Full Feature Setup
```tsx
import {
  TreeGridComponent,
  ColumnsDirective,
  ColumnDirective,
  Inject,
  Page,
  Sort,
  Filter,
  Search,
  Edit,
  Toolbar,
  Selection,
  CommandColumn,
  ContextMenu,
  ExcelExport,
  PdfExport,
  Print,
  Resize,
  Reorder,
  RowDD,
  Aggregate,
  VirtualScroll,
  LazyLoadGroup
} from '@syncfusion/ej2-react-treegrid';

// In component:
<Inject
  services={[
    Page,
    Sort,
    Filter,
    Search,
    Edit,
    Toolbar,
    Selection,
    CommandColumn,
    ContextMenu,
    ExcelExport,
    PdfExport,
    Print,
    Resize,
    Reorder,
    RowDD,
    Aggregate,
    VirtualScroll,
    LazyLoadGroup
  ]}
/>
```

### Issue: Conflicting Modules

**Symptom**: Unexpected behavior with scrolling
```tsx
<TreeGridComponent 
  allowPaging={true}
  enableVirtualization={true} // Conflict!
>
  <Inject services={[Page, VirtualScroll]} />
</TreeGridComponent>
```

**Solution**: Choose one scrolling strategy
```tsx
// Option 1: Paging
<TreeGridComponent allowPaging={true}>
  <Inject services={[Page]} />
</TreeGridComponent>

// Option 2: Virtual Scrolling
<TreeGridComponent enableVirtualization={true} height="600px">
  <Inject services={[VirtualScroll]} />
</TreeGridComponent>
```

## Bundle Optimization

### Conditional Module Loading

```tsx
import React, { useMemo } from 'react';
import { TreeGridComponent, Inject, Page, Sort, Filter, Edit, Toolbar } from '@syncfusion/ej2-react-treegrid';

function TreeGridWrapper({ enableEdit, enableExport }) {
  // Dynamically determine required modules
  const modules = useMemo(() => {
    const required = [Page, Sort, Filter];
    
    if (enableEdit) {
      required.push(Edit, Toolbar);
    }
    
    if (enableExport) {
      const { ExcelExport, PdfExport } = require('@syncfusion/ej2-react-treegrid');
      required.push(ExcelExport, PdfExport);
    }
    
    return required;
  }, [enableEdit, enableExport]);

  return (
    <TreeGridComponent>
      <ColumnsDirective>{/* columns */}</ColumnsDirective>
      <Inject services={modules} />
    </TreeGridComponent>
  );
}
```

### Tree-Shaking Verification

Check your bundle to ensure unused modules are removed:

```bash
# Webpack Bundle Analyzer
npm install --save-dev webpack-bundle-analyzer

# Analyze bundle
npm run build -- --stats
npx webpack-bundle-analyzer build/stats.json
```


## Module Dependencies

Some modules depend on others:

- **CommandColumn** requires **Edit** module
- **ContextMenu** works best with **Edit** and **CommandColumn**
- **ExcelExport** and **PdfExport** are independent
- **Aggregate** works with all other modules
- **VirtualScroll** works with all layout modules
- **RowDD** requires **Selection** module

## Performance Considerations

1. **Only inject modules you use** - Each module adds to bundle size
2. **Lazy load optional modules** - For rarely-used features, consider dynamic imports
3. **Minimal setup** - Start with essential modules (Page, Sort, Filter, Edit)
4. **Add on demand** - Add Export, Print, ContextMenu as needed

## Optional vs Required

**Always Required:**
- TreeGridComponent from @syncfusion/ej2-react-treegrid

**Optional Modules:**
- All modules listed above are optional
- TreeGrid works without any injected services, showing basic grid without advanced features
- Only inject what your feature set requires

## DataManager Module

If using remote data binding with DataManager:
```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

const remoteData = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor()
});

<TreeGridComponent dataSource={remoteData}>
  {/* ... */}
</TreeGridComponent>
```

DataManager is imported from @syncfusion/ej2-data, not @syncfusion/ej2-react-treegrid.

## Checking TreeGrid API with VS IntelliSense

After injecting a module, VS Code IntelliSense will automatically recognize new properties and methods available through the injected service.

Example: Injecting `Edit` module enables:
- `editSettings` property
- `beginEdit()` method
- `endEdit()` method
- Edit-related events like `onActionComplete`

