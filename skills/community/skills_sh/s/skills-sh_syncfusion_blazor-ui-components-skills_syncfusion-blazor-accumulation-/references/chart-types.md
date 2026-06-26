# Accumulation Chart Types

## Table of Contents

- [Overview](#overview)
- [Pie Chart](#pie-chart)
   - [When to Use Pie Charts](#when-to-use-pie-charts)
   - [Basic Pie Chart](#basic-pie-chart)
   - [Customizing Pie Chart Radius](#customizing-pie-chart-radius)
   - [Customizing Pie Center Position](#customizing-pie-center-position)
   - [Various Radius Per Slice](#various-radius-per-slice)
   - [Start and End Angles](#start-and-end-angles)
   - [Color and Text Mapping](#color-and-text-mapping)
   - [Border Radius](#border-radius)
   - [Hide Border on Hover](#hide-border-on-hover)
- [Doughnut Chart](#doughnut-chart)
   - [When to Use Doughnut Charts](#when-to-use-doughnut-charts)
   - [Basic Doughnut Chart](#basic-doughnut-chart)
   - [InnerRadius Property](#innerradius-property)
   - [Doughnut with Center Label](#doughnut-with-center-label)
   - [Combining with Data Labels](#combining-with-data-labels)
- [Funnel Chart](#funnel-chart)
   - [When to Use Funnel Charts](#when-to-use-funnel-charts)
   - [Basic Funnel Chart](#basic-funnel-chart)
   - [Funnel Size Customization](#funnel-size-customization)
   - [Neck Dimensions](#neck-dimensions)
   - [Gap Between Segments](#gap-between-segments)
   - [Explode Funnel Segments](#explode-funnel-segments)
   - [Smart Data Labels for Funnels](#smart-data-labels-for-funnels)
- [Pyramid Chart](#pyramid-chart)
   - [When to Use Pyramid Charts](#when-to-use-pyramid-charts)
   - [Basic Pyramid Chart](#basic-pyramid-chart)
   - [Pyramid Mode: Linear vs Surface](#pyramid-mode-linear-vs-surface)
   - [Pyramid Size](#pyramid-size)
   - [Gap Between Pyramid Segments](#gap-between-pyramid-segments)
   - [Pyramid Explode](#pyramid-explode)
- [Choosing the Right Chart Type](#choosing-the-right-chart-type)
   - [Decision Matrix](#decision-matrix)
   - [When NOT to Use Accumulation Charts](#when-not-to-use-accumulation-charts)
   - [Type Property Values](#type-property-values)
   - [Combining Features Across Types](#combining-features-across-types)


## Overview

Syncfusion Blazor Accumulation Charts support four distinct chart types, each designed for specific data visualization needs:

| Chart Type | Best For | Key Features |
|-----------|----------|--------------|
| **Pie** | Proportional data, market share | Full circle, simple distribution |
| **Doughnut** | Multiple series, center content | Inner radius, center label support |
| **Funnel** | Stage-based processes, conversions | Narrowing segments, neck customization |
| **Pyramid** | Hierarchical data, rankings | Triangle shape, linear or surface mode |

The chart type is specified using the `Type` property on `AccumulationChartSeries`.

---

## Pie Chart

The default and most common accumulation chart type. Displays data as slices of a circular "pie" where each slice represents a proportion of the whole.

### When to Use Pie Charts

- **Proportional data visualization** - Show parts of a whole
- **Market share distribution** - Compare competitor shares
- **Survey results** - Display response percentages
- **Budget breakdowns** - Visualize spending categories
- **Sales by product** - Compare product performance

**Avoid when:** You have many categories (>7) or need precise value comparisons.

### Basic Pie Chart

```razor
@using Syncfusion.Blazor.Charts

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
        new MarketShareData { Company = "Chrome", Share = 37 },
        new MarketShareData { Company = "Firefox", Share = 19 },
        new MarketShareData { Company = "Safari", Share = 17 },
        new MarketShareData { Company = "Edge", Share = 12 },
        new MarketShareData { Company = "Opera", Share = 11 },
        new MarketShareData { Company = "Others", Share = 4 }
    };
}
```

### Customizing Pie Chart Radius

Control the size of the pie using the `Radius` property (default: 80%):

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Category" 
                         YName="Value"
                         Radius="100%">
</AccumulationChartSeries>
```

- **"80%"** - Default, leaves margin around chart
- **"100%"** - Full size, fills available space
- **"60%"** - Smaller pie, more surrounding space

### Customizing Pie Center Position

Move the pie center using `AccumulationChartCenter`:

```razor
<SfAccumulationChart Title="Off-Center Pie">
    <AccumulationChartCenter X="70%" Y="60%" />
    
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

**Use cases:**
- Creating asymmetric layouts
- Positioning for specific design requirements
- Aligning with other page elements

### Various Radius Per Slice

Give each slice a different radius by mapping to a data property:

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Region" 
                         YName="Revenue"
                         InnerRadius="20%"
                         Radius="RadiusValue">
</AccumulationChartSeries>

@code {
    public class RevenueData
    {
        public string Region { get; set; }
        public double Revenue { get; set; }
        public string RadiusValue { get; set; }  // "100", "118.7", "124.6", etc.
    }

    public List<RevenueData> Data = new List<RevenueData>
    {
        new RevenueData { Region = "North", Revenue = 505, RadiusValue = "100" },
        new RevenueData { Region = "South", Revenue = 551, RadiusValue = "118.7" },
        new RevenueData { Region = "East", Revenue = 312, RadiusValue = "124.6" }
    };
}
```

Creates dramatic visual hierarchy - larger slices for higher values.

### Start and End Angles

Create semi-pie or custom arc charts:

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Category" 
                         YName="Value"
                         StartAngle="270" 
                         EndAngle="90">
</AccumulationChartSeries>
```

**Common configurations:**
- **0° to 360°** - Full circle (default)
- **270° to 90°** - Semi-circle (bottom half)
- **0° to 180°** - Semi-circle (right half)
- **180° to 360°** - Semi-circle (left half)

### Color and Text Mapping

Map colors and label text from your data source:

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Product" 
                         YName="Sales"
                         PointColorMapping="Color">
    <AccumulationDataLabelSettings Visible="true" 
                                   Name="LabelText">
    </AccumulationDataLabelSettings>
</AccumulationChartSeries>

@code {
    public class SalesData
    {
        public string Product { get; set; }
        public double Sales { get; set; }
        public string Color { get; set; }     // "#498fff", "#ffa060", etc.
        public string LabelText { get; set; } // "37%", "Product A", etc.
    }

    public List<SalesData> Data = new List<SalesData>
    {
        new SalesData { Product = "A", Sales = 37, Color = "#498fff", LabelText = "37%" },
        new SalesData { Product = "B", Sales = 28, Color = "#ffa060", LabelText = "28%" }
    };
}
```

### Border Radius

Round the corners of pie slices:

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Item" 
                         YName="Amount"
                         BorderRadius="8">
</AccumulationChartSeries>
```

Creates modern, polished appearance with rounded edges.

### Hide Border on Hover

Disable the highlight border that appears on mouse hover:

```razor
<SfAccumulationChart EnableBorderOnMouseMove="false">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

---

## Doughnut Chart

A pie chart with a hollow center, created by setting `InnerRadius`. Perfect for displaying center content or multiple concentric series.

### When to Use Doughnut Charts

- **Center content display** - Show total or summary in center
- **Multiple data series** - Compare two concentric rings
- **Modern design aesthetic** - More contemporary than traditional pie
- **Focus on segment lengths** - Easier to compare than pie slices

### Basic Doughnut Chart

```razor
<SfAccumulationChart Title="Revenue Distribution">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@RevenueData" 
                                 XName="Region" 
                                 YName="Revenue"
                                 InnerRadius="40%">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    public List<RegionRevenue> RevenueData = new List<RegionRevenue>
    {
        new RegionRevenue { Region = "North America", Revenue = 125.5 },
        new RegionRevenue { Region = "Europe", Revenue = 98.2 },
        new RegionRevenue { Region = "Asia", Revenue = 76.8 },
        new RegionRevenue { Region = "Latin America", Revenue = 54.3 }
    };
}
```

### InnerRadius Property

Controls the size of the hollow center:

- **"0%"** - Full pie (no hollow)
- **"40%"** - Balanced doughnut (recommended)
- **"60%"** - Thin ring
- **"80%"** - Very thin ring (almost circular line)

```razor
<AccumulationChartSeries InnerRadius="60%">
```

### Doughnut with Center Label

Display text or values in the hollow center:

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Category" 
                         YName="Value"
                         InnerRadius="40%">
    <AccumulationChartCenterLabel 
        Text="Total<br/>$1.2M">
        <AccumulationChartCenterLabelFont
            Size="18px"
            FontWeight="600"
            Color="#333">
        </AccumulationChartCenterLabelFont>
    </AccumulationChartCenterLabel>
</AccumulationChartSeries>
```

**Best practices:**
- Keep text concise (1-3 lines)
- Use `<br/>` for line breaks
- Style appropriately for visibility
- Update dynamically with events

For more center label customization, see [center-label.md](center-label.md).

### Combining with Data Labels

Doughnuts work well with outside labels and connectors:

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Product" 
                         YName="Sales"
                         InnerRadius="40%">
    <AccumulationDataLabelSettings Visible="true" 
                                   Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
        <AccumulationChartConnector Length="20px">
        </AccumulationChartConnector>
    </AccumulationDataLabelSettings>
    <AccumulationChartCenterLabel Text="Total<br/>Sales">
    </AccumulationChartCenterLabel>
</AccumulationChartSeries>
```

---

## Funnel Chart

Visualizes data as progressively narrowing stages, ideal for conversion processes and stage-based workflows.

### When to Use Funnel Charts

- **Sales pipelines** - Lead → Prospect → Customer stages
- **Conversion funnels** - Website visitor → Sign-up → Purchase
- **Recruitment process** - Applied → Screened → Interviewed → Hired
- **Manufacturing stages** - Raw material → Processing → Final product
- **Any sequential process** with decreasing quantities

### Basic Funnel Chart

```razor
<SfAccumulationChart Title="Sales Conversion Funnel">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@FunnelData" 
                                 XName="Stage" 
                                 YName="Count"
                                 Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel">
            <AccumulationDataLabelSettings Visible="true" Name="Stage">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    public class FunnelStageData
    {
        public string Stage { get; set; }
        public double Count { get; set; }
    }

    public List<FunnelStageData> FunnelData = new List<FunnelStageData>
    {
        new FunnelStageData { Stage = "Website Visitors", Count = 10000 },
        new FunnelStageData { Stage = "Product Views", Count = 5500 },
        new FunnelStageData { Stage = "Add to Cart", Count = 2800 },
        new FunnelStageData { Stage = "Checkout Started", Count = 1200 },
        new FunnelStageData { Stage = "Purchase Complete", Count = 850 }
    };
}
```

### Funnel Size Customization

Control overall funnel dimensions:

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel"
                         Width="60%" 
                         Height="80%">
</AccumulationChartSeries>
```

- **Width**: Horizontal extent (default: 80%)
- **Height**: Vertical extent (default: 80%)

### Neck Dimensions

The "neck" is the narrow bottom portion of the funnel. Customize with `NeckWidth` and `NeckHeight`:

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel"
                         NeckWidth="15%" 
                         NeckHeight="18%">
</AccumulationChartSeries>
```

- **NeckWidth**: Width of bottom section (% of chart width)
- **NeckHeight**: Height of neck section (% of funnel height)
- **Larger neck** = more gradual taper
- **Smaller neck** = dramatic narrowing effect

**Visual examples:**
- `NeckWidth="25%", NeckHeight="25%"` - Gentle taper
- `NeckWidth="10%", NeckHeight="10%"` - Sharp narrowing (classic funnel)
- `NeckWidth="0%", NeckHeight="0%"` - Perfect triangle (no neck)

### Gap Between Segments

Add spacing between funnel segments:

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel"
                         GapRatio="0.2">
</AccumulationChartSeries>
```

- **0** - No gaps (segments touch)
- **0.1** - Small gaps
- **0.2** - Medium gaps (recommended)
- **0.3+** - Large gaps (segments appear disconnected)

### Explode Funnel Segments

Separate segments from the funnel:

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel"
                         Explode="true"
                         ExplodeIndex="2"
                         ExplodeOffset="10%">
</AccumulationChartSeries>
```

- **Explode**: Enable click-to-explode behavior
- **ExplodeIndex**: Segment to explode on load (0-based)
- **ExplodeOffset**: Distance of explosion

### Smart Data Labels for Funnels

With many segments, labels can overlap. Enable smart positioning:

```razor
<SfAccumulationChart EnableAnimation="false">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel"
                                 Width="50%" Height="80%"
                                 NeckWidth="15%" NeckHeight="18%">
            <AccumulationDataLabelSettings Visible="true" 
                                           Name="Country"
                                           Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
                <AccumulationChartConnector Length="6%">
                </AccumulationChartConnector>
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

Labels automatically reposition to avoid collisions.

---

## Pyramid Chart

Displays hierarchical data in an upside-down triangle with horizontal segments. Shows ranking or hierarchical structure.

### When to Use Pyramid Charts

- **Organizational hierarchy** - Management levels
- **Food pyramid** - Dietary recommendations
- **Age distribution** - Population demographics (inverted)
- **Priority ranking** - High to low importance
- **Resource allocation** - Distribution by category

### Basic Pyramid Chart

```razor
<SfAccumulationChart Title="Organizational Hierarchy">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@HierarchyData" 
                                 XName="Level" 
                                 YName="Count"
                                 Type="Syncfusion.Blazor.Charts.AccumulationType.Pyramid">
            <AccumulationDataLabelSettings Visible="true" Name="Level">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    public class HierarchyLevel
    {
        public string Level { get; set; }
        public double Count { get; set; }
    }

    public List<HierarchyLevel> HierarchyData = new List<HierarchyLevel>
    {
        new HierarchyLevel { Level = "C-Level", Count = 5 },
        new HierarchyLevel { Level = "Directors", Count = 15 },
        new HierarchyLevel { Level = "Managers", Count = 45 },
        new HierarchyLevel { Level = "Team Leads", Count = 120 },
        new HierarchyLevel { Level = "Staff", Count = 500 }
    };
}
```

### Pyramid Mode: Linear vs Surface

Two rendering modes affect how segment heights are calculated:

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Pyramid"
                         PyramidMode="Syncfusion.Blazor.Charts.PyramidMode.Linear">
</AccumulationChartSeries>
```

**Linear Mode (default):**
- Segment height proportional to value
- Equal visual spacing
- Better for data comparison

**Surface Mode:**
- Segment area proportional to value
- Variable heights for visual balance
- More aesthetically pleasing

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Pyramid"
                         PyramidMode="Syncfusion.Blazor.Charts.PyramidMode.Surface">
</AccumulationChartSeries>
```

### Pyramid Size

Control dimensions just like funnels:

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Pyramid"
                         Width="60%" 
                         Height="80%">
</AccumulationChartSeries>
```

### Gap Between Pyramid Segments

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Pyramid"
                         GapRatio="0.2">
</AccumulationChartSeries>
```

Same behavior as funnel gaps - creates separation between horizontal segments.

### Pyramid Explode

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Pyramid"
                         Explode="true"
                         ExplodeIndex="2"
                         ExplodeOffset="10">
</AccumulationChartSeries>
```

Separates a segment horizontally from the pyramid.

---

## Choosing the Right Chart Type

### Decision Matrix

| Requirement | Recommended Chart |
|-------------|------------------|
| Show proportions of a whole | Pie |
| Display center content | Doughnut |
| Visualize stage-based process | Funnel |
| Show hierarchical ranking | Pyramid |
| Multiple data series | Doughnut (concentric) |
| Emphasize flow/conversion | Funnel |
| Need modern aesthetic | Doughnut |
| Traditional data distribution | Pie |

### When NOT to Use Accumulation Charts

- **Many categories** (>8): Consider bar/column charts
- **Precise value comparison**: Use bar or column charts
- **Time series data**: Use line or area charts
- **Negative values**: Accumulation charts require positive values
- **Multiple series comparison**: Use grouped bar/column charts

### Type Property Values

```csharp
Type="Syncfusion.Blazor.Charts.AccumulationType.Pie"      // Default if not specified
Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel"
Type="Syncfusion.Blazor.Charts.AccumulationType.Pyramid"
// Doughnut is Pie with InnerRadius > 0
```

### Combining Features Across Types

Many features work across all types:

✅ **Works for all types:**
- Data labels
- Legends
- Tooltips
- Selection and explosion
- Animations
- Events

❌ **Type-specific:**
- `InnerRadius` - Pie/Doughnut only
- `NeckWidth/NeckHeight` - Funnel only
- `PyramidMode` - Pyramid only
- `StartAngle/EndAngle` - Pie/Doughnut only

