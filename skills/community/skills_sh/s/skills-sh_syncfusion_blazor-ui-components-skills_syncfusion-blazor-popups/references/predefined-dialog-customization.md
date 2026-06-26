# Customization of Predefined Dialogs

## Table of Contents
- [Overview](#overview)
- [Customize Action Buttons](#customize-action-buttons)
- [Show or Hide Close Button](#show-or-hide-close-button)
- [Customize Dialog Content](#customize-dialog-content)
- [Complete Examples](#complete-examples)

---

## Overview

Predefined dialogs offer extensive customization options:
- **Button Customization** - Change button text, icons, and appearance
- **Close Icon** - Show or hide the dialog close button
- **Custom Content** - Load custom components in dialog body

---

## Customize Action Buttons

### DialogButtonOptions Properties

Customize dialog buttons using:
- `DialogOptions.PrimaryButtonOptions` - Customizes the primary (OK) button
- `DialogOptions.CancelButtonOptions` - Customizes the secondary (Cancel) button

**DialogButtonOptions Properties:**
- `Content` - Button text
- `IconCss` - CSS class for button icon
- `IsPrimary` - Primary button styling

---

### Alert Dialog - Custom Button Text

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowCustomAlert">Show Custom Alert</SfButton>

@code {
    private async Task ShowCustomAlert()
    {
        var options = new DialogOptions()
        {
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Okay"
            }
        };
        
        await DialogService.AlertAsync(
            "This is an alert with a custom button.",
            "Custom Alert",
            options
        );
    }
}
```

### Confirm Dialog - Custom Buttons with Icons

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowCustomConfirm">Show Custom Confirm</SfButton>

@code {
    private async Task ShowCustomConfirm()
    {
        var options = new DialogOptions()
        {
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Yes",
                IconCss = "e-icons e-check"
            },
            CancelButtonOptions = new DialogButtonOptions()
            {
                Content = "No",
                IconCss = "e-icons e-close"
            }
        };
        
        bool confirmed = await DialogService.ConfirmAsync(
            "Do you agree with the terms and conditions?",
            "Terms & Conditions",
            options
        );
    }
}
```

### Prompt Dialog - Custom Button Labels

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowCustomPrompt">Show Custom Prompt</SfButton>

@code {
    private async Task ShowCustomPrompt()
    {
        var options = new DialogOptions()
        {
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Connect"
            },
            CancelButtonOptions = new DialogButtonOptions()
            {
                Content = "Close"
            }
        };
        
        string input = await DialogService.PromptAsync(
            "Enter server address:",
            "",
            options
        );
    }
}
```

---

## Common Button Customization Patterns

### Delete Confirmation with Icon

```csharp
var options = new DialogOptions()
{
    PrimaryButtonOptions = new DialogButtonOptions()
    {
        Content = "Delete",
        IconCss = "e-icons e-delete"
    },
    CancelButtonOptions = new DialogButtonOptions()
    {
        Content = "Keep"
    }
};

bool confirmed = await DialogService.ConfirmAsync(
    "Are you sure you want to delete this item?",
    "Confirm Delete",
    options
);
```

### Save Changes Confirmation

```csharp
var options = new DialogOptions()
{
    PrimaryButtonOptions = new DialogButtonOptions()
    {
        Content = "Save",
        IconCss = "e-icons e-save"
    },
    CancelButtonOptions = new DialogButtonOptions()
    {
        Content = "Discard"
    }
};

bool confirmed = await DialogService.ConfirmAsync(
    "You have unsaved changes. Do you want to save them?",
    "Unsaved Changes",
    options
);
```

### Proceed/Abort Actions

```csharp
var options = new DialogOptions()
{
    PrimaryButtonOptions = new DialogButtonOptions()
    {
        Content = "Proceed",
        IconCss = "e-icons e-play"
    },
    CancelButtonOptions = new DialogButtonOptions()
    {
        Content = "Abort"
    }
};
```

---

## Show or Hide Close Button

Control the close icon button visibility using the `DialogOptions.ShowCloseIcon` property.

**Property:** `DialogOptions.ShowCloseIcon`  
**Type:** `bool`  
**Default:** `false`

### Alert Dialog with Close Icon

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowAlertWithCloseIcon">Show Alert with Close Icon</SfButton>

@code {
    private async Task ShowAlertWithCloseIcon()
    {
        var options = new DialogOptions()
        {
            ShowCloseIcon = true
        };
        
        await DialogService.AlertAsync(
            "You can close this dialog using the close icon.",
            "Alert with Close Icon",
            options
        );
    }
}
```

### Confirm Dialog with Close Icon

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowConfirmWithCloseIcon">Show Confirm with Close Icon</SfButton>

@code {
    private async Task ShowConfirmWithCloseIcon()
    {
        var options = new DialogOptions()
        {
            ShowCloseIcon = true
        };
        
        bool confirmed = await DialogService.ConfirmAsync(
            "Do you want to continue?",
            "Confirm Action",
            options
        );
        
        // Note: Clicking close icon returns false (same as Cancel)
    }
}
```

### Prompt Dialog with Close Icon

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowPromptWithCloseIcon">Show Prompt with Close Icon</SfButton>

@code {
    private async Task ShowPromptWithCloseIcon()
    {
        var options = new DialogOptions()
        {
            ShowCloseIcon = true
        };
        
        string input = await DialogService.PromptAsync(
            "Enter your name:",
            "",
            options
        );
        
        // Note: Clicking close icon returns null (same as Cancel)
    }
}
```

---

## Customize Dialog Content

Load custom content in predefined dialogs using the `DialogOptions.ChildContent` property.

**Property:** `DialogOptions.ChildContent`  
**Type:** `RenderFragment`

### Custom Content in Prompt Dialog

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowCustomContent">Show Custom Content Dialog</SfButton>

@code {
    private string username = "";
    
    private async Task ShowCustomContent()
    {
        var options = new DialogOptions()
        {
            ChildContent = @<div>
                <label for="username">Username:</label>
                <input id="username" type="text" @bind="username" class="e-input" style="width: 100%;" />
            </div>,
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Connect"
            },
            CancelButtonOptions = new DialogButtonOptions()
            {
                Content = "Close"
            },
            Width = "400px"
        };
        
        await DialogService.PromptAsync(
            "Please enter your credentials:",
            "",
            options
        );
        
        // Use the username variable after dialog closes
        if (!string.IsNullOrEmpty(username))
        {
            // Process username
        }
    }
}
```

### Multi-Field Custom Dialog

```razor
@code {
    private string email = "";
    private string phone = "";
    
    private async Task ShowMultiFieldDialog()
    {
        var options = new DialogOptions()
        {
            ChildContent = @<div class="custom-form">
                <div class="form-field">
                    <label>Email:</label>
                    <input type="email" @bind="email" class="e-input" />
                </div>
                <div class="form-field">
                    <label>Phone:</label>
                    <input type="tel" @bind="phone" class="e-input" />
                </div>
            </div>,
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Submit"
            },
            CancelButtonOptions = new DialogButtonOptions()
            {
                Content = "Cancel"
            },
            Width = "450px",
            Height = "250px"
        };
        
        await DialogService.PromptAsync(
            "Update Contact Information",
            "",
            options
        );
    }
}
```

### Custom Content with Rich Formatting

```razor
@code {
    private async Task ShowRichContent()
    {
        var options = new DialogOptions()
        {
            ChildContent = @<div>
                <h4>Important Information</h4>
                <ul>
                    <li>Your data will be saved securely</li>
                    <li>You can access it anytime</li>
                    <li>Changes take effect immediately</li>
                </ul>
                <p style="color: #666; font-style: italic;">
                    Click OK to acknowledge that you've read this information.
                </p>
            </div>,
            Width = "500px",
            Height = "300px"
        };
        
        await DialogService.AlertAsync(
            "",  // Empty title as content has its own heading
            "",
            options
        );
    }
}
```

---

## Complete Examples

### Example 1: Fully Customized Delete Confirmation

```razor
@inject SfDialogService DialogService

<SfButton @onclick="DeleteItem">Delete Item</SfButton>

@code {
    private async Task DeleteItem()
    {
        var options = new DialogOptions()
        {
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Delete Permanently",
                IconCss = "e-icons e-delete"
            },
            CancelButtonOptions = new DialogButtonOptions()
            {
                Content = "Keep Item",
                IconCss = "e-icons e-save"
            },
            ShowCloseIcon = true,
            Width = "500px",
            AnimationSettings = new DialogAnimationOptions()
            {
                Effect = DialogEffect.Zoom,
                Duration = 300
            }
        };
        
        bool confirmed = await DialogService.ConfirmAsync(
            "This action cannot be undone. The item will be permanently deleted from the system.",
            "Confirm Permanent Deletion",
            options
        );
        
        if (confirmed)
        {
            // Perform delete operation
        }
    }
}
```

### Example 2: Custom Login Dialog

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowLogin">Login</SfButton>

@code {
    private string username = "";
    private string password = "";
    
    private async Task ShowLogin()
    {
        var options = new DialogOptions()
        {
            ChildContent = @<div class="login-form">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" @bind="username" class="e-input" placeholder="Enter username" />
                </div>
                <div class="form-group" style="margin-top: 15px;">
                    <label>Password:</label>
                    <input type="password" @bind="password" class="e-input" placeholder="Enter password" />
                </div>
            </div>,
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Login",
                IconCss = "e-icons e-login"
            },
            CancelButtonOptions = new DialogButtonOptions()
            {
                Content = "Cancel"
            },
            ShowCloseIcon = true,
            Width = "400px",
            Height = "280px"
        };
        
        await DialogService.PromptAsync(
            "Enter Your Credentials",
            "",
            options
        );
        
        if (!string.IsNullOrEmpty(username) && !string.IsNullOrEmpty(password))
        {
            // Perform login
        }
    }
}
```

### Example 3: Notification with Custom Styling

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowNotification">Show Notification</SfButton>

<style>
    .success-notification {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
</style>

@code {
    private async Task ShowNotification()
    {
        var options = new DialogOptions()
        {
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Got it!",
                IconCss = "e-icons e-check"
            },
            ShowCloseIcon = true,
            CssClass = "success-notification",
            Width = "450px",
            Position = new PositionDataModel()
            {
                X = "center",
                Y = "top"
            },
            AnimationSettings = new DialogAnimationOptions()
            {
                Effect = DialogEffect.Zoom,
                Duration = 400
            }
        };
        
        await DialogService.AlertAsync(
            "Your changes have been saved successfully!",
            "Success",
            options
        );
    }
}
```

---

## Tips

1. **Icon Classes:** Use Syncfusion's built-in icon classes (e-icons e-*) or custom CSS classes for button icons.

2. **Button Content:** Keep button text concise but descriptive (3-15 characters).

3. **Close Icon Behavior:**
   - In Confirm dialogs, close icon returns `false` (same as Cancel button)
   - In Prompt dialogs, close icon returns `null` (same as Cancel button)
   - In Alert dialogs, close icon closes the dialog (same as OK button)

4. **Custom Content Binding:** Use `@bind` with local variables in custom content to capture user input.

5. **Accessibility:** Ensure custom content maintains proper label associations and keyboard navigation.

6. **Styling:** Combine `CssClass` property with custom CSS for advanced styling needs.
