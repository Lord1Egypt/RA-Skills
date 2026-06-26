## Table of Contents

- [Overview](#overview)
- [Basic Implementation](#basic-implementation)
- [Header Customization](#header-customization)
   - [Basic Header](#basic-header)
   - [Dynamic Header Based on Data](#dynamic-header-based-on-data)
   - [Removing Header](#removing-header)
- [Tooltip Format](#tooltip-format)
   - [Standard Placeholders](#standard-placeholders)
   - [Formatting Examples](#formatting-examples)
   - [HTML in Format](#html-in-format)
- [Appearance Customization](#appearance-customization)
   - [Background and Border](#background-and-border)
   - [Font Styling](#font-styling)
   - [Complete Styling Example](#complete-styling-example)
- [Highlight Color](#highlight-color)
- [Tooltip Text Mapping](#tooltip-text-mapping)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

# Tooltip Reference for Syncfusion Blazor Accumulation Charts

## Overview

Tooltips display contextual information when users hover over chart segments. Unlike data labels which are always visible, tooltips appear on-demand, keeping the chart clean while providing detailed information when needed. They're essential for interactive dashboards and applications where space is limited or detailed information would clutter the visualization.

**Key capabilities:**
- Display point values, percentages, and category information
- Custom formatting for numeric values
- HTML-based content with custom headers
- Template support for complex layouts
- Customizable appearance (colors, borders, fonts)
- Highlight chart segments on hover
- Responsive to mouse and touch interactions

**When to use tooltips:**
- Interactive applications (dashboards, web apps)
- Charts with many data points where labels would clutter
- Supplementary information beyond basic values
- Space-constrained layouts
- User-driven exploration of data

**When to avoid tooltips:**
- Static reports or printed materials (use data labels)
- Presentations where hover isn't possible
- Accessibility-critical applications (tooltips may not be screen-reader friendly)
- Mobile-first designs (hover interaction is difficult on touch devices)

## Basic Implementation

Enable tooltips by setting `Enable="true"` in `AccumulationChartTooltipSettings`:

```razor
<SfAccumulationChart Title="Quarterly Revenue">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@RevenueData" 
                                 XName="Quarter" 
                                 YName="Revenue">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartTooltipSettings Enable="true">
    </AccumulationChartTooltipSettings>
</SfAccumulationChart>

@code {
    public class QuarterlyRevenue
    {
        public string Quarter { get; set; }
        public double Revenue { get; set; }
    }

    public List<QuarterlyRevenue> RevenueData = new List<QuarterlyRevenue>
    {
        new QuarterlyRevenue { Quarter = "Q1", Revenue = 125000 },
        new QuarterlyRevenue { Quarter = "Q2", Revenue = 148000 },
        new QuarterlyRevenue { Quarter = "Q3", Revenue = 167000 },
        new QuarterlyRevenue { Quarter = "Q4", Revenue = 192000 }
    };
}
```

**Default tooltip format:**
```
Quarter
Q1 : 125000
```

**Default behavior:**
- Tooltip appears on mouse hover over chart segment
- Displays X-value (category) and Y-value (numeric data)
- Uses theme-based styling
- Disappears when mouse moves away
- Brief fade-in/fade-out animation

## Header Customization

The tooltip header provides context for the displayed information. By default, the series name appears as the header.

### Basic Header

```razor
<AccumulationChartTooltipSettings 
    Enable="true" 
    Header="Revenue Details">
</AccumulationChartTooltipSettings>
```

**Output:**
```
Revenue Details
Q1 : 125000
```

### Dynamic Header Based on Data

```razor
<AccumulationChartTooltipSettings 
    Enable="true" 
    Header="${point.x} Analysis">
</AccumulationChartTooltipSettings>
```

**Output:**
```
Q1 Analysis
Q1 : 125000
```

### Removing Header

```razor
<AccumulationChartTooltipSettings 
    Enable="true" 
    Header="">
</AccumulationChartTooltipSettings>
```

**Output:**
```
Q1 : 125000
```

**When to customize headers:**
- Provide additional context (e.g., "2024 Sales Data")
- Multi-series charts where series names are unclear
- Localization requirements
- Branding consistency

**Header best practices:**
- Keep headers short (< 30 characters)
- Use title case for professional appearance
- Avoid redundant information already in the tooltip body
- Consider removing headers for simple, self-explanatory tooltips

## Tooltip Format

The `Format` property controls how tooltip content is displayed using a template string with placeholders.

### Standard Placeholders

```razor
<AccumulationChartTooltipSettings 
    Enable="true" 
    Format="${point.x} : <b>${point.y}%</b>">
</AccumulationChartTooltipSettings>
```

**Available placeholders:**

| Placeholder | Description | Example Value |
|-------------|-------------|---------------|
| ${point.x} | X-axis value (category) | "Electronics" |
| ${point.y} | Y-axis value (numeric) | 45000 |
| ${point.percentage} | Percentage of total | 32.5 |
| ${point.text} | Point text property | "Top Seller" |
| ${series.name} | Series name | "2024 Sales" |

### Formatting Examples

**Simple value display:**
```razor
<AccumulationChartTooltipSettings 
    Format="${point.x} -> <b>${point.y} units</b>"/>
```
Output: `Electronics -> 45000 units`

**Percentage emphasis:**
```razor
<AccumulationChartTooltipSettings 
    Format="<b>${point.x}</b><br/>${point.y} (${point.percentage}%)"/>
```
Output:
```
Electronics
45000 (32.5%)
```

**Multi-line with HTML:**
```razor
<AccumulationChartTooltipSettings 
    Format="<div style='font-weight: bold; color: #0066cc;'>${point.x}</div>
            <div>Revenue: $${point.y}</div>
            <div style='font-size: 12px; color: #666;'>Share: ${point.percentage}%</div>"/>
```

**Currency formatting:**
Since placeholders don't support .NET format strings, pre-format in data source or use text mapping:

```razor
<AccumulationChartSeries 
    DataSource="@FormattedData" 
    TooltipMappingName="TooltipText">
</AccumulationChartSeries>

<AccumulationChartTooltipSettings 
    Enable="true"
    Format="${point.tooltip}"/>

@code {
    public class SalesData
    {
        public string Product { get; set; }
        public double Revenue { get; set; }
        public string TooltipText { get; set; }
    }

    public List<SalesData> FormattedData => GetFormattedData();

    private List<SalesData> GetFormattedData()
    {
        var rawData = GetRawSalesData();
        foreach (var item in rawData)
        {
            item.TooltipText = $"{item.Product}: {item.Revenue:C0}";
        }
        return rawData;
    }
}
```

### HTML in Format

The `Format` property supports HTML tags for rich formatting:

```razor
<AccumulationChartTooltipSettings 
    Format="<table style='width: 200px; border-collapse: collapse;'>
                <tr style='background: #f0f0f0;'>
                    <td style='padding: 5px; font-weight: bold;'>${point.x}</td>
                </tr>
                <tr>
                    <td style='padding: 5px;'>
                        <span style='color: green;'>●</span> 
                        Revenue: <b>$${point.y}</b>
                    </td>
                </tr>
                <tr>
                    <td style='padding: 5px; font-size: 12px; color: #666;'>
                        Market Share: ${point.percentage}%
                    </td>
                </tr>
            </table>"/>
```

**Supported HTML tags:**
- `<b>`, `<strong>`: Bold text
- `<i>`, `<em>`: Italic text
- `<br>`: Line break
- `<div>`, `<span>`: Containers for styling
- `<table>`, `<tr>`, `<td>`: Tables
- Inline `style` attributes for CSS

**Limitations:**
- No JavaScript or external CSS files
- Limited to inline styles
- No interactive elements (buttons, links won't work)
- Keep HTML simple for consistent rendering

## Appearance Customization

Customize tooltip visual appearance to match your application's design system.

### Background and Border

```razor
<AccumulationChartTooltipSettings 
    Enable="true"
    Fill="#1e3a8a"        <!-- Background color -->
    Opacity="0.9">        <!-- Transparency (0-1) -->
    <AccumulationChartTooltipBorder 
        Color="#fbbf24"   <!-- Border color -->
        Width="2"/>       <!-- Border width in pixels -->
</AccumulationChartTooltipSettings>
```

**Color options:**
- Named colors: `"red"`, `"blue"`, `"green"`
- Hex codes: `"#1e3a8a"`, `"#fbbf24"`
- RGB: `"rgb(30, 58, 138)"`
- RGBA: `"rgba(30, 58, 138, 0.9)"`

### Font Styling

```razor
<AccumulationChartTooltipSettings Enable="true">
    <AccumulationChartTooltipTextStyle 
        Color="#ffffff"
        Size="14px"
        FontWeight="600"
        FontFamily="'Segoe UI', Arial, sans-serif"
        FontStyle="Normal"/>
</AccumulationChartTooltipSettings>
```

**Typography properties:**

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| Color | string | Text color | Theme text color |
| Size | string | Font size with unit | "13px" |
| FontWeight | string | Weight (Normal, Bold, 600, etc.) | "Normal" |
| FontFamily | string | Font stack | Theme font |
| FontStyle | string | Normal, Italic, Oblique | "Normal" |

### Complete Styling Example

```razor
<AccumulationChartTooltipSettings 
    Enable="true"
    Fill="#2d3748"
    Opacity="0.95"
    Format="<div style='padding: 5px;'>
                <div style='font-size: 16px; font-weight: bold; margin-bottom: 5px;'>
                    ${point.x}
                </div>
                <div style='font-size: 14px;'>
                    Revenue: $${point.y}
                </div>
                <div style='font-size: 12px; opacity: 0.8; margin-top: 3px;'>
                    Share: ${point.percentage}%
                </div>
            </div>">
    <AccumulationChartTooltipBorder Color="#4299e1" Width="2"/>
    <AccumulationChartTooltipTextStyle 
        Color="#ffffff" 
        Size="14px" 
        FontWeight="400"
        FontFamily="'Inter', sans-serif"/>
</AccumulationChartTooltipSettings>
```

## Highlight Color

The `HighlightColor` property on the chart controls the color used to highlight segments when hovering:

```razor
<SfAccumulationChart 
    Title="Product Sales" 
    HighlightColor="#ff6b6b">
    <AccumulationChartTooltipSettings Enable="true"/>
    <!-- Series configuration -->
</SfAccumulationChart>
```

**Default behavior:**
- No highlight color applied
- Chart segments maintain original colors on hover

**With highlight color:**
- Hovered segment changes to specified color
- Creates visual feedback for user interaction
- Returns to original color when hover ends

**When to use highlight:**
- Interactive dashboards requiring clear visual feedback
- Charts where segment selection isn't obvious
- Applications with strong interactivity focus
- Accessibility enhancement (visual hover indication)

**Color selection guidelines:**
- Use colors that contrast with chart theme
- Avoid colors similar to existing data point colors
- Consider accessibility (sufficient contrast)
- Test with colorblind simulation tools

**Contrasting highlight example:**
```razor
<!-- Dark theme chart with light highlight -->
<SfAccumulationChart HighlightColor="#ffd700">

<!-- Light theme chart with dark highlight -->
<SfAccumulationChart HighlightColor="#4a5568">

<!-- Neutral highlight that works with most themes -->
<SfAccumulationChart HighlightColor="#cbd5e0">
```

## Tooltip Text Mapping

Use `TooltipMappingName` to display custom text from your data source:

```razor
<AccumulationChartSeries 
    DataSource="@ProductData" 
    XName="ProductName" 
    YName="Sales"
    TooltipMappingName="TooltipContent">
</AccumulationChartSeries>

<AccumulationChartTooltipSettings 
    Enable="true"
    Format="${point.tooltip}">
</AccumulationChartTooltipSettings>

@code {
    public class ProductData
    {
        public string ProductName { get; set; }
        public double Sales { get; set; }
        public string TooltipContent { get; set; }
    }

    public List<ProductData> ProductData = new List<ProductData>
    {
        new ProductData { 
            ProductName = "Laptop", 
            Sales = 125000,
            TooltipContent = "Laptop Sales: $125K (High Demand)" 
        },
        new ProductData { 
            ProductName = "Phone", 
            Sales = 98000,
            TooltipContent = "Phone Sales: $98K (Steady Growth)" 
        }
    };
}
```

**Use cases for text mapping:**
- Pre-formatted complex strings
- Localized content
- Conditional messaging based on values
- Including data not in the chart (e.g., trends, comparisons)

**Advanced example with conditional content:**
```csharp
private List<ProductData> GenerateTooltipData()
{
    var data = GetRawData();
    var totalSales = data.Sum(d => d.Sales);
    
    foreach (var item in data)
    {
        var percentage = (item.Sales / totalSales) * 100;
        var trend = item.Sales > 100000 ? "↑ Growing" : "→ Stable";
        var badge = item.Sales > 150000 ? "⭐ Top Seller" : "";
        
        item.TooltipContent = $@"
            <div style='padding: 5px;'>
                <div style='font-weight: bold; font-size: 15px;'>{item.ProductName} {badge}</div>
                <div style='margin: 5px 0;'>
                    Sales: <span style='color: #10b981; font-weight: 600;'>{item.Sales:C0}</span>
                </div>
                <div style='font-size: 12px; color: #6b7280;'>
                    Market Share: {percentage:F1}%
                </div>
                <div style='font-size: 11px; color: #4b5563; margin-top: 3px;'>
                    Trend: {trend}
                </div>
            </div>";
    }
    
    return data;
}
```

## Best Practices

**Do:**
- Enable tooltips for interactive charts
- Use clear, concise text in tooltips
- Include relevant context (units, percentages)
- Test tooltip positioning at chart edges
- Ensure color contrast for readability
- Provide meaningful headers for clarity

**Don't:**
- Overload tooltips with excessive information
- Use tiny fonts (< 11px)
- Forget to test on mobile/touch devices
- Use tooltips as primary information display
- Create tooltips wider than 300px (may overflow)
- Ignore accessibility considerations

**Performance tips:**
- Simple HTML renders faster than complex tables
- Avoid embedding images in tooltips
- Pre-format complex strings in data source
- Minimize inline styles (use CSS classes when possible)

**Accessibility considerations:**
- Tooltips may not be accessible to screen readers
- Consider providing alternative content (ARIA labels)
- Don't rely solely on tooltips for critical information
- Test keyboard navigation (ESC key should dismiss tooltip)

## Troubleshooting

**Tooltip not appearing:**
- Verify `Enable="true"` in AccumulationChartTooltipSettings
- Check if chart has valid data
- Ensure mouse events aren't being blocked by other elements
- Test in different browsers (browser compatibility)

**Tooltip text truncated:**
- Reduce text length or use line breaks (`<br>`)
- Increase tooltip width using custom HTML format
- Check container element doesn't constrain tooltip

**Tooltip positioning issues:**
- Chart positioned at edge of screen (tooltip may overflow)
- Parent container has `overflow: hidden`
- Zoom level affecting calculations
- Solution: Add padding around chart or adjust container

**Format placeholders not working:**
- Verify placeholder syntax: `${point.x}` not `{point.x}`
- Check data source has required fields
- Ensure TooltipMappingName matches actual field name
- Test with simple format first, then add complexity

**HTML not rendering:**
- Check for unclosed tags
- Verify quotes are properly escaped
- Use single quotes inside double-quoted attributes
- Test HTML separately before embedding in format

---

**Quick reference template:**
```razor
<SfAccumulationChart HighlightColor="#cbd5e0">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries 
            DataSource="@Data" 
            XName="Category" 
            YName="Value"
            TooltipMappingName="CustomTooltip">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartTooltipSettings 
        Enable="true"
        Header="Sales Data"
        Format="${point.x}: <b>${point.y}</b> (${point.percentage}%)"
        Fill="#2d3748"
        Opacity="0.95">
        <AccumulationChartTooltipBorder Color="#4299e1" Width="2"/>
        <AccumulationChartTooltipTextStyle 
            Color="#ffffff" 
            Size="14px" 
            FontWeight="Normal"/>
    </AccumulationChartTooltipSettings>
</SfAccumulationChart>
```
