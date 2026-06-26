````markdown
# Dialog Methods and Programmatic Control

## Table of Contents
- [Overview](#overview)
- [Visibility Methods](#visibility-methods)
- [Dimension Methods](#dimension-methods)
- [Button Methods](#button-methods)
- [Position Methods](#position-methods)
- [Method Examples](#method-examples)

## Overview

The Dialog component provides programmatic methods to control visibility, retrieve dimensions, manage buttons, and adjust positioning. These methods allow you to manipulate the dialog from code-behind or event handlers.

## Visibility Methods

### ShowAsync()

Opens the dialog if it is currently hidden.

**Declaration:**
```csharp
public Task ShowAsync(bool? isFullScreen = null)
```

**Parameters:**
- `isFullScreen` (optional, bool?): Whether to open in full screen mode. Default: null (normal mode)

**Returns:** Task representing the asynchronous operation

**Example:**
```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ShowDialog">Open Dialog</SfButton>

<SfDialog @ref="DialogRef" Header="Dialog" Width="400px">
    <DialogTemplates>
        <Content>Dialog content</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }

    private async Task ShowDialog()
    {
        await DialogRef.ShowAsync();
    }
}
```

### HideAsync()

Closes the dialog if it is currently visible.

**Declaration:**
```csharp
public Task HideAsync()
public Task HideAsync(MouseEventArgs args)
public Task HideAsync(KeyboardEventArgs args)
public Task HideAsync(string args = null)
```

**Example:**
```csharp
@using Syncfusion.Blazor.Popups

<SfDialog @ref="DialogRef" Header="Dialog" Width="400px">
    <DialogTemplates>
        <Content>Dialog content</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Close" OnClick="@CloseDialog" />
    </DialogButtons>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }

    private async Task CloseDialog()
    {
        await DialogRef.HideAsync();
    }
}
```

## Dimension Methods

### GetDimension()

Retrieves the current height and width of the dialog.

**Declaration:**
```csharp
public Task<DialogDimension> GetDimension()
```

**Returns:** Task containing DialogDimension object with Height and Width properties

**Example:**
```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@GetSize">Get Dialog Size</SfButton>
<p>Width: @DialogWidth, Height: @DialogHeight</p>

<SfDialog @ref="DialogRef" Header="Dialog" Width="400px" Height="300px">
    <DialogTemplates>
        <Content>Dialog content</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }
    private string DialogWidth { get; set; }
    private string DialogHeight { get; set; }

    private async Task GetSize()
    {
        var dimensions = await DialogRef.GetDimension();
        DialogWidth = dimensions.Width;
        DialogHeight = dimensions.Height;
    }
}
```

### RefreshPositionAsync()

Recalculates and refreshes the dialog position after dynamic size changes.

**Declaration:**
```csharp
public Task RefreshPositionAsync()
```

**Returns:** Task representing the asynchronous operation

**Example:**
```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ResizeAndRefresh">Resize Dialog</SfButton>

<SfDialog @ref="DialogRef" Header="Dialog" Width="400px" Height="300px">
    <DialogTemplates>
        <Content>
            <p>@DialogContent</p>
        </Content>
    </DialogTemplates>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }
    private string DialogContent { get; set; } = "Initial content";

    private async Task ResizeAndRefresh()
    {
        // Change dimensions programmatically
        DialogRef.Width = "600px";
        DialogRef.Height = "400px";
        
        // Refresh position to recalculate
        await DialogRef.RefreshPositionAsync();
        
        DialogContent = "Dialog resized and positioned";
    }
}
```

## Button Methods

### GetButton(int index)

Retrieves a specific DialogButton instance by index.

**Declaration:**
```csharp
public DialogButton GetButton(int index)
```

**Parameters:**
- `index` (int): Zero-based index of the button

**Returns:** DialogButton instance or null if not found

**Example:**
```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@GetFirstButton">Get First Button</SfButton>
<p>First button text: @FirstButtonText</p>

<SfDialog @ref="DialogRef" Header="Dialog" Width="400px">
    <DialogTemplates>
        <Content>Dialog content</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="OK" IsPrimary="true" />
        <DialogButton Content="Cancel" />
    </DialogButtons>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }
    private string FirstButtonText { get; set; }

    private void GetFirstButton()
    {
        var button = DialogRef.GetButton(0);
        if (button != null)
        {
            FirstButtonText = button.Content;
        }
    }
}
```

### GetButtonItems()

Retrieves all DialogButton instances configured for the dialog.

**Declaration:**
```csharp
public List<DialogButton> GetButtonItems()
```

**Returns:** List<DialogButton> or null if no buttons are configured

**Example:**
```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ListAllButtons">List All Buttons</SfButton>
<ul>
    @foreach (var buttonText in ButtonTexts)
    {
        <li>@buttonText</li>
    }
</ul>

<SfDialog @ref="DialogRef" Header="Dialog" Width="400px">
    <DialogTemplates>
        <Content>Dialog content</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="OK" IsPrimary="true" />
        <DialogButton Content="Save" />
        <DialogButton Content="Cancel" />
    </DialogButtons>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }
    private List<string> ButtonTexts { get; set; } = new();

    private void ListAllButtons()
    {
        var buttons = DialogRef.GetButtonItems();
        if (buttons != null)
        {
            ButtonTexts = buttons.Select(b => b.Content).ToList();
        }
    }
}
```

## Position Methods

Dialog positioning is controlled via properties (`Left`, `Top`, `Position`), but position recalculation is done via RefreshPositionAsync() method covered above.

**Position Property Values:**
- `"fixed"` - Fixed position in viewport (doesn't scroll)
- `"absolute"` - Positioned relative to target element
- `"relative"` - Part of normal document flow

## Method Examples

### Complete Dialog Control Example

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<div>
    <SfButton OnClick="@OpenDialog">Open</SfButton>
    <SfButton OnClick="@CloseDialog">Close</SfButton>
    <SfButton OnClick="@GetInfo">Get Info</SfButton>
</div>

<p>Status: @Status</p>
<p>Dimensions: @Dimensions</p>
<p>Buttons: @ButtonCount</p>

<SfDialog @ref="DialogRef" 
          Header="Controllable Dialog" 
          Width="400px" 
          Height="300px"
          @bind-Visible="DialogVisible">
    <DialogTemplates>
        <Content>
            <p>This dialog is controlled by methods</p>
        </Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Action 1" IsPrimary="true" />
        <DialogButton Content="Action 2" />
        <DialogButton Content="Close" OnClick="@CloseDialog" />
    </DialogButtons>
</SfDialog>

@code {
    private SfDialog DialogRef { get; set; }
    private bool DialogVisible { get; set; } = false;
    private string Status { get; set; } = "Closed";
    private string Dimensions { get; set; } = "Unknown";
    private string ButtonCount { get; set; } = "0";

    private async Task OpenDialog()
    {
        await DialogRef.ShowAsync();
        Status = "Opened";
    }

    private async Task CloseDialog()
    {
        await DialogRef.HideAsync();
        Status = "Closed";
    }

    private async Task GetInfo()
    {
        var dimensions = await DialogRef.GetDimension();
        Dimensions = $"{dimensions.Width} x {dimensions.Height}";
        
        var buttons = DialogRef.GetButtonItems();
        ButtonCount = buttons?.Count.ToString() ?? "0";
    }
}
```

## Best Practices

1. **Always await async methods**: Use `await` when calling ShowAsync(), HideAsync(), etc.
2. **Check for null**: GetButton() and GetButtonItems() may return null
3. **Reference requirement**: Store @ref to the SfDialog to call methods
4. **Error handling**: Wrap method calls in try-catch for robustness
5. **State management**: Update component state after method calls to trigger re-renders
6. **Performance**: Avoid calling methods in loops or during frequent re-renders

````