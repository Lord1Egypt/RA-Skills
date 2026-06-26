# Animation in Predefined Dialogs

## Overview

Predefined dialogs (Alert, Confirm, and Prompt) support animation effects on open and close. Customize the animation delay, duration, and effect using the `DialogOptions.AnimationSettings` property.

**Property:** `DialogOptions.AnimationSettings`  
**Type:** `DialogAnimationSettings`

---

## DialogAnimationSettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `Delay` | int | Animation delay in milliseconds |
| `Duration` | int | Animation duration in milliseconds |
| `Effect` | DialogEffect | Animation effect type |

---

## DialogEffect Enumeration

The `Effect` property accepts values from the `DialogEffect` enumeration:

| Effect | Description |
|--------|-------------|
| `DialogEffect.Zoom` | Zoom in/out animation |
| `DialogEffect.Fade` | Fade in/out animation |
| `DialogEffect.SlideTop` | Slide from/to top |
| `DialogEffect.SlideBottom` | Slide from/to bottom |
| `DialogEffect.SlideLeft` | Slide from/to left |
| `DialogEffect.SlideRight` | Slide from/to right |
| `DialogEffect.None` | No animation |

**Default:** If `AnimationSettings` is not specified, the dialog uses its default animation settings.

---

## Examples

### Alert Dialog with Zoom Animation

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowAnimatedAlert">Show Animated Alert</SfButton>

@code {
    private async Task ShowAnimatedAlert()
    {
        var options = new DialogOptions()
        {
            AnimationSettings = new DialogAnimationOptions()
            {
                Effect = DialogEffect.Zoom,
                Duration = 400,
                Delay = 0
            }
        };
        
        await DialogService.AlertAsync(
            "This alert opens with a zoom-in animation!",
            "Animated Alert",
            options
        );
    }
}
```

### Confirm Dialog with Zoom Animation

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowAnimatedConfirm">Show Animated Confirm</SfButton>

@code {
    private async Task ShowAnimatedConfirm()
    {
        var options = new DialogOptions()
        {
            AnimationSettings = new DialogAnimationOptions()
            {
                Effect = DialogEffect.Zoom,
                Duration = 400,
                Delay = 0
            }
        };
        
        bool confirmed = await DialogService.ConfirmAsync(
            "Do you want to proceed with this action?",
            "Animated Confirm",
            options
        );
    }
}
```

### Prompt Dialog with Zoom Animation

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowAnimatedPrompt">Show Animated Prompt</SfButton>

@code {
    private async Task ShowAnimatedPrompt()
    {
        var options = new DialogOptions()
        {
            AnimationSettings = new DialogAnimationOptions()
            {
                Effect = DialogEffect.Zoom,
                Duration = 400,
                Delay = 0
            }
        };
        
        string input = await DialogService.PromptAsync(
            "Enter your email:",
            "",
            options
        );
    }
}
```

---

## Animation Effect Examples

### Fade Effect

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Fade,
        Duration = 500,
        Delay = 0
    }
};

await DialogService.AlertAsync("Fade animation!", "Fade Effect", options);
```

### Slide from Top

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.SlideTop,
        Duration = 600,
        Delay = 0
    }
};

await DialogService.AlertAsync("Sliding from top!", "Slide Top", options);
```

### Slide from Bottom

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.SlideBottom,
        Duration = 600,
        Delay = 0
    }
};

await DialogService.AlertAsync("Sliding from bottom!", "Slide Bottom", options);
```

### Slide from Left

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.SlideLeft,
        Duration = 600,
        Delay = 0
    }
};

await DialogService.AlertAsync("Sliding from left!", "Slide Left", options);
```

### Slide from Right

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.SlideRight,
        Duration = 600,
        Delay = 0
    }
};

await DialogService.AlertAsync("Sliding from right!", "Slide Right", options);
```

### No Animation

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.None
    }
};

await DialogService.AlertAsync("No animation!", "Instant", options);
```

---

## Animation Duration Guidelines

### Fast Animation (200-300ms)
Best for small, quick notifications:

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Zoom,
        Duration = 250
    }
};
```

### Standard Animation (300-500ms)
Balanced speed for most use cases:

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Fade,
        Duration = 400
    }
};
```

### Slow Animation (500-800ms)
For emphasis or dramatic effect:

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Zoom,
        Duration = 700
    }
};
```

---

## Combining Animation with Other Options

### Animated Draggable Dialog

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Zoom,
        Duration = 400
    },
    AllowDragging = true,
    ShowCloseIcon = true,
    Width = "500px"
};

await DialogService.AlertAsync(
    "This dialog is animated and draggable!",
    "Interactive Dialog",
    options
);
```

### Animated Positioned Dialog

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.SlideTop,
        Duration = 500
    },
    Position = new PositionDataModel()
    {
        X = "center",
        Y = "top"
    },
    Width = "450px"
};

await DialogService.AlertAsync(
    "Notification from the top!",
    "Top Notification",
    options
);
```

### Animated Custom Styled Dialog

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Zoom,
        Duration = 400
    },
    CssClass = "custom-dialog",
    Width = "500px",
    PrimaryButtonOptions = new DialogButtonOptions()
    {
        Content = "Awesome!",
        IconCss = "e-icons e-check"
    }
};

await DialogService.AlertAsync(
    "This dialog has animation and custom styling!",
    "Styled Dialog",
    options
);
```

---

## Use Cases

### Success Notifications

Use zoom animation for success messages:

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Zoom,
        Duration = 300
    },
    Width = "400px"
};

await DialogService.AlertAsync(
    "Your changes have been saved successfully!",
    "Success",
    options
);
```

### Error Messages

Use fade animation for error messages:

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.Fade,
        Duration = 400
    }
};

await DialogService.AlertAsync(
    "An error occurred. Please try again.",
    "Error",
    options
);
```

### Top Notifications

Use slide from top for notification-style alerts:

```csharp
var options = new DialogOptions()
{
    AnimationSettings = new DialogAnimationOptions()
    {
        Effect = DialogEffect.SlideTop,
        Duration = 500
    },
    Position = new PositionDataModel()
    {
        X = "center",
        Y = "top"
    }
};

await DialogService.AlertAsync(
    "New message received!",
    "Notification",
    options
);
```

---

## Tips

1. **Default Animation:** If `AnimationSettings` is omitted, dialogs use their default animation.

2. **Performance:** Shorter durations (200-400ms) provide better user experience for frequent dialogs.

3. **Accessibility:** Some users may prefer reduced motion. Consider providing an option to disable animations.

4. **Consistency:** Use consistent animation effects throughout your application for a cohesive experience.

5. **Effect Selection:**
   - **Zoom** - Good for emphasis and drawing attention
   - **Fade** - Subtle and professional
   - **Slide** - Directional, good for notifications from specific screen edges

6. **Testing:** Test animations on different devices and browsers to ensure smooth performance.
