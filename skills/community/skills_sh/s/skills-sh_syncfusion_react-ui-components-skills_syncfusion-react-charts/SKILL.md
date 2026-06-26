---
name: syncfusion-react-charts
description: "Implement Syncfusion React Charts component for data visualization. Use this when creating charts, configuring axes and series, or customizing visualization styles. This skill covers chart types, data binding, user interactions, financial indicators, accessibility features, and professional data visualization in React applications."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Charts"
---

# Implementing Syncfusion React Charts

## When to Use This Skill

Use this skill when you need to:
- Create and render charts (area, bar, column, line, scatter, etc.)
- Configure chart axes and customize their appearance
- Bind local data, remote data (DataManager), or use OData/WebAPI/custom adaptors
- Dynamically add, remove, or replace data points (`addPoint`, `removePoint`, `setData`)
- Customize chart appearance (colors, labels, legends, annotations)
- Configure data labels (must be placed inside `marker.dataLabel`, not directly on the series)
- Implement user interactions (selection, zooming, tooltips)
- Add financial indicators and technical analysis
- Handle accessibility and internationalization
- Troubleshoot chart rendering or data issues

## Component Overview

Syncfusion React Chart is a powerful data visualization component that supports 20+ chart types with extensive customization options. It's designed for building professional dashboards, reports, and analytics applications with interactive features like zooming, selection, and tooltips.

**Key Capabilities:**
- 20+ chart types (cartesian, polar, radar, pie, doughnut, and more)
- Multiple axes (category, numeric, date-time, logarithmic)
- Financial indicators and candlestick charts
- Advanced interactions (zoom, pan, crosshair, tooltip)
- Responsive design and accessibility support
- Print and export functionality

---

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete ChartComponent properties reference
- All methods and events documentation
- SeriesDirective properties
- Model interfaces (AxisModel, ZoomSettingsModel, etc.)
- Module services (series types, features, indicators)
- Official API documentation links

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Creating your first chart
- CSS imports and theme configuration
- Rendering basic chart examples
- Package structure overview

### Chart Types
📄 **Read:** [references/chart-types.md](references/chart-types.md)
- Overview of 20+ supported chart types
- When to use each chart type
- Basic examples for common types (Line, Bar, Column, Area, Scatter)
- Type-specific configurations
- Choosing the right chart for your data

### Axes and Customization
📄 **Read:** [references/axes-and-customization.md](references/axes-and-customization.md)
- Category, numeric, date-time, and logarithmic axes
- Axis labels and formatting
- Multiple axes configuration
- Range and interval settings
- Axis crossing and positioning

### Series and Data Binding
📄 **Read:** [references/series-and-data.md](references/series-and-data.md)
- Series configuration and properties
- Local data binding patterns
- Remote data binding using `DataManager`
- Data adaptors: `ODataAdaptor`, `ODataV4Adaptor`, `WebApiAdaptor`, custom adaptors
- Offline mode and lazy loading
- Dynamic data updates via `addPoint`, `removePoint`, `setData`, or React state
- Multiple series handling
- Data validation and edge cases

### Appearance and Styling
📄 **Read:** [references/appearance-and-styling.md](references/appearance-and-styling.md)
- Legend configuration and positioning
- Data labels and formatting
- Chart annotations
- Gradients and color customization
- Title, subtitle, and description styling

### User Interactions
📄 **Read:** [references/user-interaction.md](references/user-interaction.md)
- Selection and highlighting
- Zooming and panning
- Tooltip and crosshair configuration
- Synchronized charts
- Event handling patterns

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Financial chart types (candlestick, HLOC, high-low)
- Technical indicators (moving average, trend lines, etc.)
- Multiple panes and indicator panes
- Accessibility (WCAG compliance, keyboard navigation)
- Internationalization and localization

---

## Quick Start Example

```jsx
import { ChartComponent, SeriesCollectionDirective, SeriesDirective, Inject, LineSeries, Category, Legend, Tooltip } from '@syncfusion/ej2-react-charts';

export default function BasicChart() {
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: 28 },
    { x: 'Mar', y: 34 },
    { x: 'Apr', y: 32 },
    { x: 'May', y: 40 }
  ];

  return (
    <ChartComponent id='charts'>
      <Inject services={[LineSeries, Category, Legend, Tooltip]} />
      <SeriesCollectionDirective>
        <SeriesDirective dataSource={data} xName='x' yName='y' type='Line' />
      </SeriesCollectionDirective>
    </ChartComponent>
  );
}
```

---

## Common Patterns

### Pattern 1: Multi-Series Chart
When displaying multiple datasets that share the same axes, add multiple `SeriesDirective` components within `SeriesCollectionDirective`:

```jsx
<SeriesCollectionDirective>
  <SeriesDirective dataSource={salesData} xName='month' yName='revenue' type='Column' />
  <SeriesDirective dataSource={profitData} xName='month' yName='profit' type='Column' />
</SeriesCollectionDirective>
```

### Pattern 2: Dynamic Data Updates
Three approaches depending on the use case:

**a) React state (simple re-render):**
```jsx
const [data, setData] = useState(initialData);

const handleDataUpdate = () => {
  setData(prev => [...prev, { x: 'Jun', y: 45 }]);
};

<SeriesDirective dataSource={data} xName='x' yName='y' type='Line' />
```

**b) `addPoint` / `removePoint` / `setData` (imperative, with animation):**
```jsx
const chartRef = useRef(null);

// Add a point
chartRef.current.series[0].addPoint({ x: 'Jun', y: 45 }, 300);

// Remove first point
chartRef.current.series[0].removePoint(0, 300);

// Replace all data
chartRef.current.series[0].setData(newDataArray, 500);

<ChartComponent ref={chartRef} ...>
  <SeriesDirective dataSource={data} xName='x' yName='y' type='Line' />
</ChartComponent>
```

### Pattern 3: Remote Data Binding
Use `DataManager` with an adaptor to bind data from a REST API or OData service:

```jsx
import { DataManager, Query, WebApiAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'your data source URL link',
  adaptor: new WebApiAdaptor()
});

<SeriesDirective dataSource={dataManager} xName='CustomerID' yName='Freight' type='Column' query={new Query()} />
```

Other adaptors: `ODataAdaptor` (OData v3), `ODataV4Adaptor` (OData v4), custom adaptor by extending `ODataAdaptor`.

### Pattern 4: Data Labels (inside marker)
Data labels **must** be placed inside `marker.dataLabel`, not directly on the series. Inject `DataLabel` service:

```jsx
<Inject services={[LineSeries, Category, DataLabel]} />

<SeriesDirective
  dataSource={data}
  xName='x'
  yName='y'
  type='Line'
  marker={{
    visible: true,
    dataLabel: { visible: true, position: 'Top' }
  }}
/>
```

### Pattern 5: Custom Tooltips
Enhance user experience with formatted tooltip templates:

```jsx
<ChartComponent tooltip={{ enable: true, template: '<div>${point.x}: ${point.y}</div>' }}>
```

### Pattern 6: Responsive Design
Use container styling to make charts responsive:

```jsx
<ChartComponent id='charts' width='100%' height='400px'>
  {/* chart content */}
</ChartComponent>
```

---

## Key Props Reference

### ChartComponent
| Prop | Type | Purpose | When to Use |
|------|------|---------|-----------|
| `id` | string | Unique identifier | Required for each chart |
| `width` | string | Chart width (px or %) | Control layout sizing |
| `height` | string | Chart height | Set explicit dimensions |
| `title` | string | Chart title | Display main heading |
| `tooltip` | object | Tooltip configuration | Interactive data inspection |
| `primaryXAxis` | object | Primary X-axis config | Define horizontal axis |
| `primaryYAxis` | object | Primary Y-axis config | Define vertical axis |

### SeriesDirective
| Prop | Type | Purpose | When to Use |
|------|------|---------|-----------|
| `dataSource` | array \| DataManager | Data source | Bind local array or remote DataManager |
| `xName` | string | X-axis property | Map data field to X |
| `yName` | string | Y-axis property | Map data field to Y |
| `type` | string | Chart type | Select visualization type |
| `fill` | string | Series color | Customize series color |
| `marker` | object | Marker + data label config | Show point markers and/or data labels (`marker.dataLabel`) |
| `name` | string | Series name | Display in legend |
| `query` | Query | DataManager query | Filter/sort/paginate remote data |

---

## Common Use Cases

1. **Sales Dashboard**: Combine column chart for revenue with line series for trends
2. **Time Series Analysis**: Use date-time axis with line chart for temporal data
3. **Comparative Analysis**: Multi-series column charts comparing categories
4. **Financial Analysis**: Candlestick chart with moving average indicators
5. **Distribution Analysis**: Histogram or box-whisker charts for statistical data
6. **Real-time Monitoring**: Use `addPoint`/`removePoint` for live feeds with smooth animation
7. **Remote Data from REST API**: Bind `DataManager` with `WebApiAdaptor` or `ODataAdaptor` directly to series
8. **Server-side OData**: Use `ODataV4Adaptor` with a `Query` to filter and paginate at the server

---

## Next Steps

Choose the reference that matches your current need:
- **Need API details?** → [API Reference](references/api-reference.md)
- **Starting out?** → [Getting Started](references/getting-started.md)
- **Choosing chart type?** → [Chart Types](references/chart-types.md)
- **Configuring axes?** → [Axes and Customization](references/axes-and-customization.md)
- **Binding data?** → [Series and Data](references/series-and-data.md)
- **Styling appearance?** → [Appearance and Styling](references/appearance-and-styling.md)
- **Adding interactions?** → [User Interactions](references/user-interaction.md)
- **Advanced features?** → [Advanced Features](references/advanced-features.md)

## External Resources

- **Official API Documentation:** https://ej2.syncfusion.com/react/documentation/api/chart/
- **Live Demos:** https://ej2.syncfusion.com/react/demos/
- **GitHub Repository:** https://github.com/syncfusion/ej2-react-ui-components
