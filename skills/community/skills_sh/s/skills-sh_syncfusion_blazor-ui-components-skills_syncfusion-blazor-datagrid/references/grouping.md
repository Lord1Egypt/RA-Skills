# Grouping — Syncfusion Blazor DataGrid

## Table of Contents

1. [Enable Grouping](#enable-grouping)
2. [Initial Group State](#initial-group-state)
3. [GridGroupSettings Options](#gridgroupsettings-options)
4. [Toggle Button in Column Headers](#toggle-button-in-column-headers)
5. [Reorder Grouped Elements](#reorder-grouped-elements)
6. [Expand All Groups Initially](#expand-all-groups-initially)
7. [Calculate Aggregates from Whole Data](#calculate-aggregates-from-whole-data)
8. [Sort Direction for Grouped Column](#sort-direction-for-grouped-column)
9. [Group by Formatted Value](#group-by-formatted-value)
10. [Caption Template](#caption-template)
    - [Custom Text in Caption](#custom-text-in-caption)
    - [Custom Component in Caption](#custom-component-in-caption)
11. [Prevent Grouping for Particular Column](#prevent-grouping-for-particular-column)
12. [Hide Drop Area](#hide-drop-area)
13. [Show Grouped Column](#show-grouped-column)
14. [Collapse All Groups on Initial Load](#collapse-all-groups-on-initial-load)
15. [Programmatic Group Operations](#programmatic-group-operations)
16. [Customize Group Caption with Locale](#customize-group-caption-with-locale)
17. [Lazy Load Grouping](#lazy-load-grouping)
    - [Lazy Load + Infinite Scrolling](#lazy-load--infinite-scrolling)
    - [Lazy Load + Virtual Scrolling](#lazy-load--virtual-scrolling)
    - [Lazy Load Limitations](#lazy-load-limitations)
18. [Grouping Events](#grouping-events)
    - [Before Grouping (Prevent/Allow)](#before-grouping-preventallow)
    - [After Grouping (Track Action)](#after-grouping-track-action)
19. [Key Rules](#key-rules)

---

## Enable Grouping

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridColumns>
        <GridColumn Field="OrderID"    Width="120"></GridColumn>
        <GridColumn Field="CustomerID" Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" AllowGrouping="false" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

Drag column headers to the "Drag a column header here to group" drop area.

## Initial Group State

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings Columns="@(new string[]{ \"CustomerID\", \"ShipCity\" })">
    </GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## GridGroupSettings Options

```razor
<GridGroupSettings
    AllowReordering="false"
    ShowDropArea="true"
    ShowGroupedColumn="false"
    ShowToggleButton="false"
    ShowUngroupButton="true"
    PersistGroupState="false"
    EnableLazyLoading="false"
    ExpandAllGroups="false"
    DisablePageWiseAggregates="false">
</GridGroupSettings>
```

| Property | Default | Description |
|---|---|---|
| `AllowReordering` | `false` | Allow grouped elements to be reordered |
| `ShowDropArea` | `true` | Show/hide the group drop area |
| `ShowGroupedColumn` | `false` | Keep grouped column visible in grid after grouping |
| `ShowToggleButton` | `false` | Show toggle button in column headers to group/ungroup |
| `ShowUngroupButton` | `true` | Show/hide ungroup button in group caption row |
| `PersistGroupState` | `false` | Persist expand/collapse state across paging/sorting/filtering |
| `EnableLazyLoading` | `false` | Load child rows on demand (renders only captions initially) |
| `ExpandAllGroups` | `false` | Expand all groups by default during initial render (requires virtualization) |
| `DisablePageWiseAggregates` | `false` | Calculate group aggregates from whole data instead of paged data |

## Toggle Button in Column Headers

Enable toggle buttons in column headers to group/ungroup columns with a single click:

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings ShowToggleButton="true"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## Reorder Grouped Elements

Allow grouped elements to be reordered by dragging:

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings AllowReordering="true" Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## Expand All Groups Initially

Expand all groups by default when the Grid initially renders (works with virtualization):

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true" EnableVirtualization="true">
    <GridGroupSettings ExpandAllGroups="true" Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

> **Note**: `ExpandAllGroups` is ignored if `EnableLazyLoading` is `true`.

## Calculate Aggregates from Whole Data

By default, group aggregates are calculated from paged data. To calculate from entire dataset:

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true" AllowPaging="true">
    <GridGroupSettings DisablePageWiseAggregates="true" Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridPageSettings PageSize="10"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## Sort Direction for Grouped Column

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true" AllowSorting="true">
    <GridGroupSettings Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridSortSettings>
        <GridSortColumns>
            <GridSortColumn Field="CustomerID" Direction="SortDirection.Descending"></GridSortColumn>
        </GridSortColumns>
    </GridSortSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## Group by Formatted Value

Group numeric/date columns by their display format:

```razor
<GridColumn Field="OrderDate" Format="yyyy/MMM" EnableGroupByFormat="true" Type="ColumnType.Date"></GridColumn>
<GridColumn Field="Freight"   Format="C2"        EnableGroupByFormat="true"></GridColumn>
```

## Caption Template

Customize group caption rows with `CaptionTemplate`:

```razor
<GridGroupSettings ShowDropArea="false" Columns="@(new string[]{ \"CustomerID\" })">
    <CaptionTemplate>
        @{
            var data = context as CaptionTemplateContext;
            <span>@data.HeaderText - @data.Key : @data.Count Items</span>
        }
    </CaptionTemplate>
</GridGroupSettings>
```

`CaptionTemplateContext` properties:
- `Field` - Column field name
- `HeaderText` - Column header text
- `Key` - Grouped value
- `Count` - Number of grouped records

### Custom Text in Caption

```razor
<CaptionTemplate>
    @{
        var data = context as CaptionTemplateContext;
        <span>@data.Key - @data.Count Records (@data.HeaderText)</span>
    }
</CaptionTemplate>
```

### Custom Component in Caption

```razor
@using Syncfusion.Blazor.Buttons

<CaptionTemplate>
    @{
        var data = context as CaptionTemplateContext;
        <SfChip Text="@data.Key" CssClass="e-outline"></SfChip>
        <span>@data.Count Items</span>
    }
</CaptionTemplate>
```

## Prevent Grouping for Particular Column

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridColumns>
        <GridColumn Field="OrderID" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" AllowGrouping="false" Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

Set `AllowGrouping="false"` in the `GridColumn` to prevent grouping for that column.

## Hide Drop Area

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings ShowDropArea="false" Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## Show Grouped Column

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings ShowGroupedColumn="true" Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

By default, grouped columns are hidden. Set `ShowGroupedColumn="true"` to keep them visible.

## Collapse All Groups on Initial Load

```razor
<SfGrid @ref="Grid" DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridEvents TValue="Order" DataBound="DataBoundHandler"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;
    bool IsFirstLoad = true;
    async Task DataBoundHandler()
    {
        if (IsFirstLoad) {
            IsFirstLoad = false;
            await Grid.CollapseAllGroupAsync();
        }
    }
}
```

## Programmatic Group Operations

### API Methods Reference

| Method | Return Type | Parameters | Description |
|--------|-------------|-----------|-------------|
| `GroupColumnAsync()` | `Task` | `string fieldName` | Group by a specific column field name |
| `UngroupColumnAsync()` | `Task` | `string fieldName` | Remove grouping from a column |
| `ExpandAllGroupAsync()` | `Task` | None | Expand all collapsed group rows |
| `CollapseAllGroupAsync()` | `Task` | None | Collapse all expanded group rows |
| `ClearGroupingAsync()` | `Task` | None | Remove all grouping from the grid |
| `ExpandGroupAsync()` | `Task` | `object[] keyValues` | Expand a specific group by key value |
| `CollapseGroupAsync()` | `Task` | `object[] keyValues` | Collapse a specific group by key value |

### Basic Group Operations

```razor
<SfGrid @ref="Grid" DataSource="@Orders" AllowGrouping="true">
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;
    
    // Group a column
    await Grid.GroupColumnAsync("CustomerID");
    
    // Ungroup a column
    await Grid.UngroupColumnAsync("CustomerID");
    
    // Expand all groups
    await Grid.ExpandAllGroupAsync();
    
    // Collapse all groups
    await Grid.CollapseAllGroupAsync();
    
    // Clear all grouping
    await Grid.ClearGroupingAsync();
}
```

### Expand/Collapse Specific Group

```razor
@code {
    // Expand a specific group by key value
    await Grid.ExpandGroupAsync(new object[] { "VINET" });
    
    // Collapse a specific group by key value
    await Grid.CollapseGroupAsync(new object[] { "VINET" });
    
    // For multiple grouping levels, pass array of all key values
    await Grid.ExpandGroupAsync(new object[] { "VINET", "Reims" });
}
```

### Practical Example - Trigger from Button Click

```razor
<button @onclick="OnGroupByCustomer">Group by Customer</button>
<button @onclick="OnUngroupAll">Clear All Grouping</button>

<SfGrid @ref="Grid" DataSource="@Orders" AllowGrouping="true">
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;
    
    async Task OnGroupByCustomer()
    {
        await Grid.GroupColumnAsync("CustomerID");
    }
    
    async Task OnUngroupAll()
    {
        await Grid.ClearGroupingAsync();
    }
}
```

### Important Notes

- ⚠️ **Do NOT call these methods in lifecycle events** (`OnInitialized`, `OnAfterRenderAsync`)
- ✅ **Call only in response to user interactions** (button clicks, dropdown changes, etc.)
- 🔄 These methods are **async** - always use `await`
- 📍 For `ExpandGroupAsync()` and `CollapseGroupAsync()`, pass the exact key values of the group
- 🔗 Use `@ref="Grid"` to get a reference to the Grid instance

## Customize Group Caption with Locale

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings Columns="@(new string[]{ \"Country\" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>

<!-- App.razor -->
<script>
    Blazor.start({
        webAssembly: {
            applicationCulture: 'ar' // or other locale codes
        }
    });
</script>
```

Configure localized strings via `ISyncfusionStringLocalizer` interface for custom group captions.

## Lazy Load Grouping

Load child rows on demand when a group is expanded (improves performance for large datasets):

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true">
    <GridGroupSettings EnableLazyLoading="true"
                       Columns="@(new string[]{ \"CustomerID\" })">
    </GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Lazy Load + Infinite Scrolling

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true"
        EnableInfiniteScrolling="true" Height="400px" RowHeight="36">
    <GridGroupSettings EnableLazyLoading="true" Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Lazy Load + Virtual Scrolling

```razor
<SfGrid DataSource="@Orders" AllowGrouping="true"
        EnableVirtualization="true" Height="400px" RowHeight="36">
    <GridGroupSettings EnableLazyLoading="true" Columns="@(new string[]{ \"CustomerID\" })"></GridGroupSettings>
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

### Lazy Load Limitations

**Not compatible with:**
- Batch editing
- Row template
- Row drag-drop
- Hierarchy
- Detail template

**Restrictions:**
- Programmatic selection not supported when groups are collapsed
- Drag selection and clipboard operations not supported in collapsed state

**Browser Limitation:**
- Maximum records limited by browser's DOM element capacity

## Grouping Events

### Before Grouping (Prevent/Allow)

```razor
<SfGrid @ref="Grid" DataSource="@Orders" AllowGrouping="true">
    <GridEvents TValue="Order" Grouping="OnGrouping"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    void OnGrouping(GroupingEventArgs args)
    {
        // args.ColumnName - Column being grouped
        // args.Cancel - Set to true to prevent grouping
        if (args.ColumnName == "Freight") 
        {
            args.Cancel = true; // Prevent grouping for Freight column
        }
    }
}
```

### After Grouping (Track Action)

```razor
<GridEvents TValue="Order" Grouped="OnGrouped"></GridEvents>

@code {
    void OnGrouped(GroupedEventArgs args)
    {
        // args.ColumnName - Column that was grouped
        // args.Action - "grouping" or "ungrouping"
        Console.WriteLine($"Column {args.ColumnName} was {args.Action}ed");
    }
}
```
## Key Rules

- **Do not call grouping or ungrouping APIs in lifecycle events** (such as `OnInitialized` or `OnAfterRenderAsync`).  
- Always trigger grouping/ungrouping actions in response to user interactions (e.g., button clicks).