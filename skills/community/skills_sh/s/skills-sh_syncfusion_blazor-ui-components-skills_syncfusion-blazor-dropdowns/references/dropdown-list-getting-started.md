# Getting Started with Syncfusion Blazor DropDown List

## Installation and Setup

### Step 1: Install NuGet Package

Install the Syncfusion.Blazor.DropDowns NuGet package for dropdown components:

```bash
dotnet add package Syncfusion.Blazor.DropDowns
```

### Step 2: Import Namespaces

Add the required namespaces in your `_Imports.razor` file:

```csharp
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns
```

### Step 3: Register Services

Register Syncfusion Blazor services in `Program.cs`:

```csharp
builder.Services.AddSyncfusionBlazor();
```

### Step 4: Add Theme CSS

Include a theme CSS in your `App.razor` or layout file. Choose from available themes:

```html
<!-- In App.razor or _Host.cshtml -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
```

**Available Themes:**
- `bootstrap5.css` - Bootstrap 5 theme
- `material.css` - Material Design theme
- `fluent.css` - Fluent UI theme
- `tailwind.css` - Tailwind CSS theme
- `fabric.css` - Office Fabric theme
- `material-dark.css` - Material dark mode

## Basic Implementation

### Minimal Working Example

The simplest dropdown requires just a `DataSource` and the component declaration:

```razor
@page "/dropdown-basic"

<h3>Basic Dropdown List</h3>

<SfDropDownList TValue="string" TItem="string" DataSource="@Items" Placeholder="Select an item">
</SfDropDownList>

@code {
    private List<string> Items = new List<string>
    {
        "Item 1",
        "Item 2",
        "Item 3",
        "Item 4"
    };
}
```

### Dropdown with Field Mapping

When working with complex objects, use `DropDownListFieldSettings` to map data fields:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees"
                Placeholder="Select employee">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
</SfDropDownList>

@code {
    public List<Employee> Employees { get; set; }

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "John Smith" },
            new Employee { Id = 2, Name = "Jane Doe" },
            new Employee { Id = 3, Name = "Bob Johnson" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Setting Initial Value

### Default Selection

Set the initial selected value using `Value` property:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                Value="@SelectedItem"
                Placeholder="Choose an item">
</SfDropDownList>

@code {
    private string SelectedItem = "Item 2";  // Pre-selected value
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
}
```

### With Value Binding

Use `@bind-Value` for two-way binding to automatically track selection:

```razor
<SfDropDownList TValue="int" TItem="Product" @bind-Value="SelectedId"
                DataSource="@Products"
                Placeholder="Select product">
    <DropDownListFieldSettings Text="@nameof(Product.Name)" Value="@nameof(Product.Id)" />
</SfDropDownList>

<p>Selected Product ID: @SelectedId</p>

@code {
    private int SelectedId;
    private List<Product> Products;

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop" },
            new Product { Id = 2, Name = "Mouse" },
            new Product { Id = 3, Name = "Keyboard" }
        };
    }
}
```

## Handling Selection Events

### ValueChange Event

Listen to selection changes using `ValueChange` event:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Departments"
                Placeholder="Select department">
    <DropDownListEvents TValue="string" TItem="string" ValueChange="@OnSelectionChange"></DropDownListEvents>
</SfDropDownList>

<p>You selected: @SelectedDepartment</p>

@code {
    private string SelectedDepartment;
    private List<string> Departments = new() { "Sales", "Marketing", "Engineering" };

    private void OnSelectionChange(ChangeEventArgs<string> args)
    {
        SelectedDepartment = args.Value;
        Console.WriteLine($"Selected: {SelectedDepartment}");
    }
}
```

### Multiple Event Handlers

Combine multiple events for comprehensive interaction handling:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedValue"
                DataSource="@Items"
                Placeholder="Select item">
    <DropDownListEvents TValue="string" TItem="string" 
                        Opened="@OnDropdownOpen" 
                        Closed="@OnDropdownClose" 
                        ValueChange="@OnValueChange">
    </DropDownListEvents>
</SfDropDownList>

@code {
    private string SelectedValue;
    private List<string> Items = new() { "Option A", "Option B", "Option C" };

    private void OnDropdownOpen()
    {
        Console.WriteLine("Dropdown opened");
    }

    private void OnDropdownClose()
    {
        Console.WriteLine("Dropdown closed");
    }

    private void OnValueChange(ChangeEventArgs<string> args)
    {
        Console.WriteLine($"Value changed to: {args.Value}");
    }
}
```

## CSS Theme Application

### Applying Different Themes

Change the visual appearance by switching CSS themes:

```razor
@page "/dropdown-theme"

<button @onclick="() => ChangeTheme('bootstrap5')">Bootstrap</button>
<button @onclick="() => ChangeTheme('material')">Material</button>
<button @onclick="() => ChangeTheme('fluent')">Fluent</button>

<SfDropDownList TValue="string" TItem="string" DataSource="@Items" Placeholder="Select item">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
    private string CurrentTheme = "bootstrap5";

    private void ChangeTheme(string theme)
    {
        CurrentTheme = theme;
        // Theme CSS should be switched via App.razor or dynamically
    }
}
```

## Complete Getting Started Example

Here's a complete example combining all concepts:

```razor
@page "/dropdown-complete"

<h3>Complete Dropdown Example</h3>

<div class="form-group">
    <label>Select an Employee</label>
    <SfDropDownList TValue="int" TItem="Employee" @bind-Value="SelectedEmployeeId"
                    DataSource="@Employees"
                    Placeholder="Choose an employee"
                    CssClass="custom-dropdown">
        <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
        <DropDownListEvents TValue="int" TItem="Employee" ValueChange="@OnEmployeeSelected"></DropDownListEvents>
    </SfDropDownList>
</div>

@if (!string.IsNullOrEmpty(SelectedEmployeeName))
{
    <div class="alert alert-info">
        Selected: @SelectedEmployeeName (ID: @SelectedEmployeeId)
    </div>
}

@code {
    private int SelectedEmployeeId;
    private string SelectedEmployeeName;
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice Johnson", Department = "Engineering" },
            new Employee { Id = 2, Name = "Bob Smith", Department = "Sales" },
            new Employee { Id = 3, Name = "Carol White", Department = "Marketing" }
        };
    }

    private void OnEmployeeSelected(ChangeEventArgs<int> args)
    {
        var employee = Employees.FirstOrDefault(e => e.Id == args.Value);
        SelectedEmployeeName = employee?.Name ?? "Unknown";
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

## Next Steps

- **Add Filtering:** Read `filtering-and-searching.md` to enable search functionality
- **Customize Appearance:** Read `customization-and-styling.md` for styling options
- **Bind Remote Data:** Read `data-binding.md` for API integration patterns
- **Add Validation:** Read `form-validation.md` for form integration
