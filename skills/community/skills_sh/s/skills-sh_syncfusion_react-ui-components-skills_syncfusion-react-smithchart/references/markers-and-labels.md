# Markers and Data Labels

## Table of contents
- [Overview](markers-and-labels.md#overview)
- [Markers](markers-and-labels.md#markers)
  - [Enabling Markers](markers-and-labels.md#enabling-markers)
  - [Marker Customization](markers-and-labels.md#marker-customization)
    - [width and height](markers-and-labels.md#width-and-height)
    - [fill](markers-and-labels.md#fill)
    - [opacity](markers-and-labels.md#opacity)
    - [border](markers-and-labels.md#border)
    - [shape](markers-and-labels.md#shape)
    - [Complete Marker Example](markers-and-labels.md#complete-marker-example)
- [Data Labels](markers-and-labels.md#data-labels)
  - [Enabling Data Labels](markers-and-labels.md#enabling-data-labels)
  - [Smart Label Arrangement](markers-and-labels.md#smart-label-arrangement)
  - [Data Label Customization](markers-and-labels.md#data-label-customization)
    - [fill](markers-and-labels.md#fill-1)
    - [opacity](markers-and-labels.md#opacity-1)
    - [border](markers-and-labels.md#border-1)
    - [textStyle](markers-and-labels.md#textstyle)
    - [Complete Data Label Example](markers-and-labels.md#complete-data-label-example)
- [Complete Examples](markers-and-labels.md#complete-examples)
- [Best Practices](markers-and-labels.md#best-practices)
  - [Marker Selection](markers-and-labels.md#marker-selection)
  - [Marker size guidelines](markers-and-labels.md#marker-size-guidelines)
  - [Shape selection](markers-and-labels.md#shape-selection)
  - [Data Label Usage](markers-and-labels.md#data-label-usage)
  - [Color and Contrast](markers-and-labels.md#color-and-contrast)
  - [Performance Considerations](markers-and-labels.md#performance-considerations)
  - [Visual Hierarchy](markers-and-labels.md#visual-hierarchy)
- [Common Patterns](markers-and-labels.md#common-patterns)
  - [Conditional Marker Visibility](markers-and-labels.md#conditional-marker-visibility)
  - [Series-Specific Styling](markers-and-labels.md#series-specific-styling)
  - [Responsive Marker Sizing](markers-and-labels.md#responsive-marker-sizing)

## Overview

Markers and data labels provide information about individual data points in Smith Chart series. Markers are visual shapes that highlight data points, while data labels display the actual values. By default, both are disabled, but they can be enabled and extensively customized for each series independently.

## Markers

Markers are shapes (circles, diamonds, triangles, etc.) that adorn each data point on the series line. They improve visibility and help users identify specific measurement points.

### Enabling Markers

Set the `visible` property to `true` in the `marker` object:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.8, reactance: 0.4 }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          points={data}
          marker={{ visible: true }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Marker Customization

Each series can have uniquely styled markers using the following properties:

### width and height

Control the size of markers in pixels.

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    width: 10,
    height: 10
  }}
/>
```

**Recommendations:**
- Small markers (6-8px): For dense data with many points
- Medium markers (10-12px): Standard visibility
- Large markers (14-16px): Emphasis on specific series

### fill

Customizes the fill color of the marker.

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    fill: '#FF5733'
  }}
/>
```

Supported color formats:
- Named colors: `'red'`, `'blue'`, `'green'`
- Hex: `'#FF5733'`, `'#3498DB'`
- RGB: `'rgb(255, 99, 71)'`
- RGBA: `'rgba(255, 99, 71, 0.8)'`

### opacity

Controls the transparency of the marker (0 to 1).

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    opacity: 0.7
  }}
/>
```

Use opacity to:
- Create visual hierarchy
- Show overlapping markers more clearly
- De-emphasize less important data points

### border

Customizes the border of markers with `width` and `color` properties.

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    border: {
      width: 2,
      color: '#333333'
    }
  }}
/>
```

Borders improve marker visibility against similar-colored backgrounds.

### shape

Changes the geometric shape of the marker.

**Available shapes:**
- `'Circle'` (default)
- `'Rectangle'`
- `'Triangle'`
- `'Diamond'`
- `'Pentagon'`
- `'InvertedTriangle'`

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    shape: 'Diamond'
  }}
/>
```

Use different shapes to distinguish between multiple series when colors alone aren't sufficient.

### Complete Marker Example

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Custom Markers' }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Transmission Line"
          points={transmissionData}
          marker={{
            visible: true,
            width: 12,
            height: 12,
            shape: 'Diamond',
            fill: '#e74c3c',
            opacity: 0.9,
            border: {
              width: 2,
              color: '#c0392b'
            }
          }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Data Labels

Data labels display the resistance and reactance values directly on the chart at each data point, improving readability when space allows.

### Enabling Data Labels

Set the `visible` property to `true` in the `dataLabel` object within marker settings:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          points={data}
          marker={{
            visible: true,
            dataLabel: {
              visible: true
            }
          }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Smart Label Arrangement

Data labels are automatically arranged to avoid overlapping with each other, improving chart readability. This smart positioning is built-in and requires no additional configuration.

## Data Label Customization

Customize data labels using the following properties:

### fill

Changes the background color of the data label shape.

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    dataLabel: {
      visible: true,
      fill: '#ffffff'
    }
  }}
/>
```

### opacity

Controls the transparency of the data label background (0 to 1).

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    dataLabel: {
      visible: true,
      opacity: 0.8
    }
  }}
/>
```

### border

Customizes the border around data labels.

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    dataLabel: {
      visible: true,
      border: {
        width: 1,
        color: '#cccccc'
      }
    }
  }}
/>
```

### textStyle

Customizes the font properties of data label text.

**Available properties:**
- `size` - Font size (e.g., '10px', '12px')
- `color` - Text color
- `fontFamily` - Font family name
- `fontWeight` - Font weight ('Normal', 'Bold')
- `opacity` - Text opacity (0 to 1)

```tsx
<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    dataLabel: {
      visible: true,
      textStyle: {
        size: '11px',
        color: '#333333',
        fontFamily: 'Arial',
        fontWeight: 'Bold',
        opacity: 1
      }
    }
  }}
/>
```

### Complete Data Label Example

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const impedanceData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Impedance with Data Labels' }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Impedance Data"
          points={impedanceData}
          marker={{
            visible: true,
            width: 10,
            height: 10,
            shape: 'Circle',
            dataLabel: {
              visible: true,
              fill: '#ffffff',
              opacity: 0.9,
              border: {
                width: 1,
                color: '#3498db'
              },
              textStyle: {
                size: '10px',
                color: '#2c3e50',
                fontFamily: 'Segoe UI',
                fontWeight: 'Normal'
              }
            }
          }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Complete Examples

### Multiple Series with Different Markers

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const series1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.4, reactance: 0.25 },
    { resistance: 0.9, reactance: 0.45 }
  ];

  const series2 = [
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.1, reactance: 0.55 }
  ];

  const series3 = [
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Multiple Series Comparison' }}
      legendSettings={{ visible: true, position: 'Bottom' }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="50Ω Line"
          points={series1}
          fill="#3498db"
          marker={{
            visible: true,
            width: 10,
            height: 10,
            shape: 'Circle',
            fill: '#3498db',
            border: { width: 2, color: '#2980b9' }
          }}
        />
        <SmithchartSeriesDirective
          name="75Ω Line"
          points={series2}
          fill="#e74c3c"
          marker={{
            visible: true,
            width: 10,
            height: 10,
            shape: 'Diamond',
            fill: '#e74c3c',
            border: { width: 2, color: '#c0392b' }
          }}
        />
        <SmithchartSeriesDirective
          name="100Ω Line"
          points={series3}
          fill="#2ecc71"
          marker={{
            visible: true,
            width: 10,
            height: 10,
            shape: 'Triangle',
            fill: '#2ecc71',
            border: { width: 2, color: '#27ae60' }
          }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Markers with Data Labels

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.7, reactance: 0.4 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Transmission Line Analysis' }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Measured Data"
          points={transmissionData}
          fill="#9b59b6"
          width={2}
          marker={{
            visible: true,
            width: 12,
            height: 12,
            shape: 'Diamond',
            fill: '#9b59b6',
            opacity: 0.9,
            border: {
              width: 2,
              color: '#8e44ad'
            },
            dataLabel: {
              visible: true,
              fill: '#ffffff',
              opacity: 0.95,
              border: {
                width: 1,
                color: '#9b59b6'
              },
              textStyle: {
                size: '11px',
                color: '#2c3e50',
                fontFamily: 'Arial',
                fontWeight: 'Bold'
              }
            }
          }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### High-Visibility Configuration

For presentations or printed materials:

```tsx
<SmithchartSeriesDirective
  name="Key Measurements"
  points={data}
  fill="#000000"
  theme={'Material'}
  width={3}
  marker={{
    visible: true,
    width: 14,
    height: 14,
    shape: 'Circle',
    fill: '#FFD700',
    opacity: 1,
    border: {
      width: 3,
      color: '#000000'
    },
    dataLabel: {
      visible: true,
      fill: '#ffffff',
      opacity: 1,
      border: {
        width: 2,
        color: '#000000'
      },
      textStyle: {
        size: '13px',
        color: '#000000',
        fontWeight: 'Bold'
      }
    }
  }}
/>
```

### Subtle Markers for Dense Data

When plotting many data points:

```tsx
<SmithchartSeriesDirective
  name="High-Density Data"
  points={denseData}
  marker={{
    visible: true,
    width: 6,
    height: 6,
    shape: 'Circle',
    opacity: 0.6,
    border: {
      width: 1,
      color: '#3498db'
    },
    dataLabel: {
      visible: false  // Disable labels for dense data
    }
  }}
/>
```

## Best Practices

### Marker Selection

**When to use markers:**
- Highlighting specific measurement points
- Distinguishing between multiple series
- Drawing attention to key data points
- Improving click/touch targeting for interactive charts

**Marker size guidelines:**
- Dense data (20+ points): 6-8px
- Standard data (5-15 points): 10-12px
- Sparse data (<5 points): 12-16px
- Emphasis points: 14-18px

**Shape selection:**
- Use different shapes for different series types
- Choose simple shapes for small markers
- Consider cultural or domain conventions (e.g., circles for measurements)

### Data Label Usage

**When to use data labels:**
- Few data points with space for labels (<10 points)
- Exact values are critical for interpretation
- Presentation or documentation requirements
- When tooltips aren't available

**When to avoid data labels:**
- Dense data with many points (causes clutter)
- When interactive tooltips provide the same information
- Limited chart space
- Values are relative rather than absolute

### Color and Contrast

- Ensure marker colors contrast with series line colors
- Use borders to improve marker visibility
- Test color combinations for accessibility (WCAG guidelines)
- Avoid relying solely on color to distinguish series

### Performance Considerations

- Limit marker count for large datasets (consider data sampling)
- Disable data labels for datasets with >15 points per series
- Use simpler marker shapes for better rendering performance
- Consider marker opacity to reduce visual weight

### Visual Hierarchy

1. **Primary series**: Larger markers (12-14px), high opacity, bold borders
2. **Secondary series**: Medium markers (10px), standard styling
3. **Reference series**: Smaller markers (8px), lower opacity, subtle styling

## Common Patterns

### Conditional Marker Visibility

Show markers only for specific conditions:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const [showMarkers, setShowMarkers] = React.useState(true);

  return (
    <>
      <button onClick={() => setShowMarkers(!showMarkers)}>
        Toggle Markers
      </button>
      <SmithchartComponent id="smithchart">
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective
            points={data}
            marker={{
              visible: showMarkers,
              width: 10,
              height: 10
            }}
          />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </>
  );
}
```

### Series-Specific Styling

Different styling for different data characteristics:

```tsx
<SmithchartSeriesCollectionDirective>
  {/* Measured data: prominent markers */}
  <SmithchartSeriesDirective
    name="Measured"
    points={measuredData}
    marker={{
      visible: true,
      width: 12,
      height: 12,
      shape: 'Diamond',
      fill: '#e74c3c'
    }}
  />
  
  {/* Simulated data: subtle markers */}
  <SmithchartSeriesDirective
    name="Simulated"
    points={simulatedData}
    marker={{
      visible: true,
      width: 8,
      height: 8,
      shape: 'Circle',
      opacity: 0.5,
      fill: '#95a5a6'
    }}
  />
</SmithchartSeriesCollectionDirective>
```

### Responsive Marker Sizing

Adjust marker size based on data point count:

```tsx
function getMarkerSize(dataLength: number) {
  if (dataLength > 20) return { width: 6, height: 6 };
  if (dataLength > 10) return { width: 10, height: 10 };
  return { width: 14, height: 14 };
}

const markerSize = getMarkerSize(data.length);

<SmithchartSeriesDirective
  points={data}
  marker={{
    visible: true,
    ...markerSize
  }}
/>
```

This comprehensive guide covers all aspects of markers and data labels in Smith Charts, enabling you to create clear, readable, and professional visualizations for transmission line and RF circuit analysis.
