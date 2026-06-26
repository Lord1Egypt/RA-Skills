# Events — Syncfusion Blazor DataGrid

## ⚠️ CRITICAL RULE: Use Specific Events, NOT Generic OnActionBegin/OnActionComplete

**DO NOT use `OnActionBegin` and `OnActionComplete` for operations with dedicated events.**

### ❌ WRONG - Using Generic Events

```razor
<GridEvents TValue="Order" OnActionBegin="OnActionBegin">
</GridEvents>

@code {
    void OnActionBegin(ActionEventArgs<Order> args)
    {
        if (args.RequestType == "sorting") { /* handle sort */ }
        if (args.RequestType == "filtering") { /* handle filter */ }
        if (args.RequestType == "paging") { /* handle page */ }
        if (args.RequestType == "grouping") { /* handle group */ }
        // ... string comparisons, casting, weak typing
    }
}
```

**Problems:**
- ❌ Weak typing (string-based `RequestType`)
- ❌ Manual type casting required
- ❌ No IntelliSense for operation-specific data
- ❌ Error-prone and hard to maintain
- ❌ Performance hit: all operations trigger single handler

### ✅ CORRECT - Use Specific Events with Typed Arguments

```razor
<GridEvents TValue="Order"
            Sorting="OnSorting"
            Filtered="OnFiltered"
            PageChanged="OnPageChanged"
            Grouped="OnGrouped"
            RowUpdating="OnRowUpdating"
            RowSelected="OnRowSelected">
</GridEvents>

@code {
    void OnSorting(SortingEventArgs args) { /* Strong typing */ }
    void OnFiltered(FilteredEventArgs args) { /* Strong typing */ }
    void OnPageChanged(PageChangeEventArgs args) { /* Strong typing */ }
    void OnGrouped(GroupedEventArgs args) { /* Strong typing */ }
    void OnRowUpdating(RowUpdatingEventArgs<Order> args) { /* Strong typing */ }
    void OnRowSelected(RowSelectEventArgs<Order> args) { /* Strong typing */ }
}
```

**Benefits:**
- ✅ Type-safe event arguments
- ✅ IntelliSense support
- ✅ Compiler-checked implementations
- ✅ Clear, specific handler per operation
- ✅ Better performance (only subscribed handlers fire)

### When to Use OnActionBegin/OnActionComplete

Use **ONLY** for:
1. **Logging/Debugging** - Log all grid operations to console
2. **Catch-all Security Checks** - Block all operations conditionally
3. **Operations WITHOUT specific events** - (Rare; check this list first)

```razor
<!-- Logging example -->
<GridEvents TValue="Order" OnActionBegin="LogAllOperations"></GridEvents>

@code {
    void LogAllOperations(ActionEventArgs<Order> args)
    {
        Console.WriteLine($"[GRID] Operation: {args.RequestType}");
        // Don't handle specific logic here — only logging
    }
}
```

---

## GridEvents Component

All events are configured inside a single `<GridEvents>` component with `TValue` matching the grid's data model:

```razor
<SfGrid DataSource="@Orders">
    <GridEvents TValue="Order"
                OnActionBegin="OnActionBegin"
                OnActionComplete="OnActionComplete"
                DataBound="OnDataBound"
                RowDataBound="OnRowDataBound">
    </GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## Lifecycle Events

| Event | Args | Description |
|---|---|---|
| `OnLoad` | `object` | Fires before the grid renders |
| `Created` | `object` | Fires after the grid is created |
| `DataBound` | `object` | Fires after data is bound to the grid |
| `OnDataBound` | `BeforeDataBoundArgs<T>` | Fires just before data is bound; cancel or modify |
| `Destroyed` | `object` | Fires when the grid is destroyed |

## Action Events

| Event | Args | Cancelable | Description |
|---|---|---|---|
| `OnActionBegin` | `ActionEventArgs<T>` | ✅ | Fires when any grid action starts (sort, filter, page, group, edit…) |
| `OnActionComplete` | `ActionEventArgs<T>` | ❌ | Fires after any grid action completes |
| `OnActionFailure` | `FailureEventArgs` | ❌ | Fires on data operation failure |

**Inspect request type in OnActionBegin:**

```razor
void OnActionBegin(ActionEventArgs<Order> args)
{
    // args.RequestType: "sorting", "filtering", "paging", "grouping", etc.
    if (args.RequestType == "delete")
        args.Cancel = true; // prevent deletion
}
```

## Row Events

| Event | Args | Cancelable | Description |
|---|---|---|---|
| `RowDataBound` | `RowDataBoundEventArgs<T>` | ❌ | Fires when each row is data-bound; used for row styling |
| `DetailDataBound` | `DetailDataBoundEventArgs<T>` | ❌ | Fires after a detail row expands; use to modify expanded content or initialize child components |
| `OnRecordClick` | `RecordClickEventArgs<T>` | ❌ | Fires on row single-click |
| `OnRecordDoubleClick` | `RecordDoubleClickEventArgs<T>` | ❌ | Fires on row double-click |
| `CommandClicked` | `CommandClickEventArgs<T>` | ❌ | Fires when a command column button is clicked; provides the row data for the clicked row |
| `RowDragStarting` | `RowDragEventArgs<T>` | ✅ | Fires before row drag starts |
| `RowDropping` | `RowDroppingEventArgs<T>` | ✅ | Fires before row is dropped |
| `RowDropped` | `RowDroppedEventArgs<T>` | ❌ | Fires after row is dropped |

## Selection Events

| Event | Args | Cancelable | Description |
|---|---|---|---|
| `RowSelecting` | `RowSelectingEventArgs<T>` | ✅ | Before row selected |
| `RowSelected` | `RowSelectEventArgs<T>` | ❌ | After row selected |
| `RowDeselecting` | `RowDeselectEventArgs<T>` | ✅ | Before row deselected |
| `RowDeselected` | `RowDeselectEventArgs<T>` | ❌ | After row deselected |
| `CellSelecting` | `CellSelectingEventArgs<T>` | ✅ | Before cell selected |
| `CellSelected` | `CellSelectEventArgs<T>` | ❌ | After cell selected |
| `CellDeselecting` | `CellDeselectEventArgs<T>` | ✅ | Before cell deselected |
| `CellDeselected` | `CellDeselectEventArgs<T>` | ❌ | After cell deselected |

## Cell Events

| Event | Args | Description |
|---|---|---|
| `QueryCellInfo` | `QueryCellInfoEventArgs<T>` | Fires per cell when bound; used for cell styling |

## Editing Events

| Event | Args | Cancelable | Description |
|---|---|---|---|
| `OnBeginEdit` | `BeginEditArgs<T>` | ✅ | Before editing starts |
| `EditCanceling` | `EditCancelingEventArgs<T>` | ✅ | Before edit is canceled |
| `EditCanceled` | `EditCanceledEventArgs<T>` | ❌ | After edit is canceled |
| `RowCreating` | `RowCreatingEventArgs<T>` | ✅ | Before new row is saved |
| `RowCreated` | `RowCreatedEventArgs<T>` | ❌ | After new row is saved |
| `RowUpdating` | `RowUpdatingEventArgs<T>` | ✅ | Before row update is saved |
| `RowUpdated` | `RowUpdatedEventArgs<T>` | ❌ | After row update is saved |
| `RowDeleting` | `RowDeletingEventArgs<T>` | ✅ | Before row is deleted |
| `RowDeleted` | `RowDeletedEventArgs<T>` | ❌ | After row is deleted |
| `OnCellEdit` | `CellEditArgs<T>` | ✅ | Batch mode: before cell enters edit |
| `OnCellSave` | `CellSaveArgs<T>` | ✅ | Batch mode: before cell save |
| `CellSaved` | `CellSavedArgs<T>` | ❌ | Batch mode: after cell saved |
| `OnBatchAdd` | `BeforeBatchAddArgs<T>` | ✅ | Batch mode: before add row |
| `OnBatchSave` | `BeforeBatchSaveArgs<T>` | ✅ | Batch mode: before save all |
| `OnBatchDelete` | `BeforeBatchDeleteArgs<T>` | ✅ | Batch mode: before delete row |
| `OnBatchCancel` | `BeforeBatchCancelArgs<T>` | ✅ | Batch mode: before cancel |

## Sorting Events

| Event | Cancelable | Description |
|---|---|---|
| `Sorting` | ✅ | Before sort applied |
| `Sorted` | ❌ | After sort applied |

## Filtering Events

| Event | Cancelable | Description |
|---|---|---|
| `Filtering` | ✅ | Before filter applied |
| `Filtered` | ❌ | After filter applied |
| `FilterDialogOpening` | ✅ | Before filter dialog opens |
| `FilterDialogOpened` | ❌ | After filter dialog opens |

## Grouping Events

| Event | Cancelable | Description |
|---|---|---|
| `Grouping` | ✅ | Before grouping applied |
| `Grouped` | ❌ | After grouping applied |

## Paging Events

| Event | Cancelable | Description |
|---|---|---|
| `PageChanging` | ✅ | Before page change |
| `PageChanged` | ❌ | After page change |

## Search Events

| Event | Cancelable | Description |
|---|---|---|
| `Searching` | ✅ | Before search applied |
| `Searched` | ❌ | After search applied |

## Toolbar Event

```razor
<GridEvents TValue="Order" OnToolbarClick="OnToolbarClick"></GridEvents>

@code {
    async Task OnToolbarClick(Syncfusion.Blazor.Navigations.ClickEventArgs args)
    {
        // args.Item.Id, args.Item.Text
    }
}
```

## Export Events

| Event | Description |
|---|---|
| `OnPdfExport` / `OnExcelExport` | Fires before export begins |
| `PdfQueryCellInfoEvent` | Per cell during PDF export |
| `PdfHeaderQueryCellInfoEvent` | Per header cell during PDF export |
| `PdfAggregateTemplateInfo` | Per aggregate cell during PDF export |
| `PdfGroupCaptionTemplateInfo` | Fires when exporting grouped data to PDF; use to customize group caption cell content/value |
| `ExcelQueryCellInfoEvent` | Per cell during Excel export |
| `ExcelHeaderQueryCellInfoEvent` | Per header cell during Excel export |
| `ExcelAggregateTemplateInfo` | Per aggregate cell during Excel export |
| `ExportComplete` | After export finishes |

## Column Menu / Context Menu Events

| Event | Description |
|---|---|
| `ColumnMenuItemClicked` | When a column menu item is clicked |
| `OnColumnMenuOpen` | Before column menu opens |
| `ContextMenuItemClicked` | When a context menu item is clicked |
| `ContextMenuOpen` | Before context menu opens |

## Resize Events

| Event | Description |
|---|---|
| `OnResizeStart` | Before column resize starts |
| `ResizeStopped` | After column resize ends |

## Column Chooser Event

| Event | Description |
|---|---|
| `BeforeOpenColumnChooser` | Before column chooser dialog opens |

## Operation-Specific Event Reference

**Use these specific events instead of OnActionBegin/OnActionComplete:**

| Operation | Before Event | After Event | Args Type | Use Case |
|---|---|---|---|---|
| **Sorting** | `Sorting` | `Sorted` | `SortingEventArgs` | Validate, intercept, or log sort |
| **Filtering** | `Filtering` | `Filtered` | `FilteringEventArgs`, `FilteredEventArgs` | Validate filter criteria |
| **Paging** | `PageChanging` | `PageChanged` | `PageChangingEventArgs`, `PageChangeEventArgs` | Update UI on page change |
| **Grouping** | `Grouping` | `Grouped` | `GroupingEventArgs`, `GroupedEventArgs` | Intercept grouping |
| **Searching** | `Searching` | `Searched` | `SearchingEventArgs`, `SearchedEventArgs` | Track search input |
| **Row Selection** | `RowSelecting` | `RowSelected` | `RowSelectingEventArgs<T>`, `RowSelectEventArgs<T>` | Track row selection |
| **Cell Selection** | `CellSelecting` | `CellSelected` | `CellSelectingEventArgs<T>`, `CellSelectEventArgs<T>` | Track cell selection |
| **Row Edit** | `OnBeginEdit` | `RowUpdating`/`RowUpdated` | `BeginEditArgs<T>`, `RowUpdatingEventArgs<T>` | Validate/intercept edits |
| **Row Add** | `RowCreating` | `RowCreated` | `RowCreatingEventArgs<T>`, `RowCreatedEventArgs<T>` | Validate new rows |
| **Row Delete** | `RowDeleting` | `RowDeleted` | `RowDeletingEventArgs<T>`, `RowDeletedEventArgs<T>` | Confirm before delete |
| **Batch Edit** | `OnCellEdit` | `OnCellSave` | `CellEditArgs<T>`, `CellSaveArgs<T>` | Batch cell editing |
| **Row Drag** | `RowDragStarting` | `RowDropped` | `RowDragEventArgs<T>`, `RowDroppedEventArgs<T>` | Validate drag-drop |
| **Filter Dialog** | `FilterDialogOpening` | `FilterDialogOpened` | `FilterDialogOpeningEventArgs` | Customize filter dialog |
| **Command Click** | — | `CommandClicked` | `CommandClickEventArgs<T>` | Handle command column button clicks per row |

---

## Complete GridEvents Example (RECOMMENDED)

```razor
<GridEvents TValue="Order"
            Sorting="OnSorting"
            Sorted="OnSorted"
            Filtering="OnFiltering"
            Filtered="OnFiltered"
            PageChanging="OnPageChanging"
            PageChanged="OnPageChanged"
            Grouping="OnGrouping"
            Grouped="OnGrouped"
            RowSelecting="OnRowSelecting"
            RowSelected="OnRowSelected"
            CellSelected="OnCellSelected"
            OnBeginEdit="OnBeginEdit"
            RowUpdating="OnRowUpdating"
            RowCreating="OnRowCreating"
            RowDeleting="OnRowDeleting"
            OnToolbarClick="OnToolbarClick"
            ExportComplete="OnExportComplete"
            OnActionFailure="OnActionFailure">
</GridEvents>

@code {
    // Sorting
    void OnSorting(SortingEventArgs args) { }
    void OnSorted(SortedEventArgs args) { }

    // Filtering
    void OnFiltering(FilteringEventArgs args) { }
    void OnFiltered(FilteredEventArgs args) { }

    // Paging
    void OnPageChanging(PageChangingEventArgs args) { }
    void OnPageChanged(PageChangeEventArgs args) { }

    // Grouping
    void OnGrouping(GroupingEventArgs args) { }
    void OnGrouped(GroupedEventArgs args) { }

    // Selection
    void OnRowSelecting(RowSelectingEventArgs<Order> args) { }
    void OnRowSelected(RowSelectEventArgs<Order> args) { }
    void OnCellSelected(CellSelectEventArgs<Order> args) { }

    // Editing
    void OnBeginEdit(BeginEditArgs<Order> args) { }
    void OnRowUpdating(RowUpdatingEventArgs<Order> args) { }
    void OnRowCreating(RowCreatingEventArgs<Order> args) { }
    void OnRowDeleting(RowDeletingEventArgs<Order> args) { }

    // Other
    void OnToolbarClick(Syncfusion.Blazor.Navigations.ClickEventArgs args) { }
    void OnExportComplete(ExportCompleteArgs args) { }
    void OnActionFailure(FailureEventArgs args) { }
}
```