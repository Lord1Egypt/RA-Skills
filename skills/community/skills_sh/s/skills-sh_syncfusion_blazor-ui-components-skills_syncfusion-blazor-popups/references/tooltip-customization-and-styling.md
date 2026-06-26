# Tooltip Customization and Styling

## Table of Contents
- [Overview](#overview)
- [CssClass Property](#cssclass-property)
- [Tip Pointer Customization](#tip-pointer-customization)
- [Tooltip Wrapper Styling](#tooltip-wrapper-styling)
- [Content Styling](#content-styling)
- [Arrow Tip Styling](#arrow-tip-styling)
- [Complete Customization Example](#complete-customization-example)
- [CSS Class Reference](#css-class-reference)
- [Best Practices](#best-practices)

## Overview

The Tooltip component can be fully customized using the `CssClass` property combined with CSS rules. You can style:
- Tooltip wrapper (background, border, shadow, opacity)
- Content area (text color, font, padding)
- Tip pointer/arrow (size, colors, shape for all 4 directions)
- Animations and transitions

All customization is done through CSS, providing complete control over appearance.

## CssClass Property

The `CssClass` property accepts a custom CSS class name that will be applied to the tooltip wrapper element.

### Basic Usage

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#target" CssClass="custom-tooltip" Content="Styled tooltip">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

<style>
    .custom-tooltip.e-tooltip-wrap {
        background-color: #2196F3;
        border-radius: 8px;
    }
    
    .custom-tooltip.e-tooltip-wrap .e-tip-content {
        color: white;
        font-weight: 600;
    }
</style>
```

### Multiple Custom Classes

```razor
<!-- Apply multiple classes -->
<SfTooltip Target="#btn1" CssClass="custom-tooltip theme-blue" Content="Blue theme">
    <SfButton ID="btn1" Content="Blue"></SfButton>
</SfTooltip>

<SfTooltip Target="#btn2" CssClass="custom-tooltip theme-green" Content="Green theme">
    <SfButton ID="btn2" Content="Green"></SfButton>
</SfTooltip>

<style>
    .theme-blue.e-tooltip-wrap {
        background-color: #2196F3;
    }
    
    .theme-green.e-tooltip-wrap {
        background-color: #4CAF50;
    }
    
    .custom-tooltip.e-tooltip-wrap .e-tip-content {
        color: white;
        padding: 10px 15px;
    }
</style>
```

## Tip Pointer Customization

The tip pointer (arrow) can be customized for size, background color, and border colors.

### Basic Tip Pointer Styling

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#target" CssClass="customtip" Content="@Content">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Tooltip arrow customized";
}

<style>
    #target {
        background-color: #cfd8dc;
        border: 3px solid #eceff1;
        box-sizing: border-box;
        margin: 80px auto;
        padding: 20px 0;
        width: 200px;
        text-align: center;
        color: #424242;
        font-size: 20px;
        user-select: none;
    }

    .customtip.e-tooltip-wrap {
        padding: 4px;
    }

    /* Tip pointer dimensions for all directions */
    .customtip.e-tooltip-wrap .e-arrow-tip.e-tip-bottom,
    .customtip.e-tooltip-wrap .e-arrow-tip.e-tip-top,
    .customtip.e-tooltip-wrap .e-arrow-tip.e-tip-left,    
    .customtip.e-tooltip-wrap .e-arrow-tip.e-tip-right {
        height: 20px;
        width: 12px;
    }

    /* Bottom arrow (tooltip above target) */
    .customtip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-bottom {
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 20px solid #616161;
    }

    /* Top arrow (tooltip below target) */
    .customtip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top {
        border-bottom: 20px solid #616161;
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
    }

    /* Left arrow (tooltip to the right) */
    .customtip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-left {
        border-bottom: 6px solid transparent;
        border-right: 20px solid #616161;
        border-top: 6px solid transparent;
    }

    /* Right arrow (tooltip to the left) */
    .customtip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-right {
        border-bottom: 6px solid transparent;
        border-left: 20px solid #616161;
        border-top: 6px solid transparent;
    }
</style>
```

### Hiding Tip Pointer

```razor
<SfTooltip Target="#target" ShowTipPointer="false" Content="No arrow">
    <SfButton ID="target" Content="No Pointer"></SfButton>
</SfTooltip>
```

### Rounded Tip Pointer

```razor
<style>
    .rounded-tip.e-tooltip-wrap .e-arrow-tip-outer {
        border-radius: 2px;
    }
</style>
```

## Tooltip Wrapper Styling

The tooltip wrapper (`.e-tooltip-wrap`) is the main container element.

### Background and Border

```razor
<SfTooltip Target="#target" CssClass="custom-wrapper" Content="Custom wrapper">
    <SfButton ID="target" Content="Show"></SfButton>
</SfTooltip>

<style>
    .custom-wrapper.e-tooltip-wrap.e-popup {
        background-color: #fff;
        border: 2px solid #000;
        border-radius: 4px;
    }
</style>
```

### Shadow and Opacity

```razor
<style>
    .shadow-tooltip.e-tooltip-wrap {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        opacity: 0.95;
    }
    
    .elevated-tooltip.e-tooltip-wrap {
        filter: drop-shadow(2px 5px 5px rgba(0, 0, 0, 0.25));
    }
</style>
```

### Size and Spacing

```razor
<style>
    .spacious-tooltip.e-tooltip-wrap {
        padding: 20px;
        min-width: 250px;
    }
    
    .compact-tooltip.e-tooltip-wrap {
        padding: 5px;
    }
</style>
```

## Content Styling

Style the tooltip content area (`.e-tip-content`).

### Text Styling

```razor
<SfTooltip Target="#target" CssClass="custom-content" Content="@Content">
    <SfButton ID="target" Content="Show"></SfButton>
</SfTooltip>

<style>
    .custom-content.e-tooltip-wrap .e-tip-content {
        color: #000;
        font-size: 14px;
        font-weight: 500;
        line-height: 1.6;
        text-align: center;
    }
</style>
```

### Content with Icons

```razor
<SfTooltip Target="#target" CssClass="icon-tooltip">
    <ContentTemplate>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 20px;">⚠️</span>
            <span>Warning: This action cannot be undone</span>
        </div>
    </ContentTemplate>
    <ChildContent>
        <SfButton ID="target" Content="Delete"></SfButton>
    </ChildContent>
</SfTooltip>

<style>
    .icon-tooltip.e-tooltip-wrap .e-tip-content {
        padding: 12px 16px;
    }
</style>
```

## Arrow Tip Styling

Complete control over arrow appearance for all 4 directions.

### All Direction Arrows

```razor
<style>
    .custom-arrows.e-tooltip-wrap .e-arrow-tip.e-tip-bottom {
        height: 12px;
        left: 50%;
        top: 100%;
        width: 24px;
    }

    .custom-arrows.e-tooltip-wrap .e-arrow-tip.e-tip-top {
        height: 12px;
        left: 50%;
        top: -9px;
        width: 24px;
    }

    .custom-arrows.e-tooltip-wrap .e-arrow-tip.e-tip-left {
        height: 24px;
        left: -9px;
        top: 48%;
        width: 12px;
    }

    .custom-arrows.e-tooltip-wrap .e-arrow-tip.e-tip-right {
        height: 24px;
        left: 100%;
        top: 50%;
        width: 12px;
    }
</style>
```

### Outer Tip (Border)

```razor
<style>
    /* Bottom arrow outer tip (border) */
    .custom-arrows.e-tooltip-wrap .e-arrow-tip-outer.e-tip-bottom {
        border-left: 12px solid transparent;
        border-right: 14px solid transparent;
        border-top: 12px solid #000;
    }

    /* Top arrow outer tip */
    .custom-arrows.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top {
        border-bottom: 12px solid #000;
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
    }

    /* Left arrow outer tip */
    .custom-arrows.e-tooltip-wrap .e-arrow-tip-outer.e-tip-left {
        border-bottom: 12px solid transparent;
        border-right: 12px solid #000;
        border-top: 12px solid transparent;
    }

    /* Right arrow outer tip */
    .custom-arrows.e-tooltip-wrap .e-arrow-tip-outer.e-tip-right {
        border-bottom: 12px solid transparent;
        border-left: 12px solid #000;
        border-top: 12px solid transparent;
    }
</style>
```

### Inner Tip (Fill)

```razor
<style>
    .custom-arrows.e-tooltip-wrap .e-arrow-tip-inner.e-tip-bottom {
        color: #fff;
        font-size: 25.9px;
    }
</style>
```

## Complete Customization Example

A fully customized tooltip with all styling elements:

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#target" CssClass="customtooltip" Content="@Content">
    <SfButton ID="target" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Tooltip customized";
}

<style>
    #target {
        background-color: #ececec;
        border: 1px solid #c8c8c8;
        box-sizing: border-box;
        margin: 70px auto;
        padding: 20px;
        width: 200px;
    }

    /* Wrapper customization */
    .customtooltip.e-tooltip-wrap {
        border-radius: 4px;
        opacity: 1;
    }

    .customtooltip.e-tooltip-wrap.e-popup {
        background-color: #fff;
        border: 2px solid #000;
    }

    /* Content customization */
    .customtooltip.e-tooltip-wrap .e-tip-content {
        color: #000;
        font-size: 12px;
        line-height: 20px;
    }

    /* Arrow size for all directions */
    .customtooltip.e-tooltip-wrap .e-arrow-tip.e-tip-bottom {
        height: 12px;
        left: 50%;
        top: 100%;
        width: 24px;
    }

    .customtooltip.e-tooltip-wrap .e-arrow-tip.e-tip-top {
        height: 12px;
        left: 50%;
        top: -9px;
        width: 24px;
    }

    .customtooltip.e-tooltip-wrap .e-arrow-tip.e-tip-left {
        height: 24px;
        left: -9px;
        top: 48%;
        width: 12px;
    }

    .customtooltip.e-tooltip-wrap .e-arrow-tip.e-tip-right {
        height: 24px;
        left: 100%;
        top: 50%;
        width: 12px;
    }

    /* Arrow colors for all directions */
    .customtooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-bottom {
        border-left: 12px solid transparent;
        border-right: 14px solid transparent;
        border-top: 12px solid #000;
    }

    .customtooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top {
        border-bottom: 12px solid #000;
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
    }

    .customtooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-left {
        border-bottom: 12px solid transparent;
        border-right: 12px solid #000;
        border-top: 12px solid transparent;
    }

    .customtooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-right {
        border-bottom: 12px solid transparent;
        border-left: 12px solid #000;
        border-top: 12px solid transparent;
    }

    .customtooltip.e-tooltip-wrap .e-arrow-tip-inner.e-tip-bottom {
        color: #fff;
        font-size: 25.9px;
    }
</style>
```

## CSS Class Reference

### Main Elements

| CSS Class | Description |
|-----------|-------------|
| `.e-tooltip-wrap` | Main tooltip wrapper |
| `.e-tooltip-wrap.e-popup` | Popup container (for background/border) |
| `.e-tip-content` | Content area inside tooltip |
| `.e-arrow-tip` | Arrow/pointer container |
| `.e-arrow-tip-outer` | Arrow border/outline |
| `.e-arrow-tip-inner` | Arrow fill |

### Direction Classes

| CSS Class | When Used |
|-----------|-----------|
| `.e-tip-top` | Tooltip below target, arrow points up |
| `.e-tip-bottom` | Tooltip above target, arrow points down |
| `.e-tip-left` | Tooltip to right of target, arrow points left |
| `.e-tip-right` | Tooltip to left of target, arrow points right |

### Complete Selector Examples

```css
/* Tooltip wrapper */
.my-tooltip.e-tooltip-wrap { }

/* Tooltip popup/background */
.my-tooltip.e-tooltip-wrap.e-popup { }

/* Content area */
.my-tooltip.e-tooltip-wrap .e-tip-content { }

/* Arrow for bottom position (tooltip above) */
.my-tooltip.e-tooltip-wrap .e-arrow-tip.e-tip-bottom { }
.my-tooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-bottom { }
.my-tooltip.e-tooltip-wrap .e-arrow-tip-inner.e-tip-bottom { }

/* Arrow for top position (tooltip below) */
.my-tooltip.e-tooltip-wrap .e-arrow-tip.e-tip-top { }
.my-tooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top { }

/* Arrow for left position (tooltip right) */
.my-tooltip.e-tooltip-wrap .e-arrow-tip.e-tip-left { }
.my-tooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-left { }

/* Arrow for right position (tooltip left) */
.my-tooltip.e-tooltip-wrap .e-arrow-tip.e-tip-right { }
.my-tooltip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-right { }
```

## Best Practices

### Specificity

Always include `.e-tooltip-wrap` in selectors for proper specificity:

✅ **Correct:**
```css
.my-tooltip.e-tooltip-wrap {
    background-color: blue;
}
```

❌ **Incorrect (may not work):**
```css
.my-tooltip {
    background-color: blue;
}
```

### Arrow Styling

When customizing arrows:
1. Set dimensions with `.e-arrow-tip`
2. Set colors with `.e-arrow-tip-outer` (border)
3. Adjust `.e-arrow-tip-inner` for fill (rarely needed)
4. Style ALL 4 directions for consistent appearance

### Performance

- Avoid complex CSS3 animations on hover tooltips
- Use `transform` and `opacity` for animations (hardware accelerated)
- Minimize box-shadow complexity
- Prefer CSS over inline styles

### Theming

Create reusable theme classes:

```css
/* Success theme */
.tooltip-success.e-tooltip-wrap.e-popup {
    background-color: #4CAF50;
    border-color: #45a049;
}

.tooltip-success.e-tooltip-wrap .e-tip-content {
    color: white;
}

/* Error theme */
.tooltip-error.e-tooltip-wrap.e-popup {
    background-color: #f44336;
    border-color: #da190b;
}

.tooltip-error.e-tooltip-wrap .e-tip-content {
    color: white;
}

/* Warning theme */
.tooltip-warning.e-tooltip-wrap.e-popup {
    background-color: #ff9800;
    border-color: #e68900;
}

.tooltip-warning.e-tooltip-wrap .e-tip-content {
    color: white;
}
```

### Accessibility

- Maintain sufficient color contrast (WCAG AA: 4.5:1 for text)
- Don't rely solely on color to convey information
- Ensure text remains readable with custom fonts
- Test with different zoom levels

### Browser Compatibility

- Test arrow rendering across browsers
- Use vendor prefixes for CSS3 properties if needed
- Fallback styles for older browsers
- Consider mobile browser rendering

### Common Patterns

**Material Design Style:**
```css
.material-tooltip.e-tooltip-wrap {
    background-color: #616161;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.material-tooltip.e-tooltip-wrap .e-tip-content {
    color: white;
    font-size: 14px;
    padding: 8px 16px;
}
```

**Flat Design:**
```css
.flat-tooltip.e-tooltip-wrap {
    background-color: #3498db;
    border: none;
    border-radius: 0;
}

.flat-tooltip.e-tooltip-wrap .e-tip-content {
    color: white;
    font-weight: 600;
}
```

**Glassmorphism:**
```css
.glass-tooltip.e-tooltip-wrap {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.glass-tooltip.e-tooltip-wrap .e-tip-content {
    color: #333;
}
```

**Dark Mode:**
```css
@media (prefers-color-scheme: dark) {
    .adaptive-tooltip.e-tooltip-wrap.e-popup {
        background-color: #2d2d2d;
        border-color: #444;
    }
    
    .adaptive-tooltip.e-tooltip-wrap .e-tip-content {
        color: #e0e0e0;
    }
}
```
