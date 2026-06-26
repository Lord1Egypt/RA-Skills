---
name: syncfusion-react-3d-circular-chart
description: Implements the Syncfusion React 3D Circular Chart component for pie and donut chart visualization. Use this when users need 3D circular charts, data labels, legends, tooltips, or empty point handling. Guides through installation, configuration, customization, and troubleshooting of 3D Circular Charts in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React 3D Circular Charts

A comprehensive skill for implementing Syncfusion's React 3D Circular Chart component. This skill guides you through creating pie and donut charts with 3D visualization, data labels, legends, tooltips, and advanced customization options.

## When to Use This Skill

Use this skill when you need to:
- Create 3D pie or donut charts in React applications
- Visualize proportional data with circular charts
- Display data with 3D depth and visual appeal
- Add interactive tooltips and legends to charts
- Customize chart appearance with data labels
- Handle empty or null data points gracefully
- Export charts to various formats (PNG, JPEG, SVG, PDF)
- Print charts directly from the browser
- Implement responsive circular chart visualizations

## Component Overview

The 3D Circular Chart component provides:
- **Pie and Donut Charts:** Classic circular visualizations with 3D depth
- **Flexible Data Binding:** Easy mapping of data sources to chart series
- **Interactive Features:** Tooltips, legends, and click events
- **Visual Customization:** Data labels, colors, and radius configurations
- **Export Options:** Print and export to multiple formats
- **Empty Point Handling:** Smart handling of null/undefined values
- **Responsive Design:** Adapts to container size automatically

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies
- Setting up React application with Vite or Create React App
- Adding 3D Circular Chart component to your project
- Importing CSS themes
- Basic pie series implementation with data source
- Mapping data fields with xName and yName properties
- Running your first 3D Circular Chart
- Minimal working example

### Pie and Donut Charts
📄 **Read:** [references/pie-donut-charts.md](references/pie-donut-charts.md)
- Injecting PieSeries3D module
- Rendering default pie charts
- Customizing chart radius (default 80% of container)
- Creating various radius pie charts with per-slice customization
- Implementing donut charts using innerRadius property
- Text and fill color mapping from data source
- Customizing individual points with pointRender event
- Complete examples for pie and donut variations

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling data label visibility
- Injecting CircularChartDataLabel3D module
- Smart label arrangement to prevent overlap
- Positioning labels inside or outside the chart
- Creating custom templates with placeholders
- Formatting text and styling labels
- Configuring connector lines
- Font customization for data labels

### Legend
📄 **Read:** [references/legend.md](references/legend.md)
- Enabling legend visibility
- Injecting CircularChartLegend3D module
- Positioning legends (left, right, top, bottom)
- Alignment options (center, far, near)
- Reversing legend item order
- Legend pagination for many items
- Shape and marker customization
- Styling and click behavior configuration

### Tooltip
📄 **Read:** [references/tooltip.md](references/tooltip.md)
- Enabling tooltip on hover
- Injecting CircularChartTooltip3D module
- Setting custom tooltip headers
- Format string customization with placeholders
- Creating tooltip templates
- Displaying series names and point values
- Styling tooltip appearance
- Event-based tooltip customization

### Empty Points
📄 **Read:** [references/empty-points.md](references/empty-points.md)
- Understanding empty points (null/undefined values)
- Configuring emptyPointSettings property
- Mode options: Gap, Average, Drop, Zero
- Gap mode: skipping empty data points
- Average mode: using calculated averages
- Drop mode: excluding from chart
- Zero mode: treating as zero values
- Custom fill colors for empty points

### Title and Subtitle
📄 **Read:** [references/title-and-subtitle.md](references/title-and-subtitle.md)
- Adding chart titles with title property
- Title positioning and alignment
- Customizing title style (font, color, size)
- Adding subtitles with subTitle property
- Subtitle positioning
- Styling subtitles independently
- Combining title and subtitle
- Responsive title sizing

### Print and Export
📄 **Read:** [references/print-and-export.md](references/print-and-export.md)
- Printing charts directly from browser
- Using print method with chart ID
- Exporting to image formats (JPEG, PNG, SVG)
- Exporting to PDF with pdfExport method
- Specifying export type and filename
- Button-triggered print and export
- Export quality and resolution settings
- Troubleshooting export issues

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Summary of component properties, methods, and events based on the official Syncfusion API docs for `CircularChart3DComponent`.

## Quick Start Example

```tsx
import { CircularChart3DComponent, CircularChart3DSeriesCollectionDirective, CircularChart3DSeriesDirective, PieSeries3D, CircularChartDataLabel3D, CircularChartLegend3D, Inject } from '@syncfusion/ej2-react-charts';
import * as React from "react";
import * as ReactDOM from "react-dom";
function App() {
    const circularData = [
        { x: 'Chrome', y: 62.92 },
        { x: 'Internet Explorer', y: 6.12 },
        { x: 'Opera', y: 3.15 },
        { x: 'Edge', y: 5.5 },
        { x: 'Safari', y: 19.97 },
        { x: 'Others', y: 2.34 }
    ];
    return <CircularChart3DComponent id='charts' title='Browser Market Shares in November 2023' tilt={-45} legendSettings={{ visible: true, position: 'Right' }}>
        <Inject services={[PieSeries3D, CircularChartDataLabel3D, CircularChartLegend3D]} />
        <CircularChart3DSeriesCollectionDirective>
            <CircularChart3DSeriesDirective dataSource={circularData} xName='x' yName='y' dataLabel={{ visible: true, position: 'Outside', name: 'x', font: { fontWeight: '600' }, connectorStyle: { length: '40px' } }}>
            </CircularChart3DSeriesDirective>
        </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>;
}
export default App;
const root = ReactDOM.createRoot(document.getElementById('charts'));
root.render(<App />);
```

## Common Patterns

### Creating a Donut Chart
```tsx
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
  innerRadius="40%"  // Creates donut effect
  radius="80%"
/>
```

### Adding Data Labels
```tsx
import { CircularChartDataLabel3D } from '@syncfusion/ej2-react-charts';

<CircularChart3DComponent>
  <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
  <CircularChart3DSeries>
    <CircularChart3DSeriesDirective
      dataSource={data}
      xName="x"
      yName="y"
      dataLabel={{ visible: true, position: 'Outside' }}
    />
  </CircularChart3DSeries>
</CircularChart3DComponent>
```

### Enabling Legend and Tooltip
```tsx
import { CircularChartLegend3D, CircularChartTooltip3D } from '@syncfusion/ej2-react-charts';

<CircularChart3DComponent
  legendSettings={{ visible: true, position: 'Bottom' }}
  tooltip={{ enable: true, format: '${point.x}: ${point.y}' }}
>
  <Inject services={[PieSeries3D, CircularChartLegend3D, CircularChartTooltip3D]} />
  {/* Series configuration */}
</CircularChart3DComponent>
```

### Handling Empty Points
```tsx
<CircularChart3DSeriesDirective
  dataSource={dataWithNulls}
  xName="category"
  yName="value"
  emptyPointSettings={{ 
    mode: 'Average',  // Options: Gap, Average, Drop, Zero
    fill: '#cccccc'
  }}
/>
```

## Key Props Reference

### CircularChart3DComponent Props
- **title**: Chart title text
- **subTitle**: Chart subtitle text
- **legendSettings**: Configure legend appearance and behavior
- **tooltip**: Enable and customize tooltips
- **enableExport**: Enable export functionality
- **width/height**: Chart dimensions

### CircularChart3DSeriesDirective Props
- **dataSource**: Array of data objects
- **xName**: Property name for category/label
- **yName**: Property name for values
- **radius**: Chart radius (percentage string, e.g., "70%")
- **innerRadius**: Inner radius for donut charts (percentage)
- **dataLabel**: Configuration for data labels
- **emptyPointSettings**: Handling null/undefined values
- **pointColorMapping**: Map colors from data source

### Module Injection
Required modules must be injected via `<Inject services={[...]} />`:
- **PieSeries3D**: Core pie/donut chart functionality
- **CircularChartDataLabel3D**: Data label features
- **CircularChartLegend3D**: Legend functionality
- **CircularChartTooltip3D**: Tooltip features
- **CircularChart3DExport**: Export to image formats
- **CircularChart3DPdfExport**: PDF export capability

## Common Use Cases

### Sales Distribution Dashboard
Perfect for displaying market share, sales by category, or revenue distribution across products/regions.

### Budget Allocation
Visualize budget breakdown by department, expense categories, or cost centers with clear proportional representation.

### Survey Results
Show poll results, customer feedback distribution, or demographic breakdowns with intuitive circular visualization.

### Portfolio Composition
Display investment allocation, asset distribution, or resource allocation with interactive charts.

### Time Allocation
Represent time spent on activities, project phases, or resource utilization with donut charts.

## Troubleshooting Tips

**Chart not rendering?**
- Ensure you've installed `@syncfusion/ej2-react-charts` package
- Import required CSS theme file
- Verify data source is properly formatted array
- Check that required modules are injected (PieSeries3D)

**Data labels overlapping?**
- The component automatically arranges labels to prevent overlap
- Use `position: 'Outside'` for better spacing
- Consider reducing font size or using templates

**Export not working?**
- Inject CircularChart3DExport or CircularChart3DPdfExport modules
- Set `enableExport: true` on the chart component
- Ensure you're calling the correct method (export or pdfExport)

**Colors not displaying correctly?**
- Use `pointColorMapping` to map colors from data source
- Specify colors in data objects or use chart palettes
- Check CSS theme is properly imported

---

**Ready to build?** Start with [references/getting-started.md](references/getting-started.md) for installation and basic setup, then explore specific features as needed.
