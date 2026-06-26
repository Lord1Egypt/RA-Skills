---
name: syncfusion-blazor-popups
description: Implement modal and modeless dialogs using Syncfusion Blazor Dialog component. Use this skill when creating dialogs, popup windows, modal confirmations, custom forms, or interactive overlay windows. Covers templates, events, positioning, animations, accessibility, and advanced customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Popups"
---

# Implementing Syncfusion Blazor Popups

## Dialog

The [Syncfusion Blazor Dialog](https://www.syncfusion.com/blazor-components/blazor-modal-dialog) component provides a flexible, feature-rich solution for creating modal and modeless dialogs in Blazor applications. Dialogs are essential UI elements for displaying alerts, confirmations, forms, and interactive content overlaid on the main application.

### Component Overview

The Dialog component supports:
- **Template-based layouts** (header, content, footer with custom HTML/components)
- **Multiple interaction modes** (modal and modeless)
- **Rich event system** (lifecycle, drag, resize, overlay interactions)
- **Advanced positioning** (fixed, absolute, relative, centered)
- **Interactive features** (draggable, resizable, minimize/maximize buttons, fullscreen mode)
- **Accessibility support** (WCAG compliance, keyboard navigation, ARIA attributes)
- **Animations** (open/close transitions)
- **State management** (visible binding, state persistence)

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/dialog-getting-started.md)
- Installation and NuGet package setup
- Blazor WebAssembly and Server project configuration
- Adding namespaces and Syncfusion services
- Basic dialog implementation
- CSS imports and theme configuration
- Displaying header, content, and setting visibility

#### Templates and Content Customization
📄 **Read:** [references/templates.md](references/dialog-templates.md)
- Header template with custom HTML and icons
- Content template with forms and Blazor components
- Footer template and custom buttons
- DialogTemplates structure
- Embedding complex UI elements in dialogs

#### Dialog Buttons
📄 **Read:** [references/dialog-buttons.md](references/dialog-buttons.md)
- DialogButton component configuration
- Button placement and click handlers
- Using DialogButtons vs FooterTemplate
- Standard button patterns and common use cases

#### Events and Interactions
📄 **Read:** [references/events.md](references/dialog-events.md)
- Lifecycle events (Created, Destroyed)
- Opening and closing events (OnOpen, Opened, OnClose, Closed)
- Drag events (OnDragStart, OnDrag, OnDragStop)
- Resize events (OnResizeStart, Resizing, OnResizeStop)
- Modal overlay interactions (OnOverlayModalClick)

#### Positioning and Visibility
📄 **Read:** [references/positioning-visibility.md](references/dialog-positioning-visibility.md)
- Position property (fixed, absolute, relative)
- Visible binding for show/hide control
- Target element configuration
- Dialog centering on page
- Width and height configuration
- Z-index management

#### Dialog Behavior and Features
📄 **Read:** [references/dialog-behavior.md](references/dialog-behavior.md)
- Modal vs modeless dialogs
- AllowDragging and EnableResize properties
- AllowPrerender for performance optimization
- ShowCloseIcon configuration
- Creating nested dialogs
- Animation support
- IsModal and overlay behavior

#### Methods and Programmatic Control
📄 **Read:** [references/methods.md](references/dialog-methods.md)
- ShowAsync() to open dialogs programmatically
- ShowAsync(true) to open dialogs in fullscreen mode
- HideAsync() to close dialogs programmatically
- GetDimension() to retrieve dialog size
- GetButton(index) and GetButtonItems() for button access
- RefreshPositionAsync() for position recalculation
- Complete control examples

#### Advanced Customization and Styling
📄 **Read:** [references/advanced-customization.md](references/dialog-advanced-customization.md)
- CSS class customization and styling
- Appearance customization
- Accessibility features (WCAG compliance, keyboard navigation)
- Animation configurations
- State persistence strategies with EnablePersistence
- Minimize/Maximize button implementation
- Localization support
- Responsive dialog design

### Quick Start

#### Basic Dialog

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="300px" Header="Welcome">
    <DialogTemplates>
        <Content>This is a basic dialog with content.</Content>
    </DialogTemplates>
</SfDialog>
```

#### Dialog with Show/Hide Control

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<div id="target">
    <SfButton OnClick="@OpenDialog">Open Dialog</SfButton>
    
    <SfDialog Target="#target" Width="400px" Header="Confirmation" 
              ShowCloseIcon="true" @bind-Visible="IsVisible">
        <DialogTemplates>
            <Content>Are you sure you want to proceed?</Content>
        </DialogTemplates>
        <DialogButtons>
            <DialogButton Content="OK" IconCss="e-icons e-ok-icon" IsPrimary="true" OnClick="@OnOkClick" />
            <DialogButton Content="Cancel" IconCss="e-icons e-close-icon" OnClick="@OnCancelClick" />
        </DialogButtons>
    </SfDialog>
</div>

@code {
    private bool IsVisible { get; set; } = false;
    
    private void OpenDialog() => IsVisible = true;
    
    private void OnOkClick()
    {
        // Handle OK action
        IsVisible = false;
    }
    
    private void OnCancelClick()
    {
        // Handle Cancel action
        IsVisible = false;
    }
}
```

### Common Patterns

#### Alert Dialog
```csharp
<SfDialog Width="350px" IsModal="true" Header="Alert">
    <DialogTemplates>
        <Content>This action cannot be undone.</Content>
    </DialogTemplates>
</SfDialog>
```

#### Form Dialog
```csharp
<SfDialog Width="400px" Header="User Information">
    <DialogTemplates>
        <Content>
            <div class="form-group">
                <input type="text" placeholder="Enter name" />
            </div>
        </Content>
    </DialogTemplates>
</SfDialog>
```

#### Draggable and Resizable Dialog
```csharp
<SfDialog Width="400px" Header="Features" AllowDragging="true" EnableResize="true">
    <DialogTemplates>
        <Content>You can drag and resize this dialog.</Content>
    </DialogTemplates>
</SfDialog>
```

#### Fullscreen Dialog
```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@OpenFullScreenDialog">Open Fullscreen Dialog</SfButton>

<SfDialog @ref="DialogRef" Width="250px" ShowCloseIcon="true" Visible="false">
    <DialogTemplates>
        <Header>Dialog</Header>
        <Content>This is a fullscreen dialog</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="OK" IsPrimary="true" OnClick="@CloseDialog" />
        <DialogButton Content="Cancel" OnClick="@CloseDialog" />
    </DialogButtons>
</SfDialog>

@code {
    SfDialog DialogRef;

    private async Task OpenFullScreenDialog()
    {
        await this.DialogRef.ShowAsync(true);
    }

    private async Task CloseDialog()
    {
        await this.DialogRef.HideAsync();
    }
}
```

### Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `Width` | string | Sets dialog width (e.g., "400px", "50%"). Default: "100%" |
| `Height` | string | Sets dialog height (e.g., "300px", "70%"). Default: "auto" |
| `Header` | string | Sets dialog header text |
| `Content` | string | Sets dialog content text |
| `Visible` | bool | Controls dialog visibility. Supports @bind-Visible. Default: true |
| `IsModal` | bool | Makes dialog modal (overlay blocking interaction). Default: false |
| `ShowCloseIcon` | bool | Shows close button in header. Default: false |
| `AllowDragging` | bool | Enables dialog dragging by header. Default: false |
| `EnableResize` | bool | Enables dialog resizing. Default: false |
| `CloseOnEscape` | bool | Closes dialog when Escape key is pressed. Default: true |
| `AnimationSettings` | DialogAnimationSettings | Configures open/close animations (effect, duration, delay). Default: Fade effect, 400ms |
| `Position` | string | Positioning mode: "fixed" (stays on screen), "absolute" (relative to target), or "relative" (document flow). Default: "fixed" |
| `Left` | string | X-coordinate position (e.g., "100px", "20%"). Works with Position property. Default: "auto" |
| `Top` | string | Y-coordinate position (e.g., "50px", "10%"). Works with Position property. Default: "auto" |
| `ID` | string | Unique identifier for the dialog. Required when EnablePersistence="true" |
| `MinHeight` | string | Sets minimum height constraint for resize (e.g., "150px"). Default: null |
| `MaxHeight` | string | Sets maximum height constraint for resize (e.g., "600px"). Default: null |
| `ResizeHandles` | ResizeDirection[] | Array of resize directions (e.g., SouthEast, NorthEast). Default: [SouthEast] |
| `Buttons` | List\<DialogButtonModel\> | Programmatic button configuration (alternative to DialogButtons component) |
| `CssClass` | string | Custom CSS class(es) for styling |
| `EnableRtl` | bool | Enables right-to-left layout support. Default: false |
| `EnablePersistence` | bool | Persists position, width, height to browser local storage. Default: false. Requires ID property |
| `Target` | string | CSS selector for dialog target/container element (e.g., "#container", ".target-div") |
| `FooterTemplate` | RenderFragment | Custom footer content (alternative to DialogButtons component) |
| `AllowPrerender` | bool | Keeps DOM elements when hidden for faster re-display. Default: false |
| `ZIndex` | double | Sets stacking order relative to other elements. Default: 1000 |

### Key Enums and Types

#### DialogEffect Enum
Animation effects for dialog open/close transitions:

| Value | Description |
|-------|-------------|
| `None` | No animation |
| `Fade` | Fade in/out effect (default) |
| `Zoom` | Zoom in/out from center |
| `SlideLeft` | Slide from/to left |
| `SlideRight` | Slide from/to right |
| `SlideTop` | Slide from/to top |
| `SlideBottom` | Slide from/to bottom |
| `FlipX` | Horizontal flip effect |
| `FlipY` | Vertical flip effect |

#### ResizeDirection Enum
Directions from which the dialog can be resized:

| Value | Description |
|-------|-------------|
| `South` | Bottom edge |
| `North` | Top edge |
| `East` | Right edge |
| `West` | Left edge |
| `SouthEast` | Bottom-right corner (default) |
| `SouthWest` | Bottom-left corner |
| `NorthEast` | Top-right corner |
| `NorthWest` | Top-left corner |
| `All` | All directions |

#### ButtonType Enum
HTML button type attribute for dialog buttons:

| Value | Description |
|-------|-------------|
| `Button` | Standard button (default) |
| `Submit` | Form submission button |
| `Reset` | Form reset button |

#### DialogAnimationSettings Class
Configuration for dialog animations:

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `Effect` | DialogEffect | Animation effect | DialogEffect.Fade |
| `Duration` | int | Animation duration (milliseconds) | 400 |
| `Delay` | int | Animation delay (milliseconds) | 0 |

- Use `ShowAsync(true)` for fullscreen dialogs when you need maximum focus and screen real estate
- Set `Visible="false"` initially when using programmatic control with ShowAsync()
**Example:**
```csharp
var animSettings = new DialogAnimationOptions 
{ 
    Effect = DialogEffect.Zoom, 
    Duration = 300, 
    Delay = 0 
};
```

#### DialogDimension Class
Returned by `GetDimension()` method:

| Property | Type | Description |
|----------|------|-------------|
| `Width` | string | Current dialog width |
| `Height` | string | Current dialog height |

### Important Constraints and Notes

⚠️ **Critical Requirements:**
- **ID Property**: Must be set when using `EnablePersistence="true"`. The ID serves as the localStorage key.
- **Mutual Exclusivity**: `FooterTemplate` and `DialogButtons` cannot be used together. Choose one approach.
- **Target Selector**: The `Target` property must reference a valid CSS selector for existing DOM elements.
- **Resize Dependency**: `ResizeHandles` only works when `EnableResize="true"`.
- **Position Context**: The `Position` property affects how `Left` and `Top` coordinates are interpreted.

📋 **Best Practices:**
- Use `IsModal="true"` for critical actions requiring user attention
- Set `AllowPrerender="true"` for frequently toggled dialogs to improve performance
- Always provide a close mechanism (button, close icon, or Escape key)
- Use `ZIndex` values in increments (1000, 1001, 1002) for nested dialogs
- Test responsive behavior with percentage-based Width/Height values

### Related Skills

- [implementing-buttons](../buttons/implementing-buttons/) - For dialog button styling and behavior
- [implementing-dropdown-list](../../dropdowns/implementing-dropdown-list/) - For select controls within dialogs
- [implementing-text-inputs](../../inputs/implementing-text-inputs/) - For form fields in dialogs

---

### See Also

- [Syncfusion Blazor Dialog Documentation](https://www.syncfusion.com/blazor-components/blazor-modal-dialog)
- [Dialog Events Reference](https://help.syncfusion.com/cr/blazor/Syncfusion.Blazor.Popups.DialogEvents.html)
- [Blazor Themes](https://blazor.syncfusion.com/documentation/appearance/themes)


## Tooltips

The Syncfusion Blazor Tooltip component provides contextual information by displaying messages when users interact with target elements through hovering, clicking, or focusing. It supports rich content, flexible positioning, multiple trigger modes, and comprehensive customization options.

### Component Overview

The Blazor Tooltip component offers:

- **Multiple content types**: Simple text, HTML title attributes, templates, RenderFragment, and MarkupString
- **Flexible positioning**: 12 static positions (TopLeft, TopCenter, TopRight, BottomLeft, etc.), mouse trailing, and custom offsets
- **Open mode options**: Hover, Click, Focus, Auto, Custom, and combinations
- **Sticky mode**: Keep tooltips open with a close button
- **Customization**: Full CSS control over wrapper, content, and tip pointer
- **Dynamic targets**: Support for elements added after component initialization
- **Accessibility**: WCAG 2.2 compliance with ARIA attributes and keyboard support
- **Collision handling**: Automatic repositioning when tooltips hit viewport boundaries

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/tooltip-getting-started.md)
- Prerequisites and system requirements
- Package installation (Syncfusion.Blazor.Popups and Themes)
- Namespace imports and service registration
- Stylesheet and script resource setup
- Basic Tooltip implementation with Button
- WebAssembly App configuration
- Web App setup (Server, Client, Auto render modes)
- Interactive render mode configuration
- First Tooltip example

#### Content Management
📄 **Read:** [references/content.md](references/tooltip-content.md)
- Simple text content using Content property
- Using HTML title attribute as tooltip content
- ContentTemplate for custom HTML layouts
- Dynamic content with RenderFragment
- Rendering HTML strings with MarkupString
- Interactive elements inside tooltips
- Images, formatted text, and links in tooltip content
- Complex tooltip layouts with multiple sections

#### Positioning and Placement
📄 **Read:** [references/positioning.md](references/tooltip-positioning.md)
- Position property with 12 static options (TopLeft, TopCenter, TopRight, BottomLeft, BottomCenter, BottomRight, LeftTop, LeftCenter, LeftBottom, RightTop, RightCenter, RightBottom)
- Mouse trailing behavior (MouseTrail property)
- Offset configuration (OffsetX and OffsetY)
- Collision detection and automatic repositioning
- WindowCollision for viewport boundary handling
- Combining positions with offsets
- Best practices for position selection

#### Open Modes and Triggers
📄 **Read:** [references/open-modes.md](references/tooltip-open-modes.md)
- OpensOn property values (Auto, Hover, Click, Focus, Custom)
- Desktop vs mobile behavior differences
- Multiple trigger combinations (e.g., "Hover Click")
- Sticky mode (IsSticky) with close button
- Open and close delays (OpenDelay, CloseDelay)
- Custom trigger implementation with public methods
- Mobile tap and hold behavior
- Best practices for trigger selection

#### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/tooltip-customization-and-styling.md)
- CssClass property for custom styles
- Tip pointer customization (size, colors, shape)
- Tooltip wrapper and popup styling
- Content styling (font, color, padding)
- Arrow tip styling for all 4 directions
- Inner and outer tip CSS structure
- Complete CSS class reference
- Theme integration examples

#### Dimensions and Sizing
📄 **Read:** [references/dimensions.md](references/tooltip-dimensions.md)
- Width and Height properties
- Auto vs fixed sizing strategies
- Scroll mode for content overflow
- Combining Height with IsSticky for scrollable tooltips
- Responsive sizing considerations
- Content overflow handling

#### Target Configuration
📄 **Read:** [references/target-configuration.md](references/tooltip-target-configuration.md)
- Target property with CSS selectors
- Single vs multiple target elements
- Dynamic target elements added after render
- TargetContainer for automatic registration
- GUID ID limitations (cannot start with digit)
- Best practices for target selection
- Examples with buttons, links, inputs, and custom elements

#### Accessibility
📄 **Read:** [references/accessibility.md](references/tooltip-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- ARIA attributes (role="tooltip", aria-describedby, aria-hidden)
- Keyboard navigation (Tab for focus, Escape to close)
- Screen reader support
- Right-to-Left (RTL) language support
- Color contrast requirements
- Mobile device accessibility
- Axe-core validation
- Best practices for accessible tooltips

### Quick Start Example

#### Basic Tooltip with Button

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip ID="Tooltip" Target="#btn" Content="@Content">
    <SfButton ID="btn" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Click to save your changes!";
}
```

#### Tooltip with Custom Position

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#saveBtn" Content="Save changes" Position="Position.RightCenter">
    <SfButton ID="saveBtn" Content="Save"></SfButton>
</SfTooltip>
```

#### Multiple Tooltips Using Class Selector

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip ID="Tooltip" Target=".action-btn" Content="Click to perform action">
    <div id="container">
        <SfButton ID="btn1" CssClass="action-btn" Content="Save" title="Save your work"></SfButton>
        <SfButton ID="btn2" CssClass="action-btn" Content="Cancel" title="Discard changes"></SfButton>
        <SfButton ID="btn3" CssClass="action-btn" Content="Delete" title="Remove item permanently"></SfButton>
    </div>
</SfTooltip>
```

### Common Patterns

#### Sticky Tooltip with Click Trigger

```razor
<SfTooltip Target="#helpBtn" Content="Need help? Contact support at help@example.com" 
           OpensOn="Click" IsSticky="true">
    <SfButton ID="helpBtn" Content="Help" IconCss="e-icons e-help"></SfButton>
</SfTooltip>
```

#### Tooltip with HTML Template

```razor
<SfTooltip Target="#infoBtn" OpensOn="Click">
    <ContentTemplate>
        <div style="padding: 10px;">
            <h4 style="margin: 0 0 10px 0;">User Information</h4>
            <p><strong>Name:</strong> John Doe</p>
            <p><strong>Email:</strong> john@example.com</p>
            <p><strong>Status:</strong> Active</p>
        </div>
    </ContentTemplate>
    <ChildContent>
        <SfButton ID="infoBtn" Content="Info" IsPrimary="true"></SfButton>
    </ChildContent>
</SfTooltip>
```

#### Tooltip with Mouse Trailing

```razor
<SfTooltip MouseTrail="true" Content="Follow the cursor" Target="#trackArea">
    <div id="trackArea" style="width: 300px; height: 200px; border: 2px dashed #ccc; padding: 20px;">
        Hover over this area - the tooltip follows your mouse!
    </div>
</SfTooltip>
```

#### Custom Styled Tooltip

```razor
<SfTooltip Target="#customBtn" Content="Custom styled tooltip" CssClass="custom-tooltip">
    <SfButton ID="customBtn" Content="Hover Me"></SfButton>
</SfTooltip>

<style>
    .custom-tooltip.e-tooltip-wrap {
        background-color: #2196F3;
        border-radius: 8px;
    }
    
    .custom-tooltip.e-tooltip-wrap .e-tip-content {
        color: white;
        font-weight: 600;
        padding: 8px 12px;
    }
    
    .custom-tooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top {
        border-bottom: 10px solid #2196F3;
    }
</style>
```

#### Dynamic Targets with TargetContainer

```razor
<SfTooltip ID="dynamicTooltip" Target=".dynamic-item" TargetContainer="#app-container" Content="Dynamic content item">
</SfTooltip>

<div id="app-container">
    <button class="dynamic-item" title="Static button">Static</button>
    @if (showDynamic)
    {
        <button class="dynamic-item" title="Dynamically added button">Dynamic</button>
    }
</div>

@code {
    private bool showDynamic = false;
}
```

### Key Properties

#### Essential Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| **Content** | string | null | Text content to display in tooltip |
| **Target** | string | null | CSS selector for target elements |
| **Position** | Position | TopCenter | Tooltip placement position |
| **OpensOn** | string | "Auto" | Trigger mode (Auto, Hover, Click, Focus, Custom) |
| **IsSticky** | bool | false | Keep tooltip open with close button |
| **Animation** | AnimationModel | null | Animation settings for open/close transitions |

#### Content Properties

| Property | Type | Description |
|----------|------|-------------|
| **ContentTemplate** | RenderFragment | Custom HTML content template. Default: null |
| **Content** | string | Simple text or HTML string content. Default: null |
| **ChildContent** | RenderFragment | Wraps the target element(s) within the tooltip component. Default: null |

#### Positioning Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| **Position** | Position | TopCenter | Static position around target |
| **MouseTrail** | bool | false | Follow mouse pointer |
| **OffsetX** | double | 0 | Horizontal offset in pixels |
| **OffsetY** | double | 0 | Vertical offset in pixels |
| **WindowCollision** | bool | false | Use viewport for collision detection instead of parent element |

#### Timing Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| **OpenDelay** | double | 0 | Delay before opening (milliseconds) |
| **CloseDelay** | double | 0 | Delay before closing (milliseconds) |

#### Event Callbacks

| Event | Type | Description |
|-------|------|-------------|
| **Created** | EventCallback\<object\> | Raised after tooltip component is created |
| **Destroyed** | EventCallback\<object\> | Raised when tooltip component is destroyed |
| **OnOpen** | EventCallback\<TooltipEventArgs\> | Raised before tooltip is displayed (cancelable) |
| **Opened** | EventCallback\<TooltipEventArgs\> | Raised after tooltip is opened |
| **OnClose** | EventCallback\<TooltipEventArgs\> | Raised before tooltip hides (cancelable) |
| **Closed** | EventCallback\<TooltipEventArgs\> | Raised after tooltip is closed |
| **OnRender** | EventCallback\<TooltipEventArgs\> | Raised before tooltip is added to DOM (cancelable) |
| **OnCollision** | EventCallback\<TooltipEventArgs\> | Raised during collision detection calculations |

#### Public Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| **OpenAsync(ElementReference?, TooltipAnimationSettings)** | Task | Opens tooltip programmatically with optional target and animation settings |
| **CloseAsync(TooltipAnimationSettings)** | Task | Closes tooltip programmatically with optional animation settings |
| **RefreshAsync()** | Task | Refreshes tooltip to sync with dynamic DOM changes and target updates |
| **RefreshPositionAsync(ElementReference?)** | Task | Recalculates and updates tooltip position based on current target location |

#### Appearance Properties

| Property | Type | Description |
|----------|------|-------------|
| **CssClass** | string | Custom CSS class for styling. Default: null |
| **Width** | string | Tooltip width (auto or pixels). Default: "auto" |
| **Height** | string | Tooltip height (auto or pixels). Default: "auto" |
| **ShowTipPointer** | bool | Show/hide arrow pointer. Default: true |
| **TipPointerPosition** | TipPointerPosition | Position of tip pointer (Auto, Start, Middle, End). Default: Auto |
| **EnableRtl** | bool | Enable right-to-left direction. Default: false |
| **HtmlAttributes** | Dictionary<string, object> | Additional HTML attributes for tooltip element. Default: null |
| **ID** | string | Unique identifier for the tooltip component. Default: auto-generated |

#### Target Properties

| Property | Type | Description |
|----------|------|-------------|
| **Target** | string | CSS selector for target elements. Default: null |
| **Container** | string | Container element where tooltip popup is appended. Default: "body" |
| **TargetContainer** | string | Container selector for dynamic target registration. Default: null |

### Key Types and Classes

#### AnimationModel Class

Configuration for tooltip open and close animations:

| Property | Type | Description |
|----------|------|-------------|
| **Open** | TooltipAnimationSettings | Animation settings for opening tooltip |
| **Close** | TooltipAnimationSettings | Animation settings for closing tooltip |

#### TooltipAnimationSettings Class

Detailed animation configuration:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| **Effect** | Effect | Fade | Animation effect (FadeIn, FadeOut, ZoomIn, ZoomOut, None) |
| **Duration** | int | 150 | Animation duration in milliseconds |
| **Delay** | int | 0 | Animation delay in milliseconds |

#### Effect Enum

Animation effects for tooltip transitions:

| Value | Description |
|-------|-------------|
| **None** | No animation |
| **FadeIn** | Fade in effect for opening |
| **FadeOut** | Fade out effect for closing |
| **ZoomIn** | Zoom in effect for opening |
| **ZoomOut** | Zoom out effect for closing |

#### Position Enum

Tooltip placement positions:

| Value | Description |
|-------|-------------|
| **TopLeft** | Above target, aligned to left edge |
| **TopCenter** | Above target, centered (default) |
| **TopRight** | Above target, aligned to right edge |
| **BottomLeft** | Below target, aligned to left edge |
| **BottomCenter** | Below target, centered |
| **BottomRight** | Below target, aligned to right edge |
| **LeftTop** | Left of target, aligned to top edge |
| **LeftCenter** | Left of target, centered vertically |
| **LeftBottom** | Left of target, aligned to bottom edge |
| **RightTop** | Right of target, aligned to top edge |
| **RightCenter** | Right of target, centered vertically |
| **RightBottom** | Right of target, aligned to bottom edge |

#### TipPointerPosition Enum

Arrow pointer placement on tooltip:

| Value | Description |
|-------|-------------|
| **Auto** | Automatically adjusts pointer position (default) |
| **Start** | Pointer at start of tooltip edge |
| **Middle** | Pointer at middle of tooltip edge |
| **End** | Pointer at end of tooltip edge |

### Common Use Cases

#### Form Field Help Text

Provide contextual help for form inputs:
- Read [references/getting-started.md](references/tooltip-getting-started.md) for basic setup
- Read [references/open-modes.md](references/tooltip-open-modes.md) for Focus trigger
- Use `OpensOn="Focus"` to show tooltip when input receives focus
- Position tooltip to avoid covering the input field

#### Icon Button Descriptions

Add descriptive text to icon-only buttons:
- Use simple `Content` property for short descriptions
- Set `OpensOn="Hover"` for immediate feedback
- Consider `Position.TopCenter` or `Position.BottomCenter` for consistency

#### Rich Content Cards

Display detailed information on hover:
- Read [references/content.md](references/tooltip-content.md) for template options
- Use `ContentTemplate` with formatted HTML
- Include images, links, and formatted text
- Consider `OpensOn="Click"` and `IsSticky="true"` for complex content

#### Status Indicators

Show status details on hover:
- Use color-coded tooltips with `CssClass`
- Read [references/customization-and-styling.md](references/tooltip-customization-and-styling.md) for styling
- Keep content concise and scannable

#### Dynamic Dashboard Elements

Add tooltips to dynamically added widgets:
- Read [references/target-configuration.md](references/tooltip-target-configuration.md) for dynamic setup
- Use `TargetContainer` to handle elements added after initialization
- Use data attributes for tooltip content

#### Accessibility Enhancements

Ensure tooltips are accessible:
- Read [references/accessibility.md](references/tooltip-accessibility.md) for compliance
- Use semantic HTML in templates
- Ensure keyboard navigation works
- Test with screen readers
- Maintain color contrast ratios


## Predefined Dialog

### Component Overview

The Syncfusion Blazor Predefined Dialogs use a service-based architecture with two key components:
- **SfDialogService** - Registered service for opening dialogs programmatically
- **SfDialogProvider** - Component added to layout to enable dialog rendering

**Key Features:**
- Three dialog types: Alert, Confirm, Prompt
- Service-based invocation from anywhere in the app
- Customizable positioning, dimensions, and animations
- Draggable dialog support
- Button customization with icons
- Custom content rendering
- Built-in accessibility support

**Package:** `Syncfusion.Blazor.Popups`  
**Namespace:** `Syncfusion.Blazor.Popups`

---

### Documentation and Navigation Guide

#### Getting Started (Setup & Basic Usage)
📄 **Read:** [references/getting-started.md](references/predefined-dialog-getting-started.md)
- Prerequisites and system requirements
- Installation for Blazor WebAssembly, Server App, and Web App
- NuGet package installation (Syncfusion.Blazor.Popups)
- Import namespaces (_Imports.razor)
- Service registration (SfDialogService, AddSyncfusionBlazor)
- Adding SfDialogProvider to MainLayout
- Stylesheet and script references
- Alert dialog basics (AlertAsync method)
- Confirm dialog basics (ConfirmAsync method)
- Prompt dialog basics (PromptAsync method)
- Basic code examples for all three dialog types

#### Positioning Dialogs
📄 **Read:** [references/positioning.md](references/predefined-dialog-positioning.md)
- DialogOptions.Position property
- PositionDataModel configuration (X and Y)
- Position values: left, center, right, top, bottom, offset
- Customizing dialog position for alert, confirm, prompt
- Examples with top-center positioning

#### Draggable Dialogs
📄 **Read:** [references/dragging.md](references/predefined-dialog-dragging.md)
- DialogOptions.AllowDragging property
- Enabling drag behavior by dialog header
- Header visibility requirement
- Examples for draggable alert, confirm, prompt dialogs

#### Dialog Dimensions
📄 **Read:** [references/dimensions.md](references/predefined-dialog-dimensions.md)
- DialogOptions.Width and Height properties
- Default auto-sizing behavior
- Setting dimensions in pixels or percentages
- Max-width and max-height using CssClass
- Min-width and min-height using CssClass
- Responsive sizing strategies
- Examples with custom dimensions

#### Customization Options
📄 **Read:** [references/customization.md](references/predefined-dialog-customization.md)
- DialogOptions.PrimaryButtonOptions (OK button)
- DialogOptions.CancelButtonOptions (Cancel button)
- DialogButtonOptions.Content (button text)
- DialogButtonOptions.IconCss (button icons)
- DialogOptions.ShowCloseIcon property
- DialogOptions.ChildContent for custom content rendering
- Customizing alert, confirm, prompt dialogs
- Advanced content customization examples

#### Animation Effects
📄 **Read:** [references/animation.md](references/predefined-dialog-animation.md)
- DialogOptions.AnimationSettings property
- DialogAnimationOptions configuration
- Animation Delay, Duration, and Effect
- DialogEffect enumeration values
- Zoom, fade, slide effects
- Examples with zoom animation

---

### Quick Start Example

#### Basic Alert Dialog

```razor
@page "/alert-example"
@inject SfDialogService DialogService

<SfButton @onclick="ShowAlert">Show Alert</SfButton>

@code {
    private async Task ShowAlert()
    {
        await DialogService.AlertAsync("This is an alert message!");
    }
}
```

#### Basic Confirm Dialog

```razor
@page "/confirm-example"
@inject SfDialogService DialogService

<SfButton @onclick="ShowConfirm">Show Confirm</SfButton>
<p>@result</p>

@code {
    private string result = "";
    
    private async Task ShowConfirm()
    {
        bool isConfirmed = await DialogService.ConfirmAsync("Do you want to proceed?");
        result = isConfirmed ? "User clicked OK" : "User clicked Cancel";
    }
}
```

#### Basic Prompt Dialog

```razor
@page "/prompt-example"
@inject SfDialogService DialogService

<SfButton @onclick="ShowPrompt">Show Prompt</SfButton>
<p>@userInput</p>

@code {
    private string userInput = "";
    
    private async Task ShowPrompt()
    {
        string input = await DialogService.PromptAsync("Enter your name:");
        userInput = input ?? "User cancelled";
    }
}
```

---

### Common Patterns

#### Pattern 1: Confirmation Before Delete

```razor
private async Task DeleteItem(int itemId)
{
    var options = new DialogOptions()
    {
        PrimaryButtonOptions = new DialogButtonOptions()
        {
            Content = "Delete",
            IconCss = "e-icons e-delete"
        },
        CancelButtonOptions = new DialogButtonOptions()
        {
            Content = "Cancel"
        }
    };
    
    bool confirmed = await DialogService.ConfirmAsync(
        "Are you sure you want to delete this item?", 
        "Confirm Delete", 
        options
    );
    
    if (confirmed)
    {
        // Perform delete operation
    }
}
```

#### Pattern 2: Positioned Dialog

```razor
private async Task ShowPositionedAlert()
{
    var options = new DialogOptions()
    {
        Position = new PositionDataModel()
        {
            X = "center",
            Y = "top"
        },
        Width = "400px",
        Height = "200px"
    };
    
    await DialogService.AlertAsync(
        "This dialog appears at the top center!",
        "Alert",
        options
    );
}
```

#### Pattern 3: Custom Content Prompt

```razor
private async Task ShowCustomPrompt()
{
    string username = "";
    
    var options = new DialogOptions()
    {
        ChildContent = @<div>
            <label>Username:</label>
            <input type="text" @bind="username" class="e-input" />
        </div>,
        PrimaryButtonOptions = new DialogButtonOptions() { Content = "Connect" },
        CancelButtonOptions = new DialogButtonOptions() { Content = "Close" }
    };
    
    await DialogService.PromptAsync("Enter your credentials:", "Login", options);
}
```

#### Pattern 4: Animated Draggable Dialog

```razor
private async Task ShowAnimatedDialog()
{
    var options = new DialogOptions()
    {
        AllowDragging = true,
        ShowCloseIcon = true,
        AnimationSettings = new DialogAnimationOptions()
        {
            Effect = DialogEffect.Zoom,
            Duration = 300,
            Delay = 0
        },
        Width = "500px"
    };
    
    await DialogService.AlertAsync(
        "Drag me around! I have zoom animation too!",
        "Draggable Dialog",
        options
    );
}
```

---

### Key Properties

#### SfDialogService Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `AlertAsync` | title, content, options | `Task` | Shows alert dialog with OK button |
| `ConfirmAsync` | title, content, options | `Task<bool>` | Shows confirm dialog, returns true/false |
| `PromptAsync` | title, defaultValue, options | `Task<string>` | Shows prompt dialog, returns input or null |

#### DialogOptions Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Position` | PositionDataModel | center/center | Dialog position (X, Y coordinates) |
| `Width` | string | "auto" | Dialog width (px, %, em) |
| `Height` | string | "auto" | Dialog height (px, %, em) |
| `AllowDragging` | bool | false | Enable dragging by header |
| `ShowCloseIcon` | bool | false | Show close icon button |
| `AnimationSettings` | DialogAnimationOptions | default | Animation configuration |
| `PrimaryButtonOptions` | DialogButtonOptions | null | Primary (OK) button customization |
| `CancelButtonOptions` | DialogButtonOptions | null | Cancel button customization |
| `ChildContent` | RenderFragment | null | Custom content for dialog body |
| `CssClass` | string | null | Custom CSS class |
| `CloseOnEscape` | bool | true | Close on Escape key |
| `ZIndex` | int | 1000 | Dialog z-index |

#### PositionDataModel Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `X` | string | left, center, right, offset | Horizontal position |
| `Y` | string | top, center, bottom, offset | Vertical position |

#### DialogButtonOptions Properties

| Property | Type | Description |
|----------|------|-------------|
| `Content` | string | Button text content |
| `IconCss` | string | CSS class for button icon |
| `IsPrimary` | bool | Primary button styling |

#### DialogAnimationSettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `Effect` | DialogEffect | Animation effect (Zoom, Fade, etc.) |
| `Duration` | int | Animation duration in milliseconds |
| `Delay` | int | Animation delay in milliseconds |

---

### Common Use Cases

#### Use Case 1: Error/Warning/Info Messages
Display system messages, errors, warnings, or information requiring user acknowledgment using Alert dialogs.

#### Use Case 2: Critical Action Confirmation
Get user confirmation before destructive actions like delete, logout, or data loss operations using Confirm dialogs.

#### Use Case 3: User Input Collection
Collect simple text input like usernames, search queries, or configuration values using Prompt dialogs.

#### Use Case 4: Form Validation Feedback
Show validation errors or success messages with positioned dialogs that don't obstruct form fields.

#### Use Case 5: Custom Interactive Dialogs
Create complex interactive dialogs with custom content, multiple inputs, and customized buttons.

#### Use Case 6: Notification System
Build notification systems with animated, positioned dialogs that appear in specific screen areas.

---

### Setup Requirements

**Prerequisites:**
1. Blazor WebAssembly, Server, or Web App project
2. .NET SDK installed
3. Visual Studio, VS Code, or .NET CLI

**Required Packages:**
- `Syncfusion.Blazor.Popups`
- `Syncfusion.Blazor.Themes`

**Required Setup:**
1. Register `SfDialogService` in Program.cs
2. Register `AddSyncfusionBlazor()` service
3. Add `SfDialogProvider` in MainLayout.razor
4. Include Syncfusion theme stylesheet in head
5. Include Syncfusion script reference in body
6. Import `Syncfusion.Blazor.Popups` namespace in _Imports.razor

Refer to **references/getting-started.md** for complete setup instructions for all Blazor app types.


