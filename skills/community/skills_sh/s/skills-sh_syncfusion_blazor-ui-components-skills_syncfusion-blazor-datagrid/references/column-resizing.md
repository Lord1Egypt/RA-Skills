# Column Resizing — Syncfusion Blazor DataGrid

## Table of Contents
1. [Enable Column Resizing](#enable-column-resizing)
2. [Min and Max Width](#min-and-max-width)
3. [Prevent Resizing](#prevent-resizing)
4. [AutoFit Columns](#autofit-columns)
5. [Resize Events](#resize-events)

---

## Enable Column Resizing

Enable column resizing by setting the `AllowResizing` property to **true**:

```razor
<SfGrid DataSource="@Orders" AllowResizing="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>
```

Behavior:
- Click and drag the right edge of column header to resize
- Column width adjusts immediately during drag operation
- In RTL mode, drag the left edge of the header cell

---

## Min and Max Width

Restrict column resizing between minimum and maximum width values:

```razor
<SfGrid DataSource="@Orders" AllowResizing="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" 
                  MinWidth="100" MaxWidth="250" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" 
                  MinWidth="120" MaxWidth="300" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" 
                  MinWidth="80" MaxWidth="200" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>
```

Properties:
- **MinWidth**: Minimum allowed column width (in pixels)
- **MaxWidth**: Maximum allowed column width (in pixels)
- When resizing exceeds the range, width is automatically restricted to the nearest valid value

> The `MinWidth` and `MaxWidth` properties are applied only during column resizing, not when resizing the browser window.

---

## Prevent Resizing

Disable resizing for specific columns by setting `AllowResizing` to **false**:

```razor
<SfGrid DataSource="@Orders" AllowResizing="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" 
                  AllowResizing="false" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>
```

Column-level configuration:
- Override grid-level resizing for specific columns
- Prevent accidental width changes
- Maintain fixed-width columns

---

## AutoFit Columns

Automatically adjust column widths to fit content using the `AutoFitColumnsAsync` method:

```razor
<SfGrid @ref="Grid" DataSource="@Orders">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="120"></GridColumn>
        <GridColumn Field="ShipName" HeaderText="Ship Name" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    // AutoFit all columns
    public async Task AutoFitAllColumns()
    {
        await Grid.AutoFitColumnsAsync();
    }
    
    // AutoFit specific columns
    public async Task AutoFitSpecificColumns()
    {
        await Grid.AutoFitColumnsAsync(new string[] { "OrderID", "ShipName" });
    }
}
```

AutoFit options:
- **All columns**: `AutoFitColumnsAsync()` - no parameters
- **Specific columns**: `AutoFitColumnsAsync(string[])` - pass array of field names

Use cases:
- Initial grid rendering with varying content
- Dynamic data updates
- Content-based layout adjustment

---

## Resize Events

Handle column resizing events:

```razor
<SfGrid DataSource="@Orders" AllowResizing="true">
    <GridEvents OnResizeStart="OnResizeStart" ResizeStopped="ResizeStopped" 
               TValue="OrderData"></GridEvents>
    <GridColumns>
        <GridColumn Field="OrderID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private void OnResizeStart(ResizeStartEventArgs args)
    {
        // Triggered before resizing starts
        // Can cancel resizing by setting args.Cancel = true
    }
    
    private void ResizeStopped(ResizeStoppedEventArgs args)
    {
        // Triggered after resizing completes
        // Access the new column width via args
    }
}
```

Available events:
- **OnResizeStart**: Fired before resizing begins (cancelable)
- **ResizeStopped**: Fired after resizing completes

