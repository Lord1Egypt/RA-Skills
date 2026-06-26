# Axis Configuration

## Table of contents
- [Overview](axis-configuration.md#overview)
- [Axis Types](axis-configuration.md#axis-types)
  - [Horizontal Axis](axis-configuration.md#horizontal-axis)
  - [Radial Axis](axis-configuration.md#radial-axis)
- [Label Customization](axis-configuration.md#label-customization)
  - [Label Position](axis-configuration.md#label-position)
  - [Label Intersection Action](axis-configuration.md#label-intersection-action)
  - [Label Style](axis-configuration.md#label-style)
- [Gridlines Configuration](axis-configuration.md#gridlines-configuration)
  - [Major Gridlines](axis-configuration.md#major-gridlines)
  - [Minor Gridlines](axis-configuration.md#minor-gridlines)
  - [Gridline Dash Patterns](axis-configuration.md#gridline-dash-patterns)
- [Axis Line Customization](axis-configuration.md#axis-line-customization)
  - [Axis Line Properties](axis-configuration.md#axis-line-properties)
  - [Hiding Axis Lines](axis-configuration.md#hiding-axis-lines)
- [Complete Examples](axis-configuration.md#complete-examples)
  - [Fully Customized Axes](axis-configuration.md#fully-customized-axes)
  - [Minimal Gridlines Configuration](axis-configuration.md#minimal-gridlines-configuration)
  - [High-Contrast Configuration](axis-configuration.md#high-contrast-configuration)
  - [Subtle Grid for Focus on Data](axis-configuration.md#subtle-grid-for-focus-on-data)
- [Best Practices](axis-configuration.md#best-practices)
  - [Label Configuration](axis-configuration.md#label-configuration)
  - [Gridlines](axis-configuration.md#gridlines)
  - [Axis Lines](axis-configuration.md#axis-lines)
  - [Visual Hierarchy](axis-configuration.md#visual-hierarchy)
- [Common Use Cases](axis-configuration.md#common-use-cases)
  - [Technical Documentation](axis-configuration.md#technical-documentation)
  - [Interactive Dashboards](axis-configuration.md#interactive-dashboards)
  - [Printed Reports](axis-configuration.md#printed-reports)

## Overview

Smith Charts support two types of axes for plotting impedance data:

1. **Horizontal Axis**: Drawn as a straight line in the horizontal direction
2. **Radial Axis**: Drawn as a circular path

Both axes can be extensively customized to improve readability and match your application's design requirements.

## Axis Types

### Horizontal Axis

The horizontal axis represents the real component of impedance and extends horizontally across the Smith Chart. It uses straight lines for major and minor gridlines.

```tsx
import { SmithchartComponent } from '@syncfusion/ej2-react-charts';

<SmithchartComponent
  id="smithchart"
  horizontalAxis={{
    // Horizontal axis configuration
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

### Radial Axis

The radial axis represents the imaginary component of impedance and is drawn as circular arcs around the Smith Chart.

```tsx
<SmithchartComponent
  id="smithchart"
  radialAxis={{
    // Radial axis configuration
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

## Label Customization

Axis labels denote the intervals and values along the axes, helping users identify data points accurately. Both horizontal and radial axes support comprehensive label customization.

### Label Position

The `labelPosition` property determines whether labels appear inside or outside the axis line.

**Available values:**
- `'Inside'` - Labels appear within the chart area
- `'Outside'` - Labels appear outside the axis line (default)

```tsx
import * as React from "react";
import { SmithchartComponent, SeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      horizontalAxis={{
        labelPosition: 'Inside'
      }}
      radialAxis={{
        labelPosition: 'Outside'
      }}
    >
      <SmithChartSeriesCollectionDirective>
        <SmithChartSeriesDirective points={data} />
      </SeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Label Intersection Action

The `labelIntersectAction` property controls how labels behave when they overlap with other labels.

**Available values:**
- `'None'` - No action taken (default)
- `'Hide'` - Hides overlapping labels

```tsx
<SmithchartComponent
  id="smithchart"
  horizontalAxis={{
    labelIntersectAction: 'Hide'
  }}
  radialAxis={{
    labelIntersectAction: 'Hide'
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

### Label Style

Customize label font properties using the `labelStyle` object.

**Available properties:**
- `size` - Font size (e.g., '12px', '14px')
- `fontFamily` - Font family (e.g., 'Arial', 'Roboto')
- `fontWeight` - Font weight (e.g., 'Normal', 'Bold')
- `opacity` - Label opacity (0 to 1)
- `color` - Label text color

```tsx
<SmithchartComponent
  id="smithchart"
  horizontalAxis={{
    labelStyle: {
      size: '14px',
      fontFamily: 'Arial',
      fontWeight: 'Bold',
      fontStyle: 'Italic',
      color: '#333333',
      opacity: 1
    }
  }}
  radialAxis={{
    labelStyle: {
      size: '12px',
      fontFamily: 'Roboto',
      fontWeight: 'Normal',
      fontStyle: 'Italic',
      color: '#666666',
      opacity: 0.9
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

## Gridlines Configuration

Gridlines extend from the axes across the plot area, making it easier to read data values. Both horizontal and radial axes support major and minor gridlines.

### Major Gridlines

Major gridlines are drawn at positions where labels are rendered. They provide primary reference lines for reading values.

**Available properties:**
- `width` - Line width in pixels
- `dashArray` - Dash pattern (e.g., '5,5' for dashed line)
- `visible` - Show or hide gridlines (boolean)
- `opacity` - Gridline opacity (0 to 1)

```tsx
import * as React from "react";
import { SmithchartComponent, SeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      horizontalAxis={{
        majorGridLines: {
          visible: true,
          width: 1,
          dashArray: '0',
          opacity: 0.8
        }
      }}
      radialAxis={{
        majorGridLines: {
          visible: true,
          width: 1,
          dashArray: '0',
          opacity: 0.8
        }
      }}
    >
      <SmithChartSeriesCollectionDirective>
        <SmithChartSeriesDirective points={data} />
      </SeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Minor Gridlines

Minor gridlines are drawn between two major gridlines, providing additional reference points.

**Available properties:**
- `width` - Line width in pixels
- `dashArray` - Dash pattern
- `visible` - Show or hide gridlines (boolean)
- `opacity` - Gridline opacity (0 to 1)
- `count` - Number of minor gridlines between major gridlines

```tsx
<SmithchartComponent
  id="smithchart"
  horizontalAxis={{
    minorGridLines: {
      visible: true,
      width: 0.5,
      dashArray: '3,3',
      opacity: 0.5,
      count: 2
    }
  }}
  radialAxis={{
    minorGridLines: {
      visible: true,
      width: 0.5,
      dashArray: '3,3',
      opacity: 0.5,
      count: 2
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

### Gridline Dash Patterns

The `dashArray` property uses a comma-separated string to define dash and gap lengths.

**Common patterns:**
- `'0'` or `''` - Solid line
- `'5,5'` - 5px dash, 5px gap
- `'10,5'` - 10px dash, 5px gap
- `'3,3,10,3'` - Complex pattern with varying dash/gap lengths

```tsx
<SmithchartComponent
  id="smithchart"
  horizontalAxis={{
    majorGridLines: {
      visible: true,
      dashArray: '5,5'  // Dashed line
    },
    minorGridLines: {
      visible: true,
      dashArray: '2,2'  // Short dashes
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

## Axis Line Customization

The axis line is the main line that defines the axis itself. You can customize its appearance or hide it entirely.

### Axis Line Properties

**Available properties:**
- `width` - Line width in pixels
- `dashArray` - Dash pattern
- `visible` - Show or hide the axis line (boolean, default: true)

```tsx
import * as React from "react";
import { SmithchartComponent, SeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      horizontalAxis={{
        axisLine: {
          visible: true,
          width: 2,
          dashArray: '0'
        }
      }}
      radialAxis={{
        axisLine: {
          visible: true,
          width: 2,
          dashArray: '0'
        }
      }}
    >
    <SmithChartSeriesCollectionDirective>
      <SmithChartSeriesDirective
          points={data}
      />
    </SeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Hiding Axis Lines

You can hide axis lines while keeping gridlines and labels visible:

```tsx
<SmithchartComponent
  id="smithchart"
  horizontalAxis={{
    axisLine: {
      visible: false
    },
    majorGridLines: {
      visible: true
    }
  }}
  radialAxis={{
    axisLine: {
      visible: false
    },
    majorGridLines: {
      visible: true
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

## Complete Examples

### Fully Customized Axes

```tsx
import * as React from "react";
import { SmithchartComponent, SeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
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
      title={{ text: 'Custom Axis Configuration' }}
      horizontalAxis={{
        labelPosition: 'Outside',
        labelIntersectAction: 'Hide',
        labelStyle: {
          size: '12px',
          fontFamily: 'Arial',
          fontWeight: 'Bold',
          color: '#2c3e50',
          opacity: 1
        },
        majorGridLines: {
          visible: true,
          width: 1.5,
          dashArray: '0',
          opacity: 0.7
        },
        minorGridLines: {
          visible: true,
          width: 0.75,
          dashArray: '5,5',
          opacity: 0.4,
          count: 3
        },
        axisLine: {
          visible: true,
          width: 2,
          dashArray: '0'
        }
      }}
      radialAxis={{
        labelPosition: 'Outside',
        labelIntersectAction: 'Hide',
        labelStyle: {
          size: '12px',
          fontFamily: 'Arial',
          fontWeight: 'Normal',
          color: '#34495e',
          opacity: 0.9
        },
        majorGridLines: {
          visible: true,
          width: 1.5,
          dashArray: '0',
          opacity: 0.7
        },
        minorGridLines: {
          visible: true,
          width: 0.75,
          dashArray: '5,5',
          opacity: 0.4,
          count: 3
        },
        axisLine: {
          visible: true,
          width: 2,
          dashArray: '0'
        }
      }}
    >
      <SmithChartSeriesCollectionDirective>
        <SmithChartSeriesDirective
          points={transmissionData}
          fill="#3498db"
          width={2}
        />
      </SeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Minimal Gridlines Configuration

For a cleaner look with fewer visual elements:

```tsx
import * as React from "react";
import { SmithchartComponent, SeriesDirective, SeriesCollectionDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Minimal Gridlines' }}
      horizontalAxis={{
        majorGridLines: {
          visible: true,
          width: 1,
          opacity: 0.5
        },
        minorGridLines: {
          visible: false
        },
        axisLine: {
          visible: true,
          width: 2
        }
      }}
      radialAxis={{
        majorGridLines: {
          visible: true,
          width: 1,
          opacity: 0.5
        },
        minorGridLines: {
          visible: false
        },
        axisLine: {
          visible: true,
          width: 2
        }
      }}
    >
      <SmithChartSeriesCollectionDirective>
        <SmithChartSeriesDirective points={data} />
      </SeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### High-Contrast Configuration

For better visibility in presentations or printed materials:

```tsx
<SmithchartComponent
  id="smithchart"
  title={{ text: 'High Contrast Axes' }}
  horizontalAxis={{
    labelStyle: {
      size: '14px',
      fontWeight: 'Bold',
      color: '#000000'
    },
    majorGridLines: {
      visible: true,
      width: 2,
      opacity: 1
    },
    minorGridLines: {
      visible: true,
      width: 1,
      opacity: 0.6,
      count: 1
    },
    axisLine: {
      visible: true,
      width: 3
    }
  }}
  radialAxis={{
    labelStyle: {
      size: '14px',
      fontWeight: 'Bold',
      color: '#000000'
    },
    majorGridLines: {
      visible: true,
      width: 2,
      opacity: 1
    },
    minorGridLines: {
      visible: true,
      width: 1,
      opacity: 0.6,
      count: 1
    },
    axisLine: {
      visible: true,
      width: 3
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

### Subtle Grid for Focus on Data

Emphasize data by making gridlines less prominent:

```tsx
<SmithchartComponent
  id="smithchart"
  title={{ text: 'Data-Focused Layout' }}
  horizontalAxis={{
    labelStyle: {
      size: '11px',
      color: '#95a5a6',
      opacity: 0.8
    },
    majorGridLines: {
      visible: true,
      width: 0.5,
      dashArray: '3,3',
      opacity: 0.3
    },
    minorGridLines: {
      visible: false
    },
    axisLine: {
      visible: true,
      width: 1,
      dashArray: '0'
    }
  }}
  radialAxis={{
    labelStyle: {
      size: '11px',
      color: '#95a5a6',
      opacity: 0.8
    },
    majorGridLines: {
      visible: true,
      width: 0.5,
      dashArray: '3,3',
      opacity: 0.3
    },
    minorGridLines: {
      visible: false
    },
    axisLine: {
      visible: true,
      width: 1,
      dashArray: '0'
    }
  }}
>
  {/* series configuration */}
</SmithchartComponent>
```

## Best Practices

### Label Configuration
- Use `labelIntersectAction: 'Hide'` when labels overlap
- Choose `labelPosition` based on chart layout needs
- Keep label font sizes readable (12px-14px recommended)
- Use contrasting label colors for better visibility

### Gridlines
- Enable major gridlines for primary reference points
- Use minor gridlines sparingly (count: 1-3) to avoid clutter
- Apply lighter opacity to minor gridlines (0.3-0.5)
- Use dashed patterns for minor gridlines to differentiate from major ones

### Axis Lines
- Keep axis lines visible for chart structure clarity
- Use solid lines (dashArray: '0') for axis lines
- Increase width (2-3px) for emphasis if needed
- Hide axis lines only when gridlines provide sufficient context

### Visual Hierarchy
- Major gridlines: Higher opacity (0.7-1.0), solid or subtle dash
- Minor gridlines: Lower opacity (0.3-0.5), dashed
- Axis lines: Highest contrast and width
- Labels: Clear, readable font with appropriate size

### Accessibility
- Ensure sufficient color contrast for labels and gridlines
- Avoid relying solely on color to convey information
- Use adequate line widths for visibility
- Test readability at different zoom levels

### Performance
- Limit minor gridline count (1-3) to reduce rendering complexity
- Hide unused elements (set visible: false) rather than using opacity: 0
- Use simpler dash patterns for better performance

## Common Use Cases

### Technical Documentation

Use high-contrast, clear gridlines with bold labels:

```tsx
horizontalAxis={{
  labelStyle: { size: '13px', fontWeight: 'Bold' },
  majorGridLines: { visible: true, width: 1.5 },
  minorGridLines: { visible: true, count: 2 }
}}
```

### Interactive Dashboards

Use subtle gridlines to focus on data interaction:

```tsx
horizontalAxis={{
  labelStyle: { size: '11px', opacity: 0.7 },
  majorGridLines: { visible: true, opacity: 0.4 },
  minorGridLines: { visible: false }
}}
```

### Printed Reports

Maximize contrast and clarity:

```tsx
horizontalAxis={{
  labelStyle: { size: '14px', color: '#000000', fontWeight: 'Bold' },
  majorGridLines: { visible: true, width: 2, opacity: 1 },
  axisLine: { visible: true, width: 3 }
}}
```

This comprehensive guide provides all the information needed to configure Smith Chart axes for optimal data visualization and user experience.
