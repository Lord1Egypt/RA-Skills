# Editing Validation — Syncfusion Blazor DataGrid

## Table of Contents

- [Per-Column ValidationRules](#per-column-validationrules)
- [Data Annotation Attributes](#data-annotation-attributes)
- [Custom Validation Attribute](#custom-validation-attribute)
- [Complex Type Validation](#complex-type-validation)
- [Custom Validator Component](#custom-validator-component)

## Per-Column ValidationRules

Define rules directly on `GridColumn` using the `ValidationRules` attribute:

```razor
<GridColumn Field="CustomerID" HeaderText="Customer"
            ValidationRules="@(new ValidationRules { Required = true, MinLength = 3, MaxLength = 8 })">
</GridColumn>

<GridColumn Field="Freight" EditType="EditType.NumericEdit"
            ValidationRules="@(new ValidationRules { Required = true, Min = 1, Max = 1000 })">
</GridColumn>
```

| Rule | Type | Description |
|---|---|---|
| `Required` | bool | Field must not be empty |
| `MinLength` | int | Minimum string length |
| `MaxLength` | int | Maximum string length |
| `Min` | int | Minimum numeric value — accepts whole numbers only (e.g., `Min = 1`) |
| `Max` | int | Maximum numeric value — accepts whole numbers only (e.g., `Max = 1000`)|
| `RegexPattern` | string | Must match regex pattern |
## Data Annotation Attributes

Apply directly on the model class. Supported attributes:

```csharp
using System.ComponentModel.DataAnnotations;

public class Order
{
    [Key]                                  // marks primary key column
    public int OrderID { get; set; }

    [Required]
    [StringLength(8, MinimumLength = 3)]
    public string CustomerID { get; set; }

    [Range(1, 1000)]
    public double Freight { get; set; }

    [RegularExpression(@"^[a-zA-Z\s]+$", ErrorMessage = "Letters only")]
    public string ShipCity { get; set; }

    [EmailAddress]
    public string ContactEmail { get; set; }

    [Display(Name = "Order Date")]         // sets column HeaderText
    public DateTime OrderDate { get; set; }

    [ScaffoldColumn(false)]                // hides column from auto-generate
    public string InternalNote { get; set; }

    [ReadOnly(true)]                       // prevents editing
    public string ReadOnlyField { get; set; }
}
```

**Full list of supported annotation attributes:**

| Attribute | Purpose |
|---|---|
| `[Key]` | Marks primary key (sets `IsPrimaryKey="true"`) |
| `[Required]` | Mandatory field |
| `[StringLength(max, MinimumLength=min)]` | String length range |
| `[Range(min, max)]` | Numeric range |
| `[RegularExpression(pattern)]` | Regex validation |
| `[MinLength(n)]` / `[MaxLength(n)]` | Min/max string length |
| `[EmailAddress]` | Email format |
| `[Compare("OtherField")]` | Must match another field |
| `[Display(Name="...")]` | Sets `HeaderText` |
| `[Display(Order=n)]` | Column display order |
| `[Display(AutoGenerateField=false)]` | Exclude from auto-generated columns |
| `[ScaffoldColumn(false)]` | Hides column in UI |
| `[ReadOnly(true)]` | Column is read-only |

> When both `[Display(Name="...")]` and column `HeaderText` are set, **`HeaderText` takes precedence**.

## Custom Validation Attribute

Inherit from `ValidationAttribute` and override `IsValid`:

```csharp
public class FreightRangeValidator : ValidationAttribute
{
    protected override ValidationResult IsValid(object value, ValidationContext ctx)
    {
        if (value is double freight && (freight < 1 || freight > 1000))
            return new ValidationResult("Freight must be between 1 and 1000",
                                        new[] { ctx.MemberName });
        return ValidationResult.Success;
    }
}

// Apply on model:
public class Order
{
    [FreightRangeValidator]
    public double Freight { get; set; }
}
```

## Complex Type Validation

Requires NuGet: `Microsoft.AspNetCore.Components.DataAnnotations.Validation`

```csharp
public class Order
{
    [ValidateComplexType]          // enables deep validation into nested object
    public Address ShipAddress { get; set; } = new();
}

public class Address
{
    [Required(ErrorMessage = "City is required")]
    public string City { get; set; }

    [Required]
    public string Country { get; set; }
}
```

> Use `Field="ShipAddress__City"` (double underscore) in `GridColumn` for nested property binding.

## Custom Validator Component

Pass a custom validator type via `GridEditSettings.Validator`:

```razor
<GridEditSettings AllowEditing="true" Validator="@typeof(CustomValidator)">
</GridEditSettings>
```

```csharp
public class CustomValidator : ComponentBase
{
    [CascadingParameter]
    private EditContext EditContext { get; set; }

    [Parameter]
    public ValidatorTemplateContext Context { get; set; }

    private ValidationMessageStore MessageStore;

    protected override void OnInitialized()
    {
        MessageStore = new ValidationMessageStore(EditContext);
        EditContext.OnValidationRequested += (s, e) =>
        {
            MessageStore.Clear();
            var data = Context.Data as Order;
            if (data?.Freight < 0)
                MessageStore.Add(EditContext.Field("Freight"), "Freight cannot be negative");
            EditContext.NotifyValidationStateChanged();
        };
    }
}
```

> **Validation timing:** Messages re-trigger only on form submit or field blur — this is standard Microsoft Blazor `EditForm` behavior.
