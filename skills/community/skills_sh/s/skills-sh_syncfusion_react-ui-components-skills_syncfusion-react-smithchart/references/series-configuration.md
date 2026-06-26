# Series Configuration

## Table of contents
- [Overview](series-configuration.md#overview)
- [Understanding Series Data](series-configuration.md#understanding-series-data)
- [Adding Series with Points](series-configuration.md#adding-series-with-points)
  - [Basic Points Configuration](series-configuration.md#basic-points-configuration)
  - [When to Use Points](series-configuration.md#when-to-use-points)
- [Adding Series with DataSource](series-configuration.md#adding-series-with-datasource)
  - [Basic DataSource Configuration](series-configuration.md#basic-datasource-configuration)
  - [When to Use DataSource](series-configuration.md#when-to-use-datasource)
  - [DataSource with Complex Objects](series-configuration.md#datasource-with-complex-objects)
- [Multiple Series](series-configuration.md#multiple-series)
  - [Multiple Series Example](series-configuration.md#multiple-series-example)
  - [Mixing Points and DataSource](series-configuration.md#mixing-points-and-datasource)
- [Series Customization](series-configuration.md#series-customization)
  - [`fill`](series-configuration.md#fill)
  - [`width`](series-configuration.md#width)
  - [`opacity`](series-configuration.md#opacity)
  - [`visibility`](series-configuration.md#visibility)
  - [`enableSmartLabels`](series-configuration.md#enablesmartlabels)
- [Complete Examples](series-configuration.md#complete-examples)
  - [Fully Customized Single Series](series-configuration.md#fully-customized-single-series)
  - [Multiple Series with Different Styles](series-configuration.md#multiple-series-with-different-styles)
  - [Dynamic Series with State](series-configuration.md#dynamic-series-with-state)
- [Best Practices](series-configuration.md#best-practices)
  - [Data Quality](series-configuration.md#data-quality)
  - [Series Organization](series-configuration.md#series-organization)
  - [Performance](series-configuration.md#performance)
  - [Visual Clarity](series-configuration.md#visual-clarity)
- [Common Patterns](series-configuration.md#common-patterns)
  - [Loading Data from API](series-configuration.md#loading-data-from-api)
  - [Computed Series Data](series-configuration.md#computed-series-data)

## Overview

You can add any number of series to a Smith Chart as needed. Using series settings, you can add or customize data, and lines are drawn for the points and data source added in the series. Each series can be customized independently with markers, data labels, animation, opacity, and other visual properties.

Smith Charts visualize transmission line data using resistance and reactance coordinates, making them essential for RF circuit analysis and impedance matching.

## Understanding Series Data

Series data in Smith Charts must contain two key values:
- **Resistance**: The resistive component of impedance
- **Reactance**: The reactive component of impedance

Both values should be numeric and represent normalized impedance values for proper plotting on the Smith Chart.

## Adding Series with Points

The `points` property allows you to provide data directly as an array of objects containing resistance and reactance values.

### Basic Points Configuration

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

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
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={transmissionData} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### When to Use Points

Use the `points` property when:
- You have static data defined in your component
- Data is already in the correct format (objects with resistance and reactance)
- You don't need field mapping from different property names
- The data structure is simple and straightforward

## Adding Series with DataSource

The `dataSource` property allows you to bind data with custom field names, providing more flexibility when working with different data structures.

### Basic DataSource Configuration

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const impedanceData = [
    { r: 0, x: 0.05 },
    { r: 0, x: 0.1 },
    { r: 0, x: 0.2 },
    { r: 0.3, x: 0.3 },
    { r: 0.5, x: 0.4 },
    { r: 1.0, x: 0.5 }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          dataSource={impedanceData}
          resistance="r"
          reactance="x"
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### When to Use DataSource

Use the `dataSource` property when:
- Data comes from an API with custom field names
- You need to map fields from a database or external source
- Field names don't match the default `resistance` and `reactance`
- You want more control over data binding

### DataSource with Complex Objects

```tsx
const rfMeasurements = [
  { id: 1, freq: '1GHz', res: 0.2, react: 0.1, phase: 45 },
  { id: 2, freq: '2GHz', res: 0.4, react: 0.2, phase: 60 },
  { id: 3, freq: '3GHz', res: 0.6, react: 0.3, phase: 75 },
  { id: 4, freq: '4GHz', res: 0.8, react: 0.4, phase: 80 }
];

<SmithchartSeriesDirective
  name="RF Measurements"
  dataSource={rfMeasurements}
  resistance="res"
  reactance="react"
/>
```

The Smith Chart will only use the specified `resistance` and `reactance` fields, ignoring other properties.

## Multiple Series

You can add multiple series to compare different transmission lines, circuit configurations, or frequency responses.

### Multiple Series Example

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const transmission1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.5, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const transmission2 = [
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.4, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.5 },
    { resistance: 1.5, reactance: 0.8 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      legendSettings={{ visible: true }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="50Ω Line"
          points={transmission1}
        />
        <SmithchartSeriesDirective
          name="75Ω Line"
          points={transmission2}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Mixing Points and DataSource

You can mix both methods in different series within the same chart:

```tsx
const directData = [
  { resistance: 0.2, reactance: 0.1 },
  { resistance: 0.4, reactance: 0.2 }
];

const apiData = [
  { r_value: 0.3, x_value: 0.15 },
  { r_value: 0.6, x_value: 0.3 }
];

<SmithchartSeriesCollectionDirective>
  <SmithchartSeriesDirective
    name="Direct Data"
    points={directData}
  />
  <SmithchartSeriesDirective
    name="API Data"
    dataSource={apiData}
    resistance="r_value"
    reactance="x_value"
  />
</SmithchartSeriesCollectionDirective>
```

## Series Customization

Each series can be customized independently using the following properties:

### fill

Customizes the line color for the series.

```tsx
<SmithchartSeriesDirective
  name="Transmission Line"
  points={data}
  fill="blue"
/>
```

Available color formats:
- Named colors: `"red"`, `"blue"`, `"green"`
- Hex colors: `"#FF5733"`, `"#3498DB"`
- RGB colors: `"rgb(255, 99, 71)"`
- RGBA colors: `"rgba(255, 99, 71, 0.5)"`

### width

Customizes the width of the series line in pixels.

```tsx
<SmithchartSeriesDirective
  name="Transmission Line"
  points={data}
  width={3}
/>
```

Default width is typically 2 pixels. Increase for emphasis or decrease for subtle lines.

### opacity

Controls the opacity of the series line (0 to 1, where 0 is transparent and 1 is fully opaque).

```tsx
<SmithchartSeriesDirective
  name="Transmission Line"
  points={data}
  opacity={0.7}
/>
```

Useful for:
- Showing multiple overlapping series
- De-emphasizing less important data
- Creating visual hierarchy

### visibility

Handles the visibility of the series. Set to `"Hidden"` to hide the series.

```tsx
<SmithchartSeriesDirective
  name="Transmission Line"
  points={data}
  visibility="Visible"  // or "Hidden"
/>
```

This is useful for:
- Conditional rendering based on user preferences
- Temporarily hiding series without removing them
- Dynamic series toggling

### enableSmartLabels

Places data labels on the Smith Chart without overlapping with each other.

```tsx
<SmithchartSeriesDirective
  name="Transmission Line"
  points={data}
  enableSmartLabels={true}
  marker={{
    visible: true,
    dataLabel: { visible: true }
  }}
/>
```

Smart labels automatically adjust position to prevent overlap, improving readability.

## Complete Examples

### Fully Customized Single Series

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const impedanceData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Custom Series Configuration' }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Impedance Match"
          points={impedanceData}
          fill="#FF6347"
          width={3}
          opacity={0.8}
          enableSmartLabels={true}
          marker={{
            visible: true,
            shape: 'Circle',
            height: 8,
            width: 8
          }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Multiple Series with Different Styles

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const series1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.8, reactance: 0.4 }
  ];

  const series2 = [
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  const series3 = [
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Multi-Series Comparison' }}
      legendSettings={{ visible: true, position: 'Bottom' }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Configuration A"
          points={series1}
          fill="#1E90FF"
          width={2}
          opacity={1}
        />
        <SmithchartSeriesDirective
          name="Configuration B"
          points={series2}
          fill="#32CD32"
          width={3}
          opacity={0.8}
        />
        <SmithchartSeriesDirective
          name="Configuration C"
          points={series3}
          fill="#FF6347"
          width={2}
          opacity={0.6}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Dynamic Series with State

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const [showSeries2, setShowSeries2] = React.useState(true);

  const series1Data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const series2Data = [
    { resistance: 0.2, reactance: 0.1 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  return (
    <div>
      <button onClick={() => setShowSeries2(!showSeries2)}>
        Toggle Series 2
      </button>
      
      <SmithchartComponent
        id="smithchart"
        legendSettings={{ visible: true }}
      >
        <Inject services={[SmithchartLegend]} />
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective
            name="Primary Line"
            points={series1Data}
            fill="blue"
          />
          <SmithchartSeriesDirective
            name="Secondary Line"
            points={series2Data}
            fill="red"
            visibility={showSeries2 ? "Visible" : "Hidden"}
          />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

## Best Practices

### Data Quality
- Ensure resistance and reactance values are valid numbers
- Avoid NaN, null, or undefined values
- Normalize impedance values appropriately for Smith Chart plotting

### Series Organization
- Use descriptive series names for legend clarity
- Limit the number of visible series to avoid visual clutter (3-5 recommended)
- Use contrasting colors for multiple series
- Apply different line widths to emphasize important series

### Performance
- For large datasets, consider data sampling or aggregation
- Limit the number of data points per series (50-100 points is typically sufficient)
- Use visibility property to temporarily hide series instead of removing them

### Visual Clarity
- Enable smart labels when using data labels with multiple series
- Use opacity to create visual hierarchy among series
- Choose colors with sufficient contrast for accessibility
- Consider line width and marker size for readability

## Common Patterns

### Loading Data from API

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const [seriesData, setSeriesData] = React.useState([]);

  React.useEffect(() => {
    fetch('/api/smith-chart-data')
      .then(response => response.json())
      .then(data => setSeriesData(data));
  }, []);

  return (
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          dataSource={seriesData}
          resistance="resistance"
          reactance="reactance"
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Computed Series Data

```tsx
function generateTransmissionLine(length: number, frequency: number) {
  const points = [];
  for (let i = 0; i <= 10; i++) {
    const resistance = i * 0.1;
    const reactance = Math.sin(i * frequency * length / 10) * 0.5;
    points.push({ resistance, reactance });
  }
  return points;
}

function App() {
  const line1 = generateTransmissionLine(1.0, 2.4);
  const line2 = generateTransmissionLine(1.5, 2.4);

  return (
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective name="1m Line" points={line1} fill="blue" />
        <SmithchartSeriesDirective name="1.5m Line" points={line2} fill="red" />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}
```

This comprehensive guide covers all aspects of series configuration in Smith Charts, providing you with the knowledge to effectively visualize transmission line and impedance data.
