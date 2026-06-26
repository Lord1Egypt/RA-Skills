# Column Menu — Syncfusion Blazor DataGrid

## Table of Contents
1. [Enable Column Menu](#enable-column-menu)
2. [Default Menu Items](#default-menu-items)
3. [Disable Menu for Specific Column](#disable-menu-for-specific-column)
4. [Add Custom Menu Items](#add-custom-menu-items)
5. [Handle Menu Item Click](#handle-menu-item-click)
6. [Customize Menu Items](#customize-menu-items)

---

## Enable Column Menu

Enable the column menu by setting `ShowColumnMenu` to **true**:

```razor
<SfGrid DataSource="@Orders" Height="315" AllowGrouping="true" AllowSorting="true" 
        AllowFiltering="true" ShowColumnMenu="true">
    <GridFilterSettings Type="FilterType.CheckBox"></GridFilterSettings>
    <GridGroupSettings ShowGroupedColumn="true"></GridGroupSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="120"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Result:
- Click menu icon in column header to open contextual menu
- Quick access to sorting, filtering, and other operations

---

## Default Menu Items

The column menu provides these built-in operations:

| Item | Function |
|------|----------|
| **SortAscending** | Sort column in ascending order |
| **SortDescending** | Sort column in descending order |
| **Group** | Group data by this column |
| **Ungroup** | Remove grouping for this column |
| **AutoFit** | Adjust column width to fit content |
| **AutoFitAll** | Adjust all columns to fit content |
| **ColumnChooser** | Open column visibility dialog |
| **Filter** | Display filter options for column |

---

## Disable Menu for Specific Column

Prevent the column menu from appearing for specific columns:

```razor
<SfGrid DataSource="@Orders" Height="315" ShowColumnMenu="true">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" 
                  ShowColumnMenu="false" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="100"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="100"></GridColumn>
        <GridColumn Field="ShipCity" HeaderText="Ship City" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>
```

Use cases:
- Protect primary key columns
- Prevent customization of critical columns
- Simplify menu for certain columns

---

## Add Custom Menu Items

Add custom items to the column menu using `ColumnMenuItems`:

```razor
<SfGrid @ref="Grid" DataSource="@Orders" Height="315" 
        ColumnMenuItems="@MenuItems" ShowColumnMenu="true" 
        AllowGrouping="true" AllowSorting="true">
    <GridEvents ColumnMenuItemClicked="ColumnMenuItemClickedHandler" TValue="OrderData"></GridEvents>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" Width="100"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    public List<ColumnMenuItemModel> MenuItems = new List<ColumnMenuItemModel>
    {
        new ColumnMenuItemModel { Text = "Clear Sorting", Id = "clearSort" },
        new ColumnMenuItemModel { Text = "Clear Grouping", Id = "clearGroup" }
    };
    
    public void ColumnMenuItemClickedHandler(ColumnMenuClickEventArgs args)
    {
        switch (args.Item.Id)
        {
            case "clearSort":
                Grid.ClearSortingAsync();
                break;
            case "clearGroup":
                Grid.ClearGroupingAsync();
                break;
        }
    }
}
```

Custom menu features:
- Define unique menu items
- Assign ID to identify items
- Handle clicks via events

---

## Handle Menu Item Click

Handle column menu item clicks using the `ColumnMenuItemClicked` event:

```razor
<SfGrid @ref="Grid" DataSource="@Orders" ShowColumnMenu="true">
    <GridEvents ColumnMenuItemClicked="OnMenuItemClicked" TValue="OrderData"></GridEvents>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="100"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    public void OnMenuItemClicked(ColumnMenuClickEventArgs args)
    {
        // Access menu item information
        var menuId = args.Item.Id;
        var columnField = args.Column.Field;
        var columnText = args.Column.HeaderText;
        
        // Handle custom logic
        if (menuId == "customAction")
        {
            // Perform custom action
        }
    }
}
```

Event arguments:
- **Item**: The clicked menu item
- **Column**: The column on which menu was opened
- Access item properties: Text, Id
- Access column properties: Field, HeaderText, Width

---

## Customize Menu Items

Hide or customize menu items for specific columns using `OnColumnMenuOpen` event:

```razor
<SfGrid @ref="Grid" DataSource="@Orders" ShowColumnMenu="true">
    <GridEvents OnColumnMenuOpen="OnColumnMenuOpenHandler" TValue="OrderData"></GridEvents>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public void OnColumnMenuOpenHandler(ColumnMenuOpenEventArgs args)
    {
        foreach (var item in args.Items)
        {
            // Hide Filter option for OrderID column
            if (item.Text == "Filter" && args.Column.Field == "OrderID")
            {
                item.Hidden = true;
            }
        }
    }
}
```

Customization options:
- Show/hide items conditionally
- Disable items based on column
- Modify item properties
- Control menu behavior per column

