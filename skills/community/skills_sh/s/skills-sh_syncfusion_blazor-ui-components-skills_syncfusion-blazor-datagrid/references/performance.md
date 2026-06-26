# Performance Optimization — Syncfusion Blazor DataGrid

## Table of Contents
- [Overview](#overview)
- [Strategy 1: Paging](#strategy-1-paging)
- [Strategy 2: Row Virtualization](#strategy-2-row-virtualization)
- [Strategy 3: Infinite Scrolling](#strategy-3-infinite-scrolling)
- [Strategy 4: Column Virtualization](#strategy-4-column-virtualization)
- [Strategy 5: Reduce Row Height](#strategy-5-reduce-row-height)
- [Browser Height Limitation with Virtual Scrolling](#browser-height-limitation-with-virtual-scrolling)
- [SignalR Buffer for State Persistence](#signalr-buffer-for-state-persistence)
- [Strategy 6: Avoid Unnecessary Re-Renders](#strategy-6-avoid-unnecessary-re-renders)
  - [Grid-level: `PreventRender()`](#grid-level-preventrender)
  - [Event-level: `args.PreventRender`](#event-level-argspreventrender)
- [WASM Performance Best Practices](#wasm-performance-best-practices)
- [Binding Data from a Service](#binding-data-from-a-service)
  - [Assign DataSource in the `Created` Event](#assign-datasource-in-the-created-event)
  - [Use Custom Adaptor for Large Collections](#use-custom-adaptor-for-large-collections)
- [Use Individual NuGet Package and Scripts](#use-individual-nuget-package-and-scripts)
- [Update Cell Values Without Server Calls](#update-cell-values-without-server-calls)
- [Recommendation Summary](#recommendation-summary)

## Overview

Each grid cell is a Blazor component. For large datasets or many columns, apply these techniques to maintain responsiveness.

## Strategy 1: Paging

The simplest approach — render only one page of rows at a time:

```razor
<SfGrid DataSource="@Orders" AllowPaging="true">
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

- Compatible with grouping, sorting, filtering, editing
- Recommended default for most scenarios

## Strategy 2: Row Virtualization

Render only viewport-visible rows; rest are virtual:

```razor
<SfGrid DataSource="@Orders" EnableVirtualization="true" Height="400">
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

- `Height` is required
- `PageSize` acts as buffer
- See `virtual-scrolling.md` for full options

## Strategy 3: Infinite Scrolling

Load data blocks on demand as user scrolls:

```razor
<SfGrid DataSource="@Orders" EnableInfiniteScrolling="true" Height="400">
    <GridPageSettings PageSize="50"></GridPageSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

- No re-fetch when revisiting a block
- See `infinite-scrolling.md` for cache options

## Strategy 4: Column Virtualization

Render only visible columns (for wide grids with many columns):

```razor
<SfGrid DataSource="@Orders" EnableVirtualization="true"
        EnableColumnVirtualization="true" Height="400">
    <GridColumns>
        <!-- All columns must have px widths -->
        <GridColumn Field="OrderID" Width="120px"></GridColumn>
        ...
    </GridColumns>
</SfGrid>
```

- All column widths must be in pixels
- Works alongside row virtualization

## Strategy 5: Reduce Row Height

Lowering `RowHeight` reduces total scroll height and DOM cost:

```razor
<SfGrid DataSource="@Orders" RowHeight="30" EnableVirtualization="true" Height="400">
    ...
</SfGrid>
```

## Browser Height Limitation with Virtual Scrolling

**Formula:** Total height = Record count × RowHeight

At 30px × 1,000,000 rows = 30,000,000px — exceeds browser max (~22,369,600px).

**Solutions:**
1. Reduce `RowHeight`
2. Switch to paging instead of virtualization

## SignalR Buffer for State Persistence

When `EnablePersistence="true"` with many columns, increase SignalR buffer in `Program.cs`:

```csharp
builder.Services.AddSignalR(hubOptions =>
{
    hubOptions.MaximumReceiveMessageSize = 10 * 1024 * 1024; // 10MB
});
```

## Strategy 6: Avoid Unnecessary Re-Renders

### Grid-level: `PreventRender()`

Call `Grid.PreventRender()` inside event callbacks to stop the grid from participating in the next Blazor render cycle. Useful when unrelated parent state changes (e.g., a counter increment) would otherwise re-evaluate every grid cell:

```razor
@code {
    SfGrid<Order> Grid;

    void IncrementCount()
    {
        Grid.PreventRender(); // grid skips next render cycle
        currentCount++;
    }
}
```

- `PreventRender()` defaults to `true` (suppress render). Pass `false` to re-enable.
- Has no effect if called before the grid completes its initial render.

### Event-level: `args.PreventRender`

Some event args expose a `PreventRender` property. Setting it to `true` prevents the grid from re-rendering after that event callback completes — without suppressing the parent component:

```razor
<GridEvents TValue="Order" RowSelected="OnRowSelected"></GridEvents>

@code {
    void OnRowSelected(RowSelectEventArgs<Order> args)
    {
        args.PreventRender = true; // grid skips re-render; parent still updates
        SelectedOrder = args.Data;
    }
}
```

This is the preferred approach when you need the parent to update (e.g., display selected record) but do not need the grid itself to re-render.

| Technique | Scope | Use When |
|---|---|---|
| `Grid.PreventRender()` | Whole grid | Unrelated parent state change triggers render |
| `args.PreventRender = true` | Single event | Event callback updates parent but grid needn't re-render |

## WASM Performance Best Practices

In Blazor WebAssembly applications, apply these additional practices to prevent unnecessary rendering:

1. **Avoid unnecessary component renders** — Prevent redundant render cycles triggered by unrelated state changes.
2. **Avoid unnecessary renders after grid events** — Ensure grid event handlers do not trigger re-renders when no visual update is needed.

Use `Grid.PreventRender()` and `args.PreventRender = true` (covered in [Strategy 6](#strategy-6-avoid-unnecessary-re-renders)) as the primary tools for this.

> See also: [Blazor WebAssembly Performance (Microsoft Docs)](https://learn.microsoft.com/en-us/aspnet/core/blazor/performance/)

## Binding Data from a Service

### Assign DataSource in the `Created` Event

Set `DataSource` in the grid's `Created` event instead of `OnInitializedAsync` to ensure the grid is fully rendered before data is assigned, reducing startup delays:

```razor
<SfGrid @ref="Grid" TValue="Order">
    <GridEvents Created="OnCreated" TValue="Order"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    async Task OnCreated(object args)
    {
        Grid.DataSource = await MyService.GetOrdersAsync();
    }
}
```

### Use Custom Adaptor for Large Collections

For very large datasets, the `Created` event may fire before data retrieval completes. Use a custom adaptor with `ReadAsync` to fetch data on demand:

```razor
<SfGrid TValue="Order">
    <SfDataManager AdaptorInstance="@typeof(MyCustomAdaptor)" Adaptor="Adaptors.CustomAdaptor"></SfDataManager>
    <GridColumns>...</GridColumns>
</SfGrid>
```

> See `connecting-to-adaptors/custom-adaptor.md` for full implementation details.

## Use Individual NuGet Package and Scripts

Use the **individual** `Syncfusion.Blazor.Grid` NuGet package instead of the consolidated `Syncfusion.Blazor` package to reduce payload size and improve initial render speed.

| Package | Includes | Size Impact |
|---|---|---|
| `Syncfusion.Blazor` | All Syncfusion components | Large |
| `Syncfusion.Blazor.Grid` | Grid + dependencies only | Minimal |

Reference only the required script and CSS for the grid component in your `index.html` / `App.razor`.

> See `getting-started-with-web-app.md` for NuGet and resource setup steps.

## Update Cell Values Without Server Calls

Use `SetRowDataAsync()` to update the grid UI for live scenarios (e.g., real-time feeds) **without triggering a database update**. Pass `true` as the third argument (`preventDataUpdate`) to skip the underlying data source update.

Also cancel the built-in edit operation with `args.Cancel = true` to prevent the grid from issuing a save request:

```razor
<SfGrid @ref="Grid" DataSource="@Orders">
    <GridEvents OnBeginEdit="OnBeginEdit" TValue="Order"></GridEvents>
    <GridColumns>...</GridColumns>
</SfGrid>

@code {
    SfGrid<Order> Grid;

    void OnBeginEdit(BeginEditArgs<Order> args)
    {
        args.Cancel = true; // prevent built-in edit/save cycle
    }

    async Task UpdateRow()
    {
        await Grid.SetRowDataAsync(10001, new Order
        {
            OrderID   = 10001,
            CustomerID = "Updated",
            Freight    = 20,
            OrderDate  = DateTime.Now,
            ShipCity   = "New"
        }, true); // true = do NOT update underlying data source
    }
}
```

| Argument | Type | Description |
|---|---|---|
| `key` | `object` | Primary key value of the row to update |
| `data` | `TValue` | New record data to display |
| `preventDataUpdate` | `bool` | `true` = update UI only, skip data source |

## Recommendation Summary

| Scenario | Recommended Approach |
|---|---|
| Typical app (< 10,000 rows) | Paging |
| Large dataset, needs scroll feel | Row virtualization |
| Very large dataset, load on demand | Infinite scrolling |
| Many columns (50+) | Column virtualization |
| Mobile / small screen | Paging with small PageSize |
| Very large rows on virtual scroll | Reduce RowHeight |
| Frequent parent state changes | `Grid.PreventRender()` |
| High-frequency event callbacks | `args.PreventRender = true` |
| Blazor WASM app | Avoid unnecessary renders + use `PreventRender` |
| Data bound from a service | Assign `DataSource` in `Created` event |
| Very large service data | Custom adaptor with `ReadAsync` |
| Minimize initial load size | Use individual `Syncfusion.Blazor.Grid` NuGet |
| Live UI update, no DB write | `SetRowDataAsync(key, data, true)` |