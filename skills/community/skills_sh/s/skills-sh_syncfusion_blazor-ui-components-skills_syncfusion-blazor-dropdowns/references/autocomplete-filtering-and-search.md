# Filtering & Search in Syncfusion Blazor AutoComplete

## Table of Contents
- [Enabling Filtering](#enabling-filtering)
- [Filter Types](#filter-types)
- [Local Data Filtering](#local-data-filtering)
- [Remote Data Filtering](#remote-data-filtering)
- [DebounceDelay](#debouncedelay)
- [Minimum Character Length](#minimum-character-length)
- [Custom Filtering](#custom-filtering)
- [Highlight Search Results](#highlight-search-results)
- [Case-Sensitive Filtering](#case-sensitive-filtering)

## Enabling Filtering

Enable the filtering feature with the **AllowFiltering** property:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true"
                Placeholder="Type to search...">
</SfAutoComplete>

@code {
    private List<string> Countries = new()
    {
        "Austria",
        "Brazil",
        "Canada",
        "Denmark",
        "Egypt"
    };
}
```

**Note:** By default, `AllowFiltering` is `false`. When enabled, filtering starts immediately as users type in the search box.

## Filter Types

Choose how the component compares user input to list items using **FilterType**:

| FilterType | Behavior | Example |
|-----------|----------|---------|
| `StartsWith` | Value begins with search text | "Ca" matches "Canada" |
| `EndsWith` | Value ends with search text | "ia" matches "Australia" |
| `Contains` | Value contains search text anywhere | "ustr" matches "Austria" |

### StartsWith Filter (Default)

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true"
                FilterType="FilterType.StartsWith">
</SfAutoComplete>
```

**Result:** Typing "Br" shows "Brazil", but "azil" won't match.

### Contains Filter

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true"
                FilterType="FilterType.Contains">
</SfAutoComplete>
```

**Result:** Typing "land" shows "Finland", "Ireland", "Poland".

### EndsWith Filter

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true"
                FilterType="FilterType.EndsWith">
</SfAutoComplete>
```

**Result:** Typing "land" shows "Finland", "Ireland", "Poland".

## Local Data Filtering

When DataSource is a local collection, filtering happens on the client side automatically:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees"
                AllowFiltering="true"
                FilterType="FilterType.Contains">
    <AutoCompleteFieldSettings Value="EmployeeName" ></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, EmployeeName = "John Smith" },
        new Employee { EmployeeId = 2, EmployeeName = "Jane Doe" },
        new Employee { EmployeeId = 3, EmployeeName = "Bob Johnson" }
    };
}
```

**Typing "john"** matches both "John Smith" and "Bob Johnson" with Contains filter.

## Remote Data Filtering

When using remote data sources (Web API, OData), filtering requests are sent to the server:

```blazor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true"
                FilterType="FilterType.Contains">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
    </SfDataManager>
    <AutoCompleteFieldSettings Value="ProductName" >
    </AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
    }
}
```

**Behavior:** Each keystroke sends a filter request to the server with the search text. The server applies filtering and returns matching results.

## DebounceDelay

Control the frequency of filtering operations with **DebounceDelay** (in milliseconds). This prevents excessive requests to remote servers:

### Default Debounce (300ms)

```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true"
                DebounceDelay="300">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
    </SfDataManager>
</SfAutoComplete>
```

**Behavior:** The filter request is delayed by 300ms after the user stops typing. If they continue typing, the delay resets.

### Aggressive Filtering (Lower Delay)

```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true"
                DebounceDelay="100">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
    </SfDataManager>
</SfAutoComplete>
```

**Use When:** You want near-instant feedback and can handle frequent server requests.

### Disable Debounce (Real-Time Filtering)

```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true"
                DebounceDelay="0">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
    </SfDataManager>
</SfAutoComplete>
```

**Warning:** With `DebounceDelay="0"`, a filter request is sent for every keystroke. Use only with small datasets or high-performance backends.

## Minimum Character Length

Set a minimum number of characters required before filtering starts using **MinLength**:

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true"
                MinLength="2"
                Placeholder="Type at least 2 characters">
</SfAutoComplete>
```

**Behavior:** Typing "C" shows no results. Typing "Ca" triggers filtering and shows "Canada".

### Use Case: Reduce Noise

For large datasets, require minimum input to reduce noise:

```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                AllowFiltering="true"
                MinLength="3"
                DebounceDelay="500">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
                   Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor">
    </SfDataManager>
</SfAutoComplete>
```

**Effect:** Reduces server load by requiring at least 3 characters before any filter request.

## Custom Filtering

Implement custom filter logic using **Filtering** event:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Product" 
                DataSource="@Products">
    <AutoCompleteFieldSettings Value="ProductName" ></AutoCompleteFieldSettings>
    <AutoCompleteEvents TValue="string" TItem="Product"
                        Filtering="@OnFiltering">
    </AutoCompleteEvents>
</SfAutoComplete>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Price { get; set; }
    }

    private List<Product> Products = new()
    {
        new Product { ProductId = 1, ProductName = "Apple", Price = 50 },
        new Product { ProductId = 2, ProductName = "Apricot", Price = 40 },
        new Product { ProductId = 3, ProductName = "Banana", Price = 30 }
    };

    private void OnFiltering(FilteringEventArgs args)
    {
        // Filter only items with price > 35
        args.FilteredData = Products
            .Where(p => p.Price > 35 && p.ProductName.Contains(args.Text))
            .Cast<object>()
            .ToList();
    }
}
```

**Advanced Example:** Filter based on multiple conditions:

```csharp
private void OnFiltering(FilteringEventArgs args)
{
    args.FilteredData = Products
        .Where(p => 
            p.ProductName.Contains(args.Text, StringComparison.OrdinalIgnoreCase)
            && p.Price > 25
            && p.ProductId != 999  // Exclude specific product
        )
        .Cast<object>()
        .ToList();
}
```

## Highlight Search Results

The AutoComplete automatically highlights matching search text in results. You can customize this with CSS:

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true"
                FilterType="FilterType.Contains">
</SfAutoComplete>

<style>
    .e-highlight {
        background-color: #fff59d;
        font-weight: bold;
    }
</style>
```

**Result:** When user types "land", the text "land" is highlighted in "Finland", "Ireland", etc.

## Case-Sensitive Filtering

By default, filtering is case-insensitive. For case-sensitive filtering, use custom filtering:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Items">
    <AutoCompleteEvents TValue="string" TItem="string"
                        Filtering="@OnCaseSensitiveFilter">
    </AutoCompleteEvents>
</SfAutoComplete>

@code {
    private List<string> Items = new() { "Apple", "apple", "APPLE" };

    private void OnCaseSensitiveFilter(FilteringEventArgs args)
    {
        // Case-sensitive filtering
        args.FilteredData = Items
            .Where(item => item.Contains(args.Text))  // Case-sensitive
            .Cast<object>()
            .ToList();
    }
}
```

## Best Practices

1. **Use DebounceDelay with Remote Data:** Prevent excessive server requests
2. **Set MinLength Appropriately:** Balance between UX and server load
3. **Choose FilterType by Use Case:** StartsWith for most, Contains for flexible matching
4. **Highlight Important Matches:** Use custom CSS to highlight search text
5. **Test Performance:** Large datasets with aggressive filtering can impact performance

## Related Topics

- [Data Binding](data-binding.md)
- [Templates & Styling](templates-and-styling.md)
- [Advanced Features](advanced-features.md)
