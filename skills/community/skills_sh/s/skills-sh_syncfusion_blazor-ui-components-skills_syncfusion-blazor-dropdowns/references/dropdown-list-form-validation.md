# Form Validation with Syncfusion Blazor DropDown List

## EditForm Integration

### Basic Form Validation

Integrate the dropdown with Blazor's EditForm for validation:

```razor
<EditForm Model="@FormModel">
    <DataAnnotationsValidator />
    <ValidationSummary />
    
    <div class="form-group">
        <label>Select Department *</label>
        <SfDropDownList TValue="string" TItem="string" @bind-Value="FormModel.SelectedDepartment"
                        DataSource="@Departments"
                        Placeholder="Choose department">
        </SfDropDownList>
        <ValidationMessage For="@(() => FormModel.SelectedDepartment)" />
    </div>
    
    <button type="submit">Submit</button>
</EditForm>

@code {
    private FormData FormModel = new();
    private List<string> Departments = new() { "Sales", "Engineering", "Marketing" };

    private class FormData
    {
        [Required(ErrorMessage = "Department is required")]
        public string SelectedDepartment { get; set; }
    }
}
```

### Complex Model Validation

Validate dropdown selections in complex forms:

```razor
<EditForm Model="@EmployeeForm" OnValidSubmit="@HandleValidSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary />
    
    <div class="form-group">
        <label>Employee Name *</label>
        <InputText @bind-Value="EmployeeForm.Name" placeholder="Enter name" />
        <ValidationMessage For="@(() => EmployeeForm.Name)" />
    </div>
    
    <div class="form-group">
        <label>Department *</label>
        <SfDropDownList TValue="int" TItem="Department" @bind-Value="EmployeeForm.DepartmentId"
                        DataSource="@Departments"
                        Placeholder="Select department">
            <DropDownListFieldSettings Text="@nameof(Department.Name)" Value="@nameof(Department.Id)" />
        </SfDropDownList>
        <ValidationMessage For="@(() => EmployeeForm.DepartmentId)" />
    </div>
    
    <div class="form-group">
        <label>Role *</label>
        <SfDropDownList TValue="int" TItem="Role" @bind-Value="EmployeeForm.RoleId"
                        DataSource="@Roles"
                        Placeholder="Select role">
            <DropDownListFieldSettings Text="@nameof(Role.Name)" Value="@nameof(Role.Id)" />
        </SfDropDownList>
        <ValidationMessage For="@(() => EmployeeForm.RoleId)" />
    </div>
    
    <button type="submit" class="btn btn-primary">Save</button>
</EditForm>

@code {
    private EmployeeFormData EmployeeForm = new();
    private List<Department> Departments;
    private List<Role> Roles;



    private void HandleValidSubmit()
    {
        Console.WriteLine("Form is valid, submitting...");
    }

    protected override void OnInitialized()
    {
        Departments = new List<Department>
        {
            new Department { Id = 1, Name = "Engineering" },
            new Department { Id = 2, Name = "Sales" },
            new Department { Id = 3, Name = "Marketing" }
        };

        Roles = new List<Role>
        {
            new Role { Id = 1, Name = "Developer" },
            new Role { Id = 2, Name = "Manager" },
            new Role { Id = 3, Name = "Analyst" }
        };
    }

    private class EmployeeFormData
    {
        [Required(ErrorMessage = "Name is required")]
        [StringLength(100, MinimumLength = 2)]
        public string Name { get; set; }

        [Required(ErrorMessage = "Department is required")]
        [Range(1, int.MaxValue, ErrorMessage = "Please select a valid department")]
        public int DepartmentId { get; set; }

        [Required(ErrorMessage = "Role is required")]
        public int RoleId { get; set; }
    }

    private class Department
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }

    private class Role
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Data Annotation Validation

### Required Validation

Make dropdown selection mandatory:

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedOption"
                DataSource="@Options"
                Placeholder="Required field *">
</SfDropDownList>

@code {
    private string SelectedOption;

    private class FormModel
    {
        [Required(ErrorMessage = "This field is required")]
        public string SelectedOption { get; set; }
    }
}
```

### Range Validation

Validate selected value is within a range:

```razor
<SfDropDownList TValue="int" TItem="int" @bind-Value="FormModel.Priority"
                DataSource="@PriorityLevels"
                Placeholder="Select priority">
</SfDropDownList>

@code {
    private FormData FormModel = new();
    private List<int> PriorityLevels = new() { 1, 2, 3, 4, 5 };

    private class FormData
    {
        [Range(1, 5, ErrorMessage = "Priority must be between 1 and 5")]
        public int Priority { get; set; }
    }
}
```

### Custom Validation Rules

Create custom validation attributes:

```razor
<EditForm Model="@Model">
    <DataAnnotationsValidator />
    <ValidationSummary />
    
    <SfDropDownList TValue="int" TItem="Employee" @bind-Value="Model.EmployeeId"
                    DataSource="@Employees"
                    Placeholder="Select employee">
        <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    </SfDropDownList>
    <ValidationMessage For="@(() => Model.EmployeeId)" />
    
    <button type="submit">Submit</button>
</EditForm>

@code {
    private FormData Model = new();
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice", Status = "Active" },
            new Employee { Id = 2, Name = "Bob", Status = "Inactive" }
        };
    }

    private class FormData
    {
        [Required(ErrorMessage = "Employee is required")]
        [ValidateActiveEmployee(ErrorMessage = "Selected employee must be active")]
        public int EmployeeId { get; set; }
    }

    // Custom validation attribute
    private class ValidateActiveEmployeeAttribute : ValidationAttribute
    {
        protected override ValidationResult IsValid(object value, ValidationContext context)
        {
            // Custom validation logic
            return ValidationResult.Success;
        }
    }

    private class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Status { get; set; }
    }
}
```

## Validation Error Display

### Show Validation Messages

Display validation errors below the dropdown:

```razor
<div class="form-group">
    <label>Select Status *</label>
    <SfDropDownList TValue="string" TItem="string" @bind-Value="FormModel.Status"
                    DataSource="@StatusOptions"
                    Placeholder="Choose status"
                    CssClass="@(HasValidationError ? "is-invalid" : "")">
    </SfDropDownList>
    <ValidationMessage For="@(() => FormModel.Status)" 
                       class="@(HasValidationError ? "d-block" : "d-none")" />
</div>

@code {
    private FormData FormModel = new();
    private List<string> StatusOptions = new() { "Active", "Inactive", "Pending" };
    private bool HasValidationError;

    private class FormData
    {
        [Required(ErrorMessage = "Status is required")]
        public string Status { get; set; }
    }
}
```

### Highlight Invalid Fields

Apply CSS classes to highlight validation errors:

```razor
<style>
    .form-group.has-error .e-ddl {
        border-color: #dc3545 !important;
        background-color: #fff5f5;
    }
    
    .validation-message {
        color: #dc3545;
        font-size: 0.9em;
        margin-top: 4px;
    }
</style>

<div class="form-group @(HasErrors ? "has-error" : "")">
    <label>Select Department *</label>
    <SfDropDownList TValue="string" TItem="string" @bind-Value="FormModel.Department"
                    DataSource="@Departments"
                    Placeholder="Select department">
    </SfDropDownList>
    @if (HasErrors)
    {
        <div class="validation-message">Department is required</div>
    }
</div>

@code {
    private FormData FormModel = new();
    private bool HasErrors;
    private List<string> Departments = new() { "Sales", "Engineering", "Marketing" };

    private class FormData
    {
        public string Department { get; set; }
    }
}
```

## Form Submission Patterns

### Validate Before Submit

Validate all form data before submission:

```razor
<EditForm Model="@FormModel" OnSubmit="@HandleSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary />
    
    <SfDropDownList TValue="int" TItem="int" @bind-Value="FormModel.SelectedId"
                    DataSource="@Items"
                    Placeholder="Select item">
    </SfDropDownList>
    
    <button type="submit">Submit</button>
</EditForm>

@code {
    private FormData FormModel = new();
    private List<int> Items = new() { 1, 2, 3 };

    private async Task HandleSubmit()
    {
        // Form validation happens automatically
        // This is only called if validation passes
        Console.WriteLine($"Form submitted with value: {FormModel.SelectedId}");
        await Task.Delay(500);
    }

    private class FormData
    {
        [Required]
        public int SelectedId { get; set; }
    }
}
```

### Async Form Submission

Handle async operations during form submission:

```razor
<EditForm Model="@FormModel" OnSubmit="@HandleSubmitAsync">
    <DataAnnotationsValidator />
    
    <div class="form-group">
        <label>Select Option *</label>
<SfDropDownList TValue="int" TItem="Option" @bind-Value="FormModel.OptionId"
                    DataSource="@Options"
                    Disabled="@IsSubmitting"
                    Placeholder="Choose option">
            <DropDownListFieldSettings Text="@nameof(Option.Name)" Value="@nameof(Option.Id)" />
        </SfDropDownList>
    </div>
    
    <button type="submit" disabled="@IsSubmitting">
        @(IsSubmitting ? "Submitting..." : "Submit")
    </button>
</EditForm>

@code {
    private FormData FormModel = new();
    private bool IsSubmitting;
    private List<Option> Options;

    private async Task HandleSubmitAsync()
    {
        IsSubmitting = true;
        try
        {
            // Simulate API call
            await Task.Delay(2000);
            Console.WriteLine($"Successfully submitted: {FormModel.OptionId}");
        }
        finally
        {
            IsSubmitting = false;
        }
    }

    protected override void OnInitialized()
    {
        Options = new List<Option>
        {
            new Option { Id = 1, Name = "Option A" },
            new Option { Id = 2, Name = "Option B" }
        };
    }

    private class FormData
    {
        [Required(ErrorMessage = "Option is required")]
        public int OptionId { get; set; }
    }

    private class Option
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Complete Validation Example

```razor
@page "/dropdown-validation"

<EditForm Model="@RegistrationForm" OnValidSubmit="@HandleValidSubmit">
    <DataAnnotationsValidator />
    <ValidationSummary class="alert alert-danger" />
    
    <h3>Registration Form</h3>
    
    <div class="form-group">
        <label>Full Name *</label>
        <InputText @bind-Value="RegistrationForm.FullName" 
                   placeholder="Enter your name"
                   class="form-control" />
        <ValidationMessage For="@(() => RegistrationForm.FullName)" class="text-danger" />
    </div>
    
    <div class="form-group">
        <label>Country *</label>
        <SfDropDownList TValue="int" TItem="Country" @bind-Value="RegistrationForm.CountryId"
                        DataSource="@Countries"
                        Placeholder="Select country"
                        class="form-control">
            <DropDownListFieldSettings Text="@nameof(Country.Name)" Value="@nameof(Country.Id)" />
        </SfDropDownList>
        <ValidationMessage For="@(() => RegistrationForm.CountryId)" class="text-danger" />
    </div>
    
    <div class="form-group">
        <label>Department *</label>
        <SfDropDownList TValue="int" TItem="Department" @bind-Value="RegistrationForm.DepartmentId"
                        DataSource="@Departments"
                        Placeholder="Select department"
                        class="form-control">
            <DropDownListFieldSettings Text="@nameof(Department.Name)" Value="@nameof(Department.Id)" />
        </SfDropDownList>
        <ValidationMessage For="@(() => RegistrationForm.DepartmentId)" class="text-danger" />
    </div>
    
    <button type="submit" class="btn btn-primary" disabled="@IsSubmitting">
        @(IsSubmitting ? "Registering..." : "Register")
    </button>
</EditForm>

@if (!string.IsNullOrEmpty(SuccessMessage))
{
    <div class="alert alert-success mt-3">@SuccessMessage</div>
}

@code {
    private RegistrationFormData RegistrationForm = new();
    private bool IsSubmitting;
    private string SuccessMessage;
    private List<Country> Countries;
    private List<Department> Departments;

    private async Task HandleValidSubmit()
    {
        IsSubmitting = true;
        try
        {
            await Task.Delay(1000);
            SuccessMessage = $"Registration successful! Welcome {RegistrationForm.FullName}";
            RegistrationForm = new();
        }
        finally
        {
            IsSubmitting = false;
        }
    }

    protected override void OnInitialized()
    {
        Countries = new List<Country>
        {
            new Country { Id = 1, Name = "United States" },
            new Country { Id = 2, Name = "Canada" },
            new Country { Id = 3, Name = "Mexico" }
        };

        Departments = new List<Department>
        {
            new Department { Id = 1, Name = "Engineering" },
            new Department { Id = 2, Name = "Sales" },
            new Department { Id = 3, Name = "Marketing" }
        };
    }

    private class RegistrationFormData
    {
        [Required(ErrorMessage = "Full name is required")]
        [StringLength(100, MinimumLength = 2)]
        public string FullName { get; set; }

        [Required(ErrorMessage = "Country is required")]
        public int CountryId { get; set; }

        [Required(ErrorMessage = "Department is required")]
        public int DepartmentId { get; set; }
    }

    private class Country
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }

    private class Department
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
}
```

## Key Takeaways

- Use EditForm wrapper for validation
- Apply data annotations for validation rules
- Display validation messages with ValidationMessage component
- Validate before form submission
- Use custom validation attributes for complex rules
- Disable submit button during submission
- Provide clear error messages to users
- Use ValidationSummary for overall feedback
- Handle async operations during submission
