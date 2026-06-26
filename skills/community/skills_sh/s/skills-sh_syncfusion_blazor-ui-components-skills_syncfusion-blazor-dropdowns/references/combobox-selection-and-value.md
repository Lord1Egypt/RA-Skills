# Selection & Value Binding in ComboBox

## Table of Contents

- [Get Selected Value](#get-selected-value)
- [Get Selected Item Data](#get-selected-item-data)
- [Value Binding](#value-binding)
- [Index Binding](#index-binding)
- [Preselected Values](#preselected-values)
- [Programmatic Selection](#programmatic-selection)
- [Selection Events](#selection-events)
- [Autofill Functionality](#autofill-functionality)
- [Read-Only Selection](#read-only-selection)

---

## Get Selected Value

Retrieve the selected value using the `ValueChange` event or by reading the bound value property:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries"
    @bind-Value="@SelectedValue">
    <ComboBoxEvents TItem="Country" TValue="string"
        ValueChange="@OnValueChange"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

<p>Selected Value: @SelectedValue</p>

@code {
    private string SelectedValue = "USA";

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

    private void OnValueChange(ChangeEventArgs<string, Country> args)
    {
        // args.Value contains the new selected value
        Console.WriteLine($"Selected: {args.Value}");
    }
}
```

---

## Get Selected Item Data

Get the complete data object (not just the value) using the `ItemData` property:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees"
    @bind-Value="@SelectedEmployeeId">
    <ComboBoxEvents TItem="Employee" TValue="int"
        ValueChange="@OnValueChange"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

<div style="margin-top: 20px;">
    @if (SelectedEmployee != null)
    {
        <p><strong>Name:</strong> @SelectedEmployee.Name</p>
        <p><strong>Department:</strong> @SelectedEmployee.Department</p>
        <p><strong>Salary:</strong> $@SelectedEmployee.Salary</p>
    }
</div>

@code {
    private int SelectedEmployeeId = 0;
    private Employee SelectedEmployee;

    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
        public decimal Salary { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith", Department = "IT", Salary = 75000 },
        new Employee { EmployeeId = 2, Name = "Jane Doe", Department = "HR", Salary = 65000 }
    };

    private void OnValueChange(ChangeEventArgs<int, Employee> args)
    {
        // Get the full item data
        SelectedEmployee = args.ItemData;
    }
}
```

---

## Value Binding

### Two-Way Binding with @bind-Value

Use `@bind-Value` for automatic two-way binding:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select a language"
    DataSource="@Languages"
    @bind-Value="@SelectedLanguage">
</SfComboBox>

<p>You selected: @SelectedLanguage</p>

<button @onclick="ChangeValue">Change to Python</button>

@code {
    private string SelectedLanguage = "C#";
    private List<string> Languages = new() { "C#", "JavaScript", "Python", "Java" };

    private void ChangeValue()
    {
        SelectedLanguage = "Python";
    }
}
```

### One-Way Binding with Value Property

For read-only or one-way binding:

```razor
<SfComboBox TItem="string" TValue="string"
    Placeholder="Select a language"
    DataSource="@Languages"
    Value="@SelectedLanguage">
</SfComboBox>

@code {
    private string SelectedLanguage = "C#";
    private List<string> Languages = new() { "C#", "JavaScript", "Python" };
}
```

---

## Index Binding

Bind selection by index position instead of value:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries"
    @bind-Index="@SelectedIndex">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

<p>Selected Index: @SelectedIndex</p>
<p>Selected Country: @(SelectedIndex.HasValue && SelectedIndex < Countries.Count ? Countries[(int)SelectedIndex].Name : "None")</p>

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

**Note:** When data is sorted, index refers to sorted position, not original position.

---

## Preselected Values

### On Initial Render

Set a value in the `OnInitializedAsync` method or component initialization:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries"
    @bind-Value="@SelectedValue">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

<p>Selected: @SelectedValue</p>

@code {
    private string SelectedValue;

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

    protected override async Task OnInitializedAsync()
    {
        // Set default selection
        SelectedValue = "USA";
        await Task.Delay(0); // Simulates async operation
    }
}
```

### Using @bind-Value Directly

```razor
<SfComboBox TItem="string" TValue="string"
    DataSource="@Languages"
    @bind-Value="@SelectedLanguage">
</SfComboBox>

@code {
    // Initialize with default value
    private string SelectedLanguage = "C#";
    private List<string> Languages = new() { "C#", "JavaScript", "Python" };
}
```

### Using Index

```razor
<SfComboBox TItem="Country" TValue="string"
    DataSource="@Countries"
    @bind-Index="@InitialIndex">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private int? InitialIndex = 1; // Select second item
    
    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "USA", Code = "1" },
        new Country { Name = "UK", Code = "2" }
    };
}
```

---

## Programmatic Selection

Change the selected value from code using component reference:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox @ref="ComboBoxRef"
    TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees"
    @bind-Value="@SelectedEmployeeId">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

<div style="margin-top: 20px;">
    <button @onclick="SelectFirst">Select First</button>
    <button @onclick="SelectSecond">Select Second</button>
    <button @onclick="ClearSelection">Clear</button>
</div>

<p>Selected: @SelectedEmployeeId</p>

@code {
    private SfComboBox<Employee, int> ComboBoxRef;
    private int SelectedEmployeeId = 0;

    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith" },
        new Employee { EmployeeId = 2, Name = "Jane Doe" }
    };

    private void SelectFirst()
    {
        SelectedEmployeeId = 1;
    }

    private void SelectSecond()
    {
        SelectedEmployeeId = 2;
    }

    private void ClearSelection()
    {
        SelectedEmployeeId = 0;
    }
}
```

---

## Selection Events

### ValueChange Event

Triggered when the value changes:

```razor
<SfComboBox TItem="Country" TValue="string"
    DataSource="@Countries"
    @bind-Value="@SelectedValue">
    <ComboBoxEvents TItem="Country" TValue="string"
        ValueChange="@OnValueChange"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private string SelectedValue;

    private void OnValueChange(ChangeEventArgs<string, Country> args)
    {
        Console.WriteLine($"Current: {args.Value}");
        Console.WriteLine($"Item: {args.ItemData?.Name}");
    }
}
```

### OnValueSelect Event

Triggered when a value is selected from the popup:

```razor
<SfComboBox TItem="Country" TValue="string"
    DataSource="@Countries"
    @bind-Value="@SelectedValue">
    <ComboBoxEvents TItem="Country" TValue="string"
        OnValueSelect="@OnValueSelect"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private string SelectedValue;

    private void OnValueSelect(SelectEventArgs<Country> args)
    {
        // You can prevent selection by setting Cancel = true
        Console.WriteLine($"Selected: {args.ItemData.Name}");
    }
}
```

---

## Autofill Functionality

The `Autofill` property automatically fills the first matching item as the user types:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Type to see autofill"
    DataSource="@Countries"
    AllowFiltering="true"
    Autofill="true"
    @bind-Value="@SelectedCountry">
</SfComboBox>

<p>Selected: @SelectedCountry</p>

@code {
    private string SelectedCountry;
    private List<string> Countries = new()
    {
        "United States",
        "United Kingdom",
        "Ukraine",
        "Canada"
    };
}
```

**Behavior:**
- User types "uni" → autofills "United States"
- User types "can" → autofills "Canada"
- No match found → remains unchanged

---

## Read-Only Selection

Make the ComboBox read-only so users can only select from the list:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries"
    Readonly="true"
    @bind-Value="@SelectedValue">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private string SelectedValue = "USA";

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
}
```

**Note:** With `Readonly="true"`, users cannot type custom values; they must select from the list.

---

## Best Practices

1. **Always Initialize Values**
   - Set default values in `OnInitializedAsync`
   - Prevents null reference issues

2. **Use @bind-Value for Two-Way Binding**
   - Simplifies state management
   - Automatically updates UI

3. **Handle ValueChange Events**
   - Validate selections
   - Trigger cascading updates
   - Log user actions

4. **Check for Null Values**
   ```razor
   @if (SelectedValue != null)
   {
       <p>Selected: @SelectedValue</p>
   }
   ```

5. **Use Type-Safe Binding**
   - Define proper TValue type
   - Avoid unnecessary conversions

---

*See also: [Data Binding](data-binding.md), [Cascading ComboBox](cascading-combobox.md), [Events & Validation](events-and-validation.md)*
