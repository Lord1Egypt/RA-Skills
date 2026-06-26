# Positioning Predefined Dialogs

## Overview

Customize the position of predefined dialogs using the `DialogOptions.Position` property. The position is defined by X and Y values on the `PositionDataModel` type and is relative to the target container.

**Property:** `DialogOptions.Position`  
**Type:** `PositionDataModel`

---

## PositionDataModel Properties

### X Coordinate (Horizontal Position)

| Value | Description |
|-------|-------------|
| `"left"` | Align to left edge |
| `"center"` | Center horizontally (default) |
| `"right"` | Align to right edge |
| Offset value | Pixel offset (e.g., "100px") |

### Y Coordinate (Vertical Position)

| Value | Description |
|-------|-------------|
| `"top"` | Align to top edge |
| `"center"` | Center vertically (default) |
| `"bottom"` | Align to bottom edge |
| Offset value | Pixel offset (e.g., "100px") |

**Default Position:** X = "center", Y = "center"

---

## Examples

### Alert Dialog - Top Center Position

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowAlert">Show Alert at Top Center</SfButton>

@code {
    private async Task ShowAlert()
    {
        var options = new DialogOptions()
        {
            Position = new PositionDataModel()
            {
                X = "center",
                Y = "top"
            }
        };
        
        await DialogService.AlertAsync(
            "This alert appears at the top center of the screen.",
            "Positioned Alert",
            options
        );
    }
}
```

### Confirm Dialog - Top Center Position

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowConfirm">Show Confirm at Top Center</SfButton>

@code {
    private async Task ShowConfirm()
    {
        var options = new DialogOptions()
        {
            Position = new PositionDataModel()
            {
                X = "center",
                Y = "top"
            }
        };
        
        bool confirmed = await DialogService.ConfirmAsync(
            "Do you want to proceed with this action?",
            "Positioned Confirm",
            options
        );
        
        // Handle result
    }
}
```

### Prompt Dialog - Top Center Position

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowPrompt">Show Prompt at Top Center</SfButton>

@code {
    private async Task ShowPrompt()
    {
        var options = new DialogOptions()
        {
            Position = new PositionDataModel()
            {
                X = "center",
                Y = "top"
            }
        };
        
        string input = await DialogService.PromptAsync(
            "Enter your email:",
            "",
            options
        );
        
        // Handle input
    }
}
```

---

## Common Position Configurations

### Top Left Corner

```csharp
var options = new DialogOptions()
{
    Position = new PositionDataModel()
    {
        X = "left",
        Y = "top"
    }
};
```

### Top Right Corner

```csharp
var options = new DialogOptions()
{
    Position = new PositionDataModel()
    {
        X = "right",
        Y = "top"
    }
};
```

### Bottom Center

```csharp
var options = new DialogOptions()
{
    Position = new PositionDataModel()
    {
        X = "center",
        Y = "bottom"
    }
};
```

### Bottom Right Corner

```csharp
var options = new DialogOptions()
{
    Position = new PositionDataModel()
    {
        X = "right",
        Y = "bottom"
    }
};
```

### Custom Pixel Offset

```csharp
var options = new DialogOptions()
{
    Position = new PositionDataModel()
    {
        X = "100px",
        Y = "50px"
    }
};
```

---

## Use Cases

### Notification-Style Dialogs

Position dialogs at the top or bottom of the screen for notification-style messages:

```csharp
// Top notification
var topNotification = new DialogOptions()
{
    Position = new PositionDataModel() { X = "center", Y = "top" },
    Width = "400px"
};

// Bottom notification
var bottomNotification = new DialogOptions()
{
    Position = new PositionDataModel() { X = "center", Y = "bottom" },
    Width = "400px"
};
```

### Context-Aware Positioning

Position dialogs near related UI elements:

```csharp
private async Task ShowContextDialog()
{
    var options = new DialogOptions()
    {
        Position = new PositionDataModel()
        {
            X = "right",
            Y = "top"
        },
        Width = "300px"
    };
    
    await DialogService.AlertAsync(
        "This action is related to the top-right menu.",
        "Context Help",
        options
    );
}
```

### Non-Intrusive Positioning

Keep dialogs out of the way of important content:

```csharp
// Position away from center content area
var options = new DialogOptions()
{
    Position = new PositionDataModel()
    {
        X = "left",
        Y = "bottom"
    }
};
```

---

## Tips

1. **Default Center Position:** Omit the Position property to use the default centered position.

2. **Combine with Width/Height:** Use positioning with custom dimensions for better control:
   ```csharp
   var options = new DialogOptions()
   {
       Position = new PositionDataModel() { X = "center", Y = "top" },
       Width = "500px",
       Height = "200px"
   };
   ```

3. **Responsive Positioning:** Use percentage-based widths with positioning for responsive layouts.

4. **Accessibility:** Keep dialogs visible within viewport boundaries to ensure accessibility.
