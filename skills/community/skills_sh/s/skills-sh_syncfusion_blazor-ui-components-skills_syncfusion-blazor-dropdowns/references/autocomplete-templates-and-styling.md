# Templates & Styling in Syncfusion Blazor AutoComplete

## Table of Contents
- [Item Template](#item-template)
- [Group Template](#group-template)
- [Header Template](#header-template)
- [Footer Template](#footer-template)
- [No Records Template](#no-records-template)
- [Placeholder & FloatLabel](#placeholder--floatlabel)
- [CSS Styling](#css-styling)
- [Appearance Customization](#appearance-customization)

## Item Template

Customize the appearance of each list item using **ItemTemplate**:

### Basic Item Template

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Product" 
                DataSource="@Products">
    <AutoCompleteFieldSettings Value="ProductName">
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Product">
        <ItemTemplate>
            <div style="padding: 8px;">
                @((context as Product)?.ProductName)
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
    }

    private List<Product> Products = new();
}
```

### Rich Item Display

Combine text, icons, and styling:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees">
    <AutoCompleteFieldSettings Value="EmployeeName" >
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Employee">
        <ItemTemplate>
            <div style="display: flex; gap: 10px; padding: 8px; align-items: center;">
                <div style="width: 32px; height: 32px; 
                            background: #007bff; 
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;">
                    @((context as Employee)?.EmployeeName[0])
                </div>
                <div>
                    <div style="font-weight: bold;">@((context as Employee)?.EmployeeName)</div>
                    <div style="font-size: 0.85em; color: #666;">@((context as Employee)?.Department)</div>
                </div>
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
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
        new Employee { EmployeeId = 2, EmployeeName = "Jane Doe", Department = "HR" }
    };
}
```

### Item with Status Indicator

```blazor
<SfAutoComplete TValue="string" TItem="Task" 
                DataSource="@Tasks">
    <AutoCompleteFieldSettings Value="TaskName" >
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Task">
        <ItemTemplate>
            <div style="display: flex; justify-content: space-between;">
                <span>@((context as Task)?.TaskName)</span>
                <span style="@GetStatusStyle((context as Task)?.Status)">
                    @((context as Task)?.Status)
                </span>
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    public class Task
    {
        public int TaskId { get; set; }
        public string TaskName { get; set; }
        public string Status { get; set; }
    }

    private List<Task> Tasks = new()
    {
        new Task { TaskId = 1, TaskName = "Design UI", Status = "Done" },
        new Task { TaskId = 2, TaskName = "Implement API", Status = "In Progress" }
    };

    private string GetStatusStyle(string status)
    {
        return status switch
        {
            "Done" => "background: #28a745; color: white; padding: 2px 6px; border-radius: 3px;",
            "In Progress" => "background: #ffc107; color: black; padding: 2px 6px; border-radius: 3px;",
            _ => "background: #dc3545; color: white; padding: 2px 6px; border-radius: 3px;"
        };
    }
}
```

## Group Template

Customize the group header appearance using **GroupTemplate**:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees">
    <AutoCompleteFieldSettings Value="EmployeeName" GroupBy="Department">
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Employee">
        <GroupTemplate>
            <div style="padding: 8px; background: #f8f9fa; 
                        font-weight: bold; border-bottom: 1px solid #dee2e6;">
                <span style="color: #007bff;">📁 </span>
                @((context as CompositeData)?.GroupData?.Key)
            </div>
        </GroupTemplate>
        <ItemTemplate>
            <div style="padding-left: 20px;">
                @((context as Employee)?.EmployeeName)
            </div>
        </ItemTemplate>
    </AutoCompleteTemplates>
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
        new Employee { EmployeeId = 3, EmployeeName = "Bob Wilson", Department = "HR" }
    };
}
```

## Header Template

Add a fixed header above the suggestion list:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
    <AutoCompleteTemplates TItem="string">
        <HeaderTemplate>
            <div style="padding: 10px; background: #007bff; color: white; font-weight: bold;">
                Available Countries
            </div>
        </HeaderTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    private List<string> Countries = new()
    {
        "Austria", "Brazil", "Canada", "Denmark", "Egypt"
    };
}
```

### Header for Column Titles

Use HeaderTemplate with multicolumn display:

```blazor
<SfAutoComplete TValue="string" TItem="Product" 
                DataSource="@Products">
    <AutoCompleteFieldSettings Value="ProductName" >
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Product">
        <HeaderTemplate>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px;
                        padding: 10px; background: #f5f5f5; font-weight: bold;">
                <span>Product</span>
                <span>Category</span>
                <span style="text-align: right;">Price</span>
            </div>
        </HeaderTemplate>
        <ItemTemplate>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px;">
                <span>@((context as Product)?.ProductName)</span>
                <span>@((context as Product)?.Category)</span>
                <span style="text-align: right;">$@((context as Product)?.Price)</span>
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
        new Product { ProductId = 2, ProductName = "Mouse", Category = "Electronics", Price = 29 }
    };
}
```

## Footer Template

Add a fixed footer at the bottom of the suggestion list:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
    <AutoCompleteTemplates TItem="string">
        <FooterTemplate>
            <div style="padding: 10px; background: #f5f5f5; text-align: center; 
                        color: #666; font-size: 0.85em;">
                Total: @Countries.Count items
            </div>
        </FooterTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    private List<string> Countries = new()
    {
        "Austria", "Brazil", "Canada", "Denmark", "Egypt"
    };
}
```

## No Records Template

Customize the message shown when no data matches the search:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true">
    <AutoCompleteTemplates TItem="string">
        <NoRecordsTemplate>
            <div style="padding: 20px; text-align: center; color: #999;">
                <p>😕 No countries found</p>
                <p style="font-size: 0.85em;">Try a different search term</p>
            </div>
        </NoRecordsTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

## Placeholder & FloatLabel

### Placeholder Text

Add hint text to the input field:

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                Placeholder="Type a country name...">
</SfAutoComplete>
```

### Floating Label

Display label that floats above the input when focused or filled:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                FloatLabelType="FloatLabelType.Auto"
                Placeholder="Country">
</SfAutoComplete>

@code {
    private List<string> Countries = new()
    {
        "Austria", "Brazil", "Canada"
    };
}
```

**FloatLabelType Options:**
- `Auto` - Label floats on focus or when value exists
- `Always` - Label always floats above
- `Never` - No floating label

### Custom Placeholder Style

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                Placeholder="Select a country..."
                FloatLabelType="FloatLabelType.Auto">
</SfAutoComplete>

<style>
    .e-autocomplete .e-input::placeholder {
        color: #999;
        font-style: italic;
    }
</style>
```

## CSS Styling

### Apply Custom CSS Classes

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                CssClass="my-autocomplete">
</SfAutoComplete>

<style>
    .my-autocomplete.e-autocomplete .e-input {
        border: 2px solid #007bff;
        border-radius: 8px;
        padding: 10px;
        font-size: 1.1em;
    }

    .my-autocomplete.e-autocomplete .e-list-item {
        padding: 12px;
        border-bottom: 1px solid #eee;
    }

    .my-autocomplete.e-autocomplete .e-list-item:hover {
        background: #e7f3ff;
    }
</style>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

### Styling Dropdown Appearance

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                CssClass="custom-dropdown">
</SfAutoComplete>

<style>
    /* Input field styling */
    .custom-dropdown.e-autocomplete .e-input {
        background: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    /* Dropdown popup styling */
    .custom-dropdown.e-autocomplete .e-popup .e-list-parent {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* List item styling */
    .custom-dropdown.e-autocomplete .e-list-item {
        padding: 8px 12px;
        line-height: 1.5;
    }

    /* Selected item */
    .custom-dropdown.e-autocomplete .e-list-item.e-item-focus {
        background: #007bff;
        color: white;
    }
</style>
```

## Appearance Customization

### Dark Mode

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                CssClass="dark-mode">
</SfAutoComplete>

<style>
    .dark-mode.e-autocomplete .e-input {
        background: #333;
        color: #fff;
        border: 1px solid #555;
    }

    .dark-mode.e-autocomplete .e-popup .e-list-parent {
        background: #333;
        color: #fff;
    }

    .dark-mode.e-autocomplete .e-list-item {
        color: #fff;
        border-color: #555;
    }

    .dark-mode.e-autocomplete .e-list-item.e-item-focus {
        background: #555;
    }
</style>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

### Compact Size

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                CssClass="compact">
</SfAutoComplete>

<style>
    .compact.e-autocomplete .e-input {
        padding: 4px 8px;
        font-size: 0.9em;
        height: 32px;
    }

    .compact.e-autocomplete .e-list-item {
        padding: 4px 8px;
        font-size: 0.9em;
        line-height: 1.4;
    }
</style>
```

### Outlined Style

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                CssClass="outlined">
</SfAutoComplete>

<style>
    .outlined.e-autocomplete .e-input {
        border: 2px solid #007bff;
        border-radius: 8px;
        padding: 12px;
        background: transparent;
    }

    .outlined.e-autocomplete .e-input:focus {
        border-color: #0056b3;
        box-shadow: 0 0 0 3px rgba(0,123,255,0.25);
    }
</style>
```

## Best Practices

1. **Keep Templates Lean:** Complex templates may impact performance
2. **Use Consistent Styling:** Maintain design consistency across items
3. **Ensure Accessibility:** Ensure templates work with screen readers
4. **Test with Long Data:** Verify templates display correctly with long text
5. **Mobile-Friendly:** Design templates that work on small screens

## Related Topics

- [Data Organization](data-organization.md)
- [Advanced Features](advanced-features.md)
- [Accessibility & Best Practices](accessibility-and-best-practices.md)
