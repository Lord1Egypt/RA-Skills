# Data Binding

## Table of Contents
- [Overview](#overview)
- [List and Collection Binding](#list-and-collection-binding)
- [Remote Data and API Integration](#remote-data-and-api-integration)
- [Custom Data Adapters](#custom-data-adapters)
- [Value Binding Patterns](#value-binding-patterns)
- [Handling Null and Empty Data](#handling-null-and-empty-data)
- [Performance Considerations](#performance-considerations)

## Overview

Data binding connects your MultiSelect Dropdown to data sources. The component supports:
- **Local collections** (List, Array, IEnumerable)
- **Remote APIs** (HTTP calls to backend)
- **Custom adapters** (DataManager with OData, WebAPI adapters)
- **Observable collections** (for real-time updates)

## List and Collection Binding

### Binding to a Simple List

```csharp
@page "/data-binding-list"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="string"
               DataSource="@CountryList"
               Placeholder="Select countries">
</SfMultiSelect>

@code {
    private List<string> CountryList { get; set; } = new()
    {
        "USA", "Germany", "France", "Japan", "India"
    };
}
```

**When to use:** Simple string lists or basic options.

### Binding to Complex Objects

```csharp
@page "/data-binding-complex"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Employee"
               DataSource="@Employees"
               Placeholder="Select employees">
    <MultiSelectFieldSettings Text="Name" Value="EmployeeID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Employee> Employees { get; set; } = new();

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { EmployeeID = "1", Name = "John Smith", Department = "IT" },
            new Employee { EmployeeID = "2", Name = "Sarah Johnson", Department = "HR" },
            new Employee { EmployeeID = "3", Name = "Mike Brown", Department = "Finance" }
        };
    }

    public class Employee
    {
        public string EmployeeID { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

**Key properties:**
- `Text` - Property to display in dropdown
- `Value` - Property to use as selected value (usually unique ID)

### Binding to ObservableCollection

For real-time updates when data changes:

```csharp
@using System.Collections.ObjectModel
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private ObservableCollection<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new ObservableCollection<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" }
        };

        // Adding items dynamically
        Items.Add(new Item { ID = "3", Name = "Item 3" });  // Component updates automatically
    }

    public class Item
    {
        public string ID { get; set; }
        public string Name { get; set; }
    }
}
```

**Benefit:** Component automatically reflects collection changes.

## Remote Data and API Integration

### Fetching Data from HTTP API

```csharp
@page "/data-binding-api"
@using Syncfusion.Blazor.DropDowns
@inject HttpClient Http

<SfMultiSelect TValue="string[]"
               TItem="ApiProduct"
               DataSource="@ApiData"
               Placeholder="Select products">
    <MultiSelectFieldSettings Text="ProductName" Value="ProductID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<ApiProduct> ApiData { get; set; } = new();
    private bool IsLoading = true;

    protected override async Task OnInitializedAsync()
    {
        try
        {
            ApiData = await Http.GetFromJsonAsync<List<ApiProduct>>("YOUR_API_ENDPOINT");
            IsLoading = false;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error loading data: {ex.Message}");
        }
    }

    public class ApiProduct
    {
        public string ProductID { get; set; }
        public string ProductName { get; set; }
        public decimal Price { get; set; }
    }
}
```

### Handling Loading States

```csharp
@page "/data-binding-loading"
@using Syncfusion.Blazor.DropDowns

@if (IsLoading)
{
    <p>Loading data...</p>
}
else if (ApiData == null || ApiData.Count == 0)
{
    <p>No data available</p>
}
else
{
    <SfMultiSelect TValue="string[]"
                   TItem="Product"
                   DataSource="@ApiData">
        <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    </SfMultiSelect>
}

@code {
    private List<Product> ApiData { get; set; }
    private bool IsLoading = true;

    protected override async Task OnInitializedAsync()
    {
        await Task.Delay(1000);  // Simulate API call
        ApiData = new List<Product>
        {
            new Product { ID = "1", Name = "Product A" }
        };
        IsLoading = false;
    }

    public class Product { public string ID { get; set; } public string Name { get; set; } }
}
```

## Custom Data Adapters

### Using OData Adapter

For OData-compliant APIs:

```csharp
@page "/data-binding-odata"
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Data
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="int[]"
               TItem="OrderData"
               Placeholder="Select orders">
    <SfDataManager Url="YOUR_ODATA_SERVICE_URL" 
                   Adaptor="Adaptors.ODataV4Adaptor">
    </SfDataManager>
    <MultiSelectFieldSettings Text="ShipName" Value="OrderID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    public class OrderData
    {
        public int OrderID { get; set; }
        public string ShipName { get; set; }
    }
}
```

### Using Web API Adapter

For RESTful APIs:

```csharp
<SfMultiSelect TValue="string[]"
               TItem="CustomerData">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Adaptors.WebApiAdaptor">
    </SfDataManager>
    <MultiSelectFieldSettings Text="CustomerName" Value="CustomerID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    public class CustomerData
    {
        public string CustomerID { get; set; }
        public string CustomerName { get; set; }
    }
}
```

## Value Binding Patterns

### Two-Way Binding

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedValues">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<p>Selected: @string.Join(", ", SelectedValues ?? Array.Empty<string>())</p>

@code {
    private string[] SelectedValues { get; set; } = Array.Empty<string>();
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Option 1" },
            new Item { ID = "2", Name = "Option 2" }
        };
        
        // Set initial selection
        SelectedValues = new string[] { "1" };
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

### One-Way Binding

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Value="SelectedValues">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private string[] SelectedValues { get; set; } = new string[] { "1", "2" };
}
```

### Binding Complex Types

```csharp
@page "/complex-binding"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="Product[]"
               TItem="Product"
               DataSource="@Products"
               @bind-Value="SelectedProducts"
               Placeholder="Select products">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Product> Products { get; set; } = new();
    private Product[] SelectedProducts { get; set; } = Array.Empty<Product>();

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { ID = "1", Name = "Product A" },
            new Product { ID = "2", Name = "Product B" }
        };
    }

    public class Product 
    { 
        public string ID { get; set; } 
        public string Name { get; set; } 
    }
}
```

## Handling Null and Empty Data

### Null Data Source

```csharp
@page "/null-handling"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="No items available">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; }  // Null initially

    protected override void OnInitialized()
    {
        // Initialize as empty list to prevent null reference
        Items = new List<Item>();  
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

### Conditional Rendering for Empty State

```csharp
@if (Items?.Count == 0)
{
    <p>No data available</p>
}
else
{
    <SfMultiSelect TValue="string[]"
                   TItem="Item"
                   DataSource="@Items">
        <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    </SfMultiSelect>
}

@code {
    private List<Item> Items { get; set; } = new();
    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

## Performance Considerations

### Enable Virtualization for Large Datasets

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@LargeDataSet"
               EnableVirtualization="true"
               PopupHeight="300px">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> LargeDataSet { get; set; } = new();

    protected override void OnInitialized()
    {
        // Generate large dataset
        LargeDataSet = Enumerable.Range(1, 10000)
            .Select(i => new Item { ID = i.ToString(), Name = $"Item {i}" })
            .ToList();
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

### Pagination for Remote Data

```csharp
protected override async Task OnInitializedAsync()
{
    var query = new Query()
        .AddParams("$skip", 0)      // Skip first 0 items
        .AddParams("$take", 50);    // Take 50 items

    ApiData = await Http.GetFromJsonAsync<List<Item>>($"YOUR_API_ENDPOINT?skip=0&take=50");
}
```

### Caching to Reduce API Calls

```csharp
private Dictionary<string, List<Item>> DataCache { get; set; } = new();

protected override async Task OnInitializedAsync()
{
    string cacheKey = "categories";
    
    if (DataCache.ContainsKey(cacheKey))
    {
        Items = DataCache[cacheKey];
    }
    else
    {
        Items = await Http.GetFromJsonAsync<List<Item>>("YOUR_API_ENDPOINT");
        DataCache[cacheKey] = Items;
    }
}
```

## Key Takeaways

✅ Always initialize collections to prevent null reference errors  
✅ Use `TItem` matching your data source type  
✅ Set `Text` and `Value` properties in `MultiSelectFieldSettings`  
✅ For large datasets, enable virtualization  
✅ Use ObservableCollection for real-time updates  
✅ Cache frequently-accessed remote data

## Next Steps

- **Configure selection modes** → See [Features and Selection](features-and-selection.md)
- **Add filtering** → See [Filtering and Grouping](filtering-and-grouping.md)
- **Handle events** → See [Events and API Reference](events-and-api.md)
