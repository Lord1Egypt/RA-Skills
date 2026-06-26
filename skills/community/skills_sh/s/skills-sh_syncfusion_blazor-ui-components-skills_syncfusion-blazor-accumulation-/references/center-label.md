## Table of Contents

- [Overview](#overview)
- [Basic Implementation](#basic-implementation)
- [Text Content](#text-content)
   - [Single Line Text](#single-line-text)
   - [Multi-Line Text](#multi-line-text)
   - [Dynamic Content](#dynamic-content)
- [Hover Text Format](#hover-text-format)
   - [Available Placeholders](#available-placeholders)
   - [Advanced Hover Examples](#advanced-hover-examples)
   - [Interactive Example](#interactive-example)
- [Font Customization](#font-customization)
   - [Font Properties](#font-properties)
   - [Typography Best Practices](#typography-best-practices)
   - [Advanced Typography Example](#advanced-typography-example)
- [Position Adjustment](#position-adjustment)
   - [Offset Properties](#offset-properties)
   - [When to Use Offsets](#when-to-use-offsets)
   - [Offset Best Practices](#offset-best-practices)
- [Complete Example: Dashboard KPI](#complete-example-dashboard-kpi)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

# Center Label Reference for Syncfusion Blazor Accumulation Charts

## Overview

The center label feature displays custom text in the middle of pie and donut charts, transforming the hollow center into valuable real estate for displaying key metrics, titles, or dynamic information. This is particularly effective for donut charts where the center space would otherwise be empty, and for presenting aggregate statistics or contextual information.

**Key capabilities:**
- Display static titles, summaries, or branding
- Show dynamic text that changes on hover
- Customize font, color, and size
- Adjust position with X/Y offsets
- Support multi-line text with HTML breaks
- Integrate seamlessly with chart theme

**When to use center labels:**
- Donut charts (mandatory for effective use of center space)
- Displaying total values or aggregate statistics
- Chart titles or contextual headings
- Branding (company names, logos as text)
- Hover-driven dynamic information displays
- Key performance indicators (KPIs) in dashboards

**When to avoid center labels:**
- Pie charts (no center space available)
- When center space is needed for other UI elements
- Charts that will be exported as images (center label may obscure data)
- Very small donut charts (< 200px) where text won't fit

## Basic Implementation

Add center label using `AccumulationChartCenterLabel` with the `Text` property:

```razor
<SfAccumulationChart Title="Browser Market Share">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries 
            DataSource="@BrowserData" 
            XName="Browser" 
            YName="Users"
            InnerRadius="60%">  <!-- Donut chart -->
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartCenterLabel Text="Browser<br>Statistics 2024">
    </AccumulationChartCenterLabel>
    
    <AccumulationChartLegendSettings Visible="false"/>
</SfAccumulationChart>

@code {
    public class BrowserStats
    {
        public string Browser { get; set; }
        public double Users { get; set; }
    }

    public List<BrowserStats> BrowserData = new List<BrowserStats>
    {
        new BrowserStats { Browser = "Chrome", Users = 63.5 },
        new BrowserStats { Browser = "Safari", Users = 25.0 },
        new BrowserStats { Browser = "Edge", Users = 6.0 },
        new BrowserStats { Browser = "Firefox", Users = 3.0 },
        new BrowserStats { Browser = "Others", Users = 2.5 }
    };
}
```

**Key requirements:**
- Series must have `InnerRadius` > 0% (donut chart)
- Recommended `InnerRadius`: 40-70% for optimal space
- Use `<br>` tags for multi-line text

**Default appearance:**
- Text centered horizontally and vertically
- Font size: 14px
- Color: Theme text color
- Font weight: Normal
- No background or border

## Text Content

The `Text` property accepts plain text or HTML break tags for line breaks.

### Single Line Text

```razor
<AccumulationChartCenterLabel Text="Total Sales: $2.4M">
</AccumulationChartCenterLabel>
```

### Multi-Line Text

```razor
<AccumulationChartCenterLabel Text="Q4 2024<br>Revenue<br>$2.4M">
</AccumulationChartCenterLabel>
```

**Output:**
```
Q4 2024
Revenue
$2.4M
```

### Dynamic Content

Calculate and display dynamic text based on data:

```razor
<AccumulationChartCenterLabel Text="@CenterLabelText">
</AccumulationChartCenterLabel>

@code {
    private string CenterLabelText => $"Total<br>{TotalSales:C0}";
    
    private double TotalSales => SalesData?.Sum(s => s.Amount) ?? 0;
    
    public List<SalesData> SalesData = new List<SalesData>
    {
        new SalesData { Category = "A", Amount = 125000 },
        new SalesData { Category = "B", Amount = 98000 },
        new SalesData { Category = "C", Amount = 87000 }
    };
}
```

**Best practices for text content:**
- Keep text concise (< 30 characters per line)
- Use 2-3 lines maximum for readability
- Center-align multi-line text visually
- Consider text length at various chart sizes
- Test with longest expected text

## Hover Text Format

Display dynamic text when hovering over chart segments using `HoverTextFormat`:

```razor
<AccumulationChartCenterLabel 
    Text="Browser<br>Statistics" 
    HoverTextFormat="${point.x}<br>Users: ${point.y}%">
</AccumulationChartCenterLabel>
```

**Behavior:**
- Default `Text` shown when not hovering
- On segment hover, center label changes to `HoverTextFormat`
- Returns to default `Text` when hover ends
- Smooth transition between states

### Available Placeholders

```razor
<AccumulationChartCenterLabel 
    HoverTextFormat="${point.x}<br>${point.y}%<br>(${point.percentage}% share)">
</AccumulationChartCenterLabel>
```

**Placeholder reference:**

| Placeholder | Description | Example |
|-------------|-------------|---------|
| ${point.x} | Category/label value | "Chrome" |
| ${point.y} | Numeric value | 63.5 |
| ${point.percentage} | Percentage of total | 45.2 |
| ${point.text} | Point text property | "Top Browser" |

### Advanced Hover Examples

**KPI Dashboard:**
```razor
<AccumulationChartCenterLabel 
    Text="Department<br>Expenses<br>2024"
    HoverTextFormat="${point.x}<br><b>${point.y:C0}</b><br>${point.percentage:F1}% of total">
</AccumulationChartCenterLabel>
```

**Conditional formatting:**
```razor
@code {
    private string GetHoverFormat(double value)
    {
        if (value > 50)
            return "${point.x}<br><b style='color: green;'>${point.y}%</b><br>High Usage";
        else
            return "${point.x}<br><b style='color: orange;'>${point.y}%</b><br>Moderate Usage";
    }
}
```

**Note:** HTML inline styles are supported in `HoverTextFormat` for rich formatting.

### Interactive Example

```razor
<SfAccumulationChart Title="Sales by Region">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries 
            DataSource="@RegionSales" 
            XName="Region" 
            YName="Sales"
            InnerRadius="65%">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartCenterLabel 
        Text="2024 Sales<br><small>Hover for details</small>"
        HoverTextFormat="${point.x}<br><b>$${point.y}K</b><br>Market Share: ${point.percentage}%">
        <AccumulationChartCenterLabelFont Size="16px" FontWeight="600"/>
    </AccumulationChartCenterLabel>
</SfAccumulationChart>

@code {
    public List<RegionalSales> RegionSales = new List<RegionalSales>
    {
        new RegionalSales { Region = "North", Sales = 450 },
        new RegionalSales { Region = "South", Sales = 380 },
        new RegionalSales { Region = "East", Sales = 290 },
        new RegionalSales { Region = "West", Sales = 520 }
    };
}
```

**Hover interaction flow:**
1. Chart displays with default text: "2024 Sales / Hover for details"
2. User hovers over "North" segment
3. Center label changes to: "North / $450K / Market Share: 27.1%"
4. User moves to "South" segment
5. Center label updates to: "South / $380K / Market Share: 22.9%"
6. User moves mouse away
7. Center label returns to: "2024 Sales / Hover for details"

## Font Customization

Customize center label typography using `AccumulationChartCenterLabelFont`:

```razor
<AccumulationChartCenterLabel Text="Total Revenue<br>$2.4M">
    <AccumulationChartCenterLabelFont 
        Size="18px"
        FontWeight="700"
        FontFamily="'Segoe UI', Arial, sans-serif"
        FontStyle="Normal"
        Color="#2563eb"/>
</AccumulationChartCenterLabel>
```

### Font Properties

| Property | Type | Description | Default | Example Values |
|----------|------|-------------|---------|----------------|
| Size | string | Font size with unit | "14px" | "16px", "1.2rem", "14pt" |
| FontWeight | string | Text weight | "Normal" | "Normal", "Bold", "600", "700" |
| FontFamily | string | Font stack | Theme font | "'Inter', sans-serif" |
| FontStyle | string | Style variant | "Normal" | "Normal", "Italic", "Oblique" |
| Color | string | Text color | Theme color | "#2563eb", "rgb(37, 99, 235)" |

### Typography Best Practices

**Size selection:**
- Small charts (< 300px): 12-14px
- Medium charts (300-500px): 14-18px
- Large charts (> 500px): 18-24px
- Multi-line: Use consistent or decreasing sizes

```razor
<!-- Primary line larger, secondary smaller -->
<AccumulationChartCenterLabel>
    <AccumulationChartCenterLabelFont Size="20px" FontWeight="700"/>
    <!-- Add secondary line with smaller font via CSS -->
</AccumulationChartCenterLabel>
```

**Font weight:**
- 400 (Normal): Body text, general information
- 600 (Semi-bold): Emphasis, key metrics
- 700 (Bold): Primary values, headings
- 800-900: Rare, for extreme emphasis

**Color selection:**
- High contrast for readability (WCAG AA minimum)
- Consider chart segment colors (avoid clashes)
- Use theme colors for consistency
- Test against different backgrounds

**Accessible color combinations:**
```razor
<!-- Light theme -->
<AccumulationChartCenterLabelFont Color="#1e293b" Size="16px"/>

<!-- Dark theme -->
<AccumulationChartCenterLabelFont Color="#f1f5f9" Size="16px"/>

<!-- Brand color with sufficient contrast -->
<AccumulationChartCenterLabelFont Color="#0369a1" Size="16px" FontWeight="600"/>
```

### Advanced Typography Example

```razor
<AccumulationChartCenterLabel Text="FY 2024<br><span style='font-size: 28px; font-weight: 800; color: #059669;'>$4.2M</span><br><span style='font-size: 14px; color: #6b7280;'>+18% YoY</span>">
    <AccumulationChartCenterLabelFont 
        Size="16px" 
        FontWeight="600"
        FontFamily="'Inter', system-ui, sans-serif"
        Color="#111827"/>
</AccumulationChartCenterLabel>
```

**Note:** While base font properties apply to the entire center label, you can use inline styles within the `Text` for varied formatting of different lines.

## Position Adjustment

Fine-tune center label position using `XOffset` and `YOffset` properties:

```razor
<AccumulationChartCenterLabel 
    Text="Centered Text"
    XOffset="10"      <!-- Shift right 10 pixels -->
    YOffset="-5">     <!-- Shift up 5 pixels -->
</AccumulationChartCenterLabel>
```

### Offset Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| XOffset | double | Horizontal shift (positive = right, negative = left) | 0 |
| YOffset | double | Vertical shift (positive = down, negative = up) | 0 |

### When to Use Offsets

**Visual alignment corrections:**
```razor
<!-- Multi-line text appears slightly high, shift down -->
<AccumulationChartCenterLabel 
    Text="Line 1<br>Line 2<br>Line 3"
    YOffset="5">
</AccumulationChartCenterLabel>
```

**Asymmetric chart designs:**
```razor
<!-- Chart has legend on right, shift label left for balance -->
<AccumulationChartCenterLabel 
    Text="Sales Data"
    XOffset="-15">
</AccumulationChartCenterLabel>
```

**Precise alignment with other elements:**
```razor
<!-- Align with specific chart feature -->
<AccumulationChartCenterLabel 
    Text="Q4 Results"
    XOffset="8"
    YOffset="-3">
</AccumulationChartCenterLabel>
```

### Offset Best Practices

**Do:**
- Use small adjustments (± 5-15 pixels)
- Test at different chart sizes
- Consider responsive behavior
- Document reasons for non-zero offsets

**Don't:**
- Use large offsets (> 30 pixels) - indicates design issue
- Rely on offsets for initial positioning (use InnerRadius instead)
- Forget to test with different data/text lengths
- Use offsets to work around layout problems

**Troubleshooting alignment:**
1. Check if `InnerRadius` is appropriate for text size
2. Verify text isn't too long (causing overflow)
3. Test with different font sizes
4. Ensure chart container isn't constraining layout
5. Use browser dev tools to inspect actual position

## Complete Example: Dashboard KPI

```razor
<SfAccumulationChart 
    Title="Department Budget Allocation"
    Width="500px" 
    Height="500px"
    Theme="Syncfusion.Blazor.Theme.Bootstrap5">
    
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries 
            DataSource="@BudgetData" 
            XName="Department" 
            YName="Budget"
            InnerRadius="65%"
            ExplodeIndex="0"
            ExplodeOffset="10%">
            <AccumulationDataLabelSettings 
                Visible="true" 
                Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside"
                Name="Label">
                <AccumulationChartConnector Type="Syncfusion.Blazor.Charts.ConnectorType.Curve" Length="20px"/>
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartCenterLabel 
        Text="Total Budget<br><b style='font-size: 32px; color: #059669;'>$@TotalBudget.ToString("N0")</b><br><small style='color: #6b7280;'>FY 2024</small>"
        HoverTextFormat="${point.x}<br><b style='font-size: 24px; color: #2563eb;'>$${point.y}K</b><br>${point.percentage}% of budget"
        YOffset="-5">
        <AccumulationChartCenterLabelFont 
            Size="18px" 
            FontWeight="600"
            FontFamily="'Inter', sans-serif"
            Color="#111827"/>
    </AccumulationChartCenterLabel>
    
    <AccumulationChartLegendSettings 
        Visible="true" 
        Position="Syncfusion.Blazor.Charts.LegendPosition.Bottom"/>
    
    <AccumulationChartTooltipSettings Enable="true"/>
</SfAccumulationChart>

@code {
    public class BudgetAllocation
    {
        public string Department { get; set; }
        public double Budget { get; set; }
        public string Label { get; set; }
    }

    public List<BudgetAllocation> BudgetData = new List<BudgetAllocation>
    {
        new BudgetAllocation { Department = "Engineering", Budget = 450, Label = "Engineering: $450K" },
        new BudgetAllocation { Department = "Sales", Budget = 380, Label = "Sales: $380K" },
        new BudgetAllocation { Department = "Marketing", Budget = 290, Label = "Marketing: $290K" },
        new BudgetAllocation { Department = "Operations", Budget = 180, Label = "Operations: $180K" },
        new BudgetAllocation { Department = "Support", Budget = 120, Label = "Support: $120K" }
    };

    private double TotalBudget => BudgetData.Sum(b => b.Budget);
}
```

**Features demonstrated:**
- Dynamic total calculation in center
- Hover text with formatted values
- Multi-line text with varied styling
- Professional typography
- Integrated with legend and tooltips
- Responsive design considerations

## Best Practices

**Content:**
- Keep text concise (3 lines maximum)
- Use line breaks strategically for hierarchy
- Show aggregate or contextual information
- Update dynamically based on data changes
- Consider text length at minimum chart size

**Design:**
- Ensure sufficient contrast (WCAG AA: 4.5:1 minimum)
- Use font sizes appropriate for chart size
- Match typography to application design system
- Test with actual data (not just placeholder text)
- Consider internationalization (text length varies)

**Interactivity:**
- Use hover text for detailed information
- Provide clear indication that hover changes text
- Ensure hover text is meaningful, not redundant
- Test hover behavior on touch devices
- Don't rely solely on hover for critical info

**Performance:**
- Avoid frequent text updates (debounce if dynamic)
- Use simple HTML formatting (complex DOM is slower)
- Pre-calculate derived values in data preparation
- Test with large datasets

## Troubleshooting

**Text not visible:**
- Verify `InnerRadius` > 40% (sufficient center space)
- Check text color contrasts with background
- Ensure font size isn't too small or too large
- Verify chart dimensions accommodate text

**Text truncated:**
- Reduce text length or font size
- Increase chart size or `InnerRadius`
- Break long lines with `<br>` tags
- Use abbreviations for long words

**Text position incorrect:**
- Check if parent container constrains chart
- Verify XOffset/YOffset values are reasonable
- Test with different chart sizes
- Ensure chart has rendered before adjusting

**Hover text not updating:**
- Verify `HoverTextFormat` property is set
- Check data binding is correct
- Ensure chart has interactive mode enabled
- Test mouse events aren't blocked

**Alignment issues:**
- Use small YOffset adjustments (± 5-10px)
- Check if multi-line text needs centering adjustment
- Verify font-size units are consistent
- Test across different browsers

---

**Quick reference:**
```razor
<AccumulationChartCenterLabel 
    Text="Default Text<br>Line 2"
    HoverTextFormat="${point.x}<br>${point.y}"
    XOffset="0"
    YOffset="0">
    <AccumulationChartCenterLabelFont 
        Size="16px"
        FontWeight="600"
        FontFamily="'Inter', sans-serif"
        FontStyle="Normal"
        Color="#111827"/>
</AccumulationChartCenterLabel>
```
