# Templates in Blazor Dialog

## Table of Contents
- [Overview](#overview)
- [DialogTemplates Structure](#dialogtemplates-structure)
- [Header Template](#header-template)
- [Content Template](#content-template)
- [Footer Template](#footer-template)
- [Advanced Template Patterns](#advanced-template-patterns)
- [Best Practices](#best-practices)

## Overview

The Blazor Dialog component provides comprehensive template support for customizing every section of the dialog: header, content, and footer. Templates enable you to embed complex HTML, Blazor components, forms, and dynamic data within the dialog, transforming it from a simple message box into a rich, interactive UI element.

**Key Benefits:**
- Full control over header appearance (icons, images, custom styling)
- Rich content areas supporting forms, grids, and other components
- Custom footer implementations without relying on DialogButtons
- Dynamic data binding within templates
- Responsive and accessible layouts

## DialogTemplates Structure

The `DialogTemplates` component acts as a container for template definitions. It provides three template properties:

```csharp
<SfDialog Width="400px">
    <DialogTemplates>
        <Header><!-- Custom header content --></Header>
        <Content><!-- Custom content area --></Content>
        <FooterTemplate><!-- Custom footer content --></FooterTemplate>
    </DialogTemplates>
</SfDialog>
```

> **Important:** `FooterTemplate` and `DialogButtons` are mutually exclusive. Use one or the other, not both.

## Header Template

The header section appears at the top of the dialog. Customize it with icons, images, titles, or any HTML/Blazor components.

### Basic Header with Icon

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="350px" ShowCloseIcon="true">
    <DialogTemplates>
        <Header>
            <span class="e-icons e-user-settings"></span>
            <span style="margin-left: 10px;">User Settings</span>
        </Header>
        <Content>Configure your user preferences here.</Content>
    </DialogTemplates>
</SfDialog>
```

### Header with Avatar and Info

```csharp
<SfDialog Width="400px" ShowCloseIcon="true">
    <DialogTemplates>
        <Header>
            <div style="display: flex; align-items: center;">
                <img src="user-avatar.png" 
                     style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;" />
                <div>
                    <strong>Nancy Davolio</strong>
                    <p style="font-size: 12px; margin: 0; color: #666;">Online</p>
                </div>
            </div>
        </Header>
        <Content>
            <p>How can I help you today?</p>
        </Content>
    </DialogTemplates>
</SfDialog>
```

### Header with Custom Styling

```csharp
<SfDialog Width="400px">
    <DialogTemplates>
        <Header>
            <div class="custom-header">
                <span class="e-icons e-info-small"></span>
                Important Notice
            </div>
        </Header>
        <Content>This is an important message.</Content>
    </DialogTemplates>
</SfDialog>

<style>
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
```

## Content Template

The content area is the main body of the dialog. It supports any HTML or Blazor components, enabling complex layouts.

### Content with Form Elements

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Inputs
@using Syncfusion.Blazor.Buttons

<SfDialog Width="400px" Header="User Registration">
    <DialogTemplates>
        <Content>
            <div class="form-group">
                <label for="name">Full Name:</label>
                <SfTextBox @bind-Value="@UserName" Placeholder="Enter your name" />
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <SfTextBox @bind-Value="@UserEmail" Type="InputType.Email" Placeholder="Enter your email" />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <SfTextBox @bind-Value="@UserPassword" Type="InputType.Password" Placeholder="Enter password" />
            </div>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private string UserName { get; set; }
    private string UserEmail { get; set; }
    private string UserPassword { get; set; }
}

<style>
    .form-group {
        margin-bottom: 15px;
    }

    .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
</style>
```

### Content with Data Grid

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Grids

<SfDialog Width="600px" Header="Employee Data">
    <DialogTemplates>
        <Content>
            <SfGrid DataSource="@EmployeeData">
                <GridColumns>
                    <GridColumn Field="EmployeeID" HeaderText="ID" Width="80"></GridColumn>
                    <GridColumn Field="FirstName" HeaderText="First Name" Width="100"></GridColumn>
                    <GridColumn Field="LastName" HeaderText="Last Name" Width="100"></GridColumn>
                    <GridColumn Field="Title" HeaderText="Title" Width="150"></GridColumn>
                </GridColumns>
            </SfGrid>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    public List<Employee> EmployeeData { get; set; }

    protected override void OnInitialized()
    {
        EmployeeData = new List<Employee>
        {
            new Employee { EmployeeID = 1, FirstName = "Nancy", LastName = "Davolio", Title = "Sales Rep" },
            new Employee { EmployeeID = 2, FirstName = "Andrew", LastName = "Fuller", Title = "Vice President" }
        };
    }

    public class Employee
    {
        public int EmployeeID { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Title { get; set; }
    }
}
```

### Content with Rich Text

```csharp
<SfDialog Width="450px" Header="Terms and Conditions">
    <DialogTemplates>
        <Content>
            <div class="terms-content">
                <h3>User Agreement</h3>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>
                <h4>Key Points:</h4>
                <ul>
                    <li>Users must be 18 years or older</li>
                    <li>All content must comply with regulations</li>
                    <li>Personal data will be protected</li>
                </ul>
            </div>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .terms-content {
        max-height: 300px;
        overflow-y: auto;
        font-size: 14px;
        line-height: 1.6;
    }

    .terms-content h3 {
        margin-top: 0;
        color: #333;
    }

    .terms-content ul {
        margin: 10px 0;
        padding-left: 20px;
    }
</style>
```

## Footer Template

The footer section allows custom content without using `DialogButtons`. Use it for custom button layouts or additional information.

### Basic Footer with Custom Buttons

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfDialog Width="400px" Header="Confirm Action" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>Are you sure you want to delete this item?</Content>
        <FooterTemplate>
            <div style="display: flex; justify-content: flex-end; gap: 10px;">
                <SfButton OnClick="@OnConfirm" IsPrimary="true">Delete</SfButton>
                <SfButton OnClick="@OnCancel">Cancel</SfButton>
            </div>
        </FooterTemplate>
    </DialogTemplates>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnConfirm()
    {
        // Handle delete action
        DialogVisible = false;
    }

    private void OnCancel()
    {
        DialogVisible = false;
    }
}
```

### Footer with Progress Indicator

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="400px" Header="Upload Progress">
    <DialogTemplates>
        <Content>
            <p>Uploading file: document.pdf</p>
            <div style="width: 100%; height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden;">
                <div style="width: 65%; height: 100%; background: #4caf50; transition: width 0.3s;"></div>
            </div>
        </Content>
        <FooterTemplate>
            <div style="text-align: right;">
                <p style="margin: 0;">Progress: 65%</p>
            </div>
        </FooterTemplate>
    </DialogTemplates>
</SfDialog>
```

### Footer with Info Text

```csharp
<SfDialog Width="400px" Header="Notification">
    <DialogTemplates>
        <Content>
            <p>Your password was changed successfully.</p>
        </Content>
        <FooterTemplate>
            <div style="padding: 10px; background: #f0f0f0; border-top: 1px solid #ccc;">
                <small>Last updated: 2024-03-18 at 10:30 AM</small>
            </div>
        </FooterTemplate>
    </DialogTemplates>
</SfDialog>
```

## Advanced Template Patterns

### Modal Dialog with Complex Form

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Inputs
@using Syncfusion.Blazor.DropDowns

<SfDialog Width="500px" IsModal="true" Header="Create New Project" @bind-Visible="ShowDialog">
    <DialogTemplates>
        <Content>
            <div class="form">
                <div class="form-row">
                    <label>Project Name:</label>
                    <SfTextBox @bind-Value="@ProjectName" Placeholder="Enter project name" />
                </div>
                <div class="form-row">
                    <label>Category:</label>
                    <SfDropDownList TValue="string" TItem="string" 
                                    DataSource="@Categories" 
                                    @bind-Value="@SelectedCategory" />
                </div>
                <div class="form-row">
                    <label>Description:</label>
                    <textarea style="width: 100%; height: 100px; padding: 8px;">@ProjectDescription</textarea>
                </div>
            </div>
        </Content>
        <FooterTemplate>
            <div style="display: flex; justify-content: space-between;">
                <SfButton OnClick="@ResetForm">Reset</SfButton>
                <div>
                    <SfButton OnClick="@CancelDialog">Cancel</SfButton>
                    <SfButton OnClick="@SaveProject" IsPrimary="true" style="margin-left: 10px;">Create</SfButton>
                </div>
            </div>
        </FooterTemplate>
    </DialogTemplates>
</SfDialog>

@code {
    private bool ShowDialog { get; set; } = true;
    private string ProjectName { get; set; }
    private string ProjectDescription { get; set; }
    private string SelectedCategory { get; set; }
    private List<string> Categories = new() { "Web", "Desktop", "Mobile" };

    private void SaveProject() => ShowDialog = false;
    private void CancelDialog() => ShowDialog = false;
    private void ResetForm()
    {
        ProjectName = "";
        ProjectDescription = "";
        SelectedCategory = "";
    }
}

<style>
    .form {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .form-row {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .form-row label {
        font-weight: bold;
    }
</style>
```

## Best Practices

1. **Keep Templates Lean**: Avoid embedding too much logic; use code-behind or separate components
2. **Template Responsiveness**: Use flexbox or grid for responsive template layouts
3. **Content Scrolling**: For long content, add CSS overflow rules to prevent dialog overflow
4. **Accessibility**: Include proper labels and ARIA attributes in templates
5. **Event Handling**: Use event handlers to manage form submissions and dialog closing
6. **Component Reusability**: Create reusable Blazor components for common template patterns
7. **Performance**: Lazy-load data when using data grids in dialog content
8. **Styling Consistency**: Apply consistent spacing and styling across all template sections

## Common Template Gotchas

- **Mixing FooterTemplate and DialogButtons**: These are mutually exclusive; choose one approach
- **Two-Way Binding**: Use `@bind-Value` to enable two-way data binding in template inputs
- **Event Callbacks**: Ensure event handlers are properly defined in the `@code` block
- **Dynamic Content**: Refresh templates by changing component state or triggering re-renders
