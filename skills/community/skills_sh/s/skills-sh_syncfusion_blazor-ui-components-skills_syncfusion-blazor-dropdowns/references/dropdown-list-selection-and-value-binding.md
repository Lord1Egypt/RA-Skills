# Selection and Value Binding in Syncfusion Blazor DropDown List

## Table of Contents
- [Basic Value Binding](#basic-value-binding)
- [Getting Selected Values](#getting-selected-values)
- [Value Change Events](#value-change-events)
- [Complex Object Selection](#complex-object-selection)
- [Clearing Selection](#clearing-selection)
- [Programmatic Selection](#programmatic-selection)

## Basic Value Binding

### Two-Way Binding with @bind-Value

The simplest approach uses `@bind-Value` for automatic two-way binding:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedValue"
                DataSource="@Items"
                Placeholder="Select item">
</SfDropDownList>

<p>Selected: @SelectedValue</p>

@code {
    private string SelectedValue;
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

### One-Way Binding with Value Property

Use `Value` property for one-way binding (set initial value but don't track changes):

```razor
<SfDropDownList TValue="string" TItem="string" Value="@DefaultValue"
                DataSource="@Items"
                Placeholder="Select item">
</SfDropDownList>

@code {
    private string DefaultValue = "Option B";
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

### Value Binding with Typed Values

Bind numeric or other typed values:

```razor
<SfDropDownList TValue="int" TItem="int" @bind-Value="SelectedId"
                DataSource="@Numbers"
                Placeholder="Select number">
</SfDropDownList>

<p>Selected ID: @SelectedId (Type: @SelectedId.GetType().Name)</p>

@code {
    private int SelectedId;
    private List<int> Numbers = new() { 10, 20, 30, 40, 50 };
}
```

## Getting Selected Values

### Access Selected Value in Code

Access the selected value at any time:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedDepartment"
                DataSource="@Departments"
                Placeholder="Choose department">
</SfDropDownList>

<button @onclick="ShowSelection">Show Selection</button>

@if (!string.IsNullOrEmpty(SelectionMessage))
{
    <p class="alert alert-info">@SelectionMessage</p>
}

@code {
    private string SelectedDepartment;
    private string SelectionMessage;
    private List<string> Departments = new() { "Sales", "Engineering", "Marketing" };

    private void ShowSelection()
    {
        SelectionMessage = string.IsNullOrEmpty(SelectedDepartment)
            ? "No selection made"
            : $"You selected: {SelectedDepartment}";
    }
}
```

### Get Full Selected Object

When binding to complex objects, access the complete object:

```razor
<SfDropDownList TValue="int" TItem="Employee" @bind-Value="SelectedEmployeeId"
                DataSource="@Employees"
                Placeholder="Select employee">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
</SfDropDownList>

@if (SelectedEmployeeId > 0 && SelectedEmployee != null)
{
    <div class="alert alert-info">
        <strong>@SelectedEmployee.Name</strong><br/>
        Department: @SelectedEmployee.Department<br/>
        Email: @SelectedEmployee.Email
    </div>
}

@code {
    private int SelectedEmployeeId;
    private List<Employee> Employees;

    private Employee SelectedEmployee
    {
        get => Employees?.FirstOrDefault(e => e.Id == SelectedEmployeeId);
    }

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice", Department = "Engineering", Email = "alice@company.com" },
            new Employee { Id = 2, Name = "Bob", Department = "Sales", Email = "bob@company.com" },
            new Employee { Id = 3, Name = "Carol", Department = "Marketing", Email = "carol@company.com" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
        public string Email { get; set; }
    }
}
```

## Value Change Events

### Listen to Selection Changes

Use `ValueChange` event to react when the selected value changes:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Categories"
                Placeholder="Select category">
    <DropDownListEvents TValue="string" TItem="string" ValueChange="@OnCategoryChange"></DropDownListEvents>
</SfDropDownList>

@if (!string.IsNullOrEmpty(Message))
{
    <p>@Message</p>
}

@code {
    private string Message;
    private List<string> Categories = new() { "Electronics", "Clothing", "Books" };

    private void OnCategoryChange(ChangeEventArgs<string> args)
    {
        Message = $"You selected: {args.Value}";
        // Perform additional actions based on selection
    }
}
```

### Multiple Event Handlers

Combine `ValueChange` with `@bind-Value` for both automatic tracking and custom logic:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedValue"
                DataSource="@Items"
                Placeholder="Select item">
    <DropDownListEvents TValue="string" TItem="string" ValueChange="@OnValueChange"></DropDownListEvents>
</SfDropDownList>

@code {
    private string SelectedValue;
    private List<string> Items = new() { "Item A", "Item B", "Item C" };

    private void OnValueChange(ChangeEventArgs<string, string> args)
    {
        // Custom logic runs when value changes
        Console.WriteLine($"Value changed to: {args.Value}");
        
        // SelectedValue is automatically updated due to @bind-Value
    }
}
```

### Event Args Details

Access detailed information from the change event:

```razor
<SfDropDownList TValue="int" TItem="Employee" @bind-Value="SelectedId"
                DataSource="@Employees"
                Placeholder="Select employee">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListEvents TValue="int" TItem="Employee" ValueChange="@OnSelectionChanged"></DropDownListEvents>
</SfDropDownList>

@code {
    private int SelectedId;
    private List<Employee> Employees;

    private void OnSelectionChanged(ChangeEventArgs<int> args)
    {
        Console.WriteLine($"New value: {args.Value}");           // The new selected value
        Console.WriteLine($"Item object: {args.ItemData}");      // The selected item
        Console.WriteLine($"IsInteracted: {args.IsInteracted}"); // User action vs programmatic
    }

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
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

## Complex Object Selection

### Selecting Complex Objects

When you need the entire object selected, not just an ID:

```razor
<SfDropDownList TValue="Product" TItem="Product" @bind-Value="SelectedProduct"
                DataSource="@Products"
                Placeholder="Select product">
    <DropDownListFieldSettings Text="@nameof(Product.Name)" Value="@nameof(Product.Name)" />
</SfDropDownList>

@if (SelectedProduct != null)
{
    <div class="alert alert-info">
        <strong>@SelectedProduct.Name</strong><br/>
        Price: $@SelectedProduct.Price
    </div>
}

@code {
    private Product SelectedProduct;
    private List<Product> Products;

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Name = "Laptop", Price = 999.99m },
            new Product { Name = "Mouse", Price = 29.99m },
            new Product { Name = "Keyboard", Price = 79.99m }
        };
    }

    public class Product
    {
        public string Name { get; set; }
        public decimal Price { get; set; }
    }
}
```

## Clearing Selection

### Reset to No Selection

Clear the selected value programmatically:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedValue"
                DataSource="@Items"
                Placeholder="Select item">
</SfDropDownList>

<button @onclick="ClearSelection">Clear Selection</button>

@code {
    private string SelectedValue;
    private List<string> Items = new() { "Option A", "Option B", "Option C" };

    private void ClearSelection()
    {
        SelectedValue = null;  // Reset to no selection
    }
}
```

### Reset with Specific Default

Clear and set to a default value:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedDepartment"
                DataSource="@Departments"
                Placeholder="Select department">
</SfDropDownList>

<button @onclick="ResetToDefault">Reset</button>

@code {
    private string SelectedDepartment;
    private List<string> Departments = new() { "Sales", "Engineering", "Marketing" };

    private void ResetToDefault()
    {
        SelectedDepartment = "Sales";  // Reset to default selection
    }
}
```

## Programmatic Selection

### Set Selection from Code

Change the selected value from C# code:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedOption"
                DataSource="@Options"
                Placeholder="Select option">
</SfDropDownList>

<button @onclick="() => SelectedOption = 'Option B'">Select Option B</button>
<button @onclick="() => SelectedOption = 'Option C'">Select Option C</button>

@code {
    private string SelectedOption;
    private List<string> Options = new() { "Option A", "Option B", "Option C" };
}
```

### Select Based on Logic

Apply selection based on conditions:

```razor
<SfDropDownList TValue="int" TItem="Employee"
                @bind-Value="SelectedEmployeeId"
                DataSource="@Employees"
                Placeholder="Select employee">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
</SfDropDownList>

<button @onclick="SelectManagerAutomatically">Auto-Select Manager</button>

@code {
    private int SelectedEmployeeId;
    private List<Employee> Employees;

    private void SelectManagerAutomatically()
    {
        var manager = Employees.FirstOrDefault(e => e.Role == "Manager");
        if (manager != null)
        {
            SelectedEmployeeId = manager.Id;
        }
    }

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice", Role = "Manager" },
            new Employee { Id = 2, Name = "Bob", Role = "Developer" },
            new Employee { Id = 3, Name = "Carol", Role = "Designer" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Role { get; set; }
    }
}
```

## Complete Selection Example

```razor
@page "/dropdown-selection"

<h3>Selection and Value Binding Example</h3>

<div class="form-group">
    <label>Select Employee</label>
    <SfDropDownList TValue="int" TItem="Employee"
                    @bind-Value="SelectedEmployeeId"
                    DataSource="@Employees"
                    Placeholder="Choose employee">
        <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
        <DropDownListEvents TValue="int" TItem="Employee" ValueChange="@OnEmployeeSelected"></DropDownListEvents>
    </SfDropDownList>
</div>

@if (SelectedEmployeeId > 0)
{
    var employee = Employees.FirstOrDefault(e => e.Id == SelectedEmployeeId);
    @if (employee != null)
    {
        <div class="alert alert-info">
            <h4>Selected Employee</h4>
            <p><strong>Name:</strong> @employee.Name</p>
            <p><strong>Department:</strong> @employee.Department</p>
            <p><strong>Email:</strong> @employee.Email</p>
            <p><strong>Salary:</strong> $@employee.Salary.ToString("F2")</p>
        </div>
    }
}

<div class="mt-3">
    <button @onclick="() => SelectedEmployeeId = 0" class="btn btn-secondary">Clear Selection</button>
    <button @onclick="SelectHighestPaid" class="btn btn-secondary">Select Highest Paid</button>
</div>

@code {
    private int SelectedEmployeeId;
    private List<Employee> Employees;

    private void SelectHighestPaid()
    {
        var highest = Employees.OrderByDescending(e => e.Salary).FirstOrDefault();
        if (highest != null)
        {
            SelectedEmployeeId = highest.Id;
        }
    }

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice Johnson", Department = "Engineering", Email = "alice@company.com", Salary = 95000 },
            new Employee { Id = 2, Name = "Bob Smith", Department = "Sales", Email = "bob@company.com", Salary = 75000 },
            new Employee { Id = 3, Name = "Carol White", Department = "Marketing", Email = "carol@company.com", Salary = 80000 }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
        public string Email { get; set; }
        public decimal Salary { get; set; }
    }
}
```

## Key Takeaways

- Use `@bind-Value` for automatic two-way binding
- Use `Value` property for one-way binding
- Access selected value directly from bound property
- Use `ValueChange` event for custom logic on selection
- Combine `@bind-Value` and `ValueChange` for complete control
- Access full object through lookup/find methods
- Clear selection by setting value to null
- Set selection programmatically from code
- Use event args to get previous value and item details
