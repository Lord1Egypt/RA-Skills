# Customization and Styling

## Table of Contents

- [Gradients](#gradients)
   - [Linear Gradients](#linear-gradients)
   - [Radial Gradients](#radial-gradients)
   - [Per-Point Gradients](#per-point-gradients)
- [Grouping Small Slices](#grouping-small-slices)
   - [Basic Grouping by Value](#basic-grouping-by-value)
   - [Grouping by Point Count](#grouping-by-point-count)
   - [Grouping Modes](#grouping-modes)
   - [Broken Slice (Interactive Grouping)](#broken-slice-interactive-grouping)
- [Annotations](#annotations)
   - [Basic Annotation](#basic-annotation)
   - [Coordinate Units](#coordinate-units)
   - [Positioning Regions](#positioning-regions)
   - [Annotation Examples](#annotation-examples)
- [Empty Points](#empty-points)
   - [Empty Point Modes](#empty-point-modes)
   - [Custom Empty Point Styling](#custom-empty-point-styling)
- [Themes and Colors](#themes-and-colors)
   - [Built-in Themes](#built-in-themes)
   - [Custom Color Palettes](#custom-color-palettes)
   - [Per-Point Colors](#per-point-colors)
- [Borders and Radius](#borders-and-radius)
   - [Slice Borders](#slice-borders)
   - [Border Radius](#border-radius)
   - [Hide Hover Border](#hide-hover-border)
- [Responsive and Adaptive Layout](#responsive-and-adaptive-layout)
   - [Responsive Sizing](#responsive-sizing)
   - [Adaptive Layout](#adaptive-layout)
   - [Mobile Optimization](#mobile-optimization)
- [Best Practices](#best-practices)
   - [Performance](#performance)
   - [Design](#design)
   - [Accessibility](#accessibility)
   - [Usability](#usability)


## Gradients

Apply smooth color transitions to slices for modern, professional appearance.

### Linear Gradients

Blend colors along a straight line:

```razor
<AccumulationChartSeries DataSource="@Data" XName="Category" YName="Value">
    <AccumulationChartLinearGradient X1="0.1" Y1="0.0" X2="0.9" Y2="1.0">
        <AccumulationChartGradientColorStops>
            <AccumulationChartGradientColorStop Offset="0" Color="#4F46E5" Opacity="1" Brighten="0.55" />
            <AccumulationChartGradientColorStop Offset="60" Color="#4F46E5" Opacity="0.98" Brighten="0.15" />
            <AccumulationChartGradientColorStop Offset="100" Color="#4F46E5" Opacity="0.95" Brighten="-0.25" />
        </AccumulationChartGradientColorStops>
    </AccumulationChartLinearGradient>
</AccumulationChartSeries>
```

**Properties:**
- **X1, Y1**: Start point (0-1 coordinates)
- **X2, Y2**: End point (0-1 coordinates)
- **Offset**: Position along gradient (0-100)
- **Brighten**: Adjust brightness (-1 to 1)
- **Lighten**: Adjust lightness
- **Opacity**: Transparency (0-1)

### Radial Gradients

Create circular color transitions from center outward:

```razor
<AccumulationChartRadialGradient CX="0.5" CY="0.5" R="1" FX="0.5" FY="0.5">
    <AccumulationChartGradientColorStops>
        <AccumulationChartGradientColorStop Offset="0" Color="#FFFFFF" Opacity="1" />
        <AccumulationChartGradientColorStop Offset="100" Color="#4F46E5" Opacity="1" />
    </AccumulationChartGradientColorStops>
</AccumulationChartRadialGradient>
```

**When to use:**
- Pie/doughnut charts for 3D effect
- Emphasize center content
- Modern, polished design

### Per-Point Gradients

Apply different gradients to individual slices using `OnPointRender` event:

```razor
<SfAccumulationChart>
    <AccumulationChartEvents OnPointRender="PointRender"></AccumulationChartEvents>
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    private void PointRender(AccumulationPointRenderEventArgs args)
    {
        var gradient = new AccumulationChartLinearGradient
        {
            X1 = "0.0", Y1 = "0.0", X2 = "1.0", Y2 = "1.0"
        };
        gradient.ColorStops = new List<AccumulationChartGradientColorStop>
        {
            new AccumulationChartGradientColorStop { Offset = 0, Color = GetColor(args.Point.Index), Opacity = 1 },
            new AccumulationChartGradientColorStop { Offset = 100, Color = GetColor(args.Point.Index), Opacity = 0.7, Brighten = -0.3 }
        };
        args.Fill = gradient;
    }
    
    private string GetColor(int index)
    {
        string[] colors = { "#4F46E5", "#06B6D4", "#10B981", "#F59E0B", "#EF4444" };
        return colors[index % colors.Length];
    }
}
```

## Grouping Small Slices

Combine small data points into an "Others" category for cleaner visualization.

### Basic Grouping by Value

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Category" 
                         YName="Value"
                         GroupTo="10">
</AccumulationChartSeries>
```

Points with values < 10 are grouped together.

### Grouping by Point Count

```razor
<AccumulationChartSeries GroupTo="3" 
                         GroupMode="Syncfusion.Blazor.Charts.GroupMode.Point">
</AccumulationChartSeries>
```

Smallest 3 points are grouped.

### Grouping Modes

**Syncfusion.Blazor.Charts.GroupMode.Value** (default):
- Groups by numeric threshold
- Example: `GroupTo="10"` groups all values < 10

**Syncfusion.Blazor.Charts.GroupMode.Point**:
- Groups by point count
- Example: `GroupTo="3"` groups 3 smallest points

### Broken Slice (Interactive Grouping)

Enable `Explode` to let users click "Others" to see grouped items:

```razor
<AccumulationChartSeries GroupTo="10" 
                         Explode="true" 
                         ExplodeOffset="10">
</AccumulationChartSeries>
```

**Best practices:**
- Use for 8+ data points
- Set threshold to group <5% values
- Maintain data integrity (show full data in tooltip)

## Annotations

Add text, shapes, or images to highlight specific regions.

### Basic Annotation

```razor
<SfAccumulationChart>
    <AccumulationChartAnnotations>
        <AccumulationChartAnnotation X="50%" Y="50%" 
                                     CoordinateUnits="Units.Percentage" 
                                     Region="Regions.Chart">
            <ContentTemplate>
                <div style="background:#f0f0f0; padding:10px; border-radius:5px;">
                    <b>Total Sales</b><br/>
                    $1.2M
                </div>
            </ContentTemplate>
        </AccumulationChartAnnotation>
    </AccumulationChartAnnotations>
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

### Coordinate Units

**Units.Percentage**:
- X, Y as percentages ("50%", "75%")
- Relative to chart/series area

**Units.Pixel**:
- Absolute pixel coordinates
- X=100, Y=150

**Units.Point**:
- Position relative to data point
- X="ProductA", Y=value

### Positioning Regions

**Regions.Chart**:
- Relative to entire chart area
- For titles, watermarks, legends

**Regions.Series**:
- Relative to plot area
- For data-specific annotations

### Annotation Examples

**Highlight a slice:**
```razor
<AccumulationChartAnnotation X="Chrome" Y="37" 
                             CoordinateUnits="Units.Point" 
                             Region="Regions.Series">
    <ContentTemplate>
        <div style="color:red; font-weight:bold;">★ Best Performer</div>
    </ContentTemplate>
</AccumulationChartAnnotation>
```

**Watermark:**
```razor
<AccumulationChartAnnotation X="50%" Y="50%" 
                             CoordinateUnits="Units.Percentage">
    <ContentTemplate>
        <div style="opacity:0.1; font-size:48px; transform:rotate(-45deg);">
            CONFIDENTIAL
        </div>
    </ContentTemplate>
</AccumulationChartAnnotation>
```

## Empty Points

Handle null, undefined, or zero values in data.

### Empty Point Modes

```razor
<AccumulationChartSeries DataSource="@Data" XName="Month" YName="Sales">
    <AccumulationChartEmptyPointSettings Mode="Syncfusion.Blazor.Charts.EmptyPointMode.Drop">
    </AccumulationChartEmptyPointSettings>
</AccumulationChartSeries>
```

**Modes:**
- **Drop**: Skip empty points (don't render)
- **Zero**: Treat as zero value
- **Average**: Use average of adjacent values
- **Gap**: Leave visual gap (funnel/pyramid)

### Custom Empty Point Styling

```razor
<AccumulationChartEmptyPointSettings Mode="Syncfusion.Blazor.Charts.EmptyPointMode.Average" 
                                     Fill="#cccccc" 
                                     Border="new { Width = 2, Color = '#ff0000' }">
</AccumulationChartEmptyPointSettings>
```

**When to use each mode:**
- **Drop**: Data truly missing, shouldn't affect totals
- **Zero**: Missing data means no value
- **Average**: Estimate missing data
- **Gap**: Show data discontinuity

## Themes and Colors

### Built-in Themes

Apply via chart `Theme` property:

```razor
<SfAccumulationChart Theme="Syncfusion.Blazor.Theme.Bootstrap5">
</SfAccumulationChart>
```

**Available themes:**
- Bootstrap5, Bootstrap5Dark
- Material, Material3, MaterialDark, Material3Dark
- Fabric, FabricDark
- Fluent, Fluent2, FluentDark, Fluent2Dark
- Tailwind, TailwindDark, Tailwind3, Tailwind3Dark
- HighContrast, HighContrastLight

### Custom Color Palettes

Define custom colors for the series:

```razor
<AccumulationChartSeries DataSource="@Data" XName="X" YName="Y" 
                         Palettes="@CustomPalette">
</AccumulationChartSeries>

@code {
    private string[] CustomPalette = new string[] 
    {
        "#4F46E5", "#06B6D4", "#10B981", "#F59E0B", "#EF4444",
        "#8B5CF6", "#EC4899", "#F97316"
    };
}
```

### Per-Point Colors

Use `PointColorMapping` to assign colors from data:

```razor
<AccumulationChartSeries DataSource="@Data" 
                         XName="Category" 
                         YName="Value"
                         PointColorMapping="Color">
</AccumulationChartSeries>

@code {
    public class DataPoint
    {
        public string Category { get; set; }
        public double Value { get; set; }
        public string Color { get; set; }  // "#4F46E5", "#06B6D4", etc.
    }
}
```

## Borders and Radius

### Slice Borders

```razor
<AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
    <AccumulationChartSeriesBorder Width="2" Color="#FFFFFF">
    </AccumulationChartSeriesBorder>
</AccumulationChartSeries>
```

**Common patterns:**
- White borders for slice separation
- Thin borders (1-2px) for clean look
- Transparent for seamless appearance

### Border Radius

Round slice corners:

```razor
<AccumulationChartSeries BorderRadius="8">
</AccumulationChartSeries>
```

- Values: 0 (sharp) to 15 (very rounded)
- Best with: Modern designs, doughnut charts
- Affects: First and last slices (pie), all segments (funnel/pyramid)

### Hide Hover Border

```razor
<SfAccumulationChart EnableBorderOnMouseMove="false">
</SfAccumulationChart>
```

Disables the highlight border on mouse hover.

## Responsive and Adaptive Layout

### Responsive Sizing

Use percentage-based dimensions:

```razor
<SfAccumulationChart Width="100%" Height="450px">
</SfAccumulationChart>
```

### Adaptive Layout

Automatically adjusts for mobile devices:

```razor
<SfAccumulationChart EnableAdaptiveUI="true">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
            <AccumulationDataLabelSettings Visible="true" Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

**Adaptive features:**
- Larger touch targets for mobile
- Adjusted label positioning
- Optimized legend placement
- Simplified data labels

### Mobile Optimization

```razor
@if (IsMobile)
{
    <SfAccumulationChart Height="350px">
        <AccumulationChartSeriesCollection>
            <AccumulationChartSeries InnerRadius="30%">
                <AccumulationDataLabelSettings Visible="false">
                </AccumulationDataLabelSettings>
            </AccumulationChartSeries>
        </AccumulationChartSeriesCollection>
        <AccumulationChartLegendSettings Visible="true" Position="Syncfusion.Blazor.Charts.LegendPosition.Bottom">
        </AccumulationChartLegendSettings>
    </SfAccumulationChart>
}
else
{
    <SfAccumulationChart Height="500px">
        <AccumulationChartSeriesCollection>
            <AccumulationChartSeries InnerRadius="40%">
                <AccumulationDataLabelSettings Visible="true" Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
                </AccumulationDataLabelSettings>
            </AccumulationChartSeries>
        </AccumulationChartSeriesCollection>
    </SfAccumulationChart>
}

@code {
    private bool IsMobile => /* detect mobile */;
}
```

## Best Practices

### Performance
- Limit data points (≤20 for optimal rendering)
- Use grouping for many small slices
- Avoid complex gradients on 15+ slices
- Minimize annotation count

### Design
- Maintain consistent color schemes across charts
- Use white/transparent borders for clean separation
- Apply gradients sparingly for emphasis
- Keep annotations minimal and relevant

### Accessibility
- Ensure sufficient color contrast
- Don't rely solely on color (use labels)
- Test with HighContrast theme
- Provide text alternatives

### Usability
- Group slices <3% of total
- Use tooltips for detailed data
- Enable legend for category identification
- Test on target devices (mobile/desktop)

