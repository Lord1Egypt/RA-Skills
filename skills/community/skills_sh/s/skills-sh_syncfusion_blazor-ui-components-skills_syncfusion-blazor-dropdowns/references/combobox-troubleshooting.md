# Troubleshooting ComboBox Issues

Quick solutions for common ComboBox problems:

---

## Data Not Loading / Empty List

### Problem
ComboBox shows empty list or no items appear in the popup.

### Solutions

**1. Check DataSource is Populated**
```razor
<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select"
    DataSource="@Countries">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private List<Country> Countries = new();

    protected override void OnInitialized()
    {
        // Ensure data is loaded
        Countries = new()
        {
            new Country { Name = "USA", Code = "1" },
            new Country { Name = "Canada", Code = "2" }
        };
    }
}
```

**2. Verify Field Settings Match Data Structure**
```razor
// ❌ Wrong - Text property doesn't exist
<ComboBoxFieldSettings Text="CountryName" Value="Code"></ComboBoxFieldSettings>

// ✅ Correct - Properties match class
public class Country
{
    public string Name { get; set; }  // Use "Name"
    public string Code { get; set; }
}

<ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
```

**3. Check for Null Values**
```razor
// Handle null data source
@if (Countries != null && Countries.Any())
{
    <SfComboBox TItem="Country" TValue="string"
        Placeholder="Select"
        DataSource="@Countries">
        <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
    </SfComboBox>
}
else
{
    <p>No data available</p>
}
```

**4. Async Data Loading**
```razor
protected override async Task OnInitializedAsync()
{
    // Wait for data to load before component renders
    Countries = await LoadCountriesAsync();
    await base.OnInitializedAsync();
}
```

---

## Filtering Not Working

### Problem
AllowFiltering is enabled but filtering doesn't work or shows no results.

### Solutions

**1. Enable Filtering**
```razor
// ✅ Correct - Filtering enabled
<SfComboBox TItem="string" TValue="string"
    Placeholder="Search"
    DataSource="@Items"
    AllowFiltering="true">
</SfComboBox>

// ❌ Wrong - Filtering disabled (default)
<SfComboBox TItem="string" TValue="string"
    DataSource="@Items">
</SfComboBox>
```

**2. Check FilterType**
```razor
// Filtering with "startsWith" (default)
<SfComboBox TItem="string" TValue="string"
    AllowFiltering="true"
    FilterType="@FilterType.StartsWith"
    DataSource="@Items">
</SfComboBox>

// Try "Contains" if items don't match "startsWith"
<SfComboBox TItem="string" TValue="string"
    AllowFiltering="true"
    FilterType="@FilterType.Contains"
    DataSource="@Items">
</SfComboBox>
```

**3. Case-Sensitive Filtering**
```razor
// IgnoreCase = true (case-insensitive, default)
<SfComboBox TItem="string" TValue="string"
    AllowFiltering="true"
    IgnoreCase="true"
    DataSource="@Items">
</SfComboBox>

// IgnoreCase = false (case-sensitive)
<SfComboBox TItem="string" TValue="string"
    AllowFiltering="true"
    IgnoreCase="false"
    DataSource="@Items">
</SfComboBox>
```

**4. Custom Filtering Logic**
```razor
<SfComboBox TItem="Employee" TValue="int"
    AllowFiltering="true"
    DataSource="@Employees">
    <ComboBoxEvents TItem="Employee" TValue="int"
        Filtering="@OnFiltering"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private void OnFiltering(FilteringEventArgs args)
    {
        // Custom filter - search in multiple fields
        var filtered = Employees.Where(e =>
            e.Name.Contains(args.Text, StringComparison.OrdinalIgnoreCase) ||
            e.Department.Contains(args.Text, StringComparison.OrdinalIgnoreCase)
        ).ToList();

        args.PreventDefault = true;
        args.UpdateData(filtered);
    }
}
```

---

## Selection / Binding Issues

### Problem
Selected value doesn't update, binding not working, or value stays null.

### Solutions

**1. Use Two-Way Binding**
```razor
// ✅ Correct - Two-way binding with @bind-Value
<SfComboBox TItem="string" TValue="string"
    Placeholder="Select"
    DataSource="@Items"
    @bind-Value="@SelectedItem">
</SfComboBox>

@code {
    private string SelectedItem = "";
}

// ❌ Wrong - One-way only (won't update)
<SfComboBox TItem="string" TValue="string"
    Value="@SelectedItem"
    DataSource="@Items">
</SfComboBox>
```

**2. Initialize Binding Value**
```razor
@code {
    // ✅ Initialize with default value
    private string SelectedCountry = "USA";

    // ❌ Never initialize (stays null)
    private string SelectedCountry;
}
```

**3. Type Matching**
```razor
// ✅ Value type matches TValue
public class Country
{
    public string Code { get; set; }
}

<SfComboBox TItem="Country" TValue="string"
    @bind-Value="@SelectedCode">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private string SelectedCode = "USA";  // TValue is string
}

// ❌ Wrong - Type mismatch
@code {
    private int SelectedCode = 1;  // TValue is string, not int
}
```

**4. Get ItemData on Change**
```razor
<SfComboBox TItem="Country" TValue="string"
    @bind-Value="@SelectedCode"
    DataSource="@Countries">
    <ComboBoxEvents TItem="Country" TValue="string"
        ValueChange="@OnValueChange"></ComboBoxEvents>
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    private string SelectedCode;
    private Country SelectedCountryData;

    private void OnValueChange(ChangeEventArgs<string, Country> args)
    {
        SelectedCountryData = args.ItemData;  // Get full object
        Console.WriteLine($"Selected: {args.Value}, Data: {args.ItemData?.Name}");
    }
}
```

---

## Validation Not Working

### Problem
Form validation doesn't trigger or errors not showing.

### Solutions

**1. Use EditForm Component**
```razor
// ✅ Correct - Form validation with EditForm
<EditForm Model="@FormData" OnValidSubmit="@HandleSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary />

    <SfComboBox TItem="Country" TValue="string"
        Placeholder="Select"
        DataSource="@Countries"
        @bind-Value="@FormData.Country">
        <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
    </SfComboBox>
    <ValidationMessage For="@(() => FormData.Country)" />

    <button type="submit">Submit</button>
</EditForm>

@code {
    public class FormModel
    {
        [Required(ErrorMessage = "Country is required")]
        public string Country { get; set; }
    }
}

// ❌ Wrong - No EditForm (validation won't work)
<SfComboBox TItem="Country" TValue="string"
    @bind-Value="@SelectedCountry"
    DataSource="@Countries">
</SfComboBox>
```

**2. Check Data Annotations**
```csharp
public class FormModel
{
    // ✅ Correct - Validation attributes
    [Required(ErrorMessage = "Please select a country")]
    public string Country { get; set; }

    // ❌ Missing validation
    public string Country { get; set; }
}
```

**3. Use ValidationMessage Component**
```razor
<SfComboBox TItem="Country" TValue="string"
    @bind-Value="@FormData.Country"
    DataSource="@Countries">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

<!-- Show validation error for this field -->
<ValidationMessage For="@(() => FormData.Country)" />
```

---

## Events Not Firing

### Problem
Event handlers (ValueChange, OnOpen, etc.) don't execute.

### Solutions

**1. Verify Event Handler Method Signature**
```razor
// ❌ Wrong signature
private void OnValueChange(string value) { }

// ✅ Correct signature
private void OnValueChange(ChangeEventArgs<string, Country> args) { }

<ComboBoxEvents TItem="Country" TValue="string"
    ValueChange="@OnValueChange"></ComboBoxEvents>
```

**2. Check Event Name Spelling**
```razor
// ✅ Correct event names
<ComboBoxEvents TItem="string" TValue="string"
    ValueChange="@OnValueChange"
    OnValueSelect="@OnValueSelect"
    Focus="@OnFocus"
    Blur="@OnBlur"
    OnOpen="@OnOpen"
    OnClose="@OnClose">
</ComboBoxEvents>

// ❌ Typos in event names won't work
OnValueChanged (should be ValueChange)
OnSelected (should be OnValueSelect)
```

**3. Ensure Events Component Added**
```razor
<SfComboBox TItem="string" TValue="string"
    DataSource="@Items">
    <!-- ✅ Events must be inside ComboBoxEvents component -->
    <ComboBoxEvents TItem="string" TValue="string"
        ValueChange="@OnValueChange">
    </ComboBoxEvents>
</SfComboBox>

@code {
    private void OnValueChange(ChangeEventArgs<string, string> args)
    {
        Console.WriteLine($"Value: {args.Value}");
    }
}
```

---

## Component Not Rendering

### Problem
ComboBox doesn't appear on the page.

### Solutions

**1. Verify Imports**
```razor
// ✅ Add to _Imports.razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns

// Without these, ComboBox won't be recognized
```

**2. Check Services Registration**
```csharp
// ✅ In Program.cs
builder.Services.AddSyncfusionBlazor();

// Without this, components won't initialize properly
```

**3. Verify Theme CSS**
```html
<!-- ✅ In _Host.cshtml or App.razor -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>

<!-- Without theme, component won't style correctly -->
```

---

## Performance Issues

### Problem
ComboBox is slow with large datasets or many items.

### Solutions

**1. Enable Virtualization**
```razor
// ✅ For 1000+ items
<SfComboBox TItem="Item" TValue="int"
    DataSource="@Items"
    EnableVirtualization="true"
    VirtualScrollHeight="300">
</SfComboBox>
```

**2. Optimize DataSource**
```razor
// ❌ Loading all data
private List<Employee> Employees = GetAllEmployees(); // 50,000+ records

// ✅ Pagination or filtering
private List<Employee> Employees = GetFirst1000Employees();
```

**3. Use Remote Filtering**
```razor
// ✅ Filter on server
<SfComboBox TItem="Employee" TValue="int"
    AllowFiltering="true"
    MinFilterLength="2">
    <SfDataManager Url="YOUR_API_ENDPOINT" 
        Adaptor="Syncfusion.Blazor.Adaptors.UrlAdaptor"></SfDataManager>
</SfComboBox>
```

**4. Debounce Delay**
```razor
// ✅ Reduce API calls
<SfComboBox TItem="Employee" TValue="int"
    AllowFiltering="true"
    DebounceDelay="500">
</SfComboBox>
```

---

## Styling Issues

### Problem
Styling doesn't look right or customization not applied.

### Solutions

**1. Check Theme CSS Path**
```html
<!-- ✅ Correct path -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />

<!-- ❌ Wrong path won't load theme -->
<link href="lib/syncfusion/bootstrap5.css" rel="stylesheet" />
```

**2. CSS Specificity**
```css
/* ❌ May not override default styles */
.e-combobox { border: 2px solid blue; }

/* ✅ Higher specificity */
.e-combobox.e-input-group { border: 2px solid blue; }
```

**3. Use CssClass Property**
```razor
<SfComboBox TItem="string" TValue="string"
    DataSource="@Items"
    CssClass="my-custom-combo">
</SfComboBox>

<style>
    .my-custom-combo .e-input-group {
        border: 2px solid #007bff;
        border-radius: 8px;
    }
</style>
```

---

## Need More Help?

- **Check Browser Console**: F12 → Console for JavaScript errors
- **Check Terminal Output**: Look for exceptions during component initialization
- **Inspect Element**: F12 → Inspector to verify structure and applied classes
- **Search Documentation**: [Syncfusion Blazor Docs](https://blazor.syncfusion.com/documentation/combobox/getting-started/)
- **Create Minimal Repro**: Simplify to isolate the issue

---

*See also: [Getting Started](getting-started.md), [Events & Validation](events-and-validation.md), [Data Binding](data-binding.md)*
