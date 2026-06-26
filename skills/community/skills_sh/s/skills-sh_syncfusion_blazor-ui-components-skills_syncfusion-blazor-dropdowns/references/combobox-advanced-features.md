# Advanced Features in ComboBox

## Table of Contents

- [Grouping](#grouping)
- [Sorting](#sorting)
- [Virtualization](#virtualization)
- [Disabled Items](#disabled-items)
- [RTL Support](#rtl-support)
- [Accessibility](#accessibility)
- [Keyboard Navigation](#keyboard-navigation)

---

## Grouping

Group ComboBox items by category:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId" GroupBy="Department"></ComboBoxFieldSettings>
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
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Department = "IT" },
        new Employee { EmployeeId = 4, Name = "Sarah Lee", Department = "HR" }
    };
}
```

**Result:**
```
IT
  John Smith
  Bob Johnson
HR
  Jane Doe
  Sarah Lee
```

### Grouped with Custom Group Template

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId" GroupBy="Department"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Employee">
        <GroupTemplate>
            <div style="padding: 10px; background-color: #f0f0f0; font-weight: bold;">
                📁 @context.Department (@GetDepartmentCount(context.Department) employees)
            </div>
        </GroupTemplate>
        <ItemTemplate>
            <div style="padding: 8px; padding-left: 20px;">👤 @context.Name</div>
        </ItemTemplate>
    </ComboBoxTemplates>
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
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Department = "IT" }
    };

    private int GetDepartmentCount(string department)
    {
        return Employees.Count(e => e.Department == department);
    }
}
```

---

## Sorting

Sort ComboBox data by a specific property:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country (sorted A-Z)"
    DataSource="@Countries"
    SortOrder="@SortOrder.Ascending">
    <ComboBoxFieldSettings Text="Name" Value="Code" SortBy="Name"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "Canada", Code = "CA" },
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "Mexico", Code = "MX" }
    };
}
```

**SortOrder Options:**
- **Ascending** - A → Z, 0 → 9
- **Descending** - Z → A, 9 → 0
- **None** - Original order

### Multiple Property Sorting

For complex sorting, manipulate data before binding:

```razor
<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@SortedEmployees">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> AllEmployees = new()
    {
        new Employee { EmployeeId = 3, Name = "Charlie Brown", Department = "HR" },
        new Employee { EmployeeId = 1, Name = "Alice Johnson", Department = "IT" },
        new Employee { EmployeeId = 2, Name = "Bob Smith", Department = "IT" }
    };

    private List<Employee> SortedEmployees => 
        AllEmployees
            .OrderBy(e => e.Department)
            .ThenBy(e => e.Name)
            .ToList();
}
```

---

## Virtualization

Handle large datasets efficiently using virtualization:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Item" TValue="int"
    Placeholder="Search items (1000+)"
    DataSource="@Items"
    AllowFiltering="true"
    EnableVirtualization="true">
    <ComboBoxFieldSettings Text="ItemName" Value="ItemId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Item
    {
        public int ItemId { get; set; }
        public string ItemName { get; set; }
    }

    private List<Item> Items = new();

    protected override void OnInitialized()
    {
        // Generate large dataset
        Items = Enumerable.Range(1, 2000)
            .Select(i => new Item 
            { 
                ItemId = i, 
                ItemName = $"Item {i}" 
            })
            .ToList();
    }
}
```

**When to Use Virtualization:**
- 1000+ items in the list
- Performance issues with large datasets
- Remote data with pagination

**EnableVirtualization:** true/false 

---

## Disabled Items

Prevent certain items from being selected:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
    <ComboBoxEvents TItem="Employee" TValue="int"
        OnValueSelect="@OnValueSelect"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Status { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith", Status = "Active" },
        new Employee { EmployeeId = 2, Name = "Jane Doe", Status = "Inactive" },
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Status = "Active" }
    };

    private void OnValueSelect(SelectEventArgs<Employee> args)
    {
        // Prevent selection of inactive employees
        if (args.ItemData.Status == "Inactive")
        {
            args.Cancel = true;
            Console.WriteLine($"{args.ItemData.Name} is inactive and cannot be selected");
        }
    }
}
```

### Visual Indicator for Disabled Items

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
    <ComboBoxEvents TItem="Employee" TValue="int"
        OnValueSelect="@OnValueSelect"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Employee">
        <ItemTemplate>
            <div style="@GetItemStyle(context)">
                @context.Name
                @if (context.Status == "Inactive")
                {
                    <span style="margin-left: 10px; color: #999;">(Inactive)</span>
                }
            </div>
        </ItemTemplate>
    </ComboBoxTemplates>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Status { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith", Status = "Active" },
        new Employee { EmployeeId = 2, Name = "Jane Doe", Status = "Inactive" },
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Status = "Active" }
    };

    private string GetItemStyle(Employee employee)
    {
        if (employee.Status == "Inactive")
        {
            return "opacity: 0.6; color: #999; pointer-events: none;";
        }
        return "";
    }

    private void OnValueSelect(SelectEventArgs<Employee> args)
    {
        if (args.ItemData.Status == "Inactive")
        {
            args.Cancel = true;
        }
    }
}
```

---

## RTL Support

Support right-to-left languages:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="اختر عنصرا"
    DataSource="@Items"
    EnableRtl="true">
</SfComboBox>

@code {
    private List<string> Items = new() 
    { 
        "عنصر ١", "عنصر ٢", "عنصر ٣" 
    };
}
```

**To enable RTL globally:**

```html
<!-- Add to _Host.cshtml or app head -->
<html dir="rtl" lang="ar">
```

**Affects:**
- Text direction (right to left)
- Popup alignment
- Icon positioning
- Scroll direction

---

## Accessibility

Ensure ComboBox meets WCAG standards:

```razor
@using Syncfusion.Blazor.DropDowns

<div class="form-group">
    <label for="country-combo" id="country-label">
        Select Your Country:
    </label>
    <SfComboBox TItem="Country" TValue="string"
        ID="country-combo"
        AriaLabelledBy="country-label"
        Placeholder="Choose a country"
        DataSource="@Countries"
        AllowFiltering="true">
        <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

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
        new Country { Name = "Canada", Code = "CA" }
    };
}
```

**Accessibility Features:**
- ARIA attributes (aria-label, aria-labelledby)
- Keyboard navigation (Tab, Enter, Arrow keys)
- Screen reader support
- High contrast mode support
- Focus indicators

---

## Keyboard Navigation

ComboBox supports full keyboard interaction:

| Key | Action |
|-----|--------|
| `Tab` | Focus/blur ComboBox |
| `Enter` | Select focused item |
| `Up Arrow` | Move to previous item |
| `Down Arrow` | Move to next item |
| `Home` | Move to first item |
| `End` | Move to last item |
| `Esc` | Close popup |
| `Alt + Down` | Open popup |
| `Alt + Up` | Close popup |

```razor
@using Syncfusion.Blazor.DropDowns

<p>Keyboard Navigation:</p>
<ul>
    <li>Press Down Arrow to open and navigate</li>
    <li>Press Enter to select</li>
    <li>Press Esc to close</li>
</ul>

<SfComboBox TItem="string" TValue="string"
    Placeholder="Use keyboard to navigate"
    DataSource="@Items">
</SfComboBox>

@code {
    private List<string> Items = new() 
    { 
        "Item1", "Item2", "Item3", "Item4", "Item5" 
    };
}
```

---

## Best Practices

1. **Virtualization for Large Lists**
   - Enable for 1000+ items
   - Improves performance

2. **Group Related Items**
   - Better UX
   - Easier to find items
   - Organize by category

3. **Sort Consistently**
   - Alphabetical (most common)
   - By frequency
   - By relevance

4. **Accessibility First**
   - Use labels and ARIA attributes
   - Support keyboard navigation
   - Test with screen readers

5. **Handle Disabled States Clearly**
   - Visual feedback
   - Prevent selection
   - Explain why disabled

---

*See also: [Data Binding](data-binding.md), [Getting Started](getting-started.md), [Templates & Customization](templates-and-customization.md)*
