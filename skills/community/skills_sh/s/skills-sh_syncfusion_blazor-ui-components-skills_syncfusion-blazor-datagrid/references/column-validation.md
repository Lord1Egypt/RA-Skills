# Column Validation — Syncfusion Blazor DataGrid

## Table of Contents
1. [Column Validation](#column-validation)
2. [Validation Rules](#validation-rules)
3. [Data Annotations](#data-annotations)
4. [Custom Validation](#custom-validation)
5. [Validation Events](#validation-events)

---

## Column Validation

Column validation ensures that edited or newly added row data meets specific criteria before being saved:

```razor
<SfGrid DataSource="@OrderData" Toolbar="@(new List<string>() { "Add", "Edit","Delete", "Update", "Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true" 
                    Mode="EditMode.Normal"></GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" HeaderText="Order ID" IsPrimaryKey="true" 
                  ValidationRules="@(new ValidationRules{ Required=true, Min=1})" 
                  Width="120"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer Name" 
                  ValidationRules="@(new ValidationRules{ Required=true, MinLength=3})" 
                  Width="120"></GridColumn>
        <GridColumn Field="Freight" HeaderText="Freight" 
                  ValidationRules="@(new ValidationRules{ Required=true, Min=1, Max=1000})" 
                  Format="C2" Width="120"></GridColumn>
    </GridColumns>
</SfGrid>
```

Benefits:
- Prevent invalid data entry
- Ensure data integrity
- Provide user feedback
- Enforce business rules

---

## Validation Rules

Use the `ValidationRules` property to define validation constraints:

```razor
<GridColumn Field="OrderID" HeaderText="Order ID" 
          ValidationRules="@(new ValidationRules{ Required=true, Min=1, Max=999999})">
</GridColumn>

<GridColumn Field="CustomerID" HeaderText="Customer" 
          ValidationRules="@(new ValidationRules{ Required=true, MinLength=3, MaxLength=50})">
</GridColumn>

<GridColumn Field="Email" HeaderText="Email" 
          ValidationRules="@(new ValidationRules{ Required=true, RegexPattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"})">
</GridColumn>
```

Available validation rules:
- **Required**: Field must have a value
- **Min**: Minimum numeric value
- **Max**: Maximum numeric value
- **MinLength**: Minimum string length
- **MaxLength**: Maximum string length
- **RegexPattern**: Regular expression pattern matching

---

## Data Annotations

Use data annotation attributes to define validation at the model level:

```csharp
public class OrderDetails
{
    [Required]
    public int OrderID { get; set; }
    
    [Required]
    [StringLength(50, MinimumLength = 3)]
    public string CustomerID { get; set; }
    
    [Range(0.01, 10000)]
    public double Freight { get; set; }
    
    [EmailAddress]
    public string Email { get; set; }
    
    [DataType(DataType.Date)]
    public DateTime? OrderDate { get; set; }
}
```

Supported attributes:
- `[Required]`: Field is mandatory
- `[StringLength]`: String length constraints
- `[Range]`: Numeric range
- `[EmailAddress]`: Email format validation
- `[RegularExpression]`: Pattern matching
- `[DataType]`: Data type specific validation

To use data annotations in Grid:

```razor
<SfGrid DataSource="@OrderData" Toolbar="@(new List<string>() { "Add", "Edit", "Update", "Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" Mode="EditMode.Dialog">
        <Validator>
            <DataAnnotationsValidator></DataAnnotationsValidator>
        </Validator>
    </GridEditSettings>
</SfGrid>
```

---

## Custom Validation

Implement custom validation logic by creating a validation class:

```csharp
public class CustomValidationFreight : ValidationAttribute
{
    protected override ValidationResult IsValid(object value, ValidationContext validationContext)
    {
        if (value != null)
        {
            double freightValue = Convert.ToDouble(value);
            if (freightValue >= 1 && freightValue <= 10000)
            {
                return ValidationResult.Success;
            }
            else
            {
                return new ValidationResult("Freight value should be between 1 and 10,000");
            }
        }
        else
        {
            return new ValidationResult("Freight value is required");
        }
    }
}

public class OrderDetails
{
    [CustomValidationFreight]
    public double Freight { get; set; }
}
```

Using custom validator:

```razor
<SfGrid DataSource="@OrderData" Toolbar="@(new List<string>() { "Add", "Edit", "Update", "Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" Mode="EditMode.Dialog">
        <Validator>
            <DataAnnotationsValidator></DataAnnotationsValidator>
        </Validator>
    </GridEditSettings>
</SfGrid>
```

---

## Validation Events

Handle validation events for custom logic:

```razor
<SfGrid @ref="Grid" DataSource="@OrderData" Toolbar="@(new List<string>() { "Add", "Edit", "Update", "Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" Mode="EditMode.Dialog">
        <Validator>
            <DataAnnotationsValidator></DataAnnotationsValidator>
        </Validator>
    </GridEditSettings>
    <GridEvents ActionFailure="OnValidationFailed" ActionComplete="OnActionComplete" 
               TValue="OrderData"></GridEvents>
</SfGrid>

@code {
    private SfGrid<OrderData> Grid;
    
    public void OnValidationFailed(FailedEventArgs args)
    {
        // Handle validation failure
        // args.Error contains error details
    }
    
    public void OnActionComplete(ActionEventArgs<OrderData> args)
    {
        if (args.RequestType == Action.Save)
        {
            // Data saved successfully after validation
        }
    }
}
```

Available events:
- **ActionFailure**: Triggered when validation fails
- **ActionComplete**: Triggered after successful action
- **ActionBegin**: Triggered before action starts

