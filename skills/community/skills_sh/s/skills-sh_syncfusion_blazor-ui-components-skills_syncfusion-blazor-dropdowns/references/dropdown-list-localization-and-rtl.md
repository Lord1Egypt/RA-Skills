# Localization and RTL Support in Syncfusion Blazor DropDown List

## RTL (Right-to-Left) Support

### Enable RTL

Enable right-to-left text direction for languages like Arabic, Hebrew, and Persian:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                EnableRtl="true"
                Placeholder="اختر عنصر">
</SfDropDownList>

@code {
    private List<string> Items = new()
    {
        "الخيار الأول",
        "الخيار الثاني",
        "الخيار الثالث"
    };
}
```

### RTL with Field Mapping

Use RTL with complex data objects:

```razor
<SfDropDownList TValue="int" TItem="Product" DataSource="@Products"
                EnableRtl="true"
                Placeholder="اختر منتج">
    <DropDownListFieldSettings Text="@nameof(Product.NameAr)" Value="@nameof(Product.Id)" />
</SfDropDownList>

@code {
    private List<Product> Products;

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Id = 1, NameAr = "جهاز كمبيوتر محمول" },
            new Product { Id = 2, NameAr = "الفأرة" },
            new Product { Id = 3, NameAr = "لوحة المفاتيح" }
        };
    }

    public class Product
    {
        public int Id { get; set; }
        public string NameAr { get; set; }
    }
}
```

### Global RTL Configuration

Set RTL globally for all Syncfusion components:

```csharp
// In Program.cs
builder.Services.AddSyncfusionBlazor(options => { options.EnableRtl = true; });
```

Then dropdowns will automatically use RTL without specifying `EnableRtl="true"` on each component.

## Localization Patterns

### Multi-Language Support

Create dropdowns that work with different languages:

```razor
<div class="mb-3">
    <button @onclick="() => CurrentLanguage = 'en'" class="btn btn-sm btn-outline-primary">English</button>
    <button @onclick="() => CurrentLanguage = 'ar'" class="btn btn-sm btn-outline-primary">العربية</button>
    <button @onclick="() => CurrentLanguage = 'es'" class="btn btn-sm btn-outline-primary">Español</button>
</div>

<SfDropDownList TValue="string" TItem="string" DataSource="@GetLocalizedItems()"
                Placeholder="@GetPlaceholder()"
                EnableRtl="@(CurrentLanguage == 'ar')">
</SfDropDownList>

@code {
    private string CurrentLanguage = "en";

    private List<string> GetLocalizedItems()
    {
        return CurrentLanguage switch
        {
            "ar" => new List<string>
            {
                "الخيار الأول",
                "الخيار الثاني",
                "الخيار الثالث"
            },
            "es" => new List<string>
            {
                "Opción uno",
                "Opción dos",
                "Opción tres"
            },
            _ => new List<string>
            {
                "Option One",
                "Option Two",
                "Option Three"
            }
        };
    }

    private string GetPlaceholder()
    {
        return CurrentLanguage switch
        {
            "ar" => "اختر عنصر",
            "es" => "Selecciona una opción",
            _ => "Select an option"
        };
    }
}
```

### Using Resource Files

Use .resx files for centralized localization:

```csharp
// In a localization service or utility class
public class LocalizationService
{
    private static readonly Dictionary<string, Dictionary<string, string>> Translations = new()
    {
        { "en", new Dictionary<string, string>
            {
                { "placeholder_select", "Select an item" },
                { "dept_engineering", "Engineering" },
                { "dept_sales", "Sales" },
                { "dept_marketing", "Marketing" }
            }
        },
        { "ar", new Dictionary<string, string>
            {
                { "placeholder_select", "اختر عنصر" },
                { "dept_engineering", "الهندسة" },
                { "dept_sales", "المبيعات" },
                { "dept_marketing", "التسويق" }
            }
        }
    };

    public static string Translate(string language, string key)
    {
        if (Translations.ContainsKey(language) && Translations[language].ContainsKey(key))
        {
            return Translations[language][key];
        }
        return key;  // Fallback to key if translation not found
    }
}
```

Then use in your component:

```razor
@inject LocalizationService Localization

<SfDropDownList TValue="int" TItem="Department" DataSource="@Departments"
                Placeholder="@Localization.Translate(CurrentLanguage, 'placeholder_select')"
                EnableRtl="@(CurrentLanguage == 'ar')">
    <DropDownListFieldSettings Text="@nameof(Department.LocalizedName)" Value="@nameof(Department.Id)" />
</SfDropDownList>

@code {
    private string CurrentLanguage = "en";
    private List<Department> Departments;

    protected override void OnInitialized()
    {
        Departments = new List<Department>
        {
            new Department { Id = 1, LocalizedName = GetDepartmentName("dept_engineering") },
            new Department { Id = 2, LocalizedName = GetDepartmentName("dept_sales") }
        };
    }

    private string GetDepartmentName(string key)
    {
        return Localization.Translate(CurrentLanguage, key);
    }

    public class Department
    {
        public int Id { get; set; }
        public string LocalizedName { get; set; }
    }
}
```

## Culture-Specific Formatting

### Date and Number Formatting

Format data based on culture/locale:

```razor
<SfDropDownList TValue="int" TItem="Product" DataSource="@Products"
                Placeholder="Select product">
    <DropDownListFieldSettings Text="@nameof(Product.Name)" Value="@nameof(Product.Id)" />
    <DropDownListTemplates TItem="Product">
        <ItemTemplate>
            <div>
                <strong>@context.Name</strong>
                <div style="font-size: 0.9em;">
                    Price: @context.Price.ToString("C", GetCultureInfo())
                </div>
            </div>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private string CurrentLanguage = "en";
    private List<Product> Products;

    private System.Globalization.CultureInfo GetCultureInfo()
    {
        return CurrentLanguage switch
        {
            "ar" => new System.Globalization.CultureInfo("ar-SA"),
            "es" => new System.Globalization.CultureInfo("es-ES"),
            _ => new System.Globalization.CultureInfo("en-US")
        };
    }

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop", Price = 999.99m },
            new Product { Id = 2, Name = "Mouse", Price = 29.99m }
        };
    }

    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public decimal Price { get; set; }
    }
}
```

### Locale-Aware Sorting

Sort items based on culture:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@GetSortedItems()"
                Placeholder="@GetPlaceholder()">
</SfDropDownList>

@code {
    private string CurrentLanguage = "en";

    private List<string> GetSortedItems()
    {
        var items = new List<string> { "Zebra", "Apple", "Banana" };
        var culture = new System.Globalization.CultureInfo(CurrentLanguage);
        return items.OrderBy(i => i, System.StringComparer.Create(culture, false)).ToList();
    }

    private string GetPlaceholder()
    {
        return CurrentLanguage switch
        {
            "ar" => "اختر عنصر",
            "es" => "Seleccionar",
            _ => "Select"
        };
    }
}
```

## Complete Localization Example

```razor
@page "/dropdown-localization"

<h3>Localization and RTL Example</h3>

<div class="mb-3">
    <button @onclick="() => ChangeLanguage('en')" class="btn btn-sm btn-outline-primary">English</button>
    <button @onclick="() => ChangeLanguage('ar')" class="btn btn-sm btn-outline-primary">العربية</button>
    <button @onclick="() => ChangeLanguage('es')" class="btn btn-sm btn-outline-primary">Español</button>
</div>

<div class="form-group">
    <label>@GetLabel("select_employee")</label>
    <SfDropDownList TValue="int" TItem="Employee" DataSource="@GetLocalizedEmployees()"
                    @bind-Value="SelectedEmployeeId"
                    Placeholder="@GetLabel('placeholder')"
                    EnableRtl="@(CurrentLanguage == 'ar')"
                    CssClass="@(CurrentLanguage == 'ar' ? 'rtl-dropdown' : '')">
        <DropDownListFieldSettings Text="@nameof(Employee.LocalizedName)" Value="@nameof(Employee.Id)" />
    </SfDropDownList>
</div>

@if (SelectedEmployeeId > 0)
{
    var selected = AllEmployees.FirstOrDefault(e => e.Id == SelectedEmployeeId);
    @if (selected != null)
    {
        <div class="alert alert-info mt-3" style="direction: @(CurrentLanguage == 'ar' ? "rtl" : "ltr");">
            <strong>@GetLabel("selected"):</strong> @selected.GetLocalizedName(CurrentLanguage)
        </div>
    }
}

<style>
    .rtl-dropdown {
        direction: rtl;
    }
</style>

@code {
    private string CurrentLanguage = "en";
    private int SelectedEmployeeId;
    private List<Employee> AllEmployees;

    private DropDownListFieldSettings ListFields { get; set; } = new()
    {
        Text = "LocalizedName",
        Value = nameof(Employee.Id)
    };

    private void ChangeLanguage(string language)
    {
        CurrentLanguage = language;
        SelectedEmployeeId = 0;
    }

    private List<Employee> GetLocalizedEmployees()
    {
        return AllEmployees.Select(e => new Employee
        {
            Id = e.Id,
            NameEn = e.NameEn,
            NameAr = e.NameAr,
            NameEs = e.NameEs,
            LocalizedName = e.GetLocalizedName(CurrentLanguage)
        }).ToList();
    }

    private string GetLabel(string key)
    {
        return (CurrentLanguage, key) switch
        {
            ("ar", "select_employee") => "اختر الموظف",
            ("ar", "placeholder") => "اختر موظف",
            ("ar", "selected") => "الموظف المختار",
            
            ("es", "select_employee") => "Seleccionar empleado",
            ("es", "placeholder") => "Seleccione empleado",
            ("es", "selected") => "Empleado seleccionado",
            
            (_, "select_employee") => "Select Employee",
            (_, "placeholder") => "Choose employee",
            (_, "selected") => "Selected Employee",
            
            _ => key
        };
    }

    protected override void OnInitialized()
    {
        AllEmployees = new List<Employee>
        {
            new Employee { Id = 1, NameEn = "Alice Johnson", NameAr = "أليس جونسون", NameEs = "Alice Johnson" },
            new Employee { Id = 2, NameEn = "Bob Smith", NameAr = "بوب سميث", NameEs = "Bob Smith" },
            new Employee { Id = 3, NameEn = "Carol White", NameAr = "كارول وايت", NameEs = "Carol White" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string NameEn { get; set; }
        public string NameAr { get; set; }
        public string NameEs { get; set; }
        public string LocalizedName { get; set; }

        public string GetLocalizedName(string language)
        {
            return language switch
            {
                "ar" => NameAr,
                "es" => NameEs,
                _ => NameEn
            };
        }
    }
}
```

## Key Takeaways

- Use `EnableRtl="true"` for right-to-left languages
- Set global RTL in Program.cs for all components
- Implement multi-language support with localization services
- Use culture-specific formatting for numbers and dates
- Apply locale-aware sorting based on language
- Store translations in centralized resource files
- Maintain separate content for each language
- Test with different languages and text directions
- Consider text length differences between languages
- Use CSS classes to handle RTL-specific styling
