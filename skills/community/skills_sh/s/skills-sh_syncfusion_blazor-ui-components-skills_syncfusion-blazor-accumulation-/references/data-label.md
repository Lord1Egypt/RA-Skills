# Data Label Reference for Syncfusion Blazor Accumulation Charts

## Table of Contents

- [Overview](#overview)
- [Basic Implementation](#basic-implementation)
- [Text Wrapping](#text-wrapping)
   - [When to Use Text Wrapping](#when-to-use-text-wrapping)
   - [Implementation Details](#implementation-details)
- [Label Positioning](#label-positioning)
   - [Inside Position](#inside-position)
   - [Outside Position](#outside-position)
   - [Position Selection Guidelines](#position-selection-guidelines)
- [Smart Labels](#smart-labels)
   - [Understanding Smart Labels](#understanding-smart-labels)
   - [Configuration](#configuration)
   - [Best Practices](#best-practices)
- [Connector Lines](#connector-lines)
   - [Connector Types](#connector-types)
   - [Customization Options](#customization-options)
   - [Troubleshooting Connector Lines](#troubleshooting-connector-lines)
- [Text Mapping](#text-mapping)
   - [Basic Mapping](#basic-mapping)
   - [Advanced Scenarios](#advanced-scenarios)
- [Formatting](#formatting)
   - [Standard Format Strings](#standard-format-strings)
   - [Custom Formatting](#custom-formatting)
- [Templates](#templates)
   - [Template Context](#template-context)
   - [Creating Custom Templates](#creating-custom-templates)
   - [Advanced Template Examples](#advanced-template-examples)
- [Troubleshooting](#troubleshooting)
   - [Labels Not Visible](#labels-not-visible)
   - [Labels Overlap](#labels-overlap)
   - [Text Truncated](#text-truncated)
   - [Format Not Applied](#format-not-applied)
- [Performance Considerations](#performance-considerations)


## Overview

Data labels are text annotations that display information about data points in accumulation charts (Pie, Doughnut, Funnel, Pyramid). They enhance data visualization by showing values, percentages, or custom text directly on the chart, eliminating the need for users to hover or inspect tooltips.

**Key capabilities:**
- Display point values, labels, or custom text
- Position labels inside or outside chart segments
- Prevent label overlap with smart label positioning
- Connect outside labels to their segments with connector lines
- Format numeric values with standard or custom patterns
- Create rich, interactive labels using templates

**When to use data labels:**
- Charts require immediate visibility of values without user interaction
- Presentations or dashboards where data must be readable at a glance
- Reports where precise values need to be displayed alongside visual representation
- Educational materials or infographics requiring clear data annotation

## Basic Implementation

Enable data labels by setting the `Visible` property to `true` in `AccumulationDataLabelSettings`:

```razor
<SfAccumulationChart Title="Sales by Category">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@SalesData" 
                                 XName="Category" 
                                 YName="Amount">
            <AccumulationDataLabelSettings Visible="true" Name="Category">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    public class SalesRecord
    {
        public string Category { get; set; }
        public double Amount { get; set; }
    }

    public List<SalesRecord> SalesData = new List<SalesRecord>
    {
        new SalesRecord { Category = "Electronics", Amount = 45000 },
        new SalesRecord { Category = "Clothing", Amount = 28000 },
        new SalesRecord { Category = "Food", Amount = 35000 },
        new SalesRecord { Category = "Books", Amount = 12000 }
    };
}
```

**Key properties:**
- `Visible` (bool): Enables/disables data label rendering
- `Name` (string): Maps to data source field for label text

**Default behavior:**
- Labels display the Y-value from data points
- Labels appear inside chart segments
- No text wrapping applied
- Font inherits from theme settings

## Text Wrapping

Text wrapping allows long label text to break into multiple lines when exceeding a specified width, preventing truncation and improving readability.

### When to Use Text Wrapping

**Use text wrapping when:**
- Labels contain long category names or descriptions
- Chart space is limited and labels would otherwise overlap
- Multi-line labels provide better readability than abbreviated text
- Working with pie/doughnut charts with many small slices

**Avoid text wrapping when:**
- Labels are already short (< 15 characters)
- Chart has ample space for full-width labels
- Performance is critical (wrapping adds rendering overhead)
- Consistent single-line appearance is required for design

### Implementation Details

```razor
<AccumulationDataLabelSettings 
    Visible="true" 
    Name="Description"
    TextWrap="Syncfusion.Blazor.TextWrap.Wrap"
    MaxWidth="100"
    Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
    <AccumulationChartConnector Type="Syncfusion.Blazor.Charts.ConnectorType.Line" Length="5%"/>
</AccumulationDataLabelSettings>

@code {
    public class ProductData
    {
        public string Product { get; set; }
        public double Sales { get; set; }
        public string Description { get; set; }
    }

    public List<ProductData> Products = new List<ProductData>
    {
        new ProductData { 
            Product = "A", 
            Sales = 120, 
            Description = "Premium Wireless Headphones with Noise Cancellation" 
        },
        new ProductData { 
            Product = "B", 
            Sales = 95, 
            Description = "Ergonomic Office Chair with Lumbar Support" 
        }
    };
}
```

**Configuration properties:**

- `TextWrap`: Enum value (`Syncfusion.Blazor.TextWrap.Wrap`, `Syncfusion.Blazor.TextWrap.Normal`, `Syncfusion.Blazor.TextWrap.AnyWhere`)
  - `Wrap`: Breaks text at MaxWidth boundary
  - `Normal`: No wrapping, text may overflow or truncate
  - `AnyWhere`: Break a word at any point if there are no otherwise-acceptable break points in the line
- `MaxWidth`: Maximum width in pixels before wrapping (default: no limit)

**Best practices:**
- Set MaxWidth to 80-120 pixels for optimal readability
- Use Outside position with text wrapping to avoid cluttering chart interior
- Test with longest expected label text to ensure proper layout
- Consider enabling smart labels when using text wrapping

## Label Positioning

Data label position determines whether labels appear inside chart segments or outside with connecting lines.

### Inside Position

Labels render within the boundaries of their corresponding chart segment.

```razor
<AccumulationDataLabelSettings 
    Visible="true" 
    Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Inside"
    Name="Category">
    <AccumulationDataLabelFont Color="White" Size="14px"/>
</AccumulationDataLabelSettings>
```

**Characteristics:**
- Compact appearance, no connector lines needed
- Works well for larger segments
- May be difficult to read on small slices or low-contrast backgrounds

**When to use:**
- Large pie/doughnut slices where labels fit comfortably
- High-contrast color schemes (light text on dark slices)
- Space-constrained layouts where outside labels would overlap
- Simple charts with few data points

### Outside Position

Labels render outside chart boundaries with connector lines pointing to segments.

```razor
<AccumulationDataLabelSettings 
    Visible="true" 
    Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside"
    Name="Category">
    <AccumulationChartConnector
        Type="Syncfusion.Blazor.Charts.ConnectorType.Curve"
        Length="20px"
        Color="#666666"
        Width="1"/>
</AccumulationDataLabelSettings>
```

**Characteristics:**
- Labels never overlap chart segments
- Requires more space around chart
- Connector lines visually link labels to slices
- Better readability for complex data

**When to use:**
- Charts with many small slices
- Long label text that won't fit inside segments
- Professional dashboards requiring clear separation
- Charts where background colors vary significantly

### Position Selection Guidelines

| Scenario | Recommended Position | Rationale |
|----------|---------------------|-----------|
| 3-5 large slices | Inside | Ample space, cleaner look |
| 6-10 mixed slices | Outside | Prevents overlap on small slices |
| 10+ slices | Outside + Smart Labels | Necessary for readability |
| Short labels (< 10 chars) | Inside or Outside | Either works well |
| Long labels (> 20 chars) | Outside + TextWrap | Requires additional space |
| Presentation/Print | Outside | Professional appearance |
| Interactive dashboard | Inside | Maximizes chart visibility |

## Smart Labels

Smart labels automatically adjust label positions to prevent overlapping, ensuring all labels remain readable without manual intervention.

### Understanding Smart Labels

Smart label algorithm:
1. Calculates optimal position for each label based on segment size and angle
2. Detects potential overlaps between adjacent labels
3. Shifts overlapping labels vertically or radially
4. Maintains connector line connections to original segments
5. Falls back to hiding labels if space is insufficient (rare)

**Visual behavior:**
- Labels that would overlap are shifted to nearby empty space
- Connector lines adjust to maintain connections
- Priority given to larger segments (displayed first)
- Smaller segments may have labels repositioned further

### Configuration

Enable at chart level (applies to all series):

```razor
<SfAccumulationChart EnableSmartLabels="true" Title="Market Share Analysis">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@MarketData" 
                                 XName="Company" 
                                 YName="Share">
            <AccumulationDataLabelSettings 
                Visible="true" 
                Name="Company"
                Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
                <AccumulationChartConnector
                    Type="Syncfusion.Blazor.Charts.ConnectorType.Curve"
                    Length="20px"/>
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    public List<MarketShareData> MarketData = new List<MarketShareData>
    {
        new MarketShareData { Company = "Company A", Share = 28.5 },
        new MarketShareData { Company = "Company B", Share = 22.3 },
        new MarketShareData { Company = "Company C", Share = 15.7 },
        new MarketShareData { Company = "Company D", Share = 12.1 },
        new MarketShareData { Company = "Company E", Share = 8.9 },
        new MarketShareData { Company = "Others", Share = 12.5 }
    };
}
```

### Best Practices

**Do:**
- Always enable smart labels for charts with > 6 data points
- Use Outside position with smart labels for best results
- Combine with curved connectors for professional appearance
- Test with maximum expected data point count
- Allow sufficient space around chart (20-30% padding)

**Don't:**
- Use smart labels with Inside position (no effect)
- Expect smart labels to work miracles with 20+ tiny slices
- Forget to test with long label text
- Ignore warning when labels still overlap (increase chart size)

**Performance note:** Smart label calculation adds 10-20ms to initial render. Negligible for most applications but consider disabling for real-time charts updating > 10 times per second.

## Connector Lines

Connector lines visually link outside-positioned labels to their corresponding chart segments. They are automatically shown when `Position="Outside"` and hidden for inside labels.

### Connector Types

**Line (Straight):**
```razor
<AccumulationChartConnector Type="Syncfusion.Blazor.Charts.ConnectorType.Line" Length="30px"/>
```
- Direct straight line from slice edge to label
- Clean, minimalist appearance
- Best for: Technical documents, dense charts

**Curve (Bezier):**
```razor
<AccumulationChartConnector Type="Syncfusion.Blazor.Charts.ConnectorType.Curve" Length="30px"/>
```
- Smooth curved line from slice to label
- Modern, professional appearance
- Best for: Presentations, marketing materials, executive dashboards

### Customization Options

```razor
<AccumulationChartConnector
    Type="Syncfusion.Blazor.Charts.ConnectorType.Curve"
    Length="50px"           <!-- Distance from slice edge to label -->
    Width="2"               <!-- Line thickness in pixels -->
    Color="#ff6384"         <!-- Custom color (overrides theme) -->
    DashArray="5,3"/>       <!-- Dashed line pattern: 5px dash, 3px gap -->
```

**Property details:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| Type | ConnectorType | Line | Line or Curve |
| Length | string | "4%" | Distance from slice to label (px or %) |
| Width | double | 1 | Line thickness in pixels |
| Color | string | (theme) | CSS color value |
| DashArray | string | null | SVG dash pattern (e.g., "5,3") |

**Length guidelines:**
- Use percentage (e.g., "5%") for responsive designs
- Use pixels (e.g., "40px") for fixed layouts
- Typical range: 20-60px or 3-8%
- Longer connectors needed for charts with many slices

### Troubleshooting Connector Lines

**Problem: Connectors not visible**
- Verify `Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside"`
- Check connector color contrasts with background
- Ensure `Visible="true"` in AccumulationDataLabelSettings

**Problem: Connectors overlap**
- Enable `EnableSmartLabels="true"` on chart
- Increase connector length for more spacing
- Consider reducing number of data points or using grouping

**Problem: Connectors point to wrong slices**
- Usually caused by animation interruption; call `Refresh()` method
- Verify data source hasn't changed during render
- Check for duplicate X-axis values in data

**Problem: Dashed lines not showing**
- Ensure Width > 1 for visibility
- Use format "dashLength,gapLength" (e.g., "5,3")
- Some browsers require explicit Width property

## Text Mapping

Text mapping displays custom text from a data source field instead of default Y-values or axis labels.

### Basic Mapping

```razor
<AccumulationDataLabelSettings 
    Visible="true" 
    Name="DisplayText">  <!-- Maps to data field -->
</AccumulationDataLabelSettings>

@code {
    public class SalesData
    {
        public string Product { get; set; }
        public double Revenue { get; set; }
        public string DisplayText { get; set; }  // Custom label text
    }

    public List<SalesData> Sales = new List<SalesData>
    {
        new SalesData { 
            Product = "Laptop", 
            Revenue = 45000, 
            DisplayText = "Laptops: $45K (32%)" 
        },
        new SalesData { 
            Product = "Phone", 
            Revenue = 38000, 
            DisplayText = "Phones: $38K (27%)" 
        }
    };
}
```

**How it works:**
- `Name` property references data source field name
- Chart reads value from specified field for each point
- If field is null/empty, falls back to Y-value
- Supports any string content (text, numbers, special characters)

### Advanced Scenarios

**Scenario 1: Conditional text based on value**

```csharp
public List<SalesData> Sales = new List<SalesData>
{
    new SalesData { 
        Product = "A", 
        Revenue = 120000, 
        DisplayText = GenerateLabel("A", 120000, 0.35) 
    }
};

private string GenerateLabel(string product, double revenue, double percentage)
{
    if (revenue > 100000)
        return $"{product}: ${revenue/1000}K ⭐"; // Star for high performers
    else
        return $"{product}: ${revenue/1000}K";
}
```

**Scenario 2: Localized labels**

```csharp
public string CurrentCulture { get; set; } = "en-US";

public List<SalesData> Sales => GetLocalizedData();

private List<SalesData> GetLocalizedData()
{
    var data = GetRawData();
    foreach (var item in data)
    {
        item.DisplayText = CurrentCulture switch
        {
            "fr-FR" => $"{item.Product}: {item.Revenue}€",
            "de-DE" => $"{item.Product}: {item.Revenue}€",
            _ => $"{item.Product}: ${item.Revenue}"
        };
    }
    return data;
}
```

**Scenario 3: Multi-line labels**

```csharp
new SalesData { 
    DisplayText = "Q4 Results\n$125,000\n+15% YoY" 
}
```

Note: Multi-line text requires `TextWrap="TextWrap.Wrap"` and appropriate `MaxWidth`.

## Formatting

### Standard Format Strings

Apply .NET standard format strings to numeric Y-values:

```razor
<AccumulationDataLabelSettings 
    Visible="true" 
    Format="C1"  <!-- Currency, 1 decimal place -->
    Position="AccumulationLabelPosition.Inside"/>
```

**Common format specifiers:**

| Format | Description | Example Input | Example Output |
|--------|-------------|---------------|----------------|
| N0 | Number, no decimals | 1234567.89 | 1,234,568 |
| N2 | Number, 2 decimals | 1234.567 | 1,234.57 |
| C0 | Currency, no decimals | 1234.56 | $1,235 |
| C2 | Currency, 2 decimals | 1234.56 | $1,234.56 |
| P0 | Percentage, no decimals | 0.8567 | 86% |
| P1 | Percentage, 1 decimal | 0.8567 | 85.7% |
| F2 | Fixed-point, 2 decimals | 1234.5678 | 1234.57 |

**Using format strings:**

```razor
<!-- Currency formatting -->
<AccumulationDataLabelSettings Format="C0"/>
<!-- Output: $45,000 -->

<!-- Percentage formatting -->
<AccumulationDataLabelSettings Format="P1"/>
<!-- Output: 32.5% -->

<!-- Custom numeric precision -->
<AccumulationDataLabelSettings Format="N2"/>
<!-- Output: 45,000.00 -->
```

### Custom Formatting

**Combining text and format:**

While the `Format` property applies .NET standard formats, custom text patterns are not directly supported. Instead, use text mapping:

```csharp
public List<SalesData> Sales = new List<SalesData>
{
    new SalesData { 
        Product = "Laptop", 
        Revenue = 45000, 
        DisplayText = $"Laptops: {45000:C0} (32%)" 
    }
};
```

```razor
<AccumulationDataLabelSettings Visible="true" Name="DisplayText"/>
```

**Culture-specific formatting:**

```razor
@using System.Globalization

<AccumulationDataLabelSettings 
    Visible="true" 
    Format="C2"/>  <!-- Uses current thread culture -->

@code {
    protected override void OnInitialized()
    {
        // Set culture for formatting
        CultureInfo.CurrentCulture = new CultureInfo("fr-FR");
        // Output: 45 000,00 €
    }
}
```

**When format doesn't apply:**
- If `Name` property maps to a text field, `Format` is ignored
- Format only applies to numeric Y-values
- For custom patterns, pre-format in data source

## Templates

Templates enable complete customization of data label appearance using Razor markup, HTML, and CSS.

### Template Context

Access data point information via the `AccumulationChartDataPointInfo` context:

```razor
<AccumulationDataLabelSettings Visible="true" Position="AccumulationLabelPosition.Outside">
    <Template>
        @{
            var data = context as AccumulationChartDataPointInfo;
            <!-- data.X: Category/Label value -->
            <!-- data.Y: Numeric value -->
            <!-- data.Percentage: Slice percentage -->
            <!-- data.Text: Default label text -->
            <!-- data.PointIndex: Index in series -->
            <!-- data.SeriesName: Series name -->
        }
    </Template>
</AccumulationDataLabelSettings>
```

**Available properties:**

| Property | Type | Description | Example Value |
|----------|------|-------------|---------------|
| X | object | X-axis value (category) | "Electronics" |
| Y | double | Y-axis value (numeric) | 45000 |
| Percentage | double | Slice percentage | 32.5 |
| Text | string | Default label text | "Electronics" |
| PointIndex | int | Point index in series | 0 |
| SeriesName | string | Series name | "Sales 2024" |

### Creating Custom Templates

**Basic HTML template:**

```razor
<Template>
    @{
        var data = context as AccumulationChartDataPointInfo;
    }
    <div style="background: linear-gradient(to right, #4facfe, #00f2fe); 
                padding: 8px 12px; 
                border-radius: 5px; 
                color: white;
                font-weight: bold;">
        @data.X: @data.Y.ToString("N0")
    </div>
</Template>
```

**Table-based layout:**

```razor
<Template>
    @{
        var data = context as AccumulationChartDataPointInfo;
    }
    <table style="border: 2px solid #333; background: white; padding: 5px;">
        <tr>
            <td style="font-weight: bold; color: #e74c3c; padding: 3px;">
                @data.X
            </td>
        </tr>
        <tr>
            <td style="font-size: 18px; color: #27ae60; padding: 3px;">
                @data.Y.ToString("C0")
            </td>
        </tr>
        <tr>
            <td style="font-size: 12px; color: #7f8c8d;">
                @data.Percentage.ToString("F1")%
            </td>
        </tr>
    </table>
</Template>
```

### Advanced Template Examples

**Conditional styling:**

```razor
<Template>
    @{
        var data = context as AccumulationChartDataPointInfo;
        var bgColor = data.Y > 50000 ? "#27ae60" : "#e74c3c";
        var icon = data.Y > 50000 ? "▲" : "▼";
    }
    <div style="background: @bgColor; 
                padding: 10px; 
                border-radius: 8px; 
                color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
        <div style="font-size: 20px;">@icon</div>
        <div style="font-weight: bold;">@data.X</div>
        <div style="font-size: 18px;">@data.Y.ToString("C0")</div>
        <div style="font-size: 12px; opacity: 0.9;">@data.Percentage.ToString("F1")%</div>
    </div>
</Template>
```

**Image + text:**

```razor
<Template>
    @{
        var data = context as AccumulationChartDataPointInfo;
        var imagePath = GetImagePath(data.X.ToString());
    }
    <div style="display: flex; align-items: center; gap: 8px; 
                background: white; padding: 6px 10px; 
                border: 1px solid #ddd; border-radius: 5px;">
        <img src="@imagePath" style="width: 24px; height: 24px;" />
        <div>
            <div style="font-weight: bold;">@data.X</div>
            <div style="color: #666;">@data.Y.ToString("N0") units</div>
        </div>
    </div>
</Template>

@code {
    private string GetImagePath(string category)
    {
        return $"/images/icons/{category.ToLower()}.png";
    }
}
```

**Performance tip:** Keep templates lightweight. Complex DOM structures or heavy CSS can impact rendering performance with 20+ data points.

## Troubleshooting

### Labels Not Visible

**Possible causes:**
1. `Visible="false"` in AccumulationDataLabelSettings
2. Label color matches background (check contrast)
3. Font size set to 0 or very small
4. Chart size too small to render labels
5. Data source is empty or null

**Solutions:**
```razor
<!-- Verify visibility -->
<AccumulationDataLabelSettings Visible="true">
    <!-- Check color contrast -->
    <AccumulationDataLabelFont Color="Black" Size="14px"/>
</AccumulationDataLabelSettings>

<!-- Ensure chart size -->
<SfAccumulationChart Width="600px" Height="400px" />
```

### Labels Overlap

**Solutions:**
```razor
<!-- Enable smart labels -->
<SfAccumulationChart EnableSmartLabels="true">

<!-- Use outside position -->
<AccumulationDataLabelSettings Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
    <AccumulationChartConnector Length="30px"/>
</AccumulationDataLabelSettings>

<!-- Reduce data points (use grouping) -->
<AccumulationChartSeries GroupTo="5" />
```

### Text Truncated

**Solutions:**
```razor
<!-- Enable text wrapping -->
<AccumulationDataLabelSettings 
    TextWrap="Syncfusion.Blazor.Charts.TextWrap.Wrap" 
    MaxWidth="120"/>

<!-- Abbreviate text in data source -->
DisplayText = category.Length > 15 ? category.Substring(0, 12) + "..." : category

<!-- Use template for custom layout -->
<Template>
    <div style="max-width: 150px; overflow: hidden; text-overflow: ellipsis;">
        @((context as AccumulationChartDataPointInfo).X)
    </div>
</Template>
```

### Format Not Applied

**Check:**
1. Format only works on numeric Y-values, not text fields
2. If using `Name` to map text field, format is ignored
3. Verify format string syntax (e.g., "C2" not "C-2")

```razor
<!-- Correct: Format applied to Y-value -->
<AccumulationDataLabelSettings Format="C0" />

<!-- Incorrect: Name maps to text, format ignored -->
<AccumulationDataLabelSettings Name="CustomText" Format="C0" />
```

## Performance Considerations

**Rendering performance:**
- Data labels add 15-30% to initial chart render time
- Smart labels add additional 10-20ms processing
- Templates with complex HTML increase render time proportionally
- Test with maximum expected data point count

**Optimization strategies:**
1. **Limit data points:** Use grouping for charts with > 15 slices
2. **Simplify templates:** Avoid nested tables, excessive CSS
3. **Disable smart labels** if not needed (< 6 points)
4. **Pre-format text** in data source rather than using templates
5. **Use text mapping** instead of templates when possible

**Memory usage:**
- Each label retains reference to context data
- Templates create additional DOM nodes
- Consider lazy loading for dashboards with multiple charts

**External resources:**
- [Syncfusion Blazor Accumulation Chart API](https://help.syncfusion.com/cr/blazor/Syncfusion.Blazor.Charts.SfAccumulationChart.html)
- [AccumulationDataLabelSettings API](https://help.syncfusion.com/cr/blazor/Syncfusion.Blazor.Charts.AccumulationDataLabelSettings.html)
- [.NET Standard Format Strings](https://docs.microsoft.com/en-us/dotnet/standard/base-types/standard-numeric-format-strings)

---

**Best practice summary:**
- Enable smart labels for charts with > 6 data points
- Use outside positioning for professional presentations
- Apply text wrapping for labels > 15 characters
- Test label visibility across different themes
- Pre-format complex text in data source rather than templates
- Consider tooltips for detailed information instead of cramming into labels
