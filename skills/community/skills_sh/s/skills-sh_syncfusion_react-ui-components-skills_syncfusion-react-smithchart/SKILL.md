---
name: syncfusion-react-smithchart
description: Implements and customizes the Syncfusion React Smith Chart component for transmission line and RF circuit visualization. Use this when users need Smith Charts for impedance matching, RF design, or telecommunications data visualization. Covers series configuration, axis customization, markers, data labels, legend, tooltip, print/export, and accessibility features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Smith Charts

A comprehensive skill for implementing and customizing Syncfusion React Smith Chart component. Smith Charts are specialized diagrams used in electrical engineering and RF design to visualize impedance, reflection coefficients, and transmission line parameters.

## When to Use This Skill

Use this skill when you need to:
- Visualize transmission line impedance and reflection data
- Plot RF circuit parameters (S-parameters, impedance matching)
- Display resistance and reactance relationships
- Create interactive Smith Charts with markers and tooltips
- Implement electrical engineering data visualizations
- Configure Smith Chart axes (horizontal and radial)
- Add legends, data labels, and annotations
- Export Smith Charts for documentation or reports
- Ensure accessibility compliance for technical charts

## Component Overview

The Syncfusion React Smith Chart is a specialized charting component that:
- Plots data points with resistance and reactance coordinates
- Supports multiple series with customizable styling
- Provides horizontal and radial axis configurations
- Includes interactive features (tooltips, legends, markers)
- Offers print and export capabilities (PNG, JPEG, SVG, PDF)
- Ensures WCAG 2.2 accessibility compliance
- Supports responsive sizing and theming

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Dependencies and package installation
- Installing `@syncfusion/ej2-react-charts` via npm
- Basic SmithchartComponent implementation
- Module injection (SmithchartLegend, TooltipRender)
- CSS theme imports and configuration
- First render and initialization
- Complete working example

### Data and Series Configuration
📄 **Read:** [references/series-configuration.md](references/series-configuration.md)
- Adding multiple series to Smith Chart
- Two data binding methods (dataSource vs points)
- Resistance and reactance field mapping
- Series customization (fill, opacity, width, visibility)
- Smart label configuration
- Multi-series examples and patterns

### Axis Configuration
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)
- Horizontal axis (straight line) configuration
- Radial axis (circular path) configuration
- Label customization (position, intersection handling, styling)
- Major and minor gridlines configuration
- Axis line properties (width, dash patterns, visibility)
- Complete axis customization examples

### Visual Elements: Markers and Data Labels
📄 **Read:** [references/markers-and-labels.md](references/markers-and-labels.md)
- Enabling and customizing markers on data points
- Marker properties (size, shape, color, border, opacity)
- Data label implementation and smart positioning
- Data label styling (font, color, border)
- Best practices for visual clarity

### Legend Configuration
📄 **Read:** [references/legend-configuration.md](references/legend-configuration.md)
- Enabling legends with SmithchartLegend module
- Positioning (top, bottom, left, right, custom)
- Alignment options (near, center, far)
- Legend customization (shape, size, padding)
- Toggle visibility functionality
- Series naming for legend display

### Tooltips and Interactivity
📄 **Read:** [references/tooltip-configuration.md](references/tooltip-configuration.md)

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Enabling tooltips with TooltipRender module
- Per-series tooltip configuration
- Tooltip visibility and appearance
- When to use tooltips vs data labels
- Interactive hover behavior

### Appearance and Sizing
📄 **Read:** [references/dimensions-and-sizing.md](references/dimensions-and-sizing.md)
- Container-based sizing (CSS/inline styles)
- Fixed pixel dimensions
- Percentage-based responsive sizing
- Responsive design considerations
- When to use each sizing approach

### Title and Subtitle
📄 **Read:** [references/title-and-subtitle.md](references/title-and-subtitle.md)
- Adding descriptive titles to charts
- Subtitle configuration
- Title trimming for long text
- Font and alignment customization
- Visibility controls

### Print, Export, and Accessibility
📄 **Read:** [references/print-export-accessibility.md](references/print-export-accessibility.md)
- Printing Smith Charts directly from browser
- Exporting to multiple formats (PNG, JPEG, SVG, PDF)
- WCAG 2.2 and Section 508 compliance
- Keyboard navigation support
- Screen reader compatibility
- WAI-ARIA attributes
- Accessibility testing and best practices

## Quick Start Example

```tsx
import * as React from 'react';
import { SmithchartComponent, SeriesCollectionDirective, SeriesDirective, Inject, SmithchartLegend, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0, reactance: 0.1 },
    { resistance: 0, reactance: 0.2 },
    { resistance: 0.3, reactance: 0.3 },
    { resistance: 0.5, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Transmission Line Impedance' }}
      legendSettings={{ visible: true }}
    >
      <Inject services={[SmithchartLegend, TooltipRender]} />
      <SmithChartSeriesCollectionDirective>
        <SmithChartSeriesDirective
          name="Transmission1"
          points={transmissionData}
          marker={{ visible: true }}
          tooltip={{ visible: true }}
        />
      </SeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Common Patterns

### Multiple Series with DataSource

```tsx
const series1Data = [
  { resistance: 0, reactance: 0.05 },
  { resistance: 0.3, reactance: 0.2 },
  { resistance: 1.0, reactance: 0.4 }
];

const series2Data = [
  { resistance: 0.1, reactance: 0.1 },
  { resistance: 0.5, reactance: 0.3 },
  { resistance: 1.5, reactance: 0.5 }
];

<SmithchartComponent legendSettings={{ visible: true }}>
  <Inject services={[SmithchartLegend]} />
  <SmithChartSeriesCollectionDirective>
    <SmithChartSeriesDirective
      name="Line 1"
      dataSource={series1Data}
      resistance="resistance"
      reactance="reactance"
      fill="blue"
    />
    <SmithChartSeriesDirective
      name="Line 2"
      dataSource={series2Data}
      resistance="resistance"
      reactance="reactance"
      fill="red"
    />
  </SeriesCollectionDirective>
</SmithchartComponent>
```

### Customized Markers and Labels

```tsx
<SmithChartSeriesDirective
  name="Impedance Data"
  points={data}
  marker={{
    visible: true,
    height: 10,
    width: 10,
    shape: 'Diamond',
    fill: 'green',
    dataLabel: {
      visible: true,
      textStyle: { color: 'black', size: '10px' }
    }
  }}
/>
```

### Export to Image

```tsx
import { useRef } from 'react';

function ChartWithExport() {
  const chartRef = useRef(null);

  const exportChart = () => {
    chartRef.current.export('PNG', 'smithchart');
  };

  return (
    <>
      <button onClick={exportChart}>Export as PNG</button>
      <SmithchartComponent ref={chartRef} id="smithchart">
        {/* series configuration */}
      </SmithchartComponent>
    </>
  );
}
```

## Key Props and Features

### SmithchartComponent Props

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier for the component |
| `title` | object | Title configuration with text and styling |
| `legendSettings` | object | Legend visibility, position, and styling |
| `width` | string | Chart width (pixels or percentage) |
| `height` | string | Chart height (pixels or percentage) |
| `horizontalAxis` | object | Horizontal axis configuration |
| `radialAxis` | object | Radial axis configuration |

### SeriesDirective Props

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Series name for legend display |
| `points` | array | Array of {resistance, reactance} objects |
| `dataSource` | array | Data array with custom field mapping |
| `resistance` | string | Field name for resistance values |
| `reactance` | string | Field name for reactance values |
| `fill` | string | Series line color |
| `width` | number | Series line width |
| `opacity` | number | Series line opacity (0-1) |
| `marker` | object | Marker configuration |
| `tooltip` | object | Tooltip configuration |
| `enableSmartLabels` | boolean | Smart label positioning |

### Required Module Injections

```tsx
import { SmithchartLegend, TooltipRender } from '@syncfusion/ej2-react-charts';

<Inject services={[SmithchartLegend, TooltipRender]} />
```

- **SmithchartLegend**: Required for legend functionality
- **TooltipRender**: Required for tooltip display

## Troubleshooting Guide

### Chart Not Rendering
- Verify `@syncfusion/ej2-react-charts` package is installed
- Ensure CSS theme is imported in your app
- Check that data has valid `resistance` and `reactance` fields
- Confirm container has defined dimensions

### Legend Not Showing
- Verify `legendSettings.visible` is set to `true`
- Ensure `SmithchartLegend` module is injected
- Check that series have `name` property defined

### Tooltips Not Working
- Confirm `TooltipRender` module is injected
- Verify `tooltip.visible` is `true` on series
- Check that mouse hover events are enabled

### Data Not Displaying
- Validate data format: array of objects with resistance/reactance
- Check field names match dataSource property configuration
- Ensure numeric values are valid (not NaN or undefined)
- Verify series visibility is not set to false

### Export Fails
- Confirm chart has a valid `id` property
- Check export format is supported (PNG, JPEG, SVG, PDF)
- Ensure export method is called on mounted component reference

### Styling Issues
- Import correct Syncfusion theme CSS file
- Check that custom styles don't conflict with component classes
- Verify width/height properties are properly formatted
- Ensure container styling allows chart to render

## Additional Resources

All detailed documentation is available in the reference files above. Each reference file is self-contained with complete examples, configuration options, and best practices specific to that feature area.
