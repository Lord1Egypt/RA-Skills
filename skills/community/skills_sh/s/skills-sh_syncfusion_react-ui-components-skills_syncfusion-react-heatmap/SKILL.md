---
name: syncfusion-react-heatmap
description: Implement Syncfusion React HeatMap Chart component for data visualization. Use this skill when user needs to create heatmaps, visualize 2D data patterns, display matrix data with color gradients, configure axes (numerical/categorical/datetime), implement legends, handle cell selection, apply custom styling, or work with large datasets. Covers installation, data binding, axis configuration, appearance customization, interaction patterns, tooltips, events, and accessibility.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React HeatMap Chart

The HeatMap component visualizes two-dimensional data using color gradients or fixed colors, making it ideal for analyzing patterns, correlations, and distributions across matrix data. Perfect for displaying heat patterns, activity matrices, performance data, and temporal correlations.

## When to Use This Skill

- **Visualizing 2D data patterns** - Display matrix data with color-coded cells
- **Creating heatmaps** - Build interactive heatmaps with custom color schemes
- **Analyzing correlations** - Show relationships between row and column variables
- **Displaying time-series patterns** - Visualize activity over time periods
- **Performance monitoring** - Display metrics across multiple dimensions
- **Data exploration** - Reveal patterns in large datasets at a glance
- **Configuring axes** - Set up numerical, categorical, or datetime axes
- **Customizing appearance** - Apply custom colors, legends, and styling
- **Handling user interaction** - Implement selection, tooltips, and event handling
- **Accessibility** - Ensure keyboard navigation and screen reader support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and setup steps
- Vite/React project configuration
- CSS imports and theme selection
- Basic component initialization
- **When:** Starting a new HeatMap implementation or setting up dependencies

### Data Binding & Setup
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- JSON data format and structure
- 2D array binding
- Data transformation techniques
- Loading and binding data dynamically
- **When:** Preparing data for the heatmap or learning data formats

### Axes Configuration
📄 **Read:** [references/axes-configuration.md](references/axes-configuration.md)
- Numerical, categorical, and datetime axis types
- Axis properties and customization
- Inverted and opposed axis positioning
- Axis intervals and label formatting
- **When:** Setting up row/column headers or configuring axis behavior

### Legend, Appearance & Styling
📄 **Read:** [references/legend-and-appearance.md](references/legend-and-appearance.md)
- Legend placement, format, and customization
- Color palettes and gradient configuration
- Sizing and dimension properties
- Rendering modes (SVG vs Canvas switching)
- Theme styling and CSS customization
- **When:** Customizing visual appearance, colors, or legends

### Interaction & Selection
📄 **Read:** [references/interaction-and-selection.md](references/interaction-and-selection.md)
- Selection modes and cell highlighting
- Mouse events and event handlers
- Tooltip configuration and customization
- Cell interaction patterns and best practices
- **When:** Implementing user interaction or handling cell clicks/hovers

### Advanced Features & Events
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Bubble heatmap implementation
- Complete event handling (select, click, hover, created)
- Automatic rendering mode switching
- Performance optimization for large datasets
- Custom rendering and cell styling
- **When:** Implementing advanced features or optimizing performance

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Comprehensive component API: props, methods, events, and model schemas
- Quick lookup for `cellSettings`, `legendSettings`, `paletteSettings`, `xAxis`, `yAxis`, `titleSettings`, `tooltipSettings`, and common methods like `export`, `print`, `clearSelection`
- **When:** Adding or validating props, wiring events, or implementing advanced customizations

### Accessibility & Troubleshooting
📄 **Read:** [references/accessibility-and-troubleshooting.md](references/accessibility-and-troubleshooting.md)
- WCAG compliance and accessibility features
- Keyboard navigation support
- ARIA attributes and screen reader support
- Common issues and solutions
- Migration from EJ1 to EJ2
- **When:** Ensuring accessibility or resolving issues

## Quick Start

```jsx
import * as React from 'react';
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';
import '@syncfusion/ej2-base/styles/material.css';

export function App() {
  const data = [
    [73, 39, 26, 39, 94],
    [93, 58, 53, 38, 26],
    [54, 39, 26, 40, 42]
  ];

  return (
    <HeatMapComponent 
      id='heatmap'
      dataSource={data}
      xAxis={{ labels: ['A', 'B', 'C', 'D', 'E'] }}
      yAxis={{ labels: ['X', 'Y', 'Z'] }}
      showTooltip={true}
      cellRender={(args) => {
        args.displayText = args.value + '%';
      }}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Basic Data Visualization
```jsx
// Visualize simple 2D data with default styling
<HeatMapComponent 
  dataSource={data}
  xAxis={{ labels: xLabels }}
  yAxis={{ labels: yLabels }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Pattern 2: Custom Colors, Legend, and Tooltips
```jsx
// Apply custom color palette with legend and styled tooltips
<HeatMapComponent 
  dataSource={data}
  paletteSettings={{
    type: 'Gradient',
    palette: [
      { value: 0, color: '#3498db' },
      { value: 50, color: '#2ecc71' },
      { value: 100, color: '#e74c3c' }
    ]
  }}
  legendSettings={{ position: 'Right', width: '150px' }}
  showTooltip={true}
  tooltipSettings={{
    fill: '#F5F5F5',
    textStyle: { color: '#333333', size: '13px' },
    border: { width: 1, color: '#999999' }
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Pattern 3: Interactive Cell Handling
```jsx
// Handle cell selection and display selected data
<HeatMapComponent 
  dataSource={data}
  cellSelected={(args) => {
    console.log(`Cell [${args.row}, ${args.column}] selected: ${args.value}`);
  }}
  cellRender={(args) => {
    args.displayText = args.value + ' units';
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Key Props

| Prop | Type | Purpose | Example |
|------|------|---------|---------|
| `dataSource` | Array | 2D data array or JSON | `[[1,2],[3,4]]` |
| `xAxis` | Object | Column axis configuration | `{ labels: ['A', 'B'] }` |
| `yAxis` | Object | Row axis configuration | `{ labels: ['X', 'Y'] }` |
| `paletteSettings` | Object | Color palette and gradient configuration | `{ type: 'Gradient', palette: [{value: 0, color: '#blue'}] }` |
| `cellRender` | Function | Custom cell formatting | Format display text |
| `cellSelected` | Function | Selection event handler | Track user selection |
| `legendSettings` | Object | Legend placement/format | `{ position: 'Right' }` |
| `showTooltip` | Boolean | Enable/disable tooltips | `true` or `false` |
| `tooltipSettings` | Object | Tooltip styling (fill, textStyle, border) | `{ fill: '#F5F5F5', textStyle: { color: '#333' } }` |
| `renderingMode` | String | SVG or Canvas | `'Canvas'` for large datasets |

## Common Use Cases

1. **Performance Dashboard** - Display metrics across departments and time periods
2. **Correlation Matrix** - Visualize relationships between variables
3. **Activity Heatmap** - Show user engagement patterns by day/hour
4. **Gene Expression** - Analyze biological data with color intensity
5. **Traffic Pattern** - Visualize network/website traffic distribution
6. **Survey Results** - Display response patterns across questions and demographics

---
