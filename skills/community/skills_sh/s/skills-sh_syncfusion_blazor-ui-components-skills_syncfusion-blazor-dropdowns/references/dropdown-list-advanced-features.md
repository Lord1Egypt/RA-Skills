# Advanced Features in Syncfusion Blazor DropDown List

## Table of Contents
- [Cascading Dropdowns](#cascading-dropdowns)
- [Grouping Items](#grouping-items)
- [Sorting and Ordering](#sorting-and-ordering)
- [Disabled Items](#disabled-items)
- [Placeholder and Float Label](#placeholder-and-float-label)
- [Popup Settings](#popup-settings)
- [Virtualization](#virtualization)

## Cascading Dropdowns

### Basic Cascading Pattern

Create dependent dropdowns where selection in one affects options in another:

```razor
<SfDropDownList TValue="int" TItem="Country" @bind-Value="SelectedCountryId"
                DataSource="@Countries"
                Placeholder="Select country">
    <DropDownListFieldSettings Text="@nameof(Country.Name)" Value="@nameof(Country.Id)" />
    <DropDownListEvents TValue="int" TItem="Country" ValueChange="@OnCountryChange"></DropDownListEvents>
</SfDropDownList>

<SfDropDownList TValue="int" TItem="State" @bind-Value="SelectedStateId"
                DataSource="@FilteredStates"
                Placeholder="Select state"
                Enabled="@(SelectedCountryId > 0)">
</SfDropDownList>

@code {
    private int SelectedCountryId;
    private int SelectedStateId;
    private List<Country> Countries;
    private List<State> FilteredStates;

    private async Task OnCountryChange(ChangeEventArgs<int, Country> args)
    {
        SelectedCountryId = args.Value;
        SelectedStateId = 0;  // Reset state selection
        
        // Filter states based on selected country
        FilteredStates = States.Where(s => s.CountryId == SelectedCountryId).ToList();
    }

    protected override void OnInitialized()
    {
        Countries = new List<Country>
        {
            new Country { Id = 1, Name = "United States" },
            new Country { Id = 2, Name = "Canada" },
            new Country { Id = 3, Name = "Mexico" }
        };

        FilteredStates = new List<State>();
    }

    public class Country
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }

    public class State
    {
        public int Id { get; set; }
        public int CountryId { get; set; }
        public string Name { get; set; }
    }
}
```

### Three-Level Cascading

Cascade through three levels (Country → State → City):

```razor
<SfDropDownList TValue="int" TItem="int" @bind-Value="SelectedCountry"
                DataSource="@Countries"
                Placeholder="Country">
    <DropDownListEvents TValue="int" TItem="int" ValueChange="@OnCountryChange"></DropDownListEvents>
</SfDropDownList>

<SfDropDownList TValue="int" TItem="int" @bind-Value="SelectedState"
                DataSource="@FilteredStates"
                Enabled="@(SelectedCountry > 0)"
                Placeholder="State">
    <DropDownListEvents TValue="int" TItem="int" ValueChange="@OnStateChange"></DropDownListEvents>
</SfDropDownList>

<SfDropDownList TValue="int" TItem="int" @bind-Value="SelectedCity"
                DataSource="@FilteredCities"
                Enabled="@(SelectedState > 0)"
                Placeholder="City">
</SfDropDownList>

@code {
    private int SelectedCountry, SelectedState, SelectedCity;
    private List<int> Countries = new() { 1, 2, 3 };
    private List<int> FilteredStates = new();
    private List<int> FilteredCities = new();

    private void OnCountryChange(ChangeEventArgs<int> args)
    {
        SelectedCountry = args.Value;
        SelectedState = 0;
        SelectedCity = 0;
        FilteredStates = GetStatesForCountry(args.Value);
        FilteredCities = new();
    }

    private void OnStateChange(ChangeEventArgs<int> args)
    {
        SelectedState = args.Value;
        SelectedCity = 0;
        FilteredCities = GetCitiesForState(args.Value);
    }

    private List<int> GetStatesForCountry(int countryId) => new();
    private List<int> GetCitiesForState(int stateId) => new();
}
```

## Grouping Items

### Group Related Items

Organize dropdown items into logical groups:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees"
                Placeholder="Select employee">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" GroupBy="@nameof(Employee.Department)" />
</SfDropDownList>

@code {
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice", Department = "Engineering" },
            new Employee { Id = 2, Name = "Bob", Department = "Engineering" },
            new Employee { Id = 3, Name = "Carol", Department = "Sales" },
            new Employee { Id = 4, Name = "David", Department = "Sales" }
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

### Group with Template

Customize group header appearance:

```razor
<SfDropDownList TValue="int" TItem="Product" DataSource="@Products">
    <DropDownListFieldSettings Text="@nameof(Product.Name)" Value="@nameof(Product.Id)" GroupBy="@nameof(Product.Category)" />
    <DropDownListTemplates TItem="Product">
        <GroupTemplate>
            <div style="padding: 8px; font-weight: bold; background: #f0f0f0;">
                @context.Key (@(Products.Count(p => p.Category == context.Key.ToString())) items)
            </div>
        </GroupTemplate>
        <ItemTemplate>
            <span>@context.Name - $@context.Price</span>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<Product> Products;

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop", Category = "Electronics", Price = 999.99m },
            new Product { Id = 2, Name = "Mouse", Category = "Electronics", Price = 29.99m },
            new Product { Id = 3, Name = "Shirt", Category = "Clothing", Price = 49.99m }
        };
    }

    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Category { get; set; }
        public decimal Price { get; set; }
    }
}
```

## Sorting and Ordering

### Sort Alphabetically

Sort items in ascending or descending order:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items.OrderBy(x => x).ToList()"
                Placeholder="Alphabetical order">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Zebra", "Apple", "Banana", "Cherry" };
}
```

### Sort Complex Objects

Sort objects by a specific property:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees.OrderBy(e => e.Name).ToList()"
                Placeholder="Sorted by name">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
</SfDropDownList>

@code {
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 3, Name = "Carol" },
            new Employee { Id = 1, Name = "Alice" },
            new Employee { Id = 2, Name = "Bob" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Disabled Items

### Disable Specific Items

Mark certain items as non-selectable:

```razor
<SfDropDownList TValue="int" TItem="Item" DataSource="@Items"
                Placeholder="Some items disabled">
    <DropDownListFieldSettings Text="@nameof(Item.Text)" Value="@nameof(Item.Value)" Disabled="@nameof(Item.IsDisabled)" />
</SfDropDownList>

@code {
    private List<Item> Items;

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { Value = 1, Text = "Option A", IsDisabled = false },
            new Item { Value = 2, Text = "Option B (Unavailable)", IsDisabled = true },
            new Item { Value = 3, Text = "Option C", IsDisabled = false }
        };
    }

    public class Item
    {
        public int Value { get; set; }
        public string Text { get; set; }
        public bool IsDisabled { get; set; }
    }
}
```

## Placeholder and Float Label

### Basic Placeholder

Show hint text when no selection is made:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                Placeholder="Select an option">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

### Float Label

Display floating label above the component:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                FloatLabelType="FloatLabelType.Auto"
                Placeholder="Choose option">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

### Float Label with Color

Customize float label appearance:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                FloatLabelType="FloatLabelType.Always"
                Placeholder="Select item"
                CssClass="float-label-colored">
</SfDropDownList>

<style>
    .float-label-colored .e-float-text {
        color: #007bff;
        font-weight: bold;
    }
</style>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
}
```

## Popup Settings

### Configure Popup Position

Control where the dropdown popup appears:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                PopupWidth="300px"
                PopupHeight="400px"
                Placeholder="Select item">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Option 1", "Option 2", "Option 3" };
}
```

### Popup with Animations

Add animations when opening/closing:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                AllowFiltering="true"
                Placeholder="Select item">
</SfDropDownList>

@code {
    // Animations are automatically handled by Syncfusion
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
}
```

## Virtualization

### Enable for Large Datasets

Use virtualization for excellent performance with thousands of items:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@LargeDataset"
                EnableVirtualization="true"
                AllowFiltering="true"
                Placeholder="Select from 10,000+ items">
</SfDropDownList>

@code {
    private List<string> LargeDataset;

    protected override void OnInitialized()
    {
        // Create dataset with 10,000+ items
        LargeDataset = Enumerable.Range(1, 10000)
            .Select(i => $"Item {i:D5}")
            .ToList();
    }
}
```

### Virtualization with Grouping

Combine virtualization with grouping for performance:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Items"
                EnableVirtualization="true"
                AllowFiltering="true"
                Placeholder="Virtual + Grouped">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" GroupBy="@nameof(Employee.Department)" />
    <DropDownListEvents TValue="int" TItem="Employee"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Employee> Items;

    protected override void OnInitialized()
    {
        // Create large dataset with grouping
        Items = new List<Employee>();
        for (int i = 1; i <= 5000; i++)
        {
            Items.Add(new Employee
            {
                Id = i,
                Name = $"Employee {i:D4}",
                Department = i % 3 switch
                {
                    0 => "Engineering",
                    1 => "Sales",
                    _ => "Marketing"
                }
            });
        }
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

## Complete Advanced Features Example

```razor
@page "/dropdown-advanced"

<h3>Advanced Features Example</h3>

<div class="form-group">
    <label>Country</label>
    <SfDropDownList TValue="int" TItem="Country"
                    @bind-Value="SelectedCountry"
                    DataSource="@Countries"
                    Placeholder="Select country">
        <DropDownListFieldSettings Text="Name" Value="Id" />
        <DropDownListEvents TValue="int" TItem="Country" ValueChange="@OnCountryChange"></DropDownListEvents>
    </SfDropDownList>
</div>

<div class="form-group">
    <label>Department</label>
    <SfDropDownList TValue="string" TItem="string"
                    @bind-Value="SelectedDepartment"
                    DataSource="@Departments.OrderBy(d => d).ToList()"
                    Placeholder="Select department">
    </SfDropDownList>
</div>

<div class="form-group">
    <label>Employee</label>
    <SfDropDownList TValue="int" TItem="Employee"
                    @bind-Value="SelectedEmployee"
                    DataSource="@Employees"
                    EnableVirtualization="true"
                    AllowFiltering="true"
                    FloatLabelType="Syncfusion.Blazor.Inputs.FloatLabelType.Auto"
                    Placeholder="Search employee">
        <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    </SfDropDownList>
</div>

@code {
    private int SelectedCountry;
    private string SelectedDepartment;
    private int SelectedEmployee;
    private List<int> Countries = new() { 1, 2, 3 };
    private List<string> Departments = new() { "Engineering", "Sales", "Marketing" };
    private List<Employee> Employees = new();

    protected override void OnInitialized()
    {
        for (int i = 1; i <= 5000; i++)
        {
            Employees.Add(new Employee { Id = i, Name = $"Employee {i:D4}" });
        }
    }

    private void OnCountryChange(ChangeEventArgs<int> args)
    {
        SelectedCountry = args.Value;
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Key Takeaways

- Use cascading dropdowns for dependent selections
- Group items to improve organization and UX
- Sort items for better discoverability
- Disable items that shouldn't be selected
- Use float labels for better form layout
- Configure popup dimensions for appropriate sizing
- Enable virtualization for large datasets (1000+ items)
- Combine features: grouping + virtualization for optimal performance
