# Dialog Behavior and Features

## Table of Contents
- [Modal vs Modeless](#modal-vs-modeless)
- [Draggable Dialogs](#draggable-dialogs)
- [Resizable Dialogs](#resizable-dialogs)
- [AllowPrerender](#allowprerender)
- [Close Icon](#close-icon)
- [Nested Dialogs](#nested-dialogs)
- [Animations](#animations)
- [Best Practices](#best-practices)

## Modal vs Modeless

### Modal Dialog (Blocking)

A modal dialog displays an overlay that prevents interaction with the rest of the page until the dialog is closed.

**When to Use Modal:**
- Critical confirmations (delete operations)
- Required form submissions
- Important alerts requiring user attention
- Capturing essential user input

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog IsModal="true" Header="Confirm Delete" Width="350px">
    <DialogTemplates>
        <Content>
            <p>Are you sure you want to delete this item?</p>
            <p>This action cannot be undone.</p>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Delete" IsPrimary="true" />
        <DialogButton Content="Cancel" />
    </DialogButtons>
</SfDialog>
```

**Key Properties:**
- `IsModal="true"` - Creates overlay blocking page interaction
- Overlay prevents clicking outside the dialog
- Overlay click can be handled with `OnOverlayModalClick` event

### Modeless Dialog (Non-Blocking)

A modeless dialog floats above the page without blocking interaction with the rest of the page content.

**When to Use Modeless:**
- Help or reference dialogs
- Floating palettes or toolbars
- Secondary information displays
- Non-critical notifications
- Chat windows or floating panels

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog IsModal="false" 
          Header="Helpful Tips" 
          Width="300px"
          AllowDragging="true">
    <DialogTemplates>
        <Content>
            <p>Tip 1: Use keyboard shortcuts for faster navigation</p>
            <p>Tip 2: Save your work frequently</p>
        </Content>
    </DialogTemplates>
</SfDialog>
```

**Key Properties:**
- `IsModal="false"` or omitted (default is false)
- User can interact with page while dialog is open
- Dialog floats above page content

### Comparison

| Feature | Modal | Modeless |
|---------|-------|----------|
| **Blocks Page Interaction** | Yes | No |
| **Overlay Background** | Yes | No |
| **Use Case** | Critical actions | Information/Help |
| **User Can Multi-task** | No | Yes |
| **Best For** | Forms, Confirmations | Floating panels, Tips |

## Draggable Dialogs

The `AllowDragging` property enables users to drag the dialog by its header to reposition it on the screen.

### Basic Draggable Dialog

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog AllowDragging="true" Header="Draggable Dialog">
    <DialogTemplates>
        <Content>Drag the header to move this dialog around the page</Content>
    </DialogTemplates>
</SfDialog>
```

### Draggable with Restricted Movement

```csharp
@using Syncfusion.Blazor.Popups

<div id="restricted-area" style="position: relative; width: 600px; height: 400px; border: 2px solid #333;">
    <SfDialog Target="#restricted-area"
              AllowDragging="true"
              Header="Restricted Drag"
              Width="300px">
        <DialogTemplates>
            <Content>Dialog can only be dragged within the container</Content>
        </DialogTemplates>
    </SfDialog>
</div>
```

### Tracking Drag Position

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog AllowDragging="true" Header="Position Tracker">
    <DialogTemplates>
        <Content>
            <p>X Position: @DialogX</p>
            <p>Y Position: @DialogY</p>
            <p>Status: @DragStatus</p>
        </Content>
    </DialogTemplates>
    <DialogEvents 
        OnDragStart="@OnDragStart"
        OnDrag="@OnDrag"
        OnDragStop="@OnDragStop" />
</SfDialog>

@code {
    private double DialogX { get; set; }
    private double DialogY { get; set; }
    private string DragStatus { get; set; } = "Idle";

    private void OnDragStart(DragStartEventArgs args)
    {
        DragStatus = "Dragging...";
    }

    private void OnDrag(DragEventArgs args)
    {
        DialogX = args.Data.OffsetX;
        DialogY = args.Data.OffsetY;
    }

    private void OnDragStop(DragStopEventArgs args)
    {
        DragStatus = "Stopped";
    }
}
```

## Resizable Dialogs

The `AllowResizing` property enables users to resize the dialog by dragging its edges or corners.

### Basic Resizable Dialog

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog EnableResize="true" Header="Resizable Dialog" Width="400px" Height="300px">
    <DialogTemplates>
        <Content>
            <p>Drag the edges or corners to resize this dialog</p>
            <p>You can make it smaller or larger as needed</p>
        </Content>
    </DialogTemplates>
</SfDialog>
```

### Resizable with Min/Max Constraints

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog EnableResize="true" 
          Header="Constrained Resize" 
          Width="400px" 
          Height="300px"
          CssClass="resizable-constrained">
    <DialogTemplates>
        <Content>
            <p>This dialog cannot be smaller than 300x200 or larger than 800x600</p>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .resizable-constrained.e-dialog {
        min-width: 300px;
        min-height: 200px;
        max-width: 800px;
        max-height: 600px;
    }
</style>
```

### Tracking Resize Events

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog EnableResize="true" Header="Resize Tracker" Width="400px">
    <DialogTemplates>
        <Content>
            <p>Resize Status: @ResizeStatus</p>
            <p>Last resized: @LastResizeTime</p>
        </Content>
    </DialogTemplates>
    <DialogEvents 
        OnResizeStart="@OnResizeStart"
        Resizing="@OnResizing"
        OnResizeStop="@OnResizeStop" />
</SfDialog>

@code {
    private string ResizeStatus { get; set; } = "Idle";
    private string LastResizeTime { get; set; } = "Never";

    private void OnResizeStart(MouseEventArgs args)
    {
        ResizeStatus = "Resizing...";
    }

    private void OnResizing(MouseEventArgs args)
    {
        // Continuous resize tracking
    }

    private void OnResizeStop(MouseEventArgs args)
    {
        ResizeStatus = "Stopped";
        LastResizeTime = DateTime.Now.ToString("HH:mm:ss");
    }
}
```

## AllowPrerender

The `AllowPrerender` property controls whether dialog DOM elements are kept in the DOM when the dialog is hidden.

### AllowPrerender = false (Default)

Dialog DOM elements are removed and recreated each time the dialog is shown. Saves memory but slower to show.

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ToggleDialog">Toggle Dialog</SfButton>

<SfDialog @bind-Visible="DialogVisible"
          AllowPrerender="false"
          Header="Memory Optimized">
    <DialogTemplates>
        <Content>
            <p>DOM elements are removed when dialog is hidden</p>
            <p>Saves memory but slower to show</p>
            <p>Render count: @RenderCount</p>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = false;
    private int RenderCount { get; set; } = 0;

    private void ToggleDialog()
    {
        DialogVisible = !DialogVisible;
        RenderCount++;
    }
}
```

### AllowPrerender = true

Dialog DOM elements remain in the DOM even when hidden. Uses more memory but faster to show.

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ToggleDialog">Toggle Dialog</SfButton>

<SfDialog @bind-Visible="DialogVisible"
          AllowPrerender="true"
          Header="Performance Optimized">
    <DialogTemplates>
        <Content>
            <p>DOM elements stay in memory when hidden</p>
            <p>Faster to show but uses more memory</p>
            <p>Toggle count: @ToggleCount</p>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = false;
    private int ToggleCount { get; set; } = 0;

    private void ToggleDialog()
    {
        DialogVisible = !DialogVisible;
        ToggleCount++;
    }
}
```

## Close Icon

The `ShowCloseIcon` property displays a close button in the dialog header.

### With Close Icon

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog ShowCloseIcon="true" 
          @bind-Visible="DialogVisible"
          Header="Dialog with Close">
    <DialogTemplates>
        <Content>
            <p>Click the X button in the header to close this dialog</p>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;
}
```

### Without Close Icon

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog ShowCloseIcon="false" Header="Dialog without Close">
    <DialogTemplates>
        <Content>
            <p>No close button in header</p>
            <p>Must use button or other means to close</p>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="OK" OnClick="@CloseDialog" IsPrimary="true" />
    </DialogButtons>
</SfDialog>
```

## Nested Dialogs

You can create dialogs that open other dialogs, creating a hierarchy.

### Basic Nested Dialogs

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@OpenDialog1">Open Dialog 1</SfButton>

<SfDialog @bind-Visible="Dialog1Visible" 
          Header="Parent Dialog" 
          Width="400px"
          ZIndex="1000">
    <DialogTemplates>
        <Content>
            <p>This is the parent dialog</p>
            <SfButton OnClick="@OpenDialog2">Open Dialog 2</SfButton>
        </Content>
    </DialogTemplates>
</SfDialog>

<SfDialog @bind-Visible="Dialog2Visible" 
          Header="Child Dialog" 
          Width="350px"
          ZIndex="1001">
    <DialogTemplates>
        <Content>
            <p>This is a nested child dialog</p>
            <SfButton OnClick="@OpenDialog3">Open Dialog 3</SfButton>
        </Content>
    </DialogTemplates>
</SfDialog>

<SfDialog @bind-Visible="Dialog3Visible" 
          Header="Grandchild Dialog" 
          Width="300px"
          ZIndex="1002">
    <DialogTemplates>
        <Content>This is a nested grandchild dialog</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool Dialog1Visible { get; set; } = false;
    private bool Dialog2Visible { get; set; } = false;
    private bool Dialog3Visible { get; set; } = false;

    private void OpenDialog1() => Dialog1Visible = true;
    private void OpenDialog2() => Dialog2Visible = true;
    private void OpenDialog3() => Dialog3Visible = true;
}
```

### Nested Dialogs with Data Passing

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog @bind-Visible="ParentOpen" Header="Parent" ZIndex="1000">
    <DialogTemplates>
        <Content>
            <p>Data: @SelectedData</p>
            <SfButton OnClick="@OpenChild">Open Child</SfButton>
        </Content>
    </DialogTemplates>
</SfDialog>

<SfDialog @bind-Visible="ChildOpen" Header="Child" ZIndex="1001">
    <DialogTemplates>
        <Content>
            <input @bind="ChildData" placeholder="Enter data" />
            <SfButton OnClick="@PassDataToParent">Pass to Parent</SfButton>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool ParentOpen { get; set; } = true;
    private bool ChildOpen { get; set; } = false;
    private string SelectedData { get; set; } = "";
    private string ChildData { get; set; } = "";

    private void OpenChild() => ChildOpen = true;

    private void PassDataToParent()
    {
        SelectedData = ChildData;
        ChildOpen = false;
    }
}
```

## Animations

The Dialog component supports rich animations when opening and closing through the `AnimationSettings` property.

### DialogAnimationSettings Class

Configure dialog animations using the `DialogAnimationSettings` class:

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `Effect` | DialogEffect | Animation effect type | DialogEffect.Fade |
| `Duration` | int | Animation duration in milliseconds | 400 |
| `Delay` | int | Animation delay before starting (milliseconds) | 0 |

### DialogEffect Enum Values

| Effect | Description | Visual Behavior |
|--------|-------------|-----------------|
| `None` | No animation | Dialog appears/disappears instantly |
| `Fade` | Fade in/out | Gradual opacity transition (default) |
| `FadeZoom` | Combined fade and zoom | Fade with scaling effect |
| `Zoom` | Zoom in/out | Scale-based zoom effect from/to center point |
| `SlideLeft` | Slide from/to left | Horizontal slide from left side |
| `SlideRight` | Slide from/to right | Horizontal slide from right side |
| `SlideTop` | Slide from/to top | Vertical slide from top |
| `SlideBottom` | Slide from/to bottom | Vertical slide from bottom |
| `FlipLeftDown` | Flip left to down | Flip animation from left to down |
| `FlipLeftUp` | Flip left to up | Flip animation from left to up |
| `FlipRightDown` | Flip right to down | Flip animation from right to down |
| `FlipRightUp` | Flip right to up | Flip animation from right to up |
| `FlipXDown` | Horizontal flip down | Horizontal flip with downward motion |
| `FlipXUp` | Horizontal flip up | Horizontal flip with upward motion |
| `FlipYLeft` | Vertical flip left | Vertical flip with leftward motion |
| `FlipYRight` | Vertical flip right | Vertical flip with rightward motion |

### Basic Animation Configuration

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Animated Dialog"
          AnimationSettings="@AnimSettings">
    <DialogTemplates>
        <Content>Dialog with custom animation</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private DialogAnimationSettings AnimSettings = new DialogAnimationSettings
    {
        Effect = DialogEffect.Fade,
        Duration = 300,
        Delay = 0
    };
}
```

### All Animation Effects Examples

```csharp
@using Syncfusion.Blazor.Popups

<!-- Fade Effect (Default) -->
<SfDialog Header="Fade Animation" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.Fade, Duration = 400 }">
    <DialogTemplates>
        <Content>Smooth fade in/out effect</Content>
    </DialogTemplates>
</SfDialog>

<!-- FadeZoom Effect -->
<SfDialog Header="FadeZoom Animation" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FadeZoom, Duration = 400 }">
    <DialogTemplates>
        <Content>Combined fade and zoom effect</Content>
    </DialogTemplates>
</SfDialog>

<!-- Zoom Effect -->
<SfDialog Header="Zoom Animation" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.Zoom, Duration = 300 }">
    <DialogTemplates>
        <Content>Scale-based zoom effect</Content>
    </DialogTemplates>
</SfDialog>

<!-- Slide Effects -->
<SfDialog Header="Slide Left" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.SlideLeft, Duration = 350 }">
    <DialogTemplates>
        <Content>Slides in from the left side</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Slide Right" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.SlideRight, Duration = 350 }">
    <DialogTemplates>
        <Content>Slides in from the right side</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Slide Top" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.SlideTop, Duration = 350 }">
    <DialogTemplates>
        <Content>Slides down from the top</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Slide Bottom" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.SlideBottom, Duration = 350 }">
    <DialogTemplates>
        <Content>Slides up from the bottom</Content>
    </DialogTemplates>
</SfDialog>

<!-- Flip Effects - Basic Directional -->
<SfDialog Header="Flip Left Down" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipLeftDown, Duration = 500 }">
    <DialogTemplates>
        <Content>Flip animation from left to down</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Flip Left Up" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipLeftUp, Duration = 500 }">
    <DialogTemplates>
        <Content>Flip animation from left to up</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Flip Right Down" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipRightDown, Duration = 500 }">
    <DialogTemplates>
        <Content>Flip animation from right to down</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Flip Right Up" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipRightUp, Duration = 500 }">
    <DialogTemplates>
        <Content>Flip animation from right to up</Content>
    </DialogTemplates>
</SfDialog>

<!-- Flip Effects - Axis Based -->
<SfDialog Header="Flip X Down" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipXDown, Duration = 500 }">
    <DialogTemplates>
        <Content>Horizontal flip with downward motion</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Flip X Up" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipXUp, Duration = 500 }">
    <DialogTemplates>
        <Content>Horizontal flip with upward motion</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Flip Y Left" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipYLeft, Duration = 500 }">
    <DialogTemplates>
        <Content>Vertical flip with leftward motion</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Flip Y Right" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.FlipYRight, Duration = 500 }">
    <DialogTemplates>
        <Content>Vertical flip with rightward motion</Content>
    </DialogTemplates>
</SfDialog>

<!-- No Animation -->
<SfDialog Header="Instant Display" 
          AnimationSettings="@new DialogAnimationSettings { Effect = DialogEffect.None }">
    <DialogTemplates>
        <Content>No animation - appears instantly</Content>
    </DialogTemplates>
</SfDialog>
```

### Animation with Delay

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Delayed Animation"
          AnimationSettings="@DelayedAnimSettings">
    <DialogTemplates>
        <Content>This dialog animation starts after a 200ms delay</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private DialogAnimationSettings DelayedAnimSettings = new DialogAnimationSettings
    {
        Effect = DialogEffect.Zoom,
        Duration = 300,
        Delay = 200 // Wait 200ms before starting animation
    };
}
```

### Dynamic Animation Control

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.DropDowns

<div>
    <label>Select Animation Effect:</label>
    <select @onchange="@ChangeAnimationEffect">
        <option value="Fade">Fade</option>
        <option value="FadeZoom">FadeZoom</option>
        <option value="Zoom">Zoom</option>
        <option value="SlideLeft">Slide Left</option>
        <option value="SlideRight">Slide Right</option>
        <option value="SlideTop">Slide Top</option>
        <option value="SlideBottom">Slide Bottom</option>
        <option value="FlipLeftDown">Flip Left Down</option>
        <option value="FlipLeftUp">Flip Left Up</option>
        <option value="FlipRightDown">Flip Right Down</option>
        <option value="FlipRightUp">Flip Right Up</option>
        <option value="FlipXDown">Flip X Down</option>
        <option value="FlipXUp">Flip X Up</option>
        <option value="FlipYLeft">Flip Y Left</option>
        <option value="FlipYRight">Flip Y Right</option>
        <option value="None">None</option>
    </select>
    
    <label>Duration (ms):</label>
    <input type="number" @bind="AnimDuration" min="100" max="2000" step="50" />
    
    <button @onclick="@ToggleDialog">Toggle Dialog</button>
</div>

<SfDialog @bind-Visible="ShowDialog"
          Header="Dynamic Animation"
          AnimationSettings="@CurrentAnimSettings">
    <DialogTemplates>
        <Content>
            <p>Current Effect: @CurrentEffect</p>
            <p>Duration: @AnimDuration ms</p>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool ShowDialog { get; set; } = false;
    private string CurrentEffect { get; set; } = "Fade";
    private int AnimDuration { get; set; } = 400;
    
    private DialogAnimationSettings CurrentAnimSettings => new DialogAnimationSettings
    {
        Effect = Enum.Parse<DialogEffect>(CurrentEffect),
        Duration = AnimDuration,
        Delay = 0
    };
    
    private void ChangeAnimationEffect(ChangeEventArgs e)
    {
        CurrentEffect = e.Value?.ToString() ?? "Fade";
    }
    
    private void ToggleDialog() => ShowDialog = !ShowDialog;
}
```

### Animation Best Practices

1. **Performance**: Keep Duration between 200-600ms for smooth user experience
2. **Accessibility**: Respect user's motion preferences with `prefers-reduced-motion` media query
3. **Context**: Use appropriate effects (e.g., SlideTop for notifications, Fade for modals)
4. **Consistency**: Use the same animation effect throughout your application
5. **Testing**: Test animations on slower devices to ensure acceptable performance
6. **Delay Usage**: Use Delay sparingly; only when you need sequential animations
7. **None Effect**: Use DialogEffect.None for performance-critical scenarios or accessibility

### Accessibility Considerations

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Accessible Animation"
          AnimationSettings="@AccessibleAnimSettings">
    <DialogTemplates>
        <Content>Respects user's motion preferences</Content>
    </DialogTemplates>
</SfDialog>

@code {
    [Inject] IJSRuntime JS { get; set; }
    
    private DialogAnimationSettings AccessibleAnimSettings { get; set; }
    
    protected override async Task OnInitializedAsync()
    {
        // Check if user prefers reduced motion
        var prefersReducedMotion = await JS.InvokeAsync<bool>(
            "window.matchMedia", "(prefers-reduced-motion: reduce)").matches;
        
        AccessibleAnimSettings = new DialogAnimationSettings
        {
            Effect = prefersReducedMotion ? DialogEffect.None : DialogEffect.Fade,
            Duration = prefersReducedMotion ? 0 : 300
        };
    }
}
```

## Best Practices

1. **Modal for Critical Actions**: Use modal dialogs for destructive or important operations
2. **Modeless for Help**: Use modeless for secondary information or floating palettes
3. **Performance Tuning**: Use `AllowPrerender="true"` for frequently toggled dialogs
4. **Accessibility**: Always provide a close mechanism (button or close icon)
5. **Z-Index Management**: Use consistent z-index values for nested dialogs
6. **Clear Animation**: Keep animation durations short (200-400ms)
7. **Responsive Design**: Test dialog behavior on different screen sizes
8. **User Feedback**: Provide visual feedback during drag/resize operations
9. **Prevent Abuse**: Limit dialog stacking to prevent overwhelming the user
10. **Test Coverage**: Test all edge cases (nested dialogs, rapid toggling, etc.)
