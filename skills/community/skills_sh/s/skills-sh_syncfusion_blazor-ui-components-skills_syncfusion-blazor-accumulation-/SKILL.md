---
name: syncfusion-blazor-accumulation-chart
description: Implement Syncfusion Blazor Accumulation Chart (SfAccumulationChart) for proportional data visualization. Use this when creating pie charts, doughnut charts, funnel charts, or pyramid charts. This skill covers data labels, legends, tooltips, slice grouping, and part-to-whole visualizations in Blazor applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Blazor Accumulation Charts

**NuGet:** `Syncfusion.Blazor.Charts` + `Syncfusion.Blazor.Themes`  
**Namespace:** `Syncfusion.Blazor.Charts`

A comprehensive guide for implementing the Syncfusion Blazor Accumulation Chart component to create interactive pie, doughnut, funnel, and pyramid charts that visualize proportional and hierarchical data in Blazor applications.

## When to Use This Skill

Use this skill when you need to:
- **Create pie charts** to show proportional data distribution
- **Build doughnut charts** with center labels or multiple series
- **Implement funnel charts** for stage-based data (sales pipeline, conversion rates)
- **Create pyramid charts** for hierarchical data visualization
- **Display percentage distributions** and part-to-whole relationships
- **Visualize market share**, survey results, or categorical proportions
- **Show composition data** with interactive slicing and legends
- **Add data labels** with smart positioning and connector lines
- **Implement center labels** for doughnut charts with dynamic content
- **Customize appearance** with gradients, themes, and annotations
- **Group small slices** to improve readability
- **Handle user interactions** with tooltips, selection, and events
- **Create accessible charts** with ARIA support and keyboard navigation

## Component Overview

The Syncfusion Blazor Accumulation Chart component specializes in circular and triangular visualizations for proportional data:

- **4 Chart Types:** Pie, Doughnut, Funnel, Pyramid
- **Data Labels:** Smart positioning, connector lines, templates, text wrapping
- **Legends:** Customizable positioning, paging, click behavior
- **Tooltips:** Formatted display, custom templates
- **Center Labels:** Doughnut-specific feature with dynamic content
- **Grouping:** Combine small slices into "Others" category
- **Customization:** Gradients, annotations, themes, colors, borders
- **Interactivity:** Selection, explosion, hover effects, animations
- **Accessibility:** WCAG compliance, ARIA support, keyboard navigation
- **Export:** Print support, image export

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Use this when:
- Setting up a new Blazor Accumulation Chart project
- Installing NuGet packages and dependencies
- Creating your first pie or doughnut chart
- Understanding basic component structure
- Working with Visual Studio, VS Code, or .NET CLI
- Binding data to accumulation charts

Topics covered:
- Installation prerequisites and system requirements
- NuGet package installation (Syncfusion.Blazor.Charts)
- Service registration and namespace imports
- Theme and script references
- Basic SfAccumulationChart implementation
- Data source configuration (XName, YName properties)
- Adding title, data labels, tooltip, and legend
- Running the application

---

### Chart Types

📄 **Read:** [references/chart-types.md](references/chart-types.md)

Use this when:
- Choosing the right chart type for your data
- Implementing pie charts (default type)
- Creating doughnut charts with inner radius
- Building funnel charts for conversion visualization
- Designing pyramid charts for hierarchical data
- Understanding type-specific properties

Topics covered:
- **Pie Chart:** Default circular visualization, when to use
- **Doughnut Chart:** Inner radius configuration, center content area
- **Funnel Chart:** Neck dimensions, width/height ratios, data flow
- **Pyramid Chart:** Linear vs surface mode, base positioning
- Type property configuration
- Visual differences and use cases
- Code examples for each type

---

### Data Labels

📄 **Read:** [references/data-label.md](references/data-label.md)

Use this when:
- Enabling and customizing data labels
- Positioning labels inside or outside slices
- Implementing smart labels for collision avoidance
- Adding connector lines from labels to slices
- Customizing label text, format, and templates
- Handling text wrapping and overflow
- Using custom data fields for label text

Topics covered:
- Visible property to enable labels
- Position options (Inside, Outside)
- Text wrapping with MaxWidth
- Smart label positioning
- Connector line customization (type, length, color, width)
- Text mapping from data source fields
- Format patterns (N1, P1, C1 for numbers/percentages/currency)
- Template customization with HTML and context values
- Font styling, borders, and backgrounds

---

### Legends

📄 **Read:** [references/legend.md](references/legend.md)

Use this when:
- Adding legends to accumulation charts
- Positioning legends (top, bottom, left, right)
- Customizing legend appearance and behavior
- Implementing legend paging for many data points
- Creating custom legend templates
- Handling legend click events

Topics covered:
- Enabling legends with Visible property
- Position and alignment options
- Legend shape customization
- Text styling and truncation
- Toggle visibility behavior on legend click
- Legend paging configuration
- Custom templates for legend items
- Click and hover events

---

### Tooltips

📄 **Read:** [references/tooltip.md](references/tooltip.md)

Use this when:
- Enabling tooltips on hover
- Formatting tooltip content
- Creating custom tooltip templates
- Styling tooltip appearance
- Configuring tooltip behavior and animation

Topics covered:
- Enable property for tooltip activation
- Format string for value display
- Header customization
- Custom templates with HTML
- Border, fill, and font styling
- Animation settings
- Shared tooltips (if applicable)

---

### Center Labels

📄 **Read:** [references/center-label.md](references/center-label.md)

Use this when:
- Adding text in the center of doughnut charts
- Displaying static or dynamic center content
- Customizing center label appearance
- Showing aggregated data in center
- Implementing hover-based center text updates

Topics covered:
- Center label Text property
- TextStyle customization (font, size, color)
- Dynamic text with templates
- Hover-based text updates using events
- Center label visibility control
- Use cases and best practices

---

### Customization and Styling

📄 **Read:** [references/customization-styling.md](references/customization-styling.md)

Use this when:
- Applying gradient fills to slices
- Grouping small slices into "Others"
- Adding annotations (text, shapes, images)
- Handling empty points in data
- Customizing themes and color palettes
- Setting border styles and radius
- Implementing responsive layouts
- Using adaptive design for mobile

Topics covered:
- **Gradients:** Radial and linear fills for slices
- **Grouping:** GroupTo and GroupMode for combining small values
- **Annotations:** Text, shape, and image annotations with positioning
- **Empty Points:** Mode options (Zero, Drop, Average, Gap)
- **Themes:** Built-in themes and custom theme application
- **Colors:** Custom color palettes and per-point colors
- **Borders:** Width, color, and dash array
- **Radius:** Inner radius (doughnut) and overall chart radius
- **Responsive:** Adaptive layout for different screen sizes

---

### Animation and Events

📄 **Read:** [references/animation-events.md](references/animation-events.md)

Use this when:
- Configuring chart load animations
- Handling point selection and click events
- Responding to mouse hover and leave events
- Implementing custom interactions
- Accessing chart lifecycle events
- Working with series and point rendering events

Topics covered:
- **Animation:** Enable, duration, delay configuration
- **Chart Events:** Load, Loaded, BeforeResize, Resized
- **Point Events:** OnPointClick, OnPointMove, PointRender
- **Series Events:** SeriesRender, OnLegendClick
- **Data Label Events:** OnDataLabelRender, TextRender
- **Selection:** OnSelectionComplete, selection mode
- **Tooltip Events:** TooltipRender
- Event data structures and parameters
- Practical event handling examples

---

### Accessibility and Printing

📄 **Read:** [references/accessibility-printing.md](references/accessibility-printing.md)

Use this when:
- Implementing WCAG-compliant charts
- Adding ARIA attributes for screen readers
- Enabling keyboard navigation
- Supporting right-to-left (RTL) layouts
- Implementing print functionality
- Exporting charts as images
- Localizing chart text

Topics covered:
- **Accessibility:** WCAG 2.1 compliance features
- **ARIA:** Role, label, and description attributes
- **Keyboard:** Tab navigation and selection
- **Screen Readers:** Alternative text and descriptions
- **Printing:** Print method and configuration
- **Export:** Image export (PNG, JPG, SVG)
- **RTL:** Right-to-left language support
- **Localization:** Culture-specific formatting

---

### API Reference

📄 **Read:** [references/api-reference.md](references/api-reference.md)

Use this when:

- Looking up enum values and their exact names
- Understanding public method signatures and parameters
- Finding correct property types and default values
- Troubleshooting API usage issues
- Referencing quick code patterns
- Checking critical usage notes and gotchas

Topics covered:

- **Common Enums:** AccumulationType, AccumulationLabelPosition, GroupMode, LegendPosition, ExportType
- **Key Properties:** Type, InnerRadius, Radius, GroupTo, GroupMode, Visible, Enable
- **Public Methods:** ExportAsync, PrintAsync, Refresh, SetAnnotationValueAsync
- **Critical Usage Notes:** Center label restrictions, GroupTo semantics, enum qualification
- **Common Patterns:** Basic pie, doughnut with center label, grouping examples
- **Troubleshooting:** Label overlap, center label issues, enum compilation errors

---

## Quick Start Example

Here's a minimal pie chart implementation:

```razor
@page "/pie-chart"
@using Syncfusion.Blazor.Charts

<SfAccumulationChart Title="Sales Distribution">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@SalesData" 
                                 XName="Product" 
                                 YName="Sales">
            <AccumulationDataLabelSettings Visible="true" 
                                           Name="Product">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartLegendSettings Visible="true">
    </AccumulationChartLegendSettings>
</SfAccumulationChart>

@code {
    public class SalesInfo
    {
        public string Product { get; set; }
        public double Sales { get; set; }
    }

    public List<SalesInfo> SalesData = new List<SalesInfo>
    {
        new SalesInfo { Product = "Product A", Sales = 35 },
        new SalesInfo { Product = "Product B", Sales = 28 },
        new SalesInfo { Product = "Product C", Sales = 22 },
        new SalesInfo { Product = "Product D", Sales = 15 }
    };
}
```

## Common Patterns

### Doughnut Chart with Center Label

```razor
<SfAccumulationChart Title="Revenue by Region">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@RevenueData" 
                                 XName="Region" 
                                 YName="Revenue"
                                 InnerRadius="40%">
            <AccumulationDataLabelSettings Visible="true" Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
                <AccumulationChartConnector Length="20px">
                </AccumulationChartConnector>
            </AccumulationDataLabelSettings>
            <AccumulationChartCenterLabel 
                Text="Total<br/>$1.2M">
                <AccumulationChartCenterLabelFont 
                    Size="16px" 
                    FontWeight="600">
                </AccumulationChartCenterLabelFont>
            </AccumulationChartCenterLabel>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

### Funnel Chart for Conversion

```razor
<SfAccumulationChart Title="Sales Funnel">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@ConversionData" 
                                 XName="Stage" 
                                 YName="Count"
                                 Type="Syncfusion.Blazor.Charts.AccumulationType.Funnel"
                                 NeckWidth="25%"
                                 NeckHeight="10%">
            <AccumulationDataLabelSettings Visible="true" Name="Stage">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

### Grouped Pie Chart with Gradients

```razor
<SfAccumulationChart Title="Market Share Analysis">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@MarketData" 
                                 XName="Company" 
                                 YName="Share"
                                 GroupTo="5"
                                 GroupMode="Syncfusion.Blazor.Charts.GroupMode.Value">
            <AccumulationDataLabelSettings Visible="true" Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    <AccumulationChartLegendSettings Visible="true" Position="Syncfusion.Blazor.Charts.LegendPosition.Right">
    </AccumulationChartLegendSettings>
</SfAccumulationChart>

@code {
    // Data source with gradient applied
    public List<MarketInfo> MarketData = new List<MarketInfo>
    {
        new MarketInfo { Company = "Company A", Share = 35 },
        new MarketInfo { Company = "Company B", Share = 20 },
        new MarketInfo { Company = "Company C", Share = 15 },
        new MarketInfo { Company = "Others", Share = 30 }
    };
}
```

## Key Properties and Components

### SfAccumulationChart
- **Title:** Chart title text
- **Height/Width:** Chart dimensions
- **Theme:** Visual theme (Bootstrap5, Material, Fluent, etc.)
- **EnableAnimation:** Enable/disable load animation
- **SelectionMode:** Point or Series selection
- **Background:** Chart background color

### AccumulationChartSeries
- **DataSource:** Data collection to visualize
- **XName:** Property name for category/label
- **YName:** Property name for values
- **Type:** Pie (default), Doughnut, Funnel, Pyramid
- **InnerRadius:** Doughnut inner radius percentage
- **Radius:** Overall chart radius
- **StartAngle/EndAngle:** Arc positioning
- **GroupTo:** Value/point count threshold for grouping
- **GroupMode:** Value or Point grouping mode
- **Explode/ExplodeIndex:** Slice separation on load

### AccumulationDataLabelSettings
- **Visible:** Show/hide data labels
- **Name:** Property for label text
- **Position:** Inside or Outside placement
- **Format:** Value format string
- **MaxWidth:** Text wrap width
- **Template:** Custom HTML template

### AccumulationChartLegendSettings
- **Visible:** Show/hide legend
- **Position:** Top, Bottom, Left, Right
- **Height/Width:** Legend dimensions
- **ToggleVisibility:** Enable click to hide/show points

### AccumulationChartTooltipSettings
- **Enable:** Show/hide tooltips
- **Format:** Tooltip text format
- **Header:** Custom header text
- **Template:** Custom HTML template

## Public Methods

The `SfAccumulationChart` component provides the following public methods. For complete method signatures and additional details, see [api-reference.md](references/api-reference.md).

### ExportAsync
Exports the chart in the specified format.

```csharp
await chart.ExportAsync(ExportType.PNG, "chart.png");
```

**Parameters:**
- `type` (ExportType): PNG, JPEG, SVG, or PDF
- `fileName` (string): Name of the exported file
- `orientation` (PdfPageOrientation?): PDF orientation (Portrait/Landscape), optional
- `allowDownload` (bool): Whether to download the file, default is true

### PrintAsync
Prints the chart.

```csharp
await chart.PrintAsync();
```

### Refresh
Refreshes the chart with optional animation.

```csharp
chart.Refresh(shouldAnimate: true);
```

**Parameters:**
- `shouldAnimate` (bool): Whether to animate the refresh, default is true

### SetAnnotationValueAsync
Updates annotation content dynamically.

```csharp
await chart.SetAnnotationValueAsync(0, "Updated Content");
```

**Parameters:**
- `annotationIndex` (double): Index of the annotation to update
- `content` (string): New content for the annotation

## Common Use Cases

### Market Share Visualization
**Use pie or doughnut charts** to show competitive market distribution with legends identifying each company.

### Sales Pipeline Tracking
**Use funnel charts** to visualize stage-by-stage conversion in sales processes, showing drop-off at each step.

### Organizational Hierarchy
**Use pyramid charts** to display hierarchical structures like company organization or food chains.

### Survey Results Display
**Use pie charts with data labels** to present survey response distributions with clear percentage values.

### Financial Portfolio Composition
**Use doughnut charts with center labels** to show asset allocation with total value in the center.

### Regional Revenue Distribution
**Use pie charts with gradients** to highlight revenue contribution by geographic regions.

## See Also

- [Syncfusion Blazor Charts Overview](https://blazor.syncfusion.com/documentation/accumulation-chart)
- [Accumulation Chart API Reference](https://help.syncfusion.com/cr/blazor/Syncfusion.Blazor.Charts.SfAccumulationChart.html)
- [Blazor Accumulation Chart Demos](https://blazor.syncfusion.com/demos/chart/pie)
