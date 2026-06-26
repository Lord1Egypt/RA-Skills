# Filtering and Searching in Syncfusion Blazor DropDown List

## Table of Contents
- [Overview](#overview)
- [Basic Filtering](#basic-filtering)
- [Filter Types](#filter-types)
- [Advanced Configuration](#advanced-configuration)
- [Custom Filtering](#custom-filtering)
- [Multi-Column Filtering](#multi-column-filtering)
- [Performance Optimization](#performance-optimization)

## Overview

Filtering allows users to quickly search and find items in a dropdown list by typing. This is especially valuable for large datasets where scrolling would be inefficient.

**When to use filtering:**
- Lists with 20+ items
- User needs quick item discovery
- Mobile-friendly interfaces
- Accessibility improvement

## Basic Filtering

### Enable Filtering

Simply set `AllowFiltering="true"` to enable search:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                AllowFiltering="true"
                Placeholder="Type to search">
    <DropDownListEvents TValue="string" TItem="string"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<string> Items = new()
    {
        "JavaScript",
        "Java",
        "C#",
        "Python",
        "C++",
        "Go",
        "Rust",
        "TypeScript"
    };
}
```

### Filtering with Object Data

Enable filtering on complex objects with field mapping:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees"
                AllowFiltering="true"
                Placeholder="Search employees">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListEvents TValue="int" TItem="Employee"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice Johnson" },
            new Employee { Id = 2, Name = "Bob Smith" },
            new Employee { Id = 3, Name = "Carol White" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Filter Types

### Contains (Partial Match)

Matches items containing the search text anywhere:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Languages"
                AllowFiltering="true"
                FilterType="FilterType.Contains"
                Placeholder="Search (Contains)">
</SfDropDownList>

<!-- Searching "script" matches: JavaScript, CoffeeScript, TypeScript -->

@code {
    private List<string> Languages = new() { "JavaScript", "Java", "C#", "Python" };
}
```

### StartsWith

Matches items that start with the search text:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Languages"
                AllowFiltering="true"
                FilterType="FilterType.StartsWith"
                Placeholder="Search (StartsWith)">
</SfDropDownList>

<!-- Searching "java" matches: Java, JavaScript -->
<!-- Does NOT match: CoffeeScript -->

@code {
    private List<string> Languages = new() { "JavaScript", "Java", "C#", "Python" };
}
```

### EndsWith

Matches items that end with the search text:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Languages"
                AllowFiltering="true"
                FilterType="FilterType.EndsWith"
                Placeholder="Search (EndsWith)">
</SfDropDownList>

<!-- Searching "Script" matches: JavaScript, TypeScript, CoffeeScript -->

@code {
    private List<string> Languages = new() { "JavaScript", "Java", "C#", "Python" };
}
```

## Advanced Configuration

### Case-Sensitive Filtering

Control filter case sensitivity:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                AllowFiltering="true"
                FilterType="FilterType.Contains"
                IgnoreCase="false"
                Placeholder="Case-sensitive search">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Java", "java", "JAVA" };
    // "java" will NOT match "Java" when IgnoreCase="false"
    // "java" WILL match "Java" when IgnoreCase="true" (default)
}
```

### Minimum Filter Length

Require a minimum number of characters before filtering starts:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Products"
                AllowFiltering="true"
                MinFilterLength="3"
                Placeholder="Type at least 3 characters">
</SfDropDownList>

@code {
    private List<string> Products = new() { "Laptop", "Phone", "Tablet", "Monitor" };
    // Users must type at least 3 characters to see filtered results
    // This reduces data processing for very large datasets
}
```

### Debounce Delay

Add delay before filter executes (reduces server calls for remote filtering):

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                AllowFiltering="true"
                FilterType="FilterType.Contains"
                DebounceDelay="300"
                Placeholder="Search">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
    // Default debounce delay is 300ms
    // This prevents filter from running on every keystroke
}
```

### Filter Textbox Placeholder

Customize the filter input placeholder:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                AllowFiltering="true"
                FilterBarPlaceholder="Find item..."
                Placeholder="Select item">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
}
```

## Custom Filtering

### Filter Events

Use `Filtering` event for custom filter logic:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees"
                AllowFiltering="true"
                Placeholder="Search employees">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListEvents TValue="int" TItem="Employee" Filtering="@HandleFiltering"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Employee> Employees;

    private void HandleFiltering(FilteringEventArgs args)
    {
        // Custom filter logic
        if (args.Text.Length > 0)
        {
            // Modify filter behavior
            var filteredData = Employees.Where(e => 
                e.Name.Contains(args.Text, StringComparison.OrdinalIgnoreCase)
            ).ToList();
            
            args.PreventDefaultAction = true;
            // Apply custom filtered data
        }
    }

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice Johnson", Department = "Engineering" },
            new Employee { Id = 2, Name = "Bob Smith", Department = "Sales" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

### Complex Custom Filters

Implement filtering on multiple fields:

```razor
<SfDropDownList TValue="int" TItem="Product" DataSource="@Products"
                AllowFiltering="true"
                Placeholder="Search products">
    <DropDownListFieldSettings Text="@nameof(Product.Name)" Value="@nameof(Product.Id)" />
    <DropDownListEvents TValue="int" TItem="Product" Filtering="@CustomFilter"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Product> Products;

    private void CustomFilter(FilteringEventArgs args)
    {
        // Search in multiple fields: Name, Category, and Manufacturer
        var searchText = args.Text.ToLower();
        
        var filtered = Products.Where(p => 
            p.Name.Contains(searchText, StringComparison.OrdinalIgnoreCase) ||
            p.Category.Contains(searchText, StringComparison.OrdinalIgnoreCase) ||
            p.Manufacturer.Contains(searchText, StringComparison.OrdinalIgnoreCase)
        ).ToList();
        
        args.PreventDefaultAction = true;
        // Update dropdown with filtered results
    }

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop Pro", Category = "Electronics", Manufacturer = "TechCorp" },
            new Product { Id = 2, Name = "USB Mouse", Category = "Accessories", Manufacturer = "PeripheralCorp" }
        };
    }

    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Category { get; set; }
        public string Manufacturer { get; set; }
    }
}
```

## Multi-Column Filtering

### Filtering Across Multiple Fields

When using multi-column display, filter across relevant columns:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees"
                AllowFiltering="true"
                FilterType="FilterType.Contains"
                Placeholder="Search by name or ID">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListTemplates TItem="Employee">
        <ItemTemplate>
            <span>@context.Id - @context.Name (@context.Department)</span>
        </ItemTemplate>
    </DropDownListTemplates>
    <DropDownListEvents TValue="int" TItem="Employee"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1001, Name = "Alice Johnson", Department = "Engineering" },
            new Employee { Id = 1002, Name = "Bob Smith", Department = "Sales" },
            new Employee { Id = 1003, Name = "Carol White", Department = "Marketing" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

## Performance Optimization

### Remote Data Filtering

For large datasets, perform filtering on the server:

```razor
<SfDropDownList TValue="int" TItem="Item"
                DataSource="@RemoteData"
                AllowFiltering="true"
                Placeholder="Search (remote)">
    <DropDownListFieldSettings Text="@nameof(Item.ItemName)" Value="@nameof(Item.ItemId)" />
    <DropDownListEvents TValue="int" TItem="Item" OnActionBegin="@OnActionBegin"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Item> RemoteData;

    private void OnActionBegin(ActionBeginEventArgs args)
    {
        // Send filter text to server
        // Server performs filtering on full dataset
        // Returns only matching items
        Console.WriteLine($"Filtering: {args.Text}");
    }

    protected override async Task OnInitializedAsync()
    {
        RemoteData = await FetchFromServer();
    }

    private async Task<List<Item>> FetchFromServer()
    {
        // API call to fetch data
        return new List<Item>();
    }

    public class Item
    {
        public int ItemId { get; set; }
        public string ItemName { get; set; }
    }
}
```

### Virtualization with Filtering

Combine filtering with virtualization for very large datasets:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                AllowFiltering="true"
                EnableVirtualization="true"
                Placeholder="Search (virtualized)">
</SfDropDownList>

@code {
    private List<string> Items;
    // Virtualization loads items on demand
    // Combined with filtering, only matching items are rendered
    // Results in fast performance even with 10,000+ items
}
```

## Complete Filtering Example

```razor
@page "/dropdown-filtering"

<h3>Advanced Filtering Example</h3>

<div class="form-group">
    <label>Filter Type</label>
    <select @onchange="e => FilterType = (Syncfusion.Blazor.DropDowns.FilterType)Enum.Parse(typeof(Syncfusion.Blazor.DropDowns.FilterType), e.Value.ToString())">
        <option>@Syncfusion.Blazor.DropDowns.FilterType.StartsWith</option>
        <option>@Syncfusion.Blazor.DropDowns.FilterType.Contains</option>
        <option>@Syncfusion.Blazor.DropDowns.FilterType.EndsWith</option>
    </select>
</div>

<div class="form-group">
    <label>Search Products</label>
    <SfDropDownList TValue="int" TItem="Product"
                    DataSource="@Products"
                    AllowFiltering="true"
                    FilterType="@FilterType"
                    MinFilterLength="1"
                    Placeholder="Type to search...">
        <DropDownListFieldSettings Text="@nameof(Product.Name)" Value="@nameof(Product.Id)" />
    </SfDropDownList>
</div>

@code {
    private List<Product> Products;
    private Syncfusion.Blazor.DropDowns.FilterType FilterType = Syncfusion.Blazor.DropDowns.FilterType.StartsWith;

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop Computer" },
            new Product { Id = 2, Name = "Wireless Mouse" },
            new Product { Id = 3, Name = "USB Keyboard" },
            new Product { Id = 4, Name = "Monitor Display" },
            new Product { Id = 5, Name = "Computer Desk" }
        };
    }

    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Key Takeaways

- Enable filtering with `AllowFiltering="true"`
- Choose appropriate filter types (StartsWith for prefixes, Contains for anywhere, EndsWith for suffixes)
- Use `MinFilterLength` to improve performance
- Implement custom filtering for complex requirements
- Use remote filtering for very large datasets
- Combine with virtualization for optimal performance
- Consider case sensitivity based on user expectations
