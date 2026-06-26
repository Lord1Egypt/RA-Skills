# Advanced Features in Syncfusion Blazor AutoComplete

## Virtualization

For large datasets (100+ items), use **virtualization** to render only visible items, improving performance:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                EnableVirtualization="true"
                Placeholder="Select a country">
</SfAutoComplete>

@code {
    private List<string> Countries = new();

    protected override void OnInitialized()
    {
        // Generate 1000 items
        for (int i = 1; i <= 1000; i++)
        {
            Countries.Add($"Country {i}");
        }
    }
}
```

**Benefits:**
- Handles 1000s of items without performance degradation
- Only renders visible items in viewport
- Smooth scrolling and instant filtering

### Virtualization with Objects

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees"
                AllowFiltering="true"
                EnableVirtualization="true">
    <AutoCompleteFieldSettings Value="EmployeeName" >
    </AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string Department { get; set; }
    }

    private List<Employee> Employees = new();

    protected override void OnInitialized()
    {
        // Generate 5000 employees
        for (int i = 1; i <= 5000; i++)
        {
            Employees.Add(new Employee 
            { 
                EmployeeId = i, 
                EmployeeName = $"Employee {i}", 
                Department = $"Dept {(i % 10)}"
            });
        }
    }
}
```

## Popup Settings

Control the appearance and behavior of the dropdown popup:

### Positioning

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                PopupHeight="200px"
                PopupWidth="300px">
</SfAutoComplete>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada", "Denmark" 
    };
}
```

**Properties:**
- `PopupHeight` - Height of dropdown (default: auto)
- `PopupWidth` - Width of dropdown (default: matches input width)

### Popup Open/Close Events

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
    <AutoCompleteEvents TValue="string" TItem="string"
                        Opened="@OnPopupOpen"
                        Closed="@OnPopupClose">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>Popup State: @PopupState</p>

@code {
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
    
    private string PopupState = "Closed";

    private void OnPopupOpen(PopupEventArgs args)
    {
        PopupState = "Opened";
        Console.WriteLine("Popup opened");
    }

    private void OnPopupClose(ClosedEventArgs args)
    {
        PopupState = "Closed";
        Console.WriteLine("Popup closed");
    }
}
```

## Disabled Items

Prevent users from selecting specific items:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees">
    <AutoCompleteFieldSettings Value="EmployeeName" Disabled="IsDisabled">
    </AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public bool IsDisabled { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, EmployeeName = "John Smith", IsDisabled = false },
        new Employee { EmployeeId = 2, EmployeeName = "Jane Doe", IsDisabled = true },  // Disabled
        new Employee { EmployeeId = 3, EmployeeName = "Bob Wilson", IsDisabled = false }
    };
}
```

**Result:** "Jane Doe" appears grayed out and cannot be selected.

## Custom Values

Allow users to enter values not in the original dataset:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowCustom="true"
                Placeholder="Select or type a country">
</SfAutoComplete>

<p>Selected: @SelectedValue</p>

@code {
    private string SelectedValue = "";
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };
}
```

**Behavior:** If user types "France", the value "France" is retained even though it's not in the list.

### Custom Values with Validation

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                AllowCustom="true"
                @bind-Value="CustomValue"
                Placeholder="Enter a country">
    <AutoCompleteEvents TValue="string" TItem="string"
                        ValueChange="@OnValueChange">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>@ValidationMessage</p>

@code {
    private string CustomValue = "";
    private string ValidationMessage = "";
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };

    private void OnValueChange(ChangeEventArgs<string, string> args)
    {
        CustomValue = args.Value;
        
        if (string.IsNullOrEmpty(args.Value))
        {
            ValidationMessage = "";
        }
        else if (args.Value.Length < 2)
        {
            ValidationMessage = "Country name must be at least 2 characters";
        }
        else
        {
            ValidationMessage = $"✓ {args.Value} is valid";
        }
    }
}
```

## Localization & RTL

### Right-to-Left (RTL) Support

Enable RTL for languages like Arabic, Hebrew:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                EnableRtl="true"
                Placeholder="اختر دولة">
</SfAutoComplete>

@code {
    private List<string> Countries = new() 
    { 
        "مصر", "السعودية", "الإمارات" 
    };
}
```

**Common Locales:** `en` (English), `es` (Spanish), `fr` (French), `de` (German), `ar` (Arabic)

## Event Handling

### ValueChange Event

Triggered when user selects or enters a value:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries"
                @bind-Value="SelectedValue">
    <AutoCompleteEvents TValue="string" TItem="string"
                        ValueChange="@OnValueChange">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>Selected: @SelectedValue</p>
<p>Change Count: @ChangeCount</p>

@code {
    private string SelectedValue = "";
    private int ChangeCount = 0;
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };

    private void OnValueChange(ChangeEventArgs<string, string> args)
    {
        SelectedValue = args.Value;
        ChangeCount++;
        Console.WriteLine($"Value changed to: {args.Value}");
    }
}
```

### Focus & Blur Events

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Countries">
    <AutoCompleteEvents TValue="string" TItem="string"
                        Focus="@OnFocus"
                        Blur="@OnBlur">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>Status: @Status</p>

@code {
    private string Status = "Not focused";
    
    private List<string> Countries = new() 
    { 
        "Austria", "Brazil", "Canada" 
    };

    private void OnFocus(object args)
    {
        Status = "Focused";
    }

    private void OnBlur(object args)
    {
        Status = "Blurred";
    }
}
```

### Filtering Event

Execute custom logic during filtering:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Employee" 
                DataSource="@Employees"
                AllowFiltering="true">
    <AutoCompleteFieldSettings Value="EmployeeName" >
    </AutoCompleteFieldSettings>
    <AutoCompleteEvents TValue="string" TItem="Employee"
                        Filtering="@OnFiltering">
    </AutoCompleteEvents>
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
        new Employee { EmployeeId = 2, EmployeeName = "Jane Doe", Department = "HR" },
        new Employee { EmployeeId = 3, EmployeeName = "Bob Wilson", Department = "IT" }
    };

    private void OnFiltering(FilteringEventArgs args)
    {
        Console.WriteLine($"Filtering for: {args.Text}");
        
        // Custom filter: only show IT department
        args.FilteredData = Employees
            .Where(e => e.Department == "IT" && e.EmployeeName.Contains(args.Text))
            .Cast<object>()
            .ToList();
    }
}
```

### Selection Event

Execute logic when user selects an item:

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Product" 
                DataSource="@Products">
    <AutoCompleteFieldSettings Value="ProductName" >
    </AutoCompleteFieldSettings>
    <AutoCompleteEvents TValue="string" TItem="Product"
                        OnValueSelect="@OnItemSelected">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>@SelectionMessage</p>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Price { get; set; }
    }

    private string SelectionMessage = "";
    
    private List<Product> Products = new()
    {
        new Product { ProductId = 1, ProductName = "Laptop", Price = 999 },
        new Product { ProductId = 2, ProductName = "Mouse", Price = 29 }
    };

    private void OnItemSelected(SelectEventArgs<Product> args)
    {
        SelectionMessage = $"You selected: {args.ItemData.ProductName} (${args.ItemData.Price})";
        Console.WriteLine($"Selected Product ID: {args.ItemData.ProductId}");
    }
}
```

## Common Patterns

### Pattern 1: Search with API Call

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="GitHubUser" 
                AllowFiltering="true"
                DebounceDelay="500">
    <AutoCompleteFieldSettings Value="Login" >
    </AutoCompleteFieldSettings>
    <AutoCompleteEvents TValue="string" TItem="GitHubUser"
                        Filtering="@OnFiltering">
    </AutoCompleteEvents>
</SfAutoComplete>

@code {
    public class GitHubUser
    {
        public string Login { get; set; }
    }

    private List<GitHubUser> SearchResults = new();

    private async Task OnFiltering(FilteringEventArgs args)
    {
        if (string.IsNullOrEmpty(args.Text) || args.Text.Length < 2)
        {
            args.FilteredData = new();
            return;
        }

        try
        {
            using var client = new HttpClient();
            var response = await client.GetAsync($"YOUR_API_ENDPOINT/search/users?q={args.Text}&per_page=5");
            // Parse response and populate args.FilteredData
        }
        catch { }
    }
}
```

### Pattern 2: Dependent AutoComplete

```blazor
@using Syncfusion.Blazor.DropDowns

<SfAutoComplete TValue="string" TItem="Country" 
                DataSource="@Countries"
                @bind-Value="SelectedCountry">
    <AutoCompleteFieldSettings Value="CountryName" ></AutoCompleteFieldSettings>
    <AutoCompleteEvents TValue="string" TItem="Country"
                        ValueChange="@OnCountryChange">
    </AutoCompleteEvents>
</SfAutoComplete>

<SfAutoComplete TValue="string" TItem="City" 
                DataSource="@Cities"
                @bind-Value="SelectedCity">
    <AutoCompleteFieldSettings Value="CityName" ></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Country { public string CountryName { get; set; } }
    public class City { public string CityName { get; set; } public string Country { get; set; } }

    private string SelectedCountry = "";
    private string SelectedCity = "";

    private List<Country> Countries = new()
    {
        new Country { CountryName = "USA" },
        new Country { CountryName = "Canada" }
    };

    private List<City> Cities = new();
    private List<City> AllCities = new()
    {
        new City { CityName = "New York", Country = "USA" },
        new City { CityName = "Los Angeles", Country = "USA" },
        new City { CityName = "Toronto", Country = "Canada" }
    };

    private void OnCountryChange(ChangeEventArgs<string, Country> args)
    {
        SelectedCountry = args.Value;
        // Filter cities based on selected country
        Cities = AllCities.Where(c => c.Country == SelectedCountry).ToList();
        SelectedCity = "";
    }
}
```

## Related Topics

- [Filtering & Search](filtering-and-search.md)
- [Templates & Styling](templates-and-styling.md)
- [Accessibility & Best Practices](accessibility-and-best-practices.md)
