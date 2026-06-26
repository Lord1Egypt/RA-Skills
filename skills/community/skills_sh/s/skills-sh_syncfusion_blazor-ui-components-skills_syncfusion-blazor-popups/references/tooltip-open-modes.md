# Tooltip Open Modes and Triggers

This guide covers how to control when and how tooltips appear through various trigger modes, delays, and sticky behavior.

## Overview

The Tooltip component supports multiple trigger modes through the `OpensOn` property:
- **Auto** - Opens on hover (desktop) or tap-and-hold (mobile)
- **Hover** - Opens when mouse hovers over target
- **Click** - Opens when target is clicked
- **Focus** - Opens when target receives keyboard focus
- **Custom** - Manual control via methods

You can also combine multiple trigger modes and add delays for opening and closing.

## OpensOn Property

The `OpensOn` property determines how users trigger the tooltip to appear.

### Auto Mode (Default)

When not specified or set to "Auto", the tooltip uses intelligent default behavior:

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#btn" Content="Auto mode tooltip">
    <SfButton ID="btn" Content="Hover or Focus Me"></SfButton>
</SfTooltip>
```

**Desktop behavior:**
- Opens on hover
- Opens on focus (Tab key navigation)

**Mobile behavior:**
- Opens on tap and hold
- Stays open while holding
- Closes 1.5 seconds after release

### Hover Mode

Tooltip appears when mouse hovers over target:

```razor
<SfTooltip Target="#hoverBtn" Content="Hover tooltip" OpensOn="Hover">
    <SfButton ID="hoverBtn" Content="Hover Me"></SfButton>
</SfTooltip>
```

**Desktop behavior:**
- Opens when cursor enters target
- Closes when cursor leaves target

**Mobile behavior:**
- Opens on tap and hold
- Same behavior as Auto mode

**When to use:**
- Quick information displays
- Icon button descriptions
- Status indicators
- Navigation hints

### Click Mode

Tooltip appears when target is clicked:

```razor
<SfTooltip Target="#clickBtn" Content="Click tooltip" OpensOn="Click">
    <SfButton ID="clickBtn" Content="Click Me"></SfButton>
</SfTooltip>
```

**Desktop behavior:**
- Opens on mouse click
- Closes when clicking outside or clicking target again

**Mobile behavior:**
- Opens on single tap
- Closes on second tap or tap outside

**When to use:**
- Detailed information requiring user intent
- Interactive tooltip content
- Preventing accidental tooltip displays
- Mobile-friendly interactions

### Focus Mode

Tooltip appears when target receives keyboard focus:

```razor
<SfTooltip Target=".e-info" Content="Focus tooltip" OpensOn="Focus">
    <div class="blocks">
        <input class="e-info" type="text" placeholder="Focus and blur" />
    </div>
</SfTooltip>

<style>
    .blocks {
        background-color: #ececec;
        border: 1px solid #c8c8c8;
        box-sizing: border-box;
        display: inline-block;
        line-height: 50px;
        margin: 0 10px 10px 0;
        padding: 10px;
        width: 200px;
    }
</style>
```

**Desktop behavior:**
- Opens when element receives focus (Tab key, click)
- Closes when element loses focus (blur)

**Mobile behavior:**
- Opens with single tap (gives focus)
- Closes when another element receives focus

**When to use:**
- Form field help text
- Input validation hints
- Keyboard-only navigation support
- Accessibility requirements

### Custom Mode

Manual control using component methods:

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip @ref="tooltipRef" Target="#customBtn" Content="Custom tooltip" OpensOn="Custom">
    <SfButton ID="customBtn" Content="Button"></SfButton>
</SfTooltip>

<SfButton Content="Open Tooltip" @onclick="OpenTooltip"></SfButton>
<SfButton Content="Close Tooltip" @onclick="CloseTooltip"></SfButton>

@code {
    SfTooltip tooltipRef;
    
    private async Task OpenTooltip()
    {
        await tooltipRef.OpenAsync();
    }
    
    private async Task CloseTooltip()
    {
        await tooltipRef.CloseAsync();
    }
}
```

**When to use:**
- Complex trigger logic
- Programmatic tooltip control
- Integration with custom events
- Conditional tooltip display

### Multiple Trigger Modes

Combine triggers by separating with spaces:

```razor
<!-- Opens on both hover and click -->
<SfTooltip Target="#multiBtn" Content="Hover or Click" OpensOn="Hover Click">
    <SfButton ID="multiBtn" Content="Multiple Triggers"></SfButton>
</SfTooltip>

<!-- Opens on hover, click, or focus -->
<SfTooltip Target="#allTriggers" Content="Any trigger" OpensOn="Hover Click Focus">
    <input id="allTriggers" type="text" placeholder="Hover, click, or focus" />
</SfTooltip>
```

**Important:** Cannot combine "Auto" with other modes. "Auto" must be used alone.

❌ **Invalid:** `OpensOn="Auto Hover"` or `OpensOn="Auto Click"`  
✅ **Valid:** `OpensOn="Hover Click"`, `OpensOn="Hover Focus"`, `OpensOn="Click Focus"`

## Desktop vs Mobile Behavior

### Behavior Comparison Table

| OpensOn Value | Desktop | Mobile |
|---------------|---------|--------|
| **Auto** | Hover or Focus | Tap and hold |
| **Hover** | Mouse hover | Tap and hold |
| **Click** | Mouse click | Single tap |
| **Focus** | Tab key or click | Single tap (for focusable elements) |
| **Custom** | Via methods | Via methods |

### Mobile-Specific Considerations

**Tap and Hold:**
- Tooltip appears after holding for ~500ms
- Remains visible while holding
- Disappears 1.5 seconds after release
- Any other action cancels the tooltip

**Testing on Mobile:**
```razor
<SfTooltip Target="#mobileTest" Content="Test on mobile device" OpensOn="Hover">
    <button id="mobileTest" style="padding: 20px; font-size: 18px;">
        Tap and Hold
    </button>
</SfTooltip>
```

## Sticky Mode

Sticky mode keeps tooltips open until explicitly closed by clicking a close button.

### Enabling Sticky Mode

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#target" Content="@Content" IsSticky="true">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Click close icon to close me";
}

<style>
    #target {
        background-color: #ececec;
        border: 1px solid #c8c8c8;
        box-sizing: border-box;
        margin: 80px auto;
        padding: 20px;
        width: 200px;
    }
</style>
```

### Sticky Mode Features

- Close icon appears in top-right corner of tooltip
- Tooltip stays open regardless of mouse position
- User must click close icon to dismiss
- Works with all trigger modes
- Essential for interactive tooltip content

### Sticky with Click Trigger

```razor
<SfTooltip Target="#infoBtn" Content="@infoContent" OpensOn="Click" IsSticky="true">
    <SfButton ID="infoBtn" IconCss="e-icons e-info" Content="Information"></SfButton>
</SfTooltip>

@code {
    string infoContent = "This tooltip stays open until you close it. You can read at your own pace.";
}
```

### When to Use Sticky Mode

**Good for:**
- Complex or lengthy content requiring time to read
- Interactive elements inside tooltips
- Forms or inputs in tooltips
- Links that users need to click
- Multi-step instructions
- Content with scroll (see dimensions.md)

**Avoid for:**
- Simple hints or labels
- Hover-triggered quick info
- Mobile experiences (can clutter small screens)
- Frequently accessed tooltips

## Open and Close Delays

Control timing of tooltip appearance and disappearance with `OpenDelay` and `CloseDelay` properties.

### Basic Delay Example

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#target" Content="@Content" OpenDelay="1000" CloseDelay="1000">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Tooltip with delay";
}

<style>
    #target {
        background-color: #ececec;
        border: 1px solid #c8c8c8;
        box-sizing: border-box;
        margin: 80px auto;
        padding: 20px;
        width: 200px;
    }
</style>
```

### OpenDelay Property

Specifies delay in milliseconds before tooltip opens:

```razor
<!-- Opens 500ms after hover -->
<SfTooltip Target="#delayBtn" Content="Delayed open" OpenDelay="500">
    <SfButton ID="delayBtn" Content="Hover (500ms delay)"></SfButton>
</SfTooltip>

<!-- Opens immediately (0ms delay) -->
<SfTooltip Target="#instantBtn" Content="Instant open" OpenDelay="0">
    <SfButton ID="instantBtn" Content="Hover (instant)"></SfButton>
</SfTooltip>
```

**When to use OpenDelay:**
- Prevent accidental tooltip displays during quick mouse movements
- Create intentional hover experiences
- Reduce visual noise in dense UIs
- Improve performance on pages with many tooltips

**Recommended values:**
- **0ms** - Instant, for critical information
- **200-300ms** - Slight delay, prevents accidents
- **500-700ms** - Intentional hover required
- **1000ms+** - Deliberate action needed

### CloseDelay Property

Specifies delay in milliseconds before tooltip closes:

```razor
<!-- Stays open 800ms after mouse leaves -->
<SfTooltip Target="#persistBtn" Content="Stays briefly" CloseDelay="800">
    <SfButton ID="persistBtn" Content="Hover (persists)"></SfButton>
</SfTooltip>
```

**When to use CloseDelay:**
- Allow users to move mouse into tooltip content
- Prevent flickering during mouse movements
- Give time to read short messages
- Create smooth user experiences

**Recommended values:**
- **0ms** - Instant close
- **200-400ms** - Brief persistence, smooth feel
- **800-1000ms** - Time to read short content
- **1500ms+** - Time to read longer content (consider sticky mode instead)

### Combining Delays

```razor
<!-- Slow to open, quick to close -->
<SfTooltip Target="#btn1" Content="Intentional hover" OpenDelay="700" CloseDelay="100">
    <SfButton ID="btn1" Content="Slow Open, Fast Close"></SfButton>
</SfTooltip>

<!-- Quick to open, slow to close -->
<SfTooltip Target="#btn2" Content="Stay and read" OpenDelay="100" CloseDelay="1000">
    <SfButton ID="btn2" Content="Fast Open, Slow Close"></SfButton>
</SfTooltip>

<!-- Balanced delays -->
<SfTooltip Target="#btn3" Content="Balanced behavior" OpenDelay="300" CloseDelay="300">
    <SfButton ID="btn3" Content="Balanced Delays"></SfButton>
</SfTooltip>
```

## Practical Examples

### Form Field Help

```razor
<SfTooltip Target="#emailInput" OpensOn="Focus" Content="Enter a valid email address">
    <div class="form-group">
        <label for="emailInput">Email:</label>
        <input id="emailInput" type="email" placeholder="you@example.com" />
    </div>
</SfTooltip>
```

### Icon Button Descriptions

```razor
<SfTooltip Target=".icon-btn" OpensOn="Hover" OpenDelay="300">
    <div class="toolbar">
        <button class="icon-btn" title="Save">💾</button>
        <button class="icon-btn" title="Copy">📋</button>
        <button class="icon-btn" title="Delete">🗑️</button>
    </div>
</SfTooltip>
```

### Detailed Information Card

```razor
<SfTooltip Target="#detailsBtn" OpensOn="Click" IsSticky="true">
    <ContentTemplate>
        <div style="padding: 15px; max-width: 300px;">
            <h4 style="margin: 0 0 10px 0;">Product Details</h4>
            <p><strong>Price:</strong> $299.99</p>
            <p><strong>Availability:</strong> In Stock</p>
            <p><strong>Shipping:</strong> Free 2-day delivery</p>
            <button style="margin-top: 10px;">Add to Cart</button>
        </div>
    </ContentTemplate>
    <ChildContent>
        <SfButton ID="detailsBtn" Content="View Details"></SfButton>
    </ChildContent>
</SfTooltip>
```

### Status Indicator

```razor
<SfTooltip Target=".status" OpensOn="Hover" OpenDelay="200" CloseDelay="500">
    <span class="status" title="System operational">🟢 Online</span>
</SfTooltip>
```

### Custom Trigger with Conditional Logic

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip @ref="conditionalTooltip" Target="#actionBtn" Content="@tooltipContent" OpensOn="Custom">
    <SfButton ID="actionBtn" Content="Action" @onclick="HandleAction"></SfButton>
</SfTooltip>

@code {
    SfTooltip conditionalTooltip;
    string tooltipContent = string.Empty;
    bool canPerformAction = false;
    
    private async Task HandleAction()
    {
        if (!canPerformAction)
        {
            tooltipContent = "Please complete the form before performing this action.";
            await conditionalTooltip.OpenAsync();
            
            // Auto-close after 3 seconds
            await Task.Delay(3000);
            await conditionalTooltip.CloseAsync();
        }
        else
        {
            // Perform action
            Console.WriteLine("Action performed");
        }
    }
}
```

## Best Practices

### Choosing the Right Trigger

**Use Hover when:**
- Information is supplementary, not essential
- Target is not interactive (labels, icons, status indicators)
- Quick glanceable content
- Desktop-primary experience

**Use Click when:**
- Content requires user attention
- Tooltip contains interactive elements
- Mobile-friendly interaction needed
- Preventing accidental displays

**Use Focus when:**
- Form field help text
- Accessibility is critical
- Keyboard navigation support
- Input validation hints

**Use Custom when:**
- Complex business logic determines display
- Integrating with other component events
- Programmatic control needed
- Building custom interaction patterns

### Delay Guidelines

**OpenDelay:**
- Use 200-500ms to prevent accidental triggers
- Use 0ms for critical, immediate information
- Consider user patience vs information importance

**CloseDelay:**
- Use 200-400ms for smooth feeling
- Use 800-1000ms if content needs reading time
- For longer content, use IsSticky instead

### Sticky Mode Guidelines

- Always use with Click trigger for complex content
- Provide visual indication that tooltip is sticky
- Ensure close button is visible and accessible
- Test on mobile devices (close button may be hard to tap)
- Consider alternatives for mobile (drawer, modal)

### Mobile Optimization

- Prefer Click trigger on mobile
- Test tap and hold behavior thoroughly
- Ensure touch targets are large enough (min 44x44px)
- Consider separate mobile experiences for complex tooltips
- Test across different devices and screen sizes

### Accessibility

- Ensure Focus trigger works with keyboard navigation
- Test with screen readers
- Don't rely solely on hover for essential information
- Provide alternative access methods for critical content
- Ensure close button in sticky mode is keyboard accessible

### Performance

- Minimize OpenDelay on performance-critical interfaces
- Avoid too many simultaneous tooltips
- Use Custom mode to control when tooltips are active
- Consider lazy loading tooltip content for complex layouts
