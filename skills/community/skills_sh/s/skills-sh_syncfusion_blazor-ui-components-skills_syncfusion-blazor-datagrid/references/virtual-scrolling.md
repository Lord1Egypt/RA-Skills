# Virtual Scrolling — Syncfusion Blazor DataGrid

## Table of Contents
- [Row Virtualization](#row-virtualization)
  - [OverscanCount](#overscancount)
  - [Row Virtualization Limitations](#row-virtualization-limitations)
- [Column Virtualization](#column-virtualization)
  - [Column Virtualization Limitations](#column-virtualization-limitations)
  - [Column Virtualization with Paging](#column-virtualization-with-paging)
- [Row + Column Virtualization Combined](#row--column-virtualization-combined)
- [Virtual Mask Row (Loading Placeholder)](#virtual-mask-row-loading-placeholder)
- [Frozen Columns + Virtualization](#frozen-columns--virtualization)
- [Programmatic Scroll (Virtualized Grid)](#programmatic-scroll-virtualized-grid)
- [Update Page Size for Virtualized Grid](#update-page-size-for-virtualized-grid)

## Row Virtualization

Renders only visible rows as you scroll — ideal for 10,000+ rows:

```razor
<SfGrid DataSource="@LargeDataset" Height="400" EnableVirtualization="true">
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

- `Height` is **required** for row virtualization
- `PageSize` controls the buffer (default auto-calculated based on viewport)
- Data is cached during scrolling — no re-fetch unless data changes

### OverscanCount

Pre-render extra rows before/after visible area (reduces blank rows during fast scroll):

```razor
<SfGrid DataSource="@LargeDataset" Height="400" EnableVirtualization="true" OverscanCount="5">
    <GridColumns>...</GridColumns>
</SfGrid>
```

> `OverscanCount` supports both local and remote data.

### Row Virtualization Limitations

- **Not compatible with:** batch editing, detail template, row template, autofill
- Copy-paste and drag-and-drop apply only to items within the current viewport
- Cell-based selection not supported
- Variable row heights in template columns (where each row has a different height) are not supported
- Aggregates and group totals reflect the **current view** only (not all data)
- Group expand/collapse state is not persisted by default — set `GridGroupSettings.PersistGroupState="true"` to persist it
- Browser element height limits the maximum number of records
- Grid content height is calculated from row height and total record count — features that change row height (such as text wrapping) are not supported
- Page size should be at least **2×** the number of visible rows; otherwise, the Grid determines an appropriate size
- `Height` must be set as a static pixel value — using `100%` requires both the component and its parent container to have defined heights

---

## Column Virtualization

Renders only visible columns — ideal for 50+ columns:

```razor
<SfGrid DataSource="@Orders" EnableColumnVirtualization="true">
    <GridColumns>
        <!-- All column widths must be in px (not %) -->
        <GridColumn Field="OrderID"    Width="120"></GridColumn>
        <GridColumn Field="CustomerID" Width="150"></GridColumn>
        <!-- ... more columns ... -->
    </GridColumns>
</SfGrid>
```

- Column `Width` must be specified in pixels
- Compatible with `AllowPaging` (see [Column Virtualization with Paging](#column-virtualization-with-paging))

### Column Virtualization Limitations

- Column width must be in pixels — percentage values are not supported
- Cell selection not supported
- `Ctrl + Home` and `Ctrl + End` keyboard shortcuts are not supported
- The following features work only **within the viewport**: column resizing, column chooser, auto-fit, clipboard, column menu (chooser/AutofitAll)
- **Not compatible with:** grouping, batch editing, infinite scrolling, stacked header, row template, detail template, hierarchy grid, autofill

---

### Column Virtualization with Paging

Combine column virtualization with paging to reduce memory usage and improve initial render time for large grids with many columns and rows:

```razor
<SfGrid DataSource="@Orders" Height="400"
        AllowPaging="true"
        EnableColumnVirtualization="true">
    <GridColumns>
        <GridColumn Field="OrderID"    Width="150"></GridColumn>
        <GridColumn Field="CustomerID" Width="150"></GridColumn>
        <!-- more columns with px widths -->
    </GridColumns>
</SfGrid>
```

- `EnableColumnVirtualization` — renders only visible columns
- `AllowPaging` — limits rows displayed per page

> If a column's width is not defined, the Grid treats it as `200px`.

---

## Row + Column Virtualization Combined

```razor
<SfGrid DataSource="@LargeDataset" Height="400"
        EnableVirtualization="true"
        EnableColumnVirtualization="true">
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>
        <GridColumn Field="OrderID"    Width="120"></GridColumn>
        <!-- many columns with px widths -->
    </GridColumns>
</SfGrid>
```

---

## Virtual Mask Row (Loading Placeholder)

Shows skeleton placeholder rows while fetching data:

```razor
<SfGrid DataSource="@Orders" Height="400"
        EnableVirtualization="true"
        EnableVirtualMaskRow="true">
    <GridColumns>...</GridColumns>
</SfGrid>
```

> `EnableVirtualMaskRow` requires either row virtualization (`EnableVirtualization`) or column virtualization (`EnableColumnVirtualization`) to be enabled. For best results, also define `PageSize` and `RowHeight`.

---

## Frozen Columns + Virtualization

```razor
<SfGrid DataSource="@LargeDataset" Height="400"
        EnableVirtualization="true"
        EnableColumnVirtualization="true">
    <GridColumns>
        <GridColumn Field="OrderID"    IsFrozen="true" Freeze="FreezeDirection.Left"  Width="120"></GridColumn>
        <GridColumn Field="CustomerID" IsFrozen="true" Freeze="FreezeDirection.Left"  Width="150"></GridColumn>
        <GridColumn Field="Freight"    Width="120"></GridColumn>
        <!-- more columns -->
    </GridColumns>
</SfGrid>
```

---

## Programmatic Scroll (Virtualized Grid)

```razor
<SfGrid @ref="Grid" DataSource="@LargeDataset" Height="400" EnableVirtualization="true">...</SfGrid>
@code {
    SfGrid<Order> Grid;
    // ScrollIntoViewAsync(columnIndex, rowIndex, rowPageIndex)
    // rowPageIndex is optional
    // Scroll to column index 5, row index 100
    await Grid.ScrollIntoViewAsync(5, 100);
}
```

- Enable `EnableVirtualization` for vertical scrolling
- Enable both `EnableVirtualization` and `EnableColumnVirtualization` for horizontal scrolling

## Update Page Size for Virtualized Grid

Recalculate `PageSize` based on container height and row height:

```razor
@code {
    await Grid.UpdatePageSizeAsync(400, 36); // containerHeight, rowHeight
}
```

> If `RowHeight` is specified on the Grid, the page size is calculated using that value; otherwise it is determined from the Grid row's actual offset height.
