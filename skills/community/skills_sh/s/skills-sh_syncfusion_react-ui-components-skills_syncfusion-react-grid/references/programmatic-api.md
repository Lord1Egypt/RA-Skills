# Programmatic Control

## Table of Contents
- [Overview](#overview)
- [Mandatory Usage Rules](#mandatory-usage-rules)
- [Complete Method Reference](#complete-method-reference)
  - [Data & Module Methods (11)](#data--module-methods-11)
  - [Row Access Methods (9)](#row-access-methods-9)
  - [Row Manipulation Methods (9)](#row-manipulation-methods-9)
  - [Row Selection Methods (12)](#row-selection-methods-12)
  - [Frozen Row/Cell Methods (9)](#frozen-rowcell-methods-9)
  - [Column Access Methods (10)](#column-access-methods-10)
  - [Column Manipulation Methods (10)](#column-manipulation-methods-10)
  - [Column Selection Methods (3)](#column-selection-methods-3)
  - [Sorting & Grouping Methods (8)](#sorting--grouping-methods-8)
  - [Filtering Methods (2)](#filtering-methods-2)
  - [Paging & Navigation Methods (2)](#paging--navigation-methods-2)
  - [Editing Methods (5)](#editing-methods-5)
  - [Batch Operation Methods (3)](#batch-operation-methods-3)
  - [Export & Print Methods (6)](#export--print-methods-6)
  - [Dialog & UI Methods (4)](#dialog--ui-methods-4)
  - [DOM Element Methods (14)](#dom-element-methods-14)
  - [Utility Methods (16)](#utility-methods-16)
- [Quick Usage Examples](#quick-usage-examples)

---

## Overview

Access all Grid methods through `gridRef.current` after attaching the ref to `<GridComponent>`. Methods enable programmatic control: data manipulation, selection, filtering, editing, export, and DOM navigation.

```tsx
const gridRef = useRef(null);
<GridComponent ref={gridRef} dataSource={data} />
```

---

## Mandatory Usage Rules

**CRITICAL**: Follow these rules when using Grid's

### Rule 1: Grid Ref is MANDATORY for Method Calls
```tsx
// ❌ WRONG - No ref
<GridComponent dataSource={data} />

// ✅ CORRECT - Use ref for method access
const gridRef = useRef(null);
<GridComponent ref={gridRef} dataSource={data} />
// Access methods: gridRef.current.addRecord(data)
```

### Rule 2: Primary Key Required for Data Manipulation Methods
Methods like `setCellValue()`, `deleteRecord()` require `isPrimaryKey={true}` on unique column.

```tsx
// ❌ WRONG - Methods fail silently
<ColumnDirective field='OrderID' />

// ✅ CORRECT
<ColumnDirective field='OrderID' isPrimaryKey={true} />

```

### Rule 3: Async Methods Must Be Awaited
Export and some data methods return Promises.

```tsx
// ❌ WRONG - Export might not complete
const handleExport = () => {
  gridRef.current.excelExport();
};

// ✅ CORRECT - Wait for completion
const handleExport = async () => {
  await gridRef.current.excelExport();
  console.log('Export complete');
};
```

### Rule 4: Use Correct Method Parameters
Check method signatures - wrong parameters = silent failure.

```tsx
// ❌ WRONG - Missing required parameters
gridRef.current.filterByColumn('Freight', 100);

// ✅ CORRECT - All 3 parameters required
gridRef.current.filterByColumn('Freight', 'greaterThan', 100);

// ❌ WRONG - Wrong parameter type
gridRef.current.selectRows(0); // Number instead of array

// ✅ CORRECT
gridRef.current.selectRows([0, 2, 4]); // Array required
```

### Rule 5: Check Return Values from Getter Methods
Don't assume methods return data - always validate.

```tsx
// ❌ WRONG - Might be undefined/empty
const selected = gridRef.current.getSelectedRecords();
console.log(selected[0].OrderID); // Crashes if empty

// ✅ CORRECT - Check before use
const selected = gridRef.current.getSelectedRecords();
if (selected && selected.length > 0) {
  console.log(selected[0].OrderID);
}
```

### Rule 5: Edit Methods Require editSettings Configuration
```tsx
// ❌ WRONG - addRecord() fails silently
<GridComponent dataSource={data} />
gridRef.current.addRecord(newData);

// ✅ CORRECT
<GridComponent 
  dataSource={data}
  editSettings={{ allowAdding: true, allowEditing: true, allowDeleting: true }}
>
  <Inject services={[Edit]} />
</GridComponent>
gridRef.current.addRecord(newData);
```

---

## Complete Method Reference

### Data & Module Methods (11)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `refresh()` | None | void | Refreshes the Grid header and content |
| `dataBind()` | None | void | When invoked, applies pending property changes immediately |
| `changeDataSource(dataSource, columns?, properties?)` | Object \| DataManager, Column[]?, Object? | void | Remove existing columns and refresh with new data source |
| `getDataModule()` | None | Data | Returns the data module used by the grid |
| `getCurrentViewRecords()` | None | Object[] | Get current visible data of grid |
| `calculatePageSizeByParentHeight(containerHeight)` | number \| string | number | Calculates page size by parent element height |
| `getRootElement()` | None | HTMLElement | Returns the root element of the component |
| `destroy()` | None | void | Destroys the component (detaches handlers, clears element) |
| `appendTo(selector?)` | string \| Element? | void | Appends control within given HTML element |
| `getPersistData()` | None | string | Get properties to maintain in persisted state |
| `Inject(moduleList)` | Function[] | void | Dynamically injects required modules |

### Row Access Methods (9)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `getRowByIndex(index)` | number | Element | Gets row DOM element by index |
| `getRowIndexByPrimaryKey(value)` | string \| number \| Object | number | Find row index by primary key or row data |
| `getRowInfo(target)` | Element \| EventTarget | RowInfo | Get row metadata based on cell element |
| `getRows()` | None | Element[] | Gets all data row DOM elements |
| `getDataRows()` | None | Element[] | Gets all Grid's data rows |
| `getRowsObject()` | None | Row[] | Get array of row objects with metadata |
| `getHiddenColumns()` | None | Column[] | Gets hidden columns from Grid |
| `getForeignKeyColumns()` | None | Column[] | Gets foreign key columns from Grid |
| `getPrimaryKeyFieldNames()` | None | string[] | Get names of primary key columns |

### Row Manipulation Methods (9)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `addRecord(data?, index?)` | Object?, number? | void | Adds new record to Grid |
| `updateRow(index, data)` | number, Object | void |  Update row data at specified index |
| `updateCell(rowIndex, field, value)` | number, string, any | void | Update single cell in row |
| `setCellValue(key, field, value)` | string \| number, string, any | void | Updates cell value by primary key |
| `setRowData(key, rowData?)` | string \| number, Object? | void | Updates and refresh row by primary key |
| `deleteRecord(fieldname?, data?)` | string?, Object? | void | Delete record by key field + record object |
| `deleteRow(tr)` | HTMLTableRowElement | void | Delete visible row by TR element |
| `reorderRows(fromIndexes, toIndex)` | number[], number | void | Changes row positions by indexes |
| `copy(withHeader?)` | boolean? | void | Copy selected rows or cells to clipboard |

### Row Selection Methods (12)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `selectRow(index, isToggle?)` | number, boolean? | void | Selects single row by index |
| `selectRows(rowIndexes, clearPrevious?)` | number \| number[], boolean? | void | Selects rows by index array |
| `selectRowsByRange(startIndex, endIndex?)` | number, number? | void | Selects range of rows from start to end |
| `getSelectedRows()` | None | Element[] | Gets selected row DOM elements |
| `getSelectedRecords()` | None | Object[] | Gets selected row data (objects) |
| `getSelectedRowIndexes()` | None | number[] | Gets index array of selected rows |
| `getSelectedRowCellIndexes()` | None | ISelectedCell[] | Gets selected cell indexes |
| `getSelectedColumnsUid()` | None | string[] | Gets collection of selected columns UID |
| `clearRowSelection()` | None | void | Deselects all rows only |
| `clearCellSelection()` | None | void | Deselects all cells only |
| `clearSelection()` | None | void | Deselects current selected rows and cells |
| `saveCell()` | None | void | Saves currently edited cell without changing state |

### Frozen Row/Cell Methods (9)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `getFrozenDataRows()` | None | Element[] | Gets all frozen table data rows |
| `getFrozenRowByIndex(index)` | number | Element | Gets frozen row element by index |
| `getFrozenLeftColumnHeaderByIndex(index)` | number | Element | Gets frozen left header cell by index |
| `getFrozenRightRows()` | None | Element[] | Gets frozen right-side row elements |
| `getFrozenRightRowByIndex(index)` | number | Element | Gets frozen right row by index |
| `getFrozenRightColumnHeaderByIndex(index)` | number | Element | Gets frozen right header cell by index |
| `getFrozenRightDataRows()` | None | Element[] | Gets frozen right data rows |
| `getFrozenRightCellFromIndex(rowIndex, columnIndex)` | number, number | Element | Gets frozen right cell by row/col index |
| `freezeRefresh()` | None | void | Refreshes frozen column/row display |

### Column Access Methods (10)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `getColumns(isRefresh?)` | boolean? | Column[] | Gets columns from Grid |
| `getVisibleColumns()` | None | Column[] | Gets only visible column objects |
| `getColumnByField(field)` | string | Column | Gets column by field name |
| `getColumnByUid(uid, isColumns?)` | string, boolean? | Column | Gets column by UID identifier |
| `getColumnFieldNames()` | None | string[] | Gets array of all field names |
| `getColumnHeaderByField(field)` | string | Element | Gets column header element by field |
| `getColumnHeaderByIndex(index)` | number | Element | Gets header cell element by column index |
| `getColumnHeaderByUid(uid)` | string | Element | Gets header cell element by UID |
| `getColumnIndexByField(field)` | string | number | Gets column index by field name |
| `getColumnIndexByUid(uid)` | string | number | Gets column index by UID |

### Column Manipulation Methods (10)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `showColumns(keys, showBy?)` | string \| string[], string? | void | Shows columns by headerText or field |
| `hideColumns(keys, hideBy?)` | string \| string[], string? | void | Hides columns by headerText or field |
| `autoFitColumns(fieldNames?, startRowIndex?, endRowIndex?)` | string \| string[]?, number?, number? | void | Auto-fits columns to content width |
| `reorderColumnByIndex(fromIndex, toIndex)` | number, number | void | Moves column from one index to another |
| `reorderColumnByModel(fromColumn, toColumn)` | Column, Column | void | Reorders column in Grid by column models |
| `reorderColumnByTargetIndex(fieldName, toIndex)` | string \| string[], number | void | Moves column by field to target index |
| `reorderColumns(fromFName, toFName)` | string \| string[], string | void | Changes column positions by field names |
| `hideScroll()` | None | void | Hides grid scroll bars |
| `refreshColumns()` | None | void | Refreshes column header display |
| `refreshHeader()` | None | void | Refreshes grid header |

### Column Selection Methods (3)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `selectCell(cellIndex, isToggle?)` | IIndex, boolean? | void | Selects single cell by row and column index |
| `selectCells(rowCellIndexes)` | ISelectedCell[] | void | Selects multiple cells by index |
| `selectCellsByRange(startIndex, endIndex?)` | IIndex, IIndex? | void | Selects range of cells from start to end |

### Sorting & Grouping Methods (8)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `sortColumn(columnName, direction, isMultiSort?)` | string, string, boolean? | void | Sorts column Ascending/Descending |
| `clearSorting()` | None | void | Removes all sort configurations |
| `groupColumn(columnName, direction?)` | string, string? | void | Groups by column field |
| `ungroupColumn(columnName)` | string | void | Removes grouping from column |
| `groupCollapseAll()` | None | void | Collapses all grouped rows |
| `groupExpandAll()` | None | void | Expands all grouped rows |
| `search(searchString)` | string | void | Performs global grid search |
| `getFilterUIInfo()` | None | FilterUI | Get current filter operator and field  |

### Filtering Methods (2)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `filterByColumn(fieldName, filterOperator, filterValue, predicate?, matchCase?, ignoreAccent?, actualFilterValue?, actualOperator?)` | string, string, any, string?, boolean?, boolean?, string?, string? | void | Filters grid row by column with options |
| `clearFiltering(fields?)` | string[]? | void | Clears all filters or specific column filters |

### Paging & Navigation Methods (2)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `goToPage(pageNo)` | number | void | Navigates to specified page number |
| `getPager()` | None | Element | Gets pager DOM element |

### Editing Methods (5)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `startEdit()` | None | void | Begins editing currently selected row |
| `endEdit()` | None | void | Confirms and saves edit changes |
| `closeEdit()` | None | void | Cancels edit without saving |
| `editCell(index, field)` | number, string | void | Changes cell into edited state (batch mode) |
| `enableToolbarItems(items, isEnable)` | string[], boolean | void | Enables or disables toolbar items |

### Batch Operation Methods (3)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `batchUpdate(changes)` | BatchChanges | void | Apply changes to Grid without refreshing rows |
| `batchAsyncUpdate(changes)` | BatchChanges | void | Apply changes after 50ms without refreshing rows  |
| `getBatchChanges()` | None | Object | Gets added, edited, deleted data before bulk save |

### Export & Print Methods (6)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `excelExport(excelExportProperties?, isMultipleExport?, workbook?, isBlob?)` | ExcelExportProperties?, boolean?, Workbook?, boolean? | Promise | Exports Grid data to Excel file |
| `pdfExport(pdfExportProperties?, isMultipleExport?, pdfDoc?, isBlob?)` | PdfExportProperties?, boolean?, Object?, boolean? | Promise | Exports Grid data to PDF document |
| `csvExport(excelExportProperties?, isMultipleExport?, workbook?, isBlob?)` | ExcelExportProperties?, boolean?, Workbook?, boolean? | Promise | Exports Grid to CSV file |
| `serverExcelExport(url, headers?)` | string, ExportHeaders? | void | Server-side Excel export POST request |
| `serverPdfExport(url, headers?)` | string, ExportHeaders? | void | Server-side PDF export POST request |
| `serverCsvExport(url, headers?)` | string, ExportHeaders? | void | Server-side CSV export POST request |

### Dialog & UI Methods (4)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `print()` | None | void | Prints grid with current data |
| `openColumnChooser(x?, y?)` | number?, number? | void | Opens column chooser dialog at position |
| `showAdaptiveFilterDialog()` | None | void | Shows adaptive filter dialog |
| `showAdaptiveSortDialog()` | None | void | Shows adaptive sort dialog |

### DOM Element Methods (14)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `getContent()` | None | Element | Gets grid content wrapper element |
| `getContentTable()` | None | Element | Gets main data table element |
| `getHeaderContent()` | None | Element | Gets header content wrapper element |
| `getHeaderTable()` | None | Element | Gets header table element |
| `getFooterContent()` | None | Element | Gets footer content wrapper element |
| `getFooterContentTable()` | None | Element | Gets footer table element |
| `getMovableRowByIndex(index)` | number | Element | Gets movable (scrollable) row by index |
| `getMovableDataRows()` | None | Element[] | Gets all movable data row elements |
| `getMovableRows()` | None | Element[] | Gets all movable rows including headers |
| `getMovableCellFromIndex(rowIndex, columnIndex)` | number, number | Element | Gets cell in movable area by indexes |
| `getMovableColumnHeaderByIndex(index)` | number | Element | Gets movable column header by index |
| `getCellFromIndex(rowIndex, columnIndex)` | number, number | Element | Gets cell element by row/col index |
| `setGridContent(element)` | Element | void | Sets grid content to replace old content |
| `setGridContentTable(element)` | Element | void | Sets content table to replace old table |

### Utility Methods (16)

| Method | Parameters | Return | Purpose |
|--------|-----------|--------|---------|
| `addEventListener(eventName, handler)` | string, Function | void | Adds handler to event listener |
| `removeEventListener(eventName, handler)` | string, Function | void | Removes handler from event listener |
| `destroyTemplate(propertyNames?, index?, callback?)` | string[]?, any?, Function? | void | Destroys compiled templates |
| `detailCollapseAll()` | None | void | Collapses all detail rows |
| `detailExpandAll()` | None | void | Expands all detail rows |
| `pinRows(data)` | Object[] | void | Freezes (pins) rows using data |
| `unpinRows(data)` | Object[] | void | Unfreezes (unpins) rows using data |
| `showSpinner()` | None | void | Shows loading spinner indicator |
| `hideSpinner()` | None | void | Hides loading spinner indicator |
| `updateExternalMessage(message)` | string | void | Updates external message text |
| `setGridHeaderContent(element)` | Element | void | Sets header content to replace old header |
| `setGridHeaderTable(element)` | Element | void | Sets header table to replace old one |
| `setGridPager(element)` | Element | void | Sets pager to replace old pager |
| `getSummaryValues(summaryCol, summaryData)` | AggregateColumnModel, Object | number | Performs aggregate operation on column |
| `getUidByColumnField(field)` | string | string | Gets UID by column name |
| `getFilteredRecords()` | None | Object[] \| Promise | Gets records matching current filters |

---

## Quick Usage Examples

```tsx
// Navigate pages
gridRef.current.goToPage(2);

// Manipulate data
gridRef.current.addRecord({ OrderID: 99, Freight: 25 });
gridRef.current.deleteRecord('OrderID', selectedRecord);
gridRef.current.updateRow(0, { Freight: 50 });

// Selection
gridRef.current.selectRows([0, 2, 4]);
const selected = gridRef.current.getSelectedRecords();

// Column operations
gridRef.current.autoFitColumns(['OrderID', 'Freight']);
gridRef.current.sortColumn('Freight', 'Descending');
gridRef.current.search('searchTerm');

// Export
await gridRef.current.excelExport({ fileName: 'data.xlsx' });
```

### Toolbar Methods
```tsx
gridRef.current.toolbarModule.enableItems(['Add', 'Edit'], true)     // Enable items
gridRef.current.toolbarModule.enableItems(['Delete', 'Update'], false) // Disable items
```

### Hierarchy / Detail Row Methods
```tsx
gridRef.current.detailRowModule.detailsExpand([0, 1, 2])   // Expand detail rows by index
gridRef.current.detailRowModule.detailsCollapse([0, 1, 2]) // Collapse detail rows
```