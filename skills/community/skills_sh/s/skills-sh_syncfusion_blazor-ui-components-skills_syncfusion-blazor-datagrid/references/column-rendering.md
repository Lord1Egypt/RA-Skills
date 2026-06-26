# Column Rendering — Syncfusion Blazor DataGrid

## Table of Contents
1. [Define Columns Manually](#define-columns-manually)
2. [Auto-Generated Columns](#auto-generated-columns)
3. [Configure Primary Key](#configure-primary-key)
4. [Configure Column Options](#configure-column-options)
5. [Column Field Binding](#column-field-binding)

---

## Define Columns Manually

Manually define columns using GridColumn to specify each column and configure properties:

```razor
<SfGrid DataSource="@Orders">
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" 
                  TextAlign="TextAlign.Right" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer ID" 
                  Width="150"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" Format="C2" 
                  TextAlign="TextAlign.Right" Width="120"></GridColumn>
        <GridColumn Field="OrderDate" HeaderText="Order Date" Format="d" 
                  Type="ColumnType.Date" Width="130"></GridColumn>
    </GridColumns>
</SfGrid>
```

Benefits:
- Full control over column behavior
- Customize properties individually
- Define sorting, filtering, and editing rules
- Set specific data types and formats

---

## Auto-Generated Columns

When no GridColumns block is defined, columns are automatically generated from the DataSource:

```razor
<SfGrid DataSource="@Orders">
    <!-- No GridColumns block — columns auto-generated from Order properties -->
</SfGrid>
```

How it works:
- All properties in DataSource become columns
- Column type inferred from first record
- Default header text is property name
- Operations like sorting and filtering enabled automatically

> When columns are auto-generated, the column `Type` is determined from the first record of the `DataSource`. For large datasets, auto-generating columns can impact performance.

---

## Configure Primary Key

Set a primary key for auto-generated columns using the `OnDataBound` event:

```razor
<SfGrid @ref="Grid" DataSource="@Orders" AllowPaging="true">
    <GridEditSettings AllowEditing="true" AllowAdding="true" AllowDeleting="true"></GridEditSettings>
    <GridEvents OnDataBound="DataBoundHandler" TValue="OrderData"></GridEvents>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    public void DataBoundHandler(BeforeDataBoundArgs<OrderData> args)
    {
        // Set first column as primary key
        Grid.Columns[0].IsPrimaryKey = true;
    }
}
```

Why it's needed:
- Uniquely identify rows for CRUD operations
- Required when editing is enabled
- Enables update and delete functionality

---

## Configure Column Options

Apply column options like Type, Format, and Width to auto-generated columns:

```razor
<SfGrid @ref="Grid" DataSource="@Orders">
    <GridEvents OnDataBound="DataBoundHandler" TValue="OrderData"></GridEvents>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    public void DataBoundHandler(BeforeDataBoundArgs<OrderData> args)
    {
        var gridColumns = Grid.Columns;
        
        foreach (var column in gridColumns)
        {
            if (column.Field == "OrderID")
            {
                column.Width = "200";
                column.Type = ColumnType.Integer;
            }
            else if (column.Field == "OrderDate")
            {
                column.Type = ColumnType.Date;
                column.Format = "d";
            }
            else if (column.Field == "Freight")
            {
                column.Format = "C2";
                column.TextAlign = TextAlign.Right;
            }
        }
    }
}
```

Configurable properties:
- **Type**: ColumnType (String, Number, Date, DateTime, Boolean)
- **Format**: Display format (C2, d, N2, etc.)
- **Width**: Column width
- **TextAlign**: Text alignment
- **HeaderText**: Custom header text

---

## Column Field Binding

The Field property maps DataSource values to Grid columns:

```razor
<GridColumn Field="OrderID" HeaderText="Order ID" Width="120"></GridColumn>
<GridColumn Field="CustomerID" HeaderText="Customer" Width="150"></GridColumn>
```

Field binding rules:
- **Required for CRUD operations**: Field must match DataSource property name
- **Not needed for template-only columns**: Pure display columns can omit Field
- **Complex binding supported**: Use dot notation for nested properties
- **Case-sensitive**: Field name must match exactly

```razor
<!-- Simple binding -->
<GridColumn Field="CustomerID"></GridColumn>

<!-- Complex binding (nested properties) -->
<GridColumn Field="Employee.Name"></GridColumn>
<GridColumn Field="Address.City"></GridColumn>
```

> If the column `Field` is not present in the `DataSource`, the column will display empty values. If the `Field` name contains a dot operator, it is treated as complex binding.

