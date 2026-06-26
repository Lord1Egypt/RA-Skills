## Table of Contents

- [Overview](#overview)
- [Basic Implementation](#basic-implementation)
- [Position and Alignment](#position-and-alignment)
   - [Position Options](#position-options)
   - [Position Guidelines](#position-guidelines)
- [Legend Reverse](#legend-reverse)
- [Legend Shape](#legend-shape)
- [Legend Size](#legend-size)
- [Legend Shape Size](#legend-shape-size)
- [Paging](#paging)
   - [Paging Customization](#paging-customization)
- [Legend Text Wrap](#legend-text-wrap)
- [Legend Template](#legend-template)
- [Toggle Visibility](#toggle-visibility)
- [Styling and Customization](#styling-and-customization)
   - [Border](#border)
   - [Font](#font)
   - [Padding and Spacing](#padding-and-spacing)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

# Legend Reference for Syncfusion Blazor Accumulation Charts

## Overview

The legend provides a visual reference that maps colors to data point categories in accumulation charts. It acts as a key for interpreting chart segments, enabling users to quickly identify what each color represents. Legends are particularly valuable in presentations, reports, and dashboards where viewers need to understand data without extensive explanation.

**Key capabilities:**
- Display series names or individual point labels
- Toggle series/point visibility by clicking legend items
- Position legend in various locations (Top, Bottom, Left, Right, Custom)
- Customize legend shape, size, and appearance
- Implement paging for charts with many data points
- Reverse legend order for alternative layouts
- Apply text wrapping for long legend labels
- Create custom legend templates for rich content

**When to use legends:**
- Charts contain more than 2-3 data points
- Color coding is not immediately obvious
- Users need to toggle data visibility interactively
- Printed materials or presentations require clear labeling
- Dashboards where chart context might not be immediately clear

**When to avoid legends:**
- Charts have 2 or fewer data points (use data labels instead)
- Space is extremely limited
- Data labels already clearly identify all segments
- Interactive legend is not needed and space is premium

## Basic Implementation

Enable legend by setting `Visible="true"` in `AccumulationChartLegendSettings`:

```razor
<SfAccumulationChart Title="Market Share Analysis">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@MarketData" 
                                 XName="Company" 
                                 YName="Share">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartLegendSettings Visible="true">
    </AccumulationChartLegendSettings>
</SfAccumulationChart>

@code {
    public class MarketShareData
    {
        public string Company { get; set; }
        public double Share { get; set; }
    }

    public List<MarketShareData> MarketData = new List<MarketShareData>
    {
        new MarketShareData { Company = "Company A", Share = 35 },
        new MarketShareData { Company = "Company B", Share = 28 },
        new MarketShareData { Company = "Company C", Share = 22 },
        new MarketShareData { Company = "Company D", Share = 15 }
    };
}
```

**Default behavior:**
- Legend positioned automatically (Right for wide charts, Bottom for tall charts)
- Legend items match data point X-values
- SeriesType shape (pie slice icon for pie charts)
- Click to toggle point visibility enabled
- Legend text wrapping disabled

## Position and Alignment

Control where the legend appears relative to the chart using `Position` and `Alignment` properties.

### Position Options

```razor
<AccumulationChartLegendSettings 
    Visible="true" 
    Position="Syncfusion.Blazor.Charts.LegendPosition.Top"
    Alignment="Alignment.Center"/>
```

**Available positions:**

| Position | Description | Best For |
|----------|-------------|----------|
| Top | Above chart | Wide charts, executive dashboards |
| Bottom | Below chart | Wide charts, presentation slides |
| Left | Left side of chart | Tall charts, narrow layouts |
| Right | Right side of chart | Standard dashboards, wide layouts |
| Custom | User-defined coordinates | Special layouts, fixed positioning |

**Alignment options:**

| Alignment | Description | Effect |
|-----------|-------------|--------|
| Near | Left (horiz) or Top (vert) | Legend starts at beginning |
| Center | Centered in available space | Balanced, professional look |
| Far | Right (horiz) or Bottom (vert) | Legend ends at boundary |

### Position Guidelines

**Top position:**
```razor
<AccumulationChartLegendSettings 
    Position="Syncfusion.Blazor.Charts.LegendPosition.Top" 
    Alignment="Alignment.Center"/>
```
- Best for: Wide layouts (aspect ratio > 1.5:1)
- Pros: Doesn't reduce chart height, easily readable
- Cons: Pushes chart down, may require scrolling

**Bottom position:**
```razor
<AccumulationChartLegendSettings 
    Position="Syncfusion.Blazor.Charts.LegendPosition.Bottom" 
    Alignment="Alignment.Center"/>
```
- Best for: Standard layouts, presentations
- Pros: Natural reading order, doesn't interfere with title
- Cons: Reduces vertical chart space

**Right position (default):**
```razor
<AccumulationChartLegendSettings 
    Position="Syncfusion.Blazor.Charts.LegendPosition.Right" 
    Alignment="Alignment.Center"/>
```
- Best for: Wide dashboards, desktop applications
- Pros: Maximizes chart size, traditional layout
- Cons: May not fit on narrow screens

**Left position:**
```razor
<AccumulationChartLegendSettings 
    Position="Syncfusion.Blazor.Charts.LegendPosition.Left" 
    Alignment="Alignment.Center"/>
```
- Best for: RTL languages, special design requirements
- Pros: Unique visual flow
- Cons: Less conventional, may confuse users

**Custom position:**
```razor
<AccumulationChartLegendSettings 
    Position="Syncfusion.Blazor.Charts.LegendPosition.Custom"
    Location="@(new ChartLocation { X = 100, Y = 50 })"/>
```
- Best for: Fixed layouts, overlay scenarios
- Pros: Complete control over positioning
- Cons: Requires manual adjustment, not responsive

## Legend Reverse

Reverse the order of legend items using the `Reverse` property:

```razor
<AccumulationChartLegendSettings 
    Visible="true" 
    Reverse="true"/>
```

**Default order:** First data point appears first in legend
**Reversed order:** Last data point appears first in legend

**When to use reverse:**
- Data points ordered smallest to largest, but you want prominent items first
- Cultural/design preferences favor reverse order
- Matching legend order to data table sort order
- Creating visual balance with chart orientation

**Example scenario:**
```csharp
// Data sorted by value (ascending)
public List<SalesData> Sales = new List<SalesData>
{
    new SalesData { Product = "Product E", Revenue = 5000 },   // Smallest
    new SalesData { Product = "Product D", Revenue = 12000 },
    new SalesData { Product = "Product C", Revenue = 18000 },
    new SalesData { Product = "Product B", Revenue = 25000 },
    new SalesData { Product = "Product A", Revenue = 35000 }   // Largest
};

// Reverse=true shows Product A first in legend (most prominent)
```

## Legend Shape

Customize the icon shape for legend items using `LegendShape` on the series:

```razor
<AccumulationChartSeries 
    DataSource="@Data" 
    XName="Category" 
    YName="Value"
    LegendShape="LegendShape.Rectangle">
</AccumulationChartSeries>
```

**Available shapes:**

| Shape | Visual | Best For |
|-------|--------|----------|
| SeriesType | Pie slice (default) | Natural representation |
| Circle | ● | Clean, minimal design |
| Rectangle | ■ | Traditional, professional |
| Triangle | ▲ | Attention-grabbing |
| Diamond | ◆ | Decorative, elegant |
| Pentagon | ⬟ | Unique, modern |
| Cross | ✕ | Warning/negative data |
| HorizontalLine | — | Trend indicators |
| VerticalLine | \| | Dividers, separators |
| InvertedTriangle | ▼ | Descending data |

**Selection guidelines:**
- **SeriesType**: Default, works for most scenarios
- **Circle**: Modern, minimal designs
- **Rectangle**: Business reports, formal documents
- **Triangle/Diamond**: When you want visual distinction
- **Cross**: Negative values, warnings
- **Lines**: When combined with other chart types

**Example with mixed shapes:**
```razor
<AccumulationChartSeriesCollection>
    <AccumulationChartSeries 
        DataSource="@PositiveData" 
        XName="Category" 
        YName="Value"
        LegendShape="LegendShape.Triangle"
        Name="Growth">
    </AccumulationChartSeries>
    <AccumulationChartSeries 
        DataSource="@NegativeData" 
        XName="Category" 
        YName="Value"
        LegendShape="LegendShape.InvertedTriangle"
        Name="Decline">
    </AccumulationChartSeries>
</AccumulationChartSeriesCollection>
```

## Legend Size

Control overall legend dimensions:

```razor
<AccumulationChartLegendSettings 
    Visible="true"
    Width="200"      <!-- Fixed width in pixels -->
    Height="100">    <!-- Fixed height in pixels -->
    <AccumulationChartLegendBorder Color="#d3d3d3" Width="1"/>
</AccumulationChartLegendSettings>
```

**Sizing strategy:**
- **Auto (default)**: Legend sizes based on content
- **Fixed**: Specify exact Width/Height
- **Percentage**: Use "30%" format for responsive layouts

**When to set fixed size:**
- Dashboards with consistent layouts
- Multiple charts need uniform legend sizes
- Prevent layout shifts when data changes
- Constrain legend in small spaces

**Example responsive sizing:**
```razor
<AccumulationChartLegendSettings 
    Width="25%"   <!-- 25% of chart width -->
    Height="80">  <!-- Fixed height -->
```

## Legend Shape Size

Adjust the size of individual legend icons:

```razor
<AccumulationChartLegendSettings 
    ShapeHeight="15"    <!-- Icon height in pixels -->
    ShapeWidth="15"/>   <!-- Icon width in pixels -->
```

**Default:** 10x10 pixels
**Recommended range:** 10-20 pixels
**Maximum:** 30 pixels (becomes disproportionate)

**Use cases:**
- Increase size for accessibility (vision impaired users)
- Reduce size to fit more legend items
- Match design system specifications
- Create visual hierarchy

**Example for accessibility:**
```razor
<AccumulationChartLegendSettings 
    ShapeHeight="18" 
    ShapeWidth="18">
    <AccumulationChartLegendFont Size="16px"/>
</AccumulationChartLegendSettings>
```

## Paging

When legend items exceed available space, paging automatically enables navigation buttons:

```razor
<AccumulationChartLegendSettings 
    Visible="true"
    Width="150"     <!-- Constrained width triggers paging -->
    Height="100"/>
```

**Automatic paging triggers when:**
- Legend item count × item height > Legend height
- Legend item width > Legend width (for horizontal layouts)

**Default paging behavior:**
- Left/Right arrows for horizontal legends
- Up/Down arrows for vertical legends
- Arrow size: 12px (adjustable)
- Page numbers displayed between arrows

### Paging Customization

```razor
<AccumulationChartLegendSettings 
    Visible="true" 
    Height="150" 
    Width="100">
    <AccumulationChartLegendPageSettings ArrowSize="15">
        <AccumulationChartLegendPageSettingsTextStyle 
            Color="#0066cc" 
            Size="14px"
            FontWeight="600"/>
    </AccumulationChartLegendPageSettings>
    <AccumulationChartLegendBorder Color="#cccccc" Width="1"/>
</AccumulationChartLegendSettings>
```

**Customizable properties:**

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| ArrowSize | double | Navigation arrow size (pixels) | 12 |
| Color | string | Arrow color | Theme color |
| Size | string | Page number font size | 14px |
| FontWeight | string | Page number font weight | Normal |

**Best practices:**
- Enable paging for charts with > 10 data points
- Use consistent arrow/text styling with chart theme
- Test navigation with keyboard (accessibility)
- Consider increasing legend size before enabling paging

**Troubleshooting:**
- **Paging doesn't appear:** Increase data points or reduce legend size
- **Too many pages:** Increase legend Height/Width or reduce data points
- **Arrows not visible:** Check arrow color contrasts with background

## Legend Text Wrap

Enable text wrapping for long legend labels:

```razor
<AccumulationChartLegendSettings 
    TextWrap="TextWrap.Wrap" 
    MaximumLabelWidth="100"/>
```

**How it works:**
- Labels exceeding `MaximumLabelWidth` break into multiple lines
- Wrapping occurs at word boundaries (preserves readability)
- Legend item height increases to accommodate wrapped text
- Paging calculation accounts for wrapped item heights

**Configuration options:**

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| TextWrap | Syncfusion.Blazor.Charts.TextWrap | Wrap or Normal | Normal |
| MaximumLabelWidth | double | Max width before wrapping (px) | No limit |

**Example with wrapping:**
```razor
<AccumulationChartLegendSettings 
    Position="Syncfusion.Blazor.Charts.LegendPosition.Right"
    Width="180"
    TextWrap="Syncfusion.Blazor.Charts.TextWrap.Wrap" 
    MaximumLabelWidth="150">
    <AccumulationChartLegendFont Size="12px"/>
</AccumulationChartLegendSettings>

@code {
    public List<ProductData> Products = new List<ProductData>
    {
        new ProductData { 
            Name = "Premium Wireless Noise-Cancelling Headphones", 
            Sales = 45000 
        },
        new ProductData { 
            Name = "Ergonomic Mechanical Gaming Keyboard", 
            Sales = 32000 
        }
    };
}
```

**When to use text wrapping:**
- Long category names (> 20 characters)
- Multilingual applications with variable label lengths
- Limited horizontal space (portrait mode, mobile)
- Professional reports requiring full category names

**When to avoid text wrapping:**
- Short labels (< 15 characters)
- Ample horizontal space available
- Performance-critical scenarios (wrapping adds layout complexity)
- Design requires single-line consistency

## Legend Template

Create custom legend items using templates for rich, branded content:

```razor
<AccumulationChartSeriesCollection>
    <AccumulationChartSeries DataSource="@Sales" 
                             XName="Product" 
                             YName="Revenue"
                             Name="2024 Sales"
                             PointColorMapping="Color">
        <LegendItemTemplate>
            @{
                var info = context as AccumulationChartLegendInfo;
                var product = info?.Data?["Product"]?.ToString() ?? "";
                var revenue = info?.Data?["Revenue"] is null ? 0 
                              : Convert.ToDouble(info.Data["Revenue"]);
                var color = info?.Data?["Color"]?.ToString() ?? "#000";
            }
            <div style="display: flex; align-items: center; gap: 8px; padding: 4px 0;">
                <div style="width: 16px; height: 16px; 
                           background: @color; 
                           border-radius: 50%;
                           border: 2px solid white;
                           box-shadow: 0 0 3px rgba(0,0,0,0.3);">
                </div>
                <div style="display: flex; flex-direction: column; line-height: 1.2;">
                    <span style="font-weight: 700; font-size: 13px; color: @color;">
                        @product
                    </span>
                    <span style="font-size: 11px; color: #666;">
                        <strong>@revenue.ToString("C0")</strong> revenue
                    </span>
                </div>
            </div>
        </LegendItemTemplate>
    </AccumulationChartSeries>
</AccumulationChartSeriesCollection>

@code {
    public class SalesData
    {
        public string Product { get; set; }
        public double Revenue { get; set; }
        public string Color { get; set; }
    }

    public List<SalesData> Sales = new()
    {
        new SalesData { Product = "Laptop", Revenue = 125000, Color = "#4CAF50" },
        new SalesData { Product = "Phone", Revenue = 98000, Color = "#2196F3" },
        new SalesData { Product = "Tablet", Revenue = 72000, Color = "#FF9800" }
    };
}
```

**Template context properties:**

| Property | Type | Description |
|----------|------|-------------|
| Text | string | Default legend text (X-value) |
| Data | IDictionary | Full data point (all fields) |
| Fill | string | Point color |
| Shape | LegendShape | Legend icon shape |

**Advanced template examples:**

**With icons:**
```razor
<LegendItemTemplate>
    @{
        var info = context as AccumulationChartLegendInfo;
        var product = info?.Text ?? "";
    }
    <div style="display: flex; align-items: center; gap: 6px;">
        <img src="/icons/@(product.ToLower()).png" 
             style="width: 20px; height: 20px;" />
        <span style="font-weight: 600;">@product</span>
    </div>
</LegendItemTemplate>
```

**With status badges:**
```razor
<LegendItemTemplate>
    @{
        var info = context as AccumulationChartLegendInfo;
        var revenue = Convert.ToDouble(info.Data["Revenue"]);
        var status = revenue > 100000 ? "High" : "Normal";
        var badgeColor = revenue > 100000 ? "#4CAF50" : "#9E9E9E";
    }
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-weight: 600;">@info.Text</span>
        <span style="background: @badgeColor; 
                     color: white; 
                     padding: 2px 6px; 
                     border-radius: 3px; 
                     font-size: 10px;">
            @status
        </span>
    </div>
</LegendItemTemplate>
```

**Best practices for templates:**
- Keep templates simple to avoid performance issues
- Ensure adequate contrast for readability
- Test with various data volumes (1-20 items)
- Consider mobile layout (smaller touch targets)
- Maintain interactive legend functionality

## Toggle Visibility

By default, clicking legend items toggles the visibility of corresponding chart segments. This feature enables users to focus on specific data subsets interactively.

**Default behavior:**
```razor
<AccumulationChartLegendSettings Visible="true"/>
<!-- Click any legend item to hide/show that segment -->
```

**Disable toggle:**
```razor
<AccumulationChartLegendSettings 
    Visible="true" 
    ToggleVisibility="false"/>
```

**When to disable toggle:**
- Presentation mode (prevent accidental clicks)
- Print/export scenarios
- Fixed visual comparison required
- Accessibility concerns (keyboard navigation only)

**Interactive behavior:**
1. User clicks legend item
2. Corresponding chart segment fades out (animates to transparent)
3. Chart recalculates percentages for visible segments
4. Legend item appears grayed out
5. Click again to restore visibility

**Customizing toggle behavior with events:**
```razor
<AccumulationChartEvents OnLegendItemRender="LegendRender"/>

@code {
    private void LegendRender(AccumulationLegendRenderEventArgs args)
    {
        // Prevent toggling specific items
        if (args.Text == "Critical Data")
        {
            args.Cancel = true;  // This prevents the item from being toggled
        }
    }
}
```

## Styling and Customization

### Border

Add borders around the legend container:

```razor
<AccumulationChartLegendSettings Visible="true">
    <AccumulationChartLegendBorder 
        Color="#cccccc" 
        Width="2"/>
</AccumulationChartLegendSettings>
```

### Font

Customize legend text appearance:

```razor
<AccumulationChartLegendSettings Visible="true">
    <AccumulationChartLegendFont 
        Size="14px"
        FontWeight="600"
        FontFamily="Arial, sans-serif"
        Color="#333333"
        FontStyle="Italic"/>
</AccumulationChartLegendSettings>
```

### Padding and Spacing

```razor
<AccumulationChartLegendSettings 
    Visible="true"
    Padding="15"        <!-- Space around legend content -->
    ItemPadding="10">   <!-- Space between legend items -->
</AccumulationChartLegendSettings>
```

## Best Practices

**Do:**
- Enable legends for charts with > 3 data points
- Use appropriate position based on layout (Right for wide, Bottom for tall)
- Enable text wrapping for labels > 20 characters
- Test legend toggle functionality before deployment
- Ensure legend color contrasts with background
- Use paging for charts with > 10 data points

**Don't:**
- Hide legend when colors aren't intuitive
- Use custom positioning without responsive design
- Create excessively tall legends (> 40% of chart height)
- Use tiny font sizes (< 10px)
- Forget to test with maximum expected data point count
- Ignore legend in mobile layouts

## Troubleshooting

**Legend not visible:**
- Check `Visible="true"` in AccumulationChartLegendSettings
- Verify chart has data
- Ensure legend position doesn't place it off-screen
- Check color contrasts with background

**Legend items cut off:**
- Increase legend Width/Height
- Enable text wrapping with MaximumLabelWidth
- Enable paging
- Reduce font size

**Paging doesn't work:**
- Verify legend Height/Width are constrained
- Ensure enough data points to trigger paging (usually > 10)
- Check ArrowSize isn't set to 0

**Toggle visibility not working:**
- Verify `ToggleVisibility="true"` (default)
- Check no custom click handlers blocking default behavior
- Ensure chart is interactive (not static image export)

---

**Quick reference:**
```razor
<!-- Complete legend configuration -->
<AccumulationChartLegendSettings 
    Visible="true"
    Position="Syncfusion.Blazor.Charts.LegendPosition.Right"
    Alignment="Alignment.Center"
    Reverse="false"
    ToggleVisibility="true"
    TextWrap="Syncfusion.Blazor.Charts.TextWrap.Wrap"
    MaximumLabelWidth="120"
    Width="200"
    Height="auto"
    ShapeHeight="15"
    ShapeWidth="15">
    <AccumulationChartLegendBorder Color="#ddd" Width="1"/>
    <AccumulationChartLegendFont Size="14px" FontWeight="Normal"/>
    <AccumulationChartLegendPageSettings ArrowSize="12">
        <AccumulationChartLegendPageSettingsTextStyle Color="#666"/>
    </AccumulationChartLegendPageSettings>
</AccumulationChartLegendSettings>
```
