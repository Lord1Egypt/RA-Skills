# Accessibility and Templates

## Table of Contents
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Attributes](#aria-attributes)
- [Screen Reader Support](#screen-reader-support)
- [Focus Management](#focus-management)
- [Item Templates](#item-templates)
- [Group Templates](#group-templates)
- [Header and Footer Templates](#header-and-footer-templates)
- [Template Accessibility](#template-accessibility)

## Keyboard Navigation

### Supported Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Arrow Down` | Move to next item |
| `Arrow Up` | Move to previous item |
| `Space` | Toggle selection of focused item |
| `Enter` | Select focused item |
| `Escape` | Close popup |
| `Home` | Move to first item |
| `End` | Move to last item |
| `Page Down` | Move 5 items down |
| `Page Up` | Move 5 items up |
| `Delete` | Remove selected chip |

### Enable Keyboard Navigation

```csharp
@page "/keyboard-navigation"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Mode="VisualMode.CheckBox"
               Placeholder="Use arrow keys to navigate">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<p>Try: Arrow Up/Down, Space, Enter, Delete keys</p>

@code {
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" },
            new Item { ID = "3", Name = "Item 3" }
        };
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

## ARIA Attributes

### Automatic ARIA Support

Syncfusion components automatically include ARIA attributes:

```html
<!-- Generated HTML includes: -->
<input role="searchbox" 
       aria-label="MultiSelect"
       aria-haspopup="listbox"
       aria-expanded="false"
       aria-controls="popup-id" />
```

### Custom ARIA Labels

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="Select options"
               HtmlAttributes="@(new Dictionary<string, object> { { "aria-label", "Select one or more options from the list" } })">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; } = new();
}
```

**Note:** Use `HtmlAttributes` to add custom ARIA attributes (there's no direct `AriaLabel` property).

### Accessible Label Association

```csharp
<label for="multiselect-id">Choose your preferences:</label>
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               ID="multiselect-id"
               Placeholder="Select options">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; } = new();
}
```

## Screen Reader Support

### WCAG 2.1 Compliance

Components follow WCAG 2.1 Level AA standards:
- Proper semantic HTML
- ARIA live regions for dynamic updates
- Descriptive role announcements
- State notifications

### Testing with Screen Readers

**NVDA (Free, Windows):**
1. Download from https://www.nvaccess.org/
2. Start NVDA
3. Tab to MultiSelect component
4. Listen to announcements

**JAWS (Commercial, Windows):**
- Tab to component
- Press Space to open popup
- Use Arrow keys to navigate

**VoiceOver (macOS/iOS):**
- Enable: System Preferences → Accessibility → VoiceOver
- Use VO+Arrow keys to navigate
- VO+Space to interact

### Example Screen Reader Experience

```
"Multiselect combo box, collapsed. Tab into the field to select items."
[User tabs to component]
"Multiselect combo box, expanded, 5 options available. Arrow keys to navigate."
[User presses Down arrow]
"Item 1, unchecked, checkbox, 1 of 5"
[User presses Space]
"Item 1, checked"
```

## Focus Management

### Default Focus Behavior

```csharp
@page "/focus-demo"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect @ref="MultiSelectRef"
               TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="Click button to focus">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

<button @onclick="FocusDropdown">Focus Dropdown</button>

@code {
    private SfMultiSelect<string[], Item> MultiSelectRef;
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Item 1" },
            new Item { ID = "2", Name = "Item 2" }
        };
    }

    private async Task FocusDropdown()
    {
        if (MultiSelectRef != null)
        {
            await MultiSelectRef.FocusAsync();
        }
    }

    public class Item { public string ID { get; set; } public string Name { get; set; } }
}
```

### Focus Indicators

Visible focus indicators are critical for keyboard users:

```csharp
<style>
    .e-multiselect:focus {
        outline: 3px solid #4A90E2;
        outline-offset: 2px;
    }
    
    .e-list-item:focus {
        box-shadow: inset 0 0 0 3px #4A90E2;
    }
</style>

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; } = new();
}
```

## Item Templates

### Basic Item Template

```csharp
@page "/item-template"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Employee"
               DataSource="@Items"
               Placeholder="Select employees">
    <MultiSelectFieldSettings Text="Name" Value="EmployeeID"></MultiSelectFieldSettings>
    <MultiSelectTemplates TItem="Employee">
        <ItemTemplate Context="employee">
            <div>
                <span>@employee.Name</span>
                <br />
                <small>@employee.Department</small>
            </div>
        </ItemTemplate>
    </MultiSelectTemplates>
</SfMultiSelect>

@code {
    private List<Employee> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Employee>
        {
            new Employee { EmployeeID = "1", Name = "Alice", Department = "IT" },
            new Employee { EmployeeID = "2", Name = "Bob", Department = "HR" }
        };
    }

    public class Employee
    {
        public string EmployeeID { get; set; }
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

### Item Template with Icon

```csharp
<MultiSelectTemplates TItem="Item">
    <ItemTemplate Context="item">
        <div class="item-with-icon">
            @if (item.Status == "Active")
            {
                <span class="status-icon active"></span>
            }
            else
            {
                <span class="status-icon inactive"></span>
            }
            <span>@item.Name</span>
        </div>
    </ItemTemplate>
</MultiSelectTemplates>

<style>
    .status-icon {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-icon.active {
        background-color: #4CAF50;
    }
    
    .status-icon.inactive {
        background-color: #F44336;
    }
</style>
```

### Value Template (Selected Item Display)

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="Select items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectTemplates TItem="Item">
        <ValueTemplate Context="item">
            <span style="color: #2196F3; font-weight: bold;">
                ✓ @item.Name
            </span>
        </ValueTemplate>
    </MultiSelectTemplates>
</SfMultiSelect>
```

## Group Templates

### Custom Group Header Template

```csharp
@page "/group-template"
@using Syncfusion.Blazor.DropDowns

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="Grouped with custom headers">
    <MultiSelectFieldSettings Text="Name" Value="ID" GroupBy="Category"></MultiSelectFieldSettings>
    <MultiSelectTemplates TItem="Item">
        <GroupTemplate>
            <div class="group-header">
                <span style="font-weight: bold; color: #2196F3;">
                    @context.Text
                </span>
                <span style="float: right; color: #999;">
                    (@context.Items.Count() items)
                </span>
            </div>
        </GroupTemplate>
    </MultiSelectTemplates>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<Item>
        {
            new Item { ID = "1", Name = "Apple", Category = "Fruit" },
            new Item { ID = "2", Name = "Banana", Category = "Fruit" },
            new Item { ID = "3", Name = "Carrot", Category = "Vegetable" }
        };
    }

    public class Item 
    { 
        public string ID { get; set; } 
        public string Name { get; set; }
        public string Category { get; set; }
    }
}
```

**Note:** Removed `AllowGrouping` property (doesn't exist). Grouping is enabled automatically when `GroupBy` is set in `MultiSelectFieldSettings`. The GroupTemplate context has `Text` (group name) and `Items` (group members).

## Header and Footer Templates

### Header Template

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               Placeholder="With custom header">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectTemplates TItem="Item">
        <HeaderTemplate>
            <div style="padding: 10px; border-bottom: 1px solid #e0e0e0;">
                <strong>Available Options</strong>
                <p style="font-size: 12px; color: #999; margin: 5px 0 0 0;">
                    Select one or more items
                </p>
            </div>
        </HeaderTemplate>
    </MultiSelectTemplates>
</SfMultiSelect>

@code {
    private List<Item> Items { get; set; } = new();
}
```

### Footer Template

```csharp
<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               @bind-Value="SelectedItems"
               Placeholder="With footer">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    <MultiSelectTemplates TItem="Item">
        <FooterTemplate>
            <div style="padding: 10px; border-top: 1px solid #e0e0e0; text-align: center;">
                <small>Selected: @(SelectedItems?.Length ?? 0) items</small>
            </div>
        </FooterTemplate>
    </MultiSelectTemplates>
</SfMultiSelect>

@code {
    private string[] SelectedItems { get; set; } = Array.Empty<string>();
    private List<Item> Items { get; set; } = new();
}
```

## Template Accessibility

### Accessible Item Template

```csharp
<MultiSelectTemplates TItem="Employee">
    <ItemTemplate Context="employee">
        <div role="option" aria-label="@employee.Name - @employee.Department">
            <strong>@employee.Name</strong>
            <br />
            <small>@employee.Department</small>
        </div>
    </ItemTemplate>
</MultiSelectTemplates>

@code {
    public class Employee
    {
        public string Name { get; set; }
        public string Department { get; set; }
    }
}
```

### Color and Text Contrast

```csharp
<style>
    .template-item {
        color: #212121;              /* Dark text */
        background-color: #FFFFFF;  /* Light background */
        /* Contrast ratio: 12:1 - exceeds WCAG AAA */
    }
    
    .template-item:hover {
        background-color: #F5F5F5;  /* Slight contrast change */
        color: #1976D2;
    }
    
    .template-item:focus {
        outline: 2px solid #1976D2;
        outline-offset: 2px;
    }
</style>
```

### Large Touch Targets

```csharp
<style>
    .e-list-item {
        padding: 12px 16px;  /* Minimum 48x48px touch target */
        min-height: 44px;
    }
</style>

<SfMultiSelect TValue="string[]"
               TItem="Item"
               DataSource="@Items"
               CssClass="accessible-list">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>
```

## Key Takeaways

✅ Keyboard navigation fully supported (Arrow keys, Space, Enter)  
✅ WCAG 2.1 Level AA compliant by default  
✅ ARIA attributes automatically included  
✅ Screen reader compatible  
✅ Use templates for rich, accessible content  
✅ Ensure adequate color contrast in templates  
✅ Maintain focus indicators for keyboard users  
✅ Test with actual assistive technology  

## Next Steps

- **Handle events** → See [Events and API Reference](events-and-api.md)
- **Advanced usage** → See [Advanced Scenarios](advanced-scenarios.md)
- **Styling** → See [Customization and Styling](customization-and-styling.md)
