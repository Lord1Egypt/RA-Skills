# Tooltip Dimensions and Sizing

This guide covers how to control tooltip size using the Width and Height properties, including scroll behavior for content overflow.

## Overview

Tooltips can have automatic or fixed dimensions:
- **Auto (default)**: Tooltip sizes based on content
- **Fixed**: Specify exact pixel dimensions
- **Scroll mode**: Enabled when content overflows fixed height

Use the `Width` and `Height` properties to control tooltip dimensions.

## Width and Height Properties

Both properties accept:
- `"auto"` (default) - Size based on content
- String with pixels - e.g., `"200px"`, `"300px"`
- Number values - Interpreted as pixels

### Auto Sizing (Default)

When Width and Height are not specified, tooltips automatically size to fit content:

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<!-- Auto-sized tooltip -->
<SfTooltip Target="#btn" Content="This tooltip will size to fit this text">
    <SfButton ID="btn" Content="Auto Size"></SfButton>
</SfTooltip>
```

**Behavior:**
- Width expands to fit content up to a maximum (browser dependent)
- Long text wraps to multiple lines
- Height grows with content
- No scroll bars appear

### Fixed Width

Set a specific width while allowing height to adjust:

```razor
<SfTooltip Target="#btn" Width="300px" Content="This tooltip has a fixed width of 300 pixels. Height adjusts automatically to fit content.">
    <SfButton ID="btn" Content="Fixed Width"></SfButton>
</SfTooltip>
```

**When to use:**
- Consistent tooltip widths across application
- Controlling text wrapping
- Aligning multiple tooltips
- Preventing overly wide tooltips

### Fixed Height

Set a specific height while allowing width to adjust:

```razor
<SfTooltip Target="#btn" Height="100px" Content="This tooltip has fixed height">
    <SfButton ID="btn" Content="Fixed Height"></SfButton>
</SfTooltip>
```

**When to use:**
- Limiting vertical space
- Creating scroll regions
- Consistent tooltip heights

### Fixed Width and Height

Control both dimensions:

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip ID="Tooltip" Height="50px" Width="200px" Target="#btn" Content="@Content">
    <SfButton ID="btn" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Lets go green & Save Earth !!";
}
```

**When to use:**
- Precise layout control
- Grid-based tooltip designs
- Uniform tooltip sizes across interface

## Scroll Mode

When Height is specified and content exceeds it, scroll mode automatically enables.

### Basic Scroll Example

```razor
@using Syncfusion.Blazor.Popups

<SfTooltip ID="tooltip" Height="60px" Width="200px" IsSticky="true" Target="#target" Content="@Content">
    <div id='container'>
        <p>
            A green home is a type of house designed to be
            <a id="target">
                <u>environmentally friendly</u>
            </a> 
            and sustainable.
        </p>
    </div>
</SfTooltip>

@code
{
    string Content = "<div><b>Environmentally friendly</b> or environment-friendly, (also referred to as eco-friendly, nature-friendly, and green) are marketing and sustainability terms referring to goods and services, laws, guidelines and policies that inflict reduced, minimal, or no harm upon ecosystems or the environment.</div>";
}
```

### Scroll Mode Features

- **Automatic activation**: Enabled when content height > tooltip height
- **Vertical scrollbar**: Appears when content overflows
- **User control**: Users scroll to view hidden content
- **Works best with IsSticky**: Gives users time to scroll

### Scroll with Template Content

```razor
<SfTooltip Height="150px" Width="300px" IsSticky="true" Target="#scrollBtn" OpensOn="Click">
    <ContentTemplate>
        <div style="padding: 10px;">
            <h4 style="margin-top: 0;">Long Content</h4>
            <p>Paragraph 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            <p>Paragraph 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            <p>Paragraph 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
            <p>Paragraph 4: Duis aute irure dolor in reprehenderit in voluptate velit.</p>
            <p>Paragraph 5: Excepteur sint occaecat cupidatat non proident.</p>
        </div>
    </ContentTemplate>
    <ChildContent>
        <SfButton ID="scrollBtn" Content="Show Scrollable Tooltip"></SfButton>
    </ChildContent>
</SfTooltip>
```

### Important Note

⚠️ Scroll mode works best when combined with `IsSticky="true"`:
- Sticky mode keeps tooltip open with close button
- Users have time to read and scroll through content
- Without sticky mode, tooltip may close while user attempts to scroll

## Sizing Strategies

### Content-Driven (Auto)

Best for:
- Short, dynamic content
- Variable-length messages
- Icon button descriptions
- Status indicators

```razor
<!-- Auto width and height -->
<SfTooltip Target=".status" Content="@GetStatusMessage()">
    <span class="status">●</span>
</SfTooltip>

@code {
    string GetStatusMessage() => DateTime.Now.Hour < 12 ? "Good morning!" : "Good afternoon!";
}
```

### Fixed Width, Auto Height

Best for:
- Consistent tooltip appearance
- Controlling text wrapping
- Multi-line descriptions
- Predictable layout

```razor
<!-- Consistent 250px width, height grows with content -->
<SfTooltip Target=".help-icon" Width="250px">
    <ContentTemplate>
        <div>
            <h5 style="margin: 0 0 8px 0;">Help Topic</h5>
            <p style="margin: 0;">This description can be multiple lines. Width is fixed at 250px, but height will grow to accommodate all content.</p>
        </div>
    </ContentTemplate>
    <ChildContent>
        <span class="help-icon">?</span>
    </ChildContent>
</SfTooltip>
```

### Fixed Dimensions with Scroll

Best for:
- Long articles or documentation
- Lists with many items
- Bounded tooltip size requirements
- Dashboard information cards

```razor
<!-- Fixed 300x200px with scroll for overflow -->
<SfTooltip Height="200px" Width="300px" IsSticky="true" Target="#articlePreview" OpensOn="Click">
    <ContentTemplate>
        <div style="padding: 15px;">
            <h4 style="margin-top: 0;">Article Preview</h4>
            <p>Long article content that exceeds the fixed height...</p>
            <p>More content...</p>
            <p>And more...</p>
            <p>Users can scroll to read everything.</p>
        </div>
    </ContentTemplate>
    <ChildContent>
        <button id="articlePreview">Preview Article</button>
    </ChildContent>
</SfTooltip>
```

## Responsive Sizing

### Using Percentage

While Width and Height don't accept percentages directly, you can use CSS:

```razor
<SfTooltip Target="#responsive" CssClass="responsive-tooltip" Content="Responsive sizing">
    <button id="responsive">Responsive</button>
</SfTooltip>

<style>
    .responsive-tooltip.e-tooltip-wrap {
        width: 80vw;
        max-width: 400px;
    }
</style>
```

### Media Queries

Adapt tooltip size based on screen size:

```razor
<SfTooltip Target="#adaptive" CssClass="adaptive-size" Width="300px" Content="Adaptive content">
    <button id="adaptive">Adaptive</button>
</SfTooltip>

<style>
    @media (max-width: 768px) {
        .adaptive-size.e-tooltip-wrap {
            width: 90vw !important;
            max-width: 300px !important;
        }
    }
    
    @media (max-width: 480px) {
        .adaptive-size.e-tooltip-wrap {
            width: 95vw !important;
            max-width: 250px !important;
        }
    }
</style>
```

### Maximum Width Constraint

Prevent tooltips from becoming too wide:

```razor
<SfTooltip Target="#constrained" CssClass="max-width-tooltip" Content="@longContent">
    <button id="constrained">Constrained Width</button>
</SfTooltip>

@code {
    string longContent = "This is a very long piece of content that could potentially make the tooltip extremely wide, but the max-width constraint will prevent that.";
}

<style>
    .max-width-tooltip.e-tooltip-wrap {
        max-width: 400px;
    }
</style>
```

## Practical Examples

### Help Text (Auto Size)

```razor
<SfTooltip Target="#helpBtn" Content="Click to view help documentation">
    <button id="helpBtn">?</button>
</SfTooltip>
```

### Description Card (Fixed Width)

```razor
<SfTooltip Target="#productCard" Width="280px" OpensOn="Hover">
    <ContentTemplate>
        <div style="padding: 12px;">
            <h4 style="margin: 0 0 8px 0;">Product Name</h4>
            <p style="margin: 0; font-size: 13px; color: #666;">
                A brief description of the product with consistent width for uniform appearance.
            </p>
            <div style="margin-top: 10px; font-weight: bold;">$99.99</div>
        </div>
    </ContentTemplate>
    <ChildContent>
        <div id="productCard" style="cursor: pointer;">View Product</div>
    </ChildContent>
</SfTooltip>
```

### Information Panel (Fixed + Scroll)

```razor
<SfTooltip Height="250px" Width="350px" IsSticky="true" Target="#infoPanel" OpensOn="Click">
    <ContentTemplate>
        <div style="padding: 15px;">
            <h3 style="margin: 0 0 15px 0;">System Information</h3>
            
            <h5>Hardware</h5>
            <ul>
                <li>CPU: Intel Core i7</li>
                <li>RAM: 16GB DDR4</li>
                <li>Storage: 512GB SSD</li>
            </ul>
            
            <h5>Software</h5>
            <ul>
                <li>OS: Windows 11</li>
                <li>Browser: Chrome 120</li>
                <li>Framework: .NET 8</li>
            </ul>
            
            <h5>Network</h5>
            <ul>
                <li>IP: 192.168.1.100</li>
                <li>Status: Connected</li>
                <li>Speed: 1 Gbps</li>
            </ul>
        </div>
    </ContentTemplate>
    <ChildContent>
        <SfButton ID="infoPanel" IconCss="e-icons e-info" Content="System Info"></SfButton>
    </ChildContent>
</SfTooltip>
```

### Mobile-Optimized Tooltip

```razor
<SfTooltip Target="#mobileBtn" CssClass="mobile-tooltip" Width="300px">
    <ContentTemplate>
        <div style="padding: 15px; font-size: 16px;">
            <p style="margin: 0;">Content optimized for mobile devices with larger touch targets and readable text.</p>
        </div>
    </ContentTemplate>
    <ChildContent>
        <button id="mobileBtn" style="padding: 15px; font-size: 16px;">Tap Me</button>
    </ChildContent>
</SfTooltip>

<style>
    @media (max-width: 480px) {
        .mobile-tooltip.e-tooltip-wrap {
            width: 90vw !important;
        }
        
        .mobile-tooltip.e-tooltip-wrap .e-tip-content {
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
    }
</style>
```

## Best Practices

### Choosing Dimensions

**Use Auto when:**
- Content length varies significantly
- Tooltips are simple text hints
- You want minimal configuration
- Content is generally short

**Use Fixed Width when:**
- You want consistent appearance across tooltips
- Text wrapping needs control
- Aligning multiple tooltips
- Building a design system

**Use Fixed Height when:**
- Limiting vertical space is critical
- Creating scrollable content areas
- Dashboard information panels
- Tooltips in constrained layouts

### Scroll Mode Guidelines

1. **Always use with IsSticky="true"**
   - Users need time to scroll
   - Without sticky, tooltip may close prematurely

2. **Set reasonable height**
   - Too small: Constant scrolling frustration
   - Too large: Defeats purpose of scroll
   - Sweet spot: Show 2-3 items, scroll for rest

3. **Consider alternatives**
   - For very long content, use modal or drawer instead
   - Tooltips should supplement, not replace main UI

4. **Visual indication**
   - Ensure scroll indicator is visible
   - Consider fade effect at bottom
   - Test on different browsers

### Performance

- Fixed dimensions can improve rendering performance
- Avoid very large tooltips (impacts layout calculations)
- Consider lazy loading content for scrollable tooltips
- Test scroll performance on mobile devices

### Accessibility

- Ensure tooltip content is readable at specified dimensions
- Don't make text too small in constrained tooltips
- Provide adequate padding around scrollable content
- Test with zoom levels (125%, 150%, 200%)
- Ensure scroll indicators are visible

### Mobile Considerations

- Mobile screens are smaller - use responsive sizing
- Touch targets should be larger (min 44x44px)
- Avoid very wide fixed-width tooltips on mobile
- Test scroll behavior on touch devices
- Consider drawer or bottom sheet for complex content

### Testing

Always test tooltip dimensions:
- With minimum and maximum content lengths
- At different screen sizes
- With zoom levels enabled
- On various devices (desktop, tablet, mobile)
- With different content types (text, images, mixed)

## Common Issues

**Content doesn't scroll:**
- Verify Height is set
- Check that content actually exceeds height
- Ensure IsSticky="true" is set
- Check for CSS overflow rules

**Tooltip too wide on mobile:**
- Use responsive CSS with max-width
- Implement media queries
- Test on actual devices
- Consider viewport units (vw)

**Scroll appears unexpectedly:**
- Check padding and margins in content
- Verify Height value is appropriate
- Inspect content actual size vs specified height
- Check line-height causing extra space

**Text cut off:**
- Height may be too small
- Consider padding in height calculation
- Check for min-height CSS conflicts
- Test with different font sizes
