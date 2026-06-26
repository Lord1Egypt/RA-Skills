# Accessibility & Best Practices for Syncfusion Blazor AutoComplete

## WCAG Compliance

The AutoComplete component is built with accessibility standards in mind. Ensure your implementation follows these guidelines:

### Semantic HTML

Use proper semantic structure in templates:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees">
    <AutoCompleteFieldSettings Value="EmployeeName">
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Employee">
        <ItemTemplate>
            <div role="option">
                @((context as Employee)?.EmployeeName)
                <span aria-label="Department: @((context as Employee)?.Department)">
                    @((context as Employee)?.Department)
                </span>
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

    private List<Employee> Employees = new();
}
```

## ARIA Attributes

Provide context for assistive technologies:

### Basic ARIA Labels

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                Placeholder="Choose country">
</SfAutoComplete>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

### ARIA Expanded & Popup

```blazor
@using Syncfusion.Blazor.DropDowns

<div role="combobox" 
     aria-label="Country selector"
     aria-expanded="@PopupOpen"
     aria-haspopup="listbox">
    <SfAutoComplete TValue="string" TItem="string" 
                    DataSource="@Countries">
        <AutoCompleteEvents TValue="string" TItem="string"
                            Opened="@OnOpened"
                            Closed="@OnClosed">
        </AutoCompleteEvents>
    </SfAutoComplete>
</div>

@code {
    private bool PopupOpen = false;
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };

    private void OnOpened(PopupEventArgs args) => PopupOpen = true;
    private void OnClosed(ClosedEventArgs args) => PopupOpen = false;
}
```

### Group Accessibility

```blazor
<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees">
    <AutoCompleteFieldSettings Value="EmployeeName" GroupBy="Department">
    </AutoCompleteFieldSettings>
    <AutoCompleteTemplates TItem="Employee">
        <GroupTemplate>
            <div role="group" aria-label="@((context as CompositeData)?.GroupData?.Key) Department">
                @((context as CompositeData)?.GroupData?.Key)
            </div>
        </GroupTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> Employees = new();
}
```

## Keyboard Navigation

### Keyboard Support (Built-in)

The AutoComplete supports these keyboard interactions by default:

| Key | Action |
|-----|--------|
| **Arrow Up** | Move focus to previous item |
| **Arrow Down** | Move focus to next item |
| **Enter** | Select focused item |
| **Escape** | Close dropdown |
| **Tab** | Move focus out of component |
| **Space** | Open/trigger component |

### Test Keyboard Navigation

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true">
</SfAutoComplete>

<p>Keyboard Tips:</p>
<ul>
    <li>Use Arrow Up/Down to navigate items</li>
    <li>Press Enter to select</li>
    <li>Press Escape to close</li>
    <li>Type to filter items</li>
</ul>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada", "Denmark", "Egypt" 
    };
}
```

## Screen Reader Support

### Announce Item Selection

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
    <AutoCompleteEvents TValue="string" TItem="string"
                        OnValueSelect="@OnItemSelected">
    </AutoCompleteEvents>
</SfAutoComplete>

<div role="status" aria-live="polite" aria-atomic="true">
    @AnnouncementMessage
</div>

@code {
    private string AnnouncementMessage = "";
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };

    private void OnItemSelected(SelectEventArgs<string> args)
    {
        AnnouncementMessage = $"Selected: {args.ItemData}";
    }
}
```

### Live Region for Filtering

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true">
    <AutoCompleteEvents TValue="string" TItem="string"
                        Filtering="@OnFiltering">
    </AutoCompleteEvents>
</SfAutoComplete>

<div role="region" aria-live="assertive" aria-atomic="true">
    @FilterMessage
</div>

@code {
    private string FilterMessage = "";
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada", "Denmark", "Egypt" 
    };

    private void OnFiltering(FilteringEventArgs args)
    {
        var matchCount = Countries.Count(c => c.Contains(args.Text, StringComparison.OrdinalIgnoreCase));
        FilterMessage = $"{matchCount} items match '{args.Text}'";
    }
}
```

## Color Contrast

Ensure sufficient contrast for readability:

```blazor
<SfAutoComplete TItem="string" 
                DataSource="@Countries"
                CssClass="accessible-autocomplete">
</SfAutoComplete>

<style>
    /* WCAG AA compliance: 4.5:1 contrast ratio for normal text */
    .accessible-autocomplete.e-autocomplete .e-input {
        color: #000;  /* Black text */
        background: #fff;  /* White background */
        border: 1px solid #333;  /* Dark border */
    }

    /* WCAG AAA compliance: 7:1 contrast ratio */
    .accessible-autocomplete.e-autocomplete .e-list-item {
        color: #000;
        background: #fff;
    }

    .accessible-autocomplete.e-autocomplete .e-list-item:focus,
    .accessible-autocomplete.e-autocomplete .e-list-item.e-item-focus {
        background: #003d7a;  /* High contrast blue */
        color: #fff;
    }
</style>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

## Focus Indicators

Make focus visible for keyboard navigation:

```blazor
<SfAutoComplete TItem="string" 
                DataSource="@Countries"
                CssClass="accessible-focus">
</SfAutoComplete>

<style>
    /* Clear focus indicator */
    .accessible-focus.e-autocomplete .e-input:focus {
        outline: 3px solid #004085;
        outline-offset: 2px;
    }

    .accessible-focus.e-autocomplete .e-list-item:focus {
        outline: 2px solid #004085;
    }
</style>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

## Label Association

Always associate a label with the AutoComplete:

```blazor
@using Syncfusion.Blazor.DropDowns

<label for="country-select">Country of Residence</label>
<SfAutoComplete TItem="string" 
                DataSource="@Countries"
                Id="country-select"
                FloatLabelType="FloatLabelType.Always"
                Placeholder="Select country">
</SfAutoComplete>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

## Error Messages & Validation

Display accessible error states:

```blazor
@using Syncfusion.Blazor.DropDowns

<div>
    <label for="email-country">Country</label>
    <SfAutoComplete TValue="string" TItem="string" 
                    DataSource="@Countries"
                    Id="email-country"
                    @bind-Value="SelectedCountry">
        <AutoCompleteEvents TValue="string" TItem="string"
                            ValueChange="@OnCountryChange">
        </AutoCompleteEvents>
    </SfAutoComplete>
    
    @if (!IsValid)
    {
        <div id="error-message" role="alert" style="color: #dc3545; margin-top: 5px;">
            ⚠️ Please select a valid country
        </div>
    }
</div>

@code {
    private string SelectedCountry = "";
    private bool IsValid = true;
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };

    private void OnCountryChange(ChangeEventArgs<string, string> args)
    {
        SelectedCountry = args.Value;
        IsValid = !string.IsNullOrEmpty(args.Value);
    }
}
```

## Best Practices

### 1. Provide Clear Instructions

```blazor
<div>
    <h3>Search for Products</h3>
    <p>Start typing the product name. Use arrow keys to navigate results.</p>
    <SfAutoComplete TValue="string" TItem="string" 
                    DataSource="@Products">
    </SfAutoComplete>
</div>

@code {
    private List<string> Products = new();
}
```

### 2. Handle Empty States

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowFiltering="true">
    <AutoCompleteTemplates TItem="string">
        <NoRecordsTemplate>
            <div role="alert">
                <p>No results found. Try a different search term.</p>
            </div>
        </NoRecordsTemplate>
    </AutoCompleteTemplates>
</SfAutoComplete>

@code {
    private List<string> Countries = new();
}
```

### 3. Performance Optimization

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees"
                AllowFiltering="true"
                MinLength="2"
                DebounceDelay="300"
                EnableVirtualization="true">
    <AutoCompleteFieldSettings Value="EmployeeName"></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
    }

    private List<Employee> Employees = new();
    
    protected override void OnInitialized()
    {
        // Load large dataset efficiently
        for (int i = 1; i <= 10000; i++)
        {
            Employees.Add(new Employee 
            { 
                EmployeeId = i, 
                EmployeeName = $"Employee {i}" 
            });
        }
    }
}
```

### 4. Mobile-Friendly Design

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                CssClass="mobile-optimized"
                PopupHeight="400px"
                PopupWidth="100%">
</SfAutoComplete>

<style>
    @media (max-width: 768px)
    {
        .mobile-optimized.e-autocomplete .e-input {
            font-size: 16px;  /* Prevents zoom on iOS */
            padding: 12px;
        }

        .mobile-optimized.e-autocomplete .e-list-item {
            padding: 12px;
            min-height: 44px;  /* Touch-friendly size */
        }
    }
</style>

@code {
    private List<string> Countries = new();
}
```

## Troubleshooting

### Issue: Screen Reader Not Reading Items

**Solution:** Ensure proper ARIA labels and roles:

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
</SfAutoComplete>
```

### Issue: Keyboard Navigation Not Working

**Solution:** Verify focus is properly managed:

```blazor
@if (FocusOnFirst)
{
    <SfAutoComplete TValue="string" TItem="string" 
                    DataSource="@Countries"
                    @ref="AutoCompleteRef">
    </SfAutoComplete>
}

@code {
    private bool FocusOnFirst = false;
    private SfAutoComplete<string, string> AutoCompleteRef;

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            FocusOnFirst = true;
            await AutoCompleteRef.FocusAsync();
        }
    }
}
```

## Related Topics

- [Templates & Styling](templates-and-styling.md)
- [Advanced Features](advanced-features.md)
- [Getting Started](getting-started.md)
