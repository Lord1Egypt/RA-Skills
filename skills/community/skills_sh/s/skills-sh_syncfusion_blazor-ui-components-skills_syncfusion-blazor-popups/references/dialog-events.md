# Events in Blazor Dialog

## Table of Contents
- [Overview](#overview)
- [Lifecycle Events](#lifecycle-events)
- [Visibility Events](#visibility-events)
- [Drag Events](#drag-events)
- [Resize Events](#resize-events)
- [Modal Events](#modal-events)
- [Event Handling Examples](#event-handling-examples)

## Overview

The Blazor Dialog component provides a comprehensive event system for handling lifecycle, visibility changes, user interactions, and configuration changes. Events are triggered at specific points during the dialog's existence and user interaction.

**Event Structure:**
```csharp
<SfDialog>
    <DialogEvents EventName="@EventHandler" />
</SfDialog>

@code {
    private void EventHandler(EventArgs args)
    {
        // Handle event
    }
}
```

## Lifecycle Events

### Created Event

Fires when the dialog is initialized and rendered in the DOM. Use this to perform setup operations.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Dialog">
    <DialogTemplates>
        <Content>Dialog has been created</Content>
    </DialogTemplates>
    <DialogEvents Created="@OnCreated" />
</SfDialog>

@code {
    private void OnCreated(object args)
    {
        Console.WriteLine("Dialog created");
        // Perform initialization tasks
    }
}
```

### Destroyed Event

Fires when the dialog component is removed from the DOM. Use this for cleanup operations.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Dialog" @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>Dialog content</Content>
    </DialogTemplates>
    <DialogEvents Destroyed="@OnDestroyed" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnDestroyed(object args)
    {
        Console.WriteLine("Dialog destroyed");
        // Cleanup resources
    }
}
```

## Visibility Events

### VisibleChanged Event

Fires when the `Visible` property changes. Used for two-way binding synchronization.

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ToggleDialog">Toggle Dialog</SfButton>
<p>Dialog is: @(DialogVisible ? "Visible" : "Hidden")</p>

<SfDialog @bind-Visible="DialogVisible" Header="Visibility Binding">
    <DialogTemplates>
        <Content>Dialog content</Content>
    </DialogTemplates>
    <DialogEvents VisibleChanged="@OnVisibleChanged" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = false;

    private void ToggleDialog() => DialogVisible = !DialogVisible;

    private void OnVisibleChanged(bool isVisible)
    {
        Console.WriteLine($"Dialog visibility changed to: {isVisible}");
    }
}
```

**Remarks:**
- This event is automatically invoked when `@bind-Visible` binding changes
- Useful for tracking visibility state changes in parent component
- Works bidirectionally: property changes trigger the event and event can update the property

### OnOpen Event

Fires **before** the dialog is opened. Use this to validate or prevent opening under certain conditions.

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@OpenDialog">Open</SfButton>

<SfDialog @bind-Visible="DialogVisible" Header="Before Open">
    <DialogTemplates>
        <Content>Opening event fired before dialog displays</Content>
    </DialogTemplates>
    <DialogEvents OnOpen="@BeforeOpenHandler" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = false;
    private bool CanOpen { get; set; } = true;

    private void OpenDialog() => DialogVisible = true;

    private void BeforeOpenHandler(BeforeOpenEventArgs args)
    {
        if (!CanOpen)
        {
            args.Cancel = true; // Prevent dialog from opening
            Console.WriteLine("Dialog opening prevented");
        }
        else
        {
            Console.WriteLine("Dialog is about to open");
        }
    }
}
```

### Opened Event

Fires **after** the dialog has been fully displayed and is visible to the user.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog @bind-Visible="DialogVisible" Header="After Open">
    <DialogTemplates>
        <Content>Dialog is now open</Content>
    </DialogTemplates>
    <DialogEvents Opened="@OnOpenedHandler" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void OnOpenedHandler(OpenEventArgs args)
    {
        Console.WriteLine("Dialog opened and displayed");
        // Perform actions after dialog is visible
    }
}
```

### OnClose Event

Fires **before** the dialog closes. Use this to validate or prevent closing.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog @bind-Visible="DialogVisible" Header="Before Close">
    <DialogTemplates>
        <Content>Close event fires before dialog hides</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Close" OnClick="@CloseDialog" />
    </DialogButtons>
    <DialogEvents OnClose="@BeforeCloseHandler" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;
    private bool HasUnsavedChanges { get; set; } = true;

    private void CloseDialog() => DialogVisible = false;

    private void BeforeCloseHandler(BeforeCloseEventArgs args)
    {
        if (HasUnsavedChanges)
        {
            args.Cancel = true; // Prevent closing
            Console.WriteLine("Cannot close - unsaved changes");
        }
    }
}
```

### Closed Event

Fires **after** the dialog has been closed and is hidden from view.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog @bind-Visible="DialogVisible" Header="After Close">
    <DialogTemplates>
        <Content>Dialog is closed</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Close" OnClick="@CloseDialog" />
    </DialogButtons>
    <DialogEvents Closed="@OnClosedHandler" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void CloseDialog() => DialogVisible = false;

    private void OnClosedHandler(CloseEventArgs args)
    {
        Console.WriteLine("Dialog closed and hidden");
    }
}
```

## Drag Events

### OnDragStart Event

Fires when the user begins dragging the dialog header.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog AllowDragging="true" Header="Draggable Dialog">
    <DialogTemplates>
        <Content>Drag the header to move this dialog</Content>
    </DialogTemplates>
    <DialogEvents OnDragStart="@OnDragStartHandler" />
</SfDialog>

@code {
    private void OnDragStartHandler(DragStartEventArgs args)
    {
        Console.WriteLine("Drag started");
    }
}
```

### OnDrag Event

Fires continuously while the user is dragging the dialog.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog AllowDragging="true" Header="Position Tracker">
    <DialogTemplates>
        <Content>Current Position: X = @PositionX, Y = @PositionY</Content>
    </DialogTemplates>
    <DialogEvents OnDrag="@OnDragHandler" />
</SfDialog>

@code {
    private int PositionX { get; set; } = 0;
    private int PositionY { get; set; } = 0;

    private void OnDragHandler(DragEventArgs args)
    {
        PositionX = (int)args.Data.OffsetX;
        PositionY = (int)args.Data.OffsetY;
    }
}
```

### OnDragStop Event

Fires when the user stops dragging the dialog.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog AllowDragging="true" Header="Drag Stop">
    <DialogTemplates>
        <Content>Dialog drag completed at position: @FinalPosition</Content>
    </DialogTemplates>
    <DialogEvents OnDragStop="@OnDragStopHandler" />
</SfDialog>

@code {
    private string FinalPosition { get; set; } = "Not dragged yet";

    private void OnDragStopHandler(DragStopEventArgs args)
    {
        FinalPosition = $"X: {args.Data.OffsetX}, Y: {args.Data.OffsetY}";
        Console.WriteLine($"Drag stopped at {FinalPosition}");
    }
}
```

## Resize Events

### OnResizeStart Event

Fires when the user begins resizing the dialog.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog EnableResize="true" Header="Resizable Dialog">
    <DialogTemplates>
        <Content>Drag the edges to resize this dialog</Content>
    </DialogTemplates>
    <DialogEvents OnResizeStart="@OnResizeStartHandler" />
</SfDialog>

@code {
    private void OnResizeStartHandler(MouseEventArgs args)
    {
        Console.WriteLine("Resize started");
    }
}
```

### Resizing Event

Fires continuously while the user is resizing the dialog.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog EnableResize="true" Header="Size Tracker">
    <DialogTemplates>
        <Content>
            <p>Current Width: @CurrentWidth</p>
            <p>Current Height: @CurrentHeight</p>
        </Content>
    </DialogTemplates>
    <DialogEvents Resizing="@OnResizingHandler" />
</SfDialog>

@code {
    private string CurrentWidth { get; set; } = "400px";
    private string CurrentHeight { get; set; } = "300px";

    private void OnResizingHandler(MouseEventArgs args)
    {
        // Update size display (dimension tracking)
    }
}
```

### OnResizeStop Event

Fires when the user stops resizing the dialog.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog EnableResize="true" Header="Resize Complete">
    <DialogTemplates>
        <Content>Final Size: @FinalSize</Content>
    </DialogTemplates>
    <DialogEvents OnResizeStop="@OnResizeStopHandler" />
</SfDialog>

@code {
    private string FinalSize { get; set; } = "Not resized yet";

    private void OnResizeStopHandler(MouseEventArgs args)
    {
        FinalSize = "Resize operation completed";
        Console.WriteLine("Resize stopped");
    }
}
```

## Modal Events

### OnOverlayModalClick Event

Fires when the user clicks on the modal overlay (background). Only fires in modal dialogs.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog IsModal="true" Header="Modal Dialog">
    <DialogTemplates>
        <Content>Click the overlay to see the event fire</Content>
    </DialogTemplates>
    <DialogEvents OnOverlayModalClick="@OnOverlayClickHandler" />
</SfDialog>

@code {
    private void OnOverlayClickHandler(OverlayModalClickEventArgs args)
    {
        Console.WriteLine("Overlay clicked");
        // Prevent default behavior or handle overlay click
    }
}
```

## Event Handling Examples

### Complete Form Submission Example

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@OpenDialog">Open Form</SfButton>

<SfDialog @bind-Visible="DialogVisible" 
          Header="User Registration" 
          Width="400px"
          ShowCloseIcon="true">
    <DialogTemplates>
        <Content>
            <div>
                <input @bind="UserName" placeholder="Enter name" />
                <input @bind="UserEmail" type="email" placeholder="Enter email" />
            </div>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Submit" IsPrimary="true" OnClick="@OnSubmit" />
        <DialogButton Content="Cancel" OnClick="@OnCancel" />
    </DialogButtons>
    <DialogEvents 
        OnOpen="@BeforeOpenHandler"
        Opened="@OnOpenedHandler"
        OnClose="@BeforeCloseHandler"
        Closed="@OnClosedHandler" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = false;
    private string UserName { get; set; }
    private string UserEmail { get; set; }

    private void OpenDialog() => DialogVisible = true;

    private void BeforeOpenHandler(BeforeOpenEventArgs args)
    {
        Console.WriteLine("Dialog opening - performing validation");
    }

    private void OnOpenedHandler(OpenEventArgs args)
    {
        Console.WriteLine("Dialog opened - focus on first input");
    }

    private void BeforeCloseHandler(BeforeCloseEventArgs args)
    {
        if (string.IsNullOrEmpty(UserName) || string.IsNullOrEmpty(UserEmail))
        {
            args.Cancel = true;
            Console.WriteLine("Cannot close - incomplete form");
        }
    }

    private void OnClosedHandler(CloseEventArgs args)
    {
        Console.WriteLine("Dialog closed - resetting form");
        UserName = "";
        UserEmail = "";
    }

    private void OnSubmit()
    {
        Console.WriteLine($"Form submitted: {UserName}, {UserEmail}");
        DialogVisible = false;
    }

    private void OnCancel()
    {
        DialogVisible = false;
    }
}
```

### Dialog with Activity Logging

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog @bind-Visible="DialogVisible" Header="Activity Log">
    <DialogTemplates>
        <Content>
            <ul>
                @foreach (var log in ActivityLogs)
                {
                    <li>@log</li>
                }
            </ul>
        </Content>
    </DialogTemplates>
    <DialogEvents 
        Created="@OnCreated"
        OnOpen="@OnOpen"
        Opened="@OnOpened"
        OnDragStart="@OnDragStart"
        OnDragStop="@OnDragStop" />
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;
    private List<string> ActivityLogs { get; set; } = new();

    private void OnCreated(object args) => AddLog("Dialog created");
    private void OnOpen(BeforeOpenEventArgs args) => AddLog("Dialog opening");
    private void OnOpened(OpenEventArgs args) => AddLog("Dialog opened");
    private void OnDragStart(DragStartEventArgs args) => AddLog("Drag started");
    private void OnDragStop(DragStopEventArgs args) => AddLog("Drag stopped");

    private void AddLog(string message)
    {
        ActivityLogs.Add($"{DateTime.Now:HH:mm:ss} - {message}");
        StateHasChanged();
    }
}
```

## Event Argument Classes Reference

### BeforeOpenEventArgs
Provides data for the `OnOpen` event, allowing you to control whether the dialog opens.

| Property | Type | Description |
|----------|------|-------------|
| `Cancel` | bool | Set to `true` to prevent the dialog from opening |
| `Element` | object | The dialog element reference |
| `Event` | object | The browser event that triggered opening |
| `MaxHeight` | string | Maximum height of the dialog |
| `Target` | string | Target element selector |

**Example:**
```csharp
private void BeforeOpenHandler(BeforeOpenEventArgs args)
{
    if (!IsUserAuthorized)
    {
        args.Cancel = true; // Prevent dialog from opening
    }
}
```

### BeforeCloseEventArgs
Provides data for the `OnClose` event, allowing you to control whether the dialog closes.

| Property | Type | Description |
|----------|------|-------------|
| `Cancel` | bool | Set to `true` to prevent the dialog from closing |
| `ClosedBy` | string | How the dialog was closed (e.g., "EscapeKey", "CloseIcon", "Overlay") |
| `Element` | object | The dialog element reference |
| `Event` | object | The browser event that triggered closing |
| `IsInteracted` | bool | Indicates if closing was triggered by user interaction |

**Example:**
```csharp
private void BeforeCloseHandler(BeforeCloseEventArgs args)
{
    if (HasUnsavedChanges && args.ClosedBy == "EscapeKey")
    {
        args.Cancel = true; // Prevent closing on Escape if unsaved changes
    }
}
```

### OpenEventArgs
Provides data for the `Opened` event after the dialog has fully opened.

| Property | Type | Description |
|----------|------|-------------|
| `Element` | object | The dialog element reference |
| `Name` | string | Event name ("Opened") |

### CloseEventArgs
Provides data for the `Closed` event after the dialog has fully closed.

| Property | Type | Description |
|----------|------|-------------|
| `Element` | object | The dialog element reference |
| `Event` | object | The browser event reference |
| `IsInteracted` | bool | Indicates if closed by user interaction |
| `Name` | string | Event name ("Closed") |

### DragStartEventArgs
Provides data when dragging begins.

| Property | Type | Description |
|----------|------|-------------|
| `Element` | object | The dialog element being dragged |
| `Event` | MouseEventArgs | Browser mouse event data |
| `Target` | object | The drag handle element |

### DragEventArgs
Provides data continuously while dragging.

| Property | Type | Description |
|----------|------|-------------|
| `Data.OffsetX` | double | Current X position offset |
| `Data.OffsetY` | double | Current Y position offset |
| `Element` | object | The dialog element being dragged |
| `Event` | MouseEventArgs | Browser mouse event data |

**Example:**
```csharp
private void OnDragHandler(DragEventArgs args)
{
    CurrentX = args.Data.OffsetX;
    CurrentY = args.Data.OffsetY;
    Console.WriteLine($"Position: ({CurrentX}, {CurrentY})");
}
```

### DragStopEventArgs
Provides data when dragging stops.

| Property | Type | Description |
|----------|------|-------------|
| `Data.OffsetX` | double | Final X position offset |
| `Data.OffsetY` | double | Final Y position offset |
| `Element` | object | The dialog element |
| `Event` | MouseEventArgs | Browser mouse event data |
| `Helper` | object | The drag helper element |
| `Target` | object | The drop target element |

### OverlayModalClickEventArgs
Provides data when the modal overlay is clicked.

| Property | Type | Description |
|----------|------|-------------|
| `Cancel` | bool | Set to `true` to prevent default overlay click behavior |
| `Element` | object | The overlay element |
| `Event` | MouseEventArgs | Browser mouse event data |

**Example:**
```csharp
private void OnOverlayClickHandler(OverlayModalClickEventArgs args)
{
    if (HasUnsavedChanges)
    {
        args.Cancel = true; // Prevent closing on overlay click
        ShowWarningMessage();
    }
}
```

## Best Practices

1. **Use OnOpen to Validate**: Check conditions before dialog opens
2. **Use OnClose to Warn**: Alert users before they close with unsaved changes
3. **Clean Up in Destroyed**: Release resources and subscriptions
4. **Event Cancellation**: Set `Cancel = true` in BeforeOpenEventArgs or BeforeCloseEventArgs to prevent default behavior
5. **Async Operations**: Use async handlers for time-consuming operations
6. **Error Handling**: Wrap event handlers in try-catch for error handling
7. **State Management**: Update component state to reflect dialog changes
8. **Performance**: Avoid heavy computations in frequently-firing events (like Resizing or OnDrag)
9. **Check Event Source**: Use `ClosedBy` property to determine how dialog was closed
10. **Validate Drag Bounds**: Monitor drag positions to keep dialog within valid boundaries
