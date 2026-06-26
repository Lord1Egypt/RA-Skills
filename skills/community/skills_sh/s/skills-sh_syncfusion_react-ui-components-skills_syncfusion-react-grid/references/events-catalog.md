# Syncfusion React Grid — Complete Events Catalog

## Table of Contents
- [Mandatory Rules](#mandatory-rules-for-inbuilt-api)
- [All 85 Grid Events by Category](#all-85-grid-events-by-category)
  - [Lifecycle Events (4)](#lifecycle-events-4)
  - [Action Events (3)](#action-events-3)
  - [Row Events (10)](#row-events-10)
  - [Cell Events (8)](#cell-events-8)
  - [Edit & Batch Events (11)](#edit--batch-events-11)
  - [Column Events (14)](#column-events-14)
  - [Data State Events (4)](#data-state-events-4)
  - [Export & Print Events (16)](#export--print-events-16)
  - [Detail Row & Hierarchy (5)](#detail-row--hierarchy-5)
  - [Menu & Toolbar Events (5)](#menu--toolbar-events-5)
  - [Copy/Paste Events (2)](#copypaste-events-2)
  - [Scroll Events (2)](#scroll-events-2)
  - [Dialog & Adaptive Events (2)](#dialog--adaptive-events-2)
  - [Other Events (3)](#other-events-3)
- [requestType Full Catalog](#requesttype-full-catalog)
- [Cancellation Patterns](#cancellation-patterns)
- [Event Timing & Firing Order](#event-timing--firing-order)

---

## Mandatory Rules for Inbuilt API

**CRITICAL**: Follow these rules when using Grid's

### Rule 1: Event Handlers Must Match Exact Signature
Wrong event signatures cause silent failures or crashes.

```tsx
// ❌ WRONG - Missing args parameter
<GridComponent actionComplete={() => console.log('done')} />

// ✅ CORRECT - Accept args parameter
<GridComponent actionComplete={(args) => {
  console.log('Request type:', args.requestType);
}} />
```

### Rule 2: Use actionBegin for Cancellation, actionComplete for Reactions

**actionBegin vs actionComplete — Decision Rule**

| Use `actionBegin` when you need to | Use `actionComplete` when you need to |
|---|---|
| Cancel / stop the action (`args.cancel = true`) | Call backend API after save/delete |
| Modify data before save (`args.data.field = value`) | Show toast / notification |
| Confirm before delete | Refresh grid data |
| Block unauthorized actions | Sync external React state |
| Customize export before start | Re-enable toolbar buttons |

**Example 1:**

```tsx
// actionBegin � intercept and mutate
const actionBegin = (args) => {
  if (args.requestType === 'delete')
    args.cancel = !window.confirm(`Delete record ${args.data[0]?.OrderID}?`);

  if (args.requestType === 'save') {
    args.data.UpdatedAt = new Date().toISOString();
    args.data.UpdatedBy = currentUser.id;
  }

  if (['add', 'beginEdit'].includes(args.requestType)) {
    gridRef.current.toolbarModule.enableItems(['Add', 'Edit', 'Delete'], false);
    gridRef.current.toolbarModule.enableItems(['Update', 'Cancel'], true);
  }
};

// actionComplete � react after action
const actionComplete = async (args) => {
  if (args.requestType === 'save') {
    await apiService.syncRecord(args.data);
    showToast('Record saved');
    gridRef.current.clearSelection();
    gridRef.current.toolbarModule.enableItems(['Add', 'Edit', 'Delete'], true);
    gridRef.current.toolbarModule.enableItems(['Update', 'Cancel'], false);
  }
  if (args.requestType === 'delete') {
    await apiService.deleteRecord(args.data[0]);
    gridRef.current.refresh();
  }
};
```

**Example 2:**

```tsx
<GridComponent
  actionBegin={(args) => {
    // Cancel action before it executes
    if (args.requestType === 'save' && !isValid) {
      args.cancel = true;
    }
  }}
  actionComplete={(args) => {
    // React after action completes
    if (args.requestType === 'save') {
      toast.success('Saved!');
    }
  }}
  actionFailure={(args) => {
    // MANDATORY - Handle errors
    console.error(args.error);
  }}
/>
```

### Rule 3: Event Timing Matters
Know when events fire relative to action execution:

| Event | Timing | Can Cancel? | Use For |
|-------|--------|-------------|---------|
| `actionBegin` | Before action starts | ✅ Yes | Validation, cancellation |
| `actionComplete` | After action finishes | ❌ No | Success handling, API calls |
| `actionFailure` | On error | ❌ No | Error handling |
| `rowSelecting` | Before selection | ✅ Yes | Prevent selection |
| `rowSelected` | After selection | ❌ No | React to selection |

### Rule 4: Don't Call Methods Inside Render Events
```tsx
// ❌ FORBIDDEN - Causes infinite loops
<GridComponent
  queryCellInfo={(args) => {
    gridRef.current.refresh(); // NEVER DO THIS
  }}
  rowDataBound={(args) => {
    gridRef.current.selectRow(0); // NEVER DO THIS
  }}
/>

// ✅ CORRECT - Use proper events
<GridComponent
  actionComplete={(args) => {
    if (args.requestType === 'refresh') {
      // Safe to call methods here
    }
  }}
/>
```

---

## All 85 Grid Events by Category

### Lifecycle Events (4)

| Event | Type | Use Case |
|-------|------|----------|
| `created` | `EmitType<Object>` | Grid initialized and rendered (use for initial setup) |
| `load` | `EmitType<Object>` | Before data binding (customize grid before data loads) |
| `dataBound` | `EmitType<Object>` | After data bound and rows rendered (perform post-render actions) |
| `destroyed` | `EmitType<Object>` | Component destroyed (cleanup subscriptions, timers) |

**Example:**
```tsx
<GridComponent
  load={() => console.log('loading')}
  dataBound={() => console.log('rendered')}
  destroyed={() => console.log('cleaned up')}
/>
```

### Action Events (3)

| Event | Type | Use Case |
|-------|------|----------|
| `actionBegin` | `EmitType<...>` | Before ANY action (paging, sort, filter, edit, etc.) — Check `args.requestType` |
| `actionComplete` | `EmitType<...>` | After ANY action completes |
| `actionFailure` | `EmitType<FailureEventArgs>` | On action error — MANDATORY to wire for error handling |

**Example:**
```tsx
<GridComponent
  actionBegin={(args) => {
    if (args.requestType === 'delete') args.cancel = !confirm('Delete?');
  }}
  actionComplete={(args) => {
    if (args.requestType === 'save') console.log('Saved');
  }}
  actionFailure={(args) => console.error(args.error)}
/>
```

### Row Events (10)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `rowDataBound` | `EmitType<RowDataBoundEventArgs>` | ❌ | Per row during render — style rows conditionally |
| `rowSelecting` | `EmitType<RowSelectingEventArgs>` | ✅ | Before row selection — prevent selecting locked rows |
| `rowSelected` | `EmitType<RowSelectEventArgs>` | ❌ | After row selected — update external state |
| `rowDeselecting` | `EmitType<RowDeselectingEventArgs>` | ✅ | Before deselection — custom validation |
| `rowDeselected` | `EmitType<RowDeselectEventArgs>` | ❌ | After deselection |
| `recordClick` | `EmitType<RecordClickEventArgs>` | ❌ | Single row click |
| `recordDoubleClick` | `EmitType<RecordDoubleClickEventArgs>` | ❌ | Double row click — common for edit trigger |
| (Reserved) | | | |
| (Reserved) | | | |
| (Reserved) | | | |

### Cell Events (8)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `queryCellInfo` | `EmitType<QueryCellInfoEventArgs>` | ❌ | Per cell during render — style cells, customize content |
| `cellSelecting` | `EmitType<CellSelectingEventArgs>` | ✅ | Before cell select — prevent selecting specific cells |
| `cellSelected` | `EmitType<CellSelectEventArgs>` | ❌ | After cell selected |
| `cellDeselecting` | `EmitType<CellDeselectEventArgs>` | ✅ | Before cell deselect |
| `cellDeselected` | `EmitType<CellDeselectEventArgs>` | ❌ | After cell deselected |
| `cellEdit` | `EmitType<CellEditArgs>` | ✅ | Cell entered edit mode (Batch only) — prevent editing primary key |
| `cellSave` | `EmitType<CellSaveArgs>` | ❌ | Cell saved (Batch mode) |
| `cellSaved` | `EmitType<CellSaveArgs>` | ❌ | After cell saved |

### Edit & Batch Events (11)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `beginEdit` | `EmitType<BeginEditArgs>` | ✅ | Edit mode started (Inline/Dialog) — prevent editing certain records |
| `batchAdd` | `EmitType<BatchAddArgs>` | ❌ | Batch: new empty row added |
| `batchDelete` | `EmitType<BatchDeleteArgs>` | ❌ | Batch: row deleted |
| `batchCancel` | `EmitType<BatchCancelArgs>` | ❌ | Batch: edit cancelled |
| `beforeBatchAdd` | `EmitType<BeforeBatchAddArgs>` | ✅ | Before batch add — block adding conditionally |
| `beforeBatchDelete` | `EmitType<BeforeBatchDeleteArgs>` | ✅ | Before batch delete — confirm deletion |
| `beforeBatchSave` | `EmitType<BeforeBatchSaveArgs>` | ✅ | Before batch save — validate changes, cancel if invalid |
| (Reserved) | | | |
| (Reserved) | | | |
| (Reserved) | | | |
| (Reserved) | | | |

### Column Events (14)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `columnDragStart` | `EmitType<ColumnDragEventArgs>` | ❌ | Column drag starts |
| `columnDrag` | `EmitType<ColumnDragEventArgs>` | ❌ | Column dragging continuously |
| `columnDrop` | `EmitType<ColumnDragEventArgs>` | ❌ | Column dropped on target |
| `columnDataStateChange` | `EmitType<ColumnDataStateChangeEventArgs>` | ❌ | Column data state changed (sort/filter/group on this column) |
| `columnDeselecting` | `EmitType<ColumnDeselectEventArgs>` | ✅ | Before column deselect |
| `columnDeselected` | `EmitType<ColumnDeselectEventArgs>` | ❌ | After column deselected |
| `columnSelecting` | `EmitType<ColumnSelectingEventArgs>` | ✅ | Before column select |
| `columnSelected` | `EmitType<ColumnSelectEventArgs>` | ❌ | After column selected |
| `columnMenuClick` | `EmitType<MenuEventArgs>` | ❌ | Column menu item clicked |
| `columnMenuOpen` | `EmitType<ColumnMenuOpenEventArgs>` | ✅ | Before column menu opens — modify menu items dynamically |
| `columnMenuClose` | `EmitType<ColumnMenuOpenEventArgs>` | ✅ | Before column menu closes |
| `resizeStart` | `EmitType<ResizeArgs>` | ❌ | Column resize starts |
| `resizing` | `EmitType<ResizeArgs>` | ❌ | Column resizing continuously |
| `resizeStop` | `EmitType<ResizeArgs>` | ❌ | Column resize ends — state auto-saved if persistence enabled |

### Data State Events (4)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `dataStateChange` | `EmitType<DataStateChangeEventArgs>` | ❌ | Grid actions (sort/filter/group/page) completed — update data from API |
| `columnDataStateChange` | `EmitType<ColumnDataStateChangeEventArgs>` | ❌ | Column-specific data state change |
| `dataSourceChanged` | `EmitType<DataSourceChangedEventArgs>` | ❌ | Data added/deleted/updated — invoke done() to render |
| `beforeDataBound` | `EmitType<BeforeDataBoundArgs>` | ❌ | Before data binding — intercept before rendering rows |

### Export & Print Events (16)

| Event | Type | Use Case |
|-------|------|----------|
| `beforeExcelExport` | `EmitType<Object>` | Modify Excel workbook before export (args.workbook) |
| `excelExportComplete` | `EmitType<ExcelExportCompleteArgs>` | Excel export finished |
| `excelQueryCellInfo` | `EmitType<ExcelQueryCellInfoEventArgs>` | Before exporting each cell to Excel — customize cell style/value |
| `excelHeaderQueryCellInfo` | `EmitType<ExcelHeaderQueryCellInfoEventArgs>` | Before exporting each header cell to Excel |
| `excelAggregateQueryCellInfo` | `EmitType<AggregateQueryCellInfoEventArgs>` | Before exporting aggregate cell to Excel |
| `beforePdfExport` | `EmitType<Object>` | Modify PDF document before export (args.pdfDocument) |
| `pdfExportComplete` | `EmitType<PdfExportCompleteArgs>` | PDF export finished |
| `pdfQueryCellInfo` | `EmitType<PdfQueryCellInfoEventArgs>` | Before exporting each cell to PDF — customize cell |
| `pdfHeaderQueryCellInfo` | `EmitType<PdfHeaderQueryCellInfoEventArgs>` | Before exporting each header cell to PDF |
| `pdfAggregateQueryCellInfo` | `EmitType<AggregateQueryCellInfoEventArgs>` | Before exporting aggregate cell to PDF |
| `beforePrint` | `EmitType<PrintEventArgs>` | Before print action starts — customize print |
| `printComplete` | `EmitType<PrintEventArgs>` | Print action completed |
| `beforeCustomFilterOpen` | `EmitType<BeforeCustomFilterOpenEventArgs>` | Before custom filter dialog opens |
| `exportDetailDataBound` | `EmitType<ExportDetailDataBoundEventArgs>` | Before exporting each detail grid |
| `exportDetailTemplate` | `EmitType<ExportDetailTemplateEventArgs>` | Before exporting each detail template |
| `exportGroupCaption` | `EmitType<ExportGroupCaptionEventArgs>` | Before exporting each group caption row — customize caption values |

### Detail Row & Hierarchy (5)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `detailExpand` | `EmitType<DetailExpandCollapseArgs>` | ✅ | Before detail row expands — prevent expansion conditionally |
| `detailCollapse` | `EmitType<DetailExpandCollapseArgs>` | ✅ | Before detail row collapses |
| `detailDataBound` | `EmitType<DetailDataBoundEventArgs>` | ❌ | After detail row expands and data bound |
| `beforeDetailTemplateDetach` | `EmitType<DetailTemplateDetachArgs>` | ❌ | Before detail template row removed from DOM — cleanup operations |
| (Reserved) | | | |

### Menu & Toolbar Events (5)

| Event | Type | Use Case |
|-------|------|----------|
| `contextMenuClick` | `EmitType<ContextMenuClickEventArgs>` | Context menu item clicked — identify item via args.item.id |
| `contextMenuOpen` | `EmitType<ContextMenuOpenEventArgs>` | Before context menu opens — modify items dynamically |
| `contextMenuClose` | `EmitType<ContextMenuOpenEventArgs>` | Before context menu closes — custom action |
| `toolbarClick` | `EmitType<ClickEventArgs>` | Toolbar item clicked — identify via args.item.id or args.item.text |
| `commandClick` | `EmitType<CommandClickEventArgs>` | Command button (Edit/Delete/etc. in inline edit) clicked |

### Copy/Paste Events (2)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `beforeCopy` | `EmitType<BeforeCopyEventArgs>` | ✅ | Before copy action — customize copied data |
| `beforePaste` | `EmitType<BeforePasteEventArgs>` | ✅ | Before paste action — validate pasted data, cancel if invalid |

### Scroll Events (2)

| Event | Type | Use Case |
|-------|------|----------|
| `lazyLoadGroupCollapse` | `EmitType<LazyLoadArgs>` | Group collapsed in lazy load grouping |
| `lazyLoadGroupExpand` | `EmitType<LazyLoadArgs>` | Group expanded in lazy load grouping |

### Dialog & Adaptive Events (2)

| Event | Type | Cancellable | Use Case |
|-------|------|------------|----------|
| `beforeOpenAdaptiveDialog` | `EmitType<AdaptiveDialogEventArgs>` | ✅ | Before adaptive filter/sort dialogs open |
| `beforeOpenColumnChooser` | `EmitType<ColumnChooserEventArgs>` | ✅ | Before column chooser dialog opens |

### Other Events (3)

| Event | Type | Use Case |
|-------|------|----------|
| `keyPressed` | `EmitType<KeyboardEventArgs>` | Any keyboard key pressed inside grid |
| `checkBoxChange` | `EmitType<CheckBoxChangeEventArgs>` | Checkbox state changed in checkbox selection column |
| `headerCellInfo` | `EmitType<HeaderCellInfoEventArgs>` | For stacked header customization |

---

## requestType Full Catalog

### CRUD / Edit

| `requestType` | When | Available in | Cancellable |
|---|---|---|---|
| `'add'` | Add clicked / addRecord() called | actionBegin | ✅ |
| `'beginEdit'` | Row double-clicked / Edit clicked | actionBegin | ✅ |
| `'save'` | Record saved (add or edit) | actionBegin, actionComplete | ✅ in actionBegin |
| `'delete'` | Record deleted | actionBegin, actionComplete | ✅ in actionBegin |
| `'cancel'` | Edit cancelled | actionBegin, actionComplete | ❌ |
| `'batchsave'` | Batch mode all changes saved | actionBegin, actionComplete | ✅ in actionBegin |

### Navigation / Data

| `requestType` | When | Available in |
|---|---|---|
| `'sorting'` | Sort applied/removed | actionBegin, actionComplete |
| `'filtering'` | Filter applied/cleared | actionBegin, actionComplete |
| `'searching'` | Global search | actionBegin, actionComplete |
| `'grouping'` | Column grouped | actionBegin, actionComplete |
| `'ungrouping'` | Column ungrouped | actionBegin, actionComplete |
| `'paging'` | Page changed | actionBegin, actionComplete |
| `'refresh'` | Grid refreshed | actionBegin, actionComplete |
| `'reorder'` | Column reordered | actionComplete |

### Export / Print

| `requestType` | When | Available in |
|---|---|---|
| `'excel'` | Excel export | actionBegin |
| `'pdfexport'` | PDF export | actionBegin |
| `'csvexport'` | CSV export | actionBegin |
| `'print'` | Print | actionBegin |

### Scroll

| `requestType` | When | Available in |
|---|---|---|
| `'virtualscroll'` | Virtual scroll chunk loaded | actionComplete |
| `'infiniteScroll'` | Infinite scroll next block | actionComplete |

---

## Cancellation Patterns

Only works in `actionBegin` and specific before-events (marked ✅ in event tables).

```tsx
// Cancel delete with confirmation
actionBegin={(args) => {
  if (args.requestType === 'delete')
    args.cancel = !window.confirm('Delete this record?');
}}

// Cancel add — permission check
actionBegin={(args) => {
  if (args.requestType === 'add' && !userHasRole('editor'))
    args.cancel = true;
}}

// Cancel row selection — locked records
rowSelecting={(args) => {
  if (args.data?.Status === 'Locked') args.cancel = true;
}}

// Cancel cell edit — protect primary key in Batch mode
cellEdit={(args) => {
  if (args.columnName === 'OrderID') args.cancel = true;
}}

// Cancel batch save — custom validation
beforeBatchSave={(args) => {
  const errors = validateBatchChanges(args.batchChanges);
  if (errors.length > 0) { args.cancel = true; showValidationDialog(errors); }
}}

// Cancel paste — validate pasted data
beforePaste={(args) => {
  if (!isValidPasteData(args.data)) args.cancel = true;
}}
```

---

## Event Timing & Firing Order

| Scenario | Event Sequence |
|----------|---|
| **Page Load** | `load` → `dataBound` |
| **Row Selection** | `rowSelecting` → `rowSelected` |
| **Row Deselection** | `rowDeselecting` → `rowDeselected` |
| **Single Click** | `recordClick` → `rowSelected` (if allowSelection) |
| **Double Click** | `recordDoubleClick` → `beginEdit` (if edit enabled) |
| **Edit Inline** | `beginEdit` → `cellEdit`/`cellSave` (per cell in batch) → `actionComplete` |
| **Edit Dialog** | `beginEdit` → `actionBegin` (requestType='save') → `actionComplete` |
| **Sort** | `actionBegin` (requestType='sorting') → `actionComplete` → `dataBound` |
| **Filter** | `actionBegin` (requestType='filtering') → `actionComplete` → `dataBound` |
| **Page Change** | `actionBegin` (requestType='paging') → `actionComplete` → `dataBound` |
| **Excel Export** | `beforeExcelExport` → `excelQueryCellInfo` (per cell) → `excelExportComplete` |
| **PDF Export** | `beforePdfExport` → `pdfQueryCellInfo` (per cell) → `pdfExportComplete` |
| **Virtual Scroll** | `actionBegin` (requestType='virtualscroll') → `actionComplete` → `rowDataBound` (new rows) |
| **Detail Expand** | `detailExpand` → `detailDataBound` |
| **Detail Collapse** | `detailCollapse` |
| **Batch Add** | `beforeBatchAdd` → `batchAdd` |
| **Batch Delete** | `beforeBatchDelete` → `batchDelete` |
| **Batch Save** | `beforeBatchSave` → `actionBegin` (requestType='batchsave') → `actionComplete` |
