# Data Organization in Syncfusion Blazor AutoComplete

## Grouping Data

Organize list items into categories using **AllowGrouping** and the **GroupBy** field:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees"
                Placeholder="Select an employee">
    <AutoCompleteFieldSettings Value="EmployeeName"  GroupBy="Department"></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, EmployeeName = "John Smith", Department = "IT" },
        new Employee { EmployeeId = 2, EmployeeName = "Jane Doe", Department = "IT" },
        new Employee { EmployeeId = 3, EmployeeName = "Bob Wilson", Department = "HR" },
        new Employee { EmployeeId = 4, EmployeeName = "Alice Brown", Department = "HR" }
    };
}
```

**Result:** Employees are grouped by Department (IT, HR), with group headers shown in the dropdown.

### Customizing Group Headers

Use **GroupTemplate** to create custom group header displays:

```blazor
<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees">
    <AutoCompleteFieldSettings Value="EmployeeName" GroupBy="Department"></AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Employee">
        <GroupTemplate>
            <div style="padding: 10px; background: #f0f0f0; font-weight: bold;">
                @((context as CompositeData)?.GroupData?.Key)
            </div>
        </GroupTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>
```

## Sorting Options

Control the order of list items using **SortOrder**:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                SortOrder="SortOrder.Ascending"
                Placeholder="Select a country">
</SfAutoComplete>

@code {
    private List<string> Countries = new() 
    { 
        "Brazil", "Austria", "Canada", "Denmark", "Egypt" 
    };
}
```

**SortOrder Options:**
- `Ascending` - Alphabetical A-Z
- `Descending` - Reverse Z-A
- `None` - Original order (default)

### Sorting Complex Objects

Sorting applies to the display field (Text):

```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                DataSource="@Products"
                SortOrder="SortOrder.Ascending">
    <AutoCompleteFieldSettings Value="ProductName" ></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
    }

    private List<Product> Products = new()
    {
        new Product { ProductId = 1, ProductName = "Zebra" },
        new Product { ProductId = 2, ProductName = "Apple" },
        new Product { ProductId = 3, ProductName = "Mango" }
    };
}
```

**Result:** Display order is Apple, Mango, Zebra (sorted by ProductName).

## Multicolumn Display

Display multiple columns of data in the dropdown using **ItemTemplate**:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Product" 
                DataSource="@Products"
                Placeholder="Search products">
    <AutoCompleteFieldSettings Value="ProductName"></AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Product">
        <ItemTemplate>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                <span>@((context as Product)?.ProductName)</span>
                <span>@((context as Product)?.Category)</span>
                <span style="text-align: right;">@((context as Product)?.Price)</span>
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public string Category { get; set; }
        public decimal Price { get; set; }
    }

    private List<Product> Products = new()
    {
        new Product { ProductId = 1, ProductName = "Laptop", Category = "Electronics", Price = 999 },
        new Product { ProductId = 2, ProductName = "Mouse", Category = "Electronics", Price = 29 },
        new Product { ProductId = 3, ProductName = "Desk", Category = "Furniture", Price = 199 }
    };
}
```

**Result:** Each dropdown item shows three columns: Name, Category, Price.

### Header Template for Multicolumn

Add column headers to multicolumn displays:

```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                DataSource="@Products">
    <AutoCompleteFieldSettings Value="ProductName" 
                               Text="ProductName">
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Product">
        <HeaderTemplate>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; 
                        padding: 10px; background: #f5f5f5; font-weight: bold;">
                <span>Product</span>
                <span>Category</span>
                <span style="text-align: right;">Price</span>
            </div>
        </HeaderTemplate>
        <ItemTemplate>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                <span>@((context as Product)?.ProductName)</span>
                <span>@((context as Product)?.Category)</span>
                <span style="text-align: right;">@((context as Product)?.Price)</span>
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>
```

## Selection Modes

Control how users interact with list items.

### Standard Selection

Single item selection (default):

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                Placeholder="Select a country">
</SfAutoComplete>
```

### Read-Only Selection

Prevent manual input, force selection from list:

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="false">
</SfAutoComplete>
```

### Custom Value Entry

Allow users to enter values not in the list:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowCustom="true"
                Placeholder="Select or type a country">
</SfAutoComplete>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

**Behavior:** User can type "France" even if it's not in the list. The custom value is retained.

### Selection Event

React to user selections:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
    <AutoCompleteEvents TValue="string" TItem="string"
                        ValueChange="@OnSelectionChange">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>Selected: @SelectedCountry</p>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
    
    private string SelectedCountry = "";

    private void OnSelectionChange(ChangeEventArgs<string, string> args)
    {
        SelectedCountry = args.Value;
        Console.WriteLine($"User selected: {args.Value}");
    }
}
```

## Value Binding

Bind the selected value to a component property:

### Two-Way Binding

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                @bind-Value="SelectedCountry"
                Placeholder="Select a country">
</SfAutoComplete>

<p>You selected: @SelectedCountry</p>

@code {
    private string SelectedCountry = "";
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

**Behavior:** Changing the AutoComplete updates `SelectedCountry`, and setting `SelectedCountry` in code updates the AutoComplete.

### Value with Objects

For object types, the value is typically the ID or unique identifier:

```blazor
<SfAutoComplete TValue="int" TItem="Employee" 
                DataSource="@Employees"
                @bind-Value="SelectedEmployeeId">
    <AutoCompleteFieldSettings Value="EmployeeId" 
                               Text="EmployeeName">
    </AutoCompleteFieldSettings>
</SfAutoComplete>

<p>Selected Employee ID: @SelectedEmployeeId</p>

@code {
    private int SelectedEmployeeId = 0;

    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, EmployeeName = "John Smith" },
        new Employee { EmployeeId = 2, EmployeeName = "Jane Doe" }
    };
}
```

## Combined Example

Combining grouping, sorting, multicolumn display, and selection:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="int" TItem="Employee" 
                DataSource="@Employees"
                AllowFiltering="true"
                SortOrder="SortOrder.Ascending"
                @bind-Value="SelectedEmployeeId">
    <AutoCompleteFieldSettings Value="EmployeeId" 
                               Text="EmployeeName"
                               GroupBy="Department">
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Employee">
        <HeaderTemplate>
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px; 
                        padding: 10px; background: #f5f5f5; font-weight: bold;">
                <span>Name</span>
                <span>Dept</span>
            </div>
        </HeaderTemplate>
        <ItemTemplate>
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px;">
                <span>@((context as Employee)?.EmployeeName)</span>
                <span>@((context as Employee)?.Department)</span>
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
    <AutoCompleteEvents TValue="int" TItem="Employee"
                        ValueChange="@OnSelectionChange">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>Selected ID: @SelectedEmployeeId</p>

@code {
    private int SelectedEmployeeId = 0;

    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, EmployeeName = "Alice Brown", Department = "IT" },
        new Employee { EmployeeId = 2, EmployeeName = "Bob Johnson", Department = "IT" },
        new Employee { EmployeeId = 3, EmployeeName = "Charlie Davis", Department = "HR" },
        new Employee { EmployeeId = 4, EmployeeName = "Diana Evans", Department = "HR" }
    };

    private void OnSelectionChange(ChangeEventArgs<int, Employee> args)
    {
        Console.WriteLine($"Selected Employee ID: {args.Value}");
    }
}
```

## Related Topics

- [Data Binding](data-binding.md)
- [Filtering & Search](filtering-and-search.md)
- [Templates & Styling](templates-and-styling.md)
