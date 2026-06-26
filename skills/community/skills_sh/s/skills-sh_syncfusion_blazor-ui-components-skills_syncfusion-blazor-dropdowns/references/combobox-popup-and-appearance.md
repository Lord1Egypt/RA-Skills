# Popup Settings & Appearance in ComboBox

## Table of Contents

- [Popup Height](#popup-height)
- [Popup Width](#popup-width)
- [Allow Resize](#allow-resize)
- [Z-Index](#z-index)
- [Popup Positioning](#popup-positioning)
- [Placeholder](#placeholder)
- [FloatLabel](#floatlabel)
- [CSS Classes](#css-classes)
- [Disabled State](#disabled-state)
- [Read-Only State](#read-only-state)

---

## Popup Height

Control the height of the dropdown list popup:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items"
    PopupHeight="400px">
</SfComboBox>

@code {
    private List<string> Items = new()
    {
        "Item1", "Item2", "Item3", "Item4", "Item5", "Item6", 
        "Item7", "Item8", "Item9", "Item10"
    };
}
```

**Default:** 300px  
**Options:** Any CSS size (px, em, %)

### Dynamic Height Based on Content

```razor
<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees"
    PopupHeight="@(Employees.Count > 10 ? "500px" : "300px")">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
    }

    private List<Employee> Employees = new() 
    { 
        // Your employee list
    };
}
```

---

## Popup Width

Customize the width of the dropdown list popup:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items"
    PopupWidth="350px">
</SfComboBox>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
}
```

**Default:** 100% (matches ComboBox width)  
**Options:** Any CSS size (px, em, %)

### Width Larger Than Input

```razor
<SfComboBox TItem="Employee" TValue="int"
    Placeholder="Select an employee"
    DataSource="@Employees"
    PopupWidth="500px"
    Width="150px">
    <ComboBoxFieldSettings Text="Name" Value="EmployeeId"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string Name { get; set; }
    }

    private List<Employee> Employees = new();
}
```

---

## Allow Resize

Enable users to resize the popup dynamically:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Drag popup corner to resize"
    DataSource="@Items"
    AllowResize="true"
    PopupHeight="300px"
    PopupWidth="300px">
</SfComboBox>

@code {
    private List<string> Items = new()
    {
        "Item1", "Item2", "Item3", "Item4", "Item5", "Item6", 
        "Item7", "Item8", "Item9", "Item10"
    };
}
```

**Default:** false  
**Note:** Resized dimensions persist during the session

---

## Z-Index

Control stacking order of the popup:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items"
    ZIndex="1050">
</SfComboBox>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
}
```

**Default:** 1000

**When to Change:**
- Modal dialogs with ComboBox: use higher z-index (1050+)
- Multiple ComboBox popups: different z-indices prevent overlapping
- Overlay components: coordinate with modal z-indices

---

## Popup Positioning

Control when and how the popup displays:

### Show Popup on Initial Load

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox @ref="ComboBoxRef"
    TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items">
    <ComboBoxEvents TItem="string" TValue="string"
        Created="@OnCreated"></ComboBoxEvents>
</SfComboBox>

@code {
    private SfComboBox<string, string> ComboBoxRef;
    private List<string> Items = new() { "Item1", "Item2", "Item3" };

    private async Task OnCreated()
    {
        // Show popup after component is created
        await ComboBoxRef.ShowPopupAsync();
    }
}
```

### Hide Popup Programmatically

```razor
<SfComboBox @ref="ComboBoxRef"
    TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items">
</SfComboBox>

<button @onclick="HidePopup">Hide Popup</button>

@code {
    private SfComboBox<string, string> ComboBoxRef;
    private List<string> Items = new() { "Item1", "Item2", "Item3" };

    private async Task HidePopup()
    {
        await ComboBoxRef.HidePopupAsync();
    }
}
```

### Prevent Popup Opening/Closing

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items">
    <ComboBoxEvents TItem="string" TValue="string"
        OnOpen="@OnPopupOpen"
        OnClose="@OnPopupClose"></ComboBoxEvents>
</SfComboBox>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };

    private void OnPopupOpen(BeforeOpenEventArgs args)
    {
        // Prevent opening based on condition
        if (DateTime.Now.Hour > 17)
        {
            args.Cancel = true;
            Console.WriteLine("ComboBox not available after 5 PM");
        }
    }

    private void OnPopupClose(PopupEventArgs args)
    {
        // Allow/prevent closing
        // args.Cancel = true; // Uncomment to prevent closing
    }
}
```

---

## Placeholder

Show hint text when no value is selected:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Type or select an item..."
    DataSource="@Items">
</SfComboBox>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
}
```

### Placeholder with Color Styling

```razor
<SfComboBox TItem="string" TValue="string"
    Placeholder="Enter text here"
    DataSource="@Items">
</SfComboBox>

<style>
    ::placeholder {
        color: #999;
        opacity: 0.7;
    }
</style>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
}
```

---

## FloatLabel

Display a floating label that moves above the input when focused:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    DataSource="@Items"
    FloatLabelType="@FloatLabelType.Auto"
    Placeholder="Select a language">
</SfComboBox>

@code {
    private List<string> Items = new() { "C#", "JavaScript", "Python" };
}
```

**FloatLabelType Options:**
- **Auto** - Label moves up on focus or when value is entered
- **Always** - Label always floats above (always visible)
- **Never** - Label stays as placeholder (no floating)

### FloatLabel with Color Change

```razor
<SfComboBox TItem="string" TValue="string"
    DataSource="@Items"
    FloatLabelType="@FloatLabelType.Always"
    Placeholder="Favorite Language">
</SfComboBox>

<style>
    .e-float-text {
        color: #007bff;
    }

    .e-input-focus ~ .e-float-text {
        color: #0056b3;
    }
</style>

@code {
    private List<string> Items = new() { "C#", "JavaScript", "Python" };
}
```

---

## CSS Classes

### Apply Custom CSS Classes

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items"
    CssClass="custom-combo">
</SfComboBox>

<style>
    .custom-combo.e-combobox .e-input-group {
        border: 2px solid #007bff;
        border-radius: 8px;
    }

    .custom-combo.e-combobox .e-input-group.e-input-focus {
        border-color: #0056b3;
        box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.25);
    }

    .custom-combo .e-list-item {
        padding: 12px;
    }

    .custom-combo .e-list-item:hover {
        background-color: #e7f3ff;
    }
</style>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
}
```

### Predefined CSS Classes

- `.e-combobox` - Main container
- `.e-input-group` - Input wrapper
- `.e-input-focus` - Focused state
- `.e-popup` - Popup container
- `.e-list-item` - List items
- `.e-list-item.e-active` - Selected item

---

## Disabled State

Disable the ComboBox to prevent user interaction:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="This is disabled"
    DataSource="@Items"
    Enabled="false">
</SfComboBox>

@code {
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
}
```

### Conditional Disable

```razor
<div>
    <label>
        <input type="checkbox" @bind="@AllowSelection" />
        Enable Selection
    </label>
</div>

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item"
    DataSource="@Items"
    Enabled="@AllowSelection">
</SfComboBox>

@code {
    private bool AllowSelection = true;
    private List<string> Items = new() { "Item1", "Item2", "Item3" };
}
```

---

## Read-Only State

Make the ComboBox read-only so users can only select from the list:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select an item (read-only)"
    DataSource="@Items"
    Readonly="true">
</SfComboBox>

@code {
    private List<string> Items = new() { "Option1", "Option2", "Option3" };
}
```

**Difference between Disabled and Readonly:**
- **Disabled:** Cannot interact at all, value not submitted
- **Readonly:** Can select and interact, but cannot type custom values

---

## Best Practices

1. **Match Popup Width to Content**
   - Wide content needs wider popup
   - Use PopupWidth for consistency

2. **Set Reasonable Height**
   - Too small: requires scrolling
   - Too large: wastes space
   - ~300px is typical default

3. **Use FloatLabel for Better UX**
   - More modern appearance
   - Saves space
   - Clear label context

4. **Coordinate Z-Index**
   - Modals: 1050+
   - Normal: 1000 (default)
   - Background: lower values

5. **Accessibility Considerations**
   - Sufficient color contrast
   - Placeholder text not sole label
   - Keyboard navigation supported

---

*See also: [Getting Started](getting-started.md), [Templates & Customization](templates-and-customization.md), [Events & Validation](events-and-validation.md)*
