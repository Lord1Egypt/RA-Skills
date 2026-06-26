# Templates and Rendering in Syncfusion Blazor DropDown List

## Table of Contents
- [Overview](#overview)
- [Item Template](#item-template)
- [Header and Footer Templates](#header-and-footer-templates)
- [Value Template](#value-template)
- [Complex Templates](#complex-templates)
- [Conditional Rendering](#conditional-rendering)

## Overview

Templates allow you to customize how items are rendered in the dropdown list. Instead of displaying plain text, you can create rich, formatted content with images, HTML, and conditional logic.

**Common use cases:**
- Display user profiles with images
- Show product details (name, price, stock)
- Format dates and numbers
- Color-code items by status
- Add icons or badges

## Item Template

### Basic Item Template

The `ItemTemplate` controls how each item appears in the dropdown list:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListTemplates TItem="Employee">
        <ItemTemplate>
            <span>@context.Name - @context.Department</span>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice", Department = "Engineering" },
            new Employee { Id = 2, Name = "Bob", Department = "Sales" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

### Item Template with Rich Content

Create items with multiple elements:

```razor
<SfDropDownList TValue="int" TItem="Product" DataSource="@Products">
    <DropDownListFieldSettings Text="@nameof(Product.Name)" Value="@nameof(Product.Id)" />
    <DropDownListTemplates TItem="Product">
        <ItemTemplate>
            <div style="padding: 8px;">
                <strong>@context.Name</strong>
                <div style="font-size: 0.9em; color: #666;">
                    Price: $@context.Price.ToString("F2")
                </div>
                <div style="font-size: 0.85em; color: #999;">
                    Stock: @context.Stock units
                </div>
            </div>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<Product> Products;

    protected override void OnInitialized()
    {
        Products = new List<Product>
        {
            new Product { Id = 1, Name = "Laptop", Price = 999.99m, Stock = 5 },
            new Product { Id = 2, Name = "Mouse", Price = 29.99m, Stock = 50 }
        };
    }

    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public decimal Price { get; set; }
        public int Stock { get; set; }
    }
}
```

## Header and Footer Templates

### Header Template

Display content above the list items:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items">
    <DropDownListTemplates TItem="string">
        <HeaderTemplate>
            <div style="padding: 8px; background: #f0f0f0; font-weight: bold;">
                Available Options
            </div>
        </HeaderTemplate>
        <ItemTemplate>
            @context
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

### Footer Template

Display content below the list items:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                Placeholder="Select">
    <DropDownListTemplates TItem="string">
        <ItemTemplate>
            @context
        </ItemTemplate>
        <FooterTemplate>
            <div style="padding: 8px; border-top: 1px solid #ddd; text-align: center;">
                <a href="#" style="font-size: 0.9em;">See all options</a>
            </div>
        </FooterTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

## Value Template

### Displaying Selected Value Differently

The `ValueTemplate` controls how the selected value appears in the closed dropdown:

```razor
<SfDropDownList TValue="int" TItem="Employee" DataSource="@Employees"
                @bind-Value="SelectedEmployeeId">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListTemplates TItem="Employee">
        <ItemTemplate>
            <div>
                <strong>@context.Name</strong> (@context.Title)
            </div>
        </ItemTemplate>
        <ValueTemplate>
            <div style="padding: 4px;">
                👤 @(Employees?.FirstOrDefault(e => e.Id == SelectedEmployeeId)?.Name ?? "Select Employee")
            </div>
        </ValueTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private int SelectedEmployeeId;
    private List<Employee> Employees;

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice", Title = "Manager" },
            new Employee { Id = 2, Name = "Bob", Title = "Developer" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Title { get; set; }
    }
}
```

## Complex Templates

### Status Badge Template

Create items with status indicators:

```razor
<SfDropDownList TValue="int" TItem="Order" DataSource="@Orders">
    <DropDownListFieldSettings Text="@nameof(Order.CustomerName)" Value="@nameof(Order.OrderId)" />
    <DropDownListTemplates TItem="Order">
        <ItemTemplate>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>@context.OrderId - @context.CustomerName</span>
                <span style="@GetStatusStyle(context.Status)">
                    @context.Status
                </span>
            </div>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<Order> Orders;

    private string GetStatusStyle(string status)
    {
        return status switch
        {
            "Pending" => "padding: 2px 6px; background: #ffc107; border-radius: 3px; font-size: 0.85em;",
            "Completed" => "padding: 2px 6px; background: #28a745; color: white; border-radius: 3px; font-size: 0.85em;",
            "Cancelled" => "padding: 2px 6px; background: #dc3545; color: white; border-radius: 3px; font-size: 0.85em;",
            _ => "padding: 2px 6px; background: #6c757d; color: white; border-radius: 3px; font-size: 0.85em;"
        };
    }

    protected override void OnInitialized()
    {
        Orders = new List<Order>
        {
            new Order { OrderId = 1001, CustomerName = "Alice", Status = "Pending" },
            new Order { OrderId = 1002, CustomerName = "Bob", Status = "Completed" },
            new Order { OrderId = 1003, CustomerName = "Carol", Status = "Cancelled" }
        };
    }

    public class Order
    {
        public int OrderId { get; set; }
        public string CustomerName { get; set; }
        public string Status { get; set; }
    }
}
```

### Currency Formatted Template

Format numeric values in templates:

```razor
<SfDropDownList TValue="int" TItem="PriceItem" DataSource="@Prices">
    <DropDownListFieldSettings Text="@nameof(PriceItem.ProductName)" Value="@nameof(PriceItem.Id)" />
    <DropDownListTemplates TValue="PriceItem">
        <ItemTemplate>
            <div style="display: flex; justify-content: space-between;">
                <span>@context.ProductName</span>
                <strong style="color: #28a745;">$@context.Amount.ToString("F2")</strong>
            </div>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<PriceItem> Prices;

    protected override void OnInitialized()
    {
        Prices = new List<PriceItem>
        {
            new PriceItem { Id = 1, ProductName = "Laptop", Amount = 999.99m },
            new PriceItem { Id = 2, ProductName = "Mouse", Amount = 29.99m },
            new PriceItem { Id = 3, ProductName = "Keyboard", Amount = 79.99m }
        };
    }

    public class PriceItem
    {
        public int Id { get; set; }
        public string ProductName { get; set; }
        public decimal Amount { get; set; }
    }
}
```

## Conditional Rendering

### Render Based on Conditions

Show different content based on item properties:

```razor
<SfDropDownList TValue="int" TItem="Task" DataSource="@Tasks">
    <DropDownListFieldSettings Text="@nameof(Task.Title)" Value="@nameof(Task.Id)" />
    <DropDownListTemplates TValue="Task">
        <ItemTemplate>
            <div>
                <span>@context.Title</span>
                @if (context.Priority == "High")
                {
                    <span style="color: #dc3545; font-weight: bold;"> ⚠️ HIGH</span>
                }
                else if (context.Priority == "Medium")
                {
                    <span style="color: #ffc107;"> ⚡ MEDIUM</span>
                }
                else
                {
                    <span style="color: #28a745;"> ✓ LOW</span>
                }
            </div>
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<Task> Tasks;

    protected override void OnInitialized()
    {
        Tasks = new List<Task>
        {
            new Task { Id = 1, Title = "Fix critical bug", Priority = "High" },
            new Task { Id = 2, Title = "Update documentation", Priority = "Low" },
            new Task { Id = 3, Title = "Refactor module", Priority = "Medium" }
        };
    }

    public class Task
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Priority { get; set; }
    }
}
```

### Disabled Items with Templates

Indicate disabled items visually:

```razor
<SfDropDownList TValue="int" TItem="MenuItem" DataSource="@Items">
    <DropDownListFieldSettings Text="@nameof(MenuItem.Name)" Value="@nameof(MenuItem.Id)" />
    <DropDownListTemplates TValue="MenuItem">
        <ItemTemplate>
            @if (context.IsDisabled)
            {
                <span style="opacity: 0.5; text-decoration: line-through;">
                    @context.Name (Unavailable)
                </span>
            }
            else
            {
                <span>@context.Name</span>
            }
        </ItemTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private List<MenuItem> Items;

    protected override void OnInitialized()
    {
        Items = new List<MenuItem>
        {
            new MenuItem { Id = 1, Name = "Option A", IsDisabled = false },
            new MenuItem { Id = 2, Name = "Option B", IsDisabled = true },
            new MenuItem { Id = 3, Name = "Option C", IsDisabled = false }
        };
    }

    public class MenuItem
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public bool IsDisabled { get; set; }
    }
}
```

## Complete Template Example

```razor
@page "/dropdown-templates"

<h3>Advanced Template Example</h3>

<SfDropDownList TValue="int" TItem="Employee"
                DataSource="@Employees"
                @bind-Value="SelectedEmployeeId">
    <DropDownListFieldSettings Text="@nameof(Employee.Name)" Value="@nameof(Employee.Id)" />
    <DropDownListTemplates TValue="Employee">
        <HeaderTemplate>
            <div style="padding: 8px; background: #f8f9fa; font-weight: bold; border-bottom: 1px solid #dee2e6;">
                Select Employee
            </div>
        </HeaderTemplate>
        
        <ItemTemplate>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px;">
                <div>
                    <strong>@context.Name</strong>
                    <div style="font-size: 0.85em; color: #666;">@context.Department</div>
                </div>
                <div style="font-size: 0.9em; color: #999;">@context.Email</div>
            </div>
        </ItemTemplate>
        
        <ValueTemplate>
            @{
                var selected = Employees?.FirstOrDefault(e => e.Id == SelectedEmployeeId);
                if (selected != null)
                {
                    <div>👤 @selected.Name</div>
                }
                else
                {
                    <div>Select an employee</div>
                }
            }
        </ValueTemplate>
        
        <FooterTemplate>
            <div style="padding: 8px; border-top: 1px solid #dee2e6; text-align: center; font-size: 0.85em;">
                Total: @Employees?.Count employees
            </div>
        </FooterTemplate>
    </DropDownListTemplates>
</SfDropDownList>

@code {
    private int SelectedEmployeeId;
    private List<Employee> Employees;

    private DropDownListFieldSettings ListFields { get; set; } = new()
    {
        Text = nameof(Employee.Name),
        Value = nameof(Employee.Id)
    };

    protected override void OnInitialized()
    {
        Employees = new List<Employee>
        {
            new Employee { Id = 1, Name = "Alice Johnson", Department = "Engineering", Email = "alice@company.com" },
            new Employee { Id = 2, Name = "Bob Smith", Department = "Sales", Email = "bob@company.com" },
            new Employee { Id = 3, Name = "Carol White", Department = "Marketing", Email = "carol@company.com" }
        };
    }

    public class Employee
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
        public string Email { get; set; }
    }
}
```

## Key Takeaways

- Use `ItemTemplate` to customize how items appear
- Use `ValueTemplate` to customize the selected value display
- Add `HeaderTemplate` and `FooterTemplate` for additional UI
- Leverage `@context` to access item properties
- Use conditional rendering for dynamic content
- Format numbers, dates, and text appropriately
- Consider accessibility when using icons and colors
- Test templates with different screen sizes
