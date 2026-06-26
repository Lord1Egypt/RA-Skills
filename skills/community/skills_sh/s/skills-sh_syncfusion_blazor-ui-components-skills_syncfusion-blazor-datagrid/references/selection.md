# Selection — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable Selection](#enable-selection)
- [GridSelectionSettings Properties](#gridSelectionsettings-properties)
- [Selection Mode](#selection-mode)
- [Selection Type](#selection-type)
- [Initial Row Selection](#initial-row-selection)
- [Toggle Selection](#toggle-selection)
- [Drag Selection](#drag-selection)
- [Persist Selection](#persist-selection)
- [Checkbox Selection](#checkbox-selection)
- [Cell Selection](#cell-selection)
- [Programmatic Selection](#programmatic-selection)
- [Selection Events](#selection-events)

## Enable Selection

```razor
<SfGrid DataSource="@Orders" AllowSelection="true">
    <GridSelectionSettings Mode="SelectionMode.Row"
                           Type="SelectionType.Multiple">
    </GridSelectionSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

Set `AllowSelection="false"` to disable selection entirely.

## GridSelectionSettings Properties

| Property | Default | Description |
|---|---|---|
| `Mode` | `Row` | `Row`, `Cell`, or `Both` |
| `Type` | `Single` | `Single` or `Multiple` |
| `EnableToggle` | `false` | Click selected item to deselect |
| `AllowDragSelection` | `false` | Drag to select range |
| `PersistSelection` | `false` | Retain selection across data operations |
| `CheckboxOnly` | `false` | Allow selection via checkbox clicks only |
| `CheckboxMode` | `Default` | `Default` or `ResetOnRowClick` — controls checkbox selection behavior |
| `CellSelectionMode` | `Flow` | `Flow` or `Box` (for cell selection) |

## Selection Mode

```razor
<GridSelectionSettings Mode="SelectionMode.Row"></GridSelectionSettings>   <!-- rows only (default) -->
<GridSelectionSettings Mode="SelectionMode.Cell"></GridSelectionSettings>  <!-- cells only -->
<GridSelectionSettings Mode="SelectionMode.Both"></GridSelectionSettings>  <!-- rows and cells -->
```

## Selection Type

```razor
<!-- Single selection (default) -->
<GridSelectionSettings Type="SelectionType.Single"></GridSelectionSettings>

<!-- Multiple selection: hold Ctrl to pick rows, Shift for range -->
<GridSelectionSettings Type="SelectionType.Multiple"></GridSelectionSettings>
```

## Initial Row Selection


```razor
<SfGrid DataSource="@Orders" SelectedRowIndex="2">
    <GridSelectionSettings Mode="SelectionMode.Row"></GridSelectionSettings>
</SfGrid>
```

## Toggle Selection

```razor
<GridSelectionSettings EnableToggle="true" Type="SelectionType.Multiple">
</GridSelectionSettings>
```

Click a selected row/cell to deselect it.

## Drag Selection

```razor
<GridSelectionSettings AllowDragSelection="true" Type="SelectionType.Multiple"
                       Mode="SelectionMode.Row">
</GridSelectionSettings>
```

> Not compatible with AutoFill.

## Persist Selection

```razor
<GridSelectionSettings PersistSelection="true" Type="SelectionType.Multiple">
</GridSelectionSettings>
```

> Requires `IsPrimaryKey="true"` on at least one column. Not supported for cell selection. Only applicable when `Type` is set to `Multiple`.

## Checkbox Selection

Add a checkbox column for multi-row selection:

```razor
<SfGrid DataSource="@Orders" AllowSelection="true">
    <GridSelectionSettings Type="SelectionType.Multiple" CheckboxOnly="true"
                           PersistSelection="true">
    </GridSelectionSettings>
    <GridColumns>
        <!-- Checkbox column -->
        <GridColumn Type="ColumnType.CheckBox" Width="50"></GridColumn>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

**Hide SelectAll checkbox in header:**

```razor
<GridColumn Type="ColumnType.CheckBox" Width="50">
    <HeaderTemplate></HeaderTemplate>
</GridColumn>
```

**Checkbox selection mode:**

```razor
<GridSelectionSettings CheckboxMode="CheckboxSelectionType.Default"></GridSelectionSettings>
<!-- CheckboxSelectionType.ResetOnRowClick — clicking row clears previous selection -->
```

## Cell Selection

```razor
<SfGrid DataSource="@Orders">
    <GridSelectionSettings Mode="SelectionMode.Cell" Type="SelectionType.Multiple"
                           CellSelectionMode="CellSelectionMode.Box">
    </GridSelectionSettings>
</SfGrid>
```

Get selected cells:

```razor
var cells = await Grid.GetSelectedRowCellIndexesAsync();
```

## Programmatic Selection

```razor
@code {
    SfGrid<Order> Grid;

    // Select single row by index
    await Grid.SelectRowAsync(2);

    // Toggle select — second arg (isToggle): if true, deselects an already-selected row
    await Grid.SelectRowAsync(2, true);

    // Select multiple rows by index
    await Grid.SelectRowsAsync(new int[] { 0, 2, 4 });

    // Get selected records
    var selected = await Grid.GetSelectedRecordsAsync();

    // Clear all selection
    await Grid.ClearSelectionAsync();

    // Clear only row selection
    await Grid.ClearRowSelectionAsync();

    // Clear only cell selection
    await Grid.ClearCellSelectionAsync();

    // Note: In Both mode, call ClearCellSelectionAsync first to clear cells,
    // then ClearRowSelectionAsync to clear rows. Order of calls determines
    // which selection type is cleared first.
}
```

**Conditional row selection on DataBound:**

```razor
<GridEvents TValue="Order" DataBound="OnDataBound"></GridEvents>

@code {
    async Task OnDataBound(object args)
    {
        var indexes = Orders
            .Select((o, i) => new { o, i })
            .Where(x => x.o.Freight > 100)
            .Select(x => x.i)
            .ToArray();
        await Grid.SelectRowsAsync(indexes);
    }
}
```

## Selection Events

```razor
<GridEvents TValue="Order"
            RowSelecting="OnRowSelecting"
            RowSelected="OnRowSelected"
            RowDeselecting="OnRowDeselecting"
            RowDeselected="OnRowDeselected">
</GridEvents>

@code {
    void OnRowSelecting(RowSelectingEventArgs<Order> args)
    {
        // args.Cancel = true; to cancel
    }

    void OnRowSelected(RowSelectEventArgs<Order> args)
    {
        var selectedRow = args.Data;
    }

    void OnRowDeselecting(RowDeselectEventArgs<Order> args)
    {
        // args.Cancel = true; to cancel
    }

    void OnRowDeselected(RowDeselectEventArgs<Order> args)
    {
        var deselectedRow = args.Data;
    }
}
```

| Event | Cancelable | Description |
|---|---|---|
| `RowSelecting` | ✅ | Before row selected |
| `RowSelected` | ❌ | After row selected |
| `RowDeselecting` | ✅ | Before row deselected |
| `RowDeselected` | ❌ | After row deselected |
| `CellSelecting` | ✅ | Before cell selected |
| `CellSelected` | ❌ | After cell selected |
| `CellDeselecting` | ✅ | Before cell deselected |
| `CellDeselected` | ❌ | After cell deselected |
