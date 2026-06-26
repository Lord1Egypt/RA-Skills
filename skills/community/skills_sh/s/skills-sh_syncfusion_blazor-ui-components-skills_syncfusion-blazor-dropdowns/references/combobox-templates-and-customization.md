# Templates & Customization in ComboBox

## Table of Contents

- [Item Template](#item-template)
- [Group Template](#group-template)
- [Header Template](#header-template)
- [Footer Template](#footer-template)
- [Value Template](#value-template)
- [No Records Template](#no-records-template)
- [Customization Best Practices](#customization-best-practices)

---

## Item Template

Customize the appearance of each list item using the `ItemTemplate` property:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Employee">
        <ItemTemplate>
            <div style="padding: 5px; border-bottom: 1px solid #e0e0e0;">
                <div style="font-weight: bold;">@context.Name</div>
                <div style="font-size: 0.9em; color: #666;">@context.Department - $@context.Salary</div>
            </div>
        </ItemTemplate>
    </ComboBoxTemplates>
</SfComboBox>

@code {
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
        new Employee { EmployeeId = 2, Name = "Jane Doe", Department = "HR", Salary = 65000 },
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Department = "Sales", Salary = 55000 }
    };
}
```

---

## Group Template

Customize group headers when data is grouped:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees"
    Fields="@Fields">
    <ComboBoxTemplates TItem="Employee">
        <GroupTemplate>
            <div style="padding: 10px; background-color: #f0f0f0; font-weight: bold;">
                <span>📁 @context.Department</span>
            </div>
        </GroupTemplate>
        <ItemTemplate>
            <div style="padding: 8px; padding-left: 20px;">
                <span>👤 @context.Name</span>
            </div>
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

    private ComboBoxFieldSettings Fields = new ComboBoxFieldSettings
    {
        Text = "Name",
        Value = "EmployeeId",
        GroupBy = "Department"
    };

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith", Department = "IT" },
        new Employee { EmployeeId = 2, Name = "Jane Doe", Department = "HR" },
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Department = "IT" },
        new Employee { EmployeeId = 4, Name = "Sarah Lee", Department = "HR" }
    };
}
```

---

## Header Template

Add a custom header at the top of the popup list:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Product" TValue="int"
    Placeholder="Search products"
    DataSource="@Products"
    AllowFiltering="true">
    <ComboBoxFieldSettings Text="ProductName" Value="ProductId"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Product">
        <HeaderTemplate>
            <div style="padding: 15px; background-color: #007bff; color: white; font-weight: bold;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Product List</span>
                    <span>@Products.Count items</span>
                </div>
            </div>
        </HeaderTemplate>
        <ItemTemplate>
            <div style="padding: 8px; display: flex; justify-content: space-between;">
                <span>@context.ProductName</span>
                <span style="color: #28a745;">$@context.Price</span>
            </div>
        </ItemTemplate>
    </ComboBoxTemplates>
</SfComboBox>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
        public decimal Price { get; set; }
    }

    private List<Product> Products = new()
    {
        new Product { ProductId = 1, ProductName = "Laptop", Price = 999 },
        new Product { ProductId = 2, ProductName = "Mouse", Price = 25 },
        new Product { ProductId = 3, ProductName = "Keyboard", Price = 75 }
    };
}
```

---

## Footer Template

Add a custom footer at the bottom of the popup list:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Employee">
        <FooterTemplate>
            <div style="padding: 10px; background-color: #f5f5f5; border-top: 1px solid #ddd; text-align: center;">
                <small>Total: @Employees.Count employees</small>
            </div>
        </FooterTemplate>
        <ItemTemplate>
            <div style="padding: 8px;">@context.Name</div>
        </ItemTemplate>
    </ComboBoxTemplates>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith" },
        new Employee { EmployeeId = 2, Name = "Jane Doe" },
        new Employee { EmployeeId = 3, Name = "Bob Johnson" }
    };
}
```

---

## Value Template

Customize how the selected value is displayed in the input field:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries"
    @bind-Value="@SelectedCountry">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Country">
        <ValueTemplate>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.2em;">🌍</span>
                <span>@context.Name (@context.Code)</span>
            </div>
        </ValueTemplate>
        <ItemTemplate>
            <div style="display: flex; justify-content: space-between; padding: 8px;">
                <span>@context.Name</span>
                <span style="color: #999;">@context.Code</span>
            </div>
        </ItemTemplate>
    </ComboBoxTemplates>
</SfComboBox>

@code {
    private string SelectedCountry = "USA";

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

---

## No Records Template

Display a message when no items match the filter:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Product" TValue="int"
    Placeholder="Search products"
    DataSource="@Products"
    AllowFiltering="true">
    <ComboBoxFieldSettings Text="ProductName" Value="ProductId"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Product">
        <NoRecordsTemplate>
            <div style="padding: 20px; text-align: center; color: #999;">
                <p style="font-size: 1.1em; margin-bottom: 10px;">😔 No Products Found</p>
                <p>Try searching with different keywords</p>
            </div>
        </NoRecordsTemplate>
        <ItemTemplate>
            <div style="padding: 8px;">@context.ProductName</div>
        </ItemTemplate>
    </ComboBoxTemplates>
</SfComboBox>

@code {
    public class Product
    {
        public int ProductId { get; set; }
        public string ProductName { get; set; }
    }

    private List<Product> Products = new()
    {
        new Product { ProductId = 1, ProductName = "Laptop" },
        new Product { ProductId = 2, ProductName = "Mouse" },
        new Product { ProductId = 3, ProductName = "Keyboard" }
    };
}
```

---

## Complex Item Template Example

Create a rich, multi-line item template with images and details:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees"
    PopupHeight="300px">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
    <ComboBoxTemplates TItem="Employee">
        <HeaderTemplate>
            <div style="padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd;">
                Available Employees
            </div>
        </HeaderTemplate>
        <ItemTemplate>
            <div style="padding: 10px; border-bottom: 1px solid #f0f0f0; min-height: 70px;">
                <div style="display: flex; gap: 10px;">
                    <div style="width: 50px; height: 50px; background-color: #007bff; color: white; 
                                display: flex; align-items: center; justify-content: center; 
                                border-radius: 50%; font-weight: bold;">
                        @context.Name.Substring(0, 1)
                    </div>
                    <div>
                        <div style="font-weight: bold; font-size: 1em;">@context.Name</div>
                        <div style="font-size: 0.9em; color: #666;">@context.Department</div>
                        <div style="font-size: 0.85em; color: #999;">@context.Email</div>
                    </div>
                </div>
            </div>
        </ItemTemplate>
        <FooterTemplate>
            <div style="padding: 10px; background-color: #f5f5f5; text-align: center; font-size: 0.9em;">
                Total: @Employees.Count employees
            </div>
        </FooterTemplate>
    </ComboBoxTemplates>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
        public string Email { get; set; }
    }

    private List<Employee> Employees = new()
    {
        new Employee { EmployeeId = 1, Name = "John Smith", Department = "IT", Email = "john@company.com" },
        new Employee { EmployeeId = 2, Name = "Jane Doe", Department = "HR", Email = "jane@company.com" },
        new Employee { EmployeeId = 3, Name = "Bob Johnson", Department = "Sales", Email = "bob@company.com" }
    };
}
```

---

## Customization Best Practices

1. **Keep Templates Lightweight**
   - Avoid complex logic in templates
   - Use simple HTML for better performance

2. **Use CSS Classes**
   ```razor
   <style>
       .combo-item { padding: 8px; }
       .combo-item-selected { background-color: #007bff; color: white; }
   </style>
   ```

3. **Make Templates Responsive**
   - Use flexbox for layout
   - Avoid fixed widths

4. **Handle Null Context**
   ```razor
   <ItemTemplate>
       @if (context != null)
       {
           <span>@context.Name</span>
       }
   </ItemTemplate>
   ```

5. **Test Template Rendering**
   - Test with empty data
   - Test with long text values
   - Test on mobile devices

---

## Troubleshooting

**Template not rendering?**
- Verify template property name is correct
- Check for null values in context
- Ensure component is properly bound to data

**Performance issues with templates?**
- Simplify template HTML
- Avoid expensive operations
- Use memoization for complex calculations

**Styling not applied?**
- Check CSS specificity
- Use inline styles if needed
- Verify theme CSS doesn't override styles

---

*See also: [Data Binding](data-binding.md), [Selection & Value](selection-and-value.md), [Getting Started](getting-started.md)*
