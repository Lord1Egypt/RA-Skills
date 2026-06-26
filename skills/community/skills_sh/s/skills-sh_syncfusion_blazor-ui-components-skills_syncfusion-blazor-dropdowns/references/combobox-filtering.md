# Filtering & Search in ComboBox

## Table of Contents

- [Enable Filtering](#enable-filtering)
- [Filter Types](#filter-types)
- [Local Data Filtering](#local-data-filtering)
- [Remote Data Filtering](#remote-data-filtering)
- [Custom Filtering](#custom-filtering)
- [Debounce Delay](#debounce-delay)
- [Case-Sensitive Filtering](#case-sensitive-filtering)
- [Minimum Filter Length](#minimum-filter-length)
- [Prevent Popup on Filter](#prevent-popup-on-filter)

---

## Enable Filtering

The `AllowFiltering` property enables users to type in the input to filter the list. The default value is `false`.

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Search for a country"
    DataSource="@Countries"
    AllowFiltering="true">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "United Kingdom", Code = "UK" },
        new Country { Name = "Ukraine", Code = "UA" }
    };
}
```

---

## Filter Types

Control how filtering matches text using the `FilterType` property. Options include:

- **StartsWith** - Matches items starting with typed text (default)
- **EndsWith** - Matches items ending with typed text
- **Contains** - Matches items containing the typed text
- **Equal** - Exact match only

### StartsWith Filter (Default)

```razor
<SfComboBox TItem="Country" TValue="string"
    Placeholder="Search (starts with)"
    DataSource="@Countries"
    AllowFiltering="true"
    FilterType="@FilterType.StartsWith">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>
```
Typing "unit" will match "United States" and "United Kingdom"

### Contains Filter

```razor
<SfComboBox TItem="Country" TValue="string"
    Placeholder="Search (contains)"
    DataSource="@Countries"
    AllowFiltering="true"
    FilterType="@FilterType.Contains">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>
```
Typing "land" will match "United Kingdom", "Ireland", "Thailand"

---

## Local Data Filtering

Filtering works automatically with local data:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Product" TValue="int"
    Placeholder="Search products"
    DataSource="@Products"
    AllowFiltering="true"
    FilterType="@FilterType.Contains"
    @bind-Value="@SelectedProduct">
    <ComboBoxFieldSettings Text="ProductName" Value="ProductId"></ComboBoxFieldSettings>
</SfComboBox>

<p>Selected: @SelectedProduct</p>

@code {
    private int SelectedProduct = 0;

    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public string Category { get; set; }
    }

    private List<Product> Products = new()
    {
        new Product { ProductId = 1, ProductName = "Laptop Pro", Category = "Electronics" },
        new Product { ProductId = 2, ProductName = "USB Cable", Category = "Accessories" },
        new Product { ProductId = 3, ProductName = "Wireless Mouse", Category = "Accessories" },
        new Product { ProductId = 4, ProductName = "Monitor", Category = "Electronics" }
    };
}
```

---

## Remote Data Filtering

With remote data via DataManager, filtering sends requests to the server:

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Search employees"
    AllowFiltering="true"
    FilterType="@FilterType.Contains">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
        Adaptor="Syncfusion.Blazor.Adaptors.UrlAdaptor"></SfDataManager>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
    }
}
```

**Server-side implementation:**
Your API should handle the filter request and return matching results:

```csharp
// API Endpoint: GET /api/employees?$filter=Name contains 'John'
[HttpGet]
public IActionResult GetEmployees([FromQuery] string filter)
{
    var employees = dbContext.Employees
        .Where(e => string.IsNullOrEmpty(filter) || e.Name.Contains(filter))
        .ToList();
    return Ok(employees);
}
```

---

## Custom Filtering

Implement custom filtering logic using the `Filtering` event:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Search employees"
    DataSource="@Employees"
    AllowFiltering="true">
    <ComboBoxEvents TItem="Employee" TValue="int" 
        Filtering="@OnFiltering"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith", Department = "IT" },
        new Employee { EmployeeId = 2, Name = "Jane Doe", Department = "HR" },
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Department = "Sales" }
    };

    private void OnFiltering(FilteringEventArgs args)
    {
        // Custom filter logic: search in Name and Department
        var filteredItems = Employees.Where(e =>
            e.Name.Contains(args.Text, StringComparison.OrdinalIgnoreCase) ||
            e.Department.Contains(args.Text, StringComparison.OrdinalIgnoreCase)
        ).ToList();

        args.PreventDefault = true;
        args.UpdateData(filteredItems);
    }
}
```

---

## Debounce Delay

The `DebounceDelay` property (in milliseconds) controls the delay before filtering triggers as the user types. This reduces API calls for remote filtering.

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Search countries"
    AllowFiltering="true"
    DebounceDelay="500">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
        Adaptor="Syncfusion.Blazor.Adaptors.UrlAdaptor"></SfDataManager>
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }
}
```

**Default:** 300ms  
**To disable:** Set to 0

**Use Cases:**
- Set higher (500-1000ms) for slow APIs
- Set lower (100-200ms) for fast local filtering
- Set to 0 only if filtering is instant

---

## Case-Sensitive Filtering

Control whether filtering is case-sensitive using the `IgnoreCase` property:

```razor
@using Syncfusion.Blazor.DropDowns

<div>
    <label>
        <input type="checkbox" @bind="@IgnoreCaseSetting" />
        Ignore Case (case-insensitive)
    </label>
</div>

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Search countries"
    DataSource="@Countries"
    AllowFiltering="true"
    IgnoreCase="@IgnoreCaseSetting"
    FilterType="@FilterType.Contains">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private bool IgnoreCaseSetting = true;

    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "CANADA", Code = "CA" }
    };
}
```

**Default:** `true` (case-insensitive)  
Set to `false` for case-sensitive matching.

---

## Minimum Filter Length

The `MinFilterLength` property determines how many characters must be typed before filtering starts:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Search (min 3 chars)"
    AllowFiltering="true"
    MinFilterLength="3">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
        Adaptor="Syncfusion.Blazor.Adaptors.UrlAdaptor"></SfDataManager>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
    }
}
```

**Use Cases:**
- Set to 3+ for large remote datasets to reduce API calls
- Set to 1 for small local datasets
- Set to 2+ to avoid common prefixes matching irrelevant items

---

## Prevent Popup on Filter

Prevent the popup from opening while filtering:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Type to search"
    DataSource="@Countries"
    AllowFiltering="true">
    <ComboBoxEvents TItem="Country" TValue="string" 
        Filtering="@OnFiltering"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "United Kingdom", Code = "UK" }
    };

    private void OnFiltering(FilteringEventArgs args)
    {
        // Prevent popup from opening
        if (args.Text.Length < 2)
        {
            args.Cancel = true;
        }
    }
}
```

---

## Best Practices

1. **Choose Right Filter Type**
   - Use `StartsWith` for quick matching (e.g., country names)
   - Use `Contains` when users might search middle of text (e.g., "New York")

2. **Optimize Debounce Delay**
   - Local data: 100-200ms
   - Remote API: 300-500ms (default)
   - Slow API: 500-1000ms

3. **Set MinFilterLength for Remote Data**
   - Reduces server load
   - Improves user experience

4. **Case-Insensitive by Default**
   - Keeps `IgnoreCase=true` unless exact match required

5. **Use Custom Filtering for Complex Logic**
   - Multi-field search
   - Fuzzy matching
   - Business rule filtering

---

## Troubleshooting

**Filtering not working?**
- Ensure `AllowFiltering="true"`
- Check `FilterType` setting
- Verify `ComboBoxFieldSettings` property names are correct

**Too many API calls?**
- Increase `DebounceDelay` value
- Set `MinFilterLength` to 2+

**Filtering slow?**
- Reduce dataset size
- Use custom filtering for complex logic
- Consider pagination with API

---

*See also: [Data Binding](data-binding.md), [Cascading ComboBox](cascading-combobox.md), [Advanced Features](advanced-features.md)*
