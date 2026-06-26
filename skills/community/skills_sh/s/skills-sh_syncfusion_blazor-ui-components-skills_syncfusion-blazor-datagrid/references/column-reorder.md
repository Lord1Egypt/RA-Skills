# Column Reorder — Syncfusion Blazor DataGrid

## Table of Contents
1. [Enable Column Reordering](#enable-column-reordering)
2. [Prevent Reordering](#prevent-reordering)
3. [Programmatic Reordering](#programmatic-reordering)
4. [Reorder by Index](#reorder-by-index)
5. [Reorder by Field](#reorder-by-field)

---

## Enable Column Reordering

Enable column reordering by setting the `AllowReordering` property to **true**:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowReordering="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
        <GridColumn Field="ShipName" HeaderText="Ship Name" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Features:
- Drag and drop column headers to reorder
- Visual feedback during drag operation
- Column data position updates with header

---

## Prevent Reordering

Disable reordering for specific columns by setting `AllowReordering` to **false**:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowReordering="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" AllowReordering="false" Width="100"></GridColumn>
        <GridColumn Field="ShipName" HeaderText="Ship Name" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Use cases:
- Keep primary key columns fixed
- Prevent accidental reordering of critical columns
- Maintain standard column layout

> When columns are reordered, the position of the corresponding column data also changes. Ensure that any logic dependent on column order is updated accordingly.

---

## Programmatic Reordering

Reorder columns programmatically using methods instead of drag-and-drop:

```razor
<SfButton OnClick="ReorderByIndex">Reorder by Index</SfButton>
<SfButton OnClick="ReorderByField">Reorder by Field</SfButton>

<SfGrid @ref="Grid" DataSource="@Orders" Height="315" AllowReordering="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
        <GridColumn Field="ShipName" HeaderText="Ship Name" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    public async Task ReorderByIndex()
    {
        // Move column at index 1 to index 3
        await Grid.ReorderColumnByIndexAsync(1, 3);
    }
    
    public async Task ReorderByField()
    {
        // Move OrderID column to index 2
        await Grid.ReorderColumnByTargetIndexAsync("OrderID", 2);
    }
}
```

Available methods:
- **ReorderColumnByIndexAsync(fromIndex, toIndex)**: Reorder by current and target index
- **ReorderColumnByTargetIndexAsync(fieldName, toIndex)**: Reorder by field name

---

## Reorder by Index

Move columns using their index positions:

```razor
@code {
    public async Task MoveColumnToPosition()
    {
        // fromIndex: current position (0-based)
        // toIndex: target position (0-based)
        await Grid.ReorderColumnByIndexAsync(0, 2);
    }
}
```

Parameters:
- **fromIndex** (int): Current index of the column to move
- **toIndex** (int): Target index where column should be placed

---

## Reorder by Field

Move columns using their field names:

```razor
@code {
    public async Task MoveColumnByName()
    {
        // Move CustomerID column to index 0 (first position)
        await Grid.ReorderColumnByTargetIndexAsync("CustomerID", 0);
        
        // Move ShipCity column to index 3
        await Grid.ReorderColumnByTargetIndexAsync("ShipCity", 3);
    }
}
```

Parameters:
- **fieldName** (string): Field name of the column to move
- **toIndex** (int): Target index where column should be placed

Benefits:
- Clear intent using field names
- No need to track index changes
- More maintainable code

