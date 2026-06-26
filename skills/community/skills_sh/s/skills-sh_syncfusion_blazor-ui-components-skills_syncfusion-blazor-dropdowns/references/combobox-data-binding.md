# Data Binding in ComboBox

## Table of Contents

- [Local Data Binding](#local-data-binding)
- [Primitive Types](#primitive-types)
- [Complex Objects](#complex-objects)
- [Collections and Observables](#collections-and-observables)
- [Index Value Binding](#index-value-binding)
- [Remote Data with DataManager](#remote-data-with-datamanager)
- [OData Adaptor](#odata-adaptor)
- [Web API Adaptor](#web-api-adaptor)
- [Custom Adaptor](#custom-adaptor)
- [Dynamic Data Loading](#dynamic-data-loading)

---

## Local Data Binding

The ComboBox component binds to local data sources using the `DataSource` property. The `TItem` generic parameter specifies the data type.

### Primitive Types

Bind directly to a list of strings, integers, or other primitive types:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select a language"
    DataSource="@Languages"
    @bind-Value="@SelectedLanguage">
</SfComboBox>

<p>Selected: @SelectedLanguage</p>

@code {
    private string SelectedLanguage = "C#";
    private List<string> Languages = new() 
    { 
        "C#", "JavaScript", "Python", "Java", "TypeScript" 
    };
}
```

### Complex Objects

For objects with multiple properties, use `ComboBoxFieldSettings` to specify which property to display and which to use as value:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
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
}
```

### Collections and Observables

ComboBox supports various collection types:

**List<T>:**
```razor
private List<string> Items = new() { "Item1", "Item2", "Item3" };
```

**ObservableCollection<T>:**
```razor
@using System.Collections.ObjectModel

private ObservableCollection<string> Items = new() 
{ 
    "Item1", "Item2", "Item3" 
};
```

**Array:**
```razor
private string[] Items = { "Item1", "Item2", "Item3" };
```

**IEnumerable<T>:**
```razor
private IEnumerable<string> Items => GetItems();

private IEnumerable<string> GetItems()
{
    return new List<string> { "Item1", "Item2", "Item3" };
}
```

---

## Index Value Binding

Bind selection by index using `@bind-Index` instead of value binding:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries"
    @bind-Index="@SelectedIndex">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

<p>Selected Index: @SelectedIndex</p>
<p>Selected Country: @(SelectedIndex.HasValue ? Countries[(int)SelectedIndex].Name : "None")</p>

@code {
    private int? SelectedIndex = 0;

    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "United Kingdom", Code = "UK" },
        new Country { Name = "Canada", Code = "CA" }
    };
}
```

**Key Points:**
- Index is 0-based
- Index binding works with both primitive and complex types
- Index updates when sorted data changes
- Useful when you need position-based selection

---

## Remote Data with DataManager

Fetch data from a remote server using DataManager:

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
        Adaptor="Syncfusion.Blazor.Adaptors.UrlAdaptor"></SfDataManager>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

---

## OData Adaptor

Bind to an OData service:

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfComboBox TItem="Order" TValue="int"
    Placeholder="Select an order"
    AllowFiltering="true">
    <SfDataManager Url="YOUR_ODATA_SERVICE_URL" 
        Adaptor="Syncfusion.Blazor.Adaptors.ODataAdaptor"
        CrossDomain="true"></SfDataManager>
    <ComboBoxFieldSettings Text="ShipName" Value="OrderID"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Order
    {
        public int OrderID { get; set; }
        public string ShipName { get; set; }
    }
}
```

---

## Web API Adaptor

Connect to a REST API endpoint:

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfComboBox TItem="Product" TValue="int"
    Placeholder="Select a product">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
        Adaptor="Syncfusion.Blazor.Adaptors.WebApiAdaptor"></SfDataManager>
    <ComboBoxFieldSettings Text="ProductName" Value="ProductID"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Product
    {
        public int ProductID { get; set; }
        public string ProductName { get; set; }
        public decimal Price { get; set; }
    }
}
```

---

## Custom Adaptor

Create a custom adaptor for special data handling:

```razor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee">
    <SfDataManager AdaptorInstance="@typeof(CustomAdaptor)" Adaptor="Syncfusion.Blazor.Adaptors.CustomAdaptor"></SfDataManager>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
    }

    public class CustomAdaptor : DataAdaptor
    {
        public override async Task<object> Read(DataManagerRequest dm, string key = null)
        {
            // Custom logic to fetch data
            var employees = await FetchFromCustomSource();
            return employees;
        }

        private async Task<List<Employee>> FetchFromCustomSource()
        {
            // Your custom data fetching logic
            return await Task.FromResult(new List<Employee>
            {
                new Employee { EmployeeId = 1, Name = "John Smith" },
                new Employee { EmployeeId = 2, Name = "Jane Doe" }
            });
        }
    }
}
```

---

## Dynamic Data Loading

Load data dynamically based on user actions:

```razor
@using Syncfusion.Blazor.DropDowns

<div>
    <label>Select Category:</label>
    <SfComboBox TItem="Category" TValue="int"
        Placeholder="Choose a category"
        DataSource="@Categories"
        @bind-Value="@SelectedCategory">
        <ComboBoxEvents TItem="Category" TValue="int"
            ValueChange="@OnCategoryChange"></ComboBoxEvents>
        <ComboBoxFieldSettings Text="CategoryName" Value="CategoryId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

<div style="margin-top: 20px;">
    <label>Select Product:</label>
    <SfComboBox TItem="Product" TValue="int"
        Placeholder="Choose a product"
        DataSource="@Products">
        <ComboBoxFieldSettings Text="ProductName" Value="ProductId"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

@code {
    private int SelectedCategory = 0;
    private List<Product> Products = new();

    public class Category
    {
        public int CategoryId { get; set; }
        public string CategoryName { get; set; }
    }

    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public int CategoryId { get; set; }
    }

    private List<Category> Categories = new()
    {
        new Category { CategoryId = 1, CategoryName = "Electronics" },
        new Category { CategoryId = 2, CategoryName = "Clothing" }
    };

    private List<Product> AllProducts = new()
    {
        new Product { ProductId = 1, ProductName = "Laptop", CategoryId = 1 },
        new Product { ProductId = 2, ProductName = "Shirt", CategoryId = 2 },
        new Product { ProductId = 3, ProductName = "Tablet", CategoryId = 1 }
    };

    private void OnCategoryChange(ChangeEventArgs<int, Category> args)
    {
        // Load products for selected category
        Products = AllProducts
            .Where(p => p.CategoryId == args.Value)
            .ToList();
    }
}
```

---

## Common Patterns

**Pattern: Multiple Data Type Support**
```razor
// Your ComboBox can use generic types that work with any class
<SfComboBox TItem="YourDataClass" TValue="int" DataSource="@YourData">
    <ComboBoxFieldSettings Text="DisplayProperty" Value="ValueProperty"></ComboBoxFieldSettings>
</SfComboBox>
```

**Pattern: Null-Safe Binding**
```razor
@if (Data != null && Data.Any())
{
    <SfComboBox TItem="Item" TValue="int" DataSource="@Data"></SfComboBox>
}
else
{
    <p>No data available</p>
}
```

---

## Troubleshooting

**Data not showing?**
- Verify `DataSource` is populated
- Check property names in `ComboBoxFieldSettings`
- Ensure TItem type matches your data

**Remote data returns empty?**
- Check API endpoint URL and CORS settings
- Verify response format matches expected structure
- Enable browser developer tools network tab to debug

**Binding doesn't update?**
- Ensure two-way binding with `@bind-Value` or `@bind-Index`
- Check for property immutability issues
- Verify StateHasChanged() called if using custom logic

---

*See also: [Filtering & Search](filtering.md), [Cascading ComboBox](cascading-combobox.md), [Selection & Value](selection-and-value.md)*
