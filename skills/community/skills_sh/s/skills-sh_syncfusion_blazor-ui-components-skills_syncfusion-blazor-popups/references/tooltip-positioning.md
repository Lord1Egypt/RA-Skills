# Tooltip Positioning and Placement

## Table of Contents
- [Overview](#overview)
- [Static Position Options](#static-position-options)
- [Mouse Trailing](#mouse-trailing)
- [Offset Configuration](#offset-configuration)
- [Collision Handling](#collision-handling)
- [Best Practices](#best-practices)

## Overview

The Tooltip component offers flexible positioning options to ensure tooltips appear in the most appropriate location relative to their target elements. You can:

- Choose from 12 static positions around the target
- Enable mouse trailing for dynamic positioning
- Apply custom offsets for fine-tuned placement
- Configure collision detection for viewport boundaries

## Static Position Options

Tooltips can be attached to 12 predefined positions around the target element using the `Position` property.

### Available Positions

The Position enum provides these options:

**Top Positions:**
- `TopLeft` - Above target, aligned to left edge
- `TopCenter` - Above target, centered (default)
- `TopRight` - Above target, aligned to right edge

**Bottom Positions:**
- `BottomLeft` - Below target, aligned to left edge
- `BottomCenter` - Below target, centered
- `BottomRight` - Below target, aligned to right edge

**Left Positions:**
- `LeftTop` - Left of target, aligned to top edge
- `LeftCenter` - Left of target, centered vertically
- `LeftBottom` - Left of target, aligned to bottom edge

**Right Positions:**
- `RightTop` - Right of target, aligned to top edge
- `RightCenter` - Right of target, centered vertically
- `RightBottom` - Right of target, aligned to bottom edge

### Default Position

By default, tooltips appear at `TopCenter` if no position is specified.

### Basic Position Example

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#target" Content="@Content" Position="Position.RightCenter">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Tooltip Content";
}
```

### All Positions Demo

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 50px;">
    
    <!-- Top Positions -->
    <SfTooltip Target="#topLeft" Content="TopLeft Position" Position="Position.TopLeft">
        <SfButton ID="topLeft" Content="Top Left"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#topCenter" Content="TopCenter Position" Position="Position.TopCenter">
        <SfButton ID="topCenter" Content="Top Center"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#topRight" Content="TopRight Position" Position="Position.TopRight">
        <SfButton ID="topRight" Content="Top Right"></SfButton>
    </SfTooltip>
    
    <!-- Bottom Positions -->
    <SfTooltip Target="#bottomLeft" Content="BottomLeft Position" Position="Position.BottomLeft">
        <SfButton ID="bottomLeft" Content="Bottom Left"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#bottomCenter" Content="BottomCenter Position" Position="Position.BottomCenter">
        <SfButton ID="bottomCenter" Content="Bottom Center"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#bottomRight" Content="BottomRight Position" Position="Position.BottomRight">
        <SfButton ID="bottomRight" Content="Bottom Right"></SfButton>
    </SfTooltip>
    
    <!-- Left Positions -->
    <SfTooltip Target="#leftTop" Content="LeftTop Position" Position="Position.LeftTop">
        <SfButton ID="leftTop" Content="Left Top"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#leftCenter" Content="LeftCenter Position" Position="Position.LeftCenter">
        <SfButton ID="leftCenter" Content="Left Center"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#leftBottom" Content="LeftBottom Position" Position="Position.LeftBottom">
        <SfButton ID="leftBottom" Content="Left Bottom"></SfButton>
    </SfTooltip>
    
    <!-- Right Positions -->
    <SfTooltip Target="#rightTop" Content="RightTop Position" Position="Position.RightTop">
        <SfButton ID="rightTop" Content="Right Top"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#rightCenter" Content="RightCenter Position" Position="Position.RightCenter">
        <SfButton ID="rightCenter" Content="Right Center"></SfButton>
    </SfTooltip>
    
    <SfTooltip Target="#rightBottom" Content="RightBottom Position" Position="Position.RightBottom">
        <SfButton ID="rightBottom" Content="Right Bottom"></SfButton>
    </SfTooltip>
    
</div>
```

### When to Use Each Position

**TopCenter (default):**
- General purpose positioning
- Form field help text
- Button descriptions
- Most common use case

**BottomCenter:**
- Elements near top of viewport
- Dropdown triggers
- Top navigation items

**LeftCenter / RightCenter:**
- Sidebar items
- Horizontal space constraints
- Icon buttons in toolbars
- Better for wide content

**Corner positions (TopLeft, TopRight, etc.):**
- Specific alignment requirements
- Custom layouts
- Precise positioning needs
- Avoiding specific UI elements

## Mouse Trailing

Mouse trailing makes the tooltip follow the mouse pointer as it moves over the target element.

### Enabling Mouse Trailing

Set the `MouseTrail` property to `true`:

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip MouseTrail="true" Content="@Content" Target="#target">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Tooltip Content";
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

### Mouse Trailing with Large Target

```razor
<SfTooltip MouseTrail="true" Content="This tooltip follows your mouse!" Target="#trackArea">
    <div id="trackArea" style="width: 400px; height: 300px; border: 2px dashed #999; 
                               display: flex; align-items: center; justify-content: center;
                               background: #f5f5f5;">
        <p>Move your mouse around this area</p>
    </div>
</SfTooltip>
```

### Key Points

- **MouseTrail** property accepts boolean (default: `false`)
- Tooltip follows cursor movement within target bounds
- Tip pointer position auto-adjusts to stay pointing at target
- Position values (TopCenter, etc.) are ignored when MouseTrail is enabled
- Works best with larger target areas
- Can be combined with offset values

### When to Use Mouse Trailing

**Good for:**
- Image annotations
- Map interactions
- Canvas/drawing areas
- Large interactive regions
- Data visualization hover details

**Avoid for:**
- Small buttons or links
- Navigation menus
- Form inputs
- Mobile devices (not supported)

### Important Note

When mouse trailing is enabled, static position values like TopCenter, BottomLeft, etc., are not applied. The tooltip automatically positions itself relative to the mouse pointer.

## Offset Configuration

Offsets allow fine-tuning tooltip position by specifying pixel distances from the default position.

### OffsetX and OffsetY Properties

- `OffsetX` - Horizontal offset (positive = right, negative = left)
- `OffsetY` - Vertical offset (positive = down, negative = up)

### Basic Offset Example

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#target" Content="@Content" OffsetX="30" OffsetY="30">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Tooltip Content";
}
```

### Combining Position with Offset

```razor
<!-- Tooltip appears to the right, but shifted down 20px -->
<SfTooltip Target="#btn1" Content="Offset tooltip" 
           Position="Position.RightCenter" OffsetY="20">
    <SfButton ID="btn1" Content="Button"></SfButton>
</SfTooltip>

<!-- Tooltip appears above, but shifted left 30px -->
<SfTooltip Target="#btn2" Content="Another offset" 
           Position="Position.TopCenter" OffsetX="-30">
    <SfButton ID="btn2" Content="Button"></SfButton>
</SfTooltip>
```

### Mouse Trailing with Offset

```razor
<SfTooltip Target="#target" ShowTipPointer="false" MouseTrail="true" 
           Content="@Content" OffsetX="30" OffsetY="30">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Tooltip Content";
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

### Offset Use Cases

**Avoiding UI Overlap:**
```razor
<!-- Shift tooltip to avoid header -->
<SfTooltip Target="#menuItem" Content="Menu option" 
           Position="Position.BottomCenter" OffsetY="10">
    <button id="menuItem">Menu</button>
</SfTooltip>
```

**Custom Spacing:**
```razor
<!-- More space between tooltip and target -->
<SfTooltip Target="#icon" Content="Icon description" 
           Position="Position.RightCenter" OffsetX="20">
    <span id="icon">🔔</span>
</SfTooltip>
```

**Alignment Adjustments:**
```razor
<!-- Fine-tune alignment with adjacent elements -->
<SfTooltip Target="#label" Content="Help text" 
           Position="Position.TopRight" OffsetX="-10" OffsetY="-5">
    <label id="label">Field Name</label>
</SfTooltip>
```

## Collision Handling

The Tooltip component automatically handles collisions with viewport boundaries, ensuring tooltips remain visible.

### Automatic Collision Detection

By default, collision detection is enabled:
- Tooltip automatically repositions when it would extend beyond viewport
- Horizontal collision: Tooltip shifts horizontally to stay within viewport
- Vertical collision: Tooltip flips to opposite side (top ↔ bottom)

### WindowCollision Property

The `WindowCollision` property changes collision detection from the parent element to the entire viewport.

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip ID="Tooltip" Target="#btn" Content="@content" 
           Position="Position.TopCenter" WindowCollision="true">
    <SfButton ID="btn" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string content = "Lets go green & Save Earth !!";
}
```

### Collision Behavior

**Default (WindowCollision="false"):**
- Collision detection relative to Tooltip's parent container
- Useful when Tooltip is within a scrollable region
- Repositions within parent bounds

**WindowCollision="true":**
- Collision detection relative to browser viewport
- Ensures tooltip never goes off-screen
- Recommended for tooltips in fixed/absolute positioned containers

### Edge Cases

**Top Edge Collision:**
```razor
<!-- Near top of page - will flip to bottom -->
<div style="margin-top: 10px;">
    <SfTooltip Target="#topBtn" Content="Near top edge" Position="Position.TopCenter">
        <button id="topBtn">Button</button>
    </SfTooltip>
</div>
```

**Right Edge Collision:**
```razor
<!-- Near right edge - will shift left -->
<div style="position: absolute; right: 10px;">
    <SfTooltip Target="#rightBtn" Content="Near right edge" Position="Position.RightCenter">
        <button id="rightBtn">Button</button>
    </SfTooltip>
</div>
```

**Scrollable Container:**
```razor
<div style="height: 200px; overflow-y: scroll; position: relative;">
    <!-- WindowCollision="false" for proper collision within scroll container -->
    <SfTooltip Target="#scrollItem" Content="Inside scroll" WindowCollision="false">
        <div id="scrollItem">Item</div>
    </SfTooltip>
</div>
```

## Best Practices

### Choosing Positions

1. **Consider content length:**
   - Short content: Any position works
   - Long content: LeftCenter/RightCenter provide more horizontal space
   - Multi-line content: TopCenter/BottomCenter for better readability

2. **Consider target location:**
   - Near viewport edges: Use positions that point away from edges
   - In navigation bars: BottomCenter for top nav, TopCenter for bottom nav
   - In sidebars: RightCenter for left sidebar, LeftCenter for right sidebar

3. **Consider surrounding UI:**
   - Avoid covering important elements
   - Use offsets to create appropriate spacing
   - Test with different screen sizes

### Performance Considerations

- Mouse trailing can be processor-intensive on complex pages
- Avoid mouse trailing for many simultaneous tooltips
- Use static positions when possible for better performance

### Accessibility

- Position shouldn't affect screen reader experience
- Ensure tooltip content is readable regardless of position
- Test keyboard navigation with different positions
- Verify tooltips don't obscure focused elements

### Mobile Considerations

- Mouse trailing doesn't work on touch devices
- Consider touch target sizes when positioning
- Test positions on different screen orientations
- Ensure tooltips don't extend beyond mobile viewport

### Testing Positions

Always test tooltip positions:
- At different viewport sizes
- Near viewport edges
- In scrollable containers
- With long and short content
- On different screen resolutions

### Common Patterns

**Form Field Help:**
```razor
<!-- Position to right to avoid covering input -->
<SfTooltip Target="#emailInput" Content="Enter valid email" 
           Position="Position.RightCenter" OpensOn="Focus">
    <input id="emailInput" type="email" />
</SfTooltip>
```

**Icon Buttons in Toolbar:**
```razor
<!-- Bottom position for top toolbar -->
<SfTooltip Target=".toolbar-icon" Content="Button description" 
           Position="Position.BottomCenter">
    <div class="toolbar">
        <button class="toolbar-icon">💾</button>
        <button class="toolbar-icon">✂️</button>
        <button class="toolbar-icon">📋</button>
    </div>
</SfTooltip>
```

**Status Indicators:**
```razor
<!-- Right position for left-aligned status -->
<SfTooltip Target=".status-dot" Content="System status: Active" 
           Position="Position.RightCenter" OffsetX="10">
    <span class="status-dot">●</span>
</SfTooltip>
```

**Image Annotations:**
```razor
<!-- Mouse trailing for image exploration -->
<SfTooltip Target="#annotatedImage" MouseTrail="true" 
           Content="Hover to explore details">
    <img id="annotatedImage" src="/image.jpg" alt="Annotated" />
</SfTooltip>
```

### Debugging Position Issues

If tooltips don't appear where expected:

1. **Check parent positioning:** Parent elements with `position: relative` affect collision detection
2. **Verify target selector:** Ensure Target matches the intended element
3. **Check z-index:** Tooltip might be behind other elements
4. **Test WindowCollision:** Try toggling WindowCollision property
5. **Inspect offsets:** Remove custom offsets to see default behavior
6. **Check viewport size:** Collision detection might be repositioning tooltip
