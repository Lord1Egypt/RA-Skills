# Getting Started — Syncfusion Blazor DataGrid

## Overview

Set up the Syncfusion Blazor DataGrid in a **Blazor WebAssembly (WASM)** project. For Server App, Web App, and MAUI variants, see `getting-started-app-types.md`.

## Installation

### 1. Install NuGet Packages

```bash
dotnet add package Syncfusion.Blazor.Grid
dotnet add package Syncfusion.Blazor.Themes
```

Or via Visual Studio NuGet Package Manager: search `Syncfusion.Blazor.Grid`.

### 2. Configure `_Imports.razor`

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Grids
```

### 3. Register Service in `Program.cs` (WASM)

```csharp
using Syncfusion.Blazor;

builder.Services.AddSyncfusionBlazor();
```

### 4. Add Theme and Script in `index.html` (WASM)

```html
<head>
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>
<body>
    ...
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</body>
```

Available themes: `bootstrap5.css`, `material.css`, `fluent.css`, `tailwind.css`, `fabric.css` (and dark variants).

## Basic DataGrid

```razor
@page "/"
@using Syncfusion.Blazor.Grids

<SfGrid DataSource="@Orders">
    <GridColumns>
        <GridColumn Field=@nameof(Order.OrderID)    HeaderText="Order ID"    Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field=@nameof(Order.CustomerID) HeaderText="Customer ID" Width="150"></GridColumn>
        <GridColumn Field=@nameof(Order.Freight)    HeaderText="Freight"     Format="C2" Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field=@nameof(Order.OrderDate)  HeaderText="Order Date"  Format="d"  Width="150" Type="ColumnType.Date"></GridColumn>
        <GridColumn Field=@nameof(Order.ShipCountry) HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public List<Order> Orders { get; set; }
    protected override void OnInitialized()
    {
        Orders = new List<Order>
        {
            new Order { OrderID = 10248, CustomerID = "VINET", Freight = 32.38, OrderDate = new DateTime(1996,7,4), ShipCountry = "France" },
            new Order { OrderID = 10249, CustomerID = "TOMSP", Freight = 11.61, OrderDate = new DateTime(1996,7,5), ShipCountry = "Germany" },
            new Order { OrderID = 10250, CustomerID = "HANAR", Freight = 65.83, OrderDate = new DateTime(1996,7,8), ShipCountry = "Brazil" },
        };
    }
    public class Order
    {
        public int    OrderID     { get; set; }
        public string CustomerID  { get; set; }
        public double Freight     { get; set; }
        public DateTime OrderDate { get; set; }
        public string ShipCountry { get; set; }
    }
}
```

## Feature Flags (Basic Grid)

Enable common features with boolean properties on `SfGrid`:

```razor
<SfGrid DataSource="@Orders"
        AllowPaging="true"
        AllowSorting="true"
        AllowFiltering="true"
        AllowGrouping="true">
    <GridPageSettings PageSize="10"></GridPageSettings>
    <GridColumns>
        ...
    </GridColumns>
</SfGrid>
```

## Error Handling

Handle API/data failures with `OnActionFailure`:

```razor
<SfGrid DataSource="@Orders">
    <GridEvents TValue="Order" OnActionFailure="ActionFailure"></GridEvents>
    ...
</SfGrid>

@code {
    public void ActionFailure(FailureEventArgs args)
    {
        // args.Error contains the exception
        Console.WriteLine($"Grid error: {args.Error}");
    }
}
```

## Model Class Requirements

- Model must have a **parameterless constructor** (used by `Activator.CreateInstance<TValue>()` for new records during editing).
- Primary key column must be set: `IsPrimaryKey="true"`.
- Editing is disabled for `IsPrimaryKey` columns automatically.

## Notes

- The `Field` property of `GridColumn` must match the property name on the data model (case-sensitive for some operations).
- Use `@nameof(Model.Property)` to avoid magic strings.
- `Format="C2"` applies currency formatting; `Format="d"` applies short date format.
- `Type="ColumnType.Date"` must be set explicitly for `DateTime` columns to enable date-specific filtering and editing.
