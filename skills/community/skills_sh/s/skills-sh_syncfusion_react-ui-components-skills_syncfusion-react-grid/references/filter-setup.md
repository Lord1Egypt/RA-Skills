# Filter Setup and Basic Configuration

## Table of Contents
- [Setup Filtering Module](#setup-filtering-module)
- [Enable Filtering](#enable-filtering)
- [Filter Types Overview](#filter-types-overview)
- [Disable Filtering for Columns](#disable-filtering-for-columns)
- [Quick Reference](#quick-reference)

---

## Setup Filtering Module

Filtering requires injecting the `Filter` module into the Grid's services. Without this module, filtering features are unavailable.

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Filter } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowFiltering={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Filter]} />  {/* REQUIRED for filtering */}
</GridComponent>
```

---

## Enable Filtering

Set `allowFiltering={true}` on the Grid component to activate filtering UI. Configure behavior via `filterSettings` property.

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Filter, Page } from '@syncfusion/ej2-react-grids';

<GridComponent 
  dataSource={data} 
  allowFiltering={true}           // Enable filtering
  allowPaging={true}
  pageSettings={{ pageSize: 6 }}
  allowSorting={true}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' textAlign='Right' />
    <ColumnDirective field='CustomerID' headerText='Customer ID' width='100' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' textAlign='Right' />
    <ColumnDirective field='OrderDate' headerText='Order Date' format='yMd' width='100' />
  </ColumnsDirective>
  <Inject services={[Filter, Page]} />
</GridComponent>
```

---

## Filter Types Overview

Grid supports three filter UI types. Set via `filterSettings.type` property.

| Type | Description | Use Case |
|------|-------------|----------|
| **FilterBar** (default) | Input fields below column headers | Real-time filtering as you type |
| **Menu** | Dropdown menu with operators in header | Precise operator selection |
| **Excel** | Checkbox list dialog | Multiple value selection |
| **CheckBox** | Checkbox list (Excel variant) | Categorical/distinct value filtering |

### FilterBar Type (Default)

```tsx
const filterSettings = { type: 'FilterBar' };
<GridComponent dataSource={data} allowFiltering={true} filterSettings={filterSettings} />
```

### Menu Type

```tsx
const filterSettings = { type: 'Menu' };
<GridComponent dataSource={data} allowFiltering={true} filterSettings={filterSettings} />
```

### Excel/Checkbox Type

```tsx
const filterSettings = { type: 'Excel' };  // or 'CheckBox'
<GridComponent dataSource={data} allowFiltering={true} filterSettings={filterSettings} />
```

---

## Disable Filtering for Columns

Set `allowFiltering={false}` on specific columns to hide filter bar/UI for those columns.

```tsx
<GridComponent dataSource={data} allowFiltering={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective 
      field='CustomerID' 
      headerText='Customer ID' 
      width='100' 
      allowFiltering={false}    {/* No filter for this column */}
    />
    <ColumnDirective field='Freight' headerText='Freight' width='100' />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</GridComponent>
```

**Use This When:**
- Column contains non-filterable data (images, custom templates)
- Column is action-only (buttons, commands)
- Column filters are not meaningful to users

---

## Quick Reference

| Task | Property/Method | Example |
|------|-----------------|---------|
| Enable filtering | `allowFiltering={true}` | `<Grid allowFiltering={true} />` |
| Set filter type | `filterSettings={{ type: 'Menu' }}` | Menu, FilterBar, Excel, CheckBox |
| Disable column filter | `allowFiltering={false}` | `<ColumnDirective allowFiltering={false} />` |
| Filter programmatically | `grid.filterByColumn()` | `grid.filterByColumn('OrderID', 'equal', 10248)` |
| Clear filters | `grid.clearFiltering()` | `grid.clearFiltering()` |
| Inject module | `<Inject services={[Filter]} />` | Required in `<Inject>` |
