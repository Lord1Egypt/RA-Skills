# Grid Component - Properties Configuration Guide

## Table of Contents
- [All Properties Reference](#all-properties-reference)
- [Common Usage Patterns](#common-usage-patterns)
- [Module Injection Requirements](#module-injection-requirements)
- [Property Notes](#property-notes)

---

## All Properties Reference

Complete reference of all 112+ Grid properties organized by functional category.

### Data & Query Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `dataSource` | `Object \| DataManager \| DataResult` | `[]` | Primary data source for grid rows |
| `columns` | `Column[] \| string[] \| ColumnModel[]` | `[]` | Column schema definition |
| `query` | `Query` | `null` | External Query for data processing |
| `aggregates` | `AggregateRowModel[]` | `[]` | Aggregate row configurations |
| `childGrid` | `GridModel` | `''` | Child grid for hierarchy |
| `queryString` | `string` | `''` | Relationship key for parent-child |

### Paging Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowPaging` | `boolean` | `false` | Enable/disable paging |
| `pageSettings` | `PageSettingsModel` | `{currentPage:1, pageSize:12}` | Pagination configuration |

### Sorting Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowSorting` | `boolean` | `false` | Enable column sorting |
| `allowMultiSorting` | `boolean` | `false` | Allow sorting multiple columns |
| `sortSettings` | `SortSettingsModel` | `{columns:[]}` | Pre-defined sort configuration |

### Filtering Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowFiltering` | `boolean` | `false` | Enable filter bar |
| `filterSettings` | `FilterSettingsModel` | `{type:'FilterBar', mode:'Immediate'}` | Filter configuration |
| `searchSettings` | `SearchSettingsModel` | `{ignoreCase:true, fields:[]}` | Search behavior |

### Selection Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowSelection` | `boolean` | `true` | Enable row/cell selection |
| `selectionSettings` | `SelectionSettingsModel` | `{mode:'Row', type:'Single'}` | Selection mode & type |
| `selectedRowIndex` | `number` | `-1` | Initial selected row index |
| `isRowSelectable` | `RowSelectable \| string` | `null` | Determine selectable rows |

### Editing Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `editSettings` | `EditSettingsModel` | `{allowEditing:false, mode:'Normal'}` | Edit behavior & mode |
| `detailTemplate` | `string \| Function` | `null` | Detail row template |
| `emptyRecordTemplate` | `string \| Function` | `null` | Empty grid message template |
| `rowTemplate` | `string \| Function` | `null` | Custom row template |

### Layout & Display Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `height` | `string \| number` | `'auto'` | Scrollable content height |
| `width` | `string \| number` | `'auto'` | Grid width |
| `rowHeight` | `number` | `null` | Uniform row height |
| `gridLines` | `GridLine` | `'Default'` | Grid line display mode |
| `clipMode` | `ClipMode` | `'Ellipsis'` | Cell overflow behavior |
| `enableAltRow` | `boolean` | `true` | Alternate row styling |
| `enableHover` | `boolean` | `true` | Row hover highlight |
| `enableStickyHeader` | `boolean` | `false` | Sticky column headers |
| `allowTextWrap` | `boolean` | `false` | Text wrapping in cells |
| `cssClass` | `string` | `''` | Custom CSS class |

### Grouping Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowGrouping` | `boolean` | `false` | Enable grouping |
| `groupSettings` | `GroupSettingsModel` | `{columns:[]}` | Pre-defined grouping |

### Virtualization & Performance

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `enableVirtualization` | `boolean` | `false` | Virtual scroll (rows) |
| `enableColumnVirtualization` | `boolean` | `false` | Virtual scroll (columns) |
| `enableInfiniteScrolling` | `boolean` | `false` | Infinite scroll loading |
| `infiniteScrollSettings` | `InfiniteScrollSettingsModel` | `{enableCache:false, maxBlocks:5}` | Infinite scroll config |
| `enableVirtualMaskRow` | `boolean` | `true` | Shimmer effect for virtual rows |
| `enablePersistence` | `boolean` | `false` | Persist state on page reload |
| `enableImmutableMode` | `boolean` | `false` | Reuse rows for better performance |
| `requireTemplateRef` | `boolean` | `true` | Keep template references |

### Column Operations

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowReordering` | `boolean` | `false` | Allow column drag-drop reorder |
| `allowResizing` | `boolean` | `false` | Allow column resize |
| `frozenColumns` | `number` | `0` | Number of frozen columns |
| `frozenRows` | `number` | `0` | Number of frozen rows |
| `resizeSettings` | `ResizeSettingsModel` | `{mode:'Normal'}` | Column resize mode |
| `rowRenderingMode` | `RowRenderingDirection` | `'Horizontal'` | Row rendering direction |
| `autoFit` | `boolean` | `false` | Auto-fit columns |

### Row Operations

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowRowDragAndDrop` | `boolean` | `false` | Enable row drag-drop |
| `rowDragAndDropModule` | `RowDD` | Module ref | Row drag-drop module |
| `rowDropSettings` | `RowDropSettingsModel` | `{targetID:''}` | Drop target config |
| `isRowPinned` | `PinRow \| Function` | `null` | Determine pinned rows |

### UI Features

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `showColumnChooser` | `boolean` | `false` | Show column visibility UI |
| `showColumnMenu` | `boolean` | `false` | Show column context menu |
| `columnChooserSettings` | `ColumnChooserSettingsModel` | `{columnChooserOperator:'startsWith'}` | Column chooser config |
| `columnMenuItems` | `ColumnMenuItem[] \| ColumnMenuItemModel[]` | `null` | Column menu items |
| `contextMenuItems` | `ContextMenuItem[] \| ContextMenuItemModel[]` | `null` | Context menu items |
| `toolbar` | `string[] \| string \| object[]` | `null` | Toolbar items |
| `toolbarTemplate` | `string \| Function` | `null` | Custom toolbar template |
| `pagerTemplate` | `string \| Function` | `null` | Custom pager template |

### Export Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `allowExcelExport` | `boolean` | `false` | Enable Excel export |
| `allowPdfExport` | `boolean` | `false` | Enable PDF export |
| `printMode` | `PrintMode` | `'AllPages'` | Print pages scope |
| `exportGrids` | `string[]` | `null` | IDs of grids to export |
| `hierarchyPrintMode` | `HierarchyGridPrintMode` | `'Expanded'` | Hierarchy print mode |

### Accessibility & Localization

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `enableKeyboard` | `boolean` | `true` | Keyboard interaction |
| `allowKeyboard` | `boolean` | `true` | Allow keyboard navigation |
| `enableAdaptiveUI` | `boolean` | `false` | Adaptive UI dialogs |
| `enableAutoFill` | `boolean` | `false` | Auto-fill on cell selection |
| `enableColumnSpan` | `boolean` | `false` | Column span for same data |
| `enableRowSpan` | `boolean` | `false` | Row span for same data |
| `enableHeaderFocus` | `boolean` | `true` | Focus on header |
| `locale` | `string` | `''` | Culture/localization |
| `adaptiveUIMode` | `AdaptiveMode` | `'Both'` | Adaptive UI mode |
| `columnQueryMode` | `ColumnQueryModeType` | `'All'` | Data retrieval mode |

### State & Configuration

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `loadingIndicator` | `LoadingIndicatorModel` | `{indicatorType:'Spinner'}` | Loading indicator config |
| `currentAction` | `ActionArgs` | `{}` | Current action details (read-only) |
| `currentViewData` | `Object[]` | `[]` | Currently visible records (read-only) |
| `parentDetails` | `ParentDetails` | `{}` | Parent grid details (read-only) |
| `ej2StatePersistenceVersion` | `string` | `''` | State persistence version |
| `textWrapSettings` | `TextWrapSettingsModel` | `{wrapMode:'Both'}` | Text wrap configuration |



---

## Common Usage Patterns

### Basic Grid Setup

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page, Sort, Filter } from '@syncfusion/ej2-react-grids';
const gridRef = useRef<GridComponent | null>();

<GridComponent 
  ref={gridRef}
  dataSource={data} 
  height={400}
  allowPaging 
  allowSorting 
  allowFiltering
  pageSettings={{ pageSize: 12 }}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100'/>
    <ColumnDirective field='CustomerID' headerText='Customer' width='120'/>
    <ColumnDirective field='Freight' headerText='Freight' width='100'/>
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter]} />
</GridComponent>
```

### Advanced Configuration with Multiple Features

```tsx
<GridComponent 
  dataSource={data}
  allowPaging allowSorting allowFiltering allowGrouping
  allowExcelExport allowPdfExport allowRowDragAndDrop
  allowSelection allowReordering allowResizing
  height={500}
  editSettings={{ allowEditing: true, allowAdding: true, allowDeleting: true, mode: 'Dialog' }}
  selectionSettings={{ mode: 'Row', type: 'Multiple' }}
  sortSettings={{ columns: [{field: 'OrderID', direction: 'Ascending'}] }}
  pageSettings={{ pageSize: 20 }}
>
  <Inject services={[Page, Sort, Filter, Group, Edit, Toolbar, ExcelExport, PdfExport, Selection, Reorder, Resize, RowDD]} />
</GridComponent>
```

### Virtual Scrolling for Large Datasets

```tsx
<GridComponent 
  dataSource={largeData}
  height={400}
  enableVirtualization
  enableColumnVirtualization
  pageSettings={{ pageSize: 50 }}
>
  <Inject services={[VirtualScroll]} />
</GridComponent>
```

### Infinite Scrolling

```tsx
<GridComponent 
  dataSource={data}
  height={400}
  enableInfiniteScrolling
  infiniteScrollSettings={{ enableCache: true, maxBlocks: 3 }}
  pageSettings={{ pageSize: 50 }}
>
  <Inject services={[InfiniteScroll]} />
</GridComponent>
```

### Frozen Columns & Rows

```tsx
<GridComponent 
  dataSource={data}
  frozenColumns={2}
  frozenRows={1}
  height={400}
>
  <Inject services={[Freeze]} />
</GridComponent>
```

### Master-Detail (Hierarchy)

```tsx
<GridComponent 
  dataSource={masterData}
  detailTemplate={childTemplate}
  queryString='OrderID'
  childGrid={{ dataSource: childData, queryString: 'OrderID' }}
/>
```

### Custom Export

```tsx
<GridComponent 
  ref={gridInstance}
  allowExcelExport
  allowPdfExport
  toolbar={['ExcelExport', 'PdfExport']}
  toolbarClick={handleToolbarClick}
>
  <Inject services={[Toolbar, ExcelExport, PdfExport]} />
</GridComponent>
```

---

## Module Injection Requirements

Grid features require specific module injection via `<Inject services={[...]} />`:

| Feature | Module | Import |
|---------|--------|--------|
| Paging | `Page` | `@syncfusion/ej2-react-grids` |
| Sorting | `Sort` | `@syncfusion/ej2-react-grids` |
| Filtering | `Filter` | `@syncfusion/ej2-react-grids` |
| Grouping | `Group` | `@syncfusion/ej2-react-grids` |
| Editing | `Edit` | `@syncfusion/ej2-react-grids` |
| Selection | `Selection` | `@syncfusion/ej2-react-grids` |
| Virtual Scrolling | `VirtualScroll` | `@syncfusion/ej2-react-grids` |
| Infinite Scrolling | `InfiniteScroll` | `@syncfusion/ej2-react-grids` |
| Toolbar | `Toolbar` | `@syncfusion/ej2-react-grids` |
| Excel Export | `ExcelExport` | `@syncfusion/ej2-react-grids` |
| PDF Export | `PdfExport` | `@syncfusion/ej2-react-grids` |
| CSV Export | `CsvExport` | `@syncfusion/ej2-react-grids` |
| Print | `Print` | `@syncfusion/ej2-react-grids` |
| Column Menu | `ColumnMenu` | `@syncfusion/ej2-react-grids` |
| Context Menu | `ContextMenu` | `@syncfusion/ej2-react-grids` |
| Column Chooser | `ColumnChooser` | `@syncfusion/ej2-react-grids` |
| Reorder | `Reorder` | `@syncfusion/ej2-react-grids` |
| Resize | `Resize` | `@syncfusion/ej2-react-grids` |
| Row Drag & Drop | `RowDD` | `@syncfusion/ej2-react-grids` |
| Freeze | `Freeze` | `@syncfusion/ej2-react-grids` |
| Search | `Search` | `@syncfusion/ej2-react-grids` |
| Summary (Aggregate) | `Aggregate` | `@syncfusion/ej2-react-grids` |
| AutoComplete | `AutoComplete` | `@syncfusion/ej2-react-grids` |
| Clipboard | `Clipboard` | `@syncfusion/ej2-react-grids` |

---

## Property Notes

- **Core properties** (dataSource, columns, query) require no module injection
- **Performance**: Use `enableVirtualization` for datasets >1000 rows, `enableInfiniteScrolling` for continuous loading
- **State Persistence**: Set `enablePersistence: true` + `ej2StatePersistenceVersion` to maintain state across page reloads
- **Accessibility**: Enable `enableRtl` for RTL languages, `enableKeyboard` for keyboard navigation
- **Formatting**: `clipMode: 'Ellipsis'` for overflow text, `enableTextWrap: true` for multi-line cells
- **Selection**: `selectionSettings.type: 'Multiple'` allows multi-select, `mode: 'Cell'` for cell selection
- **Editing**: Inject `Edit` module and set `editSettings.mode` to "Dialog", "Batch", "InlineEdit", or "InlineAdd"
