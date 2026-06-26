# Advanced Customization and Styling

## Table of Contents
- [CSS Class Customization](#css-class-customization)
- [Appearance Styling](#appearance-styling)
- [Accessibility](#accessibility)
- [State Persistence](#state-persistence)
- [Minimize and Maximize](#minimize-and-maximize)
- [Localization](#localization)
- [Responsive Design](#responsive-design)
- [Advanced Patterns](#advanced-patterns)

## CSS Class Customization

Apply custom CSS classes to dialogs for advanced styling and behavior control.

### Using CssClass Property

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Custom Styled Dialog" CssClass="custom-dialog">
    <DialogTemplates>
        <Content>This dialog has custom CSS styling applied</Content>
    </DialogTemplates>
</SfDialog>

<style>
    .custom-dialog.e-dialog {
        background-color: #f5f5f5;
        border: 2px solid #2196F3;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    .custom-dialog .e-dlg-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
    }

    .custom-dialog .e-dlg-content {
        padding: 20px;
        font-size: 14px;
        line-height: 1.6;
    }

    .custom-dialog .e-footer-content {
        padding: 15px;
        background-color: #fafafa;
        border-top: 1px solid #e0e0e0;
    }
</style>
```

### Multiple Custom Classes

```csharp
<SfDialog Header="Multi-Class Dialog" CssClass="custom-style premium-theme dark-mode">
    <DialogTemplates>
        <Content>Multiple CSS classes applied</Content>
    </DialogTemplates>
</SfDialog>

<style>
    .custom-style.e-dialog {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .premium-theme.e-dialog {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .dark-mode.e-dialog {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
</style>
```

## Appearance Styling

### Header Styling

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Styled Header" CssClass="styled-header">
    <DialogTemplates>
        <Content>Dialog with custom header styling</Content>
    </DialogTemplates>
</SfDialog>

<style>
    .styled-header.e-dialog {
        border: none;
    }

    .styled-header .e-dlg-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 20px;
        border-bottom: 3px solid #764ba2;
    }

    .styled-header .e-dlg-header-content {
        background-color: transparent;
    }
</style>
```

### Content Styling

```csharp
<SfDialog Header="Content Styling" CssClass="styled-content">
    <DialogTemplates>
        <Content>
            <p>Paragraph 1 with styling</p>
            <p>Paragraph 2 with styling</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .styled-content .e-dlg-content {
        padding: 25px;
        background-color: #f9f9f9;
    }

    .styled-content .e-dlg-content p {
        margin: 10px 0;
        line-height: 1.8;
        color: #333;
    }

    .styled-content .e-dlg-content ul {
        list-style-type: none;
        padding: 0;
    }

    .styled-content .e-dlg-content li {
        padding: 8px 0;
        padding-left: 20px;
        position: relative;
    }

    .styled-content .e-dlg-content li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #4caf50;
        font-weight: bold;
    }
</style>
```

### Footer Styling

```csharp
<SfDialog Header="Footer Styling" CssClass="styled-footer">
    <DialogTemplates>
        <Content>Dialog with styled footer</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="OK" IsPrimary="true" />
        <DialogButton Content="Cancel" />
    </DialogButtons>
</SfDialog>

<style>
    .styled-footer .e-footer-content {
        background: linear-gradient(90deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px 25px;
        border-top: 2px solid #ddd;
        display: flex;
        justify-content: flex-end;
        gap: 10px;
    }

    .styled-footer .e-btn {
        border-radius: 4px;
        padding: 8px 20px;
    }

    .styled-footer .e-btn.e-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
    }
</style>
```

## Accessibility

### WCAG Compliance

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Accessible Dialog" 
          ShowCloseIcon="true"
          CssClass="accessible-dialog">
    <DialogTemplates>
        <Header>
            <span role="heading" aria-level="2">Important Notification</span>
        </Header>
        <Content>
            <p role="region" aria-live="polite">
                This is an important message for you.
            </p>
            <form role="form">
                <label for="username">Username:</label>
                <input id="username" type="text" aria-required="true" />
            </form>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .accessible-dialog.e-dialog {
        min-width: 300px;
    }

    .accessible-dialog input {
        width: 100%;
        padding: 8px;
        margin-bottom: 10px;
    }
</style>
```

### Keyboard Navigation

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfDialog Header="Keyboard Accessible" 
          @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>
            <p>Use Tab to navigate between buttons</p>
            <p>Press Enter to activate buttons</p>
            <p>Press Escape to close the dialog</p>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="OK" IsPrimary="true" OnClick="@OnOK" />
        <DialogButton Content="Cancel" OnClick="@OnCancel" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnOK() => DialogVisible = false;
    private void OnCancel() => DialogVisible = false;
}
```

### High Contrast Mode

```csharp
<SfDialog Header="High Contrast" CssClass="high-contrast-dialog">
    <DialogTemplates>
        <Content>Enhanced contrast for visibility</Content>
    </DialogTemplates>
</SfDialog>

<style>
    @media (prefers-contrast: more) {
        .high-contrast-dialog.e-dialog {
            border: 3px solid #000;
        }

        .high-contrast-dialog .e-dlg-header {
            background-color: #000;
            color: #fff;
        }

        .high-contrast-dialog .e-dlg-content {
            color: #000;
            background-color: #fff;
        }
    }
</style>
```

## State Persistence

### Using EnablePersistence Property

The `EnablePersistence` property automatically persists dialog state (position, width, height) to browser local storage.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog @bind-Visible="DialogVisible"
          Header="Persistent Dialog"
          Width="400px"
          Height="300px"
          EnablePersistence="true"
          ID="dialog_persist">
    <DialogTemplates>
        <Content>
            <p>This dialog's position, width, and height will be saved to browser local storage</p>
            <p>Close and reopen the page to see the dialog in the same position and size</p>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Close" OnClick="@CloseDialog" />
    </DialogButtons>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void CloseDialog() => DialogVisible = false;
}
```

**Important:**
- `ID` property must be set for persistence to work (used as storage key)
- Persisted values: Position (Left, Top), Width, Height
- Persists to browser's local storage
- State persists across page reloads and browser sessions

### Custom Save Dialog Dimensions (Manual Persistence)

```csharp
@using Syncfusion.Blazor.Popups
@using System.Text.Json

<SfDialog @ref="DialogRef"
          @bind-Visible="DialogVisible"
          Width="@DialogWidth"
          Height="@DialogHeight"
          Header="Persistent Dialog">
    <DialogTemplates>
        <Content>Dialog state will be saved</Content>
    </DialogTemplates>
    <DialogEvents Closed="@SaveDialogState" />
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }
    private bool DialogVisible { get; set; } = true;
    private string DialogWidth { get; set; } = "400px";
    private string DialogHeight { get; set; } = "300px";

    protected override async Task OnInitializedAsync()
    {
        // Load saved state from localStorage
        var savedState = await JSRuntime.InvokeAsync<string>("localStorage.getItem", "dialogState");
        if (!string.IsNullOrEmpty(savedState))
        {
            var state = JsonSerializer.Deserialize<DialogState>(savedState);
            DialogWidth = state?.Width ?? "400px";
            DialogHeight = state?.Height ?? "300px";
        }
    }

    private async Task SaveDialogState()
    {
        var state = new DialogState { Width = DialogWidth, Height = DialogHeight };
        var json = JsonSerializer.Serialize(state);
        await JSRuntime.InvokeVoidAsync("localStorage.setItem", "dialogState", json);
    }

    private class DialogState
    {
        public string Width { get; set; }
        public string Height { get; set; }
    }
}
```

## Minimize and Maximize

### Custom Minimize/Maximize Buttons

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="400px" Height="300px" Header="Minimizable Dialog" CssClass="minimizable">
    <DialogTemplates>
        <Header>
            <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                <span>Dialog Title</span>
                <div>
                    <button @onclick="@MinimizeDialog" 
                            style="background: none; border: none; cursor: pointer; margin-right: 10px;">
                        _
                    </button>
                    <button @onclick="@CloseDialog" 
                            style="background: none; border: none; cursor: pointer;">
                        ×
                    </button>
                </div>
            </div>
        </Header>
        <Content>
            <p>Click the minimize button to collapse the dialog</p>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .minimizable.e-dialog {
        transition: all 0.3s ease;
    }

    .minimizable.minimized {
        height: 40px !important;
        overflow: hidden;
    }

    .minimizable.minimized .e-dlg-content,
    .minimizable.minimized .e-footer-content {
        display: none;
    }
</style>

@code {
    private bool IsMinimized { get; set; } = false;

    private void MinimizeDialog()
    {
        IsMinimized = !IsMinimized;
        StateHasChanged();
    }

    private void CloseDialog()
    {
        // Close logic
    }
}
```

## Localization

### Multi-Language Support

```csharp
@using Syncfusion.Blazor.Popups

<select @onchange="@ChangeLanguage">
    <option value="en">English</option>
    <option value="es">Spanish</option>
    <option value="fr">French</option>
</select>

<SfDialog Header="@GetLocalizedHeader()" Width="400px">
    <DialogTemplates>
        <Content>@GetLocalizedContent()</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="@GetLocalizedButtonOK()" IsPrimary="true" />
        <DialogButton Content="@GetLocalizedButtonCancel()" />
    </DialogButtons>
</SfDialog>

@code {
    private string CurrentLanguage { get; set; } = "en";

    private Dictionary<string, Dictionary<string, string>> Translations = new()
    {
        {
            "en", new Dictionary<string, string>
            {
                { "header", "Welcome" },
                { "content", "Welcome to our application" },
                { "ok", "OK" },
                { "cancel", "Cancel" }
            }
        },
        {
            "es", new Dictionary<string, string>
            {
                { "header", "Bienvenido" },
                { "content", "Bienvenido a nuestra aplicación" },
                { "ok", "OK" },
                { "cancel", "Cancelar" }
            }
        },
        {
            "fr", new Dictionary<string, string>
            {
                { "header", "Bienvenue" },
                { "content", "Bienvenue dans notre application" },
                { "ok", "OK" },
                { "cancel", "Annuler" }
            }
        }
    };

    private void ChangeLanguage(ChangeEventArgs e)
    {
        CurrentLanguage = e.Value?.ToString() ?? "en";
    }

    private string GetLocalizedHeader() => Translations[CurrentLanguage]["header"];
    private string GetLocalizedContent() => Translations[CurrentLanguage]["content"];
    private string GetLocalizedButtonOK() => Translations[CurrentLanguage]["ok"];
    private string GetLocalizedButtonCancel() => Translations[CurrentLanguage]["cancel"];
}
```

## Responsive Design

### Mobile-Friendly Dialog

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Responsive Dialog" 
          CssClass="responsive-dialog"
          Width="90%"
          @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>
            <p>This dialog adapts to different screen sizes</p>
            <img src="responsive-image.png" style="max-width: 100%; height: auto;" />
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    /* Large screens */
    @media (min-width: 1200px) {
        .responsive-dialog.e-dialog {
            width: 50% !important;
        }
    }

    /* Medium screens */
    @media (min-width: 768px) and (max-width: 1199px) {
        .responsive-dialog.e-dialog {
            width: 70% !important;
        }
    }

    /* Small screens */
    @media (max-width: 767px) {
        .responsive-dialog.e-dialog {
            width: 95% !important;
            height: auto !important;
            max-height: 90vh;
        }

        .responsive-dialog .e-dlg-content {
            padding: 15px;
        }
    }
</style>

@code {
    private bool DialogVisible { get; set; } = true;
}
```

## Advanced Patterns

### Context Menu Dialog

```csharp
@using Syncfusion.Blazor.Popups

<div @oncontextmenu:preventDefault 
     @oncontextmenu="@ShowContextMenu"
     style="width: 400px; height: 300px; border: 1px solid #ccc; padding: 20px;">
    Right-click to see context menu
</div>

<SfDialog @bind-Visible="ShowMenu" Header="Context Menu" Width="200px" CssClass="context-menu">
    <DialogTemplates>
        <Content>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li><a href="#" @onclick="@OnEdit">Edit</a></li>
                <li><a href="#" @onclick="@OnDelete">Delete</a></li>
                <li><a href="#" @onclick="@OnShare">Share</a></li>
            </ul>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool ShowMenu { get; set; } = false;

    private void ShowContextMenu(MouseEventArgs e)
    {
        ShowMenu = true;
    }

    private void OnEdit() => ShowMenu = false;
    private void OnDelete() => ShowMenu = false;
    private void OnShare() => ShowMenu = false;
}
```

### Loading Dialog

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog IsModal="true" 
          Header="Processing" 
          ShowCloseIcon="false"
          EnableResize="false"
          AllowDragging="false"
          Width="300px"
          CssClass="loading-dialog">
    <DialogTemplates>
        <Content>
            <div style="text-align: center; padding: 20px;">
                <div class="spinner"></div>
                <p>@LoadingMessage</p>
            </div>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>

@code {
    private string LoadingMessage { get; set; } = "Loading...";
}
```

## Best Practices

1. **Semantic HTML**: Use proper semantic HTML in dialog templates
2. **ARIA Labels**: Include aria-labels for screen reader users
3. **Color Contrast**: Ensure sufficient color contrast for accessibility
4. **Responsive Units**: Use percentages or viewport units for responsiveness
5. **Performance**: Minimize redraws and use CSS transforms when possible
6. **Keyboard Support**: Test all interactive elements with keyboard navigation
7. **Mobile Testing**: Test dialogs on actual mobile devices
8. **Theme Consistency**: Match dialog styling to your application theme
9. **Error Handling**: Handle edge cases in custom styling
10. **Documentation**: Comment complex CSS classes for maintainability
