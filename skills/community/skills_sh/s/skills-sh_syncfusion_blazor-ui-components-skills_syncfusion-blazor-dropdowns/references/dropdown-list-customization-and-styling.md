# Customization and Styling in Syncfusion Blazor DropDown List

## Open on Focus

### Auto-Open Dropdown

Open the dropdown automatically when the component receives focus:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                OpenOnFocus="true"
                Placeholder="Click to open">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
}
```

### Manual Focus Handling

Use JavaScript interop or Blazor events to control focus behavior:

```razor
<SfDropDownList TValue="string" TItem="string" @ref="DropdownRef"
                DataSource="@Items"
                Placeholder="Select item">
    <DropDownListEvents TValue="string" TItem="string" 
                        Focus="@HandleFocus">
    </DropDownListEvents>
</SfDropDownList>

@code {
    private SfDropDownList<string, string> DropdownRef;
    private List<string> Items = new() { "Option A", "Option B", "Option C" };

    private void HandleFocus(FocusEventArgs args)
    {
        // Dropdown opens automatically on focus
        Console.WriteLine("Dropdown received focus");
    }
}
```

## CSS Class Customization

### Apply Custom CSS Classes

Add custom CSS classes for styling:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                CssClass="custom-dropdown"
                Placeholder="Select item">
</SfDropDownList>

<style>
    .custom-dropdown {
        font-size: 16px;
        font-weight: 500;
    }
    
    .custom-dropdown .e-ddl {
        border: 2px solid #007bff;
        border-radius: 8px;
    }
</style>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
}
```

### Multiple Classes

Combine multiple CSS classes:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                CssClass="custom-dropdown large-text"
                Placeholder="Select item">
</SfDropDownList>

<style>
    .custom-dropdown {
        border-color: #28a745;
    }
    
    .large-text {
        font-size: 18px;
    }
</style>

@code {
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

## Theme Application

### Bootstrap 5 Theme

Apply the Bootstrap 5 theme (should be included in App.razor):

```razor
<!-- In App.razor or _Host.cshtml -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />

<!-- Then use dropdown normally -->
<SfDropDownList TValue="string" TItem="string" DataSource="@Items" Placeholder="Select item">
</SfDropDownList>
```

### Switch Between Themes

Dynamically change themes by switching CSS links:

```razor
<div class="mb-3">
    <button @onclick="() => ApplyTheme('bootstrap5')" class="btn btn-sm btn-outline-primary">Bootstrap</button>
    <button @onclick="() => ApplyTheme('material')" class="btn btn-sm btn-outline-primary">Material</button>
    <button @onclick="() => ApplyTheme('fluent')" class="btn btn-sm btn-outline-primary">Fluent</button>
    <button @onclick="() => ApplyTheme('tailwind')" class="btn btn-sm btn-outline-primary">Tailwind</button>
</div>

<SfDropDownList TValue="string" TItem="string" DataSource="@Items" Placeholder="Select item">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
    private string CurrentTheme = "bootstrap5";

    private void ApplyTheme(string theme)
    {
        CurrentTheme = theme;
        // Theme CSS should be switched via JavaScript or app configuration
    }
}
```

## Component Sizing

### Width Configuration

Set the dropdown width:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                Width="300px"
                Placeholder="Select item">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Option A", "Option B", "Option C" };
}
```

### Percentage Width

Use percentage for responsive sizing:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                Width="100%"
                Placeholder="Full width dropdown">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Option 1", "Option 2", "Option 3" };
}
```

### Popup Width and Height

Configure the dropdown popup dimensions:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                PopupWidth="400px"
                PopupHeight="300px"
                Placeholder="Select item">
</SfDropDownList>

@code {
    private List<string> Items = new() { "Item 1", "Item 2", "Item 3" };
}
```

## State-Based Styling

### Enabled and Disabled States

Control whether the dropdown is enabled:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                Enabled="@IsEnabled"
                Placeholder="Select item">
</SfDropDownList>

<button @onclick="ToggleEnabled">Toggle Enable</button>

@code {
    private bool IsEnabled = true;
    private List<string> Items = new() { "Option A", "Option B", "Option C" };

    private void ToggleEnabled()
    {
        IsEnabled = !IsEnabled;
    }
}
```

### Read-Only State

Make dropdown read-only (displays value but doesn't allow changes):

```razor
<SfDropDownList TValue="string" TItem="string" @bind-Value="SelectedValue"
                DataSource="@Items"
                Readonly="@IsReadOnly"
                Placeholder="Select item">
</SfDropDownList>

<button @onclick="ToggleReadOnly">Toggle Read-Only</button>

@code {
    private string SelectedValue;
    private bool IsReadOnly = false;
    private List<string> Items = new() { "Option A", "Option B", "Option C" };

    private void ToggleReadOnly()
    {
        IsReadOnly = !IsReadOnly;
    }
}
```

## Inline Styling

### Add Inline Styles

Apply styles directly to the component:

```razor
<SfDropDownList TValue="string" TItem="string" DataSource="@Items"
                CssClass="green-dropdown"
                Placeholder="Green styled dropdown">
</SfDropDownList>

<style>
    .green-dropdown {
        border-color: #28a745 !important;
        background-color: #f0fff0;
    }
</style>

@code {
    private List<string> Items = new() { "Option 1", "Option 2", "Option 3" };
}
```

## Complete Customization Example

```razor
@page "/dropdown-customization"

<h3>Customization and Styling Example</h3>

<div class="mb-4">
    <h5>Theme Options</h5>
    <button @onclick="() => CurrentTheme = 'Bootstrap'" class="btn btn-sm btn-outline-primary">Bootstrap</button>
    <button @onclick="() => CurrentTheme = 'Material'" class="btn btn-sm btn-outline-primary">Material</button>
    <button @onclick="() => CurrentTheme = 'Fluent'" class="btn btn-sm btn-outline-primary">Fluent</button>
</div>

<div class="mb-4">
    <h5>Dropdown States</h5>
    <label>
        <input type="checkbox" @onchange="e => OpenOnFocus = (bool)e.Value" />
        Open on focus
    </label>
    <label>
        <input type="checkbox" @onchange="e => IsEnabled = (bool)e.Value" checked="@IsEnabled" />
        Enabled
    </label>
</div>

<div class="form-group">
    <label>Select an option</label>
    <SfDropDownList TValue="string" TItem="string"
                    DataSource="@Items"
                    @bind-Value="SelectedValue"
                    Enabled="@IsEnabled"
                    OpenOnFocus="@OpenOnFocus"
                    Width="@DropdownWidth"
                    CssClass="@CustomClass"
                    Placeholder="Choose an option">
    </SfDropDownList>
</div>

<div class="mt-3">
    <p>Current Theme: @CurrentTheme</p>
    <p>Selected Value: @SelectedValue</p>
</div>

<style>
    .styled-dropdown {
        border-radius: 8px;
        border: 2px solid #007bff;
    }
    
    .styled-dropdown .e-ddl {
        padding: 10px 15px;
    }
</style>

@code {
    private string SelectedValue;
    private string CurrentTheme = "Bootstrap";
    private bool OpenOnFocus = false;
    private bool IsEnabled = true;
    private string DropdownWidth = "300px";
    private string CustomClass = "styled-dropdown";
    private List<string> Items = new() { "Option A", "Option B", "Option C", "Option D" };
}
```

## Key Takeaways

- Use `OpenOnFocus="true"` for automatic opening
- Apply custom styling with `CssClass` property
- Set width with `Width` property (pixels or percentage)
- Control enabled/disabled state with `Enabled` property
- Use inline `Style` for quick customization
- Themes are applied globally via CSS in App.razor
- Combine multiple customization options for complete control
- Use responsive widths for mobile-friendly design
