# Draggable Predefined Dialogs

## Overview

Predefined dialogs support dragging by the dialog header, allowing users to reposition the dialog within its target container. Enable this behavior using the `DialogOptions.AllowDragging` property.

**Property:** `DialogOptions.AllowDragging`  
**Type:** `bool`  
**Default:** `false`

**Requirements:**
- Dialog must have a visible header
- If the header is hidden or replaced, dragging behavior may be affected

---

## Enabling Draggable Behavior

### Alert Dialog - Draggable

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowDraggableAlert">Show Draggable Alert</SfButton>

@code {
    private async Task ShowDraggableAlert()
    {
        var options = new DialogOptions()
        {
            AllowDragging = true
        };
        
        await DialogService.AlertAsync(
            "You can drag this dialog by its header!",
            "Draggable Alert",
            options
        );
    }
}
```

### Confirm Dialog - Draggable

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowDraggableConfirm">Show Draggable Confirm</SfButton>

@code {
    private async Task ShowDraggableConfirm()
    {
        var options = new DialogOptions()
        {
            AllowDragging = true
        };
        
        bool confirmed = await DialogService.ConfirmAsync(
            "Do you want to proceed? Try dragging this dialog!",
            "Draggable Confirm",
            options
        );
        
        // Handle result
    }
}
```

### Prompt Dialog - Draggable

```razor
@inject SfDialogService DialogService

<SfButton @onclick="ShowDraggablePrompt">Show Draggable Prompt</SfButton>

@code {
    private async Task ShowDraggablePrompt()
    {
        var options = new DialogOptions()
        {
            AllowDragging = true
        };
        
        string input = await DialogService.PromptAsync(
            "Enter your name (drag me around!):",
            "",
            options
        );
        
        // Handle input
    }
}
```

---

## Combined with Other Options

### Draggable with Custom Dimensions

```razor
@code {
    private async Task ShowDraggableDialog()
    {
        var options = new DialogOptions()
        {
            AllowDragging = true,
            Width = "500px",
            Height = "300px"
        };
        
        await DialogService.AlertAsync(
            "This dialog is draggable and has custom dimensions.",
            "Custom Dialog",
            options
        );
    }
}
```

### Draggable with Close Icon

```razor
@code {
    private async Task ShowDraggableWithCloseIcon()
    {
        var options = new DialogOptions()
        {
            AllowDragging = true,
            ShowCloseIcon = true
        };
        
        await DialogService.AlertAsync(
            "Drag me or use the close icon!",
            "Interactive Dialog",
            options
        );
    }
}
```

### Draggable with Custom Position

```razor
@code {
    private async Task ShowDraggableAtTopRight()
    {
        var options = new DialogOptions()
        {
            AllowDragging = true,
            Position = new PositionDataModel()
            {
                X = "right",
                Y = "top"
            },
            Width = "400px"
        };
        
        await DialogService.AlertAsync(
            "Starts at top-right but you can drag me anywhere!",
            "Positioned Draggable",
            options
        );
    }
}
```

---

## Use Cases

### Long-Running Operations

Allow users to move dialogs showing progress or status updates:

```razor
private async Task ShowProgressDialog()
{
    var options = new DialogOptions()
    {
        AllowDragging = true,
        Width = "450px"
    };
    
    await DialogService.AlertAsync(
        "Processing your request. This may take a few moments...",
        "Please Wait",
        options
    );
}
```

### Multi-Window Workflows

Enable dragging when users may need to see content behind the dialog:

```razor
private async Task ShowReferenceDialog()
{
    var options = new DialogOptions()
    {
        AllowDragging = true,
        Width = "500px"
    };
    
    await DialogService.AlertAsync(
        "Reference information that you might want to move aside.",
        "Reference Guide",
        options
    );
}
```

### Comparison or Side-by-Side Viewing

Allow users to position dialogs for better visibility:

```razor
private async Task ShowComparisonDialog()
{
    var options = new DialogOptions()
    {
        AllowDragging = true,
        Width = "350px"
    };
    
    await DialogService.AlertAsync(
        "Compare this with other content by dragging the dialog.",
        "Comparison View",
        options
    );
}
```

---

## Important Notes

1. **Header Requirement:** Dragging works by clicking and dragging the dialog header. If you customize the dialog to hide the header, dragging will not work.

2. **Container Boundaries:** The dialog is constrained to its container and cannot be dragged outside the viewport.

3. **Touch Support:** Dragging is supported on touch devices - users can drag using touch gestures.

4. **Default Behavior:** By default (`AllowDragging = false`), dialogs remain in their initial position and cannot be moved.

5. **User Experience:** Enable dragging when:
   - Users might need to see content behind the dialog
   - The dialog displays reference information
   - Multiple dialogs might be open simultaneously
   - Long-running operations are displayed

6. **Avoid When:** Don't enable dragging for:
   - Critical confirmation dialogs that should demand attention
   - Quick alert messages that auto-close
   - Dialogs that should remain centered for accessibility
