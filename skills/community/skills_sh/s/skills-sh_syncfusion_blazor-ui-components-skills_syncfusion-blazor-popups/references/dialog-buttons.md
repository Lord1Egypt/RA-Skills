# Dialog Buttons

## Overview

The Dialog component supports built-in buttons through the `DialogButton` component, providing a standardized way to add actions to your dialogs. Dialog buttons appear in the footer and automatically handle click events and styling.

**When to Use DialogButtons:**
- Standard action buttons (OK, Cancel, Delete, etc.)
- Simple button layouts with consistent styling
- Built-in click event handling
- Automatic styling and theming

**When to Use FooterTemplate Instead:**
- Custom button layouts or custom footer content
- Complex button arrangements or additional footer elements
- Non-button content in the footer (progress bars, info text, etc.)
- See **references/templates.md** for FooterTemplate details

## Basic Dialog Buttons

### Simple OK Button

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfDialog Width="300px" Header="Message" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>Operation completed successfully!</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="OK" 
                      IsPrimary="true"
                      OnClick="@CloseDialog" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void CloseDialog()
    {
        DialogVisible = false;
    }
}
```

### OK and Cancel Buttons

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="350px" Header="Confirmation" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>Do you want to save changes?</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Save" 
                      IsPrimary="true"
                      OnClick="@OnSave" />
        <DialogButton Content="Cancel" 
                      OnClick="@OnCancel" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnSave()
    {
        // Save action
        DialogVisible = false;
    }

    private void OnCancel()
    {
        DialogVisible = false;
    }
}
```

## DialogButton Properties

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `Content` | string | Button display text | null |
| `IsPrimary` | bool | Highlights button as primary action | false |
| `IsFlat` | bool | Renders flat button style | false |
| `IconCss` | string | CSS class for button icon (e.g., "e-icons e-ok-icon") | null |
| `OnClick` | EventCallback | Click event handler | null |
| `Disabled` | bool | Disables button interaction | false |
| `CssClass` | string | Custom CSS class for styling | null |
| `Type` | ButtonType | HTML button type (Button, Submit, Reset) | ButtonType.Button |

## Dialog Button Examples

### Buttons with Icons

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="350px" Header="File Operations" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>Do you want to save this file?</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Save" 
                      IconCss="e-icons e-save"
                      IsPrimary="true"
                      OnClick="@OnSave" />
        <DialogButton Content="Don't Save" 
                      IconCss="e-icons e-close"
                      OnClick="@OnDontSave" />
        <DialogButton Content="Cancel" 
                      IconCss="e-icons e-cancel"
                      IsFlat="true"
                      OnClick="@OnCancel" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnSave() => DialogVisible = false;
    private void OnDontSave() => DialogVisible = false;
    private void OnCancel() => DialogVisible = false;
}
```

### Disabled and Styled Buttons

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="400px" Header="Delete Confirmation" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>This action cannot be undone. Are you sure?</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Delete" 
                      IsPrimary="true"
                      Disabled="@(!ConfirmDelete)"
                      OnClick="@OnDelete"
                      CssClass="delete-button" />
        <DialogButton Content="Cancel" 
                      OnClick="@OnCancel" />
    </DialogButtons>
</SfDialog>

<style>
    .delete-button {
        background-color: #d32f2f;
    }
</style>

@code {
    private bool DialogVisible { get; set; } = true;
    private bool ConfirmDelete { get; set; } = false;

    private void OnDelete()
    {
        // Delete action
        DialogVisible = false;
    }

    private void OnCancel() => DialogVisible = false;
}
```

### Form Submit Dialog with Button Types

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="400px" Header="User Registration" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>
            <form id="userForm" @onsubmit="@HandleSubmit">
                <div class="form-group">
                    <label>Name:</label>
                    <input @bind="UserName" type="text" required />
                </div>
                <div class="form-group">
                    <label>Email:</label>
                    <input @bind="UserEmail" type="email" required />
                </div>
            </form>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Submit" 
                      Type="ButtonType.Submit"
                      IsPrimary="true"
                      OnClick="@OnSubmit" />
        <DialogButton Content="Reset" 
                      Type="ButtonType.Reset"
                      OnClick="@OnReset" />
        <DialogButton Content="Cancel"
                      Type="ButtonType.Button"
                      OnClick="@OnCancel" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;
    private string UserName { get; set; }
    private string UserEmail { get; set; }

    private void HandleSubmit()
    {
        // Form submission logic
        Console.WriteLine($"Submitted: {UserName}, {UserEmail}");
    }

    private void OnSubmit()
    {
        // Validate and submit
        DialogVisible = false;
    }

    private void OnReset()
    {
        UserName = "";
        UserEmail = "";
    }

    private void OnCancel() => DialogVisible = false;
}
```

## Button Click Handlers

### Simple Click Handler

```csharp
private void OnClickHandler()
{
    // Perform action
    DialogVisible = false;
}
```

### Click Handler with Parameters

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="350px" Header="Action Selection" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>Choose an action:</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Edit" 
                      OnClick="@(e => OnAction('edit'))" />
        <DialogButton Content="Delete" 
                      OnClick="@(e => OnAction('delete'))" />
        <DialogButton Content="Archive" 
                      OnClick="@(e => OnAction('archive'))" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnAction(string action)
    {
        Console.WriteLine($"Action selected: {action}");
        DialogVisible = false;
    }
}
```

### Async Click Handler

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="350px" Header="Processing" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>@ProcessingMessage</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Submit" 
                      IsPrimary="true"
                      OnClick="@OnSubmitAsync" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;
    private string ProcessingMessage { get; set; } = "Ready to submit";

    private async Task OnSubmitAsync()
    {
        ProcessingMessage = "Processing...";
        await Task.Delay(2000); // Simulate work
        ProcessingMessage = "Completed!";
        DialogVisible = false;
    }
}
```

## Common Button Patterns

### Confirmation Dialog

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="350px" IsModal="true" Header="Confirm Action" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>Are you sure you want to proceed?</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Yes" 
                      IsPrimary="true"
                      OnClick="@OnConfirm" />
        <DialogButton Content="No" 
                      OnClick="@OnCancel" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnConfirm()
    {
        // Proceed with action
        DialogVisible = false;
    }

    private void OnCancel()
    {
        DialogVisible = false;
    }
}
```

### Form Dialog with Submit/Reset

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Inputs

<SfDialog Width="400px" Header="User Form" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>
            <div>
                <input type="text" @bind="UserName" placeholder="Enter name" />
                <input type="email" @bind="UserEmail" placeholder="Enter email" />
            </div>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Submit" 
                      IsPrimary="true"
                      OnClick="@OnSubmit" />
        <DialogButton Content="Reset" 
                      OnClick="@OnReset" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;
    private string UserName { get; set; }
    private string UserEmail { get; set; }

    private void OnSubmit()
    {
        // Save form data
        DialogVisible = false;
    }

    private void OnReset()
    {
        UserName = "";
        UserEmail = "";
    }
}
```

## DialogButtons vs FooterTemplate

| Feature | DialogButtons | FooterTemplate |
|---------|---------------|----------------|
| **Built-in Button Styling** | ✓ Yes | ✗ Manual styling |
| **Simple Configuration** | ✓ Yes | ✗ More code required |
| **Custom Button Layout** | ✗ Fixed layout | ✓ Fully customizable |
| **Additional Content** | ✗ Buttons only | ✓ Any content |
| **Icon Support** | ✓ Yes | ✓ Yes (manual) |
| **Use Case** | Standard dialogs | Complex footers |

**Choose DialogButtons for:** Standard OK/Cancel dialogs, confirmations, simple actions  
**Choose FooterTemplate for:** Custom layouts, progress indicators, mixed content

See **references/templates.md** for FooterTemplate examples.

## Accessibility

Ensure your dialog buttons are accessible:

```csharp
<!-- Use IsPrimary to highlight main action -->
<DialogButton Content="Delete" IsPrimary="true" />

<!-- Use descriptive text in button labels -->
<DialogButton Content="Confirm Deletion" />
<DialogButton Content="Keep Item" />

<!-- Avoid disabled buttons for critical actions -->
<DialogButton Content="Submit" Disabled="false" />
```

## Icon Classes

Common Syncfusion icon classes for buttons:

| Icon | CSS Class |
|------|-----------|
| OK | `e-icons e-ok-icon` |
| Close/Cancel | `e-icons e-close-icon` |
| Save | `e-icons e-save` |
| Delete | `e-icons e-delete` |
| Edit | `e-icons e-edit` |
| Refresh | `e-icons e-refresh` |
| Check | `e-icons e-check-icon` |
| Warning | `e-icons e-warning` |

## Best Practices

1. **Use IsPrimary**: Highlight the recommended action with `IsPrimary="true"`
2. **Consistent Button Order**: Place primary action on the right or left consistently
3. **Descriptive Labels**: Use clear, action-oriented button text
4. **Disable When Invalid**: Disable buttons when form data is incomplete or invalid
5. **Event Handling**: Always close or hide the dialog in click handlers
6. **Icon + Content**: Combine icons with text for better clarity
7. **Keyboard Support**: DialogButtons automatically support keyboard navigation (Tab, Enter)
