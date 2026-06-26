# Sorting — Syncfusion Blazor DataGrid

## Table of Contents
- [Enable Sorting](#enable-sorting)
- [Multi-Column Sorting](#multi-column-sorting)
- [Initial Sort State](#initial-sort-state)
- [Programmatic Sorting](#programmatic-sorting)
- [Allow Unsort](#allow-unsort)
- [Custom Sort Comparer](#custom-sort-comparer)
- [Sort Foreign Key Column](#sort-foreign-key-column)
- [Touch Interaction](#touch-interaction)
- [Custom Sort Icon](#custom-sort-icon)
- [Sorting Events](#sorting-events)

## Enable Sorting

```razor
<SfGrid DataSource="@Orders" AllowSorting="true">
    <GridColumns>
        <GridColumn Field="OrderID"    AllowSorting="true"  Width="120"></GridColumn>
        <GridColumn Field="CustomerID" AllowSorting="false" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

## Multi-Column Sorting

Allow sorting by multiple columns simultaneously:

```razor
<SfGrid DataSource="@Orders" AllowSorting="true" AllowMultiSorting="true">
    ...
</SfGrid>
```

Hold **Ctrl** and click column headers to add/remove sort columns.

## Initial Sort State

```razor
<SfGrid DataSource="@Orders" AllowSorting="true">
    <GridSortSettings>
        <GridSortColumns>
            <GridSortColumn Field="CustomerID" Direction="SortDirection.Ascending"></GridSortColumn>
            <GridSortColumn Field="Freight"    Direction="SortDirection.Descending"></GridSortColumn>
        </GridSortColumns>
    </GridSortSettings>
    <GridColumns>...</GridColumns>
</SfGrid>
```

## Programmatic Sorting

```razor
<SfGrid @ref="Grid" DataSource="@Orders" AllowSorting="true">...</SfGrid>
@code {
    SfGrid<Order> Grid;

    // Sort single column
    await Grid.SortColumnAsync("CustomerID", SortDirection.Ascending, false);

    // Sort multiple columns (isMultiSort = true)
    await Grid.SortColumnAsync("Freight", SortDirection.Descending, true);

    // Sort multiple at once
    await Grid.SortColumnsAsync(new List<SortColumn>
    {
        new SortColumn { Field = "CustomerID", Direction = SortDirection.Ascending },
        new SortColumn { Field = "Freight",    Direction = SortDirection.Descending }
    });

    // Sort multiple at once and clear previous sort settings
    await Grid.SortColumnsAsync(new List<SortColumn>
    {
        new SortColumn { Field = "CustomerID", Direction = SortDirection.Ascending },
        new SortColumn { Field = "Freight",    Direction = SortDirection.Descending }
    }, clearPreviousSort: true);

    // Clear sorting for specific columns
    await Grid.ClearSortingAsync(new List<string> { "CustomerID", "Freight" });

    // Clear all sorting
    await Grid.ClearSortingAsync();
}
```

## Allow Unsort

By default, `AllowUnsort` is `true`, allowing columns to cycle through Ascending → Descending → None (unsorted). Set `AllowUnsort="false"` to prevent a sorted column from returning to an unsorted state — the column stays sorted and clicking it only toggles between Ascending and Descending:

```razor
<SfGrid DataSource="@Orders" AllowSorting="true">
    <GridSortSettings AllowUnsort="false"></GridSortSettings>
    ...
</SfGrid>
```

## Custom Sort Comparer

Apply custom comparison logic:

```razor
<SfGrid DataSource="@Orders" AllowSorting="true">
    <GridColumns>
        <GridColumn Field="ShipCountry" SortComparer="@SortComparer" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
@code {
    public class CustomComparer : IComparer<object>
    {
        public int Compare(object x, object y)
        {
            // Custom comparison logic
            return string.Compare(x?.ToString(), y?.ToString(), StringComparison.OrdinalIgnoreCase);
        }
    }
    public CustomComparer SortComparer = new CustomComparer();
}
```

## Sort Foreign Key Column

Sort foreign key columns based on their **display text** using `GridForeignColumn`. Configure `ForeignDataSource`, `ForeignKeyField`, and `ForeignKeyValue`:

```razor
<SfGrid DataSource="@Orders" AllowSorting="true">
    <GridColumns>
        <GridColumn Field="OrderID" Width="90"></GridColumn>
        <GridForeignColumn Field="CustomerID" HeaderText="Customer"
            ForeignKeyValue="ContactName"
            ForeignKeyField="CustomerID"
            ForeignDataSource="@CustomerData"
            Width="150">
        </GridForeignColumn>
    </GridColumns>
</SfGrid>
@code {
    // For local data → sorted by ForeignKeyValue (display text)
    // For remote data → sorted by ForeignKeyField
}
```

> - **Local data** — sorting is based on the `ForeignKeyValue` (display text).
> - **Remote data** — sorting is based on the `ForeignKeyField` unless the service supports sorting on display text.

## Touch Interaction

On touch-enabled devices, tapping a column header sorts that column. A multi-sort popup icon appears when both `AllowSorting` and `AllowMultiSorting` are `true`. Tap the popup icon, then tap additional column headers to sort multiple columns simultaneously.

## Custom Sort Icon

Override the default sort icons using CSS by targeting `.e-icon-ascending` and `.e-icon-descending`:

```css
.e-grid .e-icon-ascending::before {
    content: '\e87a';
}

.e-grid .e-icon-descending::before {
    content: '\e70d';
}
```

## Sorting Events

```razor
<GridEvents TValue="Order" Sorting="SortingHandler" Sorted="SortedHandler"></GridEvents>
@code {
    void SortingHandler(SortingEventArgs args)
    {
        // Cancel sorting for specific column
        if (args.ColumnName == "Freight") args.Cancel = true;
        // Modify sort direction dynamically before sort is applied
        if (args.ColumnName == "CustomerID" && args.Direction == SortDirection.Ascending)
            args.Direction = SortDirection.Descending;
    }
    void SortedHandler(SortedEventArgs args)
    {
        Console.WriteLine($"Sorted by: {args.ColumnName}, Direction: {args.Direction}");
    }
}

