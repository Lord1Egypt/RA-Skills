# Legend Configuration

## Table of contents
- [Overview](legend-configuration.md#overview)
- [Enabling Legend](legend-configuration.md#enabling-legend)
- [Position and Alignment](legend-configuration.md#position-and-alignment)
  - [Position](legend-configuration.md#position)
  - [Standard Positions](legend-configuration.md#standard-positions)
  - [Custom Position](legend-configuration.md#custom-position)
  - [Alignment](legend-configuration.md#alignment)
- [Legend Customization](legend-configuration.md#legend-customization)
  - [Legend Shape](legend-configuration.md#legend-shape)
  - [Legend Size](legend-configuration.md#legend-size)
  - [Legend Padding](legend-configuration.md#legend-padding)
    - [itemPadding](legend-configuration.md#itempadding)
    - [shapePadding](legend-configuration.md#shapepadding)
- [Toggle Visibility](legend-configuration.md#toggle-visibility)
- [Complete Examples](legend-configuration.md#complete-examples)
  - [Fully Customized Legend](legend-configuration.md#fully-customized-legend)
  - [Legend with Custom Position](legend-configuration.md#legend-with-custom-position)
  - [Compact Legend for Dashboards](legend-configuration.md#compact-legend-for-dashboards)
  - [Presentation-Ready Legend](legend-configuration.md#presentation-ready-legend)
- [Best Practices](legend-configuration.md#best-practices)
  - [Position Selection](legend-configuration.md#position-selection)
  - [Alignment Guidelines](legend-configuration.md#alignment-guidelines)
  - [Shape Selection](legend-configuration.md#shape-selection)
  - [Size Recommendations](legend-configuration.md#size-recommendations)
  - [Padding Guidelines](legend-configuration.md#padding-guidelines)
  - [Toggle Visibility](legend-configuration.md#toggle-visibility-1)
- [Common Patterns](legend-configuration.md#common-patterns)
  - [Dynamic Legend Position](legend-configuration.md#dynamic-legend-position)
  - [Conditional Legend Visibility](legend-configuration.md#conditional-legend-visibility)
  - [Series Name Formatting](legend-configuration.md#series-name-formatting)

## Overview

Legends are keys used in Smith Charts that contain symbols and descriptions. They provide valuable information for interpreting what the chart displays, showing series names with corresponding colors, shapes, or other identifiers. Legends help users quickly identify and distinguish between multiple data series.

## Enabling Legend

By default, legend visibility is false. To enable the legend, you must:

1. Set the `visible` property to `true` in `legendSettings`
2. Inject the `SmithchartLegend` module

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const transmission1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const transmission2 = [
    { resistance: 0.2, reactance: 0.1 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      legendSettings={{ visible: true }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Transmission Line 1"
          points={transmission1}
        />
        <SmithchartSeriesDirective
          name="Transmission Line 2"
          points={transmission2}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

**Important:** Each series should have a `name` property for legend display. Without names, legends will show generic labels.

## Position and Alignment

### Position

The `position` property controls where the legend appears relative to the chart.

**Available positions:**
- `'Top'` - Above the chart
- `'Bottom'` - Below the chart (default)
- `'Left'` - Left side of the chart
- `'Right'` - Right side of the chart
- `'Custom'` - Custom coordinates using x and y properties

#### Standard Positions

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const data1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 }
  ];

  const data2 = [
    { resistance: 0.2, reactance: 0.1 },
    { resistance: 0.7, reactance: 0.4 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      legendSettings={{
        visible: true,
        position: 'Top'  // 'Top', 'Bottom', 'Left', or 'Right'
      }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective name="Series 1" points={data1} />
        <SmithchartSeriesDirective name="Series 2" points={data2} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

#### Custom Position

For precise legend placement, use custom positioning with x and y coordinates:

```tsx
<SmithchartComponent
  id="smithchart"
  legendSettings={{
    visible: true,
    position: 'Custom',
    x: 50,   // X coordinate in pixels
    y: 10    // Y coordinate in pixels
  }}
>
  <Inject services={[SmithchartLegend]} />
  {/* series configuration */}
</SmithchartComponent>
```

**Use custom positioning when:**
- Standard positions don't meet layout requirements
- You need legends overlaying the chart
- Building custom dashboard layouts
- Integrating with other UI elements

### Alignment

The `alignment` property controls legend alignment within its positioned area.

**Available alignments:**
- `'Near'` - Aligns to the start (left for horizontal, top for vertical)
- `'Center'` - Centers the legend (default)
- `'Far'` - Aligns to the end (right for horizontal, bottom for vertical)

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const data1 = [{ resistance: 0, reactance: 0.05 }, { resistance: 0.5, reactance: 0.3 }];
  const data2 = [{ resistance: 0.2, reactance: 0.1 }, { resistance: 0.7, reactance: 0.4 }];

  return (
    <SmithchartComponent
      id="smithchart"
      legendSettings={{
        visible: true,
        position: 'Bottom',
        alignment: 'Far'  // 'Near', 'Center', or 'Far'
      }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective name="Line 1" points={data1} />
        <SmithchartSeriesDirective name="Line 2" points={data2} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Legend Customization

### Legend Shape

The `shape` property changes the symbol displayed in the legend.

**Available shapes:**
- `'Circle'` (default)
- `'Rectangle'`
- `'Triangle'`
- `'Diamond'`
- `'Pentagon'`
- `'InvertedTriangle'`

```tsx
<SmithchartComponent
  id="smithchart"
  legendSettings={{
    visible: true,
    shape: 'Rectangle'
  }}
>
  <Inject services={[SmithchartLegend]} />
  {/* series configuration */}
</SmithchartComponent>
```

The shape color automatically matches the series color.

### Legend Size

Control legend dimensions using `width` and `height` properties.

**Default behavior:**
- Horizontal position (Top/Bottom): Legend takes 20-25% of chart height
- Vertical position (Left/Right): Legend takes 20-25% of chart width

**Custom sizing:**

```tsx
<SmithchartComponent
  id="smithchart"
  legendSettings={{
    visible: true,
    width: '200px',
    height: '100px'
  }}
>
  <Inject services={[SmithchartLegend]} />
  {/* series configuration */}
</SmithchartComponent>
```

Specify sizes in:
- Pixels: `'200px'`, `'100px'`
- Percentage: `'50%'`, `'25%'`

### Legend Padding

Control spacing within and around the legend.

#### itemPadding

Space between individual legend items:

```tsx
<SmithchartComponent
  id="smithchart"
  legendSettings={{
    visible: true,
    itemPadding: 15  // Pixels between legend items
  }}
>
  <Inject services={[SmithchartLegend]} />
  {/* series configuration */}
</SmithchartComponent>
```

#### shapePadding

Space between legend shape and text:

```tsx
<SmithchartComponent
  id="smithchart"
  legendSettings={{
    visible: true,
    shapePadding: 10  // Pixels between shape and text
  }}
>
  <Inject services={[SmithchartLegend]} />
  {/* series configuration */}
</SmithchartComponent>
```

## Toggle Visibility

The `toggleVisibility` property enables users to show/hide series by clicking legend items.

By default, this property is set to `true`, allowing interactive legend toggling.

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const data1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const data2 = [
    { resistance: 0.2, reactance: 0.1 },
    { resistance: 0.7, reactance: 0.4 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Click Legend Items to Toggle Series' }}
      legendSettings={{
        visible: true,
        toggleVisibility: true  // Enable clicking to show/hide series
      }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective name="50Ω Line" points={data1} fill="#3498db" />
        <SmithchartSeriesDirective name="75Ω Line" points={data2} fill="#e74c3c" />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

**To disable toggle functionality:**

```tsx
legendSettings={{
  visible: true,
  toggleVisibility: false
}}
```

## Complete Examples

### Fully Customized Legend

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const line1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.8, reactance: 0.4 }
  ];

  const line2 = [
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.1, reactance: 0.55 }
  ];

  const line3 = [
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Transmission Line Comparison' }}
      legendSettings={{
        visible: true,
        position: 'Bottom',
        alignment: 'Center',
        shape: 'Diamond',
        itemPadding: 20,
        shapePadding: 12,
        toggleVisibility: true
      }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="50Ω Coaxial Line"
          points={line1}
          fill="#3498db"
          width={2}
        />
        <SmithchartSeriesDirective
          name="75Ω Coaxial Line"
          points={line2}
          fill="#e74c3c"
          width={2}
        />
        <SmithchartSeriesDirective
          name="100Ω Twisted Pair"
          points={line3}
          fill="#2ecc71"
          width={2}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Legend with Custom Position

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const data1 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 }
  ];

  const data2 = [
    { resistance: 0.2, reactance: 0.1 },
    { resistance: 0.7, reactance: 0.4 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Custom Legend Position' }}
      legendSettings={{
        visible: true,
        position: 'Custom',
        x: 500,
        y: 50,
        width: '150px',
        height: '60px',
        shape: 'Rectangle',
        itemPadding: 10,
        shapePadding: 8
      }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective name="Measured" points={data1} fill="#9b59b6" />
        <SmithchartSeriesDirective name="Simulated" points={data2} fill="#f39c12" />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Compact Legend for Dashboards

```tsx
<SmithchartComponent
  id="smithchart"
  legendSettings={{
    visible: true,
    position: 'Right',
    alignment: 'Near',
    shape: 'Circle',
    width: '120px',
    itemPadding: 8,
    shapePadding: 6,
    toggleVisibility: true
  }}
>
  <Inject services={[SmithchartLegend]} />
  <SmithchartSeriesCollectionDirective>
    <SmithchartSeriesDirective name="Line A" points={dataA} fill="#1abc9c" />
    <SmithchartSeriesDirective name="Line B" points={dataB} fill="#e67e22" />
    <SmithchartSeriesDirective name="Line C" points={dataC} fill="#34495e" />
  </SmithchartSeriesCollectionDirective>
</SmithchartComponent>
```

### Presentation-Ready Legend

High-contrast, large text for presentations:

```tsx
<SmithchartComponent
  id="smithchart"
  title={{ text: 'RF Circuit Analysis', textStyle: { size: '18px', fontWeight: 'Bold' } }}
  legendSettings={{
    visible: true,
    position: 'Bottom',
    alignment: 'Center',
    shape: 'Rectangle',
    width: '500px',
    height: '100px',
    itemPadding: 25,
    shapePadding: 15,
    toggleVisibility: false  // Disable for presentations
  }}
>
  <Inject services={[SmithchartLegend]} />
  <SmithchartSeriesCollectionDirective>
    <SmithchartSeriesDirective name="Input Impedance" points={data1} fill="#2c3e50" width={3} />
    <SmithchartSeriesDirective name="Output Impedance" points={data2} fill="#c0392b" width={3} />
  </SmithchartSeriesCollectionDirective>
</SmithchartComponent>
```

## Best Practices

### Position Selection

**Bottom position (default):**
- Best for most use cases
- Doesn't obscure chart data
- Works well with horizontal aspect ratios

**Top position:**
- Use when bottom space is constrained
- Good for vertically-oriented layouts

**Left/Right positions:**
- Best for dashboards with limited vertical space
- Works well with wide aspect ratios
- Good for 3+ series with long names

**Custom position:**
- Use sparingly for special layouts
- Test across different screen sizes
- Ensure legend doesn't obscure critical data

### Alignment Guidelines

- **Center**: Default, works for most scenarios
- **Near**: Use when chart has right-side content or annotations
- **Far**: Use when chart has left-side content

### Shape Selection

- **Circle**: Universal, works for all series types
- **Rectangle**: Good for area/bar-style visualizations
- **Diamond/Triangle**: Use to match marker shapes in the series
- **Pentagon**: Distinctive, good for highlighting special series

### Size Recommendations

**Width:**
- Compact: 100-150px (few series, short names)
- Standard: 200-300px (typical use)
- Expanded: 400-500px (many series or long names)

**Height:**
- Compact: 40-60px (2-3 series)
- Standard: 80-100px (4-6 series)
- Expanded: 120-150px (7+ series)

### Padding Guidelines

**itemPadding:**
- Compact layouts: 8-12px
- Standard: 15-20px
- Presentation: 20-30px

**shapePadding:**
- Compact: 6-8px
- Standard: 10-12px
- Presentation: 12-18px

### Toggle Visibility

**Enable when:**
- Users need to compare subsets of series
- Chart has 3+ series that may overlap
- Interactive exploration is desired
- Dashboard allows user customization

**Disable when:**
- All series must always be visible
- Creating static reports or presentations
- Users shouldn't modify visualization
- Series are critical for interpretation

## Common Patterns

### Dynamic Legend Position

Switch legend position based on screen size or user preference:

```tsx
import * as React from "react";
import { SmithchartComponent, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const [legendPos, setLegendPos] = React.useState('Bottom');

  return (
    <>
      <select value={legendPos} onChange={(e) => setLegendPos(e.target.value)}>
        <option value="Top">Top</option>
        <option value="Bottom">Bottom</option>
        <option value="Left">Left</option>
        <option value="Right">Right</option>
      </select>

      <SmithchartComponent
        id="smithchart"
        legendSettings={{
          visible: true,
          position: legendPos
        }}
      >
        <Inject services={[SmithchartLegend]} />
        {/* series configuration */}
      </SmithchartComponent>
    </>
  );
}
```

### Conditional Legend Visibility

Show legend only when multiple series are present:

```tsx
function App() {
  const seriesData = [/* array of series data */];
  const showLegend = seriesData.length > 1;

  return (
    <SmithchartComponent
      id="smithchart"
      legendSettings={{
        visible: showLegend
      }}
    >
      <Inject services={[SmithchartLegend]} />
      {/* series configuration */}
    </SmithchartComponent>
  );
}
```

### Series Name Formatting

Use descriptive, concise names:

```tsx
// Good: Descriptive and concise
<SmithchartSeriesDirective name="50Ω @ 2.4GHz" points={data1} />
<SmithchartSeriesDirective name="75Ω @ 2.4GHz" points={data2} />

// Avoid: Too verbose
<SmithchartSeriesDirective name="Transmission Line with 50 Ohm Impedance at 2.4 Gigahertz" points={data1} />

// Avoid: Too vague
<SmithchartSeriesDirective name="Line 1" points={data1} />
```

This comprehensive guide covers all aspects of legend configuration in Smith Charts, enabling you to create clear, informative visualizations with effective series identification.
