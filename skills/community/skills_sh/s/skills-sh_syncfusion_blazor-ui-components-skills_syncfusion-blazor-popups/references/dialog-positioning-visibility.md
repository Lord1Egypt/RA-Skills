# Positioning and Visibility

## Table of Contents
- [Visibility Control](#visibility-control)
- [Position Modes](#position-modes)
- [Target Element](#target-element)
- [Width and Height](#width-and-height)
- [Positioning Examples](#positioning-examples)
- [Centering Dialogs](#centering-dialogs)
- [Z-Index Management](#z-index-management)

## Visibility Control

The `Visible` property controls whether the dialog is displayed or hidden. Use two-way binding (`@bind-Visible`) to synchronize visibility state with your component.

### Show and Hide Dialog

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ShowDialog">Show</SfButton>
<SfButton OnClick="@HideDialog">Hide</SfButton>

<SfDialog @bind-Visible="DialogVisible" Header="Visibility Control">
    <DialogTemplates>
        <Content>This dialog is @(DialogVisible ? "visible" : "hidden")</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = true;

    private void ShowDialog() => DialogVisible = true;
    private void HideDialog() => DialogVisible = false;
}
```

### Toggle Visibility

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ToggleDialog">Toggle Dialog</SfButton>

<SfDialog @bind-Visible="DialogVisible" Header="Toggle Example">
    <DialogTemplates>
        <Content>Dialog is currently @(DialogVisible ? "visible" : "hidden")</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool DialogVisible { get; set; } = false;

    private void ToggleDialog() => DialogVisible = !DialogVisible;
}
```

### Visibility with Multiple Dialogs

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ShowDialog1">Dialog 1</SfButton>
<SfButton OnClick="@ShowDialog2">Dialog 2</SfButton>

<SfDialog @bind-Visible="Dialog1Visible" Header="Dialog 1" ZIndex="1000">
    <DialogTemplates>
        <Content>This is the first dialog</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog @bind-Visible="Dialog2Visible" Header="Dialog 2" ZIndex="1001">
    <DialogTemplates>
        <Content>This is the second dialog</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool Dialog1Visible { get; set; } = false;
    private bool Dialog2Visible { get; set; } = false;

    private void ShowDialog1() => Dialog1Visible = true;
    private void ShowDialog2() => Dialog2Visible = true;
}
```

## Position Modes

The `Position` property determines how the dialog is positioned relative to its target element or viewport.

### Fixed Position

Dialog remains at the same screen position even when the page scrolls.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Position="fixed" 
          Left="100px" 
          Top="100px" 
          Header="Fixed Position">
    <DialogTemplates>
        <Content>This dialog stays at the same screen position when scrolling</Content>
    </DialogTemplates>
</SfDialog>
```

### Absolute Position

Dialog is positioned relative to its nearest positioned ancestor or the target element.

```csharp
@using Syncfusion.Blazor.Popups

<div id="container" style="position: relative; width: 500px; height: 400px; border: 1px solid #ccc;">
    <SfDialog Target="#container"
              Position="absolute"
              Left="50px"
              Top="50px"
              Header="Absolute Position">
        <DialogTemplates>
            <Content>Dialog positioned within the container</Content>
        </DialogTemplates>
    </SfDialog>
</div>
```

### Relative Position

Dialog is part of the normal document flow.

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Position="relative" Header="Relative Position">
    <DialogTemplates>
        <Content>Dialog flows with page content</Content>
    </DialogTemplates>
</SfDialog>
```

## Target Element

The `Target` property specifies the container element where the dialog is positioned and scoped.

### Using Target with CSS Selector

```csharp
@using Syncfusion.Blazor.Popups

<div id="dialog-container" style="height: 500px; border: 2px solid #333;">
    <p>Content area</p>
    
    <SfDialog Target="#dialog-container"
              Header="Dialog in Container"
              Width="300px">
        <DialogTemplates>
            <Content>This dialog is contained within its target element</Content>
        </DialogTemplates>
    </SfDialog>
</div>
```

### Target with Multiple Elements

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<div id="target-a" style="width: 50%; display: inline-block; border: 1px solid blue; height: 300px;">
    <SfButton OnClick="@ShowDialogA">Show in A</SfButton>
</div>

<div id="target-b" style="width: 50%; display: inline-block; border: 1px solid green; height: 300px;">
    <SfButton OnClick="@ShowDialogB">Show in B</SfButton>
</div>

<SfDialog @bind-Visible="ShowA" Target="#target-a" Header="Dialog A">
    <DialogTemplates>
        <Content>In container A</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog @bind-Visible="ShowB" Target="#target-b" Header="Dialog B">
    <DialogTemplates>
        <Content>In container B</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool ShowA { get; set; } = false;
    private bool ShowB { get; set; } = false;

    private void ShowDialogA() => ShowA = true;
    private void ShowDialogB() => ShowB = true;
}
```

## Width and Height

### Fixed Dimensions

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="400px" Height="300px" Header="Fixed Size">
    <DialogTemplates>
        <Content>
            This dialog has fixed width and height.
            Content will scroll if it exceeds the available space.
        </Content>
    </DialogTemplates>
</SfDialog>
```

### Responsive Dimensions

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="80%" Height="70%" Header="Responsive Size">
    <DialogTemplates>
        <Content>
            <p>This dialog width is 80% and height is 70% of the viewport</p>
            <p>It scales responsively on different screen sizes</p>
        </Content>
    </DialogTemplates>
</SfDialog>
```

### Min and Max Dimensions

While Syncfusion Dialog doesn't have direct min/max properties, you can control size with CSS:

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="50%" Header="Constrained Size" CssClass="size-constrained">
    <DialogTemplates>
        <Content>
            <p>This dialog has CSS-based size constraints</p>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .size-constrained.e-dialog {
        min-width: 300px;
        max-width: 800px;
    }
</style>
```

## Positioning Examples

### Top-Right Corner

```csharp
<SfDialog Position="fixed" 
          Left="auto" 
          Top="20px" 
          Width="300px"
          Header="Notification"
          CssClass="top-right">
    <DialogTemplates>
        <Content>Top-right positioned notification dialog</Content>
    </DialogTemplates>
</SfDialog>

<style>
    .top-right.e-dialog {
        right: 20px !important;
        left: auto !important;
    }
</style>
```

### Bottom-Center

```csharp
<SfDialog Position="fixed" 
          Width="400px"
          Header="Persistent Alert"
          CssClass="bottom-center">
    <DialogTemplates>
        <Content>This dialog appears at the bottom center</Content>
    </DialogTemplates>
</SfDialog>

<style>
    .bottom-center.e-dialog {
        left: 50%;
        transform: translateX(-50%);
        bottom: 20px !important;
        top: auto !important;
    }
</style>
```

### Sidebar Panel

```csharp
<SfDialog Position="fixed"
          Width="300px"
          Height="100vh"
          Header="Navigation"
          CssClass="sidebar">
    <DialogTemplates>
        <Content>
            <ul>
                <li>Home</li>
                <li>About</li>
                <li>Services</li>
                <li>Contact</li>
            </ul>
        </Content>
    </DialogTemplates>
</SfDialog>

<style>
    .sidebar.e-dialog {
        left: 0 !important;
        top: 0 !important;
        border-radius: 0;
        height: 100vh;
    }
</style>
```

## Centering Dialogs

### Center on Page

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="400px" 
          Height="300px"
          Header="Centered Dialog"
          CssClass="centered-dialog">
    <DialogTemplates>
        <Content>This dialog is centered on the page</Content>
    </DialogTemplates>
</SfDialog>

<style>
    .centered-dialog.e-dialog {
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%);
    }
</style>
```

### Center in Container

```csharp
@using Syncfusion.Blazor.Popups

<div id="parent-container" style="position: relative; width: 600px; height: 400px; border: 2px solid #333;">
    <SfDialog Target="#parent-container"
              Position="absolute"
              Width="300px"
              CssClass="container-centered">
        <DialogTemplates>
            <Content>Centered in the container</Content>
        </DialogTemplates>
    </SfDialog>
</div>

<style>
    .container-centered.e-dialog {
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }
</style>
```

### Programmatic Centering

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@CenterDialog">Center Dialog</SfButton>

<SfDialog @ref="DialogRef" Width="400px" Header="Auto-Centered">
    <DialogTemplates>
        <Content>Click the button to center this dialog</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }

    private async Task CenterDialog()
    {
        if (DialogRef != null)
        {
            // Center dialog using style manipulation
            await JSRuntime.InvokeVoidAsync("CenterDialogJS", DialogRef.Element);
        }
    }
}
```

JavaScript helper:
```javascript
function CenterDialogJS(element) {
    const dialog = element;
    const viewport = window.innerHeight;
    const dialogHeight = dialog.offsetHeight;
    const dialogWidth = dialog.offsetWidth;
    
    dialog.style.top = ((viewport - dialogHeight) / 2) + "px";
    dialog.style.left = ((window.innerWidth - dialogWidth) / 2) + "px";
}
```

## Z-Index Management

### Manual Z-Index

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Header="Dialog 1" ZIndex="1000">
    <DialogTemplates>
        <Content>First dialog</Content>
    </DialogTemplates>
</SfDialog>

<SfDialog Header="Dialog 2" ZIndex="1001">
    <DialogTemplates>
        <Content>Second dialog appears above the first</Content>
    </DialogTemplates>
</SfDialog>
```

### Stacked Dialogs

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@OpenDialog1">Open Dialog 1</SfButton>

<SfDialog @bind-Visible="Dialog1Open" 
          Header="Dialog 1" 
          ZIndex="1000">
    <DialogTemplates>
        <Content>
            <p>This is the first dialog</p>
            <SfButton OnClick="@OpenDialog2">Open Dialog 2</SfButton>
        </Content>
    </DialogTemplates>
</SfDialog>

<SfDialog @bind-Visible="Dialog2Open" 
          Header="Dialog 2 (Nested)" 
          ZIndex="1001">
    <DialogTemplates>
        <Content>
            <p>This dialog appears above Dialog 1</p>
            <SfButton OnClick="@OpenDialog3">Open Dialog 3</SfButton>
        </Content>
    </DialogTemplates>
</SfDialog>

<SfDialog @bind-Visible="Dialog3Open" 
          Header="Dialog 3 (Nested)" 
          ZIndex="1002">
    <DialogTemplates>
        <Content>This dialog appears at the top</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool Dialog1Open { get; set; } = false;
    private bool Dialog2Open { get; set; } = false;
    private bool Dialog3Open { get; set; } = false;

    private void OpenDialog1() => Dialog1Open = true;
    private void OpenDialog2() => Dialog2Open = true;
    private void OpenDialog3() => Dialog3Open = true;
}
```

## Best Practices

1. **Always Specify Target**: For contained dialogs, always set the `Target` property
2. **Use Responsive Widths**: Prefer percentage-based widths over fixed pixels
3. **Consider Viewport Size**: Test dialogs on different screen sizes
4. **Z-Index Consistency**: Use consistent z-index ranges (1000, 1001, 1002, etc.)
5. **CSS Transforms**: Use CSS transforms for centering instead of manual positioning
6. **Avoid Overflow**: Ensure dialog content fits within specified dimensions or enable scrolling
7. **Mobile Considerations**: Use responsive dimensions and positioning for mobile devices
8. **Accessibility**: Ensure dialogs don't obscure important page content
