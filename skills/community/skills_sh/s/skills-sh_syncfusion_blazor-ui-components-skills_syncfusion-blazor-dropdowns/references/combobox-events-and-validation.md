# Events & Validation in ComboBox

## Table of Contents

- [Available Events](#available-events)
- [Blur Event](#blur-event)
- [Focus Event](#focus-event)
- [ValueChange Event](#valuechange-event)
- [OnValueSelect Event](#onvalueselect-event)
- [OnOpen Event](#onopen-event)
- [OnClose Event](#onclose-event)
- [Filtering Event](#filtering-event)
- [Form Validation](#form-validation)
- [Data Annotations](#data-annotations)
- [Custom Validation](#custom-validation)

---

## Available Events

The ComboBox component provides these lifecycle and interaction events:

| Event | Trigger | Use Case |
|-------|---------|----------|
| `Blur` | Input loses focus | Validation, formatting |
| `Focus` | Input gets focus | Initialize, load data |
| `ValueChange` | Value changes | React to selection |
| `OnValueSelect` | Item selected from popup | Confirm selection |
| `Created` | Component initialized | Setup, defaults |
| `OnOpen` | Popup opens | Prevent opening, pre-load |
| `OnClose` | Popup closes | Cleanup, save state |
| `Filtering` | Filter text typed | Custom filtering |

---

## Blur Event

Triggers when the input field loses focus:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select a language"
    DataSource="@Languages">
    <ComboBoxEvents TItem="string" TValue="string"
        Blur="@OnBlur"></ComboBoxEvents>
</SfComboBox>

<p>Last blur time: @BlurTime</p>

@code {
    private string BlurTime = "Not blurred";
    private List<string> Languages = new() { "C#", "JavaScript", "Python" };

    private void OnBlur(Microsoft.AspNetCore.Components.Web.FocusEventArgs args)
    {
        BlurTime = DateTime.Now.ToString("hh:mm:ss");
        Console.WriteLine("ComboBox lost focus");
    }
}
```

---

## Focus Event

Triggers when the input field receives focus:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Type here"
    DataSource="@Languages">
    <ComboBoxEvents TItem="string" TValue="string"
        Focus="@OnFocus"></ComboBoxEvents>
</SfComboBox>

@code {
    private List<string> Languages = new() { "C#", "JavaScript", "Python" };

    private void OnFocus(object args)
    {
        Console.WriteLine("ComboBox received focus");
    }
}
```

---

## ValueChange Event

Triggers when the selected value changes:

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

<div style="margin-top: 20px;">
    <p><strong>Current:</strong> @SelectedValue</p>
    <p><strong>Item Data:</strong> @SelectedValueText</p>
</div>

@code {
    private string SelectedValue;
    private string SelectedValueText;

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
        SelectedValue = args.Value;
        SelectedValueText = args.ItemData?.Name;
        Console.WriteLine($"Value changed from {PreviousValue} to {SelectedValue}");
    }
}
```

---

## OnValueSelect Event

Triggers when an item is selected from the popup list:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
    <ComboBoxEvents TItem="Employee" TValue="int"
        OnValueSelect="@OnValueSelect"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

<p>Selection message: @SelectionMessage</p>

@code {
    private string SelectionMessage;

    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith", Department = "IT" },
        new Employee { EmployeeId = 2, Name = "Jane Doe", Department = "HR" }
    };

    private void OnValueSelect(SelectEventArgs<Employee> args)
    {
        SelectionMessage = $"Selected: {args.ItemData.Name} ({args.ItemData.Department})";
        
        // Prevent selection of specific items
        if (args.ItemData.Department == "HR")
        {
            args.Cancel = true;
            SelectionMessage = "HR department not available";
        }
    }
}
```

---

## OnOpen Event

Triggers when the popup opens:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items">
    <ComboBoxEvents TItem="string" TValue="string"
        OnOpen="@OnPopupOpen"></ComboBoxEvents>
</SfComboBox>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
    private int OpenCount = 0;

    private void OnPopupOpen(BeforeOpenEventArgs args)
    {
        OpenCount++;
        Console.WriteLine($"Popup opened {OpenCount} times");
        
        // Prevent opening based on condition
        // args.Cancel = true;
    }
}
```

---

## OnClose Event

Triggers when the popup closes:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items">
    <ComboBoxEvents TItem="string" TValue="string"
        OnClose="@OnPopupClose"></ComboBoxEvents>
</SfComboBox>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };

    private void OnPopupClose(PopupEventArgs args)
    {
        Console.WriteLine("Popup closed");
        
        // Prevent closing based on condition
        // args.Cancel = true;
    }
}
```

---

## Filtering Event

Triggers when text is entered for filtering:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Search employees"
    DataSource="@Employees"
    AllowFiltering="true">
    <ComboBoxEvents TItem="Employee" TValue="int"
        Filtering="@OnFiltering"></ComboBoxEvents>
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

    private void OnFiltering(FilteringEventArgs args)
    {
        // Custom filtering logic
        var filteredItems = Employees.Where(e =>
            e.Name.Contains(args.Text, StringComparison.OrdinalIgnoreCase) ||
            e.Department.Contains(args.Text, StringComparison.OrdinalIgnoreCase)
        ).ToList();

        args.PreventDefault = true;
        args.UpdateData(filteredItems);
    }
}
```

---

## Form Validation

### Using EditForm Component

Integrate ComboBox with Blazor's EditForm for automatic validation:

```razor
@using Syncfusion.Blazor.DropDowns
@using System.ComponentModel.DataAnnotations

<EditForm Model="@FormData" OnValidSubmit="@HandleSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary />

    <div class="form-group">
        <label for="name">Name:</label>
        <InputText id="name" @bind-Value="@FormData.Name" class="form-control" />
        <ValidationMessage For="@(() => FormData.Name)" />
    </div>

    <div class="form-group">
        <label for="country">Country:</label>
        <SfComboBox TItem="Country" TValue="string"
            ID="country"
            Placeholder="Select a country"
            DataSource="@Countries"
            @bind-Value="@FormData.Country">
            <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
        </SfComboBox>
        <ValidationMessage For="@(() => FormData.Country)" />
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>
</EditForm>

@code {
    private FormModel FormData = new();

    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    public class FormModel
    {
        [Required(ErrorMessage = "Name is required")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Please select a country")]
        public string Country { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "United Kingdom", Code = "UK" },
        new Country { Name = "Canada", Code = "CA" }
    };

    private void HandleSubmit()
    {
        Console.WriteLine($"Form submitted: {FormData.Name}, {FormData.Country}");
    }
}
```

---

## Data Annotations

### Required Attribute

```csharp
public class FormModel
{
    [Required(ErrorMessage = "Country is required")]
    public string Country { get; set; }
}
```

### String Length Validation

```csharp
public class FormModel
{
    [StringLength(50, MinimumLength = 2, 
        ErrorMessage = "Name must be between 2 and 50 characters")]
    public string Name { get; set; }
}
```

### Range Validation

```csharp
public class FormModel
{
    [Range(1, int.MaxValue, ErrorMessage = "Please select an employee")]
    public int EmployeeId { get; set; }
}
```

---

## Custom Validation

### Using Custom Validator

```razor
@using Syncfusion.Blazor.DropDowns
@using System.ComponentModel.DataAnnotations

<EditForm Model="@FormData" OnValidSubmit="@HandleSubmit">
    <ObjectGraphDataAnnotationsValidator />
    <ValidationSummary />

    <div class="form-group">
        <label>Select Department:</label>
        <SfComboBox TItem="string" TValue="string"
            Placeholder="Choose a department"
            DataSource="@Departments"
            @bind-Value="@FormData.Department">
        </SfComboBox>
        <ValidationMessage For="@(() => FormData.Department)" />
    </div>

    <button type="submit">Submit</button>
</EditForm>

@code {
    private FormModel FormData = new();
    private List<string> Departments = new() { "IT", "HR", "Sales" };

    public class FormModel
    {
        [CustomValidation(typeof(FormValidator), nameof(FormValidator.ValidateDepartment))]
        public string Department { get; set; }
    }

    public class FormValidator
    {
        public static ValidationResult ValidateDepartment(string department, ValidationContext context)
        {
            if (string.IsNullOrEmpty(department))
            {
                return new ValidationResult("Department is required");
            }

            if (department == "IT")
            {
                return new ValidationResult("IT department is not available");
            }

            return ValidationResult.Success;
        }
    }

    private void HandleSubmit()
    {
        Console.WriteLine($"Valid form submitted: {FormData.Department}");
    }
}
```

---

## Best Practices

1. **Always Handle ValueChange Event**
   - Updates related components
   - Triggers cascading logic
   - Validates dependent fields

2. **Use ValidationMessage Component**
   - Shows field-specific errors
   - Better UX than ValidationSummary alone

3. **Prevent Invalid Operations**
   - Use event Cancel property
   - Validate before allowing selection

4. **Combine Events for Complex Logic**
   - Use OnValueSelect + ValueChange
   - OnOpen + Filtering for dynamic data

5. **Test Event Sequences**
   - Blur → Focus transitions
   - ValueChange → OnClose interactions

---

## Troubleshooting

**Validation not working?**
- Ensure `DataAnnotationsValidator` in EditForm
- Check property names match ComboBox binding
- Verify validation attributes on model

**Events not firing?**
- Verify event handler method signature
- Check event name spelling
- Ensure component is bound correctly

**Form not submitting?**
- Verify all required fields populated
- Check validation rules
- Use browser console for errors

---

*See also: [Selection & Value](selection-and-value.md), [Getting Started](getting-started.md), [Cascading ComboBox](cascading-combobox.md)*
