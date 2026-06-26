# Data Binding in Syncfusion Blazor DropDown List

## Table of Contents
- [Binding Local Data](#binding-local-data)
- [Primitive Types](#primitive-types)
- [Complex Data Types](#complex-data-types)
- [Collections and Observables](#collections-and-observables)
- [Remote Data Binding](#remote-data-binding)
- [Events and Lifecycle](#events-and-lifecycle)

## Binding Local Data

### Primitive Types (Strings and Numbers)

The simplest data binding uses primitive types directly:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items" Placeholder="Select option">
    <DropDownListEvents TValue="string" TItem="string"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<string> Items = new()
    {
        "Option A",
        "Option B",
        "Option C"
    };
}
```

Numeric values work the same way:

```razor
<SfDropDownList TValue="int" TItem="int" DataSource="@Numbers" @bind-Value="SelectedNumber">
    <DropDownListEvents TValue="int" TItem="int"></DropDownListEvents>
</SfDropDownList>

@code {
    private int SelectedNumber;
    private List<int> Numbers = new() { 10, 20, 30, 40 };
}
```

### Complex Data Types

When binding objects, use `DropDownListFieldSettings` to specify which properties to display and use as values:

```razor
<SfDropDownList TValue="int" TItem="Department" DataSource="@Departments"
                @bind-Value="SelectedDeptId"
                Placeholder="Select department">
    <DropDownListFieldSettings Text="@nameof(Department.DeptName)" Value="@nameof(Department.DeptId)" />
    <DropDownListEvents TValue="int" TItem="Department"></DropDownListEvents>
</SfDropDownList>

@code {
    private int SelectedDeptId;
    private List<Department> Departments;

    protected override void OnInitialized()
    {
        Departments = new List<Department>
        {
            new Department { DeptId = 1, DeptName = "Engineering", Manager = "John" },
            new Department { DeptId = 2, DeptName = "Sales", Manager = "Jane" },
            new Department { DeptId = 3, DeptName = "HR", Manager = "Bob" }
        };
    }

    public class Department
    {
        public int DeptId { get; set; }
        public string DeptName { get; set; }
        public string Manager { get; set; }
    }
}
```

### Expando Object Binding

Bind to dynamic objects using `ExpandoObject`:

```razor
<SfDropDownList TValue="int" TItem="dynamic" DataSource="@DynamicData"
                Placeholder="Select item">
    <DropDownListFieldSettings Text="Name" Value="Id" />
    <DropDownListEvents TValue="int" TItem="dynamic"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<dynamic> DynamicData;

    protected override void OnInitialized()
    {
        DynamicData = new List<ExpandoObject>();
        
        dynamic item1 = new ExpandoObject();
        item1.Id = 1;
        item1.Name = "Item One";
        
        dynamic item2 = new ExpandoObject();
        item2.Id = 2;
        item2.Name = "Item Two";
        
        DynamicData.Add((ExpandoObject)item1);
        DynamicData.Add((ExpandoObject)item2);
    }
}
```

### Observable Collection Binding

Use `ObservableCollection` for real-time updates when the collection changes:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items" Placeholder="Select item">
    <DropDownListEvents TValue="string" TItem="string"></DropDownListEvents>
</SfDropDownList>

<button @onclick="AddItem">Add New Item</button>

@code {
    private ObservableCollection<string> Items;

    protected override void OnInitialized()
    {
        Items = new ObservableCollection<string> { "Item 1", "Item 2" };
    }

    private void AddItem()
    {
        Items.Add($"Item {Items.Count + 1}");
        // Dropdown automatically updates
    }
}
```

### Dynamic Object Binding

Bind to objects created at runtime:

```razor
<SfDropDownList TValue="int" TItem="dynamic" DataSource="@Products"
                Placeholder="Select product">
    <DropDownListFieldSettings Text="ProductName" Value="ProductId" />
    <DropDownListEvents TValue="int" TItem="dynamic"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<dynamic> Products;

    protected override void OnInitialized()
    {
        Products = new List<dynamic>
        {
            new { ProductId = 1, ProductName = "Laptop", Price = 999.99 },
            new { ProductId = 2, ProductName = "Mouse", Price = 29.99 },
            new { ProductId = 3, ProductName = "Keyboard", Price = 79.99 }
        };
    }
}
```

### Enum Data Binding

Use enums directly as data sources:

```razor
<SfDropDownList TValue="Status" TItem="Status"
                DataSource="@(Enum.GetValues(typeof(Status)).Cast<Status>())"
                @bind-Value="SelectedStatus"
                Placeholder="Select status">
</SfDropDownList>

@code {
    private Status SelectedStatus;

    public enum Status
    {
        Pending,
        Active,
        Completed,
        Archived
    }
}
```

### ValueTuple Data Binding

Bind to tuples for lightweight key-value pairs:

```razor
<SfDropDownList TValue="int" TItem="(int, string)"
                DataSource="@Statuses" Placeholder="Select status">
    <DropDownListFieldSettings Text="Status" Value="Id" />
</SfDropDownList>

@code {
    private List<(int Id, string Status)> Statuses;

    protected override void OnInitialized()
    {
        Statuses = new List<(int, string)>
        {
            (1, "Open"),
            (2, "In Progress"),
            (3, "Closed")
        };
    }
}
```

## Remote Data Binding

### Web API Integration

Bind to data from a REST API endpoint:

```razor
<SfDropDownList TValue="int" TItem="Employee"
                DataSource="@RemoteEmployees"
                Placeholder="Select employee">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListEvents TValue="int" TItem="Employee" OnActionBegin="@OnActionBegin" OnActionComplete="@OnActionComplete"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Employee> RemoteEmployees;

    private void OnActionBegin(ActionBeginEventArgs args)
    {
        // Called before data fetch
        Console.WriteLine("Fetching data...");
    }

    private async Task OnActionComplete(ActionCompleteEventArgs<Employee> args)
    {
        // Called after successful data fetch
        RemoteEmployees = args.Result?.ToList();
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

### OData Service Binding

Connect to OData services for enterprise data integration:

```razor
<SfDropDownList TValue="int" TItem="dynamic"
                DataSource="@ODataSource"
                Placeholder="Select customer">
    <DropDownListFieldSettings Text="CustomerName" Value="CustomerID" />
</SfDropDownList>

@code {
    private SfDataManager DataManager;

    protected override void OnInitialized()
    {
        DataManager = new SfDataManager
        {
            Url = "YOUR_ODATA_SERVICE_URL",
            Adaptor = Syncfusion.Blazor.Adaptors.AdaptorType.ODataV4Adaptor,
            CrossDomain = true
        };
    }

    public SfDataManager ODataSource
    {
        get { return DataManager; }
    }
}
```

### Custom Adaptor

Implement custom data fetch logic:

```razor
<SfDropDownList TValue="int" TItem="dynamic"
                DataSource="@CustomDataManager"
                Placeholder="Select item">
    <DropDownListFieldSettings Text="Name" Value="Id" />
</SfDropDownList>

@code {
    private SfDataManager CustomDataManager;

    protected override void OnInitialized()
    {
        CustomDataManager = new SfDataManager
        {
            Url = "api/items",
            Adaptor = Syncfusion.Blazor.Adaptors.AdaptorType.UrlAdaptor
        };
    }
}
```

### Async Data Fetch with HttpClient

Manually fetch data using HttpClient:

```razor
<SfDropDownList TValue="int" TItem="Item"
                DataSource="@Items"
                Placeholder="Select item">
    <DropDownListFieldSettings Text="@nameof(Item.ItemName)" Value="@nameof(Item.ItemId)" />
</SfDropDownList>

@if (Loading)
{
    <p>Loading...</p>
}

@code {
    @inject HttpClient HttpClient

    private List<Item> Items;
    private bool Loading = true;

    protected override async Task OnInitializedAsync()
    {
        try
        {
            Items = await HttpClient.GetFromJsonAsync<List<Item>>("api/items");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
        finally
        {
            Loading = false;
        }
    }

    public class Item
    {
        public int ItemId { get; set; }
        public string ItemName { get; set; }
    }
}
```

## Events and Lifecycle

### OnActionBegin Event

Triggered before data fetch begins (useful for loading states):

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items">
    <DropDownListEvents TValue="string" TItem="string" OnActionBegin="@HandleActionBegin"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<string> Items;
    
    private void HandleActionBegin(ActionBeginEventArgs args)
    {
        Console.WriteLine($"Action started: {args.ActionName}");
        // Show loading indicator
    }
}
```

### OnActionComplete Event

Triggered after successful data fetch:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Items">
    <DropDownListEvents TValue="int" TItem="Employee" OnActionComplete="@HandleActionComplete"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<Employee> Items;
    
    private void HandleActionComplete(ActionCompleteEventArgs<Employee> args)
    {
        Console.WriteLine($"Data loaded: {args.Result.Count()} items");
        Items = args.Result.ToList();
    }
}
```

### OnActionFailure Event

Handle errors when data fetch fails:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items">
    <DropDownListEvents TValue="string" TItem="string" OnActionFailure="@HandleActionFailure"></DropDownListEvents>
</SfDropDownList>

@code {
    private List<string> Items;
    private string ErrorMessage;
    
    private void HandleActionFailure(ActionFailureEventArgs args)
    {
        ErrorMessage = $"Error loading data: {args.Error}";
        Console.WriteLine(ErrorMessage);
    }
}
```

## Complete Data Binding Example

```razor
@page "/dropdown-data-binding"

<h3>Data Binding Example</h3>

<div class="form-group">
    <label>Select an Employee</label>
    <SfDropDownList TValue="int" TItem="Employee"
                    @bind-Value="SelectedEmployeeId"
                    DataSource="@Employees"
                    Placeholder="Choose employee">
        <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
        <DropDownListEvents TValue="int" TItem="Employee" OnActionBegin="@OnActionBegin" OnActionComplete="@OnActionComplete" OnActionFailure="@OnActionFailure"></DropDownListEvents>
    </SfDropDownList>
</div>

@if (Loading)
{
    <p class="text-info">Loading employees...</p>
}

@if (!string.IsNullOrEmpty(ErrorMessage))
{
    <p class="text-danger">@ErrorMessage</p>
}

@if (SelectedEmployeeId > 0 && !Loading)
{
    var employee = Employees?.FirstOrDefault(e => e.Id == SelectedEmployeeId);
    @if (employee != null)
    {
        <div class="alert alert-info">
            Selected: @employee.Name (@employee.Department)
        </div>
    }
}

@code {
    private int SelectedEmployeeId;
    private List<Employee> Employees;
    private bool Loading;
    private string ErrorMessage;

    protected override async Task OnInitializedAsync()
    {
        await LoadEmployees();
    }

    private async Task LoadEmployees()
    {
        Loading = true;
        try
        {
            // Simulate async API call
            await Task.Delay(500);
            
            Employees = new List<Employee>
            {
                new Employee { Id = 1, Name = "Alice Johnson", Department = "Engineering" },
                new Employee { Id = 2, Name = "Bob Smith", Department = "Sales" },
                new Employee { Id = 3, Name = "Carol White", Department = "Marketing" }
            };
        }
        catch (Exception ex)
        {
            ErrorMessage = ex.Message;
        }
        finally
        {
            Loading = false;
        }
    }

    private void OnActionBegin(ActionBeginEventArgs args)
    {
        Console.WriteLine("Data fetch starting");
    }

    private void OnActionComplete(ActionCompleteEventArgs<Employee> args)
    {
        Console.WriteLine("Data fetch completed");
    }

    private void OnActionFailure(ActionFailureEventArgs args)
    {
        ErrorMessage = $"Error: {args.Error}";
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

## Key Takeaways

- Use primitive types for simple lists
- Use field mapping for complex objects
- Use remote data binding for large datasets
- Handle action events for loading states and errors
- Use appropriate collection types (List, ObservableCollection, etc.)
- Always provide error handling for async operations
