# Adaptive Mode in React Grid

## Adaptive Dialogs

Enable `enableAdaptiveUI` to render filter, sort, and edit dialogs in full-screen mode. Apply `e-bigger` class to parent element.

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Filter, Sort, Edit, Toolbar, Page } from '@syncfusion/ej2-react-grids';

<div className="e-adaptive-demo e-bigger">
  <GridComponent 
    dataSource={data}
    enableAdaptiveUI={true}
    allowFiltering={true}
    allowSorting={true}
    allowPaging={true}
    editSettings={{ allowEditing: true, allowAdding: true, allowDeleting: true, mode: 'Dialog' }}
  >
    <ColumnsDirective>
      <ColumnDirective field='OrderID' headerText='Order ID' width='150' isPrimaryKey={true} />
      <ColumnDirective field='CustomerID' headerText='Customer Name' width='160' />
      <ColumnDirective field='Freight' headerText='Freight' width='150' format='C2' />
    </ColumnsDirective>
    <Inject services={[Filter, Sort, Edit, Toolbar, Page]} />
  </GridComponent>
</div>
```

## Vertical Row Rendering

Set `rowRenderingMode="Vertical"` to display rows vertically (default is Horizontal). Requires `enableAdaptiveUI={true}`.

Supported Features: Paging, Sorting, Filtering, Selection, Dialog Editing, Aggregates, Infinite Scroll, Toolbar

Note: Column Menu only works in Horizontal mode.

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Filter, Sort, Edit, Toolbar, Page } from '@syncfusion/ej2-react-grids';

<GridComponent 
  dataSource={data}
  enableAdaptiveUI={true}
  rowRenderingMode="Vertical"
  allowFiltering={true}
  allowSorting={true}
  allowPaging={true}
  editSettings={{ allowEditing: true, mode: 'Dialog' }}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='150' isPrimaryKey={true} />
    <ColumnDirective field='CustomerID' headerText='Customer Name' width='160' />
    <ColumnDirective field='Freight' headerText='Freight' width='150' format='C2' />
  </ColumnsDirective>
  <Inject services={[Filter, Sort, Edit, Toolbar, Page]} />
</GridComponent>
```

## Adaptive UI Modes

Use `adaptiveUIMode` property:
- `'Both'` (default): Render on mobile and desktop
- `'Mobile'`: Render only on mobile screens

```tsx
<GridComponent 
  dataSource={data}
  enableAdaptiveUI={true}
  adaptiveUIMode="Mobile"
  allowFiltering={true}
  allowSorting={true}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='150' isPrimaryKey={true} />
    <ColumnDirective field='CustomerID' headerText='Customer Name' width='160' />
  </ColumnsDirective>
  <Inject services={[Filter, Sort]} />
</GridComponent>
```
