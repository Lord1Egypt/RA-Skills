# Dialog Dimensions

## Table of Contents
- [Overview](#overview)
- [Basic Dimensions](#basic-dimensions)
- [Max Width and Height](#max-width-and-height)
- [Min Width and Height](#min-width-and-height)
- [Examples](#examples)

---

## Overview

Customize predefined dialog dimensions using the `DialogOptions.Width` and `DialogOptions.Height` properties.

**Properties:**
- `DialogOptions.Width` - Sets dialog width
- `DialogOptions.Height` - Sets dialog height

**Default Values:** `"auto"` for both Width and Height

**Supported Units:**
- Pixels: `"300px"`
- Percentages: `"50%"`
- Other CSS units: `"20em"`, `"10rem"`

**Default Behavior:** When Width and Height are not specified (or set to "auto"), the dialog size adapts automatically to its content.

---

## Basic Dimensions

### Setting Width Only

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowCustomWidth">Show Custom Width Dialog</SfButton>

@code {
    private async Task ShowCustomWidth()
    {
        var options = new DialogOptions()
        {
            Width = "500px"
        };
        
        await DialogService.AlertAsync(
            "This dialog has a custom width of 500px. Height adjusts to content.",
            "Custom Width",
            options
        );
    }
}
```

### Setting Height Only

```razor
@code {
    private async Task ShowCustomHeight()
    {
        var options = new DialogOptions()
        {
            Height = "300px"
        };
        
        await DialogService.AlertAsync(
            "This dialog has a custom height of 300px. Width adjusts to content.",
            "Custom Height",
            options
        );
    }
}
```

### Setting Both Width and Height

```razor
@code {
    private async Task ShowCustomDimensions()
    {
        var options = new DialogOptions()
        {
            Width = "600px",
            Height = "400px"
        };
        
        await DialogService.AlertAsync(
            "This dialog has custom width (600px) and height (400px).",
            "Custom Dimensions",
            options
        );
    }
}
```

---

## Examples for All Dialog Types

### Alert Dialog with Dimensions

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowAlert">Show Alert</SfButton>

@code {
    private async Task ShowAlert()
    {
        var options = new DialogOptions()
        {
            Width = "450px",
            Height = "200px"
        };
        
        await DialogService.AlertAsync(
            "This is an alert dialog with custom dimensions.",
            "Alert",
            options
        );
    }
}
```

### Confirm Dialog with Dimensions

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowConfirm">Show Confirm</SfButton>

@code {
    private async Task ShowConfirm()
    {
        var options = new DialogOptions()
        {
            Width = "500px",
            Height = "250px"
        };
        
        bool confirmed = await DialogService.ConfirmAsync(
            "Are you sure you want to delete this item?",
            "Confirm Delete",
            options
        );
    }
}
```

### Prompt Dialog with Dimensions

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowPrompt">Show Prompt</SfButton>

@code {
    private async Task ShowPrompt()
    {
        var options = new DialogOptions()
        {
            Width = "400px",
            Height = "220px"
        };
        
        string input = await DialogService.PromptAsync(
            "Enter your email address:",
            "",
            options
        );
    }
}
```

---

## Max Width and Height

To constrain the dialog's maximum size, specify `max-width` and `max-height` CSS properties for the component's container using the `CssClass` property.

**Note:** The component may apply an inline `max-height`. To override it, use a higher-specificity selector or `!important` if necessary.

### Example with Max Dimensions

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowMaxDimensions">Show Dialog with Max Dimensions</SfButton>

<style>
    .max-size-dialog .e-dlg-content {
        max-width: 800px !important;
        max-height: 600px !important;
    }
</style>

@code {
    private async Task ShowMaxDimensions()
    {
        var options = new DialogOptions()
        {
            CssClass = "max-size-dialog",
            Width = "100%",
            Height = "100%"
        };
        
        await DialogService.AlertAsync(
            "This dialog has max-width: 800px and max-height: 600px constraints.",
            "Max Dimensions",
            options
        );
    }
}
```

### Responsive Max Width

```razor
<style>
    .responsive-dialog .e-dlg-content {
        max-width: 90vw !important;
        max-height: 80vh !important;
    }
</style>

@code {
    private async Task ShowResponsiveDialog()
    {
        var options = new DialogOptions()
        {
            CssClass = "responsive-dialog",
            Width = "100%",
            Height = "auto"
        };
        
        await DialogService.AlertAsync(
            "This dialog is constrained to 90% viewport width and 80% viewport height.",
            "Responsive Dialog",
            options
        );
    }
}
```

---

## Min Width and Height

To ensure a minimum dialog size (for example, to keep action buttons visible), specify `min-width` and `min-height` CSS properties for the component's container using the `CssClass` property.

### Example with Min Dimensions

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowMinDimensions">Show Dialog with Min Dimensions</SfButton>

<style>
    .min-size-dialog .e-dlg-content {
        min-width: 400px;
        min-height: 200px;
    }
</style>

@code {
    private async Task ShowMinDimensions()
    {
        var options = new DialogOptions()
        {
            CssClass = "min-size-dialog"
        };
        
        await DialogService.AlertAsync(
            "Small message",
            "Min Dimensions",
            options
        );
    }
}
```

### Ensuring Button Visibility

```razor
<style>
    .button-visibility-dialog .e-dlg-content {
        min-width: 350px;
        min-height: 150px;
    }
</style>

@code {
    private async Task ShowDialogWithVisibleButtons()
    {
        var options = new DialogOptions()
        {
            CssClass = "button-visibility-dialog",
            PrimaryButtonOptions = new DialogButtonOptions()
            {
                Content = "Confirm Action"
            },
            CancelButtonOptions = new DialogButtonOptions()
            {
                Content = "Cancel"
            }
        };
        
        await DialogService.ConfirmAsync(
            "Confirm?",
            "Action",
            options
        );
    }
}
```

---

## Percentage-Based Dimensions

### Using Viewport Percentages

```razor
@code {
    private async Task ShowPercentageDimensions()
    {
        var options = new DialogOptions()
        {
            Width = "80%",
            Height = "60%"
        };
        
        await DialogService.AlertAsync(
            "This dialog takes 80% of viewport width and 60% of viewport height.",
            "Percentage Dimensions",
            options
        );
    }
}
```

### Responsive Design

```razor
@code {
    private async Task ShowResponsive()
    {
        var options = new DialogOptions()
        {
            Width = "90%",
            Height = "auto"
        };
        
        await DialogService.AlertAsync(
            "This dialog adjusts to 90% width and auto-calculates height.",
            "Responsive",
            options
        );
    }
}
```

---

## Common Dimension Patterns

### Small Notification Dialog

```csharp
var options = new DialogOptions()
{
    Width = "350px",
    Height = "150px"
};
```

### Standard Dialog

```csharp
var options = new DialogOptions()
{
    Width = "500px",
    Height = "300px"
};
```

### Large Content Dialog

```csharp
var options = new DialogOptions()
{
    Width = "800px",
    Height = "600px"
};
```

### Full-Width Dialog

```csharp
var options = new DialogOptions()
{
    Width = "90%",
    Height = "auto"
};
```

### Mobile-Friendly Dialog

```csharp
var options = new DialogOptions()
{
    Width = "95%",
    Height = "auto",
    CssClass = "mobile-dialog"
};
```

```css
.mobile-dialog .e-dlg-content {
    max-width: 600px;
    margin: 0 auto;
}
```

---

## Tips

1. **Auto Height:** Use `Height = "auto"` to let the dialog adjust to content size.

2. **Responsive Width:** Use percentage values for width to create responsive dialogs.

3. **Content Overflow:** If content exceeds dialog dimensions, scrollbars appear automatically.

4. **Combine with Positioning:** Use custom dimensions with positioning for precise control:
   ```csharp
   var options = new DialogOptions()
   {
       Width = "500px",
       Height = "300px",
       Position = new PositionDataModel() { X = "center", Y = "top" }
   };
   ```

5. **Accessibility:** Ensure minimum dimensions maintain readable text and accessible buttons.
